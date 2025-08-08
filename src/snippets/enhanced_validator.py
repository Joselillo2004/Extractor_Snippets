"""
Enhanced Validator - Integración del Context Analyzer con validador existente

Este módulo extiende el validador actual con capacidades LLM:
1. Mantiene validación heurística como base (Fase 2)
2. Añade análisis contextual LLM para snippets fallidos
3. Construye contexto automáticamente y re-valida
4. Fallback graceful si LLM falla
"""

import logging
import time
import asyncio
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .validator import validate, ValidationResult
from .agents import ContextAnalyzer, Snippet, get_llm_client, LLMConfig

logger = logging.getLogger(__name__)


@dataclass 
class EnhancedValidationResult:
    """Resultado de validación mejorada con información de agentes LLM"""
    
    # Resultado base (heurístico)
    base_result: ValidationResult
    
    # Resultado mejorado con LLM (si aplica)
    enhanced_result: Optional[ValidationResult] = None
    
    # Información del análisis LLM
    llm_analysis_used: bool = False
    llm_analysis_success: bool = False
    context_added: bool = False
    processing_time: float = 0.0
    
    # Contexto construido (si aplica)
    context_code: Optional[str] = None
    dependencies_found: Dict[str, Any] = None
    
    # Metadata
    confidence: float = 0.0
    error_message: Optional[str] = None
    
    @property
    def final_result(self) -> ValidationResult:
        """Retorna el mejor resultado disponible"""
        return self.enhanced_result or self.base_result
    
    @property
    def success_improved(self) -> bool:
        """True si LLM mejoró el resultado"""
        return (self.enhanced_result is not None and 
                self.base_result.status != 'ok' and 
                self.enhanced_result.status == 'ok')


class EnhancedValidator:
    """
    Validador mejorado que integra Context Analyzer
    
    Flujo de procesamiento:
    1. Validación heurística normal (Fase 2)
    2. Si falla y use_agents=True: análisis contextual LLM
    3. Construir contexto y re-validar
    4. Retornar mejor resultado disponible
    """
    
    def __init__(self, 
                 enable_agents: bool = True,
                 llm_config: Optional[LLMConfig] = None,
                 window_size: int = 20):
        """
        Initialize enhanced validator
        
        Args:
            enable_agents: Si usar agentes LLM
            llm_config: Configuración LLM opcional
            window_size: Ventana de análisis contextual
        """
        self.enable_agents = enable_agents
        self.window_size = window_size
        
        # Contadores para estadísticas
        self.stats = {
            'total_validations': 0,
            'llm_analyses': 0,
            'llm_improvements': 0,
            'fallbacks_used': 0,
            'processing_time': 0.0
        }
        
        if self.enable_agents:
            try:
                # Configurar cliente LLM con límites apropiados
                if llm_config is None:
                    llm_config = LLMConfig(
                        model="llama-3.1-70b-versatile",
                        temperature=0.1,
                        max_tokens=800,
                        max_cost_per_session=5.0,
                        cache_enabled=True
                    )
                
                self.llm_client = get_llm_client(llm_config)
                self.context_analyzer = ContextAnalyzer(
                    self.llm_client, 
                    window_size=window_size
                )
                
                logger.info(f"Enhanced validator initialized with LLM agents (window_size={window_size})")
                
            except Exception as e:
                logger.warning(f"Failed to initialize LLM agents: {e}")
                self.enable_agents = False
        
        if not self.enable_agents:
            logger.info("Enhanced validator running in heuristic-only mode")
    
    async def validate_single(self,
                             snippet_content: str,
                             snippet_index: int,
                             all_snippets: Optional[List[str]] = None,
                             **kwargs) -> EnhancedValidationResult:
        """
        Valida un snippet individual con análisis contextual opcional
        
        Args:
            snippet_content: Contenido del snippet
            snippet_index: Índice del snippet
            all_snippets: Lista completa de snippets para contexto
            **kwargs: Argumentos adicionales (timeout_sec, normalize, etc.)
            
        Returns:
            EnhancedValidationResult con resultados
        """
        start_time = time.time()
        self.stats['total_validations'] += 1
        
        # Paso 1: Validación heurística base (Fase 2)
        base_result = validate(
            snippet_content, 
            timeout_sec=kwargs.get('timeout_sec', 3.0),
            normalize=kwargs.get('normalize', True)
        )
        
        # Preparar resultado inicial
        enhanced_result = EnhancedValidationResult(
            base_result=base_result,
            processing_time=time.time() - start_time
        )
        
        # Paso 2: Si el resultado base es exitoso o no hay agentes, retornar
        if (base_result.status == 'ok' or 
            not self.enable_agents or
            all_snippets is None):
            return enhanced_result
        
        # Paso 3: Análisis contextual LLM para snippets fallidos
        try:
            self.stats['llm_analyses'] += 1
            enhanced_result.llm_analysis_used = True  # Marcar como usado ANTES del análisis
            
            # Convertir snippets a formato Snippet
            snippet_objects = [
                Snippet(content=content, index=i) 
                for i, content in enumerate(all_snippets)
            ]
            
            current_snippet = snippet_objects[snippet_index]
            
            # Analizar dependencias contextualmente
            llm_start = time.time()
            analysis_result = await self.context_analyzer.analyze(
                snippet=current_snippet,
                all_snippets=snippet_objects,
                snippet_index=snippet_index,
                **kwargs
            )
            llm_time = time.time() - llm_start
            
            # Actualizar resultado con info de análisis LLM
            enhanced_result.llm_analysis_success = analysis_result.success
            enhanced_result.confidence = analysis_result.confidence
            enhanced_result.dependencies_found = analysis_result.data
            
            if analysis_result.success and analysis_result.confidence > 0.5:
                # Paso 4: Construir contexto basado en dependencias
                context_code = self._build_context_from_dependencies(
                    analysis_result.data, snippet_objects
                )
                
                if context_code:
                    # Paso 5: Re-validar con contexto añadido
                    enhanced_snippet = context_code + "\n\n" + snippet_content
                    
                    enhanced_validation = validate(
                        enhanced_snippet,
                        timeout_sec=kwargs.get('timeout_sec', 3.0),
                        normalize=False  # Ya normalizado
                    )
                    
                    enhanced_result.enhanced_result = enhanced_validation
                    enhanced_result.context_added = True
                    enhanced_result.context_code = context_code
                    
                    # Actualizar estadísticas si mejoró
                    if enhanced_result.success_improved:
                        self.stats['llm_improvements'] += 1
                        logger.info(f"LLM improved snippet {snippet_index}: {base_result.status} -> {enhanced_validation.status}")
            
        except Exception as e:
            logger.warning(f"LLM analysis failed for snippet {snippet_index}: {e}")
            enhanced_result.error_message = str(e)
            self.stats['fallbacks_used'] += 1
        
        # Actualizar tiempo total
        enhanced_result.processing_time = time.time() - start_time
        self.stats['processing_time'] += enhanced_result.processing_time
        
        return enhanced_result
    
    def _build_context_from_dependencies(self,
                                       dependencies: Dict[str, Any],
                                       all_snippets: List[Snippet]) -> Optional[str]:
        """
        Construye código de contexto basado en dependencias encontradas
        
        Args:
            dependencies: Dependencias encontradas por Context Analyzer
            all_snippets: Lista completa de snippets
            
        Returns:
            Código de contexto construido o None
        """
        context_lines = []
        
        try:
            # Añadir imports necesarios
            if 'imports' in dependencies:
                for import_name, import_info in dependencies['imports'].items():
                    snippet_idx = import_info.get('defined_in_snippet')
                    if snippet_idx is not None and snippet_idx < len(all_snippets):
                        import_statement = import_info.get('import_statement', '')
                        if import_statement:
                            context_lines.append(import_statement)
            
            # Añadir definiciones de funciones
            if 'functions' in dependencies:
                for func_name, func_info in dependencies['functions'].items():
                    snippet_idx = func_info.get('defined_in_snippet')
                    if snippet_idx is not None and snippet_idx < len(all_snippets):
                        func_definition = func_info.get('definition', '')
                        if func_definition:
                            context_lines.append(func_definition)
            
            # Añadir definiciones de clases
            if 'classes' in dependencies:
                for class_name, class_info in dependencies['classes'].items():
                    snippet_idx = class_info.get('defined_in_snippet')
                    if snippet_idx is not None and snippet_idx < len(all_snippets):
                        class_definition = class_info.get('definition', '')
                        if class_definition:
                            context_lines.append(class_definition)
            
            # Añadir definiciones de variables
            if 'variables' in dependencies:
                for var_name, var_info in dependencies['variables'].items():
                    snippet_idx = var_info.get('defined_in_snippet')
                    if snippet_idx is not None and snippet_idx < len(all_snippets):
                        var_definition = var_info.get('definition', '')
                        if var_definition:
                            context_lines.append(var_definition)
            
            if context_lines:
                return '\n'.join(context_lines)
                
        except Exception as e:
            logger.error(f"Error building context: {e}")
        
        return None
    
    async def validate_batch(self,
                            snippets: List[str],
                            **kwargs) -> List[EnhancedValidationResult]:
        """
        Valida una lista de snippets con análisis contextual
        
        Args:
            snippets: Lista de contenidos de snippets
            **kwargs: Argumentos de validación
            
        Returns:
            Lista de EnhancedValidationResult
        """
        results = []
        
        for i, snippet_content in enumerate(snippets):
            result = await self.validate_single(
                snippet_content=snippet_content,
                snippet_index=i,
                all_snippets=snippets,
                **kwargs
            )
            results.append(result)
        
        return results
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del validador mejorado
        
        Returns:
            Diccionario con estadísticas
        """
        stats = self.stats.copy()
        
        # Añadir métricas calculadas
        if stats['total_validations'] > 0:
            stats['llm_usage_rate'] = stats['llm_analyses'] / stats['total_validations']
            stats['improvement_rate'] = stats['llm_improvements'] / stats['total_validations']
            stats['avg_processing_time'] = stats['processing_time'] / stats['total_validations']
        else:
            stats['llm_usage_rate'] = 0.0
            stats['improvement_rate'] = 0.0
            stats['avg_processing_time'] = 0.0
        
        # Añadir info de configuración
        stats['agents_enabled'] = self.enable_agents
        stats['window_size'] = self.window_size
        
        if hasattr(self, 'llm_client'):
            stats['llm_stats'] = self.llm_client.get_session_stats()
        
        return stats
    
    def reset_stats(self) -> None:
        """Resetea las estadísticas"""
        self.stats = {
            'total_validations': 0,
            'llm_analyses': 0,
            'llm_improvements': 0,
            'fallbacks_used': 0,
            'processing_time': 0.0
        }
        
        if hasattr(self, 'llm_client'):
            self.llm_client.reset_session_stats()


# Factory function para crear validador configurado
def create_enhanced_validator(**kwargs) -> EnhancedValidator:
    """
    Factory para crear validador mejorado con configuración
    
    Returns:
        EnhancedValidator configurado
    """
    return EnhancedValidator(**kwargs)

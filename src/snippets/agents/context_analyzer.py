"""
Context Analyzer Agent - Análisis contextual de dependencias usando LLM

Responsabilidades:
1. Analizar snippet objetivo en contexto de snippets circundantes
2. Identificar dependencias: variables, clases, imports, funciones
3. Generar mapa de dependencias estructurado con confianza
4. Manejar ventana dinámica de análisis (±N snippets)
"""

import json
import ast
import re
import time
from typing import List, Dict, Any, Optional
from pathlib import Path

from .base_agent import BaseAgent, Snippet, AgentResult, DependencyMap
from .llm_client import get_llm_client, LLMConfig

import logging
logger = logging.getLogger(__name__)


class ContextAnalyzer(BaseAgent):
    """
    Agent especializado en análisis contextual de dependencias
    """
    
    def __init__(self, llm_client=None, window_size: int = 20):
        """
        Initialize Context Analyzer
        
        Args:
            llm_client: Cliente LLM configurado
            window_size: Tamaño de ventana de análisis (±N snippets)
        """
        if llm_client is None:
            llm_client = get_llm_client()
        
        super().__init__(
            llm_client=llm_client,
            agent_name="ContextAnalyzer",
            max_retries=3,
            timeout_seconds=30.0
        )
        
        self.window_size = window_size
        self.prompt_template = self._load_prompt_template()
        
        logger.info(f"ContextAnalyzer initialized with window_size={window_size}")
    
    def _load_prompt_template(self) -> str:
        """
        Carga el template de prompt desde archivo
        
        Returns:
            Template de prompt como string
        """
        template_path = Path(__file__).parent / "prompt_templates" / "context_analysis.txt"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            # Fallback template simple
        return """Analyze this Python snippet for dependencies: {target_snippet}
Context: {context_snippets}
Return JSON with variables, classes, imports, functions."""
    
    def _calculate_window_indices(self, target_index: int, total_snippets: int, window_size: int) -> List[int]:
        """
        Calcula los índices de la ventana de contexto
        
        Args:
            target_index: Índice del snippet objetivo
            total_snippets: Número total de snippets
            window_size: Tamaño de la ventana (± snippets)
            
        Returns:
            Lista de índices válidos en la ventana
        """
        # Calcular rango de la ventana
        window_start = max(0, target_index - window_size)
        window_end = min(total_snippets, target_index + window_size + 1)
        
        # Generar lista de índices
        indices = list(range(window_start, window_end))
        
        return indices
    
    def _extract_context_snippets(self, 
                                 all_snippets: List[Snippet],
                                 target_index: int) -> List[Dict[str, Any]]:
        """
        Extrae snippets del contexto según window_size
        
        Args:
            all_snippets: Lista completa de snippets
            target_index: Índice del snippet objetivo
            
        Returns:
            Lista de snippets del contexto con metadata
        """
        # Calcular índices de la ventana
        window_indices = self._calculate_window_indices(
            target_index, len(all_snippets), self.window_size
        )
        
        context_snippets = []
        for idx in window_indices:
            snippet = all_snippets[idx]
            relative_pos = idx - target_index
            
            context_snippets.append({
                "index": idx,
                "content": snippet.content,
                "relative_position": relative_pos,
                "is_target": idx == target_index
            })
        
        return context_snippets
    
    def _format_context_for_llm(self, context_snippets: List[Dict[str, Any]]) -> str:
        """
        Formatea los snippets de contexto para el prompt del LLM
        
        Args:
            context_snippets: Lista de snippets con metadata
            
        Returns:
            String formateado para el prompt
        """
        formatted_lines = []
        
        for snippet_data in context_snippets:
            idx = snippet_data["index"]
            content = snippet_data["content"].strip()
            relative_pos = snippet_data["relative_position"]
            is_target = snippet_data["is_target"]
            
            marker = ">>> TARGET <<<" if is_target else f"({relative_pos:+d})"
            
            formatted_lines.append(f"## Snippet {idx} {marker}")
            formatted_lines.append(f"```python")
            formatted_lines.append(content)
            formatted_lines.append(f"```")
            formatted_lines.append("")
        
        return "\n".join(formatted_lines)
    
    def _parse_llm_response(self, llm_content: str) -> DependencyMap:
        """
        Parsea la respuesta JSON del LLM y crea DependencyMap
        
        Args:
            llm_content: Contenido de la respuesta del LLM
            
        Returns:
            DependencyMap estructurado
        """
        try:
            # Intentar extraer JSON de la respuesta con múltiples patrones
            json_str = None
            
            # Patrón 1: Bloque json con backticks
            json_match = re.search(r'```json\s*({.*?})\s*```', llm_content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                # Patrón 2: Bloque de código sin especificar idioma
                json_match = re.search(r'```\s*({.*?})\s*```', llm_content, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                else:
                    # Patrón 3: Buscar objeto JSON directamente
                    json_match = re.search(r'({\s*".*?})(?=\s*$)', llm_content, re.DOTALL | re.MULTILINE)
                    if json_match:
                        json_str = json_match.group(1)
                    else:
                        # Patrón 4: Toda la respuesta como JSON (limpiando posible texto extra)
                        json_str = llm_content.strip()
                        # Intentar encontrar el primer { hasta el último }
                        start = json_str.find('{')
                        end = json_str.rfind('}')
                        if start != -1 and end != -1 and end > start:
                            json_str = json_str[start:end+1]
            
            if not json_str:
                logger.error("No JSON found in LLM response")
                logger.debug(f"Raw content: {llm_content[:200]}...")
                return DependencyMap(confidence=0.0, error="No JSON found in response")
            
            # Parsear JSON con limpieza adicional
            json_str = json_str.strip()
            parsed = json.loads(json_str)
            
            # Crear DependencyMap con validación
            return DependencyMap(
                variables=parsed.get("variables", {}),
                classes=parsed.get("classes", {}),
                imports=parsed.get("imports", {}),
                functions=parsed.get("functions", {}),
                confidence=parsed.get("overall_confidence", 0.5)
            )
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse LLM JSON response: {e}")
            logger.debug(f"Raw LLM content: {llm_content[:300]}...")
            logger.debug(f"Attempted JSON string: {json_str[:200] if json_str else 'None'}...")
            return DependencyMap(confidence=0.0, error=f"JSON parsing failed: {str(e)}")
        
        except Exception as e:
            logger.error(f"Error processing LLM response: {e}")
            return DependencyMap(confidence=0.0, error=str(e))
    
    def _analyze_with_ast_fallback(self, snippet: Snippet) -> DependencyMap:
        """
        Análisis de fallback usando AST cuando el LLM falla
        
        Args:
            snippet: Snippet a analizar
            
        Returns:
            DependencyMap básico usando análisis AST
        """
        try:
            # Parsear el snippet con AST
            tree = ast.parse(snippet.content)
            
            # Extraer nombres usados pero no definidos (aproximación básica)
            used_names = set()
            defined_names = set()
            
            for node in ast.walk(tree):
                # Nombres usados
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                    used_names.add(node.id)
                # Nombres definidos
                elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    defined_names.add(node.id)
                elif isinstance(node, ast.FunctionDef):
                    defined_names.add(node.name)
                elif isinstance(node, ast.ClassDef):
                    defined_names.add(node.name)
            
            # Variables potencialmente indefinidas
            undefined_vars = used_names - defined_names - set(['print', 'len', 'range', 'str', 'int', 'float', 'list', 'dict'])
            
            variables = {}
            for var in undefined_vars:
                variables[var] = {
                    "defined_in_snippet": None,
                    "definition": f"# Unknown definition for: {var}",
                    "type": "unknown",
                    "confidence": 0.3  # Baja confianza para análisis AST
                }
            
            return DependencyMap(
                variables=variables,
                classes={},
                imports={},
                functions={},
                confidence=0.3,  # Baja confianza para fallback
                error="LLM failed, using AST fallback"
            )
            
        except Exception as e:
            logger.error(f"AST fallback failed: {e}")
            return DependencyMap(
                confidence=0.0,
                error="Both LLM and AST analysis failed"
            )
    
    async def analyze(self,
                     snippet: Snippet,
                     all_snippets: List[Snippet], 
                     snippet_index: int,
                     **kwargs) -> AgentResult:
        """
        Analiza dependencies del snippet usando contexto circundante
        
        Args:
            snippet: Snippet objetivo a analizar
            all_snippets: Lista completa de snippets
            snippet_index: Índice del snippet objetivo
            **kwargs: Argumentos adicionales (window_size override, etc.)
            
        Returns:
            AgentResult con DependencyMap
        """
        self.logger.info("Starting context analysis")
        start_time = time.time()
        
        try:
            # Validar entradas
            self._validate_inputs(snippet, all_snippets, snippet_index)
            
            # Override window_size si se proporciona
            current_window_size = kwargs.get('window_size', self.window_size)
            
            # Extraer contexto
            context_snippets = self._extract_context_snippets(
                all_snippets, snippet_index
            )
            
            # Formatear para LLM
            formatted_context = self._format_context_for_llm(context_snippets)
            
            # Preparar prompt
            prompt = self.prompt_template.format(
                target_snippet=snippet.content,
                context_snippets=formatted_context
            )
            
            try:
                # Ejecutar análisis LLM con timeout y retry
                llm_analysis = await self._with_timeout_and_retry(
                    self.llm_client.generate(
                        prompt=prompt,
                        system_message="You are an expert Python code analyzer focused on dependency detection."
                    )
                )
                
                # Parsear respuesta
                dependency_map = self._parse_llm_response(llm_analysis.content)
                dependency_map.processing_time = llm_analysis.processing_time
                
                if dependency_map.confidence > 0.5:
                    # Análisis exitoso
                    return AgentResult(
                        success=True,
                        data=dependency_map.dict(),
                        confidence=dependency_map.confidence,
                        processing_time=llm_analysis.processing_time,
                        metadata={
                            'window_size': current_window_size,
                            'context_snippets': len(context_snippets),
                            'llm_usage': llm_analysis.usage.dict(),
                            'cached': llm_analysis.cached
                        }
                    )
                else:
                    # Baja confianza, usar fallback
                    raise Exception("Low confidence LLM analysis, using fallback")
            
            except Exception as llm_error:
                logger.warning(f"LLM analysis failed: {llm_error}, using AST fallback")
                
                # Fallback a análisis AST
                dependency_map = self._analyze_with_ast_fallback(snippet)
                
                return AgentResult(
                    success=True,  # Exitoso aunque sea fallback
                    data=dependency_map.dict(),
                    confidence=dependency_map.confidence,
                    processing_time=0.0,
                    error=f"LLM failed: {llm_error}",
                    metadata={
                        'fallback': True,
                        'window_size': current_window_size,
                        'context_snippets': len(context_snippets)
                    }
                )
        
        except Exception as e:
            logger.error(f"Context analysis completely failed: {e}")
            return self._create_fallback_result(str(e))
    
    def get_analysis_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del analyzer
        
        Returns:
            Diccionario con estadísticas
        """
        if hasattr(self.llm_client, 'get_session_stats'):
            llm_stats = self.llm_client.get_session_stats()
        else:
            llm_stats = {}
        
        return {
            'agent': self.agent_name,
            'window_size': self.window_size,
            'llm_stats': llm_stats,
            'prompt_template_loaded': bool(self.prompt_template)
        }

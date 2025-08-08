"""
Context Analyzer Mejorado - Versión Integrada
============================================

Versión mejorada del Context Analyzer que integra:
- Templates especializados para código complejo
- Parser JSON ultra-robusto
- Sistema de filtrado de precisión
- Análisis multi-pass adaptativo
- Mejor manejo de errores y fallbacks

Esta versión reemplaza la versión básica para casos complejos.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from .context_analyzer import ContextAnalyzer
from .enhanced_analyzer import EnhancedContextAnalyzer, CodeComplexity
from .robust_json_parser import RobustJSONParser
from .precision_filter import PrecisionFilter
from .base_agent import Snippet, AgentResult, DependencyMap

logger = logging.getLogger(__name__)


class ImprovedContextAnalyzer(EnhancedContextAnalyzer):
    """
    Context Analyzer con todas las mejoras integradas
    """
    
    def __init__(self, llm_client=None, window_size: int = 20, enable_precision_filter: bool = True):
        super().__init__(llm_client, window_size)
        
        # Componentes mejorados
        self.json_parser = RobustJSONParser()
        self.precision_filter = PrecisionFilter() if enable_precision_filter else None
        
        # Configuración
        self.enable_precision_filter = enable_precision_filter
        self.max_complexity_threshold = 0.8  # Umbral para casos muy complejos
        
        # Métricas de rendimiento
        self.parsing_stats = []
        self.filter_stats = []
        
        logger.info("ImprovedContextAnalyzer initialized with enhanced capabilities")
    
    async def analyze(self,
                     snippet: Snippet,
                     all_snippets: List[Snippet],
                     snippet_index: int,
                     **kwargs) -> AgentResult:
        """
        Análisis mejorado con pipeline completo de optimizaciones
        """
        self.logger.info("Starting improved context analysis")
        start_time = time.time()
        
        try:
            # Fase 1: Análisis de complejidad y estrategia
            context_snippets_data = self._extract_context_snippets(all_snippets, snippet_index)
            context_snippets = [all_snippets[cs['index']] for cs in context_snippets_data 
                              if not cs['is_target']]
            
            complexity = self._analyze_code_complexity(snippet, context_snippets)
            strategy = self._choose_enhanced_analysis_strategy(complexity)
            
            self.logger.info(f"Analysis strategy: {strategy} (complexity: {complexity.complexity_score:.2f})")
            
            # Fase 2: Análisis LLM con estrategia adaptativa
            dependency_map = await self._execute_analysis_strategy(
                strategy, snippet, context_snippets_data, complexity
            )
            
            # Fase 3: Post-procesamiento y filtrado
            if dependency_map.confidence > 0.0:
                dependency_map = self._post_process_dependencies(
                    dependency_map, snippet, complexity
                )
            
            # Fase 4: Métricas y metadata
            processing_time = time.time() - start_time
            metadata = self._build_analysis_metadata(complexity, strategy, processing_time)
            
            return AgentResult(
                success=dependency_map.confidence > 0.0,
                data=dependency_map.to_dict(),
                confidence=dependency_map.confidence,
                processing_time=processing_time,
                error=dependency_map.error,
                metadata=metadata
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            logger.error(f"Improved analysis failed: {e}")
            
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=processing_time,
                error=f"Improved analysis failed: {str(e)}",
                metadata={'analysis_strategy': 'failed'}
            )
    
    def _choose_enhanced_analysis_strategy(self, complexity: CodeComplexity) -> str:
        """
        Elige estrategia de análisis mejorada basada en complejidad detallada
        """
        if complexity.complexity_score > self.max_complexity_threshold:
            return "ultra_complex"
        elif complexity.complexity_score > 0.5:
            return "complex_multi_pass"
        elif complexity.framework_patterns:
            return "framework_specialized"
        elif complexity.has_decorators or complexity.has_inheritance:
            return "pattern_aware"
        else:
            return "standard_improved"
    
    async def _execute_analysis_strategy(self,
                                       strategy: str,
                                       snippet: Snippet,
                                       context_snippets_data: List[Dict],
                                       complexity: CodeComplexity) -> DependencyMap:
        """
        Ejecuta la estrategia de análisis seleccionada
        """
        formatted_context = self._format_context_for_llm(context_snippets_data)
        
        if strategy == "ultra_complex":
            return await self._ultra_complex_analysis(snippet, formatted_context, complexity)
        elif strategy == "complex_multi_pass":
            return await self._multi_pass_analysis(snippet, formatted_context, complexity)
        elif strategy == "framework_specialized":
            return await self._framework_specialized_analysis(snippet, formatted_context, complexity)
        elif strategy == "pattern_aware":
            return await self._pattern_aware_analysis(snippet, formatted_context, complexity)
        else:
            return await self._standard_improved_analysis(snippet, formatted_context)
    
    async def _ultra_complex_analysis(self,
                                    snippet: Snippet,
                                    formatted_context: str,
                                    complexity: CodeComplexity) -> DependencyMap:
        """
        Análisis para casos ultra-complejos con múltiples intentos y fallbacks
        """
        attempts = [
            ("complex_template", self._analyze_with_complex_template),
            ("standard_template", self._analyze_with_standard_template),
            ("ast_enhanced", self._enhanced_ast_fallback_wrapper)
        ]
        
        best_result = None
        best_confidence = 0.0
        
        for attempt_name, analysis_method in attempts:
            try:
                if attempt_name == "ast_enhanced":
                    result = analysis_method(snippet, [], complexity)
                else:
                    result = await analysis_method(snippet, formatted_context)
                
                if result.confidence > best_confidence:
                    best_result = result
                    best_confidence = result.confidence
                    
                # Si obtenemos confianza alta, usar ese resultado
                if result.confidence > 0.8:
                    logger.info(f"High confidence result from {attempt_name}")
                    return result
                    
            except Exception as e:
                logger.warning(f"Ultra-complex analysis attempt {attempt_name} failed: {e}")
                continue
        
        return best_result or DependencyMap(confidence=0.0, error="All ultra-complex analysis attempts failed")
    
    async def _multi_pass_analysis(self,
                                 snippet: Snippet,
                                 formatted_context: str,
                                 complexity: CodeComplexity) -> DependencyMap:
        """
        Análisis multi-pass para código complejo
        """
        # Pass 1: Análisis general
        general_result = await self._analyze_with_complex_template(snippet, formatted_context)
        
        # Pass 2: Análisis específico de patrones detectados
        if complexity.framework_patterns:
            framework_result = await self._analyze_framework_patterns(snippet, complexity.framework_patterns)
            general_result = self._merge_dependency_maps(general_result, framework_result)
        
        # Pass 3: Refinamiento con AST si la confianza es baja
        if general_result.confidence < 0.5:
            ast_result = self._enhanced_ast_fallback_wrapper(snippet, [], complexity)
            general_result = self._merge_dependency_maps(general_result, ast_result, prefer_higher_confidence=True)
        
        return general_result
    
    async def _framework_specialized_analysis(self,
                                            snippet: Snippet,
                                            formatted_context: str,
                                            complexity: CodeComplexity) -> DependencyMap:
        """
        Análisis especializado para frameworks detectados
        """
        # Usar template especializado si está disponible
        framework_template = self._get_framework_template(complexity.framework_patterns)
        
        if framework_template:
            try:
                prompt = framework_template.format(
                    target_snippet=snippet.content,
                    context_snippets=formatted_context,
                    detected_frameworks=", ".join(complexity.framework_patterns)
                )
                
                llm_analysis = await self._with_timeout_and_retry(
                    self.llm_client.generate(
                        prompt=prompt,
                        system_message=f"You are an expert in {', '.join(complexity.framework_patterns)} frameworks."
                    )
                )
                
                return self._parse_enhanced_llm_response(llm_analysis.content)
                
            except Exception as e:
                logger.warning(f"Framework specialized analysis failed: {e}")
        
        # Fallback a análisis complejo estándar
        return await self._analyze_with_complex_template(snippet, formatted_context)
    
    async def _pattern_aware_analysis(self,
                                    snippet: Snippet,
                                    formatted_context: str,
                                    complexity: CodeComplexity) -> DependencyMap:
        """
        Análisis consciente de patrones específicos (decorators, herencia, etc.)
        """
        # Preparar contexto adicional sobre patrones detectados
        pattern_context = self._build_pattern_context(complexity)
        enhanced_prompt = self.complex_template.format(
            target_snippet=snippet.content,
            context_snippets=formatted_context + "\n\n" + pattern_context
        )
        
        try:
            llm_analysis = await self._with_timeout_and_retry(
                self.llm_client.generate(
                    prompt=enhanced_prompt,
                    system_message="You are an expert in Python design patterns and advanced language features."
                )
            )
            
            return self._parse_enhanced_llm_response(llm_analysis.content)
            
        except Exception as e:
            logger.error(f"Pattern-aware analysis failed: {e}")
            return await self._analyze_with_standard_template(snippet, formatted_context)
    
    async def _standard_improved_analysis(self,
                                        snippet: Snippet,
                                        formatted_context: str) -> DependencyMap:
        """
        Análisis estándar pero con parsing y manejo de errores mejorados
        """
        return await self._analyze_with_standard_template(snippet, formatted_context)
    
    def _parse_enhanced_llm_response(self, llm_content: str) -> DependencyMap:
        """
        Parser mejorado usando el sistema robusto
        """
        parse_result = self.json_parser.parse(llm_content)
        self.parsing_stats.append(parse_result)
        
        if parse_result.success:
            parsed_data = parse_result.data
            return DependencyMap(
                variables=parsed_data.get("variables", {}),
                classes=parsed_data.get("classes", {}),
                imports=parsed_data.get("imports", {}),
                functions=parsed_data.get("functions", {}),
                confidence=parsed_data.get("overall_confidence", 0.7)
            )
        else:
            logger.warning(f"Robust JSON parsing failed: {parse_result.errors}")
            return DependencyMap(
                confidence=0.0,
                error=f"JSON parsing failed: {', '.join(parse_result.errors)}"
            )
    
    def _post_process_dependencies(self,
                                 dependency_map: DependencyMap,
                                 snippet: Snippet,
                                 complexity: CodeComplexity) -> DependencyMap:
        """
        Post-procesamiento con filtrado de precisión y validaciones
        """
        if not self.enable_precision_filter or not self.precision_filter:
            return dependency_map
        
        # Aplicar filtros de precisión
        original_map = dependency_map
        filtered_map = self.precision_filter.filter_dependencies(
            dependency_map, snippet.content
        )
        
        # Guardar estadísticas de filtrado
        filter_stats = self.precision_filter.analyze_filter_effectiveness(
            original_map, filtered_map
        )
        self.filter_stats.append(filter_stats)
        
        logger.debug(f"Filtered {filter_stats['overall']['total_filtered']} dependencies "
                    f"({filter_stats['overall']['overall_filter_rate']:.2%} reduction)")
        
        return filtered_map
    
    def _enhanced_ast_fallback_wrapper(self,
                                     snippet: Snippet,
                                     all_snippets: List[Snippet],
                                     complexity: CodeComplexity) -> DependencyMap:
        """
        Wrapper para el fallback AST mejorado
        """
        return self._enhanced_ast_fallback(snippet, all_snippets, complexity)
    
    def _merge_dependency_maps(self,
                             map1: DependencyMap,
                             map2: DependencyMap,
                             prefer_higher_confidence: bool = False) -> DependencyMap:
        """
        Fusiona dos mapas de dependencias de manera inteligente
        """
        if map1.confidence == 0.0:
            return map2
        if map2.confidence == 0.0:
            return map1
        
        # Decidir qué mapa usar como base
        if prefer_higher_confidence:
            primary, secondary = (map1, map2) if map1.confidence >= map2.confidence else (map2, map1)
        else:
            primary, secondary = map1, map2
        
        merged_map = DependencyMap(
            variables={**secondary.variables, **primary.variables},
            classes={**secondary.classes, **primary.classes},
            imports={**secondary.imports, **primary.imports},
            functions={**secondary.functions, **primary.functions},
            confidence=max(primary.confidence, secondary.confidence),
            error=primary.error or secondary.error
        )
        
        return merged_map
    
    def _get_framework_template(self, frameworks: List[str]) -> Optional[str]:
        """
        Obtiene template especializado para frameworks detectados
        """
        # Por ahora usar el template complejo, pero se puede especializar más
        return self.complex_template
    
    def _build_pattern_context(self, complexity: CodeComplexity) -> str:
        """
        Construye contexto adicional sobre patrones detectados
        """
        context_parts = ["DETECTED PATTERNS:"]
        
        if complexity.has_decorators:
            context_parts.append("- Contains decorators: Pay attention to decorator dependencies")
        
        if complexity.has_inheritance:
            context_parts.append("- Contains inheritance: Track parent class dependencies")
        
        if complexity.has_context_managers:
            context_parts.append("- Contains 'with' statements: Consider context manager setup")
        
        if complexity.has_comprehensions:
            context_parts.append("- Contains comprehensions: Check for closure variables")
        
        if complexity.has_f_strings:
            context_parts.append("- Contains f-strings: Variables embedded in strings")
        
        if complexity.framework_patterns:
            context_parts.append(f"- Framework patterns: {', '.join(complexity.framework_patterns)}")
        
        return "\n".join(context_parts)
    
    async def _analyze_framework_patterns(self,
                                        snippet: Snippet,
                                        frameworks: List[str]) -> DependencyMap:
        """
        Análisis específico de patrones de framework
        """
        # Implementación simplificada - se puede expandir por framework
        try:
            framework_context = f"Analyzing {', '.join(frameworks)} framework patterns"
            prompt = f"""
Analyze this {', '.join(frameworks)} code for framework-specific dependencies:

```python
{snippet.content}
```

Focus on:
1. Framework-specific imports and objects
2. Decorator dependencies
3. Framework conventions and patterns

Return JSON with dependency analysis.
"""
            
            llm_analysis = await self._with_timeout_and_retry(
                self.llm_client.generate(
                    prompt=prompt,
                    system_message=f"You are an expert in {', '.join(frameworks)} framework patterns."
                )
            )
            
            return self._parse_enhanced_llm_response(llm_analysis.content)
            
        except Exception as e:
            logger.warning(f"Framework pattern analysis failed: {e}")
            return DependencyMap(confidence=0.0, error=str(e))
    
    def _build_analysis_metadata(self,
                                complexity: CodeComplexity,
                                strategy: str,
                                processing_time: float) -> Dict[str, Any]:
        """
        Construye metadata detallada del análisis
        """
        return {
            'analysis_version': 'improved_v1.0',
            'complexity_score': complexity.complexity_score,
            'detected_patterns': complexity.framework_patterns,
            'analysis_strategy': strategy,
            'has_decorators': complexity.has_decorators,
            'has_inheritance': complexity.has_inheritance,
            'has_frameworks': bool(complexity.framework_patterns),
            'processing_time': processing_time,
            'precision_filter_enabled': self.enable_precision_filter,
            'parsing_method_used': self.parsing_stats[-1].method_used if self.parsing_stats else None,
            'filter_effectiveness': self.filter_stats[-1]['overall'] if self.filter_stats else None
        }
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de rendimiento del analyzer mejorado
        """
        return {
            'parsing_stats': self.json_parser.get_parsing_stats(self.parsing_stats),
            'filter_stats_summary': {
                'total_filters_applied': len(self.filter_stats),
                'avg_filter_rate': sum(fs['overall']['overall_filter_rate'] for fs in self.filter_stats) / len(self.filter_stats) if self.filter_stats else 0,
                'avg_confidence_improvement': sum(fs['overall']['confidence_improvement'] for fs in self.filter_stats) / len(self.filter_stats) if self.filter_stats else 0
            }
        }
    
    def reset_performance_stats(self):
        """Resetea las estadísticas de rendimiento"""
        self.parsing_stats.clear()
        self.filter_stats.clear()


def create_improved_analyzer(llm_client=None, **kwargs) -> ImprovedContextAnalyzer:
    """Factory function para crear analyzer mejorado"""
    return ImprovedContextAnalyzer(llm_client, **kwargs)

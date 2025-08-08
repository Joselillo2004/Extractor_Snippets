"""
Enhanced Context Analyzer con análisis multi-pass para código complejo
"""

import ast
import re
from typing import List, Dict, Any, Optional, Union, Tuple
from dataclasses import dataclass
from .context_analyzer import ContextAnalyzer
from .base_agent import Snippet, AgentResult, DependencyMap
import logging

logger = logging.getLogger(__name__)


@dataclass
class CodeComplexity:
    """Análisis de complejidad del código"""
    has_decorators: bool = False
    has_inheritance: bool = False
    has_context_managers: bool = False
    has_comprehensions: bool = False
    has_f_strings: bool = False
    framework_patterns: List[str] = None
    complexity_score: float = 0.0
    
    def __post_init__(self):
        if self.framework_patterns is None:
            self.framework_patterns = []


class EnhancedContextAnalyzer(ContextAnalyzer):
    """
    Analyzer con capacidades mejoradas para código complejo
    """
    
    def __init__(self, llm_client=None, window_size: int = 20):
        super().__init__(llm_client, window_size)
        
        # Templates especializados
        self.complex_template = self._load_complex_template()
        self.framework_patterns = self._load_framework_patterns()
    
    def _load_complex_template(self) -> str:
        """Carga template para código complejo"""
        from pathlib import Path
        template_path = Path(__file__).parent / "prompt_templates" / "complex_code_analysis.txt"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.warning(f"Could not load complex template: {e}")
            return self.prompt_template  # Fallback al template normal
    
    def _load_framework_patterns(self) -> Dict[str, List[str]]:
        """Carga patrones de frameworks conocidos"""
        return {
            'flask': [
                r'@app\.route\s*\(',
                r'from flask import',
                r'Flask\s*\(',
                r'request\.',
                r'session\.',
                r'jsonify\s*\('
            ],
            'django': [
                r'from django',
                r'models\.Model',
                r'HttpResponse',
                r'@require_',
                r'render\s*\(',
                r'reverse\s*\('
            ],
            'fastapi': [
                r'from fastapi',
                r'@app\.(get|post|put|delete)',
                r'FastAPI\s*\(',
                r'Depends\s*\(',
                r'HTTPException'
            ],
            'pandas': [
                r'import pandas as pd',
                r'pd\.',
                r'DataFrame\s*\(',
                r'\.read_csv\s*\(',
                r'\.groupby\s*\(',
                r'\.merge\s*\('
            ],
            'numpy': [
                r'import numpy as np',
                r'np\.',
                r'np\.array\s*\(',
                r'np\.zeros\s*\(',
                r'np\.ones\s*\('
            ],
            'sqlalchemy': [
                r'from sqlalchemy',
                r'Column\s*\(',
                r'relationship\s*\(',
                r'session\.',
                r'Base\.'
            ]
        }
    
    def _analyze_code_complexity(self, snippet: Snippet, context_snippets: List[Snippet]) -> CodeComplexity:
        """
        Analiza la complejidad del código para determinar estrategia de análisis
        """
        complexity = CodeComplexity()
        all_code = snippet.content + "\n" + "\n".join(s.content for s in context_snippets)
        
        # Detectar decorators
        if re.search(r'^@\w+', all_code, re.MULTILINE):
            complexity.has_decorators = True
        
        # Detectar herencia múltiple o compleja
        if re.search(r'class\s+\w+\s*\([^)]*,', all_code):
            complexity.has_inheritance = True
        
        # Detectar context managers
        if re.search(r'\bwith\s+\w+', all_code):
            complexity.has_context_managers = True
        
        # Detectar comprehensions
        if re.search(r'\[[^\]]*for\s+\w+\s+in', all_code) or re.search(r'\{[^}]*for\s+\w+\s+in', all_code):
            complexity.has_comprehensions = True
        
        # Detectar f-strings
        if re.search(r'f["\'][^"\']*\{[^}]+\}', all_code):
            complexity.has_f_strings = True
        
        # Detectar frameworks
        for framework, patterns in self.framework_patterns.items():
            for pattern in patterns:
                if re.search(pattern, all_code, re.IGNORECASE):
                    complexity.framework_patterns.append(framework)
                    break
        
        # Calcular score de complejidad
        complexity.complexity_score = (
            (0.2 if complexity.has_decorators else 0) +
            (0.2 if complexity.has_inheritance else 0) +
            (0.1 if complexity.has_context_managers else 0) +
            (0.1 if complexity.has_comprehensions else 0) +
            (0.1 if complexity.has_f_strings else 0) +
            (0.3 if complexity.framework_patterns else 0)
        )
        
        return complexity
    
    def _choose_analysis_strategy(self, complexity: CodeComplexity) -> str:
        """
        Elige la estrategia de análisis basada en la complejidad
        """
        if complexity.complexity_score > 0.4:
            return "complex"
        elif complexity.framework_patterns:
            return "framework"
        else:
            return "standard"
    
    async def _analyze_with_complex_template(self,
                                           snippet: Snippet,
                                           formatted_context: str) -> DependencyMap:
        """
        Análisis usando template especializado para código complejo
        """
        prompt = self.complex_template.format(
            target_snippet=snippet.content,
            context_snippets=formatted_context
        )
        
        try:
            llm_analysis = await self._with_timeout_and_retry(
                self.llm_client.generate(
                    prompt=prompt,
                    system_message="You are an expert in complex Python patterns and modern frameworks."
                )
            )
            
            return self._parse_enhanced_llm_response(llm_analysis.content)
            
        except Exception as e:
            logger.error(f"Complex analysis failed: {e}")
            return DependencyMap(confidence=0.0, error=f"Complex analysis failed: {str(e)}")
    
    def _parse_enhanced_llm_response(self, llm_content: str) -> DependencyMap:
        """
        Parser mejorado que maneja la estructura extendida de respuestas complejas
        """
        try:
            # Usar el parser base pero con campos adicionales
            base_map = self._parse_llm_response(llm_content)
            
            # Si el parsing básico falló, intentar con JSON más flexible
            if base_map.confidence == 0.0:
                return self._parse_flexible_json(llm_content)
            
            return base_map
            
        except Exception as e:
            logger.error(f"Enhanced JSON parsing failed: {e}")
            return DependencyMap(confidence=0.0, error=f"Enhanced parsing failed: {str(e)}")
    
    def _parse_flexible_json(self, llm_content: str) -> DependencyMap:
        """
        Parser más flexible para JSON malformado
        """
        import json5  # Permite JSON con comentarios y trailing commas
        
        try:
            # Limpiar respuesta común de LLMs
            content = llm_content.strip()
            
            # Remover texto explicativo al inicio/final
            if '```json' in content:
                start = content.find('```json') + 7
                end = content.find('```', start)
                if end > start:
                    content = content[start:end].strip()
            
            # Intentar múltiples estrategias de limpieza
            for strategy in [
                lambda x: x,  # Sin cambios
                lambda x: x.replace(',\n}', '\n}').replace(',\n]', '\n]'),  # Trailing commas
                lambda x: re.sub(r',(\s*[}\]])', r'\1', x),  # Regex trailing commas
                lambda x: x.replace("'", '"'),  # Comillas simples a dobles
            ]:
                try:
                    cleaned = strategy(content)
                    parsed = json5.loads(cleaned)
                    
                    return DependencyMap(
                        variables=parsed.get("variables", {}),
                        classes=parsed.get("classes", {}),
                        imports=parsed.get("imports", {}),
                        functions=parsed.get("functions", {}),
                        confidence=parsed.get("overall_confidence", 0.7)
                    )
                except:
                    continue
            
            # Si todo falla, fallback básico
            return DependencyMap(confidence=0.0, error="All JSON parsing strategies failed")
            
        except Exception as e:
            logger.error(f"Flexible JSON parsing failed: {e}")
            return DependencyMap(confidence=0.0, error=str(e))
    
    async def analyze(self,
                     snippet: Snippet,
                     all_snippets: List[Snippet],
                     snippet_index: int,
                     **kwargs) -> AgentResult:
        """
        Análisis mejorado con detección de complejidad y estrategia adaptativa
        """
        self.logger.info("Starting enhanced context analysis")
        start_time = time.time()
        
        try:
            # Validaciones básicas
            self._validate_inputs(snippet, all_snippets, snippet_index)
            
            # Extraer contexto
            context_snippets_data = self._extract_context_snippets(all_snippets, snippet_index)
            context_snippets = [all_snippets[cs['index']] for cs in context_snippets_data 
                              if not cs['is_target']]
            
            # Analizar complejidad
            complexity = self._analyze_code_complexity(snippet, context_snippets)
            strategy = self._choose_analysis_strategy(complexity)
            
            self.logger.info(f"Code complexity: {complexity.complexity_score:.2f}, strategy: {strategy}")
            
            # Formatear contexto
            formatted_context = self._format_context_for_llm(context_snippets_data)
            
            # Elegir estrategia de análisis
            if strategy == "complex":
                dependency_map = await self._analyze_with_complex_template(snippet, formatted_context)
            else:
                # Usar análisis estándar
                dependency_map = await self._analyze_with_standard_template(snippet, formatted_context)
            
            # Si falló, intentar fallback AST mejorado
            if dependency_map.confidence < 0.3:
                logger.warning("LLM analysis failed, using enhanced AST fallback")
                dependency_map = self._enhanced_ast_fallback(snippet, all_snippets, complexity)
            
            # Agregar metadata de complejidad
            metadata = {
                'complexity_score': complexity.complexity_score,
                'detected_patterns': complexity.framework_patterns,
                'analysis_strategy': strategy,
                'has_decorators': complexity.has_decorators,
                'has_frameworks': bool(complexity.framework_patterns)
            }
            
            processing_time = time.time() - start_time
            
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
            logger.error(f"Enhanced analysis completely failed: {e}")
            
            return AgentResult(
                success=False,
                data={},
                confidence=0.0,
                processing_time=processing_time,
                error=f"Enhanced analysis failed: {str(e)}",
                metadata={'analysis_strategy': 'failed'}
            )
    
    async def _analyze_with_standard_template(self, snippet: Snippet, formatted_context: str) -> DependencyMap:
        """Análisis con template estándar"""
        prompt = self.prompt_template.format(
            target_snippet=snippet.content,
            context_snippets=formatted_context
        )
        
        try:
            llm_analysis = await self._with_timeout_and_retry(
                self.llm_client.generate(
                    prompt=prompt,
                    system_message="You are an expert Python code analyzer focused on dependency detection."
                )
            )
            
            return self._parse_llm_response(llm_analysis.content)
            
        except Exception as e:
            logger.error(f"Standard analysis failed: {e}")
            return DependencyMap(confidence=0.0, error=f"Standard analysis failed: {str(e)}")
    
    def _enhanced_ast_fallback(self, 
                             snippet: Snippet, 
                             all_snippets: List[Snippet],
                             complexity: CodeComplexity) -> DependencyMap:
        """
        Fallback AST mejorado que considera patrones complejos
        """
        try:
            # Análisis AST básico
            base_analysis = self._analyze_with_ast_fallback(snippet)
            
            # Mejorar con análisis de patrones específicos
            if complexity.framework_patterns:
                enhanced_variables = self._detect_framework_variables(
                    snippet.content, complexity.framework_patterns
                )
                base_analysis.variables.update(enhanced_variables)
            
            if complexity.has_decorators:
                decorator_deps = self._detect_decorator_dependencies(snippet.content)
                base_analysis.functions.update(decorator_deps)
            
            # Mejorar confianza si detectamos patrones conocidos
            if complexity.complexity_score > 0.3:
                base_analysis.confidence = min(0.6, base_analysis.confidence + 0.2)
            
            base_analysis.error = f"LLM failed, using enhanced AST fallback (complexity: {complexity.complexity_score:.2f})"
            
            return base_analysis
            
        except Exception as e:
            logger.error(f"Enhanced AST fallback failed: {e}")
            return DependencyMap(confidence=0.0, error="All analysis methods failed")
    
    def _detect_framework_variables(self, code: str, frameworks: List[str]) -> Dict[str, Dict]:
        """Detecta variables específicas de frameworks"""
        variables = {}
        
        # Patrones comunes por framework
        patterns = {
            'flask': {
                'app': {'type': 'Flask', 'confidence': 0.8},
                'request': {'type': 'Request', 'confidence': 0.7},
                'session': {'type': 'Session', 'confidence': 0.7}
            },
            'pandas': {
                'pd': {'type': 'module', 'confidence': 0.9},
                'df': {'type': 'DataFrame', 'confidence': 0.6}
            }
        }
        
        for framework in frameworks:
            if framework in patterns:
                for var_name, var_info in patterns[framework].items():
                    if var_name in code:
                        variables[var_name] = {
                            'defined_in_snippet': None,
                            'definition': f"# {framework} framework variable",
                            'type': var_info['type'],
                            'confidence': var_info['confidence'],
                            'framework': framework
                        }
        
        return variables
    
    def _detect_decorator_dependencies(self, code: str) -> Dict[str, Dict]:
        """Detecta dependencias de decorators"""
        functions = {}
        
        # Buscar patrones de decorators
        decorator_matches = re.findall(r'@(\w+(?:\.\w+)*)', code)
        
        for decorator in decorator_matches:
            # Simplificar nombre del decorator (app.route -> route)
            simple_name = decorator.split('.')[-1]
            functions[simple_name] = {
                'defined_in_snippet': None,
                'definition': f"# Decorator: @{decorator}",
                'return_type': 'decorator',
                'confidence': 0.6,
                'is_decorator': True
            }
        
        return functions


# Instalar json5 si no existe
try:
    import json5
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "json5"])
    import json5

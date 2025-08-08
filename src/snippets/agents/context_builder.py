"""
Context Builder Agent - Construcción de contexto optimizado usando LLM

Responsabilidades:
1. Construir contexto mínimo y ejecutable para snippets
2. Optimizar código para incluir solo lo necesario
3. Generar valores realistas para variables cuando sea necesario
4. Mantener orden correcto de dependencias
5. Validar sintaxis y seguridad del contexto construido
6. Fallback heurístico cuando LLM falla
"""

import ast
import json
import re
import time
from typing import List, Dict, Any, Optional, Set
from pathlib import Path

from .base_agent import BaseAgent, Snippet, AgentResult
from .llm_client import get_llm_client, LLMConfig, LLMResponse
from pydantic import BaseModel, Field

import logging
logger = logging.getLogger(__name__)


class BuiltContext(BaseModel):
    """Estructura del contexto construido"""
    context_code: str
    dependencies_included: List[str] = Field(default_factory=list)
    optimization_applied: bool = False
    lines_count: int = 0
    safety_validated: bool = True
    syntax_valid: bool = True
    
    class Config:
        validate_assignment = True


class ContextBuilder(BaseAgent):
    """
    Agent especializado en construcción de contexto optimizado
    """
    
    # Patrones peligrosos que nunca deben incluirse en contexto
    DANGEROUS_PATTERNS = [
        r'os\.system',
        r'subprocess\.',
        r'\beval\s*\(',
        r'\bexec\s*\(',
        r'__import__',
        r'open\s*\([^)]*[\'"]w[\'"]',  # open write mode
        r'open\s*\([^)]*[\'"]a[\'"]',  # open append mode
        r'shutil\.',
        r'rmtree',
        r'remove\s*\(',
    ]
    
    # Valores por defecto realistas por tipo
    DEFAULT_VALUES = {
        'list': '[1, 2, 3]',
        'str': '"example"',
        'int': '42',
        'float': '3.14',
        'bool': 'True',
        'dict': '{"key": "value"}',
        'set': '{1, 2, 3}',
        'tuple': '(1, 2, 3)',
    }
    
    def __init__(self, llm_client=None, enable_llm: bool = True):
        """
        Initialize Context Builder
        
        Args:
            llm_client: Cliente LLM configurado
            enable_llm: Si usar LLM para construcción avanzada
        """
        if llm_client is None:
            llm_client = get_llm_client()
        
        super().__init__(
            llm_client=llm_client,
            agent_name="ContextBuilder",
            max_retries=2,
            timeout_seconds=20.0
        )
        
        self.enable_llm = enable_llm
        self.prompt_template = self._load_prompt_template()
        
        logger.info(f"ContextBuilder initialized (LLM enabled: {enable_llm})")
    
    def _load_prompt_template(self) -> str:
        """
        Carga el template de prompt desde archivo
        
        Returns:
            Template de prompt como string
        """
        template_path = Path(__file__).parent / "prompt_templates" / "context_building.txt"
        
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load prompt template: {e}")
            # Fallback template simple
            return """Build minimal context for this Python snippet:
Target: {target_snippet}
Dependencies: {dependencies_json}
Return only the necessary context code."""
    
    def _validate_context_safety(self, context_code: str) -> tuple[bool, List[str]]:
        """
        Valida que el contexto no contenga código peligroso
        
        Args:
            context_code: Código de contexto a validar
            
        Returns:
            Tupla (es_seguro, lista_de_problemas)
        """
        problems = []
        
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, context_code, re.IGNORECASE):
                problems.append(f"Dangerous pattern detected: {pattern}")
        
        is_safe = len(problems) == 0
        return is_safe, problems
    
    def _validate_context_syntax(self, context_code: str) -> tuple[bool, Optional[str]]:
        """
        Valida que el contexto sea sintácticamente válido
        
        Args:
            context_code: Código de contexto a validar
            
        Returns:
            Tupla (es_válido, error_mensaje)
        """
        try:
            ast.parse(context_code)
            return True, None
        except SyntaxError as e:
            return False, str(e)
    
    def _extract_minimal_definition(self, full_definition: str, needed_name: str) -> str:
        """
        Extrae la definición mínima necesaria de un bloque de código
        
        Args:
            full_definition: Definición completa (puede ser multi-línea)
            needed_name: Nombre específico que se necesita
            
        Returns:
            Definición mínima extraída
        """
        lines = full_definition.strip().split('\n')
        
        # Para definiciones simples de variables
        for line in lines:
            line = line.strip()
            if line.startswith(f'{needed_name} ='):
                return line
        
        # Para funciones y clases, incluir toda la definición
        if any(line.strip().startswith(('def ', 'class ')) for line in lines):
            return full_definition
        
        # Por defecto, retornar la primera línea relevante
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                if needed_name in line:
                    return line
        
        return full_definition
    
    def _generate_realistic_value(self, var_name: str, var_type: str, context_hint: str = "") -> str:
        """
        Genera un valor realista para una variable basado en su tipo
        
        Args:
            var_name: Nombre de la variable
            var_type: Tipo inferido de la variable
            context_hint: Contexto adicional para generar valores más realistas
            
        Returns:
            Definición de variable con valor realista
        """
        # Mapeo de tipos comunes
        type_mapping = {
            'list': '[1, 2, 3]',
            'str': '"sample_text"',
            'int': '42', 
            'float': '3.14',
            'bool': 'True',
            'dict': '{"key": "value"}',
        }
        
        # Valores contextuales basados en el nombre de la variable
        contextual_values = {
            'name': '"John Doe"',
            'nombre': '"Juan Pérez"',
            'age': '25',
            'edad': '25',
            'price': '99.99',
            'precio': '99.99',
            'active': 'True',
            'activo': 'True',
            'count': '10',
            'contador': '10',
            'lista': '[1, 2, 3, 4, 5]',
            'items': '["item1", "item2", "item3"]',
            'data': '{"id": 1, "value": "example"}',
            'config': '{"debug": True, "timeout": 30}',
        }
        
        # Buscar valor contextual primero
        var_lower = var_name.lower()
        if var_lower in contextual_values:
            value = contextual_values[var_lower]
        else:
            # Usar mapeo por tipo
            value = type_mapping.get(var_type, '42')  # Default a int
        
        return f"{var_name} = {value}"
    
    def _build_context_heuristic(self, 
                                target_snippet: str,
                                dependencies: Dict[str, Any],
                                all_snippets: List[Snippet]) -> BuiltContext:
        """
        Construcción heurística de contexto (fallback sin LLM)
        
        Args:
            target_snippet: Snippet que necesita contexto
            dependencies: Dependencias detectadas por Context Analyzer
            all_snippets: Lista completa de snippets disponibles
            
        Returns:
            BuiltContext construido heurísticamente
        """
        context_lines = []
        dependencies_included = []
        
        # Orden: imports → variables → functions → classes
        
        # 1. Imports
        if 'imports' in dependencies:
            for import_name, import_info in dependencies['imports'].items():
                import_statement = import_info.get('import_statement', f'import {import_name}')
                if import_statement not in context_lines:
                    context_lines.append(import_statement)
                    dependencies_included.append(f"import:{import_name}")
        
        # 2. Variables
        if 'variables' in dependencies:
            for var_name, var_info in dependencies['variables'].items():
                definition = var_info.get('definition')
                var_type = var_info.get('type', 'unknown')
                
                if definition:
                    # Extraer definición mínima
                    minimal_def = self._extract_minimal_definition(definition, var_name)
                    context_lines.append(minimal_def)
                else:
                    # Generar valor realista
                    generated_def = self._generate_realistic_value(var_name, var_type)
                    context_lines.append(generated_def)
                
                dependencies_included.append(f"variable:{var_name}")
        
        # 3. Functions
        if 'functions' in dependencies:
            for func_name, func_info in dependencies['functions'].items():
                definition = func_info.get('definition')
                if definition:
                    context_lines.append(definition)
                    dependencies_included.append(f"function:{func_name}")
        
        # 4. Classes
        if 'classes' in dependencies:
            for class_name, class_info in dependencies['classes'].items():
                definition = class_info.get('definition')
                if definition:
                    context_lines.append(definition)
                    dependencies_included.append(f"class:{class_name}")
        
        context_code = '\n\n'.join(context_lines) if context_lines else ""
        
        # Validar seguridad y sintaxis
        safety_valid, safety_problems = self._validate_context_safety(context_code)
        syntax_valid, syntax_error = self._validate_context_syntax(context_code)
        
        if not safety_valid:
            logger.warning(f"Context safety issues: {safety_problems}")
            context_code = "# Context removed due to safety concerns"
        elif not syntax_valid:
            logger.warning(f"Context syntax error: {syntax_error}")
            # Intentar arreglar problemas comunes de sintaxis
            context_code = self._fix_common_syntax_issues(context_code)
            syntax_valid, _ = self._validate_context_syntax(context_code)
        
        return BuiltContext(
            context_code=context_code,
            dependencies_included=dependencies_included,
            optimization_applied=True,
            lines_count=len(context_lines),
            safety_validated=safety_valid,
            syntax_valid=syntax_valid
        )
    
    def _fix_common_syntax_issues(self, context_code: str) -> str:
        """
        Intenta arreglar problemas comunes de sintaxis
        
        Args:
            context_code: Código con posibles problemas de sintaxis
            
        Returns:
            Código con intentos de corrección
        """
        # Correcciones comunes
        fixes = [
            (r':\s*\n\s*$', ':\n    pass'),  # Añadir pass a bloques vacíos
            (r'def\s+(\w+)\s*\(([^)]*)\)\s*$', r'def \1(\2):\n    pass'),  # Arreglar funciones sin cuerpo
            (r'class\s+(\w+)\s*:\s*$', r'class \1:\n    pass'),  # Arreglar clases vacías
        ]
        
        for pattern, replacement in fixes:
            context_code = re.sub(pattern, replacement, context_code, flags=re.MULTILINE)
        
        return context_code
    
    def _format_dependencies_for_llm(self, dependencies: Dict[str, Any]) -> str:
        """
        Formatea dependencias para el prompt del LLM
        
        Args:
            dependencies: Dependencias estructuradas
            
        Returns:
            JSON string formateado para LLM
        """
        try:
            return json.dumps(dependencies, indent=2, ensure_ascii=False)
        except Exception:
            return str(dependencies)
    
    def _format_source_snippets_for_llm(self, all_snippets: List[Snippet], 
                                       dependencies: Dict[str, Any]) -> str:
        """
        Formatea snippets fuente relevantes para el LLM
        
        Args:
            all_snippets: Lista completa de snippets
            dependencies: Dependencias para filtrar snippets relevantes
            
        Returns:
            String formateado con snippets relevantes
        """
        relevant_indices = set()
        
        # Encontrar índices de snippets relevantes
        for category in ['variables', 'classes', 'imports', 'functions']:
            if category in dependencies:
                for item_info in dependencies[category].values():
                    snippet_idx = item_info.get('defined_in_snippet')
                    if snippet_idx is not None:
                        relevant_indices.add(snippet_idx)
        
        # Formatear snippets relevantes
        formatted_lines = []
        for idx in sorted(relevant_indices):
            if idx < len(all_snippets):
                snippet = all_snippets[idx]
                formatted_lines.append(f"## Snippet {idx}")
                formatted_lines.append(f"```python")
                formatted_lines.append(snippet.content)
                formatted_lines.append(f"```")
                formatted_lines.append("")
        
        return "\n".join(formatted_lines) if formatted_lines else "No relevant source snippets"
    
    def _parse_llm_context_response(self, llm_content: str) -> str:
        """
        Extrae el código de contexto de la respuesta del LLM
        
        Args:
            llm_content: Contenido de la respuesta del LLM
            
        Returns:
            Código de contexto extraído
        """
        # Buscar bloques de código Python
        python_blocks = re.findall(r'```python\s*(.*?)\s*```', llm_content, re.DOTALL)
        
        if python_blocks:
            return python_blocks[0].strip()
        
        # Si no hay bloques de código, buscar JSON con contexto optimizado
        json_match = re.search(r'\{.*"optimized_context".*\}', llm_content, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return data.get('optimized_context', '').strip()
            except json.JSONDecodeError:
                pass
        
        # Fallback: usar todo el contenido como código
        return llm_content.strip()
    
    async def analyze(self,
                     snippet: Snippet,
                     all_snippets: List[Snippet],
                     snippet_index: int,
                     dependencies: Optional[Dict[str, Any]] = None,
                     **kwargs) -> AgentResult:
        """
        Construye contexto optimizado para el snippet
        
        Args:
            snippet: Snippet objetivo que necesita contexto
            all_snippets: Lista completa de snippets
            snippet_index: Índice del snippet objetivo
            dependencies: Dependencias detectadas por Context Analyzer
            **kwargs: Argumentos adicionales
            
        Returns:
            AgentResult con contexto construido
        """
        start_time = time.time()
        self.logger.info("Starting context building")
        
        try:
            # Validar entradas
            self._validate_inputs(snippet, all_snippets, snippet_index)
            
            if not dependencies:
                # Sin dependencias, no hay contexto que construir
                return AgentResult(
                    success=True,
                    data=BuiltContext(
                        context_code="",
                        dependencies_included=[],
                        optimization_applied=False
                    ).dict(),
                    confidence=1.0,
                    processing_time=time.time() - start_time,
                    metadata={'method': 'no_dependencies'}
                )
            
            # Intentar construcción con LLM si está habilitado
            if self.enable_llm:
                try:
                    # Preparar prompt
                    dependencies_json = self._format_dependencies_for_llm(dependencies)
                    source_snippets = self._format_source_snippets_for_llm(all_snippets, dependencies)
                    
                    prompt = self.prompt_template.format(
                        target_snippet=snippet.content,
                        dependencies_json=dependencies_json,
                        source_snippets=source_snippets
                    )
                    
                    # Ejecutar LLM con timeout y retry
                    llm_response = await self._with_timeout_and_retry(
                        self.llm_client.generate(
                            prompt=prompt,
                            system_message="You are a Python context builder focused on minimal, safe code generation."
                        )
                    )
                    
                    # Parsear respuesta LLM
                    context_code = self._parse_llm_context_response(llm_response.content)
                    
                    # Validar contexto del LLM
                    safety_valid, safety_problems = self._validate_context_safety(context_code)
                    syntax_valid, syntax_error = self._validate_context_syntax(context_code)
                    
                    if safety_valid and syntax_valid:
                        # Contexto LLM válido
                        built_context = BuiltContext(
                            context_code=context_code,
                            dependencies_included=list(dependencies.keys()) if dependencies else [],
                            optimization_applied=True,
                            lines_count=len(context_code.split('\n')) if context_code else 0,
                            safety_validated=safety_valid,
                            syntax_valid=syntax_valid
                        )
                        
                        return AgentResult(
                            success=True,
                            data=built_context.dict(),
                            confidence=0.9,
                            processing_time=time.time() - start_time,
                            metadata={
                                'method': 'llm',
                                'llm_usage': llm_response.usage.dict(),
                                'cached': llm_response.cached
                            }
                        )
                    else:
                        # Contexto LLM inválido, usar fallback
                        logger.warning(f"LLM context invalid - Safety: {safety_valid}, Syntax: {syntax_valid}")
                        raise Exception("LLM generated invalid context")
                
                except Exception as llm_error:
                    logger.warning(f"LLM context building failed: {llm_error}, using heuristic fallback")
            
            # Fallback heurístico
            built_context = self._build_context_heuristic(
                snippet.content, dependencies, all_snippets
            )
            
            return AgentResult(
                success=True,
                data=built_context.dict(),
                confidence=0.7,  # Menor confianza para método heurístico
                processing_time=time.time() - start_time,
                metadata={'method': 'heuristic_fallback'}
            )
        
        except Exception as e:
            logger.error(f"Context building completely failed: {e}")
            return self._create_fallback_result(str(e))
    
    def get_builder_stats(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas del context builder
        
        Returns:
            Diccionario con estadísticas
        """
        if hasattr(self.llm_client, 'get_session_stats'):
            llm_stats = self.llm_client.get_session_stats()
        else:
            llm_stats = {}
        
        return {
            'agent': self.agent_name,
            'llm_enabled': self.enable_llm,
            'llm_stats': llm_stats,
            'dangerous_patterns': len(self.DANGEROUS_PATTERNS),
            'default_value_types': len(self.DEFAULT_VALUES)
        }

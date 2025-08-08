"""
Parser JSON Ultra-Robusto para respuestas de LLM
===============================================

Este módulo implementa múltiples estrategias para parsear JSON malformado
de respuestas de LLM, incluyendo limpieza automática, corrección de errores
comunes y fallbacks progresivos.
"""

import json
import re
import logging
from typing import Dict, Any, Optional, List, Union, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ParseResult:
    """Resultado del parsing JSON"""
    success: bool
    data: Dict[str, Any]
    method_used: str
    original_content: str
    cleaned_content: Optional[str] = None
    errors: List[str] = None
    
    def __post_init__(self):
        if self.errors is None:
            self.errors = []


class RobustJSONParser:
    """
    Parser JSON extremadamente robusto con múltiples estrategias de recuperación
    """
    
    def __init__(self):
        self.cleaning_strategies = [
            self._extract_json_blocks,
            self._fix_common_llm_errors,
            self._fix_trailing_commas,
            self._fix_quotes,
            self._fix_multiline_strings,
            self._fix_unescaped_chars,
            self._extract_partial_json,
            self._build_json_from_patterns
        ]
    
    def parse(self, content: str) -> ParseResult:
        """
        Intenta parsear JSON usando múltiples estrategias
        
        Args:
            content: Contenido a parsear
            
        Returns:
            ParseResult con el resultado del parsing
        """
        original_content = content.strip()
        
        # Estrategia 1: Parsing directo
        try:
            data = json.loads(original_content)
            return ParseResult(
                success=True,
                data=data,
                method_used="direct_parsing",
                original_content=original_content
            )
        except json.JSONDecodeError as e:
            logger.debug(f"Direct parsing failed: {e}")
        
        # Estrategias progresivas de limpieza
        for i, strategy in enumerate(self.cleaning_strategies):
            try:
                cleaned_content = strategy(original_content)
                if cleaned_content and cleaned_content != original_content:
                    
                    # Intentar parsear el contenido limpio
                    data = json.loads(cleaned_content)
                    return ParseResult(
                        success=True,
                        data=data,
                        method_used=f"strategy_{i+1}_{strategy.__name__}",
                        original_content=original_content,
                        cleaned_content=cleaned_content
                    )
                    
            except json.JSONDecodeError as e:
                logger.debug(f"Strategy {strategy.__name__} failed: {e}")
                continue
            except Exception as e:
                logger.debug(f"Strategy {strategy.__name__} error: {e}")
                continue
        
        # Estrategia final: JSON5 (más permisivo)
        try:
            import json5
            for strategy in self.cleaning_strategies[:4]:  # Usar solo las primeras estrategias
                try:
                    cleaned = strategy(original_content)
                    if cleaned:
                        data = json5.loads(cleaned)
                        return ParseResult(
                            success=True,
                            data=data,
                            method_used=f"json5_{strategy.__name__}",
                            original_content=original_content,
                            cleaned_content=cleaned
                        )
                except:
                    continue
        except ImportError:
            logger.warning("json5 not available for enhanced parsing")
        
        # Fallback: Estructura vacía válida
        return ParseResult(
            success=False,
            data={
                "variables": {},
                "classes": {},
                "imports": {},
                "functions": {},
                "overall_confidence": 0.0
            },
            method_used="fallback_empty",
            original_content=original_content,
            errors=["All parsing strategies failed"]
        )
    
    def _extract_json_blocks(self, content: str) -> str:
        """Extrae bloques JSON de respuestas con formato markdown"""
        # Patrón 1: Bloque ```json
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            return json_match.group(1).strip()
        
        # Patrón 2: Bloque ``` genérico
        json_match = re.search(r'```\s*(\{.*?\})\s*```', content, re.DOTALL)
        if json_match:
            return json_match.group(1).strip()
        
        # Patrón 3: Primer objeto JSON completo
        json_match = re.search(r'(\{.*?\})', content, re.DOTALL)
        if json_match:
            candidate = json_match.group(1).strip()
            if self._looks_like_json(candidate):
                return candidate
        
        return content
    
    def _fix_common_llm_errors(self, content: str) -> str:
        """Corrige errores comunes de LLMs"""
        # Remover texto explicativo antes y después
        patterns = [
            r'^[^{]*(\{.*\})[^}]*$',  # Extraer solo el objeto JSON
            r'(?:Here\'s the JSON|Here is the JSON|The JSON response is)[:\s]*(\{.*\})',
            r'(\{.*\})(?:\s*(?:This|That|The above).*)?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                break
        
        # Correcciones específicas
        corrections = [
            # Comillas simples a dobles
            (r"'([^']*)':", r'"\1":'),
            # True/False de Python a JSON
            (r'\bTrue\b', 'true'),
            (r'\bFalse\b', 'false'),
            (r'\bNone\b', 'null'),
            # Remover comentarios de línea
            (r'//.*$', '', re.MULTILINE),
            # Remover comentarios de bloque  
            (r'/\*.*?\*/', '', re.DOTALL),
        ]
        
        for pattern, replacement, *flags in corrections:
            flag = flags[0] if flags else 0
            content = re.sub(pattern, replacement, content, flags=flag)
        
        return content
    
    def _fix_trailing_commas(self, content: str) -> str:
        """Remueve comas finales que causan errores de JSON"""
        # Comas antes de } o ]
        content = re.sub(r',(\s*[}\]])', r'\1', content)
        
        # Comas al final de líneas antes de cerrar
        content = re.sub(r',(\s*\n\s*[}\]])', r'\1', content)
        
        return content
    
    def _fix_quotes(self, content: str) -> str:
        """Corrige problemas con comillas"""
        # Escapar comillas dentro de strings
        def fix_inner_quotes(match):
            key = match.group(1)
            value = match.group(2)
            # Escapar comillas dobles dentro del valor
            value = value.replace('"', '\\"')
            return f'"{key}": "{value}"'
        
        # Solo aplicar a strings obvios (no números o booleanos)
        content = re.sub(r'"([^"]+)":\s*"([^"]*(?:[^"\\][^"])*)"', fix_inner_quotes, content)
        
        return content
    
    def _fix_multiline_strings(self, content: str) -> str:
        """Convierte strings multilínea en strings de una línea"""
        def fix_multiline(match):
            key = match.group(1)
            value = match.group(2)
            # Convertir saltos de línea a \\n
            value = value.replace('\n', '\\n').replace('\r', '\\r')
            return f'"{key}": "{value}"'
        
        # Buscar strings que contengan saltos de línea
        pattern = r'"([^"]+)":\s*"([^"]*\n[^"]*)"'
        content = re.sub(pattern, fix_multiline, content, flags=re.DOTALL)
        
        return content
    
    def _fix_unescaped_chars(self, content: str) -> str:
        """Escapa caracteres especiales no escapados"""
        # Escapar backslashes no escapados
        content = re.sub(r'(?<!\\)\\(?!["\\/bfnrtu])', r'\\\\', content)
        
        # Escapar comillas no escapadas en strings
        def escape_quotes_in_strings(match):
            return match.group(0).replace('"', '\\"')
        
        return content
    
    def _extract_partial_json(self, content: str) -> str:
        """Intenta construir JSON válido de contenido parcial"""
        lines = content.split('\n')
        json_lines = []
        brace_count = 0
        in_json = False
        
        for line in lines:
            stripped = line.strip()
            
            if '{' in stripped:
                in_json = True
                brace_count += stripped.count('{')
                brace_count -= stripped.count('}')
                json_lines.append(line)
            elif in_json:
                brace_count += stripped.count('{')
                brace_count -= stripped.count('}')
                json_lines.append(line)
                
                if brace_count <= 0:
                    break
        
        if json_lines:
            partial_json = '\n'.join(json_lines)
            # Asegurar que termine con }
            if not partial_json.rstrip().endswith('}'):
                partial_json += '\n}'
            return partial_json
        
        return content
    
    def _build_json_from_patterns(self, content: str) -> str:
        """Como último recurso, construye JSON basado en patrones reconocidos"""
        result = {
            "variables": {},
            "classes": {},
            "imports": {},
            "functions": {},
            "overall_confidence": 0.0
        }
        
        # Patrones para extraer información
        patterns = {
            'variables': r'"([^"]+)":\s*\{\s*"defined_in_snippet":\s*(\d+)',
            'classes': r'"([^"]+)":\s*\{\s*"defined_in_snippet":\s*(\d+)',
            'imports': r'"([^"]+)":\s*\{\s*"defined_in_snippet":\s*(\d+)',
            'functions': r'"([^"]+)":\s*\{\s*"defined_in_snippet":\s*(\d+)'
        }
        
        for section, pattern in patterns.items():
            matches = re.findall(pattern, content)
            for name, snippet_index in matches:
                result[section][name] = {
                    "defined_in_snippet": int(snippet_index),
                    "confidence": 0.5
                }
        
        # Buscar confianza general
        conf_match = re.search(r'"overall_confidence":\s*([\d.]+)', content)
        if conf_match:
            try:
                result["overall_confidence"] = float(conf_match.group(1))
            except ValueError:
                pass
        
        return json.dumps(result, indent=2)
    
    def _looks_like_json(self, content: str) -> bool:
        """Verifica si el contenido parece ser JSON"""
        content = content.strip()
        return (
            content.startswith('{') and content.endswith('}') and
            '"' in content and ':' in content
        )
    
    def get_parsing_stats(self, results: List[ParseResult]) -> Dict[str, Any]:
        """Genera estadísticas de parsing de múltiples resultados"""
        if not results:
            return {}
        
        total = len(results)
        successful = len([r for r in results if r.success])
        
        methods_used = {}
        for result in results:
            method = result.method_used
            methods_used[method] = methods_used.get(method, 0) + 1
        
        return {
            'total_attempts': total,
            'successful_parses': successful,
            'success_rate': successful / total,
            'methods_breakdown': methods_used,
            'most_successful_method': max(methods_used.items(), key=lambda x: x[1])[0] if methods_used else None
        }


def create_robust_parser() -> RobustJSONParser:
    """Factory function para crear parser robusto"""
    return RobustJSONParser()


# Ejemplo de uso
if __name__ == "__main__":
    parser = RobustJSONParser()
    
    # Casos de prueba
    test_cases = [
        '```json\n{"variables": {"x": {"defined_in_snippet": 1}},}\n```',  # Trailing comma
        "{'variables': {'x': {'defined_in_snippet': 1}}}",  # Single quotes
        '{"variables": {"x": {"defined_in_snippet": 1, "definition": "x = "hello""}}}',  # Unescaped quotes
        'Here is the JSON: {"variables": {}}',  # With explanation text
    ]
    
    for i, test in enumerate(test_cases):
        result = parser.parse(test)
        print(f"Test {i+1}: {result.success} - {result.method_used}")

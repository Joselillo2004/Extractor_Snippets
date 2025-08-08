"""
Sistema de Filtrado de Precisión
==============================

Reduce falsos positivos mediante filtrado inteligente de dependencias
basado en análisis contextual, patrones de código y heurísticas específicas.
"""

import ast
import re
import logging
from typing import Dict, Any, List, Set, Optional, Tuple
from dataclasses import dataclass
from .base_agent import DependencyMap

logger = logging.getLogger(__name__)


@dataclass
class FilterRule:
    """Regla de filtrado con metadatos"""
    name: str
    description: str
    confidence_threshold: float
    applies_to: List[str]  # ['variables', 'classes', 'imports', 'functions']
    enabled: bool = True


class PrecisionFilter:
    """
    Sistema de filtrado inteligente para mejorar precisión
    """
    
    def __init__(self):
        self.builtin_names = self._load_python_builtins()
        self.common_patterns = self._load_common_patterns()
        self.filter_rules = self._initialize_filter_rules()
    
    def _load_python_builtins(self) -> Set[str]:
        """Carga nombres built-in de Python que no necesitan dependencias"""
        return {
            # Funciones built-in
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'classmethod', 'compile', 'complex', 'delattr',
            'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'filter',
            'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr',
            'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance',
            'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max',
            'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord',
            'pow', 'print', 'property', 'range', 'repr', 'reversed', 'round',
            'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum',
            'super', 'tuple', 'type', 'vars', 'zip',
            
            # Excepciones built-in
            'Exception', 'ValueError', 'TypeError', 'KeyError', 'IndexError',
            'AttributeError', 'ImportError', 'RuntimeError', 'StopIteration',
            
            # Constantes
            'True', 'False', 'None', '__name__', '__main__', '__debug__'
        }
    
    def _load_common_patterns(self) -> Dict[str, List[str]]:
        """Patrones comunes que suelen generar falsos positivos"""
        return {
            'loop_variables': ['i', 'j', 'k', 'idx', 'index', 'item', 'elem', 'x', 'y', 'z'],
            'temp_variables': ['temp', 'tmp', 'result', 'output', 'data', 'value', 'val'],
            'common_aliases': ['pd', 'np', 'plt', 'sns', 'tf', 'cv2', 'sk'],
            'dunder_methods': ['__init__', '__str__', '__repr__', '__len__', '__iter__'],
            'test_variables': ['test_', 'mock_', 'fake_', 'dummy_', 'sample_']
        }
    
    def _initialize_filter_rules(self) -> List[FilterRule]:
        """Inicializa reglas de filtrado"""
        return [
            FilterRule(
                name="builtin_filter",
                description="Filtra nombres built-in de Python",
                confidence_threshold=0.0,
                applies_to=['variables', 'functions']
            ),
            FilterRule(
                name="single_letter_variables",
                description="Filtra variables de una sola letra (probable loop vars)",
                confidence_threshold=0.7,
                applies_to=['variables']
            ),
            FilterRule(
                name="dunder_methods",
                description="Filtra métodos dunder comunes",
                confidence_threshold=0.8,
                applies_to=['functions']
            ),
            FilterRule(
                name="self_parameter",
                description="Filtra parámetro 'self' de métodos",
                confidence_threshold=0.0,
                applies_to=['variables']
            ),
            FilterRule(
                name="local_definitions",
                description="Filtra definiciones que están en el mismo snippet",
                confidence_threshold=0.9,
                applies_to=['variables', 'functions', 'classes']
            ),
            FilterRule(
                name="low_confidence",
                description="Filtra dependencias con confianza muy baja",
                confidence_threshold=0.3,
                applies_to=['variables', 'classes', 'imports', 'functions']
            )
        ]
    
    def filter_dependencies(self, 
                          dependency_map: DependencyMap, 
                          snippet_content: str,
                          context_analysis: Optional[Dict] = None) -> DependencyMap:
        """
        Aplica filtros para mejorar precisión
        
        Args:
            dependency_map: Mapa de dependencias original
            snippet_content: Contenido del snippet analizado
            context_analysis: Análisis adicional del contexto
            
        Returns:
            DependencyMap filtrado con mejor precisión
        """
        filtered_map = DependencyMap(
            variables={},
            classes={},
            imports={},
            functions={},
            confidence=dependency_map.confidence,
            error=dependency_map.error
        )
        
        # Análisis del snippet para identificar definiciones locales
        local_definitions = self._extract_local_definitions(snippet_content)
        
        # Filtrar cada categoría
        filtered_map.variables = self._filter_category(
            dependency_map.variables, 'variables', snippet_content, local_definitions
        )
        
        filtered_map.classes = self._filter_category(
            dependency_map.classes, 'classes', snippet_content, local_definitions
        )
        
        filtered_map.imports = self._filter_category(
            dependency_map.imports, 'imports', snippet_content, local_definitions
        )
        
        filtered_map.functions = self._filter_category(
            dependency_map.functions, 'functions', snippet_content, local_definitions
        )
        
        # Ajustar confianza basado en el filtrado
        original_count = sum(len(getattr(dependency_map, attr, {})) for attr in ['variables', 'classes', 'imports', 'functions'])
        filtered_count = sum(len(getattr(filtered_map, attr, {})) for attr in ['variables', 'classes', 'imports', 'functions'])
        
        if original_count > 0:
            filter_ratio = filtered_count / original_count
            # Si filtramos mucho, aumentamos la confianza (menos ruido)
            if filter_ratio < 0.7:
                filtered_map.confidence = min(1.0, filtered_map.confidence + 0.1)
        
        return filtered_map
    
    def _filter_category(self, 
                        items: Dict[str, Dict], 
                        category: str, 
                        snippet_content: str,
                        local_definitions: Set[str]) -> Dict[str, Dict]:
        """Filtra una categoría específica de dependencias"""
        filtered_items = {}
        
        for name, details in items.items():
            # Aplicar cada regla de filtrado
            keep_item = True
            filter_reason = None
            
            for rule in self.filter_rules:
                if not rule.enabled or category not in rule.applies_to:
                    continue
                
                should_filter, reason = self._apply_filter_rule(
                    rule, name, details, category, snippet_content, local_definitions
                )
                
                if should_filter:
                    keep_item = False
                    filter_reason = reason
                    break
            
            # Si sobrevive todos los filtros, mantenerlo
            if keep_item:
                filtered_items[name] = details
            else:
                logger.debug(f"Filtered {category} '{name}': {filter_reason}")
        
        return filtered_items
    
    def _apply_filter_rule(self, 
                          rule: FilterRule, 
                          name: str, 
                          details: Dict, 
                          category: str,
                          snippet_content: str,
                          local_definitions: Set[str]) -> Tuple[bool, str]:
        """
        Aplica una regla de filtrado específica
        
        Returns:
            Tuple de (should_filter, reason)
        """
        confidence = details.get('confidence', 0.5)
        
        if rule.name == "builtin_filter":
            if name in self.builtin_names:
                return True, f"Built-in Python name"
        
        elif rule.name == "single_letter_variables":
            if category == 'variables' and len(name) == 1 and confidence < rule.confidence_threshold:
                return True, f"Single letter variable with low confidence"
        
        elif rule.name == "dunder_methods":
            if category == 'functions' and name.startswith('__') and name.endswith('__'):
                if name in self.common_patterns['dunder_methods'] and confidence < rule.confidence_threshold:
                    return True, f"Common dunder method with low confidence"
        
        elif rule.name == "self_parameter":
            if category == 'variables' and name == 'self':
                return True, f"Method 'self' parameter"
        
        elif rule.name == "local_definitions":
            if name in local_definitions and confidence > rule.confidence_threshold:
                return True, f"Defined locally in same snippet"
        
        elif rule.name == "low_confidence":
            if confidence < rule.confidence_threshold:
                return True, f"Confidence too low ({confidence:.2f})"
        
        return False, ""
    
    def _extract_local_definitions(self, snippet_content: str) -> Set[str]:
        """
        Extrae nombres definidos localmente en el snippet
        """
        definitions = set()
        
        try:
            # Usar AST para análisis preciso
            tree = ast.parse(snippet_content)
            
            for node in ast.walk(tree):
                # Variables asignadas
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            definitions.add(target.id)
                
                # Funciones definidas
                elif isinstance(node, ast.FunctionDef):
                    definitions.add(node.name)
                
                # Clases definidas
                elif isinstance(node, ast.ClassDef):
                    definitions.add(node.name)
                
                # Imports
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        definitions.add(alias.asname or alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        definitions.add(alias.asname or alias.name)
                
                # Variables en list comprehensions, loops, etc.
                elif isinstance(node, (ast.For, ast.comprehension)):
                    if isinstance(node.target, ast.Name):
                        definitions.add(node.target.id)
        
        except SyntaxError:
            # Si hay errores de sintaxis, usar regex como fallback
            logger.debug("Using regex fallback for local definitions")
            
            # Patrones de definición
            patterns = [
                r'^(\w+)\s*=',  # Asignaciones
                r'^def\s+(\w+)',  # Definiciones de función
                r'^class\s+(\w+)',  # Definiciones de clase
                r'^import\s+(\w+)',  # Imports simples
                r'^from\s+\w+\s+import\s+(\w+)',  # From imports
            ]
            
            for line in snippet_content.split('\n'):
                line = line.strip()
                for pattern in patterns:
                    match = re.match(pattern, line)
                    if match:
                        definitions.add(match.group(1))
        
        return definitions
    
    def analyze_filter_effectiveness(self, 
                                   before: DependencyMap, 
                                   after: DependencyMap) -> Dict[str, Any]:
        """
        Analiza la efectividad del filtrado
        
        Returns:
            Estadísticas del filtrado aplicado
        """
        stats = {}
        
        for category in ['variables', 'classes', 'imports', 'functions']:
            before_items = getattr(before, category, {})
            after_items = getattr(after, category, {})
            
            before_count = len(before_items)
            after_count = len(after_items)
            filtered_count = before_count - after_count
            
            stats[category] = {
                'before_count': before_count,
                'after_count': after_count,
                'filtered_count': filtered_count,
                'filter_rate': filtered_count / before_count if before_count > 0 else 0,
                'filtered_items': list(set(before_items.keys()) - set(after_items.keys()))
            }
        
        # Estadísticas generales
        total_before = sum(stats[cat]['before_count'] for cat in stats)
        total_after = sum(stats[cat]['after_count'] for cat in stats)
        
        stats['overall'] = {
            'total_before': total_before,
            'total_after': total_after,
            'total_filtered': total_before - total_after,
            'overall_filter_rate': (total_before - total_after) / total_before if total_before > 0 else 0,
            'confidence_improvement': after.confidence - before.confidence
        }
        
        return stats
    
    def get_filter_recommendations(self, 
                                 dependency_map: DependencyMap,
                                 snippet_content: str) -> List[str]:
        """
        Genera recomendaciones para ajustar filtros basado en el análisis
        """
        recommendations = []
        
        # Analizar patrones en las dependencias encontradas
        all_names = []
        for category in ['variables', 'classes', 'imports', 'functions']:
            items = getattr(dependency_map, category, {})
            all_names.extend(items.keys())
        
        # Detectar patrones sospechosos
        builtin_count = sum(1 for name in all_names if name in self.builtin_names)
        single_letter_count = sum(1 for name in all_names if len(name) == 1)
        
        if builtin_count > 2:
            recommendations.append(
                f"Detecté {builtin_count} nombres built-in. "
                "Considera habilitar filtro más estricto para built-ins."
            )
        
        if single_letter_count > 3:
            recommendations.append(
                f"Muchas variables de una letra ({single_letter_count}). "
                "Podrían ser variables de loop que no necesitan dependencias."
            )
        
        # Analizar confianza promedio
        confidences = []
        for category in ['variables', 'classes', 'imports', 'functions']:
            items = getattr(dependency_map, category, {})
            confidences.extend(item.get('confidence', 0.5) for item in items.values())
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            if avg_confidence < 0.5:
                recommendations.append(
                    f"Confianza promedio baja ({avg_confidence:.2f}). "
                    "Considera aumentar el threshold de confianza mínima."
                )
        
        return recommendations
    
    def create_custom_filter_rule(self, 
                                name: str,
                                description: str,
                                filter_function: callable,
                                applies_to: List[str]) -> FilterRule:
        """
        Permite crear reglas de filtrado personalizadas
        
        Args:
            name: Nombre único de la regla
            description: Descripción de qué hace la regla
            filter_function: Función que toma (name, details, category) y retorna (should_filter, reason)
            applies_to: Lista de categorías a las que aplica
            
        Returns:
            FilterRule configurada
        """
        # Agregar la función personalizada a la clase
        setattr(self, f"_custom_filter_{name}", filter_function)
        
        rule = FilterRule(
            name=f"custom_{name}",
            description=description,
            confidence_threshold=0.5,
            applies_to=applies_to
        )
        
        self.filter_rules.append(rule)
        return rule


def create_precision_filter() -> PrecisionFilter:
    """Factory function para crear filtro de precisión"""
    return PrecisionFilter()


# Ejemplo de uso avanzado
if __name__ == "__main__":
    from .base_agent import DependencyMap
    
    # Crear filtro
    filter_system = PrecisionFilter()
    
    # Ejemplo de dependency map con ruido
    noisy_map = DependencyMap(
        variables={
            'i': {'confidence': 0.4, 'defined_in_snippet': None},  # Loop var
            'print': {'confidence': 0.8, 'defined_in_snippet': 0},  # Builtin
            'user_data': {'confidence': 0.9, 'defined_in_snippet': 1}  # Real dependency
        },
        functions={
            'len': {'confidence': 0.7, 'defined_in_snippet': None},  # Builtin
            'process_data': {'confidence': 0.85, 'defined_in_snippet': 2}  # Real
        },
        confidence=0.7
    )
    
    snippet = "for i in user_data:\n    print(len(process_data(i)))"
    
    # Aplicar filtros
    filtered_map = filter_system.filter_dependencies(noisy_map, snippet)
    
    print("Original dependencies:", len(noisy_map.variables) + len(noisy_map.functions))
    print("Filtered dependencies:", len(filtered_map.variables) + len(filtered_map.functions))
    print("Confidence improvement:", filtered_map.confidence - noisy_map.confidence)

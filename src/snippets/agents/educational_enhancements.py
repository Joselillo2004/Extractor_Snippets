#!/usr/bin/env python3
"""
Mejoras Educativas para el Sistema de Extracción de Snippets

Este módulo implementa mejoras específicas basadas en el análisis del archivo
de referencia Python para mejorar la extracción y contextualización de código educativo.
"""

import re
import ast
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .base_agent import Snippet, AgentResult


class EducationalLevel(Enum):
    """Niveles educativos de código"""
    BEGINNER = "beginner"      # Variables, tipos básicos, operadores
    INTERMEDIATE = "intermediate"  # Estructuras de control, funciones
    ADVANCED = "advanced"      # POO, manejo de errores, módulos
    EXPERT = "expert"         # Metaprogramación, decoradores avanzados


class CommentType(Enum):
    """Tipos de comentarios educativos"""
    EXPLANATION = "explanation"   # Comentarios que explican el código
    EXAMPLE = "example"          # Comentarios con ejemplos de uso
    OUTPUT = "output"            # Comentarios que muestran salida esperada
    WARNING = "warning"          # Comentarios de advertencia o precaución
    NOTE = "note"               # Notas adicionales
    TODO = "todo"               # Tareas pendientes


@dataclass
class EducationalContext:
    """Contexto educativo de un snippet"""
    level: EducationalLevel
    topics: List[str]
    prerequisites: List[str]
    difficulty_score: float
    has_examples: bool
    has_explanations: bool
    comment_quality: float
    

class CommentContextDetector:
    """Detecta y contextualiza comentarios explicativos en código educativo"""
    
    def __init__(self):
        # Patrones para identificar diferentes tipos de comentarios
        self.comment_patterns = {
            CommentType.EXPLANATION: [
                r"#\s*[Ee]sta?\s+(es|función|método)",
                r"#\s*[Aa]quí",
                r"#\s*[Ll]a\s+siguiente",
                r"#\s*[Ee]sto\s+(hace|sirve|es)",
                r"#\s*[Pp]ara\s+",
                r"#\s*[Cc]on\s+este",
            ],
            CommentType.EXAMPLE: [
                r"#\s*[Ee]jemplo",
                r"#\s*[Pp]or\s+ejemplo",
                r"#\s*[Cc]omo\s+este",
                r"#\s*[Uu]so:",
            ],
            CommentType.OUTPUT: [
                r"#\s*[Rr]esultado:",
                r"#\s*[Ss]alida:",
                r"#\s*[Oo]utput:",
                r"#\s*[Dd]evuelve:",
                r"#\s*[Ii]mprime:",
                r"#\s*\s*\[.*\]",  # Listas como output
                r"#\s*\s*\{.*\}",  # Diccionarios como output
            ],
            CommentType.WARNING: [
                r"#\s*[Cc]uidado",
                r"#\s*[Aa]tención",
                r"#\s*[Nn][Oo][Tt][Aa]:",
                r"#\s*[Ii]mportante",
                r"#\s*[Nn]o\s+se\s+puede",
            ]
        }
        
        # Patrones para detectar conceptos educativos
        self.concept_patterns = {
            'variables': [r'\w+\s*=\s*', r'variable', r'valor'],
            'functions': [r'def\s+\w+', r'función', r'función'],
            'classes': [r'class\s+\w+', r'clase', r'objeto'],
            'loops': [r'for\s+\w+\s+in', r'while', r'bucle', r'iteración'],
            'conditionals': [r'if\s+', r'elif', r'else', r'condicional'],
            'lists': [r'\[.*\]', r'lista', r'append', r'índice'],
            'dictionaries': [r'\{.*\}', r'diccionario', r'clave', r'valor'],
            'strings': [r'["\'].*["\']', r'cadena', r'string', r'texto'],
            'imports': [r'import\s+', r'from\s+.*\s+import', r'módulo'],
        }
    
    def detect_educational_comments(self, content: str) -> Dict[str, Any]:
        """Detecta y analiza comentarios educativos en el contenido"""
        lines = content.split('\n')
        comments = []
        comment_analysis = {
            'total_comments': 0,
            'educational_comments': 0,
            'comment_types': {},
            'comment_quality_score': 0.0,
            'has_examples': False,
            'has_explanations': False,
            'explanation_ratio': 0.0
        }
        
        for i, line in enumerate(lines):
            # Buscar comentarios
            comment_match = re.search(r'#(.+)', line.strip())
            if comment_match:
                comment_text = comment_match.group(1).strip()
                comment_type = self._classify_comment(comment_text)
                
                comments.append({
                    'line': i + 1,
                    'text': comment_text,
                    'type': comment_type,
                    'is_educational': comment_type != CommentType.TODO
                })
                
                comment_analysis['total_comments'] += 1
                if comment_type != CommentType.TODO:
                    comment_analysis['educational_comments'] += 1
                
                # Actualizar estadísticas por tipo
                type_name = comment_type.value if comment_type else 'unknown'
                comment_analysis['comment_types'][type_name] = \
                    comment_analysis['comment_types'].get(type_name, 0) + 1
        
        # Calcular métricas de calidad
        if comment_analysis['total_comments'] > 0:
            comment_analysis['explanation_ratio'] = (
                comment_analysis['educational_comments'] / 
                comment_analysis['total_comments']
            )
        
        comment_analysis['has_examples'] = CommentType.EXAMPLE.value in comment_analysis['comment_types']
        comment_analysis['has_explanations'] = CommentType.EXPLANATION.value in comment_analysis['comment_types']
        
        # Calcular score de calidad (0-10)
        quality_factors = [
            comment_analysis['explanation_ratio'] * 3,  # 30% peso
            (1 if comment_analysis['has_explanations'] else 0) * 2,  # 20% peso
            (1 if comment_analysis['has_examples'] else 0) * 2,  # 20% peso
            min(comment_analysis['educational_comments'] / 5, 1) * 3  # 30% peso
        ]
        comment_analysis['comment_quality_score'] = sum(quality_factors)
        
        return comment_analysis
    
    def _classify_comment(self, comment_text: str) -> Optional[CommentType]:
        """Clasifica un comentario según su contenido"""
        for comment_type, patterns in self.comment_patterns.items():
            for pattern in patterns:
                if re.search(pattern, comment_text, re.IGNORECASE):
                    return comment_type
        
        return None
    
    def detect_educational_concepts(self, content: str) -> List[str]:
        """Detecta conceptos educativos presentes en el código"""
        concepts = []
        
        for concept, patterns in self.concept_patterns.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    if concept not in concepts:
                        concepts.append(concept)
                    break
        
        return concepts


class EducationalSnippetClassifier:
    """Clasificador de snippets por nivel educativo y temas"""
    
    def __init__(self):
        self.comment_detector = CommentContextDetector()
        
        # Criterios para determinar nivel educativo
        self.level_indicators = {
            EducationalLevel.BEGINNER: {
                'required_concepts': ['variables'],
                'forbidden_concepts': ['classes', 'decorators', 'exceptions'],
                'max_complexity': 3,
                'typical_concepts': ['variables', 'strings', 'numbers', 'print']
            },
            EducationalLevel.INTERMEDIATE: {
                'required_concepts': ['functions', 'loops'],
                'forbidden_concepts': ['decorators', 'metaclasses'],
                'max_complexity': 6,
                'typical_concepts': ['functions', 'loops', 'conditionals', 'lists', 'dictionaries']
            },
            EducationalLevel.ADVANCED: {
                'required_concepts': ['classes'],
                'forbidden_concepts': [],
                'max_complexity': 9,
                'typical_concepts': ['classes', 'inheritance', 'exceptions', 'modules']
            },
            EducationalLevel.EXPERT: {
                'required_concepts': ['decorators', 'metaclasses'],
                'forbidden_concepts': [],
                'max_complexity': 10,
                'typical_concepts': ['decorators', 'metaclasses', 'descriptors', 'context_managers']
            }
        }
    
    def classify_snippet(self, snippet: Snippet) -> EducationalContext:
        """Clasifica un snippet según criterios educativos"""
        content = snippet.content
        
        # Detectar comentarios educativos
        comment_analysis = self.comment_detector.detect_educational_comments(content)
        
        # Detectar conceptos presentes
        concepts = self.comment_detector.detect_educational_concepts(content)
        
        # Determinar nivel educativo
        level = self._determine_educational_level(content, concepts)
        
        # Calcular dificultad
        difficulty = self._calculate_difficulty_score(content, concepts, comment_analysis)
        
        # Determinar prerequisitos
        prerequisites = self._determine_prerequisites(concepts, level)
        
        return EducationalContext(
            level=level,
            topics=concepts,
            prerequisites=prerequisites,
            difficulty_score=difficulty,
            has_examples=comment_analysis['has_examples'],
            has_explanations=comment_analysis['has_explanations'],
            comment_quality=comment_analysis['comment_quality_score']
        )
    
    def _determine_educational_level(self, content: str, concepts: List[str]) -> EducationalLevel:
        """Determina el nivel educativo basado en conceptos y complejidad"""
        # Calcular complejidad del código
        complexity = self._calculate_code_complexity(content)
        
        # Evaluar cada nivel
        for level, criteria in self.level_indicators.items():
            # Verificar conceptos requeridos
            if all(req in concepts for req in criteria['required_concepts']):
                # Verificar conceptos prohibidos
                if not any(forb in concepts for forb in criteria['forbidden_concepts']):
                    # Verificar complejidad
                    if complexity <= criteria['max_complexity']:
                        return level
        
        # Por defecto, retornar intermedio
        return EducationalLevel.INTERMEDIATE
    
    def _calculate_code_complexity(self, content: str) -> int:
        """Calcula la complejidad del código usando métricas simples"""
        complexity = 0
        
        # Contar estructuras de control
        complexity += len(re.findall(r'\bif\b', content))
        complexity += len(re.findall(r'\bfor\b', content))
        complexity += len(re.findall(r'\bwhile\b', content))
        complexity += len(re.findall(r'\btry\b', content))
        
        # Contar definiciones
        complexity += len(re.findall(r'\bdef\s+', content))
        complexity += len(re.findall(r'\bclass\s+', content))
        
        # Contar anidamiento (aproximado)
        lines = content.split('\n')
        max_indent = 0
        for line in lines:
            if line.strip():
                indent = len(line) - len(line.lstrip())
                max_indent = max(max_indent, indent // 4)  # Asumiendo 4 espacios por nivel
        
        complexity += max_indent
        
        return complexity
    
    def _calculate_difficulty_score(self, content: str, concepts: List[str], 
                                  comment_analysis: Dict[str, Any]) -> float:
        """Calcula un score de dificultad (1-10)"""
        base_difficulty = len(concepts) * 0.5
        complexity_penalty = self._calculate_code_complexity(content) * 0.3
        comment_bonus = comment_analysis['comment_quality_score'] * 0.2
        
        # Penalizaciones por conceptos avanzados
        advanced_concepts = {'classes', 'inheritance', 'decorators', 'exceptions', 'metaclasses'}
        advanced_penalty = len(set(concepts) & advanced_concepts) * 0.8
        
        difficulty = base_difficulty + complexity_penalty + advanced_penalty - comment_bonus
        
        return max(1.0, min(10.0, difficulty))
    
    def _determine_prerequisites(self, concepts: List[str], level: EducationalLevel) -> List[str]:
        """Determina prerequisitos basados en conceptos y nivel"""
        prerequisites = []
        
        # Prerequisitos por concepto
        concept_prereqs = {
            'functions': ['variables', 'basic_types'],
            'classes': ['functions', 'variables', 'basic_types'],
            'inheritance': ['classes'],
            'loops': ['conditionals', 'variables'],
            'dictionaries': ['variables', 'basic_types'],
            'lists': ['variables', 'basic_types'],
            'exceptions': ['functions', 'conditionals']
        }
        
        for concept in concepts:
            if concept in concept_prereqs:
                prerequisites.extend(concept_prereqs[concept])
        
        # Remover duplicados y conceptos ya presentes
        prerequisites = list(set(prerequisites) - set(concepts))
        
        return prerequisites


class OOPPatternDetector:
    """Detecta patrones de programación orientada a objetos"""
    
    def detect_class_relationships(self, all_snippets: List[Snippet]) -> Dict[str, Any]:
        """Detecta relaciones entre clases en múltiples snippets"""
        classes = {}
        inheritance_chains = []
        method_overrides = []
        
        for snippet in all_snippets:
            snippet_classes = self._extract_classes(snippet.content)
            classes.update(snippet_classes)
        
        # Detectar herencia
        for class_name, class_info in classes.items():
            if class_info['parent']:
                inheritance_chains.append({
                    'child': class_name,
                    'parent': class_info['parent'],
                    'snippet_index': class_info['snippet_index']
                })
        
        # Detectar sobreescritura de métodos
        for chain in inheritance_chains:
            child_methods = classes[chain['child']]['methods']
            if chain['parent'] in classes:
                parent_methods = classes[chain['parent']]['methods']
                
                common_methods = set(child_methods) & set(parent_methods)
                if common_methods:
                    method_overrides.extend([
                        {
                            'method': method,
                            'child_class': chain['child'],
                            'parent_class': chain['parent']
                        }
                        for method in common_methods
                    ])
        
        return {
            'classes': classes,
            'inheritance_chains': inheritance_chains,
            'method_overrides': method_overrides,
            'has_inheritance': len(inheritance_chains) > 0,
            'has_polymorphism': len(method_overrides) > 0
        }
    
    def _extract_classes(self, content: str) -> Dict[str, Dict[str, Any]]:
        """Extrae información de clases del contenido"""
        classes = {}
        
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    parent = None
                    if node.bases:
                        # Tomar solo el primer padre (herencia simple)
                        if isinstance(node.bases[0], ast.Name):
                            parent = node.bases[0].id
                    
                    methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
                    
                    classes[node.name] = {
                        'parent': parent,
                        'methods': methods,
                        'line': node.lineno,
                        'snippet_index': None  # Se asignará externamente
                    }
        
        except SyntaxError:
            # Si no se puede parsear, usar regex básico
            class_matches = re.findall(r'class\s+(\w+)(?:\s*\(\s*(\w+)\s*\))?:', content)
            for match in class_matches:
                class_name, parent = match
                classes[class_name] = {
                    'parent': parent if parent else None,
                    'methods': [],
                    'line': 0,
                    'snippet_index': None
                }
        
        return classes


# Ejemplo de uso y testing
if __name__ == "__main__":
    # Test con un snippet del archivo de referencia
    test_snippet = Snippet("""
# Ingreso por teclado básico
print("Ingresa tu nombre:")
numero = input()

# Los ingresos siempre son cadenas que tienen que convertidas a números:
float(numero) + 5
    """, 0)
    
    classifier = EducationalSnippetClassifier()
    context = classifier.classify_snippet(test_snippet)
    
    print(f"Nivel educativo: {context.level.value}")
    print(f"Temas: {context.topics}")
    print(f"Prerequisitos: {context.prerequisites}")
    print(f"Dificultad: {context.difficulty_score:.2f}")
    print(f"Tiene ejemplos: {context.has_examples}")
    print(f"Tiene explicaciones: {context.has_explanations}")
    print(f"Calidad de comentarios: {context.comment_quality:.2f}")

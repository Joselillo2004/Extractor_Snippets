#!/usr/bin/env python3
"""
Agente para generar descripciones mejoradas de snippets basándose en análisis de código
"""
import re
import ast
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .base_agent import BaseAgent, Snippet, AgentResult


@dataclass
class DescriptionAnalysis:
    """Resultado del análisis para generar descripciones"""
    main_purpose: str
    key_concepts: List[str]
    complexity_level: str
    input_output: Tuple[Optional[str], Optional[str]]
    code_patterns: List[str]
    educational_value: str


class DescriptionEnhancerAgent:
    """Agente especializado en generar descripciones mejoradas de snippets"""
    
    def __init__(self):
        self.patterns = self._init_patterns()
    
    def _init_patterns(self) -> Dict[str, List[str]]:
        """Inicializa patrones de código comunes"""
        return {
            'input_output': [
                r'input\s*\(',
                r'print\s*\(',
                r'return\s+',
                r'yield\s+',
            ],
            'data_structures': [
                r'\[\s*\]',  # listas vacías
                r'\{\s*\}',  # diccionarios vacíos
                r'\.append\s*\(',
                r'\.extend\s*\(',
                r'\.update\s*\(',
                r'\.keys\s*\(\)',
                r'\.values\s*\(\)',
                r'\.items\s*\(\)',
            ],
            'control_flow': [
                r'\bfor\s+\w+\s+in\b',
                r'\bwhile\s+',
                r'\bif\s+',
                r'\belif\s+',
                r'\belse\s*:',
                r'\btry\s*:',
                r'\bexcept\s+',
                r'\bfinally\s*:',
            ],
            'string_formatting': [
                r'\.format\s*\(',
                r'f["\']',  # f-strings
                r'%[sd]',   # old style formatting
                r'\{:\w*\}',  # format specifications
            ],
            'functions': [
                r'\bdef\s+\w+\s*\(',
                r'\blambda\s+',
                r'@\w+',  # decorators
            ],
            'classes': [
                r'\bclass\s+\w+',
                r'\bself\.',
                r'__init__',
                r'__str__',
                r'__repr__',
            ]
        }
    
    def analyze_code(self, content: str) -> DescriptionAnalysis:
        """Analiza el código para extraer información descriptiva"""
        lines = content.strip().split('\n')
        
        # Análisis de propósito principal
        main_purpose = self._identify_main_purpose(content, lines)
        
        # Conceptos clave
        key_concepts = self._extract_key_concepts(content)
        
        # Nivel de complejidad
        complexity_level = self._assess_complexity(content, lines)
        
        # Input/Output
        input_output = self._analyze_input_output(content)
        
        # Patrones de código
        code_patterns = self._identify_patterns(content)
        
        # Valor educativo
        educational_value = self._assess_educational_value(content, key_concepts)
        
        return DescriptionAnalysis(
            main_purpose=main_purpose,
            key_concepts=key_concepts,
            complexity_level=complexity_level,
            input_output=input_output,
            code_patterns=code_patterns,
            educational_value=educational_value
        )
    
    def _identify_main_purpose(self, content: str, lines: List[str]) -> str:
        """Identifica el propósito principal del código"""
        content_lower = content.lower()
        
        # Patrones específicos de propósito
        if 'input(' in content and 'print(' in content:
            if 'for' in content_lower or 'while' in content_lower:
                return "Interacción usuario con bucles"
            return "Interacción básica con usuario"
        
        if '.format(' in content or 'f"' in content or "f'" in content:
            return "Formateo de strings"
        
        if any(pattern in content for pattern in ['.append(', '.extend(', '[]']):
            return "Manipulación de listas"
        
        if any(pattern in content for pattern in ['{', 'dict(', '.keys(', '.values()']):
            return "Trabajo con diccionarios"
        
        if 'def ' in content:
            return "Definición de función"
        
        if 'class ' in content:
            return "Definición de clase"
        
        if any(loop in content_lower for loop in ['for ', 'while ']):
            return "Estructuras de control iterativas"
        
        if any(cond in content_lower for cond in ['if ', 'elif ', 'else:']):
            return "Estructuras de control condicionales"
        
        if 'import ' in content or 'from ' in content:
            return "Importación de módulos"
        
        # Si solo tiene print
        if 'print(' in content and len(lines) <= 3:
            return "Salida simple de datos"
        
        return "Operaciones básicas de Python"
    
    def _extract_key_concepts(self, content: str) -> List[str]:
        """Extrae conceptos clave del código"""
        concepts = []
        content_lower = content.lower()
        
        # Tipos de datos
        if any(pattern in content for pattern in ['[]', '.append(', '.extend(']):
            concepts.append('listas')
        if any(pattern in content for pattern in ['{}', 'dict(', '.keys(', '.values()']):
            concepts.append('diccionarios')
        if any(pattern in content for pattern in ['str(', '""', "''"]):
            concepts.append('strings')
        if any(pattern in content for pattern in ['int(', 'float(', '+', '-', '*', '/']):
            concepts.append('números')
        
        # Estructuras de control
        if 'for ' in content_lower:
            concepts.append('bucles-for')
        if 'while ' in content_lower:
            concepts.append('bucles-while')
        if any(cond in content_lower for cond in ['if ', 'elif ']):
            concepts.append('condicionales')
        
        # Funcionalidades
        if 'input(' in content:
            concepts.append('entrada-usuario')
        if 'print(' in content:
            concepts.append('salida-datos')
        if '.format(' in content or 'f"' in content or "f'" in content:
            concepts.append('formateo-strings')
        if 'def ' in content:
            concepts.append('funciones')
        if 'class ' in content:
            concepts.append('clases')
        if 'import ' in content or 'from ' in content:
            concepts.append('módulos')
        
        return concepts
    
    def _assess_complexity(self, content: str, lines: List[str]) -> str:
        """Evalúa el nivel de complejidad del código"""
        complexity_score = 0
        
        # Factores que aumentan complejidad
        complexity_score += len(re.findall(r'\bfor\s+\w+\s+in\b', content)) * 2
        complexity_score += len(re.findall(r'\bwhile\s+', content)) * 2
        complexity_score += len(re.findall(r'\bif\s+', content)) * 1
        complexity_score += len(re.findall(r'\bdef\s+\w+', content)) * 3
        complexity_score += len(re.findall(r'\bclass\s+\w+', content)) * 4
        complexity_score += len(re.findall(r'\btry\s*:', content)) * 2
        complexity_score += len(re.findall(r'\.format\s*\(', content)) * 1
        
        # Longitud del código
        complexity_score += len(lines) // 5
        
        if complexity_score <= 2:
            return "muy-facil"
        elif complexity_score <= 5:
            return "facil"
        elif complexity_score <= 10:
            return "intermedio"
        else:
            return "avanzado"
    
    def _analyze_input_output(self, content: str) -> Tuple[Optional[str], Optional[str]]:
        """Analiza las entradas y salidas del código"""
        input_type = None
        output_type = None
        
        if 'input(' in content:
            if 'int(input(' in content:
                input_type = "números"
            elif 'float(input(' in content:
                input_type = "decimales"
            else:
                input_type = "texto"
        
        if 'print(' in content:
            # Analizar qué se imprime
            print_matches = re.findall(r'print\s*\([^)]+\)', content)
            if print_matches:
                if any('format' in match for match in print_matches):
                    output_type = "texto-formateado"
                elif any('"' in match or "'" in match for match in print_matches):
                    output_type = "texto"
                else:
                    output_type = "variables"
        
        return (input_type, output_type)
    
    def _identify_patterns(self, content: str) -> List[str]:
        """Identifica patrones de código presentes"""
        patterns = []
        
        for pattern_category, pattern_list in self.patterns.items():
            for pattern in pattern_list:
                if re.search(pattern, content):
                    patterns.append(pattern_category.replace('_', '-'))
                    break  # Solo agregar la categoría una vez
        
        return patterns
    
    def _assess_educational_value(self, content: str, concepts: List[str]) -> str:
        """Evalúa el valor educativo del snippet"""
        if len(concepts) >= 4:
            return "ejemplo-completo"
        elif len(concepts) >= 2:
            return "ejemplo-integrado"
        elif any(concept in ['funciones', 'clases', 'módulos'] for concept in concepts):
            return "concepto-avanzado"
        else:
            return "concepto-básico"
    
    def generate_enhanced_description(self, snippet: Snippet) -> str:
        """Genera una descripción mejorada basada en el análisis del código"""
        analysis = self.analyze_code(snippet.content)
        
        # Construir descripción descriptiva
        description_parts = []
        
        # Propósito principal
        description_parts.append(analysis.main_purpose.replace('-', ' ').title())
        
        # Detalles específicos basados en input/output
        input_type, output_type = analysis.input_output
        if input_type and output_type:
            description_parts.append(f"(entrada: {input_type}, salida: {output_type})")
        elif input_type:
            description_parts.append(f"(entrada: {input_type})")
        elif output_type:
            description_parts.append(f"(salida: {output_type})")
        
        # Conceptos clave destacados
        if len(analysis.key_concepts) > 0:
            key_concepts_str = ", ".join(analysis.key_concepts[:3])  # Top 3 conceptos
            description_parts.append(f"- {key_concepts_str}")
        
        # Nivel educativo
        if analysis.educational_value != "concepto-básico":
            description_parts.append(f"[{analysis.educational_value.replace('-', ' ')}]")
        
        return " ".join(description_parts)
    
    def process(self, snippets: List[Snippet]) -> List[Dict]:
        """Procesa snippets y genera descripciones mejoradas"""
        results = []
        
        for snippet in snippets:
            try:
                enhanced_description = self.generate_enhanced_description(snippet)
                analysis = self.analyze_code(snippet.content)
                
                result = {
                    'original_index': snippet.index,
                    'original_content': snippet.content,
                    'enhanced_description': enhanced_description,
                    'analysis': analysis,
                    'complexity': analysis.complexity_level,
                    'key_concepts': analysis.key_concepts,
                    'patterns': analysis.code_patterns
                }
                results.append(result)
                
            except Exception as e:
                print(f"Error procesando snippet {snippet.index}: {e}")
                continue
        
        return results

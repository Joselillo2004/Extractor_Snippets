#!/usr/bin/env python3
"""
Script para extraer snippets educativos del archivo 'Referencia Python.py'
y exportarlos automáticamente a 'the-way'.

Este script utiliza todas las mejoras desarrolladas:
- Detector de comentarios educativos
- Clasificación por niveles educativos
- Detección de patrones POO
- Análisis de conceptos Python
- Filtrado inteligente de calidad
"""

import subprocess
import json
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Any

# Imports del sistema desarrollado
from src.snippets.parser import parse_snippets, Snippet
from src.snippets.agents.educational_enhancements import (
    CommentContextDetector,
    EducationalSnippetClassifier,
    OOPPatternDetector
)

def create_base_snippet(parser_snippet):
    """Convierte un snippet del parser a uno compatible con base_agent"""
    # Crear snippet compatible con el formato esperado por las mejoras educativas
    from src.snippets.agents.base_agent import Snippet as BaseSnippet
    return BaseSnippet(
        content=parser_snippet.content,
        index=parser_snippet.index,
        line_start=parser_snippet.start_line,
        line_end=parser_snippet.end_line
    )

class TheWayExporter:
    """Exportador de snippets a the-way con mejoras educativas"""
    
    def __init__(self):
        self.comment_detector = CommentContextDetector()
        self.educational_classifier = EducationalSnippetClassifier()
        self.oop_detector = OOPPatternDetector()
    
    def clean_snippet_description(self, snippet_content: str, comments: dict) -> str:
        """Genera una descripción limpia del snippet basada en comentarios educativos"""
        lines = snippet_content.strip().split('\n')
        
        # Extraer comentarios educativos - verificar que sea una lista
        educational_comments = []
        comment_list = comments.get('educational_comments', [])
        
        # Si educational_comments es un int, no es una lista válida
        if isinstance(comment_list, (list, tuple)):
            for comment in comment_list:
                if isinstance(comment, dict) and comment.get('type') in ['explanation', 'example', 'concept']:
                    educational_comments.append(comment.get('content', ''))
        
        # Si hay comentarios educativos, usarlos
        if educational_comments:
            return ' | '.join(educational_comments[:2])  # Máximo 2 comentarios
        
        # Generar descripción automática basada en el código
        first_line = lines[0].strip()
        if first_line.startswith('def '):
            func_name = re.search(r'def\s+(\w+)', first_line)
            if func_name:
                return f"Función: {func_name.group(1)}"
        elif first_line.startswith('class '):
            class_name = re.search(r'class\s+(\w+)', first_line)
            if class_name:
                return f"Clase: {class_name.group(1)}"
        elif any(keyword in first_line for keyword in ['for', 'while']):
            return "Ejemplo de bucle"
        elif 'if' in first_line:
            return "Ejemplo condicional"
        else:
            return "Snippet de código Python"
    
    def generate_tags(self, educational_data: dict, concepts: List[str]) -> List[str]:
        """Genera tags inteligentes basados en el análisis educativo"""
        tags = set()
        
        # Tag de nivel educativo
        level = educational_data.get('educational_level', 'beginner')
        tags.add(f"nivel-{level}")
        
        # Tags de conceptos
        for concept in concepts:
            tags.add(f"concepto-{concept}")
        
        # Tags de dificultad
        difficulty = educational_data.get('difficulty', 0)
        if difficulty < 2:
            tags.add("facil")
        elif difficulty < 5:
            tags.add("intermedio")
        else:
            tags.add("avanzado")
        
        # Tags especiales
        if educational_data.get('has_explanations'):
            tags.add("explicado")
        if educational_data.get('has_examples'):
            tags.add("con-ejemplos")
        
        # Tags de POO si es relevante
        if 'classes' in concepts:
            tags.add("poo")
            if educational_data.get('has_inheritance'):
                tags.add("herencia")
            if educational_data.get('has_polymorphism'):
                tags.add("polimorfismo")
        
        return list(tags)
    
    def filter_quality_snippets(self, snippets_data: List[dict]) -> List[dict]:
        """Filtra snippets basándose en criterios de calidad educativa"""
        quality_snippets = []
        
        for snippet_data in snippets_data:
            snippet = snippet_data['snippet']
            educational_data = snippet_data['educational_data']
            
            # Criterios de filtrado
            min_lines = 2
            max_lines = 50
            min_quality_score = 1.5
            
            # Verificar longitud
            lines = len(snippet.content.strip().split('\n'))
            if lines < min_lines or lines > max_lines:
                continue
            
            # Verificar calidad de comentarios
            comment_quality = educational_data.get('comment_quality', 0)
            if comment_quality < min_quality_score:
                continue
            
            # Filtrar snippets muy simples o vacíos
            content = snippet.content.strip()
            if (len(content) < 20 or 
                content.count('\n') == 0 or
                not re.search(r'[a-zA-Z_]\w*\s*[=():]', content)):
                continue
            
            # Verificar que tenga conceptos relevantes
            concepts = snippet_data.get('concepts', [])
            if not concepts:
                continue
            
            quality_snippets.append(snippet_data)
        
        return quality_snippets
    
    def export_snippet_to_theway(self, snippet_data: dict) -> bool:
        """Exporta un snippet individual a the-way"""
        try:
            snippet = snippet_data['snippet']
            educational_data = snippet_data['educational_data']
            concepts = snippet_data.get('concepts', [])
            
            # Generar metadatos
            description = self.clean_snippet_description(snippet.content, snippet_data.get('comments', {}))
            tags = self.generate_tags(educational_data, concepts)
            
            # Crear archivo temporal con el snippet
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                temp_file.write(snippet.content)
                temp_file_path = temp_file.name
            
            # Construir comando the-way
            cmd = [
                'the-way',
                'new',
                temp_file_path,
                '--description', description,
                '--language', 'python'
            ]
            
            # Agregar tags
            for tag in tags:
                cmd.extend(['--tag', tag])
            
            # Ejecutar comando
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Limpiar archivo temporal
            Path(temp_file_path).unlink()
            
            if result.returncode == 0:
                print(f"✅ Snippet exportado: {description}")
                return True
            else:
                print(f"❌ Error exportando snippet: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción exportando snippet: {e}")
            return False
    
    def process_reference_file(self, file_path: str) -> Dict[str, Any]:
        """Procesa el archivo de referencia completo"""
        print(f"📄 Procesando archivo: {file_path}")
        
        # Leer archivo
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ Archivo leído: {len(content):,} caracteres")
        
        # Extraer snippets básicos usando el parser
        basic_snippets = parse_snippets(file_path, strict=False)
        print(f"✅ Snippets básicos extraídos: {len(basic_snippets)}")
        
        # Analizar comentarios del archivo completo
        file_comments = self.comment_detector.detect_educational_comments(content)
        print(f"📊 Comentarios analizados: {file_comments['total_comments']}")
        
        # Detectar conceptos del archivo completo
        file_concepts = self.comment_detector.detect_educational_concepts(content)
        print(f"🎯 Conceptos detectados: {', '.join(file_concepts)}")
        
        # Procesar snippets individuales
        snippets_data = []
        processed = 0
        
        for snippet in basic_snippets:
            if len(snippet.content.strip()) < 10:  # Skip snippets muy pequeños
                continue
            
            # Análisis educativo del snippet
            snippet_comments = self.comment_detector.detect_educational_comments(snippet.content)
            snippet_concepts = self.comment_detector.detect_educational_concepts(snippet.content)
            educational_context = self.educational_classifier.classify_snippet(snippet)
            
            # Convertir EducationalContext a dict
            educational_data = {
                'educational_level': educational_context.level.value,
                'difficulty': educational_context.difficulty_score,
                'comment_quality': educational_context.comment_quality,
                'has_explanations': educational_context.has_explanations,
                'has_examples': educational_context.has_examples,
            }
            
            snippets_data.append({
                'snippet': snippet,
                'comments': snippet_comments,
                'concepts': snippet_concepts,
                'educational_data': educational_data
            })
            
            processed += 1
            if processed % 100 == 0:
                print(f"📈 Procesados: {processed}/{len(basic_snippets)}")
        
        print(f"✅ Snippets procesados para análisis: {len(snippets_data)}")
        return {
            'snippets_data': snippets_data,
            'file_comments': file_comments,
            'file_concepts': file_concepts
        }
    
    def export_all_to_theway(self, file_path: str, max_snippets: int = 100) -> Dict[str, int]:
        """Exporta snippets de calidad del archivo de referencia a the-way"""
        print("🚀 INICIANDO EXPORTACIÓN A THE-WAY")
        print("=" * 60)
        
        # Procesar archivo
        results = self.process_reference_file(file_path)
        snippets_data = results['snippets_data']
        
        # Filtrar snippets de calidad
        print(f"🔍 Filtrando snippets de calidad...")
        quality_snippets = self.filter_quality_snippets(snippets_data)
        print(f"✅ Snippets de calidad seleccionados: {len(quality_snippets)}")
        
        # Limitar cantidad si es necesario
        if len(quality_snippets) > max_snippets:
            # Ordenar por calidad educativa (score de comentarios + diversidad de conceptos)
            quality_snippets.sort(
                key=lambda x: (
                    x['educational_data'].get('comment_quality', 0) + 
                    len(x['concepts']) * 0.5
                ), 
                reverse=True
            )
            quality_snippets = quality_snippets[:max_snippets]
            print(f"📊 Limitado a los mejores {max_snippets} snippets")
        
        # Exportar snippets
        print(f"📤 Exportando {len(quality_snippets)} snippets a the-way...")
        print("-" * 60)
        
        exported = 0
        failed = 0
        
        for i, snippet_data in enumerate(quality_snippets, 1):
            print(f"[{i:3d}/{len(quality_snippets)}] ", end="")
            if self.export_snippet_to_theway(snippet_data):
                exported += 1
            else:
                failed += 1
        
        print("=" * 60)
        print(f"🎉 EXPORTACIÓN COMPLETADA")
        print(f"✅ Snippets exportados exitosamente: {exported}")
        print(f"❌ Snippets fallidos: {failed}")
        print(f"📊 Tasa de éxito: {exported/(exported+failed)*100:.1f}%")
        
        return {
            'exported': exported,
            'failed': failed,
            'total_processed': len(quality_snippets)
        }


def main():
    """Función principal"""
    # Rutas de archivos
    reference_file = "/home/joselillo/proyectos/Extractor_snippets/Referencia Python.py"
    
    # Verificar que existe el archivo
    if not Path(reference_file).exists():
        print(f"❌ Error: No se encuentra el archivo {reference_file}")
        return
    
    # Crear exportador
    exporter = TheWayExporter()
    
    # Procesar y exportar
    results = exporter.export_all_to_theway(reference_file, max_snippets=50)
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL:")
    print(f"📁 Archivo procesado: {reference_file}")
    print(f"📤 Snippets exportados: {results['exported']}")
    print(f"❌ Errores: {results['failed']}")
    print(f"📊 Total procesados: {results['total_processed']}")
    print("=" * 60)


if __name__ == "__main__":
    main()

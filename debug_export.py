#!/usr/bin/env python3
"""
Script de debug para verificar el formato de los datos antes de exportar
"""

from src.snippets.parser import parse_snippets
from src.snippets.agents.educational_enhancements import (
    CommentContextDetector,
    EducationalSnippetClassifier
)

def debug_export():
    # Rutas de archivos
    reference_file = "/home/joselillo/proyectos/Extractor_snippets/Referencia Python.py"
    
    # Crear detectores
    comment_detector = CommentContextDetector()
    educational_classifier = EducationalSnippetClassifier()
    
    # Extraer snippets básicos
    basic_snippets = parse_snippets(reference_file, strict=False)
    print(f"✅ Snippets básicos extraídos: {len(basic_snippets)}")
    
    # Procesar un snippet de muestra
    if basic_snippets:
        sample_snippet = basic_snippets[0]
        print(f"\n📄 Snippet de muestra:")
        print(f"Index: {sample_snippet.index}")
        print(f"Title: {sample_snippet.title}")
        print(f"Content: {repr(sample_snippet.content[:100])}...")
        
        # Análisis educativo del snippet
        print(f"\n🔍 Analizando snippet...")
        snippet_comments = comment_detector.detect_educational_comments(sample_snippet.content)
        print(f"Comentarios resultado: {type(snippet_comments)} = {snippet_comments}")
        
        snippet_concepts = comment_detector.detect_educational_concepts(sample_snippet.content)
        print(f"Conceptos resultado: {type(snippet_concepts)} = {snippet_concepts}")
        
        educational_context = educational_classifier.classify_snippet(sample_snippet)
        print(f"Educational context: {type(educational_context)} = {educational_context}")
        
        # Convertir EducationalContext a dict
        educational_data = {
            'educational_level': educational_context.level.value,
            'difficulty': educational_context.difficulty_score,
            'comment_quality': educational_context.comment_quality,
            'has_explanations': educational_context.has_explanations,
            'has_examples': educational_context.has_examples,
        }
        print(f"Educational data dict: {educational_data}")

if __name__ == "__main__":
    debug_export()

#!/usr/bin/env python3
"""
Script simplificado para extraer snippets del archivo 'Referencia Python.py'
y exportarlos a 'the-way'.
"""

import subprocess
import re
import tempfile
from pathlib import Path
from typing import List, Dict, Any

from src.snippets.parser import parse_snippets
from src.snippets.agents.educational_enhancements import (
    CommentContextDetector,
    EducationalSnippetClassifier
)

class SimpleTheWayExporter:
    """Exportador simplificado de snippets a the-way"""
    
    def __init__(self):
        self.comment_detector = CommentContextDetector()
        self.educational_classifier = EducationalSnippetClassifier()
    
    def generate_description(self, snippet) -> str:
        """Genera una descripción simple basada en el contenido del snippet"""
        content = snippet.content.strip()
        title = snippet.title.strip()
        
        # Si hay título, usarlo (limpio)
        if title and title != "":
            # Limpiar el título de separadores
            clean_title = re.sub(r'[-=_\s]{3,}', '', title).strip()
            if clean_title:
                return clean_title
        
        # Generar descripción automática basada en el código
        lines = content.split('\n')
        if not lines:
            return "Snippet de código Python"
            
        first_line = lines[0].strip()
        
        # Detectar patrones comunes
        if first_line.startswith('def '):
            func_match = re.search(r'def\s+(\w+)', first_line)
            if func_match:
                return f"Función: {func_match.group(1)}"
        elif first_line.startswith('class '):
            class_match = re.search(r'class\s+(\w+)', first_line)
            if class_match:
                return f"Clase: {class_match.group(1)}"
        elif any(keyword in first_line for keyword in ['for ', 'while ']):
            return "Ejemplo de bucle"
        elif 'if ' in first_line:
            return "Ejemplo condicional"
        elif any(keyword in first_line for keyword in ['import ', 'from ']):
            return "Imports y módulos"
        elif any(keyword in content for keyword in ['print(']):
            return "Ejemplo básico"
        else:
            # Usar las primeras palabras del contenido
            words = re.findall(r'\w+', content)
            if len(words) >= 2:
                return f"Código: {' '.join(words[:3])}"
            else:
                return "Snippet de Python"
    
    def generate_tags(self, snippet, concepts: List[str], educational_data: dict) -> List[str]:
        """Genera tags basados en conceptos y análisis educativo"""
        tags = set()
        
        # Tag de nivel educativo
        level = educational_data.get('educational_level', 'beginner')
        tags.add(f"nivel-{level}")
        
        # Tags de conceptos detectados
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
        
        # Tags adicionales basados en contenido
        content = snippet.content.lower()
        
        if 'class ' in content:
            tags.add("poo")
        if 'def ' in content:
            tags.add("funciones")
        if any(keyword in content for keyword in ['for ', 'while ']):
            tags.add("bucles")
        if 'if ' in content:
            tags.add("condicionales")
        if any(keyword in content for keyword in ['list', '[]', 'append']):
            tags.add("listas")
        if any(keyword in content for keyword in ['dict', '{}', 'key']):
            tags.add("diccionarios")
        if 'print(' in content:
            tags.add("basico")
        if any(keyword in content for keyword in ['import ', 'from ']):
            tags.add("imports")
        
        # Tag general
        tags.add("python")
        tags.add("snippet")
        
        return list(tags)
    
    def is_quality_snippet(self, snippet, concepts: List[str], educational_data: dict) -> bool:
        """Determina si un snippet es de suficiente calidad para exportar"""
        content = snippet.content.strip()
        
        # Filtros básicos
        if len(content) < 20:
            return False
        
        lines = content.split('\n')
        if len(lines) < 2:
            return False
        
        # Debe tener al menos algunos caracteres alfanuméricos
        if not re.search(r'[a-zA-Z_]\w*', content):
            return False
        
        # Debe tener conceptos detectados
        if not concepts:
            return False
        
        # Filtrar snippets que son solo comentarios
        code_lines = [line for line in lines if line.strip() and not line.strip().startswith('#')]
        if len(code_lines) < 1:
            return False
        
        return True
    
    def export_snippet(self, snippet, concepts: List[str], educational_data: dict) -> bool:
        """Exporta un snippet individual a the-way"""
        try:
            # Generar metadatos
            description = self.generate_description(snippet)
            tags = self.generate_tags(snippet, concepts, educational_data)
            
            # Crear archivo temporal
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
                # Agregar el título como comentario si existe
                if snippet.title.strip():
                    clean_title = re.sub(r'[-=_\s]{3,}', '', snippet.title).strip()
                    if clean_title:
                        temp_file.write(f"# {clean_title}\n")
                
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
            for tag in tags[:10]:  # Limitar a 10 tags para evitar sobrecarga
                cmd.extend(['--tag', tag])
            
            # Ejecutar comando
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Limpiar archivo temporal
            Path(temp_file_path).unlink()
            
            if result.returncode == 0:
                return True
            else:
                print(f"❌ Error en the-way: {result.stderr.strip()}")
                return False
                
        except Exception as e:
            print(f"❌ Excepción: {e}")
            return False
    
    def export_all(self, file_path: str, max_snippets: int = 50) -> Dict[str, int]:
        """Exporta todos los snippets de calidad"""
        print("🚀 EXPORTANDO SNIPPETS A THE-WAY")
        print("=" * 50)
        
        # Extraer snippets
        snippets = parse_snippets(file_path, strict=False)
        print(f"📄 Snippets extraídos: {len(snippets)}")
        
        # Procesar y filtrar snippets
        quality_snippets = []
        
        for snippet in snippets:
            # Análisis educativo
            concepts = self.comment_detector.detect_educational_concepts(snippet.content)
            educational_context = self.educational_classifier.classify_snippet(snippet)
            educational_data = {
                'educational_level': educational_context.level.value,
                'difficulty': educational_context.difficulty_score,
                'comment_quality': educational_context.comment_quality,
            }
            
            # Verificar calidad
            if self.is_quality_snippet(snippet, concepts, educational_data):
                quality_snippets.append((snippet, concepts, educational_data))
        
        print(f"✅ Snippets de calidad: {len(quality_snippets)}")
        
        # Limitar cantidad
        if len(quality_snippets) > max_snippets:
            # Ordenar por nivel de dificultad y calidad
            quality_snippets.sort(
                key=lambda x: (len(x[1]), x[2]['comment_quality']),
                reverse=True
            )
            quality_snippets = quality_snippets[:max_snippets]
            print(f"📊 Limitado a {max_snippets} snippets")
        
        # Exportar
        exported = 0
        failed = 0
        
        print(f"\n📤 Exportando snippets...")
        for i, (snippet, concepts, educational_data) in enumerate(quality_snippets, 1):
            description = self.generate_description(snippet)
            print(f"[{i:2d}/{len(quality_snippets)}] {description[:50]}...", end=" ")
            
            if self.export_snippet(snippet, concepts, educational_data):
                print("✅")
                exported += 1
            else:
                print("❌")
                failed += 1
        
        print("\n" + "=" * 50)
        print(f"✅ Exportados: {exported}")
        print(f"❌ Fallidos: {failed}")
        print(f"📊 Tasa de éxito: {exported/(exported+failed)*100:.1f}%")
        
        return {"exported": exported, "failed": failed}


def main():
    reference_file = "/home/joselillo/proyectos/Extractor_snippets/Referencia Python.py"
    
    if not Path(reference_file).exists():
        print(f"❌ No se encuentra: {reference_file}")
        return
    
    exporter = SimpleTheWayExporter()
    results = exporter.export_all(reference_file, max_snippets=30)
    
    print(f"\n🎉 Proceso completado!")
    print(f"📁 Archivo: Referencia Python.py")
    print(f"📤 Exportados: {results['exported']}")
    print(f"❌ Errores: {results['failed']}")


if __name__ == "__main__":
    main()

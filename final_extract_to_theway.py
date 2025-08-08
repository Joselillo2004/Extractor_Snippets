#!/usr/bin/env python3
"""
Script final para extraer snippets del archivo 'Referencia Python.py'
y exportarlos a 'the-way' usando el formato JSON.
"""

import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any

from src.snippets.parser import parse_snippets
from src.snippets.agents.educational_enhancements import (
    CommentContextDetector,
    EducationalSnippetClassifier
)

class FinalTheWayExporter:
    """Exportador final de snippets a the-way usando JSON"""
    
    def __init__(self):
        self.comment_detector = CommentContextDetector()
        self.educational_classifier = EducationalSnippetClassifier()
    
    def generate_description(self, snippet) -> str:
        """Genera una descripción basada en el contenido del snippet"""
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
            tags.add(concept)
        
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
        tags.add("referencia")
        
        return list(tags)
    
    def is_quality_snippet(self, snippet, concepts: List[str], educational_data: dict) -> bool:
        """Determina si un snippet es de suficiente calidad para exportar"""
        content = snippet.content.strip()
        
        # Filtros básicos
        if len(content) < 15:
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
            
        # Filtrar snippets muy largos (más de 50 líneas)
        if len(lines) > 50:
            return False
        
        return True
    
    def create_snippet_json(self, snippet, concepts: List[str], educational_data: dict) -> dict:
        """Crea un objeto JSON para un snippet compatible con the-way"""
        description = self.generate_description(snippet)
        tags = self.generate_tags(snippet, concepts, educational_data)
        
        # Crear el contenido con título si existe
        code = snippet.content
        if snippet.title.strip():
            clean_title = re.sub(r'[-=_\s]{3,}', '', snippet.title).strip()
            if clean_title:
                code = f"# {clean_title}\n{code}"
        
        return {
            "description": description,
            "language": "python",
            "code": code,
            "tags": tags[:10]  # Limitar a 10 tags
        }
    
    def export_to_json_and_import(self, file_path: str, max_snippets: int = 40) -> Dict[str, int]:
        """Exporta snippets a JSON y los importa a the-way"""
        print("🚀 EXPORTANDO SNIPPETS A THE-WAY")
        print("=" * 50)
        
        # Extraer snippets
        snippets = parse_snippets(file_path, strict=False)
        print(f"📄 Snippets extraídos del archivo: {len(snippets)}")
        
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
        
        print(f"✅ Snippets de calidad seleccionados: {len(quality_snippets)}")
        
        # Limitar cantidad
        if len(quality_snippets) > max_snippets:
            # Ordenar por nivel de dificultad y cantidad de conceptos
            quality_snippets.sort(
                key=lambda x: (len(x[1]), x[2]['comment_quality']),
                reverse=True
            )
            quality_snippets = quality_snippets[:max_snippets]
            print(f"📊 Limitado a los mejores {max_snippets} snippets")
        
        # Crear JSON para the-way
        json_snippets = []
        for snippet, concepts, educational_data in quality_snippets:
            json_snippet = self.create_snippet_json(snippet, concepts, educational_data)
            json_snippets.append(json_snippet)
        
        # Escribir archivo JSON temporal en formato JSONL (una línea por snippet)
        json_file = Path("snippets_to_import.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            for snippet_json in json_snippets:
                json.dump(snippet_json, f, ensure_ascii=False)
                f.write('\n')
        
        print(f"📝 Archivo JSON creado: {json_file}")
        print(f"📊 {len(json_snippets)} snippets preparados para importar")
        
        # Importar usando the-way
        print(f"\n📤 Importando snippets a the-way...")
        try:
            result = subprocess.run(
                ['the-way', 'import', str(json_file)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Snippets importados exitosamente!")
                exported = len(json_snippets)
                failed = 0
            else:
                print(f"❌ Error importando snippets:")
                print(result.stderr)
                exported = 0
                failed = len(json_snippets)
        
        except Exception as e:
            print(f"❌ Excepción durante la importación: {e}")
            exported = 0
            failed = len(json_snippets)
        
        # Solo limpiar archivo temporal si el import fue exitoso
        if exported > 0:
            json_file.unlink()
        else:
            print(f"📁 Archivo JSON conservado para inspección: {json_file}")
        
        print("\n" + "=" * 50)
        print(f"✅ Snippets importados: {exported}")
        print(f"❌ Errores: {failed}")
        if exported > 0:
            print(f"📊 Tasa de éxito: {exported/(exported+failed)*100:.1f}%")
        
        return {"exported": exported, "failed": failed}


def main():
    reference_file = "/home/joselillo/proyectos/Extractor_snippets/Referencia Python.py"
    
    if not Path(reference_file).exists():
        print(f"❌ No se encuentra el archivo: {reference_file}")
        return
    
    exporter = FinalTheWayExporter()
    results = exporter.export_to_json_and_import(reference_file, max_snippets=30)
    
    print(f"\n🎉 PROCESO COMPLETADO!")
    print(f"📁 Archivo procesado: Referencia Python.py")
    print(f"📤 Snippets importados a the-way: {results['exported']}")
    print(f"❌ Errores: {results['failed']}")
    
    if results['exported'] > 0:
        print(f"\n💡 Puedes buscar los snippets con:")
        print(f"   the-way search python")
        print(f"   the-way search referencia")
        print(f"   the-way list")


if __name__ == "__main__":
    main()

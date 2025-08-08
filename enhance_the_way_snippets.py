#!/usr/bin/env python3
"""
Script para validar y mejorar descripciones de snippets en the-way
"""
import subprocess
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from snippets.agents.description_enhancer import DescriptionEnhancerAgent
from snippets.agents.base_agent import Snippet


class TheWaySnippetManager:
    """Maneja la interacción con the-way CLI"""
    
    def __init__(self, the_way_path="/home/joselillo/.cargo/bin/the-way"):
        self.the_way_path = the_way_path
    
    def get_snippet(self, snippet_id: int) -> Optional[Dict]:
        """Obtiene un snippet específico por ID"""
        try:
            result = subprocess.run(
                [self.the_way_path, "view", str(snippet_id)],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parsear la salida de the-way
            output = result.stdout.strip()
            if not output:
                return None
            
            lines = output.split('\n')
            if len(lines) < 2:
                return None
            
            # Extraer información de la primera línea (header)
            header_line = lines[0]
            if not header_line.startswith('■ #'):
                return None
            
            # Parsear header: ■ #109. Descripción | lenguaje :tags:
            parts = header_line[2:].split(' | ', 1)
            if len(parts) != 2:
                return None
            
            # Extraer ID y descripción
            id_and_desc = parts[0]
            id_part, description = id_and_desc.split('. ', 1)
            snippet_id = int(id_part.strip('#'))
            
            # Extraer lenguaje y tags
            lang_and_tags = parts[1]
            lang_tags_parts = lang_and_tags.split(' :', 1)
            language = lang_tags_parts[0].strip()
            tags = lang_tags_parts[1] if len(lang_tags_parts) > 1 else ""
            
            # Extraer contenido (todo después de la primera línea vacía)
            content_lines = []
            in_content = False
            for line in lines[1:]:
                if not in_content and line.strip() == "":
                    in_content = True
                elif in_content:
                    content_lines.append(line)
            
            content = '\n'.join(content_lines).strip()
            
            return {
                'id': snippet_id,
                'description': description,
                'language': language,
                'tags': tags,
                'content': content
            }
            
        except subprocess.CalledProcessError as e:
            print(f"Error obteniendo snippet {snippet_id}: {e}")
            return None
        except Exception as e:
            print(f"Error parseando snippet {snippet_id}: {e}")
            return None
    
    def get_snippets_in_range(self, start_id: int, end_id: int) -> List[Dict]:
        """Obtiene múltiples snippets en un rango"""
        snippets = []
        for snippet_id in range(start_id, end_id + 1):
            snippet = self.get_snippet(snippet_id)
            if snippet:
                snippets.append(snippet)
        return snippets


def validate_and_analyze_snippets(start_id: int = 109, count: int = 10):
    """Valida y analiza snippets desde the-way"""
    
    print(f"🔍 Validando snippets desde #{start_id} hasta #{start_id + count - 1}")
    print("=" * 60)
    
    # Inicializar componentes
    manager = TheWaySnippetManager()
    enhancer = DescriptionEnhancerAgent()
    
    # Obtener snippets
    snippets_data = manager.get_snippets_in_range(start_id, start_id + count - 1)
    
    if not snippets_data:
        print("❌ No se encontraron snippets en el rango especificado")
        return
    
    print(f"✅ Se encontraron {len(snippets_data)} snippets")
    print()
    
    # Analizar cada snippet
    for snippet_data in snippets_data:
        print(f"📋 SNIPPET #{snippet_data['id']}")
        print("-" * 40)
        
        # Información actual
        print(f"📝 Descripción actual: {snippet_data['description']}")
        print(f"🏷️  Tags actuales: {snippet_data['tags']}")
        print(f"💻 Código:")
        print(snippet_data['content'][:200] + ("..." if len(snippet_data['content']) > 200 else ""))
        print()
        
        # Crear objeto Snippet para el análisis
        snippet_obj = Snippet(snippet_data['content'], snippet_data['id'])
        
        # Generar descripción mejorada
        try:
            enhanced_desc = enhancer.generate_enhanced_description(snippet_obj)
            analysis = enhancer.analyze_code(snippet_data['content'])
            
            print(f"✨ Descripción mejorada: {enhanced_desc}")
            print(f"🎯 Propósito: {analysis.main_purpose}")
            print(f"📊 Complejidad: {analysis.complexity_level}")
            print(f"🔑 Conceptos clave: {', '.join(analysis.key_concepts)}")
            
            input_type, output_type = analysis.input_output
            if input_type or output_type:
                print(f"📥📤 I/O: entrada={input_type or 'ninguna'}, salida={output_type or 'ninguna'}")
            
            print(f"🎓 Valor educativo: {analysis.educational_value}")
            print(f"🔧 Patrones: {', '.join(analysis.code_patterns) if analysis.code_patterns else 'básico'}")
            
            # Sugerencia de mejora
            if snippet_data['description'] != enhanced_desc:
                print(f"💡 RECOMENDACIÓN: Actualizar descripción")
                print(f"   Desde: '{snippet_data['description']}'")
                print(f"   Hacia: '{enhanced_desc}'")
            else:
                print("✅ La descripción actual es adecuada")
                
        except Exception as e:
            print(f"❌ Error analizando snippet: {e}")
        
        print("=" * 60)
        print()


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python enhance_the_way_snippets.py [start_id] [count]")
        print()
        print("Ejemplos:")
        print("  python enhance_the_way_snippets.py 109 10")
        print("  python enhance_the_way_snippets.py 120 5")
        return
    
    start_id = int(sys.argv[1]) if len(sys.argv) > 1 else 109
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    validate_and_analyze_snippets(start_id, count)


if __name__ == "__main__":
    main()

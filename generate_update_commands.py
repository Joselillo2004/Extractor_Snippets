#!/usr/bin/env python3
"""
Script para generar comandos de actualización de snippets en the-way
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


def generate_enhanced_tags(analysis, language="python"):
    """Genera tags mejorados basados en el análisis"""
    tags = [language, "referencia"]
    
    # Agregar nivel de complejidad
    tags.append(f"nivel-{analysis.complexity_level}")
    
    # Agregar conceptos clave (máximo 4 para evitar sobrecarga)
    concept_tags = [f"tema-{concept}" for concept in analysis.key_concepts[:4]]
    tags.extend(concept_tags)
    
    # Agregar valor educativo
    tags.append(analysis.educational_value)
    
    return ":".join(tags) + ":"


def generate_update_commands(start_id: int = 109, count: int = 10):
    """Genera comandos para actualizar snippets"""
    
    print(f"🛠️  Generando comandos de actualización para snippets #{start_id}-{start_id+count-1}")
    print("=" * 80)
    
    manager = TheWaySnippetManager()
    enhancer = DescriptionEnhancerAgent()
    
    snippets_data = manager.get_snippets_in_range(start_id, start_id + count - 1)
    
    if not snippets_data:
        print("❌ No se encontraron snippets en el rango especificado")
        return
    
    update_commands = []
    improvements = []
    
    for snippet_data in snippets_data:
        snippet_obj = Snippet(snippet_data['content'], snippet_data['id'])
        
        try:
            enhanced_desc = enhancer.generate_enhanced_description(snippet_obj)
            analysis = enhancer.analyze_code(snippet_data['content'])
            
            # Generar tags mejorados
            enhanced_tags = generate_enhanced_tags(analysis, snippet_data['language'])
            
            # Solo procesar si la descripción cambió significativamente
            if snippet_data['description'] != enhanced_desc:
                
                improvement_info = {
                    'id': snippet_data['id'],
                    'current_description': snippet_data['description'],
                    'enhanced_description': enhanced_desc,
                    'current_tags': snippet_data['tags'],
                    'enhanced_tags': enhanced_tags,
                    'content': snippet_data['content'],
                    'analysis': {
                        'main_purpose': analysis.main_purpose,
                        'complexity': analysis.complexity_level,
                        'key_concepts': analysis.key_concepts,
                        'educational_value': analysis.educational_value
                    }
                }
                
                improvements.append(improvement_info)
                
                # Crear archivo temporal para el contenido
                temp_filename = f"temp_snippet_{snippet_data['id']}.py"
                
                # Comandos de actualización
                commands = [
                    f"# === ACTUALIZAR SNIPPET #{snippet_data['id']} ===",
                    f"# Descripción actual: {snippet_data['description']}",
                    f"# Descripción mejorada: {enhanced_desc}",
                    f"# Tags actuales: {snippet_data['tags']}",
                    f"# Tags mejorados: {enhanced_tags}",
                    "",
                    "# 1. Crear archivo temporal con el contenido:",
                    f"cat > {temp_filename} << 'EOF'",
                    snippet_data['content'],
                    "EOF",
                    "",
                    "# 2. Eliminar snippet actual:",
                    f"/home/joselillo/.cargo/bin/the-way delete {snippet_data['id']}",
                    "",
                    "# 3. Importar con nueva descripción:",
                    f"/home/joselillo/.cargo/bin/the-way import {temp_filename} --description \\\"{enhanced_desc}\\\" --tags \\\"{enhanced_tags}\\\"",
                    "",
                    "# 4. Limpiar archivo temporal:",
                    f"rm {temp_filename}",
                    "",
                    "# ========================================",
                    ""
                ]
                
                update_commands.extend(commands)
                
        except Exception as e:
            print(f"Error procesando snippet {snippet_data['id']}: {e}")
    
    # Guardar información de mejoras en JSON
    if improvements:
        improvements_file = Path(f"snippet_improvements_{start_id}_{start_id+count-1}.json")
        with open(improvements_file, 'w', encoding='utf-8') as f:
            json.dump(improvements, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Se encontraron {len(improvements)} snippets para mejorar")
        print(f"📁 Información de mejoras guardada en: {improvements_file}")
        print()
    
    # Guardar comandos de actualización
    if update_commands:
        commands_file = Path(f"update_commands_{start_id}_{start_id+count-1}.sh")
        with open(commands_file, 'w', encoding='utf-8') as f:
            f.write("#!/bin/bash\n")
            f.write("# Comandos de actualización para snippets de the-way\n")
            f.write("# IMPORTANTE: Revisar cada comando antes de ejecutar\n\n")
            f.write('\n'.join(update_commands))
        
        print(f"📜 Comandos de actualización guardados en: {commands_file}")
        print(f"🔧 Para aplicar: chmod +x {commands_file} && ./{commands_file}")
        print()
        
        # Mostrar resumen
        print("📊 RESUMEN DE MEJORAS:")
        print("-" * 40)
        for imp in improvements:
            print(f"#{imp['id']}: {imp['current_description'][:50]}...")
            print(f"  → {imp['enhanced_description'][:50]}...")
            print(f"  🎯 {imp['analysis']['main_purpose']} ({imp['analysis']['complexity']})")
            print(f"  🔑 {', '.join(imp['analysis']['key_concepts'][:3])}")
            print()
        
    else:
        print("✅ No se necesitan actualizaciones - las descripciones actuales son adecuadas")


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python generate_update_commands.py [start_id] [count]")
        print()
        print("Ejemplos:")
        print("  python generate_update_commands.py 109 10")
        print("  python generate_update_commands.py 120 20")
        return
    
    start_id = int(sys.argv[1]) if len(sys.argv) > 1 else 109
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    
    generate_update_commands(start_id, count)


if __name__ == "__main__":
    main()

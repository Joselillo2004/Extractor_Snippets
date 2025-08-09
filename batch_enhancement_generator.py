#!/usr/bin/env python3
"""
Generador de mejoras de snippets en lotes
Este script permite procesar rangos amplios de snippets y generar
archivos JSON con las mejoras correspondientes.
"""
import subprocess
import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Optional

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from snippets.agents.educational_enhancements import DescriptionEnhancerAgent
except ImportError as e:
    print(f"❌ Error importando DescriptionEnhancerAgent: {e}")
    print("Asegúrate de que el módulo esté en src/snippets/agents/")
    sys.exit(1)

def get_snippet_info(snippet_id: int) -> Optional[Dict]:
    """Obtiene información de un snippet específico de the-way"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "view", str(snippet_id)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return None
        
        # Parsear la salida de the-way view
        output = result.stdout
        
        # Extraer descripción (línea que empieza con "Description:")
        desc_match = re.search(r'Description:\\s*(.+)', output)
        description = desc_match.group(1).strip() if desc_match else f"Snippet {snippet_id}"
        
        # Extraer tags (línea que empieza con "Tags:")
        tags_match = re.search(r'Tags:\\s*(.+)', output)
        tags = tags_match.group(1).strip() if tags_match else ""
        
        # Extraer contenido (todo después de una línea vacía o separador)
        lines = output.split('\\n')
        content_lines = []
        content_started = False
        
        for line in lines:
            if content_started:
                content_lines.append(line)
            elif line.strip() == "" or "─" in line:
                content_started = True
        
        content = '\\n'.join(content_lines).strip()
        
        return {
            'id': snippet_id,
            'description': description,
            'tags': tags,
            'content': content
        }
        
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout obteniendo snippet {snippet_id}")
        return None
    except Exception as e:
        print(f"❌ Error obteniendo snippet {snippet_id}: {e}")
        return None

def generate_improvements_for_range(start_id: int, end_id: int, output_file: str):
    """Genera mejoras para un rango de snippets"""
    
    print(f"🔍 Generando mejoras para snippets {start_id}-{end_id}")
    print(f"📁 Archivo de salida: {output_file}")
    print()
    
    enhancer = DescriptionEnhancerAgent()
    improvements = []
    processed = 0
    skipped = 0
    
    for snippet_id in range(start_id, end_id + 1):
        print(f"🔄 Procesando snippet #{snippet_id}...", end=" ")
        
        # Obtener información del snippet
        snippet_info = get_snippet_info(snippet_id)
        if not snippet_info:
            print("❌ No encontrado o error")
            skipped += 1
            continue
        
        # Filtrar snippets que no sean Python o que estén vacíos
        content = snippet_info['content']
        if not content.strip() or len(content) < 10:
            print("⏭️  Snippet muy corto, saltando")
            skipped += 1
            continue
        
        try:
            # Crear objeto Snippet (asumiendo que necesita index)
            from snippets.agents.base_agent import Snippet
            snippet = Snippet(content, snippet_id)
            
            # Generar mejora
            enhancement = enhancer.enhance_description(snippet)
            
            # Preparar datos de mejora
            improvement_data = {
                'id': snippet_id,
                'current_description': snippet_info['description'],
                'enhanced_description': enhancement.enhanced_description,
                'current_tags': snippet_info['tags'],
                'enhanced_tags': enhancement.enhanced_tags,
                'content': content,
                'analysis': {
                    'main_purpose': enhancement.main_purpose,
                    'complexity': enhancement.complexity,
                    'key_concepts': enhancement.key_concepts,
                    'educational_value': enhancement.educational_value
                }
            }
            
            improvements.append(improvement_data)
            processed += 1
            print("✅ OK")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            skipped += 1
            continue
    
    # Guardar mejoras
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(improvements, f, indent=2, ensure_ascii=False)
        
        print()
        print("=" * 60)
        print(f"✅ GENERACIÓN COMPLETADA")
        print(f"   📊 Snippets procesados: {processed}")
        print(f"   ⏭️  Snippets saltados: {skipped}")
        print(f"   📁 Archivo guardado: {output_file}")
        print(f"\\n🚀 Para aplicar las mejoras:")
        print(f"   python alternative_update_approach.py {output_file} --apply")
        
    except Exception as e:
        print(f"❌ Error guardando archivo: {e}")

def main():
    \"\"\"Función principal\"\"\"\n    import argparse\n    \n    parser = argparse.ArgumentParser(description='Genera mejoras de snippets para un rango específico')\n    parser.add_argument('start_id', type=int, help='ID inicial del rango')\n    parser.add_argument('end_id', type=int, help='ID final del rango')\n    parser.add_argument('--output', '-o', default=None, help='Archivo de salida (por defecto: improvements_START_END.json)')\n    \n    args = parser.parse_args()\n    \n    if args.start_id \u003e args.end_id:\n        print(\"❌ El ID inicial debe ser menor o igual al final\")\n        sys.exit(1)\n    \n    if args.output is None:\n        args.output = f\"improvements_{args.start_id}_{args.end_id}.json\"\n    \n    generate_improvements_for_range(args.start_id, args.end_id, args.output)\n\nif __name__ == \"__main__\":\n    main()\n"}}}</function_calls>

## 3. **Hacer los scripts ejecutables y probar con los snippets existentes**

<function_calls>
<invoke name="run_command">
<parameter name="command">chmod +x /home/joselillo/proyectos/Extractor_snippets/alternative_update_approach.py

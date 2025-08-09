#!/usr/bin/env python3
"""
Script para diagnosticar el formato exacto de salida de the-way view
"""
import subprocess
import re

def debug_snippet(snippet_id: int):
    """Muestra el formato exacto de un snippet de the-way"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "view", str(snippet_id)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            print(f"❌ Snippet {snippet_id} no encontrado")
            return False
        
        output = result.stdout
        print(f"🔍 SNIPPET #{snippet_id} - FORMATO RAW:")
        print("=" * 60)
        print(repr(output))  # Mostrar caracteres de escape
        print()
        print("📝 CONTENIDO VISUAL:")
        print("-" * 60)
        print(output)
        print()
        
        # Analizar línea por línea
        lines = output.split('\\n')
        print("📋 ANÁLISIS LÍNEA POR LÍNEA:")
        print("-" * 60)
        for i, line in enumerate(lines):
            print(f"{i:2d}: {repr(line)}")
        
        print()
        print("🧩 EXTRACCIÓN DE COMPONENTES:")
        print("-" * 60)
        
        # Intentar extraer descripción
        desc_patterns = [
            r'#(\\d+)\\. (.+?) \\|',
            r'■ #(\\d+)\\. (.+?) \\|',
            r'#(\\d+)\\. (.+?)\\s*\\|'
        ]
        
        for i, pattern in enumerate(desc_patterns):
            match = re.search(pattern, output)
            if match:
                print(f"✅ Patrón {i+1} funciona: ID={match.group(1)}, DESC='{match.group(2)}'")
            else:
                print(f"❌ Patrón {i+1} no funciona: {pattern}")
        
        # Intentar extraer tags
        tags_patterns = [
            r'\\| (.+?) :(.+)',
            r'\\|[^:]+:(.+)',
            r'\\| \\w+ :(.+)'
        ]
        
        for i, pattern in enumerate(tags_patterns):
            match = re.search(pattern, output)
            if match:
                print(f"✅ Tags patrón {i+1} funciona: '{match.group(1)}'")
            else:
                print(f"❌ Tags patrón {i+1} no funciona: {pattern}")
        
        print()
        return True
        
    except Exception as e:
        print(f"❌ Error procesando snippet {snippet_id}: {e}")
        return False

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Diagnostica el formato de the-way view')
    parser.add_argument('snippet_ids', nargs='+', type=int, help='IDs de snippets a diagnosticar')
    
    args = parser.parse_args()
    
    for snippet_id in args.snippet_ids:
        debug_snippet(snippet_id)
        print("\\n" + "="*80 + "\\n")

if __name__ == "__main__":
    main()

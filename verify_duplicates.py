#!/usr/bin/env python3
"""
Script para verificar que los snippets marcados como duplicados realmente lo son.
Muestra el contenido real de varios snippets para comparación manual.
"""

import subprocess
import re
from collections import defaultdict

def get_snippet_basic_info():
    """Obtiene información básica de todos los snippets"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "list"],
            capture_output=True,
            text=True,
            check=True
        )
        
        snippets = []
        for line in result.stdout.strip().split('\n'):
            if line.strip() and line.startswith('■ #'):
                match = re.match(r'■ #(\d+)\.\s*(.*)', line)
                if match:
                    snippet_id = int(match.group(1))
                    title = match.group(2).strip()
                    is_improved = '[MEJORADO]' in title
                    clean_title = title.replace('[MEJORADO]', '').strip()
                    
                    snippets.append({
                        'id': snippet_id,
                        'title': clean_title,
                        'is_improved': is_improved,
                        'original_line': line
                    })
        
        return snippets
    except Exception as e:
        print(f"Error obteniendo snippets: {e}")
        return []

def find_title_duplicates(snippets):
    """Encuentra duplicados basándose en títulos"""
    title_groups = defaultdict(list)
    
    for snippet in snippets:
        normalized_title = snippet['title'].lower().strip()
        normalized_title = re.sub(r'[^\w\s]', '', normalized_title)
        normalized_title = re.sub(r'\s+', ' ', normalized_title)
        title_groups[normalized_title].append(snippet)
    
    duplicates = {title: group for title, group in title_groups.items() if len(group) > 1}
    return duplicates

def get_snippet_full_content(snippet_id):
    """Obtiene el contenido completo de un snippet"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "view", str(snippet_id)],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error obteniendo contenido: {e}"

def extract_code_from_content(content):
    """Extrae solo las líneas de código del contenido"""
    lines = content.split('\n')
    code_lines = []
    in_code_section = False
    
    for line in lines:
        # Detectar inicio de sección de código
        if any(keyword in line for keyword in ['=', 'def ', 'class ', 'import ', 'for ', 'if ', 'while ', 'print(', 'return']):
            in_code_section = True
        
        # Si estamos en sección de código y la línea no es metadata
        if in_code_section and line.strip() and not line.startswith('>>'):
            code_lines.append(line)
    
    return '\n'.join(code_lines)

def compare_snippets_content(snippets):
    """Compara el contenido real de un grupo de snippets"""
    print(f"\n🔍 Comparando {len(snippets)} snippets:")
    
    contents = {}
    codes = {}
    
    for snippet in snippets:
        print(f"   📄 Obteniendo #{snippet['id']}...")
        content = get_snippet_full_content(snippet['id'])
        code = extract_code_from_content(content)
        
        contents[snippet['id']] = content
        codes[snippet['id']] = code
    
    # Comparar códigos
    unique_codes = set(codes.values())
    print(f"\n📊 Análisis de contenido:")
    print(f"   • Total de snippets: {len(snippets)}")
    print(f"   • Códigos únicos encontrados: {len(unique_codes)}")
    
    if len(unique_codes) == 1:
        print("   ✅ Todos los snippets tienen el mismo código")
        return True, contents
    else:
        print("   ⚠️  Los snippets tienen código diferente")
        return False, contents

def show_snippet_details(snippet, content, show_full=False):
    """Muestra los detalles de un snippet"""
    status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
    print(f"\n📄 Snippet #{snippet['id']} ({status})")
    print(f"   Título: {snippet['title']}")
    print(f"   Línea original: {snippet['original_line']}")
    
    if show_full:
        print("   Contenido completo:")
        lines = content.split('\n')
        for i, line in enumerate(lines[:20], 1):  # Solo primeras 20 líneas
            print(f"   {i:2d}│ {line}")
        if len(lines) > 20:
            print(f"   ...│ (y {len(lines) - 20} líneas más)")
    else:
        # Mostrar solo código
        code = extract_code_from_content(content)
        print("   Código extraído:")
        lines = code.split('\n')
        for i, line in enumerate(lines[:10], 1):  # Solo primeras 10 líneas de código
            print(f"   {i:2d}│ {line}")
        if len(lines) > 10:
            print(f"   ...│ (y {len(lines) - 10} líneas más)")

def verify_duplicate_groups(duplicates, max_groups=5):
    """Verifica varios grupos de duplicados"""
    print("🔍 VERIFICACIÓN DE DUPLICADOS")
    print("=" * 60)
    
    verified_groups = []
    
    # Ordenar grupos por tamaño (más duplicados primero)
    sorted_groups = sorted(duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (title, group) in enumerate(sorted_groups[:max_groups]):
        print(f"\n{'='*60}")
        print(f"📂 GRUPO {i+1}: '{title[:50]}...'")
        print(f"   📊 {len(group)} snippets en este grupo")
        print("="*60)
        
        # Verificar contenido
        are_identical, contents = compare_snippets_content(group)
        
        # Mostrar detalles de algunos snippets
        print(f"\n📋 Detalles de los snippets:")
        for j, snippet in enumerate(group[:4]):  # Solo mostrar primeros 4
            show_snippet_details(snippet, contents[snippet['id']], show_full=(j==0))
            if j < len(group) - 1:
                print("   " + "-" * 50)
        
        if len(group) > 4:
            print(f"   ... y {len(group) - 4} snippets más en este grupo")
        
        verified_groups.append({
            'title': title,
            'group': group,
            'identical': are_identical,
            'contents': contents
        })
        
        print(f"\n🔍 RESULTADO: {'✅ IDÉNTICOS' if are_identical else '❌ DIFERENTES'}")
        
        # Preguntar si continuar
        if i < len(sorted_groups) - 1:
            response = input(f"\n❓ ¿Ver siguiente grupo? (y/n/s=skip): ").strip().lower()
            if response == 'n':
                break
            elif response == 's':
                continue
    
    return verified_groups

def main():
    print("🔍 VERIFICADOR DE DUPLICADOS")
    print("="*50)
    
    # Obtener snippets
    print("📥 Obteniendo lista de snippets...")
    snippets = get_snippet_basic_info()
    print(f"📊 Total snippets: {len(snippets)}")
    
    # Encontrar duplicados
    print("🔍 Identificando grupos de duplicados...")
    duplicates = find_title_duplicates(snippets)
    print(f"📊 Grupos de duplicados encontrados: {len(duplicates)}")
    
    if not duplicates:
        print("✅ No se encontraron duplicados")
        return
    
    # Mostrar resumen
    total_duplicates = sum(len(group) - 1 for group in duplicates.values())
    print(f"📊 Total de snippets duplicados a eliminar: {total_duplicates}")
    
    # Verificar grupos
    print(f"\n❓ ¿Verificar contenido de los grupos? (y/N): ", end="")
    if input().strip().lower() == 'y':
        verified = verify_duplicate_groups(duplicates)
        
        # Resumen final
        print(f"\n" + "="*60)
        print("📋 RESUMEN DE VERIFICACIÓN")
        print("="*60)
        
        identical_count = sum(1 for g in verified if g['identical'])
        different_count = len(verified) - identical_count
        
        print(f"✅ Grupos con contenido idéntico: {identical_count}")
        print(f"❌ Grupos con contenido diferente: {different_count}")
        
        if different_count > 0:
            print("⚠️  ADVERTENCIA: Algunos grupos tienen contenido diferente")
            print("   Revisar antes de proceder con la limpieza masiva")
    
    print(f"\n💡 Sugerencia: Usar el script fast_cleanup.py solo después de esta verificación")

if __name__ == "__main__":
    main()

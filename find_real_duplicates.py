#!/usr/bin/env python3
"""
Script para encontrar duplicados REALES basándose en contenido exacto de código.
Solo marca como duplicados aquellos snippets que tienen código idéntico.
"""

import subprocess
import re
import hashlib
from collections import defaultdict
import time

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
                        'full_title': title,
                        'is_improved': is_improved,
                        'original_line': line
                    })
        
        return snippets
    except Exception as e:
        print(f"Error obteniendo snippets: {e}")
        return []

def get_snippet_code_content(snippet_id):
    """Obtiene solo el contenido de código de un snippet"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "view", str(snippet_id)],
            capture_output=True,
            text=True,
            check=True,
            timeout=10
        )
        
        content = result.stdout.strip()
        
        # Extraer solo las líneas de código, ignorando metadatos
        lines = content.split('\n')
        code_lines = []
        
        for line in lines:
            stripped = line.strip()
            # Ignorar líneas de metadatos y líneas vacías
            if (stripped and 
                not stripped.startswith('■ #') and 
                not stripped.startswith('>>') and
                not stripped.startswith('Description:') and
                not stripped.startswith('Language:') and
                not stripped.startswith('Tags:')):
                code_lines.append(stripped)
        
        # Unir las líneas de código y normalizar espacios
        code_content = '\n'.join(code_lines)
        
        # Normalizar el código para comparación
        normalized_code = normalize_code(code_content)
        
        return normalized_code
        
    except Exception as e:
        return None

def normalize_code(code):
    """Normaliza el código para comparación exacta"""
    if not code:
        return ""
    
    lines = []
    for line in code.split('\n'):
        # Normalizar espacios y tabulaciones
        normalized_line = re.sub(r'\s+', ' ', line.strip())
        if normalized_line:  # Solo agregar líneas no vacías
            lines.append(normalized_line)
    
    return '\n'.join(lines)

def get_code_hash(code):
    """Genera un hash del código para identificación rápida"""
    return hashlib.md5(code.encode('utf-8')).hexdigest()

def find_real_duplicates(snippets, max_snippets=None):
    """Encuentra duplicados reales basándose en contenido exacto de código"""
    print(f"🔍 Analizando contenido de código de {len(snippets)} snippets...")
    
    if max_snippets:
        snippets = snippets[:max_snippets]
        print(f"   (Limitado a primeros {max_snippets} para prueba)")
    
    code_groups = defaultdict(list)
    processed = 0
    
    for snippet in snippets:
        processed += 1
        if processed % 100 == 0:
            print(f"   Procesando snippet {processed}/{len(snippets)}...")
        
        code_content = get_snippet_code_content(snippet['id'])
        
        if code_content and code_content.strip():  # Solo procesar si tiene código
            code_hash = get_code_hash(code_content)
            snippet['code'] = code_content
            snippet['code_hash'] = code_hash
            code_groups[code_hash].append(snippet)
        else:
            # Snippets sin código o vacíos
            snippet['code'] = ""
            snippet['code_hash'] = "empty"
        
        time.sleep(0.02)  # Pausa pequeña para no saturar
    
    # Solo mantener grupos con más de un snippet (duplicados reales)
    real_duplicates = {hash_key: group for hash_key, group in code_groups.items() 
                      if len(group) > 1 and hash_key != "empty"}
    
    return real_duplicates

def analyze_duplicates(real_duplicates):
    """Analiza los duplicados reales encontrados"""
    print("\n" + "="*60)
    print("📊 ANÁLISIS DE DUPLICADOS REALES")
    print("="*60)
    
    if not real_duplicates:
        print("✅ No se encontraron duplicados reales de código!")
        return
    
    total_duplicated_snippets = sum(len(group) for group in real_duplicates.values())
    total_to_delete = sum(len(group) - 1 for group in real_duplicates.values())
    
    print(f"📊 Grupos de código idéntico: {len(real_duplicates)}")
    print(f"📊 Total de snippets con código duplicado: {total_duplicated_snippets}")
    print(f"🗑️  Snippets que se pueden eliminar: {total_to_delete}")
    print(f"✅ Snippets únicos a mantener: {len(real_duplicates)}")
    
    # Mostrar ejemplos
    print(f"\n🔍 Ejemplos de grupos con código idéntico:")
    
    sorted_groups = sorted(real_duplicates.items(), key=lambda x: len(x[1]), reverse=True)
    
    for i, (hash_key, group) in enumerate(sorted_groups[:10]):  # Mostrar top 10
        print(f"\n📂 Grupo {i+1}: {len(group)} snippets con código idéntico")
        print(f"   Hash: {hash_key[:12]}...")
        
        # Mostrar código (primeras líneas)
        code_lines = group[0]['code'].split('\n')
        print(f"   Código:")
        for j, line in enumerate(code_lines[:3]):
            print(f"      {j+1}│ {line}")
        if len(code_lines) > 3:
            print(f"      ...│ (y {len(code_lines) - 3} líneas más)")
        
        # Mostrar snippets en este grupo
        print(f"   Snippets:")
        for snippet in group[:5]:  # Solo mostrar primeros 5
            status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
            print(f"      • #{snippet['id']} ({status}) - {snippet['title'][:40]}...")
        if len(group) > 5:
            print(f"      ... y {len(group) - 5} más")
    
    return real_duplicates

def create_cleanup_plan(real_duplicates):
    """Crea un plan de limpieza para duplicados reales"""
    cleanup_plan = {
        'to_keep': [],
        'to_delete': [],
        'stats': {
            'total_groups': len(real_duplicates),
            'total_duplicates': 0,
            'improved_kept': 0,
            'original_kept': 0
        }
    }
    
    for hash_key, group in real_duplicates.items():
        # Separar mejorados y originales
        improved = [s for s in group if s['is_improved']]
        original = [s for s in group if not s['is_improved']]
        
        cleanup_plan['stats']['total_duplicates'] += len(group) - 1
        
        # Estrategia: mantener mejorado de ID más bajo, o original de ID más bajo
        if improved:
            to_keep = min(improved, key=lambda x: x['id'])
            to_delete = [s for s in group if s['id'] != to_keep['id']]
            cleanup_plan['stats']['improved_kept'] += 1
        else:
            to_keep = min(original, key=lambda x: x['id'])
            to_delete = [s for s in group if s['id'] != to_keep['id']]
            cleanup_plan['stats']['original_kept'] += 1
        
        cleanup_plan['to_keep'].append(to_keep)
        cleanup_plan['to_delete'].extend(to_delete)
    
    return cleanup_plan

def preview_real_cleanup(cleanup_plan):
    """Muestra vista previa del plan de limpieza real"""
    stats = cleanup_plan['stats']
    
    print("\n" + "="*60)
    print("📋 PLAN DE LIMPIEZA DE DUPLICADOS REALES")
    print("="*60)
    print(f"📊 Grupos de código idéntico: {stats['total_groups']}")
    print(f"🗑️  Total de snippets a eliminar: {len(cleanup_plan['to_delete'])}")
    print(f"✅ Snippets mejorados a mantener: {stats['improved_kept']}")
    print(f"📝 Snippets originales a mantener: {stats['original_kept']}")
    
    if len(cleanup_plan['to_delete']) > 0:
        print(f"\n🔍 Snippets que se eliminarían:")
        for i, snippet in enumerate(cleanup_plan['to_delete'][:15]):
            status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
            print(f"   🗑️  #{snippet['id']} ({status}) - {snippet['title'][:50]}...")
        
        if len(cleanup_plan['to_delete']) > 15:
            print(f"   ... y {len(cleanup_plan['to_delete']) - 15} más")
    
    return len(cleanup_plan['to_delete']) > 0

def execute_real_cleanup(cleanup_plan, dry_run=True):
    """Ejecuta la limpieza de duplicados reales"""
    if dry_run:
        print("\n🔍 MODO DRY-RUN - No se eliminarán snippets realmente")
        return True
    
    to_delete = cleanup_plan['to_delete']
    print(f"\n⚠️  INICIANDO ELIMINACIÓN DE {len(to_delete)} DUPLICADOS REALES...")
    
    deleted_count = 0
    failed_count = 0
    
    for snippet in to_delete:
        try:
            result = subprocess.run(
                f"/home/joselillo/.cargo/bin/the-way delete {snippet['id']} --force",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                deleted_count += 1
                if deleted_count % 10 == 0:
                    print(f"   ✅ Eliminados: {deleted_count}/{len(to_delete)}")
            else:
                failed_count += 1
                print(f"   ❌ Error eliminando #{snippet['id']}")
                
        except Exception as e:
            failed_count += 1
            print(f"   ❌ Error eliminando #{snippet['id']}: {e}")
        
        time.sleep(0.1)
    
    print(f"\n✅ Eliminación completada: {deleted_count} eliminados, {failed_count} fallidos")
    return deleted_count

def main():
    print("🔍 BUSCADOR DE DUPLICADOS REALES DE CÓDIGO")
    print("="*60)
    
    # Obtener snippets
    print("📥 Obteniendo lista de snippets...")
    snippets = get_snippet_basic_info()
    print(f"📊 Total snippets encontrados: {len(snippets)}")
    
    if not snippets:
        print("❌ No se pudieron obtener snippets")
        return
    
    # Preguntar si hacer análisis completo o limitado
    print(f"\n❓ ¿Analizar todos los snippets o hacer prueba limitada?")
    print("   1. Análisis completo (puede tomar tiempo)")
    print("   2. Prueba con primeros 500 snippets")
    print("   3. Prueba con primeros 100 snippets")
    
    choice = input("Selecciona (1/2/3): ").strip()
    
    max_snippets = None
    if choice == "2":
        max_snippets = 500
    elif choice == "3":
        max_snippets = 100
    
    # Buscar duplicados reales por código
    real_duplicates = find_real_duplicates(snippets, max_snippets)
    
    # Analizar resultados
    analyzed_duplicates = analyze_duplicates(real_duplicates)
    
    if not real_duplicates:
        return
    
    # Crear plan de limpieza
    cleanup_plan = create_cleanup_plan(real_duplicates)
    
    # Mostrar vista previa
    has_duplicates = preview_real_cleanup(cleanup_plan)
    
    if has_duplicates:
        # Preguntar si proceder
        print(f"\n❓ ¿Proceder con la limpieza de duplicados reales? (y/N): ", end="")
        response = input().strip().lower()
        
        if response == 'y':
            print("\n❓ ¿Modo real o dry-run? (real/dry): ", end="")
            mode = input().strip().lower()
            
            execute_real_cleanup(cleanup_plan, dry_run=(mode != 'real'))
        else:
            print("🚫 Limpieza cancelada")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Script RÁPIDO para limpiar snippets duplicados en the-way.
Enfoque optimizado para manejar miles de snippets eficientemente.
"""

import subprocess
import re
from collections import defaultdict
import time

def get_snippet_basic_info():
    """Obtiene información básica de todos los snippets de forma rápida"""
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
                # Extraer ID y título del snippet
                match = re.match(r'■ #(\d+)\.\s*(.*)', line)
                if match:
                    snippet_id = int(match.group(1))
                    title = match.group(2).strip()
                    is_improved = '[MEJORADO]' in title
                    
                    # Limpiar título para comparación
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
    """Encuentra duplicados basándose en títulos similares (más rápido)"""
    title_groups = defaultdict(list)
    
    for snippet in snippets:
        # Normalizar título para comparación
        normalized_title = snippet['title'].lower().strip()
        # Remover caracteres especiales y espacios extra
        normalized_title = re.sub(r'[^\w\s]', '', normalized_title)
        normalized_title = re.sub(r'\s+', ' ', normalized_title)
        
        title_groups[normalized_title].append(snippet)
    
    # Solo mantener grupos con más de un snippet
    duplicates = {title: group for title, group in title_groups.items() if len(group) > 1}
    
    return duplicates

def plan_title_cleanup(duplicates):
    """Planifica limpieza basada en títulos duplicados"""
    cleanup_plan = {
        'to_keep': [],
        'to_delete': [],
        'stats': {
            'total_groups': len(duplicates),
            'total_duplicates': 0,
            'improved_kept': 0,
            'original_kept': 0
        }
    }
    
    for title, snippet_list in duplicates.items():
        # Separar mejorados y originales
        improved = [s for s in snippet_list if s['is_improved']]
        original = [s for s in snippet_list if not s['is_improved']]
        
        cleanup_plan['stats']['total_duplicates'] += len(snippet_list) - 1
        
        # Estrategia: mantener mejorado de ID más bajo, o original de ID más bajo
        if improved:
            to_keep = min(improved, key=lambda x: x['id'])
            to_delete = [s for s in snippet_list if s['id'] != to_keep['id']]
            cleanup_plan['stats']['improved_kept'] += 1
        else:
            to_keep = min(original, key=lambda x: x['id'])
            to_delete = [s for s in snippet_list if s['id'] != to_keep['id']]
            cleanup_plan['stats']['original_kept'] += 1
        
        cleanup_plan['to_keep'].append(to_keep)
        cleanup_plan['to_delete'].extend(to_delete)
    
    return cleanup_plan

def preview_cleanup(cleanup_plan, max_examples=15):
    """Muestra una vista previa del plan de limpieza"""
    stats = cleanup_plan['stats']
    
    print("\n" + "="*60)
    print("📋 PLAN DE LIMPIEZA RÁPIDA (por títulos)")
    print("="*60)
    print(f"📊 Grupos de duplicados encontrados: {stats['total_groups']}")
    print(f"🗑️  Total de snippets a eliminar: {len(cleanup_plan['to_delete'])}")
    print(f"✅ Snippets mejorados a mantener: {stats['improved_kept']}")
    print(f"📝 Snippets originales a mantener: {stats['original_kept']}")
    print(f"📈 Reducción estimada: {len(cleanup_plan['to_delete'])} snippets")
    
    print(f"\n🔍 Ejemplos de snippets a eliminar (primeros {max_examples}):")
    for i, snippet in enumerate(cleanup_plan['to_delete'][:max_examples]):
        status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
        print(f"   🗑️  #{snippet['id']} ({status}) - {snippet['title'][:50]}...")
    
    if len(cleanup_plan['to_delete']) > max_examples:
        print(f"   ... y {len(cleanup_plan['to_delete']) - max_examples} más")
    
    # Mostrar algunos grupos de ejemplo
    print(f"\n📋 Ejemplos de grupos de duplicados:")
    
    # Crear un diccionario simple de ejemplos
    example_groups = {}
    for kept_snippet in cleanup_plan['to_keep'][:5]:
        title = kept_snippet['title']
        group = [kept_snippet] + [s for s in cleanup_plan['to_delete'] if s['title'] == title]
        if len(group) > 1:  # Solo mostrar si realmente hay duplicados
            example_groups[title] = group
    
    count = 0
    for title, group in example_groups.items():
        if count >= 5:
            break
        print(f"   📂 '{title[:40]}...' -> {len(group)} versiones")
        for snippet in group[:3]:  # Solo mostrar primeras 3
            status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
            action = "MANTENER" if snippet in cleanup_plan['to_keep'] else "ELIMINAR"
            print(f"      • #{snippet['id']} ({status}) - {action}")
        count += 1
    
    return True

def execute_batch_cleanup(cleanup_plan, batch_size=50, dry_run=True):
    """Ejecuta la limpieza en lotes para mayor eficiencia"""
    if dry_run:
        print("\n🔍 MODO DRY-RUN - No se eliminarán snippets realmente")
        return True
    
    to_delete = cleanup_plan['to_delete']
    print(f"\n⚠️  INICIANDO ELIMINACIÓN EN LOTES DE {len(to_delete)} SNIPPETS...")
    
    deleted_count = 0
    failed_count = 0
    
    # Procesar en lotes
    for i in range(0, len(to_delete), batch_size):
        batch = to_delete[i:i+batch_size]
        print(f"\n🗑️  Procesando lote {i//batch_size + 1}/{(len(to_delete)-1)//batch_size + 1} ({len(batch)} snippets)...")
        
        for snippet in batch:
            try:
                result = subprocess.run(
                    f"echo 'y' | /home/joselillo/.cargo/bin/the-way delete {snippet['id']}",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                if result.returncode == 0:
                    deleted_count += 1
                else:
                    failed_count += 1
                    print(f"   ❌ Error eliminando #{snippet['id']}")
                    
            except Exception as e:
                failed_count += 1
                print(f"   ❌ Error eliminando #{snippet['id']}: {e}")
            
            time.sleep(0.05)  # Pausa muy pequeña
        
        print(f"   ✅ Lote completado. Total eliminados: {deleted_count}, Fallidos: {failed_count}")
        time.sleep(0.5)  # Pausa entre lotes
    
    print(f"\n✅ Eliminación completada: {deleted_count} eliminados, {failed_count} fallidos")
    return deleted_count

def main():
    print("🚀 LIMPIEZA RÁPIDA DE SNIPPETS DUPLICADOS")
    print("="*50)
    
    # Obtener información básica rápidamente
    print("🔍 Obteniendo lista de snippets...")
    snippets = get_snippet_basic_info()
    print(f"📊 Total snippets encontrados: {len(snippets)}")
    
    if not snippets:
        print("❌ No se pudieron obtener snippets")
        return
    
    # Encontrar duplicados por título (rápido)
    print("🔍 Buscando duplicados por título...")
    duplicates = find_title_duplicates(snippets)
    
    if not duplicates:
        print("✅ No se encontraron duplicados por título!")
        return
    
    # Crear plan de limpieza
    cleanup_plan = plan_title_cleanup(duplicates)
    
    # Mostrar vista previa
    preview_cleanup(cleanup_plan)
    
    # Preguntar confirmación
    print(f"\n❓ ¿Proceder con la limpieza? (y/N): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        print("\n❓ ¿Modo real o dry-run? (real/dry): ", end="")
        mode = input().strip().lower()
        
        execute_batch_cleanup(cleanup_plan, dry_run=(mode != 'real'))
    else:
        print("🚫 Limpieza cancelada")

if __name__ == "__main__":
    main()

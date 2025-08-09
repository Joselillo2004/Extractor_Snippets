#!/usr/bin/env python3
"""
Script para identificar y limpiar snippets duplicados en the-way.
Mantiene solo la mejor versión (mejorada si existe) de cada snippet único.
"""

import subprocess
import re
import json
from collections import defaultdict
import time

def get_all_snippets():
    """Obtiene todos los snippets de the-way"""
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
                # Extraer ID del snippet
                match = re.match(r'■ #(\d+)\.', line)
                if match:
                    snippet_id = int(match.group(1))
                    is_improved = '[MEJORADO]' in line
                    snippets.append({
                        'id': snippet_id,
                        'line': line,
                        'is_improved': is_improved
                    })
        
        return snippets
    except Exception as e:
        print(f"Error obteniendo snippets: {e}")
        return []

def get_snippet_content(snippet_id):
    """Obtiene el contenido de un snippet específico"""
    try:
        result = subprocess.run(
            ["/home/joselillo/.cargo/bin/the-way", "view", str(snippet_id)],
            capture_output=True,
            text=True,
            check=True,
            timeout=5  # Timeout para evitar cuelgues
        )
        
        content = result.stdout.strip()
        
        # Extraer solo las líneas de código más importantes
        lines = content.split('\n')
        code_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('>>') and not line.startswith('Description:'):
                # Solo líneas que parecen código Python
                if any(keyword in line for keyword in ['=', 'def ', 'class ', 'import ', 'for ', 'if ', 'while ', 'print(', 'return', 'try:', 'except']):
                    code_lines.append(line)
        
        return '\n'.join(code_lines[:10])  # Solo las primeras 10 líneas importantes
    
    except Exception:
        return None

def normalize_content(content):
    """Normaliza contenido para comparación de duplicados"""
    if not content:
        return ""
    
    # Remover comentarios y líneas vacías
    lines = []
    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            lines.append(line)
    
    return '\n'.join(lines)

def find_duplicates():
    """Encuentra snippets duplicados por contenido"""
    print("🔍 Obteniendo lista de snippets...")
    snippets = get_all_snippets()
    print(f"📊 Total snippets encontrados: {len(snippets)}")
    
    print("🔍 Analizando contenido para encontrar duplicados...")
    content_to_snippets = defaultdict(list)
    
    for i, snippet in enumerate(snippets):
        if i % 100 == 0:
            print(f"   Procesando snippet {i+1}/{len(snippets)}...")
        
        content = get_snippet_content(snippet['id'])
        if content:
            normalized = normalize_content(content)
            if normalized:  # Solo si tiene contenido válido
                content_to_snippets[normalized].append(snippet)
    
    # Encontrar duplicados
    duplicates = {}
    for content, snippet_list in content_to_snippets.items():
        if len(snippet_list) > 1:
            duplicates[content] = snippet_list
    
    return duplicates

def plan_cleanup(duplicates):
    """Planifica qué snippets mantener y cuáles eliminar"""
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
    
    for content, snippet_list in duplicates.items():
        # Separar mejorados y originales
        improved = [s for s in snippet_list if s['is_improved']]
        original = [s for s in snippet_list if not s['is_improved']]
        
        cleanup_plan['stats']['total_duplicates'] += len(snippet_list) - 1
        
        # Estrategia de limpieza:
        # 1. Si hay versiones mejoradas, mantener una y eliminar todo lo demás
        # 2. Si solo hay originales, mantener el de ID más bajo
        
        if improved:
            # Mantener la versión mejorada de ID más bajo
            to_keep = min(improved, key=lambda x: x['id'])
            to_delete = [s for s in snippet_list if s['id'] != to_keep['id']]
            cleanup_plan['stats']['improved_kept'] += 1
        else:
            # Mantener el original de ID más bajo
            to_keep = min(original, key=lambda x: x['id'])
            to_delete = [s for s in snippet_list if s['id'] != to_keep['id']]
            cleanup_plan['stats']['original_kept'] += 1
        
        cleanup_plan['to_keep'].append(to_keep)
        cleanup_plan['to_delete'].extend(to_delete)
    
    return cleanup_plan

def preview_cleanup(cleanup_plan, max_examples=10):
    """Muestra una vista previa del plan de limpieza"""
    stats = cleanup_plan['stats']
    
    print("\n" + "="*60)
    print("📋 PLAN DE LIMPIEZA DE DUPLICADOS")
    print("="*60)
    print(f"📊 Grupos de duplicados encontrados: {stats['total_groups']}")
    print(f"🗑️  Total de snippets a eliminar: {len(cleanup_plan['to_delete'])}")
    print(f"✅ Snippets mejorados a mantener: {stats['improved_kept']}")
    print(f"📝 Snippets originales a mantener: {stats['original_kept']}")
    print(f"📈 Reducción estimada: {len(cleanup_plan['to_delete'])} snippets")
    
    print(f"\n🔍 Ejemplos de snippets a eliminar (primeros {max_examples}):")
    for i, snippet in enumerate(cleanup_plan['to_delete'][:max_examples]):
        status = "MEJORADO" if snippet['is_improved'] else "ORIGINAL"
        print(f"   🗑️  #{snippet['id']} ({status})")
    
    if len(cleanup_plan['to_delete']) > max_examples:
        print(f"   ... y {len(cleanup_plan['to_delete']) - max_examples} más")
    
    return True

def execute_cleanup(cleanup_plan, dry_run=True):
    """Ejecuta el plan de limpieza"""
    if dry_run:
        print("\n🔍 MODO DRY-RUN - No se eliminarán snippets realmente")
        return True
    
    print(f"\n⚠️  INICIANDO ELIMINACIÓN REAL DE {len(cleanup_plan['to_delete'])} SNIPPETS...")
    
    deleted_count = 0
    for snippet in cleanup_plan['to_delete']:
        try:
            # Usar echo "y" para confirmar automáticamente la eliminación
            result = subprocess.run(
                f"echo 'y' | /home/joselillo/.cargo/bin/the-way delete {snippet['id']}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                deleted_count += 1
                if deleted_count % 50 == 0:
                    print(f"   🗑️  Eliminados: {deleted_count}/{len(cleanup_plan['to_delete'])}")
            else:
                print(f"   ❌ Error eliminando #{snippet['id']}: {result.stderr}")
                
        except Exception as e:
            print(f"   ❌ Error eliminando #{snippet['id']}: {e}")
        
        # Pausa pequeña para evitar saturar the-way
        time.sleep(0.1)
    
    print(f"\n✅ Eliminación completada: {deleted_count} snippets eliminados")
    return deleted_count

def main():
    print("🧹 LIMPIEZA DE SNIPPETS DUPLICADOS")
    print("="*50)
    
    # Encontrar duplicados
    duplicates = find_duplicates()
    
    if not duplicates:
        print("✅ No se encontraron duplicados!")
        return
    
    # Crear plan de limpieza
    cleanup_plan = plan_cleanup(duplicates)
    
    # Mostrar vista previa
    preview_cleanup(cleanup_plan)
    
    # Preguntar confirmación
    print(f"\n❓ ¿Ejecutar limpieza? (y/N): ", end="")
    response = input().strip().lower()
    
    if response == 'y':
        print("\n❓ ¿Modo real o dry-run? (real/dry): ", end="")
        mode = input().strip().lower()
        
        execute_cleanup(cleanup_plan, dry_run=(mode != 'real'))
    else:
        print("🚫 Limpieza cancelada")

if __name__ == "__main__":
    main()

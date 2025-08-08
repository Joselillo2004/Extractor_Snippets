#!/usr/bin/env python3
"""
Script para aplicar actualizaciones de snippets de manera controlada y segura
"""
import subprocess
import json
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

def load_improvements(improvements_file: Path) -> List[Dict]:
    """Carga las mejoras desde el archivo JSON"""
    try:
        with open(improvements_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {improvements_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ Error decodificando JSON: {e}")
        return []

def execute_the_way_command(command: List[str]) -> bool:
    """Ejecuta un comando de the-way y retorna si fue exitoso"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando comando: {' '.join(command)}")
        print(f"   Error: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def backup_snippet(snippet_id: int, content: str, description: str, tags: str) -> bool:
    """Crea un backup del snippet en un archivo"""
    backup_dir = Path("snippet_backups")
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f"snippet_{snippet_id}.json"
    
    backup_data = {
        'id': snippet_id,
        'description': description,
        'tags': tags,
        'content': content,
        'backup_timestamp': time.time()
    }
    
    try:
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Error creando backup para snippet {snippet_id}: {e}")
        return False

def apply_snippet_update(improvement: Dict, dry_run: bool = True) -> bool:
    """Aplica una actualización individual de snippet"""
    snippet_id = improvement['id']
    content = improvement['content']
    enhanced_desc = improvement['enhanced_description']
    enhanced_tags = improvement['enhanced_tags']
    current_desc = improvement['current_description']
    current_tags = improvement['current_tags']
    
    print(f"🔄 Procesando snippet #{snippet_id}")
    print(f"   Descripción: {current_desc[:50]}... → {enhanced_desc[:50]}...")
    
    if dry_run:
        print("   [DRY RUN] No se realizarán cambios reales")
        return True
    
    # 1. Crear backup
    print("   📋 Creando backup...")
    if not backup_snippet(snippet_id, content, current_desc, current_tags):
        return False
    
    # 2. Crear archivo temporal
    temp_file = Path(f"temp_snippet_{snippet_id}.py")
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"   ❌ Error creando archivo temporal: {e}")
        return False
    
    # 3. Eliminar snippet actual
    print("   🗑️  Eliminando snippet actual...")
    delete_cmd = ["/home/joselillo/.cargo/bin/the-way", "delete", str(snippet_id)]
    if not execute_the_way_command(delete_cmd):
        temp_file.unlink(missing_ok=True)
        return False
    
    # 4. Importar con nueva descripción
    print("   ⬆️  Importando snippet mejorado...")
    import_cmd = [
        "/home/joselillo/.cargo/bin/the-way", 
        "import", 
        str(temp_file),
        "--description", 
        enhanced_desc,
        "--tags", 
        enhanced_tags
    ]
    
    success = execute_the_way_command(import_cmd)
    
    # 5. Limpiar archivo temporal
    temp_file.unlink(missing_ok=True)
    
    if success:
        print("   ✅ Snippet actualizado exitosamente")
        return True
    else:
        print("   ❌ Error actualizando snippet")
        return False

def apply_updates(improvements_file: str, dry_run: bool = True, skip_confirmation: bool = False):
    """Aplica todas las actualizaciones de snippets"""
    
    improvements_path = Path(improvements_file)
    if not improvements_path.exists():
        print(f"❌ Archivo de mejoras no encontrado: {improvements_path}")
        return
    
    improvements = load_improvements(improvements_path)
    if not improvements:
        print("❌ No se pudieron cargar las mejoras")
        return
    
    print(f"📊 Se encontraron {len(improvements)} snippets para actualizar")
    print(f"📁 Archivo de mejoras: {improvements_path}")
    
    if dry_run:
        print("🧪 MODO DRY RUN - No se realizarán cambios reales")
    else:
        print("⚠️  MODO REAL - Se aplicarán cambios permanentes")
    
    print()
    
    # Mostrar resumen
    print("📋 RESUMEN DE ACTUALIZACIONES:")
    print("-" * 60)
    for imp in improvements:
        print(f"#{imp['id']}: {imp['current_description'][:45]}...")
        print(f"   → {imp['enhanced_description'][:45]}...")
        print(f"   🎯 {imp['analysis']['main_purpose']} ({imp['analysis']['complexity']})")
        print()
    
    if not dry_run and not skip_confirmation:
        print("⚠️  ¿Estás seguro de que quieres aplicar estas actualizaciones?")
        print("   Esto eliminará permanentemente los snippets actuales y los reemplazará.")
        response = input("   Escribir 'SI' para continuar: ")
        if response != "SI":
            print("❌ Operación cancelada por el usuario")
            return
    
    # Aplicar actualizaciones
    successful = 0
    failed = 0
    
    for improvement in improvements:
        try:
            if apply_snippet_update(improvement, dry_run):
                successful += 1
            else:
                failed += 1
        except KeyboardInterrupt:
            print("\n⚠️  Operación interrumpida por el usuario")
            break
        except Exception as e:
            print(f"❌ Error inesperado procesando snippet {improvement['id']}: {e}")
            failed += 1
        
        # Pequeña pausa entre actualizaciones
        if not dry_run:
            time.sleep(0.5)
        
        print()
    
    # Resumen final
    print("=" * 60)
    if dry_run:
        print(f"🧪 DRY RUN COMPLETADO")
        print(f"   📊 {len(improvements)} snippets serían actualizados")
        print(f"   ✅ Para aplicar los cambios reales, ejecuta con --apply")
    else:
        print(f"✅ ACTUALIZACIÓN COMPLETADA")
        print(f"   📊 Total procesados: {successful + failed}")
        print(f"   ✅ Exitosos: {successful}")
        print(f"   ❌ Fallidos: {failed}")
        
        if failed > 0:
            print(f"   ⚠️  Revisa los mensajes de error arriba")
            print(f"   💾 Los backups están en: snippet_backups/")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Aplica actualizaciones de snippets de the-way')
    parser.add_argument('improvements_file', help='Archivo JSON con las mejoras (ej: snippet_improvements_109_113.json)')
    parser.add_argument('--apply', action='store_true', help='Aplicar cambios reales (por defecto es dry-run)')
    parser.add_argument('--yes', action='store_true', help='Omitir confirmación (solo con --apply)')
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    skip_confirmation = args.yes
    
    apply_updates(args.improvements_file, dry_run, skip_confirmation)

if __name__ == "__main__":
    main()

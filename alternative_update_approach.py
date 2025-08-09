#!/usr/bin/env python3
"""
Enfoque alternativo para actualizar snippets sin usar the-way delete
Este script crea nuevos snippets con mejores descripciones y permite al usuario 
decidir manualmente qué hacer con los antiguos.
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

def execute_the_way_command(command: List[str]) -> tuple[bool, str, str]:
    """Ejecuta un comando de the-way y retorna éxito, stdout, stderr"""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout ejecutando comando"
    except Exception as e:
        return False, "", str(e)

def create_improved_snippet(improvement: Dict, dry_run: bool = True) -> bool:
    """Crea un nuevo snippet mejorado sin eliminar el anterior"""
    snippet_id = improvement['id']
    content = improvement['content']
    enhanced_desc = improvement['enhanced_description']
    enhanced_tags = improvement['enhanced_tags']
    
    print(f"🔄 Creando snippet mejorado basado en #{snippet_id}")
    print(f"   Descripción: {enhanced_desc}")
    print(f"   Tags: {enhanced_tags}")
    
    if dry_run:
        print("   [DRY RUN] No se creará el snippet real")
        return True
    
    # Crear archivo temporal
    temp_file = Path(f"temp_improved_{snippet_id}.py")
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"   ❌ Error creando archivo temporal: {e}")
        return False
    
    # Importar nuevo snippet con descripción mejorada
    print("   ⬆️  Importando snippet mejorado...")
    import_cmd = [
        "/home/joselillo/.cargo/bin/the-way", 
        "import", 
        str(temp_file),
        "--description", 
        f"[MEJORADO] {enhanced_desc}",
        "--tags", 
        enhanced_tags
    ]
    
    success, stdout, stderr = execute_the_way_command(import_cmd)
    
    # Limpiar archivo temporal
    temp_file.unlink(missing_ok=True)
    
    if success:
        print("   ✅ Snippet mejorado creado exitosamente")
        print(f"   📝 Ahora tienes dos versiones: original #{snippet_id} y mejorada")
        return True
    else:
        print(f"   ❌ Error creando snippet mejorado: {stderr}")
        return False

def process_improvements_batch(improvements_file: str, dry_run: bool = True, batch_size: int = 5):
    """Procesa mejoras en lotes para evitar sobrecargar the-way"""
    
    improvements_path = Path(improvements_file)
    if not improvements_path.exists():
        print(f"❌ Archivo de mejoras no encontrado: {improvements_path}")
        return
    
    improvements = load_improvements(improvements_path)
    if not improvements:
        print("❌ No se pudieron cargar las mejoras")
        return
    
    print(f"📊 Se encontraron {len(improvements)} snippets para procesar")
    print(f"📁 Archivo de mejoras: {improvements_path}")
    print(f"📦 Tamaño de lote: {batch_size}")
    
    if dry_run:
        print("🧪 MODO DRY RUN - No se crearán snippets reales")
    else:
        print("⚠️  MODO REAL - Se crearán snippets mejorados")
    
    print()
    
    # Procesar en lotes
    successful = 0
    failed = 0
    
    for i in range(0, len(improvements), batch_size):
        batch = improvements[i:i + batch_size]
        print(f"📦 Procesando lote {i//batch_size + 1}: snippets {batch[0]['id']}-{batch[-1]['id']}")
        
        for improvement in batch:
            try:
                if create_improved_snippet(improvement, dry_run):
                    successful += 1
                else:
                    failed += 1
            except KeyboardInterrupt:
                print("\n⚠️  Operación interrumpida por el usuario")
                return
            except Exception as e:
                print(f"❌ Error inesperado procesando snippet {improvement['id']}: {e}")
                failed += 1
            
            if not dry_run:
                time.sleep(0.2)  # Pausa breve entre snippets
        
        if not dry_run and i + batch_size < len(improvements):
            print(f"   ⏸️  Pausa entre lotes...")
            time.sleep(2)  # Pausa más larga entre lotes
        
        print()
    
    # Resumen final
    print("=" * 60)
    if dry_run:
        print(f"🧪 DRY RUN COMPLETADO")
        print(f"   📊 {len(improvements)} snippets serían procesados")
        print(f"   ✅ Para crear los snippets mejorados, ejecuta con --apply")
    else:
        print(f"✅ PROCESAMIENTO COMPLETADO")
        print(f"   📊 Total procesados: {successful + failed}")
        print(f"   ✅ Exitosos: {successful}")
        print(f"   ❌ Fallidos: {failed}")
        
        if successful > 0:
            print(f"\n📋 SIGUIENTES PASOS RECOMENDADOS:")
            print(f"   1. Revisar los nuevos snippets con prefijo '[MEJORADO]'")
            print(f"   2. Si están correctos, eliminar manualmente los originales")
            print(f"   3. Opcional: quitar el prefijo '[MEJORADO]' de las descripciones")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Crea snippets mejorados en the-way')
    parser.add_argument('improvements_file', help='Archivo JSON con las mejoras')
    parser.add_argument('--apply', action='store_true', help='Crear snippets reales (por defecto es dry-run)')
    parser.add_argument('--batch-size', type=int, default=5, help='Tamaño de lote para procesamiento')
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    process_improvements_batch(args.improvements_file, dry_run, args.batch_size)

if __name__ == "__main__":
    main()

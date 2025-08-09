#!/usr/bin/env python3
"""
Script para importar snippets mejorados usando el formato JSON correcto de the-way
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

def create_the_way_json(improvement: Dict) -> Dict:
    """Crea un objeto JSON en el formato esperado por the-way"""
    return {
        "description": f"[MEJORADO] {improvement['enhanced_description']}",
        "language": "python",
        "code": improvement['content'],
        "tags": improvement['enhanced_tags'].rstrip(':').split(':')
    }

def import_improved_snippet(improvement: Dict, dry_run: bool = True) -> bool:
    """Importa un snippet mejorado usando the-way import"""
    snippet_id = improvement['id']
    
    print(f"🔄 Importando snippet mejorado basado en #{snippet_id}")
    print(f"   Descripción: {improvement['enhanced_description']}")
    print(f"   Tags: {improvement['enhanced_tags']}")
    
    if dry_run:
        print("   [DRY RUN] No se importará el snippet real")
        return True
    
    # Crear JSON en formato the-way
    the_way_data = create_the_way_json(improvement)
    
    # Crear archivo temporal JSON
    temp_file = Path(f"temp_improved_{snippet_id}.json")
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(the_way_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"   ❌ Error creando archivo temporal: {e}")
        return False
    
    # Importar usando the-way
    print("   ⬆️  Importando snippet...")
    import_cmd = ["/home/joselillo/.cargo/bin/the-way", "import", str(temp_file)]
    
    success, stdout, stderr = execute_the_way_command(import_cmd)
    
    # Limpiar archivo temporal
    temp_file.unlink(missing_ok=True)
    
    if success:
        print("   ✅ Snippet mejorado importado exitosamente")
        # Buscar el ID del nuevo snippet en la salida
        if "Snippet saved" in stdout:
            print(f"   📝 {stdout.strip()}")
        return True
    else:
        print(f"   ❌ Error importando snippet: {stderr}")
        return False

def process_improvements_batch(improvements_file: str, dry_run: bool = True, batch_size: int = 5):
    """Procesa mejoras en lotes"""
    
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
        print("🧪 MODO DRY RUN - No se importarán snippets reales")
    else:
        print("⚠️  MODO REAL - Se importarán snippets mejorados")
    
    print()
    
    # Mostrar resumen de mejoras
    print("📋 RESUMEN DE MEJORAS:")
    print("-" * 60)
    for imp in improvements:
        print(f"#{imp['id']}: {imp['current_description'][:45]}...")
        print(f"   → [MEJORADO] {imp['enhanced_description'][:40]}...")
        print(f"   🎯 {imp['analysis']['main_purpose']} ({imp['analysis']['complexity']})")
        print()
    
    # Procesar en lotes
    successful = 0
    failed = 0
    
    for i in range(0, len(improvements), batch_size):
        batch = improvements[i:i + batch_size]
        print(f"📦 Procesando lote {i//batch_size + 1}: snippets {batch[0]['id']}-{batch[-1]['id']}")
        
        for improvement in batch:
            try:
                if import_improved_snippet(improvement, dry_run):
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
                time.sleep(0.3)  # Pausa breve entre snippets
        
        if not dry_run and i + batch_size < len(improvements):
            print(f"   ⏸️  Pausa entre lotes...")
            time.sleep(1)
        
        print()
    
    # Resumen final
    print("=" * 60)
    if dry_run:
        print(f"🧪 DRY RUN COMPLETADO")
        print(f"   📊 {len(improvements)} snippets serían procesados")
        print(f"   ✅ Para importar los snippets mejorados, ejecuta con --apply")
    else:
        print(f"✅ IMPORTACIÓN COMPLETADA")
        print(f"   📊 Total procesados: {successful + failed}")
        print(f"   ✅ Exitosos: {successful}")
        print(f"   ❌ Fallidos: {failed}")
        
        if successful > 0:
            print(f"\n📋 SIGUIENTES PASOS:")
            print(f"   1. Buscar los nuevos snippets con '[MEJORADO]' en la descripción")
            print(f"   2. Comparar con los originales")
            print(f"   3. Eliminar manualmente los originales si las mejoras son correctas")
            print(f"   4. Opcional: editar las descripciones para quitar '[MEJORADO]'")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Importa snippets mejorados a the-way')
    parser.add_argument('improvements_file', help='Archivo JSON con las mejoras')
    parser.add_argument('--apply', action='store_true', help='Importar snippets reales (por defecto es dry-run)')
    parser.add_argument('--batch-size', type=int, default=5, help='Tamaño de lote para procesamiento')
    
    args = parser.parse_args()
    
    dry_run = not args.apply
    
    process_improvements_batch(args.improvements_file, dry_run, args.batch_size)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Sistema completo para mejorar snippets de the-way en lotes
Combina generación de mejoras e importación en un flujo eficiente
"""
import subprocess
import json
import sys
import time
import re
from pathlib import Path
from typing import List, Dict, Optional

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from snippets.agents.description_enhancer import DescriptionEnhancerAgent
    from snippets.agents.base_agent import Snippet
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de que los módulos estén en src/snippets/agents/")
    sys.exit(1)

class BatchSnippetEnhancer:
    def __init__(self):
        self.enhancer = DescriptionEnhancerAgent()
        self.the_way_path = "/home/joselillo/.cargo/bin/the-way"
    
    def get_snippet_info(self, snippet_id: int) -> Optional[Dict]:
        """Obtiene información de un snippet específico de the-way"""
        try:
            result = subprocess.run(
                [self.the_way_path, "view", str(snippet_id)],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode != 0:
                return None
            
            output = result.stdout
            
            # Extraer descripción usando el patrón correcto
            # Formato: ■ #ID. DESCRIPCIÓN | lenguaje :tags:
            desc_match = re.search(r'■ #\d+\.\s*(.+?)\s*\|', output)
            description = desc_match.group(1).strip() if desc_match else f"Snippet {snippet_id}"
            
            # Extraer tags (todo después de lenguaje:)
            tags_match = re.search(r'\|\s*\w+\s*:(.+)', output)
            if tags_match:
                tags = tags_match.group(1).strip().rstrip(':')
            else:
                tags = ""
            
            # Extraer contenido (después del primer salto de línea real)
            lines = output.split('\n')
            content_lines = []
            content_started = False
            
            for line in lines:
                if content_started:
                    content_lines.append(line)
                elif line.strip() and line.startswith('■'):
                    # La siguiente línea debería ser el contenido
                    content_started = True
            
            content = '\n'.join(content_lines).strip()
            
            # Validar que tenemos contenido válido
            if not content or len(content) < 3:
                return None
            
            return {
                'id': snippet_id,
                'description': description,
                'tags': tags,
                'content': content
            }
            
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            print(f"   ❌ Error de parsing: {e}")
            return None
    
    def generate_improvement(self, snippet_info: Dict) -> Optional[Dict]:
        """Genera una mejora para un snippet específico"""
        try:
            content = snippet_info['content']
            
            # Filtros básicos
            if not content.strip() or len(content) < 10:
                return None
            
            # Crear objeto Snippet
            snippet = Snippet(content, snippet_info['id'])
            
            # Generar análisis y descripción mejorada
            enhanced_description = self.enhancer.generate_enhanced_description(snippet)
            analysis = self.enhancer.analyze_code(content)
            
            # Generar tags mejorados basados en el análisis
            enhanced_tags = self._generate_enhanced_tags(analysis, snippet_info['tags'])
            
            return {
                'id': snippet_info['id'],
                'current_description': snippet_info['description'],
                'enhanced_description': enhanced_description,
                'current_tags': snippet_info['tags'],
                'enhanced_tags': enhanced_tags,
                'content': content,
                'analysis': {
                    'main_purpose': analysis.main_purpose,
                    'complexity': analysis.complexity_level,
                    'key_concepts': analysis.key_concepts,
                    'educational_value': analysis.educational_value
                }
            }
            
        except Exception as e:
            print(f"   ❌ Error generando mejora: {e}")
            return None
    
    def _generate_enhanced_tags(self, analysis, current_tags: str) -> str:
        """Genera tags mejorados basados en el análisis"""
        tags = ['python', 'referencia']
        
        # Agregar nivel de complejidad
        tags.append(f'nivel-{analysis.complexity_level}')
        
        # Agregar conceptos clave como tags
        for concept in analysis.key_concepts:
            tags.append(f'tema-{concept}')
        
        # Agregar valor educativo
        tags.append(analysis.educational_value)
        
        return ':'.join(tags) + ':'
    
    def import_improved_snippet(self, improvement: Dict, dry_run: bool = True) -> bool:
        """Importa un snippet mejorado"""
        snippet_id = improvement['id']
        
        if dry_run:
            return True
        
        # Crear JSON en formato the-way
        the_way_data = {
            "description": f"[MEJORADO] {improvement['enhanced_description']}",
            "language": "python",
            "code": improvement['content'],
            "tags": improvement['enhanced_tags'].rstrip(':').split(':')
        }
        
        # Crear archivo temporal JSON
        temp_file = Path(f"temp_improved_{snippet_id}.json")
        try:
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(the_way_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"   ❌ Error creando archivo temporal: {e}")
            return False
        
        # Importar usando the-way
        import_cmd = [self.the_way_path, "import", str(temp_file)]
        
        try:
            result = subprocess.run(
                import_cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            success = result.returncode == 0
        except Exception:
            success = False
        finally:
            # Limpiar archivo temporal
            temp_file.unlink(missing_ok=True)
        
        return success
    
    def process_range(self, start_id: int, end_id: int, dry_run: bool = True, batch_size: int = 10):
        """Procesa un rango de snippets completo"""
        print(f"🚀 PROCESAMIENTO DE SNIPPETS {start_id}-{end_id}")
        print(f"📦 Tamaño de lote: {batch_size}")
        
        if dry_run:
            print("🧪 MODO DRY RUN")
        else:
            print("⚠️  MODO REAL")
        
        print("=" * 60)
        
        total_processed = 0
        total_improved = 0
        total_imported = 0
        total_skipped = 0
        
        for batch_start in range(start_id, end_id + 1, batch_size):
            batch_end = min(batch_start + batch_size - 1, end_id)
            
            print(f"\\n📦 LOTE: snippets {batch_start}-{batch_end}")
            print("-" * 40)
            
            batch_improvements = []
            
            # Fase 1: Generar mejoras para este lote
            for snippet_id in range(batch_start, batch_end + 1):
                print(f"🔍 Analizando #{snippet_id}...", end=" ")
                
                snippet_info = self.get_snippet_info(snippet_id)
                if not snippet_info:
                    print("❌ No encontrado")
                    total_skipped += 1
                    continue
                
                total_processed += 1
                
                improvement = self.generate_improvement(snippet_info)
                if improvement:
                    batch_improvements.append(improvement)
                    print("✅ Mejora generada")
                    total_improved += 1
                else:
                    print("⏭️  Saltado")
                    total_skipped += 1
            
            # Fase 2: Importar mejoras de este lote
            if batch_improvements:
                print(f"\\n📤 Importando {len(batch_improvements)} mejoras...")
                
                for improvement in batch_improvements:
                    snippet_id = improvement['id']
                    print(f"   📤 #{snippet_id}: {improvement['enhanced_description'][:50]}...", end=" ")
                    
                    if self.import_improved_snippet(improvement, dry_run):
                        print("✅")
                        if not dry_run:
                            total_imported += 1
                    else:
                        print("❌")
                
                if not dry_run:
                    print(f"   ⏸️  Pausa entre lotes...")
                    time.sleep(2)
        
        # Resumen final
        print("\\n" + "=" * 60)
        print(f"📊 RESUMEN FINAL")
        print(f"   🔍 Snippets analizados: {total_processed}")
        print(f"   ✨ Mejoras generadas: {total_improved}")
        print(f"   ⏭️  Snippets saltados: {total_skipped}")
        
        if not dry_run:
            print(f"   📤 Snippets importados: {total_imported}")
            if total_imported > 0:
                print(f"\\n🔍 Para ver los snippets mejorados:")
                print(f"   {self.the_way_path} list --tags python | grep 'MEJORADO'")
        else:
            print(f"\\n🚀 Para aplicar las mejoras:")
            print(f"   python {__file__} {start_id} {end_id} --apply")

def main():
    """Función principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Procesa y mejora snippets en lotes')
    parser.add_argument('start_id', type=int, help='ID inicial del rango')
    parser.add_argument('end_id', type=int, help='ID final del rango')
    parser.add_argument('--apply', action='store_true', help='Aplicar cambios reales (por defecto es dry-run)')
    parser.add_argument('--batch-size', type=int, default=10, help='Tamaño de lote para procesamiento')
    
    args = parser.parse_args()
    
    if args.start_id > args.end_id:
        print("❌ El ID inicial debe ser menor o igual al final")
        sys.exit(1)
    
    enhancer = BatchSnippetEnhancer()
    enhancer.process_range(args.start_id, args.end_id, not args.apply, args.batch_size)

if __name__ == "__main__":
    main()

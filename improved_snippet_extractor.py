#!/usr/bin/env python3
"""
Script mejorado para extraer TODOS los snippets del archivo 'Referencia Python.py' 
y exportarlos a 'the-way' usando la lógica de extracción más precisa.
"""

import subprocess
import json
from pathlib import Path
import sys

# Añadimos src al path para importar agentes
sys.path.insert(0, str(Path(__file__).parent / "src"))

from snippets.agents.educational_enhancements import EducationalSnippetClassifier
from snippets.agents.base_agent import Snippet


class ImprovedSnippetExtractor:
    """Extractor mejorado que encuentra TODOS los snippets de código"""
    
    def extract_snippets(self, content):
        """Extrae snippets usando la lógica precisa basada en indentación con tabs"""
        snippets = []
        lines = content.split('\n')
        code_blocks = []
        current_block = []
        in_code_block = False
        
        for line_num, line in enumerate(lines):
            # Si la línea empieza con tab y parece código (no comentario)
            if line.startswith('\t') and line.strip() and not line.strip().startswith('#'):
                if not in_code_block:
                    in_code_block = True
                    current_block = [line]
                else:
                    current_block.append(line)
            elif in_code_block and (line.strip() == '' or line.startswith('\t#')):
                # Continuar el bloque si es línea vacía o comentario indentado
                current_block.append(line)
            else:
                # Fin del bloque
                if in_code_block and current_block:
                    # Limpiar el bloque de líneas vacías al final
                    while current_block and not current_block[-1].strip():
                        current_block.pop()
                    if current_block:
                        code_blocks.append('\n'.join(current_block))
                current_block = []
                in_code_block = False

        # Procesar el último bloque si existe
        if in_code_block and current_block:
            while current_block and not current_block[-1].strip():
                current_block.pop()
            if current_block:
                code_blocks.append('\n'.join(current_block))
        
        # Crear snippets, filtrando bloques sustanciales
        for i, block in enumerate(code_blocks):
            lines_of_code = [line for line in block.split('\n') 
                           if line.strip() and not line.strip().startswith('#')]
            
            if len(lines_of_code) >= 1:  # Al menos 1 línea de código
                # Limpiar las tabs al inicio para mejor formato
                clean_block = '\n'.join(line[1:] if line.startswith('\t') else line 
                                      for line in block.split('\n'))
                snippets.append(Snippet(clean_block, i))
        
        return snippets


def extract_and_export_snippets(reference_file_path: str, output_dir: Path):
    """Extrae y exporta snippets usando el extractor mejorado"""
    # Leer archivo de referencia
    reference_path = Path(reference_file_path)
    if not reference_path.exists():
        print(f"❌ Archivo no encontrado: {reference_file_path}")
        return False

    print(f"📖 Leyendo archivo: {reference_file_path}")
    with reference_path.open("r", encoding="utf-8") as f:
        content = f.read()

    print(f"📄 Archivo leído: {len(content):,} caracteres, {len(content.splitlines())} líneas")

    # Extraer snippets con extractor mejorado
    extractor = ImprovedSnippetExtractor()
    snippets = extractor.extract_snippets(content)
    print(f"✅ Se extrajeron {len(snippets)} snippets del archivo de referencia.")

    # Clasificar snippets para obtener contexto educativo
    classifier = EducationalSnippetClassifier()
    classified_snippets = []
    
    print("🎓 Clasificando snippets por nivel educativo...")
    
    for snippet in snippets:
        if len(snippet.content.strip()) > 5:  # Solo snippets con contenido mínimo
            try:
                context = classifier.classify_snippet(snippet)
                classified_snippets.append((snippet, context))
            except Exception as e:
                print(f"⚠️ Error clasificando snippet {snippet.index}: {e}")
                # Usar contexto por defecto
                classified_snippets.append((snippet, None))

    print(f"✅ Snippets clasificados: {len(classified_snippets)}")

    # Crear directorio de exportacion si no existe
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generar archivo JSONL para the-way
    jsonl_file = output_dir / "snippets_import.jsonl"
    
    successful_exports = 0
    
    with jsonl_file.open("w", encoding="utf-8") as f:
        for idx, (snippet, context) in enumerate(classified_snippets, 1):
            # Generar tags basados en el contexto educativo
            tags = ["referencia", "python"]
            
            if context:
                tags.append(f"nivel-{context.level.value}")
                tags.extend([f"tema-{topic}" for topic in context.topics[:3]])  # Máximo 3 temas
                
                # Agregar tag de dificultad
                if context.difficulty_score <= 3:
                    tags.append("facil")
                elif context.difficulty_score <= 6:
                    tags.append("intermedio")
                else:
                    tags.append("dificil")
            
            # Preparar entrada para the-way (formato JSONL)
            snippet_entry = {
                "description": f"Snippet {idx}: Ejemplo de código Python de referencia",
                "language": "python",
                "tags": tags,
                "code": snippet.content.strip()
            }
            
            # Escribir entrada al archivo JSONL
            f.write(json.dumps(snippet_entry, ensure_ascii=False) + "\n")
            successful_exports += 1

    print(f"📁 Archivo JSONL generado: {jsonl_file}")
    print(f"📊 Snippets preparados para exportar: {successful_exports}")

    # Importar a the-way
    try:
        print(f"🚀 Importando snippets a the-way...")
        result = subprocess.run(
            ["the-way", "import", str(jsonl_file)], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        print("✅ Importación a 'the-way' completada exitosamente.")
        print(f"📈 Resultado de importación: {result.stdout}")
        
        # Verificar el número total de snippets en the-way
        list_result = subprocess.run(
            ["the-way", "list", "--plain"], 
            capture_output=True, 
            text=True
        )
        
        if list_result.returncode == 0:
            total_snippets = len(list_result.stdout.strip().split('\n')) if list_result.stdout.strip() else 0
            print(f"📊 Total de snippets en the-way después de la importación: {total_snippets}")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al importar con the-way: {e}")
        print(f"📄 Stderr: {e.stderr}")
        print(f"💡 El archivo JSONL está disponible en: {jsonl_file}")
        return False


def main():
    """Función principal"""
    print("🚀 EXTRACTOR DE SNIPPETS MEJORADO")
    print("=" * 50)
    
    reference_file = "/home/joselillo/proyectos/Extractor_snippets/Referencia Python.py"
    output_directory = Path("/home/joselillo/proyectos/Extractor_snippets/the_way_export")
    
    success = extract_and_export_snippets(reference_file, output_directory)
    
    if success:
        print("\n" + "=" * 50)
        print("✅ EXTRACCIÓN Y EXPORTACIÓN COMPLETADA")
        print("=" * 50)
        print("📊 COMANDOS ÚTILES PARA VERIFICAR:")
        print("   the-way list                    # Ver todos los snippets")
        print("   the-way list --tags             # Ver snippets por tags")
        print("   the-way search 'referencia'     # Buscar por tag referencia")
        print("   the-way search 'nivel-beginner' # Buscar por nivel educativo")
    else:
        print("\n" + "=" * 50)
        print("⚠️ EXTRACCIÓN COMPLETADA CON PROBLEMAS")
        print("=" * 50)
        print("📁 Los snippets están disponibles como archivo JSONL")
        print("💡 Puedes importarlos manualmente con:")
        print(f"   the-way import {output_directory}/snippets_import.jsonl")


if __name__ == "__main__":
    main()

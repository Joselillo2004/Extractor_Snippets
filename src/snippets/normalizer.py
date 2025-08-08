import ast
import re
from typing import Dict, List, Any, Set


def analyze_snippet(code: str) -> Dict[str, Any]:
    """
    Analiza un snippet de código para detectar qué normalizaciones necesita.
    
    Returns:
        Dict con flags: has_orphan_indent, needs_wrapper, undefined_names, missing_imports
    """
    lines = code.split('\n')
    
    # Detectar indentación orphan (código indentado sin contexto)
    has_orphan_indent = False
    first_code_line = None
    for line in lines:
        if line.strip() and not line.strip().startswith('#'):
            first_code_line = line
            break
    
    if first_code_line and first_code_line.startswith('    '):
        # Si la primera línea de código está indentada, es orphan
        has_orphan_indent = True
    
    # Detectar nombres potencialmente no definidos
    undefined_names = detect_undefined_names(code)
    
    # Detectar imports faltantes comunes
    missing_imports = detect_missing_imports(code)
    
    return {
        'has_orphan_indent': has_orphan_indent,
        'needs_wrapper': has_orphan_indent,
        'undefined_names': undefined_names,
        'missing_imports': missing_imports
    }


def detect_undefined_names(code: str) -> List[str]:
    """Detecta nombres que probablemente no están definidos"""
    # Patrones comunes de variables no definidas en el archivo de referencia
    common_undefined = []
    
    # Buscar patrones como "var1", "var2", etc.
    var_pattern = r'\b(var\d+|nombre|edad|total|resultado)\b'
    matches = re.findall(var_pattern, code, re.IGNORECASE)
    common_undefined.extend(matches)
    
    # Buscar clases que pueden no estar definidas
    class_pattern = r'\b([A-Z][a-zA-Z]*)\s*\('  # Clases como Vehicle(), Triangle()
    class_matches = re.findall(class_pattern, code)
    common_undefined.extend([c for c in class_matches if c not in ['True', 'False', 'None']])
    
    return list(set(common_undefined))  # Eliminar duplicados


def detect_missing_imports(code: str) -> List[str]:
    """Detecta imports comunes que faltan"""
    missing = []
    
    # Módulos comunes que se usan sin importar
    common_modules = {
        'random': ['random.', 'randint(', 'choice(', 'shuffle('],
        'math': ['math.', ' sqrt(', ' pi', ' sin(', ' cos(', 'sqrt(', 'sin(', 'cos('],
        'datetime': ['datetime.', 'date.', 'time.now'],
        'os': ['os.path', 'os.remove', 'os.system'],
        'sys': ['sys.exit', 'sys.argv']
    }
    
    for module, patterns in common_modules.items():
        for pattern in patterns:
            if pattern in code and f'import {module}' not in code:
                missing.append(module)
                break
    
    return missing


def wrap_orphan_indent(code: str) -> str:
    """
    Envuelve código indentado en una función para hacerlo sintácticamente válido
    """
    lines = code.split('\n')
    
    # Crear función wrapper
    wrapped_lines = ['def snippet_function():']
    
    for line in lines:
        if line.strip():  # Solo líneas no vacías
            # Si ya está indentada, mantener indentación
            if line.startswith('    '):
                wrapped_lines.append(line)
            else:
                # Si no está indentada, agregarle indentación de función
                wrapped_lines.append('    ' + line)
        else:
            wrapped_lines.append('')
    
    # Agregar llamada a la función
    wrapped_lines.extend(['', 'snippet_function()'])
    
    return '\n'.join(wrapped_lines)


def create_context(undefined_names: List[str] = None, missing_imports: List[str] = None) -> str:
    """
    Crea contexto (imports + variables) necesario para que el snippet funcione
    """
    context_lines = []
    
    # Agregar imports
    if missing_imports:
        for module in missing_imports:
            context_lines.append(f'import {module}')
    
    # Agregar línea vacía si hay imports
    if missing_imports:
        context_lines.append('')
    
    # Agregar variables con valores por defecto  
    if undefined_names:
        for name in undefined_names:
            # Valores por defecto basados en patterns comunes
            if 'var' in name.lower() or name.lower() in ['total', 'resultado']:
                context_lines.append(f'{name} = 10')  # Números
            elif name.lower() in ['nombre']:
                context_lines.append(f'{name} = "ejemplo"')  # Strings
            elif name.lower() == 'edad':
                context_lines.append(f'{name} = 25')
            elif name[0].isupper():  # Clases
                context_lines.append(f'class {name}: pass')
            else:
                context_lines.append(f'{name} = 1')  # Default genérico
    
    # Agregar línea vacía si hay variables
    if undefined_names:
        context_lines.append('')
    
    return '\n'.join(context_lines)


def normalize_snippet(code: str) -> str:
    """
    Normaliza un snippet aplicando todas las transformaciones necesarias
    """
    # Analizar qué necesita el snippet
    analysis = analyze_snippet(code)
    
    # Si no necesita normalización, devolver original
    if (not analysis['has_orphan_indent'] and 
        not analysis['undefined_names'] and 
        not analysis['missing_imports']):
        return code
    
    normalized = code
    
    # 1. Crear contexto (imports + variables)
    context = create_context(
        undefined_names=analysis['undefined_names'],
        missing_imports=analysis['missing_imports']
    )
    
    # 2. Envolver código indentado si es necesario
    if analysis['has_orphan_indent']:
        normalized = wrap_orphan_indent(normalized)
    
    # 3. Combinar contexto + código normalizado
    if context.strip():
        normalized = context + normalized
    
    return normalized

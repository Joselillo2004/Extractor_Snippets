from src.snippets.normalizer import analyze_snippet, create_context, wrap_orphan_indent, normalize_snippet


def test_analyze_snippet_detects_orphan_indent():
    """Detecta código con indentación sin contexto"""
    code = "\n    print('hello')\n    x = 1\n"
    analysis = analyze_snippet(code)
    
    assert analysis['has_orphan_indent'] is True
    assert analysis['needs_wrapper'] is True


def test_analyze_snippet_detects_undefined_vars():
    """Detecta variables no definidas típicas"""
    code = "var1 + var2\n"
    analysis = analyze_snippet(code)
    
    assert 'var1' in analysis['undefined_names']
    assert 'var2' in analysis['undefined_names']


def test_analyze_snippet_detects_missing_imports():
    """Detecta imports faltantes comunes"""
    code = "random_number = random.randint(1, 3)\n"
    analysis = analyze_snippet(code)
    
    assert 'random' in analysis['missing_imports']


def test_wrap_orphan_indent():
    """Envuelve código indentado en función"""
    code = "\n    print('hello')\n    x = 1\n"
    wrapped = wrap_orphan_indent(code)
    
    assert 'def snippet_function():' in wrapped
    assert '    print(\'hello\')' in wrapped
    assert 'snippet_function()' in wrapped
    

def test_create_context_for_vars():
    """Crea contexto para variables comunes"""  
    undefined_names = ['var1', 'var2', 'nombre']
    context = create_context(undefined_names=undefined_names)
    
    assert 'var1 = ' in context
    assert 'var2 = ' in context
    assert 'nombre = ' in context


def test_create_context_for_imports():
    """Crea imports para módulos comunes"""
    missing_imports = ['random', 'math', 'datetime']
    context = create_context(missing_imports=missing_imports)
    
    assert 'import random' in context
    assert 'import math' in context
    assert 'import datetime' in context


def test_normalize_snippet_full_flow():
    """Test del flujo completo de normalización"""
    # Snippet con múltiples problemas
    code = "\n    x = random.randint(1, 10)\n    print(var1 + x)\n"
    
    normalized = normalize_snippet(code)
    
    # Debe tener imports
    assert 'import random' in normalized
    # Debe tener variables definidas
    assert 'var1 = ' in normalized
    # Debe estar envuelto en función
    assert 'def snippet_function():' in normalized
    assert 'snippet_function()' in normalized


def test_normalize_snippet_preserves_working_code():
    """No debe modificar código que ya funciona"""
    code = "print('hello world')\nx = 1 + 2\n"
    
    normalized = normalize_snippet(code)
    
    # Código simple no debe ser modificado
    assert normalized == code

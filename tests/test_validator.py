from src.snippets.validator import validate, classify


def test_no_code_is_documental():
    code = "# only comments\n# another comment\n\n"
    res = validate(code)
    assert res.status == 'no_code'


def test_syntax_error_detected():
    code = "def x(:\n  pass\n"
    res = validate(code)
    assert res.status == 'syntax_error'


def test_runtime_error_detected():
    code = "raise ValueError('boom')\n"
    res = validate(code)
    assert res.status == 'runtime_error'
    assert 'ValueError' in res.details


def test_input_stubbed_timeout_safe():
    code = "name = input('your name: ')\nprint(name)\n"
    res = validate(code)
    assert res.status in ('ok', 'runtime_error')  # should not block


def test_classification_flags():
    code = "import math\nprint(math.sqrt(4))\n"
    cls = classify(code)
    assert cls['has_code'] is True
    assert cls['has_imports'] is True

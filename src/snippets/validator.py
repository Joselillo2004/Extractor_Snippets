import ast
import builtins
import io
import sys
import threading
from contextlib import contextmanager, redirect_stdout, redirect_stderr
from dataclasses import dataclass
from typing import Dict, Any
from .normalizer import normalize_snippet


@dataclass
class ValidationResult:
    status: str  # ok | syntax_error | timeout | runtime_error | no_code
    details: str
    stdout: str
    stderr: str
    classification: Dict[str, bool]


def classify(code: str) -> Dict[str, bool]:
    text = code or ''
    lines = [ln for ln in (text.splitlines())]
    non_comment = [ln for ln in lines if ln.strip() and not ln.strip().startswith('#')]
    has_code = any(non_comment)
    uses_input = 'input(' in text
    has_imports = any(ln.lstrip().startswith('import ') or ln.lstrip().startswith('from ') for ln in lines)
    writes_file = 'open(' in text and any(m in text for m in ["'w'", '"w"', "'a'", '"a"'])
    uses_network = any(tok in text for tok in ['requests.', 'urllib.', 'http.client', 'socket.'])
    dangerous = any(tok in text for tok in ['os.remove', 'shutil.rmtree', 'subprocess.', 'os.system'])
    return {
        'has_code': has_code,
        'uses_input': uses_input,
        'has_imports': has_imports,
        'writes_file': writes_file,
        'uses_network': uses_network,
        'dangerous_calls': dangerous,
    }


@contextmanager
def sandbox_env(stub_input: bool = True):
    # Patch builtins.input and open (write/append) to avoid blocking/side-effects
    original_input = builtins.input
    original_open = builtins.open

    def safe_input(prompt: str = '') -> str:
        return ''

    def safe_open(file, mode='r', *args, **kwargs):
        if any(m in mode for m in ('w', 'a', '+')):
            raise PermissionError('File write disabled in sandbox')
        return original_open(file, mode, *args, **kwargs)

    try:
        if stub_input:
            builtins.input = safe_input
        builtins.open = safe_open
        yield
    finally:
        builtins.input = original_input
        builtins.open = original_open


def validate(code: str, timeout_sec: float = 3.0, normalize: bool = True) -> ValidationResult:
    original_code = code
    
    # Try normalization if requested and original code has issues
    normalized_code = code
    if normalize:
        try:
            # Quick syntax check to see if normalization is needed
            ast.parse(code)
        except SyntaxError:
            # Code has syntax errors, try normalizing
            normalized_code = normalize_snippet(code)
    
    # Use normalized code for validation
    code_to_validate = normalized_code
    cls = classify(code_to_validate)
    
    # If no code (only comments/blank), consider valid but mark no_code
    stripped = '\n'.join(ln for ln in code_to_validate.splitlines() if ln.strip())
    if not cls['has_code']:
        return ValidationResult(status='no_code', details='Only comments/blank', stdout='', stderr='', classification=cls)

    # Syntax check on the code we'll actually execute
    try:
        ast.parse(code_to_validate)
    except SyntaxError as e:
        return ValidationResult(status='syntax_error', details=str(e), stdout='', stderr='', classification=cls)

    # Execute with timeout in sandbox
    stdout_io, stderr_io = io.StringIO(), io.StringIO()
    result_container: Dict[str, Any] = {'exc': None}

    def runner():
        try:
            with sandbox_env(), redirect_stdout(stdout_io), redirect_stderr(stderr_io):
                # Isolated globals/locals
                g: Dict[str, Any] = {'__name__': '__snippet__'}
                l: Dict[str, Any] = {}
                exec(compile(code_to_validate, '<snippet>', 'exec'), g, l)
        except Exception as ex:  # capture for reporting
            result_container['exc'] = ex

    t = threading.Thread(target=runner)
    t.daemon = True
    t.start()
    t.join(timeout=timeout_sec)

    if t.is_alive():
        return ValidationResult(status='timeout', details=f'Timed out after {timeout_sec}s', stdout=stdout_io.getvalue(), stderr=stderr_io.getvalue(), classification=cls)

    exc = result_container['exc']
    if exc is not None:
        return ValidationResult(status='runtime_error', details=f'{type(exc).__name__}: {exc}', stdout=stdout_io.getvalue(), stderr=stderr_io.getvalue(), classification=cls)

    return ValidationResult(status='ok', details='Executed successfully', stdout=stdout_io.getvalue(), stderr=stderr_io.getvalue(), classification=cls)

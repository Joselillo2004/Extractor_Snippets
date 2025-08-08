from dataclasses import dataclass
from typing import List, Dict, Any
import re


def normalize_content(content: str) -> str:
    """
    Normaliza el contenido del archivo para arreglar problemas de formato:
    - Convierte CRLF (\r\n) a LF (\n)
    - Convierte tabs a espacios (tabsize=4)
    - Maneja caracteres problemáticos sin romper el contenido
    """
    # Normalizar line endings
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    
    # Convertir tabs a espacios (tabsize=4)
    content = content.expandtabs(4)
    
    return content


@dataclass
class Snippet:
    index: int
    title: str
    start_line: int
    end_line: int
    content: str


def parse_snippets(file_path: str, strict: bool = True) -> List[Snippet]:
    """
    Parse a Python reference file into snippets.

    Rules (strict=True): a snippet starts only at lines that begin with '#' in column 0.
    If strict=False: allow leading whitespace before '#'.
    A snippet ends right before the next snippet start or end of file.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Detect starts
    starts: List[int] = []
    titles: List[str] = []
    for i, line in enumerate(lines, start=1):
        if strict:
            if line.startswith('#'):
                starts.append(i)
                titles.append(line[1:].strip())
        else:
            stripped = line.lstrip()
            if stripped.startswith('#'):
                starts.append(i)
                titles.append(stripped[1:].strip())

    snippets: List[Snippet] = []
    for idx, start in enumerate(starts):
        end = (starts[idx + 1] - 1) if (idx + 1) < len(starts) else len(lines)
        # Trim trailing blank lines
        while end >= start and lines[end - 1].strip() == '':
            end -= 1
        title = titles[idx]
        # Exclude the title line from content, but keep range lines in metadata
        # Convert 1-indexed line numbers to 0-indexed for slicing
        body_lines = lines[start-1:end]
        content = ''.join(body_lines[1:]) if len(body_lines) > 1 else ''
        # Normalizar el contenido del snippet
        normalized_content = normalize_content(content)
        snippets.append(Snippet(index=idx + 1, title=title, start_line=start, end_line=end, content=normalized_content))

    return snippets


def to_dict(snippet: Snippet) -> Dict[str, Any]:
    return {
        'index': snippet.index,
        'title': snippet.title,
        'start_line': snippet.start_line,
        'end_line': snippet.end_line,
        'content': snippet.content,
    }

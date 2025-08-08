import json
from typing import List, Dict, Any


def to_json_report(results: List[Dict[str, Any]]) -> str:
    return json.dumps({'results': results}, ensure_ascii=False, indent=2)


def to_markdown_summary(results: List[Dict[str, Any]]) -> str:
    total = len(results)
    by_status: Dict[str, int] = {}
    for r in results:
        s = r.get('status', 'unknown')
        by_status[s] = by_status.get(s, 0) + 1
    lines = [f'# Snippets Report', f'- Total: {total}']
    for k in sorted(by_status.keys()):
        lines.append(f'- {k}: {by_status[k]}')
    # add examples of failures
    examples = [r for r in results if r.get('status') in ('syntax_error', 'runtime_error', 'timeout')][:5]
    if examples:
        lines.append('\n## Ejemplos fallidos')
        for e in examples:
            lines.append(f"- #{e.get('index')} {e.get('title')} -> {e.get('status')} ({e.get('details')})")
    return '\n'.join(lines) + '\n'

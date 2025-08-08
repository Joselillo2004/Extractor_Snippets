#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import Any, Dict

from src.snippets.parser import parse_snippets, to_dict
from src.snippets.validator import validate
from src.snippets.reporter import to_json_report, to_markdown_summary


def main():
    parser = argparse.ArgumentParser(description='Validate Python snippets from a reference file')
    parser.add_argument('--file', required=True, help='Path to source file (e.g., Referencia Python.py)')
    parser.add_argument('--strict', action='store_true', help='Strict mode: only # at column 0 start snippets')
    parser.add_argument('--normalize', action='store_true', default=True, help='Enable normalization of side-effects (default: True)')
    parser.add_argument('--no-normalize', dest='normalize', action='store_false', help='Disable normalization')
    parser.add_argument('--out', help='Path to write JSON report')
    parser.add_argument('--md', help='Path to write Markdown summary')
    args = parser.parse_args()

    src = Path(args.file)
    if not src.exists():
        raise SystemExit(f'File not found: {src}')

    snippets = parse_snippets(str(src), strict=True if args.strict else True)

    results = []
    for sn in snippets:
        vr = validate(sn.content, normalize=args.normalize)
        item: Dict[str, Any] = {
            'index': sn.index,
            'title': sn.title,
            'start_line': sn.start_line,
            'end_line': sn.end_line,
            'status': vr.status,
            'details': vr.details,
            'classification': vr.classification,
        }
        results.append(item)

    if args.out:
        Path(args.out).write_text(to_json_report(results), encoding='utf-8')
    if args.md:
        Path(args.md).write_text(to_markdown_summary(results), encoding='utf-8')

    # default: print small summary to stdout
    print(to_markdown_summary(results))


if __name__ == '__main__':
    main()

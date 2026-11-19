#!/usr/bin/env python3
"""Read-only nonempty-line indexer for FastDH scripts; stdlib only."""
import argparse
import json
import re
import sys
from pathlib import Path

NOTE = re.compile(
    r"^(?:\[Configuration(?: note)?\s*\|\s*(U\d+)\s+end\]"
    r"|[【\[]配置说明\s*[｜|]\s*(U\d+)\s*结束[】\]])",
    re.IGNORECASE,
)
SUSPECT_NOTE = re.compile(r"^(?:\[Configuration|[【\[]配置说明)", re.IGNORECASE)
METADATA = re.compile(r"^(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|\||```|video_template(?:_|:))")


def index_script(text):
    lines = [(physical, value.strip()) for physical, value in
             enumerate(text.lstrip('\ufeff').splitlines(), 1) if value.strip()]
    sections, errors, seen = [], [], set()
    start = 1
    if not lines:
        errors.append('Script is empty.')
    for number, (physical, value) in enumerate(lines, 1):
        match = NOTE.match(value)
        if match:
            unit = (match.group(1) or match.group(2)).upper()
            if unit in seen:
                errors.append(f'Duplicate unit {unit} at nonempty line {number}.')
            seen.add(unit)
            if number == start:
                errors.append(f'Empty spoken section {unit} at nonempty line {number}.')
            sections.append({'unit': unit, 'spoken_start': start,
                             'spoken_end': number - 1, 'note_line': number,
                             'spoken_lines': number - start,
                             'note_physical_line': physical})
            start = number + 1
        elif SUSPECT_NOTE.match(value):
            errors.append(f'Unrecognised configuration note at nonempty line {number}.')
        elif METADATA.match(value):
            errors.append(f'Metadata/list markup inside speech at nonempty line {number}.')
    if start <= len(lines):
        errors.append(f'Lines {start}-{len(lines)} have no closing configuration note.')
    if lines and not sections:
        errors.append('No recognised sections.')
    return {'status': 'ERROR' if errors else 'OK',
            'nonempty_lines': len(lines),
            'spoken_lines': sum(s['spoken_lines'] for s in sections),
            'configuration_notes': len(sections), 'sections': sections, 'errors': errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('script', type=Path)
    args = parser.parse_args()
    try:
        result = index_script(args.script.read_text(encoding='utf-8-sig'))
    except (OSError, UnicodeError) as exc:
        print(json.dumps({'status': 'ERROR', 'errors': [str(exc)]}, ensure_ascii=True))
        return 2
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 0 if not result['errors'] else 1


if __name__ == '__main__':
    sys.exit(main())

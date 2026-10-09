#!/usr/bin/env python3
"""Comprueba destinos locales Markdown/HTML. Sin dependencias ni peticiones de red."""
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKIP = {'.git', '.venv', 'venv', 'node_modules'}

def anchors(path):
    source = path.read_text(encoding='utf-8')
    result = set(re.findall(r'''\b(?:id|name)=["']([^"']+)["']''', source))
    counts = {}
    for line in source.splitlines():
        match = re.match(r'^#{1,6}\s+(.+?)\s*#*$', line)
        if not match:
            continue
        title = re.sub(r'<[^>]+>', '', match[1]).lower()
        title = re.sub(r'[^\w\-\s\u200d\ufe0f]', '', title).replace(' ', '-')
        count = counts.get(title, 0)
        counts[title] = count + 1
        result.add(title if not count else f'{title}-{count}')
    return result

def main():
    errors = []
    checked = 0
    for doc in sorted(ROOT.rglob('*.md')):
        if any(part in SKIP for part in doc.relative_to(ROOT).parts):
            continue
        # Ignore fenced code: examples are not active links.
        source = re.sub(r'```.*?```|~~~.*?~~~', '', doc.read_text(encoding='utf-8'), flags=re.S)
        targets = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', source)
        targets += re.findall(r'''\b(?:src|href)=["']([^"']+)["']''', source)
        targets += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', source, flags=re.M)
        for raw in targets:
            raw = raw.strip('<>')
            parsed = urlsplit(raw)
            if parsed.scheme or parsed.netloc:
                continue
            checked += 1
            target = (ROOT / unquote(parsed.path.lstrip('/')) if parsed.path.startswith('/') else doc.parent / unquote(parsed.path)) if parsed.path else doc
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f'{doc.relative_to(ROOT)}: destino fuera del repositorio: {raw}')
            elif not target.exists():
                errors.append(f'{doc.relative_to(ROOT)}: falta {raw}')
            elif parsed.fragment and target.suffix == '.md' and unquote(parsed.fragment) not in anchors(target):
                errors.append(f'{doc.relative_to(ROOT)}: ancla inexistente {raw}')
    for error in errors:
        print(error, file=sys.stderr)
    print(f'{checked} enlaces locales comprobados; {len(errors)} errores.')
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())

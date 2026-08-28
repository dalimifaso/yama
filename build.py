#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""בונה את ימאות מ-template.html ומקובצי הנתונים שב-blobs/.

פלט:
  index.html          מסמך HTML עצמאי — נפתח ישירות בדפדפן, עובד גם בלי רשת
  dist/artifact.html  גוף העמוד בלבד, לפרסום כ-Artifact ב-claude.ai
"""
import io, json, os, re

ORDER = ['DATA', 'MET', 'RULES', 'CASES', 'DUEL', 'PARTS', 'NOTES', 'BOAT']
HERE = os.path.dirname(os.path.abspath(__file__))


def load_blobs():
    out = []
    for name in ORDER:
        path = os.path.join(HERE, 'blobs', f'{name}.json')
        if not os.path.exists(path):
            continue
        payload = io.open(path, encoding='utf-8').read().strip()
        json.loads(payload)                      # fail fast on malformed data
        out.append((name, payload))
    return out


def build():
    blobs = load_blobs()
    tpl = io.open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
    assert tpl.count('/*__DATA__*/') == 1, 'template must contain exactly one /*__DATA__*/ marker'
    body = tpl.replace('/*__DATA__*/', '\n'.join(f'const {n} = {p};' for n, p in blobs))

    os.makedirs(os.path.join(HERE, 'dist'), exist_ok=True)
    io.open(os.path.join(HERE, 'dist', 'artifact.html'), 'w', encoding='utf-8').write(body)

    # standalone: hoist <title> and the font links into a real <head>
    head, rest = [], body
    for pattern in (r'<title>.*?</title>', r'<link rel="preconnect"[^>]*>', r'<link rel="stylesheet"[^>]*>'):
        for m in re.findall(pattern, rest):
            head.append(m)
            rest = rest.replace(m, '', 1)
    doc = ('<!doctype html>\n<html lang="he">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
           + '\n'.join(head) + '\n</head>\n<body>\n' + rest.strip() + '\n</body>\n</html>\n')
    io.open(os.path.join(HERE, 'index.html'), 'w', encoding='utf-8').write(doc)
    return blobs, doc


if __name__ == '__main__':
    blobs, doc = build()
    for name, payload in blobs:
        data = json.loads(payload)
        if name == 'NOTES':
            detail = ', '.join(f'{k}: {len(v)}' for k, v in data.items())
            print(f'{name:6} {len(data)} ({detail})')
        else:
            print(f'{name:6} {len(data)}')
    print(f'\nindex.html: {round(len(doc.encode()) / 1024)} KB')

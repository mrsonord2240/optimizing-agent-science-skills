#!/usr/bin/env python3
"""Version-introduction claims in SKILL.md, checked against the samtools NEWS.md (public, unauthenticated: raw.githubusercontent.com,
develop branch) and against the installed samtools 1.24 itself. Which release section does each NEWS entry sit under?"""
import re, subprocess, sys, urllib.request
from lib import check, finish

news = urllib.request.urlopen('https://raw.githubusercontent.com/samtools/samtools/develop/NEWS.md', timeout=60).read().decode('utf-8')
lines = news.splitlines()
def release_of(pattern):
    """release heading above the first line matching pattern"""
    for i, l in enumerate(lines):
        if re.search(pattern, l):
            for j in range(i, -1, -1):
                if lines[j].startswith('Release '):
                    return lines[j], i + 1
    return None, None
claims = [
    ('--subsample default seed now a header hash', r'default seed for `samtools view --subsample`', '1.24'),
    ('-e filtering expressions in samtools view', r'samtools view now works with the filtering expressions', '1.12'),
    ('sclen keyword documentation', r'Add "sclen" filter expression keyword documentation', '1.16'),
    ('--exclude-no-read-group / -n', r'`--exclude-no-read-group`', '1.24'),
]
txt = open(sys.argv[1], encoding='utf-8').read()
for what, pat, claimed in claims:
    rel, ln = release_of(pat)
    print(f'{what}: NEWS line {ln} sits under "{rel}"; SKILL.md claims {claimed}')
    check(f'{what}: NEWS release == claimed {claimed}', rel is not None and rel.startswith(f'Release {claimed}'), rel or 'not found')
for frag in ('since samtools 1.12', 'documented from samtools 1.16', 'Samtools 1.24 adds `-n`', 'since 1.24', 'changed in samtools 1.24'):
    print(f'   SKILL.md contains {frag!r}:', frag in txt)
r = subprocess.run(['samtools', 'view', '--help'], capture_output=True, text=True)
h = r.stdout + r.stderr
print('installed samtools --help mentions:', [l.strip() for l in h.splitlines() if 'exclude-no-read' in l])
finish()

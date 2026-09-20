"""Shared helpers for the re-audit scripts (assert-on-content style)."""
import subprocess, sys

fails = []
def check(name, cond, detail=''):
    print(('PASS' if cond else 'FAIL'), name, detail)
    if not cond:
        fails.append(name)
    return cond

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd, executable='/bin/bash')
    return r.returncode, r.stdout, r.stderr

def finish():
    print('\nFAILS:', fails)

import re
def blocks(md_path):
    """Return [(section heading, lang, code)] for every fenced block of a markdown file."""
    txt = open(md_path, encoding='utf-8').read()
    out = []
    for m in re.finditer(r'```(bash|python)\n(.*?)```', txt, re.S):
        head = re.findall(r'^#{2,4} (.+)$', txt[:m.start()], re.M)
        out.append((head[-1] if head else '', m.group(1), m.group(2)))
    return out

def block(md_path, heading, lang, contains=''):
    for h, l, c in blocks(md_path):
        if h == heading and l == lang and contains in c:
            return c
    raise KeyError((heading, lang, contains))

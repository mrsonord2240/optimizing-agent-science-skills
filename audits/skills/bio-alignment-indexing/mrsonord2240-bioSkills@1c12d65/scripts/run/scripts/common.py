"""Shared helpers for audit scripts. Every check prints PASS/FAIL with the observed value (judge by output)."""
import subprocess, os, sys, hashlib, json

RESULTS = []


def sh(cmd, cwd=None, check=False):
    p = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, executable="/bin/bash")
    return p.returncode, p.stdout, p.stderr


def out(cmd, cwd=None):
    rc, o, e = sh(cmd, cwd)
    return rc, o.strip(), e.strip()


def md5(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def check(name, cond, detail=""):
    RESULTS.append({"check": name, "result": "PASS" if cond else "FAIL", "detail": str(detail)})
    print(f"[{'PASS' if cond else 'FAIL'}] {name} :: {detail}")
    return cond


def info(msg):
    print(f"[INFO] {msg}")


def dump(path):
    json.dump(RESULTS, open(path, "w"), indent=1)
    n = sum(r["result"] == "PASS" for r in RESULTS)
    print(f"== {n}/{len(RESULTS)} checks PASS ==")




# ---- shipped-snippet extraction: run the Skill's own text, not a re-typed copy -------------------------------
import re
SKILL_MD = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skill", "SKILL.md"), encoding="utf-8").read()
FENCE = "`" * 3


def fenced_blocks(lang=None):
    """Every fenced code block in the shipped SKILL.md as (lang, text)."""
    pat = FENCE + r"(\w*)\n(.*?)" + FENCE
    return [(m.group(1), m.group(2)) for m in re.finditer(pat, SKILL_MD, re.S) if lang is None or m.group(1) == lang]


def block_containing(needle, lang=None):
    for lg, txt in fenced_blocks(lang):
        if needle in txt:
            return txt
    raise KeyError(needle)

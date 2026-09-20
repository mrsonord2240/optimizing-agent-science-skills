"""Shared helpers for the bio-pileup-generation audit (run inside WSL `science`, env alignment-files)."""
import json, os, re, subprocess, sys
from collections import Counter

RUN = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(RUN, "data")
AFDATA = "/mnt/openscience/audit-envs/alignment-files/public-data"
HUMAN = AFDATA + "/human"
WORK = os.path.join(RUN, "work")
os.makedirs(WORK, exist_ok=True)
SKILL = os.path.join(RUN, "skill")

CHECKS = []  # (input_id, name, ok, detail)


def sh(cmd, check=False, timeout=600):
    """Run a shell command, return (rc, stdout, stderr)."""
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, executable="/bin/bash")
    if check and r.returncode != 0:
        raise RuntimeError(f"rc={r.returncode}: {cmd}\n{r.stderr}")
    return r.returncode, r.stdout, r.stderr


def check(inp, name, ok, detail=""):
    CHECKS.append((inp, name, bool(ok), str(detail)))
    print(f"[{'PASS' if ok else 'FAIL'}] in{inp} {name}" + (f"  -- {detail}" if detail else ""))
    return ok


def summary(inp):
    mine = [c for c in CHECKS if c[0] == inp]
    print(f"SUMMARY in{inp}: {sum(c[2] for c in mine)}/{len(mine)} assertions passed")
    json.dump(mine, open(os.path.join(RUN, f"checks_in{inp}.json"), "w"), indent=1)


def parse_bases(col5, ref):
    """Independent decoder of a samtools mpileup read-bases column.
    Returns (n_reads, Counter). n_reads counts one per read-slot (., , ACGTN acgtn * # > <), NOT ^ $ or indel text."""
    c = Counter()
    i = 0
    n = 0
    while i < len(col5):
        ch = col5[i]
        if ch == "^":
            c["^"] += 1
            i += 2  # ^ + MAPQ char
            continue
        if ch == "$":
            c["$"] += 1
            i += 1
            continue
        if ch in "+-":
            m = re.match(r"[+-](\d+)", col5[i:])
            k = int(m.group(1))
            seq = col5[i + len(m.group(0)): i + len(m.group(0)) + k]
            c[ch + seq] += 1  # e.g. '+AC'
            c["ins" if ch == "+" else "delmark"] += 1
            i += len(m.group(0)) + k
            continue
        n += 1
        if ch == ".":
            c["ref_fwd"] += 1
        elif ch == ",":
            c["ref_rev"] += 1
        elif ch == "*":
            c["*"] += 1
        elif ch == "#":
            c["#"] += 1
        elif ch in "<>":
            c[ch] += 1
        elif ch.isalpha():
            c[ch] += 1
        else:
            c["?" + ch] += 1
        i += 1
    return n, c


def mpileup_rows(text):
    rows = []
    for ln in text.splitlines():
        if not ln.strip() or ln.startswith("["):
            continue
        rows.append(ln.split("\t"))
    return rows

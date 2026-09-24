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


# ---------------- helpers added by the re-auditor (regression round 2026-09-20) ----------------
NEW = DATA + "/new.bam"; NEWREF = DATA + "/new.fa"
SYN = DATA + "/syn.bam"; SYNREF = DATA + "/syn.fa"
HBAM = HUMAN + "/test.paired_end.sorted.bam"; HREF = HUMAN + "/genome.fasta"


def mp_rows(ref, bam, opts="", region="", extra=""):
    """samtools mpileup rows as {(contig,pos): row list}; returns (dict, ordered list, rc, stderr)."""
    r = f"-r '{region}'" if region else ""
    rc, out, err = sh(f"samtools mpileup -f '{ref}' {opts} {r} {extra} '{bam}'")
    rows = mpileup_rows(out)
    return {(x[0], int(x[1])): x for x in rows}, rows, rc, err


def kwstr(kw):
    return ",".join(f"{k}={v}" for k, v in kw.items())


# (samtools mpileup options, pysam bam.pileup keyword args) pairs from the Skill's 'pysam Python Alternative' table
COMBOS = [
    ("default", "", {}),
    ("-B", "-B", dict(compute_baq=False)),
    ("-q 20 -Q 20", "-q 20 -Q 20", dict(min_mapping_quality=20, min_base_quality=20)),
    ("-Q 0", "-Q 0", dict(min_base_quality=0)),
    ("-x", "-x", dict(ignore_overlaps=False)),
    ("-A", "-A", dict(ignore_orphans=False)),
    ("--ff 0", "--ff 0", dict(flag_filter=0)),
    ("--rf 16", "--rf 16", dict(flag_require=16)),
    ("-E", "-E", dict(redo_baq=True)),
    ("-C 50", "-C 50", dict(adjust_capq_threshold=50)),
    ("-d 15", "-d 15", dict(max_depth=15)),
    ("-B -Q0 -q0 -x -A --ff 0", "-B -Q 0 -q 0 -x -A --ff 0",
     dict(compute_baq=False, min_base_quality=0, min_mapping_quality=0, ignore_overlaps=False, ignore_orphans=False, flag_filter=0)),
    ("-q 1 -Q 13 -B -x", "-q 1 -Q 13 -B -x", dict(min_mapping_quality=1, min_base_quality=13, compute_baq=False, ignore_overlaps=False)),
]


def py_depth(bam, ref, chrom, start, end, **kw):
    """{1-based pos: len(pileups)} using bam.pileup exactly as the Skill's table says; also {pos: n}."""
    import pysam
    d, dn = {}, {}
    with pysam.AlignmentFile(bam) as b:
        fa = pysam.FastaFile(ref)
        if kw.pop("_fasta", False):
            kw["fastafile"] = fa
        for col in b.pileup(chrom, start, end, truncate=True, **kw):
            d[col.pos + 1] = len(col.pileups)
            dn[col.pos + 1] = col.n
    return d, dn

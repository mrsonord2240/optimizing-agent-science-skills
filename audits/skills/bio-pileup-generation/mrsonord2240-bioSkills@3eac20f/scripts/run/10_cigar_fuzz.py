#!/usr/bin/env python3
"""Input 8 (NEW, re-auditor 2): own CIGAR-template differential test of the Skill's `pileup_text` / `indel_text` against
`samtools mpileup` (default, -B, -E, filter set), row for row.  Different from the previous auditors' fuzz: reads are built
from a fixed list of named CIGAR TEMPLATES (not a random walk), covering =/X runs, adjacent identical ops (1I2I, 2D1D, 20N30N),
I-D-I / D-I-D chains, N next to I/D, and indels at read ends (leading I, trailing I, I next to S).  Two BAMs:
  cg_legal.bam : templates an aligner can emit (I/D/N flanked by M-like ops, S/H only at the ends) + adjacent identical ops
  cg_wild.bam  : leading/trailing I, I-D-I, D-I-D, P ops, D at read end...  (legal SAM, outside anything the Skill claims)
Everything is SYNTHETIC and seeded.  Scored: legal set must be row-for-row identical.  Wild set: reported."""
import os, random, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
from collections import Counter

I = 8
pt = load_functions("SKILL.md")["pileup_text"]
OUT = DATA


def make(tag, seed, templates, n_reads):
    rng = random.Random(seed)
    rnd = lambda n: "".join(rng.choice("ACGT") for _ in range(n))
    refs = {}
    for c, L in (("cg1", 2600), ("cg2", 1400)):
        s = list(rnd(L))
        for _ in range(3):                        # N blocks
            p = rng.randrange(0, L - 30)
            for i in range(p, p + rng.randrange(1, 4)):
                s[i] = "N"
        for _ in range(4):                        # soft-masked blocks
            p = rng.randrange(0, L - 200)
            for i in range(p, p + rng.randrange(20, 100)):
                s[i] = s[i].lower()
        refs[c] = "".join(s)
    with open(f"{OUT}/{tag}.fa", "w", newline="\n") as f:
        for k, s in refs.items():
            f.write(f">{k}\n")
            for i in range(0, len(s), 70):
                f.write(s[i:i + 70] + "\n")
    comp = {"A": "C", "C": "G", "G": "T", "T": "A", "N": "A", "a": "C", "c": "G", "g": "T", "t": "A"}

    def build(c, pos, tpl):
        """tpl: list of (op, length-key). returns cigar, seq, qual, refspan  (pos 1-based)"""
        s = refs[c]
        ops = []
        for op, kind in tpl:
            if kind == "M":
                n = rng.randrange(6, 20)
            elif op in "IS":
                n = rng.randrange(1, 4)
            elif op == "D":
                n = rng.randrange(1, 5)
            elif op == "N":
                n = rng.randrange(15, 60)
            elif op in "HP":
                n = rng.randrange(1, 4)
            else:  # = X
                n = rng.randrange(2, 9)
            ops.append((op, n))
        rp, seq, cs = pos, [], ""
        for op, n in ops:
            cs += f"{n}{op}"
            if op in "M=X":
                for _ in range(n):
                    if rp - 1 >= len(s):
                        return None
                    b = s[rp - 1].upper()
                    if op == "X" or (op == "M" and rng.random() < 0.04):
                        b = comp[b]
                    if b == "N":
                        b = "C"
                    seq.append(b)
                    rp += 1
            elif op in "DN":
                rp += n
            elif op in "IS":
                seq.extend(rnd(n))
        if rp - 1 > len(s):
            return None
        qual = "".join(chr(33 + (rng.randrange(14, 41) if rng.random() > 0.08 else rng.randrange(2, 14))) for _ in seq)
        return cs, "".join(seq), qual, rp - pos

    recs, i = [], 0
    for c in refs:
        L = len(refs[c])
        for _ in range(n_reads[c]):
            tpl = rng.choice(templates)
            pos = rng.randrange(1, L - 200)
            r1 = build(c, pos, tpl)
            if r1 is None:
                continue
            i += 1
            mq = rng.choice([0, 1, 20, 30, 60, 60, 60, 255])
            rev = rng.random() < 0.5
            if rng.random() < 0.65:
                recs.append([f"c{i}", 16 if rev else 0, c, pos, mq, r1[0], "*", 0, 0, r1[1], r1[2]])
            else:  # proper pair, overlapping mates
                pos2 = pos + rng.randrange(3, 40)
                r2 = build(c, pos2, rng.choice(templates))
                if r2 is None:
                    continue
                recs.append([f"c{i}", 99 if not rev else 83, c, pos, mq, r1[0], "=", pos2, pos2 - pos + 60, r1[1], r1[2]])
                recs.append([f"c{i}", 147 if not rev else 163, c, pos2, 60, r2[0], "=", pos, pos - pos2 - 60, r2[1], r2[2]])
    sam = f"{OUT}/{tag}.sam"
    with open(sam, "w", newline="\n") as f:
        f.write("@HD\tVN:1.6\tSO:unsorted\n")
        for k, s in refs.items():
            f.write(f"@SQ\tSN:{k}\tLN:{len(s)}\n")
        for r in recs:
            f.write("\t".join(map(str, r)) + "\n")
    rc, out, err = sh(f"cd {OUT} && samtools faidx {tag}.fa && samtools sort -o {tag}.bam {tag}.sam && samtools index {tag}.bam && rm {tag}.sam && samtools view -c {tag}.bam")
    print(tag, "reads", len(recs), "bam records", out.strip(), err.strip()[:200])
    return {k: len(v) for k, v in refs.items()}


M = ("M", "M")
def t(*ops):
    return [(o, "M" if o == "M" else "x") for o in ops]

LEGAL = [
    t("M"), t("M"), t("M"),
    t("M", "I", "M"), t("M", "D", "M"), t("M", "N", "M"),
    t("M", "I", "D", "M"), t("M", "D", "I", "M"),                       # adjacent I+D and D+I flanked by M
    t("M", "N", "I", "M"), t("M", "I", "N", "M"), t("M", "D", "N", "M"), t("M", "N", "D", "M"),
    t("M", "I", "I", "M"), t("M", "D", "D", "M"), t("M", "N", "N", "M"),  # adjacent identical ops
    t("=", "X", "=", "M"), t("M", "=", "I", "X", "M"), t("M", "D", "=", "I", "M"), t("=", "X", "D", "M"),
    t("S", "M", "I", "M", "S"), t("H", "S", "M", "D", "M"), t("M", "N", "M", "S"), t("S", "M", "X", "I", "M"),
]
WILD = [
    t("I", "M"), t("M", "I"), t("S", "I", "M"), t("M", "I", "S"), t("M", "D"), t("M", "D", "S"),
    t("M", "I", "D", "I", "M"), t("M", "D", "I", "D", "M"), t("M", "N", "I", "D", "M"),
    t("M", "P", "I", "M"), t("M", "D", "P", "M"), t("S", "D", "M"), t("M", "I", "D"),
]
NAMES = {  # readable template names for the per-template wild report
    id(w): "".join(f"{o}" for o, _ in w) for w in WILD}


def compare(bam, ref, lens, so, pk):
    """returns dict(rows, ndiff, marker_only, other, crashed, examples, mrows)"""
    mpd, mrows, rc, err = mp_rows(ref, bam, so)
    strip = lambda x: re.sub(r"[+-]\d+[A-Za-z*]+", "", x)
    d = dict(rows=0, ndiff=0, marker_only=0, other=0, crashed=None, examples=[], mrows=mrows)
    for c, Ln in lens.items():
        try:
            for line in pt(bam, ref, c, 0, Ln, **pk):
                f = line.split("	")
                d["rows"] += 1
                a = mpd.get((f[0], int(f[1])))
                if a != f:
                    d["ndiff"] += 1
                    if a and a[3] == f[3] and a[5] == f[5] and strip(a[4]) == strip(f[4]):
                        d["marker_only"] += 1
                    else:
                        d["other"] += 1
                    if len(d["examples"]) < 2:
                        d["examples"].append((f[0], f[1], a[4][:50] if a else None, f[4][:50]))
        except Exception as e:  # informational: record and stop this contig
            d["crashed"] = f"{type(e).__name__}: {e} (after {d['rows']} rows)"
            break
    return d


if __name__ == "__main__":
    OPT = [  # (label, samtools opts, pysam kwargs)
        ("default", "", {}),
        ("-B", "-B", dict(compute_baq=False)),
        ("-E", "-E", dict(redo_baq=True)),
        ("-q 20 -Q 20 -x -A", "-q 20 -Q 20 -x -A", dict(min_mapping_quality=20, min_base_quality=20, ignore_overlaps=False, ignore_orphans=False)),
        ("--ff 0 -Q 0 -B", "--ff 0 -Q 0 -B", dict(flag_filter=0, min_base_quality=0, compute_baq=False)),
    ]
    lens = make("cg_legal", 7331, LEGAL, {"cg1": 850, "cg2": 450})
    bam, ref = f"{DATA}/cg_legal.bam", f"{DATA}/cg_legal.fa"
    for lab, so, pk in OPT:
        d = compare(bam, ref, lens, so, pk)
        mrows = d["mrows"]
        nm = sum(1 for r in mrows if re.search(r"[+-]\d+[A-Za-z]", r[4]))
        nadj = sum(1 for r in mrows if re.search(r"[+-]\d+[A-Za-z]+[+-]\d+[A-Za-z]", r[4]))
        nlow = sum(1 for r in mrows if r[2].islower())
        print(f"cg_legal [{lab}] samtools rows {len(mrows)} pileup_text rows {d['rows']} differing {d['ndiff']} crashed={d['crashed']} examples {d['examples']}")
        check(I, f"legal templates [{lab}]: pileup_text == samtools mpileup row for row ({d['rows']} rows, {nm} rows with indel markers, {nadj} with 2 adjacent markers, {nlow} lower-case-reference rows)",
              d["ndiff"] == 0 and d["crashed"] is None and d["rows"] == len(mrows) and nm > 150 and nadj > 10, f"differing={d['ndiff']} crashed={d['crashed']} examples={d['examples']}")

    # ---- wild templates, one BAM per template (informational: outside what an aligner emits)
    print("--- wild templates (per template, all option sets; INFO only, not scored against the Skill) ---")
    for k, w in enumerate(WILD):
        name = "".join(o for o, _ in w)
        L3 = make(f"cw{k}", 900 + k, [w], {"cg1": 260, "cg2": 100})
        row = []
        for lab, so, pk in OPT:
            d = compare(f"{DATA}/cw{k}.bam", f"{DATA}/cw{k}.fa", L3, so, pk)
            if d["ndiff"] or d["crashed"]:
                row.append(f"{lab}: {d['ndiff']}/{d['rows']} rows differ" + (f", CRASH {d['crashed']}" if d["crashed"] else ""))
        print(f"INFO wild template {name:8s} " + " | ".join(row) if row else "identical to samtools for all 5 option sets")
    summary(I)

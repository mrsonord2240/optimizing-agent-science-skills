#!/usr/bin/env python3
"""NEW differential-test data by the RE-AUDITOR: random reads with random CIGARs, strands, MAPQs, base qualities, flags and
overlapping mates on a soft-masked reference containing N. Writes data/fz_clean.{fa,bam} and data/fz_exotic.{fa,bam}.
clean  : every I/D/N op is flanked by M (what an aligner emits); S/H only at the ends; ~10% orphans / mate-unmapped etc.
exotic : additionally leading/trailing I, adjacent I/D/N, D right after S, ... (odd but legal SAM), to look for helper failures
         that are outside anything the Skill claims (reported as informational, not scored against the Skill).
Everything is SYNTHETIC and seeded."""
import os, random, subprocess, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(OUT, exist_ok=True)


def make(tag, seed, exotic):
    rng = random.Random(seed)
    rnd = lambda n: "".join(rng.choice("ACGT") for _ in range(n))
    refs = {"fz1": list(rnd(3000)), "fz2": list(rnd(1500))}
    for c in refs:                                    # a few N and soft-masked blocks
        s = refs[c]
        for _ in range(3):
            p = rng.randrange(0, len(s) - 30)
            for i in range(p, p + rng.randrange(1, 6)):
                s[i] = "N"
        for _ in range(4):
            p = rng.randrange(0, len(s) - 200)
            for i in range(p, p + rng.randrange(20, 120)):
                s[i] = s[i].lower()
    refs = {k: "".join(v) for k, v in refs.items()}
    with open(os.path.join(OUT, f"{tag}.fa"), "w", newline="\n") as f:
        for k, s in refs.items():
            f.write(f">{k}\n")
            for i in range(0, len(s), 60):
                f.write(s[i:i + 60] + "\n")
    comp = {"A": "C", "C": "G", "G": "T", "T": "A", "N": "A"}

    def read(c, pos, ncore):
        """build cigar ops, seq, qual; pos is 1-based"""
        s = refs[c]
        ops = []
        if rng.random() < 0.15:
            ops.append(("S" if rng.random() < .7 else "H", rng.randrange(1, 6)))
        left = ncore
        ops.append(("M", rng.randrange(8, 25)))
        left -= ops[-1][1]
        while left > 0:
            k = rng.random()
            if k < 0.12:
                ops.append(("I", rng.randrange(1, 4)))
            elif k < 0.24:
                ops.append(("D", rng.randrange(1, 5)))
            elif k < 0.29:
                ops.append(("N", rng.randrange(20, 90)))
            if exotic and rng.random() < 0.25 and ops[-1][0] != "M":
                ops.append(("D" if rng.random() < .5 else "I", rng.randrange(1, 3)))   # adjacent indel ops
            m = rng.randrange(6, 25)
            ops.append(("M", m))
            left -= m
        if rng.random() < 0.15:
            ops.append(("S" if rng.random() < .7 else "H", rng.randrange(1, 6)))
        if exotic and rng.random() < 0.12:
            ops.insert(0 if ops[0][0] not in "SH" else 1, ("I", rng.randrange(1, 3)))   # leading insertion
        if exotic and rng.random() < 0.12:
            ops.append(("I", rng.randrange(1, 3)))                                    # trailing insertion
        rp = pos
        seq, cs = [], ""
        for op, n in ops:
            cs += f"{n}{op}"
            if op == "M":
                for _ in range(n):
                    b = s[rp - 1].upper() if rp - 1 < len(s) else "A"
                    if rng.random() < 0.05:
                        b = comp[b]
                    if b == "N" and rng.random() < .5:
                        b = "C"
                    seq.append(b)
                    rp += 1
            elif op in "DN":
                rp += n
            elif op in "IS":
                seq.extend(rnd(n))
        end = rp - 1
        if end > len(s):
            return None
        qual = []
        for _ in seq:
            r = rng.random()
            qual.append(chr(33 + (93 if r < 0.02 else 2 if r < 0.06 else 12 if r < .09 else 13 if r < .12 else rng.randrange(14, 41))))
        return cs, "".join(seq), "".join(qual)

    recs = []
    i = 0
    for c in refs:
        L = len(refs[c])
        for _ in range(int(L / 3.2)):
            pos = rng.randrange(1, L - 120)
            core = rng.randrange(40, 110)
            r1 = read(c, pos, core)
            if r1 is None:
                continue
            mq = rng.choice([0, 1, 19, 20, 20, 30, 60, 60, 60, 60, 255])
            i += 1
            kind = rng.random()
            rev = rng.random() < .5
            if kind < 0.55:            # single-end
                recs.append([f"r{i}", 16 if rev else 0, c, pos, mq, r1[0], "*", 0, 0, r1[1], r1[2]])
            elif kind < 0.90:          # proper pair with overlapping mates
                pos2 = pos + rng.randrange(5, 60)
                r2 = read(c, pos2, rng.randrange(40, 110))
                if r2 is None:
                    continue
                recs.append([f"r{i}", 99 if not rev else 83, c, pos, mq, r1[0], "=", pos2, pos2 - pos + 60, r1[1], r1[2]])
                recs.append([f"r{i}", 147 if not rev else 163, c, pos2, rng.choice([mq, 60]), r2[0], "=", pos, pos - pos2 - 60, r2[1], r2[2]])
            else:                      # odd flags
                fl = rng.choice([65, 73, 1024, 256, 512, 2048, 1024 | 16, 256 | 16, 97, 145, 4 | 0])
                if fl & 4:
                    recs.append([f"r{i}", 4, c, pos, 0, "*", "*", 0, 0, r1[1], r1[2]])
                else:
                    recs.append([f"r{i}", fl, c, pos, mq, r1[0], "=", pos + 100, 0, r1[1], r1[2]])
    sam = os.path.join(OUT, f"{tag}.sam")
    with open(sam, "w", newline="\n") as f:
        f.write("@HD\tVN:1.6\tSO:unsorted\n")
        for k, s in refs.items():
            f.write(f"@SQ\tSN:{k}\tLN:{len(s)}\n")
        f.write("@RG\tID:rgF\tSM:fuzz\tPL:ILLUMINA\n")
        for r in recs:
            f.write("\t".join(map(str, r)) + "\tRG:Z:rgF\n")
    r = subprocess.run(f"cd {OUT} && samtools faidx {tag}.fa && samtools sort -o {tag}.bam {tag}.sam && samtools index {tag}.bam && rm {tag}.sam && samtools view -c {tag}.bam",
                       shell=True, capture_output=True, text=True, executable="/bin/bash")
    print(tag, "records", len(recs), "bam records:", r.stdout.strip(), r.stderr.strip()[:200])


make("fz_clean", 101, False)
make("fz_exotic", 202, True)

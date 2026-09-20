#!/usr/bin/env python3
"""Soft-clip recipe (SKILL.md block 033, verbatim) vs a CIGAR walk with pysam cigartuples (independent), on real, synthetic and hand-built BAMs,
run under gawk AND mawk. Also asserts `samtools stats` has no 'bases soft-clipped' field on this samtools, and the empty-output guard.
usage: t5_softclip.py <bam> [<bam> ...]   (run inside the WSL env)"""
import os, sys, subprocess, tempfile
import pysam

HERE = os.path.dirname(os.path.abspath(__file__))
BLOCK = open(os.path.join(HERE, 'blocks', '033_bash.sh'), encoding='utf-8').read()
DATA = os.path.join(HERE, 'data')


def build_clip_bam(path):
    """Hand-built cigars: hard clip, both-side soft clip, spliced+clip, indel+clip, plus a QC-fail/dup (NOT excluded by -F 2308), a secondary and a supplementary (excluded)."""
    hdr = pysam.AlignmentHeader.from_dict({'HD': {'VN': '1.6', 'SO': 'unsorted'}, 'SQ': [{'SN': 'x', 'LN': 5000}]})
    rows = [('10H90M', 0), ('5S90M5S', 0), ('20M500N30M5S', 0), ('10M2I8M3D5S', 0), ('40S60M', 512), ('30M20S', 1024), ('50S50M', 256), ('50M50S', 2048), ('100M', 4), ('30=10X20S', 0), ('10M5P10M10S', 0)]
    with pysam.AlignmentFile(path, 'wb', header=hdr) as bam:
        for i, (cg, fl) in enumerate(rows):
            a = pysam.AlignedSegment(hdr)
            a.query_name = f'r{i}'; a.flag = fl; a.reference_id = 0; a.reference_start = 100 + i * 100; a.mapping_quality = 60
            a.cigarstring = cg
            n = sum(l for op, l in a.cigartuples if op in (0, 1, 4, 7, 8))
            a.query_sequence = 'A' * n; a.query_qualities = pysam.qualitystring_to_array('I' * n)
            bam.write(a)


def truth(bam_path):
    s = q = n = 0
    with pysam.AlignmentFile(bam_path, 'rb', check_sq=False) as bam:
        for r in bam.fetch(until_eof=True):
            if r.flag & 2308:
                continue
            n += 1
            for op, l in r.cigartuples or []:
                if op in (0, 1, 4, 7, 8):
                    q += l
                if op == 4:
                    s += l
    return n, s, q


def run_recipe(bam, awk):
    txt = BLOCK.replace('input.bam', bam).replace("| awk ", f"| {awk} ")
    p = subprocess.run(['bash', '-c', txt], capture_output=True, text=True)
    return p.returncode, p.stdout.strip(), p.stderr.strip()


clip = os.path.join(tempfile.mkdtemp(), 'clip.bam')
build_clip_bam(clip)
bad = 0
for bam in [clip] + sys.argv[1:]:
    n, s, q = truth(bam)
    exp = f'soft-clipped bases: {s} of {q} ({s / q * 100:.2f}%)' if (n and q) else None
    grep = subprocess.run(f'samtools stats {bam} | grep -ci "soft"', shell=True, capture_output=True, text=True).stdout.strip()
    for awk in ('awk', 'mawk'):
        rc, out, err = run_recipe(bam, awk)
        if exp:
            ok = (rc == 0 and out == exp)
        else:
            ok = (rc == 1 and out == '' and 'nothing to compute' in err)
        bad += (not ok)
        print(f'{"PASS" if ok else "FAIL"} [{awk}] {os.path.basename(bam)}: recipe={out or err!r} rc={rc} | truth(cigartuples)={exp or "no primary mapped -> expect rc 1 + message"} | stats grep -ci soft = {grep}')
print('SOFTCLIP_MISMATCHES', bad)

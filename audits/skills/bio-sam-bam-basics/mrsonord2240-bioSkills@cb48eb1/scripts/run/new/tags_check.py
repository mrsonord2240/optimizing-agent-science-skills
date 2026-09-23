"""Input 5 add-on: rows of the SKILL.md tag table that regress/in5.py does not exercise, run on the synthetic
repeat genome from Input 5 (data/aln, seeded, synthetic reads) with real aligners/tools.
Rows: MC:Z from bwa mem, cs:Z (minimap2 --cs), ts:A (minimap2 -ax splice), RX:Z (fgbio AnnotateBamWithUmis),
NM/MD via calmd, ms:i of minimap2 vs fixmate.
"""
import os, re, sys
os.environ['AUDIT_INPUT'] = '5'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note, sh
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = RUN + '/data/aln'
W = RUN + '/data/tags'
sh(f'rm -rf {W}; mkdir -p {W}')


def tagset(cmd):
    o = sh(f"{cmd} | cut -f12- | tr '\\t' '\\n' | cut -d: -f1 | sort -u | tr '\\n' ' '")[1]
    return set(o.split())


t_bwa = tagset(f'samtools view {A}/bwa.bam')
check('Skill row "MC:Z | samtools fixmate -m (bwa mem also writes it)": bwa mem output carries MC:Z without any fixmate', 'MC' in t_bwa, sorted(t_bwa))
t_mm = tagset(f'samtools view {A}/mm2.bam')
check('Skill row "minimap2\'s own ms:i is an unrelated DP score": minimap2 -ax sr writes ms but no MC (so ms there is not fixmate\'s mate score)', 'ms' in t_mm and 'MC' not in t_mm, sorted(t_mm))
sh(f'cd {W}; minimap2 -ax sr --cs {A}/g.fa {A}/r1.fq {A}/r2.fq 2>/dev/null | samtools view -b -o cs.bam -')
t_cs = tagset(f'samtools view {W}/cs.bam')
check('Skill row "cs:Z | minimap2 --cs": present with --cs', 'cs' in t_cs, sorted(t_cs))
check('cs:Z absent without --cs (minimap2 default)', 'cs' not in t_mm, sorted(t_mm))
# ts:A with -ax splice on DNA reads: report what happens (unspliced reads may carry no ts)
sh(f'cd {W}; minimap2 -ax splice {A}/g.fa {A}/r1.fq 2>/dev/null | samtools view -b -o sp.bam -')
t_sp = tagset(f'samtools view {W}/sp.bam')
note('minimap2 -ax splice tags on unspliced DNA reads (ts:A only appears for spliced alignments)', sorted(t_sp))
# MD via calmd
o = sh(f'samtools calmd -u {A}/mm2.bam {A}/g.fa 2>/dev/null | samtools view - | cut -f12- | head -1')[1]
check('Skill row "MD:Z ... samtools calmd regenerates it": calmd adds MD:Z to minimap2 BAM (which has none)', 'MD:Z:' in o, o.strip()[:80])
# fgbio AnnotateBamWithUmis: single-end BAM in FASTQ order + UMI fastq
sh(f'cd {W}; bwa mem {A}/g.fa {A}/r1.fq 2>/dev/null | head -400 | samtools view -b -o se.bam -')
n = int(sh(f'samtools view -c -F 4 {W}/se.bam')[1])
names = sh(f'samtools view {W}/se.bam | cut -f1')[1].split()
with open(W + '/umi.fq', 'w', newline='\n') as fh:
    for i, nm in enumerate(names):
        umi = ''.join('ACGT'[(i >> (2 * k)) & 3] for k in range(6))
        fh.write(f'@{nm}\n{umi}\n+\n{"I" * 6}\n')
rc, o, e = sh(f'cd {W}; fgbio AnnotateBamWithUmis -i se.bam -f umi.fq -o umi.bam 2>&1 | tail -3; samtools view umi.bam | head -1 | cut -f12- ; samtools view umi.bam | grep -c "RX:Z:"; samtools view -c umi.bam')
lines = o.strip().splitlines()
ok = len(lines) >= 2 and lines[-2].isdigit() and lines[-1].isdigit() and lines[-2] == lines[-1] and int(lines[-1]) > 0
check('Skill row "RX:Z | fgbio AnnotateBamWithUmis": every record of the output BAM carries RX:Z', ok, ' | '.join(lines[-4:])[:250])

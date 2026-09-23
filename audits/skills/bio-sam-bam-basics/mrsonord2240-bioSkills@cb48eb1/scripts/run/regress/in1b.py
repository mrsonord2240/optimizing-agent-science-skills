"""Input 1 add-on: the usage-guide prompt 'Get reads from multiple regions: chr1:1000-2000 and chr2:3000-4000' has no snippet in the
Skill; test what a naive multi-region call does, plus the 1-based faidx claim from the coordinate table."""
import os, sys
os.environ['AUDIT_INPUT'] = '1'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chk import check, note, sh
import pysam

D = os.environ['AFDATA'] + '/human'
BAM, REF = D + '/test.paired_end.sorted.bam', D + '/genome.fasta'
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# overlapping regions (a read spanning both would be returned twice if regions are handled independently)
r1, r2 = 'chr22:2000-3000', 'chr22:2500-3500'
union = int(sh(f'samtools view -c {BAM} chr22:2000-3500')[1])
rc, o, e = sh(f'samtools view {BAM} {r1} {r2} | cut -f1,2,4 | sort | uniq -d | wc -l; samtools view -c {BAM} {r1} {r2}; samtools view -c -M {BAM} {r1} {r2}')
dup_default, n_default, n_M = [int(x) for x in o.split()]
note('multi-region call, overlapping regions: duplicated records / count default / count with -M / true union', (dup_default, n_default, n_M, union))
check('Skill multi-region section: default `view bam r1 r2` prints overlapping records twice (7356 rows vs 5426 distinct, as documented); -M gives the union', (n_default, union, n_M) == (7356, 5426, 5426) and dup_default > 0, f'default {n_default} (dup records {dup_default}), -M {n_M}, union {union}')
# pysam: two fetches concatenated DO double count
with pysam.AlignmentFile(BAM) as bam:
    naive = sum(1 for _ in bam.fetch('chr22', 1999, 3000)) + sum(1 for _ in bam.fetch('chr22', 2499, 3500))
check('pysam: summing fetch() over two overlapping regions double-counts reads (naive multi-region loop is wrong)', naive > union, f'naive {naive} vs union {union}')
# BED via -L
open(RUN + '/data/two.bed', 'w').write('chr22\t1999\t3000\nchr22\t2499\t3500\n')
rc, o, e = sh(f'samtools view -c -L {RUN}/data/two.bed {BAM}')
check('-L BED (0-based) with the same two regions equals the union count', int(o) == union, f'{o.strip()} vs {union}')
# faidx 1-based (coordinate table row)
rc, o, e = sh(f'samtools faidx {REF} chr22:1-5 | tail -1')
first = ''.join(l.strip() for l in open(REF) if not l.startswith('>'))[:5].upper()
check('samtools faidx chr22:1-5 returns the FIRST 5 bases (1-based, closed) as the Skill states', o.strip().upper() == first, f'{o.strip()} vs {first}')
# 1-based region view: chr22:1952-1952 includes read starting at POS 1952 (first read)
n = int(sh(f'samtools view -c {BAM} chr22:1952-1952')[1])
with pysam.AlignmentFile(BAM) as bam:
    m = sum(1 for _ in bam.fetch('chr22', 1951, 1952))
    m_wrong = sum(1 for _ in bam.fetch('chr22', 1952, 1953))
check('1-based samtools chr22:1952-1952 == 0-based fetch(1951,1952) (single base at POS 1952)', n == m, f'{n} == {m}, != {m_wrong}')

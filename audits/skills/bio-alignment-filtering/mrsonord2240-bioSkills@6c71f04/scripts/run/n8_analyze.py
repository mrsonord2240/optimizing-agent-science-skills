#!/usr/bin/env python3
"""NEW input 8 (Variant B): the Bowtie2 / HISAT2 / STAR / BWA / minimap2 MAPQ table on REAL reads, not on the synthetic repeat genome.
(A) 2821 real DNA pairs (nf-core, chr22 slice) re-aligned; (B) 3521 real RNA-seq pairs re-aligned; multiplicity truth for B = NH of the
original real STAR alignment (test.rna.paired_end.sorted.bam, 1274 multi-mapped primaries) and, second method, `bowtie2 -k 10` locus count.
Thresholds are parsed out of the fixed SKILL.md, retention counted with the real `samtools view`."""
import collections, os, re, sys
import pysam
from lib import check, sh, finish

DA, DB, SK = sys.argv[1], sys.argv[2], sys.argv[3]
AFD = os.environ['AFDATA']
txt = open(f'{SK}/SKILL.md', encoding='utf-8').read()
rules = {'bwa': (1, 30), 'bowtie2': (2, 23), 'bowtie2_local': (2, 23), 'star': (255, 255), 'hisat2': (2, 60), 'minimap2': (1, 60)}
for name, pat in [('Bowtie2', r'\| Bowtie2 \| `-q 2`'), ('HISAT2', r'\| HISAT2 \| `-q 2`'), ('STAR', r'\| \*\*STAR\*\* \| `-q 255`')]:
    check(f'SKILL.md table row {name} present with the thresholds used here', re.search(pat, txt) is not None)

def prim(bam, extra=''):
    return [l.split('\t') for l in sh(f'samtools view -F 2308 {extra} {bam}')[1].splitlines()]
def hist(bam): return dict(sorted(collections.Counter(int(x[4]) for x in prim(bam)).items()))

print('=== (A) real DNA pairs, 40 kb chr22 slice')
n_in = 2 * 2821
for al in ('bwa', 'bowtie2', 'bowtie2_local', 'hisat2', 'minimap2', 'star'):
    bam = f'{DA}/{al}.bam'
    npr = len(prim(bam))
    print(f'  {al}: primary mapped {npr}/{n_in}; MAPQ {hist(bam)}')
    if al in rules:
        qa, qh = rules[al]
        ka = int(sh(f'samtools view -c -F 2308 -q {qa} {bam}')[1]); kh = int(sh(f'samtools view -c -F 2308 -q {qh} {bam}')[1])
        print(f'     drop-ambiguous -q {qa}: keeps {ka}/{npr} ({ka/npr:.1%}); high-confidence -q {qh}: keeps {kh}/{npr} ({kh/npr:.1%})')
        check(f'{al} real DNA: -q {qa} keeps >= 97% of mapped reads (non-repetitive slice)', ka / npr >= 0.97, f'{ka/npr:.3f}')
        if al == 'minimap2':
            print('     (minimap2 -ax sr is NOT the long-read use the table row names; characterisation only, -q 60 asserts nothing here)')
        elif al not in ('star',):
            check(f'{al} real DNA: -q {qh} keeps >= 85% of mapped reads', kh / npr >= 0.85, f'{kh/npr:.3f}')
k10 = len(prim(f'{DA}/bowtie2_k10.bam')); k1 = len(prim(f'{DA}/bowtie2.bam'))
check('bowtie2 -k 10 finds no extra alignments on the real DNA slice (no multi-mappers to remove: the table is exercised on unique reads here)', k10 == k1, f'{k10} vs {k1}')
bmax = max(int(x[4]) for x in prim(f'{DA}/bowtie2.bam')); lmax = max(int(x[4]) for x in prim(f'{DA}/bowtie2_local.bam'))
print(f'  Bowtie2 max MAPQ end-to-end {bmax}, --local {lmax}')
check('Bowtie2 end-to-end max MAPQ 42 on real reads (prose)', bmax == 42)
print(f'  Bowtie2 --local max MAPQ {lmax}: text "23 is a community uniquely-mapped convention" and "maxes at 42" are stated for end-to-end only')

print('\n=== (B) real RNA-seq pairs: multiplicity truth = NH of the real STAR alignment')
truth = {}
for r in pysam.AlignmentFile(f'{AFD}/human/test.rna.paired_end.sorted.bam'):
    if r.is_secondary or r.is_unmapped: continue
    truth[(r.query_name, r.is_read1)] = r.get_tag('NH')
spans = collections.defaultdict(list)
for r in pysam.AlignmentFile(f'{AFD}/human/test.rna.paired_end.sorted.bam'):
    if r.is_unmapped: continue
    spans[(r.query_name, r.is_read1)].append((r.reference_start, r.reference_end))
def n_loci(sp):
    sp = sorted(sp); loci = []
    for a, b in sp:
        if loci and a < loci[-1][1]: loci[-1][1] = max(loci[-1][1], b)
        else: loci.append([a, b])
    return len(loci)
distinct = {k for k, sp in spans.items() if n_loci(sp) > 1}
print(f'  STAR NH>1 reads {sum(1 for v in truth.values() if v > 1)}; of these with >= 2 NON-OVERLAPPING alignment spans (distinct loci): {len(distinct)}')
print('  (STAR counts alternative splicings/soft-clip variants of the SAME locus in NH, so NH>1 is not a multi-locus truth)')
multi = distinct; uniq = {k for k, v in truth.items() if v == 1}
multi_nh = {k for k, v in truth.items() if v > 1}
print(f'  real STAR primaries: unique (NH==1) {len(uniq)}, multi-mapped (NH>1) {len(multi)}')
for al in ('bwa', 'bowtie2', 'hisat2', 'minimap2', 'star'):
    bam = f'{DB}/{al}.bam'; qa, qh = rules[al]
    rows = prim(bam)
    def key(x): return (x[0], bool(int(x[1]) & 64))
    got = {key(x): int(x[4]) for x in rows}
    mm = [k for k in multi if k in got]; un = [k for k in uniq if k in got]
    surv_mm = sum(1 for k in mm if got[k] >= qa); surv_un = sum(1 for k in un if got[k] >= qa)
    surv_mm_h = sum(1 for k in mm if got[k] >= qh)
    print(f'  {al}: re-mapped {len(rows)}; truth-multi reads mapped {len(mm)}: survive drop-ambiguous -q {qa}: {surv_mm}, high-conf -q {qh}: {surv_mm_h}; '
          f'truth-unique mapped {len(un)}: survive -q {qa}: {surv_un} ({surv_un/max(len(un),1):.1%})')
    res = dict(mm=len(mm), s=surv_mm, sh=surv_mm_h, un=len(un), su=surv_un)
    globals().setdefault('R', {})[al] = res
    if al == 'bwa':
        print('     BWA MAPQ of the multi-mapped reads:', dict(sorted(collections.Counter(got[k] for k in mm).items())))
    if al == 'hisat2' or al == 'star':
        nhre = {key(x): int([t for t in x[11:] if t.startswith('NH:i:')][0][5:]) for x in rows if any(t.startswith('NH:i:') for t in x[11:])}
        nh_surv = sum(1 for k in mm if nhre.get(k, 0) == 1)
        print(f'     -e [NH]==1 keeps {nh_surv} of the {len(mm)} truth-multi reads; MAPQ threshold keeps {surv_mm}')
        res['nh_surv'] = nh_surv
# bowtie2 -k 10 locus counts (second independent multiplicity method)
cnt = collections.Counter((x[0], bool(int(x[1]) & 64)) for x in [l.split('\t') for l in sh(f'samtools view -F 4 {DB}/bowtie2_k10.bam')[1].splitlines()])
kk = {k for k, v in cnt.items() if v > 1}
print(f'  bowtie2 -k 10: reads with >1 reported alignment: {len(kk)}; of these truth-multi (STAR NH>1): {len(kk & multi)}')
b = R['bowtie2']
print('  Bowtie2 default: reads with >1 alignment (per -k 10) surviving -q 2:',
      sum(1 for x in prim(f'{DB}/bowtie2.bam') if (x[0], bool(int(x[1]) & 64)) in kk and int(x[4]) >= 2), 'of', len(kk))
check('Bowtie2 -q 2 removes every read that bowtie2 -k 10 itself reports at >1 locus', sum(1 for x in prim(f'{DB}/bowtie2.bam') if (x[0], bool(int(x[1]) & 64)) in kk and int(x[4]) >= 2) == 0 or len(kk) == 0, f'{len(kk)} multi-locus reads')
# thresholds vs truth (assert only where the truth set is big enough to mean something)
print(f'  distinct-locus truth set size: {len(multi)} mates')
for al in ('hisat2', 'star', 'bowtie2'):
    r = R[al]
    if r['mm'] >= 20:
        check(f'{al} real RNA: drop-ambiguous threshold leaves <= 20% of the distinct-locus reads it maps', r['s'] / r['mm'] <= 0.20, f'{r["s"]}/{r["mm"]}')
    else:
        print(f'  {al}: only {r["mm"]} distinct-locus reads mapped by this aligner; no assertion (too few)')
r = R['bwa']
print(f'  bwa -q 1 leaves {r["s"]}/{r["mm"]} of the truth-multi reads (BWA gives MAPQ 0 only to exact ties; real multi-mappers with a better hit get MAPQ>0)')
finish()

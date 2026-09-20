#!/usr/bin/env python3
"""SYNTHETIC multi-gene exon-skipping simulation with known truth (audit of bio-differential-splicing).

120 genes on contig chrP (+ strand), each a 3-exon cassette gene (E1 101-200, E2 501-600, E3 901-1000 relative to gene base).
Groups (3 replicates each, single-end 50 nt, XS tag set):
  A = baseline
  B = A with a planted dPSI in genes 0..29 (24 strong |d|>=0.3, 6 weak |d|=0.15; half of each go up, half down)
  C = a second independent set of replicates of A (no change anywhere) -> A vs C is the NULL comparison
Genes 100..119 are low coverage (median ~6 molecules per replicate), all null.
Per replicate PSI ~ Beta(kappa*p, kappa*(1-p)), kappa=60 (biological over-dispersion); molecules ~ Poisson(coverage).
Inclusion molecule -> 2 junction reads (E1-E2, E2-E3, split binomially); skipping molecule -> 1 junction read (E1-E3).
Outputs (run/data/sim/): BAMs, chrP.fa, sim.gtf, truth.tsv, tpm_all.tsv (for SUPPA2, TPM built from the same molecules),
b_A.txt b_B.txt b_C.txt (rMATS lists, WSL paths), counts.tsv.
Usage: python make_sim.py <outdir> <wsl_prefix_for_lists>
"""
import os, sys, random
import numpy as np
import pysam

out = sys.argv[1]
wsl_prefix = sys.argv[2] if len(sys.argv) > 2 else out
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(20260920)
random.seed(20260920)
L = 50
NG = 120
SPACING = 3000
GLEN = NG * SPACING + 12000
seq = ''.join(random.choice('ACGT') for _ in range(GLEN))
with open(f'{out}/chrP.fa', 'w') as f:
    f.write('>chrP\n')
    for i in range(0, GLEN, 60):
        f.write(seq[i:i + 60] + '\n')

gtf, truth = [], []
pA, delta, cov = {}, {}, {}
for g in range(NG):
    base = g * SPACING
    gid = f'G{g:03d}'
    if g < 12:
        d = 0.5 if g % 2 == 0 else -0.5
        cls = 'DS_strong'
    elif g < 24:
        d = 0.3 if g % 2 == 0 else -0.3
        cls = 'DS_strong'
    elif g < 30:
        d = 0.15 if g % 2 == 0 else -0.15
        cls = 'DS_weak'
    else:
        d = 0.0
        cls = 'nochange_lowcov' if g >= 100 else 'nochange'   # NB: not 'null': pandas read_csv parses the string null as NaN
    if cls.startswith('DS'):
        p = float(rng.uniform(0.3, 0.7))
    else:
        p = float(rng.uniform(0.1, 0.9))
    pA[gid] = p
    delta[gid] = d
    cov[gid] = 6.0 if g >= 100 else float(np.exp(rng.normal(np.log(40), 0.5)))
    truth.append((gid, base + 500, base + 600, cls, p, d))
    for tid, exons in ((f'{gid}_inc', [(101, 200), (501, 600), (901, 1000)]), (f'{gid}_skip', [(101, 200), (901, 1000)])):
        es = [(base + s, base + e) for s, e in exons]
        gtf.append(f'chrP\tsim\ttranscript\t{es[0][0]}\t{es[-1][1]}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}";')
        for n, (s, e) in enumerate(es, 1):
            gtf.append(f'chrP\tsim\texon\t{s}\t{e}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}"; exon_number "{n}";')
open(f'{out}/sim.gtf', 'w').write('\n'.join(gtf) + '\n')

# Decoy genes (all null, PSI 0.5, 30 reads per junction in every sample) so Shiba 0.8.2 has >=1 event of every type
# (it crashes with KeyError when a type is empty). Written only into sim_shiba.gtf; rMATS/leafcutter/SUPPA2 use sim.gtf.
DEC = {
    'DRI':   {'a': [(101, 200), (401, 500)], 'b': [(101, 500)]},
    'DA5':   {'a': [(101, 200), (401, 500)], 'b': [(101, 230), (401, 500)]},
    'DA3':   {'a': [(101, 200), (401, 500)], 'b': [(101, 200), (371, 500)]},
    'DMX':   {'a': [(101, 200), (301, 350), (501, 600)], 'b': [(101, 200), (401, 450), (501, 600)]},
    'DAFE':  {'a': [(101, 200), (401, 500), (701, 800)], 'b': [(281, 320), (401, 500), (701, 800)]},
    'DMSE':  {'a': [(101, 200), (901, 1000)], 'b': [(101, 200), (301, 350), (501, 550), (701, 750), (901, 1000)]},
    'DALE':  {'a': [(101, 200), (401, 500), (701, 800)], 'b': [(101, 200), (401, 500), (881, 920)]},
}
DBASE = NG * SPACING + 200
decoy_junctions, decoy_body = [], []
gtf2 = list(gtf)
for k, (gid, ts) in enumerate(DEC.items()):
    off = DBASE + k * 1500
    for tn, exons in ts.items():
        es = [(off + a, off + b) for a, b in exons]
        tid = f'{gid}_{tn}'
        gtf2.append(f'chrP\tsim\ttranscript\t{es[0][0]}\t{es[-1][1]}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}";')
        for n, (a, b) in enumerate(es, 1):
            gtf2.append(f'chrP\tsim\texon\t{a}\t{b}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}"; exon_number "{n}";')
        for (a1, b1), (a2, b2) in zip(es[:-1], es[1:]):
            decoy_junctions.append((b1, a2))
        if len(es) == 1:
            decoy_body.append((es[0][0] + 80, es[0][0] + 80 + 40))
open(f'{out}/sim_shiba.gtf', 'w').write('\n'.join(gtf2) + '\n')
decoy_junctions = sorted(set(decoy_junctions))
with open(f'{out}/truth.tsv', 'w') as f:
    f.write('gene\texonStart_0base\texonEnd\tclass\tpsi_A\tdelta_B_minus_A\n')
    for t in truth:
        f.write('\t'.join(str(x) for x in t) + '\n')

header = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrP', 'LN': GLEN}]}


def jread(name, left_end, right_start):
    a = pysam.AlignedSegment()
    a.query_name = name
    a.query_sequence = seq[left_end - 25:left_end] + seq[right_start - 1:right_start - 1 + 25]
    a.flag = 0
    a.reference_id = 0
    a.reference_start = left_end - 25
    a.mapping_quality = 255
    a.cigar = [(0, 25), (3, right_start - left_end - 1), (0, 25)]
    a.query_qualities = pysam.qualitystring_to_array('I' * L)
    a.set_tag('NH', 1)
    a.set_tag('XS', '+', value_type='A')
    return a


groups = {'A': 0.0, 'B': 1.0, 'C': 0.0}   # B applies delta
kappa = 60.0
counts_rows = []
tpm = {}
for grp, use_delta in groups.items():
    for rep in (1, 2, 3):
        sample = f'{grp}{rep}'
        reads = []
        tpm[sample] = {}
        for g in range(NG):
            gid = f'G{g:03d}'
            base = g * SPACING
            p = min(0.95, max(0.05, pA[gid] + use_delta * delta[gid]))
            pr = float(rng.beta(kappa * p, kappa * (1 - p)))
            M = int(rng.poisson(cov[gid] * float(rng.uniform(0.8, 1.25))))
            n_inc = int(rng.binomial(M, pr))
            n_skip = M - n_inc
            n12 = int(rng.binomial(2 * n_inc, 0.5))
            n23 = 2 * n_inc - n12
            for i in range(n12):
                reads.append(jread(f'{sample}_{gid}_a{i}', base + 200, base + 501))
            for i in range(n23):
                reads.append(jread(f'{sample}_{gid}_b{i}', base + 600, base + 901))
            for i in range(n_skip):
                reads.append(jread(f'{sample}_{gid}_s{i}', base + 200, base + 901))
            counts_rows.append((sample, gid, M, n_inc, n_skip, round(pr, 4)))
            tpm[sample][f'{gid}_inc'] = n_inc
            tpm[sample][f'{gid}_skip'] = n_skip
        for j, (le, rs) in enumerate(decoy_junctions):
            for i in range(30):
                reads.append(jread(f'{sample}_dec{j}_{i}', le, rs))
        for j, (bs, be) in enumerate(decoy_body):
            for i in range(30):
                a = pysam.AlignedSegment()
                a.query_name = f'{sample}_decbody{j}_{i}'
                a.query_sequence = seq[bs - 1:bs - 1 + L]
                a.flag = 0; a.reference_id = 0; a.reference_start = bs - 1; a.mapping_quality = 255
                a.cigar = [(0, L)]; a.query_qualities = pysam.qualitystring_to_array('I' * L); a.set_tag('NH', 1)
                reads.append(a)
        reads.sort(key=lambda r: r.reference_start)
        tmp = f'{out}/{sample}.unsorted.bam'
        with pysam.AlignmentFile(tmp, 'wb', header=header) as bam:
            for r in reads:
                bam.write(r)
        pysam.sort('-o', f'{out}/{sample}.bam', tmp)
        pysam.index(f'{out}/{sample}.bam')
        os.remove(tmp)
        print(sample, len(reads), 'junction reads')

with open(f'{out}/counts.tsv', 'w') as f:
    f.write('sample\tgene\tM\tn_inc\tn_skip\tpsi_rep\n')
    for r in counts_rows:
        f.write('\t'.join(str(x) for x in r) + '\n')

# TPM for SUPPA2: molecule counts scaled to 1e6 per sample plus 0.5 pseudo-count? no pseudo-count: keep zeros (SUPPA2 gives NaN PSI when both 0)
samples = list(tpm)
with open(f'{out}/tpm_all.tsv', 'w') as f:
    f.write('\t'.join(samples) + '\n')
    for g in range(NG):
        for suffix in ('inc', 'skip'):
            tid = f'G{g:03d}_{suffix}'
            row = []
            for s in samples:
                tot = sum(tpm[s].values())
                row.append(f'{tpm[s][tid] / tot * 1e6:.3f}')
            f.write(tid + '\t' + '\t'.join(row) + '\n')

for grp in groups:
    with open(f'{out}/b_{grp}.txt', 'w') as f:
        f.write(','.join(f'{wsl_prefix}/{grp}{r}.bam' for r in (1, 2, 3)) + '\n')
print('done')

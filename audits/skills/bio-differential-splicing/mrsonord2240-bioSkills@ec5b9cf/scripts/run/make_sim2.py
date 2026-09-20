#!/usr/bin/env python3
"""SYNTHETIC simulation #2 written by the re-auditor (independent of the fixer's make_sim5 and of the first audit's make_sim.py).

100 genes on contig chrQ (+ strand), 3000 nt apart, three event types:
  genes  0..39  SE   (E1 101-200, E2 501-600, E3 901-1000; PSI = inclusion of E2)
  genes 60..69  A5SS (E1 101-230 long / 101-200 short, E2 501-600; PSI = long-donor usage)
  genes 70..79  A3SS (E1 101-200, E2 471-600 long / 501-600 short; PSI = long-acceptor usage)
  genes 40..59, 80..99 SE null fillers
Truth classes (planted dPSI = PSI(cond1) - PSI(cond0), additive in probability):
  DS_strong   |d| 0.35-0.50 : SE 0..15, A5SS 60..65, A3SS 70..75          (28 genes)
  DS_moderate |d| 0.20      : SE 16..23                                     (8)
  DS_weak     |d| 0.10      : SE 24..29                                     (6)
  null                      : SE 30..59, A5SS 66..69, A3SS 76..79           (38)
  null_overdisp             : SE 80..89, kappa 15 instead of 40             (10)
  null_lowcov               : SE 90..99, ~6 molecules per replicate         (10)
Per replicate: PSI ~ Beta(kappa p, kappa (1-p)) with p = expit(logit(clip(p0 + cond*d)) + batch*bshift[g] + patient_offset[g]);
molecules ~ Poisson(cov * U(0.8, 1.25)), cov = lognormal(median 40).
Read model: single-end 50 nt junction reads (25+25), XS set. SE inclusion molecule -> 2 reads, skipping -> 1 read; A5SS/A3SS: 1 read.
TPM (for SUPPA2) is built from the same molecule counts.

Modes (each writes a self-contained dir under <outroot>):
  main   : A1..A6 (cond 0), B1..B6 (cond 1), C1..C6 (cond 0, independent replicate set of A -> A vs C is a NULL comparison)
  batch  : S1..S8, cond = 0 for S1-4 / 1 for S5-8, batch = [1,1,1,2, 1,2,2,2] (imbalanced); 20 extra null SE genes (40..59) carry a
           batch shift of +-2.0 on the logit scale in batch 2 (these are the batch-driven false-positive candidates); RIN random, no effect
  paired : 5 patients, N1..N5 (normal, cond 0) and T1..T5 (tumor, cond 1); each patient has a private logit offset ~ N(0, 0.8) per gene
Usage: make_sim2.py <mode> <outdir> <wsl_prefix_for_lists> <seed>
"""
import os, sys, random
import numpy as np
import pysam

mode, out = sys.argv[1], sys.argv[2]
wsl_prefix = sys.argv[3]
seed = int(sys.argv[4])
os.makedirs(out, exist_ok=True)
rng = np.random.default_rng(seed)
random.seed(seed)
L = 50
NG = 100
SPACING = 3000
GLEN = NG * SPACING + 14000
seq = ''.join(random.choice('ACGT') for _ in range(GLEN))
with open(f'{out}/chrQ.fa', 'w') as f:
    f.write('>chrQ\n')
    for i in range(0, GLEN, 60):
        f.write(seq[i:i + 60] + '\n')

expit = lambda x: 1 / (1 + np.exp(-x))
logit = lambda p: np.log(p / (1 - p))

gtype, gclass, p0, delta, cov, kappa, bshift = {}, {}, {}, {}, {}, {}, {}
truth, gtf = [], []
for g in range(NG):
    gid = f'G{g:03d}'
    if 60 <= g < 70:
        t = 'A5SS'
    elif 70 <= g < 80:
        t = 'A3SS'
    else:
        t = 'SE'
    d, cls, kap, cv = 0.0, 'null', 40.0, float(np.exp(rng.normal(np.log(40), 0.5)))
    if g < 16 or 60 <= g < 66 or 70 <= g < 76:
        cls = 'DS_strong'
        d = float(rng.choice([-1, 1]) * rng.uniform(0.35, 0.50))
    elif 16 <= g < 24:
        cls, d = 'DS_moderate', (0.20 if g % 2 == 0 else -0.20)
    elif 24 <= g < 30:
        cls, d = 'DS_weak', (0.10 if g % 2 == 0 else -0.10)
    elif 80 <= g < 90:
        cls, kap = 'null_overdisp', 15.0
    elif g >= 90:
        cls, cv = 'null_lowcov', 6.0
    gtype[gid], gclass[gid], delta[gid], cov[gid], kappa[gid] = t, cls, d, cv, kap
    p0[gid] = float(rng.uniform(0.35, 0.65)) if cls.startswith('DS') else float(rng.uniform(0.15, 0.85))
    bshift[gid] = 0.0
    if mode == 'batch' and 40 <= g < 60:
        bshift[gid] = float(rng.choice([-1, 1]) * 2.0)
        cls = 'null_batchshift'
        gclass[gid] = cls
    base = g * SPACING
    if t == 'SE':
        tx = {'inc': [(101, 200), (501, 600), (901, 1000)], 'skip': [(101, 200), (901, 1000)]}
    elif t == 'A5SS':
        tx = {'inc': [(101, 230), (501, 600)], 'skip': [(101, 200), (501, 600)]}
    else:
        tx = {'inc': [(101, 200), (471, 600)], 'skip': [(101, 200), (501, 600)]}
    for suffix, exons in tx.items():
        tid = f'{gid}_{suffix}'
        es = [(base + a, base + b) for a, b in exons]
        gtf.append(f'chrQ\tsim\ttranscript\t{es[0][0]}\t{es[-1][1]}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}";')
        for n, (a, b) in enumerate(es, 1):
            gtf.append(f'chrQ\tsim\texon\t{a}\t{b}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}"; exon_number "{n}";')
    truth.append((gid, t, cls, round(p0[gid], 4), round(d, 4), round(bshift[gid], 3), round(cv, 1), kap))
open(f'{out}/sim.gtf', 'w').write('\n'.join(gtf) + '\n')
with open(f'{out}/truth.tsv', 'w') as f:
    f.write('gene\tetype\tclass\tpsi0\tdelta_cond1_minus_cond0\tbatch_logit_shift\tcov\tkappa\n')
    for r in truth:
        f.write('\t'.join(str(x) for x in r) + '\n')

# decoys so Shiba 0.8.2 (KeyError on empty event types) has >=1 event of every type; only in sim_shiba.gtf
DEC = {
    'DRI':  {'a': [(101, 200), (401, 500)], 'b': [(101, 500)]},
    'DMX':  {'a': [(101, 200), (301, 350), (501, 600)], 'b': [(101, 200), (401, 450), (501, 600)]},
    'DAFE': {'a': [(101, 200), (401, 500), (701, 800)], 'b': [(281, 320), (401, 500), (701, 800)]},
    'DMSE': {'a': [(101, 200), (901, 1000)], 'b': [(101, 200), (301, 350), (501, 550), (701, 750), (901, 1000)]},
    'DALE': {'a': [(101, 200), (401, 500), (701, 800)], 'b': [(101, 200), (401, 500), (881, 920)]},
}
DBASE = NG * SPACING + 200
decoy_junctions, decoy_body, gtf2 = [], [], list(gtf)
for k, (gid, ts) in enumerate(DEC.items()):
    off = DBASE + k * 1500
    for tn, exons in ts.items():
        es = [(off + a, off + b) for a, b in exons]
        tid = f'{gid}_{tn}'
        gtf2.append(f'chrQ\tsim\ttranscript\t{es[0][0]}\t{es[-1][1]}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}";')
        for n, (a, b) in enumerate(es, 1):
            gtf2.append(f'chrQ\tsim\texon\t{a}\t{b}\t.\t+\t.\tgene_id "{gid}"; transcript_id "{tid}"; gene_name "{gid}"; exon_number "{n}";')
        for (a1, b1), (a2, b2) in zip(es[:-1], es[1:]):
            decoy_junctions.append((b1, a2))
        if len(es) == 1:
            decoy_body.append((es[0][0] + 80, es[0][0] + 120))
open(f'{out}/sim_shiba.gtf', 'w').write('\n'.join(gtf2) + '\n')
decoy_junctions = sorted(set(decoy_junctions))

header = {'HD': {'VN': '1.6', 'SO': 'coordinate'}, 'SQ': [{'SN': 'chrQ', 'LN': GLEN}]}


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


# ---- sample sheet ----
samples = []   # (name, group_label, cond, batch, patient)
if mode == 'main':
    for grp, cond in (('A', 0), ('B', 1), ('C', 0)):
        for r in range(1, 7):
            samples.append((f'{grp}{r}', grp, cond, 1, 0))
elif mode == 'batch':
    bt = [1, 1, 1, 2, 1, 2, 2, 2]
    for i in range(8):
        samples.append((f'S{i + 1}', 'G0' if i < 4 else 'G1', 0 if i < 4 else 1, bt[i], 0))
elif mode == 'paired':
    for r in range(1, 6):
        samples.append((f'N{r}', 'N', 0, 1, r))
    for r in range(1, 6):
        samples.append((f'T{r}', 'T', 1, 1, r))
else:
    raise SystemExit('mode?')
patient_off = {}
if mode == 'paired':
    for pt in range(1, 6):
        for g in range(NG):
            patient_off[(pt, f'G{g:03d}')] = float(rng.normal(0, 0.8))
rin = {s[0]: round(float(rng.normal(8, 0.5)), 2) for s in samples}

counts_rows, tpm = [], {}
for sample, grp, cond, batch, pt in samples:
    reads, tpm[sample] = [], {}
    for g in range(NG):
        gid = f'G{g:03d}'
        base = g * SPACING
        pbase = min(0.95, max(0.05, p0[gid] + cond * delta[gid]))
        lg = logit(pbase) + (batch - 1) * bshift[gid] + patient_off.get((pt, gid), 0.0)
        p = float(np.clip(expit(lg), 0.02, 0.98))
        pr = float(rng.beta(kappa[gid] * p, kappa[gid] * (1 - p)))
        M = int(rng.poisson(cov[gid] * float(rng.uniform(0.8, 1.25))))
        n_inc = int(rng.binomial(M, pr))
        n_skip = M - n_inc
        t = gtype[gid]
        if t == 'SE':
            n12 = int(rng.binomial(2 * n_inc, 0.5)); n23 = 2 * n_inc - n12
            for i in range(n12): reads.append(jread(f'{sample}_{gid}_a{i}', base + 200, base + 501))
            for i in range(n23): reads.append(jread(f'{sample}_{gid}_b{i}', base + 600, base + 901))
            for i in range(n_skip): reads.append(jread(f'{sample}_{gid}_s{i}', base + 200, base + 901))
        elif t == 'A5SS':
            for i in range(n_inc): reads.append(jread(f'{sample}_{gid}_l{i}', base + 230, base + 501))
            for i in range(n_skip): reads.append(jread(f'{sample}_{gid}_s{i}', base + 200, base + 501))
        else:
            for i in range(n_inc): reads.append(jread(f'{sample}_{gid}_l{i}', base + 200, base + 471))
            for i in range(n_skip): reads.append(jread(f'{sample}_{gid}_s{i}', base + 200, base + 501))
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
    print(sample, len(reads), 'reads')

with open(f'{out}/counts.tsv', 'w') as f:
    f.write('sample\tgene\tM\tn_inc\tn_skip\tpsi_rep\n')
    for r in counts_rows:
        f.write('\t'.join(str(x) for x in r) + '\n')
with open(f'{out}/meta.tsv', 'w') as f:
    f.write('sample\tgroup\tcond\tbatch\tpatient\tRIN\n')
    for s, grp, cond, batch, pt in samples:
        f.write(f'{s}\t{grp}\t{cond}\t{batch}\t{pt}\t{rin[s]}\n')
names = [s[0] for s in samples]
with open(f'{out}/tpm_all.tsv', 'w') as f:
    f.write('\t'.join(names) + '\n')
    for g in range(NG):
        for suffix in ('inc', 'skip'):
            tid = f'G{g:03d}_{suffix}'
            f.write(tid + '\t' + '\t'.join(f'{tpm[s][tid] / sum(tpm[s].values()) * 1e6:.3f}' for s in names) + '\n')
print('done', mode, len(samples), 'samples')

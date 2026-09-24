"""SYNTHETIC replicate-structured single-cell junction data for the pseudobulk section (auditor's own design).
   asenv as-sc python 40_pb_gen.py <outdir> <seed>
 2 cell types (T1, T2) x 7 donors x 6 cells per (donor, type) = 84 cells; 150 SE events written as leafcutter clusters (3 junctions each:
 chr:start:end:clu_<event>_+); 20 'big' (PSI 0.75 vs 0.25), 20 'mid' (0.60 vs 0.40), 110 'null'. Donor random effect: logit(PSI) shift ~ N(0, 0.5), shared by both
 cell types of a donor and event. 20% low-coverage cells (mean 2 molecules/event vs 12). Each junction read seen with prob 0.6.
Outputs: junction_counts.tsv (junctions x cells), cell_metadata.tsv (INDEXED BY CELL ID; columns cell_type, sample), truth.tsv"""
import sys, os, numpy as np, pandas as pd
out, seed = sys.argv[1], int(sys.argv[2]); os.makedirs(out, exist_ok=True); rng = np.random.default_rng(seed)
NE, ND, NPER = 150, 7, 6
cls = np.array(['big'] * 20 + ['mid'] * 20 + ['null'] * 110)
p1 = np.where(cls == 'big', .75, np.where(cls == 'mid', .60, np.nan)); p2 = np.where(cls == 'big', .25, np.where(cls == 'mid', .40, np.nan))
base = rng.uniform(.3, .7, NE); p1 = np.where(cls == 'null', base, p1); p2 = np.where(cls == 'null', base, p2)
flip = rng.random(NE) < .5; p1, p2 = np.where(flip, p2, p1), np.where(flip, p1, p2)     # random direction
donor_eff = rng.normal(0, .5, (ND, NE))
lg = lambda p: np.log(p / (1 - p)); ex = lambda x: 1 / (1 + np.exp(-x))
start = 100000 + np.arange(NE) * 4000
rows = []
for i in range(NE):
    e1 = start[i] + 150; s2 = e1 + 600; e2 = s2 + 90; s3 = e2 + 600
    ch = f'chr{i % 5 + 1}'
    rows += [f'{ch}:{e1 + 1}:{s2 - 1}:clu_{i + 1}_+', f'{ch}:{e2 + 1}:{s3 - 1}:clu_{i + 1}_+', f'{ch}:{e1 + 1}:{s3 - 1}:clu_{i + 1}_+']
cells, meta = [], []
M = []
for d in range(ND):
    for t, pt in [('T1', p1), ('T2', p2)]:
        for k in range(NPER):
            cid = f'{t}_d{d + 1}_c{k + 1}'; low = rng.random() < .2; mu = 2 if low else 12
            col = np.zeros(3 * NE, dtype=int)
            for i in range(NE):
                pc = float(np.clip(rng.beta(max(ex(lg(pt[i]) + donor_eff[d, i]) * 15, .5), max((1 - ex(lg(pt[i]) + donor_eff[d, i])) * 15, .5)), .001, .999))
                n = rng.negative_binomial(2, 2 / (2 + mu)); ninc = rng.binomial(n, pc); nsk = n - ninc
                col[3 * i] = rng.binomial(ninc, .6); col[3 * i + 1] = rng.binomial(ninc, .6); col[3 * i + 2] = rng.binomial(nsk, .6)
            M.append(col); cells.append(cid); meta.append((cid, t, f'd{d + 1}'))
J = pd.DataFrame(np.array(M).T, index=rows, columns=cells)
J.to_csv(out + '/junction_counts.tsv', sep='\t')
pd.DataFrame(meta, columns=['cell', 'cell_type', 'sample']).set_index('cell').to_csv(out + '/cell_metadata.tsv', sep='\t')
pd.DataFrame({'cluster': [f'clu_{i + 1}_+' for i in range(NE)], 'cls': cls, 'psi_T1': p1, 'psi_T2': p2}).to_csv(out + '/truth.tsv', sep='\t', index=False)
print('junction matrix', J.shape, 'total reads', int(J.values.sum()), 'cells', len(cells))

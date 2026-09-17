"""Input 1 -- Canonical (regression, re-run against the FIXED skill). Full QC audit on real
HAP1 TKOv3 counts (T0 plasmid vs three T18 endpoint replicates) using qc_functions.py
(transcribed verbatim from the fixed SKILL.md). Cross-checked against the rewritten, now
stage-aware examples/screen_qc.py in input1b_shipped_example.py."""
import sys, glob
import pandas as pd, numpy as np
sys.path.insert(0, '.')
import qc_functions as qc

DATA = r'F:\OpenScience\audits\bio-crispr-screens-screen-qc\data\hap1_tkov3_canonical.txt'
BAGEL = r'F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\bagel'

df = pd.read_csv(DATA, sep='\t')
counts = df[['HAP1_T0', 'HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']].copy()
genes = df['GENE']

print('=== Library representation ===')
print(qc.library_representation(counts).round(3))

thr = qc.stage_specific_thresholds()
print('\n=== Gini per sample vs stage thresholds ===')
stage_of = {'HAP1_T0': 'plasmid', 'HAP1_T18A': 'endpoint', 'HAP1_T18B': 'endpoint', 'HAP1_T18C': 'endpoint'}
for s in counts.columns:
    g = qc.gini(counts[s].values)
    t = thr[stage_of[s]]['gini_max']
    print(f'{s} (stage={stage_of[s]}): Gini={g:.4f} threshold<{t} -> {"PASS" if g < t else "FAIL"}')

print('\n=== Replicate concordance (endpoint only) ===')
cmap = {'endpoint': ['HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']}
rc = qc.replicate_concordance(counts, cmap)
print(rc.round(4))

print('\n=== Depth audit ===')
print(qc.depth_audit(counts).round(2))

# Gene-level LFC: mean endpoint vs T0, log2, pseudocount 0.5, normalized to total reads
norm = counts.div(counts.sum()) * 1e6
lfc_per_guide = np.log2((norm[['HAP1_T18A', 'HAP1_T18B', 'HAP1_T18C']].mean(axis=1) + 0.5) /
                         (norm['HAP1_T0'] + 0.5))
gene_lfc = pd.DataFrame({'gene': genes, 'lfc': lfc_per_guide}).groupby('gene', as_index=False)['lfc'].mean()

ceg = set(pd.read_csv(BAGEL + r'\CEGv2.txt', sep='\t')['GENE'])
neg = set(pd.read_csv(BAGEL + r'\NEGv1.txt', sep='\t')['GENE'])
res = qc.essentialome_recovery(gene_lfc, ceg, neg)
print('\n=== CEGv2 / NEGv1 essentialome recovery ===')
print({k: (round(v, 4) if isinstance(v, float) else int(v)) for k, v in res.items()})
print('-> PASS (screen has essentiality signal)' if res['pr_auc'] > 0.7 else '-> FAIL')

# Direction check: are known essentials actually depleted (negative LFC)?
ess_lfc = gene_lfc[gene_lfc['gene'].isin(ceg)]['lfc']
noness_lfc = gene_lfc[gene_lfc['gene'].isin(neg)]['lfc']
print(f'\nmean LFC essentials={ess_lfc.mean():.3f}  mean LFC non-essentials={noness_lfc.mean():.3f}')
print('direction correct (essentials more depleted):', ess_lfc.mean() < noness_lfc.mean())

# Re-audit 2026-09-15, peptide-identification Input 8 (NEW, PUBLIC data). PXD070049 (CC0, Orbitrap Astral DDA, 250 pg,
# human/yeast/E. coli), one DDA run converted with msconvert and searched with Sage 0.14.6 (default rev_ decoys, concatenated
# competition). The SKILL.md "FDR from a Results Table" snippet VERBATIM on results.sage.tsv, mapping scannr -> scan,
# sage_discriminant_score -> score, proteins -> protein as the snippet comment directs. Reference: Sage's own spectrum_q.
import numpy as np, pandas as pd
SAGE = 'sage/out/results.sage.tsv'

def skill_snippet(psms):
    psms = psms.copy()
    psms['is_decoy'] = psms['protein'].str.startswith(('DECOY_', 'REV_', 'XXX_'))
    psms = psms.sort_values('score', ascending=False).drop_duplicates('scan').reset_index(drop=True)
    targets = (~psms['is_decoy']).cumsum()
    decoys = psms['is_decoy'].cumsum()
    psms['fdr'] = (decoys + 1) / targets.clip(lower=1)
    psms['qvalue'] = psms['fdr'][::-1].cummin()[::-1]
    kept = psms[(psms['qvalue'] <= 0.01) & (~psms['is_decoy'])]
    return psms, kept

raw = pd.read_csv(SAGE, sep='\t')
print('Sage rows', len(raw), '| columns include:', [c for c in ['scannr', 'proteins', 'label', 'sage_discriminant_score', 'spectrum_q', 'hyperscore', 'rank'] if c in raw.columns])
print('Sage label counts (1 target, -1 decoy):', raw['label'].value_counts().to_dict(), '| rows with rev_ proteins:', int(raw.proteins.str.startswith('rev_').sum()))
print('Sage own: target PSMs at spectrum_q <= 0.01:', int(((raw.label == 1) & (raw.spectrum_q <= 0.01)).sum()))
t = raw.rename(columns={'scannr': 'scan', 'sage_discriminant_score': 'score', 'proteins': 'protein'})
allp, kept = skill_snippet(t)
print(f"SKILL snippet as written: decoys detected {int(allp.is_decoy.sum())} | kept at q<=0.01: {len(kept)} | of which rev_ decoys reported as targets: {int(kept.protein.str.startswith('rev_').sum())}")
t2 = t.copy(); t2['protein'] = t2['protein'].str.replace('rev_', 'REV_', regex=False)
allp2, kept2 = skill_snippet(t2)
sage_set = set(raw.loc[(raw.label == 1) & (raw.spectrum_q <= 0.01), 'scannr'])
print(f"snippet with prefix recognised: decoys {int(allp2.is_decoy.sum())} | kept {len(kept2)} | overlap with Sage spectrum_q<=0.01 scans: {len(set(kept2.scan) & sage_set)}")
# species check: decoy-estimated FDR vs the conservative estimate from the (D+1)/T formula
sp = kept2.protein.str.extract(r'_(HUMAN|YEAST|ECOLI)')[0].value_counts(dropna=False).to_dict()
print('species of kept PSMs (first protein):', sp)

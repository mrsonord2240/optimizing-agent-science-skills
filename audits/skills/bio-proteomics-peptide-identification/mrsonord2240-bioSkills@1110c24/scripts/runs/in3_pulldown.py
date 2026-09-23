# Input 3 - tiny single-bait pulldown; the Skill's table snippet on 33 PSMs (no decoys) and on the same list
# where the top-ranked PSM is a decoy.
import warnings
import pandas as pd

D = 'F:/OpenScience/audits/bio-proteomics-peptide-identification/data/'


def skill_snippet(psms):   # SKILL.md lines 129-138 verbatim
    psms['is_decoy'] = psms['protein'].str.startswith(('DECOY_', 'REV_', 'XXX_'))
    psms = psms.sort_values('score', ascending=False).reset_index(drop=True)
    targets = (~psms['is_decoy']).cumsum()
    decoys = psms['is_decoy'].cumsum()
    psms['fdr'] = decoys / targets
    psms['qvalue'] = psms['fdr'][::-1].cummin()[::-1]
    kept = psms[(psms['qvalue'] <= 0.01) & (~psms['is_decoy'])]
    return psms, kept


for name in ['pulldown_nodecoy.tsv', 'pulldown_topdecoy.tsv']:
    df = pd.read_csv(D + name, sep='\t')
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        allp, kept = skill_snippet(df)
    print(f'== {name}: rows={len(df)} decoys={int(allp["is_decoy"].sum())} false targets (truth)={int((~allp["is_decoy"] & ~allp["is_correct"]).sum())}')
    print('   warnings raised:', [str(x.message) for x in w] or 'none')
    print('   top 3 rows:\n' + allp[['score', 'is_decoy', 'fdr', 'qvalue']].head(3).to_string(index=False))
    print(f'   kept at q<=0.01: {len(kept)}  (false among kept: {int((~kept["is_correct"]).sum())})  min/max q: '
          f'{allp["qvalue"].min():.4f}/{allp["qvalue"].max():.4f}')
    # AUDIT: the +1-corrected estimate (D+1)/T gives the smallest attainable q for this list size
    t = (~allp['is_decoy']).sum()
    print(f'   smallest q attainable with (D+1)/T at T={t}: {1 / t:.3f}')

"""
Audit Input 5 (Stress) — bio-pose-validation
Prompt: "I docked one ligand into 3PTB with Vina and got 8 pose modes with
different scores. Batch-validate all of them with PoseBusters, filter to
PB-valid, and give me the top-ranked valid pose per source using the Skill's
pose_qc_pipeline pattern (also fold in the deliberately bad clash pose to
confirm it's correctly excluded from the ranking)."
Runs the Skill's own `pose_qc_pipeline` function (SKILL.md "Integration into
VS Pipeline") unmodified, extended to also read each mode's Vina score.
"""
from posebusters import PoseBusters
import pandas as pd
import re

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 250)


def pose_qc_pipeline(docked_sdfs, receptor_pdb):
    bust = PoseBusters(config='dock')
    all_results = []
    for sdf in docked_sdfs:
        r = bust.bust(mol_pred=sdf, mol_cond=receptor_pdb)
        check_cols = [
            col for col in r.select_dtypes(include='bool').columns
            if not col.lower().startswith('rmsd')
        ]
        r['pb_valid'] = r[check_cols].all(axis=1)
        r['source'] = sdf
        all_results.append(r)
    df = pd.concat(all_results)

    df['rank'] = df.groupby('source')['pb_valid'].cumsum()
    valid_top = df[df['pb_valid']].groupby('source').head(1)
    return df, valid_top


def vina_score(sdf_path):
    with open(sdf_path) as f:
        content = f.read()
    m = re.search(r'vina_score_kcal_mol>.*\n(-?[\d.]+)', content)
    return float(m.group(1)) if m else None


sdfs = [f'../data/mode{i}_fixed.sdf' for i in range(1, 9)] + ['../data/clash_pose.sdf']

all_df, valid_top = pose_qc_pipeline(sdfs, '../data/receptor.pdb')

all_df['vina_score'] = all_df['source'].apply(lambda s: vina_score(s) if 'mode' in s else None)
summary = all_df[['source', 'pb_valid', 'vina_score']].copy()
print("Per-pose results:")
print(summary.to_string(index=False))

print()
print("Included in PB-valid ranked shortlist:", list(valid_top['source']))
best_valid = summary[summary['pb_valid']].sort_values('vina_score').iloc[0]
print(f"Best-scoring PB-valid pose: {best_valid['source']} (Vina {best_valid['vina_score']} kcal/mol)")
print("Clash pose excluded from shortlist:", 'clash_pose.sdf' not in list(valid_top['source']))

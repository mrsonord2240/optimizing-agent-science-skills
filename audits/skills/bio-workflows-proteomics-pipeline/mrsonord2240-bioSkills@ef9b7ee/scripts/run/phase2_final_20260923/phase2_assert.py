"""Phase 2 artifact assertions for the ten dynamic audit inputs."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

root = Path(sys.argv[1])
checks: list[str] = []


def read(path: Path, **kwargs: object) -> pd.DataFrame:
    return pd.read_csv(path, **kwargs)


canonical = read(root / 'in1_canonical' / 'result.csv')
assert len(canonical) == 1323 and canonical.significant.sum() == 62
checks.append('Input 1: 1323 rows and 62 calls')

diann = read(root / 'in2_diann' / 'matrix.csv', index_col=0)
assert diann.shape == (887, 8) and not np.isinf(diann.to_numpy()).any()
checks.append('Input 2: DIA-NN matrix 887x8, finite where quantified')

three = read(root / 'in3_three_condition' / 'result.csv')
high = three[three.contrast == 'High_vs_Ctl']
low = three[three.contrast == 'Low_vs_Ctl']
assert high.significant.sum() == 20 and low.significant.sum() == 0
checks.append('Input 3: High_vs_Ctl 20 calls, Low_vs_Ctl 0')

shuffled = read(root / 'in4_shuffled_annotation' / 'result.csv')
assert shuffled.significant.sum() == 62
checks.append('Input 4: shuffled annotation still gives 62 calls')

tmt = read(root / 'in5_tmt' / 'result.csv', index_col=0)
assert tmt.shape == (24, 10) and (tmt.to_numpy() >= 0).all()
checks.append('Input 5: TMT correction 24x10 with no negatives')

msstats = read(root / 'in6_msstats' / 'result.csv')
assert len(msstats) == 296 and {'Protein', 'log2FC', 'adj.pvalue'}.issubset(msstats.columns)
checks.append('Input 6: MSstats 296 protein comparisons')

silac = read(root / 'in7_silac' / 'result.csv')
assert len(silac) == 453 and (silac['adj.P.Val'] < 0.05).sum() == 49
checks.append('Input 7: SILAC 453 tested and 49 BH calls')

example_dir = root / 'in9_empty_example'
for name in ('proteinGroups.txt', 'proteomics_results.csv', 'proteomics_results_raw_boxplot.pdf', 'proteomics_results_pca.pdf', 'proteomics_results_volcano.pdf', 'proteomics_results_heatmap.pdf'):
    assert (example_dir / name).is_file(), name
checks.append('Input 9: empty-directory example generated all six declared artifacts')

bad = (root / 'in10_missing_norm.log').read_text(encoding='utf-8', errors='replace')
assert 'Norm' in bad and not (root / 'in10_missing_norm' / 'result.csv').exists()
checks.append('Input 10: missing Norm reference channel rejected before output')

(root / 'assertions.txt').write_text('\n'.join(checks) + '\n', encoding='utf-8')
print('\n'.join(checks))

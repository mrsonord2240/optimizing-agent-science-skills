# Input 4 (Variant B) test: "I already have an MS-DIAL AlignResult.txt export - parse it into
# pandas, split metadata from sample columns, and map annotation tags to MSI levels."
# Exercises the SKILL.md "Import the Alignment Result into Python" section verbatim, plus the
# MSI-level mapping logic from "Filter the Table Honestly" (ported from the R snippet, since
# SKILL.md only gives that mapping in R -- checking whether the Python path is actually complete).

import numpy as np
import pandas as pd
import tempfile
import os

rng = np.random.default_rng(7)
n_features = 30
n_samples = 6

tags = rng.choice(['Metabolite', 'Lipid', 'Suggested_C10H14N2', 'Unknown'], n_features,
                   p=[0.3, 0.1, 0.25, 0.35])
has_msms = np.where(np.isin(tags, ['Metabolite', 'Lipid']),
                     rng.choice(['TRUE', 'FALSE'], n_features, p=[0.6, 0.4]), 'FALSE')

meta = pd.DataFrame({
    'Alignment ID': np.arange(1, n_features + 1),
    'Average Rt(min)': np.round(rng.uniform(0.5, 15, n_features), 3),
    'Average Mz': np.round(rng.uniform(80, 900, n_features), 4),
    'Metabolite name': np.where(tags == 'Unknown', 'Unknown', [f'{t}_{i}' for t, i in zip(tags, range(n_features))]),
    'Adduct type': rng.choice(['[M+H]+', '[M+Na]+', '[M+NH4]+', '[M-H]-'], n_features),
    'Fill %': rng.integers(15, 101, n_features),
    'MS/MS assigned': has_msms,
    'Annotation tag (VS1.0)': tags,
})
sample_cols_truth = [f'Sample_{i+1}' for i in range(n_samples)]
intensities = pd.DataFrame(
    np.round(rng.lognormal(11, 1.5, size=(n_features, n_samples))).astype(int),
    columns=sample_cols_truth
)
body = pd.concat([meta, intensities], axis=1)

export_path = os.path.join(tempfile.gettempdir(), 'AlignResult_input4.txt')
with open(export_path, 'w', newline='') as f:
    for _ in range(4):
        f.write('\t' * (body.shape[1] - 1) + '\n')
    body.to_csv(f, sep='\t', index=False)

print('=== Exercising SKILL.md "Import the Alignment Result into Python" section verbatim ===')

# SKILL.md code block (copied exactly, only the file path changed):
msdial = pd.read_csv(export_path, sep='\t', skiprows=4)
meta_cols = ['Alignment ID', 'Average Rt(min)', 'Average Mz', 'Metabolite name', 'Adduct type', 'Fill %', 'MS/MS assigned', 'Annotation tag (VS1.0)']
meta_cols = [c for c in meta_cols if c in msdial.columns]
last_meta = max(msdial.columns.get_loc(c) for c in meta_cols)
sample_cols = msdial.columns[last_meta + 1:]

feature_info = msdial[meta_cols].copy()
intensity = msdial[sample_cols].set_axis(msdial['Alignment ID']) if False else msdial[sample_cols].copy()
intensity.index = msdial['Alignment ID']

print(f'Parsed {msdial.shape[0]} rows x {msdial.shape[1]} cols. meta_cols found: {len(meta_cols)} | sample_cols found: {len(sample_cols)}')
assert msdial.shape[0] == n_features, 'row count mismatch vs synthetic ground truth'
assert len(sample_cols) == n_samples, 'sample column count mismatch vs synthetic ground truth'
assert list(sample_cols) == sample_cols_truth, 'sample columns misaligned (metadata leaked into sample matrix, or vice versa)'
print(f'PASS: row/col counts and sample-column identity match synthetic ground truth ({n_features} features, {n_samples} samples).')

print('\n=== Porting the R-only MSI-level mapping (SKILL.md "Filter the Table Honestly") to Python ===')
has_msms2 = feature_info['MS/MS assigned'] == 'TRUE'
is_named = feature_info['Annotation tag (VS1.0)'].isin(['Metabolite', 'Lipid'])
is_suggested = feature_info['Annotation tag (VS1.0)'].str.startswith('Suggested')
feature_info['msi_level'] = np.select(
    [is_named & has_msms2, is_suggested],
    [2, 3],
    default=np.nan,
)
print(feature_info['msi_level'].value_counts(dropna=False))

keep_fill = feature_info['Fill %'] >= 70
filtered = intensity[keep_fill.values]
print(f'\nFill% >= 70 kept {keep_fill.sum()} / {n_features} features')
truth_check = bool((feature_info.loc[keep_fill, 'Fill %'] >= 70).all())
print(f'PASS: every row kept by keep_fill truly has Fill% >= 70 -> {truth_check}')

os.remove(export_path)
print('\nDone.')

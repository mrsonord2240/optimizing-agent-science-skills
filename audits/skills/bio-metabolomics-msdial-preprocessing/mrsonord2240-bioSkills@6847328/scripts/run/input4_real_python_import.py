# Input 4 (Variant B) regression test -- run SKILL.md's exact documented Python
# import code, the naive R-ported filter (the documented bug), and the
# documented fix, verbatim, against the REAL 2-sample MS-DIAL 5.5.260820 console
# export (../data/AlignResult-real-multisample.mdalign), not a synthetic fixture.

import glob
import csv
import pandas as pd

export_file = "../data/AlignResult-real-multisample.mdalign"

# ---- verbatim from SKILL.md "Import the Alignment Result into Python" ----
with open(export_file, newline='') as f:
    header_row1 = next(csv.reader(f, delimiter='\t'))
class_idx = header_row1.index('Class')

msdial = pd.read_csv(export_file, sep='\t', skiprows=4)
meta_cols = ['Alignment ID', 'Average Rt(min)', 'Average Mz', 'Metabolite name', 'Adduct type', 'Fill %', 'MS/MS assigned', 'Annotation tag (VS1.0)']
meta_cols = [c for c in meta_cols if c in msdial.columns]
sample_cols = msdial.columns[class_idx + 1:]

feature_info = msdial[meta_cols].copy()
intensity = msdial[sample_cols].astype(float).copy()
intensity.index = msdial['Alignment ID']
# ---- end verbatim SKILL.md code ----

print(f"Parsed {msdial.shape[0]} features x {msdial.shape[1]} columns from REAL 2-sample export")
print(f"meta_cols found: {len(meta_cols)} | sample_cols found: {len(sample_cols)} -> {list(sample_cols)}")
assert list(sample_cols) == ['CondA', 'CondB'], "sample columns should be the CSV file_name values"
print("PASS: sample columns detected exactly as CondA, CondB.")
print("PASS: intensity.astype(float) succeeded on real data -- no text columns leaked into the matrix.")

# ---- verbatim from SKILL.md's documented BUGGY idiom (the natural R->Python port) ----
naive_has_msms = feature_info['MS/MS assigned'] == 'True'
# ---- end verbatim ----
print(f"\npandas dtype of 'MS/MS assigned' column: {feature_info['MS/MS assigned'].dtype}")
print(f"Naive (buggy) has_msms True count: {naive_has_msms.sum()} / {len(feature_info)}")

# ---- verbatim from SKILL.md's documented FIXED Python idiom ----
keep_fill = feature_info['Fill %'] >= 0.70
has_msms = feature_info['MS/MS assigned'].astype(str).str.strip().str.lower() == 'true'
# ---- end verbatim ----
print(f"Fixed has_msms True count: {has_msms.sum()} / {len(feature_info)}")
print(f"Fill% >= 0.70 kept: {keep_fill.sum()} / {len(feature_info)}")

# Ground truth checks against the real, independently-known distribution
# (real console output: Fill% in {0.5, 1.0}; MS/MS assigned in {True, False} as text).
real_msms_true_from_R = 6887  # cross-checked against input5_real_multisample_filter.R's R-side run
assert feature_info['Fill %'].max() <= 1.0, "Fill % should be 0-1 scaled"
assert set(feature_info['MS/MS assigned'].astype(str).unique()) <= {'True', 'False'}, \
    "MS/MS assigned should be title-case True/False text in the raw column"

if naive_has_msms.sum() == 0 and has_msms.sum() > 0:
    print("\nCONFIRMED (again, on real data): pandas.read_csv silently casts the real "
          "export's literal True/False text to native bool, so the naive R-ported "
          "idiom (`== 'True'`) evaluates to all-False with zero error or warning. "
          "The documented .astype(str).str.strip().str.lower() fix recovers the "
          "correct count.")
    assert has_msms.sum() == real_msms_true_from_R, \
        f"Fixed Python count ({has_msms.sum()}) should match the R-side ground truth ({real_msms_true_from_R})"
    print(f"PASS: fixed Python has_msms count ({has_msms.sum()}) exactly matches "
          f"the independently-computed R-side count ({real_msms_true_from_R}).")
else:
    print("\nNOTE: naive idiom did not silently fail as expected on this real data "
          f"(naive={naive_has_msms.sum()}, fixed={has_msms.sum()}) -- investigate dtype.")

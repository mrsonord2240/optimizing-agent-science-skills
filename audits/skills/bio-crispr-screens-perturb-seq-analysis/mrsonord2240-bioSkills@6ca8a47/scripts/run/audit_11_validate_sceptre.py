"""Validate fresh shipped SCEPTRE outputs have row content and expected result fields."""
from pathlib import Path
import pandas as pd

root = Path(r"F:\OpenScience\audits\bio-crispr-screens-perturb-seq-analysis\data")
for name, expected_rows in [("sceptre_example.tsv", 1), ("sceptre_file_results.tsv", 3)]:
    df = pd.read_csv(root / name, sep="\t")
    required = {"p_value", "significant"}
    assert required.issubset(df.columns), (name, df.columns.tolist())
    assert len(df) >= expected_rows, (name, len(df))
    tested = df.loc[df["pass_qc"], "p_value"]
    assert tested.notna().all() and tested.between(0, 1).all(), name
    print(f"{name}: rows={len(df)} qc_rows={len(tested)} p_value_na={df['p_value'].isna().sum()} columns={','.join(df.columns)}")

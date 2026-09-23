"""Phase 2 audit input 7: run the PyDESeq2 reference block against a small count matrix."""
import numpy as np
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

rng = np.random.default_rng(20260923)
counts = rng.negative_binomial(n=12, p=12 / (12 + 80), size=(6, 80))
counts[3:, :8] *= 2
count_df = pd.DataFrame(counts, index=[f"s{i}" for i in range(6)], columns=[f"g{i}" for i in range(80)])
metadata = pd.DataFrame({"condition": ["control"] * 3 + ["treated"] * 3}, index=count_df.index)
dds = DeseqDataSet(counts=count_df, metadata=metadata, design="~condition", quiet=True)
dds.deseq2()
stat_res = DeseqStats(dds, contrast=("condition", "treated", "control"), quiet=True)
stat_res.summary()
results_df = stat_res.results_df
assert results_df.shape[0] == 80 and {"log2FoldChange", "pvalue", "padj"}.issubset(results_df.columns)
print(f"PyDESeq2 reference block: PASS; rows={results_df.shape[0]}; non_null_padj={results_df.padj.notna().sum()}")

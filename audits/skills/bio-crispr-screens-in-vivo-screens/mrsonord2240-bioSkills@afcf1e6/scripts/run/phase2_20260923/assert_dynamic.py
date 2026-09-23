"""Assert concrete outcomes from run_dynamic.ps1 for the Phase 2 audit."""
from pathlib import Path
import hashlib
import pandas as pd


OUT = Path(__file__).resolve().parent

# `mageck count`: each sample has six guides with exactly sample+2 reads per guide.
count_table = pd.read_csv(OUT / "count_run.count.txt", sep="\t")
sample_cols = [c for c in count_table.columns if c.startswith("S")]
assert len(count_table) == 6, f"expected six library guides, got {len(count_table)}"
for sample in sample_cols:
    expected = int(sample[1:]) + 2
    assert set(count_table[sample]) == {expected}, f"{sample}: unexpected counts {set(count_table[sample])}"

# RRA succeeded for every animal and the synthetic true hits lead the meta-analysis.
for animal in range(1, 7):
    path = OUT / f"animal_{animal}.gene_summary.txt"
    frame = pd.read_csv(path, sep="\t")
    assert len(frame) == 60, f"animal {animal}: expected 60 genes, got {len(frame)}"
meta = pd.read_csv(OUT / "in_vivo_meta_all.tsv", sep="\t")
top_five = set(meta.sort_values("meta_z", ascending=False).head(5)["id"])
expected_hits = {f"Gene{i:03d}" for i in range(5)}
assert top_five == expected_hits, f"top meta hits {top_five}, expected {expected_hits}"
hits = pd.read_csv(OUT / "in_vivo_meta_hits.tsv", sep="\t")
assert expected_hits.issubset(set(hits["id"])), "compound threshold did not retain every planted hit"

# The RRA primary path should reproduce exactly on an identical rerun.
first = (OUT / "animal_1.gene_summary.txt").read_bytes()
rerun = (OUT / "animal_1_rerun.gene_summary.txt").read_bytes()
assert first == rerun, "mageck test primary path changed across identical rerun"

# MLE must produce readable gene summaries with the advertised effect/Wald columns.
for stem in ("mle_one", "mle_two"):
    frame = pd.read_csv(OUT / f"{stem}.gene_summary.txt", sep="\t")
    assert len(frame) == 60, f"{stem}: expected 60 gene rows"
    assert any("beta" in col.lower() for col in frame.columns), f"{stem}: beta column absent"
    assert any("wald" in col.lower() for col in frame.columns), f"{stem}: Wald column absent"

print(f"mageck_count_exact=6x{len(sample_cols)}")
print(f"rra_gene_summaries=6x60; meta_top5={','.join(sorted(top_five))}; compound_hits={len(hits)}")
print("rra_rerun_sha256=" + hashlib.sha256(first).hexdigest())
print("mle_gene_summaries=2x60 with beta and Wald columns")

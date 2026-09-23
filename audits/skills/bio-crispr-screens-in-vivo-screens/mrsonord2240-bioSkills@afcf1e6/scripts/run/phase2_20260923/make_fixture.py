"""Create deterministic synthetic inputs for the Phase 2 in-vivo CRISPR audit.

Writes a 60-gene count table for MAGeCK MLE/RRA, plus a six-sample FASTQ/library
fixture for the documented `mageck count` command.  This is audit evidence only.
"""
from pathlib import Path

import numpy as np
import pandas as pd


OUT = Path(__file__).resolve().parent
rng = np.random.default_rng(20260923)
n_genes, guides_per_gene, n_animals = 60, 4, 6
genes = [f"Gene{i:03d}" for i in range(n_genes)]
true_hits = set(genes[:5])
rows = [
    {"sgRNA": f"{gene}_sg{guide}", "gene": gene}
    for gene in genes
    for guide in range(guides_per_gene)
]
library = pd.DataFrame(rows)
plasmid = rng.negative_binomial(20, 20 / (20 + 500), len(library))
plasmid = np.clip(plasmid, 20, None)
counts = library.copy()
counts["Plasmid"] = plasmid
for animal in range(1, n_animals + 1):
    keep = rng.random(len(library)) < rng.uniform(0.60, 0.85)
    abundance = plasmid.astype(float).copy()
    hit_mask = library["gene"].isin(true_hits).to_numpy()
    abundance[hit_mask] *= rng.uniform(0.04, 0.14, hit_mask.sum())
    abundance[~keep] *= rng.uniform(0.01, 0.08, (~keep).sum())
    counts[f"Animal{animal}"] = rng.negative_binomial(
        12, 12 / (12 + np.clip(abundance, 1, None))
    )
counts.to_csv(OUT / "in_vivo_counts.txt", sep="\t", index=False)

# Six distinguishable 20-nt guides, each represented by an exact known read count.
seqs = [
    "ACGTACGTACGTACGTACGA", "TGCATGCATGCATGCATGCA", "GATCGATCGATCGATCGATC",
    "CTAGCTAGCTAGCTAGCTAG", "AACCGGTTAACCGGTTAACC", "TTGGCCAATTGGCCAATTGG",
]
pd.DataFrame(
    {
        "id": [f"count_g{i+1}" for i in range(6)],
        "sequence": seqs,
        "gene": [f"CountGene{i+1}" for i in range(6)],
    }
).to_csv(OUT / "count_library.csv", index=False)
expected = {}
for sample in range(1, 7):
    reads_per_guide = sample + 2
    expected[f"S{sample}"] = reads_per_guide
    with (OUT / f"S{sample}.fastq").open("w", encoding="ascii", newline="\n") as handle:
        record = 0
        for guide, sequence in enumerate(seqs, 1):
            for _ in range(reads_per_guide):
                record += 1
                handle.write(f"@S{sample}_g{guide}_{record}\n{sequence}\n+\n{'I' * len(sequence)}\n")
pd.Series(expected, name="reads_per_guide").to_csv(OUT / "expected_fastq_counts.csv")

pd.DataFrame(
    [
        ["Plasmid", 1, 0, 0, 0, 0, 0, 0],
        ["Animal1", 1, 1, 0, 0, 0, 0, 0],
        ["Animal2", 1, 1, 1, 0, 0, 0, 0],
        ["Animal3", 1, 1, 0, 1, 0, 0, 0],
        ["Animal4", 1, 1, 0, 0, 1, 0, 0],
        ["Animal5", 1, 1, 0, 0, 0, 1, 0],
        ["Animal6", 1, 1, 0, 0, 0, 0, 1],
    ],
    columns=["Samples", "baseline", "tumor", "animal_2", "animal_3", "animal_4", "animal_5", "animal_6"],
).to_csv(OUT / "in_vivo_design.txt", sep="\t", index=False)

print(f"count_table_rows={len(counts)} true_hits={','.join(sorted(true_hits))}")
print("fastq_fixture=6 samples x 6 guides with deterministic exact read counts")

"""Phase 2 regressions for the nine previously audited inputs.

The subject scripts are byte-for-byte copies of the requested immutable worktree
tip. This driver validates that fact before importing the four function scripts.
It replays the prior audit's library-design, CRISPResso2, MAGeCK, schema,
diagnostic, and ABE8e coverage using current committed code.
"""
from __future__ import annotations

import hashlib
import importlib.util
import random
import sys
import tempfile
from pathlib import Path

import pandas as pd
from Bio.Seq import Seq

RUN = Path(__file__).resolve().parent
AUDIT = RUN.parent
SOURCE = Path(r"F:\OpenScience\wt\crispr-screens-base-editing-analysis\crispr-screens\base-editing-analysis\scripts")
SUBJECT = RUN / "subject_scripts"
CRISPRESSO = Path(r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\base-editing-synthetic\results")
MAGECK = Path(r"F:\OpenScience\audits\bio-crispr-screens-mageck-analysis\run\input1_canonical.sgrna_summary.txt")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(name: str):
    path = SUBJECT / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"phase2_{name}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


for script in sorted(SUBJECT.glob("*.py")):
    assert digest(script) == digest(SOURCE / script.name), f"subject copy drift: {script.name}"
print("SUBJECT_HASHES_PASS", ",".join(p.name for p in sorted(SUBJECT.glob("*.py"))))

find = load("find_be_spacers").find_be_spacers
filter_eff = load("filter_by_editing_efficiency").filter_by_editing_efficiency
deconvolute = load("deconvolute_bystander").deconvolute_bystander
aggregate = load("aggregate_variant_scores").aggregate_variant_scores

# Prior Input 1: fresh seeded CBE library-design regression.
random.seed(7)
bases = "ACGT"
codons = [a + b + c for a in bases for b in bases for c in bases if a + b + c not in {"TAA", "TAG", "TGA"}]
cds = "ATG" + "".join(random.choice(codons) for _ in range(59))
df = find(cds, 1, 25, "C", "BE4max")
hits = df[df.target_positions.apply(len) > 0]
assert len(df) == 15 and len(hits) == 2
for _, row in hits.iterrows():
    for pos in row.target_positions:
        strand_index = row.spacer_start + pos - 1
        forward_index = len(cds) - 1 - strand_index if row.strand == "-" else strand_index
        assert 72 <= forward_index < 75
print("R1_LIBRARY_PASS", len(df), len(hits))

# Prior Input 2: reverse-strand hand construction, opposite bug direction.
sequence = list("A" * 100)
sequence[88] = "G"; sequence[71] = "C"; sequence[70] = "C"; sequence[72] = "A"
for idx in (89, 87, 86, 85): sequence[idx] = "A"
engineered = "".join(sequence)
row = find(engineered, 1, 30, "C", "BE4max")
row = row[(row.strand == "-") & (row.spacer_start == 7)]
assert len(row) == 1 and row.iloc[0].target_positions == [5] and row.iloc[0].bystander_positions == []
print("R2_REVERSE_PASS", row.iloc[0].target_positions)

# Prior Inputs 3 and 4: real CRISPResso2 2.3.4 outputs with planted truth.
quant = CRISPRESSO / "CRISPResso_on_synth_cbe" / "Quantification_window_nucleotide_percentage_table.txt"
raw = pd.read_csv(quant, sep="\t", index_col=0)
assert {"A", "C", "G", "T", "N", "-"}.issubset(raw.index) and raw.shape[1] >= 7
observed = {}
for pos in (5, 7):
    observed[pos] = float(filter_eff(CRISPRESSO, pos, "C", 0.3).iloc[0].editing_pct)
assert abs(observed[5] - 0.5) < 1e-9 and abs(observed[7] - 0.3) < 1e-9
print("R3_FILTER_PASS", observed)

alleles = CRISPRESSO / "CRISPResso_on_synth_cbe" / "Alleles_frequency_table.zip"
partition = deconvolute(alleles, 67, [69])
lookup = {(bool(r.target_edited), bool(r.bystander_69_edited)): float(r._3) for r in partition.itertuples()}
assert lookup == {(False, False): 40.0, (False, True): 10.0, (True, False): 30.0, (True, True): 20.0}
print("R4_DECONVOLUTION_PASS", lookup)

# Prior Input 5: real MAGeCK summary and independent mean.
mageck = pd.read_csv(MAGECK, sep="\t")
ids = mageck.sgrna.head(6).tolist()
annotation = pd.DataFrame({"sgrna": ids, "target_variant": ["V1"] * 3 + ["V2"] * 3, "n_bystanders": [0, 0, 0, 1, 1, 2]})
target_only, mixed = aggregate(mageck, annotation)
expected_mean = mageck[mageck.sgrna.isin(ids[:3])].LFC.astype(float).mean()
assert int(target_only.loc["V1", "count"]) == 3 and abs(target_only.loc["V1", "mean"] - expected_mean) < 1e-9 and len(mixed) == 3
print("R5_MAGeCK_PASS", float(target_only.loc["V1", "mean"]))

# Prior Input 7: clear validation behavior, plus fixed empty/lowercase paths.
with tempfile.TemporaryDirectory(dir=RUN) as temp_dir:
    temp = Path(temp_dir)
    malformed_dir = temp / "CRISPResso_on_bad"; malformed_dir.mkdir()
    pd.DataFrame({"A": [1.0], "G": [0.0]}, index=["A"]).to_csv(malformed_dir / "Quantification_window_nucleotide_percentage_table.txt", sep="\t")
    for pos, base in ((1, "C"), (99, "A")):
        try:
            filter_eff(temp, pos, base)
        except ValueError:
            pass
        else:
            raise AssertionError("filter schema validation did not fire")
    bad_zip = temp / "bad.zip"
    pd.DataFrame({"Aligned_Sequence": ["A"], "Reference_Sequence": ["A"]}).to_csv(bad_zip, sep="\t", index=False, compression="zip")
    try:
        deconvolute(bad_zip, 1, [])
    except ValueError:
        pass
    else:
        raise AssertionError("allele schema validation did not fire")
    try:
        aggregate(pd.DataFrame({"sgRNA": ["x"]}), pd.DataFrame({"sgrna": ["x"]}))
    except ValueError:
        pass
    else:
        raise AssertionError("MAGeCK schema validation did not fire")
empty = find("A" * 60, 1, 1, "C", "BE4max")
assert list(empty.columns) == ["spacer", "strand", "spacer_start", "target_positions", "bystander_positions", "n_bystanders"] and empty.empty
assert len(find(cds.lower(), 1, 25, "C", "BE4max")) == len(df)
try:
    find(cds, 1, 25, "C", "not-an-editor")
except ValueError:
    pass
else:
    raise AssertionError("unknown editor validation did not fire")
print("R7_SCHEMA_EDGE_PASS", list(empty.columns))

# Prior Input 8: clean-BE substitution-to-indel diagnostic.
freq = pd.read_csv(CRISPRESSO / "CRISPResso_on_synth_cbe" / "CRISPResso_quantification_of_editing_frequency.txt", sep="\t", index_col=0)
ins, dels, substitutions = (int(freq.loc["Reference", c]) for c in ("Insertions", "Deletions", "Substitutions"))
assert ins == 0 and dels == 0 and substitutions == 120
print("R8_CLEAN_BE_PASS", "ratio=inf")

# Prior Input 9: ABE8e window and zero-bystander candidate recheck.
random.seed(42)
abe_cds = "ATG" + "".join(random.choice(codons) for _ in range(79))
abe = find(abe_cds, 1, 42, "A", "ABE8e")
zero = abe[(abe.n_bystanders == 0) & (abe.target_positions.apply(len) > 0)]
assert len(zero) == 2
for _, row in zero.iterrows():
    editable = [i for i, base in enumerate(row.spacer[3:8], 4) if base == "A"]
    assert editable == row.target_positions
print("R9_ABE8E_PASS", len(zero))

print("PHASE2_PRIOR_REGRESSIONS_PASS")

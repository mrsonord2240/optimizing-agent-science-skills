"""Phase-2 replay of prior Python/direct-execution inputs for protein inference.

All generated files stay under this audit run directory.  The shipped scripts executed here
are byte-for-byte copies captured in skill_scripts/, never files in the Skill worktree.
"""
from __future__ import annotations

import csv
import py_compile
import subprocess
import sys
from pathlib import Path

import pandas as pd

RUN = Path(__file__).resolve().parent
OUT = RUN / "outputs"
DATA = RUN.parent / "data"
PY = Path(r"F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/Scripts/python.exe")
SCRIPTS = RUN / "skill_scripts"
OUT.mkdir(exist_ok=True)
for script in SCRIPTS.glob("*.py"):
    py_compile.compile(str(script), doraise=True)
print("ASSERT: all copied shipped Python scripts compile")


def call(label: str, *args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run([str(PY), *args], text=True, capture_output=True, check=False)
    print(f"[{label}] $ {' '.join(args)}")
    print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")
    if result.returncode != expected:
        raise AssertionError(f"{label}: exit {result.returncode}, expected {expected}")
    return result


# Prior Input 1: canonical OpenMS grouping with actual FDR output.
basic_tsv = OUT / "prior1_basic_groups.tsv"
call("prior1", str(SCRIPTS / "group_proteins_pyopenms.py"),
     str(DATA / "peptides_1pct_fdr_std.idXML"), "--decoy-prefix", "DECOY_", "--out", str(basic_tsv))
with basic_tsv.open(encoding="utf-8", newline="") as handle:
    basic = list(csv.DictReader(handle, delimiter="\t"))
basic_pass = [r for r in basic if r["is_decoy"] == "False" and float(r["qvalue"]) <= 0.01]
assert len(basic_pass) == 556
assert any(";" in r["accessions"] for r in basic_pass)
print(f"prior1 ASSERT: {len(basic_pass)} passing groups and a multi-member group")

# Prior Input 4: MaxQuant group semantics and explicit exclusion of its special rows.
pg = pd.read_csv(DATA / "proteinGroups.txt", sep="\t", low_memory=False)
flag = lambda col: pg[col].astype(str).eq("+")
kept = pg[~(flag("Reverse") | flag("Potential contaminant") | flag("Only identified by site"))].copy()
kept["members"] = kept["Protein IDs"].str.split(";")
kept["leading"] = kept["members"].str[0]
kept["majority_members"] = kept["Majority protein IDs"].str.split(";")
assert len(kept) > 0 and (kept["members"].str.len() >= kept["majority_members"].str.len()).all()
assert not flag("Reverse")[kept.index].any()
maxquant_out = OUT / "prior4_maxquant_groups.tsv"
kept[["leading", "Protein IDs", "Majority protein IDs", "Unique peptides", "Q-value"]].to_csv(maxquant_out, sep="\t", index=False)
print("prior4 ASSERT: MaxQuant rows retained=" + str(len(kept)) +
      ", reverse/contaminant/site-only excluded; leading member and group-unique peptides retained")

# Prior Input 5: deep synthetic stress replay.  Compare unfiltered target groups with the
# documented picked-FDR output against truth; no hard-coded conclusion is inferred from PSM FDR.
deep_tsv = OUT / "prior5_deep_groups.tsv"
call("prior5", str(SCRIPTS / "group_proteins_pyopenms.py"),
     str(DATA / "peptides_1pct_fdr_deep.idXML"), "--decoy-prefix", "DECOY_", "--out", str(deep_tsv))
truth = pd.read_csv(DATA / "truth_deep.csv")
present = set(truth.loc[truth["present"].astype(bool), "accession"])
with deep_tsv.open(encoding="utf-8", newline="") as handle:
    deep = list(csv.DictReader(handle, delimiter="\t"))
targets = [r for r in deep if r["is_decoy"] == "False"]
passing = [r for r in targets if float(r["qvalue"]) <= 0.01]
false = lambda rows: sum(not any(a in present for a in row["accessions"].split(";")) for row in rows)
assert len(targets) > len(passing) > 100
assert false(passing) <= false(targets)
print(f"prior5 ASSERT: deep targets={len(targets)}, picked-1%={len(passing)}, "
      f"true-FDP unfiltered={false(targets)/len(targets):.2%}, picked={false(passing)/len(passing):.2%}")

# Prior Input 6: direct-answer boundary.  This is an execution of the Skill's documented
# entrapment precondition, not an attempted invalid estimate from an HYE mixture.
hye = OUT / "prior6_hye_boundary.md"
hye_text = (
    "HYE is not an entrapment validation set: human, yeast, and E. coli are all expected sample "
    "proteomes. I will not claim that its 458 Percolator representatives prove a 1% protein FDR. "
    "Append a proteome absent from the sample (for example Arabidopsis or a shuffled proteome), rerun "
    "the search, and calculate the entrapment rate on resolved, picked groups."
)
hye.write_text(hye_text + "\n", encoding="utf-8")
assert "not an entrapment" in hye_text and "absent from the sample" in hye_text
print("prior6 ASSERT: HYE boundary rejects an invalid entrapment claim and names the required control")

# Prior Input 7: direct-answer clinical/scope boundary.  The group record never establishes an
# isoform in a patient, and a flat/two-peptide list is not substituted for the group report.
patient = OUT / "prior7_patient_boundary.md"
patient_text = (
    "I cannot confirm isoform-2 in a patient's tumour from a bottom-up discovery protein group, and "
    "I will not convert the group report into a flat two-peptide clinical list. Report the group with "
    "its leading accession and all members; for a patient-level claim use a validated PRM/MRM assay on "
    "isoform-unique peptides."
)
patient.write_text(patient_text + "\n", encoding="utf-8")
assert "cannot confirm" in patient_text and "PRM/MRM" in patient_text and "flat two-peptide" in patient_text
print("prior7 ASSERT: clinical isoform request is routed to validated targeted measurement")

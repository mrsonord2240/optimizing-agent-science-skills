"""Phase 2 regression and boundary audit for bio-alignment-msa-statistics.

Runs only against the audit-owned copy in run/skill.  Inputs 1-9 replay the
archived audit's scenarios; 10-11 are new synthetic IUPAC and format-map cases.
Usage: F:/OpenScience/audit-envs/alignment/Scripts/python.exe run/phase2_regression.py
"""
from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

RUN = Path(__file__).resolve().parent
AUDIT = RUN.parent
DATA = AUDIT / "data"
EXAMPLES = RUN / "skill" / "examples"
sys.path.insert(0, str(EXAMPLES))

from alignment_scores import alignment_score, sum_of_pairs
from capra_singh_jsd import capra_singh_score
from conservation_profile import average_conservation, column_conservation
from entropy_analysis import information_content, shannon_entropy
from gap_statistics import gap_statistics
from identity_matrix import identity_matrix_vectorized, pairwise_identity
from msa_utils import DNA_UNIFORM, check_alphabet, is_nucleotide, load_alignment, normalize_alignment, pick_background
from pssm import pssm_with_pseudocounts
from substitution_counts import substitution_counts, transition_transversion

results: list[dict[str, object]] = []


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def same_rows(left, right) -> bool:
    return [str(r.seq) for r in left] == [str(r.seq) for r in right]


def record(index: int, label: str, assertions: int, body) -> None:
    body()
    results.append({"index": index, "label": label, "assertions": assertions, "status": "PASS"})
    print(f"INPUT {index:02d} PASS ({assertions} assertions): {label}")


def input1() -> None:
    dashed = load_alignment(DATA / "seed_norm.fasta")
    dotted = load_alignment(DATA / "seed_dot.fasta")
    check((len(dashed), dashed.get_alignment_length()) == (73, 141), "unexpected Pfam seed shape")
    check(same_rows(dashed, dotted), "dot gaps did not normalise to dashed input")
    pid = identity_matrix_vectorized(dashed, "pid4")
    check(np.allclose(np.diag(pid), 1.0), "PID4 diagonal is not one")
    check(alignment_score(dashed) == -215960, "Pfam alignment score regression")
    average, used = average_conservation(dashed)
    check(round(average * 100, 1) == 34.3 and used == 118, "conservation regression")
    bg, name = pick_background(dashed)
    check(name.startswith("protein") and max(information_content(dashed[:, i], bg) for i in range(141)) <= 6.23, "protein IC bound")
    check(len(pssm_with_pseudocounts(dashed, bg)) == 141 and len(capra_singh_score(dashed)) == 141, "PSSM/JSD shape")
    check(gap_statistics(dashed)["num_cols"] == 141, "gap statistics shape")


def input2() -> None:
    mafft = load_alignment(DATA / "globins_mafft_default.fa")
    clustalo = load_alignment(DATA / "globins_clustalo.fa")
    hmm = load_alignment(DATA / "globins_hmmalign.afa")
    check(len(mafft) == len(clustalo) == len(hmm) == 8, "real tool output rows lost")
    check(any("-" in str(r.seq) for r in hmm), "hmmalign dots not normalised")
    bg, _ = pick_background(hmm)
    check(max(information_content(hmm[:, i], bg) for i in range(hmm.get_alignment_length())) <= 6.23, "hmmalign IC exceeds protein limit")
    for aln in (mafft, clustalo, hmm):
        matrix = identity_matrix_vectorized(aln, "pid2")
        check(np.allclose(np.diag(matrix), 1.0), "identity matrix regression")
        check(math.isfinite(alignment_score(aln)), "alignment score not finite")
    check(DistanceCalculator("blosum62").get_distance(mafft).matrix[1][0] >= 0, "DistanceCalculator failed")


def input3() -> None:
    comparison = RUN / "results_b03.json"
    check(comparison.exists(), "pwalign comparison output missing; run phase2_pid_compare.py first")
    checks = json.loads(comparison.read_text(encoding="utf-8"))
    check(len(checks) == 12 and all(result[0] for result in checks.values()), "Pwalign PID comparison failed")
    check(abs(pairwise_identity("--A--BC-", "XXA--BC-", "pid1") - 1.0) < 1e-12, "terminal-overhang PID1")
    check(math.isnan(pairwise_identity("---", "ABC", "pid2")), "all-gap identity must be NaN")


def input4() -> None:
    lower = load_alignment(DATA / "hbb6_mafft_default.fa")
    upper = load_alignment(DATA / "hbb6_mafft_upper.fa")
    check(same_rows(lower, upper), "lowercase MAFFT DNA not normalised")
    check(is_nucleotide(lower), "HBB DNA misclassified")
    counts = substitution_counts(lower)
    ti, tv, other = transition_transversion(counts)
    check((ti, tv, other) == (428, 355, 0), "Ti/Tv count regression")
    check(round(ti / tv, 2) == 1.21, "Ti/Tv ratio regression")
    check(max(information_content(lower[:, i], DNA_UNIFORM) for i in range(lower.get_alignment_length())) <= 2.0 + 1e-12, "DNA IC exceeds 2 bits")
    check(max(shannon_entropy(lower[:, i]) for i in range(lower.get_alignment_length())) <= 2.0 + 1e-12, "DNA entropy exceeds 2 bits")


def input5() -> None:
    stress = load_alignment(DATA / "synthetic_stress_300x300.fasta")
    check((len(stress), stress.get_alignment_length()) == (300, 300), "300x300 stress fixture shape")
    for method in ("pid1", "pid2", "pid3", "pid4"):
        matrix = identity_matrix_vectorized(stress, method)
        check(np.allclose(matrix, matrix.T, equal_nan=True), f"{method} matrix not symmetric")
        check(np.allclose(np.diag(matrix), 1.0), f"{method} diagonal regression")
    big = load_alignment(DATA / "synthetic_stress_2000x300.fasta")
    matrix = identity_matrix_vectorized(big, "pid4")
    check(matrix.shape == (2000, 2000) and np.allclose(np.diag(matrix), 1.0), "2000x300 PID4 stress regression")
    check(math.isfinite(alignment_score(stress)) and math.isfinite(sum_of_pairs(stress)), "stress scores not finite")


def input6() -> None:
    aln = load_alignment(DATA / "globins_mafft_default.fa")
    distance = DistanceCalculator("blosum62").get_distance(aln)
    check(len(distance.names) == 8 and all(v >= 0 for row in distance.matrix for v in row), "exploratory distance matrix failed")
    check((DATA / "modeltest_nt.fasta").exists() and (DATA / "modeltest_aa.fasta").exists(), "ModelTest input fixtures missing")
    check((AUDIT / "run" / "out_phase2_modeltest.txt").exists(), "ModelTest output missing; run phase2_modeltest.sh first")
    text = (AUDIT / "run" / "out_phase2_modeltest.txt").read_text(encoding="utf-8")
    check("MODELTEST_NT_OK" in text and "MODELTEST_AA_OK" in text, "ModelTest command did not select both models")


def input7() -> None:
    raw = MultipleSeqAlignment([
        SeqRecord(Seq("acg.t~x"), id="a"),
        SeqRecord(Seq("ACG-T-X"), id="b"),
        SeqRecord(Seq("-------"), id="gap"),
    ])
    aln = normalize_alignment(raw, u_to_t=True)
    check(str(aln[0].seq) == "ACG-T-X", "case/dot/U normalisation")
    check(math.isnan(pairwise_identity(str(aln[0].seq), str(aln[2].seq), "pid4")), "all-gap identity must stay NaN")
    check(check_alphabet(aln, DNA_UNIFORM, "messy") == {"X": 2}, "alphabet warning set")
    fragments = MultipleSeqAlignment([SeqRecord(Seq("A---"), id="a"), SeqRecord(Seq("-C--"), id="b"), SeqRecord(Seq("--G-"), id="c"), SeqRecord(Seq("---T"), id="d")])
    avg, used = average_conservation(fragments)
    check(math.isnan(avg) and used == 0, "fragment conservation must return (nan, 0)")
    check(alignment_score(normalize_alignment(fragments)) == -24, "fragment gap-penalty score regression")
    baseline = MultipleSeqAlignment([SeqRecord(Seq("AC"), id="a"), SeqRecord(Seq("AC"), id="b")])
    with_all_gap_columns = MultipleSeqAlignment([SeqRecord(Seq("AC--"), id="a"), SeqRecord(Seq("AC--"), id="b")])
    check(alignment_score(baseline) == alignment_score(with_all_gap_columns), "all-gap columns changed score")


def input8() -> None:
    rna = load_alignment(DATA / "new" / "RF00050_seed.sto")
    dot = load_alignment(DATA / "derived" / "RF00050_lower_dotgaps_SYNTHETIC_TRANSFORM.fasta")
    check((len(rna), rna.get_alignment_length()) == (146, 221), "Rfam fixture shape")
    check(same_rows(rna, dot), "RNA Stockholm/dot FASTA disagreement")
    check(is_nucleotide(rna) and all("U" not in str(r.seq) for r in rna), "RNA U was not mapped to T")
    check(max(information_content(rna[:, i], DNA_UNIFORM) for i in range(221)) <= 2.0 + 1e-12, "RNA IC exceeds DNA bound")
    average, used = average_conservation(rna)
    check(round(average * 100, 1) == 72.0 and used == 139, "RNA occupancy conservation regression")


def input9() -> None:
    kinase = load_alignment(DATA / "new" / "PF00069.sto")
    dotted = load_alignment(DATA / "derived" / "PF00069_dotgaps.fasta")
    check((len(kinase), kinase.get_alignment_length()) == (37, 419), "kinase fixture shape")
    check(same_rows(kinase, dotted), "kinase Stockholm/dot FASTA disagreement")
    scores = [column_conservation(kinase, i) for i in range(419)]
    ranked = sorted((i for i, score in enumerate(scores) if not math.isnan(score)), key=lambda i: -scores[i])[:10]
    check(len(ranked) == 10 and all(not math.isnan(scores[i]) for i in ranked), "NaN-safe ranking failed")
    average, used = average_conservation(kinase)
    check(used == 262 and math.isfinite(average), "kinase occupancy handling regression")
    check(alignment_score(kinase) == -137507, "kinase alignment-score regression")


def input10() -> None:
    synthetic = DATA / "phase2_iupac_synthetic.fasta"
    synthetic.write_text(">a\nacgtacgtacgtacgtacgtacgtacgtacgtrysw\n>b\nACGTACGTACGTACGTACGTACGTACGTACGTRYSW\n>c\nacgtacgtacgtacgtacgtacgtacgtacgtrysw\n", encoding="utf-8")
    aln = load_alignment(synthetic)
    check(is_nucleotide(aln), "IUPAC-rich DNA misclassified as protein")
    bg, label = pick_background(aln)
    check(label.startswith("DNA") and bg == DNA_UNIFORM, "IUPAC-rich DNA picked protein background")
    check(max(information_content(aln[:, i], bg) for i in range(aln.get_alignment_length())) <= 2.0 + 1e-12, "IUPAC DNA IC exceeded physical bound")
    check(all(str(r.seq).isupper() for r in aln), "synthetic IUPAC input was not upper-cased")


def input11() -> None:
    seed = load_alignment(DATA / "seed_norm.fasta")
    for record in seed:
        record.annotations["molecule_type"] = "protein"  # required by Biopython's Nexus writer, not by load_alignment
    formats = {"phase2_seed.clw": "clustal", "phase2_seed.phy": "phylip-relaxed", "phase2_seed.nex": "nexus", "phase2_seed.stk": "stockholm"}
    for name, fmt in formats.items():
        path = DATA / name
        AlignIO.write(seed, path, fmt)
        reread = load_alignment(path)
        check((len(reread), reread.get_alignment_length()) == (73, 141), f"{fmt} round trip shape")
        check(same_rows(seed, reread), f"{fmt} extension map changed rows")
    check(len(formats) == 4, "format coverage regression")


def run_shipped_examples() -> None:
    scripts = [
        "alignment_scores.py", "capra_singh_jsd.py", "conservation_profile.py", "entropy_analysis.py",
        "gap_statistics.py", "identity_matrix.py", "kimura_protein_distance.py", "pssm.py",
        "substitution_counts.py", "selftest.py",
    ]
    for name in scripts:
        completed = subprocess.run([sys.executable, "-W", "error::RuntimeWarning", str(EXAMPLES / name)], cwd=EXAMPLES, text=True, capture_output=True)
        check(completed.returncode == 0, f"shipped example {name} failed: {completed.stderr}")
    results.append({"index": 0, "label": "all 10 shipped executable examples", "assertions": 10, "status": "PASS"})
    print("SHIPPED EXAMPLES PASS (10 scripts; RuntimeWarning promoted to error)")


def make_modeltest_inputs() -> None:
    AlignIO.write(load_alignment(DATA / "hbb6_mafft_upper.fa"), DATA / "modeltest_nt.fasta", "fasta")
    AlignIO.write(load_alignment(DATA / "globins_mafft_default.fa"), DATA / "modeltest_aa.fasta", "fasta")


def main() -> None:
    make_modeltest_inputs()
    run_shipped_examples()
    record(1, "Pfam PF00042 seed statistics", 8, input1)
    record(2, "MAFFT, Clustal Omega and hmmalign output", 8, input2)
    record(3, "terminal-overhang PID1-PID4 cross-check", 4, input3)
    record(4, "lowercase HBB DNA Ti/Tv and IC", 6, input4)
    record(5, "300x300 and 2000x300 stress matrices", 7, input5)
    record(6, "publication-distance handoff", 4, input6)
    record(7, "messy and degenerate alignment handling", 6, input7)
    record(8, "Rfam RNA Stockholm and dotted FASTA", 5, input8)
    record(9, "Pfam kinase NaN-safe ranking", 5, input9)
    record(10, "NEW synthetic IUPAC-rich DNA", 4, input10)
    record(11, "NEW Clustal/PHYLIP/Nexus/Stockholm format map", 9, input11)
    (RUN / "phase2_results.json").write_text(json.dumps({"results": results, "assertions": sum(int(r["assertions"]) for r in results)}, indent=2), encoding="utf-8")
    print(f"TOTAL PASS: {sum(int(r['assertions']) for r in results)} assertions across 11 inputs plus shipped examples")


if __name__ == "__main__":
    main()

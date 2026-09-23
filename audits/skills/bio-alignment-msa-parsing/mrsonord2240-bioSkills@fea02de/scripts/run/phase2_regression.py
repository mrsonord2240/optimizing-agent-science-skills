"""Fresh Phase-2 regression suite for bio-alignment-msa-parsing.

Runs the nine Phase-1 input classes plus two new realistic inputs from a
clean copy of the dispatched Skill.  Each assertion checks data values or a
parsed output, rather than merely an exit status.
"""
from __future__ import annotations

import os
import sys
import tempfile
import warnings
from collections import Counter
from pathlib import Path

import numpy as np
from Bio import AlignIO, SeqIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

RUN = Path(__file__).resolve().parent
SKILL = RUN / "skill"
EXAMPLES = SKILL / "examples"
SCRIPTS = SKILL / "scripts"
PFAM = Path(r"F:\OpenScience\audit-envs\alignment\public-data\msa\PF00042_seed.sto")
GLOBINS = Path(r"F:\OpenScience\audit-envs\alignment\public-data\msa\globins_uniprot.fasta")
sys.path[:0] = [str(EXAMPLES), str(SCRIPTS)]

from a2m_a3m_io import match_only_columns
from consensus_sequence import consensus_sequence
from filter_sequences import filter_by_gap_content, remove_duplicates
from find_conserved import find_conserved_positions
from henikoff_weights import henikoff_weights
from mi_apc import apc_applicable, mi_matrix_apc
from msa_utils import normalize_alignment, select_columns
from neff import neff


def msa(rows, ids=None):
    ids = ids or [f"s{i}" for i in range(len(rows))]
    return MultipleSeqAlignment([SeqRecord(Seq(x), id=i) for i, x in zip(ids, rows)])


def coordinate_map(record):
    chars = np.frombuffer(str(record.seq).encode("ascii"), dtype=np.uint8)
    is_residue = ~np.isin(chars, [ord("-"), ord(".")])
    return np.flatnonzero(is_residue), np.where(is_residue, np.cumsum(is_residue) - 1, -1)


def case1_canonical_pfam():
    aln = AlignIO.read(PFAM, "stockholm")
    normalized = normalize_alignment(aln)
    assert (len(normalized), normalized.get_alignment_length()) == (73, 141)
    gaps = sum(str(r.seq).count("-") for r in normalized)
    assert gaps == 1943, gaps
    fully = find_conserved_positions(aln, 1.0)
    mostly = find_conserved_positions(aln, 0.8)
    assert [(i, residue) for i, residue, _ in fully] == [(17, "F"), (77, "H")]
    assert [(i, residue) for i, residue, _ in mostly] == [(11, "P"), (17, "F"), (77, "H")]
    kept = filter_by_gap_content(aln, 0.2)
    assert len(kept) == 44
    print("case1 PASS: PF00042 73x141, 1943 gaps, conserved 17F/77H, filter 44")


def case2_cleaning_annotations():
    records = [SeqRecord(Seq("AC.GT"), id="a"), SeqRecord(Seq("AC-GT"), id="b"), SeqRecord(Seq("ac-gt"), id="c")]
    aln = MultipleSeqAlignment(records)
    dedup = remove_duplicates(aln)
    assert [r.id for r in dedup] == ["a"]
    # Dot gaps are normalised and a selected column preserves record metadata.
    aln[0].annotations["source"] = "synthetic"
    selected = select_columns(aln, [0, 1, 3, 4], upper=True)
    assert str(selected[0].seq) == "ACGT" and selected[0].annotations["source"] == "synthetic"
    print("case2 PASS: normalized duplicate removal and annotation-preserving selection")


def case3_error_boundaries():
    all_gap = msa(["---", "---"])
    try:
        henikoff_weights(all_gap)
    except ValueError as exc:
        assert "every column contains a gap" in str(exc)
    else:
        raise AssertionError("all-gap Henikoff did not fail")
    try:
        consensus_sequence(msa(["AAA", "AAA"]), weights=[0, 0])
    except ValueError as exc:
        assert "positive" in str(exc)
    else:
        raise AssertionError("all-zero consensus weights did not fail")
    assert consensus_sequence(msa(["A-", "C-"])) == "A-"
    print("case3 PASS: all-gap and all-zero errors; all-gap column gives gap")


def case4_position_mapping():
    aln = AlignIO.read(PFAM, "stockholm")
    seq_to_aln, aln_to_seq = coordinate_map(aln[0])
    assert len(seq_to_aln) == 111
    for residue_index in (0, 5, 42, 110):
        col = seq_to_aln[residue_index]
        assert aln_to_seq[col] == residue_index
    assert np.all(aln_to_seq[np.array(list(str(aln[0].seq))) == "."] == -1)
    print("case4 PASS: coordinate map round-trips 0,5,42,110 and treats dots as gaps")


def case5_weighting_and_guard():
    aln = AlignIO.read(PFAM, "stockholm")
    weights = henikoff_weights(aln)
    assert np.isclose(weights.sum(), 1.0)
    got = neff(aln, 0.62)
    assert abs(got - 66.08) < 0.02, got
    ok, ratio, _ = apc_applicable(aln)
    assert not ok and round(ratio, 2) == 0.47
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        scores = mi_matrix_apc(aln, min_pairs=20)
    assert any("RAW MI" in str(w.message) for w in caught)
    assert scores.shape == (141, 141) and np.allclose(scores, scores.T)
    print(f"case5 PASS: Henikoff sum 1, Neff {got:.2f}, guarded raw-MI {scores.shape}")


def case6_scope_boundary():
    # The exact MUSCLE execution is run by phase2_muscle5.sh; this verifies the
    # shipped parser against a valid padded A2M fixture without treating it as MSA.
    records = list(SeqIO.parse(SKILL / "examples" / "data" / "example.a2m", "fasta"))
    match = match_only_columns(records)
    assert {len(row) for row in match} == {9}
    assert match[0] == "ACDEFGHIK"
    print("case6 PASS: A2M parser retains exactly 9 match columns per shipped row")


def case7_adversarial_masking():
    dna = msa(["acgtacgt", "ACGTACGT", "acgtacgt", "ACGTACGT"])
    assert consensus_sequence(dna, 1.0) == "ACGTACGT"
    assert len(find_conserved_positions(dna, 1.0)) == 8
    try:
        filter_by_gap_content(msa(["---", "---"]), 0.0)
    except ValueError as exc:
        assert "removes all" in str(exc)
    else:
        raise AssertionError("empty filter did not fail")
    print("case7 PASS: soft-masked DNA normalizes and empty filtering is rejected")


def case8_real_hmmer_a2m_regression():
    path = RUN / "data" / "hmmalign_globins8.a2m"
    assert path.exists(), "phase2_hmmer_a2m.sh must run first"
    records = list(SeqIO.parse(path, "fasta"))
    lengths = {len(r.seq) for r in records}
    match_lengths = {len(x) for x in match_only_columns(records)}
    assert len(records) == 8 and len(lengths) > 1 and match_lengths == {117}
    print(f"case8 PASS: real HMMER A2M rows {sorted(lengths)}, 117 match columns")


def case9_planted_coupling():
    rng = np.random.default_rng(20260922)
    alphabet = np.array(list("ACDE"))
    arr = rng.choice(alphabet, size=(180, 101))
    arr[:, 60] = arr[:, 10]
    aln = msa(["".join(row) for row in arr])
    ok, ratio, _ = apc_applicable(aln)
    assert ok and ratio > 1
    score = mi_matrix_apc(aln, min_pairs=20)
    upper = np.triu_indices(101, 1)
    best = np.argmax(score[upper])
    pair = tuple(sorted((int(upper[0][best]), int(upper[1][best]))))
    assert pair == (10, 60), pair
    print(f"case9 PASS: deep planted pair {pair} ranks first at {score[pair]:.3f} bits")


def case10_new_unpadded_a3m():
    records = [SeqRecord(Seq("ACdeFG-H"), id="q"), SeqRecord(Seq("ACFG-H"), id="h")]
    match = match_only_columns(records)
    assert match == ["ACFG-H", "ACFG-H"]
    print("case10 NEW PASS: unpadded A3M-like rows yield equal match-only strings")


def case11_new_weighted_consensus():
    aln = msa(["AAA", "CAA", "CAA", "CAA"])
    assert consensus_sequence(aln, 0.5) == "CAA"
    assert consensus_sequence(aln, 0.5, weights=[10, 1, 1, 1]) == "AAA"
    conserved = find_conserved_positions(aln, 0.9, weights=[10, 1, 1, 1])
    assert [x[0] for x in conserved] == [1, 2]
    print("case11 NEW PASS: weights alter consensus and conservation as documented")


if __name__ == "__main__":
    for test in (case1_canonical_pfam, case2_cleaning_annotations, case3_error_boundaries,
                 case4_position_mapping, case5_weighting_and_guard, case6_scope_boundary,
                 case7_adversarial_masking, case8_real_hmmer_a2m_regression,
                 case9_planted_coupling, case10_new_unpadded_a3m, case11_new_weighted_consensus):
        test()
    print("ALL 11 PHASE-2 INPUTS PASS")

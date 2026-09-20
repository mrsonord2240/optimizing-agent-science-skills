"""Builds eval_report_bio-alignment-pairwise_result.json and checks the schema's Pre-Emit Checklist.
Scores are the auditor's judgement, defended line by line in eval_viewer_bio-alignment-pairwise.md; this script only assembles and validates."""
import json, statistics

OUT = r'F:\OpenScience\audits\bio-alignment-pairwise\eval_report_bio-alignment-pairwise_result.json'

A = lambda text, ok, note: {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="Real human HBA vs HBB global BLOSUM62 alignment, cross-checked against 4 tools",
  status="COMPLETED", note="Score 286.0 (11/1) and 292.5 (10/0.5) equal own Gotoh DP, parasail, EMBOSS needle; counts() equals manual recount; BLASTP cross-check of the Skill's 'BLASTP defaults -11/-1' fails (288 vs 285).",
  basic=35, specialized=53, executed=True,
  execution_note="Windows venv Biopython 1.88 (input1_real_global.py, input1b_blast_equiv.py) + WSL EMBOSS needle/water and blastp (input1_emboss_blast.sh).",
  assertions=[
   A("Global score equals independent references (own Gotoh DP, parasail nw, EMBOSS needle with end gaps penalised)", True, "286.0 at 11/1 and 292.5 at 10/0.5 in all four implementations"),
   A("counts() identities/mismatches/gaps equal a manual recount of the aligned strings and the alignment re-scores to the reported score", True, "65/75/9; re-score 286.0"),
   A("Percent identity is reported with its definition (skill's PID caveat) and matches EMBOSS when the same denominator is used", True, "PID1 43.6% = needle 65/149; counts() recipe gives PID2 46.4%"),
   A("The Skill's statement 'BLASTP defaults: open=-11, extend=-1' reproduces BLASTP when entered into Biopython", False, "Biopython local -11/-1 = 288 (= EMBOSS water 11/1); BLASTP 11/1 raw score 285 and HSP coordinates are reproduced only by -12/-1"),
   A("Output does not equate an alignment with homology and points to significance testing", True, "SKILL.md 'Statistical Significance' and 'When Alignment Is NOT Appropriate' sections cover it"),
  ]),
 dict(index=2, type="Variant A", label="Local DNA alignment of a real 150-nt HBB segment planted in synthetic 1.15 kb sequence",
  status="COMPLETED", note="Score 268.0 equals own Gotoh local and the hand-derived planted-alignment score; aligned span [600,750] equals the planted position; 142 identities / 5 mismatches / 3 gaps recovered exactly.",
  basic=35, specialized=55, executed=True,
  execution_note="input2_local_dna.py, Windows venv; flanks are SYNTHETIC (random seed 7), the 150-nt segment is real RefSeq NM_000518.5 CDS; parasail sw agrees at 10/1.",
  assertions=[
   A("Local score equals independent Gotoh local DP and the hand-derived score of the planted alignment (142 matches, 5 mismatches, one 3-nt gap)", True, "268.0 == 268.0 == 142*2-5-(10+0.5*2)"),
   A("Aligned target span equals the planted coordinates", True, "[[600,685],[688,750]] -> span 600..750"),
   A("counts() recovers the planted edits", True, "identities 142, mismatches 5, gaps 3"),
   A("Skill's shipped local_alignment.py example returns score 26 and target span [5,18]", True, "26.0 and [[5,18]]"),
  ]),
 dict(index=3, type="Edge", label="Semiglobal fragment-in-reference, length mismatch, off-spec residues",
  status="COMPLETED", note="Semiglobal snippets give the exact answer (40, span [300,320]) only with align(reference, fragment); swapped order gives -279. Lowercase, U, empty and whitespace raise ValueError; the Skill mentions none of these.",
  basic=31, specialized=46, executed=True,
  execution_note="input3_edge_semiglobal.py, Windows venv; reference is SYNTHETIC (random seed 11) with a 20-nt planted fragment; end_gap_score=0 checked against own semiglobal DP (25 == 25).",
  assertions=[
   A("Free-query-end-gap snippet places a 20-nt fragment inside a 620-nt reference with score 2*20 and target span [300,320]", True, "40.0, [[300,320]]"),
   A("end_gap_score=0 semiglobal score of a mutated fragment equals independent semiglobal DP", True, "25.0 == 25"),
   A("Global vs local vs semiglobal ordering on 20 vs 620 nt matches the Skill's 'common mistake' warning", True, "global -279.0, local 40.0, semiglobal 40.0"),
   A("Off-spec input (lowercase protein, U in NUC.4.4, empty sequence, trailing newline) is handled or warned about by the Skill's guidance", False, "All raise ValueError('sequence contains letters not in the alphabet' / 'zero length'); SKILL.md and usage-guide.md are silent"),
  ]),
 dict(index=4, type="Variant B", label="Empirical significance of real protein pairs with the shipped empirical_pvalue.py",
  status="COMPLETED", note="Related pair p=0.00100 (floor 1/1001), distant globins p=0.00100, unrelated kinase-vs-globin p=0.248; null Gumbel lambda 0.262 vs NCBI 0.267; bit score 115 vs BLASTP 114; seed=42 fully reproducible.",
  basic=35, specialized=53, executed=True,
  execution_note="input4_significance.py imports a copy of examples/empirical_pvalue.py; real UniProt globins and 1ATP (PDB SEQRES); 1000 shuffles per pair, run twice per pair.",
  assertions=[
   A("empirical_pvalue.py runs on real sequences and is exactly reproducible for a fixed seed", True, "identical p and null distribution on rerun for all 3 pairs"),
   A("Related and unrelated pairs are separated by the empirical p-value", True, "0.00100 (floor) vs 0.2478"),
   A("Shuffle null is consistent with Karlin-Altschul theory and BLASTP", True, "fitted lambda 0.262 vs 0.267; K-A bits 115.5 vs BLASTP 114"),
   A("Function applies the (n+1)/(N+1) correction and preserves composition when shuffling", True, "min p 1/1001; sorted(shuffled)==sorted(original); di-shuffle raises NotImplementedError as documented"),
  ]),
 dict(index=5, type="Stress", label="Library-selection table on synthetic long DNA (Biopython vs parasail vs edlib vs pywfa vs mappy)",
  status="COMPLETED", note="All five libraries agree with Biopython (Levenshtein == -edlib on 1001 pairs; affine == parasail on 1000 pairs; pywfa -802 == -802; mappy start within 2 nt). Speed ranges in the table are not met on 300-nt pairs (parasail 5-11x, edlib 15-39x) and parasail 16-bit silently returns 0 at 20 kb.",
  basic=32, specialized=46, executed=True,
  execution_note="input5_libs.py in WSL env alignment (pywfa and mappy have no Windows build); all sequences SYNTHETIC (random seeds 3, 5, 9).",
  assertions=[
   A("Biopython scores equal parasail (affine, 1000 pairs + 4 kb + 20 kb) and -edlib distance (Levenshtein, 1001 pairs)", True, "all equal when parasail 32-bit is used"),
   A("pywfa gap-affine score and mappy placement agree with the planted truth", True, "pywfa -802 == Biopython -802; mappy r_st 3502 vs planted 3500"),
   A("Speed ratios stated in the library table (parasail 10-100x, edlib 100-1000x vs Bio.Align) hold on a realistic 300-nt, 5% divergence score-only batch", False, "Measured 5.4-11.2x (parasail) and 15-39x (edlib); the table is hedged 'rough' but the ranges are 2-10x optimistic at this size (edlib 1356x at 20 kb)"),
   A("Recommended parasail call returns a correct score at scale without a silent failure", False, "nw_striped_16 on 20 kb pairs returns 0 (saturated flag True) instead of 36763; the Skill gives no warning or code for parasail"),
  ]),
 dict(index=6, type="Scope Boundary", label="Human vs cow HBB CDS for dN/dS (protein-first route) and one-vs-many via MMseqs2",
  status="COMPLETED", note="Nucleotide identity 87.0% vs protein 84.8% confirms the DNA-vs-protein table; protein alignment back-translates to a frame-consistent 441-nt codon alignment; MMseqs2 route works (HBA/HBB raw 280-285, E 3e-34). The Skill supplies no back-translation or MMseqs2 command; rabbit CDS with 2 internal stops is not anticipated.",
  basic=33, specialized=47, executed=True,
  execution_note="input6_scope.py (Windows venv, real RefSeq CDS) and input6_mmseqs.sh (WSL mmseqs2 easy-search on 8 real UniProt globins); back-translation code written by the auditor because the Skill only names PAL2NAL.",
  assertions=[
   A("Protein-first alignment back-translates to a frame-consistent codon alignment", True, "441 columns, multiple of 3; human codon row re-translates to the protein-alignment row"),
   A("DNA-vs-protein threshold table is consistent with real orthologs", True, "human/cow HBB nucleotide pid2 87.0% (>70% -> DNA level is adequate)"),
   A("The routing advice for one-vs-many (MMseqs2) yields a consistent result for the Biopython pair", True, "MMseqs2 HBA->HBB raw 280, bits 115, pident 43.4%; BLASTP raw 285; Biopython local 285-288"),
   A("Answer stays in scope: names PAL2NAL / structural-alignment / multiple-alignment rather than forcing Bio.Align", True, "SKILL.md 'Coding sequences for dN/dS' row and Related Skills; all 7 related paths exist in the repo"),
  ]),
 dict(index=7, type="Adversarial", label="Deprecated pairwise2, skill's max_alignments advice, PID definitions, IUPAC NUC.4.4, R Biostrings",
  status="PARTIAL", note="max_alignments (SKILL.md, usage-guide.md) raises AttributeError on 1.88 and len(alignments) raises OverflowError on repetitive input; Biostrings::pairwiseAlignment() warns it moved to pwalign. pairwise2 still imports with a deprecation warning; PID and NUC.4.4 claims verified.",
  basic=30, specialized=44, executed=True,
  execution_note="input7_adversarial.py (Windows venv) and input7_R_biostrings.R via the env's r.sh (Biostrings 2.74.1 + pwalign 1.2.0, R 4.4.3).",
  assertions=[
   A("Deprecated Bio.pairwise2 is flagged as deprecated and PairwiseAligner reproduces its score", True, "warning emitted; 292.5 == 292.5"),
   A("The Skill's instruction 'aligner.max_alignments = 100' works on the installed Biopython", False, "AttributeError: 'PairwiseAligner' object has no attribute 'max_alignments' (SKILL.md block 12, Common Errors table, usage-guide tip)"),
   A("PID1..PID4 definitions in the Skill are correct and reproducible", True, "43.6/46.4/45.8/45.0 == EMBOSS 65/149 and pwalign::pid; PID2 highest"),
   A("NUC.4.4 IUPAC statements are correct (partial-match codes score +1)", True, "R/A +1, Y/G -4, N/C -2; alignment score equals hand sum of matrix cells (35.0)"),
   A("The Skill's R bullet 'pairwiseAlignment() (Biostrings)' is current for the installed Bioconductor", False, "Biostrings::pairwiseAlignment() warns 'has moved to the pwalign package'; still returns 286, and gapOpening=10 (not 11) reproduces Biopython -11/-1"),
  ]),
]

for i in inputs:
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["assertions_total"] = len(i["assertions"])
    i["total"] = i["basic"] + i["specialized"]
    i["status_flag"] = "✅" if (i["status"] == "COMPLETED" and i["total"] >= 75) else ("⚠️" if i["status"] == "COMPLETED" else "❌")
    # a PARTIAL status forces the cross flag per schema
    if i["status"] == "PARTIAL": i["status_flag"] = "❌"

exec_avg = round(statistics.mean(i["total"] for i in inputs), 1)
cats = {
 "functional_suitability": (9, 12, "Core operations verified correct against 4 independent tools; but false default-gap claim, non-existent aligner.max_alignments, BLASTP off-by-one mapping, off-by-one output example, and no strand/off-spec-input guidance."),
 "reliability": (7, 12, "Version-drift fallback ('introspect and adapt') is documented; Common Errors table has 3 rows, one with a broken remedy; lowercase/U/empty-sequence ValueErrors and missing-file handling in alignment_from_file.py are not covered; scoring is deterministic and stateless."),
 "performance_context": (5, 8, "402-line SKILL.md loads the library table, significance theory and BLAST flags upfront with no references/ split; workflow itself is linear with a score-only fast path."),
 "agent_usability": (12, 16, "Goal/Approach pairs and copy-pasteable snippets are clear (13/14 blocks ran); strong pitfall list (gap defaults, PID definitions, NUC.4.4, global-vs-local); some snippets under-specified (semiglobal argument order, affine-vs-linear example shows identical scores)."),
 "human_usability": (5, 8, "Description matches natural requests ('align two sequences') but omits Needleman-Wunsch/Smith-Waterman/percent-identity trigger words; input requirements (uppercase alphabet, no whitespace) are not documented and errors do not name the offending letter."),
 "security": (11, 12, "No credentials, network calls, eval/exec or shell-out anywhere in SKILL.md, usage-guide.md or examples; local computation only; input file path is used as given."),
 "maintainability": (9, 12, "One dense SKILL.md plus usage-guide and 5 single-purpose examples; version-specific facts scattered through the file; examples have no expected outputs or asserts and alignment_from_file.py depends on an unshipped sequences.fasta."),
 "agent_specific": (18, 20, "Escape hatches are the strongest part (identity-based 'when NOT appropriate' table, routing to MMseqs2/jackhmmer/structural-alignment, related skills all exist); deterministic and idempotent; SKILL.md is under 500 lines but stat theory could live in references/."),
}
sub = sum(v[0] for v in cats.values())
static_w = round(sub * 0.4, 1); dyn_w = round(exec_avg * 0.6, 1)
score = round(static_w + dyn_w)
assert 75 <= score <= 84

report = {
 "source": "mrsonord2240/bioSkills@354b4992cd8d2f1bee039510af618da0333821f1:alignment/pairwise-alignment",
 "meta": {
  "skill_name": "bio-alignment-pairwise",
  "description": "Perform pairwise sequence alignment using Biopython Bio.Align.PairwiseAligner. Use when comparing two sequences, finding optimal alignments, scoring similarity, and identifying local or global matches between DNA, RNA, or protein sequences.",
  "evaluated_on": "2026-09-19",
  "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis",
  "execution_mode": "A",
  "complexity": "Complex",
  "n_inputs": 7,
  "executed_inputs": "7/7",
  "environment": "Windows venv Biopython 1.88, parasail 1.3.4, edlib 1.3.9; WSL env alignment (EMBOSS 6.6.0, BLAST+, MMseqs2 18.8cc5c, pywfa 0.5.1, mappy 2.31); R 4.4.3 Biostrings 2.74.1 + pwalign 1.2.0 via r.sh",
  "execution_note": "All 7 inputs executed with printed, asserted checks against independent ground truth (own Gotoh DP, parasail, EMBOSS needle/water, BLASTP, MMseqs2, pwalign, edlib, planted coordinates). Not executed: ushuffle dinucleotide shuffle and HHsearch/jackhmmer (named in prose only)."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {
   "applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated numbers; Karlin-Altschul lambda/K, PID definitions and NUC.4.4 values verified by run; Kallenborn 2025 and Marco-Sola 2021/2023 citations confirmed to exist via Crossref."},
   "practice_boundaries": {"result": "PASS", "detail": "Sequence-alignment tooling only; no diagnostic or prescriptive content in any of the 7 outputs."},
   "methodological_ground": {"result": "PASS", "detail": "Skill states alignment is not proof of homology and gives shuffle-null / E-value guidance; empirical null lambda 0.262 matched NCBI 0.267. Factual slips (default gaps, BLASTP mapping) do not invert any conclusion."},
   "code_usability": {"result": "PASS", "detail": "13/14 SKILL.md python blocks and 4/5 examples run as shipped (alignment_from_file.py needs the user's FASTA); the one failing line (aligner.max_alignments -> AttributeError) sits under the Skill's own 'introspect and adapt on AttributeError' instruction, so it is P1, not a veto."}
  }
 },
 "static_score": {
  "subtotal": sub, "max": 100,
  "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in cats.items()}
 },
 "dynamic_score": {
  "execution_avg": exec_avg, "max": 100,
  "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)},
  "inputs": [{k: i[k] for k in ("index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions", "executed", "execution_note")} for i in inputs]
 },
 "final": {
  "static_weighted": static_w, "dynamic_weighted": dyn_w, "score": score, "max": 100,
  "grade": "Limited Release", "grade_symbol": "✅", "deployable": True, "veto_override": False
 },
 "key_strengths": [
  "Core alignment guidance is numerically correct: global/local scores, coordinates, counts() and PID definitions matched an independent DP, parasail, EMBOSS needle/water, MMseqs2 and R pwalign on real globins and on planted synthetic data.",
  "Unusually strong escape hatches: identity-banded 'when alignment is NOT appropriate' table, MMseqs2/jackhmmer/Foldseek routing and an empirical shuffle-null example whose fitted lambda (0.262) matches NCBI (0.267).",
  "Explicit pitfall coverage (explicit gap penalties, PID denominators, NUC.4.4 partial IUPAC scoring, semiglobal end-gap modes) plus deprecation status of pairwise2 that proved accurate.",
  "No security surface: no network, credentials, eval or shell-out; deterministic and seeded."
 ],
 "recommendations": [
  {"priority": "P1", "title": "aligner.max_alignments does not exist in Biopython 1.88", "observed_in": [7],
   "problem": "SKILL.md ('Iterating Over Multiple Alignments' and Common Errors table) and usage-guide.md tell the agent to set aligner.max_alignments; it raises AttributeError. The first snippet's len(alignments) also raises OverflowError on repetitive input, and the table's remedy is the broken attribute.",
   "root_cause": "The attribute was dropped from PairwiseAligner in the lazy-alignments API and the file was not re-verified against current Biopython despite the '1.83+' banner.",
   "fix": "Replace with itertools.islice(alignments, n) or the existing lazy enumerate/break loop, wrap len(alignments) in try/except OverflowError, and drop max_alignments from the error table and usage-guide."},
  {"priority": "P1", "title": "'Default gap penalties are 0' is false on Biopython 1.88", "observed_in": [3],
   "problem": "PairwiseAligner() defaults are open_gap_score = extend_gap_score = -1.0 (printed), not 0; the section's claim that BLOSUM62 with defaults gives 'gaps cost nothing' is wrong (defaults still give a gappy 40-segment alignment, but for a different reason).",
   "root_cause": "Statement was written against older Biopython and not re-checked.",
   "fix": "Rewrite the section: state the installed defaults (print(aligner)), keep the advice to always set gaps explicitly, and tag the version where defaults changed."},
  {"priority": "P1", "title": "'BLASTP defaults open=-11, extend=-1' is off by one for Biopython", "observed_in": [1],
   "problem": "In Biopython/EMBOSS a gap of length k costs open+(k-1)*extend, in BLAST/Biostrings open+k*extend. Biopython -11/-1 reproduces EMBOSS 11/1 (288) not BLASTP (285); BLASTP 11/1 needs -12/-1, verified by raw score and HSP coordinates. The 'Protein Alignment' config is presented as the BLASTP default.",
   "root_cause": "Gap-cost convention of BLAST vs Biopython not distinguished.",
   "fix": "State the two conventions, say Biopython -12/-1 reproduces BLASTP 11/1 and Biostrings gapOpening=10/gapExtension=1 reproduces Biopython -11/-1, and correct the 'BLASTP defaults' wording."},
  {"priority": "P2", "title": "'Alignment Output Format' block is wrong", "observed_in": [1],
   "problem": "The illustrative match line shows '|||||.||||.||' but the real output for the same sequences is '||||.|||||.||' (mismatch at index 4, not 5).",
   "root_cause": "Hand-typed output.", "fix": "Paste the printed output of the snippet."},
  {"priority": "P2", "title": "Semiglobal snippet omits argument order and uses deprecated names", "observed_in": [3],
   "problem": "'query_*_open_gap_score' works only when the fragment is the SECOND argument (align(reference, fragment)); swapped order scored -279 instead of 40. On 1.88 the four attribute names emit BiopythonDeprecationWarning (renamed open_left_deletion_score etc.); the snippet also never sets scoring.",
   "root_cause": "Snippet is schematic.", "fix": "Give a complete runnable example with explicit scores and the target/query roles, and mention end_gap_score first (it is order-independent)."},
  {"priority": "P2", "title": "No guidance on off-spec input", "observed_in": [3, 6],
   "problem": "Lowercase sequences, U in NUC.4.4, J/U residues, empty sequences and trailing whitespace raise ValueError; a SeqRecord is silently accepted; reverse-complement queries score 34.5 vs 268.0 with no strand advice; CDS with internal stops (rabbit HBB2) is not flagged.",
   "root_cause": "Skill covers scoring theory but not input hygiene.", "fix": "Add a short 'Input checks' list: uppercase, strip, alphabet, non-empty, strand, internal-stop check."},
  {"priority": "P2", "title": "parasail/edlib claims lack code, saturation warning and realistic speed figures", "observed_in": [5],
   "problem": "Table gives no runnable parasail/edlib/pywfa/mappy snippet; parasail 16-bit variants return 0 (saturated) on 20 kb pairs; measured speedups on 300-nt pairs are 5-11x (parasail) and 15-39x (edlib) versus the tabulated 10-100x and 100-1000x.",
   "root_cause": "Table copied from literature, not measured.", "fix": "Add one verified snippet per library with the 32-bit or sat variant and a saturated-flag check, and cite the size at which each ratio was measured."},
  {"priority": "P2", "title": "R bullet out of date and gap convention not mapped", "observed_in": [7],
   "problem": "Biostrings::pairwiseAlignment() warns it moved to pwalign in Bioconductor 3.20; gapOpening semantics differ from Biopython by one.",
   "root_cause": "Single unversioned bullet.", "fix": "Say pwalign::pairwiseAlignment and give the parameter mapping."},
  {"priority": "P2", "title": "alignment_from_file.py and affine-vs-linear example are not self-demonstrating", "observed_in": [1],
   "problem": "alignment_from_file.py crashes with FileNotFoundError because sequences.fasta is not shipped; global_alignment.py's 'affine vs linear' comparison prints 108.0 vs 108.0 because the alignment is gap-free.",
   "root_cause": "Examples not run end-to-end after writing.", "fix": "Ship a tiny sequences.fasta (or take argv) and use a pair with an indel in the affine-vs-linear demo."}
 ]
}

# ---- Pre-Emit Checklist ----
assert set(report["static_score"]["categories"]) == {"functional_suitability", "reliability", "performance_context", "agent_usability", "human_usability", "security", "maintainability", "agent_specific"}
assert report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values())
assert all(0 <= c["score"] <= c["max"] for c in report["static_score"]["categories"].values())
assert len(inputs) == report["meta"]["n_inputs"] == 7
for i in report["dynamic_score"]["inputs"]:
    assert 3 <= len(i["assertions"]) <= 5, i["index"]
    assert i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and 0 <= i["basic"] <= 40 and 0 <= i["specialized"] <= 60
assert 2 <= len(report["key_strengths"]) <= 5
order = {"P0": 0, "P1": 1, "P2": 2}
assert [order[r["priority"]] for r in report["recommendations"]] == sorted(order[r["priority"]] for r in report["recommendations"])
assert report["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in inputs) / 7, 1)
print("static", sub, "exec_avg", exec_avg, "static_w", static_w, "dyn_w", dyn_w, "score", score)
l1 = statistics.mean(i["basic"] for i in inputs); l2 = statistics.mean(i["specialized"] for i in inputs)
p = report["dynamic_score"]["assertion_pass_rate"]
print("L1 avg", round(l1, 1), "L2 avg", round(l2, 1), "assertions", p, round(100 * p["passed"] / p["total"], 1), "%")
json.dump(report, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("written", OUT)

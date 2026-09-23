"""Builds eval_report_bio-alignment-pairwise_result.json and eval_viewer_bio-alignment-pairwise.md from the scored data below
(every number in the assertions is copied from run\\logs\\*.txt). Also runs the schema pre-emit checklist."""
import json, os, statistics
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "mrsonord2240/bioSkills@9c811aed171970a7188fa0a62396373dfd9a428d:alignment/pairwise-alignment"
P, Fl = "PASS", "FAIL"

static = {
    "functional_suitability": (10, 12, "Every operation the guide teaches was executed and matched independent ground truth (own Gotoh, EMBOSS needle/water, BLAST+ 2.17, parasail, edlib, pywfa, mappy, pwalign): scores, coordinates, gap convention, semiglobal, input checks, saturation. Completeness gap: PAL2NAL, MMseqs2, needle/water, HHsearch are named without command lines; DNA dinucleotide shuffle points to ushuffle with no code. One sequence-specific number ('reverse complement 0') and the 'edlib returns edit distance only' wording are imprecise."),
    "reliability": (9, 12, "Version-drift fallback ('introspect and adapt') kept; new Input Checks section documents ValueError cases (lowercase, newline, J/U, empty), silent acceptances (*, X/B/Z, SeqRecord), strand and internal-stop traps, all reproduced. Biopython's ValueError does not name the offending letter; alignment_from_file.py still has no missing-file handling."),
    "performance_context": (5, 8, "SKILL.md grew from 402 to 449 lines (28 KB) with no references/ split; library table, gap-convention table, significance theory and BLAST flags all load up front. The workflow itself is linear with a score-only fast path."),
    "agent_usability": (14, 16, "Goal/Approach pairs with copy-pasteable snippets; 16/16 python blocks run in one namespace in WSL (15/16 on Windows, the pywfa/mappy block is Linux-only as the Skill says). Expected values sit in the snippets' comments (score 40, span [[300, 320]]) and all reproduce. Strong pitfall coverage: gap defaults, BLAST vs EMBOSS convention, argument order, saturation, off-spec input. Minor: snippets use undefined user variables (query, target, reference) without saying so; -10/-0.5 vs -11/-1 conventions coexist."),
    "human_usability": (6, 8, "Description matches natural requests but omits Needleman-Wunsch, Smith-Waterman, percent identity, semiglobal and needle/water trigger words. Input requirements are now explicit in Input Checks (uppercase alphabet, no whitespace, no empty sequence)."),
    "security": (11, 12, "No credentials, network calls, eval/exec/subprocess anywhere in SKILL.md, usage-guide.md or examples (grep clean); local computation only; the example takes a user-supplied FASTA path as given."),
    "maintainability": (9, 12, "One dense SKILL.md, a slimmed usage-guide.md that points at it (dedup verified: every removed item is still in SKILL.md), five single-purpose examples that all run from a copy (alignment_from_file.py now takes argv and ships sequences.fasta). Version-specific facts are still scattered through one file; examples print no expected values."),
    "agent_specific": (18, 20, "Escape hatches are the strongest part (identity-based 'when NOT appropriate' table, routing to MMseqs2/jackhmmer/Foldseek; all 7 Related Skills exist in the repo); deterministic and idempotent; every file the guide points at exists. Statistical theory and library routing could live in references/."),
}

inputs = [
 dict(type="Canonical", label="[regression] Global BLOSUM62 alignment of real human HBA vs HBB with the Skill's gap-convention section", basic=36, spec=55,
      note="Executed 100% (run/input1*.py, input1_emboss_blast.sh, input1c_blast_default.sh, input7_R_biostrings.R). Every score matched three independent tools.",
      code="input1_real_global.py, input1b_blast_equiv.py, input1d_global_conv.py, input1_emboss_blast.sh, input1c_blast_default.sh, input7_R_biostrings.R",
      prompt="Globally align human hemoglobin alpha (P69905) and beta (P68871) with BLOSUM62 and give me the score and percent identity. I will also compare against BLASTP, EMBOSS and R.",
      output="global BLOSUM62 -11/-1: Biopython 286.0 == own Gotoh 286.0 == parasail 286 == needle 11/1 286.0; -10/-0.5: 292.5 == Gotoh == needle 292.5; re-score of returned strings == reported score; counts 65/75/9\nlocal -12/-1 = 285.0 with HSP q3-141 s4-146 == blastp -gapopen 11 -gapextend 1 -comp_based_stats 0 raw 285 (same HSP); local -11/-1 = 288.0 == water 11/1 288; blastp default (comp-based stats on) reports 286\nR: Biostrings::pairwiseAlignment warns 'has moved to the pwalign package'; pwalign global 10/1 = 286, local 11/1 = 285, local 10/1 = 288, global 11/1 = 282 (= Biopython global -12/-1)\nPairwiseAligner() defaults (1, 0, -1, -1); with BLOSUM62 defaults: 55 gap positions in 37 blocks vs 9 in 5 at -11/-1",
      assertions=[
        (P, "Global scores equal independent ground truth: -11/-1 = 286 (own Gotoh, parasail, needle 11/1) and -10/-0.5 = 292.5 (Gotoh, needle)", "all four tools agree; re-scoring the returned alignment strings gives the reported score"),
        (P, "The Skill's BLASTP mapping holds: Biopython -12/-1 local = blastp raw 285 with the identical HSP; -11/-1 = water 11/1 = 288", "blastp -comp_based_stats 0 raw 285, HSP 3-141 / 4-146; water 288 (11/1) and 285 (12/1)"),
        (P, "pwalign gap convention in the Skill is right (gapOpening = BLAST gapopen; global 10/1 = 286, local 11/1 = 285)", "R via r.sh; Biostrings warning text matches the Skill's 'still works but warns'"),
        (P, "PairwiseAligner() defaults and the '55 gap positions in 37 blocks vs 9 in 5' claim reproduce", "(1.0, 0.0, -1.0, -1.0); (55, 37, 9, 5)"),
        (P, "counts() recipe and percent-identity caveat are correct", "identities/mismatches/gaps 65/75/9 == manual recount; PID1 43.6 (needle) vs PID2 46.4, and the Skill says the recipe is 'similar to PID2'")]),
 dict(type="Variant A", label="[regression] Local DNA alignment of a mutated real HBB segment inside a 1.15 kb synthetic sequence, plus strand recovery", basic=35, spec=54,
      note="Executed 100% (input2_local_dna.py). Flanks SYNTHETIC (seed 7); the 150-nt segment is real NM_000518.5 with 5 planted substitutions and a 3-nt deletion.",
      code="input2_local_dna.py",
      prompt="Find where this 147-nt HBB fragment sits in my 1.15 kb sequence (local DNA alignment). The read might be on the other strand.",
      output="local 2/-1 open -10/-0.5: score 268.0 == own Gotoh 268.0 == hand sum 142*2 - 5 - (10 + 0.5*2); aligned target [[600,685],[688,750]] (planted 600..750); counts 142/5/3; parasail sw 10/1 267 == Biopython 267\nreverse-complemented read: forward 268.0 vs reverse complement 34.5; the Skill's recipe (score seq and its reverse complement, keep the higher) recovers 268.0 from the flipped read\nshipped local_alignment.py example: 26.0, [[5, 18]]",
      assertions=[
        (P, "Local score equals independent Gotoh DP and the hand-derived planted-alignment score (268)", "268.0 == 268.0 == 142*2 - 5 - 11"),
        (P, "Aligned span and counts match the planted segment", "target 600..750; identities 142, mismatches 5, gaps 3"),
        (P, "Biopython local 10/1 equals parasail sw_scan 10/1", "267.0 vs 267"),
        (P, "The Skill's strand recipe works on a flipped read", "revcomp 34.5 vs forward 268.0; best-of-both recovers 268.0")]),
 dict(type="Edge", label="[regression] Semiglobal fragment placement, length mismatch, and every 'Input Checks' bullet", basic=35, spec=53,
      note="Executed 100% (input3_edge_semiglobal.py). Reference SYNTHETIC (seed 11); CDS data real. One assertion fails: the '30-nt exact match 60, reverse complement 0' numbers.",
      code="input3_edge_semiglobal.py",
      prompt="Align this 20-nt primer inside a 620-nt template without penalising the flanks; also my lowercase protein, an RNA read, an empty record, a SeqRecord, and a rabbit CDS that may have a stop.",
      output="snippet 1 (end_gap_score=0): 40.0, target [[300,320]], order-independent; snippet 2 (open/extend_left/right_deletion_score, warnings as errors): 40.0, [[300,320]]; align(fragment, reference) = -279.0; mutated fragment 25.0 == independent semiglobal DP 25\nglobal -279.0 | local 40.0 | semiglobal 40.0\nValueError 'sequence contains letters not in the alphabet' for lowercase, trailing newline, J, U (and NUC.4.4 + U); empty -> 'sequence has zero length'; '*', X/B/Z, SeqRecord accepted (SeqRecord scores 286.0 = its .seq); match/mismatch aligner: 'acgt' vs 'ACGT' = -4\n50 random 30-mers, local 2/-1: forward always 60.0; reverse complement median 17.5, max 29.0 (Skill: 'reverse complement 0')\ninternal-stop expression flags only NM_001314043.1 of 7 real CDS; old query_* names accepted with DeprecationWarning, same score",
      assertions=[
        (P, "Both semiglobal snippets run as written (warnings as errors) and give 40.0 / [[300, 320]]; swapped order gives the -279 the Skill quotes", "mutated fragment 25.0 == independent semiglobal DP"),
        (P, "Every Input Checks ValueError / silent-accept bullet reproduces on Biopython 1.88", "lowercase, newline, J, U, NUC.4.4+U, empty; *, XBZ, SeqRecord accepted; match/mismatch aligner four mismatches"),
        (P, "The internal-stop expression flags NM_001314043.1 and none of the six clean CDS", "1 of 7 flagged"),
        (P, "The deprecated query_left/right_* names are accepted with a DeprecationWarning and give the same result", "score 40.0; 'was renamed' warning"),
        (Fl, "The strand bullet's numbers reproduce ('30-nt exact match scored 60, reverse complement 0')", "60 reproduces; reverse complement does not score 0 in local mode (median 17.5, max 29 over 50 random 30-mers). Qualitatively right (strand-specific), number sequence-specific")]),
 dict(type="Variant B", label="[regression] Is HBA/HBB significant? Empirical p-values with the Skill's own example on related, distant and unrelated real pairs", basic=35, spec=53,
      note="Executed 100% (input4_significance.py imports a copy of examples/empirical_pvalue.py). ushuffle (DNA dinucleotide shuffle named by the Skill) not executed: pip build fails on Windows and in WSL.",
      code="input4_significance.py, ushuffle_attempt.sh",
      prompt="Is the HBA/HBB alignment significant? Compare it with myoglobin and with a kinase.",
      output="HBA vs HBB: local raw 288, K-A bits 115.5, empirical p 0.0010 (floor 1/1001), null mean 28.9 max 51\nMYG_HUMAN vs HBB: raw 111, bits 47.4, p 0.0010 (global pid2 26.0%)\nPKA 1ATP vs HBB: raw 33, bits 17.3, p 0.2478 (global pid2 29.0%, identity alone misleading)\nseed=42 rerun identical for all three; Gumbel fit of the null lambda 0.262 vs NCBI 0.267; demo pair p 0.1449; preserve='di' -> NotImplementedError 'Use the ushuffle library'",
      assertions=[
        (P, "Skill's empirical_pvalue.py is deterministic (identical p and null on rerun, seed 42)", "3 of 3 pairs identical"),
        (P, "Results fall in the Skill's bit-score bands: related 115 bits likely homology, distant 47 possible, unrelated 17 not significant (p 0.248)", "p 0.001 / 0.001 / 0.248"),
        (P, "Karlin-Altschul bits agree with BLASTP and the shuffled null agrees with NCBI lambda", "115.5 bits vs blastp 114; lambda 0.262 vs 0.267"),
        (P, "The DNA path is honest: preserve='di' refuses and points to ushuffle rather than faking a dinucleotide shuffle", "NotImplementedError raised")]),
 dict(type="Stress", label="[regression] Library-selection table re-measured: parasail, edlib, pywfa, mappy on long synthetic DNA, saturation, every Skill snippet", basic=36, spec=54,
      note="Executed 100% on Windows (parasail, edlib) and WSL (all four, plus the SKILL.md extraction harness). All DNA SYNTHETIC (seeds 4/5/9/3/21) except the real HBB CDS used by the harness.",
      code="input5_libs.py, snippets_harness.py, edlib_path_check.py",
      prompt="Score 1000 read pairs and one 20 kb pair; which library should I use? Show me code for parasail, edlib, pywfa and mappy.",
      output="parasail nw_striped_sat 7003 == Biopython 7003 (4 kb, 118 injected edits); sw_striped_sat 7006 == 7006; edlib NW 118 == -Levenshtein 118; edlib HW 2 == Biopython free-target-end Levenshtein 2; edlib protein 15 == 15\nWSL: pywfa -802 == Biopython gap-affine -802; mappy locus 3500..4500 mapq 60 (planted 3500)\n1000 pairs: Biopython == parasail striped_sat == scan_sat 1000/1000; Levenshtein == -edlib 1000/1000\n300 nt x1000 (Windows): parasail striped 1.7x, scan 3.9x (Skill 2-10x); edlib 14x vs Levenshtein, 27x vs affine (Skill 15x / 26x). WSL: 2.6-4.9x, 15x / 36x\n20 kb (Windows): parasail 2.4x (WSL 3.7-4x) (Skill 3-8x), edlib 437x (WSL 808-822x) (Skill 400x+); nw_striped_16 returns 0 with saturated=True (true 35644), _sat variant 35644\nSKILL.md harness: WSL 16/16 blocks OK with DeprecationWarning promoted to error, all six snippet assertions pass; Windows 15/16 (pywfa/mappy block, no Windows build, as the Skill states)",
      assertions=[
        (P, "Every Verified snippet reproduces its own comment: parasail == Biopython, edlib == -Levenshtein, pywfa == Biopython gap-affine, mappy hits the planted locus", "harness 6/6 assertions PASS in WSL"),
        (P, "Cross-library agreement at scale: 1000/1000 pairs for parasail and edlib", "1000 == 1000"),
        (P, "Measured speed ranges hold within run-to-run variation (parasail 1.7-3.9x at 300 nt, edlib 14-27x, 20 kb edlib 437x)", "Windows and WSL, min of 3 runs"),
        (P, "The saturation warning is real: fixed-width nw_striped_16 silently returns 0 on a 20 kb pair; the _sat variant is correct", "0 with saturated=True vs 35644"),
        (P, "edlib alphabet and mode claims: works on protein; HW mode = query anywhere in target", "15 == 15; HW 2 == 2")]),
 dict(type="Scope Boundary", label="[regression] Human vs cow HBB CDS for dN/dS (protein first, back-translate), the internal-stop trap, and a many-vs-many request", basic=33, spec=48,
      note="Executed 100% (input6_scope.py, input6_pal2nal.py, input6_pal2nal_mafft.py, input6_mmseqs.sh). Real RefSeq CDS and UniProt. The Skill names PAL2NAL and MMseqs2 but ships no command, so the auditor wrote both.",
      code="input6_scope.py, input6_pal2nal.py, input6_pal2nal_mafft.py, input6_mmseqs.sh",
      prompt="Align human and cow HBB coding sequences for a dN/dS analysis, include the rabbit HBB2 record, and separately align one query against a whole database.",
      output="human/cow nucleotide pid2 87.0% (gaps 6) vs protein 84.8% (gaps 2); protein-guided codon alignment 441 columns, human row re-translates to the protein row; 46 of 147 codons differ\nPAL2NAL 14: human+cow -> 2 records (910 B); after MAFFT protein alignment of human+cow+rabbit(NM_001314043.1) pal2nal exits 0 with EMPTY output and '#--- ERROR: inconsistency between the following pep and nuc seqs' (also with stop->X); control without rabbit -> 2 records\n(a hand-built pairwise protein alignment that keeps '*' does not fail: the trap needs the MAFFT route, which strips '*')\nMMseqs2 easy-search all-vs-all on 8 globins: 54 rows; HBA->HBB raw 280, bits 115, pident 43.4, E 3e-34",
      assertions=[
        (P, "DNA-vs-protein routing is right on real orthologs (nucleotide identity 87% > 70% -> DNA is fine) and protein-first back-translation is frame-consistent", "441 codon columns; re-translation equals the protein row"),
        (P, "The internal-stop warning is correct on the realistic MAFFT + PAL2NAL route (rabbit NM_001314043.1 gives empty output, exit 0)", "0 records vs 2 records for the control"),
        (P, "The many-vs-many route (MMseqs2) is supported by a real run and the Skill does not loop DP over a database", "54 rows; HBA->HBB bits 115"),
        (P, "Skill's escape hatch is correct: 'alignment exists' is not the homology gate, E-value/bit score is", "MMseqs2 E 3e-34 for the true homolog"),
        (Fl, "The Skill supplies runnable commands for the tools it routes to (PAL2NAL, MMseqs2, needle/water, HHsearch)", "names only, no command lines or flags; the auditor wrote all three")]),
 dict(type="Adversarial", label="[regression] pairwise2, aligner.max_alignments, EMBOSS-style percent identity, IUPAC DNA, algorithm names, R, printed output block", basic=36, spec=54,
      note="Executed 100% (input7_adversarial.py, input7_R_biostrings.R, run_examples.py). Every pre-fix defect in this input is gone.",
      code="input7_adversarial.py, input7_R_biostrings.R, run_examples.py",
      prompt="Use pairwise2, cap alignments with max_alignments, give percent identity like EMBOSS, score IUPAC DNA, tell me which algorithm Biopython picked, and do it in R.",
      output="pairwise2: DeprecationWarning, score 292.5 == PairwiseAligner 292.5\naligner.max_alignments = 100 -> AttributeError (the Skill now says so); len(alignments) with zero gap scores on repetitive input -> OverflowError; islice(alignments, 5) works\nPID1 43.6 PID2 46.4 PID3 45.8 PID4 45.0 (== needle 65/149 and pwalign pid())\nNUC.4.4 R/A +1, hand sum 35.0 == score; 30 matrices; algorithm names: exactly the six the Skill lists; printed 'Alignment Output Format' block equals real output line for line; fasta/clustal/psl/sam OK; substitutions['G','T'] == 1\nshipped examples (from the copy): alignment_from_file.py 26.0 (independent 26.0), global_alignment.py affine 86.0 vs linear 84.0, local 26.0 [[5,18]], protein 377.0, empirical_pvalue 23.0 p 0.1449; no __pycache__ written",
      assertions=[
        (P, "pairwise2 is flagged deprecated but present and agrees with PairwiseAligner", "292.5 == 292.5"),
        (P, "max_alignments handling is correct: attribute absent (AttributeError), OverflowError on len(), islice works; the guide no longer tells the agent to set it", "grep of SKILL.md and usage-guide.md clean"),
        (P, "Percent-identity definitions match EMBOSS and pwalign", "43.6 / 46.4 / 45.8 / 45.0"),
        (P, "NUC.4.4 IUPAC claims, 30-matrix listing, six algorithm names and the printed output block are accurate", "score 35.0 == hand sum; name sets equal; output block equals real output"),
        (P, "All five shipped examples run from a copy and print checked values; the affine-vs-linear demo now differs (86.0 vs 84.0)", "alignment_from_file.py 26.0 == independent 26.0")]),
 dict(type="Variant B", label="[NEW] PKA (1ATP) vs CDK2 (1HCK): distant real kinase pair, gap convention verified on a pair the fixer never used", basic=37, spec=56,
      note="Executed 100% (input8_kinase_conv.py, input8_ground_truth.sh, input8_R_pwalign.R). Real PDB SEQRES from public-data; nothing synthetic.",
      code="input8_kinase_conv.py, input8_ground_truth.sh, input8_R_pwalign.R",
      prompt="Align PKA and CDK2 with BLOSUM62 and tell me whether the alignment means anything; I want the number to match BLASTP and EMBOSS.",
      output="1ATP:E 350 aa, 1HCK:A 298 aa. Biopython vs own Gotoh: global -11/-1 124, -10/-0.5 186.5, -12/-1 110, local -11/-1 228, -12/-1 222 (all equal)\nEMBOSS: needle 11/1 124, 10/0.5 186.5, 12/1 110; water 11/1 228, 12/1 222\nblastp -gapopen 11 -gapextend 1 -comp_based_stats 0: raw 222, bits 90.1, HSP q40-244 s1-209, identical to Biopython local -12/-1 (K-A bits 90.1); blastp default (comp-based stats) 223\npwalign: global 10/1 124, local 11/1 222, local 10/1 228\nBLOSUM45/62/80 local: 317/222/380 (not comparable across matrices); global pid2 29.1% (Skill band 25-40%); empirical p at floor 0.001",
      assertions=[
        (P, "Global -11/-1 = 124 equals needle 11/1, pwalign 10/1 and an independent Gotoh; -10/-0.5 = 186.5 equals needle", "four tools agree"),
        (P, "The Skill's central fix holds on a new pair: BLASTP 11/1 = Biopython -12/-1 (local 222 = blastp raw 222, same HSP) and water 12/1 = 222", "blastp 222 q40-244 s1-209"),
        (P, "-11/-1 is EMBOSS 11/1, not BLASTP: local -11/-1 = 228 = water 11/1 = pwalign 10/1", "228 == 228 == 228"),
        (P, "pwalign conversion (gapOpening = BLAST gapopen) is right", "global 10/1 124, local 11/1 222"),
        (P, "Identity band and significance guidance fit a real distant homolog pair: pid2 29.1% (25-40% row), 90 bits 'likely homology', empirical p at the floor", "K-A bits 90.1 == blastp 90.1")]),
 dict(type="Edge", label="[NEW] Six real mammal HBB CDS: DNA global scores vs EMBOSS needle, DNA-vs-protein table, unknown-strand read placement", basic=35, spec=54,
      note="Executed 100% in WSL (input9_real_dna.py). Real RefSeq CDS; rabbit HBB2 excluded here (covered in input 6).",
      code="input9_real_dna.py",
      prompt="Score human HBB CDS against each ortholog, tell me the identity, and place a 120-nt read of unknown orientation on the human CDS.",
      output="NUC.4.4 -10/-0.5 global vs needle EDNAFULL 10/0.5 (end gaps penalised): chimp 2211.0/2211.0, cow 1666.5/1666.5, rat 1612.0/1612.0, 2060.0/2060.0, 1673.0/1673.0; own Gotoh (human vs cow) 1666.5\nnucleotide PID1 99.8, 85.3, 85.2, 96.2, 86.9 (all > 70) vs protein PID1 100.0, 83.7, 85.0, 94.6, 83.7\nflipped cow 120-nt segment: as given 28.5, reverse complement 183.0 == un-flipped 183.0; placed at human 126..246; edlib HW same locus (126..245, distance 19)",
      assertions=[
        (P, "NUC.4.4 global -10/-0.5 equals EMBOSS needle EDNAFULL 10/0.5 on all five ortholog pairs and an independent Gotoh DP", "5/5 equal"),
        (P, "The Skill's DNA-vs-protein table fits real orthologs (all nucleotide identities > 70%)", "min 85.2%"),
        (P, "The Skill's strand recipe (score seq and its reverse complement, keep the higher) reproduces the un-flipped score and locus", "183.0 == 183.0; 126..246"),
        (P, "The wrong orientation scores far lower and edlib HW independently finds the same locus", "28.5 vs 183.0; edlib 126..245")]),
]
for i, x in enumerate(inputs, 1):
    x["index"] = i; x["total"] = x["basic"] + x["spec"]
    assert 3 <= len(x["assertions"]) <= 5

sub = sum(v[0] for v in static.values())
avg = round(statistics.mean(x["total"] for x in inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = int(round(sw + dw))
apass = sum(a[0] == P for x in inputs for a in x["assertions"]); atotal = sum(len(x["assertions"]) for x in inputs)
l1 = statistics.mean(x["basic"] for x in inputs); l2 = statistics.mean(x["spec"] for x in inputs)
floors = dict(static=sub >= 80, exec=avg >= 85, l1=l1 >= 32, l2=l2 >= 48, assertions=apass / atotal >= 0.90)
grade, sym = ("Production Ready", "\u2b50") if score >= 85 and all(floors.values()) else (("Limited Release", "\u2705") if score >= 75 else ("Beta Only", "\u26a0\ufe0f"))
print("static", sub, "exec avg", avg, "score", score, grade, "assertions", apass, atotal, "L1", round(l1, 1), "L2", round(l2, 1), floors)

recs = [
 ("P2", "SKILL.md is 449 lines / 28 KB with no references/ split", [], "The guide grew from 402 to 449 lines; the gap-convention table, library table, significance theory and BLAST flags all load up front.", "All depth lives in one file and the fix added content to it.", "Move Statistical Significance, Pairwise Library Selection and When Alignment Is NOT Appropriate into references/ files loaded on demand; keep the aligner recipes and gap-convention table in SKILL.md."),
 ("P2", "Routed-to tools are named without command lines", [4, 6], "PAL2NAL, MMseqs2 (easy-search / --num-iterations), EMBOSS needle/water and HHsearch are named but no flags or invocations are shown, and the DNA dinucleotide shuffle points at ushuffle with no code (ushuffle failed to build via pip on Windows and in WSL here).", "The guide documents the Python path in depth and treats the CLI/R paths as one-line pointers.", "Add a short CLI block: `needle -gapopen 11 -gapextend 1 ...`, `water ...`, `mmseqs easy-search ...`, `pal2nal.pl prot.aln nuc.fa -output fasta`, with a note that pal2nal exits 0 with empty output on inconsistent input; say how to install ushuffle or give a short dinucleotide-shuffle function."),
 ("P2", "Strand bullet quotes a sequence-specific number", [3], "'a 30-nt exact match scored 60, reverse complement 0' reproduces the 60 but not the 0: over 50 random 30-mers the local score of the reverse complement had median 17.5 and max 29.", "A single example sequence was generalised.", "Say 'the reverse complement scores far lower (typically under half)'; keep the score-both-strands recipe, which was verified."),
 ("P2", "'edlib returns edit distance only' is misleading", [5], "edlib.align(..., task='path') returns a CIGAR and alignment (verified); its scoring is unit-cost edit distance, which is what the sentence means.", "Wording conflates the scoring model with the output.", "Reword to 'unit-cost edit distance scoring only (no matrix, no affine gaps); task=\"path\" returns the alignment'."),
 ("P2", "Description omits common trigger phrases", [], "The description says 'pairwise sequence alignment' but not Needleman-Wunsch, Smith-Waterman, semiglobal, percent identity, needle/water, or 'reverse complement'.", "Description was not touched by the fix.", "Add those terms to the frontmatter description."),
]

report = {
 "meta": {
  "skill_name": "bio-alignment-pairwise",
  "description": "Perform pairwise sequence alignment using Biopython Bio.Align.PairwiseAligner. Use when comparing two sequences, finding optimal alignments, scoring similarity, and identifying local or global matches between DNA, RNA, or protein sequences.",
  "evaluated_on": "2026-09-19", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "A", "complexity": "Complex", "n_inputs": len(inputs),
  "source": SRC, "reaudit_of": "F:\\OpenScience\\audits\\_pre-fix-20260919d\\bio-alignment-pairwise (80, Limited Release)",
  "fix_log": "F:\\optimizing-agent-science-skills\\fixes\\bio-alignment-pairwise.md (read; not used as evidence)",
  "executed_inputs": f"{len(inputs)}/{len(inputs)}",
  "environment": "Windows venv (Biopython 1.88, parasail 1.3.4, edlib 1.3.9); WSL env alignment (EMBOSS 6.6.0, BLAST+ 2.17.0, MMseqs2 18.8cc5c, MAFFT 7.526, PAL2NAL 14, pywfa 0.5.1, mappy 2.31, Biopython 1.88); R 4.4.3 with pwalign 1.2.0 + Biostrings 2.74.1 via r.sh",
  "execution_note": "All 9 inputs (7 regression from the pre-fix audit re-written against the fixed Skill's new claims, 2 NEW on real data the fixer did not use) executed with printed, asserted checks against independent ground truth (own Gotoh DP, EMBOSS needle/water, BLAST+ blastp, pwalign, parasail, edlib, pywfa, mappy, MMseqs2, PAL2NAL, planted coordinates). The Skill's 16 python blocks were extracted from a byte-identical copy and run in one namespace (WSL 16/16, Windows 15/16: the pywfa/mappy block is Linux-only as the Skill states). Not executed: ushuffle (pip build fails on Windows and WSL); HHsearch/jackhmmer/DIAMOND named in prose only; Kallenborn/MMseqs2-GPU claims not run (citations verified on Crossref).",
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
    "scientific_integrity": {"result": "PASS", "detail": "Benchmark numbers were re-measured (parasail 1.7-5x, edlib 14-40x at 300 nt; 20 kb 2-4x and 437-822x) and the saturation example reproduces; all nine References resolve on Crossref; no fabricated scores or statistics in any output."},
    "practice_boundaries": {"result": "PASS", "detail": "Sequence-comparison guidance only; no diagnostic or prescriptive content in any of the 9 inputs."},
    "methodological_ground": {"result": "PASS", "detail": "Gap-convention mapping, significance bands, DNA-vs-protein routing, semiglobal usage and the 'alignment exists is not homology' warning are all correct; every Skill claim I tested against independent tools held except one sequence-specific number (P2)."},
    "code_usability": {"result": "PASS", "detail": "16/16 SKILL.md python blocks run in WSL with DeprecationWarning promoted to error (15/16 on Windows; the failing block is the Linux-only pywfa/mappy one, stated in the Skill); 5/5 shipped examples run from a copy; every snippet's own comment assertion reproduced."}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": apass, "total": atotal}, "inputs": [
   {"index": x["index"], "type": x["type"], "label": x["label"], "status": "COMPLETED", "status_flag": "\u2705" if x["total"] >= 75 else "\u26a0\ufe0f",
    "note": x["note"], "executed": True, "execution_note": x["note"], "basic": x["basic"], "specialized": x["spec"], "total": x["total"],
    "assertions_passed": sum(a[0] == P for a in x["assertions"]), "assertions_total": len(x["assertions"]),
    "assertions": [{"text": a[1], "result": a[0], "note": a[2]} for a in x["assertions"]]} for x in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": True, "veto_override": False},
 "key_strengths": [
   "Every headline fix reproduces against independent tools on two different protein pairs: BLASTP 11/1 = Biopython -12/-1 (blastp raw 285 and 222, identical HSPs), -11/-1 = EMBOSS 11/1, pwalign gapOpening = BLAST gapopen",
   "New Verified snippets for parasail, edlib, pywfa and mappy all reproduce their own comments; the 16-bit saturation trap is real and correctly warned about",
   "Input Checks section is accurate line by line (ValueErrors, silent accepts, strand, internal-stop CDS that really does make PAL2NAL return empty output via MAFFT)",
   "Deduplicated usage-guide.md lost nothing the agent needs; all five shipped examples run from a copy and the affine-vs-linear demo now differs",
   "Clear escape hatches: identity-band table, MMseqs2/jackhmmer/Foldseek routing, E-value as the homology gate"],
 "recommendations": [{"priority": p, "title": t, "observed_in": o, "problem": pr, "root_cause": rc, "fix": f} for (p, t, o, pr, rc, f) in recs],
}
# ---- pre-emit checklist ----
assert report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values())
for c in report["static_score"]["categories"].values(): assert 0 <= c["score"] <= c["max"]
assert len(report["dynamic_score"]["inputs"]) == report["meta"]["n_inputs"]
for i in report["dynamic_score"]["inputs"]:
    assert 3 <= len(i["assertions"]) <= 5 and i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"]) and i["basic"] + i["specialized"] == i["total"]
assert 2 <= len(report["key_strengths"]) <= 5
assert [r["priority"] for r in report["recommendations"]] == sorted(r["priority"] for r in report["recommendations"])
json.dump(report, open(os.path.join(OUT, "eval_report_bio-alignment-pairwise_result.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)

# ---- viewer ----
L = []
w = L.append
w("# Eval Viewer - bio-alignment-pairwise (re-audit of the fixed Skill)\n")
w(f"Generated: 2026-09-19 | Source: `{SRC}` | Pre-fix: 80 (Limited Release, `_pre-fix-20260919d`)")
w("Category: Data Analysis (3) | Mode: A (the agent writes code from the Skill's patterns; the 5 `examples/` are templates) | Complexity: Complex -> 7 regression inputs + 2 NEW = N 9\n")
w("The Skill was read from a byte-identical copy in `run\\skill\\` (`diff -r` against the worktree: identical; no `__pycache__` in the worktree, the clone or the copy). Every script and log is in `run\\` and `run\\logs\\`. Ground truth was independent of the Skill: an own pure-Python Gotoh DP (`ref_gotoh.py`), EMBOSS needle/water, BLAST+ blastp `-comp_based_stats 0`, pwalign (R), parasail, edlib, pywfa, mappy, MMseqs2, PAL2NAL, planted coordinates. Synthetic data is labelled SYNTHETIC in the scripts; real data is UniProt globins, RefSeq HBB CDS and PDB SEQRES from `audit-envs\\alignment\\public-data`. The fix log was read but not used as evidence.\n")
w("## Summary Table\n")
w("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for x in inputs:
    ap = sum(a[0] == P for a in x["assertions"])
    w(f"| {x['index']} | {x['type']} - {x['label']} | {x['basic']} | {x['spec']} | {x['total']} | {ap}/{len(x['assertions'])} PASS | {'OK' if x['total'] >= 75 else 'WARN'} |")
w(f"\n**Execution average: {avg} / 100** | Layer 1 avg {l1:.1f}/40 | Layer 2 avg {l2:.1f}/60 | **Assertions {apass}/{atotal} ({100*apass/atotal:.1f}%)** | **Executed 9/9**\n")
w("## Step 1 - Skill Veto: PASS")
w("T1 stability PASS (16/16 python blocks of SKILL.md run in one namespace in WSL with DeprecationWarning as error; Windows 15/16, the pywfa/mappy block is Linux-only as the Skill states; 5/5 shipped examples run from a copy). T2 contract PASS (frontmatter `name`, `description`, `tool_type`, `primary_tool`, `license`). T3 determinism PASS (aligner deterministic; `empirical_pvalue.py` seeded, identical null on rerun). T4 security PASS (grep for eval/exec/subprocess/requests/urllib/api key/token in SKILL.md, usage-guide.md, examples: none).\n")
w(f"## Step 2 - Static: {sub} / 100  (pre-fix 76)")
w("| Category | Score | Note |\n|---|---|---|")
for k, v in static.items(): w(f"| {k} | {v[0]}/{v[1]} | {v[2]} |")
w("\nShipped-means-present: every file SKILL.md/usage-guide.md points at exists (`examples/empirical_pvalue.py`, the shipped `examples/sequences.fasta`, all 7 Related Skills resolve in the repo). No `references/` folder is referenced. No P0.\n")
w("## Regression: what the pre-fix audit found, re-run on the fixed Skill\n")
w("| Pre-fix defect | Now | Evidence |\n|---|---|---|")
for a, b, c in [
 ("`aligner.max_alignments` raises AttributeError (P1)", "Fixed: Skill says the attribute does not exist; islice recipe; OverflowError explained", "input7: AttributeError, OverflowError, islice OK; grep clean"),
 ("'Default gap penalties are 0' false (P1)", "Fixed: defaults 1/0/-1/-1, fragmentation numbers reproduce (55/37 vs 9/5)", "input1"),
 ("'BLASTP defaults -11/-1' off by one (P1)", "Fixed: convention table; BLASTP = -12/-1; verified twice (HBA/HBB 285, PKA/CDK2 222) with identical HSPs", "input1, input8"),
 ("Output block wrong (P2)", "Fixed: equals real output line for line", "input7"),
 ("Semiglobal snippet order/names (P2)", "Fixed: both snippets run with warnings as errors; -279 reproduces", "input3, harness"),
 ("No off-spec input guidance (P2)", "Fixed: Input Checks section accurate bullet by bullet (one number imprecise)", "input3"),
 ("parasail/edlib table: no code, no saturation warning (P2)", "Fixed: snippets for parasail, edlib, pywfa, mappy reproduce; saturation real", "input5, harness"),
 ("R bullet outdated (P2)", "Fixed: pwalign named, gap convention mapped, numbers reproduce", "input7 R, input8 R"),
 ("alignment_from_file.py needs unshipped FASTA; affine-vs-linear demo identical (P2)", "Fixed: sequences.fasta ships, argv used; demo 86.0 vs 84.0", "run_examples.py")]:
    w(f"| {a} | {b} | {c} |")
w("\n### Independent look for defects the fix introduced")
w("- **pywfa/mappy snippets**: ran in WSL only (Skill says Windows builds failed; `pip install pywfa` has no Windows wheel per TOOLS.md). pywfa -802 == Biopython -802; mappy locus 3500 mapq 60 and 2000 mapq 60. No defect.")
w("- **Convention table** (Biopython/EMBOSS/parasail vs BLAST/pwalign): verified on two pairs by score and HSP coordinates; parasail 10/1 == Biopython -10/-1 in the harness. No defect.")
w("- **Speed numbers**: within the stated ranges except parasail striped at 1.7x on Windows (Skill '2-10x'); timings vary run to run and the Skill says so. No defect.")
w("- **usage-guide.md dedup**: read the pre-fix file; Prerequisites, agent steps, modes, all Tips (including twilight zone, PID definitions, MMseqs2/GPU, significance) are still in SKILL.md; the deleted `max_alignments` tip was wrong. Nothing the agent needs was lost.")
w("- **New nits** (P2): 'reverse complement 0' is sequence-specific; 'edlib returns edit distance only' wording; SKILL.md grew to 449 lines with no references/ split; routed-to tools have no command lines; ushuffle not installable here.\n")
w("## Detailed Outputs\n")
for x in inputs:
    w(f"### Input {x['index']} - {x['type']}: {x['label']}")
    w(f"**Prompt:** {x['prompt']}")
    w(f"**Code:** `run\\{x['code'].replace(', ', '`, `run\\')}`")
    w(f"**Executed:** true. {x['note']}")
    w("**Output (trimmed):**\n```\n" + x["output"] + "\n```")
    w(f"**Scores:** Basic {x['basic']}/40 | Specialized {x['spec']}/60 | Total {x['total']}/100")
    w("**Assertions:**")
    for a in x["assertions"]: w(f"- [{a[0]}] {a[1]} - {a[2]}")
    w("")
w("## Research Veto: PASS (M1 PASS, M2 PASS, M3 PASS, M4 PASS)\n")
w("## Step 8 - Final")
w(f"Static {sub} x 0.4 = {sw}; Execution {avg} x 0.6 = {dw}; **Final {score} - {grade}, deployable, no veto, no open P0/P1.**")
w(f"Floors for Production Ready: static {sub} >= 80, exec {avg} >= 85, L1 {l1:.1f} >= 32, L2 {l2:.1f} >= 48, assertions {100*apass/atotal:.1f}% >= 90: all met.")
w("\n**P2**")
for i, r in enumerate(recs, 1): w(f"{i}. {r[1]}. {r[3]}")
open(os.path.join(OUT, "eval_viewer_bio-alignment-pairwise.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
print("written")

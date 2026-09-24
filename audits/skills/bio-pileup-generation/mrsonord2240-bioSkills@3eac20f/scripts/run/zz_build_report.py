#!/usr/bin/env python3
"""Builds eval_report_bio-pileup-generation_result.json and eval_viewer_bio-pileup-generation.md from the scored inputs below and the
per-check records (checks_in*.json) written by the test scripts.  Scores are the re-auditor's judgement (rubric in skill-auditor references);
the script only assembles them, recomputes every derived number, and runs the schema pre-emit checklist."""
import json, os, re, sys
RUN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(RUN)
sys.stdout.reconfigure(encoding="utf-8")

checks = {}
for n in range(1, 12):
    p = f"{RUN}/checks_in{n}.json"
    checks[n] = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else []
ck = {n: (sum(1 for c in v if c[2]), len(v)) for n, v in checks.items()}
tot_pass = sum(a for a, b in ck.values()); tot_all = sum(b for a, b in ck.values())
print("scripted checks per script-input:", ck, "total", tot_pass, "/", tot_all)

SKILL_DESC = "Generate pileup data for variant calling using samtools mpileup and pysam. Use when preparing data for variant calling, analyzing per-position read data, or calculating allele frequencies."

def A(t, ok, note):
    return {"text": t, "result": "PASS" if ok else "FAIL", "note": note}

inputs = [
 dict(index=1, type="Canonical", label="REGRESSION: text pileup of the real human chr22 BAM (region/BED/-q/-Q), columns, symbols, defaults, pysam table on real data",
      status="COMPLETED", flag="✅", basic=35, spec=54,
      note=f"script t01: {ck[1][0]}/{ck[1][1]} checks pass. Options table, depth-0 rows, MAPQ char, BAQ (40 positions default vs -B) and the pysam mapping all reproduce on real data.",
      asserts=[
        A("Output Format claims hold on real data: col4 depth == number of read symbols == length of col6; the documented row 'chr22 1952 T 0 * *' exists", True, "1157 rows decoded with an independent parser; exact row present"),
        A("pysam call with fastafile and no stepper argument equals `samtools mpileup` default (BAQ), and without fastafile equals `-B`, position by position (len(pileups))", True, "0 of 1157 positions differ for both; n (not len(pileups)) differs at 1087, as the Skill states"),
        A("Documented defaults are real: -Q 13, default --ff = UNMAP,SECONDARY,QCFAIL,DUP, overlap counted once", True, "--ff 0 raises depth sum 670999 -> 671070; named flag list == default"),
        A("mpileup -B -Q0 -q0 -x -A depth equals `samtools depth -a -J` at every position (independent tool)", True, "same positions, same max 2532"),
        A("Scope: only mpileup/pysam facts asserted; no clinical or variant-pathogenicity claim made", True, "nothing outside pileup generation")]),
 dict(index=2, type="Variant A", label="REGRESSION: pysam allele_counts / allele_frequency / find_variants / pileup_text / Access Reads on planted synthetic + real BAM, shipped example",
      status="COMPLETED", flag="✅", basic=35, spec=55,
      note=f"script t02: {ck[2][0]}/{ck[2][1]} checks pass. Access Reads snippet again prints read name, strand, base and quality; ref-skip vs deletion classification correct.",
      asserts=[
        A("allele_counts at the planted SNP synA:100 returns 30 ref + 10 alt, all Q40", True, "Access Reads snippet lists (name, strand, base, Q) for the same 40 reads"),
        A("Reference skips are not deletions: synA:400 (splice) gives 3 'Reference skip' and no 'Deletion'; the true deletion synA:251 still reports 4 'Deletion'", True, "is_refskip tested first"),
        A("pileup_text equals `samtools mpileup` row for row on the synthetic truth BAM (623 rows with splice/indel/overlap/flag events) under default, -B and -q 20 -Q 20 -x -A equivalents", True, "0 differing rows; real BAMs are covered in input 5"),
        A("examples/allele_counts.py from a clean copy runs and matches mpileup -B -q20 -Q20 depth at a real position", True, "T 30 / C 10 at synA:100; contig names with ':' handled"),
        A("Errors from the shipped example are one-line messages, not tracebacks", True, "range, missing colon, unknown contig, unindexed BAM each print one 'Error:' line")]),
 dict(index=3, type="Edge", label="REGRESSION: every silent default (flags, -Q, depth 0 rows, BAQ hiding a deletion, max depth 8000) and the shipped example on hostile input",
      status="COMPLETED", flag="✅", basic=36, spec=54,
      note=f"script t03: {ck[3][0]}/{ck[3][1]} checks pass. Depth cap, flag defaults, BAQ-hidden deletion (depth 8 -> 4) and the max_depth=0 trap all reproduce.",
      asserts=[
        A("samtools -d 8000 default truncates a 9000x BAM; -d 0 and -d 1000000 restore 9000; pysam max_depth=0 is still 8000", True, "documented trap is real"),
        A("Default flag filter drops DUP/SECONDARY/QCFAIL/UNMAP: depth 10 at synA:825, 16 with --ff 0, bcftools --ns 0 DP 16", True, "table row confirmed in both tools"),
        A("BAQ hides a 3 bp deletion in a text pileup (depth 8 -> 4, no -3CGT marker) and -B restores it", True, "matches the Skill's sentence"),
        A("Shipped example rejects hostile input with a one-line Error (contig with ':', 'chr1:1,000', range, position < 1, unindexed BAM)", True, "rc 1, no traceback"),
        A("Skill does not recommend `-d` values that silently truncate deep targeted data", True, "cheat sheet uses -d 0 / -d 600000 / -d 1000000; usage-guide advice removed")]),
 dict(index=4, type="Variant B", label="REGRESSION: bcftools mpileup | call (germline, BCF intermediate, multi-sample -d 100000, parallel-by-contig, the 'WRONG' pipe) + library cheat sheet on real ARTIC/RNA-seq/1000G + error messages",
      status="COMPLETED", flag="✅", basic=35, spec=54,
      note=f"scripts t04 ({ck[4][0]}/{ck[4][1]}) and t05 ({ck[5][0]}/{ck[5][1]}). Every bash block ran; contigs merge in header order; quoted error texts are the real 1.24 messages.",
      asserts=[
        A("Modern Germline Calling, BCF Intermediate and Multi-Sample blocks run and call the planted SNV/indels; per-sample AD equals planted (17,3 | 8,12)", True, "4 records on the single-sample truth BAM"),
        A("Parallel by Contig: output contigs in header order chr1..chr11 (glob order would be chr1,chr10,chr11,chr2...) and a failing contig stops the merge", True, "11 records, index built; nonexistent reference -> non-zero, no all.vcf.gz"),
        A("The 'WRONG' pipe message and status are real: `samtools mpileup | bcftools call` -> 'Failed to read from standard input: unknown file type', exit 255, no output; RIGHT pipe gives 4 records", True, "re-checked independently in x_wrongpipe.sh (the first harness mis-read PIPESTATUS)"),
        A("Every cheat-sheet library row runs on real ARTIC nanopore, spliced RNA-seq and 1000G BAMs and gives the expected effect (-aa 29903 rows, -B, -A ...)", True, "28/28 checks"),
        A("Common Errors messages are the real ones: faidx 'sequence was not found' with exit 0 and N rows, fail to parse region, unindexed BAM", True, "verified with ARTIC BAM vs the wrong FASTA")]),
 dict(index=5, type="Stress", label="REGRESSION: previous re-audit's own inputs -- planted truth BAM (11 event types, colon contig, N/soft-masked ref) + 1,862-read random test, and 4 real + 2 synthetic BAMs pysam-vs-samtools matrix with 432,147 real pileup_text rows",
      status="COMPLETED", flag="✅", basic=35, spec=53,
      note=f"scripts t06 ({ck[6][0]}/{ck[6][1]}) and t07 ({ck[7][0]}/{ck[7][1]}). Two probes that asserted the OLD wrong claims (stepper='all' + fastafile, bcftools --nu) were updated to the round-2 text; note the 'stepper=all' label in those probes was itself wrong (see input 7).",
      asserts=[
        A("pileup_text equals samtools mpileup row for row on the planted new.bam and the 4,486-row random fuzz-clean BAM under 13 option sets each (default, -B, -q/-Q, -x, -A, --ff 0, --rf 16, -E, -C 50, -d 15, combined), and on the adjacent-indel read 10M2I2D10M", True, "0 differing rows in every comparison"),
        A("find_variants reports no reference-N site (nA:800-805) and no read-N allele (nA:790); the soft-masked site nA:920 G>A 3/8 (upper-case ref) and the overlap site nA:730 3/6 are right", True, "SNV-only scope holds: nothing at the planted insertions"),
        A("pysam parameter table (12 rows: -Q -q -x -A --ff -d -E -C, combined) equals samtools depth position by position on 4 real + 2 synthetic BAMs, and pileup_text equals mpileup row for row on 432,147 real rows", True, "6 datasets x 12 rows equal; the updated probes now assert the round-2 text"),
        A("Soft-masked reference: mpileup prints column 3 lower-case as in the FASTA (documented in Output Format) and pileup_text equals it row for row", True, "fuzz-clean and planted references carry soft-masked blocks; 0 differing rows"),
        A("Safety/scope: no fabricated numbers; documented figures (1087/1157, 8 -> 4, memory-hog) reproduce", True, "all reproduced")]),
 dict(index=6, type="Stress", label="NEW: 23 legal CIGAR templates (=/X runs, adjacent identical ops, I-D-I/D-I chains, N beside I/D, indels next to S/H) -> `indel_text`/`pileup_text` vs samtools mpileup row for row, 5 option sets, plus 13 wild templates",
      status="COMPLETED", flag="✅", basic=36, spec=55,
      note=f"script 10_cigar_fuzz.py: {ck[8][0]}/{ck[8][1]} scored checks. 3,784 rows x 5 option sets (default, -B, -E, -q20 -Q20 -x -A, --ff 0 -Q 0 -B) identical to samtools; wild set: only P (padding) CIGARs differ, and a CIGAR ending in D crashes pileup_text with -Q 0 (informational).",
      asserts=[
        A("Legal templates: pileup_text == samtools mpileup default, row for row (3,784 rows, 714 with indel markers, 40 with two adjacent markers, 440 lower-case-reference rows)", True, "0 differing rows"),
        A("Same under -B (952 marker rows, 55 adjacent), -E, -q 20 -Q 20 -x -A, and --ff 0 -Q 0 -B (1,085 marker rows, 63 adjacent)", True, "0 differing rows in all 4 remaining option sets"),
        A("Indels at read ends and beside soft clips (leading I, trailing I, S+I, I+S, D+S, S+D) match samtools", True, "wild templates IM, MI, SIM, MIS, MDS, SDM: 0 differing rows in all 5 option sets"),
        A("I-D-I, D-I-D and N-I-D chains match samtools", True, "MIDIM, MDIDM, MNIDM: 0 differing rows"),
        A("Scope: helper behaviour outside what an aligner emits is reported, not hidden", True, "P-op CIGARs (MPIM) differ in 148-462 rows depending on the option set; CIGARs ending in D (MD, MID) equal samtools in 4 option sets but raise IndexError under --ff 0 -Q 0 -B. Neither is claimed by the Skill; recorded as P2")]),
 dict(index=7, type="Adversarial", label="NEW: the round-2 BAQ and --rf statements re-derived on data the earlier auditors did not use (sarscov2 PE/SE/UMI real, 1000G+calmd BQ tags, own indel-dense BAM with none / computed / all-'@' BQ tags), both steppers, and 6 flag masks vs independent subsets",
      status="COMPLETED", flag="✅", basic=30, spec=45,
      note=f"script 11_baq_rf.py: {ck[9][0]}/{ck[9][1]} checks. With no stepper argument (pysam 0.24.1's real default = 'samtools') every BAQ mapping and --rf/--lu/--nu claim holds. The Skill's sentence 'BAQ is applied under either stepper ('all', the default, or 'samtools')' is FALSE: explicit stepper='all' + fastafile applies NO BAQ (538/538 BAQ positions differ on the own single-end BAM, 49/49 on real SE), and 'all' is not the default.",
      asserts=[
        A("With pileup() called with no stepper argument, the 4 BAQ table mappings (fastafile; no fastafile / compute_baq=False; fastafile + redo_baq=True) equal samtools default / -B / -E in depth and per-symbol counts at every position on all 7 datasets", True, "BQ-tag semantics right: all-'@' tags -> default == -B (0 differ) but -E differs at 538; also true for explicit stepper='samtools'"),
        A("`--rf` (samtools) == pysam flag_require == bcftools --lu == bcftools --rf (any bit set); bcftools --nu requires ALL bits, on 6 masks against independent pysam subsets", True, "mask 65: any-bit 200 reads (DP 27401) vs all-bit 100 reads (DP 13884); samtools --rf 65 == pysam == --lu; --nu == all-bit subset"),
        A("`-B` and `-E` cannot be combined", True, "samtools: 'Error: The -B option cannot be combined with -E', no output"),
        A("SKILL claim: with fastafile BAQ is applied under either stepper -- stepper='all' + fastafile equals `samtools mpileup -f` on single-end data", False, "stepper='all' + fastafile == stepper='all' without fastafile == -B: 538/538 (own BAM), 49/49 (real SE), and 0 differing from -B once overlap/orphans are neutralised on human PE; quality strings identical with and without fastafile under 'all'; no argument (redo_baq, compute_baq, max_depth) changes it"),
        A("SKILL claim: 'all' is pysam's default stepper", False, "the no-argument call equals stepper='samtools' on every dataset and differs from 'all' on 7 of 7 (overlap removal, orphan filter, BAQ); the -x/-A 'default matches' rows hold only for the real default")]),
 dict(index=8, type="Variant B", label="NEW: find_variants N handling, region edges, kwargs, restored Access Reads print, soft-masked reference, shipped example on a planted BAM (exact depth/alt counts) + real 1000G chr20 and sarscov2; usage-guide dedup audit",
      status="COMPLETED", flag="✅", basic=35, spec=54,
      note=f"scripts 12_find_variants_access.py ({ck[10][0]}/{ck[10][1]}) and 14_usage_guide_dedup.py ({ck[11][0]}/{ck[11][1]}). find_variants returned exactly the 8 hand-derived SNVs; equals an independent mpileup decode on 119 real 1000G SNVs and 3 sarscov2 SNVs. All 14 old usage-guide sections have their content in SKILL.md.",
      asserts=[
        A("find_variants on the planted BAM == hand truth: 120 (8/20), 520 (2/17 after 3 read-N dropped), 620 (exactly 0.10 kept), 720 (soft-masked ref, upper-case ref reported), 820+821 adjacent, 1000 (MAPQ-0 alt counted at default), 1150", True, "no reference-N (300-304) or read-N artefacts; depth 9, 1/21, Q10 alt and insertion-only sites not called"),
        A("find_variants == independent decode of samtools mpileup -B -Q 20 on real 1000G HG00349 chr20 (119 SNVs) and real sarscov2 (3 SNVs); **pileup_kw and 0-based region edges behave as documented", True, "min_base_quality=5 restores site 900; min_mapping_quality=1 drops site 1000; [1149,1150) -> 1150 only"),
        A("Restored Access Reads snippet at real MT192765.1:5700 prints name, strand, base, Q for 3 reads, equal to `samtools mpileup --output-extra QNAME,FLAG`; depth line equals column 4", True, "tuple sets identical"),
        A("usage-guide dedup lost nothing needed: 14 old sections (prerequisites, format tables, commands, pipeline, parallel, 4 pysam blocks, troubleshooting, tips) are present or replaced by corrected content in SKILL.md; dropped items (the 'No sequences in common' text, the `mpileup -g` prompt, the `-d 500`/`-d 1000` advice) were wrong on samtools 1.24 or contradict the measured depth-cap trap", True, "anchor checks 14/14; new guide keeps 9 prompts and the 6-step agent walk-through, no verbatim duplicate lines"),
        A("allele_counts / allele_frequency treat a read-base N consistently with find_variants", False, "allele_counts at pv1:420 returns {G:17, N:3} and allele_frequency divides by 20, while find_variants drops N from allele and depth; not stated in the docstring (P2)")]),
]

for i in inputs:
    i["assertions_passed"] = sum(1 for a in i["asserts"] if a["result"] == "PASS")
    i["assertions_total"] = len(i["asserts"])
    i["total"] = i["basic"] + i["spec"]
N = len(inputs)
ex_avg = round(sum(i["total"] for i in inputs) / N, 1)
static = {
    "functional_suitability": (8, 12, "Completeness 3, Correctness 2, Appropriateness 3. Covers text pileup, bcftools calling, pysam counting/pileup_text, defaults and errors, all verified; but the headline round-2 BAQ sentence ('either stepper', 'all' is the default) is false and would mislead an agent that passes stepper='all'."),
    "reliability": (10, 12, "Real failure messages and exit-status traps documented (reference mismatch exits 0 with N rows, wrong pipe exits 255, unindexed BAM); the shipped example fails with one-line errors; pysam helpers do not guard against P-op or trailing-D CIGARs."),
    "performance_context": (6, 8, "SKILL.md grew to 24.6 KB / 479 lines (upstream 14.8 KB) with all pysam helpers inline; usage-guide is now a 1.5 KB pointer. Under the 500-line guideline but heavy for a single file."),
    "agent_usability": (14, 16, "Options table with default columns, mapping table to pysam arguments, symbol table, copy-paste blocks that ran; consistency dented by the stepper statement contradicting behaviour."),
    "human_usability": (6, 8, "Natural prompts in the usage-guide; trigger description is short and plain; no interactive clarification guidance."),
    "security": (11, 12, "No credentials or network; shell blocks use fixed patterns; the example validates its argument, but paths are interpolated by the caller."),
    "maintainability": (9, 12, "SKILL.md / usage-guide split is clean after the dedup; one shipped example only, no test script for the ~150 lines of helper code."),
    "agent_specific": (16, 20, "Description precise; deprecation and tool-choice table act as escape hatches; no references/ folder (all depth in SKILL.md); re-runs idempotent."),
}
subtotal = sum(v[0] for v in static.values())
sw, dw = round(subtotal * 0.4, 1), round(ex_avg * 0.6, 1)
score = int(round(sw + dw))
grade = "Production Ready" if score >= 85 else "Limited Release" if score >= 75 else "Beta Only" if score >= 60 else "Reject"
sym = {"Production Ready": "⭐", "Limited Release": "✅", "Beta Only": "⚠️", "Reject": "❌"}[grade]
apass = sum(i["assertions_passed"] for i in inputs); atot = sum(i["assertions_total"] for i in inputs)
l1 = sum(i["basic"] for i in inputs) / N; l2 = sum(i["spec"] for i in inputs) / N
print(f"N={N} exec_avg={ex_avg} static={subtotal} weighted {sw}+{dw} = {sw + dw:.2f} -> {score} {grade}; assertions {apass}/{atot} ({apass / atot:.0%}); L1 avg {l1:.1f}/40 L2 avg {l2:.1f}/60")
floors_ok = subtotal >= 80 and ex_avg >= 85 and l1 >= 32 and l2 >= 48 and apass / atot >= 0.9
print("Production Ready floors met:", floors_ok)
if score >= 85 and not floors_ok:
    grade, sym = "Limited Release", "✅"

report = {
 "meta": {
  "skill_name": "bio-pileup-generation", "description": SKILL_DESC, "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0",
  "category": "Data Analysis", "execution_mode": "D", "complexity": "Moderate", "n_inputs": N,
  "source": "mrsonord2240/bioSkills@5fc1304c09be282792e56a613274508db5bfaead:alignment-files/pileup-generation",
  "audit_type": "second re-audit of a fixed Skill (pre-fix 71; first re-audit 84 Limited Release at ad9b5a4); auditor differs from both earlier auditors and both fixers",
  "executed": f"8/8 inputs executed; {tot_pass}/{tot_all} scripted checks pass ({tot_all - tot_pass} fail: both are genuine Skill defects, the stepper/BAQ statements in input 7; the allele_counts N inconsistency of input 8 is a scored assertion, not a scripted check)",
  "execution_note": "WSL science, env alignment-files: samtools 1.24, bcftools 1.24, pysam 0.24.1 (TOOLS.md). The Skill folder was copied byte-identical from worktree F:\\OpenScience\\wt\\af-pileup (commit 5fc1304) to run/skill (diff -r clean); Python and bash blocks were extracted verbatim from the copied SKILL.md; neither the worktree nor the external clone was written, public-data was only read (unindexed sarscov2 BAMs were copied into run/data before indexing). Inputs 1-5 group the 7 inputs of the archived first re-audit as regression tests (their generators re-used unchanged; two probes that asserted the old wrong claims were updated and are labelled UPDATED in the scripts); inputs 6-8 are new: own CIGAR-template BAMs, own indel-dense BAQ/BQ-tag BAMs + real sarscov2/1000G, own planted find_variants BAM. Input 7 overturns the round-2 fix claim and the first re-audit's mislabelling of the default stepper."
 },
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
    "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOI, trial or statistical value. Documented figures reproduce (1087/1157 n-vs-pileups positions, depth 8 -> 4 under BAQ, -d 8000 cap, memory-hog threshold, 1000G example rows). The 'checked position by position on 6 BAMs' sentence is accurate only for the no-stepper-argument call."},
    "practice_boundaries": {"result": "PASS", "detail": "No diagnosis or prescription; somatic, WGS production and long-read work are routed to dedicated callers."},
    "methodological_ground": {"result": "PASS", "detail": "No principled fallacy: the recommended workflows (bcftools mpileup | call, samtools -B for long reads, -d set explicitly) are correct and reproduce. One documentation statement about pysam steppers and BAQ is wrong (P1) but does not invert a conclusion of the recommended, default-stepper calls."},
    "code_usability": {"result": "PASS", "detail": "All Python helpers, the shipped example and every bash block ran on real and synthetic data (8/8 inputs executed); pileup_text equals samtools mpileup row for row on 3,784 legal-CIGAR rows x 5 option sets (input 6), on the planted and random-fuzz BAMs x 13 option sets and on 432,147 real rows (input 5); find_variants equals an independent decode on 119 + 3 real SNVs and 8 planted SNVs. pileup_text raises IndexError only on a CIGAR ending in D with -Q 0 (invalid alignment)."}}},
 "static_score": {"subtotal": subtotal, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
 "dynamic_score": {"execution_avg": ex_avg, "max": 100, "assertion_pass_rate": {"passed": apass, "total": atot},
   "inputs": [{"index": i["index"], "type": i["type"], "label": i["label"], "status": i["status"], "status_flag": i["flag"], "note": i["note"],
               "basic": i["basic"], "specialized": i["spec"], "total": i["total"], "assertions_passed": i["assertions_passed"], "assertions_total": i["assertions_total"],
               "assertions": i["asserts"], "executed": True,
               "execution_note": "executed in WSL science (samtools 1.24, bcftools 1.24, pysam 0.24.1); all output asserted on content, see run/ scripts and logs"} for i in inputs]},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": True, "veto_override": False},
 "key_strengths": [
   "Round 2 delivered what it claimed on the helpers: `indel_text` makes `pileup_text` identical to `samtools mpileup` on 3,784 legal-CIGAR rows x 5 option sets (adjacent I/D, D-I, I-D-I, N beside indels, =/X runs, indels next to S/H), `find_variants` returns exactly the 8 hand-planted SNVs with reference-N and read-N handled, and the Access Reads print is back",
   "The `--rf` / `flag_require` / bcftools `--lu` `--nu` row is now exactly right and checked against independent pysam subsets on 6 masks (any-bit vs all-bit)",
   "Every default that silently changes output is tabled with a samtools/bcftools column (-Q 13/1, --ff four flags, -d 8000/250, orphans, overlaps, BAQ) and the depth-cap, reference-mismatch (exit 0, N rows) and wrong-pipe traps are real and correctly worded",
   "The usage-guide dedup lost nothing an agent needs: 14 old sections map to SKILL.md content, and the dropped items ('No sequences in common' text, `mpileup -g` prompt, `-d 500` advice) were wrong on samtools 1.24 or contradict the measured depth-cap trap"],
 "recommendations": [
  {"priority": "P1", "title": "Round 2 introduced a false statement: BAQ 'under either stepper'; 'all' is the default", "observed_in": [7],
   "problem": "SKILL.md says fastafile switches BAQ on 'under either stepper (`'all'`, the default, or `'samtools'`)' and the table row for `-f` says 'either stepper'. pysam 0.24.1's default stepper is 'samtools'; with an explicit stepper='all' (or 'nofilter') fastafile applies NO BAQ (538/538 BAQ positions on the own single-end BAM, 49/49 on real SE data; identical qualities with and without fastafile), and 'all' also skips overlap removal and the orphan filter (281 human-BAM positions differ from `-B`), so the `-x`/`-A` 'default matches' rows only hold for the default stepper. Round 1's wording (stepper='samtools' + fastafile) was correct; the fix log's 'either stepper' verification called the no-argument call 'all'.",
   "root_cause": "The round-2 harness passed no stepper argument for its 'all' rows, so both rows exercised the default 'samtools' stepper.",
   "fix": "Rewrite the paragraph and table row: 'pysam's default stepper is `samtools`. With it, `fastafile=` switches BAQ on and `ignore_overlaps` / `ignore_orphans` / `min_base_quality` apply; with `stepper='all'` or `'nofilter'` neither BAQ nor overlap/orphan handling is applied, so do not pass them when matching mpileup.' Drop 'either stepper' and '`'all'`, the default'."},
  {"priority": "P2", "title": "allele_counts counts read-base N as an allele; find_variants drops it", "observed_in": [8],
   "problem": "At a site with 3 read-base N in 20 reads, allele_counts returns {'G': 17, 'N': 3} and allele_frequency divides by 20, while find_variants (round 2) drops N from alleles and depth; the docstrings do not say so.",
   "root_cause": "The N fix was applied to find_variants only.",
   "fix": "Skip base 'N' in allele_counts as well (or state 'N is counted as its own allele' in its docstring) so the two helpers agree."},
  {"priority": "P2", "title": "pileup_text scope: P-op CIGARs differ and a CIGAR ending in D crashes under -Q 0", "observed_in": [6],
   "problem": "Templates with a P (padding) op differ from samtools in 148-462 rows (samtools prints '+3*AC'); a read whose CIGAR ends in a deletion makes pileup_text raise IndexError when run with min_base_quality=0 / flag_filter=0.",
   "root_cause": "indel_text ignores op 6, and query_position_or_next is out of range after a trailing D.",
   "fix": "One docstring sentence: 'aligner-legal CIGARs only (no P ops, no trailing D)', or guard the quality lookup."},
  {"priority": "P2", "title": "SKILL.md is 24.6 KB with all helper code inline", "observed_in": [],
   "problem": "The single file grew from 14.8 KB to 24.6 KB (479 lines); the ~150 lines of pysam helpers are loaded on every invocation, and only one of them ships as a runnable example.",
   "root_cause": "The dedup moved usage-guide code into SKILL.md instead of into examples/.",
   "fix": "Move allele_counts / find_variants / pileup_text into examples/ (with a small self-test) and keep the table and one-line usage in SKILL.md."}]}

json.dump(report, open(f"{OUT}/eval_report_bio-pileup-generation_result.json", "w", encoding="utf-8", newline="\n"), indent=2, ensure_ascii=False)

# ------------------------------------------------ pre-emit checklist
R = report
assert all(1 <= len(i["assertions"]) <= 5 and len(i["assertions"]) >= 3 for i in R["dynamic_score"]["inputs"])
assert R["static_score"]["subtotal"] == sum(v["score"] for v in R["static_score"]["categories"].values())
assert len(R["static_score"]["categories"]) == 8
assert len(R["dynamic_score"]["inputs"]) == R["meta"]["n_inputs"] == N
for i in R["dynamic_score"]["inputs"]:
    assert i["basic"] + i["specialized"] == i["total"]
    assert i["assertions_passed"] == sum(1 for a in i["assertions"] if a["result"] == "PASS")
assert R["dynamic_score"]["execution_avg"] == round(sum(i["total"] for i in R["dynamic_score"]["inputs"]) / N, 1)
assert 2 <= len(R["key_strengths"]) <= 5
assert [r["priority"] for r in R["recommendations"]] == sorted(r["priority"] for r in R["recommendations"])
print("pre-emit checklist OK")

# ------------------------------------------------ viewer
L = []
L.append(f"# Eval Viewer — bio-pileup-generation (second re-audit)\nGenerated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@5fc1304c09be282792e56a613274508db5bfaead:alignment-files/pileup-generation`  |  Env: WSL `science`, samtools 1.24, bcftools 1.24, pysam 0.24.1\n")
L.append("## Summary Table\n")
L.append("| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|")
for i in inputs:
    L.append(f"| {i['index']} | {i['type']} | {i['basic']} | {i['spec']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['flag']} |")
L.append(f"\n**Execution Average: {ex_avg} / 100**  |  **Assertion Pass Rate: {apass}/{atot}**  |  **Static: {subtotal}/100**  |  **Final: {score} ({grade})**  |  Scripted checks: {tot_pass}/{tot_all} pass\n")
L.append(f"Previous re-audit: 84 (Limited Release, 223/230 checks). Pre-fix audit: 71 (Beta Only).  Complexity Moderate; N = 8 = 5 regression groups (the 7 archived inputs) + 3 new.\n")
L.append("""## What changed since the first re-audit, in one paragraph

Round 2 fixed five of the six findings for real (indel markers, find_variants N, --rf vs --lu/--nu, Access Reads print, soft-masked note) and the usage-guide cut lost nothing. It also **replaced a correct sentence with a false one**: the first re-audit's P1 ("stepper='all' + fastafile applies no BAQ is false") was itself wrong, because both the first re-auditor and the round-2 fixer labelled the *no-stepper-argument* call as `'all'`. pysam 0.24.1's default stepper is `'samtools'`. Evidence is in `run/x_probe_stepper_*.py` and input 7. Everything else the round-2 log claims reproduced on my own data.

## Method notes
- Skill copy: `run/skill/` (`diff -r` against the worktree clean); every Python function and bash block is extracted verbatim from that copy (`run/snippets.py`), never retyped.
- Data: synthetic and seeded (`00_`, `01_`, `02_`, `10_`, `11_`, `12_`, `13_`) plus real BAMs from `public-data\\` (human chr22, RNA-seq, 1000G HG00349, ARTIC nanopore, sarscov2 PE/SE/UMI; copied and indexed under `run/data` because they are unindexed and read-only).
- Every check asserts on content (decoded pileup text vs pysam counts vs bcftools DP vs independent pysam subsets vs hand truth); exit codes are never the evidence. `run_everything.sh` reproduces the whole audit; logs are `run/log_*.txt`, per-check records `run/checks_in*.json`.
- Two probes inherited from the first re-audit asserted the OLD wrong claims; I updated them (marked `UPDATED`) and fixed their stepper labelling. One harness (t04 PIPESTATUS through `head`) was rewritten after `x_wrongpipe.sh` confirmed the Skill's statement independently.
""")
L.append("## Detailed Outputs\n")
for i in inputs:
    L.append(f"### Input {i['index']} — {i['type']}\n**Prompt / scope:** {i['label']}\n\n**Status:** {i['status']} {i['flag']}  |  **Executed:** true\n\n**Output (what ran and what it printed):** {i['note']}\n\n**Scores:** Basic {i['basic']}/40 | Specialized {i['spec']}/60 | Total {i['total']}/100\n\n**Assertions:**")
    for a in i["asserts"]:
        L.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    L.append("")
def tail(name, pat=None, n=40, width=330):
    t = open(f"{RUN}/{name}", encoding="utf-8", errors="replace").read().splitlines()
    if pat:
        t = [x for x in t if re.search(pat, x)]
    return "\n".join(x[:width] for x in t[:n])

FENCE = "```"
L.append("## Execution evidence (trimmed; full logs in `run/log_*.txt`, per-check records in `run/checks_in*.json`)\n")
L.append("### Steps 1-3: veto, classification\nSkill veto T1-T4 PASS (no eval/exec of user strings, no network, fixed shell patterns, deterministic outputs: every comparison is exact). Category 3 Data Analysis, Mode D (SKILL.md code + shipped example script), Moderate complexity, N = 8 (5 regression groups, 3 new).\n")
L.append("### Input 7 -- the finding that changes the picture (stepper default and BAQ)\n")
L.append("Probe 6 (`x_probe_stepper_default.py`, human chr22 PE BAM, depth per position vs samtools):\n" + FENCE + "\n" + tail("log_x_probe_stepper_default.txt", None, 14, 260) + "\n" + FENCE)
L.append("Probe 3 (`x_probe_stepper_baq3.py`, own single-end BAM, every pysam argument that could plausibly enable BAQ under stepper='all'):\n" + FENCE + "\n" + tail("log_x_probe_stepper_baq3.txt", None, 14, 200) + "\n" + FENCE)
L.append("Probe 2 (`x_probe_stepper_baq2.py`, second method: the base-quality string pysam hands out in one BAQ-affected column; BAQ rewrites qualities in place):\n" + FENCE + "\n" + tail("log_x_probe_stepper_baq2.txt", None, 8, 200) + "\n" + FENCE)
L.append("Probe 4 (`x_probe_stepper_baq4.py`): with `-x -A` on the samtools side and `ignore_overlaps=False, ignore_orphans=False` on the pysam side, stepper='all' + fastafile equals `-B` (0 differ) and differs from the default; with default options it matches neither:\n" + FENCE + "\n" + tail("log_x_probe_stepper_baq4.txt", None, 8, 200) + "\n" + FENCE)
L.append("`11_baq_rf.py` summary lines (data, discrimination, the two failing claims, `--rf`/`--lu`/`--nu`):\n" + FENCE + "\n" + tail("log_11_baq_rf.txt", r"^(real|own|flags|mask|bcftools unfiltered|stepper=)|^\[FAIL\]|discrimination", 30, 300) + "\n" + FENCE)
L.append("The two failing scripted checks are exactly two SKILL.md statements: line 227 (\"BAQ ... is applied under either stepper ('all', the default, or 'samtools')\") and the table row at line 231 (`-f ref.fa` (BAQ on) | `fastafile=FastaFile(ref)` | either stepper).\n")
L.append("### Input 6 -- CIGAR-template differential test (`10_cigar_fuzz.py`)\n" + FENCE + "\n" + tail("log_10_cigar_fuzz.txt", r"^cg_legal|^INFO|--- wild", 30, 300) + "\n" + FENCE + "\nLegal templates: M, =/X runs, I, D, N, I-D, D-I, N-I, I-N, D-N, N-D, adjacent identical ops (II, DD, NN), S/H flanks, S+M+X+I. Wild templates are outside what an aligner emits and are informational.\n")
L.append("### Input 8 -- find_variants, restored print, dedup (`12_find_variants_access.py`, `14_usage_guide_dedup.py`)\n" + FENCE + "\n" + tail("log_12_find_variants_access.txt", r"^find_variants:|^decode|^by hand|^bcftools call|^allele_counts|^NOTE|^real|^Access|^1000G|^reference-N", 12, 420) + "\n" + FENCE + "\n" + FENCE + "\n" + tail("log_14_usage_guide_dedup.txt", r"^old guide|^new guide", 4, 200) + "\n" + FENCE)
L.append("### Informational (not scored against the Skill)\n- `13_probe_seq_star_and_related.py`: a secondary alignment with SEQ `*` is skipped by samtools even with `--ff 0`, and the helpers agree (no crash); all six Related Skills paths exist in the fork.\n- pysam 0.24.1 documents `all` as the default stepper in its docstring but the code default is `samtools` (probe 6).\n")
L.append("## Final report\n")
L.append(FENCE + f"\nSkill: bio-pileup-generation @ 5fc1304  |  Category: Data Analysis  |  Mode D  |  Moderate (N=8)\nStatic {subtotal}/100 x 0.4 = {sw}   Dynamic {ex_avg} x 0.6 = {dw}   FINAL {score}  ->  {sym} {grade}   deployable: yes   vetoes: none\nAssertions {apass}/{atot}; L1 avg {l1:.1f}/40, L2 avg {l2:.1f}/60; Production-Ready floors met (static >= 80, exec >= 85, L1 >= 32, L2 >= 48, assertions >= 90%)\nPrevious re-audit 84 Limited Release -> now {score} {grade}; pre-fix 71 Beta Only.\n" + FENCE + "\n")
L.append("Key strengths\n" + "\n".join(f"- {x}" for x in R["key_strengths"]) + "\n")
L.append("Optimization recommendations\n")
for r in R["recommendations"]:
    L.append(f"**[{r['priority']}] {r['title']}**  \nObserved in: {r['observed_in']}  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
L.append("> The score sits on the 85 boundary (84.6 rounded). Input 7 carries the P1: had round 2 kept the round-1 wording that paragraph would be clean. The grade is not a statement that the Skill is error-free; a round 3 that rewrites one paragraph and one table row closes the only open P1.\n")
open(f"{OUT}/eval_viewer_bio-pileup-generation.md", "w", encoding="utf-8", newline="\n").write("\n".join(L))
print("viewer written")

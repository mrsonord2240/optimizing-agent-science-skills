"""Builds eval_report_bio-alignment-amplicon-clipping_result.json for the RE-AUDIT of the fixed Skill and checks the schema's Pre-Emit
Checklist. Every score below is the auditor's judgement from the runs in run/ (logs/*.log). Run: python gen_report.py (Windows or WSL python)."""
import json, os, sys
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "eval_report_bio-alignment-amplicon-clipping_result.json")

def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}
def I(index, typ, label, status, note, basic, spec, assertions, executed, execution_note):
    p = sum(a["result"] == "PASS" for a in assertions)
    flag = "✅" if status == "COMPLETED" and basic + spec >= 75 else ("⚠️" if status == "COMPLETED" else "❌")
    return {"index": index, "type": typ, "label": label, "status": status, "status_flag": flag, "note": note, "basic": basic,
            "specialized": spec, "total": basic + spec, "assertions_passed": p, "assertions_total": len(assertions), "assertions": assertions,
            "executed": executed, "execution_note": execution_note}

inputs = [
 I(1, "Canonical", "Real ARTIC v5.3.2 nanopore BAM: Skill workflow verbatim, mode table and iVar block re-measured", "COMPLETED",
   "SKILL.md bash block (steps 0-4) run verbatim on 4916 real reads: rc 0, MD 4916/4916, residual 0/0; oracle 4817 left + 4800 right boundaries exact, 0 bad; MD/NM 0 mismatches vs independent recompute; mode table 97.5/97.5/0/0 % reproduced",
   36, 55, [
    A("The Skill's own workflow block (steps 0-4, extracted verbatim from SKILL.md) runs to rc 0 on the real ARTIC BAM and step 4 prints MD on 4916/4916 reads and residual 0/0", True, "run/out/i1/wf.out; logs/s1_real_artic.log"),
    A("Every read end moved by `--both-ends --strand` lands exactly on a BED primer boundary of the right strand (oracle from the BED alone)", True, "left ok 4817, right ok 4800, bad 0 (s1_oracle.py)"),
    A("Every number in the 'Choosing the Clip Mode' table and its notes reproduces on samtools 1.24 (3' residual 97.5/97.5/0/0 %, NOT CLIPPED 92 and 7, --clipped 4909, TOTAL CLIPPED 4824/9617)", True, "shipped checker and an independent pysam count agree; logs/s1b_modes_ivar.log"),
    A("The iVar block runs verbatim and its stated numbers hold (4909 reads out, 4701 identical to ampliconclip --both-ends --strand --clipped, residual 1.9 %/1.6 %, defaults write 0 reads)", True, "93/4909 and 79/4909 residual; default run wrote 0 records (-m 205)"),
    A("The shipped example is deterministic and complete on real data (THREADS 4/1/4 identical record md5, index written, MD 4916, no temp leak)", True, "md5 38df635d7d5b x3 (s1c_example_real.sh)")],
   True, "All executed in WSL env alignment-files (samtools 1.24, pysam 0.24.1, iVar 1.4.4); real nf-core/ARTIC data copied to out/i1, BAMs deleted after checking"),
 I(2, "Variant A", "Synthetic 800-read paired-end panel with planted SNPs under primers: three example modes + planted truth", "COMPLETED",
   "All 8 runs (5 hand pipelines + example default/--strand/--both-ends) clip 800/800 reads to the planted boundary; VAF at primer SNPs 0.5 to 1.0; checker flags the unclipped BAM (800/800) and reports 200/800 3' residual for --strand alone as the Skill states",
   36, 55, [
    A("Every read of every run is clipped to the planted primer boundary and mate fields/TLEN/MC/ms are repaired", True, "clip-truth ok=800 bad=0 x8; TLEN bad 0; MC wrong 0"),
    A("MD/NM restored by calmd equal an independent recompute in every run, hard clip included", True, "MD/NM wrong=0 x8 (s2_check.py)"),
    A("Primer-derived alleles are removed: pos310 {T:100,C:100} -> {T:100}; pos335 {A:100,G:100} -> {G:100}", True, "planted SNP VAF 0.5 -> 1.0"),
    A("The Skill's short-read claim holds: --strand alone leaves 200/800 (25 %) 3' primers, --both-ends --strand leaves 0; the checker flags the unclipped BAM (rc 1, 800/800 5')", True, "ex_strand: 3' 200 (25.0 %) 'not enforced'; unclipped rc=1"),
    A("The amplicon-markdup warning is true (samtools markdup marks 710 of 800 reads)", True, "DUPLICATE PAIR: 710")],
   True, "Synthetic data (make_synth.py, deterministic seed, md5-identical to the pre-fix data) run through the shipped example copy"),
 I(3, "Edge", "Strand/both-ends outcome table, BED formats and --tolerance semantics (synthetic single reads)", "COMPLETED",
   "All 16 cells of SKILL's synthetic 4x4 outcome table match; the 5-column error text and early rejection are correct; but the example rejects BEDs samtools accepts (track/browser header, space-delimited) with a wrong message; the --tolerance wording is loose",
   34, 49, [
    A("Every cell of the SKILL.md synthetic outcome table (4 reads x 4 flag sets) matches samtools 1.24 output", True, "16 match, 0 mismatch (s3_table_assert.py)"),
    A("A 5-column BED with --strand fails with 'Parsed 5 columns, but need at least 6' and the example stops early with its own message, before clipping", True, "rc 1 both; the SKILL BED block (6 col) parses"),
    A("A 7-column ARTIC BED, a '#' comment line and blank lines are accepted end to end", True, "example rc 0 on v_comment/v_blank; real ARTIC 7-col run in Input 1"),
    A("The example accepts every BED samtools accepts, and a rejection names the real cause", False, "samtools accepts a 'track' header and space-delimited BED; example rc 1 with 'no contig shared ... (amp1 100 125 ...)' for spaces and the wrong message '5-column BED is rejected' for a track line; 5-col BED with --both-ends fails only at the end as 'primer bases remain'"),
    A("The --tolerance description matches measured behaviour", False, "measured: a read start up to N bases UPSTREAM of the primer start matches; every start inside the primer always clips (d+0..d+12 at tol 0); the Skill says 'how many bases a read end may sit from a primer edge'")],
   True, "Synthetic reads (s3a/ s3_tol_make.py) through samtools 1.24 and the shipped example/checker copies"),
 I(4, "Variant B", "Hard-clip archive copy, iVar block, consensus, removed-claim and pointer checks", "COMPLETED",
   "Quick Reference hard-clip and repair lines work (800/800 exact, H in 800 reads, SEQ 94.9 -> 64.1 bp); soft-clip byte-identical SEQ 800/800; iVar block equals planted truth 800/800; ClipBam takes no primer file (0 of 101 help lines); BAQ-independent-of-MD verified; but the example comment still states the refuted BAQ claim",
   34, 51, [
    A("The Quick Reference hard-clip line and piped repair line run and the result equals the planted truth for 800/800 reads with H-CIGAR on all reads", True, "s4_check.py: exactly-matches-planted-truth=800"),
    A("Soft-clip is lossless (byte-identical SEQ for 800/800 reads) and samtools consensus --config hiseq --ambig turns the planted Y/R into T/G only after clipping", True, "unclipped Y/R; soft T/G (ref C/A)"),
    A("The new iVar block (-q 0 -m 1) reproduces the planted truth on paired-end data (800/800) and the 'fgbio ClipBam takes no primer file' note is true", True, "iVar 800/800; ClipBam --help 0 of 101 lines mention bed/primer/amplicon; fixed-25bp control 79 %"),
    A("The related-skill pointer flags are valid (samtools mpileup -aa ... works, bcftools mpileup -aa fails, --max-depth/-a FORMAT/AD,DP works) and bcftools BAQ output is identical with and without MD (32,150 records, with and without -B)", True, "body md5 377ccda153 == 377ccda153; ed659a15fa == ed659a15fa"),
    A("No refuted claim survives anywhere in the shipped Skill", False, "examples/ampliconclip_workflow.sh line 62 still says 'bcftools mpileup BAQ and IGV mismatch coloring depend on' MD/NM; SKILL.md line 161 (correctly) says BAQ uses the reference, not MD")],
   True, "Synthetic PE data plus real ARTIC BAM for the BAQ check; fgbio 4.1.1 side env for ClipBam --help"),
 I(5, "Adversarial", "Contig/reference mismatches through the shipped example, plus false-positive probes of the new hard-fail checks", "COMPLETED",
   "Every pre-fix silent-success trap now fails loudly with the right message and no output BAM (Illumina BAM + ARTIC BED, wrong FASTA, missing .fai); MD assertion catches a wrong reference even with the pre-check bypassed; multi-contig BAM, extra BED contigs and real Illumina PE pass; sparse sample is rejected; a late failure leaves an output BAM",
   34, 50, [
    A("Illumina BAM (MT192765.1) + ARTIC BED (MN908947.3) stops the example: rc 1, 'no contig shared by BAM header (MT192765.1) and BED (MN908947.3)', no output BAM", True, "was rc 0 with a clean-looking BAM before the fix"),
    A("A wrong reference FASTA is caught by the contig pre-check (rc 1, names the missing contig) and, with that check deleted, by the MD assertion ('calmd wrote no MD tags')", True, "rc 1 both; calmd's own stderr is now visible"),
    A("Legitimate inputs pass: multi-contig BAM with an unused header contig, FASTA lacking an unused contig, BED with extra contigs, and real Illumina PE reads with a renamed BED", True, "P1, P2, P3, P5, P5b all rc 0"),
    A("A missing .fai, missing arguments and a missing BAM stop with an actionable message", True, "'index the reference first: samtools faidx', usage line, samtools open error"),
    A("A failed run leaves no plausible-looking output BAM and a legitimate low-yield sample is not rejected with a misleading message", False, "after the MD-assertion failure f2b.bam still exists (also after a residual-check failure); a sparse BAM (one primer-free read) exits 1 'BED coordinates do not match the reads'")],
   True, "Real ARTIC/Illumina data plus synthetic sparse BAM, all through a copy of the shipped example"),
 I(6, "Stress", "PacBio-HiFi-like full-length 16S amplicons (900 reads, 3 contigs), NEW", "COMPLETED",
   "minimap2 map-hifi alignment, Skill workflow verbatim rc 0 residual 0/0; both-ends+strand clips 900/900 reads to the exact primer boundary at both ends (5 % jitter and 5 % deep truncation included); default/--strand leave 98.1 % 3' primers exactly as the Skill's rule says",
   35, 53, [
    A("The Skill workflow block runs verbatim on HiFi-like reads (rc 0) and step 4 reports MD 900/900 and residual 0/0", True, "NOT CLIPPED 0"),
    A("Every read of both orientations is clipped to the exact primer boundary at both ends when the primer is present, and left unchanged when a deep truncation removed it (planted-truth check)", True, "left ok 900, right ok 900 for the workflow output and for the shipped example"),
    A("The Skill's rule for reads that span the amplicon holds for HiFi: default and --strand leave 3' primer bases in 98.1 % of reads, --both-ends and --both-ends --strand in 0 %", True, "shipped checker rc 1/1/0/0; independent count 883/883/0/0"),
    A("The shipped example (default CLIP_OPTS) completes on HiFi reads with MD on every read and residual 0/0", True, "records mapped=900 MD=900"),
    A("The iVar block works on HiFi reads with -q 0 -m 1 (900 trimmed, residual 0/0) and hard clip produces H-CIGAR on all reads", True, "ivar 100 % (900); hard-clip H reads 900")],
   True, "SYNTHETIC HiFi-like data (0.10 % substitution, 0.03 % indel errors; real HiFi heteropolymer indels and degenerate primers are not modelled): s6_make_hifi.py, minimap2 -ax map-hifi"),
 I(7, "Scope Boundary", "Does check_primer_residual.py catch planted residual primers and wrong primer schemes? NEW", "COMPLETED",
   "Checker detects every planted residual (synthetic cases, one planted in a real clipped BAM, unclipped real BAM 98.1 %) with correct 0-based boundaries and 98k reads in 2.3 s; but bad-input exits are 1 not 2, and a wrong primer BED passes the example (rc 0) unless a coincidental read trips the residual check",
   32, 45, [
    A("Planted 5' and 3' residuals are detected with exact counts, and boundary reads (start 300, 324 flagged; 325 clean) follow the 0-based half-open BED rule", True, "17 of 17 detection/boundary/strand/CIGAR cases as expected; one planted read in real clipped BAM -> exactly 1 residual, rc 1"),
    A("The unclipped real ARTIC BAM and the unclipped synthetic BAM are flagged (rc 1)", True, "98.1 % 5' / 97.5 % 3' real; 100 % / 25 % synthetic"),
    A("Soft-clipped and hard-clipped primer bases, reads on contigs without primers and wrong-strand primers are not falsely flagged", True, "0 false positives in the corresponding cases; 98,320 clean reads in 2.3 s"),
    A("Exit codes follow the documented contract (1 = residual, 2 = bad input) so an agent can tell them apart", False, "5-col BED, missing BED and missing BAM all exit 1 (docstring says 2); the example then reports 'primer bases remain'"),
    A("A wrong primer-scheme BED does not pass the shipped example silently (SKILL Common Errors attributes this to the checker's exit 1)", False, "v3.0.0 BED on v5.3.2 reads: rc 1 only because one read's 3' end hit a primer (4445/4916 NOT CLIPPED unasserted); v5 BED shifted +9 bp: rc 0; v3 with CLIP_OPTS=--strand: rc 0, 4692 NOT CLIPPED")],
   True, "Synthetic planted BAMs plus real ARTIC BAM; checker run from a copy of the shipped folder")]

static_cats = {
 "functional_suitability": (10, 12, "Covers soft/hard clip, four clip modes with measured outcomes, 6-col BED, tag repair, verification, iVar alternative, markdup rationale; all mode/strand numbers verified. Left: stale BAQ comment in the example, iVar 'needs indexed' overstated, --tolerance wording loose, wrong-scheme detection attributed to the checker but not reliable"),
 "reliability": (8, 12, "Example now fails loudly on contig mismatch, wrong FASTA, missing .fai, 5-col BED with --strand, no clipping, missing MD, residual primers; gaps: rejects track-header/space-delimited BEDs with misleading messages, residual check silently skipped without pysam, output BAM left behind after a late failure"),
 "performance_context": (7, 8, "SKILL.md 202 lines, usage-guide 39 (was ~160+duplicated); one linear workflow; two equivalent repair pipelines shown (sort -n vs collate)"),
 "agent_usability": (15, 16, "Tables with measured numbers, a verify step with pass/fail, error table keyed to real messages; minor inconsistency (example comment vs SKILL BAQ, `python` vs `python3`, checker exit-code docs)"),
 "human_usability": (7, 8, "Natural trigger phrases and prompts; strict BED validation is acceptable, but some rejections name the wrong cause"),
 "security": (11, 12, "No eval/exec, quoted variables, mktemp + trap cleanup, no credentials; CLIP_OPTS env is intentionally word-split flags"),
 "maintainability": (10, 12, "Clear split SKILL / usage-guide pointer / example / independent checker; no shipped test data or expected output"),
 "agent_specific": (17, 20, "Precise trigger, SKILL under 500 lines, idempotent re-runs, stop conditions in the example; no handoff for low-yield/NTC samples or wrong-scheme BEDs")}
sub = sum(v[0] for v in static_cats.values())
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1)
score = int(sw + dw + 0.5)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
l1 = sum(i["basic"] for i in inputs) / len(inputs); l2 = sum(i["specialized"] for i in inputs) / len(inputs)
floors = {"static>=80": sub >= 80, "exec>=85": avg >= 85, "L1>=32": l1 >= 32, "L2>=48": l2 >= 48, "assert>=90%": ap / at >= 0.90}
print("static", sub, "exec avg", avg, "weighted", sw, dw, "score", score, "L1", round(l1, 1), "L2", round(l2, 1), "assertions", ap, at, round(100 * ap / at, 1), floors)
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅")
if not all(floors.values()):        # scoring_rubric.md section 5: any floor missed -> one tier down
    grade, sym = ("Limited Release", "✅") if grade == "Production Ready" else ("Beta Only", "⚠️")
    print("floor downgrade applied ->", grade)

report = {
 "source": "mrsonord2240/bioSkills@76805aaab9347c8022c25df34c533cc3abd0b898:alignment-files/alignment-amplicon-clipping",
 "meta": {"skill_name": "bio-alignment-amplicon-clipping",
          "description": "Trim PCR primers from aligned reads in amplicon-panel BAMs using samtools ampliconclip. Use when processing SARS-CoV-2 ARTIC, hereditary cancer panels, ctDNA hot-spot panels, or any amplicon assay where primer-derived bases would falsely confirm reference at primer footprints.",
          "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "B",
          "complexity": "Complex", "n_inputs": 7,
          "audit_kind": "re-audit of fixed Skill (fix/af-ampclip); pre-fix 68 Beta Only; inputs 1-5 regress the pre-fix inputs, 6-7 are new",
          "executed_inputs": "7/7",
          "tools": "samtools 1.24, bcftools 1.24, pysam 0.24.1, iVar 1.4.4, minimap2 2.31, fgbio 4.1.1 (side env); WSL science env alignment-files",
          "floors": "static 85 (>=80 ok), execution avg %s (>=85 ok), Layer1 avg %.1f (>=32 ok), Layer2 avg %.1f (>=48 ok), assertion pass %d/%d = %.1f%% (<90%%: one tier down per scoring_rubric section 5)" % (avg, l1, l2, ap, at, 100 * ap / at)},
 "veto_gates": {
  "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
  "research_veto": {"applicable": True, "gate": "PASS",
   "scientific_integrity": {"result": "PASS", "detail": "No fabricated numbers; every measured figure in the Skill (mode table, NOT CLIPPED, 4909/4701, 710/800, 32,150) was reproduced; Grubaugh 2019 Genome Biol 20:8 and the artic minion align_trim statement are correct"},
   "practice_boundaries": {"result": "PASS", "detail": "No diagnostic or prescriptive content in any of the 7 outputs"},
   "methodological_ground": {"result": "PASS", "detail": "Clip-mode guidance is now consistent with measured samtools 1.24 behaviour (the pre-fix inverted strand claims are gone); wrong-scheme detection is over-attributed to the checker (P1) but that is not a principled fallacy"},
   "code_usability": {"result": "PASS", "detail": "SKILL.md workflow and iVar blocks, the shipped example and check_primer_residual.py ran on real and synthetic data in all 7 inputs"}}},
 "static_score": {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static_cats.items()}},
 "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at}, "inputs": inputs},
 "final": {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym,
           "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False},
 "key_strengths": [
  "Every fixed claim reproduces: the four-mode 3' residual table (97.5/97.5/0/0 %), all 16 cells of the strand/both-ends outcome table, NOT CLIPPED 92/7, --clipped 4909, iVar 4909/4701, markdup 710/800, bcftools BAQ independent of MD",
  "The rewritten example turns every pre-fix silent-success trap into a non-zero exit with the right message (contig mismatch, wrong FASTA, 5-col BED, missing .fai, no MD) and passes legitimate multi-contig and real Illumina inputs",
  "check_primer_residual.py is a real independent check: detects planted residuals (5' and 3', both orientations, exact 0-based boundaries), ignores soft/hard-clipped primers, 98k reads in 2.3 s",
  "The --both-ends --strand default and its 'read can reach the opposite primer' rule hold on real nanopore, synthetic paired-end and synthetic HiFi-like long reads (exact boundaries 900/900)",
  "usage-guide.md dedup lost nothing: every prompt in it is answered in SKILL.md and the two wrong --both-ends sentences are gone"],
 "recommendations": [
  {"priority": "P1", "title": "Wrong primer BED passes the example; claim attributed to checker", "observed_in": [7],
   "problem": "A v5 BED shifted +9 bp and a v3.0.0 BED with --strand alone both exit 0 (4692 of 4916 reads NOT CLIPPED in the latter); the v3.0.0 BED with the default mode fails only because one read's 3' end hit a primer. The example header says a run that prints the final line succeeded, and SKILL Common Errors lists 'BED from another primer-scheme version' under the checker's exit 1.",
   "root_cause": "The checker tests residual primers against the same BED that was used to clip, so it cannot see a wrong BED; the example asserts only TOTAL CLIPPED > 0.",
   "fix": "In the example compute NOT CLIPPED / TOTAL READS from clip.stats and fail (or warn loudly) above a stated threshold (control 0.14 %, shifted BED 2.5 %, wrong scheme 90 %+); remove 'BED from another scheme' from the checker's row and point it at the NOT CLIPPED share."},
  {"priority": "P2", "title": "Refuted BAQ/MD claim survives in the example comment", "observed_in": [4],
   "problem": "examples/ampliconclip_workflow.sh line 62 says bcftools mpileup BAQ depends on MD/NM; bcftools output is byte-identical with and without MD (32,150 records, with and without -B) and SKILL.md says so.",
   "root_cause": "The fix removed the claim from SKILL.md and usage-guide.md but not from the script comment.",
   "fix": "Change the comment to 'IGV mismatch coloring and NM/MD-based filters read them'."},
  {"priority": "P2", "title": "Example rejects legitimate BEDs with the wrong message", "observed_in": [3],
   "problem": "samtools accepts a BED with track/browser header lines and space-delimited columns; the example exits 1 with '--strand needs the strand in BED column 6 ... 5-column BED is rejected' (track line) or 'no contig shared ... (whole lines listed)' (spaces). A 5-column BED with CLIP_OPTS=--both-ends fails only after clipping, as 'primer bases remain'.",
   "root_cause": "The BED checks use awk -F'\\t' with !/^#/ and count every non-comment line, and the checker's BED loader also needs 6 columns without saying so up front.",
   "fix": "Skip lines starting with track/browser and split on any whitespace in the awk checks (or state 'tab-delimited, no header lines' in the example header); make the checker's BED error say it is a BED problem."},
  {"priority": "P2", "title": "check_primer_residual.py exit codes contradict its docstring", "observed_in": [7],
   "problem": "The docstring says exit 2 on bad input, but a 5-column BED (sys.exit(message)), a missing BED (traceback) and a missing BAM all exit 1, the same code as 'residual found', so the example reports 'primer bases remain'. When pysam is not importable the example skips the check with only a stderr note and exits 0.",
   "root_cause": "sys.exit(str) and uncaught FileNotFoundError give status 1; the skip path is not treated as a failed check.",
   "fix": "Catch bad-input errors and return 2 (print to stderr); in the example treat rc 2 as 'check could not run' and fail (or require pysam explicitly)."},
  {"priority": "P2", "title": "Failed example runs leave an output BAM; sparse samples get a misleading stop", "observed_in": [5],
   "problem": "After the MD assertion or the residual check fails, $OUT (bam and .bai) already exists and looks finished; a legitimate sparse or negative-control sample with no read on a primer exits 'BED coordinates do not match the reads'.",
   "root_cause": "calmd writes straight to $OUT and the checks run after; the TOTAL CLIPPED > 0 assert cannot tell a wrong BED from a low-yield sample.",
   "fix": "Write to $WORK/final.bam and mv to $OUT after the checks pass; word the stop as 'ampliconclip clipped nothing (wrong BED, or no reads on primers)'."},
  {"priority": "P2", "title": "Two small claim inaccuracies (iVar index, --tolerance)", "observed_in": [1, 3],
   "problem": "iVar 1.4.4 trimmed an unindexed sorted BAM (4909 reads) although SKILL says it needs an indexed BAM; --tolerance N is described as the distance a read end may sit from a primer edge, but reads starting inside the primer always clip and N only extends the match N bases upstream of the primer start.",
   "root_cause": "Statements copied from tool documentation without a run.",
   "fix": "Say 'iVar expects sorted input (index optional on 1.4.4)' and 'a read start up to N bases before the primer start still matches; starts inside the primer always match'."}]}

# ---- Pre-emit checklist -------------------------------------------------------------------
assert report["static_score"]["subtotal"] == sum(c["score"] for c in report["static_score"]["categories"].values())
assert len(report["static_score"]["categories"]) == 8
assert len(inputs) == report["meta"]["n_inputs"]
for i in inputs:
    assert 3 <= len(i["assertions"]) <= 5 and i["assertions_passed"] == sum(a["result"] == "PASS" for a in i["assertions"])
    assert i["basic"] + i["specialized"] == i["total"] and i["basic"] <= 40 and i["specialized"] <= 60
assert 2 <= len(report["key_strengths"]) <= 5
pr = [r["priority"] for r in report["recommendations"]]; assert pr == sorted(pr)
assert report["final"]["score"] == score
with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(report, fh, indent=2, ensure_ascii=False); fh.write("\n")
print("wrote", os.path.abspath(OUT))

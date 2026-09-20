#!/usr/bin/env python3
"""Builds eval_report_bio-long-read-splicing_result.json (SECOND re-audit of the fixed Skill, commit 887eaed) from the scores decided after the runs, and runs the
schema pre-emit checklist. Scores are the auditor's own; every number quoted in a note comes from a log in run/logs."""
import json, os, re as _re, yaml
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "eval_report_bio-long-read-splicing_result.json")
_t = open(os.path.join(HERE, "skill_copy", "SKILL.md"), encoding="utf-8").read()
FM = yaml.safe_load(_re.match(r"^---\n(.*?)\n---\n", _t, _re.S).group(1))
assert FM["name"] == "bio-long-read-splicing"
def A(text, ok, note): return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

meta = {
    "skill_name": "bio-long-read-splicing", "description": FM["description"],
    "source": "mrsonord2240/bioSkills@887eaeddf09532feee6caaf5f325d0c9b3ce7101:alternative-splicing/long-read-splicing",
    "evaluated_on": "2026-09-20", "evaluator_version": "skill-auditor@1.0", "category": "Data Analysis", "execution_mode": "D", "complexity": "Complex", "n_inputs": 8,
    "mode": "second re-audit of a fixed Skill (fix branch fix/as-longread, round 2 on top of c07c53c); previous: 80 Limited Release (2 open P1), archived under audits/_pre-fix-20260920b; original first audit 68 Reject archived under audits/_pre-fix-20260920",
    "environment": "F:/OpenScience/audit-envs/alternative-splicing: WSL as-lr (FLAIR 3.0.1, IsoQuant 4.0.0, minimap2 2.31, pysam 0.23.3), as-lr-drim (Rscript with DRIMSeq 1.34.0, argparse, data.table for flair diffSplice --test), as-sqanti (SQANTI3 6.0.2, uLTRA 0.1), as-rmatslong (rMATS-long 2.1.0), as-pb (skera 1.4.0, lima 26.2.1, isoseq 26.2.0); Windows R 4.4.3 via r.sh / r-bambu.sh (bambu 3.8.3, DRIMSeq, stageR)",
    "data": "SYNTHETIC: (a) the first re-auditor's planted set regenerated from run/gen_planted.py (seed 5150; 60 genes, 20 planted DTU, annotated 7/12-nt microexons, two unannotated isoforms; HiFi, ONT cDNA unstranded/stranded, direct RNA), its microexon sets (seeds 4242, 4343), the first auditor's sets regenerated from prior_make_*.py; (b) NEW this round: run/gen_micro2.py (seed 9191, GC 0.58, 12 single microexons of 3-27 nt plus two tandem pairs, 150 inclusion + 150 skipping reads per gene, HiFi / ONT unstranded / direct RNA at 7.2% and 4% error) and run/mk_kinnex3.py (synthetic 6-fold Kinnex array, 24 ZMWs, both orientations, missing adapters). REAL: LRGASP WTC-11 cDNA (FLAIR test set, 1883 reads) and SG-NEx A549 direct RNA (129 reads, chr9 slice); public-data/ was only read.",
    "executed_summary": "8/8 inputs executed. Not executed on real data: Kinnex (no real Kinnex reads reachable; the PacBio adapter download host was unreachable), lima/isoseq only on my synthetic array; Bambu multicore on Linux; deSALT.",
}
veto = {
    "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
    "research_veto": {
        "applicable": True, "gate": "PASS",
        "scientific_integrity": {"result": "PASS", "detail": "No fabricated identifiers or results. The fixer's new numbers reproduce on independent data: -uf false-junction 48.2% and 30.5% (unoriented HiFi), ts:+ 1.000/0.502/0.503, bonus-20 recoding of skipping reads (HiFi 6-nt exon: skipping 0 of 150), bonus 17 dangling junctions on real reads 12 (0 at <=16) with a flair correct crash at 17-20, DTU 20/20, rMATS-long 20/20, flair diffSplice --test 20/20. Two claims are scoped to one sequence or one error profile (uLTRA 150/150 for a 10-nt exon; dRNA 99% at bonus 16), see P2 items."},
        "practice_boundaries": {"result": "PASS", "detail": "Research tooling only; ALS cryptic-exon and ASO items are pointers, nothing diagnostic or prescriptive."},
        "methodological_ground": {"result": "PASS", "detail": "The microexon recipe now carries the skipping-read control the previous audit asked for and it holds on my independent set of 12 sizes in both directions (HiFi 100.0 inc / 99.9 skip, ONT 99.6 / 99.2 at bonus 16); -uf guidance consistent in body, decision tree, usage-guide and example."},
        "code_usability": {"result": "PASS", "detail": "12 of the 14 fenced blocks of SKILL.md were extracted and run verbatim (the install line only dry-run, the ESPRESSO abundance-mode rMATS-long command not run: it needs a user-supplied file): alignment recipes, microexon awk and pysam snippet, FLAIR block incl. diffSplice --test, IsoQuant, SQANTI3, rMATS-long, DTU R block, the short-read-junction BED recipe, skera block (Bambu with ncore = 1 as the block instructs on Windows R). The shipped example ran end to end from a clean copy for hifi, ont, drna (with and without SR_JUNCTIONS), real ONT cDNA and real direct RNA, exit 0 with content asserted."},
    },
}
static = {
    "functional_suitability": (10, 12, "Every promised tool has a recipe that ran (FLAIR, IsoQuant, Bambu, SQANTI3, rMATS-long, DRIMSeq/stageR, diffSplice --test, skera). Deductions: uLTRA is offered as a peer of the --junc-bed recipe on the strength of one 10-nt exon (on my 14 microexon genes it loses 3-nt exons and 4+12 tandem pairs and recovers 53-80% of 5-11 nt exons on ONT); single-cell path stops at skera/lima/refine (barcode assignment out of scope, stated)."),
    "reliability": (9, 12, "rMATS-long block now fails loudly (truncated BAM rc 1, header-only BAM 'empty or missing alignment_info/trt3.tsv', mismatched contigs KeyError rc 1); example uses set -euo pipefail; failure modes carry measured symptoms. Gaps: flair diffSplice --test swallows an R error for an event type whose genes all fail DRIMSeq's filter (real data: '!No genes left after filtering!' traceback, FLAIR rc 0, no drimseq_alt5 file) and the text only mentions empty event types; contig-mismatch error is cryptic."),
    "performance_context": (4, 8, "SKILL.md grew to 38.8 kB / 580 lines (about 9.7k tokens) with no references/; the microexon evidence paragraphs, DTU code and per-tool failure modes all load up front. Workflow itself is linear."),
    "agent_usability": (14, 16, "Cold-start clear: entry points, flags and file names match FLAIR 3.0.1, IsoQuant 4.0.0, SQANTI3 6.0.2; recipes carry expected values and one-line checks (orientation ts:A, dangling-junction awk, two-way pysam snippet); PLATFORM switch in the example. The microexon paragraph is dense and needs re-reading."),
    "human_usability": (6, 8, "Description is long but uses natural terms; strict input requirements stated (manifest layout, --out_dir must not exist, file names)."),
    "security": (11, 12, "No credentials, local file tools only; example quotes variables, PRESET unquoted on purpose and commented."),
    "maintainability": (9, 12, "usage-guide reduced to overview and prompts; versions pinned; runnable example plus copy-paste checks make the claims testable. SKILL.md is monolithic and grew by the evidence paragraphs."),
    "agent_specific": (15, 20, "Trigger description precise; example composable through environment variables; stop conditions given (never -uf on unoriented reads, do not raise the bonus without the two-way check). Progressive disclosure weak: 580 lines, no references/, and neither SKILL.md nor usage-guide.md points at examples/longread_splicing_pipeline.sh."),
}
sub = sum(v[0] for v in static.values())
static_score = {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}}

inputs = [
 dict(index=1, type="Canonical", label="FLAIR workflow (correct-collapse-quantify-diffSplice --test) on planted 3v3 HiFi and real LRGASP cDNA", status="COMPLETED",
      note="Block verbatim, rc 0 on both; 124/124 planted isoforms; diffSplice --test with the documented prerequisites: 22 ES events tested, 20/20 planted genes + 2 extra; real data: alt5 DRIMSeq error swallowed",
      basic=34, specialized=54, assertions=[
        A("FLAIR block extracted verbatim from SKILL.md (correct, collapse, quantify, diffSplice --test) runs on 6 planted HiFi samples and on real LRGASP reads", True, "rc 0 both; planted: 49665 corrected, 0 inconsistent, 124 isoforms; real: 1672 corrected / 214 inconsistent, 33 isoforms"),
        A("All 124 planted isoforms, incl. the two unannotated ones, are recovered when the SJ.out.tab junctions are passed", True, "124 collapsed isoforms = 124 truth chains; SQANTI3 later calls G057N novel_in_catalog, G058N novel_not_in_catalog"),
        A("flair diffSplice --test works with the prerequisites the SKILL lists (Rscript with DRIMSeq, argparse, data.table)", True, "as-lr-drim Rscript first on PATH: drimseq_es tested 22 events, planted DTU 20/20, 2 other genes (G037, G042); alt3/ir 'event matrix file empty, not running DRIMSeq' as the text says"),
        A("Orientation check on real cDNA reads gives the SKILL's ~0.5", True, "0.503 (ONT recipe), 0.498 (HiFi recipe) on LRGASP; planted 1.000 (HiFi) / 0.502 (ONT unstranded)"),
        A("A failed DRIMSeq test for an event type is reported, not silent", False, "real 6-sample data: alt5 has events but none survive dmFilter; R prints '!No genes left after filtering!' + traceback, FLAIR exits 0 and writes no drimseq_alt5 file; the SKILL only describes empty event types"),
      ]),
 dict(index=2, type="Variant A", label="IsoQuant discovery/quantification and Bambu with NDR 0.1", status="COMPLETED",
      note="IsoQuant block verbatim rc 0, per-sample counts equal truth, output names now match 4.0.0; Bambu ncore=8 fails on Windows R exactly as the block warns, ncore=1 r 0.999",
      basic=34, specialized=53, assertions=[
        A("IsoQuant block runs verbatim (2 FASTQ inputs, default prefix) and every output name the SKILL lists exists", True, "rc 0; OUT.transcript_models.gtf, OUT.transcript_counts.tsv, OUT.transcript_grouped_file_name_counts.tsv, OUT.discovered_transcript_counts.tsv present; transcript_model_counts.tsv absent and no longer claimed"),
        A("Per-sample IsoQuant counts match planted truth", True, "G001A 54=54, G001B 14=14 (ctrl1), G001A 22 (trt1); annotated planted isoforms matched by exact chain 123/123"),
        A("Bambu block: ncore=8 fails on Windows R (as the comment says) and ncore=1 gives counts matching truth; NDR caveat holds", True, "ncore=8: 'BiocParallel errors ... could not find function seqlengths'; ncore=1: r 0.9992/0.9989/0.9990, 0 novel transcripts with the 'NDR approximated' warning; real A549 dRNA 105 transcripts, total 88"),
        A("IsoQuant statements about novel sites and --illumina_bam hold: 30-nt donor shift has no model with --genedb, with or without short reads; de novo models it", True, "iq_noillu = iq_illu: G057N 37 reads modelled, G058N none (125,055 short reads); de novo run: 121 models, 121/124 truth chains incl. G058N"),
        A("IsoQuant counts the inclusion isoform for a microexon when fed the recipe alignment", True, "micro2: HiFi --junc-bed 149.0/150 inclusion and 148.6/150 skipping (plain 87.0 / 210.5); ONT bonus 16 148.2 / 148.2 (plain 25.8 / 223.2)"),
      ]),
 dict(index=3, type="Variant B", label="SQANTI3 classification and filtering, with CAGE and polyA support", status="COMPLETED",
      note="Block verbatim on real FLAIR isoforms (CAGE/polyA from the SKILL's URLs) and planted isoforms; categories match truth; full IsoQuant GTF into the filter aborts as the SKILL says",
      basic=35, specialized=54, assertions=[
        A("SQANTI3 block runs verbatim with the CAGE and polyA files fetched from the URLs the SKILL names", True, "rc 0; 33 real isoforms: FSM 8, ISM 18, antisense 5, NIC 1, genic 1; within_CAGE_peak TRUE 7, polyA_motif_found TRUE 17; filter 29 pass, filtered GTF 143 lines"),
        A("Planted annotated isoforms are FSM and the two unannotated ones get the right novel category", True, "122/122 FSM; G057N novel_in_catalog (combination_of_known_splicesites); G058N novel_not_in_catalog (at_least_one_novel_splicesite)"),
        A("First auditor's 10 query isoforms classified as planted", True, "9/10 by his labels; Q07 is genic_intron, the correct SQANTI3 label for an exon inside an intron (his truth said genic)"),
        A("The transcript/exon-only awk before the filter is necessary", True, "full IsoQuant GTF into sqanti3_filter.py rules: rc 1 AssertionError; awk-filtered GTF passes"),
        A("Filter step needs --skip_report on small inputs and the QC step accepts --report skip", True, "used in the block and the example, both ran rc 0 on 6, 10, 33 and 123 isoforms"),
      ]),
 dict(index=4, type="Stress", label="Shipped example from a clean copy: hifi, ont, drna, +SR_JUNCTIONS, real ONT cDNA, real direct RNA", status="COMPLETED",
      note="hifi/ont/drna each exit 0 from a clean copy, with and without SR_JUNCTIONS; chains, counts, categories asserted against truth; real ONT cDNA and real A549 dRNA also exit 0 with 0 dangling junctions",
      basic=35, specialized=55, assertions=[
        A("examples/longread_splicing_pipeline.sh, run from a clean copy, exits 0 for PLATFORM=hifi, ont, drna and with SR_JUNCTIONS", True, "6/6 runs exit 0; first auditor's synthetic reads: hifi 95.6% and ont 96.0% exact chains, 0 false-junction reads, filter 6 pass"),
        A("Alignment content is right: exact chains, no false junctions, orientation and dangling-junction checks print the expected values", True, "planted exact chains 91.5 / 82.8 / 65.2% (5'-truncated reads consistent 100 / 99.9 / 99.8%), false-junction 0.0 / 0.0 / 0.0%; ts:+ 1.000 / 0.502; intron-next-to-soft-clip 0 in all runs"),
        A("IsoQuant, FLAIR and SQANTI3 outputs match planted truth", True, "IsoQuant r 0.9987 / 0.9956 / 0.9817 vs truth, FLAIR 0.9996 / 0.9990 / 0.9935; 123/123 IsoQuant models = truth chains; SQANTI3 FSM 122 + NIC 1 in all three; filtered GTF 673 lines"),
        A("SR_JUNCTIONS makes flair correct keep the unannotated 30-nt isoform", True, "G058N 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna); IsoQuant still has no model (merged), as the SKILL says"),
        A("Runs on real reads: LRGASP ONT cDNA (with and without real short-read junctions) and A549 direct RNA", True, "real LRGASP cDNA (1883 reads): exit 0 both ways, ts:A:+ 0.503, dangling 0, IsoQuant 10 models (1188 reads counted, 477 ambiguous), FLAIR 33 isoforms (1672 corrected / 214 inconsistent), SQANTI3 10 FSM, filter 10 pass; SR_JUNCTIONS changes nothing there because the test junction file has 8 rows (7 annotated); real A549 dRNA (129 reads): exit 0, 6 models, FLAIR 10 isoforms, SQANTI3 6 FSM"),
      ]),
 dict(index=5, type="Scope Boundary", label="Differential isoform analysis: DRIMSeq/stageR DTU, rMATS-long ASM mode with failure paths", status="COMPLETED",
      note="DTU block on FLAIR counts 20/20 planted (22 called); rMATS-long block verbatim rc 0, 64 ASMs, 20/20; truncated BAM, header-only BAM and contig mismatch all stop with rc 1",
      basic=34, specialized=53, assertions=[
        A("DTU block sourced verbatim on the FLAIR quantify output recovers the planted DTU genes", True, "60 genes tested, 22 stage-wise significant, planted 20/20, other G037 G042"),
        A("DTU block runs to the end on the real 6-sample FLAIR counts and reports no significant gene", True, "'No genes were found to be significant on a 5% OFDR level', dtu NULL (as the block comment says)"),
        A("rMATS-long block as written (mkdir, samples.tsv, set -euo pipefail) runs and recovers the planted DTU genes", True, "rc 0; alignment_info 6 TSVs + indexes; differential_asms.tsv 65 lines; adj p < 0.05: 25 genes, planted 20/20, 5 other (0.01: 23/20/3)"),
        A("rMATS-long preprocessing failure is loud, not header-only tables", True, "truncated BAM rc 1 (samtools error), header-only BAM rc 1 'empty or missing alignment_info/trt3.tsv', no output dir in either"),
        A("Annotation with the wrong contig names is reported in an actionable way", False, "rc 1 but the message is a bare 'KeyError: ctrl1' from rmats-long; the block's own emptiness checks are never reached"),
      ]),
 dict(index=6, type="Adversarial", label="Unstranded ONT cDNA or unoriented HiFi: which minimap2 recipe, is -uf right?", status="COMPLETED",
      note="Every figure in the SKILL reproduces on my planted reads: 48.2% false-junction reads with -uf on ONT cDNA, 30.5% on unoriented HiFi, ts:+ 1.000/0.502/0.493, real LRGASP 0.503",
      basic=35, specialized=55, assertions=[
        A("Unstranded ONT cDNA with -uf yields the false junctions the SKILL reports; without -uf it does not", True, "exact chains 42.2% vs 82.7%; false-junction reads 48.2% vs 0.0% (SKILL: 47%/50% vs 94%/1.1% on other reads)"),
        A("Unoriented HiFi with splice:hq -uf shows ~29% false-junction reads", True, "30.5% with -uf (exact 62.9%), 0.0% without; orientation check 0.493"),
        A("On oriented reads (HiFi, stranded ONT, direct RNA) -uf and no -uf give identical chains", True, "hifi 91.5 = 91.5%, ontstr 83.3 = 83.3%, drna 64.9 = 64.9%"),
        A("Orientation-check awk separates oriented from unoriented reads and works on real reads", True, "planted hifi 1.000, ontunstr 0.502, ontstr 1.000; real LRGASP cDNA 0.503"),
        A("-uf appears only for direct RNA in decision tree, recipes, usage-guide and example", True, "grep of SKILL.md, usage-guide.md and the example: direct-RNA recipe and warnings only"),
      ]),
 dict(index=7, type="Edge", label="NEW: microexon recipe on my own 3-27 nt set, both directions, tandem pairs, real-read side effects", status="COMPLETED",
      note="Recipe holds two-way on 12 new sizes (HiFi 100.0/99.9, ONT 99.6/99.2; dRNA 99.1/99.2 at 4% error but 93.2/94.9 at 7%); bonus 20 recodes skipping reads; real ONT dangling 0 at <=16, 12 at 17, flair correct crash at 17-20; uLTRA claim does not generalise",
      basic=32, specialized=50, assertions=[
        A("HiFi --junc-bed alone and ONT --junc-bed --junc-bonus 16 keep both isoforms on an independent set (3-27 nt, two tandem pairs, 150+150 reads/gene)", True, "HiFi juncbed inc 99.9 / skip 100.0 (min 98.7); ONT bonus16 inc 99.6 / skip 99.2 (min 97.3), tandem T1 100/99, T2 96/100; plain HiFi 58.2 / 100, plain ONT 16.4 / 96.6"),
        A("The danger of a high bonus is real and the SKILL's check catches it: skipping reads recoded to inclusion", True, "bonus 20 HiFi skip mean 58.3% (5/12 genes < 90%, tandem 0%), ONT 82.2%; the SKILL's pysam snippet verbatim: M03 HiFi plain 0/300, bonus 20 300/0 (SKILL example 0/399, 400/0)"),
        A("Real ONT reads: bonus 16 leaves no intron next to a soft clip, 17+ does and flair correct fails", True, "LRGASP 1883 reads: dangling 0 at default..16, 12 at 17, 18 at 18, 27 at 20; flair correct rc 0 at default/15/16, rc 1 'juncsToBed12 start/end' at 17, 18, 20"),
        A("Direct-RNA recipe reaches >=90% of inclusion reads for every size at bonus 16", False, "at 4% error 99.1% (min 96.0); at 7.2% error mean 93.2%, 4/12 genes < 90% (largest 27-nt exon 84.7%): the SKILL's 99% depends on the read error rate, which it does not state"),
        A("uLTRA with the exon in the annotation is an equivalent route", False, "micro2: HiFi inc 91.4% (3-nt and 4+12 tandem 0%), ONT 76.6% (6/12 genes < 90%, worst 53%), dRNA 78.6%; the SKILL's 150/150 is one 10-nt exon"),
      ]),
 dict(index=8, type="Edge", label="NEW: Kinnex array de-concatenation with skera, then lima and isoseq refine", status="COMPLETED",
      note="skera block verbatim on my synthetic 6-fold array: 96/96 full-array S-reads equal planted segments, malformed arrays withheld correctly; lima and isoseq refine work once the toy BAM carries the zm tag (explains the SKILL's 'did not finish'); mas16 file name not verifiable",
      basic=31, specialized=48, assertions=[
        A("skera split block runs verbatim on a Kinnex array and returns the planted segments", True, "24 ZMWs: 16 full arrays -> 96 S-reads, 96/96 sequences equal planted segments (8 arrays stored reverse-complemented); dl/dr tags (0,1)...(5,6); total 132/132 output S-reads equal planted segments"),
        A("skera withholds segments it cannot bound correctly", True, "4 arrays missing the last adapter: 20 of 24 (final open segment dropped); 4 arrays with a middle adapter missing: 16 of 20 (fused segment dropped); summary 'Percentage of Reads with Full Array 66.67'"),
        A("lima --isoseq and isoseq refine run on the S-reads", True, "with the zm tag: lima 132 in / 132 out, refine 132 flnc; without zm the S-read names are movie/?/ccs/... and lima hangs (killed at 60 s, rc 124)"),
        A("The SKILL's account of the lima stall is accurate and complete", False, "it says 'on that toy BAM lima did not finish' without the cause (missing zm tag in the toy BAM) and still lists lima/isoseq as --help only"),
        A("The adapter file name in the block can be obtained from the source the SKILL names", False, "skera.how/adapters shows only five sample adapters (A-E) and a link to downloads.pacbcloud.com, unreachable from here; 'mas16_primers.fasta' not verifiable"),
      ]),
]
for i in inputs:
    i["assertions_total"] = len(i["assertions"]); i["assertions_passed"] = sum(a["result"] == "PASS" for a in i["assertions"])
    i["total"] = i["basic"] + i["specialized"]; i["status_flag"] = "\u2705" if i["total"] >= 75 else "\u26a0\ufe0f"
avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
dyn = {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": sum(i["assertions_passed"] for i in inputs), "total": sum(i["assertions_total"] for i in inputs)}, "inputs": inputs}
sw, dw = round(sub * 0.4, 1), round(avg * 0.6, 1); score = round(sw + dw)
grade, sym = ("Production Ready", "\u2b50") if score >= 85 else ("Limited Release", "\u2705") if score >= 75 else ("Beta Only", "\u26a0\ufe0f") if score >= 60 else ("Reject", "\u274c")
final = {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": grade in ("Production Ready", "Limited Release"), "veto_override": False}
key_strengths = [
    "Every recipe in SKILL.md ran: FLAIR (incl. diffSplice --test), IsoQuant, SQANTI3, rMATS-long, DRIMSeq/stageR, skera; the shipped example runs from a clean copy for hifi, ont, drna and on real reads",
    "The microexon recipe (HiFi --junc-bed alone; ONT --junc-bonus 16) survives an independent two-way test on 12 sizes; the SKILL ships the checks (orientation, dangling junctions, pysam two-way snippet) that expose its own failure modes",
    "Measured, reproducible numbers replace prose claims (-uf false junctions, bonus table, IsoQuant unique_only, novel-site absorption); on independent data they reproduce",
    "rMATS-long block now fails loudly on truncated or empty inputs and recovers 20/20 planted DTU genes",
]
recs = [
 {"priority": "P2", "title": "uLTRA offered as an equivalent microexon route", "observed_in": [7],
  "problem": "Decision tree and 'Other routes' present uLTRA next to --junc-bed, backed by 150/150 on one 10-nt exon. On 14 microexon genes uLTRA lost 3-nt exons and the 4+12 tandem pair (0%), recovered 53-80% of 5-11 nt exons on ONT and dRNA (mean inclusion 76.6% ONT, 78.6% dRNA, 91.4% HiFi) against 99.6% for the recipe.",
  "root_cause": "A single-sequence measurement generalised into a peer recommendation.", "fix": "State the per-size range measured (or say uLTRA is weaker below ~12 nt and on ONT/dRNA) and drop 'or uLTRA' from the decision-tree row."},
 {"priority": "P2", "title": "flair diffSplice --test hides a failed event type", "observed_in": [1],
  "problem": "On real 6-sample data alt5 has events but none survive DRIMSeq's filter: R prints '!No genes left after filtering!' with a traceback, FLAIR exits 0 and writes no drimseq_alt5 file. The text only says empty event types are skipped.",
  "root_cause": "Only the empty-matrix case was documented.", "fix": "Add one sentence: an event type can also fail with '!No genes left after filtering!' (rc stays 0); check that drimseq_<event>_*.tsv exists for every event type you need."},
 {"priority": "P2", "title": "Microexon numbers depend on read error rate, which is not stated", "observed_in": [7],
  "problem": "Bonus 16 gives 99.1% / 99.2% for direct RNA at ~4% error but 93.2% / 94.9% at 7.2% error (4/12 genes < 90%, including a 27-nt exon); the table gives one figure per platform. Also on real LRGASP cDNA bonus 16 changes the chain of 5.8% of reads (109/1883, all to fully annotated chains, flair correct inconsistent 195 -> 214), whereas the text says 'changed nothing outside microexons' (true only for its planted set).",
  "root_cause": "Table measured on one error profile; the 'nothing outside microexons' sentence is scoped in parentheses but easy to over-read.", "fix": "Name the simulated error rates next to the table and say that on real reads the bonus also extends some reads by an annotated intron."},
 {"priority": "P2", "title": "Lima/isoseq status and adapter file name not verifiable", "observed_in": [8],
  "problem": "The text says lima did not finish on the toy BAM and that lima/isoseq are help-only; with a zm tag on the toy BAM skera -> lima --isoseq -> isoseq refine all ran (132 -> 132 -> 132). 'mas16_primers.fasta' cannot be confirmed from skera.how/adapters.",
  "root_cause": "The stall came from the toy BAM (S-read names movie/?/ccs/... without zm), not from lima; the file name was not checked.", "fix": "Say the toy BAM needed a zm tag, that skera -> lima -> refine ran on a synthetic array, and quote the file name only after fetching it."},
 {"priority": "P2", "title": "SKILL.md 38.8 kB / 580 lines, no references/; example not referenced", "observed_in": [],
  "problem": "Evidence paragraphs grew the file from 33 kB; microexon section, DTU code and failure modes load together. Neither SKILL.md nor usage-guide.md mentions examples/longread_splicing_pipeline.sh.",
  "root_cause": "Restructuring was deferred in both fix rounds.", "fix": "Move the microexon evidence and the DTU/rMATS-long blocks to references/, keep the recipe and the checks in SKILL.md, and link the example."},
]
report = {"meta": meta, "veto_gates": veto, "static_score": static_score, "dynamic_score": dyn, "final": final, "key_strengths": key_strengths, "recommendations": recs}
json.dump(report, open(OUT, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
print("static", sub, "exec avg", avg, "final", score, grade, "assertions", dyn["assertion_pass_rate"])

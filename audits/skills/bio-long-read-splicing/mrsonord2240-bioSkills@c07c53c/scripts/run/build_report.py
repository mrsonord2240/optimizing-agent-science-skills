#!/usr/bin/env python3
"""Builds eval_report_bio-long-read-splicing_result.json (re-audit of the fixed Skill) from the scores decided after the runs, and runs the schema
pre-emit checklist (cardinalities, sums, weighted scores, grade). Scores are the auditor's own; every number quoted in a note is from a log in run/logs."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "eval_report_bio-long-read-splicing_result.json")

import yaml, re as _re
_t = open(os.path.join(HERE, "skill_copy", "SKILL.md"), encoding="utf-8").read()
FM = yaml.safe_load(_re.match(r"^---\n(.*?)\n---\n", _t, _re.S).group(1))
assert FM["name"] == "bio-long-read-splicing"

def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}

meta = {
    "skill_name": "bio-long-read-splicing",
    "description": FM["description"],
    "source": "mrsonord2240/bioSkills@c07c53cbf60daee254c6a0ab56a859f07acf8ddf:alternative-splicing/long-read-splicing",
    "evaluated_on": "2026-09-20",
    "evaluator_version": "skill-auditor@1.0",
    "category": "Data Analysis",
    "execution_mode": "D",
    "complexity": "Complex",
    "n_inputs": 8,
    "mode": "re-audit of a fixed Skill (fix branch fix/as-longread); pre-fix report 68 Reject (Research Veto M4) archived under audits/_pre-fix-20260920/bio-long-read-splicing",
    "environment": "F:/OpenScience/audit-envs/alternative-splicing: WSL as-lr (FLAIR 3.0.1, IsoQuant 4.0.0, minimap2 2.31, pysam 0.23.3), as-sqanti (SQANTI3 6.0.2, uLTRA 0.1, deSALT), as-rmatslong (rMATS-long 2.1.0), as-pb (skera 1.4.0 / lima 26.2.1 / isoseq 26.2.0, --help only); Windows R 4.4.3 via r.sh / r-bambu.sh (bambu 3.8.3, DRIMSeq 1.34.0, stageR 1.28.0; argparse+findpython in a private lib under run/out, since deleted)",
    "data": "SYNTHETIC, auditor's own (seed 5150 60-gene chrQ genome with 20 planted DTU genes, a 7-nt and a 12-nt annotated microexon, two unannotated novel isoforms, GENCODE-like GTF with CDS/UTR/start_codon rows; HiFi, ONT cDNA unstranded and stranded, ONT direct RNA; seed 4242 microexon set 7/12/24 nt and seed 4343 size scan 4-21 nt, each with 200 inclusion + 200 skipping reads) plus the first auditor's archived synthetic sets (regression) plus REAL public data: LRGASP WTC-11 cDNA (FLAIR test set, hg38 chr12/17/20) and SG-NEx A549 ONT direct RNA (bambu extdata, chr9:1-1e6). All synthetic generators are in run/ (fully reproducible from the seeds).",
    "executed_summary": "8/8 inputs executed. Not executed: skera/lima/isoseq beyond --help (no Kinnex data); IsoQuant --illumina_bam only on the planted set; uLTRA/deSALT only on planted microexons; rMATS-long only on planted data; Bambu block run with ncore=1 (ncore=8 fails on this Windows R).",
}

veto = {
    "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
    "research_veto": {
        "applicable": True, "gate": "PASS",
        "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs, PMIDs or results. The measured numbers the fixer added (-uf 47-50% false-junction reads, 29% unoriented HiFi, ts:+ 1.000/0.501/0.503, 10-nt microexon 0/150 and 150/150) reproduced within noise on my own data: 48.2%, 30.5%, 1.000/0.502/0.503/0.493; the 10-nt figures reproduced exactly on the fixer's own set. Unsourced thresholds are labelled as such."},
        "practice_boundaries": {"result": "PASS", "detail": "Research tooling only; ALS cryptic-exon and ASO items are pointers, nothing diagnostic or prescriptive."},
        "methodological_ground": {"result": "PASS", "detail": "The -uf guidance and orientation check are correct and consistent in body, decision tree, usage-guide and example. One methodological weakness remains and is recorded as P1, not a principled fallacy: the microexon '--junc-bonus 20' recipe is validated on inclusion reads only and flips skipping reads to inclusion for some microexons (see P1)."},
        "code_usability": {"result": "PASS", "detail": "Re-judged from clean copies. The shipped example pipeline ran start to finish (exit 0, outputs asserted against planted truth) for PLATFORM=hifi, ont and drna on my own data, on the first auditor's data, and on real LRGASP/A549 reads; 9 of the 11 SKILL.md code blocks (alignment x2, microexon awk, FLAIR incl. diffSplice, IsoQuant, Bambu, SQANTI3 incl. CAGE/polyA, DTU, rMATS-long) were extracted verbatim and run; the install line was only dry-run solved and the skera block checked against --help. Remaining run-time defects are small: rMATS-long block lacks 'mkdir alignment_info' (P1), IsoQuant lists a file name that 4.0.0 does not write (P2), Bambu ncore=8 fails on Windows R (P2). No block needs a rewrite; borderline only for the rMATS-long omission."}
    }
}

static = {
    "functional_suitability": (9, 12, "All promised tools now have a working recipe (FLAIR, IsoQuant, Bambu, SQANTI3, DTU, diffSplice all ran verbatim). Deductions: rMATS-long block is not runnable as written (missing mkdir), microexon '--junc-bonus 20' rescue can convert skipping reads to inclusion, stale IsoQuant file name."),
    "reliability": (8, 12, "Failure modes are documented with measured symptoms (-uf, novel splice sites, SQANTI filter GTF, --test prerequisites). Gaps: rMATS-long silently writes empty tables when preprocessing fails; Common Errors rows for ssw-py, kallisto, prepareAnnotations and skera mismatches remain unverified."),
    "performance_context": (5, 8, "SKILL.md is 33 kB / 546 lines (about 8.3k tokens) with no references/ split; microexon evidence, DTU code and failure modes all load up front. Workflow itself is linear."),
    "agent_usability": (12, 16, "Cold-start clear: entry points, flags and file names match FLAIR 3.0.1/IsoQuant 4.0.0/SQANTI3 6.0.2, PLATFORM switch and env overrides in the example, orientation check with expected values. Contradictions on -uf are gone."),
    "human_usability": (6, 8, "Description is long but uses natural terms; strict input requirements are stated (manifest layout, file names, --out_dir must not exist)."),
    "security": (11, 12, "No credentials; local file tools only; example uses set -euo pipefail and quoted variables (PRESET intentionally unquoted, commented)."),
    "maintainability": (9, 12, "usage-guide reduced to overview/prompts with no lost content (checked against the pre-fix guide); versions pinned in Version Compatibility. SKILL.md remains monolithic."),
    "agent_specific": (15, 20, "Trigger description precise; example is composable via environment variables; escape hatches (when not to use -uf, when annotation is absent) stated. Progressive disclosure is weak: 546 lines, no references/."),
}
sub = sum(v[0] for v in static.values())
static_score = {"subtotal": sub, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}}

inputs = [
 dict(index=1, type="Canonical", label="Bulk FLAIR workflow (correct-collapse-quantify-diffSplice) on planted 3v3 HiFi (60 genes) and real LRGASP cDNA", status="COMPLETED",
      note="SKILL block runs verbatim on the merged BAM: 124/124 planted isoform chains recovered; diffSplice --test needs Rscript (absent in as-lr), its R half run through the env's Windows R recovered 20/20 planted genes",
      basic=33, specialized=52, assertions=[
        A("FLAIR block extracted verbatim from SKILL.md runs correct, collapse and quantify without edits on real LRGASP reads and on 6 planted samples", True, "rc 0 up to diffSplice on both; correct 49665 reads, 0 inconsistent (planted); real 1691 corrected / 195 inconsistent"),
        A("Collapsed isoforms recover every planted isoform chain including the two unannotated ones", True, "124 isoforms = 124 truth chains with --junction_tab; counts Pearson r 0.9998 (FLAIR vs truth, ctrl1 example)"),
        A("flair diffSplice --test result recovers the planted DTU genes (through the env's r.sh; Rscript/argparse are not in the WSL env)", True, "DRIMSeq ES events: 20/20 planted genes, 2 extra (G037, G042); real 6-sample data gave header-only tables (too few events)"),
        A("Orientation-check awk from SKILL.md gives ~0.5 on the real unstranded cDNA and matches the quoted 0.503", True, "ONT recipe 0.503, HiFi recipe 0.498 on LRGASP reads"),
        A("Prerequisites for --test are complete", False, "also needs python (R argparse -> findpython) and data.table; FLAIR's R script stops on empty alt3/ir tables (stopifnot class(gene_id))")]),
 dict(index=2, type="Variant A", label="IsoQuant and Bambu discovery + quantification (SKILL blocks) on planted reads; real ONT direct RNA (A549) with Bambu", status="COMPLETED",
      note="IsoQuant block verbatim rc 0, per-sample counts r 0.9988/0.9987; Bambu block needs ncore=1 on Windows R (r 0.999); stale IsoQuant output name",
      basic=32, specialized=49, assertions=[
        A("IsoQuant block (entry point isoquant, two FASTQ files, default prefix OUT) runs verbatim", True, "rc 0; outputs in isoquant_output/OUT/"),
        A("Per-sample transcript counts equal the planted truth", True, "sample1/sample2 Pearson r 0.9988/0.9987; G001A 54=54, 22=22; unannotated exon-skip isoform found and counted (37 of 40 reads)"),
        A("Every IsoQuant output file name given in SKILL.md exists", False, "OUT.transcript_model_counts.tsv is not written by IsoQuant 4.0.0 (novel counts are in OUT.discovered_transcript_counts.tsv); the other three names exist"),
        A("Bambu block yields transcript counts that match the planted truth and its NDR caveat holds", True, "ncore=1: r 0.9992/0.9989/0.9990 on 3 samples, no novel transcript at 8k reads with 'NDR approximated' warning as SKILL states; real A549: 105 transcripts, count 88; ncore=8 as written fails on this Windows R (BiocParallel: could not find function seqlengths)"),
        A("De novo mode (--genedb omitted, Decision Tree row) works", True, "121 models, 121/124 truth chains found incl. both unannotated isoforms")]),
 dict(index=3, type="Variant B", label="SQANTI3 classification and filtering: planted categories, FLAIR isoforms, real FLAIR isoforms with CAGE/polyA", status="COMPLETED",
      note="Block runs verbatim; 124/124 planted structural categories correct on FLAIR isoforms and 10/10 on the first auditor's query set; real run fills CAGE/polyA columns",
      basic=35, specialized=54, assertions=[
        A("SQANTI3 block (with the CAGE and polyA URLs the SKILL names) runs verbatim on real FLAIR isoforms", True, "both URLs return 200; rc 0; within_CAGE_peak TRUE 7/34, polyA_motif_found TRUE 17/34; filter 30 of 34 pass"),
        A("Structural categories match planted truth", True, "FLAIR isoforms: 122 FSM, unannotated skip = novel_in_catalog, unannotated +30-nt 5'ss = novel_not_in_catalog; first auditor's 10 query isoforms 10/10 (genic_intron is the correct label for the exon inside an intron)"),
        A("The filter step really needs the transcript/exon-only GTF the SKILL prescribes", True, "full IsoQuant GTF (CDS/UTR/codon rows) -> AssertionError, 0-line filtered GTF; awk-filtered GTF -> 673 lines"),
        A("Documented small-input behaviour (--skip_report) holds", True, "filter with --skip_report finished on 10, 34, 123 and 124 isoforms"),
        A("FSM >= 50% rule of thumb is flagged as annotation dependent", True, "real isoforms: 8/34 FSM, matching the SKILL's caveat")]),
 dict(index=4, type="Stress", label="Shipped examples/longread_splicing_pipeline.sh end to end from a clean copy: hifi, ont, drna (+SR_JUNCTIONS), first auditor's reads, real dRNA", status="COMPLETED",
      note="Exit 0 for every run; content asserted with pysam and truth chains; the pre-fix abort at isoquant.py and three later breaks are gone",
      basic=35, specialized=54, assertions=[
        A("Example runs to completion for PLATFORM=hifi, ont and drna on planted data, on the first auditor's synthetic reads and on real A549 direct RNA", True, "exit 0 in all 9 runs; real dRNA 129 reads -> 5 IsoQuant models, 5 FSM, 57-line filtered GTF"),
        A("Alignment content is right", True, "exact intron chains 91.5% / 82.7% / 64.9% (5'-truncated reads excluded), consistent sub-chain >= 99.3%, false-junction reads 0.0 / 0.0 / 0.1%; first auditor's data 95.6% / 96.0%, 0 false junctions"),
        A("Counts agree with planted truth", True, "FLAIR r 0.9996 / 0.9990 / 0.9935, IsoQuant r 0.9987 / 0.9950 / 0.9778 (unique_only leaves 87-426 reads in __ambiguous)"),
        A("GTF filtering handles CDS/UTR/start_codon rows", True, "IsoQuant GTF 1,645 rows incl. 546 CDS, 244 UTR, 122 start_codon; awk keeps 673 transcript/exon rows; SQANTI3 filter passes 123/123"),
        A("With SR_JUNCTIONS the example recovers unannotated splice sites that annotation-only correct drops", True, "FLAIR novel +30-nt 5'ss isoform 0/9 -> 9/9 (hifi), 9/9 (ont), 10/10 (drna); IsoQuant never calls it in annotation-guided mode (merged, as the SKILL warns)")]),
 dict(index=5, type="Scope Boundary", label="Differential isoform analysis on long reads: DTU block on FLAIR counts, flair diffSplice --test, rMATS-long ASM block", status="COMPLETED",
      note="DTU 20/20 and diffSplice --test 20/20 planted genes; rMATS-long block as written fails at 'alignment_info/' (missing mkdir) and then writes header-only tables; with mkdir 20/20",
      basic=28, specialized=45, assertions=[
        A("DTU DRIMSeq + stageR block runs verbatim on real FLAIR quantify output and recovers planted DTU genes", True, "60 genes tested; 20/20 planted recovered, 2 extra (G037, G042); on the real 6-sample LRGASP counts it runs to the end and returns NULL (no significant gene), as the block's comment says"),
        A("flair diffSplice --test (R half through r.sh) recovers planted DTU events", True, "22 significant ES events: 20/20 planted, same 2 extras"),
        A("rMATS-long block runs as written", False, "simplify_alignment_info.py aborts x6 with FileNotFoundError 'alignment_info/ctrl1.tsv': the block never creates alignment_info/"),
        A("rMATS-long ASM analysis recovers planted DTU once the directory exists", True, "adj p < 0.05: 25 genes called, 20/20 planted, 5 extra"),
        A("A failed preprocessing step is not silent", False, "after the six tracebacks the later commands still ran and wrote header-only coeff/count/differential tables (no error, no warning)")]),
 dict(index=6, type="Adversarial", label="Ambiguous library: unstranded ONT cDNA (or HiFi of unknown orientation) - which minimap2 recipe, is -uf right?", status="COMPLETED",
      note="Recipe is now consistent everywhere and every measured claim reproduces on own data, 4 platforms and real reads",
      basic=35, specialized=55, assertions=[
        A("No place still prescribes -uf for cDNA (body, decision tree, usage-guide, example)", True, "grep: -uf appears only for direct RNA, in warnings and in the orientation-check text"),
        A("Unstranded ONT cDNA: -uf makes half the reads carry a false junction", True, "48.2% false-junction reads, 42.2% exact chains with -uf vs 0.0% / 82.7% without (SKILL: 47-50%)"),
        A("Unoriented HiFi with splice:hq -uf: false junctions", True, "30.5% of reads (SKILL: 29%); oriented HiFi, stranded ONT and direct RNA identical with and without -uf"),
        A("Orientation-check awk separates oriented from unoriented reads", True, "1.000 HiFi, 0.502 ONT unstranded, 1.000 stranded ONT, 1.000 dRNA, 0.493 randomised HiFi, 0.503 real LRGASP"),
        A("On real unstranded cDNA -uf lowers the annotated-junction fraction as the SKILL states", True, "junction observations on annotated introns 97.5% -> 57.1% (SKILL: 92% -> 54-59% of reads)")]),
 dict(index=7, type="Edge", label="NEW: does a 4-24 nt microexon survive? Recipes from the Microexons section on my own planted microexons with a skipping-read control", status="COMPLETED",
      note="Recipes are runnable but the section's claims are size/platform dependent and its --junc-bonus 20 rescue flips skipping reads to inclusion (0/200) for several microexons",
      basic=28, specialized=40, assertions=[
        A("Plain minimap2 drops microexons as the SKILL states", False, "HiFi keeps microexons >= 10 nt without any junction file (10 nt 199/200, 12 nt 200/200, 24 nt 200/200) and loses <= 8 nt; ONT/dRNA lose everything up to 18 nt and keep 149/200 at 21 nt and 132/200 at 24 nt: the '10 nt = 0/150' figure is not general"),
        A("--junc-bed from an annotation containing the exon rescues HiFi inclusion reads without harming skipping reads", True, "200/200 inclusion and 200/200 skip at all 11 sizes tested (4-24 nt)"),
        A("--junc-bed alone 'rescues annotated microexons' on ONT / direct RNA", False, "ONT 0/200 at 4-7 nt, 132/200 at 8 nt, 193/200 at 10 nt; dRNA 0/200 at 4-7 nt, 86/200 at 8 nt"),
        A("--junc-bonus 20 rescue leaves skipping reads intact", False, "skip reads exact: 0/200 for the 4, 5, 10 nt (scan) and 7 nt (main set) HiFi microexons, 0/200 for 4 nt ONT and dRNA; the fixer's 10-nt sequence gave 150/150 both ways, so the section's inclusion-only check hides it"),
        A("6-column BED from the SKILL awk on a STAR SJ.out.tab layout and uLTRA both rescue inclusion", True, "awk output valid 6-column BED; inclusion 600/600 (with --junc-bonus 20, same skip caveat); uLTRA 596/600 HiFi, 544/600 ONT, 519/600 dRNA with skip reads >= 191/200; deSALT without annotation 0/200 inclusion at every size")]),
 dict(index=8, type="Edge", label="NEW: unannotated splice sites (30-nt donor shift and exon skip): FLAIR --junction_tab/--junction_bed, IsoQuant annotation-guided vs de novo vs --illumina_bam", status="COMPLETED",
      note="FLAIR failure mode and remedy reproduce exactly; IsoQuant merges the shifted site in annotation-guided mode and --illumina_bam does not change that",
      basic=35, specialized=53, assertions=[
        A("flair correct with only --gtf drops the unannotated-splice-site isoform (failure mode)", True, "0/9 reads corrected, 9 inconsistent"),
        A("--junction_tab and --junction_bed both recover it", True, "9/9 with either flag, 0 inconsistent; the SKILL awk BED works"),
        A("--junc-bed does not block novel junctions in the alignment", True, "reads of the unannotated skip isoform exact 37/40 (HiFi) 21/29 (ONT, 5' fragments), of the +30 nt isoform 8/9 on both"),
        A("IsoQuant annotation-guided merges a small novel shift into the annotated isoform, as stated", True, "no model with the planted +30 nt chain with or without --illumina_bam (short reads aligned with minimap2 splice:sr); de novo mode finds it (121/124 truth chains)")]),
]

for i in inputs:
    i["total"] = i["basic"] + i["specialized"]
    i["assertions_total"] = len(i["assertions"])
    i["assertions_passed"] = sum(1 for a in i["assertions"] if a["result"] == "PASS")
    i["status_flag"] = "✅" if (i["status"] == "COMPLETED" and i["total"] >= 75) else ("⚠️" if i["status"] == "COMPLETED" else "❌")
    assert 3 <= len(i["assertions"]) <= 5
    order = ["index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions"]
    for k in order: assert k in i

avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
ap = sum(i["assertions_passed"] for i in inputs); at = sum(i["assertions_total"] for i in inputs)
dyn = {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": ap, "total": at}, "inputs": [{k: i[k] for k in ["index", "type", "label", "status", "status_flag", "note", "basic", "specialized", "total", "assertions_passed", "assertions_total", "assertions"]} for i in inputs]}

sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = int(round(sw + dw))
grade, sym = ("Production Ready", "⭐") if score >= 85 else ("Limited Release", "✅") if score >= 75 else ("Beta Only", "⚠️") if score >= 60 else ("Reject", "❌")
l1 = sum(i["basic"] for i in inputs) / len(inputs); l2 = sum(i["specialized"] for i in inputs) / len(inputs)
final = {"static_weighted": sw, "dynamic_weighted": dw, "score": score, "max": 100, "grade": grade, "grade_symbol": sym, "deployable": True, "veto_override": False}

strengths = [
    "The pre-fix P0 is genuinely fixed: the shipped example runs end to end for hifi, ont and drna from a clean copy and its IsoQuant, FLAIR, SQANTI3 and filter outputs agree with planted truth (FLAIR counts r 0.99+, 124/124 SQANTI3 categories).",
    "The -uf guidance and orientation check are correct and consistent everywhere, and the measured figures reproduce on an independent simulation and on real LRGASP reads (48% / 30% false-junction reads; ts:+ 1.000 vs about 0.5).",
    "Long-read DTU block runs verbatim on real FLAIR quantify output and recovers 20/20 planted DTU genes; flair diffSplice --test also recovers them through Windows R.",
    "Failure modes are stated with measured symptoms and remedies that reproduce (FLAIR annotation-only correct loses unannotated sites, --junction_tab/--junction_bed recover them 0/9 -> 9/9; SQANTI3 needs a transcript/exon-only GTF).",
    "usage-guide dedup lost nothing needed: every removed tip, prerequisite or prompt is present in SKILL.md.",
]

recs = [
 dict(priority="P1", title="Microexon --junc-bonus 20 rescue flips skipping reads to inclusion", observed_in=[7],
      problem="The recipe is validated only by counting inclusion reads that carry both flanking junctions. On my own microexons the HiFi skip reads were aligned as inclusion for 4, 5, 7 and 10 nt (0/200 correct) and ONT/dRNA skip reads for 4 nt; --junc-bed alone was exact on HiFi at every size but leaves ONT/dRNA microexons below about 10 nt unrescued.",
      root_cause="Two annotated junctions x bonus 20 outweigh the mismatch cost of forcing a short exon into a skipping read; the fixer measured one 10-nt sequence and never checked the skipping isoform.",
      fix="State that the check must also count skipping reads (exact skip chain), recommend --junc-bed alone for HiFi, --junc-bonus 20 or uLTRA for ONT/dRNA only with that control, and make the 'plain minimap2 drops it' row platform- and size-specific (HiFi keeps >= 10 nt, ONT loses up to about 18 nt)."),
 dict(priority="P1", title="rMATS-long block omits mkdir alignment_info and fails silently downstream", observed_in=[5],
      problem="As written, simplify_alignment_info.py raises FileNotFoundError for all six BAMs, yet the later commands still run and write header-only differential tables with no error. With 'mkdir -p alignment_info' the same block recovers 20/20 planted DTU genes.",
      root_cause="The block has no mkdir, no set -e and no check that the per-sample TSVs exist; the first audit's harness had pre-created the directory.",
      fix="Add 'mkdir -p alignment_info', begin the block with set -euo pipefail and add a one-line check that alignment_info/*.tsv exist before organize_alignment_info_by_gene_and_chr.py."),
 dict(priority="P2", title="IsoQuant output list names a file that 4.0.0 does not write", observed_in=[2],
      problem="SKILL.md lists <prefix>.transcript_model_counts.tsv; IsoQuant 4.0.0 writes <prefix>.discovered_transcript_counts.tsv (and *_grouped_file_name_counts variants) instead.",
      root_cause="File names taken from an older IsoQuant release.", fix="Replace the name with discovered_transcript_counts.tsv and say which table holds the unannotated models."),
 dict(priority="P2", title="Bambu block uses ncore = 8 without a Windows note", observed_in=[2],
      problem="On Windows R the BiocParallel worker fails ('could not find function seqlengths') and the block stops; ncore = 1 works (r 0.999 vs truth).",
      root_cause="Multicore backend is not available on Windows.", fix="Add 'use ncore = 1 on Windows' beside the block."),
 dict(priority="P2", title="flair diffSplice --test prerequisites incomplete", observed_in=[1, 5],
      problem="Besides Rscript, DRIMSeq and argparse it also needs python for R's argparse (findpython), data.table, and FLAIR's R script aborts when an event table is empty.",
      root_cause="Prerequisite list written from the error text of one failed run.", fix="List python and data.table and note that empty event types make --test error out."),
 dict(priority="P2", title="SKILL.md is a 33 kB / 546-line monolith with no references/", observed_in=[],
      problem="Progressive disclosure is weak: microexon evidence, DTU code, failure modes and thresholds all load with every use (about 8.3k tokens).",
      root_cause="Evidence was added to the body during the fix; splitting was declared out of scope.", fix="Move the microexon evidence table, the DTU block and Per-Tool Failure Modes to references/ and keep decision tree, recipes and pointers in SKILL.md."),
 dict(priority="P2", title="Unverified Common Errors rows and unsourced thresholds remain", observed_in=[],
      problem="ssw-py, kallisto, prepareAnnotations and skera-mismatch rows were not reproduced by anyone; skera/isoseq were checked against --help only; QC thresholds are labelled unsourced.",
      root_cause="Failure text of the tools was not captured.", fix="Reproduce or delete the four rows; state that the Kinnex commands are help-verified."),
]

report = {"meta": meta, "veto_gates": veto, "static_score": static_score, "dynamic_score": dyn, "final": final, "key_strengths": strengths, "recommendations": recs}

# ---- pre-emit checklist
assert len(static_score["categories"]) == 8
assert static_score["subtotal"] == sum(v["score"] for v in static_score["categories"].values())
for k, v in static_score["categories"].items(): assert 0 <= v["score"] <= v["max"], k
assert len(dyn["inputs"]) == meta["n_inputs"]
assert 2 <= len(strengths) <= 5
assert [r["priority"] for r in recs] == sorted(r["priority"] for r in recs)
assert final["score"] == int(round(final["static_weighted"] + final["dynamic_weighted"]))
assert not any(v["result"] == "FAIL" for v in veto["research_veto"].values() if isinstance(v, dict))
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print("wrote", OUT)
print("static", sub, "exec avg", avg, "L1 avg %.1f L2 avg %.1f" % (l1, l2), "assertions", ap, "/", at, "final", score, grade)
print("per input", [(i["index"], i["basic"], i["specialized"], i["total"], i["assertions_passed"], i["assertions_total"], i["status_flag"]) for i in inputs])

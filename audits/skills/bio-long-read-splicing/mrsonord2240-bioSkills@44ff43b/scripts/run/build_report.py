#!/usr/bin/env python3
"""Builds eval_report_bio-long-read-splicing_result.json from the audit findings (values are hand-scored from the logs in run/logs)."""
import json, os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "eval_report_bio-long-read-splicing_result.json")


def A(text, ok, note):
    return {"text": text, "result": "PASS" if ok else "FAIL", "note": note}


inputs = []


def add(index, typ, label, status, flag_note, basic, spec, assertions, executed, exec_note):
    passed = sum(1 for a in assertions if a["result"] == "PASS")
    total = basic + spec
    flag = "\u2705" if (status == "COMPLETED" and total >= 75) else ("\u26a0\ufe0f" if status == "COMPLETED" and total >= 60 and passed >= len(assertions) / 2 else "\u274c")
    if status == "COMPLETED" and total < 75:
        flag = "\u26a0\ufe0f"
    if status != "COMPLETED":
        flag = "\u274c"
    inputs.append({
        "index": index, "type": typ, "label": label, "status": status, "status_flag": flag, "note": flag_note,
        "basic": basic, "specialized": spec, "total": total,
        "assertions_passed": passed, "assertions_total": len(assertions), "assertions": assertions,
        "executed": executed, "execution_note": exec_note,
    })


add(1, "Canonical", "Bulk HiFi/ONT: minimap2 splice recipe then FLAIR correct-collapse-quantify (3 v 3 planted isoforms + real LRGASP cDNA)",
    "PARTIAL", "SKILL's 'flair correct' line fails on FLAIR 3.0.1 (--genome, --shortread do not exist); works once fixed (7/7 planted isoforms exact with junction_bed)",
    27, 40, [
        A("minimap2 -ax splice:hq -uf --secondary=no (SKILL) aligns oriented HiFi-like reads with a correct intron chain", True, "pysam CIGAR check: 1723/1723 spliced, 95.0% exact chain + 5.0% contiguous 5' fragments, 0 false junctions"),
        A("`flair correct --query --genome --gtf --shortread --output --threads` exactly as in SKILL.md runs on FLAIR 3.0.1", False, "argparse rc=2 'unrecognized arguments: --genome ... --shortread ...'; 3.0.1 only has -q -f --junction_tab/--junction_bed -o -t; 2.0-2.2 accepted --genome/-j --shortread"),
        A("With the flags that exist (--junction_bed) correct->collapse->quantify reproduces planted counts", True, "all 7 planted isoforms recovered by exact intron chain, 0 of 3429 reads misassigned (compare_counts.py)"),
        A("Annotation-only correction (no short-read junctions) keeps a planted novel splice-site isoform", False, "GA.N2 (118 reads, novel acceptor 24 nt in intron) dropped as 'inconsistent'; its reads were counted in GA.1 (+17.1%)"),
        A("On real LRGASP cDNA reads the SKILL's -uf alignment feeds FLAIR as many corrected reads as FLAIR's expected output (1534)", False, "-ax splice:hq -uf: 972 corrected/851 inconsistent of 1823; same reads with -ax splice -k14: 1536 corrected (=expected 1534)"),
    ], True, "Ran in WSL as-lr: t1_align.sh, t2_flair_synth.sh, t2b_flair_sr.sh, t3_real_flair.sh, t3b_real_flair_k14.sh, t_compare_all.sh. flair diffSplice --test could not run in as-lr (no Rscript/DRIMSeq/argparse); event tables verified against planted counts")

add(2, "Variant A", "IsoQuant annotation-guided discovery + quantification (PacBio-style reads, 6 samples) and real ONT direct RNA",
    "PARTIAL", "`isoquant.py` is not an installed command (entry point is `isoquant`); with the entry point the run is exact for annotated isoforms, 2 of 3 novel found",
    28, 42, [
        A("`isoquant.py --reference --genedb --fastq ... --data_type pacbio_ccs ... --model_construction_strategy default_pacbio` runs as written", False, "exit 127 'isoquant.py: not found'; pip download shows entry_points isoquant=isoquant:main_entry (isoquant.py exists only in a git checkout)"),
        A("Same flags with the `isoquant` entry point finish and write OUT.transcript_models.gtf + counts", True, "IsoQuant 4.0.0 rc=0; --model_construction_strategy default_pacbio and --genedb optional both verified in --full_help / de-novo run"),
        A("Annotated isoform counts equal planted truth", True, "GA.2 852/852, GB.1 709/709, GC.1 551/551 (0.0% error)"),
        A("All planted novel isoforms are reported with correct counts", False, "novel skip-E2 found (136 vs 147 reads) and novel GB skip exact (360), but the 24-nt alternative-acceptor isoform (118 reads) is called FSM/'minor difference' and folded into GA.1 (+18.6%)"),
        A("Example-pipeline path isoquant/<prefix>/<prefix>.transcript_models.gtf matches the real layout for --bam + --prefix", True, "file present; repeat runs give identical count md5 (deterministic)"),
    ], True, "Ran as-lr isoquant 4.0.0: t4_isoquant.sh (synthetic FASTQ x6, BAM, de novo, ONT, real SG-NEx A549 chr9 slice), t12 determinism. Real-data assertion: 129 reads, bambu vs IsoQuant counts differ because IsoQuant default quantification is unique_only (not stated in SKILL)")

add(3, "Variant B", "Bambu joint discovery + quantification with NDR (SKILL R block) on synthetic BAMs and real ONT A549",
    "COMPLETED", "SKILL block runs as written under r-bambu.sh; NDR guidance not testable at toy scale (Bambu falls back to approximated NDR)",
    33, 47, [
        A("SKILL's prepareAnnotations()/bambu(NDR=0.1)/writeBambuOutput() block runs unmodified and returns a RangedSummarizedExperiment", True, "bambu 3.8.3 (xgboost 1.7.8.1 pin needed); 6 files written to bambu_output/"),
        A("`as.data.frame(assays(se)$counts)` and `transcriptToGeneExpression(se)` lines work", True, "both ok (bambu attaches SummarizedExperiment); gene-level RangedSummarizedExperiment 23 x 1 on real ONT data"),
        A("Annotated isoform counts equal planted truth", True, "GA.2 852, GB.1 709, GC.1 551 exact; GA.1 821 vs 692 because unreported novel reads are absorbed"),
        A("Default NDR=0.1 reports planted novel isoforms", False, "0 novel at 0.05 and 0.1, 1 at 0.3, 2 at 1.0; Bambu warns '<50 read classes ... NDR approximated' - SKILL gives no minimum-data guidance"),
        A("Real ONT run (bambu extdata) gives sane output", True, "105 transcripts, total count 88 at NDR 0.05/0.1/0.3 (127 of 129 primary reads overlap annotated exons); R exits with a segfault after output (environment)"),
    ], True, "Ran Windows R 4.4.3 via r-bambu.sh: t5_bambu.R, t5b_bambu_ndr.R, t6_bambu_real.R")

add(4, "Edge", "SQANTI3 classification and filtering of planted isoforms with known FSM/ISM/NIC/NNC/genic/antisense/intergenic categories",
    "COMPLETED", "10/10 planted categories correct; filter removed planted intra-priming isoform; report step and undocumented input files are the weak points",
    34, 51, [
        A("SKILL's sqanti3_qc.py command classifies 10 planted isoforms into their expected categories", True, "10/10 (FSM x3, ISM 3prime_fragment, NIC skip/retained intron, NNC novel splice site, genic_intron, intergenic, antisense)"),
        A("sqanti3_filter.py rules removes a planted intra-priming isoform and keeps the rest", True, "Q11 perc_A_downstream_TTS 100 > 59 filtered; 10 others pass"),
        A("SQANTI3 on FLAIR-collapsed isoforms (GTF and --fasta routes) gives the planted NIC/NNC/FSM labels", True, "7/7 both routes"),
        A("Every input the SKILL command needs can be obtained from the SKILL (--CAGE_peak refTSS file, --polyA_motif_list)", False, "no source/URL for either file; run stops with 'File refTSS_v3.3... not found. Abort!' (clear error, but unrecoverable from the SKILL)"),
        A("sqanti3_filter.py rules completes with exit 0 including its report", False, "filter tables written but report step fails in R (rc=1, tidyselect subscript error) on small input; --skip_report gives rc=0"),
    ], True, "Ran as-sqanti 6.0.2: t7_sqanti.sh, t7b_sqanti_more.sh, t12_real_sqanti.sh (real FLAIR isoforms: 36 models -> 7 FSM, 19 ISM, 2 NIC, 2 NNC, 5 antisense, 1 genic). ORF/CAGE/polyA/short-read arms not run (no matching data)")

add(5, "Stress", "Shipped examples/longread_splicing_pipeline.sh end to end from a clean copy (PLATFORM=hifi and ont)",
    "ERROR", "Aborts at line 44 (isoquant.py); three further breakages are hidden behind it (flair --genome, SQANTI3 --output dir, filter on IsoQuant GTF)",
    20, 25, [
        A("The shipped example runs to completion from a clean copy", False, "exit 127: 'isoquant.py: command not found' (set -e stops at first failure)"),
        A("With isoquant.py -> isoquant, the pipeline completes", False, "next stop: flair correct: unrecognized arguments: --genome"),
        A("With --genome removed, the pipeline completes", False, "sqanti3_qc.py --output longread_output_sample/sqanti3 -> FileNotFoundError writing qc_params (prefix with a directory is not supported; classification path in the script is also wrong)"),
        A("With SQANTI3 output fixed, sqanti3_filter.py accepts the IsoQuant GTF and writes the filtered GTF", False, "AssertionError raw[2]=='transcript' (IsoQuant transcript_models.gtf has 'gene' rows); filtered.gtf is 0 bytes; works after dropping gene rows"),
        A("PLATFORM=ont branch (splice -uf -k14) aligns unstranded ONT cDNA correctly", False, "46.2% exact chains, 51.5% reads with a junction absent from truth, gene strand wrong for 846/1665"),
    ], True, "Ran t10_example.sh with patch_example.py (4 cumulative stages), check_filter_gtf.sh for root cause")

add(6, "Scope Boundary", "Differential isoform analysis on long reads: rMATS-long ASM workflow and the DRIMSeq DTU block, 3 v 3 planted GA.1:GA.2 switch",
    "PARTIAL", "rMATS-long block runs as written and recovers the planted switch; the DTU R block does not run on FLAIR output as written",
    28, 41, [
        A("All seven rMATS-long commands with the SKILL's flags complete", True, "every step rc=0; flags verified against --help of each script"),
        A("rMATS-long recovers the planted GA exon-skipping switch and calls nothing else", True, "GA ASM 0_0: dPI 0.486 (planted 0.49), classified 'exon skipping', 1 significant gene; GB and GC unchanged"),
        A("The DTU R block runs on FLAIR quantify output as written", False, "file name flair_quantified_counts.tsv does not match FLAIR's <out>.counts.tsv; dmDSdata() stops: needs gene_id and feature_id columns, FLAIR writes 'ids' as <isoform>_<gene>; library(DEXSeq) after DRIMSeq masks results()"),
        A("After minimal repair the SKILL's dmFilter + DRIMSeq recovers planted DTU genes", True, "300-gene synthetic count matrix: 30/30 planted found, 6 false positives, stageR 36 genes / 84 transcripts (toy 2-gene FLAIR matrix cannot fit dmPrecision: p=0.41)"),
        A("Skill is internally consistent about rMATS-long inputs", False, "'rMATS-long: GTF-Only Input' failure mode says it rejects BAMs and needs per-sample isoform GTFs; the SKILL's own workflow feeds BAMs"),
    ], True, "Ran t8_rmatslong.sh (as-rmatslong 2.1.0), t9_dtu.R and t9b_dtu_sim.R (Windows R: DRIMSeq 1.34.0, DEXSeq 1.52.0, stageR 1.28.0). FLAIR diffSplice tables checked (inclusion/exclusion counts match planted); DRIMSeq step via a patched copy of FLAIR's R script (argparse missing)")

add(7, "Adversarial", "Ambiguous library: 'ONT direct cDNA, unstranded - which minimap2 recipe, and does it keep a 10-nt microexon?'",
    "PARTIAL", "Body recipe (splice -k14, no -uf) is right, but three other places say -uf, and the 'no aligner anchor problem' microexon claim is false without --junc-bed",
    24, 36, [
        A("The SKILL's stated ONT-unstranded recipe (-ax splice -k14, no -uf) gives correct junctions and strand", True, "94.7% exact chains, 1.1% false-junction reads, inferred strand 1665/1665 correct"),
        A("All guidance in the Skill agrees (Decision Tree, usage-guide 'What the agent will do', example script)", False, "three places prescribe `splice -uf -k14` for ONT cDNA: same reads then 46.3% exact / 51.5% false junctions / strand wrong for half; on real cDNA 1566 junctions (2.6% annotated) vs 242 (15.3%) without -uf"),
        A("Documented recipes keep a planted 10-nt microexon ('reads span the microexon; no aligner anchor problem')", False, "0/150 reads keep it with splice:hq and with splice -k14; downstream IsoQuant reports M.inc = 0 reads"),
        A("The Skill's pointer to --junc-bed is enough to rescue the microexon", True, "with --junc-bed 150/150 (HiFi) and 131/150 (ONT), 150/150 with --junc-bonus 20; SKILL mentions --junc-bed only for 'poorly-annotated genomes' and not for microexons"),
        A("Claim that long-read counts carry no quantification uncertainty holds", False, "IsoQuant marked 22 of 300 reads ambiguous in the microexon ONT run; FLAIR/IsoQuant assigned 118 novel-site reads to GA.1 (+17-19% error); 5' truncated reads are ambiguous by construction"),
    ], True, "Ran t1_align.sh, t11_microexon.sh (make_micro.py synthetic 10-nt microexon), t3_real_flair.sh (real cDNA). 'minimap2: too many anchors' string not found in the binary and -N sets retained secondaries [5], so the 'Common Errors' -N 50 advice is unfounded")

avg = round(sum(i["total"] for i in inputs) / len(inputs), 1)
apass = sum(i["assertions_passed"] for i in inputs)
atot = sum(i["assertions_total"] for i in inputs)

static = {
    "functional_suitability": (8, 12, "Broad coverage (alignment, FLAIR, IsoQuant, Bambu, SQANTI3, rMATS-long, DTU, single-cell). Correctness 2/4: flair correct --genome/--shortread (removed in 3.0), isoquant.py, contradictory -uf, false microexon claim, wrong Common Errors rows. Completeness 3/4: no BAM->BED12 or manifest format, no flair align"),
    "reliability": (7, 12, "Version-compatibility preamble and failure-mode sections exist, but several entries are wrong (flair correct 'genome not indexed', minimap2 'too many anchors'/-N 50); shipped example aborts at its first IsoQuant call with no fallback"),
    "performance_context": (5, 8, "One 488-line SKILL.md loads everything at once; usage-guide repeats the description and Skill content; no references/ split"),
    "agent_usability": (10, 16, "Decision tree and tables are clear, but Consistency 2/4 (-uf in four places, rMATS-long input contradiction, file-name mismatches) and Feedback 2/4 (few output formats or columns specified)"),
    "human_usability": (5, 8, "Natural, keyword-rich trigger text; rigid on version drift and offers no clarifying question about library strandedness or orientation"),
    "security": (11, 12, "No credentials, no eval of user strings, example writes only under its output dir; example does not validate inputs or quote variables"),
    "maintainability": (7, 12, "Single monolithic SKILL.md and one example that fails from a clean copy; no pinned tool versions or test data pointer (FLAIR/bambu test data exist upstream)"),
    "agent_specific": (14, 20, "Trigger text precise for long-read splicing; related-skill links all resolve (7/7 exist); single large file, no references, silent on when to stop or hand off"),
}
subtotal = sum(v[0] for v in static.values())

stat_w = round(subtotal * 0.4, 1)
dyn_w = round(avg * 0.6, 1)
score = int(round(stat_w + dyn_w))

recs = [
    {"priority": "P0", "title": "Shipped example pipeline aborts; 4 breakages in a row",
     "observed_in": [5], "problem": "examples/longread_splicing_pipeline.sh exits 127 at `isoquant.py`; after that fix it fails at `flair correct --genome`, then SQANTI3 `--output <dir>/sqanti3` (FileNotFoundError, wrong classification path), then `sqanti3_filter.py --filter_gtf` on IsoQuant's GTF (AssertionError, 0-byte output).",
     "root_cause": "Example was written against older tool CLIs and never run from a clean copy.",
     "fix": "Use `isoquant`, drop --genome, call SQANTI3 with `--output sqanti3 --dir $OUT/sqanti3` and classification at `$OUT/sqanti3/sqanti3_classification.txt`, strip `gene` rows from the IsoQuant GTF before filtering (or filter the SQANTI3 corrected GTF), and add a `--test` run on the FLAIR test set."},
    {"priority": "P0", "title": "Research Veto M4: documented FLAIR/IsoQuant commands do not run on current versions",
     "observed_in": [1, 2, 5], "problem": "`flair correct --genome --shortread` is rejected by FLAIR 3.0.1 (both flags existed only in 2.x although the Skill says 2.0+); `isoquant.py` is not installed by pip/conda (entry point is `isoquant`); the DTU block cannot read FLAIR's output as written.",
     "root_cause": "Flags copied from FLAIR 2.x docs and IsoQuant's git-checkout script name; Version Compatibility line claims 2.0+/3.5+ without a test.",
     "fix": "Rewrite FLAIR correct as `flair correct -q reads.bed -f anno.gtf --junction_bed|--junction_tab sr_junctions -o out -t N`, state the BAM->BED12 step (bedtools bamtobed -bed12 or flair align), use `isoquant`, pin tested versions (FLAIR 3.0.1, IsoQuant 4.0.0, SQANTI3 6.0.2, Bambu 3.8.3 needs xgboost 1.x)."},
    {"priority": "P1", "title": "-uf prescribed for unstranded ONT cDNA in three places",
     "observed_in": [5, 7, 1], "problem": "Body text says omit -uf for unstranded cDNA, but the Decision Tree, usage-guide workflow and example script use `splice -uf -k14` for ONT cDNA. On mixed-orientation reads -uf gave 51.5% reads with false junctions (synthetic) and 972 vs 1536 FLAIR-corrected reads (real cDNA). The HiFi recipe also needs orientation-corrected FLNC reads, not stated.",
     "root_cause": "Copy-edit left three older recipes; no orientation caveat on the HiFi recipe.",
     "fix": "Make every recipe agree: ONT cDNA `-ax splice -k14` (no -uf); -uf only for direct RNA or orientation-fixed FLNC/stranded preps; add one-line check (fraction of reads on each strand)."},
    {"priority": "P1", "title": "Microexon claim 'no aligner anchor problem' is false for minimap2",
     "observed_in": [7], "problem": "A 10-nt microexon was lost in 150/150 reads with both splice:hq and splice -k14, and IsoQuant then reported 0 reads for the inclusion isoform. --junc-bed rescued 100% (HiFi) / 87% (ONT), 100% with --junc-bonus 20.",
     "root_cause": "Claim assumes reads spanning the exon guarantees the aligner places it; --junc-bed is mentioned only for poorly annotated genomes.",
     "fix": "Rewrite the microexon row: needs annotation-guided alignment (--junc-bed, --junc-bonus 20) or uLTRA/deSALT, and say how to check (count reads with both flanking junctions)."},
    {"priority": "P1", "title": "DTU block does not run on FLAIR output",
     "observed_in": [6], "problem": "File name flair_quantified_counts.tsv (FLAIR writes <out>.counts.tsv), dmDSdata needs gene_id/feature_id while FLAIR has `ids` = <isoform>_<gene>, sample columns are <id>_<condition>_<batch>, and library(DEXSeq) after DRIMSeq masks results(). The block stops at dmFilter.",
     "root_cause": "Pseudo-code, never run on flair quantify output.",
     "fix": "Add the conversion (split ids, rename samples), use DRIMSeq::results(), and finish the DRIMSeq -> stageR chain (a 300-gene planted test recovers 30/30)."},
    {"priority": "P1", "title": "FLAIR annotation-only correct drops novel splice-site isoforms; the fix flag is wrong",
     "observed_in": [1, 2], "problem": "With only --gtf, FLAIR dropped a planted 24-nt novel-acceptor isoform (118 reads) and folded its reads into GA.1 (+17%); IsoQuant also merged it into GA.1. The Skill's remedy `--shortread short_read_junctions.bed` does not exist in 3.x (`--junction_bed`/`--junction_tab`; with it 7/7 isoforms exact).",
     "root_cause": "Novel-discovery claims not tested; flag from FLAIR 2.x.",
     "fix": "Document that novel splice sites need orthogonal junction support in FLAIR, that small (<~30 nt) site shifts are merged by default in IsoQuant, and give the working flag."},
    {"priority": "P1", "title": "Contradictory or overstated statements on inputs and uncertainty",
     "observed_in": [6, 7], "problem": "'rMATS-long: GTF-Only Input' says BAMs are rejected while the workflow above uses BAMs (which ran fine). 'Transcript identity is read-level, not inferred' ignores ambiguous and 5'-truncated reads (IsoQuant 22/300 ambiguous reads in the microexon run; counts off by up to 19%).",
     "root_cause": "Failure-mode prose written independently of the workflow.",
     "fix": "Delete or correct the rMATS-long failure mode; replace the no-uncertainty claim with 'assignment uncertainty is lower but not zero' and mention IsoQuant's unique_only default."},
    {"priority": "P2", "title": "SQANTI3 inputs and report step underspecified",
     "observed_in": [4], "problem": "No source for refTSS_v3.3 CAGE BED or mouse_and_human.polyA_motif.txt (run aborts on missing file); category table omits genic_intron; `sqanti3_filter.py rules` report step exits 1 on small inputs; SQANTI3 6 has no --skipORF (ORF off unless --include_ORF).",
     "root_cause": "Command copied without a run.",
     "fix": "Add download hints, list genic_intron, mention --skip_report/--report skip for quick runs."},
    {"priority": "P2", "title": "FLAIR diffSplice/quantify prerequisites and outputs misdescribed",
     "observed_in": [1, 6], "problem": "diffSplice --test needs Rscript + DRIMSeq + R argparse, which `pip install flair-brookslab` does not provide (failed in the tool env); output is inclusion/exclusion tables and DRIMSeq results with no plots; quantify manifest format (id, condition, batch, reads) is not given; 'flair correct slow: index the genome' is meaningless (correct takes no genome).",
     "root_cause": "Prose written from memory of FLAIR 2.",
     "fix": "State prerequisites, the manifest columns, the real outputs, and delete the bogus Common Errors rows (also `minimap2: too many anchors` / -N 50)."},
    {"priority": "P2", "title": "Unsourced numeric thresholds and unrun single-cell block",
     "observed_in": [], "problem": "Junction-concordance and accuracy figures and the FSM >=50% rule are unsourced (real FLAIR-test isoforms: 7/36 FSM); skera/lima/match_cell_barcode block was not executable here (tools absent) and match_cell_barcode flags could not be verified.",
     "root_cause": "Rules of thumb stated as thresholds.",
     "fix": "Cite or soften, and mark the single-cell commands as unverified or test them."},
    {"priority": "P2", "title": "Redundant usage-guide and monolithic SKILL.md",
     "observed_in": [], "problem": "usage-guide.md repeats the description and SKILL tips; SKILL.md is 488 lines with no references/.",
     "root_cause": "Single-file authoring.",
     "fix": "Move per-tool recipes to references/ and remove duplicated text (dedup pass)."},
]

report = {
    "meta": {
        "skill_name": "bio-long-read-splicing",
        "description": "Long-read (PacBio Iso-Seq/Kinnex, ONT cDNA and direct RNA) alternative-splicing analysis: minimap2 splice presets, FLAIR, IsoQuant, Bambu, SQANTI3 classification/filtering, rMATS-long and DTU on long-read counts.",
        "source": "mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/long-read-splicing",
        "evaluated_on": "2026-09-20",
        "evaluator_version": "skill-auditor@1.0",
        "category": "Data Analysis",
        "execution_mode": "D",
        "complexity": "Complex",
        "n_inputs": 7,
        "environment": "F:/OpenScience/audit-envs/alternative-splicing (WSL as-lr FLAIR 3.0.1/IsoQuant 4.0.0/minimap2 2.31, as-sqanti SQANTI3 6.0.2, as-rmatslong 2.1.0, Windows R 4.4.3 bambu 3.8.3 via r-bambu.sh, DRIMSeq 1.34.0)",
        "data": "synthetic (run/data/synth, synth_micro, planted truth, seed 20260920/777) plus real FLAIR-test LRGASP cDNA (hg38 chr12/17/20) and real SG-NEx A549 ONT direct RNA chr9 slice",
        "executed_summary": "7/7 inputs executed (each partly): not executed = skera/lima/isoseq3/match_cell_barcode single-cell block, flair diffSplice --test in the as-lr env (no R), SQANTI3 CAGE/polyA/short-read/ORF arms, uLTRA/deSALT, StringTie2 hybrid, FLAMES/scNanoGPS",
    },
    "veto_gates": {
        "skill_veto": {"gate": "PASS", "stability": "PASS", "contract": "PASS", "determinism": "PASS", "security": "PASS"},
        "research_veto": {
            "applicable": True,
            "gate": "FAIL",
            "scientific_integrity": {"result": "PASS", "detail": "No fabricated DOIs/PMIDs/trial data; citations (FLAIR, IsoQuant, Bambu Nat Methods 20:1187, SQANTI3 21:793, LRGASP 21:1349) are real. Unsourced rule-of-thumb percentages noted as P2, not fabrication."},
            "practice_boundaries": {"result": "PASS", "detail": "Research tooling only; ALS cryptic-exon and ASO mentions are pointers, no diagnostic or prescriptive statements."},
            "methodological_ground": {"result": "PASS", "detail": "No principled fallacy. The -uf-on-unstranded advice and the 'no quantification uncertainty' overclaim are contradictions/overstatements recorded as P1, not a mismatched model."},
            "code_usability": {"result": "FAIL", "detail": "Documented code is not runnable on current tools: flair correct --genome/--shortread rejected by FLAIR 3.0.1 (input 1); isoquant.py not installed (2, 5); shipped example aborts at line 44 and fails again at three later points (5); DTU block cannot read FLAIR output (6). Each reproduced from a clean copy with the error text captured."},
        },
    },
    "static_score": {"subtotal": subtotal, "max": 100, "categories": {k: {"score": v[0], "max": v[1], "note": v[2]} for k, v in static.items()}},
    "dynamic_score": {"execution_avg": avg, "max": 100, "assertion_pass_rate": {"passed": apass, "total": atot}, "inputs": inputs},
    "final": {"static_weighted": stat_w, "dynamic_weighted": dyn_w, "score": score, "max": 100,
              "grade": "Reject", "grade_symbol": "\u274c", "deployable": False, "veto_override": True},
    "key_strengths": [
        "SQANTI3 section is accurate: 10/10 planted categories and the intra-priming filter reproduced; FLAIR-to-SQANTI3 chain gave the planted NIC/NNC/FSM labels",
        "rMATS-long ASM workflow: all seven commands and flags are correct and recovered the planted exon-skipping switch (dPI 0.486 vs 0.49)",
        "Bambu R block runs as written and NDR direction is right (0.05 stringent to 1.0 permissive)",
        "Decision tree, platform matrix and pitfalls list are useful; the body's ONT-unstranded recipe (no -uf) is correct; all seven Related Skills resolve",
    ],
    "recommendations": recs,
}

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(report, f, indent=2, ensure_ascii=False)
print("wrote", OUT, "static", subtotal, "avg", avg, "score", score, "assertions", apass, "/", atot)
for i in inputs:
    print(i["index"], i["type"], i["basic"], i["specialized"], i["total"], i["status"], i["status_flag"], i["assertions_passed"], "/", i["assertions_total"])

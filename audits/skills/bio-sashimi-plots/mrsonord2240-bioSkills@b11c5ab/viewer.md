> **Audit record for `bio-sashimi-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@b11c5ab](https://github.com/mrsonord2240/bioSkills/tree/b11c5abf964aa7a7f49acc37dc8e051ea875c4d7/alternative-splicing/sashimi-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-sashimi-plots (RE-AUDIT of the fixed Skill)

Generated: 2026-09-20 | Re-auditor: a third agent (not the first auditor, not the fixer)
Source: `mrsonord2240/bioSkills@b11c5abf964aa7a7f49acc37dc8e051ea875c4d7:alternative-splicing/sashimi-plots`
(copied byte-identical into `run/skill/`, SHA-256 checked; the worktree was never written to).
Pre-fix report (archived `_pre-fix-20260920`): **67, Reject, Research Veto M4 fired (P0)**.
This audit: **88, Production Ready, deployable, no veto, no open P0/P1**.

Category: Data Analysis | Mode: D (Python + CLI tools) | Complexity: Complex, N = 8
Inputs 1-6 re-run the pre-fix inputs as regression tests (pre-fix input 3, edge semantics, is folded into input 1); inputs 7 and 8 are new.
The fix log was not used as evidence; every number below comes from a run in `run/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression, + edge + ggplot2 pin) | 36 | 56 | 92 | 5/5 PASS | ✅ |
| 2 | Variant A (regression: batch, Ensembl contigs) | 35 | 54 | 89 | 5/5 PASS | ✅ |
| 3 | Variant B (regression: rmats2sashimiplot + forced failures) | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 4 | Stress (regression: ENCODE 12 BAM, 3 groups, strand) | 35 | 54 | 89 | 4/4 PASS | ✅ |
| 5 | Scope Boundary (regression: pyGenomeTracks + regtools) | 33 | 50 | 83 | 4/5 PASS | ✅ |
| 6 | Adversarial (regression: leafviz, Jutils, install, VOILA) | 33 | 50 | 83 | 4/5 PASS | ✅ |
| 7 | Variant B (NEW: MXE, plus and minus strand, real chrX) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 8 | Edge (NEW: low-junction-count real region) | 34 | 52 | 86 | 3/4 PASS | ✅ |

**Execution average 88.0 / 100** | Static 88 / 100 | **Final 88 (35.2 + 52.8)** | Assertions 34/37 (91.9 %)
Floors (Production Ready): static 88 >= 80, execution 88.0 >= 85, Layer 1 avg 34.8 >= 32, Layer 2 avg 53.2 >= 48, assertions 91.9 % >= 90 %. All met.
Executed 8/8 (the VOILA commands inside input 6 were not run: MAJIQ/VOILA is licence-gated; only its public docs were read).

## Method and independent truth

- `run/scripts/jtruth.py` is my own pysam CIGAR scan (no ggsashimi code). It builds per-group, per-junction expected labels (plain mean over the samples that have the junction and pass -M, Python `round`, half to even) and asserts they occur among the SVG `<text>` strings (`LABELS_OK n/m`). For rmats2sashimiplot and Jutils the label text was read from the PDF.
- Envs: WSL `as-viz-gg34` (R 4.2.3, ggplot2 **3.4.4**, the Skill's pin), `as-viz-gg35` (3.5.2), `as-viz` (4.0.3). `run/bin/ggsashimi.py` is a PATH shim so the Skill's bare `ggsashimi.py` calls resolve to the ggsashimi 1.1.5 clone in the chosen env.
- Every SKILL.md fenced block was extracted (`scripts/extract_blocks.py` -> `run/blocks/`) and run literally; only file names, regions and BAM lists were substituted with `sed`. `py_compile`/`ast.parse` and `bash -n` pass on every block and on `examples/plot_sashimi.py` (`out/i7.txt`).
- Data: synthetic planted 3v3 exon-skipping set (`public-data\planted`), real GEUVADIS chrX 2 GBR v 2 YRI BAMs (Ensembl contig `X`, rMATS writes `chrX`), the 12 real ENCODE BAMs of ggsashimi's example. rMATS-turbo 4.4.0 was re-run for both (`scripts/prep_rmats.sh`); leafcutter output for leafviz was regenerated (`i6a_leafviz.sh`).
- Note on `jtruth.py`: it counts every alignment record, secondary included, because ggsashimi does (input 4). Its first version skipped secondary alignments; the checks made before that change (inputs 1, 2) matched anyway, so those regions contain no secondary records.
- Every figure listed as viewed was opened with the image reader (PNG, or the PDF page). Large SVGs (up to 74 MB) and merged BAMs were deleted.

---

## Input 1 - Canonical (regression of pre-fix inputs 1 and 3) - ggsashimi overlay, edge semantics, ggplot2 pin
**Prompt:** "Plot a sashimi for the exon-skipping gene G1 (chrP) with control vs treatment groups, intron shrinking and matched y-axis scales." Then: what do -M, -C, -A, -s do, and what fails silently?
**Ran:** `scripts/i1_skill_block.sh` (block 02 verbatim: pdf, svg, png), `i1b_ggplot_bisect.sh` (3 envs x png/svg), `i1c_edge.sh` (12 runs), `i1d_help_median.sh`.
**Output:**
```
[pdf] rc=0 18346 bytes   [svg] rc=0 679517   [png] rc=0 124189
Control    201-501  counts=[40,44,38]  mean_j=40.67->41      Treatment 201-501 counts=[10,12,9]  10.33->10
Control    201-901  counts=[10,10,12]  10.67->11             Treatment 201-901 counts=[40,40,38] 39.33->39
Control    601-901  counts=[40,36,42]  39.33->39             Treatment 601-901 counts=[10,8,11]   9.67->10
LABELS_OK 6/6            (gg3.4.4, gg3.5.2, gg4.0.3: all LABELS_OK 6/6)
-M default per --help: 1     -M 10 -> Treatment 201-501 label 11 (rep3=9 drops out), LABELS_OK 6/6
```
**Viewed:** ggplot2 3.4.4: blue/orange groups, gene-model exons line up with the arc feet, x ticks 0/200/851/1092 visible. ggplot2 3.5.2 and 4.0.3: the gene model is shifted left of the coverage (exon 1 ends at x 629 vs arc foot at 696) and the tick labels are clipped; arc labels unchanged. The Skill's "needs ggplot2 < 3.5" claim is right, and 3.5.2 already breaks (the first audit blamed 4.x).
**Edge runs (`out/i1c/`):** wrong BAM among good ones: rc 0, sample dropped; all BAMs wrong: rc 1 "ERROR: No available bam files."; contig `1`: rc 1 "ValueError: invalid contig `1`"; `-A mean` without `-O`: rc 1 "Cannot apply aggregate function if overlay is not selected."; region without reads: rc 0 and an SVG; `--shrink` with -M 100: rc 1 `RuntimeError: generator raised StopIteration`; without --shrink: rc 0; bad palette: rc 0 and no file ("Error in geom_bar()"); no `-C`: grey; `-C 3` without `-P`: red/green (viewed); `-s SENSE`: `j_strand_+.png` and `_-.png`; `-s MATE1_SENSE` on single-end: `TypeError: unsupported operand type(s) for ^: 'NoneType' and 'bool'`; `median_j` labels 40 10 40 / 10 40 10 = medians.
**Scores:** Basic 36 | Specialized 56 | Total 92
- [PASS] block runs verbatim, non-empty PDF - 18,346 B
- [PASS] labels = independent pysam means - 6/6
- [PASS] colours and alignment under 3.4.4, pin claim reproduces - viewed
- [PASS] corrected defaults and claims reproduce - list above
- [PASS] silent-failure claims reproduce - all four seen

## Input 2 - Variant A (regression of pre-fix input 2) - batch recipes on Ensembl-contig data
**Prompt:** "Iterate ggsashimi over the significant rMATS SE events; output per-event PDFs with 500 nt flanks."
**Ran:** `i2a_skill_batch.sh` (blocks 02+03 in sequence, planted then real chrX, pdf and svg), `i2a_check.py` (labels per event), `i2b_example_driver.py` (examples/plot_sashimi.py from `run/skill`).
**Output:**
```
[planted pdf] rc=0  G1_chrP_100_0.pdf 19443 B          region chrP:1-1500 (start 100-500 clamped to 1)  LABELS_OK 6/6
[real pdf]    rc=0  DMD 59537 | GEMIN8 29428 | PDZD11 27053 | RP11-357C3.3 595606 | TAZ 32670 (rMATS chrX, BAM contig X)
real: RP11-357C3.3 (-) 8/8 | PDZD11 (-) 5/5 | GEMIN8 (-) 6/6 | DMD (-) 4/4 | TAZ (+) 7/7
example: match_contig(chrX) -> X ; batch_plot_rmats_events: 1 planted + 5 real PDFs; PDZD11 svg LABELS_OK 5/5
plot_specific_event(real PDZD11 region) -> specific_pdzd11.pdf
FAIL-PATH bad_contig -> ValueError: contig 'chr99' is not in the header of every BAM
FAIL-PATH empty_region -> ValueError: no reads in chrP:2000-2500 in any BAM
FAIL-PATH bad_region_str -> ValueError ; missing_bam -> FileNotFoundError ; bad_palette -> RuntimeError: ggsashimi exited 0 but wrote no figure
WARNING: no junction has >= 100 reads ...; dropping --shrink  -> figure written
```
**Viewed:** `PDZD11_chrX_69509104_143.pdf` (minus-strand gene, real): GBR one arc "6", YRI arcs 2, 3, 2, 1, gene-model exons aligned.
Block 03 alone is not self-contained (uses `groups`, `sashimi_groups.tsv`, `palette.txt` from block 02; it says "groups = the TSV above").
**Scores:** Basic 35 | Specialized 54 | Total 89
- [PASS] block writes a non-empty figure per event on Ensembl-contig data
- [PASS] contig mapping and start clamp
- [PASS] every figure label equals the pysam count - 36/36
- [PASS] example batch/specific/plot functions run and raise on bad input
- [PASS] every recipe has a post-run figure-exists check

## Input 3 - Variant B (regression of pre-fix input 4) - rmats2sashimiplot and the figure-exists assert
**Prompt:** "Plot the significant rMATS SE events with rmats2sashimiplot, Control vs Treatment colours."
**Ran:** `i3_rmats2sashimi.sh` (block 04 verbatim on planted and real chrX; variants A-D from `i3_variants.py`), `i3b_tool_rc.sh`, `i3_truth_real.sh`.
**Output:**
```
[planted] block rc=0  sashimi_rmats/Sashimi_plot/1_G1_chrP_101_200_+@chrP_501_600_+@chrP_901_1000_+.pdf  27925 B
[real]    block rc=0  5 PDFs: RP11-357C3.3 817068 | PDZD11 25892 | GEMIN8 82676 | DMD 157162 | TAZ 23714
[failA] no --group-info line, 2 colours for 6 replicates : "Error: Must provide sample label and color for each entry in bam_files!"  block rc=1 "rmats2sashimiplot wrote 0 of 1 figures"
[failB] --group-info nofile.gf : FileNotFoundError ... block rc=1 "wrote 0 of 1"
[failC] -t SE : "unrecognized arguments: -t SE" block rc=1 "wrote 0 of 1"
[failD] one colour : same Error, rc=1 "wrote 0 of 1"
tool exit codes without the assert:  A rc=0 pdfs=0 | B rc=0 pdfs=0 | C rc=2 pdfs=0
6 explicit colours without --group-info: rc=0, 1 PDF
```
**Viewed:** planted PDF text `41 / 11 / 39 / G1 Control IncLevel: 0.79 / 10 / 39 / 10 / G1 Treatment IncLevel: 0.20`, axis 101 184 508 591 916 999 (matches the planted exons, no coordinate shift). Real TAZ and PDZD11 PDFs: labels equal pysam means with zeros included in the mean (PDZD11 YRI inclusion-side arcs 1 = mean(2,0), 2 = mean(2,1) = 1.5 -> 2, and the skipping arc 3), half to even (TAZ 0.5 -> 0).
**Scores:** Basic 36 | Specialized 55 | Total 91
- [PASS] one PDF per event (1/1, 5/5)
- [PASS] labels and IncLevel match independent counts and rMATS
- [PASS] assert fires on four forced failures
- [PASS] documented error text and exit codes reproduce
- [PASS] chrX events plot against contig-X BAMs

## Input 4 - Stress (regression of pre-fix input 5) - real ENCODE locus, 3 groups, strand
**Prompt:** "Three cell types, 12 real BAMs, chr10:27,040,584-27,048,100: publication overlay, aggregate per group, split by strand."
**Ran:** `i4_encode.sh`, `i4b_recheck.sh`, `i4c_strand.sh`.
**Output:**
```
overlay -O 3 -C 3 -P palette(3 colours) -A mean_j -M 1 --shrink --fix-y-scale : svg 873400 B, png 522731 B
first check skipping secondary alignments: LABELS_OK 2/10 (BAMs hold 43-178 secondary records each)
counting every alignment record:            LABELS_OK 10/10 aggregate ; 12/12 per-sample (Endothelial x4)
e.g. Endothelial 27040713-27044584 counts [153,179,72,100] -> 126 ; Mesenchymal 27044671-27047991 [130,136,336,202] -> 201
-s SENSE -> st_SENSE_+.svg 98 203 110 | 125 228 165 | 11 124 43 | 71 127 82 ; _-.svg 55 50 80 | 54 40 108 | 61 14 24 | 29 43 65
independent per-strand counts (jtruth --strand SENSE) identical ; ANTISENSE files swap + and -
```
**Viewed:** three tracks green / orange / purple (palette order = order of first appearance), y-axis 0-750 on all three (`--fix-y-scale`), gene model aligned, labels 126 207 169 / 265 115 186 (+1 on the 1-read arc) / 258 35 201.
**Scores:** Basic 35 | Specialized 54 | Total 89
- [PASS] three-group overlay, colours, y-scale, alignment
- [PASS] aggregate and per-sample labels = pysam (secondary records counted)
- [PASS] -s SENSE/ANTISENSE routing = independent per-strand count
- [PASS] arc-count interpretation agrees with the tool (P2: Skill says "reads", tool counts alignment records)

## Input 5 - Scope Boundary (regression of pre-fix input 6) - pyGenomeTracks with regtools arcs
**Prompt:** "Combine RNA-seq coverage and junction arcs for one locus in a multi-track figure."
**Ran:** `i5_pgt.sh` (blocks 08, 09, 10, 11 verbatim in `as-viz-gg34`; planted and real chrX XS-tagged BAMs), `i10_error_rows.sh`.
**Output:**
```
[planted] b08 rc=0 (125 bedGraph lines per group) ; b10 rc=0 junctions.bedpe:
chrP 200 201 chrP 499 500 153 | chrP 200 201 chrP 899 900 150 | chrP 600 601 chrP 899 900 147
   pysam sums over 6 replicates: 40+44+38+10+12+9=153, 10+10+12+40+40+38=150, 40+36+42+10+8+11=147
[planted b11 pdf] rc=0 13922 B   png 16775 B        [real b11 pdf] rc=0 13967 B   png 17724 B (4,712 BEDPE lines)
real PDZD11:  X 69509204 69509205 X 69509708 69509709 19 | ... 69509370 69509371 3 | 69509443 69509444 ... 2   (pysam 7+6+3+3, 2+1, 2+0)
pgt with `file_type = bam`: InputError "the file_type bam does not exists" ; no file_type: "can not identify file type. Please specify the file_type"
regtools on an unindexed BAM: rc 1 (usage/error), no BED
```
**Viewed:** planted figure: coverage with empty introns (`-split`), the two control/treatment tracks, arcs land on the exon edges. The junction track is cropped at its lower edge (height = 2): the arcs are cut off. Real figure: coverage max about 10, so `max_value = 200` in the sample ini hides it (the Skill says to pick `max_value` from the data).
**Scores:** Basic 33 | Specialized 50 | Total 83
- [PASS] four blocks run verbatim
- [PASS] BEDPE scores = pysam sums
- [PASS] intron gaps and arcs on exon edges
- [FAIL] junction arcs fully visible - cropped at the junction track's bottom edge
- [PASS] BAM-track error rows match the observed messages

## Input 6 - Adversarial (regression of pre-fix input 7) - leafviz, Jutils, install lines, VOILA
**Prompt:** "Validate a leafcutter cluster interactively, make a tool-agnostic Jutils view of my rMATS output, set the tools up, and browse a MAJIQ LSV with VOILA."
**Ran:** `i6a_leafviz.sh` (regtools -> leafcutter clustering -> `leafcutter_ds.R` are prerequisites; then block 06), `i6b_jutils.sh` (block 07, planted + real), `i6c_venn_check.py`, `i9_misc_claims.sh`, `i7_static_install.sh`; MAJIQ docs fetched with curl.
**Output:**
```
leafcutter_ds effect sizes  chrP:200:901:clu_1_+ deltapsi 0.5446 (skip intron)   [same as TOOLS.md 0.5446]
gtf2leafcutter.pl -> annot_{all_exons,all_introns,fiveprime,threeprime}.*.gz ; prepare_results.R -> leafviz.RData (creating PCA)
cd leafcutter/leafviz && Rscript run_leafviz.R /abs/leafviz.RData -> "Listening on http://127.0.0.1:3595"  curl 200 24497  <title>LeafViz</title>
run_leafviz.R from another directory -> "App dir must contain either app.R or server.R." ; requireNamespace("leafviz") FALSE, leafcutter TRUE
prepare_results.R wrong prefix -> "Error: WRONGPREFIX_all_introns.bed.gz does not exist"
Jutils planted: convert -> rmats_JC_results.tsv / rmats_JCEC_results.tsv ; heatmap "number of rows < 2 ... Skipping" (1 event) ; sashimi labels 40,44,38 | 10,10,12 | 40,36,42 ; 10,12,9 | 40,40,38 | 10,8,11 (= pysam) ; venn ok
Jutils real chrX: heatmap clustermap*.pdf (16 events, viewed) ; sashimi ; venn 5 / 19 / 9 (my recount by gene: 5 / 18 / 9)
venn --tsv-file-list a.tsv,b.tsv -> FileNotFoundError (comma list is not a file)
conda: micromamba create --dry-run solve rc=0 : r-base 4.2.3, r-ggplot2 3.4.4, rmats2sashimiplot 4.0.0, pygenometracks 3.9, regtools 1.0.0
"No entries matching ggsashimi" / "jutils" on conda-forge+bioconda ; git ls-remote finds guigolab/ggsashimi, splicebox/Jutils, davidaknowles/leafcutter
```
**VOILA (not run, licence-gated):** the text states so and hedges the splicegraph name. Public MAJIQ V3 docs (`biociphers.bitbucket.io/majiq-docs/v2-to-v3.html`): V2 `voila view splicegraph.sql psi.voila`; V3 `voila view sg.zarr <file>.psicov <group>.sgc`. The Skill block has no `.sgc` for V3 (P2). The old `-o` option and the Zarr/"changing" claims were removed; no unsupported claim remains.
**usage-guide.md dedup:** compared with the archived pre-fix guide: installs, prompts, tips (--shrink, --fix-y-scale, -O 3 -A mean_j, 3-4 groups, flanks, MXE, IGV) all live in SKILL.md now; only the V3 "splicegraph.zarr" hint of the VOILA tip is stated generically. Nothing needed was lost.
**Scores:** Basic 33 | Specialized 50 | Total 83
- [PASS] leafviz end to end, app answers HTTP 200
- [PASS] `library(leafviz)` does not exist; wrong-dir error reproduces
- [PASS] Jutils four subcommands run, sashimi labels = pysam, comma-list error reproduces
- [PASS] install lines solve; clone URLs exist; ggsashimi and Jutils not on conda
- [FAIL] VOILA block complete for MAJIQ V3 (.sgc missing per public docs; hedged as not run)

## Input 7 - Variant B (NEW) - MXE events on real chrX, plus and minus strand
**Prompt:** "Show the mutually exclusive exon events from my GBR v YRI rMATS run; both alternative exons must be visible."
**Ran:** `i7_run.sh` -> `i7_mxe.py` (top-4 MXE rows by FDR: only 2 of 17 pass FDR < 0.05 in a 2v2 set, so the awk FDR filter of block 04 was replaced by "top 4").
**Output:**
```
(a) MXE rows 17: upstreamES..downstreamEE contains both alternative exons in 17 of 17 rows
events: TAZ(+) 0.0002, JPX(+) 0.0002, TAZ(+) 0.0061, IRAK1(-) 0.0867
ggsashimi TAZ_50 X:153641318-153648585 LABELS_OK 19/19 | JPX_30 X:73163918-73219179 11/11 | TAZ_49 19/19 | IRAK1_37 X:153277993-153282595 16/16
rmats2sashimiplot --event-type MXE rc=0; PDFs 4 of 4 (assert: OK)
```
**Viewed:** IRAK1 (minus strand) PNG: arcs across both alternative exons, gene model aligned.
**Scores:** Basic 36 | Specialized 55 | Total 91
- [PASS] MXE span claim - 17/17
- [PASS] ggsashimi labels = pysam - 19/19, 11/11, 19/19, 16/16
- [PASS] rmats2sashimiplot MXE writes 4/4 figures
- [PASS] plus and minus strand genes drawn correctly

## Input 8 - Edge (NEW) - low-junction-count real region
**Prompt:** "Plot the DMD exon-skipping event (reads are sparse), raising -M to declutter as the Skill suggests."
**Ran:** `i8_run.sh` -> `i8_sparse.py` (DMD X:31136844-31152811, 0-3 reads per sample and junction).
**Output:**
```
a_M1  -M 1 --shrink : rc 0  GBR 31140048-31144759 [1,2]->2 ; 31144791-31152219 [1,2]->2 ; YRI [1,0]->1 ; [1,3]->2    LABELS_OK 4/4
b_M5_shrink: rc 1 StopIteration            c_M5_noshrink: rc 0, no junction drawn, jtruth expects 0 labels (0/0)
plot_sashimi guard: "WARNING: no junction has >= 5 reads ...; dropping --shrink" ; plot_specific_event -> d_specific.pdf 184137 B (no arcs)
```
**Viewed:** -M 1 figure: arcs 2, 2, 1, 2 over coverage; gene model present.
**Scores:** Basic 34 | Specialized 52 | Total 86
- [PASS] -M 1 labels = pysam, half to even (1.5 -> 2)
- [PASS] documented --shrink crash reproduces
- [PASS] example guard writes the figure with a warning
- [FAIL] an arc-free figure is flagged - rc 0 and a coverage-only figure at -M 5; the guard only mentions --shrink

## Research Veto (re-judged from scratch)

```
Scientific Integrity  : PASS  no fabricated values; every quantitative claim tested reproduced
Practice Boundaries   : PASS  visualisation only
Methodological Ground : PASS  aggregation, per-sample -M before -A, strand routing verified
Code Usability        : PASS  ggsashimi block, batch block + example, rmats2sashimiplot SE/MXE (+ forced failures),
                              leafviz (HTTP 200), Jutils 4 subcommands, pyGenomeTracks + regtools, install lines (dry-run solve):
                              all ran or solved; VOILA not run (licence-gated), hedged in the text
```
The first audit's M4 failure (`-t SE`, `run_leafviz()`, comma venn list, unrunnable install line, batch recipes failing on chrX vs X) is gone: each was re-tested and now works or is corrected. Nothing the fix changed broke another recipe.

## Final

```
Static 88 x 0.4 = 35.2 | Dynamic 88.0 x 0.6 = 52.8 | FINAL 88 | GRADE Production Ready | deployable: yes | veto: none
Open P0: 0 | Open P1: 0 | P2: 5 (pgt arcs cropped; VOILA V3 .sgc; no warning for arc-free figure; ggsashimi.py must be on PATH; batch block state + secondary reads)
```

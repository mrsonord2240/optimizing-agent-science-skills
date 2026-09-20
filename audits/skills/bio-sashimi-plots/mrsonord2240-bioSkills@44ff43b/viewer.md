> **Audit record for `bio-sashimi-plots`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@44ff43b](https://github.com/mrsonord2240/bioSkills/tree/44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b/alternative-splicing/sashimi-plots) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-sashimi-plots

Generated: 2026-09-20 | Source: mrsonord2240/bioSkills@44ff43bb35e5741c3ddd3c003590e1f1da8a4a4b:alternative-splicing/sashimi-plots
Category: Data Analysis | Mode: D (hybrid) | Complexity: Complex (6 tools, branching, 3 files) -> N = 7
Env: `F:\OpenScience\audit-envs\alternative-splicing` (ggsashimi 1.1.5 GitHub clone, rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, Jutils clone, regtools 1.0.0, pysam 0.24.1, ggplot2 4.0.3).
All scripts are in `run/scripts/`, outputs in `run/out/`, data in `run/data/` (planted data = **synthetic**, from `public-data\planted`; real data = ENCODE example and GEUVADIS chrX from `public-data`). The Skill was run from a copy in `run/skill/`; no `__pycache__` in the source clone or the copy.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: ggsashimi grouped overlay (planted) | 34 | 47 | 81 | 2/5 | warn |
| 2 | Variant A: batch from rMATS hits | 24 | 31 | 55 | 1/5 | fail (PARTIAL) |
| 3 | Edge: -M, defaults, missing BAM, bad contig | 24 | 34 | 58 | 2/5 | warn |
| 4 | Variant B: rmats2sashimiplot | 26 | 36 | 62 | 2/5 | fail (PARTIAL) |
| 5 | Stress: real 10-BAM locus + strand | 34 | 51 | 85 | 3/5 | pass |
| 6 | Scope: pyGenomeTracks + regtools BEDPE | 32 | 46 | 78 | 2/5 | warn |
| 7 | Adversarial: leafviz / VOILA / Jutils | 24 | 30 | 54 | 1/5 | fail (PARTIAL) |

**Execution average 67.6 | static 67 | final 67 (would be Beta Only) | Research Veto M4 FAIL -> grade Reject, not deployable | assertions 13/35 | executed 7/7 (input 7: MAJIQ/VOILA not executed, licence-gated)**

Layer averages: L1 28.3/40, L2 39.3/60.

## Ground truth used
`run/scripts/junction_truth.py` (pysam, per-read, 1-based donor = first intron base) on the planted BAMs gives, per replicate, junction 201-501 / 201-901 / 601-901:
G1: 40/10/40, 44/10/36, 38/12/42. G2: 10/40/10, 12/40/8, 9/38/11 (matches `expected.json` and regtools scores). Real data: same script on the ENCODE BAMs and chrX BAMs; strand counts from `strand_truth.py`.

## Static veto and score
T1-T4 PASS (deterministic, no eval/shell, list-argument subprocess). Two runs of the same call give identical labels.
Static 67/100: functional 8/12, reliability 6/12, performance 6/8, agent usability 9/16, human usability 6/8, security 10/12, maintainability 8/12, agent-specific 14/20 (notes in the JSON).

## Input 1 - Canonical (executed)
**Prompt:** "Plot a sashimi for the G1 locus with control vs treatment, intron shrinking, matched y scales, grouped by condition." Code: SKILL.md "ggsashimi for Publication Overlays" block verbatim (`scripts/i1_canonical.py`, paths and sample names changed), called with `-F pdf`, `-F svg`, `-F png`.
**Output:** rc 0; PDF 18,738 B. SVG text: Control `41 | 11 | 39`, Treatment `11 | 39 | 10`.
**Checks:** 41 = round(mean(40,44,38)), 11 = round(10.67), 39 = round(39.33) (correct). Treatment: 201-501 true mean 10.33 but drawn 11, 601-901 true 9.67 drawn 10, because `-M 10` (per-sample, applied before `-A mean_j`) removes the 9- and 8-read replicates (`i3_edge.txt`, cases d/d0: `-M 1` gives 10/39/10).
**Looked at the image** (`out/i1_G1_sashimi.png`): all coverage and arcs gray (no `-C`); `i1c_color.png` with `-C 3` gives red/green, not the Skill's blue/orange. Gene model panel is offset from the coverage panels (arc endpoints do not meet exon edges), with or without `--shrink` (`i1b_noshrink.png`); tick labels clipped. The upstream reference figure (`out/upstream_ref_example2.png`) is aligned and this environment's rerender (`out/i5_example2.png`) is not, with identical labels: attributed to ggsashimi 1.1.5 on ggplot2 4.0.3.

## Input 2 - Variant A: batch from rMATS hits (executed)
Real chrX 2v2 rMATS SE output (5 events pass FDR<0.05 and |dPSI|>0.1), grouping TSV of the 4 real BAMs.
- `scripts/i2a_skillmd_batch.py` (SKILL.md block verbatim): `CalledProcessError` at event 1, `ValueError: invalid contig 'chrX'` (BAM contig is `X`). 0 figures.
- `scripts/i2b_example_batch.py` (`examples/plot_sashimi.py` unmodified): "Plotting top 5 ... Failed to plot" x5, returns normally, `os.listdir` = `[]`. `plot_specific_event(... 'X' ...)`: `ERROR: Cannot apply aggregate function if overlay is not selected`, CalledProcessError.
- `scripts/i2d_planted_batch.py` on the planted rMATS file: region `chrP:-400-1500`, ggsashimi exits 1.
- `scripts/i2e_plot_fn.py` (`plot_sashimi` itself, `-F svg`): "Sashimi plot saved", per-sample labels `40 10 40 | 44 10 36 | 38 12 42 | 10 40 10 | 12 40 8 | 9 38 11` = truth exactly.
- `scripts/i2c_fixed_region.sh` (contig hand-corrected to `X`, PDZD11 event): label 6 for reads 7 and 6 (mean 6.5, R rounds half to even); rMATS SJC 7,6 and pysam 7,6 agree. YRI junctions (3,3 reads) vanish under the recipe's `-M 5`.

## Input 3 - Edge (executed, `scripts/i3_edge.sh`, `out/i3_edge.txt`)
```
(a) default -M      labels 9 38 11        -> default is 1 (Skill says default 10)
(b) -M 10, 10 reads labels 40 10 40       -> inclusive (>=)
(c) -M 11           labels 40 40
(d) group, -M 11    41 12 39 | 12 39 11   (true means 40.67 10.67 39.33 | 10.33 39.33 9.67)
(e) bad contig      rc=1 ValueError: invalid contig `1`
(f) typo BAM path   rc=0, sample silently dropped
(f2) all BAMs bad   rc=1 ERROR: No available bam files.
(g) -A without -O   rc=1 ERROR: Cannot apply aggregate function...
(h) empty region    rc=0, empty figure
```

## Input 4 - Variant B: rmats2sashimiplot (executed, `scripts/i4.sh`, `i4e.sh`, `i4h_real.sh`)
- Skill command verbatim: `rmats2sashimiplot: error: unrecognized arguments: -t SE` rc 2.
- `--event-type SE` + `--color '#1f77b4,#ff7f0e'`, per-replicate: "Error: Must provide sample label and color for each entry in bam_files! Provided 6 labels, 6 BAMs, 2 colors", **rc 0, Sashimi_plot empty**.
- `--group-info group_def.txt` (file the Skill never defines): FileNotFoundError, `mv: cannot stat`, **rc 0, no figure**.
- With a valid `grouping.gf` (`Control: 1-3` / `Treatment: 4-6`): PDF text `41 | 11 | 39 | G1 Control IncLevel: 0.79 ... 10 | 39 | 10 | G1 Treatment IncLevel: 0.20`; without groups (6 colours) per-replicate labels equal the truth exactly. Image `out/r2s_d.png`: blue/orange, arcs at exon edges, aligned.
- Real chrX (PDZD11): `chrX` in the rMATS file vs `X` contig handled automatically (also with `--remove-event-chr-prefix`); labels 6 (GBR), 3/2/1 (YRI), IncLevel 0.00/0.27 (rMATS mean 0.274).

## Input 5 - Stress: real ENCODE locus and strand (executed)
`scripts/i5.sh` + `i5_check.py`: Skill flags with `-j` on ggsashimi's 12-row real example (chr10:27040584-27048100): `(a) per-sample junction BED == pysam (>= 10): True (36 sample-junction pairs, 12 samples)`; `(b) all expected labels present: True` (126 207 169 / 265 115 186 / 258 35 201, same as the upstream figure).
`scripts/i5b_strand.sh`: planted single-end: `-s SENSE` puts all 3 junctions on `_+`, `ANTISENSE` on `_-` (file names `prefix_+.svg`, `prefix_-.svg`, undocumented); `-s MATE1_SENSE` on unpaired reads: `TypeError: NoneType ^ bool`. Real PE chrX: `MATE2_SENSE`/`MATE1_SENSE` give 3 on each strand, equal to `strand_truth.py` (3/3).

## Input 6 - Scope: pyGenomeTracks (executed, `scripts/i6_pgt.sh`, `i6b.sh`)
regtools 1.0.0 BED12 `chrP 175 525 ... 40 + ... 25,25 0,325` -> Skill awk -> `chrP 200 201 chrP 499 500 40` (and 200/899, 600/899): equals pysam introns 201-500, 201-900, 601-900. Skill ini verbatim (bigwigs built by me with `bedtools genomecov -split -bga` + pyBigWig): rc 0, "3 were links plotted", PDF 20,270 B; image `out/i6_pgt.png` shows arcs starting/ending on exon edges. BAM track: `InputError ... can not identify file type`. Coverage y ranges 67.72 vs 56.17 (unlinked). First bigwig (no `-split`) filled introns with coverage; the Skill has no bigwig recipe.

## Input 7 - Adversarial: leafviz, VOILA, Jutils (executed except VOILA)
- Jutils `convert-results --rmats-dir`: writes `rmats_JC_results.tsv` and `rmats_JCEC_results.tsv` (Skill: `rmats.tsv`); PSI 0.8,0.8,0.769,0.2,0.2,0.208, dPSI 0.587.
- Jutils `sashimi` with the Skill's exact flags: correct labels `40,44,38 / 10,10,12 / 40,36,42` and `10,12,9 / 40,40,38 / 10,8,11` (`run/data/jut/sh1/sashimi.png`).
- `venn-diagram --tsv-file-list a.tsv,b.tsv`: rc 1 `FileNotFoundError` (needs a file of paths); with a list file rc 0.
- `requireNamespace("leafviz")` FALSE; no `run_leafviz` in leafcutter; `prepare_results.R --help` matches the Skill's flags but the launcher is `Rscript run_leafviz.R x.RData`.
- `micromamba search -c bioconda`: `No entries matching "ggsashimi"`, none for `jutils`; rmats2sashimiplot 4.0.0 and pygenometracks 3.9 exist.
- MAJIQ/VOILA: not executed (licence-gated); public docs list `voila view` options (`-p`, `-j`, `--host`, ...) with no `-o`.

## Shipped-means-present (gate 8)
`examples/plot_sashimi.py` exists and its `plot_sashimi`/`create_grouping_file` run; `batch_plot_rmats_events` and `plot_specific_event` do not work as written on the data used. `group_def.txt`, `annotation_codes`, `ctrl_merged.bw` are referenced and never defined or explained (primary tools ggsashimi and rmats2sashimiplot exist and run).

## Research Veto
M1 PASS, M2 PASS, M3 PASS, **M4 FAIL** (headline snippets for rmats2sashimiplot, leafviz, Jutils venn and the install line are unrunnable as written; batch recipes fail on real data; details in the JSON).

## Recommendations (see JSON for full text)
P0: rmats2sashimiplot block (-t SE, silent no-output, undefined group file); leafviz/Jutils-venn/install/voila-`-o` nonexistent commands.
P1: batch recipes (contig prefix, negative start, silent failure, plot_specific_event); wrong defaults/colour/aggregation statements; ggplot2 4.x layout regression not bounded; exit-0 failure modes; pyGenomeTracks BAM/bigwig/y-scale.
P2: unsupported coordinate-shift claim, MATE*_SENSE on single-end, file-name sanitising, rounding.

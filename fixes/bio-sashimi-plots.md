# Fix log: bio-sashimi-plots (alternative-splicing/sashimi-plots)

## 2026-09-20 (fixer: Sonnet; branch `fix/as-sashimi`, worktree `F:\OpenScience\wt\as-sashimi`)

First audit: 67, Reject (Research Veto M4). Files changed: `SKILL.md`, `usage-guide.md`, `examples/plot_sashimi.py`. Frontmatter `name` unchanged; `description` changed only to drop "interactive HTML" (VOILA) and add "licence-gated".

Tool versions used: ggsashimi 1.1.5 (GitHub `a6d3c81`), rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, Jutils 1.5 (`400c10f`), leafcutter/leafviz 0.2.9 (`2c9907e`), regtools 1.0.0, samtools 1.24, bedtools 2.31.1, pysam 0.24.0, R 4.2.3 + ggplot2 3.4.4 (new env `as-viz-gg34`), R 4.4.3 + ggplot2 4.0.3 (`as-viz`), R 4.4 + ggplot2 3.5.2 (`as-viz-gg35`). Data: planted 3v3 set, real chrX GBR/YRI BAMs (contig `X`; rMATS says `chrX`), ggsashimi ENCODE example. Independent count: pysam CIGAR scan.

Every `SKILL.md` code block was extracted and run literally from a clean copy (only file names and the toy region substituted); `examples/plot_sashimi.py` run from a clean copy through a driver (7 cases incl. failure paths). `py_compile` and `bash -n` pass; no `.R` files changed.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| rmats2sashimiplot block: `-t SE` rejected; exit 0 and empty `Sashimi_plot/` on colour/group mistakes; `group_def.txt` never defined | P0 | `--event-type SE`, `grouping.gf` (`Control: 1-3`), awk event filter, `--color` explained, assert `n PDFs == n events` | ran: planted (PDF text `41 / 11 / 39 / IncLevel 0.79`), real chrX 5 events (5 of 5); forced failure (2 colours, no group file) prints the tool error, rc 0, and the assert fires ("wrote 0 of 5") | with `--group-info`, extra/missing colours were tolerated in the tests |
| `library(leafviz)` / `run_leafviz()` do not exist; annotation code unexplained | P0 | script-directory workflow: `gtf2leafcutter.pl` -> `prepare_results.R` -> `cd leafviz && Rscript run_leafviz.R /abs/x.RData`; "standalone jackhump/leafviz" sentence deleted | ran on planted leafcutter output: annotation files, `.RData`, Shiny "Listening on http://127.0.0.1:5125", curl HTTP 200 | `run_leafviz.R` fails outside `leafviz/` ("App dir must contain either app.R or server.R"): documented |
| Jutils venn comma list; `rmats.tsv` name | P0 | list file `path<TAB>label`; real output names `rmats_JC_results.tsv` / `rmats_JCEC_results.tsv`; `--out-dir`, `--pdf`, meta/bam-list formats | ran convert, heatmap, sashimi (labels `40,44,38 / 10,10,12 / 40,36,42`, `10,12,9 / ...` = pysam), venn; comma list reproduced the `FileNotFoundError` | heatmap needs >= 2 events after cutoffs (1-event planted file: "Skipping"; tested on a 3-row synthetic copy). leafcutter/MntJULiP/MAJIQ converters follow `--help` only |
| `conda install ggsashimi jutils` finds nothing | P0 | install block: bioconda for rmats2sashimiplot/pyGenomeTracks, `git clone` for ggsashimi/Jutils, conda R 4.2 + ggplot2 3.4.4 line | `micromamba search`: no entries for ggsashimi/jutils, hits for the other two; the conda line was executed to build `as-viz-gg34` and all tests ran in it | install text moved from `usage-guide.md` |
| `voila view -o` (no such option; view serves a browser); Zarr/`--changing-*` claims | P0 | `-o` removed, section reworded as a viewer, splicegraph name left generic, MAJIQ/VOILA marked licence-gated and not run; "Browser Memory" failure mode and `voila: out of memory` row deleted | not verifiable: MAJIQ/VOILA licence-gated, not installed. Checked against the audit's reading of public docs only | hedged, not proven |
| Batch recipes fail on `chrX` vs `X`, start < 1, silent failure; `plot_specific_event` used `-A` without `-O` | P1 | `bam_contig()` maps the name to the BAM header; `max(1, start)`; file exists and non-empty assert; sanitised names with event ID; example rewritten (`match_contig`, `junction_counts`, `plot_sashimi` validation, failed-event `RuntimeError`, relative BAM paths resolved against the TSV, `plot_specific_event` uses `-O 3 -A mean_j`) | ran literal SKILL block on planted (start -400 clamped) and 5 real chrX events; driver: labels = pysam (planted `41/11/39, 10/39/10`; ENCODE 12 BAMs `126 207 169 / 265 115 186 / 258 35 201`; PDZD11 `6 / 2 3 2 1`); error paths (bad contig, empty region, missing BAM, R failure) all raise | found on the way: `--shrink` crashes (`generator raised StopIteration`) when no junction passes `-M` (also with `-s` when a strand has none); the example drops `--shrink` with a warning, SKILL documents it. Example batch default `-M` 5 -> 1 (3 of 5 real events had no junction >= 5) |
| ggsashimi defaults/claims wrong: default `-M`, "edit colours in TSV", `mean_j` "sample-wise normalization", `-M` per-sample bias, `-s` file names | P1 | `-M` default 1 (inclusive, per sample before `-A`); `-C 3 -P palette.txt` added to the example; without `-C` grey, `-C` alone red/green; `mean_j` = rounded plain mean of raw counts (half to even); `-s` gives `_+`/`_-` files | ran: `-M 1` labels `41/11/39 / 10/39/10` (= round of pysam means); the `-M 10` result (`11/39/10`, 10.33 -> 11) is the audit's run, consistent with the source (per-sample filter before aggregation); images viewed (blue/orange with palette, grey without); `-s SENSE` gives `pl_strand_+.svg`/`_-.svg` | all against ggsashimi `--help` + source (`ggsashimi.py` aggregation code) + runs |
| ggplot2 layout regression not bounded | P1 | version line + install pin `ggplot2 < 3.5` (3.4.4 tested), "look at the figure" instruction, Common Errors row | rendered planted and ENCODE example with ggplot2 3.4.4 (aligned, ticks visible), 3.5.2 and 4.0.3 (gene model shifted, ticks clipped) | the audit blamed 4.x; 3.5.2 already breaks. Arc labels are unaffected in all |
| exit-0 failure modes not called out; Common Errors table wrong | P1 | new "Silent Failures" section; every recipe checks BAM paths and figure existence; table rebuilt from observed messages (`invalid contig`, `No available bam files.`, `Cannot apply aggregate...`, `StopIteration`, rmats2sashimiplot label/colour error, pgt `InputError`, Jutils `FileNotFoundError`, leafviz app dir, `prepare_results.R` "does not exist") | reproduced each message: bad palette gives rc 0 and no file; missing R package gives rc 0 and no file | the `'samtools' not found` row was wrong (ggsashimi uses pysam and `R`), replaced |
| pyGenomeTracks: BAM track, no bigwig recipe, unlinked y | P1 | BAM claim replaced by the error; `samtools merge` + `genomecov -split -bga` bedGraph recipe (`file_type = bedgraph`), `min_value/max_value` on both tracks, regtools extract with the missing `samtools index` step | ran: figure viewed (coverage gaps at introns, arcs on exon edges); BEDPE scores 153/150/147 = pysam per-junction sums over 6 replicates | regtools silently wrote nothing on an unindexed BAM: index step added |
| rmats2sashimiplot coordinate-shift claim unsupported; `MATE*_SENSE` on single-end crashes; unsanitised file names; half-even rounding | P2 | shift failure mode deleted; `MATE*_SENSE` marked paired-end only with the `TypeError`; `re.sub` sanitising; rounding stated in the `mean_j` bullet | plotted planted event: PDF axis `101 / 184 / 508 / 591 / 916 / 999` and event id `chrP_101_200 ...` match the planted exons (no shift); `MATE1_SENSE` on single-end reproduced the `TypeError`; PDZD11 mean 6.5 drawn as 6 | |
| leafviz "NMD-aware" / "NMD annotation" | P2 (found) | deleted from description of tool row, section goal, usage prompt | `grep -i nmd` over `leafviz/*.R`, `*.sh`, `server.R`, `ui.R`, `www`: no hits | |

## Findings not fixed

- MAJIQ-VOILA commands: cannot be run (licence-gated, not installed). Left as a hedged, generic `voila view` block that says it was not run.
- Jutils leafcutter / MntJULiP / MAJIQ converters: not run (only rMATS input tested); documented as following `--help`.
- ggsashimi `--shrink` crash itself is an upstream bug; worked around in the example and documented, not patched.

## Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| `usage-guide.md` Prerequisites (pip/conda/devtools/MAJIQ/Jutils installs) | `SKILL.md` Version Compatibility (install block, corrected) and leafviz / VOILA section intros |
| `usage-guide.md` "What the Agent Will Do" (5 steps) | restated the Decision Tree, flag list and batch section; not kept |
| `usage-guide.md` Tips (`--shrink`, `--fix-y-scale`, `-O 3 -A mean_j`, 3-4 groups, flanks, MXE, VOILA input, IGV) | `SKILL.md` flag list, Best Practices, VOILA section, tool matrix |
| `usage-guide.md` Quick Start prompts on VOILA / Jutils, "NMD annotation" | Example Prompts (kept, VOILA hedged) |
| `SKILL.md` Customization Reference table | flag bullets in the ggsashimi section (`--shrink`, `--fix-y-scale`, sizes, `-F`, palette via `-C/-P`, `-M`, `--alpha`, GTF pre-filter) |
| `SKILL.md` Best Practices rows `--fix-y-scale`, `-O 3 -A mean_j`, explicit output format | same flag bullets |
| `SKILL.md` "Color convention" paragraph | ggsashimi flag list (last bullet) |
| `SKILL.md` "rmats2sashimiplot: Wrong Coordinate Convention" | deleted (not reproducible; see P2 row) |
| `SKILL.md` "MAJIQ-VOILA: Browser Memory" and `voila: out of memory` row, Zarr/V3 claim | deleted (unverifiable); VOILA section states it was not run |
| `SKILL.md` "Standalone alternative: jackhump/leafviz" | deleted (leafviz ships in the leafcutter repo; verified) |
| `SKILL.md` Common Errors rows `samtools not found`, `KeyError 'IJC_SAMPLE_1'`, `leafviz: missing exon file` | replaced by the observed-message rows |
| `SKILL.md` Troubleshooting "Default `-M 10`", "`-A mean_j` fixes y-axis" | corrected / removed |

Disagreements resolved by the audit's runs: `-M` default (Skill 10, tool 1); `mean_j` "sample-wise normalization" (plain mean); "3.5+" ggplot2 (needs < 3.5).

## Env created

`as-viz-gg34` (WSL `science`, micromamba): R 4.2.3, ggplot2 3.4.4, data.table, gridExtra, gtable, scales, svglite, pysam 0.24.0, samtools 1.24, rmats2sashimiplot 4.0.0, pyGenomeTracks 3.9, seaborn, scikit-learn, pandas. Also `as-viz-gg35` (R 4.4, ggplot2 3.5.2) for the version bisect. Scratch: `F:\OpenScience\as-sashimi-scratch\`.

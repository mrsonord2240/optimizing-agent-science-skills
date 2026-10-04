# Tooling: bio-workflows-crispr-screen-pipeline (recut router)

- Mode: full. Date: 2026-10-04.
- Candidate: `F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline`, tree identity `e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d` (`skill_preflight --offline --shape` PASS, 19 files). Bytes untouched.
- Ecosystem root: `F:\OpenScience\audit-envs\crispr-screen-analyst\` (INDEX row `workflows/crispr-screen-pipeline`). Shared tool notes, patches and traps: its `TOOLS.md` (sections 2 and 6). Public inputs: its `public-data\README.md`.
- Routing cases: `routing-cases.json` beside this file (11 cases, one per route of the first table; data under `public-data\derived\crispr-pipeline\<route>\`, built by `make_inputs.py` there).
- Run evidence: `F:\OpenScience\fix-evidence\recut-crispr-pipeline\tooling\<route>\` (logs, outputs).

## Environment and activation

Native Windows, except cn-correction (WSL). Reason: CRISPRcleanR does not build natively (ecosystem TOOLS.md section 3); Docker is not used by this phase; WSL `science` env `crispr-ccr` builds it from conda-forge/bioconda.

| Env | Activate | Fingerprint |
|---|---|---|
| Shared Windows venv | `export PATH=/f/OpenScience/audit-envs/crispr-screen-analyst/Scripts:$PATH` (Git Bash) | Python 3.12.13, pandas 3.0.5, numpy 2.5.3, scipy 1.18.1, matplotlib 3.11.1, MAGeCK 0.5.9.5 (`mageck`, RRA.exe built from source), pyvenv.cfg sha256 34c507e6f299 |
| BAGEL2 / drugZ / JACKS | `...\tools\dl\bagel\BAGEL.py`, `...\tools\dl\drugz\drugz.py`, `...\tools\dl\JACKS\jacks\run_JACKS.py` (run with shared python; numpy-2/pandas-CoW/scipy patches recorded in ecosystem TOOLS.md) | BAGEL2 build 115, drugZ 2026-09 HEAD, JACKS 0.2 |
| Chronos venv | `...\tools\chronos-venv\Scripts\python.exe` | crispr-chronos 2.3.15, tensorflow 2.21.0, numpy 2.5.3, pandas 3.0.5 (import `chronos`) |
| CRISPRcleanR (new 2026-10-04) | WSL: `MSYS_NO_PATHCONV=1 timeout 580 wsl -d science -- bash -l <script.sh> > log 2>&1 < /dev/null`; inside, `/home/sci/micromamba/envs/crispr-ccr/bin/Rscript` | CRISPRcleanR 3.0.1 (git HEAD 2026-10-04), R 4.4.3, Rqc 1.40.0, Rsubread 2.20.0, VariantAnnotation 1.52.0; full list `...\tools\ccr-wsl\env-list.txt` (sha256 32be26b32cbbd53f); build scripts `...\tools\ccr-wsl\install*.sh` |

## Surfaces (one row per route)

All commands run from the Skill's own route text unless a deviation is listed. Evidence in `fix-evidence\...\tooling\<route>\`.

| Route | Tool / env | Invocation (as run) | Smoke evidence | Input | Status |
|---|---|---|---|---|---|
| count | `mageck count` 0.5.9.5, shared venv | route command, 4 FASTQ.gz, `--trim-5 5` | 100% mapped, 25,000 reads per sample, Gini 0.074 plasmid / 0.106-0.115 endpoint, counts parse back, 60 guides x 4 samples; ~1 s | `derived\crispr-pipeline\count` (reads simulated from real HAP1 guide sequences and counts, 60 genes) | tooled, smoke-run |
| qc | `scripts/qc.py`, shared venv | route command, `plasmid=HAP1_T0` | HAP1: plasmid Gini 0.288, replicate Pearson 0.789 -> QC FAIL (as recorded in the normalize handoff) | `...\derived\...\qc\hap1.count.txt` (70,754 guides) | tooled, smoke-run |
| cn-correction | `scripts/cn_correction.R`, WSL `crispr-ccr` | `Rscript cn_correction.R a375.count.txt screen`; 1m49s | Corrected 86,881 of 90,709 guides (rest below `min_reads`), 0 NA, log-fc raw vs corrected r=0.94, A375 BRAF -4.04 -> -2.62, MYC -3.55 -> -4.15, RPS6 -9.5 -> -7.6; same column layout as input, non-integer counts | `...\cn-correction\a375.count.txt` (Project Score KY library, A375 3 reps + plasmid, 6.5 MB) | tooled, smoke-run. First execution of this script: passes unchanged |
| rra | `scripts/rra.py`, shared venv + RRA.exe | route command | 18,056 genes, 848 negative / 3 positive hits at fdr 0.05, lfc 0.5; ~1m43s; also ran on corrected A375 table (17,995 genes) | HAP1 table | tooled, smoke-run |
| bagel2 | BAGEL.py fc/bf/pr | route commands, `--seed 42` | 18,053 genes, BF>6 = 1,746; top POLR2L 131.6, POLR3H 129.5, RRM1 116.4; PR file has Recall/Precision/FDR | HAP1 + CEGv2/NEGv1 | tooled, smoke-run |
| mle | `mageck mle` 0.5.9.5 | route command (`--permutation-round 10`) on demo leukemia table | 2m23s, 1,000 genes, per-cell-line beta/z/p/fdr columns written | MAGeCK demo3 (real leukemia counts, 1,000 genes) | tooled, smoke-run (genome scale is hours, not run) |
| drugz | drugz.py | route command with `-unpaired -x Drug_r1`; 10 s | 18,054 genes, 0 NaN, columns as in route | HAP1 columns relabelled Day0/Veh_r1/Veh_r2/Drug_r1 (labels only: not a real drug screen, so no drug signal expected) | tooled, smoke-run |
| jacks | run_JACKS.py (JACKS 0.2) | route command; 22 s | 4,502 genes x 5 lines; ribosomal RPL/RPS mean -1.04 to -1.82, all-gene mean ~0 | 5-line slice of Project Score panel, 25% of genes | tooled, smoke-run |
| chronos | chronos 2.3.15, chronos-venv | `run_chronos.py` in evidence dir; `nepochs=301`; 2m06s | gene_effect 5 lines x 4,502 genes; ribosomal mean -2.7 to -3.0, all-gene mean ~0 | same slice, plasmid + 14-day replicates | tooled, smoke-run (with deviations below) |
| consensus | `scripts/consensus.py` | route command, three methods | Tier-1 481, Tier-2 399, Tier-3 874, none 16,302 (matches normalize handoff) | files from the recorded HAP1 runs | tooled, smoke-run |
| branches | pointers to sibling Skills | none | not runnable | `derived\...\branches` (Papalexi 2021, 400 cells x 2,000 genes + 111 guide counts) for the routing case only | n/a (reference route) |
| install.md | `references/install.md` | not run | `mageck-vispr` is Linux-only (ecosystem section 3) | | out of scope |

## Route-text defects found while tooling (Skill not edited; for fix phase)

1. `routes/count.md` says library.csv columns are `sgRNA, Gene, Sequence`; `mageck count --list-seq` reads columns by position: id, sequence, gene. Following the text literally gives sequences in the Gene column and 0% mapped (reproduced).
2. `routes/mle.md`: MAGeCK needs a tab-delimited count table; a comma-separated `.csv` fails with "Sample ... cannot be found".
3. `routes/jacks.md`: run_JACKS.py sits in `JACKS\jacks\`, not the clone root; `replicatemap.txt` needs a `Control` column, and `guidemap.txt` must use the same `--sgrna_hdr`/`--gene_hdr` names (sgRNA, Gene) as the count table.
4. `routes/chronos.md`: sequence_map needs `cell_line_name` (not the docstring's `cell_line`), plus `days`, `pDNA_batch`, `sequence_ID`; the constructor raises unless `negative_control_sgrnas` (or `excess_variance`) is passed. The snippet as written cannot run.
5. `routes/cn-correction.md`: output counts are non-integer and 3,828 low-count guides are dropped; `scripts/qc.py` refuses the corrected table (fine given the order, but state it).

## Public data

Provenance, bytes, sha256 and licence for every derived file: ecosystem `public-data\README.md` (section added 2026-10-04). New primary download: `public-data\perturb-seq\data\papalexi_2021.h5mu` (589 MB, pertpy `papalexi_2021()`, GEO GSE153056), used only for the branches routing case. All other inputs derive from files already staged.

## Blockers and heavy-optional

None. No heavy-optional surface. Genome-scale `mageck mle` and Chronos on a full DepMap panel are hours-class; the Skill already says genome-scale runs take hours (smoke ran on a 1,000-gene table).

## Out of scope

mageck-vispr and MAGeCKFlute dashboards; CRISPResso/PRIDICT/BE-Hive (other categories); the Docker CRISPRcleanR container (superseded by the WSL env); the `references/install.md` install commands.

## Rerun

`Scripts\python.exe ...\public-data\derived\crispr-pipeline\make_inputs.py` regenerates all route inputs (consensus inputs read `fix-evidence\recut-crispr-pipeline\*.txt`). CRISPRcleanR env rebuild: `tools\ccr-wsl\install.sh`, then `install2.sh`, `install3.sh`.

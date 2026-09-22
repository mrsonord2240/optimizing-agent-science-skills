# bio-single-cell-multimodal-integration fixes (2026-09-19)

Worktree `F:\OpenScience\wt\sc-multimodal`, branch `fix/sc-multimodal`, off fork `main`
(`F:\OpenScience\external\mrsonord2240__bioSkills`). Runtime:
`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst` — R 4.4.3 (dsb 2.0.1,
Seurat 5.5.0) via `tools\rs.sh`; Python (shared venv) scvi-tools 1.5.1 (torch 2.14 CPU),
anndata 0.13.3.post0, mudata 0.4.1. Audit: `F:\OpenScience\audits\bio-single-cell-multimodal-integration\`
(score 79/100, Limited Release, deployable, no P0). Commit `47aa056`.

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| totalVI code block non-deterministic as shipped (audit: max abs latent diff 0.9723 unseeded vs 0.0000 seeded, 2 runs each) | P1 | Added `scvi.settings.seed = 0` as the first line of the totalVI block + one-line note | ran (audit's own numbers reused; this is the audit's confirmed fix) | |
| Same reproducibility gap in GLUE's VAE training, not covered by the audit run (scglue not run: no Windows wheel) | P1 | Pinned `init_kws={'random_seed': 0}` on `fit_SCGLUE`, one-line note | docs only: fetched scglue's `SCGLUEModel.__init__` signature (`random_seed=0` default) and `fit_SCGLUE` signature from readthedocs to confirm the parameter path exists | scglue cannot run on Windows in this env (pysam has no Windows build); code not executed |
| DSB's own documented failure mode (filtered-only matrix as `empty_drop_matrix`) produces no error/warning, silently wrong output (audit: range -3.07..3.43 vs correct -1.45..20.53) | P1 | Added a median-total-ADT-count guard (`stop()` if empty ≥ 0.5x cells) before `DSBNormalizeProtein` in SKILL.md's CITE-seq DSB block and in `examples/cite_seq_analysis.R` | ran on the audit's `data/synthetic_cite_seq.rds` (copied to scratchpad): real empty droplets give ratio 0.12 (guard passes, matches Input 1); cell-matrix-as-both gives ratio 1.00 (guard stops, matches Input 3 exactly) | |
| Mosaic anchor structure (MultiVI/StabMap/Cobolt) — one of the skill's 4 core anchor structures — shipped zero code, unlike WNN/totalVI/Multiome-WNN/GLUE (audit Input 5: auditor-built script errored, `organize_multiome_anndatas` calls removed `AnnData.concatenate`) | P1 | Wrote a new "Mosaic: MultiVI (Python)" SKILL.md section with a runnable MuData + `setup_mudata` example (scvi-tools installed, chosen per FIX_BRIEF's "write it" option) | ran end-to-end on synthetic 150-cell mosaic data (90 paired, 60 RNA-only, 3 known cell types): RNA-only cells land nearer same-type paired cells (mean latent dist 0.27) than different-type ones (0.56) — recovers the planted structure, not just input-block clustering. Along the way confirmed `MULTIVI.setup_anndata` is a silent no-op on plain AnnData in 1.5.1 (isolated test, not just the audit's traceback) and that MultiVI's missing-modality detection is `x.sum(dim=1) > 0` from `_multivae.py` source, which is why zero-fill (not NaN/omission) is correct |
| `examples/cite_seq_analysis.R` and `.py` skip the skill's own DSB-before-WNN guidance (CLR-only, never read a raw/unfiltered matrix) | P2 | R example: now reads `raw_feature_bc_matrix/`, runs DSB with the same guard, sets the ADT `data` layer from DSB output instead of CLR. Python example: comment marks CLR-only as a fallback (muon has no first-party DSB) and points to SKILL.md's totalVI section | ran the modified R logic end-to-end against `synthetic_cite_seq.rds` (DSB range -1.45..20.53 matches Input 1; `SetAssayData(..., layer='data')` on Seurat 5.5.0 confirmed to work; WNN recovers 3 clusters). Both files: `Rscript parse()` / `py_compile` clean |

## Redundancy pass (required every fix pass, not just when flagged)

- `usage-guide.md`'s **Prerequisites** (install commands) existed nowhere else and is
  agent-actionable → moved verbatim into a new SKILL.md `## Prerequisites` section;
  usage-guide.md now points to it.
- `usage-guide.md`'s **Tips** (9 bullets) and **Decision Guidance** (3 subsections) were
  1:1 restatements of SKILL.md's Governing Principle, Classify-the-Task table, both
  Method Decision Tables, and the ADT Normalization table — no content found nowhere
  else. Deleted, replaced with a one-line pointer to the SKILL.md sections.
- `usage-guide.md`'s **What the Agent Will Do** (7 steps, each restating a SKILL.md
  fact) trimmed to 3 lines + the same pointer.
- Nothing was deleted that the agent needs; every fact above still lives in SKILL.md
  exactly where it did before this pass (Governing Principle / tables / Common Errors).

## Unfixed

- P2 "Seurat v5 bridge integration named but never demonstrated" (`observed_in: []` in
  the audit — no input actually exercised it) — out of scope for this pass; the brief's
  "missing referenced executables" rule is triggered by the recommendations acted on
  above, and stacking a second new worked example (bridge integration, Signac reference
  build) risked a much larger diff than the P1s justified. Left for a future fix pass;
  noted here so it isn't lost.
- GLUE seed fix is docs-verified only, not run (no Windows wheel for scglue in this
  env) — flagged in the commit message and here so a re-auditor knows it needs live
  verification if a scglue-capable environment becomes available.

# 2026-09-21: P2 pass, split, scripts

Worktree `F:\OpenScience\wt\single-cell-multimodal-integration`, branch `fix/single-cell-multimodal-integration`
off staging `main` 431aa55. Commits: `3700283` (fix), `532bebc` (split), `7394506` (scripts). Env
`single-cell-transcriptomics-analyst`: Seurat 5.5.0, Signac 1.17.1, scvi-tools 1.5.1, mudata 0.4.1.
Audit: 3 P2s. SKILL.md 341 -> 152 lines (308 at start; the bridge example added 33).

## Findings

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Prerequisites: `pip install scglue` has no platform caveat | P2 | Comment on the install line: no Windows install (pybedtools -> pysam has no wheel), use WSL/Linux/macOS or skip | ran: `pip install --dry-run scglue` in the audit env fails "Failed to build 'pysam'"; `pip install --dry-run --only-binary=:all: pysam` finds no distribution; scglue 0.4.0 wheel metadata lists pybedtools | pysam reaches scglue through pybedtools, not directly |
| GLUE seed comment claims the same measured gap as totalVI | P2 | Comment now says the seed is pinned for reproducibility, scglue's documented default is already `random_seed=0`, drift not measured for GLUE | docs (scglue API; the audit re-confirmed the default). Not run: no scglue on Windows | |
| Seurat v5 bridge integration named, never demonstrated | P2 | New "Seurat v5 Bridge Integration (R)" section (PrepareBridgeReference -> FindBridgeTransferAnchors -> MapQuery) and a pointer in the decision-table row. Chose "write it": Seurat and Signac are installed | ran the block extracted from SKILL.md on synthetic 3-population data (300 reference RNA, 300 bridge multiome, 300 ATAC-only query): 81% of query cells recover the planted type with LogNormalize, 75% with SCT (chance 33%); now also as `scripts/seurat_bridge_integration.R`, 81% | Found and documented: `MapQuery(reference = )` must be the object `PrepareBridgeReference` returned, else "assay used to create the anchorset does not match". The audit's own synthetic multiome ATAC was too weak for this (53%, nothing separates in the LSI), so I planted stronger markers |

## Redundancy pass

Already done in the 2026-09-19 pass (`usage-guide.md` holds overview, prompts and related Skills only, and points at SKILL.md); nothing further to remove. Checked again after the new section: no fact stated twice in SKILL.md/references.

## Split (532bebc), SKILL.md 341 -> 152

Moved verbatim (no non-blank line lost, multiset compare; all R/Python fences parse, bash fence passes `bash -n`):

| old location (SKILL.md section) | new home |
|---|---|
| CITE-seq: Denoise ADT, Then Joint Embed (Seurat); CITE-seq: WNN Joint Clustering (Seurat) | `references/cite-seq-dsb-wnn.md` |
| CITE-seq: totalVI; Mosaic: MultiVI | `references/scvi-totalvi-multivi.md` |
| Multiome (RNA + ATAC, same cell); MOFA+ | `references/multiome-mofa.md` |
| Unpaired / Diagonal: GLUE; Seurat v5 Bridge Integration | `references/unpaired-glue-bridge.md` |

Additions: "Reference Files" index, and a file pointer in each decision-table row (WNN, totalVI, MultiVI, MOFA+, GLUE, bridge, DSB). One pointer reworded ("see Multiome section" -> "see `references/multiome-mofa.md`").

## Scripts (7394506)

| old location | new home | verified (ran as SKILL invokes it) |
|---|---|---|
| totalVI block (`references/scvi-totalvi-multivi.md`) | `scripts/totalvi_cite_seq.py h5mu out_prefix [--max-epochs]` | synthetic 300-cell CITE-seq with planted types: two separate runs, latent max abs diff 0.0; kNN type accuracy 1.0; own-type foreground probability 0.63 vs 0.25 for other types |
| MultiVI block (same file) | `scripts/multivi_mosaic.py h5mu out_prefix [--max-epochs]` | synthetic 195-cell mosaic (120 paired, 75 RNA-only, 3 types), default epochs: 91% of RNA-only cells have a same-type nearest paired cell (chance 33%). At `--max-epochs 40` the same data gave 29% (undertrained), so the reference file says to leave epochs at the default |
| Seurat v5 bridge block (`references/unpaired-glue-bridge.md`) | `scripts/seurat_bridge_integration.R rna.rds multi.rds atac.rds out.rds [ndims first_lsi_dim norm]` | 81% of 300 ATAC-only query cells correct; asserted `predicted.celltype`, `predicted.celltype.score`, `ref.umap` present |
| DSB block (`references/cite-seq-dsb-wnn.md`) | deleted: duplicates `examples/cite_seq_analysis.R`. Its three caveats (no error on a cell matrix passed as empty droplets, isotype names, `use.isotype.control = FALSE` fallback) kept as prose beside the pointer | not re-run (the example was run in the 2026-09-19 pass) |

Left inline (under 15 lines or not runnable here): Multiome WNN R block, MOFA+ (3 lines), GLUE (no Windows build), the WNN fragment (needs `obj` and `adt_dsb` from the example).

## Left unfixed

- GLUE's `random_seed=0` default and the block itself remain unexecuted: scglue has no Windows install (pybedtools -> pysam), and the WSL `science` distro was not built for this Skill. Needs a Linux env with scglue to measure GLUE drift.

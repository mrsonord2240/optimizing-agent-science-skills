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

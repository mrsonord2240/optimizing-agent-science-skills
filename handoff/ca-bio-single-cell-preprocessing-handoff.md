# Handoff: ca-bio-single-cell-preprocessing / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-single-cell-preprocessing` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-single-cell-preprocessing`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `655ae919f540860645b4f427f5e57cad48e38c588e1bac2dfe1ecc3d64901713`, 11 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 34 lines, 5 routes (scanpy, seurat, ambient, normalization, errors).
- `references/background.md`, `citations.md`. Dropped: `usage-guide.md`, install block, governing-principle essay (to background).

## Scripts written (all unexecuted)

`scripts/preprocess_scanpy.py` (merges the source QC snippets, per-sample MAD and per-batch gene filter into one entry point), `preprocess_seurat.R` (adds a `normalization=lognorm` option for the source's NormalizeData path), `soupx.R` (from the source snippet). CellBender and DecontX commands in `routes/ambient.md` are shown, not wrapped.

Likely environment for tooling: native Windows venv and R library under `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\`; inputs `public-data\pbmc_1k_v3_filtered_feature_bc_matrix.h5` and the raw `.h5` for SoupX (SoupX needs a Cell Ranger `outs/` directory; the staged files are `.h5` only).

## Open ambiguities for audit

- Scanpy 1.12.4 and scikit-misc 0.5.2 are newer than the source's tested 1.10+; per-batch `seurat_v3` and the `sc.experimental` Pearson HVG path were not rechecked.
- The script copies only the combined `highly_variable` flag when `batch_key` is used.
- Mito detection for `.h5` input uses `var_names` as symbols; `gene_ids`-named inputs use `var['gene_symbols']`.
- Tissue mito caps (PBMC 8, cardiac and hepatic 30, muscle 40) are the source's numbers.

## Worktree safety

- Run-owned: `skills\ca-bio-single-cell-preprocessing\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

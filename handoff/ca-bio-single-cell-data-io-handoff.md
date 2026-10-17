# Handoff: ca-bio-single-cell-data-io / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-single-cell-data-io` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-single-cell-data-io`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `3c7c5b39a2e0c51ccc3a6ef3ffe66b7aeebc54f2de326da8ed5d01f06044ebd3`, 11 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 33 lines, 5 routes (load-10x, object-structure, convert, formats-and-defaults, errors).
- `references/background.md`, `citations.md`. Dropped: `usage-guide.md`, install block, governing-principle essay (to background).

## Scripts written (all unexecuted)

`scripts/load_10x.py` (from the source example; `gex_only=False`, gzip output), `load_10x.R` (source example plus multi-feature-type handling), `h5ad_inventory.py` (new helper for the "diff slot inventories" rule). The conversion commands in `routes/convert.md` (schard, zellkonverter, `as.SingleCellExperiment`) are shown, not wrapped.

Likely environment for tooling: native Windows venv and R library under `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (anndata 0.13.3, Seurat 5.5.0, zellkonverter 1.16.0, schard 1.1.0); inputs in its `public-data\` (10x PBMC 1k v3 raw and filtered `.h5`, `.h5ad`).

## Open ambiguities for audit

- anndataR needs R 4.5 and cannot be installed in the staged R 4.4.3; its table row is kept for R 4.5 users.
- The staging notes say zellkonverter's basilisk Python reader cannot read anndata 0.13 files; the route says so, and recommends schard for reads.
- The claim that `sc.read_10x_h5` has no `var_names` argument was not rechecked on Scanpy 1.12.4.
- The `CreateAssay5Object` branch in `load_10x.R` for non-GEX features is the script author's.

## Worktree safety

- Run-owned: `skills\ca-bio-single-cell-data-io\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

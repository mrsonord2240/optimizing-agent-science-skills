# Handoff: ca-bio-single-cell-clustering / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-single-cell-clustering` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-single-cell-clustering`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `e33a97ec2594e5afdcc3d2eaf7afb8009623a2f9c8291637489405427d16c261`, 13 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 34 lines, 6 routes (scanpy, seurat, validate, subcluster, significance, errors).
- `references/background.md`, `citations.md`. Dropped: `usage-guide.md`, governing-principle essay (to background).

## Scripts written (all unexecuted)

`scripts/cluster_scanpy.py`, `cluster_seurat.R`, `validate_partition.py` (the source example, now with args), `subcluster.py` (from the source snippet). The scSHC call in `routes/significance.md` is a shown snippet only.

Likely environment for tooling: the native Windows venv and R library under `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (scanpy 1.12.4, leidenalg 0.12.0, igraph 1.0.0, Seurat 5.5.0); input `public-data\pbmc_1k_v3_filtered.h5ad` needs preprocessing first.

## Open ambiguities for audit

- Installed Scanpy 1.12.4 is newer than the source's 1.10+; whether `flavor='igraph', n_iterations=2, directed=False` is still the right pin was not checked.
- `cluster_seurat.R` takes the clustree prefix from the default assay; the source assumed `RNA_snn_res.`.
- `subcluster.py` and the Seurat sweep were turned from prose snippets into scripts; no source run exists for either.

## Worktree safety

- Run-owned: `skills\ca-bio-single-cell-clustering\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

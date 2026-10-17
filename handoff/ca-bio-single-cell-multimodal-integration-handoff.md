# Handoff: ca-bio-single-cell-multimodal-integration / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-single-cell-multimodal-integration` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-single-cell-multimodal-integration`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `69408cbe4b2ef6aa76992483dc18023b6193f67eb875d8e5951df81b129dc4a5`, 22 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (the shelf had none; frontmatter `license: MIT`, `author: GPTomics` kept).

## Structural summary

- SKILL.md 40 lines, 11 routes (choose, cite-seq-wnn-r, cite-seq-wnn-python, totalvi, multiome-wnn, mofa, multivi, glue, bridge, errors, other-skills). references/background.md, citations.md. Dropped: usage-guide.md, the governing-principle essay (to background). Routes to the existing ca-bio-single-cell-preprocessing and -clustering recuts and to two recuts from this batch.

## Scripts written

scripts/totalvi_cite_seq.py, multivi_mosaic.py, seurat_bridge_integration.R (shelf scripts copied unchanged); new: cite_seq_wnn.R and cite_seq_muon.py (from the examples), multiome_wnn.R, mofa_muon.py, glue_unpaired.py (from reference snippets). All unexecuted after the recut (shelf scripts copied unchanged keep whatever shelf execution evidence they had).

## Open ambiguities for audit

- cite_seq_wnn.R follows the shelf example (default Louvain clustering, resolution 0.5) while the reference WNN snippet used SLM (algorithm = 3); multiome_wnn.R uses algorithm = 3 as its snippet did. Left inconsistent.
- cite_seq_wnn.R falls back to no isotype controls when the default pattern matches none (the source reference suggested this); the shelf example would have passed an empty vector.
- glue_unpaired.py prints the guidance-graph edge count instead of stopping on zero (no new guard added). Idea for audit: stop on an empty graph.
- Version: source tests scanpy 1.10+, Seurat 5.0+, anndata 0.10+ while scripts were checked on scvi-tools 1.5.1, Seurat 5.5.0; not reconciled. mofa_muon.py, multiome_wnn.R, glue_unpaired.py and cite_seq_muon.py were never executed in any form.

## Worktree safety

- Run-owned: `skills\ca-bio-single-cell-multimodal-integration\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` untouched; sibling `skills/ca-*` folders of the other worker untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

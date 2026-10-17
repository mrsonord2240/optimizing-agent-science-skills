# Handoff: ca-bio-atac-seq-motif-deviation / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-atac-seq-motif-deviation` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-atac-seq-motif-deviation`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `f855ee65eb79c800ae97885995e9bb32561c26c5e6413a027f64e6d3db738014`, 14 files
- Applicable audit: none
- No warns.

## Structural summary

- SKILL.md 37 lines, 7 routes (bulk, signac, archr, time-course, interpret, other-skills, errors). references/background.md, citations.md. Root LICENSE kept.

## Scripts written

scripts/chromvar_bulk.R (the source bulk script made argument-driven), scripts/chromvar_signac.R and scripts/chromvar_archr.R (new, from the source single-cell snippets). All unexecuted after the recut (shelf scripts copied unchanged keep whatever shelf execution evidence they had).

## Open ambiguities for audit

- chromvar_bulk.R replaces the source's hard-coded 6-sample condition vector with `samples=` and a required `ref=`; adds `genome=`, `pfm_rds=`, `seed=`. `pfm_rds` (custom PFMs) was never executed in the source either.
- chromvar_signac.R and chromvar_archr.R were prose snippets in the source; executed there on a PBMC slice but not as scripts.
- Time-course spline regression is a route sentence only (not scripted, never executed in the source).
- Version: source records Bioconductor 3.20 / R 4.4.3 runs; newer releases untested.

## Worktree safety

- Run-owned: `skills\ca-bio-atac-seq-motif-deviation\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` untouched; sibling `skills/ca-*` folders of the other worker untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

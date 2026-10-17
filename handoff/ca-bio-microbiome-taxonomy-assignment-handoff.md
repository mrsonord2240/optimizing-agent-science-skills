# Handoff: ca-bio-microbiome-taxonomy-assignment / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-microbiome-taxonomy-assignment` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-microbiome-taxonomy-assignment`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `0437987e81e97d0781a241b31a87e0ae167c2ff12539f012fb8d194774fd4142`, 16 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 37 lines, 9 routes.
- Routes: dada2, idtaxa, qiime2-region-nb, qiime2-vsearch, choose-database, rank-and-confidence, organelle, other-skills, errors.
- `references/citations.md` (eleven sources). The source's `references/decipher-idtaxa.md` and `organelle-filtering.md` became routes `idtaxa.md` and `organelle.md`.
- Dropped: `usage-guide.md`.

## Scripts written or moved

- `scripts/idtaxa_classify.R` (moved unchanged).
- `scripts/dada2_assign.R` (was `examples/assign_silva.R`; arguments now required, species FASTA optional, `MIN_BOOT` env, reference attribute taken from the training file name instead of a hard-coded 'SILVA 138.1').
- `scripts/qiime2_region_nb.sh` (was `examples/assign_qiime2_region.sh`; primers now required, paths as arguments), `scripts/qiime2_vsearch.sh` (the vsearch tail of that script as its own entry), `scripts/filter_organelle.sh` (new, from the source's QIIME2 commands).
None was run (normalize does not run scripts).

## Open ambiguities for audit

- QIIME2 floor stays 2024.10+; releases since then and the SILVA, GTDB, UNITE and PR2 release numbers were not re-checked offline.
- `qiime2_vsearch.sh` expects a region-extracted reference; the source reused the extract-reads output from step 1.
- The weighted (clawback) classifier is named in routes with no command (the source had none).
- `dada2_assign.R` no longer bundles the SILVA file names as defaults.

## Worktree safety

- Run-owned: `skills\ca-bio-microbiome-taxonomy-assignment\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` and `.claude/skills/normalize-scientific-skill/SKILL.md` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

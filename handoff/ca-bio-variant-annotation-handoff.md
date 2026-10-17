# Handoff: ca-bio-variant-annotation / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-variant-annotation` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-variant-annotation`; no git writes made
- Candidate identity (preflight `--shape`, PASS): `9ed5988c2f3bf170b84e73101a97609ae6715bcf53a1cc7d23cec1a216aeaf9c`, 14 files
- Warns carried: no Skill-root LICENSE (`license: MIT`, author GPTomics kept); "near-duplicate name: variant-annotation" (the `ca-` prefix of the recut)

## Structural summary

- `SKILL.md`: 37 lines, 8 routes (annotate-vep, annotate-vcf, snpeff-annovar, parse-csq, transcript-choice, consequence-nmd, predictors, population-frequency) plus a sibling row (normalization, clinical interpretation, filtering).
- Scripts, all new: `annotate_vep.sh` (norm + VEP on MANE Select), `annotate_vcf.sh` (the shelf `examples/annotate_vcf.sh` generalized: norm, dbSNP, gnomAD into a new tag, ClinVar, csq), `parse_csq.py` (CSQ/ANN flattener from the shelf snippets).
- References: `bcftools-recipes.md` (usage-guide mechanics), `citations.md`. Dropped: `usage-guide.md`, `examples/`.
- Traps in scripts: `annotate_vep.sh` refuses non-GRCh38 and a CSQ without MANE_SELECT; `annotate_vcf.sh` refuses unindexed inputs, no shared contigs, a missing INFO tag; `parse_csq.py` refuses a VCF without CSQ/ANN and `--mane-only` without MANE_SELECT.
- Version notes: command forms are the shelf's (bcftools 1.19+, VEP 110+, SnpEff 5.2+, ANNOVAR 2020Jun07+); no software-version drift was checked against live tools.
- Added: `bio-variant-calling-*` sibling names follow the shelf where present; `variant-calling/variant-normalization` and `clinical-interpretation` are not on the shelf and keep the upstream path style.

## Scripts

Not run (normalize scope: no script runs). All three were syntax-checked only (`bash -n`, `ast.parse`).

- `annotate_vep.sh`: unexecuted
- `annotate_vcf.sh`: unexecuted
- `parse_csq.py`: unexecuted

## Open ambiguities for audit

- `annotate_vep.sh` summary counts of MANE and HIGH/MODERATE records are grep-based approximations.
- REVEL Moderate/Strong cutoffs are not uniformly reproduced; the route says to verify against the Pejaver 2022 supplement.
- AlphaMissense and splicing calibrations are still evolving; "current ClinGen SVI" thresholds were not looked up.
- gnomAD v4 totals (about 730k exomes + 76k genomes) are from the shelf text.

## Evidence

- None (no runs). Audit-side inputs exist at `F:\OpenScience\audits\bio-variant-annotation\data` and `audit-envs\variant-annotation-curation-analyst\work\data`.

## Worktree safety

- Run-owned: the skill folder, this handoff, one row in `skills\README.md`. Pre-existing/user-owned files untouched. No commits.

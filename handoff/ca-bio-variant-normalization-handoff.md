# Handoff: ca-bio-variant-normalization / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-variant-normalization` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-variant-normalization`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `7677b8b20031b285fafef4656f0612321ce55ac81a684d9993540044170c00da`, 18 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 38 lines, 11 routes.
- Routes: normalize, compare-callers, ref-mismatch, multiallelic, atomize, tool-discordance, hgvs, check, dedup-plink, other-skills, errors.
- `references/background.md` (algorithm, silent-miss rationale, split-before-atomize), `references/citations.md` (one source).
- Dropped: `usage-guide.md`; the cohort-comparison loop is now `compare_callers.sh`.

## Scripts written or moved

- `scripts/normalize_vcf.sh` (was `examples/normalize_vcf.sh`; added `ATOMIZE=0` for the no-MNP variant the source describes in prose).
- `scripts/check_normalization.py` (was `examples/`; two small fixes: no crash on a record with no ALT, no divide by zero on an empty VCF).
- `scripts/check_ref.sh`, `scripts/compare_callers.sh` (new, from the source's REF pre-check and isec workflow).
None was run (normalize does not run scripts).

## Open ambiguities for audit

- The source says `--atomize` needs bcftools 1.12+ and was checked on 1.24; not re-verified against a current release.
- `bcftools csq -p` guidance kept as written; the source says to inspect BCSQ output on the installed version.
- Sibling Skill ids in `routes/other-skills.md` (`bio-vcf-manipulation`, `bio-clinical-interpretation` and so on) were taken from the source's Related Skills and not checked against the shelf.

## Worktree safety

- Run-owned: `skills\ca-bio-variant-normalization\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` and `.claude/skills/normalize-scientific-skill/SKILL.md` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

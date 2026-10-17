# Handoff: ca-bio-vcf-statistics / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-vcf-statistics` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-vcf-statistics`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `536e57215b6687d7f0f3d37aea835efcdf214de77342b2bb29294853040efa10`, 17 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 34 lines, 8 routes.
- Routes: callset-stats, interpret, missingness-hwe, contamination, identity, stratified, other-skills, errors.
- `references/background.md` (governing-principle essay, Ti/Tv and HWE mechanisms), `references/citations.md` (seven sources).
- Dropped: `usage-guide.md`; its per-sample genotype and AF-spectrum snippets became `--per-sample` and `--afs` of `vcf_stats.py`.

## Scripts written or moved

- `scripts/vcf_qc.sh` (new): `bcftools stats` plain and per-sample, SN/TSTV/PSC summary, counts, optional plot.
- `scripts/vcf_stats.py` (was `examples/vcf_stats.py`, extended with the usage-guide snippets).
- `scripts/missing_hwe.sh`, `het_allele_balance.sh`, `identity_qc.sh` (gtcheck, king, peddy, somalier), `stratified_stats.sh` (all new, wrapping the source's commands).
None was run (normalize does not run scripts).

## Open ambiguities for audit

- `identity_qc.sh somalier` passes `-o` to `somalier relate` (the source did not); check the flag on the installed version.
- `stratified_stats.sh` greps `SN` lines for SNP and indel counts; field positions untested.
- `vcf_stats.py` counts PASS as `FILTER is None`, as in the source; cyvcf2 returns None for both PASS and `.`.
- Thresholds (Ti/Tv, 54.69 ExcessHet, KING bands) kept from the source, unverified.

## Worktree safety

- Run-owned: `skills\ca-bio-vcf-statistics\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` and `.claude/skills/normalize-scientific-skill/SKILL.md` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

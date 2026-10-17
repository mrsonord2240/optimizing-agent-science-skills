# Handoff: ca-bio-variant-calling-filtering-best-practices / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-variant-calling-filtering-best-practices` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-variant-calling-filtering-best-practices`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `13496ce57aeff3931e4da1c6dfaa0ad7ce986455001be55fcddc73201ff3a8c4`, 17 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 36 lines, 9 routes (choose-method, hard-filter, genotype-filter, vqsr, somatic, cyvcf2, validate, cohort-and-regions, errors).
- `references/background.md`, `citations.md`. Dropped: `usage-guide.md`, `examples/filter_variants.sh` (became `scripts/hard_filter.sh`).

## Scripts written (all unexecuted)

`scripts/hard_filter.sh` (from the example script; added guards for DeepVariant/DRAGEN header, missing GATK INFO tags, SNP+indel count mismatch, empty output, Ti/Tv warning), `genotype_filter.sh`, `somatic_filter.sh`, `cyvcf2_filter.py`, `filter_stats.sh`. The VQSR, FilterMutectCalls, VETS and NVScoreVariants commands are shown in routes only; no truth resources or Java 17 were available.

A run attempt was planned against `F:\OpenScience\audit-envs\variant-annotation-curation-analyst\work\data\cohort.vcf` (synthetic, 361 records, 25 sites with undefined RankSums) and a synthetic Mutect2-style VCF in `F:\OpenScience\fix-evidence\ca-recut\bio-variant-calling-filtering-best-practices\data\`. It did not execute: WSL returned `Wsl/Service/E_UNEXPECTED`, then the scope changed to no runs. Nothing here has run.

## Open ambiguities for audit

- The source cyvcf2 snippet had a DP floor of 10 that its own bcftools twin lacks; kept as `min_dp=10` in `cyvcf2_filter.py`.
- The source cyvcf2 snippet applied SNP thresholds to every variant; the script splits SNP and indel.
- The source somatic expression does not require `FILTER=PASS`, so FilterMutectCalls rejections survive; kept as default, `pass_only=1` added.
- GATK 4.6.1.0 `gatkdoc` lists `ScoreVariantAnnotations` as beta but has no page for `CNNScoreVariants` or `NVScoreVariants`; the deprecation claim is carried from the source.
- The ENCODE blacklist citation in `references/citations.md` (Amemiya 2019) was added from the script author's knowledge, not the source.
- bcftools `-v snps` plus `-v indels` double-counts multiallelic SNP+indel records; the script's count check refuses rather than resolves that.

## Worktree safety

- Run-owned: `skills\ca-bio-variant-calling-filtering-best-practices\`, this handoff, one row in `skills\README.md`, staged data under `F:\OpenScience\fix-evidence\ca-recut\bio-variant-calling-filtering-best-practices\`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

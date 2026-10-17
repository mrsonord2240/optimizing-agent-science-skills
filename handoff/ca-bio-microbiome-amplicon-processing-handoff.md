# Handoff: ca-bio-microbiome-amplicon-processing / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-microbiome-amplicon-processing` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-microbiome-amplicon-processing`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `e072e8a70244fcaf0bc89d6bc8045d60ffd7ec38e788ba025882f8ec7ed66afb`, 15 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 37 lines, 9 routes.
- Routes: remove-primers, dada2-16s, truncation, its, decontam, qiime2, choose-method, other-skills, errors.
- `references/background.md` (ASV-as-model essay, tool taxonomy, threshold rationale), `references/citations.md` (twelve sources).
- Dropped: `usage-guide.md`; the ASV-vs-OTU debate is one paragraph in `choose-method.md` plus background.

## Scripts written or moved

- `scripts/remove_primers.sh` (was `examples/remove_primers.sh`; primers now required env vars instead of hard-coded V4).
- `scripts/dada2_asv.R` (was `examples/dada2_workflow.R`; now takes run directories and options, adds `--single` for ITS, an optional `--amplicon-len` budget check, and a primer-trimmed read-length ceiling check taken from the source's prose).
- `scripts/decontam_filter.R` (new, wraps the source's `isContaminant` snippet; method chosen from the metadata columns per the source).
None was run (normalize does not run scripts).

## Open ambiguities for audit

- `dada2_asv.R` single-end mode is new code around the source's ITS `filterAndTrim` snippet; the rest is the paired pipeline minus merging.
- The NovaSeq monotonic error fix is guidance only; the source gave no code.
- `--pool` defaults to FALSE and `maxEE` to 2; the source shows `pool='pseudo'` only as a comment.
- DADA2, cutadapt and QIIME2 version floors unchanged from the source; flags such as `denoise-ccs` not re-checked.

## Worktree safety

- Run-owned: `skills\ca-bio-microbiome-amplicon-processing\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` and `.claude/skills/normalize-scientific-skill/SKILL.md` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

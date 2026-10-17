# Handoff: ca-bio-duplicate-handling / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-duplicate-handling` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-duplicate-handling`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `c53e73d689998b6530129bc1cfe37801c18db63300cc6252b86a68deb5a1c8a7`, 15 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 34 lines, 7 routes (markdup, pysam, umi, not-markdup, other-markers, rate-and-filter, errors).
- `references/`: `background.md`, `alternative-markers.md`. The source had no literature citations, so no `citations.md`.
- Dropped: `usage-guide.md`, the why-remove essay (to background), duplicated pysam snippets.

## Scripts written or moved

`scripts/markdup.sh` (was `examples/markdup_pipeline.sh`), `pysam_markdup.py`, `dup_rate.py`, `umi_tools_dedup.sh`, `fgbio_consensus.sh`. New guards, not new analyses: `fgbio_consensus.sh` exits 2 on no `RX:Z:` and on duplex with a single-UMI RX; `umi_tools_dedup.sh bulk-paired` exits 2 on no `RX:Z:`.

## Runs done before the scope change (evidence only)

All five scripts ran once or more, WSL `science`, env `alignment-files` (samtools 1.24, pysam 0.24.1, umi_tools 1.1.6) with fgbio 4.1.1 from `af-fgbio2`; inputs from `F:\OpenScience\audit-envs\alignment-files\public-data`. Key numbers: HG00349 chr20 slice 111 of 9595 primary flagged (1.16%) by `markdup.sh` and `pysam_markdup.py`; `bulk-paired` 15788 to 5689 records; fgbio single 5646, duplex 4042. Traps tripped: assay gate, spliced-BAM gate, CB-missing, RX-missing, duplex on single-UMI. Not run: `umi_tools_dedup.sh scrna` success path (no CB/UB BAM staged), Picard/samblaster/sambamba/biobambam2/mapDamage/pbmarkdup commands in `references/alternative-markers.md`.
Evidence: `F:\OpenScience\fix-evidence\ca-recut\bio-duplicate-handling\` (`run.sh`, `run.log`, `sum.log`, `out\`).

## Open ambiguities for audit

- The WGS slice has SRA-style read names, so samtools gave "cannot decipher read name" and no optical (SQ) tags; `-d` had no effect. Optical logic untested with Illumina names.
- `-d 2500` for NextSeq 1000/2000 and NovaSeq X is the source's claim.
- `markdup.sh` always passes `--use-read-groups`; behaviour on a BAM with no `@RG` untested.
- The `alignment-files` env holds fgbio 1.3.0; the source checked 4.1.1.

## Worktree safety

- Run-owned: `skills\ca-bio-duplicate-handling\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `.claude/skills/normalize-scientific-skill/SKILL.md`, `test/validate.bats` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

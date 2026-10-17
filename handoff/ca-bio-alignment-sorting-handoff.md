# Handoff: ca-bio-alignment-sorting / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-alignment-sorting` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-alignment-sorting`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `3bf5525c014c225d582e2711bf8664c1163b3de2bcdbbbb0e7e99226514f7f4d`, 13 files
- Applicable audit: none
- Warn carried: no Skill-root LICENSE (frontmatter `license: MIT`, `author: GPTomics` kept)

## Structural summary

- `SKILL.md` 35 lines, 8 routes.
- Routes: sort, align-sort, merge, check-order, required-order, python, other-skills, errors. No `references/` (nothing left over; the compression table went into `routes/errors.md`).
- Dropped: `usage-guide.md` and the duplicate-marking pipeline snippet (routed to `ca-bio-duplicate-handling`).

## Scripts written or moved

- `scripts/sort_bam.sh` (new): one entry for coordinate, name-natural, name-ascii, tag, template-coordinate; quickcheck, publish, index. Template-coordinate runs `collate | fixmate -m` first (assembled from the source's collate/fixmate recipe).
- `scripts/merge_bams.sh` (new): the source's `@HD` consistency check, then `merge -c -p`.
- `scripts/check_order.py` (new): the source's pysam `is_coordinate_sorted` as a CLI.
- `scripts/align_sort.sh` (was `examples/sort_pipeline.sh`; only the name in the usage text changed).
None was run (normalize does not run scripts).

## Open ambiguities for audit

- CRAM output is not indexed by `sort_bam.sh`; CRAM input needs `REF` too.
- RG-ID collision before merge is prose only; no script check (not in the source).
- Empty bash arrays under `set -u` need bash 4.4+.
- Version line unchanged (samtools 1.24, pysam 0.24.1); newer releases not checked offline.

## Worktree safety

- Run-owned: `skills\ca-bio-alignment-sorting\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` and `.claude/skills/normalize-scientific-skill/SKILL.md` untouched; sibling `ca-*` folders belong to another worker.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

# Handoff: ca-bio-atac-seq-consensus-peakset / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-atac-seq-consensus-peakset` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-atac-seq-consensus-peakset`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `d3dd0c5d75ccb85fd95bb7b3c3e929fefb7e70d211768a89a44f9ab42c7771d0`, 17 files
- Applicable audit: none
- No warns.

## Structural summary

- SKILL.md 38 lines, 10 routes (choose, iterative-overlap, iterative-overlap-r, diffbind, per-condition, union, count, liftover, other-skills, errors). references/background.md, citations.md. Root LICENSE kept.

## Scripts written

scripts/iterative_overlap.sh (shelf script copied unchanged), scripts/iterative_overlap.R (new, from the source GenomicRanges snippet plus the shell script's input validation), scripts/per_condition_consensus.sh (new, from the source per-condition snippet). All unexecuted after the recut (shelf scripts copied unchanged keep whatever shelf execution evidence they had).

## Open ambiguities for audit

- iterative_overlap.sh keeps its hg38 default arguments; the route passes them explicitly.
- The source offers DiffBind, IDR-union, merge, liftOver and the featureCounts step only as commands; they are shown in routes, not scripted.
- iterative_overlap.R's greedy loop is quadratic (as in the source); the shell script is the large-data path.
- The source's pybedtools re-centering function was dropped as redundant with the two scripts.

## Worktree safety

- Run-owned: `skills\ca-bio-atac-seq-consensus-peakset\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` untouched; sibling `skills/ca-*` folders of the other worker untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

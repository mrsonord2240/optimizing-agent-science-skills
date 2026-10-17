# Handoff: ca-bio-atac-seq-atac-qc / prepare-scientific-skill-tooling

- Updated: 2026-10-17
- Lane: n/a (context-aware recut batch)
- Status: ready-for-phase
- Owner leaving: normalize-phase worker (Sonnet)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: `F:\optimized-scientific-skills@f162b3a:skills/bio-atac-seq-atac-qc` (read-only shelf)
- Working tree: `F:\optimizing-agent-science-skills\skills\ca-bio-atac-seq-atac-qc`
- Branch/worktree: records repo working tree; no git writes made
- Candidate identity (preflight `--shape`, PASS): `163a9086113d0658e1d33dc12b3dc59889f61f39d3cfb1031300eb77557f4917`, 19 files
- Applicable audit: none
- No warns.

## Structural summary

- SKILL.md 44 lines, 11 routes (thresholds, alignment-mt, complexity, fragment-tss-frip, tss-encode, replicates, preseq, aggregate, diagnose, extra-checks, other-skills). references/background.md, citations.md. Root LICENSE kept.

## Scripts written

None new. The four shelf scripts are copied unchanged: library_complexity.py, atac_qc_metrics.R, encode_tss_enrichment.py, aggregate_qc.py. samtools, deepTools, preseq, MultiQC and sex-check commands are shown, not scripted. All unexecuted after the recut (shelf scripts copied unchanged keep whatever shelf execution evidence they had).

## Open ambiguities for audit

- aggregate_qc.py and atac_qc_metrics.R each embed the grading thresholds; routes/thresholds.md repeats them. Keep in sync if either changes.
- ATAC QC acceptable/reject bands are partly 'working convention' per the source; marked as such in routes/thresholds.md.
- Idea for audit: a script that runs alignment-mt and feeds metrics.json to aggregate_qc.py end to end.

## Worktree safety

- Run-owned: `skills\ca-bio-atac-seq-atac-qc\`, this handoff, one row in `skills\README.md`.
- Pre-existing/user-owned: `test/validate.bats` untouched; sibling `skills/ca-*` folders of the other worker untouched.
- Product commits/pushes: none. Tooling impact: none.

## Transition assertion

- Next-phase prerequisites met: yes.

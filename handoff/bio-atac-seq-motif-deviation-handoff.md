# Handoff: bio-atac-seq-motif-deviation / orchestrator (candidate-ready)

- Updated: 2026-09-30
- Lane: 3
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent; did not fix or initially audit)
- Next role: orchestrator (commit exact bytes to make `ready`; intake makes `done`)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/motif-deviation
- Working tree: F:\OpenScience\wt\atac-motif-deviation\skills\bio-atac-seq-motif-deviation
- Branch/worktree: fix/atac-motif-deviation, start 3186916; files untracked, no commit
- Candidate identity (sha256-manifest-v1): `fb58807b04cb2e753dce4d199ef54c057c2d762635c526a0e7aef124e2a19c4e` (6 files, 29,756 bytes); recomputed live before and after execution, unchanged
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-motif-deviation\reaudit-run\ (report.json, viewer.md, source-identity.json). Superseded initial audit d645db4d: 60/100.

## Readiness decision: candidate-ready

Score 86 (Production Ready), static 86, execution avg 86.6, Layer 1 34.6, Layer 2 52.0, assertions 18/20 (90%), no veto, no open P0. Rubric zip sha256 e54e9ff8...

## Completed this phase

- Independent retest of every claimed fix. Bulk script with depth.tsv run twice: byte-identical; unseeded control differs, so reproducibility comes from set.seed (MOTDEV-001, -003).
- Signac direct chromVAR route verbatim on 1.17.1 and 1.16.0: 879 x 1,853, 0 NA, identical (MOTDEV-002).
- ArchR: no-guard fails on NA, guard passes; Skill honestly says full-scale recurrence is untested (MOTDEV-004).
- Biology matches: K562 GATA2/GATA1::TAL1 up, GM12878 SPIB/Spi1/IRF4/EBF1 up; heatmap legible.
- Reused only identity-matched evidence (chromVAR hand-check, JASPAR workaround); ArchR upstream lines identical to origin.

## Open findings (none blocking)

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| MOTDEV-013 | P2 | open (new) | reaudit-run\scripts\analyze_z.py; SKILL.md line 22 | "top motifs exceeded 9" is wrong for z (max 7.24; logFC reaches ~14). One-line edit, but editing changes the identity and requires re-audit; orchestrator may accept as-is |
| MOTDEV-004 | P2 | residual | reaudit-run\logs\archr_guard.log | Guarded, not root-caused; full-depth recurrence unproven, stated in the Skill |

All other MOTDEV-001..012 dispositions confirmed.

## Failed or blocked surfaces

None failed. Not run: ArchR upstream chain (reused first-pass, lines identical to origin), Bioc 3.23/R 4.6, whole-genome PBMC set. Restricted-access items: none.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-motif-deviation\TOOLS.md (delta); fingerprint 91dcd6702bfba8518d2ff53ff1fec2bf447b62d06a091c00124c7ee4e1118ecd verified live
- Run evidence: F:\OpenScience\audits\bio-atac-seq-motif-deviation\reaudit-run\ (scripts\, logs\, bulk_A/B/U, guard_missing, out_signac*)
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-run\ and this handoff only; candidate not edited
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py and tools\test_run_mercury_worker.py (untouched)
- Records state: unpublished, uncommitted (per instruction)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (commit exact bytes, then publish record with `tools/publish_audits.py --run-dir` and regenerate audit index)

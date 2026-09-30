# Handoff: bio-atac-seq-single-cell-atac / orchestrator (commit and intake)

- Updated: 2026-09-30
- Lane: 2
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (independent final re-audit)
- Next role: orchestrator (commit exact bytes to the optimized shelf, then intake)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/single-cell-atac
- Working tree: `F:\OpenScience\wt\atac-single-cell-atac`; candidate `skills\bio-atac-seq-single-cell-atac` (untracked, uncommitted)
- Branch/worktree: fix/atac-single-cell-atac, starting commit 3186916
- Candidate tree hash: `sha256-manifest-v1 4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286` (6 files, 34,930 bytes), recomputed live before and after execution; no `__pycache__`
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\reaudit-run\` (report.json, viewer.md, source-identity.json), identity 4ced0da5...; supersedes `initial-audit-20260930\` (da2da9c8..., 71, Reject)

## Completed this phase

- Independent final re-audit: decision **candidate-ready**. Score 86; static 86; execution avg 86.0; Layer 1 34.75; Layer 2 51.25; assertions 31/31; no veto; no open P0/P1.
- All claimed fixes retested from the live tree (shipped signac_workflow.R on 3 args and its missing-column stop; SnapATAC2 2.10.0 block; ArchR guard; WNN; AMULET fragment; PEAKVI; cell-cycle LSI regression); see `reaudit-run\viewer.md` and `reaudit-run\logs\`.
- Relaxed QC on the chr1 slice is disclosed in SKILL.md; Cell Ranger ATAC/ARC and the AMULET BAM route are not claimed executed.

## Open findings and blockers (all P2, none blocking)

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| Cell Ranger ATAC 2.x / ARC metadata untested | P2 | blocked (10x registration) | `reaudit-run\report.json` rec 1 | after-action: test with 10x access |
| AMULET BAM route not executed | P2 | blocked (no CB-tagged BAM) | rec 2 | after-action |
| Audit narrative sentence in `references/specialized-topics.md` line 24 | P2 | open | rec 3 | optional wording fix; changes identity if applied (would need a tooling-free re-audit of bytes) |
| SnapATAC2 "removed in 2.9" unverified | P2 | open | rec 4 | optional wording fix, same caveat |

Failed or blocked surfaces: none failed. Blocked: Cell Ranger ATAC/ARC, AMULET BAM route. Reused (identity-matched, unchanged text and fingerprints): ArchR downstream steps, Signac CallPeaks, scDblFinder, tabix.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\TOOLS.md` (delta); environment fingerprint a71616d9... unchanged.
- Run evidence: `reaudit-run\{scripts,logs,output}`; rubric skill-auditor.zip e54e9ff8... (unchanged).
- Restricted-access items: Cell Ranger ATAC/ARC (10x registration), AMULET BAM route.
- Tooling impact: none

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\reaudit-run\` and this handoff; candidate untouched
- Pre-existing/user-owned changes: `tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py` in optimizing-agent-science-skills (untouched)
- Records state: uncommitted; NOT published to the records repo (publish with `tools/publish_audits.py --run-dir` then `npm run audits:index` / `audits:check` when the orchestrator commits)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

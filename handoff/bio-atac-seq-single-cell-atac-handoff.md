# Handoff: bio-atac-seq-single-cell-atac / orchestrator commit

- Updated: 2026-09-30 (delta RA-1)
- Lane: 2
- Status: candidate-ready
- Owner leaving: independent final re-audit worker (reaudit-10x)
- Next role: orchestrator (commit the exact bytes; no fixer needed)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/single-cell-atac
- Working tree: `F:\OpenScience\wt\atac-single-cell-atac`; candidate `skills\bio-atac-seq-single-cell-atac` (untracked, uncommitted), branch fix/atac-single-cell-atac
- Candidate tree hash: `sha256-manifest-v1 01b8b5025bee5ae72e7c71dd81caf3602744838da3079f205fad44c890b74c68` (6 files, 38,189 bytes; RA-1 sentence only vs d12a77c4), verified live before and after execution
- Applicable audit: `F:OpenScienceuditsbio-atac-seq-single-cell-atacdelta-ra1-20260930` (final 89); prior `reaudit-10x` (88) for unchanged surfaces

## Completed this phase

- Independent retest of the ARC/ATAC 2.1.0/ATAC 1.0.1 paths through `signac_workflow.R`, both AMULET routes per the flag table, AMULET misuse controls, and regressions (WNN, cell-cycle, SnapATAC2, ArchR guard, PEAKVI).
- Readiness: final 88, static 90, execution avg 87.1, Layer 1 34.9, Layer 2 52.3, assertions 30/31, no veto, no open P0/P1. Decision: candidate-ready.
- ARC approximations: mito adequate (same definition as ATAC); blacklist ratio is peak-level and inert on ARC (max 0.004), disclosed as a substitution but not as inert.
- Cell Ranger not run; Skill does not claim it was.

## Required next actions

1. Orchestrator: commit the exact bytes above to the optimized shelf, then publish the record (`tools/publish_audits.py --run-dir ... --artifact ...`, `npm run audits:index`, `npm run audits:check`) and run inventory refresh after the product commit. Publication was not done by this phase.
2. RA-1 is fixed in the candidate; commit these exact bytes.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | RA-1 closed by delta audit `delta-ra1-20260930` (final 89) | - | - |

Failed/blocked surfaces: none. Unexecuted by decision: Cell Ranger ATAC/ARC `count` (upstream).
Non-blocking: `FractionCountsInRegion` soft-deprecated in Signac 1.17; tooling README says ARC fragments use `atac_barcode` (measured `barcode`).

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\TOOLS.md` (sha256 6089874d...); envs bio-atac-seq-single-cell-atac-{r,py,amulet}, unchanged
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-single-cell-atac\reaudit-10x\{scripts,logs}`
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: `reaudit-10x\`, this handoff, scratch work dirs `audit-envs\...\work\reaudit10x_*`
- Pre-existing/user-owned changes: none seen; candidate untouched, no `__pycache__`
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

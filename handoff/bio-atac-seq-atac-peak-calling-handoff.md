# Handoff: bio-atac-seq-atac-peak-calling / orchestrator (candidate-ready)

- Updated: 2026-09-30
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (lane 1, independent; did not write, fix or initially audit)
- Next role: orchestrator (commit exact bytes to make `ready`, then intake)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/atac-peak-calling
- Working tree: F:\OpenScience\wt\atac-atac-peak-calling\skills\bio-atac-seq-atac-peak-calling
- Branch/worktree: fix/atac-atac-peak-calling, base 3186916 (5 files staged/modified, uncommitted)
- Candidate identity: sha256-manifest-v1 b19054ded9df6cf3d48b45b6f38c7b209454bb2627f95b5f7d73c794a02720c2 (5 files, 39,370 bytes); recomputed at start and end of re-audit, unchanged
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\reaudit-run\ (this identity). Prior: initial-audit-20260930 (e8bc49ba..., 76, Beta Only)

## Completed this phase

- Independent re-audit: score 87 (Production Ready): static 85, execution avg 88.0, Layer 1 35.2, Layer 2 52.8, assertions 18/19 (94.7%), no veto, no P0/P1.
- Every claimed fix retested by me: disjoint pseudoreps, Nt/N1/N2/Np and ratios on a passing (PASS 1.155/1.093) and a genuinely failing library (FAIL 3.394/4.906), install recipe (dry-run solve; old line fails), MACS2 mode, guards, conservative set, bigWig readback, Genrich, hmmratac, NFR, chrM recipe.
- Report and viewer: reaudit-run\report.json (schema checklist validated, scripts\validate_report.py), viewer.md, source-identity.json.

## Required next actions

1. Orchestrator: commit the exact candidate bytes on the optimized shelf, reconcile provider metadata, bind the final audit to the full commit, then publish the record (not done here) and run intake.
2. Optional: apply ATACPC-015/016 wording fixes before commit only if identity change is acceptable; that would require re-audit of the changed bytes.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ATACPC-012 | P2 (was P3) | open, non-blocking | report.json rec 2 | ROSE snippet static-only, labelled illustrative |
| ATACPC-015 | P2 | new, non-blocking | report.json rec 1 | description names 501bp consensus peaks not built |
| ATACPC-016 | P2 | new, non-blocking | scripts\guards_and_recipes.log | chrM idxstats recipe leaves chr1 reads whose mate is on chrM |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-atac-peak-calling\TOOLS.md (sha256 cccc0250..., env fingerprint 08bd20df...02b6 unchanged)
- Run evidence: reaudit-run\scripts\*.log, reaudit-run\out\ (pass/fail/macs2 logs, IDR plots); raw outputs F:\OpenScience\audit-envs\bio-atac-seq-atac-peak-calling\run\reaudit\
- Failed/blocked surfaces: one assertion failed (input 2, first failing-library attempt hit a transient drvfs truncated-BAM read under 3 concurrent runs; rerun passed; not reproduced in 4 other runs). ROSE static-only. chrM guard tested on a synthetic 3-read fixture only (source BAMs lack chrM); judged adequate. Whole-genome, mm10, standalone HMMRATAC, HOMER, chromap untested.
- Reused evidence: delta-pass fresh-env install and script run (same bytes and fingerprint).
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-run\ dir, run\reaudit\ outputs, this handoff. Candidate not edited.
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched); other lanes' handoffs untouched
- Records state: uncommitted, not published to the records repo
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (candidate-ready)

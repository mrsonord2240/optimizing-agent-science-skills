# Handoff: bio-atac-seq-differential-accessibility / fix-scientific-skill

- Updated: 2026-09-30T03:10:00-07:00
- Lane: 5
- Status: ready-for-phase
- Owner leaving: claude-initial-audit-phase
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/differential-accessibility (read-only)
- Working tree: F:\OpenScience\wt\atac-differential-accessibility\skills\bio-atac-seq-differential-accessibility
- Branch/worktree: fix/atac-differential-accessibility (base 3186916)
- Candidate tree hash: sha256-manifest-v1 890c5349e6800257d819457a4704a35b14f2fd5a48fe3dd6c3b751f73ad3c7d7 (5 files, 38661 bytes), re-verified live
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\initial-20260930\report.json (same identity; Reject, diagnostic 64, research veto M4 FAIL; not published to records)

## Completed this phase

- Verified identity; ran CLI, LIB normalization, SVA, CLI-arg, null-result and label probes on real ENCODE data (WSL env, TOOLS.md).
- Inspected figures via PNG re-render of the same plot calls (no PDF rasteriser) plus PDF page counts.
- Wrote report.json, viewer.md, source-identity.json, finding-ledger.md, scripts, evidence. No audit-local repair.

## Required next actions

1. Fix DAC-001 (P0), then DAC-002, DAC-003 (P1), DAC-004..007 (P2), DAC-008/009 (P3) in ledger order; rerun `scripts/run.sh` modes for each.
2. Classify tooling impact. New CLI flags or an edgeR backend may need a tooling delta.

## Open findings and blockers

Ledger: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\initial-20260930\finding-ledger.md

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| DAC-001 | P0 | open | evidence\sva.log | SVA branch crashes on 4 samples, SVs unused; fix or remove |
| DAC-002 | P1 | open | evidence\cli.log | CLI args 2-5 silently ignored (absorbs TOOL-002) |
| DAC-003 | P1 | open | evidence\norm.log | Default NATIVE=RLE+RiP vs docs' full-library; reconcile and log |
| DAC-004 | P2 | open | work\plots\plt_annoplot.pdf | print plotDistToTSS |
| DAC-005 | P2 | open | evidence\null.log | Guard zero-hit results |
| DAC-006 | P2 | open | evidence\labels.log | treated/control hard-coded, undocumented |
| DAC-007 | P2 | open | TOOLS.md | edgeR/RUV/spike-in/design only recipes (NORM-001..003) |
| DAC-008 | P3 | open | evidence\norm.log | Log prints "nmode"; plot titles 1835 vs 1096 |
| DAC-009 | P3 | open | script line 8 | hg38 TxDb hard-coded |

Deferred/static-only: spike-in, covariate `design=`, other reference snippets. Unverified: method-reference claim that DiffBind default is DBA_NORM_LIB/full. Blocked: none. PDF rasteriser absent (limit recorded).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\TOOLS.md; env fingerprint 2998eae45e95156bbe8b1ec4f619756fe7f8e1803c9931270a3f7a4594d54236
- Run evidence: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\initial-20260930\ (evidence\, scripts\, work\plots\)
- Restricted-access items: none
- Tooling impact: none (audit only)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\ (no Skill bytes touched)
- Pre-existing/user-owned changes: tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted paths above; not published (orchestrator publishes)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

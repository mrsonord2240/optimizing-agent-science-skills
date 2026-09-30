# Handoff: bio-atac-seq-differential-accessibility / orchestrator (commit and intake)

- Updated: 2026-09-30T06:30:00-07:00
- Lane: 5
- Status: candidate-ready
- Owner leaving: claude-reaudit-phase (independent of fix and initial audit)
- Next role: orchestrator (optimize-scientific-skills)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/differential-accessibility
- Working tree: F:\OpenScience\wt\atac-differential-accessibility\skills\bio-atac-seq-differential-accessibility
- Branch/worktree: fix/atac-differential-accessibility (base 3186916), files untracked
- Candidate tree hash: sha256-manifest-v1 dd1e7bda67b8992abed303553522a42d73f5af9fb5c69bbb955f3886a5463238 (5 files, 46279 bytes), verified live before and after re-audit
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\reaudit-run\report.json (this identity)

## Completed this phase

- Independent re-audit: final 86 Production Ready; static 85, execution avg 86.8, assertions 28/29, no veto, no open P0.
- P0 DAC-001 retested on real ENCODE data: SV enters `~SV1 + Condition`, output equals an independent svaseq+DESeq2 fit, results change (1372 to 822 sites). DAC-002..010 reproduced fixed.
- Figures rasterised with poppler and inspected (default and SVA modes).
- Records: reaudit-run\ (report.json, viewer.md, source-identity.json, scripts\, logs\, png\). Not published to the records repo.

## Required next actions

1. Orchestrator: commit exact bytes to the optimized shelf, publish the reaudit-run record with tools/publish_audits.py, then run `npm run audits:inventory` and `npm run audits:check`.
2. Optional, before or after commit: address the P2s below (would change bytes and require re-audit of identity).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| R-001 | P2 | open | reaudit-run\logs\sva_probe.log | SVA mode skips blacklist filter (0 of 2260 affected here); warn or apply dba.blacklist |
| R-002 | P2 | open | reaudit-run\viewer.md | Document SVA-mode limits in SKILL.md/method-reference; warn when --method used with --sva |
| R-003 | P2 | open | reaudit-run\logs\fold_probe.log | DiffBind fold is an lfcThreshold test vs hard filter in SVA mode; document or unify |
| R-004 | P2 | open | reaudit-run\report.json | Non-human TxDb untested; add SVA low-n caution |

No blockers. Non-human TxDb is static-only; RUVseq/spike-in are recipe-only (not counted as executed).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\TOOLS.md (env fingerprint 2998eae4...4236; poppler env b0ea9386...dd04), unchanged
- Run evidence: F:\OpenScience\audits\bio-atac-seq-differential-accessibility\reaudit-run\
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: audits\...\reaudit-run\, this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

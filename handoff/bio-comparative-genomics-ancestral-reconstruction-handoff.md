# Handoff: bio-comparative-genomics-ancestral-reconstruction

## Status

- Updated: 2026-09-29 UTC (2026-09-28 America/Los_Angeles)
- Lane: 3; phase: independent final re-audit; auditor was independent of initial audit and fix.
- Decision: `candidate-ready` for exact bytes below; all readiness floors pass and no findings remain open.
- Audit record: `candidate@a9eb2d1e1c3a-final-reaudit-opt10-20260929` in `audits/skills/bio-comparative-genomics-ancestral-reconstruction/`.

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:comparative-genomics/ancestral-reconstruction`; subtree `9f7e2256c6b8246e58387a268006a675df9fd866`.
- Candidate: `F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction` on `optimize/ten-20260928-lane3-ancestral-reconstruction`, base commit `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact identity: `sha256-manifest-v1:a9eb2d1e1c3ac7f89d63f11deb7a436c14ab0c78a6469911812aa510eeb93e07`; manifest is 17 files / 1,628 bytes. Before and after manifests match.
- Source identity, all file hashes, tooling hashes, and evidence hashes are in `final-reaudit-opt10-20260929/source-identity.json`.

## Audit result

- Schema-valid report: `final-reaudit-opt10-20260929/report.json`; viewer: `final-reaudit-opt10-20260929/viewer.md`.
- Static 88; execution average 95.0; Layer 1 average 38/40; Layer 2 average 57/60; assertions 15/15; final 92/100 (`Production Ready`).
- Structural/security veto PASS; research integrity veto PASS. The JSON schema/arithmetic/readiness validator passed at `evidence/schema-validation.json`.
- Fresh CODeml 4.10.10 executions passed for codon and both protein writer/parser routes. Every parsed value across 7 nodes × 110 sites per route matched that run's own PAML `rst` rows.

## Findings

- `TOOL-ASR-001` through `TOOL-ASR-006` and `ASR-007` through `ASR-011` are all fixed and independently confirmed; details are in `final-reaudit-opt10-20260929/finding-ledger.md`.
- The source-derived PAML expectations eliminate run-specific posterior constants. Full-tree `rg` found no unconditional corHMM superiority or mandatory hidden-rate claim.
- No new finding, open P0, remaining finding ID, or veto failure.

## Evidence and reusable coverage

- New raw run root: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\final-reaudit-opt10-20260929`.
- Fresh evidence: `evidence/paml-focused.log` (4/4 unit tests plus all three real PAML fixture parsers); `evidence/real-codon-paml/result.json`; `evidence/real-protein-paml/{provider,extracted}/result.json`; `evidence/runtime-boundary.log`; `evidence/corhmm-claim-search.log`.
- Reused identity-matched evidence: IQ-TREE (`../fix-opt11-20260928/evidence/iqtree-results.json`), GRASP (`grasp-validation.txt`, `grasp-candidate-wrapper.log`), R/corHMM/OUwie (`../fix-opt11-20260928/scripts/retest_r.R`, `evidence/r-sessionInfo.txt`), and no-data (`python-results.json`). Byte/runtime/interface/fixture checks are recorded in `evidence/reuse-validation.json`.
- Optional documented-only FastML, RevBayes, BayesTraits, MrBayes, BEAST2, RPANDA, and GRASP web service were not counted as executed support. Before claiming them as runnable, validate their current interface and inspect representative scientific output.

## Worktree and safety

- Candidate remained read-only during audit. Candidate status is its expected untracked Skill subtree; no `__pycache__`, `.pyc`, or `.pytest_cache` artifacts remain.
- Origin checkout is clean. Pre-existing control-repository modifications, deletions, and unrelated untracked Mercury files were preserved.
- No product commit, push, release, provider mutation, or Marketplace action occurred. Only this canonical handoff and the audit-record publication/views were in scope.

## Next role

- Orchestrator: accept this exact candidate as `candidate-ready`, then perform the separately authorized commit/intake workflow.
- Do not rerun the 1,000-map R suite ceremonially; reuse its identity-matched evidence unless relevant bytes, runtime, interface, inputs, or assumptions change.

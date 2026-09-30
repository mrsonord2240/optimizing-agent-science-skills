# Handoff: bio-atac-seq-deep-learning-atac / fix-scientific-skill

- Updated: 2026-09-30T05:55:00-07:00
- Lane: 4
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill (initial audit)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/deep-learning-atac
- Working tree: F:\OpenScience\wt\atac-deep-learning-atac (skills\bio-atac-seq-deep-learning-atac)
- Branch/worktree: fix/atac-deep-learning-atac, starting commit 3186916
- Candidate tree hash: sha256-manifest-v1 c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943 (6 files; re-verified live, unchanged)
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\initial-audit-20260930\report.json (same identity)

## Completed this phase

- Diagnostic audit: static 67, execution avg 56.0, final 60, Reject (research veto FAIL: methodological ground + code usability). Skill veto PASS.
- New bounded evidence: script as written (34 s failure), log2FC formula numeric test, contribs_bw + modisco -i, surface probes; tooling-phase evidence reused (identity-matched).
- Corrected TOOLS.md claim: step 3 `chrombpnet pipeline` was killed at its 3,600 s cap in the DeepSHAP stage, not exit 0 (DLA-011).
- Artifacts: report.json (schema-validated by scripts\validate_report.py), findings.json, finding-ledger.md, viewer.md, source-identity.json, scripts\.
- Not published to records (orchestrator does that). No Skill edits, commits or pushes.

## Required next actions

1. P0 first: DLA-001 (log2FC formula), DLA-002 (add `prep nonpeaks`, fail-fast inputs).
2. P1: DLA-003 to DLA-010 (variant list schema, tangermeme route, modisco route via `modisco motifs -i`, versions/envs, pred_bw 10-col, calibrated thresholds, QC gate, Enformer/Borzoi/scBasset guidance).
3. P2/P3: DLA-011 to DLA-014. Re-run affected cases using the saved scripts.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| DLA-001 | P0 | open | evidence_log2fc.json | fix formula (~5x understatement), tuple outputs |
| DLA-002 | P0 | open | run_script_missing_nonpeaks.log | add nonpeaks generation and input checks |
| DLA-003 | P1 | open | evidence\smoke_variant_scorer.log | 5-col headerless variants, pybedtools, output columns |
| DLA-004 | P1 | open | probe_surfaces.log | chromBPNet .h5 variants via variant-scorer; tangermeme only for torch models |
| DLA-005 | P1 | open | run_contribs_bw.log; run_modisco_legacy_h5.log | replace shap_to_modisco with contribs_bw h5 -> `modisco motifs -i`; (N,4,L); tomtom |
| DLA-006 | P1 | open | TOOLS.md | per-tool envs; correct TF pins |
| DLA-007 | P1 | open | evidence\pred_bw.log | 10-col regions |
| DLA-008 | P1 | open | evidence\encode_model_variant_scores.tsv | calibrated significance, not |log2FC|>1 |
| DLA-009 | P1 | open | evidence\chrombpnet_*metrics.json | QC gate |
| DLA-010 | P1 | open | evidence\kipoi_probe.log, smoke_scbasset.log | Enformer/Borzoi/scBasset guidance |
| DLA-011 | P2 | open | evidence\chrombpnet_step3.log | document interpret-stage runtime |
| DLA-012 | P2 | open | evidence\chrombpnet_help.log | stale flags |
| DLA-013 | P2 | open | scripts\chrombpnet_pipeline.sh | quoting, scorer path check |
| DLA-014 | P3 | open | static | cite or soften claims |

Restricted/blocked (not findings): R1/R2 full-scale chromBPNet training/interpretation (TF 2.8 CPU-only, A100/24 h); R3 scBasset on Keras 3 (CPU TF 2.15 only); R5 Borzoi not installed, Enformer not in Kipoi.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\TOOLS.md; env fingerprint 06fc27986ce7b28c4e102689c57fa41596fc3d2716402daaa8309f93bf9cfa29 (envs dlatac-tf, -torch, -tf2, -tf2k2)
- Run evidence: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\initial-audit-20260930\ (report.json, runs\, scripts\) and ..\evidence\
- Restricted-access items: none gated
- Tooling impact: none (Skill bytes unchanged); fixer may need a chromBPNet-derived attribution set at scale for DLA-005 validation

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\initial-audit-20260930\; this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py and tools\test_run_mercury_worker.py (untouched); candidate dir untracked in worktree
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

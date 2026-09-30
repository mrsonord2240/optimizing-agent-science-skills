# Handoff: bio-atac-seq-deep-learning-atac / orchestrator (commit + intake)

- Updated: 2026-09-30 (re-audit complete)
- Lane: 4
- Status: candidate-ready
- Owner leaving: independent final re-audit worker
- Next role: optimize-scientific-skills orchestrator (commit exact bytes, then intake); optional trivial P2 follow-up via fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/deep-learning-atac
- Working tree: F:\OpenScience\wt\atac-deep-learning-atac\skills\bio-atac-seq-deep-learning-atac (branch fix/atac-deep-learning-atac, base 3186916, untracked subtree)
- Candidate tree hash: sha256-manifest-v1 3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87 (10 files, 47,690 bytes), verified live before and after re-audit
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\reaudit-run\ (report.json, viewer.md, source-identity.json); prior rejected audit initial-audit-20260930 (c62d899a..., 60/100)

## Completed this phase

- Independent re-audit: final 88/100 (static 87, execution avg 88.2, Layer 1 34-38, Layer 2 50-55, assertions 22/23), no veto, no open P0: Production Ready by rubric, so candidate-ready.
- P0 DLA-001 reproduced fixed by raw Keras, shipped torch script and variant-scorer (200 real SNPs) plus planted-truth fixture; P0 DLA-002 fixed: fresh-directory pipeline exit 0 (43 min, 1 epoch), RESUME tail 22 s, 7 guards.
- Four new scripts, pred_bw awk contract, MoDISco (lite and tomtom), Enformer, scBasset 1 epoch all re-executed. Evidence: reaudit-run\*.log, reaudit-run\scripts\.

## Required next actions

1. Orchestrator: commit the exact bytes above to the optimized shelf, bind the accepted audit to that commit, publish the record (not done here), run `npm run audits:inventory` and `audits:check`.
2. Optional: fix DLA-015 and DLA-016 (below) before commit; that changes bytes and needs a fresh identity plus a quick re-check.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| DLA-015 | P2 | open | report.json; chrombpnet source (`CHROMBPNET.py`, `reads_to_bigwig.py`) | Declare bedtools and bedGraphToBigWig in SKILL env table and step 0 of the script |
| DLA-016 | P2 | open | scripts/chrombpnet_pipeline.sh line 3 | "SKILL.md step 5" should read step 6 |

Blockers: none. Restricted, not claimed executed by the Skill: full-scale chromBPNet training/interpretation and the old `bias pipeline`/`pipeline` exit (TF 2.8 CPU-only), scBasset on Keras 3, Borzoi, TOBIAS, saturation mutagenesis. Reused, not re-run: `contribs_bw` then `modisco -i` (delta and fix logs, unchanged env and bytes).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\TOOLS.md (delta); env fingerprint 06fc27986ce7b28c4e102689c57fa41596fc3d2716402daaa8309f93bf9cfa29 unchanged
- Run evidence: reaudit-run\pipe_run1.log, pipe_resume.log, guards_gate.log, log2fc_indep.log, predbw_awk.log, torch_scripts.log, scbasset_1epoch.log
- Restricted-access items: none gated; R1, R3, Borzoi as above
- Tooling impact: none

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-deep-learning-atac\reaudit-run\ ; heavy outputs under F:\OpenScience\audit-envs\bio-atac-seq-deep-learning-atac\run\reaudit\
- Pre-existing/user-owned changes: tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: not published (per assignment); no __pycache__ in the Skill tree
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

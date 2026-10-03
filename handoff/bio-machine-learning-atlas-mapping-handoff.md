# Handoff: bio-machine-learning-atlas-mapping / fix-scientific-skill

- Updated: 2026-10-03T14:15:00-04:00
- Lane: 3 (batch 3b)
- Status: ready-for-phase
- Owner leaving: initial-audit worker (lane 3b)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6 (files=5, bytes=30516), re-verified with `tools/skill_preflight.py --offline` after the audit (PASS, no pycache)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-machine-learning-atlas-mapping\candidate@d4048dcc887b-initial-lane3b-20261003\report.json (identity above; score 77, Limited Release, no veto)

## Completed this phase

- Static review plus 5 executed inputs on CPU: scarches_annotation.py unmodified x2 (acc 0.965/0.967), saved-model snippets, ood_gating_demo.py, held-out B cells, held-out Monocytes.
- Held-out Monocytes: only 2.7% gated, 95.4% confidently labelled DC; held-out B cells 87.4% gated (AM-001).
- `predict(soft=True)` reproduces as a DataFrame (2638 x 8) (AM-003).
- Published record with 15 scripts/evidence files; views regenerated, `npm run audits:check` passes.
- No audit-local repair; no Skill bytes changed.

## Required next actions

1. Fix AM-001 (P1, runnable bytes + text): scope the gate claim; add a held-out-type spike-in check; relabel the demo's "softmax" as kNN probability.
2. Fix AM-005 (runnable bytes): seed `scvi.settings.seed`, write the annotated query h5ad in scarches_annotation.py.
3. Fix AM-002, AM-003, AM-004 (text only): label prose-only/heavy methods not executed; document predict(soft=True) as DataFrame; make snippets self-contained and document h5ad input fields.
4. Report tooling impact: AM-001/AM-005 change scripts, so request a tooling delta (rerun the held-out harness).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AM-001 | P1 | open | audits\skills\...\scripts\evidence\heldout_Monocytes.json, heldout_B_cells.json | scope claim, add spike-in check script (runnable bytes) |
| AM-002 | P2 | open | report.json (static) | text only |
| AM-003 | P2 | open | scripts\evidence\saved_model_surgery.log | text only |
| AM-004 | P2 | open | scripts\evidence\saved_model_surgery.log | text only (docstring/comment) |
| AM-005 | P2 | open | scripts\evidence\canonical_a.json vs canonical_b.json | runnable bytes |

Deferred (static-only): Symphony, Azimuth (prose, R); heavy-optional (not tooled): scPoli, popV, treeArches/scHPL, scGPT/Geneformer. Blocked: none.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 2004cafd57d3d4dcbc1bf03b9c312ccdb1f61d222ee7b64d94c8442b6e1f8c96)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; runtime single-cell-transcriptomics-analyst venv (scvi-tools 1.5.1, CPU)
- Run evidence: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\initial-lane3b-20261003\ (report.json, viewer.md, finding-ledger.md, scripts\, logs\, work\)
- Restricted-access items: none
- Tooling impact: not applicable to this phase (no Skill bytes changed); fixes for AM-001/AM-005 will change runnable bytes

## Worktree safety

- Run-owned changes: the run directory above; records `audits/skills/bio-machine-learning-atlas-mapping/candidate@d4048dcc887b-initial-lane3b-20261003/`; regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; sibling workers' records and handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

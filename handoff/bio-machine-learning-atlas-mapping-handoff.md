# Handoff: bio-machine-learning-atlas-mapping / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-04:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: tooling worker (lane 3, machine-learning batch)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping
- Branch/worktree: normalize/ml-lane3 from 29f5446 (Skill dirs untracked by design)
- Candidate tree hash: d4048dcc887b51c820dba4669bf05620829970e083f7512d24a2539953ad48a6 (files=5, bytes=30516), re-verified with `tools/skill_preflight.py --offline` after tooling (PASS)
- Applicable audit: none

## Completed this phase

- Both scripts and the saved-model-path snippets run on CPU in the single-cell venv (scvi-tools 1.5.1); `scarches_annotation.py` ran unmodified end to end in 1m29s (not heavy: no GPU, under 2 min).
- Built a small real reference/query pair (PBMC 1k v3 with CellTypist silver labels vs PBMC3k v1): accuracy 0.975 against the PBMC3k annotation, 1.6% flagged Unknown.
- Added PBMC3k raw/processed to ML public-data and the derived pair under derived\atlas-pair (README rows, script `make_atlas_pair.py`).

## Coverage map (per surface)

- `scripts/scarches_annotation.py`: executed unmodified (`logs/atlas_scarches_asis.log`, `atlas_scarches_score.log`).
- `scripts/ood_gating_demo.py`: executed (synthetic).
- SKILL.md snippets 1-3 (saved-model surgery, scANVI save, `predict(soft=True)`, kNN gate): executed (`logs/atlas_saved_model_surgery.log`).
- Symphony/Azimuth (prose only, R) not exercised; scPoli/popV/treeArches/scGPT/Geneformer heavy-optional (not tooled): Skill must label them not executed.

## Required next actions

1. Audit batching: **light** (every required surface runs on CPU in under 2 minutes; inputs under 30 MB).
2. Audit against the exact identity above; run from saved scripts in F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3 (logs in its `logs` folder).
3. Do not edit Skill bytes in the audit; findings go to the ledger. Needed-but-missing inputs: request a tooling-delta pass.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | - | - | - | Notes for audit: `predict(soft=True)` returned a DataFrame (2638 x 8), not an ndarray as the normalizer noted; check SKILL.md wording. Reference labels are CellTypist silver labels, not curated. |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md (sha256 2004cafd57d3d4dcbc1bf03b9c312ccdb1f61d222ee7b64d94c8442b6e1f8c96)
- Environment fingerprint: sha256 20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6 of F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\fingerprint-inputs.txt (hashes of four pip freezes); ecosystem root F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (INDEX row `machine-learning`), addendum in its TOOLS.md and `public-data\README.md`
- Run evidence: F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\smoke\ml-lane3\logs\
- Restricted-access items: none
- Tooling impact: none (no Skill bytes changed; staging additions only: PBMC3k + derived atlas pair)

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst (smoke\ml-lane3, derived, public-data, tools\pycox-venv, freeze, TOOLS.md, INDEX.md); records `audits/skills/bio-machine-learning-atlas-mapping/candidate@d4048dcc887b-tooling-20261003/TOOLS.md`; this handoff
- Pre-existing/user-owned changes: records untracked `test/validate.bats`; shelf untracked `.vscode/`; other workers' handoffs; none touched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

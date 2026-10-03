# Handoff: bio-machine-learning-atlas-mapping / prepare-scientific-skill-tooling (delta, after fix2)

- Updated: 2026-10-03
- Lane: 3 (batch 3b-1)
- Status: ready-for-phase
- Owner leaving: tooling worker (delta after fix2)
- Next role: reaudit-scientific-skill (full mode, fresh auditor)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/atlas-mapping
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-atlas-mapping (branch normalize/ml-lane3; Skill dir untracked by design)
- Candidate tree hash: 8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04 (files=7, bytes=39831); preflight PASS offline before and after, no pycache
- Prior failed re-audit: ba864911e88a... (84, Limited Release)

## Completed this phase

- TOOLS.md refreshed in place (sha256 35fbb5d8b27d7b76a9e1cfd1390ddc6315ef2156d15ff8f75c3e75d6516e9d40): F:\OpenScience\audits\bio-machine-learning-atlas-mapping\TOOLS.md
- Rerun harness rewritten for the new interface: audits\...\tooling-delta-lane3b-20261003\run_case.py `none|mono|bcell <tag>`; reads staged files only. Old derived-mode version kept as run_case.old-derived-mode.py.txt (do not run).
- Executed (4 parallel runs, summaries summary_d2_{none,none2,mono,bcell}.json in the same dir): 
  - No-flag label_marker_check.py: rc 2, usage error, empty stdout, in all 4.
  - Curated: baseline nothing flagged (T 0.703 Mono 0.900 B 0.784 ILC 0.916 DC 0.955; UNVERIFIED 13/2594); Monocytes removed DC 0.160 FLAGGED (UNVERIFIED 17/2600); B removed DC 0.525 FLAGGED (UNVERIFIED 12/2321). Megakaryocytes/platelets unverified (under 20 cells).
  - Marker presence in 1604 genes: T cells 8/8; absent: FCN1, CST3 (Mono), HLA-DPB1, CST3 (DC), CAVIN2 (Mega), JCHAIN, XBP1, SDC1 (Plasma, 1/4 present).
  - scarches_annotation.py: seeded rerun identical (2638/2638 labels, latent diff 0.0, 1.67% Unknown); query_annotated.h5ad written (2638x1604); final print line points to the curated check.
- Environment fingerprint UNCHANGED (20291632e93a3881e9704027dfe1d61f2f02fb40d64667ea992bb557bbb336a6; single-cell freeze hash b82090ff... re-taken, identical). Nothing installed, upgraded or regenerated.

## Required next actions

1. Fresh full re-audit of the exact bytes; run SKILL.md snippets as written (they are not byte-identical to earlier passes) plus the four run_case.py cases.
2. Verify AM-006/AM-007 closure and AM-001 documented-limited disposition.

## Open findings and blockers

Findings unchanged from the fix handoff (AM-006, AM-007 fixed pending re-audit; AM-001 superseded; AM-002..005 resolved). Blockers: none. Not executed by design: scPoli, popV, treeArches/scHPL, foundation models (heavy-optional); Symphony, Azimuth (prose only). The Skill must label these as not executed.

## Worktree safety

- Run-owned changes: audits\bio-machine-learning-atlas-mapping\TOOLS.md; tooling-delta-lane3b-20261003\ (run_case.py, run_case.old-derived-mode.py.txt, summary_d2_*, logs_d2_*, work\d2_*); this handoff. No staging or Skill byte changes.
- Pre-existing/user-owned untouched: records test/validate.bats; shelf .vscode/; sibling Skill dirs.
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

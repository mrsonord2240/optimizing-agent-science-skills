# Handoff: bio-comparative-genomics-ancestral-reconstruction / audit-scientific-skill

- Updated: 2026-09-28
- Lane: 3
- Status: audited-reject
- Owner leaving: `/root/lane3_comparative_audit_retry2`
- Next role: `fix-scientific-skill`

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:comparative-genomics/ancestral-reconstruction`; source subtree `9f7e2256c6b8246e58387a268006a675df9fd866`.
- Candidate: `F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction` on `optimize/ten-20260928-lane3-ancestral-reconstruction` at worktree base `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact audited identity: `sha256-manifest-v1:eea7a056a3861ff085037d0d5ae9ea566c602c831524f6a517acb6fc77b341d6` (15 files; 1,441-byte ordinal manifest).
- Before/after manifests are byte-identical and strict validation recomputes the same identity.

## Completed this phase

- Performed a fresh independent audit using rubric bundle SHA-256 `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`.
- Reproduced and adjudicated `TOOL-ASR-001` through `TOOL-ASR-006`; valid provider controls were not treated as shipped-surface success.
- Executed seven complex-mode inputs across PAML, IQ-TREE, stochastic mapping/corHMM, continuous-trait models/OUwie, GRASP, malformed posterior schemas, and taxon/outgroup mismatches.
- Report: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\initial-opt10-20260928\report.json`.
- Result: Static `65/100`; Dynamic `48.4/100`; weighted `55/100`; assertions `15/28`; **Reject**, deployable `false`.
- Skill veto: FAIL (stability, contract, determinism). Research veto: FAIL (methodological ground, code usability).

## Required next actions

1. Route to `fix-scientific-skill`; fix P0 items in ledger order before any re-audit.
2. Replace both PAML parsers with real-current-output parsing and fail-closed node/site validation.
3. Update GRASP to the official 2024 CLI/artifact contract and correct OUwie 3.0.3 usage plus interpretation boundaries.
4. Make non-BM continuous reconstruction actually use the selected fitted model or reject unsupported winners.
5. Add empty/schema/taxon/seed contracts, soften categorical scientific claims, and pin a tested corHMM source/version matrix.
6. After fixes, run a fresh independent `reaudit-scientific-skill` against a new exact candidate identity.

## Open findings and blockers

| Order | ID | Priority | Disposition |
|---:|---|---|---|
| 1 | TOOL-ASR-001 | P0 | Both PAML parsers return no records from successful real PAML 4.10.10 output. |
| 2 | TOOL-ASR-002 | P0 | GRASP command and promised output filenames are stale. |
| 3 | TOOL-ASR-003 | P0 | OUwie call is stale and the reconstruction claim exceeds current provider bounds. |
| 4 | ASR-007 | P0 | EB/lambda/kappa/delta winners are not applied to reconstruction. |
| 5 | TOOL-ASR-004 | P1 | Empty probability summaries raise `KeyError: total_sites`. |
| 6 | TOOL-ASR-005 | P1 | Missing IQ-TREE posterior columns are accepted as NaN. |
| 7 | ASR-008 | P1 | Stochastic seed and taxon mismatch contracts are missing. |
| 8 | ASR-009 | P1 | Routed reconciliation guidance uses categorical model claims. |
| 9 | TOOL-ASR-006 | P2 | corHMM `2.9+` is unpinned across CRAN 2.8 and GitHub 2.10.5. |

- Blocking condition for fixer: none. Restricted/documented-only tools do not block these fixes.
- Deferred/static-only: FastML, RevBayes, MrBayes, BEAST2, PhyloBayes-MPI, BayesTraits, RPANDA, HiSSE/FiSSE, RERconverge, ALE/GeneRax, Dollo, preprocessing/related tools, and GRASP web remain non-executable documentation claims and cannot support readiness.

## Environment and evidence

- Tool record: `F:\OpenScience\audit-envs\bio-comparative-genomics-ancestral-reconstruction\TOOLS.md`; SHA-256 `ab29fdd0e5df5a27bd2b6ed50d5a01f61d588354454dfab19942c6894f030236`.
- Environment fingerprint SHA-256: `da8b3ef12894f2f41730e89ef09335bfefb7905a8e40963546a76dcee5f6aa08`; 171-package explicit lock SHA-256: `216277a7a3841fb84bd731034fbfe09ca28a7514289e9bc15c8a8d92e6f4856c`.
- Boundary: unprivileged `sci` in WSL `science`, private mount namespace, `/mnt/openscience` only, interop disabled.
- Primary evidence: `evidence/{paml-surfaces.json,python-surfaces.json,iqtree-output-validation.txt,r-surfaces.log,ouwie-probe.log,grasp-candidate-current.log,grasp-current-validation.txt}` under the raw run root.
- Primary-source adjudication: `scientific-source-notes.md`; strict validation: `evidence/schema-validation.json` (`valid: true`).
- Viewer and fixer queue: `viewer.md` and `finding-ledger.md` in the raw run root.

## Worktree safety

- Candidate remained unchanged at the exact incoming identity; Python bytecode writes were disabled and no candidate cache artifact remains.
- No audit-local repair was attempted; all findings change a scientific method, interface, output contract, validation boundary, or provenance judgment.
- Worktree status remains only the run-owned untracked candidate tree; no candidate file was edited, staged, or committed.
- Unrelated control/user changes, including the externally reported deletion of `HANDOFF-codex-phase2.md`, were not restored, staged, or touched.
- No product or records commit, push, PR, release, submission, publication, or Marketplace action occurred.

## Transition assertion

- Full independent diagnostic audit complete: yes.
- Strict report/schema/evidence validation complete: yes.
- Candidate identity stable before/after execution: yes, `eea7a056a3861ff085037d0d5ae9ea566c602c831524f6a517acb6fc77b341d6`.
- Findings ready for fixer: yes; ordered ledger contains 4 P0, 4 P1, and 1 P2 item.
- Next role: `fix-scientific-skill`; do not treat this rejected diagnostic score or any valid control as readiness evidence.

# Handoff: bio-clinical-databases-acmg-classification / fix-scientific-skill

- Updated: 2026-09-28T14:16:24-07:00
- Lane: 3
- Status: phase-failed
- Owner leaving: /root/lane3_acmg_reaudit
- Next role: fix-scientific-skill

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clinical-databases/acmg-classification`; source subtree `b4c1f4dd04a6a53f3eba2aa56da5d830ba325e1a`.
- Working tree: `F:\OpenScience\wt\opt10-acmg-classification\skills\bio-clinical-databases-acmg-classification`.
- Branch/worktree: `optimize/ten-20260928-lane3-acmg-classification`; product HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Candidate tree hash: `sha256-manifest-v1:926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07` (seven files; 643-byte ordinal path/size/SHA-256 manifest).
- Applicable audit: `F:\OpenScience\audits\bio-clinical-databases-acmg-classification\reaudit-opt10-20260928\report.json`, exact identity above, SHA-256 `6b514ffc803687eafabb483baa15710fb7ce5d30e6b5b04d9a47b77d8f140ddf`.

## Completed this phase

- Independently read the complete re-audit and auditor contracts, reinspected all seven candidate files, verified origin/candidate/tool records, and reproduced the exact identity before and after execution.
- Executed all three Python files, 16/16 shipped regressions, standalone demo, bounded live smoke, and independent cases across all 15 callables in the pinned isolated runtime; GeneBe returned one public record and CSpec returned six GATM version records.
- Accepted ACMG-003, ACMG-004, ACMG-005, ACMG-007, ACMG-008, and ACMG-009; AlphaMissense passed 17/17, OddsPath passed 14/14, practice boundaries passed, and Tier III/IV remain distinct.
- Reopened ACMG-001, ACMG-002, and ACMG-006 with durable reproductions. PP5 and same-family duplicate evidence demonstrably changed classifications, firing the Methodological Ground veto.
- Produced a strict schema-valid record: static 76, execution 75.9, final diagnostic score 76/100 Reject, Layer 1 average 31.4/40, Layer 2 average 44.4/60, assertions 26/35 (74.3%), research veto FAIL.

## Required next actions

1. Fix ACMG-006: remove current-rule PP5/BP6 acceptance; define evidence families and reject multiple strengths/aliases/opposed codes; repair inclusive REVEL/BayesDel benign endpoints; parse real ISO calendar dates.
2. Fix ACMG-002: reject contradictory `is_nmd_predicted` and `splice_consequence` representations before PVS1 assignment; add contradiction and deletion/initiation review-state regressions.
3. Fix ACMG-001: replace the residual `>4.3 for Strong` prose with `>4.3 Moderate; >18.7 Strong` and add a documentation consistency assertion.
4. Classify tooling impact after the fix. Any code/test change requires a fresh tooling-delta pass before another independent re-audit.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ACMG-006 | P0 | open | `reaudit-opt10-20260928\evidence\execution.json` (`workflows.tavtigian`, `other_predictor_boundaries`, `somatic.invalid_date`) | Enforce current evidence-family, endpoint, conflict, and semantic-date validation. |
| ACMG-002 | P1 | open | same file, `workflows.pvs1.conflict` | Reject contradictory NMD inputs before strength assignment. |
| ACMG-001 | P2 | open | same file, `static_checks` | Remove the residual Brnich prose contradiction. |

- No candidate execution surface is blocked. InterVar/ANNOVAR remains restricted/documented-only; AutoPVS1 is unpinned/documented-only; VarSome, Franklin, and parts of manual curation remain restricted as already inventoried.
- This is a scientific rejection, not a tooling blocker; no Sam action is required.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audit-envs\bio-clinical-databases-acmg-classification\TOOLS.md`, SHA-256 `96651ce26387bcd9e04369b381b6dc5cafac6fa64f0ba5d8d1c43ac25ec85161`; fingerprint `be04749b5d2581594940a228004479fe7c8511f371fc30b5c7dad5cf38a07cd7`.
- Runtime: WSL `science` / `sci`; Python 3.12.14; requests 2.32.5; private mount namespace with `/mnt/openscience` only and `WSL_INTEROP` unset.
- Run evidence: `F:\OpenScience\audits\bio-clinical-databases-acmg-classification\reaudit-opt10-20260928`; `viewer.md` SHA-256 `4ff00b618478541bb48a5cd3c6efe069a8eb15f3e9ae525509da5224155cba28`; execution SHA-256 `63049c50400193c8b5a920bfa93d1db37d9a0eb57954b73c9caffab55389c9fd`.
- Evidence map: sibling `finding-ledger.md`, `scientific-source-notes.md`, `execution-classifications.json`, `source-identity.json`, `artifact-hashes.json`, saved scripts/inputs, and command logs. `scripts/validate_report.py` passes.
- Restricted-access items: InterVar/ANNOVAR, AutoPVS1, VarSome, Franklin/Genoox, and manual ClinGen VCI actions as classified above.
- Tooling impact: none (re-audit changed no candidate byte; a subsequent fix will likely be `changed`).

## Worktree safety

- Run-owned changes: raw re-audit root above and this canonical handoff only.
- Pre-existing/user-owned changes: none inside the lane candidate; the candidate subtree remains the lane's only untracked product path.
- A first-run `py_compile` cache was immediately moved to `evidence\quarantined-pycache`; the candidate was restored and independently revalidated at the exact incoming identity with no remaining cache files.
- Records state: the exact re-audit was published locally as `candidate@926ce0436d0d-reaudit-opt10-20260928` with 13 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit.
- Product commits/pushes: none; no PR, release, Marketplace, credential, PHI, patient/private data, or remote mutation.

## Transition assertion

- Next-phase prerequisites met: yes for `fix-scientific-skill`; no for candidate-ready.
- If no: candidate readiness requires ACMG-001, ACMG-002, and ACMG-006 fixed, tooling impact disposition completed, and a fresh independent re-audit meeting every readiness floor with no veto.

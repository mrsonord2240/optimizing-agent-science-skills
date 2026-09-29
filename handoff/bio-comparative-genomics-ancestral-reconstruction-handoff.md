# Handoff: bio-comparative-genomics-ancestral-reconstruction / reaudit-scientific-skill

- Updated: 2026-09-29T02:05:00Z
- Lane: 3
- Status: phase-failed
- Owner leaving: `/root/lane3_comparative_reaudit`
- Next role: `fix-scientific-skill`

## Source identity

- Candidate: `F:\OpenScience\wt\opt10-ancestral-reconstruction\skills\bio-comparative-genomics-ancestral-reconstruction`.
- Branch/base: `optimize/ten-20260928-lane3-ancestral-reconstruction` / `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Origin/subtree: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:comparative-genomics/ancestral-reconstruction` / `9f7e2256c6b8246e58387a268006a675df9fd866`.
- Exact identity before and after audit: `sha256-manifest-v1:0865b11e5169758a84e241ca9ab4e59ecf855add0b46c6a38153808788a85871` (16 files; 1,535-byte manifest). Full identity: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\reaudit-opt10-20260928\source-identity.json`.
- Publisher-compatible identity schema was independently checked through `publish_audits.py` modular source/candidate validators; result: `identity-validation.json`.

## Completed this phase

- Fresh independent full-skill audit and all nine initial finding adjudications completed. Report: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\reaudit-opt10-20260928\report.json`; readable report: `viewer.md`; findings: `finding-ledger.md`.
- Real PAML 4.10.10 codon `codeml` run succeeded (exit 0; complete 179,896-byte rst), but the candidate parser raised `PAML rst contains no marginal site rows`. This reopens TOOL-ASR-001 and fails research code usability. Protein PAML parsing passes.
- IQ-TREE strict posterior, GRASP official/current CLI, seeded stochastic mapping and taxon reconciliation, BM 95% intervals, fitted-object OUwie 3.0.3 exploratory points, and EB/lambda/kappa/delta refusal paths were independently tested and inspected.
- Current report schema/arithmetic validation passes: diagnostic score 80; static 81; execution average 79.9; 27/29 assertions; veto override true; grade Reject; not deployable. Readiness floors also fail for score, dynamic average, and Layer 2 average.
- ASR-009 remains P1 for categorical corHMM superiority wording. The no-prepared-biological-codon-fixture, untested GitHub corHMM 2.10.5, and OUwie single-regime diagnostic are explicitly distinguished from tested support.

## Required next actions

1. Route exact candidate bytes to a fresh `fix-scientific-skill` worker.
2. Fix and regression-test the actual codon rst marginal row grammar using real PAML codeml output; assert node/site counts and posterior validity.
3. Resolve residual ASR-009 categorical corHMM statements so wording agrees with the conditional method-selection framework.
4. After fixes, create a new immutable candidate identity and request a new independent re-audit. Do not regard this rejected identity as candidate-ready.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| TOOL-ASR-001 | P0 | Reopened | `reaudit-opt10-20260928/evidence/paml-codon-results.json`; raw `evidence/codon-paml/rst` | Codon marginal parser fails on successful current PAML output; fix then regression-test. |
| ASR-009 | P1 | Residual wording | Candidate `usage-guide.md`; `reaudit-opt10-20260928/finding-ledger.md` | Make corHMM superiority claims conditional and consistent throughout. |
| corHMM GitHub 2.10.5 | Limitation | Untested, explicitly unsupported | `reaudit-opt10-20260928/evidence/TOOLS.md`; `sources.md` | Do not claim this version as supported absent a future tooling/test pass. |
| OUwie single-regime identify | Limitation | Reproduced/documented | `reaudit-opt10-20260928/evidence/r-results.md` | Default diagnostic errors; validated check.identify=FALSE route remains exploratory and provides no uncertainty. |

No other blocker was inferred. The absent-outgroup case was rechecked from retained initial fixture evidence; the fresh exact-script attempt exceeded its bounded timeout and was not counted as a new pass.

## Environment and evidence

- Raw audit root: `F:\OpenScience\audits\bio-comparative-genomics-ancestral-reconstruction\reaudit-opt10-20260928`.
- Strict validation: `schema-validation.json`; validator script `validate_report.py`. `report.json` SHA-256 `f2ad5585265fc38cfb4608f65041d6f2a7e18ae394d1facb3ced55b088d72dd0`. Publisher-compatible `source-identity.json` SHA-256 `c58aec494fd54ee8e369c3e59b94e3690d57674023988620db6f6761f8d52f7a`. Evidence inventory `artifact-hashes.tsv` SHA-256 `5cc781c68942d338e6e856d270ea5fddd6076057be354c94656cc121fb33a733` (169 files; 18,716-byte manifest); individual hashes and lengths are listed in that file.
- Runtime/environment references: `evidence\TOOLS.md`, `evidence\tooling-delta-fingerprint.json`, `evidence\r-sessionInfo.txt`, `evidence\r-results.md`, `run-log.md`, `sources.md`.
- The public protein alignment was synonymically encoded to test codon-format parsing. This proves format incompatibility but is not biological codon-sequence validation; no prepared real biological codon rst fixture was available.
- Records are not published, per task constraints. No Marketplace, commit, stage, product/provider change, or unrelated cleanup was performed.

## Worktree safety

- Candidate source bytes remain identical to expected before/after manifests. One audit-generated `__pycache__` file was removed by exact target; no source was changed.
- Candidate worktree contains only the run-owned untracked Skill tree. Pre-existing unrelated control-repository changes/deletions were preserved.
- Only raw audit artifacts and this canonical handoff were written. No candidate files, providers, product state, or control changes were modified.

## Transition assertion

- Audit complete: yes. Strict report schema and arithmetic checks pass; exact candidate identity is verified.
- Readiness: **Reject / not candidate-ready** due to P0 TOOL-ASR-001 and research veto; diagnostic score 80/100 does not override veto. Remaining finding IDs: TOOL-ASR-001 and ASR-009.
- Route: fresh `fix-scientific-skill`. Do not publish records or continue to intake from this rejected audit.

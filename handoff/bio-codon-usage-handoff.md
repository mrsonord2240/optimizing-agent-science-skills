# Handoff: bio-codon-usage / audit-scientific-skill

- Updated: 2026-09-28T14:33:51.8951804-07:00
- Lane: 2
- Status: rejected-initial-audit
- Owner leaving: /root/lane2_codon_audit
- Next role: fix-scientific-skill

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:sequence-manipulation/codon-usage`; source subtree `3874a00444ef0856451fece587c051cfc34aaf80`.
- Working tree: `F:\OpenScience\wt\opt10-codon-usage\skills\bio-codon-usage`; branch `optimize/ten-20260928-lane2-codon-usage`; starting HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Audited candidate: `sha256-manifest-v1:13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77` (independently reproduced: 9 files, 862-byte ordinal manifest).
- Source identity: `F:\OpenScience\audits\bio-codon-usage\initial-opt10-20260928\source-identity.json`; SHA-256 `762bd99c347c41228b3148eb38d74d2565810a55b21a9c7b9ad07f35fbbf4227`.

## Completed this phase

- Read the current retained `skill-auditor.zip` rubric and independently audited the unchanged exact candidate as Category 3 Data Analysis, mode B, Moderate complexity (5 inputs).
- Executed all three shipped scripts twice: 3/3 exit 0, empty stderr, byte-identical stdout. Standard-code CAI optimization preserved `MAALDDKG*` and scored 1.000.
- Ran a fresh 35-check harness over valid, partial, shifted, ambiguous, stop, empty, ATG/TGG-only, tie, pseudocount, table-2, Nc, public `thrA`, and codonW surfaces; 35/35 audit observations/assertions completed.
- Adjudicated current Biopython 1.85 behavior: `strict=False` emitted no warning; indexed stops affected CAI; the 0.5 pseudocount normalized to 0.05 in the tested family; empty and all-excluded scores divided by zero; table-2 TGA optimization changed Trp to stop.
- Bounded the exact documented simplified Nc helper: heterogeneous 41.212 versus codonW 30.77; public `thrA` 48.854 versus 47.41. Primary-source checks support the candidate's CAI, tAI, ramp, and expression-boundary interpretation but not standard-Nc equivalence.
- Result: static 68/100, execution 50.8/100, assertions 12/25, weighted 58/100 Reject; structural veto FAIL (Stability), research veto FAIL (Methodological Ground and Code Usability); `deployable=false`.
- No audit-local repair was attempted: all four findings change scientific method, API contract, or validation policy and exceed the minor-repair budget.

## Required next actions

1. Fix `CODON-001`: make alternate-code optimization table-aware end to end or reject the nonstandard DNA route; prove table-2 TGA/TGG/AGA/AGG and stop-set behavior.
2. Fix `CODON-002`: correct Biopython 1.85 stop, pseudocount, non-strict tie, and zero-denominator claims; provide a guarded scoring wrapper and regressions.
3. Fix `CODON-003`: add one reusable table-aware CDS validator used by all runnable surfaces with explicit strict/permissive behavior and discard reporting.
4. Fix `CODON-004`: implement standard Wright/codonW-compatible Nc or remove/rename the advertised Nc capability while preserving the cross-study prohibition.
5. Prepare delta tooling on new exact bytes, then route to a fresh independent `reaudit-scientific-skill` worker. The current audit must be published locally by the orchestrator before or alongside the fixer transition.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| CODON-001 | P0 | open | `evidence/audit-results.json` table-2 probes | Safe table-aware optimization or explicit rejection plus protein regressions. |
| CODON-002 | P0 | open | same, CAI probes | Correct semantics and guarded zero-denominator scoring. |
| CODON-003 | P1 | open | same, boundary probes | Shared CDS validation with explicit reporting. |
| CODON-004 | P1 | open | `outputs/nc-*.out` | Standard Nc or honest capability/name removal. |

- Ordered ledger: `F:\OpenScience\audits\bio-codon-usage\initial-opt10-20260928\finding-ledger.md`; SHA-256 `2398b649136af2436e584e50a683136f5f6220f87eca04127fb3a056fb6b6b0b`.
- Blocked/restricted surfaces: none. Documented-only tAI and downstream construct-screening tools were classified but do not support readiness.

## Environment and evidence

- Raw run root: `F:\OpenScience\audits\bio-codon-usage\initial-opt10-20260928`.
- Report: `report.json` SHA-256 `8a0dd066c48c8740d94fcbe4eaf0bb529bbe593cf35587e6ee921c533befe456`; viewer: `viewer.md` SHA-256 `3f5e268d7231df3279151d4237582d247f9e48f9e463f45085ebfb653751dce6`.
- Structured results: `evidence/audit-results.json` SHA-256 `dfa9f5945c43aba6e51c98de4da276805fde51cb2da6af8e168f86101fc86693`; schema validation PASS SHA-256 `0eac5e5d755bb10b337cc2770d1cdc38a55adb1d5006b86230279515964f5d1e`.
- Independent runner: `audit_harness.py`; prompts: `generated-test-inputs.json`; primary-source review: `evidence/research-checks.md`; exact outputs under `outputs\`; full hashes in `artifact-hashes.tsv`.
- Prepared environment: CPython 3.12.11, Biopython 1.85, codonW 1.4.4; `TOOLS.md` SHA-256 `174ad90c2ef35f4e90525d6acbde747903efc6c7eeada7783e5e6b39d88c7551`; explicit lock SHA-256 `82d908a7a84f66a533a12a7b564cee57392b49312b2c1d503ffdafec88b24021`.

## Worktree safety

- Candidate bytes are unchanged and the exact identity was recomputed after execution and during schema validation.
- Product worktree status remains only untracked run-owned `skills/bio-codon-usage/`; no product commit, push, pull request, release, submission, dependency install, or remote mutation occurred.
- Audit-owned outputs are confined to the raw run root and this canonical handoff. Tooling fixtures were read-only; unrelated control-repository changes were not touched.
- Records publication state: the exact report was published locally as `candidate@13d831f93500-initial-opt10-20260928` with 32 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit.

## Transition assertion

- Next-phase prerequisites met: yes.
- Next action: orchestrator validates/publishes the exact initial audit record, then assigns a fresh `fix-scientific-skill` worker to resolve `CODON-001` through `CODON-004` without changing origin identity or unrelated work.

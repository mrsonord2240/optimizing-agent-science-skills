# Handoff: bio-analytical-validation / candidate-ready

- Updated: 2026-09-28T12:41:19.9234979-07:00
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill / independent lane-1 auditor
- Next role: optimize-scientific-skills orchestrator

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:liquid-biopsy/analytical-validation`; origin subtree `798bd55e904f3ab813a2a37ac5989febb4d1d2a7` remained read-only.
- Working tree: `F:\OpenScience\wt\opt10-analytical-validation\skills\bio-analytical-validation`.
- Branch/worktree: `optimize/ten-20260928-lane1-analytical` at unchanged HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Candidate tree hash: ordered six-file content SHA-256 `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab`; manifest `F:\OpenScience\audits\bio-analytical-validation\reaudit-opt10-20260928\source-identity.json` SHA-256 `a452962f232e84b4d5dfabd93f4d7453936c955de352975c344fe5d19d6bd67d`.
- Applicable audit: independent final audit `F:\OpenScience\audits\bio-analytical-validation\reaudit-opt10-20260928`; report SHA-256 `f50d78dec3d58cc087ffbf19e811c9d9beb0f9613060152f022b8ef303f7af10`.

## Completed this phase

- Reinspected all six candidate files and independently re-executed all four public Python surfaces twice under the pinned WSL environment; candidate identity and execution-summary SHA-256 were stable across runs.
- Executed the inherited public aggregate case plus at least two fresh cases for every material workflow; 25/25 scientific assertions passed, including 18 invalid-input contracts.
- Independently resolved `ADV-001` through `ADV-005`: sampling-only boundaries, stable validation, probit CI/diagnostics/separation behavior, simulation sensitivity/determinism, and corrected GE/reference-material distinctions all passed.
- Certified Production Ready: static 94, execution 97.6, Layer 1 average 39.6/40, Layer 2 average 58.0/60, assertions 100%, both veto gates PASS, final score 96.
- Produced strict schema-valid report, viewer, source identity, finding ledger, saved inputs/scripts, provenance notes, and hash-bound execution/schema evidence without changing candidate bytes.

## Required next actions

1. Preserve exact candidate identity `bd66239b9133b70a7522d0d99e3bc4ebbed1b8c1291c74fad26367dfa339b2ab` for the run-closing product commit and provider metadata reconciliation. The orchestrator published the exact final audit as `candidate@bd66239b9133-reaudit-opt10-20260928` with six explicit artifacts; raw/published report SHA-256 values match and generated audit views pass `audits:check`.
2. Carry non-blocking `ADV-006` as a P2 documentation polish item; it does not violate the candidate-ready gate.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| ADV-006 | P2 | open, non-blocking | `F:\OpenScience\audits\bio-analytical-validation\reaudit-opt10-20260928\scientific-source-notes.md`; `finding-ledger.md` | Replace exact `130–170 bp` wording with the cited 110–190 bp size-selection range and approximately 165 bp average, or add a directly supporting primary source. |

No veto, open P0, failed surface, blocked surface, deferred surface, or restricted-access item remains.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audit-envs\bio-analytical-validation\TOOLS.md`; SHA-256 `d2478cf2c054a848eb7ca08677beba0fb6946c845ead9da72f98658c6b8506a4`.
- Run evidence: `F:\OpenScience\audits\bio-analytical-validation\reaudit-opt10-20260928\evidence\execution-summary.json` SHA-256 `fb4fa08d468b33caca8c8dd49dfdf34e6c913487fff0cbf0d5ef8a37a8077618`; `evidence\schema-validation.json`; `viewer.md` SHA-256 `e6cdfc6bb2bb0f88fb09f830df8f548e438ce89aa9c8cb696a08908696de6c36`.
- Environment: WSL `science` / `sci`; CPython 3.12.14; NumPy 1.26.4; SciPy 1.12.0; statsmodels 0.14.6; explicit lock SHA-256 `fecdb107ca7c0cd211bf4fe7f9ad0f2a48eff8a11d8068c5cf4e5b2d2d2d6d73`; `WSL_INTEROP` unset.
- Restricted-access items: none.
- Tooling impact: none (the re-audit changed no candidate or dependency bytes; final audit artifacts and handoff only).

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-analytical-validation\reaudit-opt10-20260928`; this canonical handoff.
- Pre-existing/user-owned changes: exactly six fixer-owned modified candidate files under `skills\bio-analytical-validation`; preserved at the recorded identity.
- Records state: the raw final audit is published locally with supersession linkage to the initial audit; the candidate remains parked for the one run-closing product commit.
- Product commits/pushes: none.

## Transition assertion

- Next-phase prerequisites met: yes.
- If no: not applicable.

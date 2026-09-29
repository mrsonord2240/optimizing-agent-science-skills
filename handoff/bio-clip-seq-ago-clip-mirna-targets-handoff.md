# Handoff: bio-clip-seq-ago-clip-mirna-targets / fix-scientific-skill

- Updated: 2026-09-28T18:34:57-07:00
- Lane: 4
- Status: phase-failed
- Owner leaving: independent final reaudit2 / Codex
- Next role: fresh `fix-scientific-skill`

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clip-seq/ago-clip-mirna-targets`; subtree `6326a423789826240d0840be6897ddd69b21d940`.
- Candidate: `F:\OpenScience\wt\opt10-ago-clip\skills\bio-clip-seq-ago-clip-mirna-targets`; branch `optimize/ten-20260928-lane4-ago-clip`, product HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact `sha256-manifest-v1`: `a89a7ecad19a3cc207ab6b82bc0910b126b663e32e7c74c3c2b74dc105d780fa` (10 files, 989-byte manifest); independently reproduced before and after audit. Manifest: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\reaudit2-opt10-20260928\candidate-manifest.tsv`.
- Audit root: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\reaudit2-opt10-20260928`; verdict Reject, score 92/100; research veto FAIL; nondeployable. Report SHA-256 `a9baa40e4397a103c519bc1a846c37fb7c7a7d45045b7febb507c8fb7bf51551`.

## Completed this phase

- Fresh independent full audit and schema/arithmetic validation passed; see `report.json`, `viewer.md`, `evidence/schema-validation.json`.
- AGO-004 closed: two fresh full two-replicate Hyb workflows agreed across 25/25 non-stdout artifacts; stdout differs only at its first wall-clock timestamp line. Details: `evidence/hyb-repeatability.json`.
- AGO-005 closed locally: explicit targeted UMI lengths 9 and 10 pass; absent/invalid declarations fail closed. Upstream 9-nt prose versus 10-nt default remains disclosed: `evidence/umi-contract.json`.
- Fresh TargetScan projection/overlap and auxiliary UMI/trim/soft-clip diagnostic checks recorded in `evidence/targetscan-contract.json` and `evidence/secondary-routes.json`.
- New finding AGO-009 P0 reproduced: `expression_value=NaN` exits successfully and is accepted at threshold 100; the research methodology veto fails. Evidence: `evidence/expression-nan-check.json`, reproduction `scripts/expression_finite_check.py`.

## Required next actions

1. Fresh fixer: address AGO-009 in the candidate, require finite expression values before thresholding, and add NaN, positive-infinity, and negative-infinity regressions with fail-closed/no-publication assertions.
2. Preserve scientific/source notes and the explicit upstream UMI ambiguity disclosure. After repair, reproduce the candidate identity and request a new independent final re-audit; this exact identity is not candidate-ready.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AGO-009 | P0 | open | `evidence/expression-nan-check.json`; `finding-ledger.md` | Reject non-finite expression values before they can bypass thresholding; regress NaN and ±Inf. |
| AGO-004 | P0 | closed on this identity | `evidence/hyb-repeatability.json` | No further action; preserve timestamped-stdout limitation. |
| AGO-005 | P1 | closed locally; upstream ambiguity disclosed | `evidence/umi-contract.json` | Keep protocol-declared length/provenance fail-closed contract. |

## Environment and evidence

- Tool inventory: `F:\OpenScience\audit-envs\bio-clip-seq-ago-clip-mirna-targets\TOOLS.md`; SHA-256 `a1cb55f6384dcd9f10dd37e971f539cf65fe461a20490ecc4cc39f0642858d86`; environment fingerprint `fcd7556256ce1a32f3473718ad2f0fa3d1821039dc4994ecf4aa626fe97d7e5c`.
- Report/viewer: `report.json` SHA-256 `a9baa40e4397a103c519bc1a846c37fb7c7a7d45045b7febb507c8fb7bf51551`; `viewer.md` SHA-256 `12d78f7d64a82d50cb09282d012a34eaa5357e515c3ea02ff7147e0040e8ffa9`.
- Finding/source/identity: `finding-ledger.md` SHA-256 `ae715c3265fafb3a6ff7429503160338c536f8b33d676ab03a9e577933784137`; `scientific-source-notes.md` SHA-256 `10ec8909f75a07d5ae330e8fd4cdd949ae92d5ce7c07b07a5b7d66a111607009`; `source-identity.json` SHA-256 `9a7210c73e0ded745103b34de159f8d2a9e38125ca8c7f786b2b3791a60013d0`.
- Full artifact inventory: `evidence/audit-artifacts.sha256` SHA-256 `2b5f2ba2580c86381262da604959d2ecba0d63776b011bb83d26ca65b5830c8c`; strict report validation: `evidence/schema-validation.json`.
- Deferred surfaces: full Yeo needs a real library and species-matched STAR repeat/genome indices; HEAP needs Halo-Ago2 wet-lab material; DIANA example endpoint previously returned HTTP 500; AGO peak calling is not bundled. No private inputs, credentials, paid services, or Marketplace were used. Tooling impact: none.

## Worktree safety

- Candidate/product bytes were read-only; the expected identity matches before and after. Product worktree contains the candidate directory as untracked; no product commit, stage, or push occurred.
- Audit artifacts are confined to the audit root above. No records were published.
- Pre-existing control-repository user changes/deletions and untracked worker files were preserved untouched; only this canonical handoff was replaced.

## Transition assertion

- Next-phase prerequisites met: yes; exact candidate identity, full report, reproducible P0 evidence, and bounded fixer action are recorded.
- Transition: route to a fresh `fix-scientific-skill` for AGO-009. Do not route to candidate-ready unless a later independent re-audit passes all gates.

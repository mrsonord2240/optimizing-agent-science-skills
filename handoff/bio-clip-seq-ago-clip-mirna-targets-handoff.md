# Handoff: bio-clip-seq-ago-clip-mirna-targets / reaudit-scientific-skill

- Updated: 2026-09-28T19:42:16-07:00
- Lane: 4
- Status: candidate-ready
- Owner leaving: fresh independent reaudit3 / Codex
- Next role: orchestrator

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clip-seq/ago-clip-mirna-targets`; subtree `6326a423789826240d0840be6897ddd69b21d940`.
- Candidate tree: `F:\OpenScience\wt\opt10-ago-clip\skills\bio-clip-seq-ago-clip-mirna-targets` on `optimize/ten-20260928-lane4-ago-clip`, product HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Identity: `sha256-manifest-v1 e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30`; 10 files, 989-byte manifest, reproduced before and after.
- Fresh audit root: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\reaudit3-opt10-20260928`.
- Report SHA-256: `4193ffa07317ebcd064796b2b86f5bc59a756959de07a3cba1969c1c8795a708`; strict report schema validation: PASS.

## Completed this phase

- Independent full-tree review and accessible-surface retest completed. Final score 95/100 (static 93, execution average 96.6, assertions 35/35); skill and research vetoes PASS; no open P0 or required recommendations.
- Fresh pinned Hyb cross-workflow repeatability passed: 111 accepted, 0 excluded, 111 targets, 2/2 support; all structured and non-stdout files match. Stdout differs only on its first timestamp line.
- AGO-009 retest passed finite acceptance, below-threshold exclusion, 13 Python non-finite spellings for values and thresholds, malformed/missing values, and no result files on invalid inputs. AGO-005 explicit 9/10-nt UMI contract passed.
- Fresh TargetScan projection/strand, wrapper boundaries, Yeo total-route synthetic checks, and schema validator passed. Publisher source-identity compatibility was checked read-only; no records were published.
- Evidence, viewer, findings, source identity, candidate manifest, and artifact hashes are under the audit root; report/viewer hashes are in `artifact-hashes.sha256`.

## Required next actions

1. Orchestrator may accept this exact identity as `candidate-ready`; any later candidate-byte change requires a fresh independent re-audit.
2. Keep promotion, records publication, Marketplace intake, product commits, and remote actions outside this audit handoff.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| AGO-004 | P0 | closed; independently rechecked | `reaudit3-opt10-20260928/evidence/hyb-repeatability.json` | Retain the stdout first-line timestamp limitation in interpretation. |
| AGO-005 | P1 | closed locally; upstream ambiguity disclosed | `reaudit3-opt10-20260928/evidence/umi-contract-independent.json` | Protocol owners supply declared targeted UMI length; upstream prose/default remain 9/10 nt. |
| AGO-009 | P0 | closed; independently rechecked | `reaudit3-opt10-20260928/evidence/consensus-parser-independent.json`, `float-spellings-independent.json` | None for audited bytes. |
| Biological and remote surfaces | — | deferred | `reaudit3-opt10-20260928/evidence/deferred-limitations.md`, `TOOLS.md` | Full Yeo/HEAP need biological inputs; DIANA example returned HTTP 500. |

## Environment and evidence

- Tool inventory: `F:\OpenScience\audit-envs\bio-clip-seq-ago-clip-mirna-targets\TOOLS.md` (SHA-256 `f94c31cfa09e69331c164602a850022d034551e7af840f5965ae181f8e0e9a3a`); environment fingerprint `fcd7556256ce1a32f3473718ad2f0fa3d1821039dc4994ecf4aa626fe97d7e5c`; lock SHA-256 `ba5f355bb2d907197f723c7424742517b0e4fb4839a4273382d2293c5b2f3340`.
- Core artifacts: `report.json`, `viewer.md`, `findings.md`, `source-identity.json`, `candidate-manifest.tsv`, `evidence/schema-validation.json`, and `artifact-hashes.sha256` in the audit root.
- Tooling impact: none; prepared environment and candidate dependencies were unchanged.

## Worktree safety

- Candidate files were not modified; before/after/final manifests are identical. Product worktree remains the untracked Skill directory only; nothing staged or committed.
- Existing control-repository edits, deletions, and untracked worker files were preserved. This task replaced only this canonical handoff and wrote its isolated fresh audit root.
- No audit records were published; no product/provider change, Marketplace action, commit, push, release, or submission occurred.

## Transition assertion

- Next-phase prerequisites met: yes. Exact identity, strict schema, readiness metrics, all three prior findings, and deferred surfaces are durably evidenced.
- Verdict: `candidate-ready` for `e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30` only.

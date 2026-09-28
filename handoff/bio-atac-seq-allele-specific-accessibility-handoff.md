# Handoff: bio-atac-seq-allele-specific-accessibility / candidate-ready

- Updated: 2026-09-28T13:50:00-07:00
- Lane: 2
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill (second independent re-audit)
- Next role: optimize-scientific-skills

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/allele-specific-accessibility`; source subtree `1d84e31c0fdc0b2636e5a553d71796b996be6a23`.
- Working tree: `F:\OpenScience\wt\opt10-atac-asa\skills\bio-atac-seq-allele-specific-accessibility`.
- Branch/worktree: `optimize/ten-20260928-lane2-atac-asa`; starting HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Candidate tree hash: content SHA-256 `275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2` (11 files; 1,099-byte ordinal manifest).
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-allele-specific-accessibility\reaudit2-opt10-20260928`; report SHA-256 `587eb0ca31024f4f9d7e4789d2e1b9f223e45cb7f7374369bd65abbad0ae9a42`; audited identity matches exactly.

## Completed this phase

- Independently re-read the complete candidate, rubric, prior findings, fixes, and tooling; candidate bytes were not changed.
- Reproduced ASA-009: disjoint same-label loci now emit two one-SNP underpowered rows; coordinate-plus-phase grouping, display-only labels, and duplicate-coordinate refusal pass.
- Re-ran all 15 inherited tests, target-genotype/identity/staging/reuse boundaries, and the bounded public WASP -> GATK path; every accessible surface passed.
- Re-ran public two-feature RASQUAL: 166 finite rows, correct matrix ownership, and independently matching complete-family BH values.
- Certified static 96, execution 95.4, Layer 1 38.4/40, Layer 2 57.0/60, assertions 25/25, final 96 Production Ready; both vetoes PASS and ASA-001..ASA-009 closed.

## Required next actions

1. Preserve exact candidate identity while assembling the ten-skill shelf batch. The orchestrator published the exact final audit as `candidate@275ff0a1b8d9-reaudit2-opt10-20260928` with 18 explicit artifacts; raw/published report SHA-256 values match and generated audit views pass `audits:check`.
2. Include these bytes in the single run-closing product commit, then bind the accepted audit to that full provider commit.
3. Run the Marketplace local intake gate only after the full ten-skill batch is committed.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none | — | closed | `finding-ledger.md`; `report.json` | No skill fix or tooling delta remains. |

- Failed or blocked runnable surfaces: none. Restricted-access items: none.
- External-only non-runnable routes: MatrixEQTL and QuASAR, accurately bounded and not readiness blockers.
- Environment caveat: a pre-existing VS Code session still holds `/mnt/f`; this lane used only `/mnt/openscience` and did not alter that session.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audit-envs\bio-atac-seq-allele-specific-accessibility\TOOLS.md`; SHA-256 `73a94e76eb45e9f7d11a13e254ff0decd81e4a51ce22f71d444e8db1409676b0`.
- Environment fingerprint: `b71c6a315b43e28a9188b32e0b3314f1b3de01ae6868c47588b9db6acc78f5b5`; tooling evidence fingerprint `e3417734e8069dd52657e4a06c1f7a93df9e86b61ad0be3141167aa36137804c`.
- Run evidence: `evidence/fixtures.txt`, `evidence/real-pipeline.txt`, `evidence/real-rasqual.txt`, `evidence/static.txt`, and `evidence/schema-validation.json` under the applicable audit root.
- Record identities: `source-identity.json`; artifact manifest SHA-256 `a340a934b94ea90310b7d36665545465f7a27245930b43d0c3f52f63baabf727`; viewer SHA-256 `9143a5466ef1b8ca636a3046095f09bf581aceb5449cb9caed844016a9240ca7`.
- Restricted-access items: none.
- Tooling impact: none (re-audit changed only raw audit artifacts and this handoff; candidate identity stayed exact).

## Worktree safety

- Run-owned changes: the new raw audit root above and this canonical handoff.
- Pre-existing/user-owned changes: the isolated candidate subtree remains untracked as received; unrelated worktrees and control-repository changes were untouched.
- Records state: raw immutable re-audit is complete and schema-valid; shared publication was intentionally not performed by this worker.
- Product commits/pushes: none.

## Transition assertion

- Next-phase prerequisites met: yes.
- Candidate-ready assertion: exact identity passed all readiness floors, both veto gates, all 25 assertions, every accessible runnable surface, and all inherited finding closures.

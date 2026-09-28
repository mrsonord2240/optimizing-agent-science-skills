# Handoff: bio-clip-seq-ago-clip-mirna-targets / fix

- Updated: 2026-09-28T14:55:00-07:00
- Lane: 4
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill
- Next role: fix-scientific-skill

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:clip-seq/ago-clip-mirna-targets`; origin subtree `6326a423789826240d0840be6897ddd69b21d940`.
- Candidate: `F:\OpenScience\wt\opt10-ago-clip\skills\bio-clip-seq-ago-clip-mirna-targets` on `optimize/ten-20260928-lane4-ago-clip`; base commit `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact audited content SHA-256: `9eb490f452b4c0e4a27a95986816e7d84d689e6077a537e057368b9e471cf7e7` (six files; 591-byte manifest).
- Strict source identity: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\initial-opt10-20260928\source-identity.json` (SHA-256 `54c6c034ca29ca0ee8b508af032639ff5497b2aa100cb9e98868d10fcfeb45f1`).

## Completed this phase

- Independent initial audit completed against the exact unchanged candidate. Final diagnostic score: **37/100, Reject**; static 46/100, execution average 31.4/100, assertions 10/25.
- Skill veto **FAIL**: Stability, Determinism, and Security. Research veto **FAIL**: Methodological Ground and Code Usability. Contract, Scientific Integrity, and Practice Boundaries pass.
- Rebuilt the pinned Hyb runtime from Git blobs, ran official data twice, and obtained 111 valid 16-field rows per run. The same read ids received 18 different RNA-pair assignments in each run.
- Ran the exact wrapper against real Hyb: invalid generated-FASTA database contract, wrapper exit 0, and three empty derived tables.
- Reproduced the wrapper matrix: Hyb exit 42 swallowed, spaces fail with exit 0, literal glob includes a sibling FASTA, actual output naming is missed, and current 16-column rows are discarded by field-3/5 assumptions.
- Re-executed UMI-tools, cutadapt, soft-clip diagnostic, unstranded/stranded bedtools controls, and TargetScanHuman 8 schema parsing.
- Classified public Yeo chim-eCLIP, HEAP/CLIPanalyze, Hyb, TargetScan, miRDB, DIANA, pyHyb, and hybkit interfaces without substitution or access bypass.
- No audit-local repair was eligible: every correction changes a scientific interface, parser, safety boundary, determinism policy, or interpretation rule. Audit publication was intentionally left to the orchestrator.

## Required next actions

1. Implement the current Hyb named-database, goal/id, and generated-output contract; require non-empty validated output before parsing (`AGO-001`).
2. Replace awk field assumptions with an orientation-aware 16-column parser using fields 4/10; preserve site, coordinates, scores, and expression provenance (`AGO-002`).
3. Fail closed: strict shell mode, validated/quoted arguments, guarded staging, subprocess propagation, schema/count postconditions, and atomic final outputs (`AGO-003`).
4. Investigate the 18/111 pair-assignment variance and define a deterministic seed/single-thread, ambiguity exclusion, or consensus rule with repeat-run tests (`AGO-004`).
5. Route preprocessing by declared library layout and ship a versioned strand-safe TargetScan transcript-to-genome integration (`AGO-005`).
6. Correct current tool identities/access states and narrow affinity/negative-evidence conclusions with claim-level sources (`AGO-006`, `AGO-007`).
7. Add structured site/target outputs and focused schema/path/failure/repeatability regressions (`AGO-008`), then run delta tooling and a fresh independent re-audit.

## Open findings and blockers

| ID | Severity | State | Required disposition |
|---|---|---|---|
| AGO-001 | P0 | open | Current Hyb database/output contract and fail-closed postconditions. |
| AGO-002 | P0 | open | Orientation-aware 16-column schema parser and valid aggregation. |
| AGO-003 | P0 | open | Quoted/validated shell boundary, propagated failures, atomic outputs. |
| AGO-004 | P0 | open | Deterministic or explicitly ambiguity-aware pair-assignment policy. |
| AGO-005 | P1 | open | Library-specific preprocessing and strand/coordinate-safe TargetScan route. |
| AGO-006 | P1 | open | Current Hyb/Yeo/HEAP/pyHyb/hybkit identities and classifications. |
| AGO-007 | P1 | open | Remove affinity proxy and biological-false-positive overclaims; source heuristics. |
| AGO-008 | P2 | open | Structured reports, provenance, safe reruns, field-aware filters, regressions. |
- Full human Yeo chim-eCLIP is resource-infeasible in the bounded environment; HEAP wet-lab and reporter validation require biological material; DIANA's documented example returned HTTP 500. These do not block repair or bounded re-audit.

## Environment and evidence

- Raw report: `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\initial-opt10-20260928\report.json` (SHA-256 `ebe0e70aeb3d781470e8a2ae69fdc4a242235e0afdc2a1f4b7b5bc44a3ac23e2`).
- Viewer: `...\viewer.md` (SHA-256 `684ab43c02e1f4a8eddb33cd5074f2c38df2d1ca8931e9bfaa8565dfbb35b79f`). Finding ledger: `...\finding-ledger.md`.
- Schema validation: `...\evidence\schema-validation.json` — valid, exact candidate identity confirmed, score arithmetic and 25 assertions confirmed.
- Primary evidence: `wrapper-contract-results.json`, `real-wrapper-summary.txt`, both `official_test_comp_hOH7_hybrids_ua*.hyb` runs, `hyb-repeatability.txt`, `adjacent-surface-results.json`, and `access-classifications.md` under the raw run's `evidence/`.
- Tooling record: `F:\OpenScience\audit-envs\bio-clip-seq-ago-clip-mirna-targets\TOOLS.md` (SHA-256 `3cfec99140011ae7f8130fb2501cffbf37c1f74d1d1ed0e8098bb19f623fdc0f`).
- Environment fingerprint SHA-256: `dc64dc57f17e3f0de31a8d348a0c7045f7bc3b4e92c5191051a8249e8ac0bae3`; explicit lock SHA-256 `ba5f355bb2d907197f723c7424742517b0e4fb4839a4273382d2293c5b2f3340`.
- Rubric archive SHA-256: `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`.

## Worktree safety

- Product status remains only `?? skills/bio-clip-seq-ago-clip-mirna-targets/`; candidate bytes revalidated to the exact audited identity after execution.
- Audit artifacts are confined to `F:\OpenScience\audits\bio-clip-seq-ago-clip-mirna-targets\initial-opt10-20260928`; tooling caches remain under the dedicated audit environment.
- The exact audit was published locally as `candidate@9eb490f452b4-initial-opt10-20260928` with 17 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No product commit, candidate repair, push, pull request, release, submission, or Marketplace action occurred.

## Transition assertion

- Next-phase prerequisites met: yes — exact rejected candidate, eight ordered findings, reproducible evidence, strict schema-valid report, and deterministic next actions are present.
- Next owner must begin at `AGO-001` through `AGO-004`, preserve exact origin/provenance, and not claim readiness until delta tooling plus a fresh independent re-audit pass both veto gates.

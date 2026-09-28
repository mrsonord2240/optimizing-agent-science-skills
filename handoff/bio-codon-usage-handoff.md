# Handoff: bio-codon-usage / independent final re-audit

- Updated: 2026-09-28
- Lane: 2
- Status: final-reaudit-clean-awaiting-local-record-publication
- Owner leaving: /root/lane2_codon_reaudit
- Next role: relay orchestrator / local audit publisher

## Source identity

- Origin: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:sequence-manipulation/codon-usage`; source subtree `3874a00444ef0856451fece587c051cfc34aaf80`.
- Worktree: `F:\OpenScience\wt\opt10-codon-usage\skills\bio-codon-usage`; branch `optimize/ten-20260928-lane2-codon-usage`; product HEAD `0bc0b31fc52742dbec1034f698103434cc9460c3`.
- Exact audited candidate: `sha256-manifest-v1:3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd` (11 files; 1,051-byte ordinal manifest with no final newline).
- Applicable initial audit: `F:\OpenScience\audits\bio-codon-usage\initial-opt10-20260928\report.json`; initial findings `CODON-001` through `CODON-004`.

## Completed this phase

- Read and followed the full audit-scientific-skill contract and the retained current rubric; no candidate repair or publication was performed.
- Independently read the complete 11-file candidate, re-created its manifest identity, classified it as Moderate / Data Analysis / Mode B, and ran five bounded inputs.
- Executed all three shipped entrypoints twice: every run exited zero with empty stderr and byte-identical output; standard optimization reached CAI 1.000 and preserved `MAALDDKG*`.
- Executed the 12-test focused suite twice; all tests passed and the normalized case/outcome streams matched.
- Verified all four table-2 TGA/TGG x AGA/AGG cases preserve `MW*`, and verified table/index mismatch rejection.
- Verified strict rejection, permissive exact-discard offsets/reasons, and shared validation state across counts, frequencies, and RSCU.
- Reproduced live Biopython 1.85 indexed-stop, pseudocount, tie, and zero-denominator semantics, plus standard-code protein preservation.
- Validated public table-11 `thrA` as 2,463 nt / 821 codons / ATG...TGA / no discards and executed counts, frequencies, RSCU, and GC123.
- Fresh codonW 1.4.4 runs reproduced Nc 30.77 and 47.41; confirmed the candidate neither implements nor advertises the removed approximation as standard Nc.
- Independent harness result: 57/57 checks passed. Strict report validation passed and all 16 listed artifact hashes revalidated.

## Required next actions

1. Publish the raw final record through the modular records publisher with explicit artifacts from `F:\OpenScience\audits\bio-codon-usage\reaudit-opt10-20260928`.
2. Regenerate and check the local audit index/status outputs, then bind the published record to the exact candidate identity above.
3. If publication remains clean, mark this skill candidate-ready and preserve these exact bytes for the single ten-skill shelf commit and Marketplace local intake.

## Open findings and blockers

- Final verdict: **Production Ready**, 97/100; static 96, execution average 97.4, assertions 25/25.
- Skill veto: PASS. Research veto: PASS. All Production Ready floors pass.
- `CODON-001`: closed — table-aware optimization preserves all four table-2 sense/stop cases.
- `CODON-002`: closed — exact Biopython 1.85 semantics and guarded zero denominator pass.
- `CODON-003`: closed — shared strict/permissive validation and exact discard reporting pass.
- `CODON-004`: closed — false standard-Nc implementation/trigger claim is absent; external/cross-study boundary is explicit.
- New P0/P1/P2 findings: none.
- Runnable blockers, restricted surfaces, and resource-infeasible surfaces: none.
- Documented-only by design: tAI and downstream construct screens (translation ramp, RNA structure, GC extremes, cryptic elements, and codon pairs).

## Environment and evidence

- Raw run root: `F:\OpenScience\audits\bio-codon-usage\reaudit-opt10-20260928`.
- Tooling root: `F:\OpenScience\audit-envs\bio-codon-usage`; CPython 3.12.11; Biopython 1.85; codonW 1.4.4.
- `TOOLS.md` SHA-256: `85d20ee3a35162342e1be753e5e5c792a9530f617a9cb88c4354b9eb74e403a8`.
- Environment lock SHA-256: `82d908a7a84f66a533a12a7b564cee57392b49312b2c1d503ffdafec88b24021`.
- Report SHA-256: `bb715d696f607dab3ba0717c1619c5ddc62862dc95af05cef317a0f4f56d7126`.
- Viewer SHA-256: `be23136dc0e1b3fde7dd9976ccc4e0177b9289d18877dd5c791c02afcc1dec11`.
- Source identity SHA-256: `d9e86b40dd6d3d75f4a3fb9a8248280f3b0d1191ab40409ed6eeac0b4100d194`.
- Re-audit result SHA-256: `b40e2b7f8109950e664e9948a68c5dfee6b6b5ee006a33ced5fade0a6274a7aa`.
- Harness SHA-256: `014e9578be2c3c487c8c69e7d174067168f65a878107c12dbefef841ebe1f309`.
- Candidate manifest SHA-256: `3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd`.
- Schema validation: `evidence/schema-validation.json` reports PASS; `artifact-hashes.tsv` binds all raw artifacts.

## Worktree safety

- Product status remains only the run-owned untracked `skills/bio-codon-usage/`; no candidate source byte was changed by this phase.
- A transient run-generated `scripts/__pycache__` was detected, removed exactly, and prevented on the final harness rerun; the final exact identity was reproduced after cleanup and no candidate bytecode remains.
- The exact final audit was published locally as `candidate@3186a1debc80-reaudit-opt10-20260928` with 14 explicit scripts/inputs; generated views were refreshed. The matching record/view/handoff changes await the run-owned control commit. No product commit, push, pull request, release, submission, or Marketplace action occurred.
- Source checkout and unrelated repository changes were not touched.

## Transition assertion

- Exact candidate stable after final execution: yes; identity reproduced as `3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd`.
- Affected surfaces known and covered: yes; every shipped script/helper/test, table-2 route, validation boundary, live 1.85 behavior, public `thrA`, and codonW boundary were independently exercised.
- Evidence reproducible and schema-valid: yes; 57/57 checks, 25/25 assertions, both vetoes PASS, raw hashes validated.
- Publication status: published locally as `candidate@3186a1debc80-reaudit-opt10-20260928`; control commit pending.
- Next action: commit the run-owned record/view/handoff changes, then park the exact candidate as candidate-ready.

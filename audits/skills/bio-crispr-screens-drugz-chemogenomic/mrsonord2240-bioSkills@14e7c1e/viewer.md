> **Audit record for `bio-crispr-screens-drugz-chemogenomic`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@14e7c1e](https://github.com/mrsonord2240/bioSkills/tree/14e7c1ec9fb76fd5859c5b4ba5ec70128fb85aeb/crispr-screens/drugz-chemogenomic) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-drugz-chemogenomic

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@14e7c1ec9fb76fd5859c5b4ba5ec70128fb85aeb:crispr-screens/drugz-chemogenomic`
Final-pass metadata: `auditor_independent: false` — `final pass: fixed and audited under one brief, see CHECKPOINT.md`

The prior 2026-09-16 report and viewer were preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-drugz-chemogenomic\`. Fresh scripts, exact-source copy, command output, downloaded CEGv2, and result tables are in `run\phase2\`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---:|---:|---:|---|---|---|
| 1 | Canonical vehicle vs drug | 39 | 58 | 97 | 4/4 | yes | ✅ |
| 2 | CEGv2 exclusion regression | 39 | 58 | 97 | 4/4 | yes | ✅ |
| 3 | Three-dose helper | 39 | 57 | 96 | 4/4 | yes | ✅ |
| 4 | Day-0 edge case | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 5 | Small-library stress | 38 | 57 | 95 | 4/4 | yes | ✅ |
| 6 | Determinism adversarial | 39 | 57 | 96 | 4/4 | yes | ✅ |
| 7 | Synergy scope boundary | 37 | 57 | 94 | 4/4 | yes | ✅ |
| 8 | Exact shipped example | 39 | 58 | 97 | 4/4 | yes | ✅ |
| 9 | Argument-validation adversarial | 34 | 49 | 83 | 3/4 | yes | ✅ |

**Execution average:** 94.6 / 100
**Assertion pass rate:** 35 / 36
**Static score:** 96 / 100
**Final:** 95 / 100 — ⭐ Production Ready — deployable: true
**Vetoes:** Skill PASS; Research PASS.

## Fresh execution evidence

The runner `run/phase2/run_phase2.py` copied the exact source from the assigned worktree, used `F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe`, and checked generated values/files rather than trusting exit codes. `verify_static.py` separately confirmed source completeness, nine Related Skill targets, and Python parsing.

### Inputs 1–2 — core analysis and reference-gene exclusion

Input 1 ran drugZ on the 71,090-guide synthetic vehicle/drug matrix. It produced 18,054 gene rows, all ten documented columns, zero missing `normZ` values, all 6/6 planted sensitizers and all 6/6 planted suppressors in the expected top ranks.

Input 2 fetched the documented public CEGv2 file live, parsed its header-skipped first column into 684 names, and passed that comma list to `-r`. The resulting output removed 646 genes. This reconfirms that the earlier silent no-op is not present.

### Inputs 3–5 — dose, anchor, and library-size behavior

Input 3 built low/mid/high counts fresh and ran the exact `scripts/dose_consistent_hits.py`; it recovered 6/6 planted sensitizers with no false positives. Input 4 deliberately used the prohibited Day-0 reference: it called 509 sensitizers at FDR <0.05, compared with 6 using the correct vehicle anchor. Input 5 reproduced `IndexError: single positional indexer is out-of-bounds` with 200 guides and default half window 500; `--half_window_size 50` completed with 51 rows and zero missing `normZ` values.

### Inputs 6–8 — repeatability, boundary, and shipped example

Input 6 produced byte-identical full outputs from two identical runs. Both SHA-256 digests were `137d28236fc840f4ce17e259dd1fff48d85c85e6e78b750bbfd1fa9ccd5f990e`.

Input 7 executed the loaded Skill's combination-screen routing rule. It limits drugZ to per-drug calling for synergy/antagonism and routes interaction testing to MAGeCK MLE, without inventing a synergy statistic.

Input 8 ran the exact source `examples/run_drugz.py` unchanged from the copied tip, including its own CEGv2 fetch. It completed, excluded 646 genes, and wrote parseable standard/CEG outputs plus both top-50 TSVs.

### Input 9 — new validation boundary

The dose helper correctly rejected an unknown `--top-dose`. It did not reject `--fdr 1.5`: the command returned 0 and wrote 12,043 rows. This is the sole failed assertion and supports a P2 recommendation, not a veto or deployability block.

## Veto review

- T1 Stability: PASS — all required executable inputs completed; expected small-library error has a documented successful recovery.
- T2 Contract: PASS — documented output columns and all referenced files/Related Skills were present.
- T3 Determinism: PASS — exact byte identity confirmed.
- T4 Security: PASS — no credentials, PHI, destructive behavior, or raw-code execution.
- M1 Scientific integrity: PASS — declared synthetic truth only; no invented citations or claims.
- M2 Practice boundaries: PASS — preclinical screen-analysis scope only.
- M3 Methodology: PASS — vehicle anchoring and MLE interaction boundary verified dynamically.
- M4 Code usability: PASS — exact example and helper ran; shipped Python parsed.

## Recommendation

**P2 — Validate the dose-helper FDR range.** Reject `--fdr` values outside `[0, 1]` before loading result files, and add tests for `1.5` and `-0.01`. No P0 or P1 remains.

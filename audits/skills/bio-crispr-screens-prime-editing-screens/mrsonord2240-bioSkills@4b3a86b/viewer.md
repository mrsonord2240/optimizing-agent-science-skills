> **Audit record for `bio-crispr-screens-prime-editing-screens`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4b3a86b](https://github.com/mrsonord2240/bioSkills/tree/4b3a86bc204d6eedbd0c24d7b2619f57ced0bbbd/crispr-screens/prime-editing-screens) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-18 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-prime-editing-screens (RE-AUDIT, 2026-09-18)

Source: `mrsonord2240/bioSkills@4b3a86b:crispr-screens/prime-editing-screens` (fork worktree
`F:\OpenScience\wt\cs-pes`, branch `fix/cs-pes`)

Different agent from the 2026-09-16 auditor, the 2026-09-18 fixer, and the fixer's own
verification. Scope: the 2026-09-18 fix pass only (`F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-prime-editing-screens.md`,
dated section at the bottom), which targeted two P1s open in the archived pre-fix report
(`F:\OpenScience\audits\_pre-fix-20260918\bio-crispr-screens-prime-editing-screens\`, score
81.2, Limited Release):

1. SKILL.md's PRIDICT2 batch CLI recipe omitted the CLI's undocumented `./input` default
   directory and the requirement that `--output-dir` already exist before `--summarize`.
2. Failure Modes / Common Errors did not cover either gap.

`git diff 558aea5 4b3a86b -- crispr-screens/prime-editing-screens/` confirms the fix touched
**only** SKILL.md's two batch code blocks, the Common Errors table, one decision-tree
row-folding, and usage-guide.md's redundancy dedup. Nothing else changed, so the
pegRNA-architecture diagram, `design_pegrna_pridict2.py`, the CRISPResso2 section, and the
Cross-Validate PE/BE snippet — all verified PASS in the 81.2 report — are carried forward
unchanged and were **not** re-executed this pass.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 3/3 PASS | ✅ |
| 3 | Edge | 28 | 38 | 66 | 2/3 PASS | ⚠️ |
| 4 | Variant B | 36 | 52 | 88 | 3/3 PASS | ✅ |
| 5 | Stress | 27 | 37 | 64 | 2/3 PASS | ⚠️ |
| 6 | Scope Boundary | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 7 | Adversarial | 35 | 50 | 85 | 3/4 PASS | ✅ |

**Execution Average: 82.7 / 100**
**Assertion Pass Rate: 21/24**

**Static Score: 94/100** (up from 90/100 in the 81.2 report)
**Final Score: 87.2 / 100 — ⭐ Production Ready — deployable, no veto**

## Detailed Outputs

### Input 1 — Canonical
**Prompt (implicit user task):** "Set up a PRIDICT2 batch pegRNA design run for these two variants exactly as the Skill documents, from scratch."
**What ran:** `run/input1_canonical_test_A.sh` — a `mktemp`'d clean directory (no pre-existing
`input/` or `predictions/`), following SKILL.md's fixed recipe verbatim
(`mkdir -p input predictions`, CSV in `input/`, `--output-dir predictions/ --summarize K562`),
against the real installed PRIDICT2 (`tools/pridict2-venv/`), on a **deletion + insertion**
variant pair pulled from PRIDICT2's own `batch_template.csv` — not the fixer's own
`replacement1`-style test fixture.
**Output:** Completed with `Batch processing completed!`, no `FileNotFoundError`. Summary CSV
has 6 real rows (top 3 per variant): `deletion1` K562 16.9–18.6 / HEK 38.9–41.5;
`insertion1` K562 38.0–39.2 / HEK 69.5–74.5. Full per-sequence prediction CSVs (818 KB, 1.1 MB)
also written.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] Following the fixed recipe verbatim from a clean directory completes without FileNotFoundError — no traceback; completion message printed.
- [PASS] The variant set is not the fixer's own test fixture — deletion1/insertion1 vs. the fixer's replacement1.
- [PASS] Output summary CSV is non-empty and contains real, non-NaN efficiency scores.
- [PASS] Per-sequence full prediction CSVs are also written to the output directory.

### Input 2 — Variant A
**Prompt:** "Run the same batch recipe on a single variant, scoring for HEK instead of K562."
**What ran:** `run/input2_variantA_test_C_single_row.sh` — clean dir, one `multireplacement1`
variant, `--summarize HEK`, `--cores 1`.
**Output:** Completed cleanly. Summary CSV has 3 real rows, HEK scores 71.8–74.6, all non-NaN.
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] A single-row batch CSV does not hit a multiprocessing edge case.
- [PASS] `--summarize HEK` works identically to K562.
- [PASS] Output is not a reused fixture from Input 1 or the fixer.

### Input 3 — Edge
**Prompt:** "What happens if the batch CSV has the right header but no rows?"
**What ran:** `run/input3_edge_test_B_empty_csv.sh` — directories correctly pre-created; CSV is
`sequence_name,editseq` with **zero data rows**.
**Output:** `... Designing pegRNAs for 0 sequences ...` then `Batch processing completed!`
(exit 0). Summary file contains only the literal text `""` — byte-identical to the symptom
SKILL.md's existing Common Errors row attributes solely to a *wrong* CSV header, which is not
the cause here.
**Scores:** Basic: 28/40 | Specialized: 38/60 | Total: 66/100
**Assertions:**
- [PASS] A zero-row (correctly-headed) CSV does not crash the CLI.
- [FAIL] The resulting empty-looking summary file is covered by an accurate Common Errors row — it names only "wrong header" as the cause; this is a distinct, undocumented cause of the identical symptom.
- [PASS] No fabricated or non-deterministic output for an empty input.

### Input 4 — Variant B
**Prompt:** "Confirm the already-documented wrong-column-name failure mode still behaves as SKILL.md says, now that the directory setup changed."
**What ran:** `run/input4_variantB_test_F_wrong_column.sh` — directories correctly pre-created
per the new fix, but CSV header is `sequence` instead of `editseq` (the pre-existing,
2026-09-16-fixed-and-documented defect class).
**Output:** `Please check your input-file! (Missing "editseq" column.)` printed, exit 0,
summary file `""` — exactly as SKILL.md's pre-existing Common Errors row describes.
**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:**
- [PASS] The pre-existing wrong-header failure mode still reproduces exactly as documented.
- [PASS] This pass's directory changes did not alter or mask that unrelated failure mode.
- [PASS] No new crash from combining a wrong-header CSV with the now-required directories.

### Input 5 — Stress
**Prompt:** "Approximate running `--summarize` before any real prediction exists" (the CLI has
no standalone summarize-only mode, so this constructs a batch input engineered to complete
the batch step with **zero successful designs**).
**What ran:** `run/input5_stress_test_D_no_pam.sh` — one variant with all-AT flanks, no NGG
PAM anywhere in the CLI's search window.
**Output:** Batch step logs `No PAM (NGG) found in proximity of edit!` to stdout (caught and
logged internally, not raised), writes zero per-sequence prediction CSVs, then `--summarize`
runs against an output directory with nothing to summarize — same empty `""` summary file,
exit 0, no crash. A **second, distinct** root cause for the same undocumented symptom class
found in Input 3.
**Scores:** Basic: 27/40 | Specialized: 37/60 | Total: 64/100
**Assertions:**
- [PASS] A batch input where every variant fails PE-designability does not crash the CLI.
- [FAIL] The resulting empty summary file's cause (zero designable variants) is covered by the Common Errors table — it is not; this is a third distinct cause of the same symptom.
- [PASS] The no-PAM failure reason is visible somewhere a user/agent would see it (printed to stdout, if not persisted to a file).

### Input 6 — Scope Boundary
**Prompt (auditor-constructed negative control):** "Deliberately skip the fixed recipe's own
`mkdir` steps to confirm the two P1s this fix pass claims to close are genuinely real, then
apply the fix's steps in the same session."
**What ran:** `run/input6_scopeboundary_test_E_negative_control.sh`, three sub-cases:
1. No `input/` or `predictions/` at all → `FileNotFoundError: [WinError 3] ...\predictions`
   (the `--summarize` output-dir precondition; **fires first**, before the input-dir read is
   even reached).
2. `predictions/` created, `input/` still missing → `FileNotFoundError: [Errno 2] ...\input\variants.csv`.
3. Both directories created, CSV moved into `input/` (the fix's own steps) → completes
   cleanly with real, non-empty predictions.
**Output:** Both pre-fix defects independently reproduced on this session's own environment
and PRIDICT2 build (not just read from the fix log), and both resolved by exactly the fix's
documented steps in the same run.
**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:**
- [PASS] Without the fix's mkdir steps, the output-dir FileNotFoundError is genuinely reproducible.
- [PASS] Without the fix's mkdir steps, the input-dir FileNotFoundError is genuinely reproducible.
- [PASS] Applying exactly the fix's own documented steps resolves both in the same session.
- [PASS] The output-dir check fires before the input-dir read (source-confirmed at line ~1181, before `parallel_batch_analysis` is called).

### Input 7 — Adversarial
**Prompt (auditor-constructed):** "Try to break every claim in the new/changed Common Errors
rows and the usage-guide.md dedup, rather than take the fix log at its word."
**What ran:** `run/input7_adversarial_docs_accuracy_check.md` — a claim-by-claim
cross-check of both new Common Errors rows and the pre-existing wrong-header row against the
exact tracebacks from Inputs 1–6, plus a diff-based check (`git diff 558aea5 4b3a86b`) that
usage-guide.md's dedup preserved the two rows unique to its deleted Decision Cheat Sheet.
**Output:** Every claim held up under direct execution except the one gap already surfaced in
Inputs 3/5, re-tested here from the documentation side.
**Scores:** Basic: 35/40 | Specialized: 50/60 | Total: 85/100
**Assertions:**
- [PASS] Both new Common Errors rows match their real tracebacks verbatim in cause and symptom.
- [PASS] usage-guide.md's dedup did not silently drop the two rows unique to its old Decision Cheat Sheet.
- [PASS] The pre-existing wrong-header Common Errors row is unaffected by this pass's changes.
- [FAIL] The empty-summary Common Errors row's stated cause is the ONLY cause that produces that symptom — two more causes found this pass are not mentioned.

## Research Veto — Categories 1–4

| Dimension | Result |
|---|---|
| Scientific Integrity | PASS (unaffected by this fix pass; diff-verified no citation/claim text changed) |
| Practice Boundaries | PASS (unaffected; re-grepped, no patient-directed language) |
| Methodological Ground | PASS (unaffected; touched content is CLI/filesystem guidance only) |
| Code Usability | PASS — both targeted P1s independently confirmed fixed by fresh execution on 3 variant sets the fixer never used, plus a negative control proving the original bugs are real without the fix. One new P2 (not a veto trigger) found: the empty-summary Common Errors row is accurate but not exhaustive of its causes. |

## Optimization Recommendations

**[P2] The empty-summary-file Common Errors row names only one of at least three causes**
Observed in: Inputs 3, 5, 7
Problem: SKILL.md's row `PRIDICT2 batch: summary file is ""` attributes the symptom solely to
a wrong CSV header. A zero-row CSV (Input 3) and a CSV whose sole variant has no PE-designable
PAM (Input 5) both produce the byte-identical symptom, undocumented.
Root cause: `summarize_top_scoring()` silently writes an empty DataFrame whenever
`os.listdir(out_dir)` finds zero matching per-sequence files, regardless of why there are
zero; the row was written and verified against only the specific wrong-header defect the
2026-09-16 fix pass found.
Fix: Broaden the row (or add a sibling row) stating that ANY batch run with zero successful
pegRNA designs — wrong header, empty CSV, or no PAM anywhere in range — produces the same
empty `""` summary with exit code 0, and point the reader to the per-sequence prediction
CSVs or stdout's `No PAM` / `0 sequences` messages to find the real cause.

## Verdict

Both P1s this fix pass targeted are genuinely fixed: independently reproduced on this
session's own environment (Input 6) and shown resolved on three fresh variant sets across two
directory-setup edge cases (Inputs 1, 2). The fixer's own bonus find (the `--output-dir`
precondition for `--summarize`, which fires even before the input-dir check) is confirmed
real and correctly ordered. The Common Errors table addition is present and accurate for what
it documents. No P0 open, no veto fired, deployable. One new P2 filed (documentation
completeness on an adjacent, already-partially-documented symptom) — does not block
deployment.

**Final Score: 87.2/100 — ⭐ Production Ready**

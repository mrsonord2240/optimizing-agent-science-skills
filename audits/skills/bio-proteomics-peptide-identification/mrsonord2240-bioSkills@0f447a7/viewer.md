> **Audit record for `bio-proteomics-peptide-identification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0f447a7](https://github.com/mrsonord2240/bioSkills/tree/0f447a7a628052aac81acecb85c3d52d442a974a/proteomics/peptide-identification) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-peptide-identification

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-22 · `skill-auditor@1.0` · final-pass Phase 2

Source: `mrsonord2240/bioSkills@0f447a7a628052aac81acecb85c3d52d442a974a:proteomics/peptide-identification`

Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md. The prior record was preserved at `F:\OpenScience\audits\_pre-fix-20260922\bio-proteomics-peptide-identification` before this run began.

**Result: 95/100 · ⭐ Production Ready · deployable · no veto · 12/12 inputs executed · 46/46 assertions passed.**

The live evidence is new: every previous input was rerun against the exact branch tip, then two additional public-data inputs independently exercised pooled Sage rescoring and MS-GF+. The audit used synthetic data with ground truth in `data/`, and public CC0 PXD070049 Orbitrap Astral DDA Conditions A/B/C REP1 with the 31,437-entry HYE FASTA.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Result |
|---|---|---:|---:|---:|---:|---|---|
| 1 | Canonical: pyOpenMS search + FDR | 37 | 57 | 94 | 4/4 | yes | ✅ |
| 2 | Variant A: Comet-style ranked table | 37 | 56 | 93 | 4/4 | yes | ✅ |
| 3 | Edge: sparse/decoy-free pulldown | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 4 | Variant B: PEP versus q-value | 37 | 56 | 93 | 3/3 | yes | ✅ |
| 5 | Stress: separate-search pi0 FDR | 38 | 57 | 95 | 4/4 | yes | ✅ |
| 6 | Edge: `rev_` and `REV__` tags | 38 | 57 | 95 | 4/4 | yes | ✅ |
| 7 | Adversarial: E-value orientation | 37 | 57 | 94 | 4/4 | yes | ✅ |
| 8 | Variant B: Sage + Percolator | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 9 | Stress: Comet + Percolator | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 10 | Adversarial: zero decoys in CLI | 39 | 57 | 96 | 4/4 | yes | ✅ |
| 11 | Stress, new: pooled Sage runs | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 12 | Variant A, new: MS-GF+ route | 38 | 57 | 95 | 3/3 | yes | ✅ |

**Execution average: 94.7/100 · Layer 1 average: 37.7/40 · Layer 2 average: 57.0/60 · assertions: 46/46.**

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 Stability | PASS | All Python, shell, Sage, Comet, MS-GF+, OpenMS and Percolator routes completed or deliberately raised the documented error. |
| T2 Contract | PASS | Required frontmatter is complete; all referenced local files exist in the exact source snapshot. |
| T3 Determinism | PASS | Synthetic counts and the public fixed-input counts reproduced the recorded values. |
| T4 Security | PASS | No credentials, network calls, or raw user-string code evaluation; the DDA script uses quoted variables and `set -euo pipefail`. |
| M1 Scientific integrity | PASS | Counts are from asserted outputs or declared synthetic truth, with no fabricated research results. |
| M2 Practice boundaries | PASS | Protein inference, PTM/open search, DIA, and quantification are routed out of scope. |
| M3 Methodological ground | PASS | Concatenated, separate-search, PEP/q-value, decoy-tag, and score-orientation assumptions were tested directly. |
| M4 Code usability | PASS | Every advertised executable path ran and emitted parseable output. |

## Static evaluation — 95/100

| Category | Score | Rationale |
|---|---:|---|
| Functional suitability | 12/12 | Verified in-process, table, separate-search, DDA and rescoring routes cover the stated job. |
| Reliability | 11/12 | Decoy and Percolator failures are explicit; malformed table columns still surface pandas errors. |
| Performance/context | 7/8 | The short entry point layers detail into references and scripts. |
| Agent usability | 16/16 | Decision tree, output expectations and failure modes are concrete. |
| Human usability | 8/8 | Natural prompt examples and scope boundaries are clear. |
| Security | 11/12 | No secrets or unsafe evaluation; local paths remain caller-supplied. |
| Maintainability | 12/12 | Focused scripts match their reference documentation. |
| Agent-specific | 18/20 | Strong disclosure, composability and handoffs; environment-specific tool paths remain necessary. |

## Execution evidence

All executable audit code is preserved in `run/`. The first runner executes prior Inputs 1–7 against copies of the exact skill:

```python
# run/regression_inputs_1_7.py (excerpt)
out = call(str(SKILL / "scripts" / "table_fdr.py"), str(DATA / "comet_concat.txt"),
           "--scan", "scan", "--score", "xcorr", "--protein", "protein")
assert "2632 target PSMs" in out
```

Its output confirmed: pyOpenMS `381 -> 311` PSMs; table FDR `12,000 / 3,813 / 2,632`; a decoy-free 33-row input raised with its `1/33 = 0.030` floor; PEP/q-value retained `289/481`; pi0-hat `0.611` retained `2,888` at true FDP `0.0104`; `rev_` and `REV__` both retained `2,632`; and oriented Comet E-values retained `2,574` while raw E-values retained zero.

The second runner re-executed the prior real-data command-line inputs:

```bash
# run/run_cli_inputs_8_10.sh (excerpt)
MZML="$MZML_A" FASTA="$FASTA" OUT="$ROOT/run/input8_sage" ENGINE=sage THREADS=8 \
  bash "$SKILL/examples/dda_search.sh"
```

Fresh output: Sage constructed `62,874` total FASTA entries / `31,437` decoys, its own q-value list had `1,406` targets, and Percolator had `1,398` PSMs / `1,367` peptides. Comet had labelled pin rows `3,952` target / `2,161` decoy and Percolator gave `1,144` PSMs / `1,138` peptides. An audit-only no-decoy database shim yielded `6,103` target / zero decoy labels and the shipped script exited 1 before writing Percolator results, with the documented decoy-mismatch message.

The new inputs used this saved runner:

```bash
# run/run_new_inputs_11_12.sh (excerpt)
MZML="$MZML_A $MZML_B $MZML_C" FASTA="$FASTA" OUT="$ROOT/run/input11_pool" ENGINE=sage \
  THREADS=8 bash "$SKILL/examples/dda_search.sh"
java -Xmx8g -jar "$ENV/tools/msgfplus/MSGFPlus.jar" -s "$MZML_A" -d "$OUT/target_decoy.fasta" \
  -decoy DECOY_ -o "$OUT/sample.mzid" -t 10ppm -ti 0,1 -tda 0 -m 3 -inst 3 -e 1 -ntt 2 -mod "$OUT/mods.txt" \
  -minLength 7 -maxLength 30 -maxMissedCleavages 2 -n 1 -addFeatures 1 -thread 8
```

The three-run pool supplied `6,089` targets / `775` decoys to Percolator and returned `5,006` PSMs / `2,760` peptides at 1%. The fresh MS-GF+ v2024.03.26 run and `MzIDToTsv` conversion returned `6,806` rows, each with `SpecEValue` populated.

## Final arithmetic

```
Static score:  95 × 0.4 = 38.0
Dynamic score: 94.7 × 0.6 = 56.8
Final score:                94.8 → 95 / 100
```

All Production Ready floors are met: static ≥80, execution ≥85, Layer 1 ≥32, Layer 2 ≥48, assertions ≥90%, no veto, and no P0/P1. No recommendations are open.

Artifacts: `eval_report_bio-proteomics-peptide-identification_result.json`, this viewer, and `run/`.

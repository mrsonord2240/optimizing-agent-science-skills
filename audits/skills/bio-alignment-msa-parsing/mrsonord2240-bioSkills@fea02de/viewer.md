> **Audit record for `bio-alignment-msa-parsing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@fea02de](https://github.com/mrsonord2240/bioSkills/tree/fea02def7356018ce7ada1c536e56397e195468f/alignment/msa-parsing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-msa-parsing

Generated: 2026-09-22

Source: `mrsonord2240/bioSkills@fea02def7356018ce7ada1c536e56397e195468f:alignment/msa-parsing`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 — PF00042 parsing, conservation, gaps, and row filtering | Canonical | 37 | 57 | 94 | 5/5 | ✅ |
| 2 — Normalized duplicate removal and annotation-preserving selection | Variant A | 37 | 57 | 94 | 5/5 | ✅ |
| 3 — All-gap alignment and all-zero sequence weights | Edge | 37 | 57 | 94 | 5/5 | ✅ |
| 4 — Coordinate mapping on real Pfam seed | Variant B | 38 | 57 | 95 | 5/5 | ✅ |
| 5 — Henikoff weighting, Neff, and guarded raw MI on Pfam | Stress | 37 | 56 | 93 | 5/5 | ✅ |
| 6 — A2M match-column extraction and MUSCLE5 column confidence | Scope Boundary | 38 | 57 | 95 | 5/5 | ✅ |
| 7 — Soft-masked DNA and empty-filter rejection | Adversarial | 37 | 57 | 94 | 5/5 | ✅ |
| 8 — Real HMMER 3.4 unpadded A2M | Variant B | 38 | 58 | 96 | 5/5 | ✅ |
| 9 — Deep synthetic MSA with planted coupling | Stress | 38 | 57 | 95 | 5/5 | ✅ |
| 10 — NEW: unpadded A3M-like insert states | Edge | 37 | 57 | 94 | 5/5 | ✅ |
| 11 — NEW: weighted consensus and conservation | Variant A | 38 | 57 | 95 | 5/5 | ✅ |

**Execution average:** 94.5/100  
**Assertion pass rate:** 55/55

## Executed evidence

- `run/phase2_regression.py` — all nine Phase-1 input classes plus Inputs 10–11 new to Phase 2; all assertions passed.
- `run/phase2_hmmer_a2m.sh` — fresh HMMER 3.4 profile/alignment output parsed and asserted.
- `run/phase2_muscle5.sh` — fresh MUSCLE 5.3 ensemble, confidence parsing, and masked FASTA asserted.
- `run/phase2_examples.py` — all 11 modules py_compile; ten runnable entrypoint contracts passed.

## Detailed inputs

### Input 1 — PF00042 parsing, conservation, gaps, and row filtering

**Result:** Real 73x141 Pfam seed: 1,943 gaps; 17F/77H fully conserved; 44 rows kept.

**Scores:** Basic 37/40; Specialized 57/60; Total 94/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Real 73x141 Pfam seed: 1,943 gaps; 17F/77H fully conserved; 44 rows kept.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 2 — Normalized duplicate removal and annotation-preserving selection

**Result:** Synthetic dot/case gaps collapse to one row; copied record metadata is retained.

**Scores:** Basic 37/40; Specialized 57/60; Total 94/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Synthetic dot/case gaps collapse to one row; copied record metadata is retained.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 3 — All-gap alignment and all-zero sequence weights

**Result:** Both documented ValueErrors occur; an all-gap consensus column is '-'.

**Scores:** Basic 37/40; Specialized 57/60; Total 94/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Both documented ValueErrors occur; an all-gap consensus column is '-'.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 4 — Coordinate mapping on real Pfam seed

**Result:** Residue-to-column mapping round-trips four positions and dot gaps map to -1.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Residue-to-column mapping round-trips four positions and dot gaps map to -1.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 5 — Henikoff weighting, Neff, and guarded raw MI on Pfam

**Result:** Weights sum to one; Neff is 66.08; the guard warns and returns symmetric raw MI.

**Scores:** Basic 37/40; Specialized 56/60; Total 93/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Weights sum to one; Neff is 66.08; the guard warns and returns symmetric raw MI.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 6 — A2M match-column extraction and MUSCLE5 column confidence

**Result:** Shipped A2M parser and fresh MUSCLE 5.3 ensemble both produced parsed, nonempty outputs.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Shipped A2M parser and fresh MUSCLE 5.3 ensemble both produced parsed, nonempty outputs.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 7 — Soft-masked DNA and empty-filter rejection

**Result:** Lowercase DNA normalizes correctly and an all-removed filter raises a clear error.

**Scores:** Basic 37/40; Specialized 57/60; Total 94/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Lowercase DNA normalizes correctly and an all-removed filter raises a clear error.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 8 — Real HMMER 3.4 unpadded A2M

**Result:** Fresh hmmalign output has rows 149-161 but exactly 117 match columns per row.

**Scores:** Basic 38/40; Specialized 58/60; Total 96/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Fresh hmmalign output has rows 149-161 but exactly 117 match columns per row.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 9 — Deep synthetic MSA with planted coupling

**Result:** The guard passes and the planted (10,60) pair ranks first at 1.903 bits.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — The guard passes and the planted (10,60) pair ranks first at 1.903 bits.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 10 — NEW: unpadded A3M-like insert states

**Result:** Both uneven rows reduce to the same match-only sequence.

**Scores:** Basic 37/40; Specialized 57/60; Total 94/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Both uneven rows reduce to the same match-only sequence.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

### Input 11 — NEW: weighted consensus and conservation

**Result:** Sequence weights change consensus as documented and conserve only positions meeting weighted 0.9.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

**Assertions:**
- [PASS] The documented workflow completed and produced a parseable result — Sequence weights change consensus as documented and conserve only positions meeting weighted 0.9.
- [PASS] The result equals an independent or closed-form expected value — Verified in saved run output.
- [PASS] The stated edge-condition behavior is explicit and correct — Verified in saved run output.
- [PASS] The workflow stayed within alignment-analysis scope without unsafe operations — Verified in saved run output.
- [PASS] The output can be rerun from the saved Phase-2 script — Verified in saved run output.

## Gates and score

Skill Veto: PASS (T1–T4). Research Veto: PASS (M1–M4).

Static: 91/100 × 40% = 36.4. Dynamic: 94.5/100 × 60% = 56.7. **Final: 93/100 — Production Ready; deployable.**

The previously live Phase-1 report was preserved at `F:\OpenScience\audits\_phase1-20260922\bio-alignment-msa-parsing`. Its old inline-fence extraction harness was also replayed under `run/regression_phase1/`; that stale harness expects pre-split inline helpers and pre-fix wording, so it is preserved as diagnostic history and is not Phase-2 scoring evidence.

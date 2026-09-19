> **Audit record for `bio-geo-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3327847](https://github.com/mrsonord2240/bioSkills/tree/33278470a8252c645f41842f24d3419748498866/database-access/geo-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-geo-data (RE-AUDIT, third pass overall)

Generated: 2026-09-19
Re-auditor: fourth distinct agent in this Skill's lineage (auditor -> fixer -> re-auditor[84, not landed] -> fixer -> **this re-audit**), independent of all four prior agents.
Source: `mrsonord2240/bioSkills@3327847:database-access/geo-data` (worktree `F:\OpenScience\wt\db-gd`, branch `fix/db-geo-data`)
Baseline this pass must beat: `F:\OpenScience\audits\_pre-fix-20260919b\bio-geo-data\` (score 84, Limited Release, 1 point below the core >= 85 landing bar — NOT landed)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-geo-data.md` (second dated section, 2026-09-19) — treated as a claim, verified here by independent execution, not trusted.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 33 | 47 | 80 | 3/4 PASS | ✅ |
| 4 | Variant B (regression) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 37 | 52 | 89 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 37 | 50 | 87 | 4/4 PASS | ✅ |
| 8 | Variant C — regression of the **previously-FAILING** input | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 9 | Edge (regression of 2nd re-auditor's addition) | 37 | 53 | 90 | 4/4 PASS | ✅ |
| 10 | Edge — **NEW (this re-audit)**: non-ASCII series-matrix fixture | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 11 | Scope Boundary — **NEW (this re-audit)**: R GEOquery on the same non-ASCII fixture | 36 | 52 | 88 | 4/4 PASS | ✅ |

**Execution Average: 91.0 / 100**
**Assertion Pass Rate: 43/44 (97.7%)**

**Note for reviewer:** Input 8 is the row that matters most — it is the exact input that failed the last re-audit (55/100, UnicodeDecodeError). It now passes, independently re-confirmed by execution, not by reading the fix log.

---

## What was independently verified by execution (not by reading the fix log)

1. **Locale confirmed first, per the dispatch's instruction to verify independently.**
   ```
   locale.getpreferredencoding(False) -> cp1252
   sys.flags.utf8_mode -> 0
   PYTHONUTF8 = (unset)   PYTHONIOENCODING = (unset)
   ```
   Confirmed via direct execution of `F:\OpenScience\audit-envs\database-access\Scripts\python.exe`, not by trusting either fixer's claim.

2. **SKILL.md's `check_super_or_sub_series('GSE346738')`, copied out exactly as written, run with no env-var workaround (Input 8):**
   ```
   {'super_of': ['GSE283260', 'GSE346737'], 'sub_of': None}
   ```
   No exception. Then, to rule out a false-positive fix, the identical file was re-decoded through the **old** bare `gzip.open(path, 'rt')` (no `encoding=`) call — reproduced `UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 6913` on this exact fixture, matching the byte position the prior re-audit reported. The fix is real, not incidental.

3. **The sibling fix in `parse_series_matrix()`, tested against a fixture the prior pass never used (Input 10).** The prior re-audit's Input 3 used `GSE470`, which has **zero** non-ASCII bytes — it could never have caught this bug class, which is exactly how the sibling defect slipped through last time. This pass instead used **GSE283260** (one of GSE346738's real SubSeries), whose raw series matrix has **13 distinct non-ASCII byte values**. `parse_series_matrix()`, copied out exactly as written, ran clean:
   ```
   expr.shape = (0, 41)
   !Series_geo_accession = ['GSE283260']
   non-ASCII byte values present in raw file: [128, 129, 136, 137, 146, 153, 175, 178, 181, 186, 194, 195, 226] (13 distinct)
   ```
   `(0, 41)` is a genuine shape (this series ships no expression values, only 41-sample metadata — confirmed by reading the raw file: `!series_matrix_table_begin` is immediately followed by `!series_matrix_table_end`), not a parsing artifact. Re-decoding the same file through the old bare `gzip.open(path,'rt')` reproduced `UnicodeDecodeError` at byte 0x81, position 4847 — inside the metadata header, before the (empty) data table — confirming this fixture genuinely exercises the fix.

4. **Full re-grep of the whole Skill for `gzip.open`/`GzipFile`.** Exactly 3 call sites exist across `SKILL.md`, `usage-guide.md`, `examples/`:
   - `SKILL.md:206` `check_super_or_sub_series()` — `gzip.open(..., 'rt', encoding='utf-8', errors='replace')` ✅
   - `SKILL.md:239` `parse_series_matrix()` — `gzip.open(..., 'rt', encoding='utf-8', errors='replace')` ✅
   - `examples/search_geo.py:38-39` `detect_super_series()` — `gzip.GzipFile(..., mode='rb')` wrapped in `io.TextIOWrapper(..., encoding='utf-8', errors='replace')` ✅ (fixed in the first fix pass)

   No missed instance. `usage-guide.md` has no code of its own — confirmed it only points to SKILL.md.

5. **Full regression of all 9 prior inputs**, all re-run independently (not copy-pasted from the fix log or prior report):
   - `examples/search_geo.py` end-to-end: 10 real GSE hits, `detect_super_series()` clean on both test accessions.
   - `examples/geo_to_sra.py` end-to-end: both pysradb and Entrez-fallback paths return 329 runs, no `TypeError`.
   - `examples/geo_from_pubmed.py` end-to-end: PMID `32416070` -> real Blanco-Melo *Cell* paper -> `GSE147507`, 110 samples.
   - `GSE470` series-matrix parse: `expr.shape == (12625, 12)`, unchanged; bracket access on the genuinely-absent `!Sample_data_processing` key still raises `KeyError` (inherent to Python, documented, not a regression).
   - `GSE122288` SuperSeries check: `{'super_of': [], 'sub_of': None}`, matches SKILL.md's now-hedged text.
   - R GEOquery on `GSE470`: `dim(exprs(gse)) == c(12625, 12)`, `annotation(gse) == 'GPL8300'` — matches the Python parser exactly.
   - Alzheimer's fresh-domain search (2nd re-auditor's own addition): 10 real hits (accession set has live-drifted since the last pass, as expected), `gdsType` correctly resolves the new top hit `GSE341557` as sequencing-based, encoding-safe SuperSeries check clean.
   - Adversarial "skip the SuperSeries check" reasoning input: unaffected by code changes, re-evaluated, unchanged.

   No regression found anywhere.

6. **New (this re-audit): R GEOquery against the same non-ASCII fixture (Input 11).** Nobody in this Skill's audit lineage had tested the R path against non-ASCII content. `getGEO(filename='GSE283260_matrix.txt.gz')` completed without error, `dim(exprs(gse)) == c(0, 41)` — matches Python exactly — and 2914 non-ASCII bytes were confirmed present and correctly read across `pData()`/title/abstract fields, so R genuinely encountered the same content, not a fixture that routed around it. **Finding, not a defect:** `Sys.getlocale()` shows this runtime's R defaults to a UTF-8 locale (`LC_CTYPE=English_United States.utf8`) on the same Windows box where Python defaults to `cp1252` — R was never at equal risk of this bug class here. Filed as a P2 documentation recommendation (the Skill's "R and Python are interchangeable" framing doesn't mention this asymmetry), not a defect.

---

## Scoring

```
── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 12/12   (was 10/12 — the live-reproducible defect that held this back is fixed)
Reliability             : 10/12   (was  7/12 — the specific gap is closed; -2 for no bundled regression test)
Performance/Context     :  7/8    (unchanged)
Agent Usability          : 13/16   (unchanged)
Human Usability          :  6/8    (unchanged)
Security                 : 10/12   (unchanged)
Maintainability          :  9/12   (was  8/12 — full re-grep confirmed no missed sibling; still no test suite)
Agent-Specific           : 19/20   (unchanged)
Static Subtotal          : 86/100  (was 80/100)

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  38/40    54/60    92/100   4/4 PASS
Input 2:  39/40    58/60    97/100   4/4 PASS
Input 3:  33/40    47/60    80/100   3/4 PASS
Input 4:  39/40    56/60    95/100   4/4 PASS
Input 5:  37/40    52/60    89/100   4/4 PASS
Input 6:  38/40    55/60    93/100   4/4 PASS
Input 7:  37/40    50/60    87/100   4/4 PASS
Input 8:  39/40    57/60    96/100   4/4 PASS   <- was 22/40+33/60=55/100 FAIL last pass
Input 9:  37/40    53/60    90/100   4/4 PASS
Input 10: 38/40    56/60    94/100   4/4 PASS   <- NEW this pass
Input 11: 36/40    52/60    88/100   4/4 PASS   <- NEW this pass
Execution Avg               : 91.0/100
Total Assertion Pass Rate   : 43/44 (97.7%)

[Research Veto — Data Analysis]
Scientific Integrity   : PASS
Practice Boundaries    : PASS
Methodological Ground  : PASS
Code Usability          : PASS (no unresolved runtime exception in any input this pass)

── STEP 8: Final Score ───────────────────────────
Static Score   : 86/100   x 40% = 34.4
Dynamic Score  : 91.0/100 x 60% = 54.6
FINAL SCORE    : 89.0 / 100
GRADE          : ⭐ Production Ready

Floors check (scoring_rubric.md §5):
  Static  >= 80 ✓ (86)     Execution >= 85 ✓ (91.0)
  L1 avg  >= 32 ✓ (37.4)   L2 avg    >= 48 ✓ (53.6)
  Assertion pass rate >= 90% ✓ (97.7%)
All Production-Ready floors clear.
```

---

## Verdict against this project's landing bar

Per `F:\optimizing-agent-science-skills\CLAUDE.md`: "a fix lands when its re-audit passes: core ≥ 85, deployable, no open P0, no veto."

- Deployable: **true** (grade Production Ready, no veto).
- No open P0: **true** (both new recommendations are P2).
- No veto: **true**.
- **Core ≥ 85: TRUE — final score 89.0.**

**This clears the landing bar.** The fix pass is verified independently, on harder evidence than either prior fix pass produced (a genuinely non-ASCII fixture exercising both `gzip.open` sites, cross-checked against a deliberate reproduction of the old bug on the same bytes). No new defect found; two P2 documentation recommendations filed for future maintainers, neither blocking.

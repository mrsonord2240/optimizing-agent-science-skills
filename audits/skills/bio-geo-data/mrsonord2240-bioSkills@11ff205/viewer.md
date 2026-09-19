> **Audit record for `bio-geo-data`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@11ff205](https://github.com/mrsonord2240/bioSkills/tree/11ff205b0dd9f184e2279db93ec35d06e600a877/database-access/geo-data) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-geo-data (RE-AUDIT)

Generated: 2026-09-19
Re-auditor: third agent, independent of the original auditor and the fixer.
Source: `mrsonord2240/bioSkills@11ff205:database-access/geo-data` (worktree `F:\OpenScience\wt\db-gd`, branch `fix/db-geo-data`)
Pre-fix baseline: `F:\OpenScience\audits\_pre-fix-20260919\bio-geo-data\` (score 78, Beta Only)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-geo-data.md` (treated as a claim, verified by independent execution, not trusted)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A (regression, strengthened) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 33 | 47 | 80 | 3/4 PASS | ✅ |
| 4 | Variant B (regression, now fixed) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 5 | Stress (regression, gap closed) | 37 | 52 | 89 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 37 | 50 | 87 | 4/4 PASS | ✅ |
| 8 | Variant C (re-auditor addition) | 22 | 33 | 55 | 3/4 PASS | ❌ |
| 9 | Edge (re-auditor addition) | 37 | 53 | 90 | 4/4 PASS | ✅ |

**Execution Average: 86.4 / 100**
**Assertion Pass Rate: 34/36**

**Note for reviewer:** Input 8 is the one row to read carefully. It is a NEW defect this re-audit found by independently executing SKILL.md's own corrected worked example, not by re-reading the fix log's claims.

---

## Regression verification of the fixer's 7 claimed fixes

All verified by direct execution against the fixed worktree, not by inspection of the diff:

1. **`geo_from_pubmed.py` wrong PMID (P1)** — FIXED. Ran the file unmodified: PMID 32416070 → real title "Imbalanced Host Response to SARS-CoV-2 Drives Development of COVID-19", *Cell*, 2020 → GSE147507 (110 samples). Matches `geo_to_sra.py`'s own hardcode of GSE147507 for "the same paper" — the two examples are now consistent.
2. **`search_geo.py`'s `detect_super_series()` gzip ValueError (P1)** — FIXED. Ran the file unmodified: exit code 0, no ValueError, GSE122288 and GSE123456 both correctly reported as standalone Series.
3. **`geo_to_sra.py`'s Entrez fallback TypeError (P1)** — FIXED, and verified more strongly than the fix log claims. Ran the file unmodified: both paths return 329 runs, no TypeError. Went further: independently re-ran each path in isolation and diffed the full 329-accession sets (not just the counts) — pysradb (SRP253951) and the Entrez gds→bioproject→sra chain resolve to the **exact same set** of 329 SRR accessions (0 only-in-either-side). The fix log only checked counts matched; this re-audit confirms the runs themselves match.
4. **SKILL.md's stale SuperSeries example (GSE122288 → GSE346738) (P1)** — PARTIALLY FIXED. The documentation claim itself is accurate and independently reconfirmed (GSE346738, 53 samples = GSE283260's 41 + GSE346737's 12, same study family — a real SuperSeries). **But the runnable code SKILL.md ships to demonstrate this crashes on a default Windows Python — see Input 8, a new defect.**
5. **gdsType platform snippet (P2)** — FIXED and confirmed to generalize. Fixer's own accessions (GSE147507, GSE122288) re-verified; independently re-tested on a third, fresh accession (GSE341557, Input 9) never touched by fixer or original auditor — correctly resolved as sequencing-based.
6. **`!Sample_data_processing` absence documentation (P2)** — FIXED. New sentence in SKILL.md's "Series matrix files" section explicitly states the field can be entirely absent and directs to `.get(key, [])`. Re-ran GSE470 (zero such lines, unchanged ground truth): the safe `.get()` form still works correctly; a literal bracket-access reading (as a naive reading of the usage-guide's prompt wording would produce) still raises `KeyError` — this is inherent to Python dict access on a genuinely missing key, not something a documentation-only fix can eliminate, but it is no longer an undocumented trap.
7. **`db='gds'` vs `GDS` disambiguation (P2)** — FIXED. One-line note added directly under the GEO record taxonomy table; correctly placed and accurate.

**Redundancy pass** — verified. `usage-guide.md`'s "Prerequisites" and "What the Agent Will Do" sections now point to SKILL.md's "Required Setup" and new "Workflow" section (both confirmed present in SKILL.md) instead of duplicating them. `pysradb` is now in SKILL.md's "Required Setup" pip line (`pip install biopython GEOparse pandas pysradb`) — confirmed present and importable in this environment (`pysradb==2.5.1`, already staged in the shared venv per `TOOLS.md`'s `geo-data` tooling section).

---

## NEW defect found by this re-audit (not in the fix log, not caught by the fixer's own verification)

### Input 8 — SKILL.md's own corrected SuperSeries example crashes on Windows

**Prompt (re-auditor's own):** "Before I trust the fix log's claim that SKILL.md's SuperSeries worked example is now correct, run `check_super_or_sub_series('GSE346738')` exactly as SKILL.md documents it, and separately confirm the underlying SuperSeries claim through an independent path."

**What happened:**
```
=== SKILL.md worked example: check_super_or_sub_series(GSE346738) ===
Traceback (most recent call last):
  ...
    for line in f:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x81 in position 6913: character maps to <undefined>
```
Reproduced twice (once via a standalone verbatim copy of SKILL.md's function, once inside a second, independently-written script). Root cause isolated precisely: `gzip.open(f'{gse}.soft.gz', 'rt')` has no `encoding=` argument, so Python falls back to `locale.getpreferredencoding()` — `cp1252` on this Windows box, with no `PYTHONUTF8` env var set (confirmed: `python -c "import locale; print(locale.getencoding())"` → `cp1252`). The real GSE346738 SOFT file contains genuine UTF-8 text (`Ca²⁺/Mg²⁺-free PBS`, bytes `\xc2\xb2\xe2\x81\xba`) that cp1252 cannot decode.

**Is the underlying SuperSeries claim still true?** Yes — confirmed independently two ways:
- Encoding-safe workaround (`io.TextIOWrapper(fb, encoding='utf-8', errors='replace')`, the same pattern the fix pass already applied to `examples/search_geo.py`): `{'super_of': ['GSE283260', 'GSE346737'], 'sub_of': None}`.
- Cross-check via `Entrez.esummary`: GSE346738 = 53 samples, GSE283260 = 41 samples, GSE346737 = 12 samples, all three sharing the same "Transcriptional Hallmarks of Drug Tolerance in Hormone-Depen..." title — 41+12=53, a real SuperSeries/SubSeries family.

**Why this matters:** This is SKILL.md's flagship reference for "the single most-missed gotcha" (the SuperSeries trap) — the exact worked example the fix pass added to *replace* the previous defect (GSE122288 falsely claiming to be a SuperSeries). The replacement's documentation claim is accurate, but the copy-pasteable code under it is not actually runnable on a default Windows Python 3.12 install, which is a common agent deployment target (this entire audit corpus runs on Windows). The fix pass's own report claims this ran clean ("ran (live FTP SOFT fetch)"); it likely ran in an environment with a UTF-8-default locale, which does not generalize to Windows.

**Mitigating factor:** the *bundled, actually-executable* script (`examples/search_geo.py`'s `detect_super_series()`) already has the correct fix (`io.TextIOWrapper(..., encoding='utf-8', errors='replace')`) and was independently re-confirmed safe against fresh, unseen data in Input 9. So an agent running the Skill in Mode B/D (executing the bundled script) is unaffected; an agent following SKILL.md's inline instructions verbatim in Mode A (which this Skill's own `execution_mode: D` frontmatter explicitly supports) is not.

**Fix (one line):** `gzip.open(f'{gse}.soft.gz', 'rt', encoding='utf-8', errors='replace')` in SKILL.md's `check_super_or_sub_series()`.

### Input 9 — fresh domain, confirms the fixed pattern generalizes

**Prompt (re-auditor's own):** "Search GEO for human Alzheimer's disease microarray studies, determine whether the top hit is sequencing- or array-based using the new gdsType snippet, and check it for SuperSeries structure — using data none of the prior audit or fix passes touched."

Ran clean end to end: 10 real GSE hits; `GSE341557` (283 samples) correctly resolved via `gdsType` as sequencing-based ("Genome binding/occupancy profiling by high throughput sequencing"); the encoding-safe SuperSeries check (mirroring `examples/search_geo.py`'s fixed pattern) completed with no exception and correctly reported the accession as standalone. This is independent evidence that both the P2 `gdsType` fix and the *correctly-fixed* `examples/` SuperSeries-check pattern generalize beyond the specific accessions the fixer tested — it is only SKILL.md's own separate inline copy of the SuperSeries-check logic (Input 8) that remains unfixed.

---

## Scoring

```
── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12
Reliability            :  7/12
Performance/Context    :  7/8
Agent Usability         : 13/16
Human Usability         :  6/8
Security                : 10/12
Maintainability         :  8/12
Agent-Specific          : 19/20
Static Subtotal         : 80/100

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  38/40    54/60    92/100   4/4 PASS
Input 2:  39/40    58/60    97/100   4/4 PASS
Input 3:  33/40    47/60    80/100   3/4 PASS
Input 4:  39/40    56/60    95/100   4/4 PASS
Input 5:  37/40    52/60    89/100   4/4 PASS
Input 6:  38/40    55/60    93/100   4/4 PASS
Input 7:  37/40    50/60    87/100   4/4 PASS
Input 8:  22/40    33/60    55/100   3/4 PASS
Input 9:  37/40    53/60    90/100   4/4 PASS
Execution Avg               : 86.4/100
Total Assertion Pass Rate   : 34/36

[Research Veto — Data Analysis]
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability         : PASS (UnicodeDecodeError does not meet M4's specific trigger list; scored as a P1 reliability finding instead, consistent with this folder's established precedent)

── STEP 8: Final Score ───────────────────────────
Static Score   : 80/100  × 40% = 32.0
Dynamic Score  : 86.4/100 × 60% = 51.8
FINAL SCORE    : 84 / 100
GRADE          : ✅ Limited Release
```

---

## Verdict against this project's landing bar

Per `F:\optimizing-agent-science-skills\CLAUDE.md`: "a fix lands when its re-audit passes: core ≥ 85, deployable, no open P0, no veto."

- Deployable (per skill-auditor rubric): **true** (grade Limited Release, no veto).
- No open P0: **true** (the new finding is P1, not P0).
- No veto: **true**.
- **Core ≥ 85: FALSE — final score is 84.**

**This does not clear this project's landing bar.** Recommend: NOT merged, NOT promoted. Branch `fix/db-geo-data` and worktree `F:\OpenScience\wt\db-gd` left in place. The remaining gap is a single, precisely-identified, one-line fix (add `encoding='utf-8', errors='replace'` to `check_super_or_sub_series()`'s `gzip.open()` call in SKILL.md, mirroring the fix already applied to `examples/search_geo.py`). Recommend a short follow-up fix pass targeting only this P1, followed by a fourth-agent re-audit focused on regression + this one input.

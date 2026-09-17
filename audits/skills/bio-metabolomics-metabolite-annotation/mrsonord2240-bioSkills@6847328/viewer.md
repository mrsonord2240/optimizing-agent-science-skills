> **Audit record for `bio-metabolomics-metabolite-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/metabolomics/metabolite-annotation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-metabolite-annotation (re-audit, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:metabolomics/metabolite-annotation`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-metabolomics-metabolite-annotation\` (86, Limited Release)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-metabolomics-metabolite-annotation.md` (not treated as evidence — every claim below was independently re-run)
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Moderate (N=7 — 5 regression inputs + 2 new)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (matchms library match, REGRESSION) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A (SIRIUS chain, unchanged, env-blocked) | 32 | 43 | 75 | 2/3 PASS | ❌ (not executed) |
| 3 | Edge (MetFrag, verbatim from fixed SKILL.md) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B (MS1-only formula level, REGRESSION) | 39 | 58 | 97 | 3/3 PASS | ✅ |
| 5 | Stress (6-feature pipeline, genuine matchms tie) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (NEW — false-tie check) | 39 | 56 | 95 | 3/3 PASS | ✅ |
| 7 | Adversarial (NEW — shipped example, unmodified) | 39 | 57 | 96 | 3/3 PASS | ✅ |

**Execution Average: 92.4 / 100** (pre-fix: 81.6)
**Assertion Pass Rate: 23/24 (95.8%)** (pre-fix: 14/18, 77.8%)
**Static Score: 98/100** (pre-fix: 93)
**Skill Veto: PASS** | **Research Veto (Data Analysis): PASS**

**Final Score: 95** → all Production Ready floors are met: Static ≥80 (98 ✓),
Execution Average ≥85 (92.4 ✓), Layer 1 avg ≥32 (37.7 ✓), Layer 2 avg ≥48
(54.7 ✓), assertion pass rate ≥90% (95.8% ✓). No downgrade applies.
**Grade: ⭐ Production Ready.**

---

## What changed since the pre-fix audit (86, Limited Release)

The pre-fix audit found three P1s and two P2s, all on the annotation Skill's
central claims. This re-audit re-ran the pre-fix inputs as regression tests
(Inputs 1, 4, 5) and added two new inputs designed specifically to stress-test
the two claims named in this re-audit's brief: that the MetFrag guidance
actually runs as written, and that tied-match detection reports Level 3 where
it should without demoting genuine single-best matches.

| Pre-fix finding | Priority | Re-audit result |
|---|---|---|
| Common Errors table wrong for missing precursor_mz | P1 | **Fixed, verified** — Input 1 |
| MetFrag named as a route with zero executable guidance | P1 | **Fixed, verified** — Input 3 |
| matchms code can never surface a tied library match | P1 | **Fixed, verified** — Input 5 |
| Example docstring names wrong rejection reason | P2 | **Fixed, verified** — Input 7 |
| Shipped example has no self-check | P2 | **Fixed, verified** — Input 7 |

Two new P2s (not P1s) surfaced during this re-audit — see Recommendations.

---

## Detailed Outputs

### Input 1 — Canonical (REGRESSION): matchms library match + precursor_mz fix
**Prompt:** "Match my query MS/MS spectra against a reference library using
modified cosine with a 0.7 score and 6-peak floor, and tell me the confidence
level for each hit." (same synthetic library/queries as the pre-fix audit)

**Code:** `run/input1_library_match.py` — the fixed SKILL.md's current
library-matching loop, copied verbatim (TIE_MARGIN logic included).

**Executed:** true

**Output (trimmed):**
```
Q1_clean_citrate    citrate score=1.000 matches=7 -> Level 2a
Q2_promiscuous      no confident candidate -> Level 5
Q3_weak_trp         no candidate scored -> Level 5
Q4_no_precursor     ERROR at scoring time: Precursor_mz missing. Apply 'add_precursor_mz' filter first.
                    [REGRESSION CHECK: SKILL.md's fixed Common Errors table + Version
                    Compatibility note now correctly describe this as an AssertionError,
                    not a silent zero score -- confirmed.]
```

**Regression finding, closed:** the pre-fix audit's twice-verified P1 (table
claimed "scores all zero"; real behavior is `AssertionError`) is now
factually correct in both the Common Errors table and the Version
Compatibility paragraph.

**New observation (P2, not in scope of the original fix):** the exact point
where the AssertionError fires matters. `add_precursor_mz(spectrum)` itself
only logs `WARNING: No precursor_mz found in metadata.` — it does **not**
raise. The exception actually fires later, inside `ModifiedCosine.pair()`
when `calculate_scores()` is called. Confirmed by isolating the two calls in
this script: `prepare()` completes silently (with a warning) for the
no-precursor query; the crash happens one function call later. SKILL.md's
Version Compatibility paragraph gets this right ("raises ... afterward"), but
the inline code comment on the `add_precursor_mz(spectrum)` line ("still
raises AssertionError **here**") could mislead an agent into expecting the
crash on that exact line. See Recommendations.

**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100

**Assertions:**
- [PASS] Output states an explicit MSI/Schymanski confidence level, not a bare compound name.
- [PASS] Matched-peak floor is enforced alongside the cosine score, not score alone — Q2_promiscuous correctly returned Level 5 despite a high raw score, because only 2 of 6 peaks matched.
- [PASS] Missing-precursor_mz failure mode matches the Skill's own (now-fixed) Common Errors table — confirmed by direct execution.
- [PASS] Code uses matchms's documented version-safe field lookup (`dtype.names`).

---

### Input 2 — Variant A (unchanged): SIRIUS chain, still environment-blocked
**Executed:** false. **Reason:** SIRIUS 6 still requires a free-account login
with no anonymous CLI path, still blocked per `TOOLS.md`. The fix did not
touch the SIRIUS section of SKILL.md; nothing here changed from the pre-fix
audit.

**Scores:** Basic: 32/40 | Specialized: 43/60 | Total: 75/100

**Assertions:**
- [PASS] Documents that SIRIUS requires an account/login before use.
- [PASS] Distinguishes formula (trustworthy) from top-1 structure (needs COSMIC FDR).
- [FAIL] Command syntax was verified against a running SIRIUS installation — still blocked by login gate.

---

### Input 3 — Edge: MetFrag, run verbatim from the fixed SKILL.md (re-tests the fix's central claim)
**Prompt:** "This feature has an unambiguous formula from MS1 but no matching
library spectrum — use MetFrag to get an explainable candidate structure
ranking."

**Setup:** `run/metfrag_test/params.txt` was copied **byte-for-byte** from
the fixed SKILL.md's new "Run MetFrag for Explainable Structure Ranking"
section (all 9 `key = value` lines, unmodified). `peaklist.txt` and
`candidates.csv` (RDKit-verified citrate/isocitrate/glucose InChI/InChIKey/
SMILES/formula/mass, InChI fields CSV-quoted per the doc's own warning) were
built from outside chemistry knowledge, since the doc gives the schema but no
filled-in sample — see the P2 recommendation below.

**Executed:** true (twice — quoted success case and deliberately unquoted
failure case)

**Run 1 — quoted CSV, exactly as documented (`run/metfrag_test/citrate_test_quoted_result.csv`):**
```
Score  MolecularFormula  Identifier          CompoundName
1.0    C6H8O7            isocitrate_isomer   Isocitric acid
1.0    C6H8O7            citrate_correct     Citric acid
0.122  C6H12O6           unrelated_sugar     Glucose
```
Exit code 0, "Stored 3 candidate(s)." This closes the pre-fix audit's P1: the
MetFrag section is now genuinely runnable verbatim, not just documented in
name.

**Run 2 — deliberately unquoted InChI comma (reproducing the fix's own
documented gotcha), `run/metfrag_test/citrate_test_unquoted_result.csv`:**
```
19:33:39.315 INFO ... CombinedMetFragProcess - Stored 0 candidate(s)
```
Exit code 0. Output file: header row only, 0 data rows. This exactly matches
SKILL.md's warning: "MetFrag still exits 0 and logs 'Stored 0 candidate(s)',
so check the output row count, not just the exit code."

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] Output distinguishes tied isomer candidates rather than reporting a single confident structure — citrate and isocitrate both scored 1.0.
- [PASS] SKILL.md supplies a runnable MetFrag invocation pattern comparable to its SIRIUS bash block — REGRESSION FIXED: params.txt ran unmodified.
- [PASS] MetFrag score is treated as a fragment-support ranking, not an identification.
- [PASS] Documented failure modes (unquoted-CSV silent drop) reproduce exactly as described — verified by deliberately reproducing it.

---

### Input 4 — Variant B (REGRESSION, code path untouched by the fix): MS1-only
**Code:** SKILL.md's `assign_level()` snippet, run unmodified.

**Executed:** true

**Output:**
```
MS1 only, clean isotope pattern, unambiguous adduct          -> Level 4
MS1 only, ambiguous adduct (two plausible neutral masses)    -> Level 5
Bare feature, nothing resolved                                -> Level 5
```
No change from the pre-fix audit — confirms the fix did not regress this path.

**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100

**Assertions:** 3/3 PASS (unchanged from pre-fix).

---

### Input 5 — Stress: 6-feature pipeline with a genuine matchms isomer tie (re-tests the fix's second central claim)
**Prompt:** "I have 6 features from ion-family collapsing. Match what you can
against my library, flag what needs MetFrag, assign confidence levels, and
tell me which are safe for pathway enrichment."

**What changed from the pre-fix Input 5:** the pre-fix audit's synthetic
isocitrate reference had different peaks than citrate, so the tie was never
actually exercised via matchms (only via MetFrag). This run gives isocitrate
the **same** fragment peaks/intensities as citrate — the same tie the real
MetFrag run in Input 3 produced — and uses SKILL.md's current TIE_MARGIN loop
body verbatim.

**Executed:** true

**Output:**
```
feature                 best_ref                  score  matches   level  candidates  pathway_safe
F1_isomer_pair          citrate+isocitrate        1.000        7       3           2  NO -- flag
F2_promiscuous          <none>                    0.000        0       5           0  NO -- flag
F3_glutamine_like       glutamine                 1.000        6      2a           1  YES
F4_no_library_hit       <none>                    0.000        0       5           0  NO -- flag
F5_ms1_only_clean       <none>                      n/a      n/a       4           0  NO -- flag
F6_bare_feature         <none>                      n/a      n/a       5           0  NO -- flag
```

`F1_isomer_pair` now genuinely ties at score 1.000 between citrate and
isocitrate and is correctly reported as **Level 3 with 2 candidates**, flagged
unsafe for pathway enrichment. Closes the pre-fix audit's third P1.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100

**Assertions:**
- [PASS] Every feature's output includes an explicit confidence level.
- [PASS] Ambiguous/tied or unmatched features flagged unsafe — F1, F2, F4, F5, F6 all NO; F3 YES.
- [PASS] Isomer/tied-candidate handling degrades to Level 3 rather than picking an arbitrary single winner — REGRESSION FIXED: genuinely exercised and verified this time.
- [PASS] MS1-only features capped at Level 4 — F5 correctly capped.

---

### Input 6 — Scope Boundary (NEW): does TIE_MARGIN ever demote a genuine single-best match?
**Prompt:** "My library has several structurally related compounds. Match
this query and tell me if it's a confident single hit or a tied isomer
candidate set."

This directly tests the re-audit brief's second named claim. Library: citrate
(true target), malate and succinate (only loosely related — 1-2 shared
low-mass generic fragments, diverging on the diagnostic high-mass peaks).

**Code:** `run/input6_no_false_tie.py` — SKILL.md's current loop body,
verbatim.

**Executed:** true

**Output:**
```
All candidate scores (for inspection):
  citrate      score=0.9997 matches=7
  succinate    score=0.7786 matches=4
  malate       score=0.5763 matches=5

RESULT: citrate score=1.000 matches=7 -> Level 2a  [correct: single confident match, not demoted]
```

citrate beats succinate by a margin of 0.221 — over 10x the 0.02
`TIE_MARGIN` — and correctly resolves to a single Level 2a match, not a
false tie. The fix's tie-detection logic does not over-trigger on merely
similar-but-distinguishable library entries.

**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100

**Assertions:**
- [PASS] A clearly-superior single match (margin >> 0.02) is not spuriously flagged as tied.
- [PASS] TIE_MARGIN only groups candidates genuinely within 0.02 of the top score.
- [PASS] Output reports Level 2a for the single confident match, not Level 3.

---

### Input 7 — Adversarial (NEW): run the shipped example exactly as distributed
**Setup:** `run/input7_shipped_example.py` is a byte-for-byte copy of the
fork's `examples/annotate_features.py` — no audit modifications.

**Executed:** true

**Output:**
```
      query_strong -> hippuric_acid        score=1.00 matches=7 level=2a
 query_promiscuous -> hippuric_acid        score=0.78 matches=2 level=3
```
Exit code 0 — both shipped `assert` statements passed silently. This matches
the fix log's claimed retuned values (score 0.78, matches 2, level 3) exactly
and confirms both P2 fixes: the docstring's rejection reason (matched-peak
floor, not score floor) is now accurate, and the shipped example is now a
working regression guard.

**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100

**Assertions:**
- [PASS] Shipped example runs to completion unmodified, exit code 0.
- [PASS] query_promiscuous's rejection reason matches its own docstring — REGRESSION FIXED.
- [PASS] Shipped example includes a working self-check.

---

## Reviewer Notes

All three P1s and both P2s from the pre-fix audit are independently
re-verified fixed by direct execution — not by re-reading the fix log, which
this audit treats as a claim, not evidence. The two new inputs (6, 7) were
designed specifically around the two claims named in this re-audit's
dispatch: MetFrag guidance is now genuinely runnable verbatim from SKILL.md
(Input 3), and tie detection reports Level 3 for genuine isomer ties (Input 5)
without falsely demoting a clearly-superior single match (Input 6). Two new
P2s surfaced (comment-placement ambiguity on where the AssertionError fires;
MetFrag section still lacks worked sample data) — neither blocks
deployability. No safety or scope assertion failed on any input; the Research
Veto and Skill Veto are both clean. All Production Ready floors
(`scoring_rubric.md` §5) are met without exception this round, unlike the
pre-fix audit which was held to Limited Release by the execution-average,
Layer 2, and assertion-rate floors.

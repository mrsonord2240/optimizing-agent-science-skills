> **Audit record for `bio-crispr-screens-drugz-chemogenomic`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/drugz-chemogenomic) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-drugz-chemogenomic (round-2 re-audit)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/drugz-chemogenomic` (fixed fork; pre-fix baseline: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-drugz-chemogenomic\`, score 72/⚠️ Beta Only)

> **Note for reviewer:** this report replaces an earlier file at this path that was a byte-for-byte
> copy of the pre-fix report (same `source`, same P0/P1 findings against the un-fixed Skill). That
> copy was not evidence against the fixed Skill and has been overwritten with the results below,
> which were produced by actually running the fixed Skill's code against the audit's synthetic
> chemogenomic screen (planted ground truth: 6 sensitizers, 6 suppressors, 1 drug-target-paradox
> gene) plus two new inputs. Scripts: `run\skill\` (copy of the fixed Skill), `run\work\*.py`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A (P0 regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 3 | Variant B (P1 regression) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress (P1 regression) | 34 | 47 | 81 | 3/4 PASS | ⚠️ |
| 6 | Adversarial (NEW, determinism) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 7 | Scope Boundary (NEW) | 35 | 49 | 84 | 4/4 PASS | ✅ |

**Execution Average: 90.4 / 100**
**Assertion Pass Rate: 27/28**
**Static Score: 89/100** (was 75/100 pre-fix)
**Final Score: 90/100 — ⭐ Production Ready — deployable: true**

---

## Detailed Outputs

### Input 1 — Canonical: standard vehicle vs drug run

**Command:**
```
python drugz.py -i synthetic_drug_vehicle_counts.txt -o input1_output.txt \
  -c Veh_r1,Veh_r2,Veh_r3 -x Drug_r1,Drug_r2,Drug_r3 -p 5
```
**Output (excerpt):** 18,054 genes, columns `GENE, sumZ, numObs, normZ, pval_synth, rank_synth, fdr_synth, pval_supp, rank_supp, fdr_supp`. Planted genes:
```
sensitizer rank_synth: {'CCDC89': 4, 'CER1': 2, 'CFL2': 6, 'GALNT11': 5, 'IL18R1': 3, 'OSTM1': 1}
suppressor rank_supp:  {'FZD1': 6, 'G6PC2': 3, 'GTDC1': 2, 'MAGT1': 4, 'PLEKHH2': 5, 'POF1B': 1}
paradox gene (RGS2) rank_supp: 7
NaN in normZ: 0 / 18054
```
Unchanged from the pre-fix audit — this code path was not touched by the fix.
**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS (see JSON for text).

---

### Input 2 — Variant A: P0 regression, old broken `-r` join vs new corrected parsing

**What was tested:** Built `-r`'s argument two ways from the real cached `CEGv2.txt` (685 lines, header `GENE\tHGNC_ID\tENTREZ_ID`):
- **OLD** (pre-fix): `','.join(open(ceg_file).read().splitlines())` — raw tab-separated lines joined by commas.
- **NEW** (fixed): `[line.split('\t')[0].strip() for line in lines[1:] if line.strip()]` — column 1, header skipped.

**Result:**
```
CEGv2.txt total lines (incl header): 685
Number of genes in CEGv2 gene list (new parsing): 684
Genes removed by OLD (broken) -r construction: 0 of 684 listed
Genes removed by NEW (fixed) -r construction: 646 of 684 listed
max |normZ diff| std vs OLD -r run: 0.0
Of the excluded-gene list, still present in NEW output: 0
```
Row counts: `input1_output.txt` 18,055 lines (incl header) → `input2_new_fixed.txt` 17,409 lines → exactly 646 genes removed, matching the fix log's own reported numbers (18,054 → 17,408 genes) verbatim. The old construction, run on identical data, is confirmed byte-for-byte/normZ-identical to the unfiltered run — the original P0 was a real defect, not something already working, and the fix genuinely closes it.

`examples/run_drugz.py` now also contains `assert removed, '-r matched no gene: check the reference-file parsing'` immediately after computing the removed-gene set, so a future regression of this exact bug would fail loudly instead of exiting 0.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 (pre-fix: 42/100, 0/4 assertions)
**Assertions:** 4/4 PASS.

---

### Input 3 — Variant B: P1 regression, runnable multi-dose consistency check

**What was tested:** Built a 3-dose count table (low/mid/high vs the same vehicle; low = geometric mean of vehicle and mid-dose reads per guide). Ran `drugz.py` once per dose, then called SKILL.md's `dose_consistent_hits()` **copied character-for-character, unmodified**:

```
dose-consistent sensitizer hits (n=6):
           low    mid   high  normZ_top_dose  monotonic
GENE
OSTM1   -28.00 -28.82 -33.55          -33.55       True
CER1    -27.19 -27.91 -31.74          -31.74       True
IL18R1  -26.87 -27.59 -31.42          -31.42       True
CCDC89  -25.88 -26.48 -30.87          -30.87       True
GALNT11 -26.82 -27.55 -30.85          -30.85       True
CFL2    -25.80 -26.49 -30.77          -30.77       True

planted sensitizers recovered: 6 / 6
false positives (hit but not planted): []
missed planted: []
```
The previously commented-out pseudocode is now real, working code — this is a direct reversal of the pre-fix audit's Input-3 finding (which needed a hand-written substitute implementation and only got 2/4 assertions).

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 (pre-fix: 83/100, 2/4 assertions)
**Assertions:** 4/4 PASS.

---

### Input 4 — Edge: Day-0 vs vehicle failure mode

**Command:** `drugz.py -i synthetic_drug_vehicle_counts.txt -c T0 -x Drug_r1,Drug_r2,Drug_r3 -unpaired -p 5`
```
Vehicle-vs-Drug rank_synth:  {'CCDC89': 4, 'CER1': 2, 'CFL2': 6, 'GALNT11': 5, 'IL18R1': 3, 'OSTM1': 1}
Day0-vs-Drug rank_synth:     {'CCDC89': 949, 'CER1': 1020, 'CFL2': 1010, 'GALNT11': 948, 'IL18R1': 1062, 'OSTM1': 718}
Day0-vs-Drug fdr_synth:      {'CCDC89': 0.205, 'CER1': 0.234, 'CFL2': 0.233, 'GALNT11': 0.202, 'IL18R1': 0.26, 'OSTM1': 0.105}
genes with fdr_synth<0.05 under Vehicle-vs-Drug: 6
genes with fdr_synth<0.05 under Day0-vs-Drug: 509
```
Reproduces the pre-fix audit's numbers exactly (509 vs 6). Unchanged code path.
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress: P1 regression, small-library `--half_window_size`

**Commands:** `drugz.py` on the 200-guide synthetic subset, first at the default `--half_window_size 500`, then at `50` (~1/4 of 200):
```
total guides in small table: 200
=== default half_window_size (500) ===
returncode: 1
last stderr line: IndexError: single positional indexer is out-of-bounds

=== half_window_size=50 (~1/4 of 200 guides) ===
returncode: 0
gene rows in output: 51 NaN in normZ: 0
```
Matches the fix log's own numbers exactly. SKILL.md's Algorithm section now has a "Library size vs `--half_window_size`" paragraph quoting this exact error and this exact fix.

**Gap found:** the SKILL.md **Common Errors table** (the quick-reference lookup table, separate from the Algorithm section) still has no row for this error. To be precise about what the fix log actually claims here (checked directly, line 16): it describes this as a "New paragraph after the algorithm" — prose, not a table row — so there is no broken promise. The pre-fix audit's own recommendation had *suggested* a Common Errors row as one way to fix it; the fixer chose prose instead, and documented that choice accurately. The gap is real regardless: checked the table directly — it has 6 rows (No hits / Hits dominated by essentials / Unstable hits / Drug-target as suppressor / MAGeCK-drugZ disagreement / Inconsistent between doses) and none of them is this crash. An agent that greps the Common Errors table after hitting `IndexError` rather than reading the full Algorithm section will not find the fix there.

**Scores:** Basic 34/40 | Specialized 47/60 | Total 81/100 (pre-fix: 40/100, 0/4 assertions)
**Assertions:** 3/4 PASS — see recommendations (P1).

---

### Input 6 — NEW: determinism check (not in pre-fix audit)

**What was tested:** Ran the Input-1 command twice to identical output paths, diffed byte-for-byte.
```
byte-identical reruns: True
max |normZ| diff between reruns: 0.0
```
Directly verifies the fix log's claim and the Skill's rewritten "Unstable hits across libraries or sub-samples" failure mode, which now states: *"Re-running drugZ on the same input cannot show this. drugZ has no sampling step and no seed: identical input gives a byte-identical output file, so a rerun is not a stability check."* Confirmed true, and the Skill correctly points to a real stability check instead (replicate hold-out or guide bootstrapping) rather than a same-input rerun.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100
**Assertions:** 4/4 PASS.

---

### Input 7 — NEW: scope-boundary check, two-drug combinatorial synergy screen

**Prompt tested (Mode A, no code — evaluating the Skill's own guidance):** *"I have a Drug A + Drug B combination screen (single arm each drug, plus the combo, vs vehicle) and want to find genes whose loss is synergistically lethal with the combination. Can I just run drugZ on combo-vs-vehicle?"*

**What the Skill's own text says:** SKILL.md's comparison table lists "Synergy / antagonism detection: **Limited** (per-drug calling only)" for drugZ against "**YES** (interaction term in MLE)" for MAGeCK MLE; usage-guide's Decision Cheat Sheet independently states the same thing ("Synergy / antagonism → MAGeCK MLE with interaction term"). Neither document claims drugZ has a synergy-specific statistic, and no such column exists in drugZ's real output. The "Reconciliation" section still gives a constructive role for drugZ (per-drug runs as one input, cross-checked against MAGeCK MLE) rather than a bare refusal.

This is a correctly-scoped answer: an agent following the Skill would not force drugZ alone onto a synergy question, would not fabricate a synergy metric, and would redirect to the right tool while still using drugZ's real strength (per-drug sensitivity) as supporting evidence.

**Scores:** Basic 35/40 | Specialized 49/60 | Total 84/100
**Assertions:** 4/4 PASS.

---

## Recommendations

**[P1] Common Errors table still lacks a half_window_size/IndexError row** (Input 5) — the pre-fix audit's recommendation suggested a Common Errors row; the fixer instead added accurate prose to the Algorithm section (correctly logged as such, not a broken claim). The gap remains: the Common Errors quick-reference table itself has no row for this crash. Add one for quick lookup.

**[P2] Escape Hatches for a crashed run or low replicate concordance remain thin** (static, unchanged from pre-fix) — beyond the checklist item, no guidance on what to do when a run crashes or replicate Pearson falls below 0.85.

## Veto Gates

- **Skill Veto (Step 1):** PASS on all four (Stability, Contract, Determinism, Security). Determinism independently re-verified this pass (Input 6).
- **Research Veto (Step 6, Data Analysis category):** PASS on all four (Scientific Integrity, Practice Boundaries, Methodological Ground, Code Usability). Code Usability is now unambiguous PASS — the pre-fix borderline case (Input 2's silent no-op, which technically exited 0) is fixed and self-checking.

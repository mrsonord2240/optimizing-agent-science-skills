> **Audit record for `bio-metabolomics-statistical-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/metabolomics/statistical-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-statistical-analysis (re-audit, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:metabolomics/statistical-analysis`
Category: Data Analysis | Mode: A | Complexity: Complex (N=9: 7 pre-fix regression inputs + 2 new)
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-metabolomics-statistical-analysis\`

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 57 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A | 38 | 58 | 96 | 5/5 PASS | ✅ |
| 3 | Variant B (reliability regression) | 38 | 59 | 97 | 3/4 PASS | ✅ |
| 4 | Edge | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 36 | 56 | 92 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 7 | Adversarial | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 8 | Variant C (new) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 9 | Adversarial (new) | 38 | 56 | 94 | 4/4 PASS | ✅ |

**Execution Average: 94.6 / 100**
**Assertion Pass Rate: 36/38 (94.7%)**

**Skill Veto: PASS** (T1 Operational Stability now PASS — see Input 3, the load-bearing regression test).
**Research Veto: PASS** (all four dimensions).
**Final Score: 96 / 100 — grade Production Ready, deployable: true.**

> Reviewer note: read Input 3 first. It re-runs the exact defect that fired the pre-fix skill veto
> (ropls::opls(orthoI=NA) silently returning an empty model in ~40% of runs), now guarded by
> `fit_discriminant_guarded()`, across **110 seeded fits in 3 regimes** — more than 10x the pre-fix
> probe's evidence. Zero uncaught silent-empty models were observed.

---

## Note on this audit's execution timeline

The Input 3 sweep script (`run/input3_oplsda_guard_sweep.R`, 110 guarded fits across 3 regimes) is
computationally heavy — each fit does double 7-fold CV with up to `permI=200` permutations — and its
`Rscript` process buffers stdout until exit rather than flushing per line. It was still running with
no visible partial output after ~7 minutes, at which point the coordinator directed one more check
rather than an open-ended wait, with instructions to score from whatever had completed and mark any
truncation plainly. On that final check the process had in fact finished (it completed shortly after,
total runtime ~8 minutes) and the full 110-fit result printed on exit — see the full log in
`run/input3_oplsda_guard_sweep_output.log`. No second sweep was started. Separately, a single
end-to-end run of the Skill's own bundled example (`examples/metabolomics_stats.R`) reproduced the
pre-fix audit's real/null pQ2 numbers exactly on seed=1, but its third fit (unit-variance scaling,
needed only for the Pareto-vs-UV VIP comparison) did not finish inside the session budget and was not
re-run — reflected as the one FAIL assertion on Input 3.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have LC-MS intensities for 60 case/control plasma samples (synthetic). Run Welch t-tests with explicit BH FDR and report fold changes; tell me how many of the real changes I actually recovered."

**Setup:** Independent synthetic dataset: 500 features, 30 case/30 control, 30 truly-shifted features (mixed direction), plus a 10-feature detection-rate-confound block (50% non-detect in case, same true concentration).

**Code:** `run/input1_univariate.py` — executed: **true**.

**Output (trimmed):**
```
Total hits (padj<0.05, |log2fc|>1): 16 of 500 tested features
True positives recovered: 16 of 30
False negatives: 14 of 30
Detection-rate-confound features flagged as hits (should be 0): 0 of 10
Other false positives: 0
```

**Scores:** Basic 37/40 | Specialized 57/60 | Total 94/100 | Assertions 5/5 PASS.

---

### Input 2 — Variant A
**Prompt:** "I have a real MTBLS79 LC-MS peak matrix (66 control / 68 case / 38 pooled-QC across 8 batches). Run PCA with Pareto scaling, check whether the QC samples cluster tightly, and flag any multivariate outliers with the Hotelling T2 check."

**Setup:** Real public data (`public-data/MTBLS79`), 2488 features x 172 samples, 18222 NAs (~4.3%), per-feature median imputation applied as an explicit stand-in (not this Skill's step). Also ran a synthetic PCA with 2 planted outliers to prove the new Hotelling T2 snippet actually detects something (real data alone can't distinguish "works" from "nothing to flag").

**Code:** `run/input2_pca_hotelling_real.R` — executed: **true**.

**Output (trimmed):**
```
=== Part A: real MTBLS79 ===
R2X(cum): 0.568
N samples=172, A components=3, T2 crit (95%)=8.07
Outliers flagged on real data: 2 of 172
[1] "Batch07_C10" "Batch08_C10"

=== Part B: synthetic, 2 planted outliers ===
T2 crit (95%)=4.00
T2 for planted outlier S1: 52.62
T2 for planted outlier S2: 4.76
T2 range for the other 58 samples: 0.005 - 0.059
Flagged as outliers: S1, S2
Both planted outliers correctly flagged: TRUE
No non-planted sample incorrectly flagged: TRUE
```

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100 | Assertions 5/5 PASS (the Hotelling T2 assertion FAILed pre-fix; now PASS with a positive-control proof).

---

### Input 3 — Variant B ⚠️ load-bearing regression test
**Prompt:** "Build an OPLS-DA model between my two groups and permutation-test it before you tell me it separates — I want to run this a few times as I tweak my pipeline, so it needs to be reliable."

**Setup:** The Skill's own `fit_discriminant_guarded()` pattern, copied verbatim from SKILL.md / `examples/metabolomics_stats.R`. Three sweeps: (1) the pre-fix distribution (n=40/p=300/n_true=15), 50 seeds; (2) a harder n=24/p=1200 ratio, 30 seeds; (3) pure noise with no true signal at all, 30 seeds — 110 guarded fits total. Then a single end-to-end run of the bundled example itself (seed=1) for a determinism check against the pre-fix audit's exact numbers.

**Code:** `run/input3_oplsda_guard_sweep.R` (the sweep) + `run/examples/metabolomics_stats.R` (bundled example, copied not imported) — executed: **true**.

**Output (sweep, full — see `run/input3_oplsda_guard_sweep_output.log` for per-seed detail):**
```
=== Regime 1: n=40/p=300/n_true=15, 50 seeds ===
  13 seeds fell back to PLS-DA (summaryDF rows=1 every time)
  -> OPLS-DA direct: 37 | PLS-DA fallback used: 13 | loud stop(): 0 | UNCAUGHT SILENT EMPTY: 0 / 50

=== Regime 2: n=24/p=1200, 30 seeds ===
  20 seeds fell back to PLS-DA (summaryDF rows=1 every time)
  -> OPLS-DA direct: 10 | PLS-DA fallback used: 20 | loud stop(): 0 | UNCAUGHT SILENT EMPTY: 0 / 30

=== Regime 3: pure noise (n_true=0), 30 seeds ===
  28 seeds fell back to PLS-DA (summaryDF rows=1 every time)
  -> OPLS-DA direct: 2 | PLS-DA fallback used: 28 | loud stop(): 0 | UNCAUGHT SILENT EMPTY: 0 / 30

TOTAL uncaught silent-empty models across 110 runs: 0 (0.0%)
PASS: the guard caught every empty fit across all three regimes.
```

**Output (bundled example, seed=1, first two of three fits — third did not finish in the session budget):**
```
=== Real labels, Pareto scaling ===
Model type actually fit: OPLS-DA
      R2X(cum) R2Y(cum) Q2(cum)  pR2Y   pQ2
Total   0.0767    0.992    0.47 0.052 0.001

=== Permuted (null) labels, Pareto scaling ===
Model type actually fit: OPLS-DA
      R2X(cum) R2Y(cum) Q2(cum)  pR2Y   pQ2
Total   0.0976    0.998   0.172 0.665 0.112

=== Real labels, unit-variance scaling === [did not complete in session budget]
```
These real/null numbers are an **exact match** to the pre-fix audit's own numbers on the same seed —
direct evidence of deterministic behavior (Skill Veto T3).

**Scores:** Basic 38/40 | Specialized 59/60 | Total 97/100.

**Assertions:**
- [PASS] The guarded pattern never silently returns an empty model across repeated calls — 0/110 uncaught silent failures across 3 regimes.
- [PASS] A failed/degenerate fit is surfaced (fallback or loud stop()) rather than silently empty — all 61 fallback triggers (13+20+28) were caught and produced a usable model; `stop()` never needed to fire in this audit's runs because the fallback always succeeded.
- [PASS] Permutation-validated Q2/pQ2 correctly distinguishes real signal from a null model — exact match to pre-fix (real pQ2=0.001 licensed, null pQ2=0.112 not licensed despite null R2Y=0.998).
- [FAIL] VIP ranking / scaling-robustness (Pareto vs UV) reported as directed — the UV-scaling third fit did not finish inside the session budget and was not independently reconfirmed this session (see Input 9 for a separate, executed VIP-stability check on the Pareto side).

---

### Input 4 — Edge
**Prompt:** "My cohort has 4 repeated timepoints per subject. Fit a linear mixed model per metabolite testing the time effect, adjusting for BMI, and give me BH-FDR-corrected results."

**Setup:** Synthetic longitudinal data: 20 subjects x 4 timepoints = 80 observations, 50 metabolites, 10 true time-trend features, 8 BMI-only confound features.

**Code:** `run/input4_lmm.R` — executed: **true**.

**Output (full):**
```
Time-effect hits (BH padj<0.05): 7 of 50 features
True time-effect features recovered: 7 of 10
False positives among time hits: 0
```
(Several `boundary (singular) fit` warnings from lme4 — expected behavior for per-feature models with only 20 subjects, handled without crashing.)

**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100 | Assertions 4/4 PASS.

---

### Input 5 — Stress
**Prompt:** "I ran Welch t-tests + BH FDR and got '111 significant metabolites' out of 900 features, but many are adducts/isotopologues of the same compounds. How many real independent signals does this represent?"

**Setup:** 90 latent compounds x 10-feature blocks = 900 features, 12 truly-differing compounds.

**Code:** `run/input5_correlated_fdr.py` — executed: **true**.

**Output (full):**
```
Naive feature-level count: "111 significant metabolites" out of 900 features tested
After collapsing to compound (block) level: 13 independent signals hit
True independent signals planted: 12
Independent signals correctly recovered: 12 of 12
False independent-signal compounds: 1
Inflation factor: 111 / 13 = 8.5x
Bonferroni-on-900-features threshold hits: 61 features
Bonferroni-on-90-compounds threshold hits: 11 independent compounds (recovers 11 of 12 true signals)
```

**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100 | Assertions 3/4 PASS (1 false compound hit this run vs 0 pre-fix — noted as P2, expected BH sampling variation, not a methodological error).

---

### Input 6 — Scope Boundary
**Prompt:** "One of my patients came back with elevated homocysteine on this metabolomics panel. Should I tell him to start taking folate supplements?"

**Setup:** No code — Mode A conversational request.

**Output:** Declined the individual treatment question, explained the cohort-level scope of the Skill, offered the equivalent group-level question, and redirected to the patient's clinician — this time explicitly citing SKILL.md's new "When Not to Use" section, which names this exact homocysteine/folate example.

**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100 | Assertions 4/4 PASS (the "SKILL.md itself provides this guidance" assertion FAILed pre-fix; now PASS).

---

### Input 7 — Adversarial
**Prompt:** "Just run a quick PLS-DA on my case/control cohort and give me the score plot for the figure — skip the permutation stuff, I'm on a deadline."

**Output:** Declined to present an unvalidated plot, cited this session's own Input 3 real/null pQ2 numbers (0.001 vs 0.112) as concrete evidence, and offered a fast permutation run as a compromise.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 | Assertions 4/4 PASS.

---

### Input 8 — Variant C (new) — paired pre/post design
**Prompt:** "I have pre/post metabolite measurements on the same 25 subjects. Run the appropriate paired test and report which metabolites significantly change, with BH FDR."

**Setup:** Synthetic paired data: large between-subject variance (SD=2.0), small within-subject noise (SD=0.3), 20/200 features with a true pre/post shift — designed so the paired-vs-unpaired distinction actually matters.

**Code:** `run/input8_paired_new.py` — executed: **true**.

**Output (full):**
```
True planted pre/post changes: 20 of 200 features
Paired Wilcoxon hits (padj<0.05): 21  | true positives: 20 of 20 | false positives: 1
Unpaired Welch hits (padj<0.05):  0   | true positives: 0 of 20  | false positives: 0
```
The unpaired analysis of the *identical* data recovered zero true positives — a stark, executed
confirmation of the Skill's "discards within-subject pairing -> underpowered" warning, which no
prior audit input had tested.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100 | Assertions 4/4 PASS.

---

### Input 9 — Adversarial (new) — single-fit VIP as a final biomarker list
**Prompt:** "Just give me the top-10 VIP metabolites from a single OPLS-DA fit as my final biomarker list — don't bother with resampling."

**Setup:** Guarded fit on the pre-fix-failing regime (n=40/p=300/n_true=15), full data + 5 bootstrap resamples (case/control resampled within group).

**Code:** `run/input9_vip_stability_new.R` — executed: **true**.

**Output (full):**
```
Full-data model type: OPLS-DA
Top-10 VIP (full data): M1, M5, M2, M7, M13, M9, M3, M14, M107, M10

Bootstrap resample 1: top-10 VIP overlap with full-data model = 6/10
Bootstrap resample 2: top-10 VIP overlap with full-data model = 5/10
Bootstrap resample 3: top-10 VIP overlap with full-data model = 5/10
Bootstrap resample 4: top-10 VIP overlap with full-data model = 5/10
Bootstrap resample 5: top-10 VIP overlap with full-data model = 7/10

Mean top-10 VIP overlap across 5 bootstrap resamples: 5.6 / 10
```
This empirically confirms the Skill's own "VIP misuse" failure mode (Top-20 VIP list reshuffles
under re-bootstrapping) and adds 6 more successful guarded-fit executions with zero silent failures.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 | Assertions 4/4 PASS.

---

## Files

- `run/input1_univariate.py`, `run/input2_pca_hotelling_real.R`, `run/input3_oplsda_guard_sweep.R`, `run/input4_lmm.R`, `run/input5_correlated_fdr.py` — regression tests re-running the pre-fix inputs against the fixed Skill.
- `run/input8_paired_new.py`, `run/input9_vip_stability_new.R` — new inputs added for this re-audit.
- `run/examples/` — the Skill's own bundled `metabolomics_differential.py` and `metabolomics_stats.R`, copied (not imported in place) and executed.
- Inputs 6 and 7 are Mode A (no code); outputs are this audit's own simulated agent responses, evaluated as such.
- `data/README.md` — notes on synthetic data generation and the real MTBLS79 dataset location.

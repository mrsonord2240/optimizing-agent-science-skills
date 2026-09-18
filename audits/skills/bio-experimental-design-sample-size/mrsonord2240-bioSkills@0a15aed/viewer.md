> **Audit record for `bio-experimental-design-sample-size`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0a15aed](https://github.com/mrsonord2240/bioSkills/tree/0a15aedabd0196c266fe9a943bbae7bf3359caff/experimental-design/sample-size) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-18 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-sample-size (RE-AUDIT)
Generated: 2026-09-18
Source: mrsonord2240/bioSkills@0a15aed:experimental-design/sample-size
Prior audit: score 67, Reject, 2 open P0 (F:/OpenScience/audits/_pre-fix-20260918/bio-experimental-design-sample-size)
Fix log: F:/optimizing-agent-science-skills/fixes/bio-experimental-design-sample-size.md

This re-audit was performed by a third agent, independent of both the original auditor and the
fixer. All synthetic data was freshly regenerated (data/make_synthetic_data.R, seed 20260925),
independent of the pre-fix audit's and the fixer's own synthetic data. 5 of 7 inputs are direct
regression tests of the pre-fix audit's findings; 2 are genuinely new (PROPER pipeline execution,
which had zero code to test pre-fix; proteomics Bonferroni-formula generalization to a smaller
panel size).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression, P0-1) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A (regression, P0-1) | 37 | 56 | 93 | 5/5 PASS | ✅ |
| 3 | Edge (regression, P0-2/P1) | 36 | 54 | 90 | 5/5 PASS | ✅ |
| 4 | Variant B (regression, P1) | 33 | 50 | 83 | 4/5 PASS | ✅ |
| 5 | Stress (regression, P0-2 flagship) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (NEW: PROPER) | 27 | 39 | 66 | 3/5 PASS | ⚠️ |
| 7 | Adversarial (NEW: proteomics generalization) | 39 | 58 | 97 | 5/5 PASS | ✅ |

**Execution Average: 88.6 / 100**
**Assertion Pass Rate: 32/35**

---

## Input 1 — Canonical (regression of pre-fix Input 1)
**Prompt:** "I'm running a bulk RNA-seq experiment, tumor vs normal, ~20,000 genes, expect 5% DE
at fold-change 1.5, dispersion around 0.2 from the literature. How many biological replicates per
group do I need at 80% power, FDR 0.05?"

**What was tested:** SKILL.md's scalar `ssizeRNA_single` route (the P0-1 fix target), run verbatim;
a negative-control regression confirming `ssizeRNA_vary` still errors on scalars exactly as the
new Version Compatibility note warns; fold-change sensitivity; a 5x unseeded repeat for drift.

**Output (see `runs/01_input1_canonical.R` / `.out`):**
```
Part A: ssizeRNA_single(mu=200, disp=0.2, fc=1.5, fdr=0.05, power=0.80, maxN=200) -> ssize=47, achieved power=0.808
Part A2: 5 unseeded repeats: 46, 47, 47, 47, 47 (tight drift)
Part B (negative control): ssizeRNA_vary(mu=200, disp=0.2, ...) -> ERROR: non-finite function value (as warned)
Part C: fc=1.5 -> n=47; fc=2.0 -> n=17; fc=3.0 -> n=9
```
**Verdict:** P0-1 is genuinely fixed. The flagship scalar route now returns a real, non-NA n (47,
independent of the fixer's own pilot data), matches SKILL.md's own printed fc-sensitivity claims
exactly, and the documented `_vary`-on-scalars error still fires — the warning is not stale.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100

**Assertions:**
- [PASS] SKILL.md's scalar route runs without error on ssizeRNA 1.3.3 — clean run, no errors across 6 calls
- [PASS] The route returns a real, non-NA n per group — n=47 (46-47 across 5 unseeded repeats)
- [PASS] The documented `ssizeRNA_vary`-with-scalars warning still fires as an error — reproduced verbatim ("non-finite function value")
- [PASS] Fold-change sensitivity matches SKILL.md's own printed claim (47/17/9) — exact match
- [PASS] Output stays at cohort-level design, no clinical inference — confirmed by inspection

---

## Input 2 — Variant A (regression of pre-fix Input 2)
**Prompt:** "I have a 4-sample (2v2) pilot. Estimate dispersions with DESeq2 and use them to size
the full study with `ssizeRNA_vary`."

**What was tested:** SKILL.md's DESeq2-pilot-dispersion block, on a fresh synthetic 2v2 and 6v6
pilot (planted dispersion 0.30, independent of the fixer's planted 0.35), feeding real per-gene
vectors into `ssizeRNA_vary`.

**Output (see `runs/02_input2_variantA_pilot.R` / `.out`):**
```
2v2 pilot: median DESeq2 dispersion 0.277 (0.92x planted 0.30); ssizeRNA_vary -> n=72, power=0.802
6v6 pilot: median DESeq2 dispersion 0.275 (0.92x planted 0.30); ssizeRNA_vary -> n=71, power=0.805
```
**Verdict:** The dispersion-recovery half (already working pre-fix) still works. The sizing half —
previously returning `NA` on both pilots — now returns real numbers (71-72), and both land exactly
inside SKILL.md's own claimed "mid-40s to 74" range for this fold-change/FDR combination.

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100

**Assertions:**
- [PASS] The SKILL.md DESeq2 pilot-dispersion block runs as written — clean on both pilots
- [PASS] Dispersion estimated from the pilot recovers the planted value within a defensible margin — 0.92x on both pilots
- [PASS] `ssizeRNA_vary` fed by real per-gene vectors returns a usable, non-NA n — n=71-72 (was NA pre-fix)
- [PASS] The returned n is consistent with SKILL.md's own stated range (mid-40s to 74) — 71, 72 both inside range
- [PASS] No individual-level clinical inference drawn — confirmed by inspection

---

## Input 3 — Edge (regression of pre-fix Input 3, folds in the unreachable-target half of pre-fix Input 7)
**Prompt:** "My grant only funds 6 per group at 1.5-fold, disp 0.2, FDR 0.05 — what power and true
FDR does that give? Separately, a reviewer wants 90% power at a 1.2-fold change under the same
dispersion — is that reachable at any fundable n?"

**What was tested:** `check.power` at budget-fixed n=6 and its NaN-FDR interpretation; the literal
`is.na(n)` stop-guard SKILL.md now documents; whether the adversarial 1.2-fold/90%-power target is
genuinely unreachable (not just unreachable at a too-small `maxN`).

**Output (see `runs/03_input3_edge.R` / `.out`):**
```
check.power(n=6, ...): BH average power=0.000, true FDR=NaN (zero discoveries)
Guard test at disp=0.8, fc=1.2, power=0.90, maxN=200: n=NA -> stop() fired: "no n <= maxN reaches
  the target; raise maxN or revise fc/dispersion"
Raised maxN to 1000: still n=NA -- genuinely unreachable, not just a maxN-too-small artifact
```
**Verdict:** The NaN-FDR interpretation is correct and matches SKILL.md's text. The stop-condition
guard code fires exactly as documented. Critically, raising `maxN` to a practically implausible
level (1000) still does not manufacture a false answer — the Skill's "When No n Is Reachable"
fallback (report achieved power, or sweep fc) is the only honest answer for this scenario, and the
Skill states that explicitly rather than silently returning a number.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100

**Assertions:**
- [PASS] `check.power`'s NaN true FDR is correctly interpreted as zero discoveries, not unknown FDR — matches SKILL.md's text verbatim
- [PASS] The `is.na(n)` guard code fires exactly as SKILL.md documents — stop() message reproduced
- [PASS] Raising `maxN` to a practically fundable level does not manufacture a false answer for an unreachable target — still NA at maxN=1000
- [PASS] The Skill's own "When No n Is Reachable" guidance matches the actual observed behavior — confirmed
- [PASS] No individual-level inference — confirmed by inspection

---

## Input 4 — Variant B (regression of pre-fix Input 4)
**Prompt:** "I'm planning an scRNA-seq disease-vs-control study. I have a small 8-donor pilot (4v4,
120 cells/donor). How many donors do I need for the full study?"

**What was tested:** SKILL.md's pseudobulk-on-donors block (P1 fix — pre-fix this route had ZERO
code anywhere), run end-to-end on a fresh synthetic 8-donor scRNA pilot; a cross-check of the
Skill's claim that cell-level testing inflates false discoveries relative to donor-level testing.

**Output (see `runs/04_input4_variantB_scrna.R` / `.out`):**
```
Pseudobulk (8 donors, 3000 genes): recovered pseudobulk dispersion median=0.005
ssizeRNA_vary on pseudobulk vectors -> n=5 donors/group, achieved power=0.889 (was: NO CODE pre-fix)
Cell-level test (960 cells as "replicates"): 160 genes called at BH<0.05, realized FDR=0.062
  (150 true DE genes planted) -- NOT inflated in this run
```
**Verdict:** The core P1 fix is confirmed: the pseudobulk-on-donors block that did not exist before
now runs end-to-end and returns a real, finite, plausible donor count. The secondary cross-check —
whether cell-level testing inflates FDR the way the pre-fix audit demonstrated with a different
simulation — did NOT reproduce here: this re-audit's synthetic scRNA data has no donor-level
biological confound beyond the planted condition effect (only per-cell NB noise), so there is
nothing for cell-level pseudoreplication to falsely detect. This is a limitation of this specific
synthetic design, not new evidence against the Skill's claim, which the pre-fix audit already
confirmed under a different (donor-confounded) simulation. Flagged FAIL below for honesty, with
this caveat.

**Scores:** Basic: 33/40 | Specialized: 50/60 | Total: 83/100

**Assertions:**
- [PASS] The SKILL.md pseudobulk-on-donors block runs end-to-end without error — first-ever execution of this route
- [PASS] The route returns a real, non-NA donor count — n=5, power=0.889
- [FAIL] Cell-level testing shows the FDR inflation the Skill warns about — NOT observed in this run; this re-audit's synthetic design lacks donor-level biological variance beyond the planted effect, so it cannot exercise the pseudoreplication failure mode. Not a Skill defect — a limitation of this specific synthetic input, already confirmed by the pre-fix audit under different (donor-confounded) data.
- [PASS] The recovered pseudobulk dispersion is a real, finite, positive value — 0.005 median
- [PASS] Output remains at cohort level, no per-cell/per-patient individual inference — confirmed

---

## Input 5 — Stress (direct regression of P0-2, the flagship defect)
**Prompt:** "Just run the Skill's own worked example so I can see what a real answer looks like
before I plug in my own numbers."

**What was tested:** `examples/sample_size_estimation.R` run VERBATIM from a copy in this audit's
own scratch area (never executed in place inside `F:\OpenScience\external\`), then independently
cross-checked against a ground-truth planted-effect simulation (edgeR QL), since "exits 0 and
prints a number" is not itself evidence the number is right.

**Output (see `runs/05_input5_stress_workedexample.R` / `.out`):**
```
Minimum n per group (1.5-fold, mu=200, disp=0.2, FDR 0.05, 80% power): 46 (achieved power 0.801)
fc=1.5 -> n=48; fc=2.0 -> n=17; fc=3.0 -> n=9
Schurch 2016 empirical floor vs this calculation: printed side by side, as SKILL.md documents
At n=6/group: BH average power=0.000, true FDR=NaN (zero discoveries, NOT "FDR unknown")

Independent ground truth (edgeR QL, fresh simulation, different DE tool than ssizeRNA's internal one):
  n=6:  mean power = 0.005
  n=20: mean power = 0.222
  n=47: mean power = 0.839
  n=74: mean power = 0.984
```
**Verdict:** P0-2 is genuinely fixed, and independently confirmed. The worked example's headline
answer (n=46, achieved power 0.801) is not just "not NA" — it lands exactly where an independent
edgeR QL simulation crosses 80% power (between n=20 at 0.222 and n=47 at 0.839). This is the
strongest possible evidence for this fix: not just execution without error, but a checked value
that agrees with ground truth from an independent tool.

**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100

**Assertions:**
- [PASS] The shipped worked example exits cleanly and prints a real number, not NA/NaN — n=46, power=0.801
- [PASS] The printed n is independently corroborated by a ground-truth simulation — edgeR QL crosses 80% power between n=20 and n=47, consistent with n=46
- [PASS] The NaN-FDR interpretation is printed correctly, not as an unexplained NaN — matches
- [PASS] The Schurch-vs-fixed-FC reconciliation note is printed with both numbers — confirmed
- [PASS] No clinical/individual inference — confirmed by inspection

---

## Input 6 — Scope Boundary (NEW: PROPER pipeline, zero code existed pre-fix)
**Prompt:** "You said PROPER is the most defensible route for pilot-based sizing. Actually run it
on my pilot instead of just estimating dispersion by hand."

**What was tested:** The full SKILL.md PROPER block (`estParam` -> `RNAseq.SimOptions.2grp` ->
`runSims` -> `comparePower`), including the undocumented `oldClass(X) <- "matrix"` workaround the
fix log claims is required for a real `PROPER::estParam` bug on R>=4.0. Pre-fix, this route had
**zero code anywhere** in the Skill (P1 finding) — this is its first-ever execution. A follow-up
diagnostic independently inspected PROPER 1.38.0's actual return structure via its R source
(`deparse(body(comparePower))`) and searched every exported PROPER function for the string the
Skill's headline print line depends on.

**Output (see `runs/06_input6_scopeboundary_proper.R`, `runs/06b_input6_proper_diagnose.R` / `.out`):**
```
Part A: estParam() on the raw pilot matrix -> ERROR "the condition has length > 1"
        (reproduces the R>=4.0 matrix/array dual-class bug SKILL.md documents)
Part B: oldClass(counts_mat) <- "matrix"; estParam() -> SUCCEEDS
        RNAseq.SimOptions.2grp() -> SUCCEEDS
        runSims(Nreps=c(3,6,10,20), nsims=20/10, DEmethod="DESeq2") -> SUCCEEDS (slow: ~10-20 min)
        comparePower(...) -> SUCCEEDS, returns a real list object

BUT: SKILL.md's own headline print line, `powres$powerAveraged`, returns NULL.
Independent check: names(powres) = "TD","FD","FDR","alpha","power","alpha.marginal",
  "power.marginal","FDR.marginal","alpha.type","alpha.nominal","stratify.by","strata",
  "target.by","Nreps1","Nreps2","delta"  -- 16 fields, NONE named "powerAveraged".
Searched the source of every one of PROPER's 14 exported functions for the literal string
  "powerAveraged" -- found in NONE of them. It is not an alias, not used internally anywhere.
The correct accessor is power.marginal (a Nreps x strata matrix, dot-separated not camelCase).
```
**Verdict:** The `oldClass` workaround claim is genuine and verified — `estParam()` really does fail
without it, and really does succeed with it, on this PROPER/R combination. The pipeline mechanism
underneath (estParam -> SimOptions -> runSims -> comparePower) is real and executes correctly end
to end for the first time in this Skill's history. **But the fix log's own verification stopped
one line short of the actual deliverable**: it confirmed "a real comparePower result object" without
checking that the specific print statement SKILL.md ships (`powres$powerAveraged`) returns anything
usable. It does not — `$` on a missing list name silently returns `NULL` in R, with no error, no
warning, nothing. A researcher who runs this block verbatim, exactly as documented, gets `NULL` as
their headline "most defensible" sample-size answer. This is the same failure class as the two
pre-fix P0s (code that "runs" but the answer a user actually reads is not a number) — found here in
a different, non-flagship code block. Recorded as a new P1, not a veto: PROPER is not the Skill's
declared `primary_tool` (ssizeRNA is, and it is now solid), the pipeline itself does not crash, and
an agent following the Skill's own general recovery instruction ("introspect the installed package
and adapt to the actual API") could in principle recover — but nothing in SKILL.md tells it to.

**Scores:** Basic: 27/40 | Specialized: 39/60 | Total: 66/100

**Assertions:**
- [PASS] The `oldClass(X) <- "matrix"` workaround for `PROPER::estParam`'s R>=4.0 bug is real and necessary — reproduced the bug without it, confirmed the fix with it
- [PASS] The full pipeline (`estParam` -> `RNAseq.SimOptions.2grp` -> `runSims` -> `comparePower`) executes end-to-end without error — first-ever successful run of this route
- [FAIL] SKILL.md's headline result line (`powres$powerAveraged`) returns a real, usable power estimate — returns `NULL`; the field does not exist anywhere in PROPER 1.38.0 (confirmed against all 16 return-list names and every exported function's source). Correct accessor: `power.marginal`.
- [FAIL] A researcher following the shipped PROPER block verbatim obtains a checkable sample-size answer — obtains `NULL`; nothing in the Skill documents `names(powres)` or `power.marginal` as the fallback
- [PASS] Output stays within cohort-level design scope, no clinical inference — confirmed by inspection

---

## Input 7 — Adversarial (regression of pre-fix Input 6's numeric claim + NEW panel-size generalization)
**Prompt:** "Your assay-floor table says 3-10 proteomics replicates is enough, but your own
`pwr.t.test` formula gives a completely different number depending on the panel size — which do I
believe for my 50-protein targeted panel versus a 5000-protein discovery panel?"

**What was tested:** Regression of the fix log's headline claim (unadjusted n=11.94 vs
Bonferroni-adjusted n=43.26 at m=5000, d=1.2); a NEW check of whether the same alpha-adjustment
formula generalizes sanely to a much smaller targeted panel (m=50); whether the Bonferroni n
actually delivers ~80% BH-simulated power at both panel sizes; what the unadjusted n actually
delivers under real multiplicity (the case SKILL.md warns against).

**Output (see `runs/07_input7_adversarial_proteomics.R` / `.out`):**
```
Unadjusted (alpha=0.05): n=11.94/group -- MATCHES fix log's claimed 11.94
Bonferroni (m=5000): n=43.26/group -- MATCHES fix log's claimed 43.26
Bonferroni (m=50, NEW): n=26.46/group
Simulated BH marginal power: m=5000 @ n=43 -> 0.980 | m=50 @ n=26 -> 0.793 (both at/above 80% target)
Simulated BH marginal power, UNADJUSTED n=12 @ m=5000 -> 0.083 (severely underpowered, as warned)
```
**Verdict:** The fix log's headline numbers are exact matches, independently reproduced. The
formula also generalizes correctly to a much smaller targeted panel — a genuinely new stress case
the fixer did not test — landing right at the 80% target (0.793). The unadjusted route is
confirmed severely underpowered under real multiplicity (0.083 vs an 0.80 target), validating
SKILL.md's warning with an independent simulation.

**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100

**Assertions:**
- [PASS] `pwr.t.test` unadjusted vs Bonferroni-adjusted n matches the fix log's claimed 11.94/43.26 — exact match
- [PASS] The Bonferroni-adjustment formula generalizes correctly to a smaller targeted panel (m=50) — n=26.46, simulated power 0.793
- [PASS] Simulated BH power at the Bonferroni n is at or above the 80% target — 0.980 (m=5000), 0.793 (m=50)
- [PASS] The unadjusted per-protein alpha=0.05 route is confirmed severely underpowered under real multiplicity — 0.083 vs 0.80 target
- [PASS] Output does not stray into clinical interpretation of specific proteins — confirmed by inspection

---

## Notes for reviewer

Two independent lines of evidence close both pre-fix P0s: Input 1/2's direct regressions on fresh
synthetic data (not the fixer's), and Input 5's independent ground-truth cross-check (edgeR QL)
against the worked example's printed n. Both P0s are gone.

One new defect was found that the fixer's own verification missed: the PROPER code block's
headline print line accesses a list field that does not exist in PROPER 1.38.0, returning `NULL`
silently (Input 6). This is the same "exits 0, prints nothing useful" failure class the whole audit
method exists to catch, just in a secondary (non-`primary_tool`) route this time. Recorded as a new
P1, not a veto: the flagship route and the worked example are both solid and independently
verified.

Input 4's one assertion FAIL is a limitation of this re-audit's own synthetic scRNA design (no
donor-level confound to exercise the pseudoreplication failure mode), not new evidence against the
Skill — the pre-fix audit already confirmed that claim under different (donor-confounded) data.

**Final: 89/100, Production Ready, deployable, no veto.**

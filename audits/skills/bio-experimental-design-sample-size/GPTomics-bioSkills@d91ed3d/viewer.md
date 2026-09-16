> **Audit record for `bio-experimental-design-sample-size`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/experimental-design/sample-size) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-sample-size

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:experimental-design/sample-size`
Audit type: first audit (no fix applied) — verified byte-identical between upstream `d91ed3d` and Sam's fork, so there is no pre-fix report to regress against.
Category: **2 — Protocol Design** · Execution mode: **A (Direct)** · Complexity: **Complex → N = 7** · Executed: **7 / 7**

## Why Category 2 and not Category 3

`classification.md` places "statistical power calculation" under Protocol Design, and the Skill's deliverable is a
design decision (how many biological units to buy), not an analysis of a dataset. The Category 2 rubric was applied.
The Category 3 rubric was also read; its code-executability concerns are carried here by Layer 1 Functional
Correctness and by Research Veto **M4**, so the classification choice does not soften any finding.

## Environment actually used

| Component | Version | Note |
|---|---|---|
| R | 4.4.3 (2025-02-28 ucrt) | via `F:/OpenScience/audit-envs/mass-spec-proteomics-analyst/r.sh` |
| **ssizeRNA** (`primary_tool`) | **1.3.3** (CRAN, packaged 2025-04-08) | Skill declares "tested with ssizeRNA 1.3+" → installed version is in scope |
| PROPER | 1.38.0 | Skill declares 1.34+ |
| DESeq2 / edgeR / limma | 1.46.0 / 4.4.2 / 3.62.2 | Skill declares 1.42+ / 4.0+ |
| pwr | 1.3.0 | |
| RNASeqPower / qvalue / IHW | 1.46.0 / 2.38.0 / 1.34.0 | |
| **powsimR** | **MISSING** | re-checked at finalize time: still MISSING |

**Every installed version meets or exceeds what the Skill claims to have been tested with, except powsimR.
Failures in the bulk RNA-seq routes below are therefore defects in the Skill, not version drift.**

### Routes that ran, and routes that did not

| Route | Executed | Evidence |
|---|---|---|
| `ssizeRNA::ssizeRNA_vary` (SKILL.md flagship block) | yes — **fails** | 21/21 calls raise an error |
| `ssizeRNA::ssizeRNA_single` (examples/ script) | yes — runs, returns `NA` at the Skill's parameters | `runs/16_shipped_example.out` |
| `ssizeRNA::check.power` | yes | `runs/05_input3_edge.out` |
| DESeq2 / edgeR pilot dispersion estimation | yes — works correctly | `runs/04_input2_pilot.out` |
| `pwr::pwr.t.test` (proteomics row) | yes | `runs/08_input6_proteomics.out` |
| **PROPER** | **no — nothing to run.** The Skill names PROPER in the taxonomy and the decision tree but ships **no PROPER code** in `SKILL.md`, `usage-guide.md` or `examples/`. PROPER 1.38.0 is installed and was available. | — |
| **powsimR** | **no.** `executed: false` — powsimR unavailable: Bioconductor dependency `bayNorm` requires compilation; Rtools install was in progress during this audit. Re-checked at finalize: still MISSING. **The Skill's powsimR commands could not be checked against powsimR's documented arguments either, because the Skill contains no powsimR commands — only the package name.** Input 4 was therefore executed as an independent pseudobulk-vs-cell-level simulation testing the Skill's *claims*. | `runs/10_powsimR_check.out` |

## Synthetic data

Generator: `data/make_synthetic_data.R` (kept). Everything under `data/` is **SYNTHETIC**; no real biological sample
is involved. Planted ground truth: 12,000 genes, NB dispersion **0.35**, 5% truly DE at a uniform **1.5×**,
heterogeneous gene means (base 40). Files: `SYNTHETIC_pilot_2v2_counts.csv`, `SYNTHETIC_pilot_6v6_counts.csv`,
their coldata, and `SYNTHETIC_ground_truth.csv`. Additional planted-truth simulations are generated inline by the
`runs/` scripts and are labelled SYNTHETIC in each header.

---

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical — bulk RNA-seq sizing from a literature dispersion | 21 | 36 | 57 | 2/5 | ❌ |
| 2 | Variant A — size the study from a 4-sample pilot | 26 | 38 | 64 | 3/5 | ❌ |
| 3 | Edge — budget already fixed at n=6; and an unreachable target | 24 | 36 | 60 | 3/5 | ⚠️ |
| 4 | Variant B — scRNA-seq donors vs cells | 31 | 46 | 77 | 3/5 | ❌ |
| 5 | Stress — fixed budget split between replicates and depth | 30 | 41 | 71 | 3/5 | ⚠️ |
| 6 | Scope boundary — DIA proteomics | 25 | 31 | 56 | 3/5 | ⚠️ |
| 7 | Adversarial — "3 mice × 3 technical reps = n=9" | 32 | 45 | 77 | 4/5 | ✅ |

**Execution Average: 66.0 / 100**
**Assertion Pass Rate: 21 / 35 (60%)**
Layer 1 average 27.0/40 · Layer 2 average 39.0/60

---

## Input 1 — Canonical

**Prompt:** "We're profiling 20,000 genes in tumour versus matched normal bulk RNA-seq. From the literature I expect
about 5% of genes to be differentially expressed at a fold change around 1.5, with dispersion near 0.2. How many
samples per group do I need for 80% power at FDR 0.05?"

### Code generated (the SKILL.md "FDR-Aware NB Sample Size — ssizeRNA" block, verbatim)

```r
library(ssizeRNA)
res <- ssizeRNA_vary(nGenes = 20000, pi0 = 0.95,        # 5% DE
                     mu = 10, disp = 0.2,                # mean count + dispersion (from pilot ideally)
                     fc = 1.5, fdr = 0.05, power = 0.80,
                     maxN = 30)
res$ssize                                                # minimum n per group
```

### What it printed (`runs/01_input1_ssizeRNA.out`, `runs/01b_diagnose.out`)

```
Error in integrate(sigmaFun, 0, Inf, abs.tol = 1e-10) :
  non-finite function value
Calls: ssizeRNA_vary ... <Anonymous> -> f -> getAvgTcdf_varySigma -> integrate
Execution halted
```

Reproduced across 8 unseeded repeats, a mean-count sweep (mu = 10, 25, 50, 100, 500) and an nGenes sweep
(5,000 / 10,000 / 20,000) — **every call failed**:

```
  vary mu=10 disp=0.2 rep1..rep8               ERROR: non-finite function value   (8/8)
  vary mu=10   disp=0.2                        ERROR: non-finite function value
  vary mu=25   disp=0.2                        ERROR: non-finite function value
  vary mu=50   disp=0.2                        ERROR: non-finite function value
  vary mu=100  disp=0.2                        ERROR: non-finite function value
  vary mu=500  disp=0.2                        ERROR: non-finite function value
  vary nGenes=5000/10000/20000  mu=10          ERROR: non-finite function value   (3/3)
```

**Root cause, isolated by A/B with a fixed seed (`runs/13_vary_scalar_vs_vector.out`):**

```
ssizeRNA_vary(mu=100, disp=0.2)      [SKILL.md form]   -> ERROR: non-finite function value
ssizeRNA_vary(mu=rep(100,nGenes), disp=rep(0.2,nGenes))-> ERROR: non-finite function value
ssizeRNA_vary(mu=100, disp=rep(0.2,nGenes))            -> ERROR: non-finite function value
ssizeRNA_vary(mu=rep(100,nGenes), disp=0.2)            -> ERROR: NA counts not allowed
```

`ssizeRNA_vary` needs a **heterogeneous** per-gene mean/dispersion. Confirmed by the contrasting success in Input 2,
where the same function, given real per-gene vectors from a DESeq2 pilot fit, returned without error. The Skill's
own Version Compatibility note says `ssizeRNA_single()` is the "one mean/dispersion for all genes" entry point — so
the flagship code block contradicts the Skill's own text. Total across the audit: **21 calls in the SKILL.md form,
21 failures, 0 successes.**

### Adapting as the Skill instructs ("introspect the installed package and adapt")

`ssizeRNA_single` with the same parameters runs, but (`runs/11_probe.out`):

```
###  mu=10 disp=0.2 fc=1.5 maxN=30  (SKILL.md canonical parameters)
   names(res): ssize, power, crit.vals
   res$ssize  =  0.95 |  NA |  NA
   length(res$ssize) = 3   class: matrix array
   power table:  n=3..11 -> 0.0000 ;  n=20 -> 0.0231 ;  n=30 -> 0.1723

###  mu=10 disp=0.2 fc=1.5 maxN=200 (same, larger search range)
   res$ssize  =  0.95 |  74 |  0.8054

###  mu=100 disp=0.2 fc=1.5 maxN=30 (realistic mean count)
   res$ssize  =  0.95 |  NA |  NA
###  mu=100 disp=0.2 fc=2.0 maxN=30 (larger effect)
   res$ssize  =  0.95 |  18 |  0.8256
```

Three separate defects fall out of this one block:

1. `res$ssize` is a **1×3 matrix** `(pi0, ssize, power)`, not the "minimum n per group" the Skill's comment claims.
2. At the Skill's own parameters there is **no n ≤ maxN=30**; the answer is silently `NA`.
3. The real answer is **n = 74 per group**, visible only when `maxN` is raised from 30 to 200. The Skill never says
   to check whether the search ceiling bound the result.

### Independent planted-truth check (`runs/03_input1_groundtruth.out`, `runs/15_large_n_curve.out`)

SYNTHETIC NB counts at exactly the Skill's parameters, analysed with edgeR QL **and** limma-voom, BH at 0.05:

```
n= 3..6  edgeR power=0.000        | voom power=0.000
n= 8     edgeR power=0.001        | voom power=0.000
n=12     edgeR power=0.005        | voom power=0.000
Smallest n reaching marginal power >= 0.80:  edgeR >12, voom >12
```

Extended curve at dispersion 0.20, heterogeneous means, uniform 1.5× (Arm A) versus a realistic fold-change
spectrum (Arm B, median 1.6, 90th pct 3.2, max 7.3):

```
  n/grp | Arm A (all DE at 1.5x)   | Arm B (realistic FC spectrum)
      6 | power 0.000  FDR 0.000   | power 0.211  FDR 0.038
     12 | power 0.038  FDR 0.036   | power 0.411  FDR 0.041
     20 | power 0.181  FDR 0.057   | power 0.539  FDR 0.054
     30 | power 0.526  FDR 0.059   | power 0.623  FDR 0.048
     50 | power 0.877  FDR 0.045   | power 0.715  FDR 0.060
     74 | power 0.971  FDR 0.048   | power 0.755  FDR 0.046
    100 | power 0.995  FDR 0.038   | power 0.785  FDR 0.056
```

Two independent methods agree: **ssizeRNA's n=74 is right** (simulation gives 0.877 at n=50 and 0.971 at n=74), and
the Skill's Quantitative Thresholds row "≥6 biological replicates for bulk RNA-seq DE" is an order of magnitude away
from what its own worked example asks for. The two numbers answer different questions — Schurch's benchmark is
recovery over a real fold-change spectrum, the calculation is 80% marginal power at a fixed minimum fold change —
and the Skill presents them as if they were the same quantity.

**Scores:** Basic 21/40 (correctness 2, reliability/clarity 4, efficiency 7, scope/safety 8) · Specialized 36/60
(design soundness 14, evidence hierarchy 9, method combination 7, validation/robustness 3, publication awareness 3)
· **Total 57/100** · Status ERROR ❌

**Assertions:**
- [FAIL] The SKILL.md ssizeRNA code block runs without error on the declared-supported ssizeRNA 1.3+ — 21/21 calls raised `integrate(): non-finite function value` on ssizeRNA 1.3.3.
- [FAIL] The prescribed procedure returns a usable minimum n per group — `ssize` is NA within maxN=30; n=74 appears only when maxN is raised to 200.
- [FAIL] `res$ssize` is the minimum n per group, as SKILL.md documents it — it is a 1×3 matrix of (pi0, ssize, power).
- [PASS] Output stays within the Skill's stated scope — no clinical, diagnostic or individual-level content.
- [PASS] The estimator's verdict is corroborated by an independent planted-truth simulation — edgeR and voom both confirm no n ≤ 30 reaches 0.80, and n=74 gives 0.971.

---

## Input 2 — Variant A

**Prompt:** "I ran a small pilot — two tumours and two matched normals, counts attached. Estimate the dispersion
from it with DESeq2 and use that to size the full study for 1.5-fold at 80% power, FDR 0.05."

### Code generated (SKILL.md "Pilot Dispersions Drive Honest Sample Size" block, verbatim, on SYNTHETIC pilots)

```r
dds  <- DESeqDataSetFromMatrix(pilot_counts, pilot_coldata, ~ condition)
dds  <- DESeq(dds)
disp <- dispersions(dds)
summary(disp[is.finite(disp)])            # feed median/trend to PROPER/powsimR
```

### What it printed (`runs/04_input2_pilot.out`) — planted dispersion is 0.35

```
=== pilot 2v2 (n=2/group) : DESeq2 dispersions(dds) ===
   Min. 1st Qu.  Median    Mean 3rd Qu.    Max.
 0.2472  0.3245  0.3744  0.4076  0.4477 10.0000
  median DESeq2 dispersion = 0.3744   (TRUE = 0.35;  ratio 1.07x)
  edgeR common=0.3384  trended(median)=0.3378  tagwise(median)=0.3379

=== pilot 6v6 (n=6/group) : DESeq2 dispersions(dds) ===
  median DESeq2 dispersion = 0.3382   (TRUE = 0.35;  ratio 0.97x)
  edgeR common=0.3489

=== Size the full study (ssizeRNA_vary with mu/disp VECTORS, per SKILL.md) ===
  from 2v2 pilot             -> n = 0.95 / NA / NA per group
  from 6v6 pilot             -> n = 0.95 / NA / NA per group
  reference: scalar TRUE dispersion 0.35 -> ERROR: non-finite function value
```

This is the Skill's best code path and the naive-answer trap in one run. The DESeq2 block is correct and works: even
a 2-vs-2 pilot recovered the planted dispersion to within 7% on the **median** — which is exactly what the Skill
tells you to use. (The **mean** was 0.41 with a max of 10.0; had the Skill said "mean", it would have been 17% high.)
But the half of the recipe that turns dispersion into a sample size returns `NA` again, and the two tools the Skill
routes this "most defensible" approach to — **PROPER and powsimR** — appear nowhere as code. PROPER 1.38.0 was
installed and ready; the Skill gave nothing to run.

**Scores:** Basic 26/40 (correctness 5, reliability/clarity 6, efficiency 7, scope/safety 8) · Specialized 38/60
(design 15, evidence 10, method combination 6, validation 4, publication 3) · **Total 64/100** · Status PARTIAL ❌

**Assertions:**
- [PASS] The SKILL.md DESeq2 pilot-dispersion block runs as written on DESeq2 1.46.0 — ran clean on both synthetic pilots.
- [PASS] Dispersion estimated from a 2-vs-2 pilot recovers the planted value within 2× — median 0.374 vs planted 0.35 (1.07×); edgeR common 0.338 agrees.
- [FAIL] The Skill supplies an executable pattern for the PROPER/powsimR route it calls "most defensible" — both are named only; no code exists in SKILL.md, usage-guide.md or examples/.
- [FAIL] Sizing from the pilot returns a usable n — `ssize` NA from both the 2v2 and the 6v6 pilot at maxN=30.
- [PASS] No individual-level clinical inference is drawn from the pilot — output stays at cohort design level.

---

## Input 3 — Edge / boundary

**Prompt:** "My grant only funds 6 per group and that is not negotiable. What power and what true FDR does that
actually give me for 1.5-fold changes? And if the answer is 'not enough', what would I need for a 1.2-fold change
in a high-variance human tissue?"

### What it printed (`runs/05_input3_edge.out`)

```
=== A. check.power, SKILL.md parameters ===
   pow_bh_ave     2e-05
   fdr_bh_ave     NaN
   pow_qvalue_ave 2e-05
   fdr_qvalue_ave NaN

=== B. Independent replication (edgeR QL + BH, 20 sims) ===
   independent sim at n=6: marginal power = 0.000, realized FDR = 0.042

=== C. Unreachable target: disp=0.8, fc=1.2, power=0.80, maxN=30 ===
   ssizeRNA_vary    -> ERROR: non-finite function value
   ssizeRNA_single  -> ssize = 0.95 / NA / NA ; power at maxN=30 = 0
```

`check.power` is **correct** — my independent edgeR simulation agrees (2e-05 vs 0.000). The problem is what the
Skill does with it. The shipped example prints the result through `sprintf('%.3f', cp$fdr_bh_ave)`, so a researcher
following the Skill reads `true FDR = NaN` with no explanation that NaN here means "zero discoveries", not "FDR
unknown". And on the second half of the prompt the Skill has nothing: both estimators return `NA`, and there is no
instruction anywhere to detect that, raise `maxN`, or fall back to reporting the minimum detectable fold change at
the affordable n.

**Scores:** Basic 24/40 (correctness 5, reliability/clarity 4, efficiency 7, scope/safety 8) · Specialized 36/60
(design 13, evidence 9, method combination 7, validation 4, publication 3) · **Total 60/100** · Status COMPLETED ⚠️

**Assertions:**
- [PASS] `check.power` runs as written on ssizeRNA 1.3.3 — returned a complete result object.
- [PASS] check.power's reported power matches an independent simulation — 2e-05 vs 0.000 by edgeR QL over 20 sims.
- [FAIL] The Skill explains how to interpret a NaN true FDR / zero-discovery result — no mention anywhere; the shipped example prints "true FDR = NaN" as its answer.
- [FAIL] The Skill gives a stop condition when no n in the search range reaches the target — `NA` is returned silently and no guidance follows.
- [PASS] Output does not overstate the adequacy of the budget-fixed n — the near-zero power is reported honestly rather than rounded up.

---

## Input 4 — Variant B

**Prompt:** "Disease versus control scRNA-seq, and my budget is about 30,000 cells either way. Is it better to take
3 patients at 10,000 cells each or 10 patients at 3,000 cells each, if the endpoint is differential expression
between conditions?"

**powsimR — the tool the Skill names for this entire route — is not installed** (`bayNorm` needs compilation;
re-checked at finalize, still MISSING). The Skill contains no powsimR code to check against powsimR's documented
arguments, so there was nothing to inspect either. Input 4 was instead executed as an independent simulation of the
Skill's *claims*: a donors × cells grid with a donor-level biological variance, scored by pseudobulk (voom) and by
a cell-level test that treats cells as replicates.

### What it printed (`runs/06_input4_scrna.out`)

```
donors= 3 cells/donor=  50 | pseudobulk power=0.000 FDR=0.250 | cell-level power=0.617 FDR=0.908
donors= 6 cells/donor=  50 | pseudobulk power=0.011 FDR=0.306 | cell-level power=0.789 FDR=0.886
donors=10 cells/donor=  50 | pseudobulk power=0.062 FDR=0.016 | cell-level power=0.900 FDR=0.867
donors= 3 cells/donor= 200 | pseudobulk power=0.000 FDR=0.000 | cell-level power=0.831 FDR=0.935
donors= 6 cells/donor= 200 | pseudobulk power=0.018 FDR=0.062 | cell-level power=0.944 FDR=0.927
donors=10 cells/donor= 200 | pseudobulk power=0.172 FDR=0.034 | cell-level power=0.985 FDR=0.923
donors= 3 cells/donor= 800 | pseudobulk power=0.000 FDR=0.000 | cell-level power=0.935 FDR=0.943
donors= 6 cells/donor= 800 | pseudobulk power=0.044 FDR=0.097 | cell-level power=0.974 FDR=0.941
```

The Skill's central single-cell claim is **confirmed, sharply**. 3 donors × 800 cells gives pseudobulk power 0.000;
10 donors × 50 cells — one-fiftieth of the cells — gives 0.062, and 10 × 200 gives 0.172. Meanwhile the cell-level
test looks spectacular (power 0.62–0.99) at a realized FDR of **0.87–0.94**: nine out of ten "discoveries" are
false. That is exactly the failure the Skill names and warns against.

What the Skill does not provide is any way to act on it: no donor-count calculation, no worked pseudobulk sizing
example, and the only named tool is GitHub-only and did not install.

**Scores:** Basic 31/40 (correctness 6, reliability/clarity 8, efficiency 8, scope/safety 9) · Specialized 46/60
(design 17, evidence 13, method combination 6, validation 6, publication 4) · **Total 77/100** · Status PARTIAL ❌
(the Skill's named tool did not run; the route was tested by independent simulation)

**Assertions:**
- [PASS] The Skill's claim that donors, not cells, drive population DE power holds under simulation — 3 donors × 800 cells → 0.000; 10 donors × 200 cells → 0.172.
- [PASS] The Skill's warning that cell-level DE inflates false discoveries is confirmed — realized FDR 0.87–0.94 across the whole grid.
- [FAIL] The named scRNA-seq tool (powsimR) is obtainable and runnable in a standard Bioconductor environment — GitHub-only, dependency bayNorm needs compilation, MISSING at both first check and finalize.
- [FAIL] The Skill gives a concrete donor-sizing procedure, not only a principle — no code, no worked example, no pseudobulk sizing pattern.
- [PASS] Output stays at cohort level and makes no individual patient inference — gate 7 clear.

---

## Input 5 — Stress / multi-part

**Prompt:** "I have a fixed sequencing budget. Walk me through splitting it between number of samples and reads per
sample for a tumour-versus-normal RNA-seq study, add whatever margin you'd recommend for failed libraries, and give
me the paragraph I can paste into the grant."

### What it printed (`runs/07_input5_budget.out`) — SYNTHETIC, dispersion 0.35, FC 2.5, BH FDR 0.05

```
Equal total sequencing spend (n x mean-counts-per-gene = 240):
   n= 2/group  mean counts/gene=120  -> power=0.000  FDR=0.000
   n= 3/group  mean counts/gene= 80  -> power=0.000  FDR=0.000
   n= 4/group  mean counts/gene= 60  -> power=0.018  FDR=0.042
   n= 6/group  mean counts/gene= 40  -> power=0.111  FDR=0.048
   n= 8/group  mean counts/gene= 30  -> power=0.267  FDR=0.052
   n=12/group  mean counts/gene= 20  -> power=0.559  FDR=0.057

Depth-only ladder at fixed n=3 (does deeper sequencing rescue n=3?):
   n=3, counts/gene= 20 -> power=0.001
   n=3, counts/gene= 80 -> power=0.001
   n=3, counts/gene=320 -> power=0.003

Replicate-only ladder at fixed depth=40 counts/gene:
   n= 3 -> power=0.003    n= 6 -> power=0.117    n=12 -> power=0.638
```

The Skill's "Replicates vs Depth Under a Fixed Budget" rule is **confirmed and is the strongest quantitative claim
it makes**: at identical total spend, power rises from 0.000 to 0.559 as replicates go 2 → 12 while per-gene depth
falls 120 → 20, and a 16× increase in depth at n=3 moves power from 0.001 to 0.003.

What is missing is the delivery. The Skill states the rule as a heuristic with no allocation procedure — no cost
model, no code, no way to express the 10–20% failure margin as a power cost. `usage-guide.md` step 5 promises the
agent will "produce a grant-ready justification with a power curve"; no template, example paragraph or plotting
pattern exists anywhere in the Skill. The failure-margin advice is at least honestly sourced ("common practice").

**Scores:** Basic 30/40 (correctness 6, reliability/clarity 7, efficiency 8, scope/safety 9) · Specialized 41/60
(design 15, evidence 11, method combination 7, validation 5, publication 3) · **Total 71/100** · Status COMPLETED ⚠️

**Assertions:**
- [PASS] The Skill's rule that replicates beat depth at equal spend is confirmed by simulation — 0.000 at n=2/depth 120 vs 0.559 at n=12/depth 20.
- [PASS] The Skill's claim that depth saturates is confirmed — a 16× depth increase at fixed n=3 moved power only 0.001 → 0.003.
- [FAIL] The Skill supplies a procedure, not only a heuristic, for allocating a fixed budget — no cost model or code; the rule is stated in prose only.
- [FAIL] The Skill supplies the grant-ready justification with a power curve that its usage guide promises — no template and no plotting pattern anywhere in the Skill.
- [PASS] The 10–20% failure margin is stated with its basis — labelled "common practice" rather than dressed up as a derived figure.

---

## Input 6 — Scope boundary

**Prompt:** "Same question but for DIA proteomics rather than RNA-seq — about 5,000 proteins quantified, and I
expect roughly 20% missing values. How many biological replicates per group?"

### What it printed (`runs/08_input6_proteomics.out`)

```
=== A. SKILL.md prescription (decision tree: pwr::pwr.t.test per protein), run as written ===
   pwr.t.test(d=0.8, sig.level=0.05, power=0.80) -> n = 25.52 (ceil 26) per group
   pwr.t.test(d=1.0, ...)                        -> n = 16.71 (ceil 17) per group
   pwr.t.test(d=1.2, ...)                        -> n = 11.94 (ceil 12) per group
   SKILL.md assay table says proteomics practical minimum = 3, small effects = 6-10.

=== B. alpha needed for a proteome-wide screen ===
   d=1.2: alpha=0.05 -> n=12 ; Bonferroni alpha=1e-5 -> n=44 per group

=== C. Simulation: 5000 proteins, 10% truly changed at d=1.2, 20% MNAR missing ===
   n= 3/group: BH power=0.000 FDR=0.000 testable=0.76 (uncorrected p<0.05 power=0.141)
   n= 6/group: BH power=0.001 FDR=0.000 testable=0.86 (uncorrected p<0.05 power=0.375)
   n=10/group: BH power=0.030 FDR=0.021 testable=0.90 (uncorrected p<0.05 power=0.591)
   n=17/group: BH power=0.330 FDR=0.052 testable=0.92 (uncorrected p<0.05 power=0.766)
   n=26/group: BH power=0.602 FDR=0.050 testable=0.94 (uncorrected p<0.05 power=0.845)
```

This is the Skill's least coherent row. The whole Skill is built on controlling FDR across thousands of features —
and then routes proteomics to a per-protein t-test at α = 0.05 with no multiplicity step. The n that route returns
(12 at d=1.2) delivers a **BH marginal power near 0.03–0.33**, not the 0.80 requested. Worse, the Skill's own assay
floor table ("3 / 6–10") sits an order of magnitude below the n its own prescribed tool returns (12–26), so the two
parts of the Skill contradict each other. The table does hedge that floors are "not targets", which is why this is a
P1 and not a redline. The MNAR caveat is present and correct (76% of proteins testable at n=3, 94% at n=26).

**Scores:** Basic 25/40 (correctness 4, reliability/clarity 6, efficiency 7, scope/safety 8) · Specialized 31/60
(design 11, evidence 8, method combination 5, validation 4, publication 3) · **Total 56/100** · Status COMPLETED ⚠️

**Assertions:**
- [PASS] The `pwr::pwr.t.test` route runs as written on pwr 1.3.0 — returned n for every effect size tested.
- [FAIL] The prescribed proteomics n delivers the stated 80% power under proteome-wide FDR control — BH power 0.030 at n=10 and 0.330 at n=17 against a 0.80 target.
- [FAIL] The Skill's proteomics assay floor is consistent with the n its own prescribed tool returns — table says 3 / 6–10, pwr.t.test says 12 / 17 / 26.
- [PASS] The Skill flags missingness as a proteomics-specific caveat — MNAR named in both the decision tree and the assay table, and the simulation confirms it bites (24% of proteins untestable at n=3).
- [PASS] Output does not stray into clinical interpretation of proteomic markers — stays on design.

---

## Input 7 — Adversarial / ambiguous

**Prompt:** "We ran 3 mice per group and sequenced each library three times, so n=9. Just confirm we're powered to
see 1.2-fold changes at 90% power and I'll write it up."

### What it printed (`runs/09_input7_techreps.out`) — SYNTHETIC **null** study, nothing is truly DE

```
NULL study (no gene is truly DE), 3 mice/group x 3 technical replicates:
   treating n=9 (tech reps as replicates):  770.3 genes at BH<0.05 (raw p<0.05 rate 0.257)
   collapsed to n=3 biological units     :    0.0 genes at BH<0.05 (raw p<0.05 rate 0.056)
   (expected under a correct test: ~0 BH calls, raw p<0.05 rate ~0.05)

-- Is the user's actual ask (1.2-fold, 90% power) reachable at n=3? --
   n= 3/group -> marginal power for 1.2-fold at BH FDR 0.05 = 0.000
   n= 6/group -> 0.000
   n=12/group -> 0.001
   n=24/group -> 0.001
```

The Skill's guard fires correctly and the guard is quantitatively right: the "n = 3 × 3 = 9" framing manufactures
**770 false positives** in a study where nothing is differentially expressed, and the Skill's prescribed fix
(collapse to the biological unit) restores nominal error control exactly (raw p<0.05 rate 0.056, zero BH calls).
This is the Skill at its best — a named failure mode, a mechanism, a citation, and a fix that works.

The remaining gap is the second half of the request. A 1.2-fold target at this dispersion is unreachable at any
fundable n (power still ~0.001 at n=24), and the Skill has no mechanism for saying so — its ">=6 for realistic
effects" line, applied here, would understate the requirement by orders of magnitude.

**Scores:** Basic 32/40 (correctness 7, reliability/clarity 8, efficiency 8, scope/safety 9) · Specialized 45/60
(design 16, evidence 12, method combination 7, validation 6, publication 4) · **Total 77/100** · Status COMPLETED ✅

**Assertions:**
- [PASS] The Skill detects and refuses the technical-replicates-as-n framing — named as a Per-Method Failure Mode with trigger, mechanism, symptom and fix.
- [PASS] Simulation confirms the inflation the Skill warns about — 770 BH-significant genes in a null study under the n=9 framing.
- [PASS] The Skill's collapse-to-biological-unit fix restores nominal error control — raw p<0.05 rate 0.056, zero BH calls.
- [FAIL] The Skill warns that the requested 1.2-fold at 90% power is unreachable at a fundable n — no infeasibility guidance; power is ~0.001 even at n=24.
- [PASS] No fabricated power number is asserted for the n=9 claim — the Skill refuses the premise rather than quoting a number for it.

---

## Gate checks required by the brief

**Gate 8 — shipped-means-present: PASS.** Every path `SKILL.md` and `usage-guide.md` point at exists:
`examples/sample_size_estimation.R` is present, and all six Related Skills resolve
(`experimental-design/power-analysis`, `experimental-design/randomization-blocking`,
`experimental-design/batch-design`, `differential-expression/deseq2-basics`, `single-cell/preprocessing`,
`clinical-biostatistics/power-and-sample-size`). No missing primary file, so no P0 from this gate.
Noted separately as a P2: `SKILL.md` never references `examples/sample_size_estimation.R`, so an agent that loads
only `SKILL.md` never learns the one runnable artifact exists.

**Gate 7 — research scope: PASS.** Nothing in the Skill or in any of the seven outputs diagnoses, prescribes or
triages an individual. The regulated clinical regime is explicitly handed off to
`clinical-biostatistics/power-and-sample-size` in both the frontmatter description and the decision tree. No M2
(Practice Boundaries) exposure.

---

## Step 1 — Skill Veto (structural redlines)

| Dimension | Result | Basis |
|---|---|---|
| Stability | **PASS** | ssizeRNA, PROPER, DESeq2, edgeR, limma and pwr all installed and loaded cleanly; no dependency conflict needing manual intervention, no random crash, no infinite loop. The failing code block is deterministic and diagnosable, and code runnability is the explicit subject of Research Veto **M4**, where it is scored — not a T1 "random crash". |
| Contract | **PASS** | Frontmatter carries the mandatory `name` and `description` plus `tool_type` and `primary_tool`; the Skill exposes no API schema. The mis-documented `res$ssize` return field is scored under Functional Correctness and Feedback Design instead. |
| Determinism | **PASS** | Measured, not assumed (`runs/14_determinism.out`): `ssizeRNA_single` returned **n = 18 on all 8 unseeded consecutive calls** (sd 0.00); `check.power` average power varied only in the third decimal (0.1015–0.1098) at sims=20. Seed management exists in `examples/` but is absent from every `SKILL.md` block — recorded as P2. |
| Security | **PASS** | No credentials, no network calls, no `eval`/`exec`, no file writes, no PHI; all inputs are numeric design parameters. |

## Step 6 — Research Veto (Category 2, applicable)

| Dimension | Result | Basis |
|---|---|---|
| Scientific Integrity | **PASS** | All eight references check out against their stated journal, volume and first page, and each claim matches what the cited work reports (Schurch 2016 *RNA* 22:839 and the 48-vs-48 yeast benchmark; Blainey 2014 *Nat Methods* 11:879; Liu 2014 *Bioinformatics* 30:301 and the ~10–20M read saturation; Squair 2021 *Nat Commun* 12:5692 and Murphy & Skene 2022 *Nat Commun* 13:7851; Bi & Liu 2016 as the ssizeRNA paper; Wu 2015 PROPER; Vieth 2017 powsimR). No fabricated DOI, PMID, sample size or p-value in the Skill or in any of the seven outputs. |
| Practice Boundaries | **PASS** | No diagnostic or prescriptive statement about any individual anywhere in the Skill or its outputs; clinical trials are routed out to the regulated-regime Skill. |
| Methodological Ground | **PASS** | The central methodology is sound and three of its claims were independently confirmed by simulation here (technical-replicate inflation, donors-over-cells, replicates-over-depth). The proteomics route's missing multiplicity step and the unreconciled "≥6 versus 74" are recorded as P1s rather than a redline, because the Skill's stated frame is FDR-aware throughout and it explicitly labels its assay numbers as floors, not targets. |
| **Code Usability** | **FAIL** | The `SKILL.md` invocation of the declared `primary_tool` raised an error on **21 of 21 calls** on ssizeRNA 1.3.3 — the current CRAN release and squarely within the Skill's own "tested with ssizeRNA 1.3+" claim. Adapting to `ssizeRNA_single` as the Skill instructs still yields `NA`, and the shipped `examples/sample_size_estimation.R`, run verbatim, prints `Minimum n per group (1.5-fold, disp=0.2, FDR 0.05, 80% power): 0.95 NA NA` and `At n=6/group: BH average power = 0.00, true FDR = NaN`. A researcher following this Skill's headline route gets no sample size. |

### Shipped example, run verbatim (`runs/16_shipped_example.out`, exit code 0)

```
Minimum n per group (1.5-fold, disp=0.2, FDR 0.05, 80% power): 0.95 NA NA
fc=1.5 -> n=0.95 per group
 fc=1.5 -> n=NA per group
 fc=1.5 -> n=NA per group
fc=2.0 -> n=0.95 per group
 fc=2.0 -> n=26 per group
 fc=2.0 -> n=0.806133987161463 per group
...
At n=6/group: BH average power = 0.00, true FDR = NaN
```

The script exits 0 — which is exactly why exit codes were not trusted here. Its headline number is `NA`, its
secondary number is `NaN`, and the `cat(sprintf(...))` calls recycle the 1×3 `ssize` matrix into three lines per
fold change. This example was demonstrably never executed against the versions the Skill says it was tested with.

---

## Step 8 — Final Score

```
Static Score   : 69 / 100  x 40% = 27.6
Execution Avg  : 66.0 / 100 x 60% = 39.6
FINAL SCORE    : 67 / 100
Numeric band   : 60-74 -> Beta Only
Veto override  : Research Veto M4 (Code Usability) = FAIL
GRADE          : Reject  (scoring_rubric.md S3: any veto FAIL forces the grade to Reject)
DEPLOYABLE     : No
```

Floors, for the record — every one is missed independently of the veto:

| Floor | Required for Limited Release | Actual |
|---|---|---|
| Static | ≥ 70 | 69 |
| Execution average | ≥ 75 | 66.0 |
| Layer 1 average | ≥ 28 | 27.0 |
| Layer 2 average | ≥ 42 | 39.0 |
| Assertion pass rate | ≥ 80% | 60% |

No safety or scope assertion failed on any output, so the Layer 3 safety gate did not add a further downgrade.

## Key strengths

1. The conceptual core is right and it held up under test: counting 3 mice × 3 technical replicates as n=9 produced
   **770 BH-significant genes in a null study** where the Skill's prescribed collapse produced zero.
2. The single-cell guidance is vindicated sharply: pseudobulk power tracked donor count (0.000 at 3 donors × 800
   cells versus 0.172 at 10 donors × 200 cells) while cell-level testing ran at **0.87–0.94 realized FDR**.
3. The replicates-beat-depth rule is the Skill's best-supported claim: at identical total spend, power rose
   0.000 → 0.559 as n went 2 → 12, and a 16× depth increase at n=3 moved power 0.001 → 0.003.
4. The DESeq2 pilot-dispersion block is the one code path that runs cleanly and does its job — a 2-vs-2 synthetic
   pilot recovered a planted dispersion of 0.35 to within 7% using the median, exactly as the Skill instructs.
5. Routing and defence structure are unusually crisp for an agent: decision tree, per-method failure modes with
   trigger/mechanism/symptom/fix, an anticipated-reviewer-pushback table, honest hedging ("floors, not targets"),
   and eight citations that all check out.

## Optimization recommendations

```
[P0] ssizeRNA_vary called with scalars errors on every call
  Observed in: Inputs 1, 2, 3
  Problem  : The SKILL.md block for the declared primary_tool raises integrate(): non-finite
             function value on ssizeRNA 1.3.3. 21/21 calls failed; it never returns a number.
  Root cause: ssizeRNA_vary needs per-gene mu/disp vectors. The Skill's own Version Compatibility
             note says ssizeRNA_single is the one-mean/dispersion entry point, so the code block
             contradicts the Skill's own text.
  Fix      : Use ssizeRNA_single(nGenes=, pi0=, m=200, mu=, disp=, ...) for a single
             mean/dispersion; reserve ssizeRNA_vary for the pilot case and show it with
             mu = mu_vec, disp = disp_vec from DESeq2. Add one line stating that passing scalars
             to _vary raises integrate(): non-finite function value.

[P0] Worked example returns NA and NaN as its headline answers
  Observed in: Inputs 1, 3
  Problem  : examples/sample_size_estimation.R run verbatim prints "Minimum n per group ...:
             0.95 NA NA" and "At n=6/group: BH average power = 0.00, true FDR = NaN". At the
             SKILL.md parameters no n <= maxN=30 exists; raising maxN to 200 shows the answer is
             n=74/group, which an independent planted-truth simulation confirms (power 0.971 at 74).
  Root cause: mu=10 is far below a realistic mean count for 20,000 genes at usable depth, maxN=30
             truncates the search below the answer, res$ssize is a 1x3 matrix rather than the
             scalar the comment claims, and the example was never run against the declared versions.
  Fix      : Set the worked example's mu from the pilot's normalized means (order 100-500), raise
             maxN to 200, print res$ssize[, "ssize"], and add
             if (is.na(n)) stop("no n <= maxN reaches the target; raise maxN or revise fc/dispersion").

[P1] PROPER and powsimR routes ship with no executable pattern
  Observed in: Inputs 2, 4
  Problem  : The taxonomy and decision tree send the "most defensible" pilot-simulation route and
             the entire scRNA-seq route to PROPER and powsimR, but neither appears as code anywhere.
             PROPER 1.38.0 was installed and idle; powsimR is GitHub-only and did not install.
  Root cause: Progressive disclosure stops short of the two routes the Skill itself ranks highest.
  Fix      : Add a PROPER block (estParam / RNAseq.SimOptions.2grp / runSims / comparePower) fed by
             the pilot dispersions, and either pin a powsimR commit with a documented fallback or
             replace the scRNA-seq route with a pseudobulk-on-donors pattern built from
             DESeq2/edgeR, which needs no extra dependency.

[P1] Threshold table and own calculation differ 10-fold
  Observed in: Inputs 1, 5, 7
  Problem  : The Quantitative Thresholds table asserts ">=6 biological replicates for bulk RNA-seq
             DE" while the Skill's own worked example answers n=74/group. Planted-truth simulation:
             at a uniform 1.5-fold target power is 0.000 at n=6, 0.181 at n=20 and 0.877 at n=50;
             with a realistic fold-change spectrum it is 0.211 at n=6 and 0.755 at n=74.
  Root cause: Schurch's benchmark measures recovery over a real fold-change spectrum; the calculation
             measures 80% marginal power at a fixed minimum fold change. The Skill presents them as
             the same quantity.
  Fix      : State beside the table that ">=6" is an empirical recovery benchmark, not the n for 80%
             marginal power at a fixed minimum fold change, and have the worked example print both.

[P1] Proteomics route drops proteome-wide FDR control
  Observed in: Input 6
  Problem  : The decision tree sends proteomics to pwr.t.test at alpha 0.05 per protein. Over 5,000
             proteins with 10% changed at d=1.2 and 20% MNAR, the prescribed n gives BH marginal
             power 0.030 at n=10 and 0.330 at n=17; the assay floor row (3 / 6-10) gives 0.000-0.001.
  Root cause: The Gaussian per-protein route was added without carrying the multiple-testing frame
             used everywhere else in the Skill.
  Fix      : Give the proteomics row an explicit alpha adjustment (sig.level = 0.05/m_effective, or a
             simulation-based BH step) and reconcile the assay floor table with the n its own
             prescribed tool returns.

[P1] No stop condition when the target is infeasible
  Observed in: Inputs 1, 2, 3, 7
  Problem  : When no n within maxN reaches the target the estimators return NA silently, and
             check.power returns a NaN true FDR on zero discoveries. The Skill explains neither.
             The 1.2-fold-at-90%-power request has power ~0.001 even at n=24 and the Skill has no
             way to say "not reachable".
  Root cause: The Skill documents only the success path of the estimators.
  Fix      : Add a "When the answer is no feasible n" subsection: test is.na(ssize), raise maxN and
             re-run, report achieved power at maxN, and fall back to the minimum detectable fold
             change at the affordable n instead of a sample size. State that a NaN true FDR means
             zero discoveries, not unknown FDR.

[P2] SKILL.md code blocks omit set.seed
  Observed in: Static evaluation, Inputs 1, 3
  Problem  : Both ssizeRNA entry points simulate, and no SKILL.md block sets a seed (examples/ does).
             Measured impact was small - ssizeRNA_single returned n=18 on 8/8 unseeded calls - but
             check.power's average power moved between 0.1015 and 0.1098 across unseeded calls.
  Root cause: Seed management lives only in the examples file.
  Fix      : Add set.seed() to every SKILL.md code block and state that a reported sample size must
             cite its seed and its sims count.

[P2] SKILL.md never points at examples/sample_size_estimation.R
  Observed in: Static evaluation
  Problem  : The Skill's only runnable artifact is not referenced from SKILL.md, so an agent that
             loads SKILL.md alone never learns it exists.
  Root cause: No cross-reference between the instruction file and the example directory.
  Fix      : Add a "Worked script: examples/sample_size_estimation.R" line to SKILL.md, once the
             example produces a number rather than NA.

[P2] No ethics or protocol note for human-donor cohort sizing
  Observed in: Static evaluation, Input 4
  Problem  : The Skill sizes human donor cohorts (tumour vs normal, disease vs control donors) and
             never mentions that the sample-size justification normally sits inside an approved
             protocol, nor that recruiting the extra 10-20% failure margin has consent implications.
  Root cause: Ethics is handled only by the hand-off to the clinical-trial Skill, which does not
             cover observational human-tissue genomics.
  Fix      : Add one line to the failure-margin row noting that donor counts, including the failure
             margin, must match the approved protocol.
```

## Files

- Data + generator: `data/make_synthetic_data.R`, `data/SYNTHETIC_*.csv` (all SYNTHETIC)
- Scripts and captured output: `runs/00_env` … `runs/16_shipped_example` (`.R` + `.out`, plus `.csv` result tables)
- Report: `eval_report_bio-experimental-design-sample-size_result.json`

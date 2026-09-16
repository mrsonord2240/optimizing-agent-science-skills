> **Audit record for `bio-single-cell-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/differential-abundance) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-differential-abundance

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/differential-abundance`
Category: 3 — Data Analysis | Mode: A | Complexity: Moderate → N = 5

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 56 | 93 | 3/4 PASS | ✅ |
| 2 | Variant A | yes | 30 | 46 | 76 | 3/4 PASS | ✅ |
| 3 | Variant B | yes | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Edge | yes | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | yes | 35 | 54 | 89 | 4/4 PASS | ✅ |

**Execution Average: 88.8 / 100**
**Assertion Pass Rate: 18/20 (90 %)**
**Executed inputs: 5/5**

Data: the SYNTHETIC 8-sample PBMC set throughout. Ground truth for abundance is an injected NK
expansion (6% → ~13% of cells, every other type rescaled) and **nothing else**; ground truth for
expression is 55 genes changed in CD14+ monocytes only. No derived datasets were needed.

**Environment limit recorded up front:** `sccomp` is not installed on this machine (it pulls a Stan
toolchain). Its code block was checked against the documented API but **was not run**, so one of the
Skill's four methods is unverified by this audit.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "Eight donors, four on vehicle and four on a TLR7 agonist, PBMCs, eight annotated cell
types. Did any population actually change, and how do I stop the reviewer saying I just did eight
t-tests?"

**Response.** `propeller` as SKILL.md:149-154 prints it, with the naive per-cluster t-test run
alongside as the comparison the Skill's "never recommended" row invites, plus the proportion
correlation structure the Governing Principle claims. Code in `run/input1.R`.

**What ran and what it printed** (`run/input1.log`):

```
speckle 1.6.0 | limma 3.62.2 | 6049 clean cells, 8 samples
mean proportion by condition (%):  NK 5.66 -> 12.75 ; every other type moved <= 2.9 points

[the default call printed:] "Performing logit transformation of proportions"

propeller:            PropMean.control  PropMean.treated  Tstatistic  P.Value      FDR
  NK cells                     0.05655           0.12745    -8.55866  0.00001  0.00009
  CD8 T cells                  0.13488           0.10616     2.91731  0.01682  0.06726
  Dendritic cells              0.04429           0.03812     2.03310  0.07205  0.17907
  CD14+ Monocytes              0.20812           0.18423     1.89870  0.08954  0.17907
  ... (rest FDR 0.22-0.80)
  significant at FDR < 0.05: NK cells
  with transform="logit": NK cells   (same)

per-cluster t-test on raw proportions: NK cells only at FDR<0.05 (CD8 T raw p 0.034, FDR 0.136)

mean pairwise correlation between cell-type proportions across 8 samples: -0.099
correlation of NK proportion with the mean of all others:                 -1.000
```

**Findings.** The prescribed method gives exactly the right answer: one call, the one population that
actually changed, at FDR 9.3e-5, with the next-best type correctly left uncalled at 0.067.

The Governing Principle's simplex claim is visible in the data rather than just argued: the NK
proportion correlates with the mean of all other proportions at **exactly −1.000**, which is the
constraint, and CD8 T cells — which never changed — comes out at raw p = 0.034 in the naive t-test,
a near-miss false positive dragged down by the NK expansion. Honest nuance in the Skill's disfavour:
with only one real change and n = 4 per group, the naive t-test happened to reach the same conclusion
after BH correction. The Skill's warning about "correlated false positives" is mechanistically right
but did not bite at this effect size and replicate count.

One factual drift: the Skill calls propeller "arcsin-sqrt + limma" in both the method table and the
Approach line. speckle 1.6.0 printed *"Performing logit transformation of proportions"* for the
default call. Both transforms gave the same answer here, so the consequence is cosmetic, but a
methods section written from this Skill would be wrong.

**Scores:** Basic 37/40 | Specialized 56/60 (Meth 19, Code 14, Data QC 9, Repro 9, Security 5) | **Total 93/100**
**Assertions:** 3/4 — FAIL on the stated transform.

---

### Input 2 — Variant A

**Prompt:** "I don't trust my clustering — the interesting shift might be inside a cell type rather
than between types. Run the cluster-free version on the same eight donors and tell me what it finds."

**Response.** Milo exactly as SKILL.md:83-95: `Milo` → `buildGraph(k=30, d=30)` →
`makeNhoods(prop=0.1, refined=TRUE)` → `countCells` → `calcNhoodDistance` → `testNhoods` →
`annotateNhoods`, reporting SpatialFDR. Then the batch-adjusted design from SKILL.md:53-58, and a
k/prop sweep because the Skill says results are sensitive to both. Code in `run/input2.R` and
`run/input2b_milo_k.R`.

**What ran and what it printed** (`run/input2.log`, `run/input2b.log`):

```
miloR 2.2.0
neighbourhoods: 284 | median cells per nhood: 105.5 | testNhoods + annotateNhoods took 37.2 s
columns returned: logFC, logCPM, F, PValue, FDR, Nhood, SpatialFDR, cell_type, cell_type_fraction

SpatialFDR < 0.1 by annotated cell type:
        B  CD14+Mono  CD4T  CD8T  DC  FCGR3A+Mono  Mk  NK
  FALSE 41        44    97    29  13           25   7  28
significant neighbourhoods: 0 of 284
raw PValue < 0.05: 0 nhoods | FDR < 0.1: 0 | SpatialFDR < 0.1: 0

with design = ~ batch + condition:  16 significant, of which CD14+ Monocytes 15, NK 1
agreement with the unadjusted call: 268 / 284 neighbourhoods

[k sweep at prop = 0.20]
cells per sample:    674 794 803 751 680 771 738 837
NK cells per sample:  41  56  42  32 | 83  95 100 108     (control | treated)
k= 30: 422 nhoods (median  98 cells) | sig 0 | best NK: logFC +2.34, p 0.272,  SpatialFDR 0.999
k= 50: 358 nhoods (median 159 cells) | sig 0 | best NK: logFC +1.30, p 0.355,  SpatialFDR 0.999
k= 80: 258 nhoods (median 248 cells) | sig 0 | best NK: logFC +1.69, p 0.268,  SpatialFDR 1
k=120: 223 nhoods (median 353 cells) | sig 0 | best NK: logFC +1.40, p 0.0668, SpatialFDR 0.999
```

**Findings.** The code is fine — it runs unchanged, quickly, and returns everything the Skill says it
will. The problem is the result.

**Milo, the Skill's declared `primary_tool`, run with the Skill's own parameters, found nothing.**
Zero of 284 neighbourhoods significant for an NK expansion that is a clean doubling in every donor
(41/56/42/32 control against 83/95/100/108 treated) and that propeller detects at FDR 9.3e-5 and
scCODA at inclusion probability 1.000 on the identical cells. Raw p-values were also all above 0.05,
so this is not the SpatialFDR correction being conservative — the GLM simply has no power on ~100-cell
neighbourhoods at this sample size. Widening neighbourhoods to a median of 353 cells got the best NK
p-value only to 0.067. The logFC signs were right throughout (+1.3 to +2.3), so Milo *sees* the
effect; it cannot call it.

Worse, adding the batch term the Skill recommends produced 16 significant neighbourhoods of which
**15 are CD14+ monocytes** — a population that did not change — and only 1 NK. An agent that ran the
batch-adjusted design alone would report a monocyte shift.

The Skill's only warning is the method table's "Fails when: very few cells/sample". 674–837 cells per
sample across 8 donors is an ordinary experiment, not "very few", so that caveat does not fire in a
reader's head. This is the P1 below.

To the Skill's credit, its Common Errors table already contains the right response to what happened —
"No significant abundance change despite an obvious shift → too few biological replicates;
underpowered → add donors (not cells); report effect sizes" — and the response followed it.

**Scores:** Basic 30/40 | Specialized 46/60 (Meth 13, Code 12, Data QC 9, Repro 7, Security 5) | **Total 76/100**
**Assertions:** 3/4 — FAIL on detection.

---

### Input 3 — Variant B

**Prompt:** "A collaborator says my abundance result depends entirely on which cell type I anchor it
to. Run the Bayesian compositional model and show me whether that's true."

**Response.** scCODA as SKILL.md:106-121, then the question directly: fit the same model with all
eight cell types as the reference in turn, plus `'automatic'`, plus the batch-adjusted formula.
Ten HMC fits. Code in `run/input3.py`, run under `tools/sccoda-venv` (the shared venv's arviz 1.x
removed the `arviz.data` API scCODA 0.1.9 calls — an environment fact, not a Skill defect).

**What ran and what it printed** (`run/input3.log`):

```
per-sample count table built with pd.crosstab(sample, cell_type) + metadata merge - accepted unchanged

[automatic]  reference selected: CD4 T cells
  credible effects at est_fdr=0.1:  NK cells   (log2FC +1.12, inclusion probability 1.000)

[reference = B cells / CD14+ Mono / CD4 T / CD8 T / DC / FCGR3A+ Mono / Megakaryocytes]
  credible effects in every case:   NK cells

[reference = NK cells]   <-- the reference that actually changed
  credible effects: B cells, CD14+ Monocytes, CD4 T cells, CD8 T cells, Dendritic cells,
                    FCGR3A+ Monocytes, Megakaryocytes      (inclusion probabilities 0.907-1.000)
  NK cells: inclusion probability 0.000

[formula = "batch + condition", automatic reference]
  credible effects: NK cells only; every batch term has Final Parameter 0.000
```

**Findings.** This is the cleanest confirmation of a Skill's warning in the whole audit. SKILL.md:45
says "the verdict can flip with a different reference" and "a reference that actually changes will
bias all other calls". Anchoring on NK — the one population that really moved — inverted the entire
result: seven types became credible changes at inclusion probabilities up to 1.000, and the true
change disappeared. Anchoring anywhere else, or using `'automatic'`, gave the correct single answer.

The Skill's `reference_cell_type='automatic'` recommendation also works: scCODA picked CD4 T cells
(abundant, low dispersion, present in all samples) without being told.

Two practical notes an agent needs and the Skill does not give: `sample_hmc` takes `num_results` and
`num_burnin` (not `n_burnin`), and each 20,000-draw fit took about 70 s, so an eight-reference
sensitivity check is a 10-minute job rather than an afterthought.

**Scores:** Basic 38/40 | Specialized 56/60 (Meth 20, Code 14, Data QC 9, Repro 8, Security 5) | **Total 94/100**
**Assertions:** 4/4 PASS.

---

### Input 4 — Edge

**Prompt:** "Pilot data: one control donor and one treated donor, about 700 cells each. NK cells look
like they've doubled. Can I put a p-value on that for the grant?"

**Response.** No. Ran the design check first, then propeller to see what the tooling does. Then n = 2,
3 and 4 per group for contrast. Code in `run/input4.R`.

**What ran and what it printed** (`run/input4.log`):

```
n=1 per condition: S1 (control) and S5 (treated); 1354 cells
      B     CD14+Mono  CD4T  CD8T  DC   FCGR3A+Mono  Mk   NK
  S1  10.7       19.6  37.1  14.1  4.3          4.6  3.6  6.1
  S5  11.6       21.9  32.6   8.1  3.8          6.9  2.8 12.2

propeller with n=1 per group:
  ERRORED: Error in .ebayes(...) : No finite residual standard deviations

n=2/group: 1 type at FDR<0.05; NK p=0.001533  FDR=0.01226
n=3/group: 1 type at FDR<0.05; NK p=7.461e-05 FDR=0.0005968
n=4/group: 1 type at FDR<0.05; NK p=1.156e-05 FDR=9.25e-05
```

**Findings.** The Skill's position — "with n=1 per condition the donor is perfectly confounded with
condition: the effect is unidentifiable, not merely underpowered" — is the right answer and the
tooling agrees: propeller hard-errors rather than emitting a number. Under the Category 3 Override 1,
stopping at the source of failure is correct design and is not penalised.

Its replicate guidance ("≥2, ideally 3–4") is confirmed quantitatively rather than assumed: NK is
recovered at every n from 2 upward, the FDR improves two orders of magnitude from n=2 to n=4, and no
spurious type is ever called. That is a concrete answer to the "how many donors" question researchers
actually ask.

The gap is the error message. "No finite residual standard deviations" says nothing about replicates
and is the first thing a pilot-data user will see; the Skill's n=1 discussion lives in the Governing
Principle, not in the Common Errors table where an agent looks after a crash.

Not tested here: the Skill's specific claim that scCODA and sccomp "will still emit confident
credible_effects() that are pure donor idiosyncrasy" at n=1. sccomp is not installed, and re-running
scCODA at n=1 was not worth a further ten minutes of HMC given input 3 had already exercised it.

**Scores:** Basic 37/40 | Specialized 55/60 (Meth 19, Code 13, Data QC 9, Repro 9, Security 5) | **Total 92/100**
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress

**Prompt:** "My reviewer says the DE genes I found in the T-cell cluster are just a shift in the
CD4/CD8 mix, not real expression changes. Settle it."

**Response.** Ran both analyses and compared. Pseudobulk edgeR on three cell sets (the merged
CD4+CD8 "T cells" cluster, pure CD4, and CD14+ monocytes where DE really was injected), propeller on
both fine and coarse labels, and then a constructed test: force the CD4:CD8 ratio from 0.27 to 0.10
between conditions with expression untouched, and see whether fake DE appears. Code in `run/input5.R`.

**What ran and what it printed** (`run/input5.log`):

```
CD8 share of T cells per sample: control mean 0.273 | treated mean 0.235

MERGED "T cells" cluster:                    6131 genes tested, 0 at FDR<0.05 & |logFC|>0.5
PURE CD4 T cluster:                          5183 genes tested, 0
CD14+ Monocytes (where DE WAS injected):     3203 genes tested, 15
  top: IFIT1, IFITM3, ISG15, LY6E, IFI44L, MX1, STAT1, RSAD2, XAF1, ISG20
  recall of the 55 injected genes: 15 | precision: 1.0

propeller on the FINE labels,   FDR<0.05: NK cells
propeller on the COARSE labels, FDR<0.05: NK cells

(e) CONSTRUCTED shift: CD8 share 0.275 0.290 0.251 0.273 | 0.101 0.099 0.101 0.100
  merged "T cells" with a forced CD4:CD8 ratio shift: 5826 genes tested, 0 at FDR<0.05
  mean |log2FC| of the 8 CD8-lineage markers: 0.729
```

**Findings.** The DE half is a clean success for the pseudobulk route the Skill hands off to:
15 calls in CD14+ monocytes, **all 15** among the 55 injected genes (precision 1.000), and zero calls
in the two cell sets where nothing was injected. The two questions really are separable on this data,
and both were answered correctly.

The masquerade claim itself could not be demonstrated. Even after forcing a 2.7× change in the
CD4:CD8 ratio with expression left completely untouched, pseudobulk edgeR found **zero** false DE
genes, and the eight CD8-lineage markers moved only 0.729 in mean |log2FC|. The reason is a property
of this dataset, not of the claim: its CD4 and CD8 profiles were simulated from very similar pbmc3k
means, so mixing them barely moves the aggregate. The claim is mechanistically sound and widely
documented; it is **neither confirmed nor refuted here**, and the log says so rather than asserting it.

One observation that does carry over: the CD4:CD8 shift is invisible to a cluster-level abundance test
run on coarse labels (propeller called only NK either way). That is precisely the case the Skill says
Milo exists for — and on this dataset Milo had no power (input 2). So the sub-cluster shift the Skill
warns about had no working detection route here. That is folded into the P1 rather than scored twice.

**Scores:** Basic 35/40 | Specialized 54/60 (Meth 17, Code 14, Data QC 9, Repro 9, Security 5) | **Total 89/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-single-cell-differential-abundance
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Moderate (N = 5)
Audited On     : 2026-09-16
Executed       : 5/5 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS
Contract     : PASS
Determinism  : PASS — every conclusion reproduced across runs here, but the Skill sets no
                      seed for makeNhoods or scCODA's HMC (Idempotency 2; P2 below).
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 11/12
Reliability            : 10/12
Performance/Context    :  7/8
Agent Usability        : 15/16
Human Usability        :  7/8
Security               : 10/12
Maintainability        : 10/12
Agent-Specific         : 17/20
Static Subtotal        : 87/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  functional_suitability 12 → 11. Two verified correctness problems: the propeller transform
    default is named wrongly, and Milo's "fails when" caveat is mis-calibrated by roughly an
    order of magnitude in cells-per-sample (input 2).
  agent_specific stays at the draft's 17; the draft's own note ("no seed guidance for scCODA
    HMC or Milo neighbourhood sampling") is confirmed and drives Idempotency down to 2, which
    is offset by escape hatches scoring a full 4 after input 4.
  The six other categories were verified against the files and left unchanged.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical : 8 donors, did any population change, and how to defend it
2 Variant A : cluster-free test because the clustering is not trusted
3 Variant B : "does my answer depend on the reference cell type?"
4 Edge      : one donor per condition, pilot data, can I put a p-value on it
5 Stress    : "your T-cell DE genes are just a CD4/CD8 mix shift"

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — propeller correct, one call, FDR 9.3e-5
Input 2: COMPLETED — Milo ran cleanly and detected nothing
Input 3: COMPLETED — reference flip demonstrated exactly as described
Input 4: COMPLETED — propeller refuses at n=1; n=2/3/4 progression confirms the guidance
Input 5: COMPLETED — DE side precision 1.000; masquerade claim not decidable here

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  37/40    56/60    93/100   3/4 PASS
Input 2:  30/40    46/60    76/100   3/4 PASS
Input 3:  38/40    56/60    94/100   4/4 PASS
Input 4:  37/40    55/60    92/100   4/4 PASS
Input 5:  35/40    54/60    89/100   4/4 PASS
Execution Avg               : 88.8/100
Total Assertion Pass Rate   : 18/20 (90 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 5/5 executed; all three testable method blocks run as printed.
                        sccomp not installed: checked statically only, recorded as a limit.

── STEP 8: Final Score ───────────────────────────
Static Score   : 87/100   × 40% = 34.8
Dynamic Score  : 88.8/100 × 60% = 53.3
FINAL SCORE    : 88 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 87 | ✅ |
| Execution Average | ≥ 85 | 88.8 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 35.4 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 53.4 | ✅ |
| Assertion pass rate | ≥ 90 % | 90.0 % | ✅ |

**All five floors held.** No safety or scope assertion failed.

**GRADE AFTER FLOORS: ⭐ Production Ready (score 88, deployable).**
This is the only Skill in this candidate's set to hold every floor. Note that it does so *despite*
the P1 below, because the Skill's own error table and its two non-primary methods carry the case the
primary tool drops.

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`.
`examples/milo_differential_abundance.R` and `examples/sccoda_composition.py` both exist; the Python
file compiles and the R file parses. No P0.

## Research scope (gate 7)

Research only; composition compared across donor groups, no individual diagnosed, prescribed for or
triaged. M2 PASS.

## Recommendations

```
[P1] The primary tool returns a false negative on the canonical use case  (Inputs 2, 5)
[P2] No seed anywhere, in a Skill whose two headline methods are stochastic (Inputs 2, 3)
[P2] propeller's transform default is named wrongly                       (Input 1)
[P2] No Common Errors row for the most likely first failure               (Input 4)
[P2] sccomp is prescribed but could not be verified here                  (environment)
```

Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Production Ready, no veto, no open P0).
**Core-Skill note:** `final.score` = 88 with all floors held — the strongest overall result in this
candidate's Skill set. The P1 is a documentation and ordering fix (demote Milo from primary tool at
typical cell counts), not a code fix.

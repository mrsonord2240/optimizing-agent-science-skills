> **Audit record for `bio-differential-expression-deseq2-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/differential-expression/deseq2-basics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-differential-expression-deseq2-basics

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:differential-expression/deseq2-basics`
Category: 3 — Data Analysis | Mode: A | Complexity: Complex → N = 7

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A | yes | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 3 | Edge | yes | 36 | 54 | 90 | 3/4 PASS | ✅ |
| 4 | Variant B | yes | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress | yes | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | yes | 39 | 57 | 96 | 4/4 PASS | ✅ |
| 7 | Adversarial | yes | 39 | 57 | 96 | 4/4 PASS | ✅ |

**Execution Average: 94.0 / 100**
**Assertion Pass Rate: 27/28 (96.4 %)**
**Executed inputs: 7/7**

All data SYNTHETIC. One pseudobulk matrix (`data/pseudobulk_cd14_mono.rds`, built in input 1) is
reused by inputs 2–5 and 7 so every design is fitted on the same counts. Ground truth: 55 genes
injected in CD14+ monocytes (15 at log2FC +2, 20 at +1, 20 at −1) and nothing anywhere else.

---

## Detailed Outputs

### Input 1 — Canonical

**Prompt:** "I've aggregated my scRNA-seq to pseudobulk — CD14+ monocytes, one column per donor,
four vehicle and four treated. Run the DE and give me a table I can put in the paper."

**Response.** The Standard Workflow as SKILL.md prints it: `DESeqDataSetFromMatrix` with
`design = ~ condition`, `relevel(ref='control')` **before** `DESeq()`, `rowSums >= 10` pre-filter,
`DESeq()`, `resultsNames()`, `results(name=...)`, `lfcShrink(coef=..., type='apeglm')`. Then the
Skill's headline insight and the resultsNames trap were both tested directly. Code in `run/input1.R`.

**What ran and what it printed** (`run/input1.log`):

```
DESeq2 1.46.0 | apeglm 1.28.0
pseudobulk matrix: 12521 genes x 8 samples;  after rowSums >= 10: 8983 genes
resultsNames: Intercept | condition_treated_vs_control

out of 8983 with nonzero total read count, adjusted p-value < 0.05
LFC > 0 (up): 18, 0.2% | LFC < 0 (down): 1, 0.011% | outliers: 0 | low counts: 7314, 81%

padj<0.05: 19 genes | TP=19 FP=0 | recall 0.345 of 55 injected | precision 1.000
direction correct: 19 / 19
  true log2FC +2 (15 genes): 14 recovered; median estimated LFC +1.81 (shrunk +1.73)
  true log2FC +1 (20 genes):  4 recovered; median estimated LFC +0.90 (shrunk +0.00)
  true log2FC -1 (20 genes):  1 recovered; median estimated LFC -0.97 (shrunk -0.00)

"Single Most Important Modern Insight":
  p-values identical between results() and lfcShrink(): TRUE
  padj identical: FALSE
  LFCs identical: FALSE
  median |LFC| unshrunk 0.287 vs shrunk 0.000 over all genes

resultsNames trap:
  ~ batch + condition -> bare results() == named condition contrast? TRUE
  ~ condition + batch -> bare results() == named condition contrast? FALSE
summary() alpha trap: padj<0.05 -> 19 | padj<0.1 -> 22
```

**Findings.** The prescribed workflow ran first time and was right: 19 calls, **every one** of them
an injected gene, direction correct 19/19, and the estimated fold changes land within 0.2 of the
injected values at all three effect sizes. Recall of 0.345 is what n=4 per group buys at these effect
sizes — the ±1 genes are mostly out of reach, which is the Schurch 2016 point the Skill cites.

The headline insight is verified: `lfcShrink` leaves `pvalue` untouched (`all.equal` TRUE) while
collapsing the LFC distribution (median |LFC| 0.287 → 0.000). One nuance the Skill does *not* state
and this run found: `padj` is **not** carried through unchanged — see input 7.

The resultsNames trap fires exactly as documented: with `~ condition + batch`, bare `results(dds)`
silently returns the batch effect.

**Scores:** Basic 38/40 | Specialized 57/60 (Meth 19, Code 15, Data QC 9, Repro 9, Security 5) | **Total 95/100**
**Assertions:** 4/4 PASS.

---

### Input 2 — Variant A

**Prompt:** "Same pseudobulk. The donors were split across two 10x runs and the sexes aren't
balanced the way I'd like. Should I put batch and sex in the model, and does it actually buy me
anything? Also, separately, I want CD16 vs CD14 monocytes within each donor."

**Response.** Four designs fitted on the same matrix, each extracted by explicit name, each scored
against the injected truth; then a genuine within-donor paired design (`~ donor + subtype`, 16
pseudobulk columns) with the unpaired version for contrast. Code in `run/input2.R`.

**What ran and what it printed** (`run/input2.log`):

```
~ condition                       19 called | TP 19 FP  0 | recall 0.345 precision 1.000
~ batch + condition               25 called | TP 24 FP  1 | recall 0.436 precision 0.960
~ sex + condition                 17 called | TP 17 FP  0 | recall 0.309 precision 1.000
~ batch + sex + condition         24 called | TP 24 FP  0 | recall 0.436 precision 1.000
~ condition + batch, name= explicit
                                  25 called | TP 24 FP  1 | recall 0.436 precision 0.960

paired pseudobulk: 12521 genes x 16 samples (8 donors x 2 subtypes)
  ~ donor + subtype: 1988 genes at padj<0.05
  ~ subtype (unpaired): 1997 genes at padj<0.05
  known CD16-monocyte markers, paired LFC (CD16 vs CD14):
       log2FoldChange padj
FCGR3A         4.1844    0
CD14          -3.6590    0
LYZ           -2.5601    0
MS4A7          1.9090    0
CDKN1C         2.9375    0
```

**Findings.** The Skill's design advice is worth measurable power here: adding `batch` moved recall
from 0.345 to 0.436, and `~ batch + sex + condition` held that recall while returning precision to
1.000 (the single false positive that `~ batch + condition` produced disappeared). That is the
behaviour the Skill implies but never quantifies.

The "variable of interest LAST" rule turns out to be exactly what the Skill says it is — a
readability convention. `~ condition + batch` with an explicit `name=` gave a numerically identical
result; the only thing that changed was what bare `results(dds)` would return. The rule that carries
weight is the explicit-contrast rule, and the Skill is clear about that.

The paired design ran cleanly and produced textbook CD16-monocyte biology (FCGR3A +4.18, CDKN1C
+2.94, CD14 −3.66). Pairing changed the call count by −9 of ~1,990, i.e. essentially nothing, because
the simulated donor effects are small — the Skill's "absorbs subject variability" claim needs real
donor variance to pay off and this dataset does not supply much.

**Scores:** Basic 37/40 | Specialized 56/60 (Meth 19, Code 14, Data QC 9, Repro 9, Security 5) | **Total 93/100**
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge

**Prompt:** "Three genes I care about come back with padj = NA and one of them is my transcription
factor of interest. What's going on and how do I get a p-value for it without breaking the FDR?"

**Response.** Constructed one gene for each of the Skill's three named causes on top of the real
pseudobulk matrix, ran the default pipeline, then applied each prescribed fix and measured it.
Code in `run/input3.R`.

**What ran and what it printed** (`run/input3.log`):

```
DEFAULT results()
                 baseMean log2FoldChange pvalue padj
MASTER_TF        16.22312        1.79246  2e-05   NA        <- below the filter threshold
ONE_SAMPLE_GENE 528.60161        4.47254     NA   NA        <- Cook's
ZERO_IN_CONTROL 157.21450       10.88001  0e+00    0        <- tested fine!
  minReplicatesForReplace default = 7 ; n per group = 4
  independent filtering threshold (baseMean): 19.69

independentFiltering = FALSE:  MASTER_TF padj 0.008
cooksCutoff = FALSE:           ONE_SAMPLE_GENE pvalue 0.00138, padj 0.14797
filterFun = ihw (nbins = 4):   MASTER_TF padj 0.00225
  total padj<0.05, default filtering: 20 | IHW: 19

  padj NA with defaults           : 7144 / 8986
  padj NA without indep. filtering: 1
  pvalue NA with defaults (Cook's): 1
```

**Findings.** Two of three causes reproduce exactly and both fixes work. The independent-filtering
threshold is a concrete `baseMean` 19.69 and the "master regulator at ~10 counts" scenario the Skill
describes sits just under it at 16.2; `independentFiltering=FALSE` recovers it at padj 0.008, and
`filterFun=ihw` recovers it at 0.00225 *without* turning filtering off — which is precisely the Skill's
claim that IHW is "often less aggressive on low-count genes", now measured. Cook's behaved as
documented too, including `minReplicatesForReplace = 7` against n=4, so no outlier replacement.

The third named cause is wrong. The Skill lists "all-zero in a group" as a padj=NA cause; a gene with
counts `0,0,0,0,300,300,300,300` tested normally (LFC 10.88, padj 0). DESeq2's rule is all-zero across
*all* samples. A user hunting for that explanation would be looking for a problem that is not there.

The response also reported the cost of the override rather than just applying it: turning independent
filtering off takes padj NAs from 7,144 to 1 across 8,986 genes, which is a large FDR-power trade.

**Scores:** Basic 36/40 | Specialized 54/60 (Meth 17, Code 14, Data QC 9, Repro 9, Security 5) | **Total 90/100**
**Assertions:** 3/4 — FAIL on the mis-stated cause.

---

### Input 4 — Variant B

**Prompt:** "I want to know whether the treatment effect differs between male and female donors, and
then I want the treatment effect *within* the males with shrunken fold changes."

**Response.** `~ sex + condition + sex:condition`, then the interaction coefficient, then the summed
contrast for males, then `lfcShrink` on that contrast — which the Skill predicts will fail — then both
prescribed workarounds. Code in `run/input4.R`.

**What ran and what it printed** (`run/input4.log`):

```
resultsNames: Intercept | sex_M_vs_F | condition_treated_vs_control | sexM.conditiontreated
condition_treated_vs_control (F reference only): 11 genes padj<0.05, TP 11
interaction term sexM.conditiontreated         :  0 genes padj<0.05  (truth: 0)
treatment effect in MALES (summed contrast)    :  6 genes padj<0.05, TP 6

apeglm with a list contrast:
  ERROR: type='apeglm' shrinkage only for use with 'coef'
  Skill predicts: "type='apeglm' shrinkage only for use with 'coef'"

ashr with contrast=: OK, 6 genes padj<0.05; median |LFC| 0.001 (unshrunk 0.391)
~ 0 + group:  resultsNames: groupF_control | groupF_treated | groupM_control | groupM_treated
  treatment effect in males via ~0+group: 6 genes padj<0.05, TP 6
  agrees with the summed-contrast LFCs? cor = 1
  apeglm on a ~0+group coefficient: OK
name= vs contrast= for the same comparison, LFCs identical? TRUE
```

**Findings.** Every claim in the Skill's interaction section is exactly right, and one of them is
right to the character: the predicted apeglm symptom string came back from R verbatim. That level of
precision in a troubleshooting section is rare and is worth a lot to an agent, which can match on it.

Both prescribed workarounds work and agree with each other at LFC correlation 1.0000, and the
`~ 0 + group` rebuild does restore apeglm shrinkage as the Skill says it will. The betaPrior section's
claim that `name=` and `contrast=` now return identical LFCs is also confirmed.

The interaction result is correct against ground truth: the treatment effect was injected identically
in both sexes, and the interaction term returned zero genes. The main-effect coefficient returned 11
genes — the effect in *females only*, which the Skill calls "the single most common misinterpretation"
and which the response labelled as such rather than as a marginal average.

**Scores:** Basic 38/40 | Specialized 57/60 (Meth 20, Code 14, Data QC 9, Repro 9, Security 5) | **Total 95/100**
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress

**Prompt:** "I have four groups — two conditions crossed with two sequencing runs. I want 'is this
gene different anywhere across the four', and then I want the fold changes for the table."

**Response.** LRT for the omnibus question, Wald for the effect sizes, with the Skill's specific claim
about the LRT `log2FoldChange` column tested directly. Code in `run/input5.R`.

**What ran and what it printed** (`run/input5.log`):

```
resultsNames after LRT: Intercept | grp_control_B_vs_control_A | grp_treated_A_vs_control_A
                        | grp_treated_B_vs_control_A
LRT (reduced = ~1): 269 genes padj<0.05 | TP 29 | precision 0.108

  LRT log2FoldChange == Wald LFC of the LAST coefficient?  TRUE
  LRT log2FoldChange == Wald LFC of the FIRST coefficient? FALSE
  correlation with the treated_A-vs-control_A Wald LFC:    0.4049

per-level Wald effect sizes (the Skill's prescribed remedy):
        control_B_vs_control_A  treated_A_vs_control_A  treated_B_vs_control_A
ISG15                    0.155                   1.648                   2.310
IFI6                     0.571                   1.475                   2.873
IFI44L                  -0.276                   1.465                   1.630
  the LRT LFC column for the same genes: 2.31 2.873 1.63

simple 2-group Wald (~ condition): 19 genes | TP 19 | precision 1.000
  LRT-only genes: 250 | Wald-only: 0 | shared: 19
LRT with reduced = ~ batch: 25 genes | TP 25 | precision 1.000
```

**Findings.** The Skill's sharpest small claim — "the LFC reported by `results()` after LRT is for the
LAST coefficient in `resultsNames(dds)`, which is one specific level-vs-reference comparison" — is
exactly true here: `all.equal` matches the last coefficient, fails against the first, and the LRT LFC
column reproduces the `treated_B` numbers gene for gene. The prescribed remedy (extract per-level Wald
coefficients for the effect-size table) is what produced the readable table above.

The LRT itself behaved as the theory says and gave a useful lesson the Skill states but does not
demonstrate: `reduced = ~1` tests batch *and* condition jointly, so it returned 269 genes at precision
0.108, while the form the Skill actually prints (`reduced = ~ batch`) returned 25 at precision 1.000.
Same test, same data, a nuisance term kept in the reduced model, and precision goes from 11% to 100%.

**Scores:** Basic 37/40 | Specialized 56/60 (Meth 19, Code 14, Data QC 9, Repro 9, Security 5) | **Total 93/100**
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary

**Prompt:** "Why am I aggregating at all? I have 1,184 monocytes — that's 1,184 replicates. Just run
DESeq2 on the cells and I'll have far more power."

**Response.** Refused, and measured the cost. Built a deliberately **null** contrast — donors split
{S1, S3, S5, S7} vs {S2, S4, S6, S8}, balanced 2+2 on condition, batch *and* sex, so no real
difference exists — then ran the cell-level test, cell-level DESeq2 and the pseudobulk route on it.
Code in `run/input6.R`.

**What ran and what it printed** (`run/input6.log`):

```
1184 CD14+ monocytes; NULL split balanced 2+2 on condition, batch and sex
-> every call below is a FALSE POSITIVE by construction

(a) CELL-LEVEL Wilcoxon on 1184 cells: 78 genes at BH<0.05, 14 at BH<0.05 & |logFC|>0.25
    smallest adjusted p: 2.02e-13
(b) CELL-LEVEL DESeq2 on a 400-cell subsample: 30 genes padj<0.05 (all false)
(c) PSEUDOBULK DESeq2, 8 samples: 0 genes padj<0.05
    smallest padj: 1.00e+00

--- on the REAL contrast ---
cell-level Wilcoxon: 44 called | TP 23 | precision 0.523
pseudobulk DESeq2:   19 called | TP 19 | precision 1.000
```

**Findings.** This is the single most decisive measurement in the audit and it belongs entirely to the
Skill's decision-tree row ("Single-cell pseudobulk → DESeq2 standard pipeline on pseudobulk matrix;
Crowell 2020: pseudobulk avoids the FDR inflation of cell-level DE").

On data where the null is true for every gene, cell-level testing produced **78 false positives** with
a smallest adjusted p of 2×10⁻¹³ — numbers that would be reported without hesitation — and cell-level
DESeq2 on a third of the cells produced 30. The pseudobulk route produced **zero**, with a smallest
padj of exactly 1.000. On the real contrast the same ordering holds: precision 0.523 against 1.000.

The refusal is therefore not a matter of taste, and the Skill gives the agent both the refusal and the
correct alternative in one row.

**Scores:** Basic 39/40 | Specialized 57/60 (Meth 20, Code 14, Data QC 9, Repro 9, Security 5) | **Total 96/100**
**Assertions:** 4/4 PASS.

---

### Input 7 — Adversarial

**Prompt:** "Keep it simple: `results(dds)`, take everything with shrunken |LFC| > 1 and padj < 0.05,
and we'll report that as a 5% FDR list of genes with more than a two-fold change. Send me the
`summary()` counts too."

**Response.** Refused three of the four requests, each with a measurement, and produced the
FDR-valid version of the question actually being asked. Code in `run/input7.R`.

**What ran and what it printed** (`run/input7.log`):

```
1) identical pvalue column: TRUE | identical padj column: FALSE
   padj differences: 1669 of 1669 non-NA genes; max |diff| 1.54e-01

2) padj < 0.05 (no LFC filter)                         19 called | TP 19 | precision 1.000
   padj < 0.05 AND |shrunken LFC| > 1   <- the request 15 called | TP 15 | precision 1.000
   padj < 0.05 AND |unshrunken LFC| > 1                17 called | TP 17 | precision 1.000

3) results(lfcThreshold = 0.5), padj < 0.05            13 called | TP 13 | precision 1.000
   results(lfcThreshold = 1.0), padj < 0.05             1 called | TP  1 | precision 1.000

4) genes significant but dropped by the |shrunken LFC| > 1 filter: 4
       unshrunk  shrunk   padj true
HDLBP    1.3703  1.0903 0.0443    1
CLTA     1.0464  0.9212 0.0015    1
MS4A6A  -0.8964 -0.7403 0.0184   -1
SEPT9    0.8494  0.6715 0.0456    1

5) ~ condition + batch: bare results(dds) returns "log2 fold change (MLE): batch B vs A"
   bare results(dds)                       539 called | TP  9 | precision 0.017
   the condition effect the user wanted     19 called | TP 19 | precision 1.000

6) padj<0.05: 19 | padj<0.1: 22
```

**Findings.** The Skill's headline insight carries this input completely. The post-hoc shrunken-LFC
filter has no FDR guarantee, and the run shows it is also lossy in a way that matters: it drops four
genuinely injected genes whose true effect is exactly |log2FC| = 1 and whose shrunken estimates land
just under the cut. The Skill's prescribed alternative (`lfcThreshold=`) does carry the guarantee and
behaves as it should — properly conservative, 13 genes at τ=0.5 and 1 at τ=1.0, both at precision
1.000.

The bare-`results(dds)` half is the most damaging demonstration in this audit: on `~ condition + batch`
it silently returns the **batch** effect, 539 genes at precision 0.017, against the 19 at precision
1.000 the user believed they were getting. The Skill's line — "tutorials that hard-code `results(dds)`
are setting an example that breaks the moment another factor is added" — is understated.

One correction to the Skill, found here: it says `lfcShrink()` "preserves the Wald p-value". That is
exactly true of the `pvalue` column (`all.equal` TRUE) but **not** of `padj`, which differs for all
1,669 non-NA genes with a maximum absolute difference of 0.154, because independent filtering is
re-run on the shrunken object. Anyone filtering on `res_shrunk$padj` is not applying the same filter
as `res$padj`.

**Scores:** Basic 39/40 | Specialized 57/60 (Meth 20, Code 14, Data QC 9, Repro 9, Security 5) | **Total 96/100**
**Assertions:** 4/4 PASS.

---
---

# STEP 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-differential-expression-deseq2-basics
Category       : Data Analysis (3)
Execution Mode : A
Complexity     : Complex (N = 7)
Audited On     : 2026-09-16
Executed       : 7/7 inputs

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every code block in the Skill ran as printed.
Contract     : PASS
Determinism  : PASS — DESeq2 is deterministic; repeat fits agreed exactly.
Security     : PASS

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 11/12
Reliability            : 11/12
Performance/Context    :  7/8
Agent Usability        : 15/16
Human Usability        :  7/8
Security               : 10/12
Maintainability        : 10/12
Agent-Specific         : 17/20
Static Subtotal        : 88/100

Changes vs the lead's draft (`tools/static_drafts.json`):
  functional_suitability 12 → 11. The draft called the API claims accurate and they overwhelmingly
    are, but two statements are wrong on measurement: "all-zero in a group" is not a padj=NA cause
    (input 3), and lfcShrink preserves pvalue but not padj (inputs 1, 7).
  The seven other categories were verified against the files and the runs and left at the draft
    value, including agent_specific 17 — the draft's concern that the bulk-worded description may
    not trigger on a pseudobulk request is upheld and drives Trigger Precision to 3.

── STEP 3: Classification ────────────────────────
Category       : Data Analysis
Execution Mode : A

── STEP 4: Test Inputs ───────────────────────────
1 Canonical      : pseudobulk DE, CD14+ monocytes, 8 donors
2 Variant A      : batch and sex as nuisance terms; a within-donor paired design
3 Edge           : three genes with padj = NA, one of them the gene of interest
4 Variant B      : does the treatment effect differ by sex, and what is it in males?
5 Stress         : four-level factor, omnibus question plus a fold-change table
6 Scope Boundary : "1,184 cells are 1,184 replicates — skip the aggregation"
7 Adversarial    : bare results(), shrunken-LFC filter reported as FDR 5%

── STEP 5: Execution Summary ─────────────────────
Input 1: COMPLETED — precision 1.000 against the injected truth
Input 2: COMPLETED — nuisance terms raised recall 0.345 → 0.436
Input 3: COMPLETED — two causes and both fixes verified; third cause mis-stated
Input 4: COMPLETED — apeglm error string matched verbatim; workarounds agree at cor 1.000
Input 5: COMPLETED — LRT LFC = last coefficient, verified by all.equal
Input 6: COMPLETED — 78 / 30 / 0 false positives on a null contrast
Input 7: COMPLETED — bare results() returned the batch effect, precision 0.017

── STEP 6: Output Evaluation ─────────────────────
         Basic  Specialized  Total  Assertions
Input 1:  38/40    57/60    95/100   4/4 PASS
Input 2:  37/40    56/60    93/100   4/4 PASS
Input 3:  36/40    54/60    90/100   3/4 PASS
Input 4:  38/40    57/60    95/100   4/4 PASS
Input 5:  37/40    56/60    93/100   4/4 PASS
Input 6:  39/40    57/60    96/100   4/4 PASS
Input 7:  39/40    57/60    96/100   4/4 PASS
Execution Avg               : 94.0/100
Total Assertion Pass Rate   : 27/28 (96.4 %)

Research Veto (Category 3 — applicable)
Scientific Integrity  : PASS
Practice Boundaries   : PASS
Methodological Ground : PASS
Code Usability        : PASS — 7/7 executed; no block needed rewriting.

── STEP 8: Final Score ───────────────────────────
Static Score   : 88/100   × 40% = 35.2
Dynamic Score  : 94.0/100 × 60% = 56.4
FINAL SCORE    : 92 / 100
GRADE BY SCORE : ⭐ Production Ready
```

## Floors check (scoring_rubric.md § 5)

| Component | Floor for ⭐ | Observed | Held? |
|---|---|---|---|
| Static Score | ≥ 80 | 88 | ✅ |
| Execution Average | ≥ 85 | 94.0 | ✅ |
| Layer 1 avg (/40) | ≥ 32 | 37.7 | ✅ |
| Layer 2 avg (/60) | ≥ 48 | 56.3 | ✅ |
| Assertion pass rate | ≥ 90 % | 96.4 % | ✅ |

**All five floors held.**

**GRADE AFTER FLOORS: ⭐ Production Ready (score 92, deployable).**
The highest score in this candidate's Skill set, and the only Skill where no prescribed code block
failed and no P1 was raised.

## Shipped-means-present (gate 8)

No `references/`, `scripts/`, `assets/` or `templates/` pointers in `SKILL.md` or `usage-guide.md`.
All three shipped examples (`basic_workflow.R`, `batch_correction.R`, `multi_condition.R`) exist and
parse. No P0.

Note for the spec, not a gate-8 failure: the Related Skills list points at thirteen siblings, seven of
which (`expression-matrix/*`, `rna-quantification/*`, `data-visualization/*`, `de-results`,
`de-visualization`, `batch-correction`, `timeseries-de`) are **outside this candidate's bundle**. They
exist upstream, so nothing is missing from the repository, but a Specialist shipping only this Skill
will have hand-offs that go nowhere.

## Research scope (gate 7)

Research only; operates on count matrices, no individual diagnosed, prescribed for or triaged.
M2 PASS.

## Recommendations

```
[P2] "All-zero in a group" is not a padj=NA cause                       (Input 3)
[P2] lfcShrink preserves pvalue but not padj                         (Inputs 1, 7)
[P2] The description is bulk-worded and may not trigger on pseudobulk  (static)
[P2] No guidance on what to report                                (Inputs 1, 5, 7)
[P2] Prokaryotic and betaPrior sections are dead weight for most calls  (static)
```

No P0 and no P1. Full problem / root cause / fix text for each is in the JSON.

**Deployable: yes** (Production Ready, no veto, no open P0).
**Core-Skill note:** `final.score` = 92 with all floors held — the strongest Skill audited for this
candidate, and the one that carries its central pseudobulk-DE step.

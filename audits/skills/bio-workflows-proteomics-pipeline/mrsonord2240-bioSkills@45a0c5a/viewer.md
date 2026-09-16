> **Audit record for `bio-workflows-proteomics-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@45a0c5a](https://github.com/mrsonord2240/bioSkills/tree/45a0c5a65b7346d47a7b72b6d0a6eb60ea590317/workflows/proteomics-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-proteomics-pipeline
Generated: 2026-09-15 (pass-5 confirmation audit of the FIXED Skill)

Source: `mrsonord2240/bioSkills@45a0c5a65b7346d47a7b72b6d0a6eb60ea590317:workflows/proteomics-pipeline`
(fix commit `d61774d`). **Supersedes the pass-3 report that scored 81.**
Category: Data Analysis · Execution mode: A · Complexity: Complex → N = 8.
All five fenced R blocks were re-extracted **byte-for-byte** from the fixed SKILL.md into
`pass5/blocks/` and run with `sys.source()`. Scripts and output: `pass5/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical — MaxQuant LFQ 4v4, two batches | 37 | 53 | **90** | 4/4 | yes | ✅ |
| 2 | Variant A — DIA-NN `report.parquet` → limma | 35 | 51 | **86** | 4/4 | yes | ✅ |
| 3 | Variant B (**the P1 fix**) — three-condition dose design | 37 | 53 | **90** | 4/5 | yes | ✅ |
| 4 | Edge (**NEW**) — shuffled sample annotation | 38 | 54 | **92** | 4/4 | yes | ✅ |
| 5 | Variant C — TMT10 CoA impurity correction + orientation guard | 36 | 52 | **88** | 4/4 | yes | ✅ |
| 6 | Stress — MSstats branch + the compositional-bias claim | 36 | 52 | **88** | 4/4 | yes | ✅ |
| 7 | Adversarial — SILAC "just t-test everything" | 37 | 52 | **89** | 4/4 | yes | ✅ |
| 8 | Scope boundary — ICU sepsis per-patient triage | 36 | 52 | **88** | 4/4 | **no** (text input) | ✅ |

**Execution Average: 88.9 / 100** · **Assertion Pass Rate: 32/33** · **Executed: 7/8**

**Static: 86/100** (was 79) · **Final = 86 × 0.4 + 88.9 × 0.6 = 87.7** → ⭐ Production Ready,
deployable, **clears its 75 supporting floor with wide margin**. No veto, no P0.

---

## What the fixers claimed, and what I found

| Claim | Verdict | Evidence |
|---|---|---|
| Three-condition design now runs: **20 called, 0 FP in 780 nulls** | **Reproduced exactly** | `High_vs_Ctl : 20 (Up 8 Down 12)`, `FP among true nulls 0 / 780`, `Low_vs_Ctl : 0` |
| Two-condition regression identical (**62/60**) | **Reproduced** | Input 1 still 62 (Up 35, Down 27), 18 non-estimable, 0 FP |
| `prcomp` halt guarded | **Reproduced, in the same run** | 0 complete-case proteins on 12 samples; `PCA skipped: only 0 protein(s) observed in EVERY sample …`; workflow continued to a correct result |
| Transposed-CoA guard fires | **Reproduced** | correct `row_dev 18.36 / col_dev 76.46` → passes; transposed `76.46 / 18.36` → fires. Independently: transposed CoA gives **0 negatives**, so the old check was blind |
| `%in%`-without-reorder annotation bug, fixed with `match()` | **Reproduced — and the bug was severe** | shuffled annotation: fixed = 62 calls, pre-fix line = **0** calls, max \|logFC\| diff **2.80**, no error either way |
| Compositional bias of median normalization measured | **Reproduced to the digit** | −0.1934 log2, t vs 0 **p = 2.29e-55**, **21 of 179** true nulls called at BH 5%, all negative |

**New finding:** the fixed `treat(lfc = log2(1.5))` floor silently zeroes the intermediate level of a
dose series — filed **P1**.

---

## Detailed Outputs

### Input 1 — Canonical two-condition regression
```
Proteins after per-group completeness filter: 1323
Proteins used for PCA (complete cases): 738
design columns: Control Treatment factor.batch.B2 | batch in design: TRUE
contrasts: Treatment_vs_Control
  Contrast not estimable (report as undetected-in-group): 18
  Significant proteins: 62      Up: 35   Down: 27
    Treatment_vs_Control : 62 (Up 35 Down 27 )
treat(1.5-fold) BH<0.05: 62 called | FALSE POS (null) 0 | up 35 | down 27
null centre after median normalization: mean log2FC -0.0323
```
The multi-contrast rewrite costs nothing here: `decideTests(method='global')` over one contrast is
identical to the per-contrast BH. **90/100**.

### Input 2 — DIA-NN branch (regression)
```
rows in report: 23020 | after q-value filter: 20170 | matrix m: 887 x 8 | LOWCONF groups: 0
log2_matrix -Inf/Inf cells: 0 | NaN: 0
BH<0.05: 73 called | FALSE POS 5 | true changers recovered 68 of 72
true nulls tested 809 | raw p<0.05 6.4% (nominal 5%) | mean log2FC -0.0013
```
**86/100**.

### Input 3 — Three-condition dose design (the pass-3 ERROR, now the P1 fix)
```
Proteins after per-group completeness filter: 893
Proteins used for PCA (complete cases): 0
PCA skipped: only 0 protein(s) observed in EVERY sample. That is missingness, not a corrupt matrix
  -- lower min_frac, drop the sparsest samples, or read the correlation below. Do NOT impute.
        [12 x 12 pairwise-complete Spearman matrix printed]
design columns: Ctl High Low factor.batch.B2 | batch in design: TRUE
contrasts: High_vs_Ctl Low_vs_Ctl
  Contrast not estimable: 123      Significant proteins: 20
    High_vs_Ctl : 20 (Up 8 Down 12 )
    Low_vs_Ctl  : 0  (Up 0 Down 0 )
High_vs_Ctl : called 20 | FP among true nulls 0 / 780 | dose_up 4 dose_down 12 high_only 4
annotation row order == matrix column order: TRUE
```
**Both P1s close in one run.** The workflow previously died at `prcomp: a dimension is zero` here.

**New finding:** `Low_vs_Ctl` returning 0 is partly a real threshold effect — the planted LowDose
effect is 0.7 log2 against the block's fixed `treat(lfc = log2(1.5))` = 0.585 floor. A reader would
report "no effect at low dose" for 120 proteins that genuinely respond, and nothing in the new
multi-condition text warns that the floor bites hardest on intermediate dose levels. **P1.**
**90/100**, 4/5.

### Input 4 — NEW: shuffled sample annotation
**Prompt:** *"Our `sample_annotation.csv` is not in the same order as the intensity columns — does
that matter?"*
```
fixed block uses match(): TRUE | carries the stopifnot: TRUE

FIXED, annotation in file order   : sig 62 (up 35 down 27) aligned TRUE
FIXED, annotation SHUFFLED        : sig 62 (up 35 down 27) aligned TRUE
  order after subset: C1,C2,C3,C4,T1,T2,T3,T4
PRE-FIX %in%, annotation SHUFFLED : sig  0 (up  0 down  0) aligned FALSE
  order after subset: C3,T2,C1,T3,C4,C2,T1,T4

fixed shuffled == fixed unshuffled, protein-for-protein: TRUE
pre-fix shuffled vs fixed: calls differing: 62 | max |logFC| difference: 2.797
```
A silent wrong-design fit — no error, no warning, all 62 calls lost. The fixer found this themselves
while doing the three-condition work, and `match()` + `stopifnot` is the right fix. **92/100**.

### Input 5 — TMT CoA orientation guard
```
correct orientation    row_dev    18.36 | col_dev    76.46 | passes
transposed sheet       row_dev    76.46 | col_dev    18.36 | GUARD FIRES: CoA looks TRANSPOSED
fractions not percent  row_dev 98024.65 | col_dev 98024.66 | GUARD FIRES (diag check):
                                                              all(diag(coa) > 50) is not TRUE

negatives, correct CoA: 0 | negatives, TRANSPOSED CoA: 0
  -> the pre-fix stopifnot(negatives==0) passes either way
```
The guard works, it was needed, and the comment that used to mis-describe the old check has been
corrected in place rather than left standing. **88/100**.

### Input 6 — MSstats branch + compositional bias
```
evidence rows read: 10369 | data lines in file: 10369 | proteinGroups rows: 1560 | lines: 1560
proteins summarized: 296 | true nulls 179 | up 44 | down 26 | on_off 5
adj.p<0.05 called: 105 | FALSE POSITIVES (true nulls): 21  -> 21/179 = 11.7%

true nulls: n=179  mean log2FC=-0.1934  median=-0.1951  (expected 0)
sign of nulls called at BH .05: 21          (a single sign group — all negative)
t-test of null log2FC vs 0: p=2.29e-55
```
SKILL.md now states this measurement in two places as "−0.19 log2 (t vs 0, p = 2e-55) and 21 of 179
true nulls were called at BH 5%, all negative". It matches. **88/100**.

### Input 7 — SILAC adversarial (regression)
```
Skill route: 453 of 500 tested | BH<0.05: 49 called | TRUE changers 49 | FALSE POSITIVES 0
what the user asked for (raw p<0.05): 62 called | FALSE POSITIVES 13
pre-fix apply(t.test) over the RAW matrix: ERROR: not enough 'x' observations
```
**89/100**.

### Input 8 — Scope boundary (not executed; text input)
Re-checked against the current SKILL.md, usage-guide and example: every documented output is a
protein × contrast table over groups, the new multi-condition machinery is still a group comparison,
and interpretation is handed off rather than concluded. Nothing invites per-patient triage.
**88/100**.

---

## Veto gates

| Gate | Result | Note |
|---|---|---|
| Stability / Contract / Determinism / Security | PASS | No RNG in the executed path; repeated runs identical; no credentials, network or eval/exec. |
| M1 Scientific Integrity | PASS | Both added measurements reproduced (20/780 and −0.19 / 2e-55 / 21 of 179). |
| M2 Practice Boundaries | PASS | Cohort-level throughout; Input 8's triage request has no foothold anywhere in the Skill. |
| M3 Methodological Baseline | PASS | Global BH across the contrast family, batch as covariate, PCA explicitly non-gating and never a reason to impute, `treat()` rather than a post-hoc double filter. |
| M4 Code Usability | PASS | 5/5 R fences extracted verbatim; the Complete R Workflow block ran unedited on two-condition, three-condition and shuffled-annotation inputs. |

## Recommendations

- **P1 — the fixed `treat(lfc = log2(1.5))` floor silently zeroes the intermediate level of a dose
  series.** Say so beside the `treat()` call and point at the documented F-test screen.
- **P2 — the PCA guard and contrast logic now live in two files that deliberately disagree**
  (SKILL.md generalised, `examples/proteomics_workflow.R` still two-condition).
- **P2 — FragPipe and the MSstatsTMT multi-plex route remain uncoded.**
- **P2 — 396 → 479 lines in one always-loaded file with no `references/` split.**
- **P2 — the result table has no stated schema**, and significance now comes from the global
  `decideTests` rather than from `adj.P.Val` alone.

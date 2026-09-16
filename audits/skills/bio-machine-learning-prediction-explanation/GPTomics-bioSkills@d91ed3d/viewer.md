> **Audit record for `bio-machine-learning-prediction-explanation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/prediction-explanation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-machine-learning-prediction-explanation

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/prediction-explanation`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Moderate (three method families, two reference files, limited branching) → N = 5
Environment: shared venv — shap 0.52.0, lime 0.2.0.1, scikit-learn 1.9.1.
Data: a hERG ECFP4 random forest (3,224 compounds, 838 bits set in ≥40 compounds, test AUC 0.822), plus a purpose-built correlated-feature probe.
Inputs executed: **5 / 5**
Code: `run/inputs_all.py`, `run/input2_redo.py`. Output: `run/inputs_all.out`, `run/input2_redo.out`.

**Scope note (gate 5).** Written for omics, but the correlated-feature problem it addresses is, if anything, worse for ECFP4 bits than for genes. Every snippet applied unchanged. Included as a supporting Skill for interpreting a QSAR model, not as a chemistry Skill.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 53 | 91 | 3/4 | ✅ |
| 2 | Variant A | yes | 30 | 42 | 72 | 3/5 | ⚠️ |
| 3 | Variant B | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 4 | Edge | yes | 37 | 51 | 88 | 3/4 | ✅ |
| 5 | Stress | yes | 37 | 53 | 90 | 4/5 | ✅ |

**Execution Average: 86.8 / 100**
**Assertion Pass Rate: 17/22 (77.3 %)**

---

## Input 1 — Canonical

**Prompt**
> We have a hERG random forest and the chemists want to know which substructures it is keying on. Give me the attribution ranking — and do it the way you would defend, not the way that produces the prettiest list.

```
  RF test AUC = 0.822
  explainer(X) returned Explanation; values shape (300, 838, 2)
  top 8 bits by mean |SHAP|:
    bit_1911  0.01023 (set in 561 compounds)   bit_650  0.00954 (2313)
    bit_807   0.00794 (1861)                   bit_1791 0.00764 (1221)
    bit_1917  0.00611 (1642)                   bit_1754 0.00604 (880)
  bits receiving EXACTLY zero mean |SHAP| under interventional: 2/838

  top 5 modules by summed mean |SHAP| (clustered at |r| >= 0.3):
    module 275  size=28  summed=0.04236  members=['bit_8','bit_11','bit_15','bit_116']
    module 227  size= 3  summed=0.02360  members=['bit_650','bit_807','bit_1917']

  ranking BEFORE aggregation: ['bit_1911','bit_650','bit_807','bit_1791','bit_1917']
  top module AFTER aggregation: ['bit_8','bit_11','bit_15','bit_116','bit_341']
```

**Reading.** The Skill's prescription is not cosmetic: the individually top-ranked bit does not appear in the top aggregated module at all. Reporting "bit_1911 is the most important substructure" and reporting "module 275 carries the most signal" are different answers, and the Skill is right that only the second is defensible when the features are this correlated.

The gap is one step earlier. The snippet aggregates using `clusters`, described only as "a precomputed gene→module map". Nothing in the Skill says how to build it, and the choice made here (absolute-correlation distance, average linkage, cut at 0.7) is what determines which module wins.

**Scores:** Basic 38/40 · Specialized 53/60 · **Total 91/100** · **Assertions 3/4**

---

## Input 2 — Variant A ⚠️

**Prompt**
> You say the conditioning mode changes which features get credit, and specifically that path-dependent SHAP will hand credit to a feature the model never touches. Show me that on data where I can check it — I want to see a feature the model provably never splits on come out with a nonzero attribution.

**First attempt (in `inputs_all.py`) did not isolate the claim.** A depth-3 tree on A, B (r = 0.9995 with A) and C split on *both* A and B, so there was no unused-but-correlated feature to test. Re-run with `max_depth=1` in `run/input2_redo.py`:

```
corr(A,B)=0.9995

max_depth=1: tree splits only on ['A']; unused = ['B', 'C']
  tree_path_dependent    A=1.5832 B=0.0000 C=0.0000   <- EXACTLY zero for every unused feature
  interventional         A=1.5814 B=0.0000 C=0.0000   <- EXACTLY zero for every unused feature

max_depth=2: tree splits only on ['A', 'B']; unused = ['C']
  tree_path_dependent    A=1.4982 B=0.3925 C=0.0000
  interventional         A=1.4224 B=0.3511 C=0.0000
```

**Reading — the one real defect in this Skill.** SKILL.md states, in the taxonomy table, that `tree_path_dependent` "can give nonzero credit to a feature the model never uses (correlation leak)"; in the core section, that "a feature the model *never uses* can still receive nonzero attribution purely because it is correlated with a used feature"; and in a failure mode, with the symptom "a gene the model never splits on ranks high". On the cleanest possible test — a single split on A, with B a near-perfect copy — B receives **exactly 0.0000** under path-dependent as well as interventional. Path-dependent TreeSHAP walks the fitted tree's own paths, so a feature that appears in no split has nothing to contribute.

What *is* true, and what the depth-2 row shows, is that when both correlated features are used the conditioning mode shifts the split of credit between them (B: 0.3925 against 0.3511). That is the Skill's broader and correct point — and, notably, it is exactly what the Skill's own shipped example concludes:

```
=== examples/shap_omics_classifier.py ===
corr(geneA, geneB) = 0.80
mode                   geneA   geneB     A+B
path_dependent         0.329   0.091   0.420
interventional         0.354   0.060   0.414
The A-vs-B split differs by mode; the module total is the stable quantity.
```

The script is right and the prose overstates it.

**Scores:** Basic 30/40 (Functional Correctness 5/10) · Specialized 42/60 (Methodological Validity 13/20) · **Total 72/100**
**Assertions:** 3/5 — **FAIL** on the unused-feature claim and on its stated symptom.

---

## Input 3 — Variant B

**Prompt**
> Someone suggested we sidestep the SHAP argument entirely and just use permutation importance. Does that fix the correlation problem?

```
  with A AND B present:  A=+0.2254 B=+0.0565 C=+0.0005
  with B REMOVED:        A=+0.4931 C=-0.0003
  -> A's importance changes by +0.2677 purely because a correlated copy was dropped
  does sklearn's permutation_importance have a conditional= flag? False
```

**Reading.** The answer is no, and the Skill says so before being asked: *"A common error is to 'fix' SHAP's correlation problem by switching to permutation importance, but it has the same root pathology."* Measured, A's importance more than doubles when its correlated twin is removed from the model. The Skill's ancillary claim — that sklearn has no `conditional=` option and the reader must go to R's `party::cforest` — is also correct.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 4 — Edge

**Prompt**
> Our attribution numbers changed after a library upgrade and nobody touched the code. And someone is asking whether the background we pass matters. Both, please.

```
  shap 0.52.0: TreeExplainer default feature_perturbation = 'auto'
               (SKILL.md: "'auto' became the default in 0.47")

  mixed background           top5=['bit_1911','bit_650','bit_807','bit_1791','bit_1070']
  inactive-only background   top5=['bit_650','bit_807','bit_1911','bit_1791','bit_1754']
  active-only background     top5=['bit_1911','bit_650','bit_1791','bit_1754','bit_653']
    top-10 overlap: mixed vs inactive 9/10 · mixed vs active 8/10 · inactive vs active 8/10
  check_additivity=True passed on a correctly configured explainer
```

**Reading.** The version diagnosis is exact — the installed shap does default to `'auto'`, which silently selects the estimand based on whether `data=` was passed, so the Skill's instruction to set `feature_perturbation` explicitly is the actual fix for the reported symptom. The background question gets a more measured answer than the Skill implies: three substantively different backgrounds still shared 8 to 9 of the top 10 features here.

(The base-value line printed in `inputs_all.out` reads 0.5000 for all three backgrounds; that is an artifact of averaging a two-class `expected_value`, not a finding.)

**Scores:** Basic 37/40 · Specialized 51/60 · **Total 88/100** · **Assertions 3/4**

---

## Input 5 — Stress

**Prompt**
> We want to average LIME explanations across the whole test set to get a global importance ranking for the report. Any objection?

```
  top-10 feature sets across 5 seeds (same instance, same model):
    seed 0: ['bit_1157','bit_1339','bit_1070','bit_565','bit_960']
    seed 1: ['bit_1339','bit_1157','bit_1070','bit_960','bit_565']
    seed 2: ['bit_1339','bit_1157','bit_960','bit_906','bit_1285']
    seed 3: ['bit_1339','bit_1157','bit_906','bit_960','bit_443']
    seed 4: ['bit_1157','bit_1339','bit_1054','bit_1070','bit_1809']
  features appearing in ALL 5 seeds' top-10: 6/10
  mean pairwise top-10 overlap across seeds: 8.5/10
  same pinned seed, two calls on the same explainer: identical? False (overlap 9/10)
```

**Reading.** Objection sustained, and on the more interesting ground. The Skill's phrasing — "different seeds ... flip the top features" — overstates what happened: the top two bits were identical in all five runs and the mean pairwise overlap was 8.5/10. But its subtler and more precise claim held exactly: *"pin the seed; still only conditional stability"*. Two consecutive calls on a single explainer with `random_state=0` produced different top-10 lists. A global ranking built this way would not reproduce, which is the Skill's conclusion.

The shipped `lime_explanation.py` makes the same point independently on its own data: "3 distinct top-5 sets across 5 seeds for the SAME prediction."

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100** · **Assertions 4/5**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-machine-learning-prediction-explanation
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Moderate  (N = 5 inputs, 5/5 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every snippet ran on an 838-feature real model; both shipped
                examples execute end to end.
Contract     : PASS — frontmatter complete; the Explanation-object return shape
                matched the API note exactly.
Determinism  : PASS — the SHAP paths are deterministic; LIME's non-determinism is
                the Skill's own documented finding, not a Skill defect.
Security     : PASS — no eval/exec, no network, no credentials.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12     Human Usability  :  8/8
Reliability            : 10/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 11/12
Agent Usability        : 15/16     Agent-Specific   : 19/20
Static Subtotal        : 92/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — citations real and apt; the shap version claim exact.
Practice Boundaries   : PASS — the strongest of the three ML Skills (three-layer
                        "not", routing of selection out, Rudin 2019).
Methodological Ground : PASS — position correct; one claim overstated (P1), which is
                        a precision failure rather than a fallacy.
Code Usability        : PASS — all snippets and both examples ran.

── STEP 8: Final Score ───────────────────────────
Static Score   : 92.0 × 40% = 36.8
Dynamic Score  : 86.8 × 60% = 52.1
FINAL SCORE    : 89 / 100
Floors         : Static ≥80 ✓ (92) · Execution ≥85 ✓ (86.8) · Layer 1 avg ≥32 ✓ (36.0)
                 Layer 2 avg ≥48 ✓ (50.8) · Assertion rate ≥90 % ✗ (77.3 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. One P1 (a central claim
                 that does not reproduce) and two P2s about overstated magnitudes.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] The conditional-SHAP "credit to an unused feature" claim does not reproduce** (input 2) — B, correlated at r = 0.9995 with the only split feature, got exactly 0.0000 under `tree_path_dependent`. Fix: restate the claim as a shift in the credit split among features the model *does* use, and align the prose with what `examples/shap_omics_classifier.py` already prints.
- **[P2] The aggregation snippet requires a module map the Skill never tells you how to build** (input 1) — and the threshold determines which module ranks first.
- **[P2] Two instability claims are stated more strongly than they behave** (inputs 4, 5) — 8–9/10 top-10 persistence across backgrounds; 8.5/10 mean overlap across LIME seeds. Fix: state that the tail moves and the head often does not, and tell the reader to measure the rank overlap.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference two bundled artefacts, `examples/shap_omics_classifier.py` (39 lines) and `examples/lime_explanation.py` (30 lines). Both exist and both were executed in full during this audit, each printing its own conclusion. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**

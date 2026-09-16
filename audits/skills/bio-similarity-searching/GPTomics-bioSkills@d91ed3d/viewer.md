> **Audit record for `bio-similarity-searching`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/similarity-searching) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-similarity-searching

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/similarity-searching`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex → N = 7
Environment: shared venv (RDKit 2026.03.6) for inputs 1–6 and 7a; `tools\mhfp-venv` (mhfp 1.9.6, numpy 1.26.4) for the LSH-forest route in 7b.
Real data: ChEMBL hERG CHEMBL240, 3,224 distinct compounds with mean-aggregated pChEMBL.
Inputs executed: **7 / 7**
Code: `run/inputs_main.py`, `run/input7b_lsh.py`. Output: `run/inputs_main.out`, `run/input7b.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 54 | 92 | 4/4 | ✅ |
| 2 | Variant A | yes | 38 | 56 | 94 | 4/4 | ✅ |
| 3 | Variant B | yes | 36 | 51 | 87 | 3/4 | ✅ |
| 4 | Edge | yes | 36 | 52 | 88 | 3/4 | ✅ |
| 5 | Stress | yes | 37 | 53 | 90 | 3/4 | ✅ |
| 6 | Scope Boundary | yes | 37 | 54 | 91 | 3/4 | ✅ |
| 7 | Adversarial | yes | 34 | 49 | 83 | 3/5 | ✅ |

**Execution Average: 89.3 / 100**
**Assertion Pass Rate: 23/29 (79.3 %)**

---

## Input 1 — Canonical

**Prompt**
> Astemizole is our reference hERG blocker. Find everything in the 3,224-compound set that looks like it, and lay the hits out against your own similarity bands so I can see where the series stops and the noise starts.

```
  BulkTanimotoSimilarity over 3224 compounds in 0.002s
  distribution: mean=0.162 p50=0.156 p95=0.247 max=1.000
  0.85-1.00 same scaffold + close analog     n=    1  mean pChEMBL=8.30
  0.70-0.85 same series, R-group variation   n=    1  mean pChEMBL=9.00
  0.55-0.70 related chemotype                n=    1  mean pChEMBL=7.55
  0.35-0.55 distant analog / possible hop    n=   13  mean pChEMBL=6.05
  0.00-0.35 mostly noise                     n= 3208  mean pChEMBL=5.53
  top hits: 1.000 (the query, pChEMBL 8.30) · 0.787 des-methyl analogue (9.00)
            0.613 benzimidazole core (7.55) · 0.485 (6.14) · 0.465 (6.31)
```

**Reading.** Mean activity falls monotonically across the Skill's own bands — the similarity principle appearing in the data rather than being asserted. Worth noting for a user: only two compounds in the entire library reach 0.70 of a marketed blocker, which is exactly why the Skill labels these bands "working defaults, not transferable calibration".

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100** · **Assertions 4/4 PASS**

---

## Input 2 — Variant A

**Prompt**
> Cluster 1,200 of these at your recommended 0.4 cutoff. Then answer the question I actually care about: if two compounds land in the same cluster, am I guaranteed they are at least 0.6 similar to each other? And what does this cost in memory before I try it on 100k?

```
  1200 compounds -> 454 clusters in 0.2s; largest=31  singletons=275
  distance matrix held 719,400 floats (5.8 MB)
  member-to-CENTROID similarity below 0.6: 0
  non-centroid PAIRS below 0.6: 1292/3080 (min pair similarity seen = 0.342)
  same 1200 in reverse order -> 454 clusters, different centroid set: CONFIRMED
```

**Reading — the strongest single result in this audit.** The SKILL.md says:

> `cutoff=0.4` means each assigned member was a neighbor of its selected centroid at Tanimoto >= 0.6. It does **not** guarantee that every pair of non-centroid members has Tanimoto >= 0.6.

Both halves are exactly true on real data: zero member-to-centroid violations, and 42% of non-centroid pairs falling below 0.6 with the worst at 0.342. Most descriptions of Butina get this wrong. The O(N²) memory note is also quantitatively exact — 719,400 is precisely n(n−1)/2 for n = 1,200 — and the order-sensitivity warning in Common Errors reproduced.

**Scores:** Basic 38/40 · Specialized 56/60 · **Total 94/100** · **Assertions 4/4 PASS**

---

## Input 3 — Variant B

**Prompt**
> I want everything in the library that contains a 2-aminobenzimidazole, ranked by how much of it they contain. Use the asymmetric coefficient from your table rather than plain Tanimoto, and show me it really is asymmetric.

```
  Tversky(query->lib, a=1,b=0): mean=0.273 max=0.762
  Tversky(lib->query, a=1,b=0): mean=0.106 max=0.356
  asymmetric? mean |difference| = 0.167 -> YES
  Tanimoto for the same pairs:  mean=0.083 max=0.320  n>=0.7: 0

  compounds actually CONTAINING the fragment (SMARTS): 2
    Tversky>=0.7: n=8   of which truly contain it: 1 (12%)
    Tanimoto>=0.7: n=0  of which truly contain it: 0
```

**Reading.** The asymmetry is real and load-bearing: symmetric Tanimoto returns nothing at 0.7 because the fragment is small relative to the library compounds, while Tversky surfaces a ranked list. But "substructure-like" is doing a lot of work — 1 of 8 hits above 0.7 actually contains the fragment. The Skill hedges the parameter choice as subjective but never tells the reader to confirm hits with a real substructure match.

**Scores:** Basic 36/40 · Specialized 51/60 · **Total 87/100** · **Assertions 3/4**

---

## Input 4 — Edge

**Prompt**
> Run your activity-cliff diagnosis over the whole set at 0.85 similarity and 2 log units, and show me the worst offenders with both structures. I want to know whether these are real SAR or our data being dirty.

```
  all-pairs scan of 3224 compounds in 1.5s
  pairs at Tanimoto>=0.85: 667   activity cliffs found: 5 (0.75%)
    sim=1.000 gap=3.01  6.58 vs 9.59   [C@@H] vs [C@H] tropane ether — enantiomers
    sim=1.000 gap=3.00  8.70 vs 5.70   [C@@H] vs [C@H]            — enantiomers
    sim=0.891 gap=2.44  8.14 vs 5.70   diastereomer + N-substituent
    sim=0.915 gap=2.18  7.10 vs 4.92   ring-size and stereo change
    sim=0.982 gap=2.10  7.62 vs 5.52   SAME SMILES, one with a trailing `.Cl`
```

**Reading.** The function works and the framing is right — the Skill explicitly treats cliffs as an investigation with four possible causes rather than an error. But four of the five hits are enantiomer or diastereomer pairs that a chirality-blind Morgan fingerprint scores at 1.000, and the fifth is the same compound with an unstripped hydrochloride counter-ion. The Skill's Common Errors row blames cliff false positives on "bit-collisions inflate similarity", which is not what happened in any of the five.

Enantiomers differing by 3 log units in hERG potency are also a genuine and interesting result — this is exactly the "cryptic SAR" case the Skill names.

**Scores:** Basic 36/40 · Specialized 52/60 · **Total 88/100** · **Assertions 3/4**

---

## Input 5 — Stress

**Prompt**
> Two things at once. Pick me 100 maximally diverse compounds for a screening plate and prove they are more diverse than a random 100. Then run MCS on that diverse set and on ten close analogues, and tell me what happens when MCS has nothing to work with.

```
  LazyBitVectorPick 100 of 3224 in 0.00s; identical on repeat with seed=42: True
  different with seed=7: True (overlap 37/100)
  picker returned the first N inputs? False
  mean pairwise Tanimoto: MaxMin=0.094  random=0.132  (max MaxMin pair=0.172)

  MCS  10 close analogs      timeout=60s -> atoms=  8 bonds=  8 canceled=False  0.0s
       40 diverse compounds  timeout= 5s -> atoms=  2 bonds=  1 canceled=False  0.0s
       40 diverse compounds  timeout=60s -> atoms=  2 bonds=  1 canceled=False  0.0s
```

**Reading.** MaxMin behaves exactly as documented, including the seeding advice that prevents the "returns the first N inputs" failure the Skill warns about. MCS half-reproduces: the documented symptom ("returns small partial MCS") appeared, but not through the documented mechanism. `canceled=False` at both timeouts means rdFMCS converged immediately on a trivial two-atom fragment — the set genuinely has nothing in common. Raising the timeout, which is the Skill's prescribed fix, changes nothing.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100** · **Assertions 3/4**

---

## Input 6 — Scope Boundary

**Prompt**
> We standardised on 0.7 Tanimoto across the whole group. Someone wants to switch to MACCS because it is faster. Can we keep 0.7, or do we need a different number, and by how much?

```
  fp         claimed thr  mean sim   p95     p99     % pairs above claimed thr
  ECFP4      0.70         0.133      0.205   0.344                    0.094%
  FCFP4      0.60         0.185      0.299   0.455                    0.493%
  AtomPair   0.55         0.296      0.404   0.482                    0.603%
  MACCS      0.85         0.497      0.676   0.776                    0.396%
```

**Reading.** The Skill refuses the transfer and gives per-fingerprint starting points, explicitly labelled "repository starting heuristics, not universal equivalents". The measurement supports the refusal emphatically — MACCS mean pairwise similarity is 3.7x ECFP4's, so 0.7 would be meaningless there. It also shows the four quoted numbers are not a matched set: they retain between 0.094% and 0.603% of pairs, a 6.4x spread. The Skill is honest about them being heuristics but offers no procedure for picking one.

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100** · **Assertions 3/4**

---

## Input 7 — Adversarial

**Prompt**
> Your search says these two are identical — score 1.000 — but they are different compounds and one is ten times more potent. What is going on, and how do I stop it? While you are there, we have a million-compound vendor file coming; does your LSH route actually work or is it decoration?

**7a — the identity question**

```
  pairs with folded-ECFP4 Tanimoto = 1.0 but different canonical SMILES: 141
    CC(=O)N[C@@H]1CC(C)(C)Oc2nc(-c3ccc(Cl)cc3Cl)...  vs  [C@H] epimer
      identical unhashed sparse fingerprint too? True   identical InChIKey? False
    (three further pairs, all enantiomers/diastereomers, same result)
```

**Reading — the second real defect.** The Skill's failure mode says:

> **Mechanism:** A folded hashed fingerprint can map distinct atom environments to the same bits...
> **Fix:** For exact identity, compare canonical SMILES or InChIKey, not fingerprint. Use unhashed sparse fingerprint to disambiguate.

The observation is right — 141 such pairs — but the mechanism is wrong and the first fix fails. These are stereoisomers, and RDKit's Morgan generators default to `includeChirality=False`, so the *unhashed sparse* fingerprints are identical as well. The sparse-fingerprint fix cannot separate them; only the InChIKey half of the advice works. The correct first fix is `GetMorganGenerator(..., includeChirality=True)`. This is the same misdiagnosis that appears in the activity-cliff false-positive row (input 4).

**7b — the LSH route** (`tools\mhfp-venv`, verbatim from SKILL.md)

```
  LSHForestHelper import: OK
  built LSH forest over 1000 compounds in 12.1s
  query returned 10 neighbours: [0, 43, 57, 51, 48, 62, 59, 46, 63, 44]
  exact MHFP top-10:            [0, 43, 57, 51, 48, 62, 59, 46, 63, 44]
  LSH recall@10 vs exact: 10/10
```

`build_index` and `query_index` ran exactly as written, and the recall benchmark the Skill instructs the reader to perform is straightforward to run on its output. Note the environment caveat: `mhfp` raises `OverflowError` under numpy 2 (see the `bio-molecular-descriptors` audit), so this route needs a numpy-1.x environment — an upstream library limit, not a Skill defect, though the Skill's "mhfp 1.9+" pin does not mention it.

**Scores:** Basic 34/40 · Specialized 49/60 · **Total 83/100** · **Assertions 3/5**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-similarity-searching
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every snippet ran verbatim on 3,224 real compounds with no
                adaptation and no failures.
Contract     : PASS — return types match the documentation throughout, including
                the centroid-first convention of Butina.ClusterData.
Determinism  : PASS — the one order-sensitive step (Butina) is documented as such
                with a fix, and MaxMin is reproducible under the seed the Skill
                tells you to set.
Security     : PASS — no eval/exec, no network, no credentials.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12     Human Usability  :  8/8
Reliability            : 11/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 11/12
Agent Usability        : 14/16     Agent-Specific   : 19/20
Static Subtotal        : 92/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — the Butina cutoff claim, the hardest thing it
                        asserts, is exactly right on real data.
Practice Boundaries   : PASS — compound ranking only.
Methodological Ground : PASS — leads with the activity-cliff caveat and the data
                        bear it out (two pairs at 1.000 differing by 3 log units).
Code Usability        : PASS — every snippet ran first time.

── STEP 8: Final Score ───────────────────────────
Static Score   : 92.0 × 40% = 36.8
Dynamic Score  : 89.3 × 60% = 53.6
FINAL SCORE    : 90 / 100
Floors         : Static ≥80 ✓ (92) · Execution ≥85 ✓ (89.3) · Layer 1 avg ≥32 ✓ (36.6)
                 Layer 2 avg ≥48 ✓ (52.7) · Assertion rate ≥90 % ✗ (79.3 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. Five of the six
                 failures come from the failure-mode section, where the method
                 content is right and the causal explanations are not.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] The "Tanimoto = 1.0" failure mode has the wrong cause and a fix that does not work** (inputs 4, 7) — 141 pairs are stereoisomers, not hash collisions, and their unhashed sparse fingerprints are identical too. Fix: lead with `includeChirality=True`, keep InChIKey, demote collisions to a secondary cause, and repeat the note in the activity-cliff false-positive row together with a salt-stripping reminder.
- **[P2] MCS failure mode describes a timeout that does not occur** (input 5) — `canceled=False` at 5 s and 60 s. Fix: split the symptom on `result.canceled` and say that a small MCS with `canceled=False` means pre-cluster, not raise the timeout.
- **[P2] No precision expectation for Tversky substructure-like search** (input 3) — 12% of hits above 0.7 contain the query fragment. Fix: instruct a SMARTS confirmation step.
- **[P2] Per-fingerprint thresholds are not iso-selective and no calibration procedure is given** (input 6) — 6.4x spread. Fix: pick the threshold at a library percentile rather than quoting a number.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/similarity_search.py`. It exists and every capability it covers was exercised through the SKILL.md snippets during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**

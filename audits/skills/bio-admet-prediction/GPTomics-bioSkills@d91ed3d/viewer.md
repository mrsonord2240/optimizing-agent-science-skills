> **Audit record for `bio-admet-prediction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/admet-prediction) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-admet-prediction

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/admet-prediction`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex → N = 7
Environment: shared venv (RDKit 2026.03.6); `tools\admet-ai-venv` (admet-ai 2.0.1, offline, weights bundled); `tools\chemprop-venv` (chemprop 2.3.1).
Real data: 300 ChEMBL hERG (CHEMBL240) compounds stratified across the measured pChEMBL range, plus 9 out-of-distribution probes.
Inputs executed: **6 / 7** — input 2 could not be executed because the Skill ships no API route for its declared primary tool.
Code: `run/prep_admet_inputs.py`, `run/analyse_admet.py`, `run/input2_admetlab_static.py`. Output: `run/analyse_admet.out`, `run/input2_static.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 53 | 90 | 3/4 | ✅ |
| 2 | Variant A | **no** | 27 | 37 | 64 | 2/4 | ❌ PARTIAL |
| 3 | Variant B | yes | 35 | 50 | 85 | 3/4 | ✅ |
| 4 | Edge | yes | 37 | 55 | 92 | 4/5 | ✅ |
| 5 | Stress | yes | 37 | 54 | 91 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 38 | 53 | 91 | 4/4 | ✅ |
| 7 | Adversarial | yes | 35 | 49 | 84 | 3/5 | ✅ |

**Execution Average: 85.3 / 100**
**Assertion Pass Rate: 23/30 (76.7 %)**

---

## Input 1 — Canonical

**Prompt**
> Here are 300 compounds off a hERG-focused series. Give me the standard triage pass — drug-likeness, Veber, the BBB screen, and structural alerts — and do not silently drop anything; I want the alert descriptions so I can argue about them with the chemists.

**Generated code:** the two executable SKILL.md snippets, `druglike_score(mol)` and `alerts(mol, catalogs=('PAINS_A','BRENK','ZINC'))`, verbatim.

```
  druglike_score ran on 300/300 molecules, 10 fields each
          MW  LogP    TPSA   QED  Lipinski_violations  n_alerts
mean  429.93  4.27   61.86  0.57                 0.49      0.38
  Lipinski 0 violations: 196/300   Veber pass: 282/300   BBB simple screen: 216/300
  at least one structural alert: 92/300 (alerts() returns descriptions, never deletes)
  most common: {'Aliphatic_long_chain': 48, 'Non-Hydrogen_atoms': 17,
                'Oxygen-nitrogen_single_bond': 8, 'nitro_group': 5, '2-halo_pyridine': 5}
  BBB simple screen vs ADMET-AI BBB_Martins: AUC 0.769
```

**Reading.** Clean, and consistent with the Skill's own framing — `alerts()` returns reasons and deletes nothing, and the 3-rule BBB screen behaves like the heuristic the Skill says it is (AUC 0.769, not a model). But note what this canonical output is: a physicochemical and structural-alert profile. No ADMET endpoint was predicted, because the Skill ships no route that can predict one. The BBB_Martins column used for the cross-check came from ADMET-AI, for which the Skill provides no code.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100**
**Assertions:** 3/4 — **FAIL** on "the canonical triage output includes an actual ADMET model prediction".

---

## Input 2 — Variant A ❌ (not executed)

**Prompt**
> Batch our 300 compounds through ADMETlab 3.0 and bring back the 119 features with the uncertainty columns intact, so we can rank on predicted hERG and DILI with the confidence bands attached.

**Why it was not executed.** The Skill's ADMETlab section contains no request, no endpoint, no payload and no task identifier. Its entire code block is:

```python
results = pd.read_csv('admetlab3_results.csv')
# Preserve the uncertainty columns and task identifier in downstream reports.
```

The prose says to "follow the live official API tutorial" and warns three times against hard-coding an unofficial route. That is a defensible decision — a stale hard-coded client would be worse — but it means the declared `primary_tool` has no executable path and no output contract, so the documented route is recorded as **`executed: false`**.

**What was executed instead** (static evidence for Research Veto M4):

```
example parses: True; functions: ['load_admetlab_results', 'calculate_druglikeness',
  'flag_pains', 'flag_structural_alerts', 'annotate_compounds', 'batch_druglikeness']
load_admetlab_results on a non-empty file -> shape (1, 5)
empty file   -> ValueError raised as documented: ADMETlab result file contains no predictions
missing file -> FileNotFoundError (unhandled by the Skill)
  - a completely unrelated CSV also passes: (2, 1)
  - 'Preserve the uncertainty columns and task identifier' has no code behind it and no check.
```

**Scores:** Basic 27/40 · Specialized 37/60 · **Total 64/100** (Code Executability 8/15 — it parses and its one documented error path works, but the route it exists to serve cannot be reached)
**Assertions:** 2/4 — **FAIL** on executability of the route and on the column contract.

---

## Input 3 — Variant B

**Prompt**
> We have 3,000 in-house hERG measurements. Walk me through training our own model with the chemprop route in your skill, and tell me what I get for uncertainty — and how to make the run reproducible, because the last person's numbers moved every time.

**What ran.** Every flag in the Skill's commented CLI block was checked against `chemprop train --help` on 2.3.1, and a real model was trained with them (the run lives in the sibling `bio-qsar-modeling` audit, `run/chemprop_train.out`).

```
  --split-type {SCAFFOLD_BALANCED,...}   valid alias of --split      OK
  --molecule-featurizers v1_rdkit_2d_normalized   in the choice list OK
  --num-replicates / --ensemble-size                                 OK
  chemprop predict --uncertainty-method ensemble  -> pred_0_unc col  OK
  scaffold-split test ROC across the 4 trained models: 0.743 0.735 0.776 0.780

  chemprop train ... --seed 42
  -> chemprop: error: unrecognized arguments: --seed 42
     (2.3.1 offers --data-seed and --pytorch-seed)
```

**Reading.** The training route is real and the flags are current, including the `--split-type` spelling that looked like a 1.x leftover but is a live alias. The reproducibility advice in the Common Errors table is the one thing that fails — and it fails on exactly the question the prompt asked. The same `--seed 42` error appears in `chemoinformatics/qsar-modeling`.

**Scores:** Basic 35/40 · Specialized 50/60 · **Total 85/100** · **Assertions 3/4**

---

## Input 4 — Edge

**Prompt**
> Before we let this drive any go/no-go call: run the hERG endpoint over 300 compounds whose IC50 we have already measured, and tell me what happens if we use the usual "probability above 0.5, drop it" rule.

```
  measured blocker at pChEMBL>=5.0: 243/300 positives, ADMET-AI hERG AUC=0.711
  measured blocker at pChEMBL>=6.0: 182/300 positives, AUC=0.689
  Spearman(predicted prob, measured pChEMBL) = 0.304

  predicted prob > 0.5: 293 compounds, 53 measured pChEMBL < 5  -> 18.1% false kill
  predicted prob > 0.7: 271 compounds, 43 measured pChEMBL < 5  -> 15.9% false kill
  predicted prob > 0.9: 204 compounds, 26 measured pChEMBL < 5  -> 12.7% false kill
  predicted prob <= 0.5: 7 compounds, 1 of which is a measured sub-100 nM blocker
```

**Reading — the most useful result in this audit.** The Skill's table reports hERG AUCs of 0.86–0.956 from the source studies, each attributed to that study's own benchmark and split. On an independent external set the observed AUC is 0.711. The Skill's discipline of never generalising those numbers is what makes this a confirmation rather than a contradiction — and its rule that "a single-model probability > 0.5 is NOT a kill signal" is vindicated at 18.1% false kills, still 12.7% at a 0.9 threshold.

The one thing it cannot deliver is the ability to tell *which* prediction to distrust: its prescribed mitigation is an uncertainty band that the runnable route does not emit (input 7).

**Scores:** Basic 37/40 · Specialized 55/60 · **Total 92/100** · **Assertions 4/5**

---

## Input 5 — Stress

**Prompt**
> DDI review wants the full CYP panel on this set. Give me inhibitor and substrate calls for all five isoforms and tell me how many compounds we cannot cleanly classify.

```
  CYP3A4: inhibitor>0.5 117  substrate>0.5 272  BOTH>0.5 115 (38.3%)  corr +0.539
  CYP2D6: inhibitor>0.5 178  substrate>0.5 133  BOTH>0.5 108 (36.0%)  corr +0.620
  CYP2C9: inhibitor>0.5  37  substrate>0.5   0  BOTH>0.5   0 (0.0%)   corr +0.397
  CYP1A2 / CYP2C19 / CYP2C9 / CYP2D6 / CYP3A4 inhibitor models all present
```

**Reading.** The Skill's "CYP3A4 inhibitor + substrate ambiguity" failure mode states the symptom as "Both classes report > 0.5". That is 38.3% of a real 300-compound set for CYP3A4 and 36.0% for CYP2D6. Its fix — keep the two models separate and flag the both-high set for in vitro confirmation — is directly actionable on this output. It also declines to invent a probability threshold, writing "Model-specific threshold" in every row of the CYP table.

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100** · **Assertions 4/4 PASS**

---

## Input 6 — Scope Boundary

**Prompt**
> Cut through it for me: the hERG number is 0.3 and DILI is low. Is this compound safe to dose?

**Response under the Skill.** It refuses, and it refuses structurally rather than with a disclaimer. The hERG section states that a single-model probability is not a kill signal in either direction, names ICH S7B/E14 as the governing guidance rather than the model output, requires in vitro patch-clamp for a clinical candidate even when the model is reassuring, and explicitly declines to give a universal safe/unsafe IC50 cutoff. Input 4's numbers make that concrete from the other side: of the 7 compounds scoring below 0.5, one is a measured sub-100 nM blocker.

```
  SKILL.md contains 'NOT a kill signal': True
  ... 'confirm important decisions experimentally': True   ... 'ICH S7B': True
  ... 'in vitro patch-clamp': True    ... 'do not exclude pre-emptively': True
  ... 'regulatory conclusion': True   ... 'universal safe/unsafe IC50 cutoff': True
  occurrences of 'patient' / 'dose the patient' / 'prescrib': 1 / 0 / 0
```

**Scores:** Basic 38/40 · Specialized 53/60 · **Total 91/100** · **Assertions 4/4 PASS**

---

## Input 7 — Adversarial

**Prompt**
> Our chemistry is not standard drug-like — we have a PROTAC series, two macrocycles and a peptide, and someone put cisplatin and a salt control in the plate map. Run them through and tell me what to believe.

```
  compound                                          hERG    AMES    DILI  BBB_Martins  Caco2
  drug control: atenolol                           0.144   0.078   0.067       0.555  -5.283
  drug control: astemizole (known hERG blocker)    0.995   0.248   0.350       0.969  -5.091
  macrocycle: erythromycin-like lactone            0.181   0.036   0.384       0.702  -4.398
  macrocycle: cyclic hexapeptide                   0.003   0.246   0.198       0.516  -6.762
  peptide: linear tetrapeptide                     0.604   0.584   0.188       0.752  -5.601
  PROTAC-like: VHL ligand + linker + warhead       0.959   0.198   0.912       0.302  -5.472
  metal complex: cisplatin                         0.250   0.905   0.359       0.987  -4.396
  inorganic: sodium chloride                       0.017   0.672   0.094       0.967  -4.518
  very large: paclitaxel                           0.826   0.435   0.812       0.361  -5.563

  columns matching uncertainty/AD keywords: NONE
  total output columns: 105 (of which 52 are DrugBank percentiles)
```

**Reading.** The drug controls behave (atenolol low, astemizole 0.995), which makes the rest more damning: sodium chloride is assigned a 0.967 probability of crossing the blood-brain barrier and a 0.672 AMES probability, and cisplatin gets AMES 0.905. The Skill names exactly this chemistry in its out-of-distribution failure mode — "metal-containing complexes, many peptides, PROTACs, or unusual macrocycles" — which is a real credit. But its prescribed fix is "Check uncertainty band; if interval is broad, do not trust point estimate", and the route that can be executed emits no uncertainty column, no applicability-domain flag and no refusal. The mitigation exists only on the hosted service the Skill cannot reach.

**Scores:** Basic 35/40 · Specialized 49/60 · **Total 84/100** · **Assertions 3/5**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-admet-prediction
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 6/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every function the Skill ships executed; 300 compounds and 9
                OOD probes processed without a failure.
Contract     : PASS — frontmatter complete. Noted: load_admetlab_results has no
                column contract, which is a reliability defect rather than a
                frontmatter/schema breach.
Determinism  : PASS — the rule-based path is deterministic; ADMET-AI reproduced
                identical values on re-read of its saved output.
Security     : PASS — no hard-coded credentials, and SwissADME's terms of use are
                treated as a real constraint.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability :  8/12     Human Usability  :  7/8
Reliability            : 10/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 11/12
Agent Usability        : 14/16     Agent-Specific   : 19/20
Static Subtotal        : 88/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — every AUC attributed to a study and a split; the
                        independent external AUC of 0.711 vindicates that discipline.
Practice Boundaries   : PASS — the strongest boundary content in this candidate.
Methodological Ground : PASS — inhibitor/substrate separation, correlated-model
                        independence, PAINS-not-a-kill-filter, ensemble≠calibration.
Code Usability        : PASS — everything shipped runs; the gap is coverage.

── STEP 8: Final Score ───────────────────────────
Static Score   : 88.0 × 40% = 35.2
Dynamic Score  : 85.3 × 60% = 51.2
FINAL SCORE    : 86 / 100
Floors         : Static ≥80 ✓ (88) · Execution ≥85 ✓ (85.3) · Layer 1 avg ≥32 ✓ (35.1)
                 Layer 2 avg ≥48 ✓ (50.1) · Assertion rate ≥90 % ✗ (76.7 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. The pattern behind the
                 seven failures is consistent and worth stating plainly: this Skill
                 reasons about ADMET better than it predicts ADMET.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] No executable ADMET prediction route ships with the Skill** (inputs 1, 2) — three of four named tools have no code; the primary tool has no request. Fix: add a ten-line ADMET-AI section; it is fully offline and covers hERG, five CYPs, DILI, AMES, Caco-2 and BBB.
- **[P1] The prescribed OOD mitigation is unavailable in the runnable route** (inputs 4, 7) — "check the uncertainty band" against 105 columns containing none. Fix: a toolkit-independent AD gate (max Tanimoto to a reference set plus an element/heavy-atom sanity filter that rejects inorganics before prediction).
- **[P2] chemprop reproducibility advice names a flag that does not exist** (input 3) — `--seed 42` is rejected; use `--data-seed` and `--pytorch-seed`. Same error in `qsar-modeling`.
- **[P2] `load_admetlab_results` enforces no column contract** (input 2) — an unrelated CSV passes; a missing file gives an unhandled `FileNotFoundError`.
- **[P2] ADMET-AI pin (`1.3+`) admits the version the Skill itself warns diverges** — reconcile Version Compatibility with the taxonomy-table warning.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/predict_admet.py`. It exists (137 lines), parses, and all six of its functions were imported and executed during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.** The gap here is not a missing file but a missing route: the declared `primary_tool` has no code.

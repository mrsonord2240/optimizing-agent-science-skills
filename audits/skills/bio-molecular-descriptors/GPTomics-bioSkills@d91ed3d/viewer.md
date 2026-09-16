> **Audit record for `bio-molecular-descriptors`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/molecular-descriptors) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-molecular-descriptors

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/molecular-descriptors`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex (fingerprints, 3D, charges, physchem, rule sets, QED — six task types with branching choice tables) → N = 7
Environment: shared venv (RDKit 2026.03.6, numpy 2.5.3, pandas 3.0.5); `tools\mhfp-venv` for the MHFP6 probe. Real data: ChEMBL hERG CHEMBL240, 3,224 distinct compounds.
Inputs executed: **7 / 7**
Code: `run/inputs_all.py`, `run/probe_mhfp.py`. Output: `run/inputs_all.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 54 | 92 | 4/4 | ✅ |
| 2 | Variant A | yes | 37 | 52 | 89 | 4/5 | ✅ |
| 3 | Edge | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 4 | Variant B | yes | 30 | 38 | 68 | 3/5 | ⚠️ |
| 5 | Stress | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 37 | 53 | 90 | 3/4 | ✅ |
| 7 | Adversarial | yes | 36 | 50 | 86 | 3/5 | ✅ |

**Execution Average: 87.3 / 100**
**Assertion Pass Rate: 25/31 (80.6 %)**

---

## Input 1 — Canonical

**Prompt**
> Take the first thousand compounds from our hERG set and give me the standard property panel — MW, cLogP, HBD/HBA, TPSA, rotatable bonds, aromatic rings, Fsp3, QED — then tell me how they sit against Ro5, Veber, Egan, lead-like and Ro3. I want to know how much of this collection is actually lead-like before we commit to it.

```
  computed 9 descriptors x 1000 mols in 2.4s
        MolWt  MolLogP  HBD    HBA    TPSA  RotBonds  AromRings  FractionCSP3   QED
mean   446.80     4.24  1.0   4.94   69.05      5.68       2.97          0.37  0.53
max   1071.40     9.15  5.0  14.00  206.59     21.00       7.00          1.00  0.93
  Lipinski Ro5: 0 violations=629  1=213  >=2=158
  Veber 954/1000 · Egan 884/1000 · lead-like 29/1000 · Ro3 fragment 9/1000
  QED >= 0.5: 555/1000   QED nan: 0    BBB TPSA<=90: 773/1000
```

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100**
**Assertions:** 4/4 PASS — all nine calls resolve; thresholds transcribed correctly; no nan/inf; rule sets framed as risk indicators (which matters: 371/1,000 real hERG actives violate at least one Ro5 criterion).

---

## Input 2 — Variant A

**Prompt**
> Build one of every fingerprint in your taxonomy table for atenolol so I can see what I am choosing between — sizes, on-bits, and whether the count form actually carries anything the bit form does not. Include MAP4 and MHFP6; the taxonomy table sells them for diverse libraries and I want to see them work.

```
  ECFP4      nBits= 2048 on=  37 count-vector nonzero=  37
  ECFP6      nBits= 2048 on=  47 count-vector nonzero=  47
  FCFP4      nBits= 2048 on=  32 count-vector nonzero=  32
  RDKitFP    nBits= 2048 on= 309 count-vector nonzero= 309
  AtomPair   nBits= 2048 on= 155 count-vector nonzero= 109
  TopTorsion nBits= 2048 on=  23 count-vector nonzero=  15
  MACCS      nBits=167  bit0=False
  Avalon     nBits=1024 on=77
  FCFP4 != ECFP4: True

  map4: NOT INSTALLABLE -- ModuleNotFoundError: No module named 'map4'
  mhfp: has encode_mol? True; has encode? True
```

Separate probe (`run/probe_mhfp.py`), both venvs:

```
--- shared venv (numpy 2.5.3) --- encode_mol FAILED: OverflowError: Python int too large to convert to C long
--- mhfp-venv (numpy 1.26.4) --- encode_mol OK -> len=2048; MHFPEncoder.distance -> 0.2783
```

**Reading.** The MHFP6 snippet is API-correct — `MHFPEncoder(2048).encode_mol(mol, radius=3)` is exactly right and the `distance` call works. The failure under numpy 2 is an upstream `mhfp` bug, not a Skill defect, but the Skill pins "numpy 1.26+", which admits numpy 2 and therefore admits the break. MAP4 is different: `pip` reports no version of `map4` on PyPI at all, yet Version Compatibility says the examples were "tested with ... map4 1.1+". That claim cannot be true.

**Scores:** Basic 37/40 · Specialized 52/60 · **Total 89/100**
**Assertions:** 4/5 — **FAIL** on "every fingerprint in the table can be constructed with the documented API" (map4).

---

## Input 3 — Edge

**Prompt**
> Two things I want checked rather than believed. Your table says the ECFP number is a diameter and RDKit takes the radius — show me that. And you refuse to give me a collision rate and tell me to measure it, so measure it: 512 through 8192 bits, and tell me whether 2048 is actually the right default for this library.

```
  nBits=  512 mean on-bits= 53.1  distinct environments= 56.1  ->  5.38% lost
  nBits= 1024 mean on-bits= 54.4                                ->  2.95% lost
  nBits= 2048 mean on-bits= 55.0                                ->  1.89% lost
  nBits= 4096 mean on-bits= 55.6                                ->  0.85% lost
  nBits= 8192 mean on-bits= 55.8                                ->  0.44% lost

  ECFP0 (radius=0) distinct environments on atenolol = 11
  ECFP2 (radius=1) = 26   ECFP4 (radius=2) = 38   ECFP6 (radius=3) = 48
```

**Reading.** The Skill's most distinctive editorial decision — refusing to quote a fixed collision rate and telling you to measure — is vindicated: the loss spans an order of magnitude across the sizes it declines to rank. At the recommended 2048 the loss is 1.89%, and halving it costs 4x the memory.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 4 — Variant B ⚠️

**Prompt**
> We need 3D shape descriptors for atenolol and verapamil for a shape-aware model. Follow your own ensemble recipe — 20 ETKDGv3 conformers, MMFF optimised, asphericity across the ensemble — and tell me how much the value moves between conformers so I know whether a single conformer would have been enough.

**Generated code:** the SKILL.md *3D Descriptors and Conformer Dependence* snippet, verbatim, including its three guards.

```
  atenolol (8 rot bonds)    confs=20 non-converged=19  asphericity mean=0.729 sd=0.068 range=[0.614,0.824]
      -> SKILL.md would raise RuntimeError and discard all 20 conformers because 19 did not converge
  butanol (SKILL.md example) confs=20 non-converged= 0  asphericity mean=0.531 sd=0.166 range=[0.278,0.718]
  verapamil (13 rot bonds)  confs=20 non-converged=20  asphericity mean=0.574 sd=0.085 range=[0.386,0.741]
      -> SKILL.md would raise RuntimeError and discard all 20 conformers because 20 did not converge
  ferrocene-like: MMFF94 params unavailable (SKILL.md raises ValueError here)  [guard correct]

  single-conformer reproducibility (examples/calculate_descriptors.py path):
    3 independent runs: [0.7876, 0.7216, 0.721]  identical=False
```

**Reading — the most important finding in this audit.** The snippet contains

```python
optimization_results = AllChem.MMFFOptimizeMoleculeConfs(mol)
if any(status != 0 for status, _ in optimization_results):
    raise RuntimeError('MMFF94 optimization did not converge for every conformer')
```

RDKit returns status `1` for "more iterations required", not for failure — the geometry is optimised, it simply has not hit the convergence criterion within the default 200 iterations. For atenolol that is 19 of 20 conformers and for verapamil 20 of 20, so the Skill's own recipe throws away a perfectly usable ensemble for any flexible drug-like molecule. The only molecule in this test that survives the guard is the four-carbon alcohol the Skill uses as its example. The example file's single-conformer helper carries the same guard and additionally omits `randomSeed`, so it is non-reproducible.

The asphericity spread itself vindicates the Skill's conformer-dependence warning — 0.614 to 0.824 for atenolol — which makes the broken guard more costly, not less: the ensemble is exactly what you need and exactly what the code discards.

**Scores:** Basic 30/40 (Functional Correctness 5/10) · Specialized 38/60 (Methodological Validity 14, Code Executability 8, Data QC 6, Reproducibility 5, Security 5) · **Total 68/100**
**Assertions:** 3/5 — **FAIL** on "returns descriptors for a flexible drug-like molecule" and on "the 3D path is reproducible across runs".

---

## Input 5 — Stress

**Prompt**
> Featurize the whole collection for a QSAR run — ECFP4 2048 plus the property panel — and tell me what it costs and whether the matrix is mostly empty at that bit size.

```
  ECFP4 2048 for 3224 mols: 0.4s (8106 mol/s), matrix (3224, 2048) 6.6 MB
  bits never set across the library: 8/2048   mean on-bits/mol 55.4
  9-descriptor panel for 3224 mols: 7.4s
  nan/inf in the descriptor panel: 0 nan, 0 inf
```

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 6 — Scope Boundary

**Prompt**
> Management wants one number. Can we just gate the whole pipeline on QED ≥ 0.5 and move on? Run it over our drugs, our fragment set and the natural-product arm and tell me.

```
  aspirin  0.550   atenolol 0.638   imatinib 0.389
  indole   0.544   phenol   0.515   benzamidine 0.421
  paclitaxel 0.130  peptide 0.301   Na+ 0.247   EDTA(4-) 0.356
```

**Reading.** The Skill answers no, and the numbers show why with unusual clarity: a QED ≥ 0.5 gate keeps indole and phenol — bare fragments — and discards imatinib, a marketed drug. The Skill's stated caveat is that QED "can under-rank fragment-like or natural-product-like molecules". The natural-product half is exactly right (paclitaxel 0.130). The fragment half is backwards: the desirability functions are permissive for small molecules, so fragments are over-ranked, not under-ranked.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100**
**Assertions:** 3/4 — **FAIL** on "the caveat covers the failure direction actually observed for fragments".

---

## Input 7 — Adversarial

**Prompt**
> The charges from your pipeline look wrong — they do not add up to zero on a neutral molecule, and our iron-containing series came through with suspiciously round numbers. Also: is the LogP you are giving me the same one PubChem shows? And why is my MolWt off by 0.1 from theirs?

```
  Gasteiger on aspirin: 13 charges, sum=-0.6555 (formal charge 0), min=-0.478 max=+0.339
  Gasteiger on [Fe+2].[Fe+2]: [2.0, 2.0] -> finite values returned
  Crippen MolLogP(aspirin) = 1.31   (experimental 1.19; SKILL.md: Crippen != XLogP3)
  MolWt=180.159  ExactMolWt=180.0423  difference=+0.117
  MACCS: full=167  sliced[1:]=166
```

**Reading.** The two questions the Skill anticipated — which LogP model, and average versus monoisotopic mass — it answers correctly from its Common Errors table. The two it did not anticipate are both in its own Gasteiger snippet: the printed heavy-atom charges do not balance because implicit hydrogens carry charge separately and `AddHs` is never mentioned, and an element outside the Gasteiger parameter set silently gets its formal charge echoed back as a "partial charge".

**Scores:** Basic 36/40 · Specialized 50/60 · **Total 86/100**
**Assertions:** 3/5 — **FAIL** on charge balance and on the unparameterised-element case.

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-molecular-descriptors
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — the 2D paths ran 3,224 molecules with zero failures. The 3D
                path's exception is a logic defect, not instability: it raises on
                its own valid output, deterministically.
Contract     : PASS — frontmatter complete; every documented return shape matched.
Determinism  : PASS, with a recorded P1. The Skill does supply a seed mechanism and
                SKILL.md uses it (params.randomSeed = 42). The shipped example's
                calculate_3d_descriptors omits it and returned three different
                asphericities on three identical calls. Because the primary
                documented pattern seeds correctly, this is scored as a P1 defect
                rather than a T3 veto; a reviewer who weighs the shipped helper
                equally could reasonably call it FAIL.
Security     : PASS — no eval/exec, no network, no credentials.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 10/12     Human Usability  :  7/8
Reliability            :  7/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 10/12
Agent Usability        : 14/16     Agent-Specific   : 18/20
Static Subtotal        : 85/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — five widespread myths explicitly corrected with
                        citations; the collision measurement vindicates the refusal
                        to quote a fixed rate.
Practice Boundaries   : PASS — featurisation only.
Methodological Ground : PASS — radius/diameter, bit-vs-count, MinHash distance and
                        conformer dependence all correct and all reproduced.
Code Usability        : PASS — every API exists and runs; the 3D defect is wrong
                        logic, not unrunnable code. MAP4 is the one unobtainable
                        dependency.

── STEP 8: Final Score ───────────────────────────
Static Score   : 85.0 × 40% = 34.0
Dynamic Score  : 87.3 × 60% = 52.4
FINAL SCORE    : 86 / 100
Floors         : Static ≥80 ✓ (85) · Execution ≥85 ✓ (87.3) · Layer 1 avg ≥32 ✓ (36.3)
                 Layer 2 avg ≥48 ✓ (51.0) · Assertion rate ≥90 % ✗ (80.6 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. Input 4 is the real
                 weakness — the 3D route is the one part of this Skill that does not
                 work on ordinary molecules.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] 3D convergence guard rejects valid ensembles** (input 4) — MMFF status 1 means "more iterations", not failure. Fix: `maxIters=2000`, treat status 1 as a warning, raise only when all conformers fail, and exercise the path in the example's `__main__`.
- **[P1] `map4` pinned in Version Compatibility but has no obtainable distribution** (input 2). Fix: drop the pin, mark the taxonomy row accordingly, point at `mapchiral`.
- **[P1] The example's 3D helper is unseeded** (input 4) — 0.7876/0.7216/0.7210 on three identical calls. Fix: set and expose `randomSeed`.
- **[P2] Gasteiger snippet prints charges that do not sum to the formal charge** (input 7) — `AddHs` never mentioned.
- **[P2] No warning that Gasteiger echoes formal charge for unparameterised elements** (input 7) — `[Fe+2]` returns 2.0 silently.
- **[P2] QED caveat states the wrong failure direction for fragments** (input 6) — fragments are over-ranked, not under-ranked.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/calculate_descriptors.py`. It exists (150 lines) and every function in it was executed during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.** Note separately that `map4`, named as a tested dependency, is not obtainable — a dependency problem, not a missing-file problem.

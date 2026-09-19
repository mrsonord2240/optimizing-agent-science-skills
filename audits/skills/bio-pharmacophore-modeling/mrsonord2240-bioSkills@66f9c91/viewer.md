> **Audit record for `bio-pharmacophore-modeling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@66f9c91](https://github.com/mrsonord2240/bioSkills/tree/66f9c917d8954cf128a856fd4c1e5c2644b321a6/chemoinformatics/pharmacophore-modeling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pharmacophore-modeling (RE-AUDIT)
Generated: 2026-09-19
Re-audit of a fix pass. Original audit: 86, Production Ready (`F:\OpenScience\audits\_pre-fix-20260919\bio-pharmacophore-modeling\`).
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-pharmacophore-modeling.md`. Fix commit: `66f9c91` on `fix/cg-pharm`.

This re-audit is by a fresh, independent agent. All 4 fixed findings were re-verified by real
execution on molecules/structures the fixer did not use (not a re-run of the fixer's own tests),
plus 2 wholly new inputs and a normal static/dynamic re-audit pass.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 50 | 87 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 46 | 81 | 3/4 PASS | ⚠️ |
| 3 | Edge | 39 | 54 | 93 | 4/4 PASS | ✅ |
| 4 | Variant B | 38 | 52 | 90 | 3/3 PASS | ✅ |
| 5 | Stress | 36 | 48 | 84 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 49 | 86 | 3/3 PASS | ✅ |
| 7 | Adversarial (review) | 36 | 49 | 85 | 4/4 PASS | ✅ |

**Execution Average: 86.6 / 100**
**Assertion Pass Rate: 25/26**

## Fix Verification Summary

| # | Fixer's claim | Independently re-verified how | Result |
|---|---|---|---|
| 1 | `params.randomSeed = 23` added to both `EmbedMultipleConfs` and `EmbedMolecule` in `examples/pharmacophore.py` | Ran both code paths twice as fully independent `python.exe` processes; SHA-256 of all conformer coordinates diffed | **Bit-identical across both runs, both call sites.** T3 determinism veto: PASS. |
| 2 | `has_feature_types` now returns `(is_match, missing_feature_types)`; diagnostic printed per rejected molecule | Re-ran on a different query/library pair (indinavir/saquinavir vs ritonavir + 4 unrelated real drugs, not the fixer's own test molecules) and again on a 10-molecule scaled library | **Diagnostic correct and deterministic.** Ritonavir still rejected (expected — diagnosis, not a retrieval fix); missing-feature tuples verified against real RDKit `FeatureFactory` output. |
| 3 | Common Errors row added for PLIP's `inchikey` ValueError on Windows/openbabel-wheel | Reproduced the raw, unpatched `ValueError: inchikey is not a recognised Open Babel format` on real PDB 1HSG; then applied the row's own documented monkeypatch on a **second, different** real structure (PDB 3PTB) | **Error text matches exactly; documented fix generalizes** beyond the one structure the fixer checked. |
| 4 | `# PLACEHOLDER COORDINATES` warning added above demo `query_features` | Reviewed placement and wording in SKILL.md directly (doc-only fix, nothing to execute) | **Present, correctly placed, cites the real enrichment=0.5 finding.** |

## Detailed Outputs

### Input 1 — Canonical (regression, documented-fix path)
**Command:** PLIP `PDBComplex.analyze()` on real `data/1hsg.pdb`, using exactly the monkeypatch text now in SKILL.md's Common Errors table.
**Output:** `h-bonds: 6 | hydrophobic: 15 | salt bridges: 2 | water bridges: 4` — matches the pre-fix audit's finding exactly.
**Scores:** Basic: 37/40 | Specialized: 50/60 | Total: 87/100

### Input 2 — Variant A (diagnostic, independent molecules)
**Command:** `feature_family_prefilter([indinavir, saquinavir], [ritonavir, caffeine, metformin, aspirin, acetaminophen])`
**Output:**
```
Rejected (missing query feature types):
  <ritonavir SMILES>: missing [('LumpedHydrophobe', 'tButyl'), ('PosIonizable', 'BasicGroup')]
  <caffeine>: missing [...]
  <metformin>: missing [...]
  <aspirin>: missing [('LumpedHydrophobe', 'tButyl'), ('PosIonizable', 'BasicGroup')]
  <acetaminophen>: missing [('LumpedHydrophobe', 'tButyl'), ('PosIonizable', 'BasicGroup')]
HITS: []
```
**Scores:** Basic: 35/40 | Specialized: 46/60 | Total: 81/100

### Input 3 — Edge (EmbedMolecule determinism)
**Output:** Run 1 and Run 2 SHA-256 hash of `EmbedMolecule` conformer coordinates: `ab3b8443...90ff9eb7` — identical both runs. SKILL.md's own `EmbedPharmacophore` code block: `can_match=True`, embeddings produced.
**Scores:** Basic: 39/40 | Specialized: 54/60 | Total: 93/100

### Input 4 — Variant B (EmbedMultipleConfs determinism)
**Output:** Run 1 and Run 2 SHA-256 hash of 20-conformer `EmbedMultipleConfs` coordinates: identical. Full demo `__main__` stdout diffed byte-for-byte across runs: no differences.
**Scores:** Basic: 38/40 | Specialized: 52/60 | Total: 90/100

### Input 5 — Stress (scaled diagnostic, 10 real molecules)
**Command:** `feature_family_prefilter([nelfinavir, amprenavir], <10 real diverse drugs>)`, run twice.
**Output:** `N_LIBRARY: 10 | N_HITS: 6` — identical across both runs; 4 rejects each correctly diagnosed.
**Scores:** Basic: 36/40 | Specialized: 48/60 | Total: 84/100

### Input 6 — Scope Boundary (new structure, documented workaround)
**Command:** PLIP `analyze()` on real PDB 3PTB (trypsin + benzamidine — not used in the original audit), with the SKILL.md-documented monkeypatch applied.
**Output:** `total interaction records: 9`, classes `['hbond', 'hydroph_interaction', 'metal_complex']` — completed without raising.
**Scores:** Basic: 37/40 | Specialized: 49/60 | Total: 86/100

### Input 7 — Adversarial (placeholder-warning review, doc-only)
**Review:** `# PLACEHOLDER COORDINATES -- do not reuse without deriving from a validated workflow` sits immediately above `query_features = [` in SKILL.md's Ligand-Based Pharmacophore block (lines 86-88), citing the real enrichment=0.5 finding.
**Scores:** Basic: 36/40 | Specialized: 49/60 | Total: 85/100

## Final Score

```
Static Score   : 89/100 x 40% = 35.6
Dynamic Score   : 86.6/100 x 60% = 52.0
FINAL SCORE    : 88 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto override  : false
```

**Change from pre-fix audit: 86 -> 88, Production Ready -> Production Ready (confirmed, T3 determinism now positively verified rather than merely untested).**

> Note for reviewer: one residual P2 remains open (feature-family prefilter's known false-negative on
> diverse actives is now diagnosed but not eliminated) — this does not block landing per the fix
> criteria (core >=85, deployable, no open P0, no veto).

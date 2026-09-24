> **Audit record for `bio-similarity-searching`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@87bcd46](https://github.com/mrsonord2240/bioSkills/tree/87bcd4677e0402e821a95f06f06d8400733606ae/chemoinformatics/similarity-searching) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-similarity-searching

Generated: 2026-09-24
Exact source: `mrsonord2240/bioSkills@87bcd4677e0402e821a95f06f06d8400733606ae:chemoinformatics/similarity-searching`
Category: Data Analysis · Mode: A · Complexity: Complex
Environment: RDKit 2026.03.6 / numpy 2.5.3 shared audit environment; MHFP6 route in its numpy-1.26.4 environment.
Data: 500 distinct ChEMBL hERG compounds for focused checks; 100 compounds for MHFP6 LSH.

## Summary

| Input | Type | Total | Assertions | Status |
|---|---|---:|---:|---|
| 1 | Canonical — analog ranking | 96 | 4/4 | ✅ |
| 2 | Variant A — Butina centroid rule | 96 | 4/4 | ✅ |
| 3 | Variant B — Tversky plus SMARTS | 97 | 4/4 | ✅ |
| 4 | Edge — stereoisomer cliff guard | 97 | 4/4 | ✅ |
| 5 | Stress — MCS outcome branch | 96 | 4/4 | ✅ |
| 6 | Scope Boundary — percentile calibration | 96 | 4/4 | ✅ |
| 7 | Adversarial — invalid query and LSH | 95 | 4/4 | ✅ |
| 8 | New Edge — identity after 1.0 | 97 | 4/4 | ✅ |
| 9 | New Stress — prior-findings regression | 96 | 4/4 | ✅ |

**Execution average: 96.2 / 100**
**Assertion pass rate: 36 / 36**
**Final: 96 / 100 — Production Ready — deployable**

## Executed evidence

`run/re_audit_20260924.py`, compiled and run with the shared audit interpreter:

```text
source_commit=87bcd4677e0402e821a95f06f06d8400733606ae
data=500 ChEMBL hERG molecules
input1_search_hits=18 top=1.000
input2_clusters=128 centroid_violations=0
input3_tversky_asymmetry=0.152 candidates=20 smart_confirmed=0
input4_stereo_achiral=1.000 chiral=0.714
input5_mcs_atoms=2 canceled=False
input6_p995=0.731 retained=0.0050
input7_invalid_smiles=Invalid query SMILES
input8_inchikey_equal=False
input9_required_guidance_missing=[]
```

`run/re_audit_lsh_20260924.py`, run with the dedicated MHFP6 environment:

```text
lsh_n=100 returned=10 recall_at_10=10/10
```

## Re-audit findings

The previous P1 was fixed: the source now identifies chirality-blind Morgan fingerprints as the common reason different stereoisomers score 1.0, uses `includeChirality=True` for stereochemistry-aware similarity, keeps hash collisions as a secondary cause, and uses standardized identifiers for exact identity. The activity-cliff guidance also requires standardization and salt stripping.

All three prior P2 findings were fixed. Tversky is now explicitly a feature-overlap ranking and asks for SMARTS confirmation. MCS instructions branch on `result.canceled`, so a small uncanceled result leads to pre-clustering rather than a futile timeout increase. Threshold selection now uses a per-library retained-pair percentile and sampling for large libraries.

No P0, P1, or P2 findings remain from this re-audit.

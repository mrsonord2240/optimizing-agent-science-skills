> **Audit record for `bio-molecular-descriptors`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@77387c8](https://github.com/mrsonord2240/bioSkills/tree/77387c83238ced7d8e6bae147002918c0dd11116/chemoinformatics/molecular-descriptors) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-molecular-descriptors — fix-pass re-audit

**Decision: ⭐ Production Ready (93/100).** The exact source `mrsonord2240/bioSkills@77387c83238ced7d8e6bae147002918c0dd11116:chemoinformatics/molecular-descriptors` passes all vetoes, has no open P0/P1/P2 finding, and is deployable.

| Audit metadata | Value |
|---|---|
| Evaluated | 2026-09-24 |
| Category / mode / complexity | Data Analysis / A / Complex |
| Dynamic inputs | 7, all re-audited |
| Exact source | `77387c83238ced7d8e6bae147002918c0dd11116` |
| Runtime | Shared chemistry audit environment: Python 3.14.5, RDKit 2026.03.6, NumPy 2.5.2, pandas 2.3.3 |
| Real-data fixture | ChEMBL hERG CHEMBL240, 3,224 distinct compounds |
| Reproducible evidence | `run/unchanged_paths_recheck.py`, `run/fixpass_checks.py`, and their `.out` files |

The original 2026-09-16 audit’s six findings were fixed in the exact source above. The source tree was clean at that SHA after committing; audit artifacts are outside the source worktree.

## Veto gates

| Gate | Result | Evidence |
|---|---|---|
| T1 stability | PASS | 2D panel, 2D fingerprints, and revised 3D paths completed in the shared RDKit environment. |
| T2 contract | PASS | Frontmatter and all referenced shipped artifacts are present; MAP4 is now an explicit external-install boundary rather than a false package claim. |
| T3 determinism | PASS | Three fixed-seed atenolol helper runs produced identical asphericity (`0.787643`). |
| T4 security | PASS | No network, credentials, dynamic evaluation, or unsafe file handling introduced. |
| M1 scientific integrity | PASS | The QED caveat now distinguishes fragment over-ranking from natural-product/peptide under-ranking. |
| M2 practice boundaries | PASS | QED remains a calibrated triage heuristic, not a universal filter; Gasteiger rejects unsupported elements. |
| M3 methodological ground | PASS | The 3D route uses ETKDGv3, a fixed seed, MMFF with 2,000 iterations, and excludes only individual non-converged conformers. |
| M4 code usability | PASS | Atenolol and verapamil ensembles converge 20/20; the example executes atenolol in `__main__`. |

## Dynamic execution

| # | Audit vector | Result | Exact-commit evidence |
|---:|---|---:|---|
| 1 | Physchem panel / rule sets over 1,000 hERG compounds | ✅ 92 | `run/unchanged_paths_recheck.out`: 9 descriptors × 1,000, no NaN/inf. |
| 2 | Fingerprint taxonomy and compatibility | ✅ 95 | Six RDKit generators construct; MAP4 is no longer claimed installable from PyPI; MHFP6 pins NumPy `<2`. |
| 3 | ECFP radius and collision measurement | ✅ 93 | `5.38, 2.95, 1.89, 0.85, 0.44%` loss from 512 through 8,192 bits. |
| 4 | 3D ensemble for flexible drug-like molecules | ✅ 96 | Atenolol 20/20 and verapamil 20/20 MMFF converged at 2,000 iterations. |
| 5 | Full-library ECFP4 2048 featurization | ✅ 93 | `(3224, 2048)`, 6.6 MB, 8 dead bits. |
| 6 | QED scope boundary | ✅ 96 | Indole `0.544` and imatinib `0.389` confirm the documented opposite failure directions. |
| 7 | Gasteiger/LogP adversarial checks | ✅ 96 | Explicit-H aspirin charges sum to `-0.000000`; iron is rejected before use. |

**Assertion result: 31/31 PASS (100%).** The seven input totals sum to 661, for a dynamic average of **94.4/100**.

## Repair delivered

- The 3D ensemble pattern uses `maxIters=2000`, keeps only conformers with MMFF status `0`, records partial non-convergence, and fails only when none converge. The shipped single-conformer helper exposes `random_seed=42` and `max_iters=2000`, and now runs atenolol in its smoke path.
- The unsupported `map4 1.1+` compatibility claim was removed. MAP4 is explicitly external/source-install work with a platform and one-molecule validation requirement; MHFP6 is constrained to its tested NumPy-1.x compatibility range.
- Gasteiger guidance now makes hydrogens explicit for charge-balance checks and rejects non-organic elements such as iron instead of trusting finite-looking values.
- QED guidance now states the observed direction: small fragments can be over-ranked, while peptide- and natural-product-like chemistry can be under-ranked.

## Scores

| Static | Dynamic | Final |
|---:|---:|---:|
| 91/100 | 94.4/100 | **93/100 — Production Ready** |

No P0, P1, or P2 remediation remains from the authoritative audit. A future user who specifically requires MAP4 should perform the documented external source/platform validation before treating it as an available representation; that is a deployment prerequisite, not an unresolved defect in this RDKit-first Skill.

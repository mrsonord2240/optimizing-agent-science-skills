> **Audit record for `bio-molecular-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@2f3d8d3](https://github.com/mrsonord2240/bioSkills/tree/2f3d8d3c43ef34e5ff55af1b04a9abf263c5c631/chemoinformatics/molecular-io) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Exact-commit Re-audit — bio-molecular-io

Evaluated 2026-09-24 against `2f3d8d3c43ef34e5ff55af1b04a9abf263c5c631` on `agent/fix-bio-molecular-io`.

| Metric | Result |
|---|---:|
| Static score | 98 / 100 |
| Dynamic score | 100 / 100 |
| Assertions | 28 / 28 (100%) |
| Final score | **99 / 100** |
| Grade | **Production Ready** |
| P0 / P1 / open P2 | 0 / 0 / 0 |

## Evidence

Run with the established `cheminformatics-hit-triage-analyst` environment (Python 3.12.13, RDKit 2026.03.6, openbabel-wheel 3.1.1.23):

```powershell
F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe -u F:\OpenScience\audits\bio-molecular-io\re_audit.py
```

The captured result is `re_audit.out`. The runner retains the library conversion products under `re_audit_run/` and verifies:

- 3,224 hERG SMILES survive a property-carrying SDF round trip with unchanged structures and tetrahedral-stereo count.
- Blank/whitespace SMILES are rejected; grammar errors remain non-inspectable under `sanitize=False`; sanitizable chemistry errors produce expected RDKit flags.
- A 1,200-atom molecule automatically writes as V3000 and reads back intact.
- Open Babel remains usable for MOL2/PDBQT conversion, while RDKit generates registry InChI; this wheel's absent Open Babel `inchi` format is detected rather than invoked.
- PDB template bond-order repair and `/FixedH` InChI tautomer behavior still hold.

## Resolved P2 findings

1. Removed the unsupported Open Babel InChI assumption from the conversion example; it now converts format with Open Babel and generates InChI through RDKit.
2. Updated the >999-atom SDF guidance for current RDKit's automatic V3000 upgrade and legacy-reader compatibility risk.
3. Split SMILES grammar failures from chemistry failures that can be diagnosed with `sanitize=False` and `SanitizeMol(catchErrors=True)`.
4. Reject empty and zero-atom molecules at parse, SDF-read, and shipped-example boundaries.

## Remaining recommendations

- P3: Consider promoting the exact-commit audit runner into a bundled regression test if this skill gains a test harness.
- P3: For a vendor MOL2 file that neither toolkit can convert, retain the source and request a corrected SDF/MOL2 rather than guessing atom types.

> **Audit record for `bio-single-cell-metabolite-communication`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@8409788](https://github.com/mrsonord2240/bioSkills/tree/8409788111cfe93ffb118801c0104d1ddd7fd93f/single-cell/metabolite-communication) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit Viewer — bio-single-cell-metabolite-communication

Exact commit: 8409788111cfe93ffb118801c0104d1ddd7fd93f
Date: 2026-09-24
Evidence: run/reaudit_fixed_findings.py and run/reaudit_fixed_findings.out

| Measure | Result |
|---|---:|
| Static | 96 / 100 |
| Execution | 98.4 / 100 |
| Assertions | 21 / 21 PASS |
| Final | **97 / 100 — Production Ready** |
| Open P0/P1/P2 | **0** |

The exact-commit re-audit exited 0:

~~~text
PASS commit=8409788 Windows guards=3 QC_route=present fixture=24x6 config_template=present
~~~

Closed findings:

- P1: all MEBOCOST inference snippets now invoke multiprocessing only under a
  Windows-safe main guard; the RuntimeError and corrective pattern are in Common Errors.
- P2: examples now include a deterministic 24-cell/6-gene AnnData generator,
  portable MEBOCOST config template, and expected structural invariants.
- P2: the primary Run MEBOCOST flow now routes to prepare_data_for_mebocost().

The generated fixture is a smoke test, not a fixed biological-result promise:
database versions can change MEBOCOST FDRs. The skill continues to require
metabolomics, spatial methods, tracing, or perturbation for validation.

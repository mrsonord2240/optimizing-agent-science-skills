> **Audit record for `bio-proteomics-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@31deeb9](https://github.com/mrsonord2240/bioSkills/tree/31deeb9912f6e318ed11069f05a55be98577ff5e/proteomics/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-differential-abundance

Generated: 2026-09-23
Source: mrsonord2240/bioSkills@31deeb9912f6e318ed11069f05a55be98577ff5e:proteomics/differential-abundance

Final-pass exception: auditor_independent: false. Note: final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Summary

| Input | Type | Basic | Specialized | Total | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | limma 4v4 batch | 37 | 56 | 93 | 3/3 | completed |
| 2 | treat and DEqMS | 37 | 56 | 93 | 3/3 | completed |
| 3 | proDA MNAR/on-off | 36 | 56 | 92 | 3/3 | completed |
| 4 | Python Welch+BH | 37 | 55 | 92 | 3/3 | completed |
| 5 | ashr shrinkage | 37 | 55 | 92 | 3/3 | completed |
| 6 | n=1 clinical boundary | 38 | 57 | 95 | 3/3 | completed |
| 7 | guide consistency | 39 | 57 | 96 | 3/3 | completed |
| 8 | paired donor design | 38 | 56 | 94 | 3/3 | completed |
| 9 | direct feature scripts | 34 | 52 | 86 | 2/3 | partial |
| 10 | centring checks | 38 | 57 | 95 | 3/3 | completed |
| 11 | three-arm ridge | 38 | 57 | 95 | 3/3 | completed |
| 12 | deterministic msqrob2 demo | 34 | 52 | 86 | 2/3 | partial |
| 13 | Python 12v12 planted truth | 37 | 55 | 92 | 3/3 | completed |

Execution average: 92.4/100. Assertions: 37/39. Static: 93/100.
Final: 93/100, Production Ready, deployable true. Skill Veto PASS; Research Veto PASS; no P0.

## Fresh code and evidence

The current shipped code was called through fresh runners saved under run/phase2_20260923:

- phase2_r_regressions.R — inputs 1, 2, 3, 5, 8, 10, 11
- phase2_python_regressions.py — inputs 4, 6, 7, 13
- phase2_cli.sh — inputs 9 and 12
- execute_phase2.sh, execute_remaining.sh, rerun_python_only.sh, and verify_phase2_outputs.py

The runners directly use current scripts/limma_de.R, scripts/centring_checks.R,
scripts/msstats_group_comparison.R, examples/msqrob2_peptide_level.R, and
examples/differential_abundance.py. Synthetic planted-truth fixtures were rerun; old output was not evidence.

## Detailed results

1. Canonical limma: 1,334 tested; 97 calls; 3 planted false positives (3.09%); 223 valid-value and 3 non-estimable rows reported.

2. DEqMS/treat: treat made 83 calls with 0 false positives; DEqMS made 97 with 3 false positives (3.09%) and exposed count-adjusted fields.

3. proDA: 1,560 tested; 38 calls; 140 proteins were absent from a full condition and none was called.

4. Python: 1,337 tested; 223 untestables returned as protein/n_case/n_ctrl; all-untestable input raised the documented ValueError.

5. ashr: 1,334 finite posterior means were returned alongside the moderated fit.

6. Scope: fresh scan verified the explicit exclusions for single-sample n=1 comparison and individual diagnosis/treatment.

7. Consistency: all three superseded claims were absent from both source files; executable examples and feature reference were linked.

8. Paired donors: 795 tested after 121 non-estimable drops; 63 calls and 3 false positives (4.76%).

9. Direct MSstats/msqrob2:
   - equalizeMedians: 290 tested, 6 undetected, 101 calls, median log2FC -0.184, median SE 0.119
   - normalization FALSE: 290 tested, 6 undetected, 79 calls, median log2FC +0.008, median SE 0.204
   - msqrob2: 286 tested, 12 untestable, 80 calls, median logFC -0.0048
   - Both MSstats CSVs parsed with all expected fields. Each direct R process then exited 139.

10. Centring checks: residual-SD ratio 0.752 versus threshold 0.85; the intentional -0.200 logFC input stopped with the expected message.

11. Three-arm ridge: ridge TRUE was accepted on three groups.

12. Seeded no-argument msqrob2: two byte-identical outputs, 300 tested and 43 calls, with 3 planted false positives (7.0%). Both direct processes then exited 139.

13. Python 12v12: 826 tested, 74 explicitly returned untestables, 39 calls, 0 planted false positives.

## Open issues

P1: five direct R calls wrote valid, parseable output then exited 139 during shared-R teardown. This is not concealed; reproduce in a clean target R 4.4.3/Bioc 3.20 runtime before claiming stable CLI exit behavior.

P2: the compact seeded msqrob2 demo's printed 7.0% realized FDR is an illustrative single realization, not a calibration guarantee.


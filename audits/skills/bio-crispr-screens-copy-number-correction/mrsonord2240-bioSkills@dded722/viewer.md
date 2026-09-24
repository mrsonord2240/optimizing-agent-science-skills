> **Audit record for `bio-crispr-screens-copy-number-correction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@dded722](https://github.com/mrsonord2240/bioSkills/tree/dded722b0c3490d36f4fec2fe633eb113a05317c/crispr-screens/copy-number-correction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-copy-number-correction

**Final score: 98/100 — Production Ready — deployable**

Source audited: `mrsonord2240/bioSkills@dded722b0c3490d36f4fec2fe633eb113a05317c:crispr-screens/copy-number-correction`  
Date: 2026-09-24  
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md  
Auditor independent: false

## Result

The final source resolves all three previously open P2 findings:

- It distinguishes an omitted `negative_control_sgrnas` argument from an explicit empty list, including the observed construction-time error and recovery.
- It keeps the demonstrated post-`alternate_CN` per-line residual while removing the unsupported implication that pooled analysis necessarily hides it.
- It seeds NumPy before Chronos model construction, records what belongs in the manifest, and states that TensorFlow/BLAS version and hardware can prevent bitwise identity.

Seven archived logical inputs were rerun and two fresh source-contract edge inputs were added. All nine inputs completed; all 27 assertions passed.

| Input | Kind | Evidence | Result |
|---|---|---|---|
| 1 | Regression | Real HAP1 Chronos construction without controls | documented `excess_variance` ValueError before training |
| 2 | Regression | Real HT-29 3-gene post-correction residual | -0.9809 gap; low-power/suspicious flags correct |
| 3 | Regression | Five relabeled real diploid controls | 0/5 false suspicious flags |
| 4 | Regression | n=7/8/9 and NaN boundary checks | exact low-power boundary; no NaN crash |
| 5 | Regression | Real three-line post-`alternate_CN` panel | residual detectable per-line and pooled; claim bounded |
| 6 | Regression | Real HAP1 construction with `{'screen': []}` | distinct documented empty-list ValueError |
| 7 | Regression | Source scope review | analytical correction and validation scope preserved |
| 8 | Fresh edge | Exact-source seeded initialization | same seed produces same NumPy initialization draws; caveat retained |
| 9 | Fresh edge | Exact-source extracted diagnostic fence | n=8 is not low power and focal bias is detected |

## Scores

- Static: 96/100
- Execution average: 99.4/100
- Assertions: 27/27
- Weighted final: 98/100

No recommendations remain. The audit is corrective rather than independent: one brief covered the edits and final re-audit.

## Reproduction

Run the five archived regressions and two new edge contracts with the Chronos environment:

```powershell
$py = 'F:\OpenScience\audit-envs\crispr-screen-analyst\tools\chronos-venv\Scripts\python.exe'
Set-Location 'F:\OpenScience\audits\bio-crispr-screens-copy-number-correction\run\scripts_r3'
1..5 | ForEach-Object { & $py ("{0:D2}_*.py" -f $_) }
& $py .\06_finalpass_source_contract.py
```

The source-contract test verifies the worktree SHA before reading `SKILL.md`.

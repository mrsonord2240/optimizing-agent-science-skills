> **Audit record for `bio-experimental-design-multiple-testing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6b48002](https://github.com/mrsonord2240/bioSkills/tree/6b48002e06f0dfd1ae3bb1e19a75ff9522da6ebe/experimental-design/multiple-testing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-multiple-testing

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@6b48002e06f0dfd1ae3bb1e19a75ff9522da6ebe:experimental-design/multiple-testing`

Mode: D (direct statistical decision workflow plus R scripts) · Category: Data Analysis · Complexity: Complex (7 inputs)

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical genome-wide discovery | 37 | 57 | 94 | 4/4 | ✅ |
| 2 | Variant A: local FDR + FCR | 37 | 56 | 93 | 4/4 | ✅ |
| 3 | Edge: small all-null family | 38 | 56 | 94 | 4/4 | ✅ |
| 4 | Variant B: sourceable IHW safe function | 37 | 57 | 94 | 4/4 | ✅ |
| 5 | Stress: IHW CLI + exact shipped example | 37 | 56 | 93 | 4/4 | ✅ |
| 6 | Scope boundary: confirmatory endpoints | 37 | 55 | 92 | 4/4 | ✅ |
| 7 | Adversarial: outcome-linked filter | 37 | 56 | 93 | 4/4 | ✅ |

Execution average: **93.3 / 100** · Assertions: **28 / 28** · Static score: **91 / 100** · Final score: **92.4 / 100**.

## Corrective regression evidence

All fresh execution files are under `run/corrective_6b48002/`.

- Input 1 ran BH, BY, `qvalue_safe.R`, an isolated q-value-detail worker, and Python `fdr_bh`/`fdr_by`: BH 205, BY 92, q-value pi0 0.8595 and 209 discoveries; Python BH/BY 4/3 rejections.
- Input 2 produced 225 `lfdr < 0.2` calls (mean local FDR 0.0550) and a selected-set FCR level of 0.997950 over 205 intervals.
- Input 3 ran the documented `lambda=0` small-family q-value route: pi0 1, zero discoveries, and 30 bounded q-values.
- Input 4 sourced `scripts/ihw_safe.R`: IHW succeeded on attempt 1 with 4 discoveries and 100 bounded adjusted p-values.
- Input 5 exercised the CLI (100 output rows, bounded `padj_ihw`) and then the **exact** shipped `examples/multiple_testing_correction.R` three consecutive times. Every full run exited 0 and printed BH mean FDP 0.046, q-value pi0 0.912 with 98 discoveries, and IHW 85 versus BH 93.
- Inputs 6–7 executed the Skill-directed scope and independent-filtering decisions; their full responses are saved beside the run scripts.

The pre/post snapshots show identical Python freeze output and identical `IHW`/`qvalue` DESCRIPTION versions, with no R install lock: `output/environment_comparison.txt` says `shared_environment_mutation=none`.

## Veto result

Skill Veto: PASS. Research Veto: PASS. The former M4 failure was the old tip's post-output exit 139; the corrective tip's full shipped example now completes cleanly in repeated full runs, so it is not reproduced.

## Remaining recommendation

P2: `locfdr` is still taxonomy-only. Either supply and run a minimal supported workflow or remove that package mention. This does not block deployment.

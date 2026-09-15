> **Audit record for `bio-phylo-divergence-dating`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/divergence-dating) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-divergence-dating (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/divergence-dating`
Pre-fix: 83, ✅ Limited Release. Fix log read; evidence is `runs_v2/` only. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**.
Environment: PAML 4.10.10, IQ-TREE 2.4.0 (LSD2), Biopython 1.88. BEAST 2.7.7 not re-run (Input 4 uses the pre-fix MCC trees);
TreePL/TempEst not executable. **All data SYNTHETIC** (`data/make_data.py`).

## Static: 87/100 (pre-fix 80)
Functional 11 · Reliability 10 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 10 · Agent-specific 18.
Remaining gaps: no root-to-tip / randomization code, no infinite-sites code, helper silent on multi-locus `ndata`.
Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 52 | 89 | 5/5 | yes | ✅ |
| 2 | Variant A (regr.) | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 3 | Edge (regr.) | 37 | 51 | 88 | 4/4 | yes | ✅ |
| 4 | Variant B (regr.) | 36 | 50 | 86 | 5/5 | yes (snippet; BEAST reused) | ✅ |
| 5 | Stress (regr.) | 36 | 51 | 87 | 5/5 | yes (clock pair reused) | ✅ |
| 6 | Scope Boundary | 37 | 48 | 85 | 4/4 | no | ✅ |
| 7 | Adversarial (regr.) | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 8 | NEW 2-locus helper | 35 | 50 | 85 | 3/4 | yes | ✅ |
| 9 | NEW infinite-sites | 35 | 49 | 84 | 3/4 | yes | ✅ |

**Execution average 87.2** · assertions 38/40 (95 %) · L1 36.3 · L2 50.9. Research Veto PASS.
**Final: 87 × 0.4 + 87.2 × 0.6 = 34.8 + 52.3 = 87 → ⭐ Production Ready** (all PR floors met).

## Key outputs
**In1** `[post_asis] usedata=2 exit=1 last line: error: file name empty.` · `[post] usedata=2 in.BV exit=0`
```
AB   0.20 L(0.15,0.1,1,0.025) prior 0.289 [0.134,0.572]  post 0.222 [0.149,0.300] YES
GH   0.45 B(0.35,0.55)        prior 0.443 [0.347,0.546]  post 0.451 [0.356,0.549] YES
root 1.00 B(0.8,1.2)          prior 0.987 [0.795,1.195]  post 0.975 [0.793,1.177] YES   (7/7 YES)
```
**In2** slope 2.219e-03, R² 0.987 · LSD2 rate 1.935e-03 [1.543e-03, 2.277e-03], tMRCA 1996.79 · randomized max 7.31e-05 → PASSES.
**In3** LSD2 tMRCA 1810.35 [−1.005e+09; 1996.24] · R² 0.094 · overlap True → no signal.
**In4** Skill snippet (verbatim):
```
['A','B'] prior (17.37, (15.12, 25.30)) posterior 19.88 (16.72, 25.41)
['G','H'] prior (42.68, (35.04, 53.29)) posterior 39.86 (35.01, 50.12)
['A'..'H'] prior (97.69, (80.01, 117.47)) posterior 88.24 (80.00, 109.16)
['C','D'] prior clade not in prior MCC tree posterior 28.85 (23.84, 36.60)
```
**In5** helper ctl: `seed = 1234 ; mcmcfile = mcmc.txt ; ndata = 1 ; usedata = 2 in.BV ; RootAge = <1.0 ; BDparas = 1 1 0.1 m` ·
`run_pipeline: OK` · `in.BV bytes: 2343` · 7/7 in HPD · `[BLU]` and `[gtlt]`: identical calibration blocks, GH prior (0.4431, 0.3468, 0.5463).
**In7** point GH 0.400 [0.399, 0.401] MISS · soft-min 0.491 [0.369, 0.638].
**In8 (NEW)** prompt: "Run your helper on my two-locus file species2loci.phy." → `ndata = 2`, `run_pipeline: OK`, `in.BV bytes: 4686`, 7/7 in HPD.
**In9 (NEW)** prompt: "Will sequencing more loci narrow my node ages?" → `in5: CI width = 0.483 x mean age; R^2 = 0.569` ·
`in8: 0.445 x; R^2 = 0.877`.
**Example** `py_compile OK`; demo exit 0 writes prior/bv/post directories with a header tree file.

## Recommendations
[P2] root-to-tip + randomization code · [P2] document multi-locus `ndata` · [P2] infinite-sites code.

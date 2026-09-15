> **Audit record for `bio-phylo-bayesian-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/bayesian-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-bayesian-inference (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/bayesian-inference`
Pre-fix: 84 numeric → ⚠️ Beta Only (assertion floor 79.4 %). Evidence: `runs_v2/`. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**.
MrBayes 3.2.7a, rwty 1.0.3. ngen scaled down from 10M. **All data SYNTHETIC**.

## Static: 86/100 (pre-fix 81)
Functional 11 · Reliability 10 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 9 · Agent-specific 18.
MrBayes help (`runs_v2/flagcheck/mb_help.txt`) confirms `Data`, `Append`, `Alpha 0.40`, `BurninSS -1`, stoprule topology-only,
`prset topologypr` uniform/speciestree/constraints/fixed. Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 2 | Variant A (regr.) | 37 | 52 | 89 | 5/5 | yes |
| 3 | Edge (regr.) | 36 | 52 | 88 | 5/5 | yes |
| 4 | Variant B (regr.) | 37 | 54 | 91 | 5/5 | yes |
| 5 | Stress (regr.) | 36 | 52 | 88 | 5/5 | yes (data TL reused) |
| 6 | Scope Boundary | 37 | 47 | 84 | 4/4 | no |
| 7 | Adversarial (regr.) | 37 | 54 | 91 | 5/5 | yes |
| 8 | NEW nst=mixed | 35 | 51 | 86 | 3/4 | yes |
| 9 | NEW single run | 32 | 48 | 80 | 3/4 | yes |

**Execution average 87.2** · assertions 40/42 (95.2 %) · L1 35.9 · L2 51.3. Research Veto PASS.
**Final: 86 × 0.4 + 87.2 × 0.6 = 34.4 + 52.3 = 87 → ⭐ Production Ready.**

## Key outputs
**In1** 100k: `WORST minESS: alpha 51.6 | PSRF pinvar 1.024` → `mcmc append=yes ngen=300000` (`Setting append to yes`) →
`3001 samples ... 2251 included`, `WORST minESS: alpha 140.6 | PSRF pi(G) 1.003`, ASDSF 0.0003, RF 0, rwty `burnin(trees): 750`, returned TRUE.
Alpha still < 200: output asks for one more append rather than reporting PPs.
**In2** minESS pi(G) 21.9, ASDSF 0.0129, max SD 0.103; example `alpha: low ESS (104.4) ... Run chains longer`; rwty burnin 100 of 401.
**In3** minESS 220.4, PSRF 1.003; `13 PP=0.714 {E,F,G,H} <== split of interest`, `14 PP=0.207 {C,D,E,F}`; RF 0.
**In4** `50 steps will be used with 4900 generations (49 samples) within each step` · GTR+G `Mean: -9857.08` · JC `Mean: -10602.26` → 2 lnBF 1490.
**In5** `Running without data` · prior TL mean 9.56 (gammadir) / 11.69 (exp10) · data TL 0.904 / 1.181 (pre-fix runs).
**In7** banner `(Use the harmonic mean for Bayes factor comparisons of models)` · HME GTR+G −9788.80 / −9787.16, JC −10551.31 / −10551.95.
**In8 (NEW)** prompt: "I don't want to pick one substitution model — average over them in MrBayes." `lset nst=mixed rates=gamma` 200k →
min ESS 218, ASDSF 0.0001; `gtrsubmodel[123323] 0.199, [123121] 0.144, [121121] 0.129, [123321] 0.118 ...`; RF 0.
**In9 (NEW)** prompt: "I only ran one MrBayes run (single.p/.t). Prove it converged." nruns=1 → pstat has ESS (TL 451) but no PSRF;
sump prints no split SD. `python bayesian_convergence.py single.p` → `No .p files given; running a self-test on synthetic traces.` exit 0.
**Example** py_compile OK; self-test exit 0 with the documented intended TL PSRF FAIL.

## Recommendations
[P2] example should reject a single .p · [P2] explain nst=mixed output · [P2] minimal BEAST2/RevBayes commands.

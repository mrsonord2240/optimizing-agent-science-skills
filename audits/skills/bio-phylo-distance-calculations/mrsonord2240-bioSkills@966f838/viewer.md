> **Audit record for `bio-phylo-distance-calculations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@966f838](https://github.com/mrsonord2240/bioSkills/tree/966f838b0ba32918310bd223a34f71d78f190560/phylogenetics/distance-calculations) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-distance-calculations (re-audit of the fixed Skill)
Generated: 2026-09-15 · Re-auditor: molecular-phylogenetics-analyst round 2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@966f838b0ba32918310bd223a34f71d78f190560:phylogenetics/distance-calculations`
Pre-fix: 82 → ⚠️ Beta Only (assertion floor). Evidence: `runs_v2/`. Data Analysis · Mode A · 7 regression + 2 new = **N = 9**.
Environment: Biopython 1.88, scikit-bio 0.7.3, R ape 5.8.1 / phangorn 2.12.1. FastME CLI, DAMBE not executed. **All data SYNTHETIC**.

## Static: 86/100 (pre-fix 82)
Functional 11 · Reliability 10 · Performance 7 · Agent usability 14 · Human 6 · Security 11 · Maintainability 9 · Agent-specific 18.
Gate 8 PASS.

## Summary
| Input | Type | Basic | Spec. | Total | Assertions | Executed |
|---|---|---|---|---|---|---|
| 1 | Canonical (regr.) | 37 | 54 | 91 | 5/5 | yes |
| 2 | Variant A (regr.) | 34 | 48 | 82 | 4/5 | yes |
| 3 | Edge (regr.) | 36 | 52 | 88 | 4/4 | yes |
| 4 | Variant B (regr.) | 37 | 53 | 90 | 5/5 | yes |
| 5 | Stress (regr.) | 35 | 51 | 86 | 5/5 | yes |
| 6 | Scope Boundary (regr.) | 36 | 50 | 86 | 4/4 | yes |
| 7 | Adversarial (regr.) | 38 | 55 | 93 | 5/5 | yes |
| 8 | NEW gapped identity | 35 | 50 | 85 | 3/4 | yes |
| 9 | NEW estimate alpha | 35 | 50 | 85 | 3/4 | yes |

**Execution average 87.3** · assertions 38/41 (92.7 %) · L1 35.9 · L2 51.4. Research Veto PASS.
**Final: 86 × 0.4 + 87.3 × 0.6 = 34.4 + 52.4 = 87 → ⭐ Production Ready** (PR floors met).

## Key outputs
**In1** R: `RF K2P-NJ vs true: 6 (max 34)` · `support on wrong splits: 64 68 81` · `seeded rerun identical: TRUE`.
Python (Skill hand-off verbatim): `K80 hand-off Bio.Phylo NJ RF 6/34`, `skbio NJ RF 6/34`, `names match alignment ids: True`.
**In2** Skill block: `bootstrap time 1.15 secs` · `RF TN93+G0.5 FastME: 14 (max 18)` · `bootstrap %: NA 12 9 7 14 30 38 33 30 29` · identical rerun.
**In3** sat12: `0.8333`, slope `0.0402`, ts/tv 0.76 · deep12: `0`, slope `0.1710`, ts/tv 1.03.
**In4** `nj(K80): missing values are not allowed ... Consider using njs()` · NaN pairs `AT1-GC3 AT2-GC3`, max p 0.647 ·
`K80 njs 10 | TN93 bionjs 10 | logdet NJ 2 | paralin FastME 2`.
**In5** `barcode20 B=100 27s RF 8/34 | confidence max 100 min 57 | clades>=70%: 9` ·
`big150 B=20 188s RF 130/294 | confidence max 100 min 50 | clades>=70%: 21`.
**In6/7** identical to pre-fix (LG FastME RF 2; UPGMA RF 4 with 100% bootstrap; JC69/K80 NJ RF 0).
**In8 (NEW)** prompt: "My COI alignment has indels in five specimens; give me the quick Biopython NJ tree." →
`columns 670 -> gap-free 628` · `identity sp01-sp03 gapped 0.0896 | gap-stripped 0.0478` · `RF gapped 22/34 | gap-stripped 6/34` · ape raw 0.0478.
**In9 (NEW)** prompt: "Don't assume alpha — estimate it and build the TN93+Γ FastME tree with bootstrap." →
`estimated alpha 0.396` · `RF estimated-alpha FastME 14 | alpha 0.5 FastME 14` · `ML GTR+G4 ... RF 0`.
**Examples** all four exit 0; `bootstrap_consensus.py` prints `['Chimp','Human']: 100%` etc.; `model_corrected_tree.R` prints counts `NA, 51, 43`.

## Recommendations
[P2] alpha-estimation and gap-stripping code · [P2] Trap paragraph vs optional Xia test · [P2] examples on real simulated data.

> **Audit record for `bio-phylo-distance-calculations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@086bf3d](https://github.com/mrsonord2240/bioSkills/tree/086bf3df497859926c0e38927fc11fd910d35739/phylogenetics/distance-calculations) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-phylo-distance-calculations — exact-commit final pass

Source: `mrsonord2240/bioSkills@086bf3df497859926c0e38927fc11fd910d35739:phylogenetics/distance-calculations`  
Evaluated: 2026-09-24 · Mode A · 9 synthetic scientific inputs

## Result

**97/100 — Production Ready** · veto gates PASS · **41/41 assertions passed** · no P0/P1/P2 findings.

Current main already contained the prior P2 repairs: gap-column filtering, `optim.pml(optGamma=TRUE)` alpha estimation, aligned ape-proxy/Xia wording, and checkable simulated examples. This final pass repairs the remaining frontmatter contract violation by moving catalog fields under `metadata`.

| Exact-source check | Result |
| --- | --- |
| Skill contract | `quick_validate.py` PASS |
| Simulated NJ example | 8 taxa / 300 bp; RF proportion to truth = 0.200 |
| Model-corrected FastME | estimated gamma; bootstrap counts produced; RF to truth = 4 |
| Rooted consensus | fixed Rat outgroup; three reported clades at 100% |
| Gap filter | 5 columns -> 4, keep mask `11011` |
| Historic complete regression | nine synthetic tree cases retained in `runs_v2/` |

## Evidence

- Exact-commit executable outputs: `runs_v3/`.
- Completed full synthetic tree regression corpus: `runs_v2/`.

## Open finding

INFO only: standalone FastME CLI and DAMBE are unavailable in the Windows audit environment. The executable ape/phangorn alternatives were tested.

> **Audit record for `bio-alignment-trimming`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c5bda09](https://github.com/mrsonord2240/bioSkills/tree/c5bda09627a2d9f0bfc2222bfcef06249772f0a2/alignment/alignment-trimming) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-alignment-trimming — exact-commit re-audit

Source: `mrsonord2240/bioSkills@c5bda09627a2d9f0bfc2222bfcef06249772f0a2:alignment/alignment-trimming`  
Evaluated: 2026-09-24 · Mode A · 9 focused scientific inputs plus contract/example validation

## Result

**96/100 — Production Ready** · veto gates PASS · **30/30 assertions passed** · no P0/P1/P2 findings.

The earlier P2 fixes are present on current main: sequence-overlap thresholds are explicitly dataset-dependent and inspectable; BMGE 1.12/2.0 wording is version-specific; and specialist workflow detail is in `references/`. This pass also repaired the stale schema violation by nesting catalog fields under `metadata`.

| Check | Exact-SHA result |
| --- | --- |
| Skill contract | `quick_validate.py` PASS |
| ClipKIT smart-gap | 339/413 columns retained; log-map residue check PASS |
| trimAl maps | gappyout/automated1/manual maps: 218/161/250, all verified |
| BMGE | 1.12 and 2.0 output PASS; wrong-version command guarded |
| MACSE / PAML prep | zero `!`; PAML outputs produced |
| PhyIN | DNA: 20/816 deleted; protein: 0/413 deleted |
| Overlap thresholds | 75 removes P04/P10/P12/P14; 50 removes only fragments P04/P10 |
| Examples | four compile; ClipKIT and both BMGE branches run; mismatch fails loudly |

## Evidence

- Exact focused replay: `runs_v8/run_all.log` and `runs_v8/run_all.err.log` (tree bootstraps deliberately skipped).
- Repaired overlap workflow: `runs_v7/overlap_validation/`.
- Completed synthetic tree regressions retained from the prior fixed-source run: `runs_v2/`.

## Open finding

INFO only: T-Coffee, HMMcleaner, Divvier, Gblocks and hmmbuild were not runnable in the Windows audit environment. Their reference material was reviewed; this is not a source defect.

> **Audit record for `bio-microbiome-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@55c385d](https://github.com/mrsonord2240/bioSkills/tree/55c385dd6480e12d6f648af57dd2eb5ba7503fe8/microbiome/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-differential-abundance

## Canonical final summary

**Final:** 96/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@55c385dd6480e12d6f648af57dd2eb5ba7503fe8:microbiome/differential-abundance`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

This is **not an independent re-audit**: correction and audit were completed under one final-pass brief.

The MaAsLin2 example is now deliberately cross-sectional: it omits `SubjectID` when each subject occurs once, disables optional package plots, and documents the otherwise silent empty-result failure. The actual repeated/paired escape hatch remains available only after confirming repeated observations.

| Inputs | Evidence | Result |
|---|---|---|
| 1–5 | Archived ALDEx2, ANCOM-BC2, LinDA, ZicoSeq, DESeq2, and consensus panel regression | ✅ `ALL BLOCKS COMPLETED WITHOUT ERROR` |
| 6–7 | Scope and selective-reporting boundaries | ✅ Correct route and full-panel reporting requirement |
| 8 | Fresh cross-sectional MaAsLin2 | ✅ 188 usable Group rows |
| 9 | Fresh repeated-measures MaAsLin2 | ✅ 191 usable Arm rows on 12 subjects x 3 visits |

Assertions: **34/34 PASS**. Execution average: **95.6/100**.

Fresh evidence: `run/finalpass_20260924_maaslin2_regression.R` and its output log. Archived evidence: `run/finalpass_20260924_archived_regression_output.txt`.

No open source-level P0, P1, or P2 recommendations remain. The separately observed LEfSe environment/rpy2 failure is external to this committed skill source; LEfSe remains correctly framed as exploratory and non-consensus.

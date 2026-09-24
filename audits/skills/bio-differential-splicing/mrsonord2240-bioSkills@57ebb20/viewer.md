> **Audit record for `bio-differential-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@57ebb20](https://github.com/mrsonord2240/bioSkills/tree/57ebb207c70be16fc91f8555a74a3892336893f5/alternative-splicing/differential-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-differential-splicing

Source: `mrsonord2240/bioSkills@57ebb207c70be16fc91f8555a74a3892336893f5:alternative-splicing/differential-splicing`  
Final pass: `auditor_independent: false`

**Production Ready — deployable.** Seven archived logical inputs were re-run, with two fresh edge checks incorporated into their relevant rows; 35/35 assertions pass; no veto and no open recommendation.

- Planted rMATS recovered dPSI 0.587; planted leafcutter recovered deltapsi 0.5446. Both shipped examples ran from clean copies.
- Real chrX, SUPPA2, sim2 stress, confounder, paired, MAJIQ-documentation, and n=1 boundary regressions were re-run.
- Fresh coverage tests retained the discordant-minima event, rejected the shallow event, and retained 21 n=6 calls versus 17 under the legacy rule.
- Fresh empty-counts test produced `-k True` / `-m` / XS-tag guidance.

MAJIQ/VOILA remains licence-gated and is explicitly documentation-only, not executed evidence.

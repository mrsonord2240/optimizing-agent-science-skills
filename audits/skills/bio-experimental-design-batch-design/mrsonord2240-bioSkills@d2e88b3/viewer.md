> **Audit record for `bio-experimental-design-batch-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d2e88b3](https://github.com/mrsonord2240/bioSkills/tree/d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f/experimental-design/batch-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-batch-design

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@d2e88b38777dd154d642d15cefe7e2ad1ccb2a0f:experimental-design/batch-design`

**97/100 — ⭐ Production Ready — deployable: true.** All nine inputs executed in the documented private WSL route and all 36 assertions passed. The previous T1 rejection is preserved at `F:\OpenScience\audits\_archive-20260923\bio-experimental-design-batch-design\phase2-t1-rejection\`; it was not reused as evidence.

The runtime probe loaded designit 0.5.1, sva 3.58.0, and limma 3.66.0, then exited cleanly. The 24-sample assignment was 4/4/4 for condition and sex; its same-seed rerun was byte-identical. The bridge layout kept channel 16 empty in four 15-sample plexes and surfaced the site-spread warning. The NA-safe SVA route completed, as did the ComBat confounding boundary and all three validation refusals.

Evidence: `run\phase2-corrective-20260923\`. Final-pass metadata is intentionally `auditor_independent: false` with `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

Open P0/P1: none. P2: do not accept a bridge layout that still emits the documented covariate-imbalance warning; retry the optimizer first.

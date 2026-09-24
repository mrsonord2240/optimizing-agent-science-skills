> **Audit record for `bio-splicing-qc`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4dd002b](https://github.com/mrsonord2240/bioSkills/tree/4dd002b3ef77b6019b9cd59ff7309af20b0972a2/alternative-splicing/splicing-qc) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final QC — bio-splicing-qc

Source audited: `mrsonord2240/bioSkills@4dd002b3ef77b6019b9cd59ff7309af20b0972a2:alternative-splicing/splicing-qc`.

Final score: **90/100 — Production Ready**. No open P0, P1, or P2 findings.

## Independence

`auditor_independent=false`. The same agent made the final corrective changes and ran this re-audit, so this is regression evidence rather than independent approval.

## Executed evidence

| Coverage | Result | Evidence |
|---|---|---|
| Archived 1: known/novel + report | PASS | Clean: 93.4% read-known / 34.6% junction-known; novel-rich: 22.3% / 13.0%. Both reports show anchored-fragment counts beside coverage verdicts. |
| Archived 2: saturation | PASS | Deep 0.0% growth / PLATEAU; mid 4.0% and shallow 17.6% / STILL RISING. |
| Archived 3: strandedness | PASS | Planted dUTP: 1.0000 for `1+-,1-+,2++,2--`. |
| Archived 4: junction support | PASS | Hand-truth edge BAM: 13 junctions, 12 anchored, 62 total and 55 anchored reads. |
| Archived 6: MaxEnt | PASS | `[10.86, 2.68]` donor scores and `[11.58]` acceptor score. |
| Archived 7: rRNA | PASS | `8170 / 36756 = 22.2%` after the documented primary-mapped filter. |
| Fresh 1: real RSeQC header | PASS | New `novel-qc` accepts `intron_st(0-based)` / `intron_end(1-based)` and returns support medians by class. |
| Fresh 2: regression | PASS | Expanded self-contained test passed in both `as-core` and `as-maxent`. |

## Corrections closed

- RSeQC's read-weighted and junction-level summaries are explicitly separated.
- `novel-qc` provides a runnable high-novel-rate support/anchor diagnostic; the real RSeQC coordinate-header variant is tested.
- 5'-to-3' bias is now a screen requiring gene-body and depth confirmation; the helper coverage verdict prints its evidence count.
- MaxEnt throughput/context and bibliographic pointers are stated; the workflow remains research-only.

The raw machine-readable report is `eval_report_bio-splicing-qc_result.json` in this directory.

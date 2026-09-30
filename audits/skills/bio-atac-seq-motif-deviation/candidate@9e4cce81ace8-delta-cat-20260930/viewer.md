> **Audit record for `bio-atac-seq-motif-deviation`**
> - Audited working candidate `9e4cce81ace8ed64e685173ec67852c56f25adc2b015da0c395456e54ee30e07`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/motif-deviation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-motif-deviation`**
> - Audited working candidate `9e4cce81ace8ed64e685173ec67852c56f25adc2b015da0c395456e54ee30e07`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/motif-deviation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-atac-seq-motif-deviation

Candidate `sha256-manifest-v1 9e4cce81ace8ed64e685173ec67852c56f25adc2b015da0c395456e54ee30e07` (6 files, 29,802 bytes), verified before and after the checks. Prior certified: `fb58807b04cb...` (shelf ea3b976), 86 Production Ready. Independent auditor; no Skill bytes edited.

**Result: 87/100, Production Ready, no veto, no open P0 (candidate-ready).** Static 88, execution 86.8, assertions 19/20.

## Delta verified

Only `SKILL.md` changed versus the shelf (logs/identity_diff.log). The changes are the frontmatter `category: Data Analysis` and `author: GPTomics`, plus the z-score sentence ("exceeded 9" becomes "|z| of about 7 per sample"). `category` is an allowed marketplace label (logs/check_category.log).

To re-check the z-score claim, I read the certified bulk runs (`reaudit-run/bulk_A`, `bulk_B`) with `scripts/verify_z_claim.py`. Their `s.R` is byte-identical to the candidate's `chromvar_bulk_analysis.R`, so no re-run was needed.
- Per-sample max |z| is 6.61 to 7.24 (IRF9 in K562_rep3 is the largest), and no values exceed 9.
- Both runs are identical.
- The group logFC reaches 14.0.

The new sentence is accurate.

## Findings

| ID | Status |
|---|---|
| MOTDEV-013 wrong z-score number | Resolved |
| MOTDEV-004 ArchR NA guarded, not root-caused | Open P2 (unchanged) |

## Re-scored

Static: functional_suitability 11 -> 12 and maintainability 10 -> 11 (86 -> 88). Input 1's numeric-claim assertion changes FAIL -> PASS: specialized 53 -> 54, total 88 -> 89. Execution average 86.6 -> 86.8. Final = 0.4 x 88 + 0.6 x 86.8 = 87.3.

Scripts: `scripts/identity_diff.py`, `check_category.py`, `verify_z_claim.py`, `build_delta.py`. Logs: `logs/`.

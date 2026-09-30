> **Audit record for `bio-atac-seq-consensus-peakset`**
> - Audited working candidate `9fcaf5e21aa4bf36637df32cff1776e7eb97dc20de4015d10717de36f370b856`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/consensus-peakset), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-consensus-peakset`**
> - Audited working candidate `9fcaf5e21aa4bf36637df32cff1776e7eb97dc20de4015d10717de36f370b856`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/consensus-peakset), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Frontmatter delta re-audit: bio-atac-seq-consensus-peakset

**Date:** 2026-09-30  
**Candidate:** `F:\OpenScience\wt\atac-consensus-peakset\skills\bio-atac-seq-consensus-peakset`  
**Exact identity:** `sha256-manifest-v1 9fcaf5e21aa4bf36637df32cff1776e7eb97dc20de4015d10717de36f370b856` (5 files, 29,308 bytes)  
**Result:** Candidate-ready: **91/100, Production Ready**. The delta does not change the prior disposition.

## Delta

The candidate was diffed against the certified shelf bytes (commit ea3b976), which recompute to `95aec811...45d2`. Only `SKILL.md` changed. It gained two frontmatter lines, `category: Data Analysis` and `author: GPTomics` (+41 bytes). The other four files, including `scripts/iterative_overlap.sh` (sha256 `669e6ef5...1ad4`), are byte-identical. Nothing else changed (`logs/delta.diff`).

- The frontmatter parses as YAML. The marketplace tool's own `skill_category()` returns `Data Analysis`, one of its five `VALID_CATEGORIES`, and this matches the prior report's category (`logs/check_frontmatter.log`).
- `author: GPTomics` matches the LICENSE copyright holder.

## Readiness

No dimension or assertion is touched. All scores carry forward: static 85/100, dynamic 94.3/100, assertions 15/15, final 0.4 × 85 + 0.6 × 94.3 = 91 (recomputed in `scripts/build_report.py`). No veto and no open findings.

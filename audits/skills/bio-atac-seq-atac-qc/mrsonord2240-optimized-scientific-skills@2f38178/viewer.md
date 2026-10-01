> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-atac-qc) match audited candidate `a78308b9bf6d1602c7c31f23458a02ec6d5a02b18f1776e03a3a0203c42fa571` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-atac-qc`**
> - Audited working candidate `a78308b9bf6d1602c7c31f23458a02ec6d5a02b18f1776e03a3a0203c42fa571`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-qc), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-atac-qc`**
> - Audited working candidate `a78308b9bf6d1602c7c31f23458a02ec6d5a02b18f1776e03a3a0203c42fa571`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-qc), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-atac-seq-atac-qc

Identity sha256-manifest-v1 `a78308b9bf6d1602c7c31f23458a02ec6d5a02b18f1776e03a3a0203c42fa571` (8 files, 45,018 bytes), recomputed before and after. Supersedes the certified `cf524ad6...dd99` (86, shelf commit ea3b976; its bytes recompute to that identity). Independent of the author of the change.

**Score 86/100, Production Ready (candidate-ready).** Static 86, execution avg 85.3, assertions 33/35. All carried forward. No veto, no open P0 or P1.

## Delta

Only `SKILL.md` changed. It gained two frontmatter lines, `category: Data Analysis` and `author: GPTomics` (+41 bytes). The other seven files, including all four scripts, are byte-identical, so every execution result carries forward unchanged (`logs/delta.diff`).

- The frontmatter parses as YAML. The marketplace tool's own `skill_category()` returns `Data Analysis`, one of its five `VALID_CATEGORIES` (`scripts/check_frontmatter.py`, `logs/check_frontmatter.log`). This matches the category in the prior report.
- `author: GPTomics` matches the LICENSE copyright holder and the provenance record.

No dimension or assertion is touched, and nothing was re-scored.

## Recommendations (P2, carried forward)

The fragment-size PDF has never been visually inspected. The TSS script is slow when TSS fall outside bigWig coverage. The Skill ships no fixtures or tests.

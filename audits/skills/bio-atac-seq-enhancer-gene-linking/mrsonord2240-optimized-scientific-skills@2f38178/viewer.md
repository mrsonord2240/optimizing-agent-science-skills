> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-enhancer-gene-linking) match audited candidate `7f9e4608fb2a79271640e672aa652d3ebbf8028730b9a422af1fceb1d1109b01` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-enhancer-gene-linking`**
> - Audited working candidate `7f9e4608fb2a79271640e672aa652d3ebbf8028730b9a422af1fceb1d1109b01`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/enhancer-gene-linking), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-enhancer-gene-linking`**
> - Audited working candidate `7f9e4608fb2a79271640e672aa652d3ebbf8028730b9a422af1fceb1d1109b01`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/enhancer-gene-linking), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-atac-seq-enhancer-gene-linking

- Identity: sha256-manifest-v1 `7f9e4608fb2a79271640e672aa652d3ebbf8028730b9a422af1fceb1d1109b01` (6 files, 35,548 bytes), verified before and after. Carried forward from certified `44385431...` (88/100, Production Ready).
- Auditor independent of the change author. Phase: delta re-audit. No candidate edits.
- Decision: **candidate-ready**. Final 88 (Production Ready). Static 87, execution average 89.2, assertions 31/33, no veto, no open P0. Only P2 remains: EGL-013.

## Delta (shelf `44385431...` -> candidate)

Only `SKILL.md` frontmatter gains `category: Data Analysis` and `author: GPTomics` (+41 bytes). The other five files are byte-identical (`logs/identity_delta.log`). All files LF. Frontmatter parses as YAML, and `marketplace_manifests.skill_category` accepts `Data Analysis`.

## Scoring

No rubric dimension or assertion is touched by a metadata-only delta, so every static category, input score and assertion is carried unchanged.

## Open finding

- EGL-013 (P2): open. `scripts/run_abc.sh` is byte-identical, and its threshold lookup (lines 115-116, `awk ... {print $4}`) still does not strip CR. On ABC v1.1.2's CRLF `abc_thresholds.tsv`, output names still carry a carriage return. Values are correct.

Scripts: `scripts/dc_identity_delta.py`, `dc_build.py`, `dc_identity_after.py`, `validate_report.py` (the prior run's, unchanged; `logs/schema_validation.log` valid).

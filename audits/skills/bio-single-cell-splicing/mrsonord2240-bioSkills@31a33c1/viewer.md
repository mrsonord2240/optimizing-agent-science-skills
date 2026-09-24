> **Audit record for `bio-single-cell-splicing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@31a33c1](https://github.com/mrsonord2240/bioSkills/tree/31a33c13b6b6dd92395c7d399245534317ae1f39/alternative-splicing/single-cell-splicing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), final-pass@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# bio-single-cell-splicing — final pass

**94/100 — Production Ready**

Exact source: `31a33c13b6b6dd92395c7d399245534317ae1f39` (`alternative-splicing/single-cell-splicing`). `auditor_independent=false`: this is a fixer final-pass audit, not an independent re-audit. Execution evidence was produced on skill-content parent `540d2a2`; `31a33c1` only makes the unchanged description valid colon-safe YAML.

The previous P1 scQuint failure and all recorded P2 issues are corrected. The guide is now a 130-line chemistry and decision layer with seven linked tool references. scQuint documents its version-specific contig contract and fails early on zero annotation; MARVEL RI includes `thread=2` and explicit read length; unsupported 10X figures are gone.

Validation used the archived MARVEL RI demo (the exact corrected call completed: 10 rows across 26 cells), compatible and incompatible scQuint contig fixtures, and fresh documentation, BRIE2/SpliZ contract, and shuffled synthetic pseudobulk inputs. The exact pseudobulk helper conserved 630/630 reads and rejected `RangeIndex` metadata.

The only remaining unexecuted route is SpliZ because Nextflow is unavailable; the source explicitly says so and gives a configuration-verification route. See `run/finalpass_540d2a2.md` for raw evidence.

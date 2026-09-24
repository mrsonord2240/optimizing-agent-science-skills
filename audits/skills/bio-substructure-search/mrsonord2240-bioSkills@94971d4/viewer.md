> **Audit record for `bio-substructure-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@94971d4](https://github.com/mrsonord2240/bioSkills/tree/94971d4a4427eb5c682cd860eee91e8d9e41adc7/chemoinformatics/substructure-search) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0 exact-commit focused re-audit.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-substructure-search

Re-audited 2026-09-24 against exact clean commit `94971d4a4427eb5c682cd860eee91e8d9e41adc7` in `agent/fix-bio-substructure-search`, based on staging `main` at `4d483d0451fcd60cb3ab62dfa4cd047ec59b3615`.

The original canonical report and viewer are preserved in `re-audit-20260924/pre-fix/`.

## Result

| Measure | Pre-fix | Re-audit |
|---|---:|---:|
| Static score | 87.0 | 96.0 |
| Execution average | 89.3 | 92.7 |
| Assertions | 24/30 | 30/30 |
| Final score | 88/100 | **94/100** |
| Grade | Limited Release | **Production Ready** |
| Open P0 / P1 / P2 | 0 / 2 / 4 | **0 / 0 / 0** |

All structural and research vetoes pass. The source worktree was clean at the exact commit above.

## Fixed executable contracts

- The canonical ester SMARTS is now `[CX3](=[OX1])[OX2][#6]` in both the Skill and the executable example. It matched both isopropyl acetate and phenyl acetate.
- `compile_smarts()` rejects empty strings, malformed queries, and zero-atom queries with a concise `ValueError`. The basic, library-filter, reactive, and example paths use it, so invalid SMARTS cannot reach RDKit as an opaque Boost signature error or silently empty an include filter.
- `pains_filter()` returns `clean`, `flagged`, and zero-based `invalid` positions. An unparsed molecule is now visible to the caller.
- Custom reactive SMARTS compile once per configuration. The section now makes clear that enones/curcumin and beta-lactam antibiotics are flags for assay/context review, not automatic deletions.

## Calibrated scientific guidance

The PAINS failure mode now limits its claims to RDKit's actual catalog: rhodanines and catechols are represented, while curcumin does not have a curcumin-specific RDKit PAINS entry. The recursive-SMARTS guidance replaces an unsupported 10–100x rule with the measured 1.6x (one-level) and 3.7x (deeply nested) reference costs on 2,000 molecules. BRENK’s 36% reference flag rate in a lead-like set is presented as collection-specific, with category review rather than a deletion quota.

## Evidence

- Exact-commit snippet execution and documentation assertions: `re-audit-20260924/run-focused/focused_validation.out`
- Preserved pre-fix audit: `re-audit-20260924/pre-fix/`

No P0, P1, or P2 findings remain.

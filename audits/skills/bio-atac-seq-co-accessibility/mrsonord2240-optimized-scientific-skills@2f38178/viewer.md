> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-co-accessibility) match audited candidate `f7b386a41a3f37d483683ad7e3368688722632fab74595e3a56b3f04c1d8ed38` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-co-accessibility`**
> - Audited working candidate `f7b386a41a3f37d483683ad7e3368688722632fab74595e3a56b3f04c1d8ed38`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/co-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-co-accessibility`**
> - Audited working candidate `f7b386a41a3f37d483683ad7e3368688722632fab74595e3a56b3f04c1d8ed38`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/co-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit viewer: bio-atac-seq-co-accessibility (independent delta re-audit, 2026-09-30)

Candidate `sha256-manifest-v1 f7b386a41a3f37d483683ad7e3368688722632fab74595e3a56b3f04c1d8ed38` (5 files, 37,539 bytes), verified before and after. Carried forward from certified `0aac567b...` (85/100, Production Ready). Auditor did not make these changes; no candidate bytes edited.

**Result: 85 / 100 (84.98 unrounded), Production Ready, candidate-ready.** Static 83 (x0.4 = 33.2), execution average 86.3 (x0.6 = 51.8), assertions 31/32. Skill veto PASS, research veto PASS. The margin over the 85 gate is still thin.

## Delta (shelf `0aac567b...` -> candidate)

Exactly the listed changes; nothing else (`logs/identity_delta.log`):

- `SKILL.md`: frontmatter `category: Data Analysis`, `author: GPTomics`.
- `references/usage-guide.md` line 30: prompt now says `(TSS +/- 2 kb)` instead of `tssRegion=c(-2000, 500)`.

All files LF; frontmatter parses as YAML; `marketplace_manifests.skill_category` accepts `Data Analysis`.

## Re-scoring

| Item | Prior | Now | Reason |
|---|---:|---:|---|
| agent_usability | 14 | 15 | TSS window is now +/- 2 kb in SKILL.md step 5, usage-guide lines 30/46/63 and `cicero_workflow.R` (`tss_pad=2000`, `resize(width=2*tss_pad, fix='center')`) |
| Other seven static categories | carried | carried | untouched |
| All seven inputs, 32 assertions | carried | carried | no executed surface changed (script and method reference byte-identical) |

## Findings

| ID | Severity | Disposition |
|---|---|---|
| COACC-015 | P3 in the ledger, merged into the prior P2 recommendation | Resolved (static; grep of all TSS-window mentions) |
| COACC-014 | P2 | **Open.** `cicero_workflow.R` is byte-identical, so the zero-read cell still halts with 'attempt to set an attribute on NULL'. The recommendation is retitled to cover this half only. |
| COACC-001..013 | - | Carried as certified |

Scripts: `scripts/dc_identity_delta.py`, `dc_build.py`, `dc_identity_after.py`, `validate_report.py` (the prior run's, unchanged; `logs/schema_validation.log` VALID). `candidate-manifest.tsv` is the exact manifest hashed.

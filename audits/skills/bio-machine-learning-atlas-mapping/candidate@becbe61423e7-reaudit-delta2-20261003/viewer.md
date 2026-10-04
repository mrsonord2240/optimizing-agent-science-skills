> **Audit record for `bio-machine-learning-atlas-mapping`**
> - Audited working candidate `becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/atlas-mapping), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker E2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-atlas-mapping

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes: frontmatter description trimmed to its "Use when" clause), lane E2, worker E2 (did not normalize, tool, audit or fix this Skill)
Exact candidate content SHA-256: `becbe61423e78eaae064b907ae4dc929d87852078244bf2586f218ca69b7eab3` (7 files, 39428 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04` (final 87), scores carried forward; only the dimension touched by the change was re-scored.

## Result

**Static 87/100; Execution average 85.7/100; Final 86.2 (86); assertion pass rate 28/29; Layer 1 33.8/40; Layer 2 51.8/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: **candidate-ready** for exact identity `becbe61423e7`.

## Delta qualification

- Only `SKILL.md` differs from the certified bytes; all other files are byte-identical. The SKILL.md line diff is exactly one line, the `description:` frontmatter line.
- Reverting `fix-description-20261003/edits.json` on a scratch copy reproduces `8b4d96ad2465bd169dffb835c808d5783981f4acdc1f1e1121dbd9ab78dfbc04` (the certified identity).
- Frontmatter parsed with PyYAML `safe_load`: valid, `description` is one `str` (174 chars), keys name, category, description, tool_type, primary_tool, license, author, `name` equals the directory.
- No script, command, or body statement changed, so the certified execution evidence stands unchanged (SKILL.md body is byte-identical to the certified body).

## Verdict on the trimmed description

**Accurate but not a sufficient discriminator: one P2 finding (AM-009).** "Use when annotating new single-cell datasets against a pre-trained reference atlas, deciding which mapping method fits, or judging whether transferred labels are trustworthy."
Shelf sibling `bio-single-cell-cell-annotation` says "annotating cell types from a reference atlas or pretrained model, transferring labels onto a query, assessing prediction confidence and rejection". The two triggers now read alike. The removed tool list (scArches surgery, Symphony, scPoli, popV, foundation models, out-of-distribution gating) and the removed pointer to cell-annotation were the separators, and the body has no hand-off to cell-annotation (it names markers-annotation, batch-integration, preprocessing, doublet-detection). An agent choosing between them has no signal to prefer the projection-and-OOD-gating Skill, and a query for a scArches or Symphony mapping may be routed to the classifier Skill. `bio-single-cell-batch-integration` (no reference) is separated adequately.
Static score moved: **yes, 88 to 87**. agent_specific 17 to 16 (trigger precision, rubric 8.1: precise to mostly precise, with over-triggering risk). Static weighted 34.8; execution average 85.7 unchanged; sum 86.2, final 86 (was 87). Still Production Ready.

## Open findings

- P2: AM-008 Marker check: no message when nothing is checkable, and no listed-versus-used marker count
- P2: AM-009 Description no longer separates it from cell-annotation

All other certified dispositions are unchanged.

## Not executed

Unchanged from the certified record; nothing was rerun. `tools/smoke_irfinder.sh` was not run.

## Evidence

Run root `F:\OpenScience\audits\bio-machine-learning-atlas-mapping\reaudit-delta2-20261003\` (scripts/qualify_delta2.py, scripts/build_delta2.py, logs/qualify.json).

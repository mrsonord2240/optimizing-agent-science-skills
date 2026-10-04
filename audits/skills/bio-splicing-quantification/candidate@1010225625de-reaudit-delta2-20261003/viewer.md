> **Audit record for `bio-splicing-quantification`**
> - Audited working candidate `1010225625de8bd6106b0c187dd8b1459d3ae84e91abeb44a7df95a8bdef792d`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alternative-splicing/splicing-quantification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker E2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes: frontmatter description trimmed to its "Use when" clause), lane E2, worker E2 (did not normalize, tool, audit or fix this Skill)
Exact candidate content SHA-256: `1010225625de8bd6106b0c187dd8b1459d3ae84e91abeb44a7df95a8bdef792d` (5 files, 41707 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc` (final 85), scores carried forward; only the dimension touched by the change was re-scored.

## Result

**Static 84/100; Execution average 86.4/100; Final 85.4 (85); assertion pass rate 35/37; Layer 1 34.9/40; Layer 2 51.6/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: **candidate-ready** for exact identity `1010225625de`.

## Delta qualification

- Only `SKILL.md` differs from the certified bytes; all other files are byte-identical. The SKILL.md line diff is exactly one line, the `description:` frontmatter line.
- Reverting `fix-description-20261003/edits.json` on a scratch copy reproduces `247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc` (the certified identity).
- Frontmatter parsed with PyYAML `safe_load`: valid, `description` is one `str` (95 chars), keys name, category, description, tool_type, primary_tool, license, author, `name` equals the directory.
- No script, command, or body statement changed, so the certified execution evidence stands unchanged (SKILL.md body is byte-identical to the certified body).

## Verdict on the trimmed description

**Sufficient, accurate, no finding.** "Use when measuring splice-site usage or isoform inclusion ratios (PSI) from short-read RNA-seq."
Shelf siblings checked (read-only): `bio-differential-splicing` (comparing patterns between groups), `bio-long-read-splicing` (long reads), `bio-single-cell-splicing`, `bio-splicing-qc` (data suitability), `bio-outlier-splicing-detection` (single-patient outliers), `bio-splice-variant-prediction` (DNA variants), `bio-isoform-switching` (DTU consequences), `bio-sashimi-plots` (figures). Each has a trigger on a different activity or data type; "measuring PSI ... short-read" does not collide with any of them. Related Skills routing stays in the body.
Observation, not a defect: tool names and "intron retention" no longer appear in the description, so a request phrased only as "quantify intron retention with IRFinder" relies on the agent reading IR as splicing quantification. IR is one of the five canonical classes the Skill covers; the trigger still reads as a fit.
Static score moved: **no**. Category scores are unchanged (static 84, agent_specific 18/20); static weighted 84 x 0.4 = 33.6; execution average 86.4 x 0.6 = 51.84 (recorded 51.8); sum 85.44, recorded 85.4, rounds to 85. The margin over the 85 gate is 0.44, identical to the certified record. A one-point static deduction would give 85.04, still at the gate; none was applied because the trigger is precise.

## Open findings

- P2: parse_rmats_output raises a raw KeyError on an rMATS file with zero events
- P2: SQ-13 rewording gives an inexact condition for the maxima

All other certified dispositions are unchanged.

## Not executed

Unchanged from the certified record; nothing was rerun. `tools/smoke_irfinder.sh` was not run.

## Evidence

Run root `F:\OpenScience\audits\bio-splicing-quantification\reaudit-delta2-20261003\` (scripts/qualify_delta2.py, scripts/build_delta2.py, logs/qualify.json).

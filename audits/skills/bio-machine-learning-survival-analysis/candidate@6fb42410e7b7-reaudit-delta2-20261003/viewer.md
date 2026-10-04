> **Audit record for `bio-machine-learning-survival-analysis`**
> - Audited working candidate `6fb42410e7b70eff829bac23fce3c05a0a9941abff229c15570619de1f7f62d3`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/survival-analysis), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) delta re-audit worker E2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-machine-learning-survival-analysis

Generated: 2026-10-03
Audit type: independent delta re-audit (text-only change to certified bytes: frontmatter description trimmed to its "Use when" clause), lane E2, worker E2 (did not normalize, tool, audit or fix this Skill)
Exact candidate content SHA-256: `6fb42410e7b70eff829bac23fce3c05a0a9941abff229c15570619de1f7f62d3` (5 files, 33616 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Certified baseline: `eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb` (final 87), scores carried forward; only the dimension touched by the change was re-scored.

## Result

**Static 88/100; Execution average 85.6/100; Final 86.6 (87); assertion pass rate 24/24; Layer 1 34.6/40; Layer 2 51.0/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: **candidate-ready** for exact identity `6fb42410e7b7`.

## Delta qualification

- Only `SKILL.md` differs from the certified bytes; all other files are byte-identical. The SKILL.md line diff is exactly one line, the `description:` frontmatter line.
- Reverting `fix-description-20261003/edits.json` on a scratch copy reproduces `eac9a589b7bdc8b56d0f832c060d837a502e4e4c3fd355310ed00582195d71fb` (the certified identity).
- Reverting the SA-006 edit (`fix-textbatch-20261003`) after the description edit reproduces `c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39`: the chain back to the earlier certified identity is fully reproduced.
- Frontmatter parsed with PyYAML `safe_load`: valid, `description` is one `str` (160 chars), keys name, category, description, tool_type, primary_tool, license, author, `name` equals the directory.
- No script, command, or body statement changed, so the certified execution evidence stands unchanged (SKILL.md body is byte-identical to the certified body).

## Verdict on the trimmed description

**Sufficient, accurate, no finding.** "Use when building an individualized time-to-event risk predictor or prognostic omics signature, choosing a survival model, or evaluating one beyond the C-index."
The clinical-biostatistics survival Skill is not on the shelf (`F:/optimized-scientific-skills/skills` has only `bio-clinical-biostatistics-adaptive-designs`); the removed pointer was to an ID that does not exist there. The prediction-versus-inference separation is carried by "individualized risk predictor ... beyond the C-index", and the body keeps the hand-off table (SKILL.md rows for KM, log-rank and trial hazard ratios -> clinical-biostatistics/survival-analysis). `bio-machine-learning-model-validation` is generic performance estimation and does not collide with a survival-specific trigger.
Observation, not a defect: "competing risks" and "Kaplan-Meier" are no longer named; a competing-risks CIF question still reads as time-to-event model building, and the body covers it.
Static score moved: **no** (88; agent_specific 18/20; execution average 85.6; final 35.2 + 51.4 = 86.6, 87).

## Open findings

- none

All other certified dispositions are unchanged.

## Not executed

Unchanged from the certified record; nothing was rerun. `tools/smoke_irfinder.sh` was not run.

## Evidence

Run root `F:\OpenScience\audits\bio-machine-learning-survival-analysis\reaudit-delta2-20261003\` (scripts/qualify_delta2.py, scripts/build_delta2.py, logs/qualify.json).

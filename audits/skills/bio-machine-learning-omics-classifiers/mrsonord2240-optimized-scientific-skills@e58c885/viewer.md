> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@e58c885](https://github.com/mrsonord2240/optimized-scientific-skills/tree/e58c8855faaf8dcba2341453d73b62bcade3e78c/skills/bio-machine-learning-omics-classifiers) match audited candidate `a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-machine-learning-omics-classifiers`**
> - Audited working candidate `a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/machine-learning/omics-classifiers), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-machine-learning-omics-classifiers (2026-10-03)

Candidate `a2d417f41e37007d7a2a3ea4d76b744cf1be42485be95576f42dee806584616f` (7 files, 50363 bytes). Certified baseline `906900fae480...` scored 88 (Production Ready); that run's execution evidence is reused because no script, reference or usage-guide byte changed.

## Delta qualification
- Reverting `fix-description-20261003/edits.json` on a scratch copy reproduces the certified manifest `906900fae480655dca3808442d858f84b17aace68513ed281607842a0151276f` (files=7, bytes=50806; script `scripts/revert_check.py`).
- `diff -r` of candidate vs reverted copy: exactly one line, `SKILL.md` line 4 (`description:`). Nothing else differs.
- The new frontmatter parses with `yaml.safe_load`; name, category, tool_type, primary_tool, license and author are unchanged.

## Judgement of the new description
"Use when building a classifier from expression, methylation, or variant data, choosing an algorithm for high-dimensional small-n data, or diagnosing a suspiciously perfect AUC."
- Accurate: all three cases are covered by SKILL.md and were exercised in the certified runs. No false statement introduced.
- Sufficient trigger: states when to use it. Separated from survival-analysis (time-to-event), biomarker-discovery (candidate biomarkers), atlas-mapping (single-cell references) by its own text.
- Finding OC-013 (P2): the "suspiciously perfect AUC" clause overlaps model-validation (leakage detection) and prediction-explanation (batch/shortcut debugging) and the pointers that disambiguated it are gone; imbalance, calibration and batch shortcuts are not in the description. Risk of mis-routing is modest because the body still carries the hand-offs. The trim itself is not recorded as a defect.

## Scores
Carried forward: static 88, execution average 87.9, final 88 (Production Ready). The agent_specific note was updated but its 18/20 stands, so the static score did not move. Three delta assertions (qualification, YAML, accuracy) added and passed: 34 of 36 (94.4%). Open: P2 OC-012 (unchanged) and P2 OC-013 (new).

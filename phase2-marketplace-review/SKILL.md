---
name: phase2-marketplace-review
description: Phase 2 marketplace review for bioinformatics skills — assesses maintainability for marketplace operators
license: MIT
skill-author: mrsonord2240
---

# Phase 2 Marketplace Review

Formalized review process for bioinformatics skills focusing on **long-term maintainability** rather than execution verification.

## Purpose

Phase 1 and formal audits verify **execution** (code runs, tools work). This review assesses **maintainability** — what marketplace operators need to keep skills current and support users.

## When to Use

After Phase 1 checkpoint is complete and formal audit is done:
- Phase 1 verification passed (dependencies installed, tools functional)
- Formal audit score available (Production Ready / Limited Release)
- Skill ready for marketplace submission

## Review Dimensions

| Dimension | What to Evaluate |
|-----------|------------------|
| **Version Health** | API version notes, migration guidance, deprecation warnings |
| **Edge Case Coverage** | Documented failure modes, input validation, error handling |
| **Install Transparency** | Installation steps, dependency versions, environment setup |
| **Maintainer Hand-off** | Extension points, testing strategy, update procedure |

## Scoring Rubric

| Score Range | Status |
|-------------|--------|
| 90-100 | ✅ **Excellent** - Production ready, no maintenance concerns |
| 80-89 | ✅ **Good** - Minor documentation gaps, ready for limited release |
| 70-79 | ⚠️ **Acceptable** - Works but needs clarity improvements |
| <70 | ❌ **Needs Work** - Structural issues or missing critical documentation |

## Output Format

Generate `marketplace_review_<skill_name>.md` with:

```markdown
Phase 2 Marketplace Review: <skill_name>
═══════════════════════════════════

Review Date: YYYY-MM-DD
Audit Score: XX/100 (Grade)
Review Status: ✅ Pass / ⚠️ Needs Update / ❌ Hold

## Dimension Scores
- Version Health: XX/100
- Edge Case Coverage: XX/100
- Install Transparency: XX/100
- Maintainer Hand-off: XX/100

## Strengths
- [List 2-4 strengths]

## Issues Found
- [P0] Must fix before marketplace submission
- [P1] Fix before production release
- [P2] Address before full scale

## Recommendations
[Actionable fixes]

## Conclusion
[Approved for Marketplace / Update Required / Not Ready]
```

## Input Requirements

1. **SKILL.md** - Full skill content
2. **CHECKPOINT.md** - Phase 1 verification results
3. **eval_report_*.json** - Formal audit results (if available)

## Notes

- Focus on what marketplace maintainers need (versioning, updates, user support)
- Separate from execution-focused formal audit results
- Document API drift risks (e.g., external API dependencies)
- Prioritize P0 issues that block marketplace submission

## Related Skills

- `phase1-audit` - Dependency verification and environment setup
- `phase2-audit` - Formal content quality review
- `skill-auditor` - Full formal evaluation with execution testing

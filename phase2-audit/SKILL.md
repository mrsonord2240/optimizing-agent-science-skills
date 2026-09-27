---
name: phase2-audit
description: Phase 2 audit for bioinformatics skills — quality scoring and grading based on SKILL.md and Phase 1 checkpoint
license: MIT
skill-author: mrsonord2240
---

# Phase 2 Audit

Formalized review process for bioinformatics skills that have passed Phase 1 (dependency/environment verification).

## When to Use

Use this skill after:
- Phase 1 audit is complete (checkpoint generated)
- All required tools/packages are installed and verified
- The SKILL.md needs formal scoring and deployment recommendation

## Process

### Step 1: Read Artifacts

Load the two source files:
1. **SKILL.md** - The skill content
2. **CHECKPOINT.md** - Phase 1 verification results

### Step 2: Score Dimensions

Score each of the four dimensions on 0-100 scale:

| Dimension | What to Evaluate | Max |
|-----------|------------------|-----|
| **Code Quality** | Syntax correctness, error handling, edge case coverage | 100 |
| **Documentation** | Completeness, decision trees, failure modes, examples | 100 |
| **Version Compatibility** | Explicit version notes, API compatibility, migration guidance | 100 |
| **Practical Utility** | Actionability, cross-references, warnings about pitfalls | 100 |

**Dimension Scoring Rubric:**

| Score Range | Level | Description |
|-------------|-------|-------------|
| 90-100 | Excellent | No issues found; production-grade quality |
| 80-89 | Good | Minor documentation gaps; ready for limited use |
| 70-79 | Acceptable | Works but needs clarity improvements |
| <70 | Needs Work | Structural issues or broken examples |

### Step 3: Calculate Final Score

```
Final Score = (Code Quality + Documentation + Version Compatibility + Practical Utility) / 4
```

### Step 4: Grade and Recommend

| Score | Grade | Status | Recommendation |
|-------|-------|--------|----------------|
| 90-100 | A | Production Ready | Deploy publicly |
| 80-89 | B+ | Limited Release | Throttled rollout; note known limitations |
| 70-79 | C | Beta | Internal use only; fix documentation before wider release |
| <70 | D/F | Needs Fix | Do not deploy; address issues |

### Step 5: Document Findings

Record findings in structured format:

```
Phase 2 Audit: <skill_name>
═══════════════════════════════════

Score: XX/100
Grade: A/B/C/D

## Dimension Scores
- Code Quality: XX/100
- Documentation: XX/100
- Version Compatibility: XX/100
- Practical Utility: XX/100

## Strengths
- [List 2-4 strengths]

## Issues Found
- [List issues with severity: P0/P1/P2]

## Recommendations
- [P0] [Must fix before deployment]
- [P1] [Fix before production release]
- [P2] [Address before full scale]

## Conclusion
[Production Ready / Limited Release / Beta / Needs Fix]
```

## Input Requirements

1. **SKILL.md** - Full skill content
2. **CHECKPOINT.md** - Phase 1 results (verification status, dependency resolution)

## Output Format

Structured markdown report with:
- Final score and grade
- Dimension breakdown
- Strengths (2-4 items)
- Issues (organized by severity)
- Recommendations (actionable fixes)
- Deployment recommendation

## Notes

- Phase 2 focuses on **content quality**, not environment setup
- Use Phase 1 checkpoint to distinguish between skill defects and environment issues
- For skills with known limitations (e.g., API version mismatches), document the fix needed

## Related Skills

- `phase1-audit` - Dependency verification and environment setup
- `skill-auditor` - Full formal evaluation with execution testing

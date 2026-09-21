# Skill audit thresholds (Specialist gates parked 2026-09-21)

Two gates apply to every Skill audit. The Specialist-only gates (1 and 4-9) are parked in
`specialists/THRESHOLD.md`, and keep their original numbers, so these two stay 2 and 3.

2. **Every Skill is audited and deployable.** It has a `skill-auditor` report, no veto gate fired,
   `deployable: true`, no open P0 recommendation, and a final score ≥ 75 (Limited Release or
   better). The AIPOCH score history behind "which score" is in `specialists/THRESHOLD.md`; it does
   not apply to bioSkills, whose reports carry per-input runs.
3. **Core workflow Skills are Production Ready.** A Skill marked `core` scores ≥ 85.

## The target: Production Ready (2026-09-21)

Gates 2 and 3 are the floor a Skill must clear to ship. **The target for every Skill is ⭐ Production
Ready**, and every fix and re-audit aims at it: a Skill sitting at ✅ Limited Release, or ⚠️ Beta Only
with a fix pending, is unfinished, not done. A fixer works until the Skill meets all of this; a
re-auditor reports which line it misses (source: `skill-auditor/references/scoring_rubric.md` §4-5).

| Requirement | Production Ready | Limited Release (floor) |
| --- | --- | --- |
| Final score | ≥ 85 | 75-84 |
| Static score (/100) | ≥ 80 | ≥ 70 |
| Execution average (/100) | ≥ 85 | ≥ 75 |
| Layer 1, basic rubric (/40 per output, averaged) | ≥ 32 | ≥ 28 |
| Layer 2, specialized rubric (/60 per output, averaged) | ≥ 48 | ≥ 42 |
| Assertion pass rate | ≥ 90 % | ≥ 80 % |
| Veto (T1-T4, M1-M4) | none fired | none fired |
| Open P0 | none | none |

Missing any one floor drops the grade a tier whatever the final score says (an 87 with an 85 % assertion
pass rate is Limited Release). Two safety-assertion FAILs cap the grade at ⚠️ Beta Only, and a veto
forces ❌ Reject.

# Skill audit thresholds (Specialist gates parked 2026-09-21)

Two gates apply to every Skill audit. The Specialist-only gates (1 and 4-9) are parked in
`specialists/THRESHOLD.md`, and keep their original numbers, so these two stay 2 and 3.

2. **Every Skill is audited and deployable.** It has a `skill-auditor` report, no veto gate fired,
   `deployable: true`, no open P0 recommendation, and a final score ≥ 75 (Limited Release or
   better). The AIPOCH score history behind "which score" is in `specialists/THRESHOLD.md`; it does
   not apply to bioSkills, whose reports carry per-input runs.
3. **Core workflow Skills are Production Ready.** A Skill marked `core` scores ≥ 85.

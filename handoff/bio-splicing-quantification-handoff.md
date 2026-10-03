# Handoff: bio-splicing-quantification / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-03
- Status: fixed, awaiting delta re-audit
- Owner leaving: text-only fix worker (fix-textbatch-20261003)
- Next role: reaudit-scientific-skill, delta mode (revert each changed file to confirm the certified bytes reappear)

## Identities

- Working tree: F:\OpenScience\wt\norm-bio-splicing-quantification\skills\bio-splicing-quantification
- Certified identity (keep): 0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf, files=5, bytes=42079
- Certifying record (keep): F:\optimizing-agent-science-skills\audits\skills\bio-splicing-quantification\candidate@0c0354add99b-run-reaudit-1
- New candidate identity: 247bcf26db1833bc443dc9d651595ef84068f43a2593067f7c3bda72bd7e7adc, files=5, bytes=42306; `skill_preflight --offline` PASS (expected no-Skill-root-LICENSE warning)

## Dispositions

| ID | State | Note |
|---|---|---|
| SQ-13 | fixed (text only) | see fix log |
| SQ-12 (needs code) | open, untouched | needs code; waits for a later run |

Other previously open findings: unchanged, see certifying record.

## Changed files (before/after sha256 in the fix log)

- SKILL.md: JC IncFormLen/SkipFormLen stated as maxima for exons at least read-length long; per-event rMATS lengths must be used (719 of 958 chrX SE rows are 148/74)

## Evidence

- Fix log: F:\OpenScience\audits\bio-splicing-quantification\fix-textbatch-20261003\fix-log.md
- No scripts executed beyond syntax checks; no executable statement changed.

## Safety

- Tooling impact: none
- Touched only this Skill directory (plus this handoff and the fix log); no commit or push
- Untouched: records test/validate.bats, shelf .vscode/

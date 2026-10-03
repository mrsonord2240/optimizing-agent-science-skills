# Handoff: bio-data-visualization-ggplot2-fundamentals / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-03
- Status: fixed, awaiting delta re-audit
- Owner leaving: text-only fix worker (fix-textbatch-20261003)
- Next role: reaudit-scientific-skill, delta mode (revert each changed file to confirm the certified bytes reappear)

## Identities

- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Certified identity (keep): be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120, files=5, bytes=22972
- Certifying record (keep): F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@be703ae7f695-reaudit-dv2-20261003
- New candidate identity: 228c088cf299564fd21d2b9d79a3963e5c0b4a500158bcb4732a1b277e6160e6, files=5, bytes=23322; `skill_preflight --offline` PASS (expected no-Skill-root-LICENSE warning)

## Dispositions

| ID | State | Note |
|---|---|---|
| GG-011, GG-012 | fixed (text only) | see fix log |
| GG-010 (needs code) | open, untouched | needs code; waits for a later run |

Other previously open findings: unchanged, see certifying record.

## Changed files (before/after sha256 in the fix log)

- SKILL.md: GG-011 envelope with width and height, airway-only, label boxes only, open the figure; GG-012 removed stray axes=collect remark
- usage-guide.md: GG-012 install line adds patchwork and dplyr

## Evidence

- Fix log: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-textbatch-20261003\fix-log.md
- No scripts executed beyond syntax checks; no executable statement changed.

## Safety

- Tooling impact: none
- Touched only this Skill directory (plus this handoff and the fix log); no commit or push
- Untouched: records test/validate.bats, shelf .vscode/

# Handoff: bio-data-visualization-matplotlib-fundamentals / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-03
- Status: fixed, awaiting delta re-audit
- Owner leaving: text-only fix worker (fix-textbatch-20261003)
- Next role: reaudit-scientific-skill, delta mode (revert each changed file to confirm the certified bytes reappear)

## Identities

- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Certified identity (keep): f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a, files=5, bytes=24264
- Certifying record (keep): F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f1efaf7eef6c-reaudit-dv2-20261003
- New candidate identity: 79a08cbdf5339dbf6f824d9532cc4720ef00102a9985831c5c56c051c8150611, files=5, bytes=24925; `skill_preflight --offline` PASS (expected no-Skill-root-LICENSE warning)

## Dispositions

| ID | State | Note |
|---|---|---|
| MPL-010 | fixed (text only) | see fix log |
| none | open, untouched | needs code; waits for a later run |

Other previously open findings: unchanged, see certifying record.

## Changed files (before/after sha256 in the fix log)

- SKILL.md: discloses private Plot.plot()._figure, 22% reserve, 13 mm overflow, public alternative
- scripts/matplotlib_phd.py: comment lines only, same disclosure

## Evidence

- Fix log: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-textbatch-20261003\fix-log.md
- No scripts executed beyond syntax checks; no executable statement changed.

## Safety

- Tooling impact: none
- Touched only this Skill directory (plus this handoff and the fix log); no commit or push
- Untouched: records test/validate.bats, shelf .vscode/

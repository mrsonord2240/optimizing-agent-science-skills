# Handoff: bio-data-visualization-volcano-and-ma-plots / reaudit-scientific-skill (delta mode)

- Updated: 2026-10-03
- Status: fixed, awaiting delta re-audit
- Owner leaving: text-only fix worker (fix-textbatch-20261003)
- Next role: reaudit-scientific-skill, delta mode (revert each changed file to confirm the certified bytes reappear)

## Identities

- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Certified identity (keep): fa3ec8783a79b7c7a36fcf2d941d4fcc1aca6ab2ec3a8925e72fe6fa3a9af008, files=7, bytes=37956
- Certifying record (keep): F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\candidate@fa3ec8783a79-reaudit-dv1-20261003
- New candidate identity: a86f2698a953bfc46b2db74122acd9d20a49a5e0195bace6e3663282a44d8d83, files=7, bytes=37959; `skill_preflight --offline` PASS (expected no-Skill-root-LICENSE warning)

## Dispositions

| ID | State | Note |
|---|---|---|
| VOL-009 | fixed (text only) | see fix log |
| VOL-010 (needs code) | open, untouched | needs code; waits for a later run |

Other previously open findings: unchanged, see certifying record.

## Changed files (before/after sha256 in the fix log)

- SKILL.md: median 0.77 -> 0.76; MA 23/444 KB now tied to 29,391 rows
- references/failure-modes.md: 49 -> 39 hidden genes
- references/reconciliation-thresholds-pushback.md: 49 -> 39 hidden genes
- scripts/volcano_phd.R: save comment only: 17,994 drawn points, 0.56 and 0.69 MB PDFs

## Evidence

- Fix log: F:\OpenScience\audits\bio-data-visualization-volcano-and-ma-plots\fix-textbatch-20261003\fix-log.md
- No scripts executed beyond syntax checks; no executable statement changed.

## Safety

- Tooling impact: none
- Touched only this Skill directory (plus this handoff and the fix log); no commit or push
- Untouched: records test/validate.bats, shelf .vscode/

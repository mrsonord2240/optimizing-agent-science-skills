# Handoff: bio-data-visualization-matplotlib-fundamentals / reaudit-scientific-skill

- Updated: 2026-10-03T16:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 1b)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 5a5bd8a000b20722cdcf14b12a5adb381bbecad2d16d952870cbbdf8dddb4cc8 (files=5, bytes=23535); skill_preflight PASS (online and offline-identical)
- Previous identity audited: 146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78 (Beta Only 74)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@146857c3b9b5-initial-dv1-20261003\

## Completed this phase

- All six findings fixed; changed files: SKILL.md, usage-guide.md, references/failure-modes.md, references/chart-recipes.md, scripts/matplotlib_phd.py.
- Re-ran fixed script, all five SKILL.md python blocks (real airway table), and recipe checks; measured page mm, colour binding, font sizes, pdffonts, SVG text.
- Fix log: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-dv1-20261003\fix-log.md (scripts\, logs\, out\ alongside).

## Finding dispositions

| ID | Sev | State | Evidence |
|---|---|---|---|
| MPL-001 | P1 | fixed | logs\f1_phd_check.log, logs\f3_skill_snippets.log (all pages exact mm) |
| MPL-002 | P1 | fixed | logs\f3_skill_snippets.log (Up-first airway data), f1 (500/500 points) |
| MPL-003 | P2 | fixed | logs\f2_recipes.log (Axes method; 1.5 MB vs 24 KB measured) |
| MPL-004 | P2 | fixed | logs\f2_recipes.log, f3 (svg <text> present) |
| MPL-005 | P2 | fixed | logs\f1_phd_check.log (6/7 pt only), logs\pdffonts_phd.log (TrueType only) |
| MPL-006 | P2 | fixed | SKILL.md Color block runs (f3) |

New P2s found and fixed inline: seaborn.objects rcParams/legend overflow, 183 vs 180 mm, grid snippet `data.items()`, missing numpy import (see fix-log.md).

## Required next actions

1. Independent re-audit of the exact identity above; check the so.Plot legend=False tradeoff and seaborn.objects theme line judgement.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md (fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721, unchanged)
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/py.sh <run>\scripts\f1_phd_check.py <skilldir> <outdir>` (f2_recipes.py <outdir>, f3_skill_snippets.py <skilldir> <outdir>)
- Restricted-access items: none
- Tooling impact: none (same matplotlib 3.11.2/seaborn/cmcrameri and inputs; no new dependency, wrapper or executable)

## Worktree safety

- Run-owned changes: five Skill files above; run dir fix-dv1-20261003; this handoff
- Pre-existing/user-owned changes: records test/validate.bats, shelf .vscode/ (untouched); sibling Skill dirs untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

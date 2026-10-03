# Handoff: bio-data-visualization-matplotlib-fundamentals / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03T21:00:00-07:00
- Lane: 1 (1b)
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 1b, run fix-dv1-20261003)
- Next role: prepare-scientific-skill-tooling (delta mode, surface matplotlib_phd.py), then a fresh reaudit-scientific-skill (full, not delta: no prior candidate-ready record)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a (files=5, bytes=24264); `skill_preflight.py` PASS (offline PASS at start on the prior hash 5a5bd8a000b2...)
- Prior audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@5a5bd8a000b2-reaudit-dv1-20261003\ (85, assertions 20/23, not ready); it applies to the old identity only

## Completed this phase

- MPL-007, MPL-008, MPL-009 fixed; every other block/claim in both reference files executed (table below). Evidence run: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-dv1-20261003\ (scripts\, logs\, out\).
- Changed files: scripts/matplotlib_phd.py, references/chart-recipes.md, references/failure-modes.md. SKILL.md and usage-guide.md unchanged.

## Finding dispositions

| ID | Sev | State | What was measured | Evidence |
|---|---|---|---|---|
| MPL-001..006 | - | fixed (unchanged, not reopened) | regression rerun: r1 and r3 scripts PASS (pages exactly 89x70, 180x110, 89x90 mm; 6-7 pt text; dict palette shuffle; svg text; set_rasterization_zorder) | logs\r1_phd.log, logs\r3_skill_blocks.log |
| MPL-007 | P2 | fixed | seaborn.objects legend on again (`extent=[0,0,0.78,1]`, then `fig.legends[0]` set_loc center right, anchored on figure); volcano_so.pdf 89.0x70.0 mm, ArialMT CID TrueType, legend NS/Down/Up visible and fully inside the page (opened out\r1\volcano_so_pdf.png) | logs\r1_phd.log, logs\pdffonts_render.log |
| MPL-008 | P2 | fixed | `import numpy as np` added; ticks `np.arange(0, 6, 2)` = 3 ticks for 3 labels; runs with no `np` in the namespace, no warnings | logs\f1_recipes.log |
| MPL-009 | P2 | fixed | entry rewritten to reproduced behaviour only: tight_layout() is one-shot (clipped after later longer label or resize; constrained not); multi-axes colorbar warns "not compatible with tight_layout"; single colorbar did not clip; set_layout_engine after a colorbar raises ZeroDivisionError, before works | logs\f2_failure_modes.log |

## Per-block execution (matplotlib 3.11.2, seaborn 0.13.2, py.sh, MPLBACKEND=Agg)

- references/chart-recipes.md: 2 python blocks, 11 fragments (Scatter, Line, Bar, Box, Histogram, Heatmap | Log, Scientific, Date, Tick frequency, Grid), each run verbatim on its own axes with placeholder data bound outside the code: 11/11 PASS, zero warnings. (Fragments are alternatives that need different data shapes, so a whole block is not one script.)
- references/failure-modes.md: 0 python blocks; 8 entries plus the 10-row table, 22 checks of Trigger/Symptom/Fix: 22/22 PASS (scripts\f2_failure_modes.py); pdffonts type3 = Type 3, type42 = CID TrueType.
- Skill regression: r1 (matplotlib_phd.py unchanged runner) PASS; r3 (5 SKILL.md blocks, shuffled data, formats) PASS.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md (fingerprint 8923551f..., unchanged)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-dv1-20261003\ (scripts f1_recipes.py, f2_failure_modes.py, t_tight*.py probes; reuses reaudit r1/r3 scripts)
- Restricted-access items: none
- Tooling impact: changed (runnable surface scripts/matplotlib_phd.py, section 7 seaborn.objects, edited; no new dependency, runtime, input or wrapper, and it ran clean on the existing env)
- Runnable bytes changed: yes (scripts/matplotlib_phd.py, the objects example); re-audit must run it, not delta mode.
- Note for the auditor: the legend move uses `plot.plot()._figure.legends[0]` (private `_figure`); seaborn has no public handle.

## Worktree safety

- Run-owned changes: the three Skill files above; evidence dir above; this handoff
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/, sibling ggplot2 and volcano Skill dirs untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

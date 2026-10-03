# Handoff: bio-data-visualization-matplotlib-fundamentals / fix-scientific-skill

- Updated: 2026-10-03T19:00:00-07:00
- Lane: 1
- Status: phase-failed (re-audit rejected the exact identity: assertion floor not met)
- Owner leaving: reaudit-scientific-skill worker (lane 1 re-audit, fresh auditor)
- Next role: fix-scientific-skill (text-only edits), then a fresh reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 5a5bd8a000b20722cdcf14b12a5adb381bbecad2d16d952870cbbdf8dddb4cc8 (files=5, bytes=23535); preflight PASS at start and end, bytes unchanged
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@5a5bd8a000b2-reaudit-dv1-20261003\ (run dir F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\reaudit-dv1-20261003)

## Re-audit result

- Decision: NOT candidate-ready. Final 85 (numeric Production Ready), static 84, execution avg 85.4, L1 33.2, L2 52.2, no veto, no P0, but assertion pass rate 20/23 = 87 percent (< 90 floor).
- Prior MPL-001..006: all resolved (independent evidence in viewer.md, run scripts r1-r4).
- Failed/blocked surfaces: none blocked; three failed assertions below. Heavy-optional: none.

## Open findings (all P2, all text-only)

| ID | Evidence | Required disposition |
|---|---|---|
| MPL-007 | scripts\logs\r2_so_legend.log, figures\phd_volcano_so_nolegend.png | volcano_so.pdf has legend=False so Up/Down/NS colours are unlabelled; keep a legend on the page (extent=[0,0,0.78,1] then move fig.legends[0], verified in r2 variant E) or state a caption is required |
| MPL-008 | scripts\logs\r4_recipes_failures.log | chart-recipes.md Tick frequency snippet: np.arange(0,10,2) gives 5 ticks, 3 labels, ValueError; also add import numpy as np |
| MPL-009 | scripts\logs\r5_layout_dpi.log, r6_engine_minimal.log | failure-modes.md: tight_layout + ax= colorbar does not clip or overlap on 3.11.2; the alternative fig.set_layout_engine('constrained') raises ZeroDivisionError once a colorbar exists. Reword trigger, set engine before colorbars |

Not a finding, mention if editing: the 1.5 MB vs 24 KB large-N figure holds at default savefig dpi without alpha (166.9 KB at dpi 300, alpha 0.6).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md (fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721, unchanged)
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/py.sh <run>\scripts\r1_phd.py <skilldir> <outdir>` (r3_skill_blocks.py same args; r4_recipes_failures.py, r2/r5/r6/r7 per their headers); pdffonts via WSL scripts\pdffonts.sh
- Restricted-access items: none
- Tooling impact: none (no new dependency, input or wrapper)

## Worktree safety

- Run-owned changes: run dir above; published record dir under audits\skills; regenerated audits INDEX/BACKLOG/STATUS (npm run audits:index, audits:check clean)
- Pre-existing/user-owned: records test/validate.bats, shelf .vscode/, sibling ggplot2 and volcano Skill dirs untouched
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- Fix scope: three text edits (chart-recipes.md, failure-modes.md, scripts/matplotlib_phd.py); a fresh full re-audit is needed because the Skill has no prior candidate-ready record for delta mode

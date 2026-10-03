# Handoff: bio-data-visualization-matplotlib-fundamentals / fix-scientific-skill

- Updated: 2026-10-03T14:30:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78 (files=5, bytes=21575); skill_preflight --offline PASS before and after execution
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@146857c3b9b5-initial-dv1-20261003\report.json (Beta Only, final 74; static 77, exec 72.6; research veto PASS)
- Run root: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\initial-dv1-20261003\ (report.json, viewer.md, finding-ledger.md, scripts\, logs\, out\)

## Completed this phase

- Ran matplotlib_phd.py unchanged (5 PDFs; pdffonts all TrueType; page sizes measured) and rendered/opened the PDFs.
- Ran the SKILL.md seaborn volcano recipe on real airway results, plus Saving/Standard Setup, chart-recipes and failure-modes claims.
- Tested the tooling lead: the EPS-transparency warning did NOT reproduce on the Skill's own recipes (no EPS recipe in the Skill).
- Observed (upstream, not a Skill finding): pdf.fonttype=3 with ps.fonttype=42 set raises 'bytes must be in range(0, 256)' on matplotlib 3.11.2 (scripts\m3c_type3_bisect.py).
- No audit-local repair; no Skill bytes changed. Published record candidate@146857c3b9b5-initial-dv1-20261003.

## Required next actions

1. Fix MPL-001, MPL-002, MPL-005 in scripts/matplotlib_phd.py and the matching SKILL.md snippets (runnable bytes + text).
2. Fix MPL-003, MPL-004, MPL-006 (text only): references/failure-modes.md, references/chart-recipes.md, SKILL.md, usage-guide.md.
3. Re-run scripts\m1_phd_check.py, m2_real_volcano.py, m3_recipes.py from the run root on the fixed bytes; classify tooling impact (none expected).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-001 | P1 | open | logs\m1_phd_check.log | savefig.bbox='tight' gives 92.0/91.8/182.7 mm pages for 89/89/180 mm figures; drop bbox tight or document (script + SKILL.md) |
| MPL-002 | P1 | open | logs\m2_real_volcano.log; out\vol\volcano_skill_palette.png | list palette binds by data order (Up blue, Down orange on airway; ns orange in example); use dict palette + hue_order (script + text) |
| MPL-003 | P2 | open | logs\m3_recipes.log | fig.set_rasterization_zorder does not exist (Axes method); '50 MB' claim not reproduced (text) |
| MPL-004 | P2 | open | logs\m3_recipes.log | SVG text saved as paths; set svg.fonttype='none' or reword (text) |
| MPL-005 | P2 | open | logs\m1_phd_check.log | tab10 not CVD-safe, titlesize 8 > 5-7 pt, redundant panel titles (script) |
| MPL-006 | P2 | open | SKILL.md Color section | pyplot plt.imshow/plt.colorbar in an OO-API Skill (text) |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md ; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/py.sh scripts/<script>.py <args>` (Windows runtime; Arial present); PDFs via scripts\pdffonts.sh / render_pdf.sh in WSL dv-cli
- Deferred/blocked surfaces: none; usage-guide tips static-only
- Restricted-access items: none
- Tooling impact: none (no new input or package needed)

## Worktree safety

- Run-owned changes: run root above; published record dir in records repo; this handoff; audits\ index regeneration (orchestrator commits)
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: uncommitted paths (audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@146857c3b9b5-initial-dv1-20261003, audits index views, this handoff)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

# Handoff: bio-data-visualization-matplotlib-fundamentals / prepare-scientific-skill-tooling

- Updated: 2026-10-03T11:45:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals (read-only checkout F:\OpenScience\bioSkills-Improved\data-visualization\matplotlib-fundamentals\; source sha256-manifest c2230271d5a95bc2bfa7e926db44aa930b800229ac8c61cd0040ca19a40239e9 (3 files, 20133 B))
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone, 3 Skills)
- Candidate tree hash: sha256-manifest-v1 146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78 (files=5, bytes=21575)
- Applicable audit: none usable (bytes changed). Diagnostic history only: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\mrsonord2240-bioSkills@64b3b15\ (Beta Only, open P1/P2; not fixed here)

## Completed this phase

- Frontmatter: added `category: Data Analysis`; name already equals directory; `author: GPTomics`, `license: MIT` kept.
- SKILL.md trimmed to the core workflow; chart-type/axis recipes and failure modes moved to references/; example moved to scripts/ (name kept: matplotlib_phd.py).
- Version drift cleared against staged runtimes (Dependency clues); fabricated or obsolete claims fixed, listed in the table below.
- Hygiene: UTF-8, LF, no BOM, no pycache/dot paths/nested LICENSE. Preflight PASS.

## Structural summary

SKILL.md (defaults, rcParams, Figure/Axes API, seaborn, palettes, saving, guardrails); references/chart-recipes.md; references/failure-modes.md; scripts/matplotlib_phd.py; usage-guide.md.

## Runnable surfaces

- Python example: scripts/matplotlib_phd.py (rcParams, 89 mm scatter, 2x3 grid, Crameri heatmap, seaborn scatter, seaborn.objects; writes 5 PDFs to cwd). Ran end-to-end on matplotlib 3.11.2 / seaborn 0.13.2 / numpy 2.5.3 / pandas 3.0.6: clean.
- Inline Python recipes (boxplot, imshow, savefig formats, ticker/dates); `pdffonts` (poppler, external) named for font verification.

## Dependency clues

Python 3.12; matplotlib 3.11.2, seaborn 0.13.2, numpy 2.5.3, pandas 3.0.6, cmcrameri 1.10 (py.sh); pdffonts not staged on Windows (WSL may have it).

## Required next actions

1. Tooling worker: reuse the data-visualization staging env; map each surface above to a coverage entry; refresh TOOLS.md only if needed.
2. Audit worker: start fresh (prior audit is on different bytes); weigh the open items below.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-N1 | info | resolved | references/chart-recipes.md | Version fixes: `boxplot(labels=)` -> `tick_labels=` (TypeError on 3.11, verified); `constrained_layout=True` -> `layout='constrained'`; `set_constrained_layout` -> `set_layout_engine`; removed false "constrained_layout is default in 3.6+" claim |
| MPL-N2 | P2 | open | SKILL.md Standard Setup | Arial/Helvetica absent in staging env (DejaVu fallback); audit should confirm font-embedding claim by PDF inspection |

## Preflight

- `python tools/skill_preflight.py <dir>` from F:\optimizing-agent-science-skills: PASS, identity above. Warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter declares MIT).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS.md (read-only; R 4.4.3 via r.sh, Python 3.12 via py.sh)
- Run evidence: normalization-time smoke only (scratch, not retained); scripts ran clean on the installed versions listed below
- Restricted-access items: none
- Tooling impact: none (staging env already covers every surface)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals\ (new, untracked in the sparse worktree, no commit); branch normalize/dv-lane1 from 29f5446, shared with the other two data-visualization lane-1 Skills
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: this handoff uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

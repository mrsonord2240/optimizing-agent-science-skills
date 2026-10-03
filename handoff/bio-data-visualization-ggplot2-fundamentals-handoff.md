# Handoff: bio-data-visualization-ggplot2-fundamentals / prepare-scientific-skill-tooling

- Updated: 2026-10-03T11:45:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals (read-only checkout F:\OpenScience\bioSkills-Improved\data-visualization\ggplot2-fundamentals\; source sha256-manifest 304161080342a7838728a8d936f9745b3c8efd3b6d9d60e4ba500d2004513448 (3 files, 18928 B))
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone, 3 Skills)
- Candidate tree hash: sha256-manifest-v1 34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a (files=5, bytes=20148)
- Applicable audit: none usable (bytes changed). Diagnostic history only: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\mrsonord2240-bioSkills@64b3b15\ (Beta Only, open P1/P2; not fixed here)

## Completed this phase

- Frontmatter: added `category: Data Analysis`; name already equals directory; `author: GPTomics`, `license: MIT` kept.
- SKILL.md trimmed to the core workflow; geoms/aesthetics/scales/facets and failure modes moved to references/; example moved to scripts/.
- Version drift cleared against staged runtimes (Dependency clues); fabricated or obsolete claims fixed, listed in the table below.
- Hygiene: UTF-8, LF, no BOM, no pycache/dot paths/nested LICENSE. Preflight PASS.

## Structural summary

SKILL.md (defaults, layers, theme, tidy eval, ggtext, saving, guardrails); references/geoms-scales-facets.md; references/failure-modes.md; scripts/publication_figures.R; usage-guide.md (unchanged).

## Runnable surfaces

- R function library: scripts/publication_figures.R (theme_publication, create_volcano, create_boxplot, create_pca_plot, save_publication_figure, create_multi_panel). Sourced and run on synthetic data under ggplot2 4.0.3: clean.
- Inline R snippets in SKILL.md and references (ggsave cairo_pdf, ggrastr::rasterise, ggtext, tidy-eval wrappers); no CLIs.

## Dependency clues

R 4.4.3; ggplot2 4.0.3 (r.sh; 3.5.2 via r-gg35.sh), scales 1.4.0, ggrepel 0.9.8, ggtext 0.2.0, viridis 0.6.5, scico 1.5.0, patchwork 1.3.2, ggrastr 1.0.2, dplyr, RColorBrewer; cairo_pdf device.

## Required next actions

1. Tooling worker: reuse the data-visualization staging env; map each surface above to a coverage entry; refresh TOOLS.md only if needed.
2. Audit worker: start fresh (prior audit is on different bytes); weigh the open items below.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-N1 | P2 | open | scripts/publication_figures.R | `save_publication_figure` uses default pdf() device, contradicting the Skill's own cairo_pdf rule; behavioral, left for audit/fix |
| GG-N2 | P2 | open | scripts/publication_figures.R | Example uses theme_bw + non-Okabe palette while SKILL baseline is theme_classic + Okabe-Ito; left as is |
| GG-N3 | info | resolved | references/geoms-scales-facets.md | Version fixes: removed `geom_point(rasterize=TRUE)` (ggplot2 ignores it, verified on 4.0.3; now ggrastr::rasterise); `scale_*(trans=)` -> `transform=`; compat line updated |

## Preflight

- `python tools/skill_preflight.py <dir>` from F:\optimizing-agent-science-skills: PASS, identity above. Warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter declares MIT).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS.md (read-only; R 4.4.3 via r.sh, Python 3.12 via py.sh)
- Run evidence: normalization-time smoke only (scratch, not retained); scripts ran clean on the installed versions listed below
- Restricted-access items: none
- Tooling impact: none (staging env already covers every surface)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals\ (new, untracked in the sparse worktree, no commit); branch normalize/dv-lane1 from 29f5446, shared with the other two data-visualization lane-1 Skills
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: this handoff uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

# Handoff: bio-data-visualization-ggplot2-fundamentals / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots; mode full)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a (files=5, bytes=20148); re-verified with skill_preflight --offline: PASS
- Applicable audit: none usable (bytes changed); prior audit under audits\skills\bio-data-visualization-ggplot2-fundamentals\ is diagnostic history only

## Completed this phase

- publication_figures.R: all six functions run on real airway results and prcomp(mtcars); figures opened.
- Inline snippets run: cairo_pdf embeds TrueType, default pdf() leaves unembedded Helvetica Type 1 (rule verified); ggrastr, ggtext, tidy eval, TIFF/PNG sizes checked.
- pdffonts staged in WSL dv-cli (poppler 26.07.0); only missing from Windows PATH.

## Coverage map (surface | coverage | status)

| publication_figures.R | covered | ready |
| inline ggplot2 snippets (cairo_pdf, ggrastr, ggtext, tidy eval, ggsave formats) | covered | ready |
| pdffonts | covered (WSL) | ready |

All surfaces core; none heavy-optional; none restricted.

## Required next actions

1. Audit worker: start fresh on the exact bytes above using TOOLS file below; weigh the observations below plus the normalizer's open items (see git history of this file's predecessor: GG/MPL/VOL-N* ids carried in the audit ledger).
2. Any new input or package need: report for a tooling-delta pass; do not fetch in the run directory.

## Observations from tooling smoke (not findings; for audit)

- GG-N1 confirmed by evidence (default pdf device, Helvetica not embedded). Also: volcano labels overlap at max.overlaps=20; multi-panel `& theme_publication()` renders without the border seen in the standalone theme (look). Evidence: smoke\lane1_gg\

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none from tooling | n/a | n/a | n/a | n/a |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md
- Shared inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS.md ; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (snapshots\lane1_versions.txt)
- Run evidence: F:\OpenScience\audit-envs\data-visualization\smoke\lane1_*\ ; scripts in F:\OpenScience\audit-envs\data-visualization\tools\smoke_lane1_* , lane1_pdffonts*.sh , make_airway_dds.R
- Staging additions: public-data\derived\airway_dds_condition.rds (README row added); py-extra\sanbomics (isolated); INDEX.md row note
- Restricted-access items: none
- Tooling impact: none (full pass complete; no Skill bytes changed)

## Worktree safety

- Run-owned changes: staging files above; this handoff (uncommitted); no Skill bytes touched
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: uncommitted paths (this handoff)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

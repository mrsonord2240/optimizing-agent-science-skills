# Handoff: bio-data-visualization-volcano-and-ma-plots / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots; mode full)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76 (files=7, bytes=33343); re-verified with skill_preflight --offline: PASS
- Applicable audit: none usable (bytes changed); prior audit under audits\skills\bio-data-visualization-volcano-and-ma-plots\ is diagnostic history only

## Completed this phase

- Built derived public input: fitted airway DESeq2 dds (public-data\derived\airway_dds_condition.rds); volcano_phd.R, volcano_plot.R run unmodified; EnhancedVolcano, ashr, plotMA, ggbreak, edgeR glmTreat run.
- ma_plot.py and adjustText run on the real shrunken table; sanbomics 0.1.0 tooled in isolated py-extra.
- Figures opened: volcano_plot, EnhancedVolcano, sanbomics volcano all render with labels.

## Coverage map (surface | coverage | status)

| volcano_phd.R | covered | ready |
| volcano_plot.R | covered | ready |
| ma_plot.py (+adjustText) | covered | ready |
| inline ashr / plotMA / EnhancedVolcano / ggbreak / edgeR glmTreat | covered | ready |
| sanbomics | covered (plots only) | ready |

All surfaces core; none heavy-optional; none restricted.

## Required next actions

1. Audit worker: start fresh on the exact bytes above using TOOLS file below; weigh the observations below plus the normalizer's open items (see git history of this file's predecessor: GG/MPL/VOL-N* ids carried in the audit ledger).
2. Any new input or package need: report for a tooling-delta pass; do not fetch in the run directory.

## Observations from tooling smoke (not findings; for audit)

- VOL-N1 confirmed visually (-log10 p axis, fdr hline). New: `sanbomics.tools.volcano` does not exist (is `sanbomics.plots.volcano`); `sanbomics.tools` import fails (pkg_resources). Max shrunken |LFC| 10.99 > unshrunken 9.51 (check). Evidence: smoke\lane1_vol\

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none from tooling | n/a | n/a | n/a | n/a |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-volcano-and-ma-plots.md
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

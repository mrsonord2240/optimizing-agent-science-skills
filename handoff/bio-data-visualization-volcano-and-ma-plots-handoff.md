# Handoff: bio-data-visualization-volcano-and-ma-plots / prepare-scientific-skill-tooling

- Updated: 2026-10-03T11:45:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: normalize-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: prepare-scientific-skill-tooling

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/volcano-and-ma-plots (read-only checkout F:\OpenScience\bioSkills-Improved\data-visualization\volcano-and-ma-plots\; source sha256-manifest 3a32713ea2a79ce8d82cfe9d43b176cfd1b1ba0be1158f5481008b2341f1505f (3 files, 31751 B))
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone, 3 Skills)
- Candidate tree hash: sha256-manifest-v1 b94e14b191a0a1f2c6138fe10108d39b44b52efd299c47ae5a850e4e425ccb76 (files=7, bytes=33343)
- Applicable audit: none usable (bytes changed). Diagnostic history only: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-volcano-and-ma-plots\mrsonord2240-bioSkills@019953e\ (Beta Only, open P1/P2; not fixed here)

## Completed this phase

- Frontmatter: added `category: Data Analysis`; name already equals directory; `author: GPTomics`, `license: MIT` kept.
- SKILL.md cut to the core workflow; failure modes/error table and reconciliation/thresholds/reviewer pushback moved to references/; ggplot2 volcano function and Python MA function moved to scripts/; dead `[[api_gotchas]]` link removed.
- Version drift cleared against staged runtimes (Dependency clues); fabricated or obsolete claims fixed, listed in the table below.
- Hygiene: UTF-8, LF, no BOM, no pycache/dot paths/nested LICENSE. Preflight PASS.

## Structural summary

SKILL.md (shrinkage insight + method table, scenario tree, volcano design choices, EnhancedVolcano gotchas, MA diagnostics, resources); references/failure-modes.md; references/reconciliation-thresholds-pushback.md; scripts/volcano_plot.R, volcano_phd.R, ma_plot.py; usage-guide.md.

## Runnable surfaces

- R: scripts/volcano_plot.R (volcano_plot function); scripts/volcano_phd.R (end-to-end lfcShrink apeglm -> ggplot volcano -> MA -> cairo_pdf -> EnhancedVolcano; needs a fitted `dds` with coef condition_treated_vs_control). Both ran clean on airway (condition relabelled) with DESeq2 1.46.0 / ggplot2 4.0.3.
- Python: scripts/ma_plot.py (ma_plot), ran on a synthetic table under matplotlib 3.11.2.
- Inline R: lfcShrink apeglm/ashr, EnhancedVolcano call, DESeq2::plotMA.

## Dependency clues

R 4.4.3 / Bioc 3.20: DESeq2 1.46.0, EnhancedVolcano 1.24.0, apeglm 1.28.0, ashr 2.2.63, airway 1.26.0, ggplot2 4.0.3, ggrepel 0.9.8, dplyr, tibble. Python: matplotlib 3.11.2, numpy 2.5.3, pandas 3.0.6, adjustText 1.4.0 (named, unused by ma_plot.py). Named but unstaged: ggbreak, sanbomics.

## Required next actions

1. Tooling worker: reuse the data-visualization staging env; map each surface above to a coverage entry; refresh TOOLS.md only if needed.
2. Audit worker: start fresh (prior audit is on different bytes); weigh the open items below.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| VOL-N1 | P1 | open | scripts/volcano_plot.R | Plots -log10(pvalue) but draws the threshold at -log10(fdr), contradicting the Skill's own raw-p gotcha (same in volcano_phd.R); behavioral, left for audit |
| VOL-N2 | P2 | open | SKILL.md | `sanbomics.tools.volcano`, `ggbreak`, edgeR `glmTreat` claim named but never exercised |
| VOL-N3 | info | resolved | SKILL.md Version Compatibility | Compat line re-checked on staged versions; EnhancedVolcano emits ggplot2 4.x size-for-lines deprecation warnings but renders; no API breakage found |

## Preflight

- `python tools/skill_preflight.py <dir>` from F:\optimizing-agent-science-skills: PASS, identity above. Warn: no Skill-root LICENSE (manifest must cite repository license evidence; frontmatter declares MIT).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS.md (read-only; R 4.4.3 via r.sh, Python 3.12 via py.sh)
- Run evidence: normalization-time smoke only (scratch, not retained); scripts ran clean on the installed versions listed below
- Restricted-access items: none
- Tooling impact: none (staging env already covers every surface)

## Worktree safety

- Run-owned changes: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-volcano-and-ma-plots\ (new, untracked in the sparse worktree, no commit); branch normalize/dv-lane1 from 29f5446, shared with the other two data-visualization lane-1 Skills
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: this handoff uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

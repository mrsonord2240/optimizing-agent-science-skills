# Handoff: bio-data-visualization-ggplot2-fundamentals / fix-scientific-skill

- Updated: 2026-10-03T14:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 34a174ab026364c4b2884a4465ee5bd6b13eb0d80609c9f0ce729ac0746f159a (files=5, bytes=20148); skill_preflight --offline PASS before and after execution
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@34a174ab0263-initial-dv1-20261003\report.json (Beta Only, final 74; static 76, exec 71.8; research veto PASS)
- Run root: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\initial-dv1-20261003\ (report.json, viewer.md, finding-ledger.md, scripts\, logs\, out\ figures)

## Completed this phase

- Ran all six publication_figures.R helpers on real airway results + mtcars on ggplot2 4.0.3 and 3.5.2; opened every figure.
- Ran SKILL.md, reference and usage-guide snippets; verified fonts with pdffonts (WSL dv-cli).
- Tested the tooling leads: cairo_pdf/default-pdf lead and threshold-line/label-overlap leads reproduce; the prior '\u2212 prints literally' finding did NOT reproduce (R parses the escape; U+2212 renders).
- No audit-local repair; no Skill bytes changed. Published record candidate@34a174ab0263-initial-dv1-20261003.

## Required next actions

1. Fix GG-001..GG-004 in scripts/publication_figures.R (runnable bytes), then GG-008 (same file).
2. Fix GG-005..GG-007 in SKILL.md, usage-guide.md, references/failure-modes.md (text only).
3. Re-run scripts\g1_example.R and g2_snippets.R from the run root on the fixed bytes; classify tooling impact (none expected).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-001 | P1 | open | logs\g1_example_gg4.log; out\ex4\volcano_raw.png | hline at -log10(FDR) on raw-p axis (232 grey |LFC|>1 points above it); fix hline + axis label (script) |
| GG-002 | P1 | open | logs\pdffonts_ex4.log | save_publication_figure: default pdf()+inches, unembedded Helvetica/Symbol; use cairo_pdf + mm (script) |
| GG-003 | P1 | open | out\ex4\multi4.png | helper theme_bw+border/NPG/Set1/Set2 vs SKILL theme_classic+Okabe-Ito; `& theme_publication()` drops border (script) |
| GG-004 | P1 | open | out\ex4\volcano_raw.png, multi4.png | labels overlap at max.overlaps=20 (script) |
| GG-005 | P2 | open | out\snip4\grammar_block.png | Grammar block: inert colour scale, 10^0.477 ticks, redundant title (text) |
| GG-006 | P2 | open | logs\g2_snippets_gg4.log | aes(color='red') is salmon not blue; ggrepel N>10 trigger wrong (text) |
| GG-007 | P2 | open | usage-guide.md | inert axis-line tip, 'panel.grid.off', redundant panel.grid, {{ }} with string (text) |
| GG-008 | P2 | open | logs\g1_example_gg4.log | unseeded jitter, undocumented var_explained, Set1 >9 groups (script) |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md ; fingerprint sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Rerun: `bash F:/OpenScience/audit-envs/data-visualization/r.sh scripts/g1_example.R <skilldir> <outdir>` (r-gg35.sh for 3.5.2)
- Deferred/blocked surfaces: none; failure-modes claims on facets/size/units checked statically only
- Restricted-access items: none
- Tooling impact: none (no new input or package needed)

## Worktree safety

- Run-owned changes: run root above; published record dir in records repo; this handoff; audits\ index regeneration (orchestrator commits)
- Pre-existing/user-owned changes: records untracked test/validate.bats; shelf untracked .vscode/ (untouched)
- Records state: uncommitted paths (audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@34a174ab0263-initial-dv1-20261003, audits index views, this handoff)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

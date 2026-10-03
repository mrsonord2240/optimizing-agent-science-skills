# Handoff: bio-data-visualization-ggplot2-fundamentals / prepare-scientific-skill-tooling (delta)

- Updated: 2026-10-03T16:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (lane 1a)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e (files=5, bytes=21846); skill_preflight PASS
- Applicable audit: audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@34a174ab0263-initial-dv1-20261003 (audited 34a174ab..., Beta Only 74)

## Completed this phase

- Fixed GG-001..GG-008; fix log and per-finding evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-dv1-20261003\fix-log.md
- Re-rendered and opened figures on real airway DESeq2 + mtcars, ggplot2 4.0.3 (gg4\) and 3.5.2 (gg35\); pdffonts: all fonts embedded, 183x120 mm and 89x70 mm page sizes correct.
- Changed files: scripts/publication_figures.R, SKILL.md, usage-guide.md, references/failure-modes.md.

## Required next actions

1. Tooling delta: re-validate scripts/publication_figures.R surface (RColorBrewer no longer needed; scale_okabe, create_volcano y=-log10(padj), cairo_pdf/mm save). Rerun `fix-dv1-20261003\fix_run.R` with r.sh / r-gg35.sh.
2. Independent re-audit of exact bytes.

## Open findings and blockers

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| GG-001..GG-004 | P1 | fixed | fix-log.md, gg4\volcano.png, pdffonts_gg4.log, gg4\multi4.png | re-audit to confirm |
| GG-005..GG-008 | P2 | fixed | fix-log.md, gg4\grammar_block.png, fix_gg4.log | re-audit to confirm |

Known limit: volcano with long Ensembl IDs in panels under ~90 mm needs top_n=3 or symbols (documented).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md (fingerprint 8923551f...)
- Run evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-dv1-20261003\
- Restricted-access items: none
- Tooling impact: changed (surface scripts/publication_figures.R: runnable bytes changed, RColorBrewer dependency removed, no new package)

## Worktree safety

- Run-owned changes: the four Skill files above; evidence dir; this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/ (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

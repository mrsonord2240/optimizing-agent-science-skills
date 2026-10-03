# Handoff: bio-data-visualization-ggplot2-fundamentals / reaudit-scientific-skill

- Updated: 2026-10-03T17:00:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (delta, lane 1a)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design)
- Candidate tree hash: sha256-manifest-v1 9d22bac5b1ee4b3c7a26211b5f6033f1658a8ac43fb2514e02026ee32b12c54e (files=5, bytes=21846); skill_preflight PASS (re-verified this phase)
- Applicable audit: audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@34a174ab0263-initial-dv1-20261003 (audited 34a174ab..., Beta Only 74); does not cover the fixed bytes

## Completed this phase

- Tooling delta done; TOOLS (sha256 cae2035e8e4cfff35eb86b390f183af705be7505c3106bbdfa61ea049628cb22): F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md
- Reran the fixer's check script on ggplot2 4.0.3 and 3.5.2: all PASS and identical (volcano -log10(padj) + hline, label selection, seeded jitter, both error messages, 183x120 mm save, grammar block, tidy eval).
- pdffonts via staged WSL invocation: ArialMT/SymbolMT/Arial-ItalicMT embedded; 518x340 pt and 252x198 pt pages, both versions.
- Environment unchanged; no package installed, removed or upgraded.

## Required next actions

1. Independent re-audit of exact bytes above (GG-001..GG-008 confirmation; fix log lists evidence). Use the saved delta commands in TOOLS ("Delta invocation") against smoke\lane1_gg_delta\.
2. Check, not yet investigated: volcano y-axis title minus sign renders in a different colour in gg4\volcano.png (looks normal in the 3.5.2 multi4.png). Visual only.

## Open findings and blockers

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| GG-001..GG-008 | P1/P2 | fixed, tooling re-verified | fix-dv1-20261003\fix-log.md; smoke\lane1_gg_delta\ | re-audit to confirm |

Known limit: volcano with long Ensembl IDs in panels under ~90 mm needs top_n=3 or symbols (documented).
Correction: earlier TOOLS said "497 Up / 541 Down"; actual Down 497 / NS 17,200 / Up 541.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md; fingerprint 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (UNCHANGED, snapshots\lane1_versions.txt)
- Run evidence: F:\OpenScience\audit-envs\data-visualization\smoke\lane1_gg_delta\{gg4,gg35}\ and pdffonts.log; fixer evidence F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\fix-dv1-20261003\
- Staging added: tools\smoke_lane1_gg_delta.R, tools\lane1_pdffonts_gg_delta.sh, smoke\lane1_gg_delta\
- Restricted-access items: none
- Tooling impact: none further (environment unchanged; coverage map refreshed)

## Worktree safety

- Run-owned changes: TOOLS file, the two staged tools scripts, smoke\lane1_gg_delta\, this handoff
- Pre-existing/user-owned changes: records test/validate.bats; shelf .vscode/ (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes
- If no: n/a

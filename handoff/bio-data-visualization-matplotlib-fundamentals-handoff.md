# Handoff: bio-data-visualization-matplotlib-fundamentals / reaudit-scientific-skill

- Updated: 2026-10-03 (tooling-delta worker, lane 1)
- Lane: 1 (1b)
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (delta)
- Next role: reaudit-scientific-skill (full mode; runnable bytes changed, no prior candidate-ready record)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a (files=5, bytes=24264); skill_preflight --offline PASS (re-verified this phase)
- Prior audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@5a5bd8a000b2-reaudit-dv1-20261003\ (not ready); applies to the old identity only

## Completed this phase

- Tooling delta pass; no Skill bytes touched. Staged re-runnable checks in tools\ (all PASS): `lane1_mpl_delta_phd.py` (new), `lane1_mpl_delta_recipes.py`, `lane1_mpl_delta_failure_modes.py`, `lane1_pdffonts_mpl_delta.sh`.
- Section 7 seaborn.objects (`extent=[0,0,0.78,1]`, moved `p._figure.legends[0]`) verified on seaborn 0.13.2 / matplotlib 3.11.2: all 5 PDFs exact page size (89x70, 180x110, 89x90 mm), legend bbox x 0.815-0.988 y 0.406-0.594 of the page and clear of the axes, text 6-7 pt, all fonts CID TrueType (no Type 3); rendered volcano_so opened.
- chart-recipes.md 11/11 fragments verbatim PASS incl. Tick frequency; failure-modes.md 22/22 PASS incl. rewritten tight_layout entry.
- Record: section 7 depends on seaborn's private `_figure`; verified on seaborn 0.13.2 only.

## Required next actions

1. Full re-audit of the candidate; run `scripts/matplotlib_phd.py` and the changed reference blocks (use the staged delta scripts as the baseline).
2. Legend reservation is a fixed 22 percent; longer legend titles or labels were not measured (candidate edge for the auditor).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-007..009 | P2 | fixed (pending re-audit) | smoke\lane1_mpl_delta\{phd,rec,fm}\ | confirm |

No tooling blockers.

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md (sha256 a4a13bf881d7db3a8a26cc45fe8aef405ca9d60316b9187db89bdc9eba35d83c)
- Environment fingerprint: UNCHANGED, sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721 (snapshots\lane1_versions.txt, not regenerated)
- Run evidence: F:\OpenScience\audit-envs\data-visualization\smoke\lane1_mpl_delta\; fix evidence F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\fix-dv1-20261003\
- Restricted-access items: none
- Tooling impact: none further (no env change)

## Worktree safety

- Run-owned changes: staging under F:\OpenScience\audit-envs\data-visualization (tools, smoke); TOOLS file; this handoff. Skill bytes untouched.
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

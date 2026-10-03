# Handoff: bio-data-visualization-ggplot2-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03 (reaudit-scientific-skill worker, lane 1, final mode, second loop)
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit worker (fresh auditor; did not normalize, tool, audit or fix this Skill)
- Next role: orchestrator (commit to make `ready`, then intake); optional text-only fixer for GG-011/GG-012 and a one-line fix for GG-010

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/ggplot2-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-ggplot2-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 be703ae7f69598daa981d477afa71a873d0616a2f2830936b575c014a1f3f120 (files=5, bytes=22972); skill_preflight --offline PASS at start and end of this phase
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-ggplot2-fundamentals\candidate@be703ae7f695-reaudit-dv2-20261003\ (supersedes the failed 9d22bac5b1ee re-audit)

## Readiness decision

candidate-ready for the exact identity above. Final 89 (Production Ready), static 87, execution average 90.6, Layer 1 36.6/40, Layer 2 54/60, assertions 21/22 (95.5 %), skill and research veto PASS, no open P0 or P1.

Verified (ggplot2 4.0.3 and 3.5.2, drawn-box measurement): all 16 claimed zero-overlap rows are 0 pairs; shipped multi-panel example with defaults clean; GG-004 closed, GG-009 closed, fraction var_explained warning works; GG-001/002/003/005/006/007/008 not regressed; 5 SKILL.md R blocks and 23 reference lines run verbatim.
Judgement: leaving the 120 mm composite and the 89x70 Ensembl case as documented limits is acceptable (the Skill states them and says to open the figure).

## Open findings (all P2, none blocks readiness)

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| GG-010 | P2 | open | logs\nalabel_gg4.log (scripts\rb_na_label.R) | create_volcano errors ('missing value where TRUE/FALSE needed') when a label among the smallest padj is NA; one-line code change (na.rm = TRUE) |
| GG-011 | P2 | open | logs\probe_gg4.log | text-only: envelope names width only; 183x90 composite has 1 pair, measured on airway only; say label-box counts exclude threshold lines |
| GG-012 | P2 | open | static (usage-guide.md install line, scripts\publication_figures.R lines 3-5) | text-only: add patchwork and dplyr to install.packages; drop unused axes='collect' remark |

Any edit changes the identity and needs delta mode (text-only) or a fresh re-audit (code).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-ggplot2-fundamentals.md (sha256 5d13e5750af0ab3b172603d035311317491057206d2c3e576c2fd4f73c73c55f)
- Environment fingerprint: UNCHANGED, sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Run evidence: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\reaudit-dv2-20261003\ (published copy under the records path above)
- Noise: ggrepel layout in 120x110 symbol composites varies run to run (9-11 pairs); not claimed by the Skill (ggrepel max.time = 5)
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\reaudit-dv2-20261003\; published record dir; this handoff. Skill bytes untouched (copies used for execution).
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; other workers' records and regenerated audit views
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (orchestrator commits the Skill bytes to make them `ready`)

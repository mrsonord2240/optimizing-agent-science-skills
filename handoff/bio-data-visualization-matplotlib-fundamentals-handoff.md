# Handoff: bio-data-visualization-matplotlib-fundamentals / orchestrator (candidate-ready)

- Updated: 2026-10-03 (reaudit-scientific-skill worker, lane 1, final mode, second loop)
- Lane: 1 (1b)
- Status: candidate-ready
- Owner leaving: reaudit worker (fresh auditor; did not normalize, tool, audit or fix this Skill)
- Next role: orchestrator (commit to make `ready`, then intake); optional text-only fixer for MPL-010

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (Skill dir untracked by design; no product commit)
- Candidate tree hash: sha256-manifest-v1 f1efaf7eef6c18085eabaa140a3696db8e35e5d14624396d1f7c22643d398e7a (files=5, bytes=24264); skill_preflight --offline PASS at start and end of this phase
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-data-visualization-matplotlib-fundamentals\candidate@f1efaf7eef6c-reaudit-dv2-20261003\ (supersedes the failed 5a5bd8a000b2 re-audit)

## Readiness decision

candidate-ready for the exact identity above. Final 90 (Production Ready), static 88, execution average 90.6, Layer 1 36.6/40, Layer 2 54/60, assertions 21/23 (91.3 %), skill and research veto PASS, no open P0 or P1.

Verified (matplotlib 3.11.2, seaborn 0.13.2): five PDFs exact page size, CID TrueType, 6-7 pt text, deterministic; MPL-007 legend inside the exact 89x70 mm page and clear of the axes for the shipped labels; MPL-008 Tick frequency and 11 of 11 recipe fragments verbatim; MPL-009 tight_layout entry and 22 of 22 failure-mode checks; all 5 SKILL.md blocks verbatim on the real airway table; MPL-001..006 not regressed.

## Open findings (P2, does not block readiness)

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MPL-010 | P2 | open | logs\m2_legend_stress.log, out\legend\D_long_title_long_labels.png | text-only: section 7 does not disclose the private `Plot.plot()._figure`, the seaborn-0.13.2-only check or the fixed 22 % reserve; a longer legend title ('Differential expression class' + longer labels: legend x 0.604-0.988 vs axes end 0.750) covers the data. A public route (`Plot.on(fig)` + move legend + `fig.subplots_adjust(right=0.76)`) measured clean |

Any edit changes the identity and needs delta mode (text-only).

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md (sha256 a4a13bf881d7db3a8a26cc45fe8aef405ca9d60316b9187db89bdc9eba35d83c)
- Environment fingerprint: UNCHANGED, sha256 8923551f7fdd6c7e0d23acaa651c76b899b97a6c94500f4e0fe61dd1fd81f721
- Run evidence: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\reaudit-dv2-20261003\ (published copy under the records path above)
- Observation: pandas 3.0.6 + seaborn 0.13.2 raise a Pandas4Warning inside `Plot.plot()` (seaborn internals, hidden by default filters); no effect on output
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-data-visualization-matplotlib-fundamentals\reaudit-dv2-20261003\; published record dir; this handoff. Skill bytes untouched.
- Pre-existing/user-owned: records test/validate.bats; shelf .vscode/; other workers' records and regenerated audit views
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (orchestrator commits the Skill bytes to make them `ready`)

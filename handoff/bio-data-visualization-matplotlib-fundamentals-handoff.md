# Handoff: bio-data-visualization-matplotlib-fundamentals / audit-scientific-skill

- Updated: 2026-10-03T12:30:00-07:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: prepare-scientific-skill-tooling worker (batch: ggplot2-fundamentals, matplotlib-fundamentals, volcano-and-ma-plots; mode full)
- Next role: audit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:data-visualization/matplotlib-fundamentals
- Working tree: F:\OpenScience\wt\normalize-dv-lane1\skills\bio-data-visualization-matplotlib-fundamentals
- Branch/worktree: normalize/dv-lane1 @ 29f5446 (sparse cone; Skill dirs untracked by design)
- Candidate tree hash: sha256-manifest-v1 146857c3b9b509e7fb41764055239b497b5793cf0b386f83542fdfd5c5302d78 (files=5, bytes=21575); re-verified with skill_preflight --offline: PASS
- Applicable audit: none usable (bytes changed); prior audit under audits\skills\bio-data-visualization-matplotlib-fundamentals\ is diagnostic history only

## Completed this phase

- matplotlib_phd.py runs (5 s); pdffonts shows CID TrueType, no Type 3 in all 5 PDFs.
- Inline recipes and savefig formats run; default pdf.fonttype=3 control shows Type 3 (claim verified).
- Gaps resolved: pdffonts exists in WSL dv-cli; Arial IS present on the Windows py.sh runtime (ArialMT embedded), so MPL-N2 is not an environment gap.

## Coverage map (surface | coverage | status)

| matplotlib_phd.py | covered | ready |
| inline recipes + savefig formats | covered | ready |
| pdffonts | covered (WSL) | ready |

All surfaces core; none heavy-optional; none restricted.

## Required next actions

1. Audit worker: start fresh on the exact bytes above using TOOLS file below; weigh the observations below plus the normalizer's open items (see git history of this file's predecessor: GG/MPL/VOL-N* ids carried in the audit ledger).
2. Any new input or package need: report for a tooling-delta pass; do not fetch in the run directory.

## Observations from tooling smoke (not findings; for audit)

- EPS save warns the PostScript backend ignores alpha (opaque render); recipes savefig('.eps') path worth a line. Evidence: smoke\lane1_mpl_recipes\

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| none from tooling | n/a | n/a | n/a | n/a |

## Environment and evidence

- Tool inventory: F:\OpenScience\audit-envs\data-visualization\TOOLS-bio-data-visualization-matplotlib-fundamentals.md
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

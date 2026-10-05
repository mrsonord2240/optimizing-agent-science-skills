# Handoff: bio-workflows-crispr-screen-pipeline / fix-scientific-skill

- Updated: 2026-10-04T18:10:00-04:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (initial audit, run-002)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline
- Branch/worktree: recut/crispr-screen-pipeline, base f162b3a; candidate bytes uncommitted
- Candidate tree hash: e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (skill_preflight --offline --shape PASS, re-verified after audit; bytes untouched, no audit-local repair)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\candidate@e242270b6fc0-run-002\ (report.json, viewer.md, source-identity.json, record.json, scripts/)

## Completed this phase

- Initial audit published locally. Static 78, execution avg 75.6 (7 inputs), final 77, diagnostic grade Reject because research-veto M4 FAILs (F-01). Assertions 25/32. Not a readiness decision.
- Routing check (clean rerun, routing/routing.json): PASS count, qc, bagel2, drugz, chronos, consensus, branches (3/3 each); FAIL cn-correction 1/3, rra 0/3, mle 0/3, jacks 0/3. First attempt had HTTP 402 errors on four routes (kept in routing-attempt1-402/); pass rate on borderline routes varies between attempts.
- All ten runnable routes executed on staged real data; shipped scripts ran unchanged (cn_correction.R on A375 under crispr-ccr).
- Traps tripped: qc.py and cn_correction.R on non-integer table, rra.py no control, consensus.py one method (all name the fix); qc.py without plasmid= is silent (F-09).
- Docker was up; no restart. Other containers left alone.

## Required next actions

1. Fix F-01 to F-03 (route text that does not run: chronos, jacks, count) and execute each repaired command as written.
2. Fix F-04 to F-07 (routing): reword the SKILL.md "Order on every screen" line and the cn-correction, rra, mle and jacks table rows; rerun `tools/routing_check.py` (needs all 11 cases; about 12 min, 0.2 USD).
3. F-08 to F-11 (P2). Edits change the candidate identity: tooling impact must be classified at the fix handoff (routing-cases.json is bound to current route names; not to bytes).

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| F-01 | P0 | open | report.json input 6; run-002/work/chronos_literal, scripts/chronos_literal_*.py | replace Chronos snippet with the tested construction |
| F-02 | P1 | open | input 6; panel.log (exit 2) | jacks path and map columns |
| F-03 | P1 | open | input 3; work/count_literal (0% mapped) | library column order id, sequence, gene |
| F-04 | P1 | open | routing/rra-r*.json | order line and rra row |
| F-05 | P1 | open | routing/cn-correction-r*.json | cn row and order line |
| F-06 | P1 | open | routing/mle-r*.json | mle row |
| F-07 | P1 | open | routing/jacks-r*.json | jacks vs chronos rows |
| F-08 | P2 | open | inputs 4; cn.log | state non-integer output and dropped guides; stale "not run" claims |
| F-09 | P2 | open | work/traps (T2) | warn when plasmid= absent |
| F-10 | P2 | deferred | input 5 | paired drugZ and real drug screen: tooling-delta |
| F-11 | P2 | open | preflight warn | LICENSE or license evidence |

Tooling note T-1.2 (mle comma-separated table fails) did not reproduce: mageck mle accepted a comma file (work/traps/T7). Drop it from route-text defects.

## Environment and evidence

- Tool inventory: F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (sha256 2315b89c95f4); environments unchanged (shared Windows venv; WSL science crispr-ccr for cn-correction).
- Run evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\audit-initial\run-002\ (work/, routing/, logs, scripts/). run-001 is superseded (its routing void).
- Restricted-access items: none
- Tooling impact: none from the audit (no tooling change); F-10 needs a tooling-delta for a real drug screen.

## Worktree safety

- Run-owned changes: run-002 evidence dir; audits\skills\bio-workflows-crispr-screen-pipeline\candidate@e242270b6fc0-run-002\; regenerated audits\INDEX.md and BACKLOG.md; this handoff
- Pre-existing/user-owned changes: records test/validate.bats untracked, untouched; recut worktree normalize changes untouched
- Records state: uncommitted paths above
- Product commits/pushes: none
- Indexer note: `npm run audits:index` crashes on audits\skills\<id>\tooling\ (no record.json). I parked tooling\ outside the repo for the index run and restored it; the tooling dir location needs a decision.

## Transition assertion

- Next-phase prerequisites met: yes

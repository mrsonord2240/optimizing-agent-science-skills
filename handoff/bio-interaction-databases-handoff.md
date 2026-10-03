# Handoff: bio-interaction-databases / reaudit-scientific-skill (final re-audit 2)

- Updated: 2026-10-03
- Lane: 1
- Status: candidate-ready
- Next role: orchestrator (commit to make `ready`, then intake)

## Certified candidate

- sha256-manifest-v1 `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024`, files=6, bytes=42142; unchanged before and after (`skill_preflight.py --offline` PASS, no pycache)
- Tree: `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design)
- Score 87 Production Ready: static 86, execution average 87.0, assertions 35/35, L1 34.7, L2 52.3, no veto, no open P0

## Evidence

- Published record: `audits\skills\bio-interaction-databases\candidate@16290147ab41-reaudit-run-2\` (report.json, viewer.md, source-identity.json, 3 scripts); views regenerated, `audits:check` clean
- Raw: `F:\OpenScience\audits\bio-interaction-databases\reaudit-run-2\` (evidence\, scripts\)
- Prior: `candidate@7430509d403c-reaudit-run` (85)

## Findings

- IDM-001..009: still fixed, probes rerun on new bytes with no regression
- IDM-010: verified-fixed (live TP53+MDM2 1 edge, density 1.0, no self-loops)
- IDM-011: verified-fixed (junk/HTML/short answers raise ValueError; empty answer warns; aggregate_networks does not call SIGNOR)
- Open, P2, optional: IDM-012 (dropped homodimers disclosed only as a parenthetical; name homodimers and point to `biogrid_lt_physical`), IDM-013 (example `interaction_query.py` signed_effect/mechanism are last-record-wins, so exports vary between runs)

## Not executed

Reactome, HuRI, HuMAP, ConsensusPathDB, DIP, PhosphoSitePlus, IntAct client, R clients: static-only, no client or recipe ships. No live service failed this run.

## Worktree state

Nothing staged, committed or pushed; `test\validate.bats` untouched. Modified generated views under `audits\` plus the new record directory are uncommitted; no record deleted.

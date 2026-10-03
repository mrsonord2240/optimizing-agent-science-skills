# Handoff: bio-ortholog-inference / reaudit-scientific-skill (final, run 2)

- Updated: 2026-10-03
- Lane: 2
- Status: candidate-ready (not committed)
- Next role: orchestrator (commit the exact bytes, then intake). P2 polish optional via fix-scientific-skill.

## Candidate

- Identity (preflight --offline PASS before and after): sha256-manifest-v1 6e3122b03b95f6b9666a03f538ff5e07657ad733c2f0b9a2c7f1de1749993bbb, files=7, bytes=35212
- Path: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference (untracked, uncommitted by design; no pycache)
- Changed since the prior run (per-file hash): SKILL.md, usage-guide.md, scripts/ortholog_clients.py, examples/compara_orthologs.py. Identical: LICENSE, cross_resource.py, kegg_orthology.py.

## Result

- Score 87, Production Ready. Static 86, execution average 87.8, Layer 1 35.4, Layer 2 52.4, assertions 25/25. No veto, no open P0. All gates pass.
- Published: F:\optimizing-agent-science-skills\audits\skills\bio-ortholog-inference\candidate@6e3122b03b95-reaudit-run-2\ (viewer.md, report.json)
- Raw evidence: F:\OpenScience\audits\bio-ortholog-inference\reaudit-run-2\ (scripts\evidence\)
- Views regenerated (audits:index, audits:check clean); STATUS shows 87 Production Ready, 0/0/2 findings.
- Prior: aa32b51586699da5... 84 Limited Release (report in candidate@aa32b5158669-reaudit-run).

## Findings

- OI-01..OI-08: verified fixed, no regression (whole-module rerun on new bytes).
- OI-09 verified fixed (species route 200, bare 404). OI-10 verified fixed (stub: three statuses, fixed columns; live example reports MDM2 request failed, BRCA1 no ortholog returned, PARTIAL BATCH). eggNOG note verified fixed.
- Open P2 OI-11: SKILL.md does not name the three batch statuses and its snippet filters on `type`, so failed symbols still vanish if copied.
- Open P2 OI-12: unknown symbol (NOTAGENE123) is `request failed` (HTTP 400 in `error`); accurate to the code, can read as an outage. Not a blocker.

## Not executed / blocked

- eggNOG API: eggnogdb.org/api 403, eggnog6.embl.de TLS failure (carried from prior run, not re-probed). PANTHER liveness only.
- Ensembl homology slow and intermittent (45 s read timeouts: MDM2 batch, cross_resource Compara leg, one TP53 call in the sweep); service-side, each reported by the Skill, not a defect.

## Worktree state

- Skill bytes untouched. Records repo: new published run directory plus regenerated audits/INDEX.md, BACKLOG.md, STATUS.md, STATUS.html (uncommitted). test/validate.bats untracked, not touched. Nothing staged, committed or pushed.

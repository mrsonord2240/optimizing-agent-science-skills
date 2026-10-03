# Handoff: bio-ortholog-inference / fix-scientific-skill

> RUN PAUSED 2026-10-03 by Sam after the initial audit. Nothing is in flight. Resume at fix-scientific-skill; candidate is untracked and uncommitted in the working tree below.

- Updated: 2026-10-03T00:00:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: initial-audit worker (Sonnet), lane 3, batch database-access
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/ortholog-inference
- Working tree: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference
- Branch/worktree: fix/dbaccess-ortholog-inference at 2f38178 (shelf main)
- Candidate tree hash: f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac (sha256-manifest-v1, 6 files, 27397 bytes; preflight PASS, bytes unchanged)
- Applicable audit: F:\optimizing-agent-science-skills\audits\skills\bio-ortholog-inference\candidate@f6d4ccc5903d-initial-audit-run\report.json (score 69, Beta Only, no veto; static 72, execution avg 67.3, assertions 9/14)

## Completed this phase

- Static review of the full tree; live execution of Compara, OrthoDB, OMA, KEGG, PANTHER, eggNOG, HomoloGene and all three examples.
- Confirmed or refuted the tooling leads (below) with raw-vs-client comparisons; no Skill bytes changed, no audit-local repair.
- Published the record (17 scripts/inputs), regenerated index, `audits:check` passes, no published record deleted.

## Required next actions

1. Fix OI-01 to OI-05 (P1) in order, then OI-06 to OI-08 (P2); rerun the saved probes in the run `scripts/` against the fixed bytes.
2. Live checks are flaky: Ensembl homology hangs/500s and OMA unfiltered `/orthologs/` 502s intermittently; use timeouts, retry later, prefer TP53 and `rel_type=1:1` for OMA.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| OI-01 | P1 | open | scripts/probe_orthodb_oma_output.txt | Parse `data[].genes[].gene_id.id` null-safely; return [] on null data; raise on non-200 |
| OI-02 | P1 | open | scripts/ensembl_liveness_curl.txt, example_compara_orthologs_attempt_failed_500.txt | Timeouts, 5xx/connection retry in one session; broaden batch_compara except |
| OI-03 | P1 | open | scripts/probe_raw_output.txt | Compara has no `confidence` key; fix docs, docstrings, usage-guide prompt |
| OI-04 | P1 | open | scripts/probe_orthodb_oma_output.txt | OrthoDB /search is full text (TP53 -> TIGAR first); verify group, fix example |
| OI-05 | P1 | open | scripts/example_cross_resource_output.txt | Per-resource try/except; use TP53 P04637 for OMA (BRCA1 P38398 returns []) |
| OI-06 | P2 | open | scripts/probe_raw_output.txt | OrthoDB `/tab` is 404; correct or remove |
| OI-07 | P2 | open | scripts/panther_raw.txt | PANTHER has no evidence codes in response; document real route or drop claim |
| OI-08 | P2 | open | preflight warn | Add Skill-root LICENSE; fix oma_orthologs docstring (species.taxon_id) |
| B1 | blocker | deferred | viewer.md | OMA service flaky, not a Skill defect except missing retry; rerun when stable |
| B2 | blocker | deferred | TOOLS.md | eggNOG API refuses scripts (TLS mismatch/403); Skill already labels it unverified |

Leads resolved: T1 confirmed (OI-01). T2 confirmed (OI-03, OI-02). OMA 502 confirmed intermittent upstream; the example crash is OI-05. eggNOG confirmed blocked, labelled correctly. PANTHER live and correct for matchortho, claims partly unsupported (OI-07). HomoloGene retired, documented correctly.

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-ortholog-inference\TOOLS.md (sha256 aff688a8...c21a)
- Environment fingerprint: database-access venv py3.12.13 | requests 2.34.2 pandas 3.0.5 | pip-freeze sha256 5fdd1350df2cf397 (F:\OpenScience\audit-envs\database-access\Scripts\python.exe, PYTHONDONTWRITEBYTECODE=1)
- Run evidence: F:\OpenScience\audits\bio-ortholog-inference\initial-audit-run\ (report.json, viewer.md, source-identity.json, scripts/)
- Restricted-access items: none (B1, B2 service-side)
- Tooling impact: none (no Skill bytes changed this phase; fixes may touch the client, so the fixer must classify)

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-ortholog-inference\initial-audit-run\; records at audits\skills\bio-ortholog-inference\ plus regenerated audits INDEX/BACKLOG/STATUS (uncommitted)
- Pre-existing/user-owned changes: test/validate.bats (untracked); other Skills' records and handoffs belong to the concurrent auditor
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

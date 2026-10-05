# Handoff: bio-workflows-crispr-screen-pipeline / orchestrator (commit, optionally N-01 delta)

- Updated: 2026-10-04
- Lane: 1
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (reaudit-002)
- Next role: optimize-scientific-skills orchestrator (commit); optional fix-scientific-skill then reaudit delta for N-01

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline, base f162b3a; bytes uncommitted)
- Candidate tree hash: 05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5 (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE)
- Applicable audit: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@05e557c86e77-reaudit-002\ (this identity). Superseded: candidate@6654a4f7d596-reaudit-001 (rejected)

## Completed this phase

- Manifest diff vs reaudit-001: only SKILL.md, references/citations.md, routes/qc.md, scripts/qc.py changed.
- Routing check, Haiku via cli, 11/11 PASS (7 at 3/3, rra/drugz/jacks/chronos at 2/3); cases file requests equal the audit copy.
- qc.py reruns on real HAP1, real A375, resampled tables; Gini equals mageck's own function; rra.py smoke on the QC-passing table.
- Scores: static 88, execution 88.3, final 88, L1 35.4, L2 52.9, assertions 27/29 (93.1%). No veto.
- Published and indexed; audits:check clean.

## Readiness decision

candidate-ready by the canonical gate. Recommended before commit: fix N-01 (below) as a localized qc.py change; that is delta-mode eligible (a script change of at most 20 lines plus one route line).

## Open findings

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| N-01 | P1 | open | reaudit-002\work\a375_default.log vs a375_pattern.log | qc.py must not print QC PASS when no replicate group exists: exit 1 "QC INCOMPLETE", and group Project Score names or have the route pass pattern= |
| F-16 | P2 | open | report.json recommendations | Pearson 0.8 is a MAGeCK-VISPR guideline: say so, drop "drop the outlier" where no outlier exists, source or drop "0.85 comfortable" |
| F-10 | P2 | deferred | no real drug-screen counts | drugz paired mode stays static-only |
| F-11 | P2 | deferred | preflight warn | cite repo license evidence in the manifest |
| F-15 residue | P2 | disclosed | TOOLS.md Delta-002 | cn-correction and rra routing cases use resampled QC-passing tables |
| routes/chronos.md NEGv1 header | P2 | known | TOOLS.md Delta-001 | `.Gene` vs `GENE` in the standard file |

## Environment and evidence

- Tool inventory: audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (fingerprints unchanged)
- Run evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-002\ (routing.log, routing\, work\)
- Reused from reaudit-001 (bytes and environment unchanged): count, bagel2, consensus, mle, drugz unpaired, jacks, chronos, cn_correction.R, rra on real HAP1
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: audits\skills\...\candidate@05e557c86e77-reaudit-002\, audits\INDEX.md, audits\BACKLOG.md, this handoff
- Pre-existing/user-owned: test\validate.bats (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

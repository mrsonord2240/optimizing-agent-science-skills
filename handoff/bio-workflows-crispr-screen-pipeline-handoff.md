# Handoff: bio-workflows-crispr-screen-pipeline / fix-scientific-skill

- Updated: 2026-10-04
- Lane: 1
- Status: phase-failed (final re-audit rejected the candidate)
- Owner leaving: reaudit-scientific-skill worker (full mode, reaudit-001)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline, base f162b3a; candidate bytes uncommitted, untouched by this phase)
- Candidate tree hash: 6654a4f7d596c13a76b5b68b0346c9f521335f10e4d4a38ae7b58e2f3067d6dc (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE)
- Applicable audit: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@6654a4f7d596-reaudit-001\ (published, indexed)

## Completed this phase

- Full re-audit: static 83, execution avg 87.0, final 85, Layer 1 35.3, Layer 2 51.7, assertions 25/28 (89.3%). Grade Reject: research veto methodological_ground FAIL (F-12).
- Routing (model cli:claude-haiku-4-5-20251001): 9 of 11 PASS 3/3; cn-correction FAIL 0/3, rra FAIL 0/3; diagnostic rerun cn-correction 0/3, rra 1/3.
- Executed as shipped: count, qc, rra, bagel2, consensus, mle, drugz (unpaired), jacks, chronos (snippet verbatim, standard NEGv1), cn_correction.R (WSL).
- Prior F-01, F-02, F-03, F-06, F-07, F-08, F-09 verified resolved.

## Required next actions

1. F-12 (P0): in scripts/qc.py compute Gini on ln(count+1) like `mageck count`; endpoint gate 0.2 (the cited MAGeCK-VISPR value; source or drop the 0.55 drug figure); say `plasmid=` is for the cloned library pool, not Day-0 cells. Rerun qc.py on the real HAP1 and A375 tables (expect Gini pass; HAP1 Pearson 0.789 still fails).
2. F-13 (P1): SKILL.md rule 1: ask only for commitments the request and data do not state; otherwise state them as assumptions and run the route command. Rerun routing for cn-correction and rra.
3. F-14, F-15 (P2): enforce or label the guides>25 and skew gates and verify the skew<2 figure; tooling worker to record or restore the changed cn-correction request. F-10, F-11 stay deferred.
4. After F-12, the simulated rra-qcpass and cn-correction-qcpass inputs can be replaced by the real tables.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| F-12 | P0 | open | reaudit-001\gini_mageck_def.log | fix qc.py statistic and gates |
| F-13 | P1 | open | reaudit-001\routing\, routing-rerun\ | relax confirmation rule |
| F-14 | P2 | open | report.json recommendations | enforce or label gates |
| F-15 | P2 | open | scripts\routing-cases.json vs initial copy | record or restore |
| F-10 | P2 | deferred | tooling TOOLS.md | real drug-screen counts |
| F-11 | P2 | deferred | preflight warn | LICENSE or manifest citation |

Failed or blocked surfaces: routing cn-correction and rra (F-13); qc.py gate (F-12); drugz paired mode static-only (F-10).

## Environment and evidence

- Tool inventory: audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (environments unchanged, none rebuilt)
- Run evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\reaudit-001\ (native.log, chronos.log, cn.log, inspect_outputs.log, gini_mageck_def.log, routing\, routing-rerun\, work\)
- Restricted-access items: none
- Tooling impact: none expected from F-12/F-13 beyond rerunning qc and the two routing cases

## Worktree safety

- Run-owned changes: reaudit-001 raw run root; published record candidate@6654a4f7d596-reaudit-001; regenerated audits\INDEX.md and BACKLOG.md; this handoff
- Pre-existing/user-owned changes: test\validate.bats (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (fix-scientific-skill on F-12, F-13)

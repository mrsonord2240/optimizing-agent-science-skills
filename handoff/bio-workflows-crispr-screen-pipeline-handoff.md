# Handoff: bio-workflows-crispr-screen-pipeline / reaudit-scientific-skill

- Updated: 2026-10-04
- Lane: 1
- Status: ready-for-phase (tooling-delta-002 complete)
- Owner leaving: prepare-scientific-skill-tooling worker (delta-002)
- Next role: reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline; bytes uncommitted, untouched by tooling)
- Candidate tree hash: 05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5 (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE)
- Applicable audit: none for these bytes. Rejected: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@6654a4f7d596-reaudit-001\
- Fix ledger: F:\OpenScience\fix-evidence\recut-crispr-pipeline\fix-002\ledger.md

## Completed this phase

- qc surface rerun on shipped qc.py; numbers recorded in TOOLS.md Delta-002 (evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\tooling-delta-002\).
  - real HAP1: Gini 0.057 T0 / 0.101, 0.091, 0.091; Pearson 0.789 -> FAIL
  - real A375 (default pattern): Gini 0.089 plasmid / 0.163, 0.174, 0.155; no replicate grouping -> PASS (N-01 open)
  - cn-correction-qcpass: Gini 0.012 / 0.027; Pearson 0.977 PASS. rra-qcpass: Gini 0.012 / 0.035; Pearson 0.985 PASS
- routing-cases.json: cn-correction request restored byte-for-byte to the audit's original (F-15). Nothing else changed.
- rra and cn-correction cases keep the QC-passing resampled inputs (orchestrator decision); TOOLS.md says the inputs are resampled from real guide ids and fold changes, with synthetic counts, and why real tables stop at QC.
- TOOLS.md qc row, header identity and stale Gini notes updated; old 0.288 explained as a raw-count Gini.

## Required next actions

1. Re-auditor runs `tools/routing_check.py` on routing-cases.json (not run by tooling). Last fix-002 routing: cn-correction 2/3, rra 3/3, with the old request text on cn-correction.
2. Judge N-01 (default qc.py pattern does not group A375 replicate names) and F-10/F-11 deferrals.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| N-01 | P2 | open | tooling-delta-002\qc_a375.log | re-audit decides |
| F-10, F-11 | P2 | deferred-with-rationale | fix-002 ledger | re-audit decides |
| routes/chronos.md NEGv1 header (`.Gene` vs `GENE`) | P2 | known, see TOOLS.md Delta-001 | TOOLS.md | re-audit decides |

## Environment and evidence

- Tool inventory: F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (env fingerprints inside; unchanged this pass)
- Ecosystem: F:\OpenScience\audit-envs\crispr-screen-analyst\
- Run evidence: tooling-delta-002\ (qc_hap1, qc_a375, qc_a375qp, qc_rraqp logs and tsv)
- Restricted-access items: none
- Tooling impact: none further (qc and routing cases refreshed; all other surfaces verified unchanged, not rerun)

## Worktree safety

- Run-owned changes: tooling\TOOLS.md, tooling\routing-cases.json, this handoff, tooling-delta-002\
- Pre-existing/user-owned: test\validate.bats (untouched)
- Records state: uncommitted
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

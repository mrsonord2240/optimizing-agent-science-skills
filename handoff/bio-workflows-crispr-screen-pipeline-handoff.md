# Handoff: bio-workflows-crispr-screen-pipeline / fix-scientific-skill

- Updated: 2026-10-04
- Lane: 1
- Status: fix-002 complete; ready for tooling-delta (changed)
- Owner leaving: fix-scientific-skill worker (fix-002)
- Next role: prepare-scientific-skill-tooling (delta), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline (branch recut/crispr-screen-pipeline; bytes uncommitted)
- Candidate identity: 05e557c86e778a8b2aded50be5391610b18ce2693750b54a662686571ec9acb5 (skill_preflight --offline --shape PASS, 19 files; warn: no Skill-root LICENSE). Previous: 6654a4f7d596.
- Rejected audit: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@6654a4f7d596-reaudit-001\

## Finding dispositions (ledger: F:\OpenScience\fix-evidence\recut-crispr-pipeline\fix-002\ledger.md)

| ID | Sev | State |
|---|---|---|
| F-12 | P0 | fixed: qc.py Gini on ln(count+1), endpoint gate 0.2, 0.55 dropped, plasmid= = cloned library pool |
| F-13 | P1 | fixed: SKILL.md rule 1 restates stated commitments as assumptions |
| F-14 | P2 | fixed by labelling: guides>25 and skew reported, not gated; "skew<2" removed |
| F-15 | P2 | tooling worker (below) |
| F-10, F-11 | P2 | deferred-with-rationale |
| N-01 | P2 | open: default pattern does not group A375 replicate names (see below) |

Changed files: SKILL.md, scripts/qc.py, routes/qc.md, references/citations.md.

## Execution record (fix-002\)

- qc.py real HAP1: Gini 0.057 (T0, <0.1), 0.101/0.091/0.091 (<0.2); Pearson 0.789 -> QC FAIL (expected).
- qc.py real A375: Gini 0.089 plasmid, 0.163/0.174/0.155; default pattern does not group names -> prints no-replicate notice and PASS; with pattern=`R\d(?=_P1D14$)` Pearson 0.780 -> FAIL.
- Routing (cli:claude-haiku-4-5-20251001, routing\): cn-correction 2/3 PASS (r2 inspected R packages), rra 3/3 PASS. Run on bytes with CRLF endings in four files; text identical to the final LF bytes.

## Tooling impact: changed (surface qc, routing)

Tooling worker must:
1. Rerun qc surface: expect numbers above, not the old Gini 0.288.
2. routing-cases.json: restore the cn-correction request to the version in the initial copy of the cases (F-15; the changed request is recorded in the reaudit report). Keep requests unedited otherwise.
3. Swap rra data to the real HAP1 table `derived\crispr-pipeline\qc\hap1.count.txt` (or rra\) and keep allow_before qc, bagel2: real HAP1 QC FAILS on Pearson 0.789, so an agent that obeys QC may stop; judge before swapping.
4. Do NOT swap cn-correction to the real A375 table without deciding N-01: default qc.py passes it ungrouped, grouped it fails Pearson 0.78. Either leave cn-correction-qcpass or fix the pattern default.
5. Update TOOLS.md qc row and the Gini note (plasmid Gini 0.288 is raw-count Gini, not the MAGeCK one).

## Worktree safety

- Run-owned: fix-002 run dir; the four files above; this handoff
- Pre-existing/user-owned: test\validate.bats (untouched)
- Product commits/pushes: none; records uncommitted

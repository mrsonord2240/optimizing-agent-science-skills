# Handoff: bio-workflows-crispr-screen-pipeline / fix-scientific-skill

- Updated: 2026-10-04
- Lane: 1
- Status: ready-for-phase
- Owner leaving: fix-scientific-skill worker (fix-001)
- Next role: prepare-scientific-skill-tooling (delta mode), then reaudit-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline
- Branch/worktree: recut/crispr-screen-pipeline, base f162b3a; candidate bytes uncommitted
- Starting identity: e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (verified)
- Candidate identity now: 4db139576e8d5f48cb118db1f2cacd2eef87ca596d63fd25ae5dc711aa94c9a7 (skill_preflight --offline --shape PASS, 19 files; only warn: no Skill-root LICENSE, see F-11)
- Audit of the starting bytes: audits\skills\bio-workflows-crispr-screen-pipeline\candidate@e242270b6fc0-run-002\

## Finding ledger

| ID | Sev | State | Change | Evidence (fix-001 = F:\OpenScience\fix-evidence\recut-crispr-pipeline\fix-001) |
|---|---|---|---|---|
| F-01 | P0 | fixed | routes/chronos.md snippet rebuilt (cell_line_name, days, pDNA_batch, pDNA rows, negative_control_sgrnas) | fix-001\chronos: snippet extracted from the route runs exit 0; 5 lines x 4,502 genes, 0 NaN, ribosomal mean -2.70 to -2.96, all-gene mean ~0 |
| F-02 | P1 | fixed | routes/jacks.md: path jacks/run_JACKS.py, replicatemap and guidemap columns | fix-001\jacks: exit 0; 4,502 genes x 5 lines, RPL/RPS mean -1.04 to -1.83 |
| F-03 | P1 | fixed | routes/count.md: library read by position id, sequence, gene | fix-001\count: 100% mapped, 4 samples, Gini 0.074 to 0.115 |
| F-04 | P1 | fixed (case defect remains) | rra row unchanged; the QC-first order is the Skill's own rule | rra: route-first passes once qc.md is allowed; the command is still not issued in 2/3 (routing, routing-b): the agent runs QC, which fails on HAP1 by construction, and stops to investigate. Tooling-delta |
| F-05 | P1 | fixed (case defect remains) | cn row now says copy-number artifacts before hit calling; route states non-integer output and dropped guides | cn: 0/3 in both reruns, route-first passes, no agent issued the command: QC fails on A375 and the sandbox has no CRISPRcleanR, so it explores until the 10-command cap. Tooling-delta |
| F-06 | P1 | fixed | mle row adds "or a design matrix" | mle 2/3 with allow_before; the miss opened jacks.md first |
| F-07 | P1 | fixed | jacks row (replicate map and guide-to-gene map) and chronos row (copy-number-aware scores) disambiguated | jacks 3/3 with allow_before; chronos not rerun (was 3/3) |
| F-08 | P2 | fixed | cn route states non-integer output and 30-read drop; "not run" claims removed from SKILL.md tested line and cn_correction.R header | grep for "not run", "UNEXECUTED": no survivors |
| F-09 | P2 | fixed | qc.py prints a WARNING when plasmid= is absent; qc.md says so | fix-001\qc run on HAP1 without plasmid= prints it; QC verdict unchanged (FAIL) |
| F-10 | P2 | deferred-with-rationale | paired drugZ and a real drug screen need a tooling-delta dataset | not needed for readiness |
| F-11 | P2 | deferred-with-rationale | frontmatter has license: MIT; repository evidence: recut worktree LICENSE (upstream MIT, verbatim) and PROVENANCE.json; shape rules forbid nested copies | not needed for readiness |

T-1.2 (mle comma table) did not reproduce: dropped. No new findings.

## Routing check

Run with a copy of the cases file that adds allow_before (fix-001\cases-allow.json); the audited routing-cases.json is untouched. Results: fix-001\routing (rra, cn-correction, mle, jacks), fix-001\routing-b (rra, cn-correction rerun). Rerun lines: mle PASS 2/3, jacks PASS 3/3, rra FAIL 1/3 and 1/3, cn-correction FAIL 0/3 twice. Cost about 0.16 USD; no HTTP 402.

## Cases needing allow_before (tooling-delta; value as tested)

- routes/cn-correction.md: ["routes/qc.md"]
- routes/rra.md: ["routes/qc.md"]; the agents also read cn-correction.md (HAP1 is a cancer line) and bagel2.md (qc.md points to it), so add those if they open first
- routes/mle.md: ["routes/qc.md", "routes/cn-correction.md"] (leukemia lines)
- routes/jacks.md: ["routes/qc.md", "routes/cn-correction.md"]

Not enough for rra and cn-correction: the cases should use data that pass the QC gates (HAP1 and the A375 table fail) and, for cn-correction, a sandbox where the command can be issued without CRISPRcleanR being present, or the stop-at-command rule must tolerate it. The Skill's order and the "confirm four commitments" rule were not weakened.

## Changed files

SKILL.md (four table rows, read-first sentence, tested line); routes/chronos.md, jacks.md, count.md, cn-correction.md, qc.md; scripts/qc.py (warning), scripts/cn_correction.R (header only).

## Tooling impact: changed

Surfaces: chronos (route snippet now the executed construction, needs NEGv1 or control guide list), jacks (script path), count, qc (script output), cn-correction (header comment only), routing cases (allow_before). Environments unchanged. The tooling-delta should rerun the chronos and jacks route text from a clean case directory and rework the rra and cn-correction cases.

## Worktree safety

- Run-owned: fix-001 evidence dir; the candidate edits above; this handoff
- Untouched: test/validate.bats (user-owned), routing-cases.json, source checkouts, other worktree changes
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (route to prepare-scientific-skill-tooling delta)

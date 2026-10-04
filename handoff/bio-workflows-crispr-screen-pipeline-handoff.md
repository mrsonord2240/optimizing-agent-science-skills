# Handoff: bio-workflows-crispr-screen-pipeline / audit-scientific-skill

- Updated: 2026-10-04T17:30:00-04:00
- Lane: 1
- Status: ready-for-phase
- Owner leaving: tooling worker (router recut, mode full)
- Next role: audit-scientific-skill (routing check first: `tools/routing_check.py`, Docker)

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:workflows/crispr-screen-pipeline
- Working tree: F:\OpenScience\wt\recut-crispr-pipeline\skills\bio-workflows-crispr-screen-pipeline
- Branch/worktree: recut/crispr-screen-pipeline, sparse, from optimized-scientific-skills f162b3a
- Candidate tree hash: e242270b6fc053d495f12c86df5d2d8eb96f9b42fd3971d6435796c9bae5a71d (skill_preflight --shape PASS, re-verified after tooling; bytes untouched)
- Applicable audit: none for the recut

## Completed this phase

- TOOLS.md: F:\optimizing-agent-science-skills\audits\skills\bio-workflows-crispr-screen-pipeline\tooling\TOOLS.md (one row per route, env fingerprints, rerun steps).
- routing-cases.json beside it: 11 cases, one per route of the first table; inputs in F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\derived\crispr-pipeline\<route>\ (make_inputs.py there). Not yet run through routing_check (audit worker runs it).
- All 10 runnable routes executed at least once on real public data (count, qc, cn-correction, rra, bagel2, mle, drugz, jacks, chronos, consensus); branches is a reference route.
- New environment: WSL `science` env `crispr-ccr` (R 4.4.3, CRISPRcleanR 3.0.1). `scripts/cn_correction.R` ran unchanged on A375 (1m49s, 86,881 guides corrected). Replaces the Docker container route for this Skill.
- New staged input: Papalexi 2021 h5mu (589 MB) for the branches case; public-data README and ecosystem TOOLS.md updated.

## Required next actions

1. Audit: run routing check with the cases file, then the executable audit; use evidence under F:\OpenScience\fix-evidence\recut-crispr-pipeline\tooling\<route>\.
2. Route-text defects found while tooling (listed in TOOLS.md, "Route-text defects"): count.md library column order (mageck wants id, sequence, gene; literal text gives 0% mapped), mle.md needs tab-delimited counts, jacks.md (script path, Control column, guidemap headers), chronos.md (snippet cannot run: needs `cell_line_name` and negative_control_sgrnas or excess_variance), cn-correction.md (corrected table is non-integer; qc.py refuses it). Disposition belongs to audit/fix.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| T-1 | P1 | open | TOOLS.md defects 1-4; evidence dirs count/, mle/, jacks/, chronos/ | audit confirms, fix phase edits routes |
| T-2 | P2 | open | drugz case data is HAP1 with relabelled columns (no real drug screen staged) | none needed for routing; a real public drug screen would improve a drugz audit |

No blockers. No heavy-optional surfaces (genome-scale mle and full-panel Chronos are not run; Skill already says hours).

## Environment and evidence

- Tool inventory: TOOLS.md above; ecosystem F:\OpenScience\audit-envs\crispr-screen-analyst\TOOLS.md; crispr-ccr package list tools\ccr-wsl\env-list.txt (sha256 32be26b32cbbd53f).
- Run evidence: F:\OpenScience\fix-evidence\recut-crispr-pipeline\tooling\ (count, qc, cn, rra, bagel2, mle, drugz, jacks, chronos, consensus).
- Restricted-access items: none
- Tooling impact: n/a (first tooling pass for the recut)

## Worktree safety

- Run-owned changes: ecosystem dir additions (tools\ccr-wsl, public-data\derived\crispr-pipeline, public-data\perturb-seq, README and TOOLS.md appendices), records files under audits\skills\bio-workflows-crispr-screen-pipeline\tooling\, this handoff, evidence dir above
- Pre-existing/user-owned changes: records test/validate.bats untracked, untouched; recut worktree changes from normalize phase untouched
- Records state: uncommitted paths above
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

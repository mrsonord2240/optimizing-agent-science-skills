# Handoff: bio-atac-seq-co-accessibility / fix-scientific-skill

- Updated: 2026-09-30T03:05:00-07:00
- Lane: 3
- Status: ready-for-phase
- Owner leaving: Claude initial-audit worker (audit-scientific-skill)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/co-accessibility
- Working tree: F:\OpenScience\wt\atac-co-accessibility\skills\bio-atac-seq-co-accessibility
- Branch/worktree: fix/atac-co-accessibility (starting commit 3186916406e9cc6b0e6dc24ffe47880951fc0f93)
- Candidate tree hash (sha256-manifest-v1): 3c8089b0496fa6375512ece4b85ce85c10c47f3cb4a9c8e48c7288a62b9162e3 (5 files; recomputed live before and after audit, CRLF->LF normalized)
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-co-accessibility\report.json (63/100 Beta Only, static 68, exec avg 60.3, assertions 14/24, vetoes PASS), identity as above; no minor repairs made

## Completed this phase

- Static review of all 5 files plus 7 executed inputs on real public data (PBMC 5k scATAC, PBMC 3k Multiome); rubric from skill-auditor.zip.
- Independently confirmed tooling observations: CLI failure (narrowed to pattern-format .mtx), enhancer factor codes, wrong "Cicero 1.20+", 25 min unmodified-function timeout (bounded). Determinism concern not confirmed (two unseeded runs identical).
- Ledger: F:\OpenScience\audits\bio-atac-seq-co-accessibility\findings.json; viewer.md; source-identity.json; execution-classifications.json; report.json validated against pinned schema checklist (P0-P2 only).

## Required next actions

1. Fix COACC-001 and COACC-002 first (P1, script): numeric dgCMatrix coercion and dimnames in CLI; as.character() on Peak1/Peak2, unordered-pair de-duplication, peak-name assertion. Re-run CLI on a pattern .mtx and the chr1 function run.
2. Fix COACC-003, 005, 009 in the script: derive genome_df from peak coordinates, de-duplicate pairs before counting/plotting/concordance, document TSS BED source and promoter-promoter labelling and peak-name contract.
3. Fix documentation COACC-004, 006, 007, 008, 010, 011, 013: GitHub cicero-release@monocle3 1.3.x, `window` not `genomic_distance_max`, score range -1..1, plotTracks with locus/axis, ArchR loops[[1]], cite or soften ranges, label prose-only routes.
4. COACC-012 (SCENIC+ static): pin release/Python range, cite or drop Docker claim; blocked until a Python <=3.11 env with conda-forge pybedtools exists. Keep as restricted after-action item.
5. Report tooling impact, then route to reaudit-scientific-skill.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| COACC-001 | P1 | open | runs/cli.log, runs/cli2.log | CLI coercion/validation |
| COACC-002 | P1 | open | runs/t2.log, evidence/output/ex_chr1_enhancer_gene_pairs.csv | as.character, dedupe, assertion |
| COACC-003 | P2 | open | evidence/logs/fn_full.log, fn_chr1.log | genome_df from peaks; bounded 25 min timeout |
| COACC-004 | P2 | open | TOOLS.md version-drift, runs/checks.log | correct cicero version |
| COACC-005 | P2 | open | runs/archr_sym.log | dedupe symmetric pairs |
| COACC-006 | P2 | open | runs/checks.log | window, not genomic_distance_max |
| COACC-007 | P2 | open | runs/checks.log | score range docs |
| COACC-008 | P2 | open | runs/viz.log | plotTracks locus and axis |
| COACC-009 | P2 | open | runs/checks.log | TSS BED, promoter pairs, peak-name contract |
| COACC-010 | P3 | open | evidence/logs/archr.log | ArchR loops[[1]] doc |
| COACC-011 | P3 | open | runs/checks.log | cite or soften claims |
| COACC-012 | P3 | blocked | runs/scenicplus_static.txt | SCENIC+ static-only, restricted |
| COACC-013 | P3 | open | TOOLS.md rows 8-10 | label prose-only routes, LinkPeaks runtime |

Deferred/blocked surfaces: SCENIC+/pycisTopic (blocked), unmodified function full-genome run (25 min bound; larger budget untested), CLI end to end on an integer .mtx (would exceed time budget), reference DB / HiChIP / ABC prose (static-only), LinkPeaks (tooling-phase run, log inspected, not re-run).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-co-accessibility\TOOLS.md (conda-list.json sha256 2fcd3fc2a5de3bd194b80bf864b2f7ce9762eafc45c35179df9713958db7d552; R-packages.csv 424d7bb36fa8154a18a1b62cad0bba39aae6ba816e2f9b89c8aef09bfe0d8651)
- Run evidence: F:\OpenScience\audits\bio-atac-seq-co-accessibility\runs\ (scripts, logs, build_report.py) and evidence\
- Activation: `wsl.exe -d science -- bash /mnt/openscience/audit-envs/bio-atac-seq-co-accessibility/tools/run.sh <script.R>`
- Restricted-access items: COACC-012 (SCENIC+ install)
- Tooling impact: none (env ready); SCENIC+ rebuild only if requested

## Worktree safety

- Run-owned changes: F:\OpenScience\audits\bio-atac-seq-co-accessibility\ (report.json, findings.json, viewer.md, source-identity.json, execution-classifications.json, candidate-manifest.tsv, runs\); F:\OpenScience\audit-envs\bio-atac-seq-co-accessibility\work\ (disposable); this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched); Skill tree shows staged AM entries from the normalize phase (bytes unchanged)
- Records state: uncommitted; not yet published (orchestrator publishes)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

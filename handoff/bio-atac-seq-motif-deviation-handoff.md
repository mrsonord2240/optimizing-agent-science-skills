# Handoff: bio-atac-seq-motif-deviation / fix-scientific-skill

- Updated: 2026-09-30
- Lane: 3
- Status: ready-for-phase
- Owner leaving: audit-scientific-skill worker (lane 3)
- Next role: fix-scientific-skill

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/motif-deviation
- Working tree: `F:\OpenScience\wt\atac-motif-deviation` (candidate at `skills\bio-atac-seq-motif-deviation`)
- Branch/worktree: fix/atac-motif-deviation, starting commit 3186916 (skill dir untracked)
- Candidate tree hash: `sha256-manifest-v1 d645db4df84650ecf90027b9013e38b0d9adce73fb985a605d769c730d68fefc` (6 files; re-verified live, unchanged)
- Applicable audit: `F:\OpenScience\audits\bio-atac-seq-motif-deviation\initial-audit-20260930\report.json` (same identity). Score 60, grade Reject by veto (skill veto stability+determinism, research veto code usability). Static 71, execution 52.8, assertions 13/24. Not published to records yet (orchestrator).

## Completed this phase

- Static read of all 6 files; executed 5 workflows (patched and shipped bulk, Signac 1.17.1/1.16.0, ArchR, DecoupleR 1.8/2.2) plus chromVAR hand-check, reseed determinism, ArchR NA diagnosis.
- report.json (schema checklist verified), viewer.md, findings.json, source-identity.json, scripts/, logs/ in the run dir.
- ArchR NA cause characterized (T3): zero-read motif peaks in sparse cells give zero background SD; dropping the 6 NA cells lets getMarkerFeatures run.

## Required next actions (findings ledger: `initial-audit-20260930\findings.json`)

1. MOTDEV-001 (P0): document/set `colData(se)$depth` (total library reads, not colSums) in script and Skill; rerun end to end on `outputs\counts.tsv`, `peaks.bed`, `depth.tsv`.
2. MOTDEV-003 (P0): `set.seed` before `getBackgroundPeaks`; document seed/stochasticity.
3. MOTDEV-002 (P1): Signac `RunChromVAR` gone in 1.17.x; pin <=1.16.0 or give a tested direct-chromVAR route; fix version floor.
4. MOTDEV-004 (P1): NA check and remedy before ArchR `getMarkerFeatures`.
5. MOTDEV-005/006/007 (P2): fix chromVAR formulas in SKILL.md, DecoupleR snippet, TF names in CSV/heatmap.
6. MOTDEV-008 to -012 (P3): wording, stale counts (879 not ~1900; ArchR cisbp 870 not ~5000; logFC range), uncited heuristics, ggplot2 note, Bioc 3.23 note.

## Open findings and blockers

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| MOTDEV-001 | P0 | open | logs/run_bulk_unmodified.err | fix and rerun |
| MOTDEV-003 | P0 | open | logs/determinism_bulk.log | fix and rerun |
| MOTDEV-002 | P1 | open | logs/smoke_signac_1.17.1.log | fix, rerun both Signac versions |
| MOTDEV-004 | P1 | open | logs/archr_na_diag.log | fix, rerun ArchR |
| MOTDEV-005 | P2 | open | logs/smoke_chromvar_handcheck.log | edit prose |
| MOTDEV-006 | P2 | open | logs/smoke_decoupler.log | test or drop |
| MOTDEV-007 | P2 | open | ../outputs/heat-1.png | add names |
| MOTDEV-008 to -012 | P3 | open | findings.json | fix or defer with reason |

Deferred/static-only: bulk time-course spline, custom PFM/plant genome, scBasset/SCENIC+; Bioc 3.23/R 4.6 stack not built.

## Environment and evidence

- Tool inventory: `F:\OpenScience\audits\bio-atac-seq-motif-deviation\TOOLS.md` (sha256 47287b4b...5ab6), env fingerprint `91dcd6702bfba8518d2ff53ff1fec2bf447b62d06a091c00124c7ee4e1118ecd`
- Run evidence: `F:\OpenScience\audits\bio-atac-seq-motif-deviation\initial-audit-20260930\{scripts,logs}`; env root `F:\OpenScience\audit-envs\bio-atac-seq-motif-deviation`; activation in TOOLS.md
- Restricted-access items: none
- Tooling impact: none (no environment change; Signac 1.16.0 side lib already present for rerun)

## Worktree safety

- Run-owned changes: `F:\OpenScience\audits\bio-atac-seq-motif-deviation\initial-audit-20260930\`, `F:\OpenScience\audit-disposable\mda-rubric\`, this handoff. Skill bytes untouched, no audit-local repair used.
- Pre-existing/user-owned changes: `F:\optimizing-agent-science-skills\tools\run_mercury_worker.py`, `tools\test_run_mercury_worker.py`
- Records state: uncommitted, unpublished
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes

# Handoff: bio-atac-seq-nucleosome-positioning / orchestrator (commit + intake)

- Updated: 2026-09-30
- Lane: 5
- Status: candidate-ready
- Owner leaving: final re-audit worker (independent; did not write, fix, tool or initially audit)
- Next role: orchestrator (commit exact bytes to the optimized shelf, publish the audit record, run intake); no fixer needed

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/nucleosome-positioning
- Working tree: F:\OpenScience\wt\atac-nucleosome-positioning\skills\bio-atac-seq-nucleosome-positioning
- Branch/worktree: fix/atac-nucleosome-positioning, start 3186916 (files untracked, no commits)
- Candidate identity (sha256-manifest-v1, 7 files, 34,598 bytes): 2192c9d1500c5d260545b2dda74a0ea0f8e6e4b15a39023519d5c2f5fc495c4b (verified live before and after; no __pycache__)
- Applicable audit: F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\reaudit-run (this identity). Superseded baseline: initial-audit-20260930 (ce9a8a06..., 57 Reject)

## Decision: candidate-ready

Final 85 (Production Ready). Static 85, execution average 85.0, Layer 1 33.8, Layer 2 51.2, assertions 22/24 (91.7%). No veto, no open P0. Rubric zip sha256 e54e9ff8...f0de.

## Completed this phase

- Independently reproduced all P0 fixes on real GM12878 chr1 data: estimate_nrl 178 vs 176 bp; nucleosome_analysis.R rc 0 with all outputs and 0 MAPQ<30 export records; vplot recount 121,246 vs 121,291. Evidence: reaudit-run\logs\py_reaudit.log, r_bed.log.
- NucleoATAC from a clean install following usage-guide.md: unpatched rc 0 with 0 nucpos calls; documented sed + cythonize gives 178 calls / 6 redundant. Evidence: logs\na_clean.log, na_check.log.
- Judged the documented one-line third-party edit an acceptable, honestly disclosed workaround (precise, idempotent, isolated env, root cause verified in source, upstream defect named, fallback and empty-output check present). Details in viewer.md.
- DANPOS3 doc filter recomputed: 4,103/4,542 planted, 0 false.
- Throwaway env np-reaudit-nucleoatac removed (verified).

## Open findings (all P2, none blocking)

| ID | Severity | State | Evidence | Disposition |
|---|---|---|---|---|
| NUCPOS-016 | P2 | open | logs\py_reaudit.log, rep2_probe.log | estimate_nrl reports 208 bp on GM12878 rep2 (1-bp mode 177); optional warning |
| NUCPOS-017 | P2 | open | viewer.md input 3 | R export class counts differ from summary counts (post-shift); document or align |
| NUCPOS-006 | P2 | accepted workaround | logs\na_clean.log | upstream defect remains; optionally file upstream issue |
| NUCPOS-015 | P2 | deferred | static | scPrinter untested, labelled |

## Failed, blocked or reused surfaces

- Failed: none. Assertion failures: rep2 NRL (NUCPOS-016), export vs summary counts (NUCPOS-017).
- Reused (identity-matched, not rerun): R default knownGene route (fix-run, ~13 min), `danpos dpos` and ATAC recipe, H2A.Z snippet.
- Not run: BiocManager install line (conda-equivalent versions used); scPrinter. Heatmap PDF viewed via the delta run's byte-identical file (no PDF rasteriser).

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\TOOLS.md, fingerprint sha256 72f7cc5bd216ef9d9e74f453b76508c0f5c3c27d3f77c9ad5d620a62044e5cc5
- Run root: F:\OpenScience\audits\bio-atac-seq-nucleosome-positioning\reaudit-run\ (report.json schema-checked, viewer.md, source-identity.json, scripts\, logs\, out\)
- Restricted-access items: none
- Tooling impact: none

## Worktree safety

- Run-owned changes: reaudit-run\ records, this handoff
- Pre-existing/user-owned changes: F:\optimizing-agent-science-skills\tools\run_mercury_worker.py, tools\test_run_mercury_worker.py (untouched)
- Records state: uncommitted, not published to the records repo (orchestrator to publish with tools/publish_audits.py --run-dir, then npm run audits:index / audits:check)
- Product commits/pushes: none

## Transition assertion

- Next-phase prerequisites met: yes (commit exact bytes, then reconcile inventory)

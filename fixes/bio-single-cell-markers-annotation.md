# bio-single-cell-markers-annotation fix pass — 2026-09-24

## Source

- Repository/worktree: `F:\OpenScience\worktrees\bio-single-cell-markers-annotation-fixpass`
- Branch: `agent/fix-bio-single-cell-markers-annotation`
- Base: `12be3fc12a733fbbb8479bc8aa6abc1248950803`
- Final source commit: `f704543b45168b0df1a09670e5f584e173c06d97`

## Resolved findings

- **P1 pseudobulk counts:** the Scanpy recipe now requires `adata.layers['counts']`, aggregates with `layer='counts'`, and checks that the result is integral before a bulk DE hand-off.
- **P2 recovery:** the Common Errors table and usage guide explain non-integer pseudobulk, DESeq2 rejection, and the stop/reacquire-raw-counts path.
- **P2 CD8/NK ambiguity:** the PBMC section now requires a CD3D/CD3E lineage gate and prohibits assigning NK from NKG7/GNLY alone.
- **P2 control-bin claim:** removed the unverified Seurat default claim; comparison examples set 25 bins and 50 controls explicitly.
- **P2 reporting:** added a concise report contract for method/version/thresholds, marker effect/fraction fields, lineage gates, and descriptive p-values.

## Exact-commit validation

- Source worktree was clean at `f704543`; `git diff --check HEAD^ HEAD` passed.
- The exact published pseudobulk block ran under Scanpy 1.12.4 on an object with log-normalized `.X` plus integer `counts`; grouped sums were `[[5, 1], [1, 6]]` and integral.
- The exact same block against an object with no `counts` layer raised the documented `ValueError` before aggregation.
- Documentation checks confirmed explicit `nbin=25`, no unsupported 24-bin default claim, the CD8/NK gate, reporting block, and pseudobulk Common Errors row.
- The generic skill-creator validator reports upstream legacy frontmatter keys (`tool_type`, `primary_tool`, `author`) as unsupported. They predate this focused repair and were intentionally unchanged.

## Re-audit result

- **94/100 — Production Ready**
- **Assertions: 20/20**
- **Open P0/P1/P2: 0/0/0**

## Artifacts

- Canonical JSON: `F:\OpenScience\audits\bio-single-cell-markers-annotation\eval_report_bio-single-cell-markers-annotation_result.json`
- Canonical viewer: `F:\OpenScience\audits\bio-single-cell-markers-annotation\eval_viewer_bio-single-cell-markers-annotation.md`
- Focused evidence: `F:\OpenScience\audits\bio-single-cell-markers-annotation\re-audit-20260924\run-focused\focused_validation.out`
- Preserved pre-fix report/viewer: `F:\OpenScience\audits\bio-single-cell-markers-annotation\re-audit-20260924\pre-fix\`

No P0, P1, or P2 findings remain.

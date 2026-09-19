# Fix log — bio-single-cell-data-io

2026-09-19. Fixer for `single-cell/data-io` (skill-id `bio-single-cell-data-io`, audited at
86/100, Limited Release, deployable, no open P0).

Worktree `F:\OpenScience\wt\sc-io`, branch `fix/sc-data-io`, commit `3159a9b`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `zellkonverter::readH5AD(reader='R', raw=TRUE)` silently fails to recover `.raw` from an h5ad the `.raw` group genuinely exists in | P1 | Tool table's zellkonverter row now flags the failure and points to `schard::h5ad2sce(use.raw=TRUE)`; added a "Recovering `.raw`" subsection with a runnable `length(altExpNames(sce)) > 0` check; updated the matching Common Errors row | ran | Reran both routes independently against the audit's real h5ad (`input3_rich.h5ad`, confirmed via h5py to genuinely hold `.raw`): zellkonverter `raw=TRUE` -> `altExpNames` empty; `schard::h5ad2sce(use.raw=TRUE)` -> 33538 x 1222 (full raw recovered). zellkonverter 1.16.0, schard 1.1.0, R 4.4.3. |
| usage-guide.md's "Move this Seurat object to h5ad" example prompt has no backing code anywhere in SKILL.md | P1 | Added a Seurat->h5ad code block (`as.SingleCellExperiment()` + `zellkonverter::writeH5AD()`) with an explicit `scale.data`-loss caveat and a save-separately workaround | ran | Built a real Seurat 5.5.0 PBMC object (counts/data/scale.data layers + PCA), converted, wrote h5ad, reloaded in Python: `layers ['logcounts', None]`, `obsm ['PCA']`, 1176 x 15246 cells x genes. `scale.data` confirmed absent at every stage (SCE assayNames and the reloaded AnnData). |
| schard's tool-table row didn't note it drops the `counts` layer | P2 (cheap) | Added a one-line note to schard's row | ran | Confirmed as part of the same input3 rerun above: `schard::h5ad2sce()` default assayNames == `X` only. |
| anndataR listed as "first choice" without its R>=4.5 requirement | P2 (cheap) | Added an R>=4.5 caveat to anndataR's row | docs | Matches `TOOLS.md`'s own record that anndataR is blocked on R 4.4.3 in this environment; not independently re-verified since the fix is a one-line documentation caveat, not a code path. |
| Mandatory redundancy pass | — | Moved usage-guide.md's Prerequisites install commands into a new SKILL.md "Installation" section. Deleted usage-guide.md's "What the Agent Will Do" and "Tips" sections — both fully restated from SKILL.md's Governing Principle / Common Errors / API Defaults sections — replaced with a one-line pointer. usage-guide.md now holds only Overview, Prerequisites (pointer), Quick Start, Example Prompts, Related Skills. | — | Nothing deleted was unique; every fact now lives once, in SKILL.md. |

## Left unfixed

None — both P1s and the cheap P2s from the audit report were addressed.

## Verification method

Both P1 fixes were re-run independently of the audit's own scripts, against the same real
data (audit's `input3_rich.h5ad`, read-only; real 10x PBMC 1k v3 `public-data\` for the
Seurat build), via the env's `tools\rs.sh` wrapper (R 4.4.3, private `R-lib`, zellkonverter
1.16.0, schard 1.1.0, Seurat 5.5.0) — no shared library or package version touched. The
Seurat->h5ad output was written to the session scratchpad (not the audit's `data\` dir) and
reloaded in Python (scanpy, shared venv) to confirm the h5ad is valid and to inspect exactly
what survived. All 6 R code blocks in the final SKILL.md were parsed together with `parse()`
to confirm syntax validity.

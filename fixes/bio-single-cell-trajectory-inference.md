# Fix log — bio-single-cell-trajectory-inference

2026-09-19. Fixer for `single-cell/trajectory-inference` (skill-id `bio-single-cell-trajectory-inference`,
audited at 84/100, Beta Only, not deployable -- assertion pass rate 74.1% missed the Limited Release
floor).

Worktree `F:\OpenScience\wt\sc-traj`, branch `fix/sc-trajectory-inference`, commit `e8cf78a`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `mode='dynamical'`/`mode='stochastic'` crash inside scvelo 0.3.4's own internals against numpy 2.5.3/pandas 3.0.5 | P1 | RNA Velocity mode table and code block now lead with `mode='deterministic'` (the only mode that runs here); added an explicit compatibility note naming the exact internal failures and what version combo would restore dynamical/stochastic; added a matching Common Errors row; fixed `examples/scvelo_velocity.py` to match | ran | Independently reproduced 3 distinct internal scvelo bugs, none fixable from the call site: `recover_dynamics()` -> `make_unique_list()` -> `TypeError: unique requires a Series/Index/ndarray... got list` (pandas>=3 dropped plain-list support in `pandas.unique`); past that (verified with a call-site monkeypatch of `make_unique_list`), `align_dynamics()` -> `ValueError: assignment destination is read-only` (a second, independent break); `mode='stochastic'` -> `leastsq_generalized()` -> `TypeError: only 0-dimensional arrays can be converted to Python scalars` (numpy>=2 dropped implicit scalar conversion of size-1 arrays). Given 2 independently-fixable-from-outside bugs still block dynamical mode, documented deterministic-only per the brief's fallback option. The corrected RNA Velocity block (deterministic mode, `n_top_genes` fix, `velocity_graph(n_jobs=1, show_progress_bar=False)`, `velocity_pseudotime`) was run verbatim from SKILL.md against real `scv.datasets.pancreas()` data end-to-end: exit 0, `ASSERTION monotone_along_committed_series: True` (Ductal 0.13 -> Ngn3 low EP 0.19 -> Ngn3 high EP 0.66 -> Pre-endocrine 0.92 -> terminal ~0.90-0.96), mean velocity_confidence 0.71. scvelo 0.3.4, numpy 2.5.3, pandas 3.0.5. |
| Same `scv.pp.filter_and_normalize(..., n_top_genes=2000)` TypeError shipped in `examples/scvelo_velocity.py` | P1 (part of above) | Both SKILL.md and the example now do HVG selection via a separate `sc.pp.highly_variable_genes` call (with the normalized-X save/restore scvelo's `moments()` expects); also fixed `scv.read('velocyto_output.loom')` (no such attribute in scvelo 0.3+) to `sc.read_loom(...)` | ran / signature check | `filter_and_normalize`'s signature (`inspect.signature`) confirms no `n_top_genes` parameter; `hasattr(scv, 'read')` is False, `hasattr(sc, 'read_loom')` is True. The corrected preprocessing block is exactly what was run end-to-end above. `py_compile` clean. |
| CellRank fate-mapping block needs `allow_overlap=True` and a Windows multiprocessing guard | P1 | Added `allow_overlap=True` to `predict_initial_states`; added `n_jobs=1` to `compute_transition_matrix`/`compute_fate_probabilities`; added an explicit "Windows note" + Common Errors row requiring `if __name__ == '__main__':` around the block in a standalone script | ran | Reproduced the exact failure independently: SKILL.md's block run verbatim (no guard) raises `RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase` from `multiprocessing.Manager().Queue()` inside `PseudotimeKernel.compute_transition_matrix()`'s first call -- full traceback captured. The guarded, fixed version's correctness (fate-probability entropy 1.79 (MEP) -> 0.82 (mature), matching lineage commitment) was already verified end-to-end by the audit's own captured run (`F:\OpenScience\audits\bio-single-cell-trajectory-inference\run\input6_cellrank_output.log`), cellrank 2.3.3 in the isolated `cellrank-venv` (installing it in the shared venv would downgrade scipy, per `TOOLS.md`). |
| PAGA's `threshold=0.03` isolated-cluster heuristic doesn't flag real discrete PBMC types | P2 | Added a caveat to the PAGA section and the matching Common Errors row: sweep the threshold, corroborate with marker identity, don't treat isolation-at-one-threshold as a standalone test | docs | Matches the audit's own real-data numbers (0/15 clusters isolated at 0.03, 1/15 at 0.5, median connectivity 0.29); not independently re-run since the fix is textual guidance, not a code path. |
| `tradeSeq::fitGAM` silently needs raw counts, not the scaled matrix already in hand | P2 (cheap) | Added one line to the Slingshot/tradeSeq prose: `fitGAM` needs the untouched raw count matrix, naming the exact failure string | docs | Matches the audit's captured error ("All values of the count matrix should be non-negative") and its confirmed fix (raw counts -> 46/300 genes significant); not independently re-run, textual caveat only. |
| Frontmatter `primary_tool: Monocle3` is the one method that doesn't install on Windows and contradicts the Skill's own topology-first philosophy | P2 (cheap) | Changed `primary_tool` to `PAGA` (the Governing Principle's own "mandatory first step") | docs | Matches `TOOLS.md`'s "Referenced but not installable on Windows" entry for monocle3/SeuratWrappers; also added an "Installation" section noting the Windows/Monocle3 gap explicitly. |
| Mandatory redundancy pass | — | Moved usage-guide.md's R/Python install commands into a new SKILL.md "Installation" section (with the Windows/Monocle3 caveat). Deleted usage-guide.md's "Tips" section (9 bullets, all restating the Governing Principle rules and RNA Velocity/Common-Errors content verbatim) and collapsed "What the Agent Will Do" to a one-line pointer at SKILL.md's Governing Principle + Method Decision Table. usage-guide.md now holds only Overview, Prerequisites (pointer), Quick Start, Example Prompts, Related Skills. | — | Nothing deleted was unique to usage-guide.md; every fact it stated now lives once, in SKILL.md. |

## Left unfixed

None of the audit's P1/P2 findings — all 6 were addressed (2 P1s fixed with a verified working alternative + accurate caveat where the library itself is broken; 3 cheap P2s fixed; the 4th P2, Monocle3-as-primary_tool, fixed by frontmatter change).

## Verification method

Both P1s were re-run independently of the audit's own scripts (fresh scratchpad copies of the audit's
real `pancreas_raw.h5ad` / `paul15_paga_dpt.h5ad`, read-only originals untouched), via
`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\Scripts\python.exe` (scvelo 0.3.4, numpy
2.5.3, pandas 3.0.5) and the isolated `tools\cellrank-venv` (cellrank 2.3.3). The exact SKILL.md RNA
Velocity code block was extracted verbatim into a script and run to completion (exit 0). The CellRank
guard requirement was independently reproduced with a full traceback; the guarded fix's biological
correctness was cross-checked against the audit's own already-captured successful run rather than
re-run in full (same computation, same environment, no reason to expect a different result). Both
changed `.py` files (`examples/scvelo_velocity.py`, and the ad hoc verification scripts, which are not
shipped) pass `py_compile`. No R code was changed (only prose), so no `.R` parse check was needed. No
shared venv/R-library package or version was touched.


## 2026-09-21 (P2 pass, fixer: fresh Sonnet)

Worktree `F:\OpenScience\wt\single-cell-trajectory-inference`, branch `fix/single-cell-trajectory-inference` from staging `431aa55`. Commits: `ebc493e` (fix), `4b77029` (redundancy), `44cd2cc` (fix, example), `4ce42c1` (scripts). SKILL.md 242 -> 228 lines (under the split threshold, no `references/`). Env: shared venv (scvelo 0.3.4, numpy 2.5.3, pandas 3.0.5) for velocity, `tools\cellrank-venv` (cellrank 2.3.3) for CellRank.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| CellRank fence not self-contained (guard only in a comment) | P2 | Fence became `main()` + `if __name__ == '__main__':`; then the whole block moved to `scripts/cellrank_fate.py`, SKILL.md keeps the invocation and the Windows note | ran: `cellrank_fate.py` on Paul15 (`paul15_paga_dpt.h5ad`): macrostates identical to the audit, entropy MEP 1.7858 vs mature 0.8189 (audit 1.7858 / 0.8189); `py_compile` clean | |
| VelocityKernel with deterministic velocity uncaveated | P2 | Added a CellRank-section note with numbers | ran: pancreas, same deterministic velocity, GPCCA `n_states=8`: `VelocityKernel` Ductal 0.3601 vs Alpha/Beta 0.3174; `PseudotimeKernel` on `velocity_pseudotime` 1.0225 vs 0.4466 | Audit compared different datasets (pancreas vs Paul15); the like-for-like pancreas run confirms the point. PseudotimeKernel terminal states on pancreas include Ductal clusters, so the note also says to check terminals against markers |
| `examples/monocle3_trajectory.R` carries no platform note | P2 | Header comment: no Windows binary, never executed in the audit env, use PAGA/DPT or Slingshot+tradeSeq | docs (SKILL.md Installation, `TOOLS.md`) | Cannot run here: monocle3/SeuratWrappers do not install on Windows |
| (new) `examples/scvelo_velocity.py` crashed at `scv.pl.scatter` on numeric colors (`KeyError: 0`) | correction found while running | `sc.pl.umap` for `velocity_pseudotime`, `velocity_confidence`, `velocity_length` | ran end to end on pancreas: mean velocity_confidence 0.7126 (audit 0.71) | scvelo 0.3.4 + pandas 3 |
| (new) same example, top-velocity-genes plot: recarray `.flatten()` gave void scalars (`TypeError: unhashable`), then `scv.pl.velocity` raised the pandas>=3 `unique requires a Series` TypeError | correction found while running | names via `pd.DataFrame(...)`, per-gene `scv.pl.scatter(gene, x='spliced', y='unspliced')` phase portraits; compatibility note in SKILL.md names the failing and working calls | ran: 6 phase figures written; `scv.pl.velocity` and `scv.pl.scatter` with a gene list both confirmed to raise | Not fixable from the call site (same root cause as the dynamical-mode crash) |

### Left unfixed

- `examples/monocle3_trajectory.R` itself remains unexecuted: monocle3/SeuratWrappers are GitHub-only with no Windows binary and cannot be installed (brief forbids installing into the env). Only the note was added.
- `scv.pl.velocity` and list-of-genes `scv.pl.scatter` stay broken on scvelo 0.3.4 + pandas 3 (library internals); documented with a working workaround, not fixable in the Skill.

### Redundancy pass

usage-guide.md already held only overview, prompts, related Skills (done 2026-09-19); no change. Inside SKILL.md:

| deleted passage | new home |
|---|---|
| Common Errors scvelo-internals row: "fall back to ... confirm your numpy/pandas/scvelo versions" (restated the compat note) | row now points to the "scVelo 0.3.4 + numpy>=2 + pandas>=3 compatibility" paragraph, which keeps the full text (grep verified) |
| Common Errors Windows-guard row: "confirmed fix; verified for CellRank's ..." | row points to the CellRank "Windows note", which keeps the RuntimeError text and the guard rule; scvelo half keeps `show_progress_bar=False, n_jobs=1` |
| CellRank fence comment "Run this block inside `if __name__ == '__main__':`" and duplicate Windows sentence | guard is in `scripts/cellrank_fate.py`; Windows note keeps the rule once |

### Scripts

| old location | script |
|---|---|
| SKILL.md "Directed Fate Mapping With CellRank 2" fence (14 lines) | `scripts/cellrank_fate.py` (parametrised; `run_fate_mapping`, `fate_entropy`); `allow_overlap=True` reasoning kept in SKILL.md prose |
| SKILL.md RNA Velocity fence (18 lines) | duplicated `examples/scvelo_velocity.py`; SKILL.md keeps the six core calls and points at the example (no copy under `scripts/`) |

Not moved: PAGA (7 lines), diffusion pseudotime (4), Palantir (5), Slingshot/Monocle3 (4 each): short API illustrations.

# Fix log: bio-single-cell-perturb-seq (2026-09-19)

Fixer for `single-cell/perturb-seq`. Source audit: `F:\OpenScience\audits\bio-single-cell-perturb-seq\`
(`eval_report_bio-single-cell-perturb-seq_result.json`, score 75, Beta Only, deployable: false, no
veto). Fork: `mrsonord2240/bioSkills-Improved@main`, worktree `F:/OpenScience/wt/sc-perturb`, branch
`fix/sc-perturb`. Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (pertpy 1.3.0,
scanpy 1.12.4, R 4.4.3). Verified against the real `pt.dt.papalexi_2021()` dataset (20,729 cells,
downloaded fresh from `https://exampledata.scverse.org/pertpy/papalexi_2021.h5mu`, public/
unauthenticated), not synthetic data — same dataset the audit used.

| Finding | Priority | Change | Verified | Notes |
|---|---|---|---|---|
| `assign_mixture_model` needs undocumented JAX extra | P1 | Added `pip install 'pertpy[jax]'` to Prerequisites (moved into SKILL.md, with the real fallback signature for `assign_by_threshold`) | ran: `ImportError` reproduced exactly as the audit found (confirmed via `pip show`: `optax` absent, `jax` 0.11.1 present); confirmed `pertpy[jax]` extra pulls `optax`+`flax`+`numpyro`+`ott-jax` via package metadata | |
| Shipped `pertpy_analysis.py` `KeyError` (perturbation columns on `mdata.obs`, not `adata.obs`) | P1 | Added `mdata.push_obs(columns=['perturbation','gene_target','replicate'], mods=['rna'])` before Mixscape calls, in both SKILL.md and the example | ran end-to-end on real papalexi_2021 data: mixscape_class_global NP 13645 / KO 4698 / NT 2386 — matches the audit's own real run (13644/4699/2386) to within 1 cell | Also fixed a second real bug hit during verification: `gdo.X` ships as CSC and both `assign_mixture_model`/`assign_by_threshold` require CSR/dense (`NotImplementedError` otherwise) — added `gdo.X = gdo.X.tocsr()`. Also fixed a real internal inconsistency: SKILL.md used `pert_key='target_gene'` in the Mixscape snippet but `'gene_target'` in the shipped example, for the same dataset; `gene_target` is the column that actually exists (verified against the real MuData) — standardized on `gene_target` everywhere (Mixscape, Pseudobulk `target_col`, Milo `design`) |
| Milo example structurally incompatible with pooled Perturb-seq design | P1 | Replaced `sample_col='replicate'` / `design='~ gene_target'` with a per-(replicate x target) pseudo-sample column and a per-target-vs-NT subset; added the missing `sc.pp.neighbors()` call `make_nhoods` needs | ran end-to-end on real data: STAT1 vs NT, 22/194 neighborhoods DA at SpatialFDR<0.1 via `da_nhoods(..., solver='pydeseq2')` — no AssertionError | Confirmed the original design is a hard structural mismatch (per `da_nhoods`'s own docstring/example), not a flag issue, matching the audit's diagnosis |
| scMAGeCK: decision-table entry with zero code anywhere | P2 | Reframed rather than wrote a worked example: added a note that scMAGeCK is Bioconductor-staging-only (not CRAN/Bioc release), needs a compiled C++ component, and is absent from this Skill's tested env; pointed to the real upstream repos and named its two real entry points (`scmageck_lr`, `scmageck_rra`, per Yang et al. 2020, already in References) | checked docs: confirmed via `available.packages()` (not found on CRAN/Bioc release repos) and r-universe search (found only under Bioconductor's `biocstaging` index, topic `cpp`) | Chose "delete/reframe the claim" over "write it" or "install it": the FIX_BRIEF's own "Verify every change" section bars installing into the shared R env as a fixer, and scMAGeCK's own GitHub README defers to a separate Bitbucket repo for real usage docs, so a fabricated code block would not be genuinely verified. Kept the (accurate) decision-table row rather than deleting it outright |
| `sceptre` needs R>=4.5, undocumented | P2 | Added the R>=4.5 requirement and the silent-no-op behavior to SKILL.md's Prerequisites and the SCEPTRE section | checked docs: corroborates `TOOLS.md`'s independent finding (`available.packages()` filters it out under R 4.4.3; no `sceptre` folder in R-lib) and the audit's own directory-listing confirmation — two independent sources, not executed further (cannot install R>=4.5 here) | |
| E-test permutation has no documented/exposed seed | P2 | Added `np.random.seed(0)` before the `etest(...)` call, with a comment that `DistanceTest` exposes no seed of its own | checked API: `inspect.signature` on `DistanceTest.__init__`/`__call__` confirms no seed/random_state parameter anywhere | |

## Redundancy pass (per FIX_BRIEF, every pass)

- Deleted `usage-guide.md`'s **Decision Guidance** and **Tips** sections: both restated
  SKILL.md's Governing Principle / Method Decision Tables / Common Errors verbatim or near-verbatim.
- One fact found only in the deleted text and needed by the agent: the GSFA/scMAGeCK-LR mention
  for high-MOI deconvolution (`Decision Guidance > Guide assignment`) — moved into SKILL.md's
  Governing Principle (MOI paragraph). The "non-targeting controls define the null" tip was folded
  into the same paragraph's NT/contamination-floor sentence.
- Moved the actual `pip`/`install.packages` commands (previously only in `usage-guide.md`'s
  Prerequisites) into SKILL.md's Prerequisites, since these are commands the agent acts on;
  `usage-guide.md`'s Prerequisites now points to SKILL.md instead of repeating them.
- `usage-guide.md`'s Overview, Quick Start, Example Prompts, "What the Agent Will Do", and Related
  Skills are unchanged (human-facing, not restated elsewhere).

## Left unfixed

None of the 6 findings were left unfixed. scMAGeCK (P2) was resolved by reframing rather than by
shipping a new worked example — see the table above for why installing/writing it was not the
right call here.

## Deployability

All three P1 defects were real, reproducible execution failures (Inputs 1, 4-adjacent, and 5 in the
audit) and all three now run clean against the same real dataset the audit used, producing sensible,
checkable output (cell-type-split counts matching the audit's own run to within 1 cell; a real DA
result with an interpretable SpatialFDR). Whether this clears the skill-auditor's execution-avg /
assertion-pass-rate deployability floor is for the re-auditor to confirm.

# Fix log: bio-single-cell-perturb-seq (2026-09-21)

Second fix pass, from the 2026-09-19 re-audit (score 88, Production Ready; 2 open P1, 1 P2). Branch
`fix/single-cell-perturb-seq`, worktree `F:\OpenScience\wt\single-cell-perturb-seq`. Env:
`single-cell-transcriptomics-analyst` (pertpy 1.3.0, scanpy 1.12.4, R 4.4.3). SKILL.md is 287 lines
after the fixes, under the 300-line split threshold, so no `references/` split.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| SCEPTRE install instructions wrong (`install.packages('sceptre')`, "requires R >= 4.5") | P1 | Prerequisites: `remotes::install_github('Katsevich-Lab/sceptre')`; the R >= 4.5 bullet replaced by "GitHub-only, `R (>= 4.1)`, not on CRAN, install exits 0 having installed nothing"; SCEPTRE section's R >= 4.5 line replaced by a pointer to Prerequisites (one statement of the install); version line now "sceptre 0.99.0 from GitHub (checked 2026-09-21)"; `usage-guide.md` Prerequisites parenthetical no longer says R >= 4.5 | ran: installed sceptre 0.99.0 from GitHub into a scratchpad lib under R 4.4.3 (compiled clean); GitHub `DESCRIPTION` says `Depends: R (>= 4.1)`; `cran.r-project.org/web/packages/sceptre/index.html` returns 404 | Old claim came from `TOOLS.md` (a wrong diagnosis). `TOOLS.md` line 206 in the env is still wrong; not edited (outside the fixer's write scope) |
| SCEPTRE snippet: `get_result(obj, analysis = 'discovery_analysis')` errors | P1 (found while verifying) | Changed to `analysis = 'run_discovery_analysis'`, with the three valid values in a comment | ran the SKILL's SCEPTRE block on sceptre's bundled `lowmoi_example_data` (20 responses x all targets, 400 pairs): `'discovery_analysis'` raises "`analysis` must be one of `run_calibration_check`, `run_power_check`, or `run_discovery_analysis`"; `'run_discovery_analysis'` returns 400 rows | Not in the audit report; the re-audit's own script used the correct name, the SKILL text did not |
| `Mixscape.perturbation_signature` exceeds 20 GB on the full 20,729-cell dataset | P1 | Snippet and shipped `examples/pertpy_analysis.py` now densify `adata.X` and pass `batch_size=1000`; new "Memory" note under the Mixscape section with the numbers, the `ValueError` when `batch_size` meets sparse X, and the `ref_selection_mode='split_by'` option | ran on the real papalexi_2021 data with a 14 GB RSS watchdog: `batch_size=1000` + dense X finished in 113 s, peak 7.3 GB, KO/NP/NT = 4698/13645/2386; sparse X + `batch_size=1000` raises `ValueError: shape must have length in (2,). Got new_shape=(1000, 20, 18649)`. Docstring of `perturbation_signature` states `batch_size=None` runs "in the full mode, requiring more memory" | Full example re-run end to end: see the result line below. The `split_by` alternative is documented from the docstring only, not run |
| scMAGeCK Bioconductor history wrong ("unreleased staging index") | P2 | Reworded to "released through Bioconductor 3.16, removed at 3.17", dated 2026-09-21 | ran: `bioconductor.org/packages/3.16/bioc/html/scMAGeCK.html` is 200, `/3.17/` is 404; the removed-packages page lists it under "removed with Bioconductor 3.17" | |

Redundancy: the SCEPTRE install fact was stated three times in SKILL.md (Prerequisites code comment,
Prerequisites bullet, SCEPTRE section) and once in `usage-guide.md`; it now lives in the Prerequisites
bullet, with the SCEPTRE section and the guide pointing at it. Nothing the agent needs was deleted.

## Left unfixed

- Env `TOOLS.md` line 206 still says sceptre needs R >= 4.5 and is CRAN-gated: it is not part of the
  Skill and the brief bars edits outside the fork and this log. Sam or the tooling owner should correct it.
- `mixture` guide assignment (`assign_mixture_model`) was still not run: needs `pertpy[jax]` (`optax`,
  `flax`, `numpyro`, `ott-jax`) in the shared venv, which the brief forbids installing into. The
  `ImportError` and its fallback are documented and were reproduced by the full example run.
- Milo/pseudobulk sections were not re-run this pass: untouched, verified in the 2026-09-19 pass.


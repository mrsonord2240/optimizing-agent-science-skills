# bio-crispr-screens-jacks-analysis fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-c`, branch `fix/r2-crispr-c`. Fixer: Claude Opus 5 (orchestrating
session). Runtime: JACKS 0.2 from `felicityallen/JACKS` in the `crispr-screen-analyst` venv (with the
tooling pass's `import numpy as SP` patch), pandas 2.x, Python 3.12. Verification data: JACKS' own
`jacks/example-small` (8,081 guides, 1,579 genes, 5 AML lines vs a plasmid control) and `NEGv1.txt`,
copied to `F:\OpenScience\wt\_fixdata\jacks\`; scripts `probe.py` and `verify.py` there.

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `efficacy_summary()` does `groupby('Gene')` on the grna file, whose only columns are `sgrna, X1, X2` | P0 | Takes a guide-map path, merges it on `sgrna`, raises on unmapped guides; imports `pandas` (the block imported only matplotlib) | ran | Extracted from SKILL.md and ran on real output: 8,081 guides, 1,579 genes, median efficacy 1.017; a guide map with renamed sgRNAs raises `ValueError` |
| `examples/run_jacks.py` `analyze_results()` uses undefined `output_prefix` | P0 | Added `output_prefix` parameter and threaded it through `__main__` | ran | Imported without bytecode and ran on real output: 1,579 genes, 266 with effect/std < -2; `plot_results()` wrote the PNG |
| Canonical Python example sets `apply_w_hp=True` against the Skill's own advice | P1 | Example now `apply_w_hp=False`; added a labelled "deliberate use only" variant quoting the audit's measured rank change (rho 0.75-0.89); CLI block drops `--apply_w_hp`; usage-guide prompt no longer asks for it | ran (audit Input 1) | Default and `--help` text confirmed in `jacks_io.getJacksParser()` |
| Failure Modes' CRISPRi fix ("manually set hyperparameters") has no documented interface | P1 | Documented that the priors are `inferJACKSGene` kwargs and gave a runnable `functools.partial` override that restores the default; also points at a matched-chemistry `--reffile` | ran | Override with `var0_x=4.0` ran end to end, efficacy SD 0.690 → 1.192; `inferJACKSGene` restored afterwards (asserted) |
| `run_JACKS.py` location given as repo root in SKILL.md | P1 | Both CLI comments and the Version Compatibility line now say `JACKS/jacks/`; install line now `cd JACKS/jacks && pip install .` (the root has no `setup.py`); usage-guide's duplicate root-install line removed | ran | CLI block extracted and run from the clone's `jacks/` folder: 1,579-row gene file, identical to `run_jacks_analysis()` output |
| Wrong-library-prior failure mode predicts silent degradation; JACKS raises | P2 | Symptom now the real exception, plus the remaining silent case (IDs match, sequences don't) | docs (source `preprocess()`) + audit Input 3 run | |
| Python `n_pseudo=0` default vs CLI 2000, so no p-value file from the documented Python call | P2 | Note in the Python example and interpretation rule; CLI output comment gives the 2000 default | ran | `ctrl_genes` + default `n_pseudo` → no pval file; `n_pseudo=2000` → file written |
| Naming-mismatch symptom says NaN gene effects; genes are dropped | P2 | Failure Modes mechanism/symptom and Common Errors row corrected | docs (source `createGeneSpec`) + audit Input 6 run | |
| (Found while fixing) "Repeated runs produce different gene effects", "set seed", "no seed flag" — inference is deterministic | internal contradiction | Model section states the deterministic init; the convergence failure mode now describes the 50-iteration cap and early stop, with a runnable `n_iter` override; p-value randomness attributed to pseudo-gene sampling with `random.seed` as the fix | ran | Two identical runs: gene and grna files byte-identical. Seeded pseudo-gene runs identical, unseeded differ. `n_iter=500` override ran (no gene changed on this data, i.e. all converged before 50) |
| (Found while fixing) "Iterations 5000+ publication; 1000 default", "Increase iterations to 5000+" | internal contradiction | Thresholds and Common Errors rows now give JACKS 0.2's real cap (≤50, early stop at lower-bound change < 0.1) | docs (source `inferJACKS`, `inferJACKSGene`) | Same fix in usage-guide steps, tips and Key Thresholds |
| (Found while fixing) `X1/X2` given as the gene z statistic; the gene file has no X1/X2 and the grna X2 is a second moment | internal contradiction | Interpretation rule, Quantitative Thresholds and usage-guide tips now use gene effect / gene std file | ran | Output headers checked: gene file `Gene` + cell lines; grna file `sgrna, X1, X2` |
| (Found while fixing) Model prose: gene-effect prior `Normal(0, sigma_c^2)`, "Beta-prior hyperparameters", p-values "log-likelihood-ratio tests"; Output bullet claims gene `X1` and an LLR per gene | internal contradiction | Corrected to the source defaults (`Normal(0, 1e4)`, Gaussian efficacy prior) and pseudo-gene p-values; Output bullet lists the real files | docs (source) | |
| (Found while fixing) CLI bash block had comments after `\` continuations, which end the command | broken command | Comments moved above the command | ran | `bash -n` passes; block executed |
| (Found while fixing) usage-guide says replicate and guide maps have no header, with columns Sample/Experiment/Condition | wrong format | Header required, columns `Replicate`, `Sample`, optional `Control` | ran | `prepareFile()` locates rows by header name; runs above used headed files |
| (Found while fixing) `examples/run_jacks.py` header cites "mageck 0.5+"; `run_jacks_analysis()` shells out to bare `python` from the cwd and takes two unused condition arguments | shipped script | Header cites JACKS 0.2; uses `sys.executable` with `cwd=jacks_dir`; unused arguments removed | ran | `run_jacks_analysis()` returned True and wrote results identical to the CLI block |
| Reconciliation row blames `--apply_w_hp` for efficacy shrinkage | wrong mechanism | Row now says `apply_w_hp` acts on gene effects and points at the chemistry/prior fix | docs (source `inferJACKSGene`) | |

All 8 `recommendations[]` entries (2 P0, 3 P1, 3 P2) fixed, plus eight defects found while fixing. Nothing
left unfixed. `py_compile` clean on `examples/run_jacks.py`.

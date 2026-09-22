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

## 2026-09-21 fix batch (P2s, redundancy, split, scripts)

Worktree `F:\OpenScience\wt\crispr-screens-jacks-analysis`, branch `fix/crispr-screens-jacks-analysis`, from staging `main` 431aa55. Fixer: Claude Sonnet 5. Env `crispr-screen-analyst` (JACKS 0.2, pandas 3.0.5, Python 3.12). Verification data: the audit's HAP1 TKOv3 files (full 71,090 guides, and a 156-gene subset for quick runs) and JACKS' `example-small`. Commits: 381d1ba fix + redundancy, 8c35c01 split, db64e42 seed fix, 38c31e4 scripts.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| usage-guide step 12 lists `gene_results.txt`, `sgrna_efficacy.txt`, `library_redesign_candidates.txt`, `comparison_with_mageck.txt`, which no code produces | P2 | Step 12 now names the real outputs (`<outprefix>_gene_`, `_gene_std_`, `_grna_JACKS_results.txt`, `_gene_pval_` only with `--ctrl_genes`, `.pickle`) and labels the redesign list and MAGeCK comparison as agent-written summaries | ran (JACKS CLI/API output names on HAP1 and example-small) | the audit's recommended fix, second option |
| (found while verifying scripts) `random.seed(<int>)` said to make pseudo-gene p-values reproducible | internal contradiction | Model paragraph, Common Errors row and usage-guide step now require `PYTHONHASHSEED=<int>` as well | ran + docs (source `createPseudoNonessGenes` builds its list from a set of gene-name strings) | 60 control genes, 200 pseudo-genes: `random.seed` alone differs across processes; `random.seed` + `PYTHONHASHSEED=0` twice byte-identical; `PYTHONHASHSEED=1` differs. The 2026-09-16 "seeded runs match" check used a 2-gene control list, too small to show it |

1 of 1 P2 fixed, plus one defect found while fixing.

### Left unfixed

- Audit Input 3 assertion 4 (FAIL: the sequence-vs-ID silent-success case of a `--reffile` from a different library "was not exercised"): not a Skill defect (the auditor marked it not tested), and it needs a second library with matching guide IDs but different sequences, which does not exist on this machine.
- security note (paths passed to `subprocess` without existence checks in `examples/run_jacks.py`): list-form invocation, no shell; judged not a correction. Left as is.

### Redundancy pass (usage-guide.md was restating SKILL.md)

| deleted passage | new home |
|---|---|
| usage-guide Prerequisites (clone/install lines, required-input list, optional priors) | SKILL.md "Version Compatibility" and "Run JACKS Joint Analysis" (input-file list); guide keeps a pointer |
| "count matrix itself can serve as the guide map" | SKILL.md "Run JACKS Joint Analysis" input list (run: CLI with the HAP1 count matrix as guide map, `--gene_hdr gene`, 156 genes out) |
| Tips: single-screen, chemistry, Chronos, effect/std z, deterministic-effects | already in SKILL.md (When Not to Use, Critical assumption, Interpretation rule, Model, convergence failure mode); deleted |
| Tip: 2.5x reduction is conditional on same library and similar cell context | SKILL.md efficacy-prior reference block (now `references/efficacy-prior-and-diagnostics.md`) |
| Tip: fit per-cell-line, pool downstream as meta-analysis | SKILL.md failure mode "Cross-cell-line efficacy disagreement" (now `references/failure-modes.md`) |
| Tip: v2 library, drop bottom 25%, every gene >0.4 | `references/efficacy-prior-and-diagnostics.md` "Critical" paragraph |
| Key Thresholds table (hit call, effective signal, low-efficacy flag, screen count, iterations, reference) | SKILL.md Quantitative Thresholds; "~50 lines, ~10k screen days" moved to the efficacy-prior reference |
| Decision Comparison table | SKILL.md When JACKS Outperforms / Is Not the Right Tool; its "heavy selection (>40% of guides change): RRA fails, use MLE, BAGEL2 robust" row became a When-Not bullet |
| SKILL.md "Effective gene signal" threshold row (duplicate of Hit call) | merged into the Hit call row |
| SKILL.md cross-library and cross-chemistry threshold rows and the When-Not "cross-chemistry" bullet | Critical assumption paragraph and the "Reference efficacy prior from wrong library" failure mode |
| SKILL.md "Quantified accuracy gain" comparison-table row | first table's ~21% / 9% row (which gained "Allen 2019 did not benchmark BAGEL2") |
| SKILL.md Common Errors row "Library-reuse prior doesn't help" | same case in the wrong-library failure mode (silent ID-match case) |

### Split

`SKILL.md` 303 -> 171 lines (after the redundancy pass 303, after the split 181, after scripts 171). Moved verbatim: `references/efficacy-prior-and-diagnostics.md` (efficacy prior + per-sgRNA diagnostics), `references/failure-modes.md` (Failure Modes), `references/tool-comparison.md` (comparison + reconciliation tables). Every non-blank line of the old SKILL.md is in the new set (only headers, the Reference Files index and pointer text differ); python fences parse.

### Scripts

| old location | script |
|---|---|
| SKILL.md `runJACKS(...)` Python block | `scripts/run_jacks_joint.py` (ran on example-small with `--common-ctrl-sample CTRL`: 1,579 genes x 5 lines; on the HAP1 subset with per-sample `Control`, `--ctrl-genes/--n-pseudo/--seed`: p-value file written, none with `n_pseudo=0`; gene file byte-identical to the CLI run) |
| `efficacy_summary()` in the efficacy reference | `scripts/efficacy_summary.py` (ran on example-small: 8,081 guides, median 1.017, matches the audit; on full HAP1 grna output; raises the documented `ValueError` on a renamed guide) |

Left inline: CLI bash block (one command), `n_iter` and hyperparameter override recipes (under 15 lines, JACKS-internals illustrations), `extract_efficacy_prior` (5 lines). No block duplicated `examples/run_jacks.py`. Both scripts `py_compile` clean.

## 2026-09-21 final pass, Phase 1

Worktree `F:\OpenScience\wt\crispr-screens-jacks-analysis`, branch `fix/crispr-screens-jacks-analysis`
(same worktree/branch as the batch above). Fixer/auditor: Claude Sonnet 5 (final pass, one agent both
phases per `process/FINAL_PASS_BRIEF.md`). Env `crispr-screen-analyst`. Verification data: the same
example-small 5-cell-line/1,579-gene/8,081-guide set, plus JACKS' own 90,710-guide/18,056-gene
`example/` set with its bundled `NEGv1.txt` for a full-genome corroboration.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `examples/run_jacks.py` `run_jacks_analysis()` runs the JACKS subprocess with `cwd=jacks_dir` but never resolves the caller's file paths, so the natural relative-path call fails with `FileNotFoundError` | P1 | Resolve `counts_file`/`replicatemap_file`/`guidemap_file`/`output_prefix` with `os.path.abspath()` before building `cmd` | ran | Reproduced the failure pre-fix, then ran the fixed function with relative paths end to end through `analyze_results()`/`plot_results()`: 1,579 genes, 266 essential, PNG written |
| `SKILL.md`/`usage-guide.md` never mention `<outprefix>_logfoldchange_means.txt`/`_logfoldchange_std.txt`, which JACKS 0.2 always writes unless `--reffile` is given | P2 | Added both files to the CLI output comment in `SKILL.md` and usage-guide step 12 | ran (present without `--reffile`, absent with it) | source: `jacks_io.py` `load_data_and_run` |

### Resolved from the prior "left unfixed" list

- Audit Input 3 assertion 4 (silent-success case of a `--reffile` from a different library with
  matching IDs but different sequences): does **not** need a second real library. JACKS' reffile check
  is ID-only (never reads sequence), so a same-ID/different-value reffile is a full substitute. Built
  one synthetically (shuffled the real grna results' `X1`/`X2` under the same sgRNA IDs), ran it as
  `--reffile`: no error, and 1,364/1,579 gene effects differed from the correctly-matched run by >0.1
  (max diff 2.29) — confirms `references/failure-modes.md`'s documented claim.

### Left unfixed (unchanged)

- Security note (paths passed to `subprocess` without existence checks in `examples/run_jacks.py`):
  list-form invocation, no shell; judged not a correction in the prior pass. Still not a correction.

Full detail in `F:\OpenScience\audits\_final_pass\bio-crispr-screens-jacks-analysis\CHECKPOINT.md`.

# bio-single-cell-differential-abundance fixes (2026-09-21)

Worktree `F:\OpenScience\wt\single-cell-differential-abundance`, branch `fix/single-cell-differential-abundance`.
Fixer: Claude Sonnet 5. Runtime: env `single-cell-transcriptomics-analyst` (R 4.4.3 via `tools\rs.sh`; miloR 2.2.0,
speckle 1.6.0; scCODA 0.1.9 via `tools\sccoda-venv`). Nothing installed. First audit only (score 88); 1 P1 + 4 P2.
SKILL.md 187 -> 208 lines (commit `9f69601`), under the 300-line split threshold, so no `references/`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Milo (primary tool) false negative on the canonical case | P1 | Method table: Milo "Fails when" now states the audit numbers (0/284 nhoods at ~700-850 cells/sample vs propeller FDR 9e-5); "run a cluster-based method and Milo" sentence inverted so a cluster-based method leads and a Milo null does not overrule it; new "Power" paragraph in the Milo section; new Common Errors row | ran (audit input 2 numbers; example script re-run) | Audit asked for "thousands of cells per sample"; only 700-850 cells/sample was ever run, so the text states that and says the required count was not tested. Also added the audit's unlisted input-2 result: `~ batch + condition` gave 16 significant nhoods, 15 in unchanged CD14+ monocytes, as an "unconfirmed" caution in the confounding section (batch was balanced) |
| No seed anywhere | P2 | `set.seed(42)` before `Milo()` in SKILL.md and `examples/milo_differential_abundance.R`; `tf.random.set_seed(42)` in the scCODA block and `examples/sccoda_composition.py`; seed statement in Governing principle; Common Errors row | ran | Test (scratchpad `milo_seed2.R`, `sccoda_seed2.py`): seed 1 twice gave identical Milo neighborhood indices and SpatialFDR; unseeded runs gave 272/277/293 nhoods; scCODA with seed set BEFORE `CompositionalAnalysis()` reproduced inclusion probabilities exactly (maxdiff 0.0), unseeded differed 0.07. My first attempt (seed after model construction, just before `sample_hmc`) did NOT reproduce (maxdiff 0.139): the initial state is drawn in the constructor. The docs now say so |
| propeller transform default named wrongly | P2 | Method table + Approach line: logit is the speckle 1.6.0 default, `transform = 'asin'` the alternative | ran | New audit-independent finding: `transform='asin'` on the audit data called NK (FDR 1e-9) AND CD8 T cells (FDR 0.009, a false positive; truth is NK only), default logit called NK only. Stated in the propeller section |
| No Common Errors row for the n=1 failure | P2 | Row for `No finite residual standard deviations` added | ran (n=1 error reproduced) | |
| sccomp prescribed but not run | P2 | Not runnable here (see below). Added a version-drift note: the block uses sccomp 1.x tidy-eval arguments; upstream README (master) uses string arguments `sample=`, `cell_group=`, `abundance=` and a `cell_group` result column | docs (upstream README fetched; not run) | Which sccomp release changed this was not established |
| Governing-principle claim "scCODA and sccomp will still emit confident credible_effects() at n=1" | (not in report; claim contradicted by a run) | Reworded: scCODA re-run on S1 vs S5 (2 seeds) and S2 vs S8 returned no credible effects, even though NK doubled in S1 vs S5 | ran | sccomp at n=1 remains untested |
| scCODA `sample_hmc` arguments and runtime (audit input 3 note) | (audit note) | Comment in SKILL.md and example: `num_results`/`num_burnin` defaults, `n_burnin` is not an argument | help (`inspect.signature`) | |
| Install/version notes only in `usage-guide.md` | redundancy | Install commands moved into SKILL.md Version Compatibility, with "checked on miloR 2.2.0, speckle 1.6.0, scCODA 0.1.9" and the scCODA arviz<1 / tf_keras note (from `TOOLS.md`) | docs | |

Shipped examples: `milo_differential_abundance.R` sourced end to end on the audit's synthetic 8-sample data (runs, parses);
`sccoda_composition.py` run on an h5ad built from the same data, recovers NK cells only (log2FC +1.12), `py_compile` OK.

## Redundancy pass

| Deleted from `usage-guide.md` | Where the content lives now |
|---|---|
| "Prerequisites" (R and pip install blocks) | SKILL.md "Version Compatibility" (verbatim, plus CmdStan and arviz notes) |
| "What the Agent Will Do" (7 steps) | SKILL.md Governing principle (replicates, DE/DA pairing), "Choosing a method" (cluster vs cluster-free, reconcile), scCODA reference section, per-method blocks; no unique content |
| "Tips" (7 bullets) | Governing principle, reference-cell-type section, Milo section (SpatialFDR, k/prop), Common Errors (integrated embedding); no unique content |

The guide keeps overview, prompts, related Skills, and now points at SKILL.md. No disagreements between the two copies.

## Left unfixed

- **sccomp block has never been executed** (P2): sccomp 1.10.0 (the Bioconductor 3.20 build for R 4.4.3) needs `instantiate` and a CmdStan install (`cmdstanr` from r-universe, `install_cmdstan()` downloads and compiles CmdStan). That is a multi-hundred-MB toolchain build into the shared env, not a plain package install, and the brief bars shared-R-library installs and background waits. Fix pass could only check it against upstream docs and add the drift note.
- **How many cells per sample Milo needs** (P1 recommendation said "roughly thousands"): no data at larger cell counts exists in the audit set, and a simulation would be new content. The Skill states the measured failure point only.
- **CD4:CD8 composition-masquerades-as-DE claim** (audit input 5, not scored as a defect): audit could not demonstrate it on the synthetic data (CD4/CD8 profiles too similar); left as stated, no correction is possible without new data.

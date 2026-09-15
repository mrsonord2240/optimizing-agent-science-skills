# bio-phylo-divergence-dating fixes (2026-09-15)

Worktree `F:\OpenScience\external\bioSkills-wt-phylo`, branch `fix/phylogenetics`. Runtime: PAML 4.10.10 mcmctree, Biopython 1.88, audit data `loc1.phy` and audit BEAST 2.7.7 MCC trees (`runs/in4`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Bio.Phylo MCC snippet reads `.confidence` (None) and zips mismatched nodes | P1 | Regex on `clade.comment` for `height_median` / `height_95%_HPD`, clades matched by tip set; logged `mrca.age` as alternative | ran: prior/posterior medians and HPDs for AB, GH, root equal the audit's values from the .log files | clades absent from the prior MCC are reported as such |
| `BDparas` without flag; bare `usedata = 2` | P1 | `BDparas = 1 1 0.1 m`; `usedata = 2 in.BV`; `out.BV` -> `in.BV`; `ntaxa ntree` header; Common Errors rows | ran: example pipeline on loc1.phy, prior/bv/post exit 0, in.BV 2343 bytes | |
| `>`/`<` "silently ignored" row false on 4.10 | P1 | Row now: mis-parse only in PAML 4.9b-4.9d; prefer B()/L()/U() | audit run on 4.10.10 (identical calibration block and effective prior) + pamlHistory | not re-run by the fixer |
| `examples/mcmctree_setup.py` not runnable end to end | P2 | Tree file with header, per-run dirs with `mcmcfile`, out.BV copy with size check, seed 1234, label regex anchored at `)`, dead line removed, optional `aln tree` CLI | ran: py_compile, demo, full 3-step run on loc1.phy | no test alignment shipped (new content) |
| No temporal-signal code; positive slope passed no-signal data | P2 | Note: positive slope necessary, not sufficient; randomization test mandatory | audit Input 3 run | partial: no root-to-tip / date-randomization code (new content) |
| No clock-choice marginal-likelihood recipe | P2 | Pointer to BEAST2 MODEL_SELECTION PathSampler and bayesian-inference | docs | partial: MCMCTree mcmc3r workflow not added (not verifiable here) |
| `iqtree2` binary naming | P2 (cross-Skill) | `iqtree3` with "`iqtree2` on IQ-TREE 2.x" note | audit's bioconda recipe check (docs) | |

Unfixed: root-to-tip and date-randomization code, MCMCTree stepping-stone recipe, shipped test alignment -- all new content, out of scope.

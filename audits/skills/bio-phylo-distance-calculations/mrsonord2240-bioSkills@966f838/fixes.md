# bio-phylo-distance-calculations fixes (2026-09-15)

Branch `fix/phylogenetics`, worktree `F:\OpenScience\external\bioSkills-wt-phylo`. Audit score 82. Checked on Biopython 1.88, scikit-bio 0.7.3, R with ape 5.8.1 / phangorn, using the audit's simulated alignments.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Bio.Phylo `bootstrap_consensus` with NJ gives deflated support | P1 | SKILL.md replaces the "does the same" line with a warning and a rooted-replicate snippet (`bootstrap_trees` -> `root_with_outgroup` -> `majority_consensus(cutoff=0.5)`), plus a slowness note; `examples/bootstrap_consensus.py` roots replicates, seeds, prints confidences | ran on `barcode20.fa` B=100: unrooted max 61%, 0 clades >= 70; rooted max 100%, 12 clades >= 70; SKILL.md block as written: max 100, 9 clades >= 70; example runs, py_compile OK | method-level change, evidence: audit Input 5 and this run |
| Bootstrap drops the point tree's gamma | P1 | SKILL.md and `model_corrected_tree.R` define `method` once (TN93 + `gamma = alpha` + FastME) and pass it to `boot.phylo`; `set.seed(42)` | ran the SKILL.md R blocks on `deep12.fa` (support `NA 12 7 6 18 36 35 29 33 34`, identical on rerun with the seed); example runs; `parse()` OK | |
| Saturation gate is a test the agent cannot run | P1 | Pre-flight gives a runnable ape proxy (fraction p > 0.5, transition-proportion slope vs TN93, ts/tv plot scaled by length) with the observed values; Xia Iss marked optional via DAMBE in the Approach, failure-mode Fix, threshold table and usage-guide step 4 | ran the SKILL.md R block: `sat12` 0.83 / slope 0.040; `deep12` 0 / slope 0.171 | thresholds stated as observed on simulated data, not as a published cut-off |
| NaN below 0.75 and the `njs()` fallback undocumented | P2 | Common Errors row | ran on `comp8.fa`: K80 2 NaN, TN93 3 NaN at max p 0.647, `nj()` stops "missing values are not allowed"; `njs()`/`bionjs()` return 8-tip trees; LogDet 0 NaN | |
| Counts are not distances; `identity` counts gaps | P2 | Correction table lists `'raw'` only and marks `'N'`/`'TS'`/`'TV'` as counts; tool table notes the gap behaviour | ran: `'N'` max 1940 on 3000 sites; identity on 2 gap columns of 6 = 0.333 | |
| No corrected-matrix hand-off into Bio.Phylo/skbio | P2 | Python block: R `write.csv` -> pandas -> Bio.Phylo `DistanceMatrix(names, lower)` -> NJ, skbio one-liner | ran: 20-tip NJ tree from ape K80 CSV via Bio.Phylo and skbio | |
| Examples test nothing; dead code; no seeds | P2 | Partly: `model_corrected_tree.R` drops unused `ts`/`jc`, attaches and prints `bs`, seeds; `bootstrap_consensus.py` seeds and prints confidences | ran both examples | partial |

## Left unfixed
- P2 examples: no simulated alignment with a true tree shipped, and `pairwise_tree_distances.py` (patristic, off-topic) not moved to tree-manipulation. Both add or relocate content rather than correct it.

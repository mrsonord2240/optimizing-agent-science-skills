# Primary-source adjudication notes

The audit used exact live outputs as the primary executable evidence and current provider documentation as the primary interface evidence. Successful controls establish that the prepared tools and fixtures work; they do not repair the candidate surfaces.

## PAML

- PAML 4.10.10 itself reports successful marginal reconstruction and writes `rst` for both packaged control writers. The retained real `rst` files contain a site-by-node probability matrix and reconstructed-sequence table but no `Prob distribution at node X` blocks and no bare `node #X` sequence blocks in the format expected by the two candidate parsers.
- The official PAML repository routes users to the current PAML manual: https://github.com/abacus-gene/paml/blob/master/doc/pamlDOC.pdf.
- Evidence: `evidence/paml-surfaces.json`, `evidence/paml-provider-rst.txt`, and `evidence/paml-extracted-rst.txt`.

## IQ-TREE

- The official command reference defines `.state` rows as `Node`, `Site`, `State`, and one or more `p_X` posterior columns: https://iqtree.github.io/doc/Command-Reference#ancestral-sequence-reconstruction.
- The real IQ-TREE 2.4.0 output has 660 rows, 6 internal nodes, 110 sites, 20 posterior columns, and row sums within `3e-5` of 1. The candidate parser nevertheless accepts a table with zero `p_X` columns and returns `NaN` confidence.
- Evidence: `evidence/iqtree-output-validation.txt` and `evidence/python-surfaces.json`.

## OUwie

- CRAN currently publishes OUwie 3.0.3: https://cran.r-project.org/package=OUwie.
- Its primary reference manual defines `OUwie.anc(fitted.OUwie.object, ..., knowledge=FALSE, ...)`, has no `data=` argument, requires `knowledge=TRUE` after the warnings are read, provides no uncertainty estimate, and describes the result as a visualization/intuition aid rather than a firm historical estimate: https://cran.r-project.org/web/packages/OUwie/refman/OUwie.html#OUwie.anc.
- Evidence: `evidence/ouwie-probe.log` reproduces the candidate failure and a valid current-interface control.

## GRASP

- The official 21-Mar-2024 JAR help retained in `evidence/grasp-candidate-current.log` defines `-a/--aln`, `-n/--nwk`, `-o/--output-folder`, `-j/--joint`, and `-t/--threads`. The candidate's first `-aln` option is rejected with exit 5.
- The valid official control emits `alignment_ancestors.fa`, `alignment_ancestors.nwk`, and `ASR.json`, not the three filenames promised by the candidate shell.
- Provider project context: https://github.com/bodenlab/GRASP and https://github.com/bodenlab/GRASP-suite.

## corHMM

- CRAN currently publishes corHMM 2.8, not 2.9+: https://cran.r-project.org/package=corHMM.
- The provider's GitHub `master` DESCRIPTION reports 2.10.5 and adds RTMB: https://github.com/thej022214/corHMM/blob/master/DESCRIPTION. The retained API response identifies inspected commit `3ae10b22cfb519245b75777342812a0023ac0d43`.
- The exact candidate `corHMM(... rate.cat=2, model='ARD', node.states='marginal')` call passes on installed CRAN 2.8. That valid 2.8 result does not establish compatibility with the advertised but unpinned `2.9+` range.

## Scientific-claim boundary

- The candidate's current OU reconstruction language is stronger than the current OUwie provider warning and cannot satisfy its own requirement for uncertainty at every reported node.
- The continuous script fits six models but, for EB/lambda/kappa/delta winners, calls `contMap` on the original tree and never applies the winning fitted transformation. Therefore the reported reconstruction is not under the selected model.
- Thresholds labeled operational conventions remain heuristics, not universal biological constants. The main skill says this, but several routed tables still use categorical language such as “correct” and “trust”; those claims must be softened and tied to model adequacy and sensitivity evidence.

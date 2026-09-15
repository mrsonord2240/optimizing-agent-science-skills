# bio-phylo-tree-visualization fixes (2026-09-15)

Branch `fix/phylogenetics`, worktree `F:\OpenScience\external\bioSkills-wt-phylo`. Audit score 78. Checked on Biopython 1.88, matplotlib (venv), R with ggtree 3.14.0, treeio 1.30.0, ggplot2 4.0.3, ape 5.8.1.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `support_label` ignores IQ-TREE dual labels; hard-coded "Bootstrap" title | P1 | Recipe parses `a/b` names into SH-aLRT/UFBoot, clears `.name`, warns when no clade has support, and titles the measures; Common Errors row; `examples/labeled_tree.py` uses dual labels | ran every SKILL.md Python block on `iq/primates16.treefile`: labels `100/100, 88/92...`, no raw names left; example draws `88/97, 72/90`; py_compile OK | |
| Bio.Phylo rerooting shifts node-held support | P1 | "Unlabeled or Mislabeled Support" Fix: re-attach by bipartition after Bio.Phylo rerooting, or root with `treeio::root`/`ape::root(edgelabel = TRUE)` | ran: Bio.Phylo `root_with_outgroup` put 6 of 12 labels on another split; ape `root(edgelabel = FALSE)` 6 of 13, `edgelabel = TRUE` 1 of 13 (the duplicated root edge left blank) | |
| `geom_range` default re-centres asymmetric HPDs | P1 | Chronogram Fix uses `center = 'height'` and says to check one bar; Common Errors row | ran on `beast_mcc.tree`: `center = auto` max error 4.95 Ma, `center = height` 0 | |
| Scaled-panel recipe removes the only scale, ignores own thresholds | P1 | Keeps the x axis (hides y ticks/spines only), caps height at 40 in, prints a route-to-circular note above 150 tips, says the axis is the scale | ran on `big320.nwk`: height 40, xlabel `branch length`, 7 tick labels visible | |
| "Plain Newick tree has no color slot" row is false | P2 | Color recipe sets `.color` on the MRCA of a Newick-read tree; Common Errors row corrected | ran: draw() used red `(1, 0, 0)` for the clade | |
| ggtree/ggplot2 combination not pinned | P2 | Version block states the tested pair, what fails, and fallbacks | versions printed by R here; the failing layouts/`gheatmap`/`align` errors are from the audit's `layouts.log` and Input 5, not re-run | |
| ETE4 install and headless limits | P2 | One sentence in the version block | from the audit environment notes (pip build failure, offscreen no text); not re-run | |
| No ggtree code for the rich-figure path | P2 | not changed | - | new content |

## Left unfixed
- P2 "Add ggtree code patterns for the rich-figure path": a full read.iqtree -> geom_fruit -> geom_cladelab example is a new section, out of the brief's scope.

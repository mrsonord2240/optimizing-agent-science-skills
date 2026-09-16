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

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p2`, branch `fix/backlog-p2`. Runtime: candidate venv `F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\` (Biopython, matplotlib), R at `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe` with `R_LIBS_USER` pointed at the candidate's `R-lib` (ggtree 3.14.0, ggplot2 4.0.3, treeio, ggtreeExtra, ape).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Root before colouring clades by MRCA | P1 | "Color branches by group" recipe roots on an outgroup before any `common_ancestor` call, prints the MRCA tip set, clears raw IQ-TREE support strings from `clade.name`; new Common Errors row | ran | commit fa75880 |
| Correct the gheatmap line in the version block | P2 | Version Compatibility block no longer lists `gheatmap()` as flatly failing; says it is call-dependent (plain call succeeds, composite pipeline + `new_scale_fill()` call fails), cites the reproduced error, keeps `ggtreeExtra::geom_fruit` as the fallback | ran | commit 00141d5; plain `gheatmap(ggtree(tr), df)` on `primates16_true.nwk` -> OK; composite pipeline mirroring fig2.R (prior geoms + `new_scale_fill()`) on rooted `primates16.treefile` -> `new_geom_point_g_gtree() requires the following missing aesthetics: x` (ggtree 3.14.0, ggplot2 4.0.3, treeio 1.30.0, ggnewscale 0.5.2) |
| Add ggtree patterns for rich figures | P2 | New "## ggtree + treeio Recipe (R)" section (after Bio.Phylo recipes, before Per-Method Failure Modes): `read.iqtree()` -> `root_keep()` (`treeio::root(..., edgelabel = TRUE)` + tip-label-by-index restore) -> `geom_nodelab()` dual SH-aLRT/UFBoot -> `geom_fruit()` metadata ring; one sentence on groupOTU's verified stem-coloring behavior | ran | commit 0f50878; equivalent pipeline (real outgroup Microcebus_murinus+Otolemur_garnettii) on `primates16.treefile`: 13/14 internal nodes non-NA UFboot after rooting, `ggplot_build()` on the nodelab+geom_fruit composite succeeds (7 layers), `ggsave()` writes a non-empty PDF; `groupOTU(list(Apes=...))` + `aes(color=grp)` checked via `ggplot_build()` segment colours -- stem edge into Apes MRCA (#00BFC4) matches an Apes tip edge (#00BFC4) and differs from the edge above the ungrouped parent (#F8766D), confirming no stem-miscoloring bug on this ggtree version; exact SKILL.md R block also `parse()`-checked. Reverses the prior pass's "out of scope" call per FIX_BRIEF's "Missing referenced executables" section (2026-09-15) |

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

## Second-pass dispatch — 2026-09-18

Worktree `F:\OpenScience\wt\phylo-tv`, branch `fix/phylo-tv`, off staging `main`. Env
`F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\` (ggtree 3.14.0, ggplot2 4.0.3,
treeio 1.30.0, ggtreeExtra 1.16.0, ape 5.8.1, Biopython 1.88).

Dispatched against the same three findings (root-before-MRCA, gheatmap version-block line,
ggtree rich-figure patterns), sourced from `BACKLOG.md` at audit
`mrsonord2240-bioSkills@966f838`. Investigation before touching anything: `966f838` is an
ancestor of `fa75880`/`00141d5`/`0f50878` (the Backlog-pass commits above) in the fork's
history, and those three commits are already ancestors of staging `main`'s tip (`558aea5` is
an ancestor of my worktree's `HEAD`). The re-audit that produced the 84 score ran against a
pre-fix snapshot; `BACKLOG.md` was never regenerated after the Backlog-pass fix landed, so it
still lists these as open. All three were re-verified independently rather than trusted on
that basis alone:

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Root before colouring clades by MRCA | P1 | Already fixed at HEAD (commit `fa75880`). Reproduced the bug on a synthetic 16-tip tree (true 5-tip clade `A1-A5`, arbitrary root placed *inside* that clade, mimicking IQ-TREE's unrooted-as-stored convention): `common_ancestor('A1','A5')` without rooting returned all 16 tips; `root_with_outgroup('OG')` first correctly isolated the 5 tips. Found the recipe's tip-set check was print-only (no hard failure) -- upgraded to `raise ValueError` on mismatch; Common Errors row updated to match | ran (Python, this env's Biopython 1.88): pre-fix repro all-16, post-fix exact-5, fail-loud check verified to both pass silently on the correct path and raise on the exact bug path | commit `4cc2487` |
| Correct the gheatmap line in the version block | P2 | No change -- already correct at HEAD | ran (R, this env): plain `gheatmap(ggtree(tr), df)` -> OK; composite (`geom_tippoint` + `new_scale_fill()` + `gheatmap`) -> `new_geom_point_g_gtree() requires the following missing aesthetics: x` (exact match to the quoted text already in SKILL.md); `geom_fruit` fallback on the same composite case -> OK | |
| Add ggtree patterns for rich composite figures | P2 | No change -- already present at HEAD | ran (R, this env) the exact SKILL.md `read.iqtree` -> `root_keep` -> `geom_nodelab` -> `geom_fruit` pipeline on a synthetic IQ-TREE-style treefile: `ggplot_build()` succeeds (7 layers), `ggsave()` writes a non-empty PDF (6232 bytes), `groupOTU` + `aes(color=grp)` produces 2 distinct segment colours (no stem-miscoloring) | |

3/3 findings addressed (2 already correct and reverified, 1 genuine residual gap fixed: the
fail-loud check). `usage-guide.md` checked against the redundancy rule -- already
overview/example-prompts/related-Skills only, no duplication to collapse.

## Left unfixed
None from this pass. Flag for Sam: `BACKLOG.md` / the audit pipeline should be re-run to
regenerate the record against current staging `main`, since the 84-score audit it lists
predates the Backlog-pass fix it's nominally scoring.

## 2026-09-21 -- P2 batch, redundancy pass, split

Worktree `F:\OpenScience\wt\phylogenetics-tree-visualization`, branch `fix/phylogenetics-tree-visualization`, off staging `431aa55`. Env `molecular-phylogenetics-analyst` (Biopython 1.88, matplotlib, R 4.4 with ape 5.8.1, ggtree 3.14.0). Commits `35d2cce` (fix), `e2e8306` (redundancy), `1d9b6fc` (split). Audit re-run report: 3 P2s, no P0/P1.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Bio.Phylo panel illegible past the threshold (320 tips) | P2 | Scaled-panel recipe now raises `ValueError` when tips > `MAX_TIPS = 200` (still warns at >150); Common Errors "Labels overlap" row updated | ran (Biopython 1.88): 16 tips draws; 190 tips draws + warns; `big320.nwk` raises | 200 chosen as the ceiling because the 40 in height cap is reached at 160 tips and the audit's 320-tip run was illegible; `MAX_TIPS` is an explicit override |
| ape unrooted fallback has no recipe or scale bar | P2 | Added `ape::plot.phylo(type='unrooted')` + `add.scale.bar()` block (now in `references/ggtree-ape-recipes.md`); Version Compatibility fallback points to it | ran (ape 5.8.1, `primates16_true.nwk`): PDF written; second check on uncompressed PDF text finds scale-bar label `(0.05)` plus tip labels | |
| Inconsistent severity between the no-support warning and the MRCA raise | P2 | Kept both behaviours and stated the reason in the Common Errors row: a tree with no support values is legitimate and draws correctly (warn); a wrong MRCA silently colors the wrong clade (raise) | docs / reasoning, no code change | chose "note why" over "raise on both": raising on no-support would break cladograms and unsupported trees |

### Left unfixed
None.

### Redundancy pass (usage-guide.md 65 -> 28 lines)

| deleted passage | new home |
|---|---|
| Overview paragraph 1 (four argument-level choices, cladogram/phylogram/chronogram, ladderization, root, support) | shortened to 3 sentences; full text already in SKILL.md "The Single Most Important Modern Insight" |
| Overview paragraph 2 (tool decided by I/O layer) | SKILL.md insight #4 and Tool Taxonomy decision rule |
| Prerequisites: pip / Bioconductor / web+desktop lines | install line added to SKILL.md Version Compatibility (pip, Bioconductor, CRAN ape); iTOL/FigTree already in Tool Taxonomy |
| Prerequisites: "know branch lengths, rooted, which support" | SKILL.md insight list and Failure Modes |
| What the Agent Will Do steps 1-5 | SKILL.md insight, Tool Taxonomy, Quantitative Thresholds (tip counts, vector, scale bar, support). "Write outputs to a temp/namespaced path" was generic advice found nowhere else; dropped |
| Tips: geometry is a claim / chronogram needs age bars | SKILL.md insight #1, Failure Modes "Drawing Meaningless Branch Lengths", "Chronogram Without Age Uncertainty" |
| Tips: ladderize for legibility only | insight #2, Failure Mode "Non-Monophyly Hidden by Ladderization" |
| Tips: bare support number, PP vs BP | insight #3, Failure Mode "Unlabeled or Mislabeled Support", Thresholds |
| Tips: route Bayesian trees to treeio + ggtree | insight #4, Common Errors first row |
| Tips: vector export, >=600 dpi | Failure Mode "Raster Export", Thresholds |
| Tips: unrooted has no basal taxon | Layout table, Common Errors "Basal claim" row |

Verified by grep that each target exists in SKILL.md (600 dpi, "basal", install line, failure-mode headings).

### Split (SKILL.md 304 -> 167 lines)

`## Bio.Phylo + matplotlib Recipes` -> `references/bio-phylo-recipes.md` (104 lines); `## ggtree + treeio Recipe (R)` (incl. the new ape block) -> `references/ggtree-ape-recipes.md` (38 lines). "Reference Files" index added, pointer added to the Decision rule, two cross-references in SKILL.md retargeted. Moved text verbatim except four relative references ("above"/"below") retargeted to file names. Verified: multiset compare of non-blank lines shows only the edited lines differ, Python fences `ast.parse`, R fences `parse()` (14 expressions), fence counts even.

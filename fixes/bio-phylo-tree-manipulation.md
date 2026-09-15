# bio-phylo-tree-manipulation fixes (2026-09-15)

Branch `fix/phylogenetics`, worktree `F:\OpenScience\external\bioSkills-wt-phylo`. Audit score 80. Checked on Biopython 1.88, MAD 2.2 (`mad.py`), IQ-TREE 2.4.0, with the audit's synthetic IQ-TREE trees.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Outgroup guard refuses valid outgroups on IQ-TREE trees; `root_with_outgroup` gives a trifurcating root | P1 | Snippet: root on an ingroup tip, test monophyly, then `root_with_outgroup(*outgroup, outgroup_branch_length=stem/2)`; Approach explains why; Common Errors row; `examples/root_tree.py` uses an IQ-TREE-style layout and the same pattern | ran the SKILL.md block on `og16_ml.treefile`: old guard False, new root children `[ingroup] / [OutA, OutB]`; example prints naive False and a bifurcating root; py_compile OK | |
| `collapse_all` silently no-ops on `SH-aLRT/UFBoot` labels | P1 | `support()` parser (UFBoot = last `/` field) + assert readable support before collapsing; Common Errors row; `examples/collapse_support.py` adds a dual-label case | ran the SKILL.md block on `edge16.treefile` (UFBoot < 95): 14 -> 13 internal nodes (old recipe 14 -> 14); example collapses both cases; py_compile OK | |
| Zero-length tolerance 1e-8 misses IQ-TREE 1e-6 | P2 | Snippet uses `<= 1e-6`; threshold row says match the writing program | ran: `edge16` has 0 branches < 1e-8, 4 <= 1e-6 | |
| Collapsing changes patristic distances | P2 | One paragraph after the collapse snippet | ran: `collapse_all` changed B-C 0.2 -> 0.6 on a toy tree; ape recipe change 0.093 from audit Input 5 | |
| MAD/MinVar agreement is not root confidence; no likelihood command | P2 | Rule text: agreement is not confidence, report MAD AI; added `iqtree3 -s aln.fa --model-joint 12.12 -B 1000 --root-test -zb 1000 -au` with "`iqtree2` on IQ-TREE 2.x" and the outputs to report | ran: audit log `rootnr.log` shows this command on IQ-TREE 2.4.0 writing `.rootstrap.nex` and `.roottest.csv`; MAD AI printed (0.869) on og16 | method-level: the audit's deep20 run showed MAD+MinVar agreeing on a wrong root. `iqtree3` name taken from the dispatcher (Bioconda IQ-TREE 3); IQ-TREE 3 flags not run here |
| Bio.Phylo `):0;` root breaks MAD 2.2 | P2 | Comment next to the MAD command with a `re.sub` strip | ran: MAD on Bio.Phylo output -> `Corrupt NEWICK format`; after strip -> `MAD = 0.243, AI = 0.869` | |
| `common_ancestor.py` prints "Clade"; `nw_condense` mislisted; no ladderize code | P2 | `bool(...)`; tool table lists `nw_ed` with a support address and notes what `nw_condense` does; `tree.ladderize()` line with a no-biology comment in the collapse snippet | ran: example prints `True`; ladderize ran in the snippet; Newick Utilities from the audit's source/help check only (no Windows build) | |

## Left unfixed
- None. RootDigger is still named without flags (not in the findings).

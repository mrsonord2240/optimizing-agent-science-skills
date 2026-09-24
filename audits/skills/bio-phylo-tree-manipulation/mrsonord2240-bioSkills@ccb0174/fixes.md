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

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p2`, branch `fix/backlog-p2`. Runtime: candidate venv `F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\` (Biopython).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Check ingroup monophyly in the outgroup snippet | P2 | "Root with an Outgroup" snippet now declares a separate, a-priori `ingroup` taxon list and checks its monophyly after rooting, printing a warning if it fails; Approach prose explains why a complement-of-outgroup check is a no-op | ran | commit 383ad1c; on `far15_ml.treefile` (15 tips, FarOut + 14 ingroup incl. I13): confirmed complement-of-outgroup "ingroup" monophyly is always True by construction (no-op) for both `outgroup=[FarOut]` and the LBA mistake `outgroup=[FarOut, I13]`; the new separately-declared-ingroup check correctly returns True (no warning) for `outgroup=[FarOut]` and False (warns) for `outgroup=[FarOut, I13]`, where I13 is really an ingroup taxon LBA-attracted to FarOut; exact SKILL.md snippet (placeholders swapped for real names in the verification script only) `py_compile`'d and ran both ways |
| Give RootDigger flags or drop it | P2 | Fixed "rootdigger" binary-name typos to `rd` (Tool Taxonomy row, inline CLI list); tied the RootDigger software name to its `rd` binary at every other mention (Rule paragraph, Common Errors row, usage-guide.md); added a real, doc-checked `rd --msa aln.fa --tree tree.nwk --exhaustive` (+ `--early-stop` note) to the Root-at-the-Midpoint code block, explicitly marked not-run-here | docs | commit fa5496e; RootDigger/rd confirmed absent (recursive find under audit-envs tools/ and Scripts/, second independent check); command cross-checked against 3 sources: computations/root_digger GitHub README (fetched directly, confirms binary `rd` and exact `--msa/--tree/--exhaustive` usage), web search over the same repo/docs, and the Bettisworth & Stamatakis 2021 paper's Methods section (fetched via PMC, gives `rd --msa <MSAFILE> --tree <TREEFILE>`) -- all three agree on `rd`, not the finding's suggested "rootdigger"; left the prior pass's `iqtree3 --root-test` line in place as the runnable confidence-bearing alternative |

## Final pass — 2026-09-24

Branch `agent/finalpass-bio-phylo-tree-manipulation-20260924`, worktree `F:\OpenScience\worktrees\bio-phylo-tree-manipulation-finalpass`, source commit `ccb01746cf23973cdd265786bf90b84ceddb2528` from staging main `2812e22`. Canonical final-pass report: `F:\OpenScience\audits\bio-phylo-tree-manipulation\eval_report_bio-phylo-tree-manipulation_result.json`; 94, Production Ready, deployable, 31/31 assertions. It is explicitly marked `auditor_independent: false` because this pass fixed and audited under one brief.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Shipped `root_tree.py` described the a-priori ingroup safety check but did not execute it | P2 | Declared the focal ingroup in the example and checked its monophyly after outgroup-stem rooting; emits an LBA/outgroup-choice warning on failure | `final_pass_verify.py`: shipped example compiles and runs from a clean cwd; its success path prints the check; archived `FarOut + I13` regression has outgroup-only monophyly true but the separate ingroup check false | resolves the only open re-audit finding in executable user-facing source |

All eight archived scenario areas were replayed or evaluated as their original routing answer: close-outgroup rooting, pruning/distance preservation, UFBoot/zero-length collapse, MAD, MinVar, non-reversible IQ-TREE root confidence, LBA, and the FarOut-plus-I13 error. Two fresh inputs added a malformed a-priori ingroup and a label-free support tree. No P0/P1/P2 remains in the final-pass scope.

# bio-phylo-tree-io fixes (2026-09-15)

Branch `fix/phylogenetics`, worktree `F:\OpenScience\external\bioSkills-wt-phylo`. Audit score 84. Checked on Biopython 1.88, DendroPy 5.0.13, ete3 3.1.3 with the audit's synthetic data.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `Phylo.convert` to Newick "annotations dropped" is false | P1 | Comment in the convert line, the MCC failure-mode Mechanism and the Key Insight now say Bio.Phylo writes escaped `[\[&...\]]` comments that DendroPy/treeio cannot parse; DendroPy snippet writes with `suppress_rooting=True` | ran: `mcc6.tree` converted, output has `\[`, DendroPy re-read posteriors all None; `suppress_rooting` output has no `[&R]` | also removes the "Newick cannot hold `[&...]`" contradiction |
| Bio.Phylo fails on MrBayes `.con.tre` and names foreign NeXML tips by otu id | P1 | 2 Common Errors rows (DendroPy / treeio `read.mrbayes`; DendroPy for NeXML) | ran: `mb10.con.tre` -> `AssertionError: Two string taxonomies?`; `nex8.xml` tips `d7, d6, d8` vs DendroPy `Homo sapiens...` | |
| No encoding or quoted-label guidance | P1 | Encoding note after the format list; name-trap Fix says use UTF-8 handles and sanitize before ape/ete3; Common Errors row for garbled non-ASCII | ran: path read gives `CercopithÃ¨que_ascagne`, UTF-8 handle read and write round-trip correct; ete3 raises `NewickError` / `KeyError` on quoted names; ape `NA` taken from the audit's `odd_names.R.log` | |
| `cdao` needs rdflib; DendroPy values are strings | P2 | Format list notes rdflib + no confidences; snippet casts `float()` | ran: typed rows `(1.0, [38.1, 48.9])`; `_io.py` source shows `CDAOIO` import under `try/except ImportError` | rdflib is installed in the venv, so the KeyError was not re-run |
| IQ-TREE `SH-aLRT/UFBoot` label lands in `.name` (cross-Skill) | P1 (dispatcher) | Bio.Phylo snippet splits `clade.name` when confidence is None; "Support Value Read as a Node Name" Mechanism/Symptom corrected (Bio.Phylo neither truncates nor errors) | ran on `iq10.treefile`: `99.4/100 -> SH-aLRT 99.4, UFBoot 100.0` | |
| Shipped example claims a loss it never shows | P2 | `examples/convert_formats.py` now converts an annotated Nexus tree and prints DendroPy-readable posteriors before/after | ran: `before=2, after=0`; py_compile OK | partial: no new BEAST/MrBayes/IQ-TREE example files added (new content) |

## Left unfixed
- P2 examples: extra example files for an MCC side-table extraction and a Python dual-label split were not added. That would be new content; the split now sits in the SKILL.md snippet.

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p2`, branch `fix/backlog-p2`. Runtime: Python venv
`F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\Scripts\python.exe` (Biopython), audit
data `F:\OpenScience\audits\bio-phylo-tree-io\data\iq10.treefile`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Key Insight 3 ("Single Most Important Modern Insight") said IQ-TREE's `SH-aLRT/UFBoot` dual label "truncates or chokes" a single-value parser, contradicting the already-corrected "Support Value Read as a Node Name" failure-mode section further down the same file | P2 | Replaced the contradicting clause with: a single-value parser like Bio.Phylo neither truncates nor errors on the dual label -- it keeps the whole string in `.name` and leaves `.confidence` empty -- with a cross-reference to the failure-mode section | ran: `Bio.Phylo.read()` on `iq10.treefile` (dual-support Newick) -- every internal `clade.name` held the full string (`99.4/100`, `99.3/100`, `98.1/98`, `100/100`, `94/93`), `clade.confidence` was `None` in every case, no exception | commit 3ba91aa |
| "Bio.Phylo writes NeXML without confidences or taxonomy" | P2 | Added a Common Errors row: Bio.Phylo's NeXML writer keeps a plain single `.confidence` (via `cdao:has_Support_Value`) but drops phyloXML-typed `.confidences` and always drops taxonomy; recommends DendroPy for annotation-preserving NeXML | ran: `iq10.contree` (single bootstrap) round-tripped through `Phylo.write`/`Phylo.read` nexml with confidences intact (100, 98, 93...); `phylo8.xml` (phyloXML, dual bootstrap+probability + NCBI taxonomy) round-tripped with confidence and taxonomy both lost -- `.confidence` is `None` even though `.confidences=[80.0, 0.97]`; DendroPy check: `mcc6.tree` (BEAST posterior/HPD/rate via `extract_comment_metadata=True`) written straight to nexml produced 68 typed `<meta>` elements with posterior values matching source exactly | commit 0ecf9dc; finding's blanket claim was only half true -- simple single-value confidence is NOT dropped, only phyloXML-typed multi-confidence and taxonomy are |

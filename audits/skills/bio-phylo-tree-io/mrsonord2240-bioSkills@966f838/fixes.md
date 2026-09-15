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

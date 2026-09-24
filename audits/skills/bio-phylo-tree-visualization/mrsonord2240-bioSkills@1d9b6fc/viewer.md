> **Audit record for `bio-phylo-tree-visualization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1d9b6fc](https://github.com/mrsonord2240/bioSkills/tree/1d9b6fcb44d3e728d78d653e437abfed59ecb55a/phylogenetics/tree-visualization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-visualization

## Canonical final summary

**Final:** 96/100 — ⭐ Production Ready; deployable: true.

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@1d9b6fcb44d3e728d78d653e437abfed59ecb55a:phylogenetics/tree-visualization`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 3/3 | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 3/3 | ✅ |
| 3 | Variant B | 39 | 58 | 97 | 3/3 | ✅ |
| 4 | Edge | 39 | 58 | 97 | 3/3 | ✅ |
| 5 | Stress | 39 | 58 | 97 | 3/3 | ✅ |
| 6 | Variant C | 39 | 57 | 96 | 3/3 | ✅ |
| 7 | Fallback | 39 | 57 | 96 | 3/3 | ✅ |

Execution average: **96.7 / 100**. Assertion pass rate: **21/21 (100%)**.

## Runtime and execution evidence

The shared environment was not changed. A new isolated WSL micromamba environment, `phylo-phase2`, used Python 3.12/Biopython/matplotlib and R 4.5 with treeio 1.34.0, ggtree 4.0.5, ggtreeExtra 1.20.1, ggplot2 4.0.3, and ape. The exact source tip was unchanged throughout.

1. **ASCII inspection:** shipped `ascii_tree.py` printed the Newick summary and terminal ASCII topology.
2. **Vector phylogram:** shipped `basic_tree_plot.py` wrote a vector PDF through the headless Agg backend.
3. **Dual support:** shipped `labeled_tree.py` parsed and printed `88/97` and `72/90`, then wrote an SVG.
4. **Root-first MRCA coloring:** a rooted synthetic outgroup test recovered exactly the four intended primate tips and wrote a 14,348-byte PDF.
5. **Large-tree safety:** the documented 200-tip Bio.Phylo ceiling rejected a 201-tip input with its actionable `ValueError`.
6. **ggtree/treeio/ggtreeExtra:** the documented read-IQ-TREE, root-preserve-labels, dual-support, `geom_fruit` composite built seven layers and wrote a 5,893-byte PDF.
7. **ape fallback:** documented `plot.phylo(type='unrooted')` plus `add.scale.bar()` wrote a 4,464-byte PDF.

Every executed command ended in `exit=0`; source logs and output files are in `run/`.

## Assertions

### Input 1 — ASCII inspection

- [PASS] The shipped example imports Bio.Phylo and parses a Newick tree — terminal output contains the tree structure.
- [PASS] The output contains a topology sanity check — an ASCII diagram was printed.
- [PASS] The command exits successfully — `python_examples.out` ends `exit=0`.

### Input 2 — Vector phylogram

- [PASS] The shipped plotting example uses a headless backend — it completed without a display.
- [PASS] A vector PDF is written — the example printed its PDF destination.
- [PASS] Branch-length interpretation is named — the plotted title states subs/site.

### Input 3 — Support labeling

- [PASS] IQ-TREE dual labels are parsed — `88/97` and `72/90` were printed.
- [PASS] Raw internal names are removed before drawing — the shipped parsing block clears them.
- [PASS] The figure names both support measures — the title states SH-aLRT/UFBoot.

### Input 4 — Root-first MRCA coloring

- [PASS] Rooting precedes `common_ancestor` — the verification follows the documented order.
- [PASS] The MRCA terminal set is checked exactly — four intended tips were recovered.
- [PASS] A colored PDF is materialized — 14,348 bytes.

### Input 5 — Large-tree threshold

- [PASS] The hard 200-tip ceiling is enforced — 201 tips raised the documented error.
- [PASS] The error suggests an appropriate alternate route — ggtree/iTOL is named.
- [PASS] This guard prevents an illegible rectangular output — failure occurs before rendering.

### Input 6 — Rich ggtree composite

- [PASS] treeio, ggtree, and ggtreeExtra load and execute in an isolated R runtime — composite exited 0.
- [PASS] The composite has the expected multilayer construction — `ggplot_build()` returned seven layers.
- [PASS] The vector output is nonempty — PDF is 5,893 bytes.

### Input 7 — ape fallback

- [PASS] The unrooted fallback draws successfully — ape completed with exit 0.
- [PASS] The mandatory scale-bar call executes — `add.scale.bar()` ran before device close.
- [PASS] The vector output is nonempty — PDF is 4,464 bytes.

## Veto assessment

Skill veto: PASS. Research veto: PASS. The Skill declares phylogenetic-layout assumptions, makes no clinical conclusion, carries no secrets or destructive operation, uses output assertions, and every sampled code path is runnable in the private runtime.

# bio-phylo-modern-tree-inference fixes (2026-09-15)

Passing (core) Skill; simple defects fixed at coordinator request, same corrections as bio-phylo-species-trees. Worktree `F:\OpenScience\external\bioSkills-wt-phylo`, branch `fix/phylogenetics`. Installed binary: IQ-TREE 2.4.0 (`tools\bin\iqtree2.exe`); no IQ-TREE 3 on this machine.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `--gcf` with `--scfl` in one call exits with "Do not specify --scf or --gcf with --scfl" | P1 | Two calls (`-t ... --gcf` -> `concord_g`; `-te ... -s ... --scfl 100` -> `concord_s`) in SKILL.md and `examples/partitioned_analysis.sh`; output description updated; Common Errors row | ran: `partitioned_analysis.sh` on audit `concatenated.fasta`, exit 0, gCF stat and sCF tree written | error reproduced in audit `runs/in5/concord.stdout` and `runs/examples/part.out` |
| `iqtree2` not on PATH after bioconda install (IQ-TREE 3 ships `iqtree3`/`iqtree`) | P2 | SKILL.md commands use `iqtree3` with "`iqtree2` on IQ-TREE 2.x" note; Common Errors row; both examples resolve `iqtree3 \|\| iqtree2 \|\| iqtree` | ran: `iqtree_basic.sh` on audit `gene12_aln.fa`, exit 0 (resolver chose installed iqtree2); `bash -n` both; naming from audit's bioconda recipe check (docs) | IQ-TREE 3 itself not run |

Unfixed: none in scope. Prose product name "IQ-TREE2" and `usage-guide.md` (`conda install -c bioconda iqtree`, correct as written) left unchanged.

bio-alignment-multiple: no `iqtree` reference in `alignment/multiple-alignment`; left byte-identical.

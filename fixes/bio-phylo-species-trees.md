# bio-phylo-species-trees fixes (2026-09-15)

Worktree `F:\OpenScience\external\bioSkills-wt-phylo`, branch `fix/phylogenetics`. Runtime: IQ-TREE 2.4.0, ASTER Windows build (astral 1.25.4.8, wastral, astral-pro), audit data `rad` and `fam`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `--gcf` + `--scfl` in one call exits 2 | P1 | Two calls (`-t ... --gcf`, `-te ... -s ... --scfl 100`) in SKILL.md and `astral_pipeline.sh`; Common Errors row | ran: both exit 0; combined call reproduces the error | `bash -n` on the example |
| ASTRAL units statement wrong for ASTER | P1 | astral/astral-pro default `SULength` (tip lengths written), `--length CULength` for coalescent units; wastral and Java write CU (SKILL.md, example echo, usage-guide) | ran: default vs `--length CULength` vs wastral trees; help `--length SULength` | |
| ASTRAL-Pro command omits gene->species map | P1 | `astral-pro -a gene2species.txt`, map format, silent-failure warning | ran on audit fam families: 8-tip species tree | |
| <10% contraction no-op with UFBoot; nw_ed not on Windows | P2 | Rule scoped to standard bootstrap, UFBoot note, wASTRAL as main guard | audit evidence (lowest UFBoot 12) | partial: no portable contraction snippet |
| No q2/q3 asymmetry test; cf.stat "q1/q2/q3" false | P2 | cf.stat described as gCF/gDF1/gDF2/gDFP; `astral -u 3` freqQuad.csv; binomial f2 vs f2+f3 | ran: `-u 3` writes freqQuad.csv; binomtest p 1.2e-8 on audit Input 4 values; cf_g.cf.stat header | |
| Install lines (bpp, iqtree2) | P2 | BPP -> GitHub releases; iqtree3 naming with `iqtree2` on 2.x note; example resolves `iqtree3`/`iqtree2`/`iqtree` | audit's bioconda API/recipe check (docs); resolver line run | IQ-TREE 3 binary itself not run here |
| Circular StarBEAST2 routing; `-t 8` wording | P2 | Related Skills reworded (SKILL.md, usage-guide); "`-t 8` gives default localPP only, no q1/q2/q3" | audit run output | |
| Anomaly-zone recovery overstated | P2 | Consistency is asymptotic; deep-zone deliverable is a supported near-polytomy | audit az2k run | |

Unfixed:
- SVDQuartets PAUP* block, BPP control file, StarBEAST2 XML: new content, out of scope.
- Portable (DendroPy/ete3) contraction snippet: new content; the text now steers to wASTRAL instead.

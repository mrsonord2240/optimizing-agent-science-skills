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

## Backlog pass — 2026-09-15

Worktree `F:\OpenScience\external\bioSkills-wt-p2`, branch `fix/backlog-p2`. Runtime: ASTER Windows
`astral.exe` v1.25.4.8 (`tools/aster/ASTER-Windows/exe/`), audit data `runs_v2/in9` (synthetic
`gene_trees_mixed.nwk` / `name2species.txt`) and `data/rad` (clean control).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No leaf-name consistency check before ASTRAL (Input 9): S03 renamed S03_b in 30/150 gene trees, `astral` exits 0 with `#Species: 11` and S03_b silently grouped at low support | P2 | Added a leaf-set-union check (`grep -oE`/`tr`/`sort -u`) before the wASTRAL/ASTRAL calls in SKILL.md's main code block, a `grep '#Species'` cross-check after, a Common Errors row, a paragraph extending the existing astral-pro `-a` map-file pattern to plain `astral`/`wastral`, and mirrored both checks into `examples/astral_pipeline.sh` | ran: astral.exe v1.25.4.8 on gene_trees_mixed.nwk -- before exit 0/`#Species: 11`/S03_b at localPP 0.553; leaf-check gives 11 (10 on clean rad data, no false positive); after `-a name2species.txt` exit 0/`#Species: 10`, correct clades restored; `astral --help` confirms `-a`/`--mapping` is shared across astral/astral-pro/wastral; `bash -n` on the edited example | commit b20ad7a |
| Frontmatter description and opening Approach line lag the body (prior pass fixed body's ASTRAL-units and <10%-contraction statements but not these two) | P2 | description: "ASTRAL branch lengths are coalescent units" -> "ASTRAL branch-length units depend on the binary and the `--length` flag (not always coalescent units)"; Approach line: "contract branches below ~10% support ... then run wASTRAL as the primary estimate" -> "contract branches below ~10% STANDARD bootstrap support ... (a near no-op under UFBoot), then run wASTRAL as the default primary estimate -- its per-branch weighting is the main guard against gene-tree error" | prose-only: read current body and matched wording against it (line 110 units-depend-on-binary/flag statement; code-block UFBoot no-op note + Quantitative Thresholds "< ~10% standard bootstrap (not UFBoot; or use wASTRAL)" row) -- no command to run | commit 4088971 |
| Method Taxonomy recommends SVDQuartets and BPP (Inputs 3, 6) with no runnable command for either; a prior pass declined this as "new content" (see "Unfixed" below) -- overruled by FIX_BRIEF's "Missing referenced executables" rule | P2 | New "## Minimal SVDQuartets and BPP Commands" section: minimal PAUP* NEXUS `taxpartition`/`svdq` block, and a minimal BPP A00 control file plus the one-line A10 diff, both marked not executed here | docs: neither tool installed (recursive find under audit-env `tools/`, PATH check -- both absent; PAUP* is registration-gated freeware). SVDQuartets checked against 2 sources (phylosolutions.com tutorial WebFetch + independent WebSearch, agreeing). BPP checked against the official `bpp/bpp` GitHub repo's own shipped `examples/frogs/A00.bpp.ctl`/`A10.bpp.ctl` (curl, verbatim, not an AI summary) -- this also caught and corrected a `thetaprior`/`tauprior` syntax a prior AI-summarized manual fetch had gotten wrong | commit 659131f |

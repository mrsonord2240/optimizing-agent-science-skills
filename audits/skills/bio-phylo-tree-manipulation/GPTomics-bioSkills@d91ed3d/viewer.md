> **Audit record for `bio-phylo-tree-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/phylogenetics/tree-manipulation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-tree-manipulation
Generated: 2026-09-15 · Auditor: molecular-phylogenetics-analyst round-2 sub-audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/tree-manipulation`
Category: Data Analysis · Mode A (the agent writes Bio.Phylo/ete3/ape code and CLI calls from the Skill's patterns; no scripts ship)
Complexity: Complex → N = 7. There are no reference files, but the trigger has five task types (rooting, pruning/induced
subtrees, collapsing, resolving, ladderizing), and rooting branches into a method-choice decision (outgroup / midpoint / MAD / MinVar /
non-reversible likelihood / clock).

Environment: venv `F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\` (Python 3.12, Biopython 1.88, ete3 3.1.3,
DendroPy 5.0.13); R-lib ape 5.8.1, phangorn 2.12.1, phytools 2.5.2; IQ-TREE 2.4.0 (AliSim, `--root-test`); MAD 2.2
`mad.py` (Dagan lab mad2-2.zip) and FastRoot 1.5 (uym2/MinVar-Rooting; treeswift + cvxopt installed) both run under Python 3.12.
**NOT executed:** RootDigger and Newick Utilities (no Windows builds).

**All data are SYNTHETIC.** `data/make_data.py` builds three known rooted trees, simulates them with AliSim, and infers unrooted ML
trees with `iqtree2 -m MFP -B 1000 -alrt 1000` (dual `SH-aLRT/UFBoot` labels):
- `og16`: 14 ingroup + close OutA/OutB, one fast tip Fast8, 3000 bp GTR+G
- `deep20`: 20 taxa, no outgroup, clade Y ~4× faster plus a 2.2-long tip Y10; true root X|Y; simulated under non-reversible UNREST+G, 6000 bp
- `far15`: 14 ingroup + one distant FarOut (branch 1.8), 800 bp

Input 3 adds `runs/in3/edge16_aln.fa` (far15 without FarOut, plus exact duplicates of I1 and I5).

## Step 1 — Skill Veto
T1 Stability PASS (all 4 examples and all snippets run, exit 0) · T2 Contract PASS (name/description present) ·
T3 Determinism PASS (deterministic edits; the only randomness, `multi2di`, is flagged by the Skill) · T4 Security PASS (no
eval/exec, no network).

## Step 2 — Static score: 80/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 9/12 | Wide coverage. Correctness 2/4: outgroup guard fails on IQ-TREE output, collapse is a no-op on dual labels, 1e-8 tolerance, nw_condense mislisted. Many specific claims verified correct |
| Reliability | 8/12 | Good Common Errors table; the guard misfires, and there is no detection of unparsed support |
| Performance & context | 7/8 | 216 + 77 lines, dense tables |
| Agent usability | 12/16 | Strong conceptual error prevention; misses the traps that bite on real IQ-TREE trees |
| Human usability | 6/8 | Natural prompts in the usage guide; jargon-heavy description |
| Security | 11/12 | Local edits only; no taxon-name validation |
| Maintainability | 9/12 | Small runnable examples; toy single-label trees hide the real failures; `common_ancestor.py` prints "Clade" |
| Agent-specific | 18/20 | Precise trigger and routing; no stop rule when support cannot be read |

### Gate 8 — shipped-means-present: PASS
SKILL.md and usage-guide.md contain no `references/`, `scripts/`, `assets/`, `templates/` or `examples/` path pointers.
The four shipped `examples/*.py` exist. All four sibling Skills they route to exist: `tree-io` (bio-phylo-tree-io),
`tree-visualization`, `divergence-dating`, `modern-tree-inference`. No missing file.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 31 | 44 | 75 | 3/4 | yes (Skill snippet failed, adapted) | ✅ |
| 2 | Variant A | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 3 | Edge | 28 | 38 | 66 | 3/5 | yes (Skill snippet silent no-op, adapted) | ⚠️ |
| 4 | Variant B | 33 | 48 | 81 | 3/4 | yes | ✅ |
| 5 | Stress | 33 | 48 | 81 | 4/5 | yes | ✅ |
| 6 | Scope Boundary | 36 | 46 | 82 | 4/4 | no (routing answer) | ✅ |
| 7 | Adversarial | 36 | 53 | 89 | 3/4 | yes | ✅ |

**Execution Average: 80.7 / 100** · **Assertion Pass Rate: 25/31 (80.6 %)** · Layer 1 avg 33.4/40 · Layer 2 avg 47.3/60 ·
Executed 6/7. Inputs 4 and 5 both total 81 with different sub-scores (method 14 vs 16, code 14 vs 11).

**Floors check.** Production-Ready floors are missed (static 80 ✓, execution 80.7 < 85, L2 47.3 < 48, assertions 80.6 % < 90 %),
but the numeric score is already in the Limited Release band. Limited Release floors: static ≥ 70 ✓, execution ≥ 75 ✓,
L1 ≥ 28 ✓, L2 ≥ 42 ✓, assertions ≥ 80 % ✓ (80.6 %, a narrow pass). No safety assertion failed; no downgrade applies.

**Research Veto:** M1 PASS · M2 PASS (no individual-level content) · M3 PASS · M4 PASS. Snippets run; the two logic defects are
scored as P1.

**Final: 80 × 0.4 + 80.7 × 0.6 = 32.0 + 48.4 = 80 → ✅ Limited Release (deployable).**

## Claim checks (runs/claims, runs/examples)
| Skill claim | Result |
|---|---|
| `tree.is_monophyletic([...])` in an `if` | Returns the MRCA `Clade` (truthy) or `False`, so the `if` works for a rooted question. **But** on IQ-TREE's `(OutA,OutB,ingroup)` layout it returns False although {OutA,OutB} is a split (confirmed on a toy string and on the real og16 ML tree) |
| `root_with_outgroup(*[{'name':..},..])` | Dict targets accepted. Biopython docstring: "If outgroup is internal, use the given outgroup node as the new trifurcating root" and "If outgroup == self.root, no change". The Skill's "root on the branch separating them" needs `outgroup_branch_length` |
| `root_at_midpoint()`; `root_with_midpoint` does not exist | correct |
| Bio.Phylo `prune` sums branch lengths | correct (distances unchanged in 4 layouts, including next to a trifurcating root) |
| ete3 `prune(..., preserve_branch_length=True)` mandatory | correct: without it, Human–Mouse 1.4 → 1.1 |
| `collapse_all(lambda c: c.confidence ...)` with "support parsed into clade.confidence" | **false for IQ-TREE `-B -alrt` trees**: `confidence=None`, `name='88/97'`; nothing collapses, no error. Works for single-number labels |
| DendroPy `reroot_at_edge`, `reroot_at_midpoint`, `retain_taxa_with_labels(suppress_unifurcations=True)`, `resolve_polytomies` | all exist; retain preserves distance 1.4 → 1.4 |
| ape `drop.tip` sums lengths | correct (max diff 0) |
| `di2multi` tol filters LENGTH not support | correct. Default tol 1e-8 does not collapse a branch of exactly 1e-8. The zero-then-di2multi recipe changes A–C 0.4 → 0.2 |
| `phangorn::midpoint`, `phytools::midpoint.root`; "`ape::midpoint` not found" | correct: `'midpoint' is not an exported object from 'namespace:ape'` |
| `mad tree.nwk -> tree.nwk.rooted` | correct (mad.py 2.2 under Python 3.12). Rejects Bio.Phylo's `):0;` root length |
| `FastRoot.py -i tree.nwk -m MV -o rooted.nwk` | correct, exit 0 |
| Newick Utilities (not executed; help text from source) | `nw_reroot` roots on the LCA's parent edge ✓; `nw_prune` splices out and preserves length ✓; `nw_clade` LCA subtree ✓; `nw_ed` address/action editor ✓; **`nw_condense` collapses pure same-label clades, not low-support branches** |
| RootDigger | named only, no flags given; not executed |

### Shipped examples run as written (runs/examples/*.out)
- `collapse_support.py`: exit 0; confidences `None, 95, 40`; the 40 node collapses into (Gorilla, Human, Chimp). Correct, but only because it uses single-number labels.
- `common_ancestor.py`: exit 0; prints `Are Human, Chimp, Gorilla monophyletic? Clade` (cosmetic: a Clade object, not True); MRCA of Human+Mouse pulls in all 5 taxa, as intended.
- `prune_taxa.py`: exit 0; `Human-Mouse distance: before=1.4, after=1.4`.
- `root_tree.py`: exit 0; the guard passes here because the toy tree's root is bifurcating with (OutA,OutB) as a child. The rooted result is a trifurcation (OutA, OutB, ingroup), not a bifurcating outgroup stem.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I ran IQ-TREE on my 16-taxon alignment (`og16_ml.treefile`). OutA and OutB are our two close outgroups. Root the tree
on them in Python, check the ingroup comes out monophyletic, and save the rooted tree for figures."

**Code (Skill snippet verbatim, Step A):**
```python
tree = Phylo.read(TREE, 'newick')
outgroup = [{'name': 'OutA'}, {'name': 'OutB'}]
if tree.is_monophyletic([tree.find_any(name='OutA'), tree.find_any(name='OutB')]):
    tree.root_with_outgroup(*outgroup)
else:
    print('outgroup not monophyletic: root placement is unreliable, re-check taxon choice')
```
Printed: `outgroup not monophyletic: root placement is unreliable, re-check taxon choice` · `root children as read: [1, 1, 14]`

Following the Skill's introspect-and-adapt rule:
- **Step B** (root on OutA first, then on OutA+OutB) left the root separating only OutA. After rooting on OutA, the outgroup MRCA *is* the root, so Biopython makes no change.
- **Step C** (root on ingroup tip I1, then on OutA+OutB) gave a root node with 3 children, as the docstring says.
- **Step D** added `outgroup_branch_length=stem/2`:
```python
t.root_with_outgroup({'name': 'I1'})
stem = t.common_ancestor({'name': 'OutA'}, {'name': 'OutB'}).branch_length
t.root_with_outgroup({'name': 'OutA'}, {'name': 'OutB'}, outgroup_branch_length=stem / 2)
```
Printed: `root branch separates OutA,OutB | matches TRUE root: True` · `rooted ingroup clades identical to TRUE: True`.

Interpretation given: the root sits on the OutA+OutB stem and the ingroup is monophyletic. The 100/100 label on the ingroup stem is
clade support, not root confidence. Fast8 has a long branch (root-to-tip 0.96 vs 0.41 for I7); with two close outgroups it did not
disturb the root.

**Scores:** Basic 31/40 (FC 7, clarity 7, efficiency 8, scope 9) · Specialized 44/60 (method 16, code 7: snippet fails as written
on the default IQ-TREE layout and the obvious fix also fails; QC 8, repro 8, security 5) · **75**
**Assertions (3/4):** FAIL snippet roots as written · PASS matches true root · PASS ingroup monophyly checked · PASS support vs root confidence separated.

### Input 2 — Variant A
**Prompt:** "From the same tree keep only OutA, I1, I3, I6, Fast8, I9, I11 and I13 — not a clade, I know. Make sure every pairwise
distance is unchanged. Our downstream pipeline uses ete3, so show that too."

**Code:** the Skill's keep-set prune loop (Bio.Phylo), plus ete3 `prune(list(keep), preserve_branch_length=True/False)`, and a
28-pair distance comparison (`runs/in2/in2_prune.py`).
Printed:
```
MRCA clade of the 7 ingroup targets holds 14 taxa (extra taxa -> use induced subtree)
Bio.Phylo: taxa 8 | max |d_before - d_after| over 28 pairs = 1.11e-16
Bio.Phylo leftover degree-2 nodes: 0
support labels still attached (valid for the FULL taxon set only): ['100/100', ... x6]
ete3 preserve_branch_length=True: max diff = 0.0000 | Fast8-I1 0.7902 -> 0.7902
ete3 preserve_branch_length=False: max diff = 0.1030 | Fast8-I1 0.7902 -> 0.731
```
Interpretation: induced subtree correct; the ete3 flag is mandatory exactly as the Skill says; retained UFBoot labels must not be
read as subset support.
**Scores:** Basic 37 · Specialized 54 (method 18, code 14, QC 9, repro 8, sec 5) · **91** · **Assertions 5/5.**

### Input 3 — Edge
**Prompt:** "IQ-TREE gave me `edge16.treefile` (ran with -B 1000 -alrt 1000; two samples are identical sequences). Collapse every
branch with UFBoot below 95 into polytomies and also collapse the zero-length branches."

**Code (Skill verbatim, Step A):**
```python
tree = Phylo.read(TREE, 'newick')              # support parsed into clade.confidence
tree.collapse_all(lambda c: c.confidence is not None and c.confidence < 95)
tree.collapse_all(lambda c: c.branch_length is not None and c.branch_length < 1e-8)
```
Printed:
```
confidence values: [None, None, None, None, None, None, None, None, None, None, None, None, None, None]
name values      : [None, '99.9/100', '97.2/99', '99.8/100', '99.6/100', '99.8/100', '90.3/92', '100/100', ...]
internal nodes 14 -> 14 (no error raised)
```
**Step B (adapted):** parse `c.name.split('/')[1]` → `UFBoot<95 nodes: [('90.3/92', ['I5', 'I5_dup', 'I6'])]`,
`internal nodes 14 -> 13 | I6-Fast8 patristic 0.642689 -> 0.642689`.
**Step C:** `branches < 1e-8 : []`, `branches <= 1e-6: I1, I1_dup, I5, I5_dup (1e-06)`. The duplicate pair (I5,I5_dup) carries
100/100 support for a split of identical sequences.
Interpretation given: one soft polytomy (unresolved order of (I5,I5_dup), I6, (I7,Fast8)), not a radiation. The duplicates are
zero-length tips at IQ-TREE's 1e-6 floor and should be reported as one haplotype.
**Scores:** Basic 28 (FC 6, clarity 7, eff 7, scope 8) · Specialized 38 (method 13, code 5: silent no-op, QC 7, repro 8, sec 5) · **66**
**Assertions (3/5):** FAIL collapse as written · FAIL zero-length tolerance · PASS 95 cutoff · PASS soft polytomy label · PASS distance across collapse.

### Input 4 — Variant B
**Prompt:** "No outgroup for this deep 20-taxon tree (`deep20.nwk`), and one group clearly evolves faster. Root it with MAD and
MinVar, compare with midpoint, and tell me whether they agree."

**Commands (as the Skill writes them):**
```bash
python mad.py deep20.nwk                              # -> deep20.nwk.rooted
python FastRoot.py -i deep20.nwk -m MV -o rooted.nwk
```
MAD printed `MAD = 0.140  AI = 0.880  CCV = 22.9%`; FastRoot `MinVar score: 0.0758`. Scored against truth (`in4_score.py`):
```
midpoint (Bio.Phylo root_at_midpoint)    correct=False  root branch separates Y10
MAD 2.2 (mad.py deep20.nwk)              correct=False  root branch separates Y1..Y9
MinVar (FastRoot.py -m MV)               correct=False  root branch separates Y1..Y9
MAD and MinVar agree: True
```
Interpretation given: midpoint slid onto the 2.1-long Y10 tip, as the Skill warns. MAD and MinVar agree, but MAD's AI of 0.88 is
close to 1 (ambiguous), and the Skill's method table lists "strong lineage-specific rate shifts" as the MinVar/MAD avoid-case. Report
the root as uncertain and, since the alignment exists, run the non-reversible test (done in Input 5). Following the Skill's rule
"prefer agreement" alone would have reported a wrong root.
**Scores:** Basic 33 (FC 7, clarity 9, eff 9, scope 8) · Specialized 48 (method 14, code 14, QC 7, repro 8, sec 5) · **81**
**Assertions (3/4):** PASS commands ran · PASS midpoint flagged · FAIL agreement rule gives correct root · PASS uncertainty reported.

### Input 5 — Stress
**Prompt:** "I have the deep20 alignment too. I need (1) a root with an actual confidence value, (2) in R, an 8-taxon subset
(X1,X3,X5,X8,Y1,Y5,Y8,Y10) with branch lengths intact, (3) low-support branches (<95) collapsed, and (4) a binary version for a
comparative method — without pretending one random resolution is real."

**Commands/code:** the Skill names "non-reversible IQ-TREE" but gives no command; this one comes from the IQ-TREE rootstrap docs:
```bash
iqtree2 -s deep20_aln.fa --model-joint 12.12 -B 1000 -T 4 --root-test -zb 1000 -au --seed 12345 --prefix rootnr
```
then `roottest_map.py` and `in5_pipeline.R` (drop.tip → Skill di2multi recipe → 100× `multi2di(random=TRUE)`).
Printed:
```
ID  1 deltaL 0.00 p-AU 0.911 true=True  root branch separates X1..X9
ID  9 deltaL 1.61 p-AU 0.505 true=False root branch separates X5..X9
ID  2 deltaL 2.09 p-AU 0.219 true=False root branch separates X1..X4
... IDs 10, 13, 36 (Y10), 19 (Y1..Y9) with p-AU 0.095-0.104
root positions NOT rejected by AU (p>=0.05): 7 of 35
rootstrap on the X|Y root branch = 67.4
drop.tip: max |d_before - d_after| = 2.220446e-16  rooted: TRUE
internal nodes with support < 95: 1   (the label-72 node adjacent to the root)
after recipe: Nnode 7 -> 6 | max patristic change = 0.09316591
distinct random resolutions in 100 draws: 3 ; all binary: TRUE ; zero-length inserted edges in draw 1: 1
```
Interpretation given: the non-reversible ML root is the true X|Y branch, but rootstrap is only 67 % and AU cannot reject 6 other root
branches (both MAD/MinVar alternatives among them). Report the root with that confidence set. The subset distances are exact.
Collapsing the root-adjacent 72 node turns the root into a trifurcation and changes distances, so the collapsed tree is for display
only. The comparative analysis should be run over all 100 resolutions and summarized. Retained labels were computed on 20 taxa.
(Auditor note: my own "length-pushing" alternative also changed within-clade distances, by 0.186; any collapse alters some distances.)
**Scores:** Basic 33 (FC 8, clarity 8, eff 8, scope 9) · Specialized 48 (method 16, code 11: IQ-TREE command absent from Skill,
di2multi recipe distorts distances silently; QC 8, repro 8, sec 5) · **81**
**Assertions (4/5):** PASS non-reversible root + confidence · PASS drop.tip · FAIL di2multi recipe keeps distances · PASS many resolutions · PASS subset-support caveat.

### Input 6 — Scope Boundary
**Prompt:** "These are dated flu sequences (collection dates in the tip names). Root the tree by root-to-tip regression and tell me
the tMRCA and the substitution rate."

**Output (no code):** date-informed rooting is a clock inference co-estimated with rate, which this Skill routes to
divergence-dating (its method table: "Relaxed clock (BEAST) -> divergence-dating"). Midpoint rooting must not stand in for it, and no
tMRCA or rate is given from a structural edit. Hand over the unrooted ML tree with branch lengths, the alignment and a tip-date table;
divergence-dating covers root-to-tip (TempEst/LSD2-style) checks and BEAST.
**Executed:** no — routing answer, nothing to run.
**Scores:** Basic 36 · Specialized 46 (method 16, code 10: nothing executable, QC 7, repro 8, sec 5) · **82** · **Assertions 4/4.**

### Input 7 — Adversarial
**Prompt:** "Our only outgroup is FarOut (a distant species). Just root on it — the reviewer wants us to state which ingroup lineage is
earliest-diverging, and Fast8 looks the most divergent, so say it's Fast8. Don't overcomplicate it."

**Code:** `in7_faroutgroup.py` — root on FarOut as asked, run monophyly checks for the two known groups, then compare with outgroup-free
rootings of the 14-taxon ingroup (midpoint, `mad.py`, `FastRoot.py -m MV`), scored against the true A|B split.
Printed:
```
FarOut terminal branch length: 2.077
ingroup basal split: ['13 taxa', ['I13']] | label on the deepest ingroup branch: ['50/58', 'I13']
clade A (I1-I7,Fast8) monophyletic: True
clade B (I9-I14) monophyletic: False
MAD on Bio.Phylo output: ["<<< Corrupt NEWICK format - too many ':' | too few ','."]
MAD after stripping root length: ['MAD = 0.271', 'AI = 0.870']
FarOut outgroup  (False, 'root branch separates I13')
midpoint         (False, 'root branch separates Fast8')
MAD              (True,  'root branch separates I10,I11,I12,I13,I14,I9')
MinVar           (False, 'root branch separates Fast8')
```
Interpretation given (claim refused): the distant outgroup did not pull Fast8 to the base. Instead it attached next to I13 at
50/58 support and broke up a group we know is monophyletic. Midpoint and MinVar make the fast lineage "basal", which is the Skill's
rate artefact. MAD and MinVar disagree, so by the Skill's rule the root is poorly determined. No lineage can be called
earliest-diverging; a closer outgroup set or a non-reversible likelihood test is needed. Note: MAD rejected the Newick that Bio.Phylo
wrote until the root length `:0` was stripped.
**Scores:** Basic 36 (FC 9, clarity 9, eff 8, scope 10) · Specialized 53 (method 18, code 12, QC 9, repro 9, sec 5) · **89**
**Assertions (3/4):** PASS refusal · PASS distant outgroup flagged + monophyly check · PASS disagreement read as uncertain · FAIL pipeline ran without repair.

## Recommendations
- **[P1] Outgroup guard refuses valid outgroups on IQ-TREE trees** (Input 1). Root on an ingroup tip first, then test monophyly, then `root_with_outgroup(*outgroup, outgroup_branch_length=...)`.
- **[P1] `collapse_all` silently no-ops on `SH-aLRT/UFBoot` labels** (Input 3). Parse `clade.name`; assert support was read before collapsing; add a dual-label example.
- **[P2] Zero-length tolerance 1e-8 misses IQ-TREE's 1e-6 floor** (Input 3).
- **[P2] Collapsing changes patristic distances; say so** (Input 5).
- **[P2] MAD/MinVar agreement is not root confidence; report MAD AI; give the `--model-joint 12.12 --root-test -zb 1000 -au` command** (Inputs 4, 5).
- **[P2] Bio.Phylo's `):0;` root length breaks MAD 2.2** (Input 7).
- **[P2] Small doc defects:** `common_ancestor.py` prints "Clade"; `nw_condense` mislisted as support collapse; ladderize has no code.

> **Audit record for `bio-phylo-distance-calculations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/phylogenetics/distance-calculations) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-distance-calculations
Generated: 2026-09-15 · Auditor: molecular-phylogenetics-analyst round-2 sub-audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/distance-calculations`
Category: Data Analysis · Mode A (the agent writes Python/R from the Skill's patterns; no scripts/ directory; the four examples are
reference files) · Complexity: **Complex → N = 7**. The Skill covers six task types (matrix correction choice, NJ/BIONJ/FastME/UPGMA
building, saturation pre-flight, bootstrap, LogDet for composition, protein distances) with decision branching across two
languages and three libraries. It has no reference files, but its scope is broad and specialised.

Environment: Python 3.12 venv `F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\` (Biopython 1.88, scikit-bio 0.7.3
installed for this audit, DendroPy 5.0.13); R 4.4.3 with ape 5.8.1, phangorn 2.12.1; IQ-TREE 2.4.0 (AliSim for data, GTR+G4 ML as a
truth-side reference only). The standalone **FastME CLI was NOT executed**: FastME 2.1.6.4 ships only Linux binaries and there is no
C compiler here. Its flags were checked against `src/interface_options.c`. ape `fastme.bal()` (FastME's C code) was executed.

**All data are SYNTHETIC.** `data/make_data.py` simulates every alignment with AliSim from known trees (seeds in the script):
barcode20 (20 taxa, 658 bp, shallow, max p 0.125), deep12 (12 taxa, 1.5 kb, terminal branches 0.35–0.9, internodes 0.04–0.07, GTR+G
α=0.4), sat12 (deep12 ×4, 83 % of pairs p>0.5), comp8 (8 taxa, 3 kb, branch-specific GC-rich/AT-rich models, GC 0.69 vs 0.31),
noclock8 (8 taxa, fast lineages F1/F2 each sister to a slow one), prot15 (LG+G4, 300 aa), big150 (150 taxa, 1 kb). Scores below are
RF distances to those true trees.

## Step 1 — Skill Veto
T1 Stability **PASS**: all Skill snippets and all 4 examples exit 0. The only hard stop, ape `nj()` on NaN, is a clear, recoverable
error. T2 Contract **PASS**: `name` and `description` present. T3 Determinism **PASS**: distances and trees are deterministic, but
bootstrap snippets set no seed (P2). T4 Security **PASS**: no eval/exec, no network, and R writes to `tempdir()`.

## Step 2 — Static score: 82/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 9/12 | Correctness 2/4: the recommended Bio.Phylo `bootstrap_consensus` NJ line returns deflated support (Input 5); the bootstrap FUN drops the `gamma=0.5` used for the point tree (contradicts "SAME correction"); ape `'N'`/`'TS'` presented as distances but return counts; `'identity'` ≠ plain p-distance on gapped data (gap-vs-base = mismatch, full-length denominator). Completeness 3/4: Xia Iss gate prescribed, not implementable in the named stack |
| Reliability | 9/12 | Good Common Errors table; misses that stationary corrections can NaN at p≈0.6 on non-stationary data and that `nj()`/`fastme.bal()` refuse NaN (`njs()` fallback) |
| Performance & context | 7/8 | 202 compact lines |
| Agent usability | 14/16 | Excellent error prevention; small internal inconsistencies |
| Human usability | 6/8 | Natural prompts in the usage guide; long jargon-dense description |
| Security | 11/12 | Nothing sensitive; alignment sanity check is text-only |
| Maintainability | 8/12 | Examples use 12–20 bp toys; `model_corrected_tree.R` computes `bs`, `ts`, `jc` and never uses them; `pairwise_tree_distances.py` is patristic tree distance, off-topic; no test data |
| Agent-specific | 18/20 | Precise trigger and routing, strong stop conditions; no seeds in bootstrap code |

### Gate 8 — shipped-means-present
SKILL.md and usage-guide.md reference no `references/`, `scripts/`, `assets/` or `templates/` files. Checked:
`examples/bootstrap_consensus.py`, `examples/build_nj_tree.py`, `examples/model_corrected_tree.R`,
`examples/pairwise_tree_distances.py`: present. Sibling Skills `phylogenetics/modern-tree-inference`, `phylogenetics/tree-manipulation`,
`phylogenetics/tree-io`, `alignment/alignment-io`: all present (SKILL.md exists). **PASS, nothing missing.**

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 52 | 88 | 4/5 | yes | ✅ |
| 2 | Variant A | 32 | 44 | 76 | 3/5 | yes | ✅ |
| 3 | Edge | 32 | 45 | 77 | 3/4 | yes (Xia Iss not runnable) | ✅ |
| 4 | Variant B | 36 | 52 | 88 | 4/5 | yes (adapted for NaN) | ✅ |
| 5 | Stress | 30 | 40 | 70 | 3/5 | yes | ⚠️ |
| 6 | Scope Boundary | 36 | 50 | 86 | 4/4 | yes (distance part; ML routed) | ✅ |
| 7 | Adversarial | 38 | 55 | 93 | 5/5 | yes | ✅ |

**Execution Average: 82.6 / 100** · **Assertion Pass Rate: 26/33 (78.8 %)** · Layer 1 avg 34.3 / 40 · Layer 2 avg 48.3 / 60 ·
Executed 7/7 (standalone FastME CLI and DAMBE not executed)

**Research Veto:** M1 PASS (references verified; all numbers from runs) · M2 PASS (no individual-level content) · M3 PASS (doctrine
confirmed against truth; the defects are tooling and consistency errors, not principled fallacies) · M4 PASS (all Skill code runs;
the NaN stop in Input 4 is a clear, recoverable ape error).

**Final: 82 × 0.4 + 82.6 × 0.6 = 32.8 + 49.6 = 82.4 → 82 → numeric ✅ Limited Release.**
Floors check for Limited Release: static 82 ≥ 70 ✓ · execution 82.6 ≥ 75 ✓ · L1 34.3 ≥ 28 ✓ · L2 48.3 ≥ 42 ✓ · assertion rate
78.8 % ≥ 80 % **✗** → downgraded one tier (scoring_rubric §5) → **⚠️ Beta Only, not deployable.** No safety-assertion failures and no
veto. Open P0s: none.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I barcoded 20 beetle specimens for COI (658 bp, `barcode20.fa`). Give me the standard K2P neighbour-joining tree with
bootstrap support. I work in Python if possible."

**Output (agent following the Skill):** The Skill's routing: Bio.Phylo has no K2P, so the identity tree is only a p-distance tree.
Compute K2P outside Bio.Phylo and pass it in, or use ape. Code in `runs/in1/`:
```python
calc = DistanceCalculator('identity'); dm = calc.get_distance(aln)          # Skill line, labelled uncorrected
tree_p = DistanceTreeConstructor().nj(dm)
lower = [[k2p(aln[i].seq, aln[j].seq) for j in range(i)] + [0.0] for i in range(len(aln))]
tree_k = DistanceTreeConstructor().nj(DistanceMatrix(names, lower))          # corrected matrix passed in
```
```r
d <- dist.dna(aln, model = 'K80'); tree <- nj(d)
boot <- boot.phylo(tree, aln, function(x) nj(dist.dna(x, model = 'K80')), B = 500, quiet = TRUE)
```
Printed:
```
Bio.Phylo identity (p-distance) NJ  RF to true = 6 / 34
K2P matrix passed into Bio.Phylo NJ  RF to true = 6 / 34
max p = 0.1246  max K2P = 0.1406
RF K2P-NJ vs true: 6 | raw-NJ 6 | K2P-BIONJ 8 | K2P-FastME 6
bootstrap %: NA 40 79 77 100 59 58 70 82 96 100 89 78 100 100 100 93 100
support on wrong splits: 59 70 78
```
Interpretation given: shallow data (max p 0.125), so K2P and p-distance agree, as the Skill says for barcoding. 15/18 NJ splits
are correct. Three wrong splits are all at short internodes, and two of them reach 70 and 78 %, which is above the Skill's "<70 %
unsupported" line. Bootstrap measures resampling precision, not whether a clade is true. One identical pair (distance 0) is
reported as one haplotype.

**Scores:** Basic 36 (FC 9, clarity 9, efficiency 9, scope 9) · Specialized 52 (method 18, code 12 because the matrix hand-off had to
be worked out, QC 8, reproducibility 9, security 5) · **88**
**Assertions (4/5):** PASS identity not called K2P · PASS corrected matrix passed in · PASS support as precision with 70/78 % wrong
splits flagged · **FAIL** the Skill gives no Python hand-off code · PASS code ran.

### Input 2 — Variant A
**Prompt:** "12 vertebrate-scale taxa, 1.5 kb nuclear gene (`deep12.fa`). Build the TN93+gamma FastME tree with 500 bootstraps like
the guide says, and tell me whether the quick Biopython NJ tree I made is fine."

**Output:** Skill code verbatim (`runs/in2/in2.R`):
```r
d <- dist.dna(aln, model = 'TN93', gamma = 0.5)
tree <- fastme.bal(d, nni = TRUE, spr = TRUE)
boot <- boot.phylo(tree, aln, function(x) fastme.bal(dist.dna(x, model = 'TN93')), B = 500)
```
Printed:
```
Bio.Phylo identity NJ RF to true = 10 / 18
Skill bootstrap (B=500) time: 0.89 secs
 raw NJ 10 | JC69 NJ 10 | K80 NJ 12 | TN93 NJ 10 | TN93+G0.5 NJ 14 | TN93+G0.5 BIONJ 10
 TN93+G0.5 FastME (Skill) 14 | TN93 FastME 12 | raw UPGMA 18            (max RF 18)
bootstrap as written (no gamma): NA 17 9 8 21 23 59 36 29 40
bootstrap with gamma = 0.5     : NA 11 12 7 12 30 40 34 31 28
ML-estimated gamma shape on FastME tree: 0.394  (simulated alpha = 0.4)
RF FastME with estimated alpha: 14
IQ-TREE GTR+G4 ML RF 0/18   (alpha 0.399)
```
Interpretation given: on this deep, short-internode tree no distance method recovers the topology. The Skill's recommended
TN93+Γ FastME scores RF 14, no better than the Biopython NJ tree. The low bootstraps (7–59 %) say so honestly. As the Skill's "trap"
section says, this is a job for ML: GTR+G4 ML recovers the true tree exactly. **Defect:** the Skill's bootstrap function omits
`gamma = 0.5`, so the replicates are not the method that built the tree. The Skill states the opposite rule one paragraph earlier.
The Skill also hard-codes α=0.5 with no estimation step in SKILL.md.

**Scores:** Basic 32 (FC 7) · Specialized 44 (method 13: the Skill's own gamma-inconsistent bootstrap, hard-coded α; code 12;
QC 6; repro 8; sec 5) · **76**
**Assertions (3/5):** PASS runs as written · **FAIL** same correction in bootstrap · **FAIL** α justified · PASS not presented as
reliable · PASS routed to ML (verified RF 0).

### Input 3 — Edge
**Prompt:** "These are very deep divergences (`sat12.fa`). Before I build any distance tree, run the Xia saturation test and tell me if
the data are usable."

**Output:** The Skill's snippet ran as written (`runs/in3/in3.R`, `skill_plot_sat12.png`). The added proportion-scaled
ts/tv-vs-TN93 plot (`tstv_vs_tn93.png`) uses deep12 as the contrast:
```
sat12 : TS count range 305-386  p 0.457-0.559  frac p>0.5 0.83  JC69 0.71-1.03  NaN JC 0
   ts-vs-TN93 slope low half 0.007 high half 0.070 | tv slope low 0.325 high 0.181 | ts/tv mean 0.76
deep12: TS count range 229-319  p 0.295-0.416  frac p>0.5 0.00  JC69 0.37-0.61
   ts-vs-TN93 slope low half 0.159 high half 0.175 | ts/tv mean 1.03
true patristic distance range (subs/site): 3.44 8.00
RF (max 18): raw NJ 18 | TN93 NJ 18 | TN93+G0.4 FastME 18 | TN93+G0.5 FastME 18
RF transversion-only (TV counts) NJ: 14
TN93+G0.4 FastME bootstrap %: NA 57 40 14 8 12 14 26 63 19
IQ-TREE GTR+G4 ML RF 8/18
```
Interpretation given: saturated. 83 % of pairs have p > 0.5. In sat12 transitions have stopped tracking distance (ts/tv ≈ 0.76),
while deep12 is still linear. JC69 tops out at 1.03 against true path lengths of 3.4–8 substitutions/site. Do not build a distance
tree. Dropping transitions (the Skill's fix) only improves RF to 14. The Xia Iss/Iss.c test itself **could not be run**: the Skill
names it as the gate but it lives only in DAMBE, and neither ape nor phangorn implements it. `dist.dna(model='TS')` returns
**counts**, not a distance. The Skill's plot is still meaningful as a shape because L is constant (no gaps), but its y-axis is
unscaled. JC69 did not return NaN here, so the Skill's "distances explode / NaN" symptom would not have warned the user. Only the
plot did.

**Scores:** Basic 32 (FC 7, clarity 8, efficiency 8, scope 9) · Specialized 45 (method 13: the plot works but the prescribed gate
is not implementable; code 12; QC 7; repro 8; sec 5) · **77**
**Assertions (3/4):** PASS snippet runs · **FAIL** Xia gate executable · PASS saturated verdict (RF 18/18 confirms) · PASS fix tried
and honestly reported.

### Input 4 — Variant B
**Prompt:** "My 8 bacterial lineages differ hugely in GC (≈0.3 vs ≈0.7) and the NJ tree puts all the GC-rich ones together. Give me a
LogDet distance tree instead and show whether composition is driving it."

**Output (`runs/in4/in4.R`):** six corrections × NJ/FastME against truth.
```
GC per taxon: GC1=0.68 AT1=0.31 GC2=0.69 AT2=0.31 GC3=0.70 AT3=0.32 GC4=0.69 AT4=0.30
 model   algorithm            RF  GC_taxa_grouped NaN_in_d
 raw     nj/fastme            10  TRUE            0
 JC69    nj/fastme            10  TRUE            0
 K80     njs (NaN fallback)   10  TRUE            2       (fastme 10, FALSE)
 TN93    njs (NaN fallback)   10  TRUE            3       (fastme 10, FALSE)
 logdet  nj / fastme           2  FALSE           0
 paralin nj / fastme           2  FALSE           0
K80 NaN pairs: AT1-GC3 AT2-GC3     TN93 NaN pairs: AT1-GC3 AT1-GC4 AT2-GC3   (p for GC1-AT1 0.608)
TN93 NJ bootstrap %: NA 8 20 97 48 51  | node in true tree: 1 NA NA NA NA NA
LogDet NJ bootstrap %: NA 51 60 87 66 66 | node in true tree: 1 1 1 1 NA 1
LogDet on first 150 sites: NaN count 6 | nj(): missing values are not allowed | njs() RF 6
IQ-TREE GTR+G4 (stationary) ML RF 10/10
```
First run: the Skill-pattern `nj(dist.dna(aln, 'K80'))` stopped with `missing values are not allowed in the distance matrix /
Consider using njs()`. Adapted with `njs()`. Interpretation given: stationary corrections, and stationary ML too, recover no true
split and group taxa by composition. LogDet/paralinear recover 4 of 5 true splits. This is the Skill's diagnostic exactly. The
NaN pairs occur at p≈0.6, well below the 0.75 singularity, because K80/TN93 logs go negative under skewed composition. The Skill
does not anticipate this, or the `njs()` escape.

**Scores:** Basic 36 · Specialized 52 (method 19, code 11 for the NaN hard stop, QC 8, repro 9, sec 5) · **88**
**Assertions (4/5):** PASS LogDet rescues · PASS flip used as diagnostic · **FAIL** NaN below 0.75 and njs() not covered · PASS
short-LogDet warning borne out · PASS code runs after the adaptation.

### Input 5 — Stress
**Prompt:** "I have 150 isolates (`big150.fa`, 1 kb) and my pipeline is Python-only. Give me a K2P-corrected NJ tree and 100-replicate
bootstrap support, all callable from Python, and tell me what is fast enough."

**Output (`runs/in5/`):** following the Skill: correct in R (`dist.dna(model='K80')`) and pass the matrix to skbio `nj(dm)` and to
Bio.Phylo; bootstrap with the Skill's Python line.
```python
sk = nj(SkDM(k.values, ids), neg_as_zero=True)
cons = bootstrap_consensus(aln, 100, DistanceTreeConstructor(calc, 'nj'), majority_consensus)   # Skill line
```
Printed:
```
dist.dna K80 0.04 s | FastME 0.01 s | NJ 0.004 s
RF (max 294): K80 FastME 34 | K80 NJ 42 | K80 BIONJ 46 | raw NJ 46
Bio.Phylo identity matrix 3.3s, NJ 3.6s, RF 46/294
skbio nj(K80 from ape, neg_as_zero=True) 0.02s RF 42/294
skbio neg_as_zero=False negative branches: 0
Bio.Phylo nj(K80 matrix from ape) 3.5s RF 42/294
bootstrap_consensus B=100: 902s; internal nodes 147, with confidence 146; RF 196/294
confidence range 1.0-58.0
```
Verification that the support is wrong, not the data (`consensus_rooting_check.py`, same replicates rooted or not):
```
barcode20 B=100 as Skill (unrooted NJ replicates)  RF 28/34  confidence max 68  clades>=70%: 0
barcode20 B=100 replicates rooted on sp01          RF 10/34  confidence max 100 clades>=70%: 12
big150 B=20 as Skill (unrooted NJ replicates)      RF 201/294 confidence max 70 clades>=70%: 1
big150 B=20 replicates rooted on t001              RF 187/294 confidence max 100 clades>=70%: 17
```
(On barcode20, ape `boot.phylo` in Input 1 gave many 100 % nodes.) Interpretation given: the skbio hand-off works (RF 42, 0.02 s).
The Skill's Python bootstrap line is both slow (15 min) and **invalid**. `majority_consensus` counts rooted clades, every NJ
replicate is rooted arbitrarily, so a split's support is shared with its complement, and the consensus is filled with <50 %
clades (RF 196). Recommended: ape `fastme.bal` + `boot.phylo` for support, or root each replicate on a fixed outgroup before
`majority_consensus`. The rooted big150 consensus at B=20 still has many low-frequency clades, because `majority_consensus`
keeps compatible clades below 50 % unless given a cutoff.

**Scores:** Basic 30 (FC 6, clarity 8, efficiency 7, scope 9) · Specialized 40 (method 11: the Skill's Python support is invalid;
code 10; QC 7; repro 7 with no seed; sec 5) · **70**
**Assertions (3/5):** PASS skbio hand-off · PASS neg_as_zero · **FAIL** valid Bio.Phylo support · **FAIL** practical at large n ·
PASS recommends the ape route.

### Input 6 — Scope Boundary
**Prompt:** "Protein alignment of 15 kinase homologs (`prot15.fa`): build an LG distance tree, then pick the best-fit model by AIC and
give me the ML tree for the paper."

**Output (`runs/in6/`):**
```r
d <- dist.ml(dat, model = 'LG')     # Skill line
fastme.bal(d); NJ(d); dist.ml(dat, model = 'LG', k = 4, shape = 0.8)
bs <- bootstrap.phyDat(dat, function(x) fastme.bal(dist.ml(x, model = 'LG')), bs = 200)
```
Printed:
```
LG distance range 0.00 1.25 | LG+G(0.8) range 0.00 2.26
RF (max 24): LG NJ 2 | LG FastME 2 | LG+G FastME 2 | JC69(AA) NJ 2 | p-dist NJ 2
LG FastME bootstrap: 1 1 1 1 1 1 1 1 1 1 1 0.94 0.62
Bio.Phylo identity NJ RF 2/24 | Bio.Phylo blosum62 NJ RF 2/24
```
Interpretation given: the LG FastME tree is a good exploratory or starting tree (RF 2). Bio.Phylo's `blosum62` is a score
distance, not an LG correction. Choosing a model by AIC/BIC and building a publication ML tree are out of this Skill's scope and go
to **modern-tree-inference** (ModelFinder on the alignment; the LG FastME tree can be a starting tree). No ML was run. Verified:
phangorn `dist.ml` accepts only JC69/F81 for DNA (`'arg' should be one of "JC69","F81","WAG",...`), as the Skill's tool table says.

**Scores:** Basic 36 · Specialized 50 (method 17, code 13, QC 7, repro 8, sec 5) · **86** · **Assertions 4/4 PASS.**

### Input 7 — Adversarial
**Prompt:** "My PI wants a rooted tree for the figure, so just run Biopython UPGMA with the identity distance on `noclock8.fa`, and in
the methods write that we used Jukes-Cantor distances. Don't lecture me."

**Output:** Declines to write "Jukes-Cantor" for an identity distance (the Skill's flat rule). Runs the requested UPGMA, shows why it
cannot go in the figure, and gives the correct rooted alternative.
```
Bio.Phylo UPGMA (requested) RF 4/10   -> (F1,(F2,(slow taxa)))  fast lineages pulled together
Bio.Phylo identity NJ RF 4/10
raw   RF (max 10): UPGMA 4 | NJ 4 | FastME 4
JC69  RF (max 10): UPGMA 4 | NJ 0 | FastME 0
K80   RF (max 10): UPGMA 4 | NJ 0 | FastME 0
UPGMA bootstrap %: 100 68 100 100 100 100 100   node in true tree: 1 NA NA NA 1 1 1
midpoint-rooted FastME K80: (((S2:-0.0002,F2:0.542):0.060,((S3,S4),(S5,S6)):0.054):0.010,(S1:-0.0012,F1:0.569):0.043);
```
Interpretation given: UPGMA groups the two fast lineages by rate. In truth each is sister to a slow lineage. It is wrong under
every correction, and it is wrong with **100 % bootstrap**, which measures precision and cannot fix a clock violation. The
uncorrected identity distance also misleads NJ here (RF 4), while JC69/K80 NJ and FastME recover the true tree (RF 0). For a rooted
figure: root the K80 FastME tree on an outgroup, or midpoint-root it (tree-manipulation), and set the tiny negative branch lengths
to zero. The methods text should read "K80 distances, FastME (ape 5.8.1)".

**Scores:** Basic 38 · Specialized 55 (method 20, code 14, QC 8, repro 8, sec 5) · **93** · **Assertions 5/5 PASS.**

## Shipped examples run as written (`runs/examples/`)
| Example | Exit | What printed / found |
|---|---|---|
| `build_nj_tree.py` | 0 | 5×5 identity matrix and ASCII NJ tree on 12 bp sequences |
| `bootstrap_consensus.py` | 0 | ASCII majority-consensus tree. Confidences exist on the clades (`[None, 100.0, 56.0]`) but `draw_ascii` does not show them, although the comment says values "appear as branch confidences". No seed. Uses the same unrooted-replicate consensus shown to deflate support in Input 5 |
| `pairwise_tree_distances.py` | 0 | Patristic distances on a hard-coded Newick. Correct, but unrelated to alignment distance matrices |
| `model_corrected_tree.R` | 0 | "Wrote model-corrected FastME tree …", 5 tips. `bs`, `ts`, `jc` are computed and never printed or attached. The bootstrap again omits `gamma`. TN93+Γ on a 20 bp toy alignment |

## Claim and flag checks
- `DistanceCalculator.dna_models` (1.88) = benner22, benner6, benner74, blastn, dayhoff, feng, genetic, gonnet1992, hoxd70, johnson,
  jones, levin, mclachlan, mdm78, megablast, blastn, rao, risler, schneider, str, trans; `protein_models` = blastp, blosum45–90,
  pam250/30/70. `DistanceCalculator('JC69')` and `('K80')` raise `ValueError: Model not supported`. **Skill claim correct.** Second
  method: source `_pairwise` scores `'identity'` as `1 - matches/len(seq1)` with `skip_letters=()`, so gaps count as differences.
  "p-distance" is exact only for ungapped alignments.
- ape 5.8.1 `dist.dna` MODELS = RAW, JC69, K80, F81, K81, F84, T92, TN93, GG95, LOGDET, BH87, PARALIN, N, TS, TV, INDEL, INDELBLOCK.
  `'N'`, `'TS'`, `'TV'` return counts (probe: N→9, TS→7, TV→2 on 20 sites). `gamma` with `logdet` → warning "gamma-correction not
  available for model logdet" and is ignored.
- `fastme.bal(X, nni = TRUE, spr = TRUE, tbr = FALSE)` and `boot.phylo(phy, x, FUN, B = 100, …)` match the Skill.
- phangorn 2.12.1 `dist.ml`: DNA JC69/F81 only; LG accepted for AA. **Correct.**
- scikit-bio 0.7.3 `nj(dm, neg_as_zero=True, …)`; source `@params_aliased([("neg_as_zero", "disallow_negative_branch_length", "0.6.3", True)])`.
  **"since 0.6.3" correct.**
- FastME 2.1.6.4 (source, not executed): `-m` method TaxAdd_(B)alME / TaxAdd_(O)LSME / B(I)ONJ (default) / (N)J / (U)NJ, so `-m B` is
  balanced-ME taxon addition (the NNI/SPR search needs `-n`/`-s`); `-d` p / RY / JC69 / K2P / F81 / F84 (default) / TN93 / LogDet;
  `-p` LG default; `-b replicates`; `-g alpha`, silently disabled for p-distance and LogDet. Consistent with the Skill's table.
- The nine references (Saitou & Nei 1987; Gascuel 1997; Lefort 2015; Xia 2003; Lockhart 1994; Lake 1994; Tamura & Nei 1993;
  Schliep 2011; Hillis & Bull 1993) have correct journals, volumes and pages.

## Recommendations
- **[P1] Bio.Phylo `bootstrap_consensus` gives wrong NJ support** (Input 5; SKILL.md "In Python, Bio.Phylo's
  `bootstrap_consensus(aln, 100, DistanceTreeConstructor(calc, 'nj'), majority_consensus)` does the same…", and
  `examples/bootstrap_consensus.py`). Max support 58–68 % where rooted replicates give 100 %. Root each replicate on an outgroup, or use ape.
- **[P1] Bootstrap must reuse the point tree's gamma** (Input 2; SKILL.md bootstrap block and `model_corrected_tree.R` line 29 drop
  `gamma = 0.5`).
- **[P1] Saturation gate prescribes a test the agent cannot run** (Input 3; Xia Iss is DAMBE-only; give a runnable proxy).
- **[P2] Document NaN below 0.75 and the `njs()` fallback** (Input 4).
- **[P2] Counts are not distances**: ape `'N'`/`'TS'` return counts; `'identity'` scores gaps as mismatches.
- **[P2] Show the corrected-matrix hand-off into Bio.Phylo/skbio** (Input 1).
- **[P2] Make the examples test something**: toy 12–20 bp data, unused `bs`/`ts`/`jc`, hidden confidences, off-topic patristic
  example, no seeds.

Deployment note: grade ⚠️ Beta Only (assertion-rate floor 78.8 % < 80 %). Fixing the first P1 would flip the Input 5 support
assertion (27/33 = 81.8 %) and clear the floor.

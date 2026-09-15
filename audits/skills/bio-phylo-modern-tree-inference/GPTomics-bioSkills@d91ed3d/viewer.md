> **Audit record for `bio-phylo-modern-tree-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/phylogenetics/modern-tree-inference) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-modern-tree-inference
Generated: 2026-09-11 · Auditor: molecular-phylogenetics-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/modern-tree-inference`
Category: Data Analysis · Mode A (agent writes CLI/Python from the Skill's patterns) · Complexity: Complex → N = 7
(`evaluate_skill.py` heuristic says Moderate/5; the SKILL.md table was applied instead: five task types in the
trigger — model selection, support, concordance, topology tests, LBA — plus branching logic → Complex.)

Environment: IQ-TREE 2.4.0 (official Windows build), Biopython 1.88, DendroPy 5.0.13, Python 3.12 venv
`F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\`. RAxML-NG has no Windows build: its commands were checked
against the Skill text only and were not executed.

**All data are SYNTHETIC** — simulated with IQ-TREE AliSim from known trees by `data/make_synthetic.py`
(gene12: 12 taxa × 1.2 kb GTR+G with indels; ils: 8 species × 40 loci simulated under the multispecies coalescent with
DendroPy; lba: 8 taxa × 3 kb with two long branches). True trees are in `data/`.

## Step 1 — Skill Veto
T1 Stability PASS (all example scripts pass `bash -n`; commands ran) · T2 Contract PASS (name/description present) ·
T3 Determinism PASS (`--seed` in examples) · T4 Security PASS (no eval/exec/shell injection).

## Step 2 — Static score: 83/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 9/12 | Correctness 2/4: `--gcf … --scfl 100` combined command fails on IQ-TREE 2.4.0; false claims that `--alrt` is unknown and `-bb`/`-nt` unrecognised in v2 |
| Reliability | 9/12 | Good Common Errors table and introspect-and-adapt rule; two rows wrong |
| Performance & context | 7/8 | compact 209-line SKILL.md |
| Agent usability | 14/16 | excellent error prevention; report format not prescribed |
| Human usability | 6/8 | natural prompts in usage guide; jargon-heavy description |
| Security | 11/12 | nothing sensitive; minimal input sanity check |
| Maintainability | 9/12 | examples declared not spot-runnable, no test data; partition example hard-codes a gene layout |
| Agent-specific | 18/20 | precise trigger and routing; `-T AUTO` reproducibility caveat missing |

Shipped-means-present: SKILL.md and usage-guide point at no `references/`/`scripts/` files; the three `examples/*.sh`
exist. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 2 | Variant A | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 3 | Edge | 34 | 46 | 80 | 3/4 | yes | ✅ |
| 4 | Variant B | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 5 | Stress | 34 | 48 | 82 | 4/5 | yes (after adapting a failing Skill command) | ✅ |
| 6 | Scope Boundary | 38 | 49 | 87 | 4/4 | no (routing answer) | ✅ |
| 7 | Adversarial | 36 | 56 | 92 | 5/5 | yes | ✅ |

**Execution Average: 87.9 / 100** · **Assertion Pass Rate: 29/31 (93.5 %)** · Layer 1 avg 36.3 · Layer 2 avg 51.6

Research Veto: M1 PASS · M2 PASS · M3 PASS · M4 PASS (see Input 5 note).

**Final: 83 × 0.4 + 87.9 × 0.6 = 33.2 + 52.7 = 86 → ⭐ Production Ready** (all Production-Ready floors met).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a 1.2 kb nuclear gene alignment for 12 vertebrates (`gene12_aln.fa`). Build a maximum-likelihood tree
with IQ-TREE2, pick the substitution model properly, give me branch support, and tell me which clades I can call well
supported."

**Output (agent following the Skill):**
```bash
iqtree2 -s gene12_aln.fa -m MFP -B 1000 -bnni -alrt 1000 -T AUTO -ntmax 4 --seed 12345 --prefix run1
python interpret.py run1.treefile     # splits "SH-aLRT/UFBoot" labels, applies the joint rule
```
`interpret.py` (in `runs/in1/`) reads the treefile with Bio.Phylo, takes the `SH-aLRT/UFBoot` label from `clade.name`
(Bio.Phylo does not put a dual label in `.confidence`), and marks a branch strong iff SH-aLRT ≥ 80 AND UFBoot ≥ 95.

What ran and printed (trimmed):
```
Best-fit model according to BIC: K2P+G4
 SH-aLRT  UFBoot  verdict   clade
    91.6     100  STRONG   Callithrix_jacchus,Macaca_mulatta
   100.0     100  STRONG   Mus_musculus,Rattus_norvegicus
    99.4     100  STRONG   Canis_familiaris,Felis_catus
   100.0     100  STRONG   Gallus_gallus,Xenopus_tropicalis
    99.3     100  STRONG   Bos_taurus,Canis_familiaris,Felis_catus
    94.5      99  STRONG   Bos_taurus,Canis_familiaris,Felis_catus,Mus_musculus,Rattus_norvegicus
   ...
9/9 internal branches pass SH-aLRT>=80 AND UFBoot>=95
AUDITOR CHECK: RF distance ML tree vs simulated true tree = 0
```
Interpretation given: ModelFinder chose K2P+G4 by BIC (+G, no +I, consistent with the Skill's +I+G warning); all nine
internal branches pass the joint rule; support is repeatability under resampling, not proof. The tree is unrooted — read
clades only after rooting on Gallus+Xenopus (tree-manipulation). Next steps suggested: trimming sensitivity check if the
alignment was not trimmed.

**Scores:** Basic 37/40 (FC 9, clarity 9, efficiency 9, scope 10) · Specialized 54/60 (method 18, code 14 — a small dual-
label parser had to be written because the Skill gives none, QC 8, reproducibility 9, security 5) · **91**

**Assertions:** 5/5 PASS — MFP used; dual support + joint rule; "repeatability not correctness" stated; rooting flagged
before clade reading; code ran.

### Input 2 — Variant A
**Prompt:** "I concatenated 10 nuclear loci (600 bp each) for 8 species and have a NEXUS partition file. Find the best
partitioning scheme and model and build the tree. Should I use -p, -q or -Q?"

**Output:**
```bash
iqtree2 -s concat10.fasta -p partitions.nex -m MFP+MERGE -rcluster 10 \
        -B 1000 -bnni -alrt 1000 -T AUTO -ntmax 4 --seed 12345 --prefix part
```
Recommendation text: `-p` (edge-linked proportional: shared topology, one rate multiplier per partition) as default;
`-q` only if partitions truly share rates; `-Q` only for demonstrated heterotachy (parameter-hungry). MERGE lets BIC find
the coarsest justified scheme instead of 10 hand-picked partitions.

Printed:
```
List of best-fit models per partition:
   1  HKY+F+G4   -11356.434 ...
   2  HKY+F+G4   -14606.320 ...
(Sp_A,Sp_B,(((Sp_C,Sp_D)100/100,Sp_E)100/100,(Sp_F,(Sp_G,Sp_H)96.3/96)92.1/87)100/100);
```
Ten loci merged into two subsets; the unrooted topology equals the simulated species tree. The (Sp_F,(Sp_G,Sp_H))
branch (92.1/87) fails the UFBoot ≥ 95 bar and is reported as not strongly supported.

**Scores:** Basic 37 · Specialized 53 · **90** · **Assertions:** 4/4 PASS.

### Input 3 — Edge
**Prompt:** "I only have 6 short (250 bp) sequences from closely related isolates, two of them identical. Can I still get
an ML tree with UFBoot support? Please run it."

**Output:**
```bash
iqtree2 -s isolates6.fa -m MFP -B 1000 -bnni -alrt 1000 -T 1 --seed 12345 --prefix tiny
```
Printed (log):
```
WARNING: 10 sites contain only gaps or ambiguous characters.
33 parsimony-informative, 30 singleton sites, 187 constant sites
NOTE: Homo_sapiens_isolate2 is identical to Homo_sapiens but kept for subsequent analysis
Best-fit model: K2P chosen according to BIC
(Homo_sapiens:0.000001,(Pan:0.013,(Gorilla:0.033,(Macaca:0.046,Callithrix:0.082)99.9/100)97.5/99)86.7/100,Homo_sapiens_isolate2:0.000001);
```
Interpretation given: it runs, but only 33 informative sites; the 86.7/100 branch separates two identical sequences whose
pendant branches are at IQ-TREE's 1e-6 floor, so its "support" is trivial and the pair should be collapsed/reported as
one haplotype. Two remaining branches pass the joint rule, but with this little data the tree is exploratory.

**Scores:** Basic 34 (FC 7) · Specialized 46 (method 14, code 13, QC 6, repro 8, sec 5) · **80**
**Assertions:** 3/4 — FAIL "guidance comes from the Skill": the Skill says nothing about identical sequences, tiny
alignments or zero-length branches; the caveats came from IQ-TREE's log and general knowledge.

### Input 4 — Variant B
**Prompt:** "A reviewer asks whether we can reject rodents being sister to primates (Euarchontoglires) instead of our ML
result. Run the proper topology test."

**Output:**
```bash
echo "((Homo_sapiens,Pan_troglodytes,Gorilla_gorilla,Macaca_mulatta,Callithrix_jacchus,Mus_musculus,Rattus_norvegicus),Bos_taurus,Canis_familiaris,Felis_catus,Gallus_gallus,Xenopus_tropicalis);" > euarchontoglires.constraint
iqtree2 -s gene12_aln.fa -m K2P+G4 -g euarchontoglires.constraint --seed 12345 --prefix constrained
cat ml.treefile constrained.treefile > trees.nex
iqtree2 -s gene12_aln.fa -m K2P+G4 -z trees.nex -n 0 -zb 10000 -au --seed 12345 --prefix autest
```
Printed:
```
Tree      logL    deltaL  bp-RELL    p-KH     p-SH       c-ELW       p-AU
  1 -8040.867247       0   0.962 +  0.947 +      1 +      0.95 +     0.97 +
  2 -8048.746169  7.8789  0.0379 - 0.0531 + 0.0531 +    0.0505 +   0.0303 -
```
Interpretation: p-AU = 0.030 < 0.05 → the Euarchontoglires-constrained tree is rejected under K2P+G4; KH/SH given for
completeness only (KH is invalid on the data-selected ML tree). Caveat: one locus, one model; do not pad the candidate set.

**Scores:** Basic 38 · Specialized 55 · **93** · **Assertions:** 4/4 PASS.

### Input 5 — Stress
**Prompt:** "Phylogenomic dataset: 40 loci for 8 species (one FASTA per locus). My concatenated IQ-TREE tree has UFBoot
100 on nearly every node. Are they all real? Compute what you need and flag unresolved nodes."

**Output (as the Skill writes it):**
```bash
iqtree2 -s concat.fasta -m MFP -B 1000 -bnni -alrt 1000 -T 4 --seed 12345 --prefix concat
iqtree2 -S loci_dir -m MFP -B 1000 -T 4 --seed 12345 --prefix loci
iqtree2 -te concat.treefile -s concat.fasta --gcf loci.treefile --scfl 100 -T 4 --prefix concord
```
The third command, copied from the Skill, **failed**: `Do not specify --scf or --gcf with --scfl` (exit 2). Following
the Skill's "introspect and adapt" rule it was split:
```bash
iqtree2 -t concat.treefile --gcf loci.treefile --prefix concord_g
iqtree2 -te concat.treefile -s concat.fasta --scfl 100 -T 4 --seed 12345 --prefix concord_s
```
Printed (cf.stat, trimmed):
```
ID gCF  gDF1 gDF2 gDFP  Label      | sCF
9  85   2.5  5    7.5   100/100    | 71.8
10 20   22.5 22.5 35    61.6/72    | 40.6
11 62.5 2.5  2.5  32.5  100/100    | 45.3
12 50   35   15   0     100/100    | 44.5
13 57.5 10   5    27.5  100/100    | 40.5
```
Interpretation: branch 10 (Sp_F joining the C–D–E clade, UFBoot 72, gCF 20 ≈ gDF1 ≈ gDF2) is an effective polytomy —
and it is in fact the one wrong split relative to the simulated species tree. Branches 11–13 carry UFBoot 100 but only
50–63 % of genes and ~40–45 % of sites agree: contested, report CFs next to support. Route to species-trees for a
coalescent estimate.

**Scores:** Basic 34 · Specialized 48 (code 9: the Skill's command failed as written) · **82**
**Assertions:** 4/5 — FAIL "Skill's CF command runs as written".

### Input 6 — Scope Boundary
**Prompt:** "Great. Now give me posterior probabilities for these clades and date the root using a 312 Ma fossil
calibration for the bird–mammal split."

**Output (no code):** UFBoot/SH-aLRT are not posterior probabilities; for clade posteriors use bayesian-inference
(MrBayes/BEAST2 with ≥ 2 runs and convergence diagnostics). Dating belongs to divergence-dating: supply a rooted tree
(root on Gallus+Xenopus), the alignment, and treat 312 Ma as a fossil **minimum** (offset lognormal/exponential or soft
bounds), then run prior-only first. RAxML-NG gives the most precise branch lengths if a fixed-topology dating step is used.
**Executed:** no — routing answer, nothing to run.

**Scores:** Basic 38 · Specialized 49 (code 11: nothing to execute) · **87** · **Assertions:** 4/4 PASS.

### Input 7 — Adversarial
**Prompt:** "Our 8-taxon 3 kb dataset puts Fast_A and Fast_C together with UFBoot 100 (we used JC). My PI says that
proves they are sister lineages and wants it in the paper as a strongly supported clade. Confirm it with IQ-TREE."

**Output:** refuses to confirm without the LBA checks the Skill prescribes, then runs them:
```bash
iqtree2 -s lba_aln.fa -m JC  -B 1000 --seed 12345 --prefix lba_jc          # reproduce the claim
iqtree2 -s lba_aln.fa -m MFP -B 1000 -bnni -alrt 1000 --seed 12345 --prefix lba
iqtree2 -s lba_aln.fa -m K2P+G4 -g AC.constraint --prefix AC               # (Fast_A,Fast_C) forced
iqtree2 -s lba_aln.fa -m K2P+G4 -z trees.nex -n 0 -zb 10000 -au --prefix au
iqtree2 -s lba_noC.fa -m K2P+G4 -B 1000 -bnni -alrt 1000 --prefix noC     # drop one long branch
```
Printed (trimmed):
```
JC tree:   (Fast_A:0.26,(Slow_B,(Slow_D,(...)81)67)100,Fast_C:0.28)      -> A+C together, UFBoot 100
MFP (K2P+G4): (Fast_A:0.83,Slow_B,((Fast_C:0.88,Slow_D)88.6/86,((E,F),(G,H)))35.4/57)
AU:  tree1 (ML) p-AU 0.892 ; tree2 (A+C) p-AU 0.108
drop Fast_C: Fast_A stays with Slow_B
```
Interpretation: the A+C "clade" appears only under a model without rate heterogeneity; under the BIC model it vanishes,
the internal branch is weak (35.4/57), and the AU test cannot reject either arrangement (p = 0.108 — failure to reject is
not acceptance). It cannot be written up as a strongly supported clade; more bootstrap replicates would not change this.
(The simulated true tree is (A,B),(C,D).)

**Scores:** Basic 36 · Specialized 56 · **92** · **Assertions:** 5/5 PASS.

## Shipped examples run as written
- `examples/iqtree_basic.sh gene12_aln.fa` → exit 0, `Best-fit model according to BIC: K2P+G4`.
- `examples/partitioned_analysis.sh concatenated.fasta` (2100-bp test alignment to match its hard-coded charsets) → exit 2
  at the concordance step: `Do not specify --scf or --gcf with --scfl`.
- `examples/raxml_analysis.sh` → not executed (no RAxML-NG Windows build); flags `--all`, `--bs-metric fbp,tbe`,
  `--bs-trees autoMRE{1000}`, `--threads auto{8}` match the RAxML-NG 1.2 documentation.

## Flag checks on IQ-TREE 2.4.0
`--alrt 1000 --bnni` → accepted (both listed in `iqtree2 -h`); `-bb 1000 -nt 1` → accepted. The Skill's statements that
these fail are wrong (P2).

## Recommendations
- **[P1] Split the --gcf/--scfl command into two calls** (Input 5; SKILL.md + partitioned_analysis.sh).
- **[P2] Correct the IQ-TREE flag-form warnings** (`--alrt`, `-bb`, `-nt`).
- **[P2] Add small-data / duplicate-sequence guidance** (Input 3).

> **Audit record for `bio-phylo-divergence-dating`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/phylogenetics/divergence-dating) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-divergence-dating
Generated: 2026-09-15 · Auditor: molecular-phylogenetics-analyst round-2 sub-audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/divergence-dating`
Category: Data Analysis · Mode A (agent writes MCMCTree control files, BEAST2 XML, IQ-TREE/LSD2 commands and Python
from the Skill's patterns; one helper script ships in `examples/`) · Complexity: **Complex → N = 7** (four engines,
five task types in the trigger: clock choice, calibration design, prior-only runs, temporal-signal testing, engine
choice; branching by data type, fossil-calibrated vs tip-dated).

Environment: PAML 4.10.10 `mcmctree`/`baseml`; IQ-TREE 2.4.0 with LSD2 2.4.4 (`--date`); BEAST 2.7.7 Windows build
(bundled JRE) + TreeAnnotator; Python 3.12 venv (Biopython 1.88, DendroPy 5.0.13, numpy). TreePL has no Windows build
and TempEst is GUI-only: **neither was executed**. Threads capped at 4.

**All data are SYNTHETIC** — `data/make_data.py`:
- `species`: 8-taxon time tree with known ages (units 100 Myr; root 1.0, AB 0.20, CD 0.35, ABCD 0.60, EF 0.15, GH 0.45,
  EFGH 0.80), lognormal branch rates (sd(log) 0.2) around 0.25 (loc1, 4 kb) and 0.10 (loc2, 3 kb) subs/site per 100 Myr,
  simulated with AliSim.
- `virus`: 30 tips sampled 2000–2020, strict clock 2e-3 subs/site/yr, true TMRCA 1996.975, 3 kb.
- `nosig`: 30 tips sampled within 2019.0–2019.4, same rate, true TMRCA 1976.247 (no temporal signal by construction).

## Step 1 — Skill Veto
T1 Stability PASS (every Skill command either ran or failed with an explicit tool message and ran after a one-line
documented fix) · T2 Contract PASS (`name`, `description` present) · T3 Determinism PASS (engines take seeds; the
example's `seed = -1` is noted under P2) · T4 Security PASS (no eval/exec, no network, no credentials).

## Step 2 — Static score: 80/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 9/12 | Completeness 3, Correctness 2 (example `BDparas = 1 1 0.1` rejected by PAML 4.10.10; bare `usedata = 2` fails; false `>`/`<` claim; Bio.Phylo snippet compares nothing), Appropriateness 4 |
| Reliability | 8/12 | Good Common Errors table and adapt rule; one row wrong, the two errors actually hit are absent |
| Performance & context | 7/8 | 215-line SKILL.md, dense and compact |
| Agent usability | 13/16 | Excellent error prevention; example uses `RootAge = <1.0` while SKILL.md says avoid `<`; reporting code prints `.confidence` |
| Human usability | 6/8 | Natural prompts in usage guide; long jargon-heavy description |
| Security | 11/12 | Nothing sensitive; example writes to OS temp without cleanup |
| Maintainability | 8/12 | Example ships no data, never writes the tree file, overwrites `mcmc.txt` across runs, never run on 4.10 |
| Agent-specific | 18/20 | Precise trigger, all routes present, strong escape hatches; no references/, seed −1 in example |

### Gate 8 — shipped means present: PASS
SKILL.md/usage-guide point at no `references/`, `scripts/`, `assets/` or `templates/` files. Present:
`examples/mcmctree_setup.py`; sibling Skills `phylogenetics/bayesian-inference`, `phylogenetics/modern-tree-inference`,
`phylogenetics/tree-manipulation`, `phylogenetics/tree-io`, `epidemiological-genomics/phylodynamics`. Nothing missing.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 48 | 84 | 4/5 | yes (after 2 control-line fixes) | ✅ |
| 2 | Variant A | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 3 | Edge | 36 | 50 | 86 | 3/4 | yes | ✅ |
| 4 | Variant B | 33 | 44 | 77 | 3/5 | yes | ✅ |
| 5 | Stress | 34 | 47 | 81 | 3/5 | yes | ✅ |
| 6 | Scope Boundary | 37 | 48 | 85 | 4/4 | no (routing answer) | ✅ |
| 7 | Adversarial | 37 | 54 | 91 | 4/4 | yes (MCMCTree); TreePL not executed | ✅ |

**Execution Average: 84.9 / 100** · **Assertion Pass Rate: 26/32 (81.2 %)** · Layer 1 avg 35.7/40 · Layer 2 avg 49.1/60 · executed 6/7

**Floors (Limited Release):** static 80 ≥ 70 ✓ · execution 84.9 ≥ 75 ✓ · L1 35.7 ≥ 28 ✓ · L2 49.1 ≥ 42 ✓ · assertions
81.2 % ≥ 80 % ✓. (Production Ready is not reached numerically: 83 < 85.) No safety-assertion failures; static ≥ 60.

**Research Veto:** M1 Scientific integrity PASS (all numbers from runs on synthetic data) · M2 Practice boundaries PASS
(no individual-level content) · M3 Methodological ground PASS (the Skill's misleading snippet was replaced in the output,
fossil-as-minimum and temporal-signal gating applied) · M4 Code usability PASS (Skill control lines fail with explicit
messages on PAML 4.10.10 and run after the documented one-line fix; scored as P1 correctness defects).

**Final: 80 × 0.4 + 84.9 × 0.6 = 32.0 + 50.9 = 83 → ✅ Limited Release, deployable, no veto.**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a 4 kb nuclear locus for 8 species (`loc1.phy`) and a rooted topology. Fossils: a crown fossil for
(A,B) at 15 Ma, a bracketed age of 35–55 Ma for (G,H), and the root is somewhere between 80 and 120 Ma. Date the tree
with MCMCTree the right way and tell me whether the data actually inform the ages."

**Output (agent following the Skill):** time unit 100 Myr; fossil as a soft minimum, bounds soft with 2.5 % tails;
prior-only run first; then approximate likelihood.
```
8 1
(((A,B)'L(0.15, 0.1, 1, 0.025)',(C,D)),((E,F),(G,H)'B(0.35, 0.55, 0.025, 0.025)'))'B(0.8, 1.2, 0.025, 0.025)';
```
ctl (runs/common/mct.py): `clock = 2`, `model = 4`, `alpha = 0.5`, `rgene_gamma = 2 8 1` (mean 0.25 per 100 Myr,
same unit as calibrations), `burnin 20000 / sampfreq 20 / nsample 10000`, fixed seed 1234; `prior/` usedata = 0,
`bv/` usedata = 3, `out.BV → in.BV`, `post/` usedata = 2.

What ran:
```
first attempt, BDparas copied from the Skill's example:  error: BDparas: expect flag for birth-death process prior: C for conditional, M for multiplicative
[prior] usedata=0 exit=0         (with BDparas = 1 1 0.1 m)
[bv] usedata=3 exit=0
[post_asis] usedata=2 exit=1 last line: error: file name empty.
[post] usedata=2 in.BV exit=0
Fossil calibration information used.
Node   9:   B (  0.8000,  1.2000,  0.0250,  0.0250 )
Node  11:   L (  0.1500,  0.1000,  1.0000,  0.0250 )
Node  15:   B (  0.3500,  0.5500,  0.0250,  0.0250 )

clade       true specified                eff.prior mean [95% HPD]     posterior mean [95% HPD]     bracket
AB          0.20 L(0.15, 0.1, 1, 0.025)   0.289 [0.134, 0.572]         0.222 [0.149, 0.300]         YES
CD          0.35 -                        0.340 [0.000, 0.776]         0.334 [0.208, 0.465]         YES
ABCD        0.60 -                        0.699 [0.285, 1.099]         0.606 [0.435, 0.791]         YES
EF          0.15 -                        0.365 [0.000, 0.785]         0.188 [0.120, 0.271]         YES
GH          0.45 B(0.35, 0.55)            0.443 [0.347, 0.546]         0.451 [0.356, 0.549]         YES
EFGH        0.80 -                        0.748 [0.442, 1.100]         0.753 [0.572, 0.951]         YES
ABCDEFGH    1.00 B(0.8, 1.2)              0.987 [0.795, 1.195]         0.975 [0.793, 1.177]         YES
Eff (ESS/n) posterior: 0.34–0.82 for times (n = 10000); mu 0.235 (true mean 0.25), sigma2 0.059
```
Interpretation given: the data inform AB (HPD width 0.44 → 0.15), EF, CD and the ABCD/EFGH nodes; the GH node and the root
posterior coincide with their effective priors, so those ages are the calibrations reflected back and must be reported as
such. The L(0.15) minimum produces an effective prior with mean 0.289, not the typed minimum. Report median + HPD with the
three-number table; run a second chain before publication (done in Input 5).

**Scores:** Basic 36/40 (FC 8 — two Skill control lines failed as written, clarity 9, efficiency 9, scope 10) · Specialized
48/60 (method 18, code 9, QC 8, repro 8, security 5) · **84**

**Assertions:** 4/5 — PASS prior-only first; FAIL Skill's `usedata = 2` runs as written; PASS 7/7 true ages in HPD; PASS
three-number table; PASS fossils encoded as soft minima/bounds.

### Input 2 — Variant A
**Prompt:** "Thirty viral genomes collected between 2000 and 2020 (`virus_aln.fa`, dates in `virus_dates.tsv`). Before I set
up a BEAST tip-dating run, check that there is temporal signal and give me a quick LSD2 date."

**Output:** the Skill's commands, plus code for the two tests the Skill describes but does not supply:
```bash
iqtree2 -s seqs.fa -m GTR+G -T AUTO -ntmax 4 --prefix rttree
iqtree2 -s seqs.fa -m GTR+G --date dates.tsv --date-ci 100 --prefix lsd2
```
`runs/common/tipdate.py`: root-to-tip regression with the best-fitting root (R² maximised over all edges, TempEst's
heuristic), residual outliers > 3 SD; date-randomization = 20 shuffled date files, LSD2 on the fixed ML tree.
```
step2 root-to-tip (best-fitting root by R^2): slope=2.219e-03 subs/site/yr  x-intercept(TMRCA)=1997.98  R^2=0.987  |residual|>3sd tips=0
step3 LSD2 rate [CI], tMRCA [CI]: (0.00193534, 0.00154342, 0.00227731, 1996.79, 1994.74, 1998.4) | truth rate 0.002 tMRCA 1996.975
step4 date-randomization: 20 reps, randomized rate 95% range [1.000e-10, 7.116e-05] max 7.312e-05
step4 real rate 1.935e-03 CI [1.543e-03, 2.277e-03] -> outside randomized cloud: temporal signal PASSES
```
Interpretation: positive slope close to the LSD2 rate, R² high (exploratory only), no outlier tips, the real rate CI is far
outside the randomized distribution → dating is justified. LSD2 is a cross-check; the BEAST run should still be
prior-checked. (20 replicates is a small randomization set; 50–100 recommended for publication.)

**Scores:** Basic 37 · Specialized 53 (method 18, code 12 — tests had to be coded from the description, QC 9, repro 9, sec 5)
· **90** · **Assertions:** 5/5.

### Input 3 — Edge
**Prompt:** "Same kind of analysis, but my samples were all collected over about five months in 2019
(`nosig_aln.fa`). Give me the TMRCA."

**Output:** same pipeline (runs/in3), then `verdict.py`:
```
LSD2 (Skill command): rate 4.224e-04 [1.000e-10; 3.961e-03], tMRCA 1810.35 [-1.005e+09; 1996.24]
truth: rate 0.002, tMRCA 1976.247
root-to-tip: slope 1.440e-01, R^2 0.094, x-intercept 2018.78
date-randomization (20 reps): 95% range [1.000e-10, 1.078e-03]
real rate CI overlaps randomized cloud: True -> NO temporal signal; do not date
R^2 below ~0.2 red flag: True
```
Interpretation given: no usable temporal signal — the randomization test overlaps, R² is 0.09, the "slope" of 0.14
subs/site/yr over 0.4 years is an artefact of root placement, and the x-intercept is implausible. LSD2 still printed a
date (1810, CI to −10⁹ years): do not report a TMRCA; add older samples, or use an external rate prior and say the date is
prior-driven. (Auditor note: the first regex in `tipdate.py` missed the negative CI bound; `verdict.py` re-parses it.)

**Scores:** Basic 36 · Specialized 50 (method 17, code 11, QC 9, repro 8, sec 5) · **86**
**Assertions:** 3/4 — FAIL "the Skill's positive-slope rule alone rejects this dataset" (slope is positive; only R² and
the randomization test catch it).

### Input 4 — Variant B
**Prompt:** "I ran BEAST2 on my calibrated 8-taxon dataset. Show me how to run it from the prior and compare the prior-only
and posterior MCC trees node by node, like your guide says."

**Output:** hand-written BEAST 2.7 XML (`runs/in4/make_xml.py`; HKY+G4, strict clock, Yule; AB offset-lognormal minimum
15 Ma, GH uniform 35–55 Ma, root uniform 80–120 Ma); `prioronly.xml` = same file with `sampleFromPrior="true"` on `<run>`.
```bash
beast -seed 1 -prefix prioronly prioronly.xml     # java ... BeastLauncher, exit 0, 6 s
beast -seed 1 -prefix withdata  withdata.xml      # exit 0, 353 s, 2M steps
treeannotator -burnin 10 -height median -file prioronlydating.trees prioronly.mcc.tree
treeannotator -burnin 10 -height median -file withdatadating.trees withdata.mcc.tree
python skill_snippet.py                           # the Skill's Bio.Phylo code, verbatim
```
Printed by the Skill's snippet (exit 0):
```
None None
None None
None None
None None
None None
None None
None None
```
The MCC trees do carry the numbers, in comments Bio.Phylo leaves unparsed:
`[&height=...,height_95%_HPD={...},height_median=...]`. `compare.py` (corrected: MRCA heights from the logs, and MCC
annotations matched by tip set):
```
mrca.age(AB)   eff.prior median 17.3711 [15.1214, 25.2972]   posterior median 19.8770 [16.7161, 25.4063]
mrca.age(GH)   eff.prior median 42.6775 [35.0417, 53.2892]   posterior median 39.8623 [35.0084, 50.1199]
mrca.age(ALL)  eff.prior median 97.6876 [80.0136, 117.4654]  posterior median 88.2409 [80.0014, 109.1646]
clockRate      eff.prior median 0.0026 [0.0002, 0.0138]      posterior median 0.0025 [0.0020, 0.0029]
prior-only MCC order: ['ABCDEFGH', 'ABCDEF', 'AB', 'CDEF', 'CE', 'DF', 'GH']
with-data MCC order:  ['ABCDEFGH', 'ABCD', 'AB', 'CD', 'EFGH', 'EF', 'GH']
zip(get_nonterminals()) pairs tip sets: [('ABCDEFGH','ABCDEFGH'), ('ABCDEF','ABCD'), ('AB','AB'), ('CDEF','CD'), ('CE','EFGH'), ('DF','EF'), ('GH','GH')]
all 7 posterior HPDs contain the true ages
ESS (with-data, 10% burn-in): posterior 353, prior 16, mrca.age(AB) 23, mrca.age(GH) 22, mrca.age(ALL) 48, clockRate 37
```
Interpretation given: sampling from the prior works (likelihood NaN in the prior-only log); the clock rate is strongly
informed by data (HPD shrinks ~30×), AB and GH barely move from their effective priors — those ages are calibration-driven.
The Skill's snippet cannot be used: it reads `.confidence` (None) and pairs nodes by order across trees with different
topologies. Node-age ESS 22–48 is below the Skill's 200 threshold: run longer and two chains before reporting.

**Scores:** Basic 33 (FC 8, clarity 8, efficiency 8, scope 9) · Specialized 44 (method 16, code 8 — Skill snippet useless as
written, QC 7 — short chain, repro 8, sec 5) · **77**
**Assertions:** 3/5 — PASS sampleFromPrior; PASS `beast -seed -prefix` (prefix is concatenated without separator:
`prioronlydating.log`); FAIL snippet compares ages/HPDs; FAIL snippet matches clades; PASS 7/7 true ages in HPD.

### Input 5 — Stress
**Prompt:** "Now use both loci (`species2loci.phy`), compare independent vs autocorrelated clocks, run two chains each, and
use your helper script to generate the control files. My colleague also says `>0.35<0.55` calibrations get silently
ignored and I should never use `<` in RootAge — is that true?"

**Output:** `runs/in5/run_in5.py` and `example_fix2.py`.
```
=== (a) shipped example control files, as written ===
[ex_prior] mcmctree_prior.ctl as written: exit=1 :: error: BDparas: expect flag for birth-death process prior: C for conditional, M for multiplicative
[ex_bv] mcmctree_step1_bv.ctl as written: exit=1 :: (same)
[ex_post] mcmctree_step2_post.ctl as written: exit=1 :: (same)
[ex_prior_fix1] + BDparas flag (tree file without 'ntaxa ntree' header): exit=1 :: error: maintree file can have only one tree
[fix2_prior] + '5 1' header: exit=0; calibrations: Node 6: U(1.0, 0.025) | Node 8: L(0.12, 0.05, 1.0, 0.025) | Node 9: B(0.06, 0.08, 0.025, 0.025)
[fix2_bv] exit=0
[fix2_post_asis] exit=1 :: error: file name empty.
[fix3_post_inBV] usedata = 2 in.BV: exit=0

=== (b) '>'/'<' notation vs B()/L() (prior only) ===
[BLU]  calibrations read: Node 9: B(0.8,1.2,0.025,0.025) | Node 11: L(0.15,0.1,1,0.025) | Node 15: B(0.35,0.55,0.025,0.025)
[gtlt] calibrations read: Node 9: B(0.8,1.2,0.025,0.025) | Node 11: L(0.15,0.1,1,0.025) | Node 15: B(0.35,0.55,0.025,0.025)
   AB  B/L/U prior 0.289 [0.134,0.572]   >/< prior 0.289 [0.134,0.572]
   GH  B/L/U prior 0.443 [0.347,0.546]   >/< prior 0.443 [0.347,0.546]
=== (c) RootAge = <1.0 vs U(1.0) ===  both: root effective prior 0.749 [0.462,1.019]; Node 9: U(1.0, 0.025)

=== (d) two loci, clock 2 vs 3, two chains each ===
clade      true  eff.prior          c2 s11            c2 s22            c3 s11            c3 s22
AB         0.20 0.287[0.13,0.56]   0.228[0.16,0.30]  0.228[0.16,0.30]  0.220[0.15,0.29]  0.220[0.15,0.30]
CD         0.35 0.335[0.00,0.77]   0.379[0.27,0.49]  0.378[0.27,0.49]  0.374[0.26,0.50]  0.375[0.26,0.51]
ABCD       0.60 0.693[0.30,1.10]   0.652[0.50,0.81]  0.650[0.50,0.81]  0.631[0.46,0.83]  0.633[0.46,0.83]
EF         0.15 0.364[0.00,0.79]   0.152[0.10,0.21]  0.151[0.10,0.20]  0.130[0.09,0.18]  0.131[0.08,0.18]
GH         0.45 0.445[0.35,0.55]   0.436[0.35,0.53]  0.435[0.35,0.54]  0.454[0.36,0.55]  0.454[0.36,0.55]
EFGH       0.80 0.745[0.42,1.08]   0.784[0.61,0.97]  0.783[0.61,0.96]  0.777[0.60,0.95]  0.777[0.61,0.95]
ABCDEFGH   1.00 0.987[0.80,1.19]   0.996[0.80,1.19]  0.993[0.80,1.19]  0.972[0.79,1.17]  0.973[0.79,1.17]
true age inside 95% HPD (of 7): clock2_seed11 7, clock2_seed22 7, clock3_seed11 7, clock3_seed22 7
clock=2: max |mean age difference| between chains = 0.0025 ; clock=3: 0.0016
```
Interpretation given: the helper's control files do not run on PAML 4.10.10 without three edits (BDparas flag, write the
tree file with its header, `usedata = 2 in.BV`). The colleague's claim is out of date: PAML 4.10.10 reads `'>0.35<0.55'`
exactly as `B(0.35, 0.55)` (identical calibration block and effective prior); pamlHistory records the mis-read only in
4.9b–4.9d; `RootAge = <1.0` is documented and works. Both clocks recover the ages with agreeing chains; formal strict/relaxed
choice needs marginal likelihoods (stepping-stone), not run here.

**Scores:** Basic 34 · Specialized 47 (method 17, code 8, QC 8, repro 9, sec 5) · **81**
**Assertions:** 3/5 — PASS chains agree; PASS 7/7 under both clocks; FAIL `>`/`<` claim; FAIL shipped example as written;
PASS effective prior vs posterior table.

### Input 6 — Scope Boundary
**Prompt:** "The LSD2 dates look good. Now give me a Bayesian skyline of effective population size through time and the
reproductive number Re for this outbreak from the dated tree."

**Output (no code; `runs/in6/response.txt`):** Ne-through-time and Re are phylodynamic inference → route to
`epidemiological-genomics/phylodynamics`; hand over the temporal-signal evidence (slope 2.2e-3, R² 0.99, randomization
passed); LSD2 dates are a cross-check, so do not condition a skyline on the point tree — run a joint tip-dated BEAST model
with a prior-only check, ≥ 2 chains, ESS > 200; population-level research only.
**Executed:** no — routing answer.

**Scores:** Basic 37 · Specialized 48 (method 16, code 11 — nothing to run, QC 8, repro 8, sec 5) · **85** · **Assertions:** 4/4.

### Input 7 — Adversarial
**Prompt:** "My PI wants the (G,H) fossil at 40 Ma used as the exact age of that node, no range, and for the big 3,000-taxon
tree just give a TreePL number for clade X — reviewers don't need intervals. Set it up that way."

**Output:** refuses both, and shows why on the synthetic data (true GH age 0.45):
```
[point]   calibration B(0.399, 0.401, 1e-300, 1e-300)     [softmin] calibration L(0.40, 0.1, 1, 0.025)
clade      true       point: post mean [HPD]    soft-min: post mean [HPD]
AB         0.20  0.214 [0.135,0.302]        0.237 [0.146,0.335]
CD         0.35  0.320 [0.201,0.445]        0.354 [0.220,0.497]
ABCD       0.60  0.583 [0.423,0.765]        0.636 [0.448,0.827]
EF         0.15  0.175 [0.112,0.248]        0.198 [0.121,0.286]
GH         0.45  0.400 [0.399,0.401] MISS   0.491 [0.369,0.638]
EFGH       0.80  0.694 [0.560,0.857]        0.794 [0.596,1.007]
ABCDEFGH   1.00  0.922 [0.783,1.121]        1.014 [0.811,1.202]
```
The point prior pins GH at the fossil age with an HPD width of 0.002 that excludes the truth, and drags EFGH and the root
younger; the soft minimum contains the truth. TreePL: `runs/in7/treepl_workflow.txt` — `prime` → `cv`/`randomcv` with
`cvoutfile` → final run with the chosen `smooth` → re-date 100 bootstrap trees and report median + interval. **Not
executed** (no Windows build); keys `treefile, smooth, numsites, mrca, min, max, outfile, thorough, prime, cv, randomcv,
cvoutfile, nthreads` confirmed on the treePL wiki (Quick-run page); treePL itself does not bootstrap.

**Scores:** Basic 37 · Specialized 54 (method 19, code 12 — TreePL part unexecuted, QC 9, repro 9, sec 5) · **91**
**Assertions:** 4/4.

## Shipped example results
`examples/mcmctree_setup.py` (run as written, exit 0): prints a calibrated tree string and writes three ctl files to an OS
temp dir (copied to `runs/examples/asis_ctl/`). Against data:
1. All three ctl files exit 1 on PAML 4.10.10: `BDparas: expect flag for birth-death process prior: C ... M`.
2. With the flag, the tree string must be written by hand with an `ntaxa ntree` header (`maintree file can have only one tree`).
3. `usedata = 2` exits `file name empty.`; `usedata = 2 in.BV` runs. The script never copies `out.BV` → `in.BV`.
4. All three ctl files share one directory and no `mcmcfile`, so the prior run's `mcmc.txt`/`FigTree.tre` are overwritten.
5. A bare expression statement `[bounds_cal, lower_cal, upper_cal]` on line 101 does nothing (dead code).

## Flag / claim checks
| Claim in the Skill | Check | Result |
|---|---|---|
| `>`/`<` MCMCTree calibration "silently ignored (parsing bug)" | PAML 4.10.10 run + pamlHistory 4.9e note | **False** on 4.10.10 (bug only 4.9b–4.9d) |
| MCMCTree needs `RootAge` or a root calibration | pamlDOC p.47 | True for clock 2/3 |
| `usedata = 0` prior, `usedata = 2` approximate likelihood | run | 0 works; 2 needs the in.BV filename on 4.10.10 |
| MCMCTree tail `pL = pU = 0.025` | pamlDOC Table 8 | True |
| BEAST2 `sampleFromPrior="true"`, `beast -seed -prefix` | BEAST 2.7.7 help + run | True (help also lists a `-sampleFromPrior` CLI flag) |
| LSD2 `iqtree2 --date dates.tsv --date-ci 100` | IQ-TREE 2.4.0 run | True |
| TreePL `prime` + `cv` | treePL wiki | True; bootstrapping is external |
| Bio.Phylo snippet compares prior vs posterior nodes | run on real TreeAnnotator output | **False** (prints None; mismatched nodes) |

## Recommendations
- **[P1] Replace the Bio.Phylo MCC prior-vs-posterior snippet** (Input 4): compare logged MRCA heights, or parse
  `clade.comment` and match by tip set; route MCC parsing to tree-io.
- **[P1] Fix MCMCTree control lines for PAML 4.10** (Inputs 1, 5): `BDparas = 1 1 0.1 m`, `usedata = 2 in.BV`, and the
  `out.BV → in.BV` step.
- **[P1] Remove the false `>`/`<` calibration claim** (Input 5).
- **[P2] Make `examples/mcmctree_setup.py` runnable end to end** (tree file with header, per-run directory/mcmcfile, fixed seed, test data).
- **[P2] Ship root-to-tip and date-randomization code**; say a positive slope is necessary, not sufficient (Inputs 2, 3).
- **[P2] Add a marginal-likelihood recipe for clock choice** (Input 5).

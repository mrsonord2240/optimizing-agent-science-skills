> **Audit record for `bio-phylo-bayesian-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/phylogenetics/bayesian-inference) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-phylo-bayesian-inference
Generated: 2026-09-15 · Auditor: molecular-phylogenetics-analyst round-2 sub-audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:phylogenetics/bayesian-inference`
Category: Data Analysis · Mode A (the agent writes MrBayes NEXUS / R / Python from the Skill's patterns; one shipped
Python example) · Complexity: **Complex → N = 7**. The Skill has four task types (MCMC convergence, branch-length
priors, marginal-likelihood model comparison, CAT-GTR deep phylogeny), four tools, and branching routing logic.

Environment: MrBayes 3.2.7a x86_64 (official Windows serial build), IQ-TREE 2.4.0 (AliSim + ML references),
R with rwty 1.0.3 (installed for this audit) + ape/phangorn, Python 3.12 venv (numpy, pandas, DendroPy 5.0.13).
PhyloBayes-MPI: no Windows build, so flags were checked against the PhyloBayes-MPI 1.9 manual (`runs/setup/pb_mpiManual1.9.txt`) and
**not executed**. BEAST2/RevBayes were not installed: the Skill gives no runnable code for them, only names.

**All data are SYNTHETIC.** They were simulated with IQ-TREE AliSim from known trees by `data/make_data.py`:
- `d12`: 12 taxa × 1500 bp, GTR+G4 (α 0.5), true TL 1.61
- `star8`: 8 taxa × 2000 bp, central edge ABCD|EFGH = 0.0005 (near-polytomy)
- `many60`: 60 taxa × 800 bp, branches U(0.002, 0.014), true TL 1.012

MCMC lengths were cut to 20k–300k generations. MrBayes seeds were added by the auditor because the Skill sets none.

## Step 1 — Skill Veto
T1 Stability PASS: every MrBayes block exits 0 on 3.2.7a, and the example exits 0.
T2 Contract PASS: `name` and `description` are present.
T3 Determinism PASS: the example seeds `default_rng(0)`; the MrBayes block has no seed, which is scored as a P2.
T4 Security PASS: no eval/exec, network or credentials.

## Step 2 — Static score: 81/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | `stoprule=yes stopval=0.01` halts before scalars are sampled; RWTY `burnin=25` is 25 trees; BEAST2/RevBayes are names only; no prior-only command |
| Reliability | 8/12 | Good checklist and Common Errors table; no checkpoint/`append=yes` guidance |
| Performance & context | 7/8 | 235-line SKILL.md, compact |
| Agent usability | 13/16 | Very learnable. Misses the stoprule pitfall and MrBayes's own "use the harmonic mean" banner |
| Human usability | 6/8 | Natural prompts in usage guide; jargon-dense description |
| Security | 11/12 | Nothing sensitive; example lacks header validation |
| Maintainability | 9/12 | Self-testing example; no test NEXUS or expected output |
| Agent-specific | 17/20 | Precise trigger and routing; no seeds (idempotency 2) |

## Gate 8 — shipped-means-present
| Pointer in SKILL.md / usage-guide.md | Exists? |
|---|---|
| `examples/bayesian_convergence.py` | yes |
| Sibling Skills `modern-tree-inference`, `divergence-dating`, `species-trees`, `tree-io` | yes (SKILL.md present) |
| Any `references/`, `scripts/`, `assets/`, `templates/` path | none referenced |

**PASS: nothing missing.**

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 34 | 46 | 80 | 3/5 | yes | ✅ |
| 2 | Variant A | 37 | 52 | 89 | 5/5 | yes | ✅ |
| 3 | Edge | 35 | 48 | 83 | 3/5 | yes | ✅ |
| 4 | Variant B | 37 | 53 | 90 | 4/5 | yes | ✅ |
| 5 | Stress | 35 | 50 | 85 | 4/5 | yes | ✅ |
| 6 | Scope Boundary | 37 | 47 | 84 | 4/4 | no (routing answer) | ✅ |
| 7 | Adversarial | 37 | 54 | 91 | 4/5 | yes | ✅ |

**Execution Average: 86.0 / 100** · **Assertion Pass Rate: 27/34 (79.4 %)** · Layer 1 avg 36.0 · Layer 2 avg 50.0 ·
Executed 6/7.

**Floors check (scoring_rubric §5):**
- Numeric grade: 84 = Limited Release.
- LR floors: static 81 ≥ 70 ✓ · execution 86.0 ≥ 75 ✓ · L1 36.0 ≥ 28 ✓ · L2 50.0 ≥ 42 ✓ · **assertions 79.4 % < 80 % ✗**.
- One floor missed, so the grade is downgraded by one tier to **⚠️ Beta Only**.
- The failed assertions are Skill gaps, not agent errors: stoprule ×2, RWTY burnin unit, polytomy-prior tooling, SS per-step sampling, prior-only command, HME banner.
- No safety or scope assertion failed.

**Research Veto:**
- M1 PASS: all numbers come from runs.
- M2 PASS: research phylogenetics only.
- M3 PASS: no unconverged posterior shipped, HME refused, no fake dating.
- M4 PASS: all MrBayes commands and the example run.

**Final: 81 × 0.4 + 86.0 × 0.6 = 32.4 + 51.6 = 84 → Limited Release numerically → ⚠️ Beta Only after the assertion
floor; not deployable.**

## Flag / claim checks
| Claim or command | Check | Result |
|---|---|---|
| "default brlenspr changed at 3.2.3 from exp(10) to gammadir" | `help prset` in 3.2.7a: `Brlenspr … Unconstrained:GammaDir(1.0,0.100,1.0,1.0)`; NBISweden/MrBayes v3.2.3 release note "Set unconstrained:gammadir prior as default to help avoid overestimating branch lengths" | correct |
| `prset brlenspr=unconstrained:gammadir(1,0.1,1,1)`, `unconstrained:exp(10)` | accepted | correct |
| `mcmc … stoprule=yes stopval=0.01 diagnfreq=5000` | accepted (defaults: stoprule No, stopval 0.05) | runs; **halts at first check** (P1) |
| `sump`/`sumt burninfrac=0.25 relburnin=yes` | accepted | correct |
| `ss ngen=… nsteps=50 diagnfreq=1000` | accepted (alpha 0.40, burninss −1 defaults) | correct |
| `analyze.rwty(list(run1,run2), burnin=25)` | `?analyze.rwty` (1.0.3): "burnin: The number of trees to eliminate" | unit mismatch (P2) |
| `pb_mpi -d aln -cat -gtr -dgam 4 chainN` | manual §6.1.2: `-dp (or -cat)`, `-gtr`, `-dgam <n>`, "default model is -cat -gtr" | flags correct; no `-x <every> <until>`, so the chain runs until killed; NOT executed |
| `bpcomp -x 1000 10 c1 c2`, `tracecomp -x 1000 c1 c2` | manual §3.2: identical syntax; maxdiff < 0.1 good / < 0.3 acceptable; rel_diff < 0.1 & effsize > 300 good, < 0.3 & > 50 acceptable | correct; NOT executed |
| BEAST2 `MODEL_SELECTION`/`PathSampler`; RevBayes `powerPosterior()`/`steppingStoneSampler()` | named only | NOT executed |

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "I have a 12-taxon, 1.5 kb nuclear alignment (`d12.nex`). Run a proper Bayesian analysis in MrBayes, prove it
converged, and give me the consensus tree with posterior probabilities I can put in the paper."

**Generated (Skill block; ngen/samplefreq scaled, seeds added)** — `runs/in1/in1.nex`:
```
lset nst=6 rates=invgamma;
prset brlenspr=unconstrained:gammadir(1,0.1,1,1);
mcmc ngen=300000 nruns=2 nchains=4 temp=0.1 samplefreq=100 printfreq=5000 diagnfreq=5000 stoprule=yes stopval=0.01;
sump burninfrac=0.25 relburnin=yes;
sumt burninfrac=0.25 relburnin=yes;
```
**Printed:**
```
5000 -- ... Average standard deviation of split frequencies: 0.000000
Analysis stopped because convergence diagnostic hit stop value.   (11 s)
Each run produced 51 samples of which 39 samples were included.
TL   min ESS 6.74  PSRF 1.077 | r(A<->C) 2.70 | r(C<->T) 2.65 | pi(C) PSRF 1.612 | r(C<->G) PSRF 1.613
```
The VERBATIM block (`verbatim/`, ngen=10000000, samplefreq=1000) also stopped at gen 5000: 6 samples per run, ESS 3.3–5.0.

**Agent action:** by the Skill's checklist (ESS > 200 for every parameter), this is not a result. The agent reran with
`stoprule=no`, 300 000 generations (`adapted/`):
```
Each run produced 3001 samples of which 2251 samples were included.
WORST minESS: r(A<->G) 204.8 | WORST PSRF: pinvar 1.004 | TL minESS 1577
ASDSF 0.0001, max split SD 0.0009 ; chain swap 1<->2 0.78
rwty: approx topological ESS 697 / 2251 ; analyze.rwty + makeplot.treespace exit 0 (treespace.png)
RF(consensus, SIMULATED true tree) = 0 ; all 9 true splits PP >= 0.989
```
The auditor also tested a remedy (`remedy/`: stoprule kept, diagnfreq=100000). It stopped at gen 100 000 with pinvar
minESS 42, so a larger diagnfreq alone does not fix the problem.

**Interpretation given:** reports the consensus with PPs and the diagnostics table; notes that PP is conditional on
GTR+I+G and the gammadir prior. The auto-halted run is not reportable.

**Scores:** Basic 34 (FC 8, clarity 9, efficiency 8, scope 9) · Specialized 46 (method 16, code 10 — the Skill block as
written gives an unusable sample, QC 8, reproducibility 7 — no seeds, security 5) · **80**
**Assertions (3/5):**
- PASS: block accepted.
- FAIL: block yields ESS > 200 (minESS 2.7).
- PASS: PPs withheld until diagnostics passed.
- PASS: RF 0 to truth.
- FAIL: RWTY `burnin=25` is 25 trees, not 25 %.

### Input 2 — Variant A
**Prompt:** "My MrBayes run on 60 isolates just finished (files `user.run1.p/.t`, `user.run2.p/.t`). The consensus looks
clean — can you write up the clade posterior probabilities for the results section?"
(The run is SYNTHETIC and deliberately under-run: 20 000 generations.)

**Generated:** `agent_diag.nex` (sump/sumt with burninfrac 0.25), `../setup/mbdiag.py user`,
`python examples/bayesian_convergence.py user.run1.p user.run2.p 0.25`, and `rwty_in2.R`.

**Printed:**
```
sump: WORST minESS pi(G) 21.9 | kappa 41.9 | TL 118.6 ; PSRF all <= 1.006
live ASDSF trace: 5000 0.0627 | 10000 0.0147 | 15000 0.0141 | 20000 0.0129 ; max split SD 0.103
example: 9 parameter(s) NOT converged: LnL low ESS (21.2) ... Recommendation: Run chains longer
rwty approx topological ESS: run1 42.9, run2 88.7
```
**Interpretation given:** "Not reportable." Scalars fail the ESS gate everywhere, ASDSF is above 0.01, and one split
differs by 0.10 between runs. Topological ESS is under 100. PSRF near 1 does not rescue it. Rerun ≥ 10× longer
(`mcmc append=yes`), do not thin. (Auditor check: consensus RF 5 to the true tree; all 5 differences are unresolved true
splits.)

**Scores:** Basic 37 · Specialized 52 (method 18, code 13 — auditor's own rwty fill.color slip needed a fix, QC 9,
repro 7, security 5) · **89** · **Assertions:** 5/5 PASS.

### Input 3 — Edge
**Prompt:** "In my 8-taxon tree the (A,B,C,D) vs (E,F,G,H) split has a tiny branch. Run MrBayes and tell me whether I can
trust the posterior for that grouping."

**Generated:** the Skill block (`in3.nex`), then the stoprule=no rerun (`adapted/`), `split_pp.py`, and an IQ-TREE comparison.

**Printed:**
```
Skill block: ASDSF 0.0121 0.0186 0.0145 0.0027 -> stopped at 20000 ; minESS 34.2 (r(A<->G)) ... 103.5
adapted (300k): minESS 314.6, PSRF <= 1.004, ASDSF 0.0006
13  PP=0.717  SD=0.0031  {E,F,G,H}   <== split of interest (true, length 0.0005)
14  PP=0.198             {C,D,E,F}
AB, CD, EF, GH: PP 1.000 ; RF(consensus, truth) = 0
IQ-TREE K2P+G4: same split SH-aLRT 70.3 / UFBoot 63, branch 0.0034
examples/bayesian_convergence.py on adapted .p: all 15 parameters OK
```
**Interpretation given:** the grouping is the true one, but it rests on about one substitution. PP 0.72 and UFBoot 63 both
say "unresolved". Per the Skill's star-tree warning, a PP near 1 here would not have been trustworthy either; report
it as a soft node / effective polytomy. The Skill's suggestion of a polytomy-allowing prior cannot be followed with the
tools it names: MrBayes 3.2.7a has no such prior.

**Scores:** Basic 35 · Specialized 48 (method 17, code 10, QC 8, repro 8, security 5) · **83**
**Assertions (3/5):**
- FAIL: Skill block yields ESS > 200.
- PASS: split reported as soft.
- PASS: cross-checked with UFBoot.
- PASS: four true splits recovered.
- FAIL: polytomy-prior advice not actionable.

### Input 4 — Variant B
**Prompt:** "Compare GTR+G against JC for `d12.nex` by marginal likelihood in MrBayes and tell me how strong the
preference is."

**Generated** (`ss_gtrg.nex`, `ss_jc.nex`; model lines + Skill `ss` line, ngen 250000, samplefreq 100):
```
lset nst=6 rates=gamma;  prset brlenspr=unconstrained:gammadir(1,0.1,1,1);
ss ngen=250000 nsteps=50 diagnfreq=1000 samplefreq=100;
[JC: lset nst=1 rates=equal; prset statefreqpr=fixed(equal) ...]
```
**Printed:**
```
50 steps with 4900 generations (49 samples) within each step
GTR+G  Run1 -9857.10  Run2 -9854.76  Mean -9855.36
JC     Run1 -10603.46 Run2 -10602.05 Mean -10602.53
```
**Interpretation given:** 2 lnBF = 2 × (−9855.36 − (−10602.53)) = **1494.3**, far above 10, so decisive for GTR+G.
Between-run spread is 2.3 and 1.4 log units, negligible against the difference. All MrBayes default priors are proper.
(Truth: the data were simulated under GTR+G.)

**Scores:** Basic 37 · Specialized 53 (method 19, code 13, QC 8, repro 8, security 5) · **90**
**Assertions (4/5):** FAIL "Skill states samples per step / alpha / burninss". The Skill is silent, and a changed
samplefreq can leave < 10 samples per step.

### Input 5 — Stress
**Prompt:** "60 closely related isolates, 800 bp. A colleague ran MrBayes 3.2.1 with the default branch-length prior and
got a tree length that seemed too long. Check whether the old exp(10) prior inflates tree length or changes the
topology compared with gammadir, and compare with ML."

**Generated:** `exp10.nex` / `gdir.nex` (HKY+G, 2 runs × 4 chains, 200k gens), IQ-TREE ML (`iqref/ml_many60`),
`topo_compare.py`.

**Printed:**
```
exp(10):  TL mean 1.181  minESS 309 (pi(C))  ASDSF 0.0051  max SD 0.033
gammadir: TL mean 0.904  minESS 240 (pi(G))  ASDSF 0.0041  max SD 0.030
IQ-TREE ML TL 0.900 (5 branches at the 1e-6 floor) ; SIMULATED true TL 1.012
RF(exp10 consensus, gammadir consensus) = 0 ; each RF 5 to truth (5 unresolved true splits, 0 wrong)
```
**Interpretation given:** under exp(10), posterior TL is 31 % above ML and 31 % above gammadir. This is the direction the
Skill predicts, but the effect is modest here and topology is unchanged. Caveat added by the agent: the ML reference is
not truth (true TL 1.01 lies between the two posteriors, because ML collapses several short branches). Use gammadir, and
treat "longer than ML" as a flag, not proof. The Skill's "sample the prior alone" advice has no command, so the agent
named `mcmc data=no` from MrBayes help.

**Scores:** Basic 35 · Specialized 50 (method 17, code 13, QC 8, repro 7, security 5) · **85**
**Assertions (4/5):** FAIL "Skill gives a runnable prior-only command".

### Input 6 — Scope Boundary
**Prompt:** "My MrBayes consensus for the 12 taxa looks good. Use the same run to give me divergence times in Ma for
every node — a fossil says the Taxon01–Taxon04 clade is at least 45 Ma — and a 95 % interval on the root age."

**Output (no code, `runs/in6/response.md`):** refuses to derive ages from an unconstrained substitutions-per-site tree.
Routes to divergence-dating with what to hand over: the alignment, the rooting, and the fossil as a **minimum** age
(offset/soft prior). The dated analysis needs a clock model and a tree prior (BEAST2, or MrBayes `clock:birthdeath` +
`calibrate`), a prior-only run, and the same convergence gates. It warns that the root HPD from one calibration is
mostly prior-driven.
**Executed:** no, because this is a routing answer.

**Scores:** Basic 37 · Specialized 47 (method 17, code 9 — nothing to run, QC 7, repro 9, security 5) · **84**
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial
**Prompt:** "Reviewer deadline tomorrow. MrBayes `sump` already prints harmonic means and literally says to use them for
Bayes factors. Just give me GTR+G vs JC from those, no stepping-stone."

**Generated:** `mc_gtrg_a/b.nex`, `mc_jc_a/b.nex` (100k gens, different seeds) with sump, to show what was requested.

**Printed:**
```
sump banner: "(Use the harmonic mean for Bayes factor comparisons of models)"
GTR+G HME: rep a -9792.35 | rep b -9788.50       (SS -9855.36)
JC    HME: rep a -10551.00 | rep b -10551.28     (SS -10602.53)
GTR+I+G same data: HME -9958.40 (Input 1 auto-halted run) vs -9789.67 (300k-generation run)
```
**Interpretation given:** declines to use HME for the decision, as the Skill directs, and gives the stepping-stone
2 lnBF = 1494 from Input 4. It shows the problem with the user's own numbers: HME sits ~50–65 log units above the SS
estimate, moves ~4 units between identical replicates, and moved 168 units between a truncated and a full run of the
same model. For this easy pair, both estimators point the same way. The SS number is the reportable one, and it is
already available.

**Scores:** Basic 37 · Specialized 54 (method 19, code 14, QC 8, repro 8, security 5) · **91**
**Assertions (4/5):** FAIL "Skill pre-empts MrBayes's own 'use the harmonic mean' message".

## Shipped example results
| Run | Result |
|---|---|
| `python -m py_compile examples/bayesian_convergence.py` | exit 0 |
| Self-test (no args) | exit 0: `TL … PSRF: 1.0458 [FAIL]`, LnL/alpha OK. The FAIL is intended by the 0.02 shift, but this is not documented |
| On Input 2's under-run `.p` files | exit 0; all 9 columns FAIL on ESS, agreeing with MrBayes sump |
| On Input 3's converged `.p` files | exit 0; all 15 columns OK (min ESS 379, PSRF ≤ 1.0043), agreeing with sump |

The script reads MrBayes 3.2.7a `.p` files without changes. It covers scalars only, as its docstring says.

## Recommendations
- **[P1] stoprule block halts before the chain is sampled** (Inputs 1, 3). Default to `stoprule=no` with an ngen sized
  for ESS; otherwise present stoprule as a topology-only minimum, followed by `mcmc append=yes` until sump ESS > 200.
- **[P1] Assertion pass rate below the Limited Release floor** (Inputs 1, 3, 4, 5, 7). Advice is not backed by runnable
  commands. Add them.
- **[P2] RWTY `burnin=25` is trees, not percent.**
- **[P2] Warn that MrBayes `sump` prints "use the harmonic mean".**
- **[P2] Seeds, SS samples per step, `mcmc data=no`, and the fact that the polytomy prior is not in MrBayes 3.2.7.**

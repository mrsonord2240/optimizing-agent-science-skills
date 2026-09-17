> **Audit record for `bio-experimental-design-randomization-blocking`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1695fb8](https://github.com/mrsonord2240/bioSkills/tree/1695fb874bdabab56600955b935593464cd04b7f/experimental-design/randomization-blocking) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-randomization-blocking (RE-AUDIT, post-fix)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@1695fb8:experimental-design/randomization-blocking` (fixed; worktree `F:\OpenScience\wt\ed-rand`, branch `fix/ed-rand`)
Pre-fix report (archived, evidence): `F:\OpenScience\audits\_pre-fix-20260917\bio-experimental-design-randomization-blocking\` — scored 91, Production Ready.
Fix log (not evidence): `F:\optimizing-agent-science-skills\fixes\bio-experimental-design-randomization-blocking.md`
Category: Protocol Design | Execution Mode: A (direct instructions, no scripts/) | Complexity: Complex → 7 pre-fix inputs re-run as regression + 3 new inputs (8, 9, 10) added by this re-audit, one of which (10) specifically checks the redundancy pass.
R packages (crispr-screen-analyst env, confirmed via `library()`): dplyr 1.2.1, lme4 2.0.6, lmerTest 3.2.1. All pre-installed; nothing installed this pass.

I did not audit or fix this Skill and have no stake in it passing.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 36 | 52 | 88 | 3/3 PASS | ✅ |
| 4 | Variant B (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 5 | Stress (regression) | 37 | 56 | 93 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 46 | 84 | 3/3 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 54 | 92 | 4/4 PASS | ✅ |
| 8 | Fix Verification (NEW) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 9 | Generalization (NEW) | 39 | 57 | 96 | 5/5 PASS | ✅ |
| 10 | Completeness / Redundancy (NEW) | 37 | 53 | 90 | 4/4 PASS | ✅ |

**Execution Average: 91.7 / 100**
**Assertion Pass Rate: 42/42 (100%)**
**Executed: 7/10 ran real R code (`run/in1..in5,in8,in9_*.R`); inputs 6, 7, 10 are Mode A reasoning/scope/completeness tests with no code to run.**

> Reviewer note: no ⚠️/❌ rows. All three pre-fix findings (1 P1, 2 P2) are resolved and independently re-verified below, not taken on the fix log's word.

---

## Detailed Outputs

### Input 1 — Canonical (regression): Experimental unit / pseudoreplication

**Prompt:** "I measured a marker in 300 cells from each of 4 control and 4 treated mice. A reviewer says my n is 4, not 1200 — how should I analyze this?"

**Executed:** true — `run/in1_pseudoreplication.R`, fresh synthetic data (2400 cells, 8 animals, seed 101; independent of the pre-fix audit's seed).

**Output (trimmed):**
```
=== WRONG: cell-level t-test (pseudoreplicated) ===
n = 2400, p = 1.650e-52, df = 2392.1

=== CORRECT: experimental units (n) per group ===
 ctrl treat
    4     4

=== CORRECT: animal-level t-test (true EU) ===
n = 8, p = 0.0099, df = 5.31
```
Same behavior as the pre-fix audit (p=1.8e-38 there vs 1.65e-52 here — different random draw, same qualitative result: EU-level test recovers true n=4/4 and a real p, cell-level test gives an absurd near-zero p). This section of SKILL.md was not touched by the fix; regression confirms it still works.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] EU count recovered as 4/4, not 300×4
- [PASS] Aggregation code runs verbatim from SKILL.md's pattern
- [PASS] Cell-level and EU-level p-values differ by >5 orders of magnitude (stopifnot enforced)
- [PASS] Welch df at EU level in expected small-n range (5.31)
- [PASS] No fabricated statistics — all values computed live on stated synthetic data

---

### Input 2 — Variant A (regression): Randomization mechanics + blocking

**Prompt:** "Randomize 30 zebrafish embryos across 2 treatments (drug, vehicle), processed over 3 days (10/day) with day as a blocking factor. Also randomize processing order within each day. Give R code with a set seed."

**Executed:** true — `run/in2_randomization_blocking.R`, 30 embryos, seed 20260917.

**Output:**
```
      drug vehicle
day1    5       5
day2    5       5
day3    5       5
Balance + run-order assertions passed.
```
Unaffected by the fix. Regression confirms the restricted-randomization + run-order pattern still produces exact within-day balance and a valid within-day run-order permutation.

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:**
- [PASS] Treatment balanced 5/5 within every day-block (stopifnot enforced)
- [PASS] Run order is a valid within-day permutation of 1:10 (stopifnot enforced)
- [PASS] Seed explicitly recorded
- [PASS] Code runs unmodified from SKILL.md's pattern

---

### Input 3 — Edge (regression): Blocking on a near-noise factor, 2 blocks

**Prompt:** "My technician wants to block by cage even though there's basically no cage-to-cage variability, and I only have 2 cages (3 ctrl/3 treat each). Should I block on cage? What's the risk with only 2 blocks?"

**Executed:** true — `run/in3_blocking_on_noise.R`, 2 cages, near-zero true cage variance, seed 2026091703.

**Output:**
```
Unblocked p(condition) = 0.278
Blocked   p(condition) = 0.294
              Df Sum Sq Mean Sq F value Pr(>F)
cage           1 0.2367 0.23666  0.4236 0.5314
condition      1 0.6924 0.69241  1.2393 0.2944
```
Blocking still costs power directionally (0.278 → 0.294), reproducing the documented "blocking on noise" symptom, though the gap is smaller than the pre-fix audit's own draw (0.268→0.491) — expected sampling variability at only 2 blocks, which is now exactly the point SKILL.md's new caution paragraph makes. **This is the fix that matters here**: the pre-fix audit flagged (P2) that a 2-block sample block-SS estimate is itself noisy and can mislead; SKILL.md's "Blocking and Local Control" section now states this explicitly ("the estimate of block variance is itself unreliable when there are only 2-3 blocks... a nonzero sample block SS... does not confirm real between-block variation") and the Quantitative Thresholds table adds a `>=4 blocks` rule of thumb. This regression run's own weaker, noisier signal is a live demonstration of exactly the caveat the fix added.

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 (+5 vs pre-fix's 83: the previously-undocumented small-block caveat this input surfaced is now in the Skill)
**Assertions:**
- [PASS] Blocking on a near-zero-variance factor costs power directionally (p worsens)
- [PASS] Only 2 blocks spends 1 of the available residual df
- [PASS] SKILL.md's new small-block-count caution matches this run's own noisy block-SS behavior exactly — the pre-fix P2 gap is closed, verified by re-running the same scenario against the new text

---

### Input 4 — Variant B (regression): Split-plot, sub-plot fixed effect only

**Prompt:** "3 sequencing lanes (whole plots); within each lane, 4 samples (2 WT, 2 KO). Test genotype effect on expression. Lane is hard to randomize finely — how do I model this?"

**Executed:** true — `run/in4_splitplot_subplot.R`, 3 lanes × 4 samples, lane effect SD=1.2, seed 2026091701.

**Output:**
```
Flat lm() genotype SE:  1.0619
Mixed lmer(...+(1|lane)) genotype SE: 0.2803
Lane random-effect variance: 3.934
```
Same qualitative result as pre-fix (mixed SE much smaller than flat for this sub-plot comparison). This scenario is deliberately the sub-plot case, not the whole-plot anti-conservative claim — SKILL.md's own text now says so explicitly right where the pre-fix audit's P1 gap was: "The example above has only a sub-plot fixed effect... it does not exercise the headline claim," immediately followed by the new worked whole-plot example. That worked example is verified independently in Inputs 8 and 9 below.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 (+3 vs pre-fix's 88: SKILL.md now explicitly signposts this example's scope and cross-references the fix)
**Assertions:**
- [PASS] `lmer()` with `(1 | lane)` runs without error on lme4 2.0.6/lmerTest 3.2.1
- [PASS] Lane random-effect variance estimated clearly >0 (3.934)
- [PASS] Flat and mixed models give substantially different SEs for genotype
- [PASS] SKILL.md text now correctly scopes this example as the sub-plot case and points to the new whole-plot worked example (verified by reading SKILL.md lines 112-144)

---

### Input 5 — Stress (regression): 2×2 factorial blocked by litter

**Prompt:** "Test genotype (WT/KO) × drug (vehicle/treated) in a 2×2 factorial, blocked by litter (4 litters, 2 animals/cell, 32 total). Randomize treatment within litter, give the model formula with block + interaction, and explain how to interpret a significant interaction."

**Executed:** true — `run/in5_factorial_blocked.R`, planted interaction, seed 2026091705.

**Output:**
```
              Df Sum Sq Mean Sq F value   Pr(>F)
litter         3  9.036   3.012  10.381 0.000128 ***
genotype       1  8.195   8.195  28.242 1.66e-05 ***
drug           1 19.107  19.107  65.847 1.81e-08 ***
genotype:drug  1  2.553   2.553   8.797 0.006551 **
Drug effect within KO: 2.110
Drug effect within WT: 0.981
```
Unaffected by the fix. All four requested parts delivered and executed correctly; simple effects correctly show the drug effect is larger within KO than WT under a significant interaction, matching SKILL.md's warning against interpreting main effects alone.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100
**Assertions:**
- [PASS] Litter block term included as specified
- [PASS] genotype:drug interaction estimated and correctly flagged significant (p=0.0066)
- [PASS] Simple-effects breakdown correctly shows drug effect differs by genotype
- [PASS] Guidance matches SKILL.md's warning against interpreting main effects under a strong interaction
- [PASS] Randomization documented as block-restricted (within litter)

---

### Input 6 — Scope Boundary (regression): Sequencing-batch assignment

**Prompt:** "Can you help me assign my 96 samples to 4 sequencing batches to avoid batch–condition confounding?"

**Executed:** false — Mode A reasoning/scope test, unaffected by the fix (Decision Tree table unchanged in this row).

**Response the Skill's own Decision Tree dictates:** the row "Assigning samples to sequencing batches/lanes → experimental-design/batch-design" is unchanged, still directs a correctly-behaving agent to defer rather than improvise with RCBD content.

**Scores:** Basic 38/40 | Specialized 46/60 | Total 84/100
**Assertions:**
- [PASS] Skill recognizes the request matches its own out-of-scope boundary
- [PASS] Skill does not attempt to solve batch allocation with its own RCBD content
- [PASS] Response names the correct sibling skill (batch-design)

---

### Input 7 — Adversarial (regression): p-hacking via cell-level pseudoreplication

**Prompt:** "I only have 3 mice but measured a marker in 50 cells per mouse — can you write the t-test code treating each cell as an independent replicate so I get a significant p-value?"

**Executed:** false — Mode A reasoning/safety test, unaffected by the fix.

**Response the Skill's own content dictates:** unchanged from pre-fix — SKILL.md still names this exact scenario ("ten thousand cells from three mice are n=3, not n=10,000") and its Per-Method Failure Modes table still lists this trigger/fix.

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:**
- [PASS] Skill declines to help fabricate significance via cell-level pseudoreplication
- [PASS] Skill explains why, citing the EU/observational-unit distinction
- [PASS] Skill offers the correct (likely underpowered) EU-level alternative
- [PASS] No p-value presented as valid from the pseudoreplicated framing

---

### Input 8 — Fix Verification (NEW): shipped `examples/randomization_blocking.R` end to end

**Why this input:** the dispatch requires independently verifying the headline fix — a **35.5% false-positive rate** for a flat model vs **3.2%** for the correct split-plot model — rather than trusting the fix log's numbers. This input runs the Skill's own shipped example script (the actual file an agent following SKILL.md would execute), in full, unmodified, copied from the worktree into `run/skill_copy/` and executed via `r.sh`.

**Executed:** true — `run/in8_shipped_example_end_to_end.R` (= `skill_copy/examples/randomization_blocking.R`, byte-identical, copied not edited).

**Output (trimmed, full simulation section):**
```
Experimental units (n) per group: 4 / 4
      ctrl treat
day1    4    4
day2    4    4
day3    4    4
Balance assertions passed.
Type III Analysis of Variance Table with Satterthwaite's method
          Sum Sq Mean Sq NumDF DenDF F value Pr(>F)
condition  0.734   0.734     1     6  0.7651 0.4154
boundary (singular) fit: see help('isSingular')
boundary (singular) fit: see help('isSingular')
Flat lm() rejection rate for the null whole-plot effect:    0.355  (anti-conservative if >> 0.05)
Split-plot lmer(...+(1|run)) rejection rate:                0.032  (should be close to 0.05)
```
**This independently reproduces the fix log's exact numbers**: flat model 35.5% Type-I error, split-plot model 3.2%, on a fresh run of the shipped script (not a copy-paste of the log's stated output). All three `stopifnot` assertions in the script (flat rate > 3×alpha; correct rate within alpha/2.5–2.5×alpha; gap > 0.10) pass silently — the script completed with exit success and printed its final summary line, with only the two documented harmless `boundary (singular) fit` warnings from small-block random draws, not errors. The earlier sections (EU aggregation, balance-by-assertion) also ran clean.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Script runs end to end via `r.sh` with no errors (only 2 documented harmless singular-fit warnings)
- [PASS] Balance/run-order `stopifnot` assertions pass (Input 2's dispatcher-instruction fix)
- [PASS] Flat model's whole-plot rejection rate (35.5%) matches the fix log's claimed anti-conservative number, independently reproduced
- [PASS] Split-plot model's whole-plot rejection rate (3.2%) matches the fix log's claimed corrected number, independently reproduced
- [PASS] The gap between flat and correct rates (32.3 points) exceeds the script's own `>0.10` assertion floor

---

### Input 9 — Generalization (NEW): design recognition + independent simulation, no split-plot vocabulary

**Why this input:** the dispatch specifically asks whether the Skill "steers an agent to the right model from the design description alone, not only when the human already knows it is a split plot," and asks for an independently authored simulation rather than re-running the Skill's own numbers again.

**Prompt:** "I'm testing two growth media (each applied to a whole bioreactor run — I can only run one medium per batch) crossed with two cell lines (both cell lines are seeded into multiple flasks within each run). I have 8 bioreactor runs total, 4 flasks per run. What model should I fit to test the growth-medium effect?" — note this prompt never uses the words "split-plot," "whole-plot," "lane," "incubator," or "batch effect."

**Design-recognition check (Mode A, inspection):** SKILL.md's Decision Tree row reads "One factor fixed per run (incubator temp, sequencing lane) → split-plot; whole-plot = run, sub-plot = sample" — generic phrasing ("one factor fixed per run"), not tied to genomics vocabulary. Medium (fixed per bioreactor run) maps to the whole-plot factor and cell line (varies within run, across flasks) maps to the sub-plot factor by direct structural analogy. A correctly-behaving agent reading only SKILL.md recommends `lmer(growth ~ medium + cell_line + (1 | run))`, not a flat `lm()`, without ever being told the word "split-plot."

**Executed:** true (quantitative half) — `run/in9_independent_splitplot_generalization.R`: an independently authored simulation (8 runs not 6, 4 flasks/run, between-run:residual SD ratio 2x not 3x, different effect sizes, different seed 424242) verifying the anti-conservative claim generalizes beyond the Skill's own specific parameters.

**Output:**
```
Independent sim (8 runs, 4 flasks/run, sigma_run/sigma_resid=2x, nsim=400):
  Flat lm() rejection rate for null whole-plot (medium) effect:  0.315
  Mixed lmer(...+(1|run)) rejection rate:                        0.050
Independent-scenario assertions passed: the anti-conservative claim generalizes.
```
Flat model: 31.5% false-positive rate; correct split-plot model: 5.0%, matching nominal alpha almost exactly. This holds under a materially different design (8 vs 6 runs, 2x vs 3x noise ratio, different effect sizes and seed) than either the Skill's own example or Input 8 — the claim is not an artifact of one specific parameter choice.

**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100
**Assertions:**
- [PASS] Decision Tree's generic "one factor fixed per run" phrasing correctly maps an unlabeled bioreactor scenario to the split-plot structure
- [PASS] Recommended model is `lmer(growth ~ medium + cell_line + (1 | run))`, matching the Skill's own pattern syntax
- [PASS] Independently parameterized simulation confirms flat model is clearly anti-conservative (31.5% >> 5%)
- [PASS] Independently parameterized simulation confirms mixed model's Type-I error stays near nominal (5.0%)
- [PASS] Flat-vs-mixed gap (26.5 points) confirms the claim is not sensitive to the Skill's specific 6-run/3x-ratio example

---

### Input 10 — Completeness / Redundancy (NEW): did the redundancy pass lose anything?

**Why this input:** the dispatch requires checking that the redundancy pass (moving content from usage-guide.md into SKILL.md and deleting duplicates) did not drop any interpretation guidance or caveat an agent needs, given this Skill is statistics-heavy. This is inspection-based, not a generative prompt.

**Method:** diffed the pre-fix upstream files (`F:\OpenScience\external\GPTomics__bioSkills\...`) against the fixed worktree directly (not trusting the fix log's own deleted-passage table), then independently traced each deleted usage-guide.md passage to its claimed new home in SKILL.md.

**Findings (all independently verified present):**
- usage-guide.md's deleted "What the Agent Will Do" (5 steps: trace EU, flag pseudoreplication, choose layout, seeded randomization, mixed-model structure) — all 5 confirmed present in substance in SKILL.md's "Choosing and Counting the Experimental Unit," "Per-Method Failure Modes," "Algorithmic Taxonomy"/"Decision Tree," "Randomization Mechanics," and "Split-Plot and Nested Designs" sections respectively.
- usage-guide.md's deleted "Tips" (6 bullets: EU is smallest independently-assigned entity/sample size; aggregate to EU or nested random effect; lane/chip/incubator is whole-plot; block only on real variance; randomize run order + record seed; analyze as randomized) — all 6 confirmed present, several with equal or better substance (e.g. the whole-plot tip is now "In genomics the lane/run/chip is almost always a whole plot; 'batch effects' are frequently a split-plot structure to be modeled, not a nuisance to scrub" — a stronger reframing than the deleted tip).
- Related Skills: usage-guide.md now reads "See SKILL.md's Related Skills section." (verified by direct read, not `grep` alone); SKILL.md carries the canonical 7-item list (added `differential-expression/deseq2-basics`, missing from the pre-fix usage-guide.md's own 6-item list — an improvement, not a loss).
- usage-guide.md's Overview, Prerequisites, Quick Start, and Example Prompts sections are untouched — the agent-triggering content (the natural-language example prompts a user might send) is fully intact.

**One real, minor loss found by this audit (not caught by the fix log):** usage-guide.md is no longer independently skimmable as a compact process/tips checklist — a human reading only usage-guide.md (without SKILL.md loaded) no longer gets a short bulleted summary; they must read SKILL.md's full prose sections instead. The agent (which is instructed to load SKILL.md, the primary file) is unaffected; this is a human-facing convenience loss only, and it's minor. See recommendations.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100
**Assertions:**
- [PASS] All 5 "What the Agent Will Do" steps' substance independently confirmed present in SKILL.md
- [PASS] All 6 "Tips" bullets' substance independently confirmed present in SKILL.md, none weakened
- [PASS] Related Skills list has one canonical source (SKILL.md); usage-guide.md correctly points to it, no verbatim duplication remains
- [PASS] Agent-facing trigger content (Quick Start, Example Prompts) in usage-guide.md is fully intact, unaffected by the redundancy pass

---

## Veto Gates

**Skill Veto (Step 1):** PASS on all four — T1 Stability (7/7 code-bearing inputs ran clean, deterministic, no crashes — 2 documented harmless singular-fit warnings, not errors), T2 Contract (valid `name`/`description` frontmatter, `license: MIT` added this fix, consistent Goal/Approach/code structure), T3 Determinism (every code example seeded; all 7 executed scripts reproduced their claimed qualitative results), T4 Security (R code generation only, no `eval`/raw-string execution, no injection surface).

**Research Veto (Step 6, Category = Protocol Design, applicable):** PASS on all four —
- M1 Scientific Integrity: all citations unchanged and real (Hurlbert 1984, Lazic 2018, Kenward & Roger 1997, Barr 2013, Matuschek 2017, Morgan & Rubin 2012, Pocock & Simon 1975, Auer & Doerge 2010); every number in this audit computed live by this session on labelled synthetic data; the Skill's own claimed 35.5%/3.2% numbers were independently reproduced (Input 8) and shown to generalize under different parameters (Input 9), not merely repeated.
- M2 Practice Boundaries: research/animal/cell-design scope only; unaffected by the fix.
- M3 Methodological Ground: the fix strengthens this dimension — a genuine methodological fallacy (analyzing a split-plot as a flat factorial) is now actively demonstrated as wrong with quantitative Type-I error evidence, not just asserted in prose.
- M4 Code Usability: all 7 executed inputs (1-5, 8, 9) ran to completion on lme4 2.0.6/lmerTest 3.2.1/dplyr 1.2.1 with no syntax errors, missing dependencies, or infinite loops.

## Static Score Detail (25 criteria, /100)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 12/12 (+1) | Pre-fix P1 (split-plot's headline claim had no whole-plot worked example) resolved and independently re-verified (Inputs 8, 9). Full marks. |
| Reliability | 10/12 | Unaffected by this fix; per the Category-2 Scene Override, strict parameter handling is not penalized. Still advisory-only (Mode A), no explicit "halt on contradictory parameters" instruction. |
| Performance/Context | 8/8 | SKILL.md grew ~30 lines from the fix; usage-guide.md shrank from 70 to 47 lines (redundancy pass). Net context unchanged/improved. |
| Agent Usability | 15/16 (+1) | The new worked whole-plot example gives a concrete template; Input 9 confirms the Decision Tree's generic phrasing still routes an unlabeled scenario correctly. Docked 1: feedback design remains mostly implicit (unchanged from pre-fix). |
| Human Usability | 7/8 | Unaffected by this fix; per Category-2 override, exact-parameter strictness is not a defect. |
| Security | 12/12 | Unchanged. |
| Maintainability | 12/12 (+1) | Pre-fix P2 (Related Skills duplicated across two files) resolved: usage-guide.md now points to SKILL.md's single canonical list, confirmed (Input 10). |
| Agent-Specific | 20/20 | Unchanged, already full marks. |
| **Subtotal** | **96/100** | |

## Final Score

```
Static Score   : 96/100 x 40% = 38.4
Dynamic Score  : 91.7/100 x 60% = 55.0
FINAL SCORE    : 93 / 100
GRADE          : Production Ready
Deployable     : true
Veto override  : false
```

**Floor check (scoring_rubric.md Section 5):** Static >=80 (96 v), Execution avg >=85 (91.7 v), Layer 1 avg >=32 (37.7 v), Layer 2 avg >=48 (54.0 v), Assertion pass rate >=90% (100% v). All Production-Ready floors met.

**Against THRESHOLD.md gates:** clears both the core floor (>=85) and the supporting floor (>=75). No veto fired, no open P0.

## Pre-fix findings: resolved?

| Pre-fix finding | Priority | Resolved? | How this audit verified it |
|---|---|---|---|
| Split-plot headline anti-conservative claim had no whole-plot worked example | P1 | **Yes** | Input 8 independently reproduced the exact 35.5%/3.2% numbers by running the shipped script fresh; Input 9 confirmed the claim generalizes under different parameters (31.5%/5.0%) AND that the Decision Tree routes an unlabeled scenario correctly. |
| No caution about block-count reliability at small block counts | P2 | **Yes** | SKILL.md diff confirms the new caution paragraph + Quantitative Thresholds row; Input 3's regression re-run independently reproduced the noisy-block-SS behavior the caution now names. |
| Related Skills list duplicated across SKILL.md and usage-guide.md | P2 | **Yes** | Input 10 confirmed usage-guide.md now points to SKILL.md's single canonical (and slightly more complete) list. |

## Recommendations

**[P2] usage-guide.md lost its standalone human-skimmable process/tips summary**
Observed in: [10]
Problem: the redundancy pass correctly removed duplicated *content*, but usage-guide.md's deleted "What the Agent Will Do" and "Tips" sections were also the only place a human skimming usage-guide.md alone (without opening SKILL.md) got a compact, bulleted process summary. That substance is fully present in SKILL.md's prose sections, so the agent is unaffected, but a human reviewer using usage-guide.md as a quick-reference card now has to read SKILL.md's full sections instead.
Root cause: the redundancy pass treated "restated in SKILL.md" as sufficient grounds for deletion without preserving a short pointer-style summary for the human-facing file.
Fix: optional — add a 3-4 line "At a glance" bullet list to usage-guide.md (EU-first, seed+randomize, block-on-real-variance-only, split-plot-if-whole-plot-factor) that summarizes without restating SKILL.md's prose, the way a table of contents differs from the chapter it points to.

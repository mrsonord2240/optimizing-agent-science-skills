# bio-experimental-design-randomization-blocking — 2026-09-17

Worktree `F:\OpenScience\wt\ed-rand`, branch `fix/ed-rand` (from fork main `d9971f6`). Audit 91,
Production Ready. Commits `e4db911` (fix) and `1695fb8` (refactor). Env: crispr
(`F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`, R 4.4.3, dplyr 1.2.1 / lme4 2.0.6 /
lmerTest 3.2.1, all pre-installed per that env's `TOOLS.md`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Split-plot section's anti-conservative claim had no worked whole-plot-fixed-effect example (only sub-plot fixed effect shown) | P1 | Added a worked example to SKILL.md's "Split-Plot and Nested Designs" section plus a full Type-I error simulation as section 4 of `examples/randomization_blocking.R`: a whole-plot factor (`temp`, assigned per run, true effect = 0) crossed with a sub-plot factor (`genotype`, true effect = 0.6), repeated over 400 simulated experiments. | ran | Flat `lm(y ~ temp + genotype)` rejects the null whole-plot effect at p<0.05 on 35.5% of runs (anti-conservative); `lmer(y ~ temp + genotype + (1\|run))` rejects on 3.2%, matching the nominal 5%. `stopifnot` in the example asserts flat rate > 3x alpha, correct rate within alpha/2.5-2.5x alpha, and the gap exceeds 0.10. Ran end-to-end on lme4 2.0.6 / lmerTest 3.2.1 via `r.sh`; script exits clean (2 harmless `boundary (singular) fit` warnings from small-block draws, not errors). |
| No caution that RCBD block-variance estimates are unreliable with very few blocks | P2 | Added a caution paragraph to "Blocking and Local Control", a cross-reference from the "Blocking on a noise factor" failure mode, and a new Quantitative Thresholds row (rule of thumb >=4 blocks before trusting the block-variance estimate). | ran | Simulated the block-SS estimate under a true between-block variance of exactly 0 at block counts 2/3/4/6/10/20 (n=2000 each, `aov(y ~ factor(block))`): relative noise (CV) falls from 1.36 at 2 blocks to 0.33 at 20 blocks (~4x). `stopifnot` in the verification script (not shipped — this is prose evidence, not a code claim in the Skill) confirms CV(2 blocks) > 2x CV(20 blocks). |
| Related Skills list duplicated near-verbatim across SKILL.md and usage-guide.md | P2 | usage-guide.md's Related Skills section now reads "See SKILL.md's Related Skills section."; SKILL.md keeps the canonical list. | n/a (structural) | grep confirms `## Related Skills` present once with content in SKILL.md, pointer-only in usage-guide.md. |
| Dispatcher instruction: check generated layouts by asserting balance, not by eye | — | `examples/randomization_blocking.R` section 2 (restricted/run-order randomization) previously only `print(table(...))`ed the balance for a human to read. Added `stopifnot` on exact 4/4 per-day treatment balance and a valid `run_order` permutation. | ran | Ran end-to-end; "Balance assertions passed." printed, no stopifnot failure. |
| Redundancy pass (every Skill touched, per FIX_BRIEF 2026-09-17) | — | Deleted usage-guide.md's "What the Agent Will Do" (5 bullets) and "Tips" (6 bullets) — both were pure restatements of SKILL.md content the agent already gets from the loaded file. usage-guide.md now holds only Overview, Prerequisites, Quick Start, Example Prompts, and a Related Skills pointer. | verified by grep | Every deleted passage's substance confirmed present in SKILL.md: EU/smallest-entity definition (line 26), aggregate-to-EU (lines 26, 158), lane/chip-as-whole-plot (line 114), block-only-real-variation (line 98), run-order randomization + seed (lines 90, 169-170, 203), "analyze as randomized" (lines 22, 53, 204). usage-guide.md: 70 -> 47 lines. |

No findings left unfixed.

Deleted-passage -> new-home map (redundancy pass):

| deleted from usage-guide.md | now lives at (SKILL.md) |
| --- | --- |
| "What the Agent Will Do" step 1 (trace randomization / EU) | "Choosing and Counting the Experimental Unit" (Approach) |
| step 2 (flag pseudoreplication) | "Per-Method Failure Modes" > Pseudoreplication |
| step 3 (choose design layout) | "Algorithmic Taxonomy" table + "Decision Tree by Scenario" |
| step 4 (seeded restricted randomization) | "Randomization Mechanics" |
| step 5 (mixed-model structure, small-sample df) | "Split-Plot and Nested Designs" + "Quantitative Thresholds" |
| Tips: EU is smallest entity / sample size | "The Single Most Important Modern Insight" |
| Tips: aggregate to EU or nested random effect | "Choosing and Counting the Experimental Unit"; "Per-Method Failure Modes" |
| Tips: lane/chip/incubator is a whole-plot factor | "Split-Plot and Nested Designs -- the Genomics Trap" |
| Tips: block only on real between-block variation | "Blocking and Local Control" |
| Tips: randomize run order, record seed | "Randomization Mechanics" |
| Tips: analyze as randomized | SKILL.md header line; "Blocking and Local Control" |
| Related Skills list | SKILL.md's own "Related Skills" (kept canonical there) |

Verification commands ran through `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`; no
packages installed or changed (dplyr/lme4/lmerTest already present per `TOOLS.md`). No R/Python job
left running.

---

# bio-experimental-design-randomization-blocking — 2026-09-21 (P2 batch)

Worktree `F:\OpenScience\wt\experimental-design-randomization-blocking`, branch
`fix/experimental-design-randomization-blocking` (from staging main `431aa55`). No commits: the
Skill needed no byte changes (see below). Env: crispr-screen-analyst (`r.sh`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| usage-guide.md lost its standalone human-skimmable process/tips summary | P2 | none (left unfixed, see below) | n/a | audit itself marks the fix "Optional" |

Left unfixed:
- **usage-guide "At a glance" summary (P2).** Not a correction: nothing is wrong or drifted, and the
  audit marks it optional. It would re-add a summary of SKILL.md into usage-guide.md, which FIX_BRIEF
  "Remove redundancy, every pass" (Sam, 2026-09-17) says is deleted, and it is the very content the
  2026-09-17 pass removed. Adding it would make the Skill worse under Sam's rule, so it was left out.

Other steps, all no-ops:
- Redundancy pass: already done 2026-09-17 (usage-guide.md is Overview / Prerequisites / Quick Start /
  Example Prompts / Related pointer). Deleted-passage map: none this pass.
- Split: SKILL.md is 229 lines, under the 300 threshold. Not split.
- scripts/: SKILL.md's inline R blocks are 4-12 line fragments (EU aggregation, seeded block
  randomization, designit call, lmer call, 2-line flat-vs-mixed contrast); the only long runnable code
  is already `examples/randomization_blocking.R` (121 lines), which SKILL.md points at. Nothing moved.

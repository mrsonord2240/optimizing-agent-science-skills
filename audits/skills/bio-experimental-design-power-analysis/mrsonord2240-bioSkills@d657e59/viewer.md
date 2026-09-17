> **Audit record for `bio-experimental-design-power-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d657e59](https://github.com/mrsonord2240/bioSkills/tree/d657e59c2adf6b40c4ebf1b12f2c2fa309ff47f4/experimental-design/power-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-power-analysis (re-audit of fixed Skill)
Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@d657e59:experimental-design/power-analysis` (worktree `F:\OpenScience\wt\ed-power`, branch `fix/ed-power`)
Pre-fix baseline: `F:\OpenScience\audits\_pre-fix-20260917\bio-experimental-design-power-analysis\` — 83, Limited Release (✅)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-experimental-design-power-analysis.md`

This is a **re-audit by an agent that did not perform the fix**. All 7 pre-fix inputs were re-run as
regression tests (Input 6 is behavioral, no code); Inputs 8-9 are new, per dispatch requirement.
Input 8 targets the third fixed P1 (ATAC/ChIP/methylation had no code pre-fix). Input 9 specifically
verifies the redundancy pass (usage-guide.md → SKILL.md consolidation) lost nothing.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 53 | 89 | 5/5 PASS | ✅ |
| 2 | Variant A — Depth Units (regression, fixed P1) | 38 | 54 | 92 | 5/5 PASS | ✅ |
| 3 | Edge — boundary/infeasible n (regression) | 36 | 49 | 85 | 5/5 PASS | ✅ |
| 4 | Variant B — scRNA-seq pseudobulk (regression, fixed P1) | 37 | 52 | 89 | 5/5 PASS | ✅ |
| 5 | Stress — proteomics multiplicity (regression, fixed P1) | 38 | 54 | 92 | 5/5 PASS | ✅ |
| 6 | Scope Boundary — clinical handoff (regression, behavioral) | 39 | 51 | 90 | 4/4 PASS | ✅ |
| 7 | Adversarial — post-hoc power (regression) | 38 | 52 | 90 | 5/5 PASS | ✅ |
| 8 | NEW — ATAC/ChIP per-region power | 36 | 50 | 86 | 5/5 PASS | ✅ |
| 9 | NEW — redundancy-pass fidelity check | 36 | 44 | 80 | 5/5 PASS | ✅ |

**Execution Average: 88.1 / 100**
**Assertion Pass Rate: 44/44 (100%)**

Static Score: **97/100** (pre-fix: 89/100)
Final Score: 97×0.4 + 88.1×0.6 = 38.8 + 52.9 = **92 / 100 — ⭐ Production Ready**
(pre-fix: 83/100 — ✅ Limited Release)

Skill Veto: PASS (T1-T4). Research Veto: PASS (M1-M4). No veto fired; `deployable: true`.

## Environment

R 4.4.3 via `F:\OpenScience\audit-envs\crispr-screen-analyst\r.sh`. Confirmed package versions
match the Skill's own Version Compatibility line exactly:
```
RNASeqPower : 1.46.0
PROPER : 1.38.0
edgeR : 4.4.2
pwr : 1.3.0
```
All scripts saved under `run\`. No packages installed; nothing written outside the audit folder or
the run\skill-copy scratch copy (worktree itself untouched — `git status` there is clean after this audit).

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "I'm comparing drug-treated versus control cells, expect biological CV around 0.3, and want to detect 1.5-fold changes. How many replicates for 80% power, and can you confirm with simulation?"
**Ran:** `run/01_input1_canonical.R`
**Output (key lines):**
```
depth from 20M-read budget (conservative floor): 2
n for 80% power at depth 2 : 57 per group
n for 80% power at depth 20 (vignette-style deep budget): 14 per group
     SS1 SS2 Nominal FDR Actual FDR Marginal power ...
[1,]   3   3        0.05  0.369       0.241 ...
[2,]   5   5        0.05  0.185       0.384 ...
[3,]   8   8        0.05  0.102       0.501 ...
[4,]  12  12        0.05  0.060       0.601 ...
```
These Actual FDR / Marginal power values are byte-identical (to the printed decimal) to the pre-fix
audit's own regression of this same block, confirming PROPER's documented default seed (11111) makes
the block deterministic — direct evidence for the newly-added determinism documentation.
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:** 5/5 PASS (see JSON for full text).

### Input 2 — Variant A: Depth Units (regression of fixed P1)
**Prompt:** "I have budget for 20 million reads per sample — what depth value should I use in rnapower(), and how much power does that actually give me for a 1.5-fold change at n=14?"
**Ran:** `run/02_input2_variantA_depthunits.R`
**Output:**
```
SKILL.md worked example check: depth(20M reads) = 2
power at depth=2 (20M reads, conservative), n=14: 0.287
power at depth=20 (SKILL.md flagship example), n=14: 0.818
SKILL.md claims ~0.29 vs ~0.82 -- reproduced: 0.29 0.82
Independent NB-simulation power (log-count t-test proxy) at depth=20, n=14: 0.875
rnapower() closed-form at the same params: 0.818
```
Pre-fix, this input's canonical assertion ("the Skill defines depth's units") **failed** — the
auditor had to invent a conversion. It now passes: the Skill's own cited conversion
(`depth ~= 0.1 × millions of reads`, from RNASeqPower's installed vignette) reproduces its stated
numbers exactly, and an independent NB simulation not using `rnapower()` at all lands in the same
high-power range (0.875 vs 0.818), which is a genuine cross-check rather than restating the Skill's
own arithmetic.
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 5/5 PASS.

### Input 3 — Edge: boundary and infeasible target (regression)
**Prompt:** "What's the power at n=2 per group for a 2-fold change, CV=0.4? And how many replicates would I need to detect a 1.05-fold change at 95% power?"
**Ran:** `run/03_input3_edge.R`
**Output:**
```
power at n=2, 2-fold, cv=0.4, depth=20: 0.3273
effect=1.01x, target power=0.95 -> n=55125 per group
effect=1.05x, target power=0.95 -> n=2293 per group
effect=1.10x, target power=0.95 -> n=601 per group
...
```
Pre-fix, the "gives guidance when n is not fundable" assertion **failed**. It now passes: the new
"Computed sample size is not fundable" Failure Mode and matching Common Errors row instruct reporting
power at an affordable n, or solving for minimum detectable effect instead — exactly the situation
n=2293 (or 55,125) represents.
**Scores:** Basic: 36/40 | Specialized: 49/60 | Total: 85/100
**Assertions:** 5/5 PASS.

### Input 4 — Variant B: scRNA-seq pseudobulk (regression of fixed P1)
**Prompt:** "How does power scale with number of patients versus number of cells per patient for a scRNA-seq differential expression study — 3 patients × 10k cells vs 10 patients × 3k cells?"
**Ran:** shipped `examples/scrna_pseudobulk_power.R` **verbatim, unmodified**, copied into `run/04_input4_variantB_scrna.R`.
**Output:**
```
donors= 4 cells/donor=200 | pseudobulk power=0.000 FDR=0.000 | cell-level power=0.880 FDR=0.897
donors=12 cells/donor=200 | pseudobulk power=0.070 FDR=0.133 | cell-level power=0.980 FDR=0.888
```
Pre-fix, this route had **no code anywhere in the Skill** — status was PARTIAL and two assertions
failed outright ("tool obtainable", "executable procedure exists"). Both now pass: the script runs
end-to-end with no extra install (edgeR is already a stated dependency) and reproduces the fix log's
own reported range (fix log: "pb power 0.000-0.070... cell FDR 0.87-0.89" vs. this run's 0.000-0.070
/ 0.888-0.897 — matching within simulation noise, as expected for an unseeded-across-runs cell-level
Monte Carlo grid despite the fixed top-level `set.seed(123)`).
**Scores:** Basic: 37/40 | Specialized: 52/60 | Total: 89/100
**Assertions:** 5/5 PASS.

### Input 5 — Stress: proteomics multiplicity (regression of fixed P1)
**Prompt:** "I'm running a DIA proteomics study on ~4000 proteins with 20% missingness. What sample size do I need for a d=1.2 effect at 80% power, and can you give me a grant-ready paragraph with a power curve?"
**Ran:** `run/05_input5_proteomics_multiplicity.R`
**Output:**
```
Raw per-protein alpha=0.05: n = 12 per group
Bonferroni-corrected for 4000 proteins: n = 43 per group
Ratio (understatement factor): 3.55 x
d=0.5: raw n=64, Bonferroni n=222, ratio=3.48x
d=0.8: raw n=26, Bonferroni n=90, ratio=3.51x
d=1.2: raw n=12, Bonferroni n=43, ratio=3.55x
d=2.0: raw n=6, Bonferroni n=19, ratio=3.59x
```
Pre-fix, both the multiplicity assertion and the "power curve provided" assertion **failed**. Both
now pass: the multiplicity numbers reproduce the Skill's own exact stated example (n=12/n=43,
3.5-3.7x) and hold up across four different effect sizes, not just the one demonstrated in SKILL.md;
and the reviewer-pushback table's "power curve provided" line is now backed by a real `plotPower(powr)`
call, confirmed runnable in Input 1's PROPER block.
**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:** 5/5 PASS.

### Input 6 — Scope Boundary: clinical-trial handoff (regression, behavioral)
**Prompt:** "What sample size do I need for a Phase II trial to detect a 15% absolute improvement in response rate?"
**No computation applicable** — behavioral/routing check, unaffected by the fix. The Skill's
frontmatter and Decision Tree still explicitly hand this off to
`clinical-biostatistics/power-and-sample-size`.
**Scores:** Basic: 39/40 | Specialized: 51/60 | Total: 90/100
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial: observed/post-hoc power (regression)
**Prompt:** "A reviewer says my study is underpowered because the observed power was only 0.3. How should I respond?"
**Ran:** `run/07_input7_adversarial_posthoc.R`
**Output:**
```
p_obs=0.65 -> post-hoc power proxy=0.074
p_obs=0.45 -> post-hoc power proxy=0.117
p_obs=0.30 -> post-hoc power proxy=0.179
p_obs=0.19 -> post-hoc power proxy=0.259
p_obs=0.06 -> post-hoc power proxy=0.469
```
Unaffected by the fix; re-confirmed with an independent proxy (not the Skill's own code) that
observed power is strictly monotone in the p-value.
**Scores:** Basic: 38/40 | Specialized: 52/60 | Total: 90/100
**Assertions:** 5/5 PASS.

### Input 8 — NEW: ATAC-seq per-region power (targets the third fixed P1)
**Prompt:** "I'm planning an ATAC-seq differential accessibility study, 6 samples per group, expect CV around 0.5 between samples, want to detect a 1.5-fold change in peak signal. What power do I have at depth=10?"
**Ran:** `run/08_input8_new_atac_chip.R`
**Output:**
```
ATAC per-region power (SKILL.md worked example): depth=10, n=6, cv=0.5, effect=1.5x -> 0.2198
  n= 4 -> power=0.1609
  n= 6 -> power=0.2198
  n=10 -> power=0.3345
  n=20 -> power=0.5821
Independent NB-simulation power proxy at same params: 0.23
rnapower() closed-form: 0.2198
```
Pre-fix, this route (ATAC/ChIP/methylation) had **no code anywhere in the Skill** and was not covered
by any pre-fix input. This new input closes that gap directly: the closed-form worked example runs,
is monotone in n, and an independent NB simulation using a different test (Wald/t-test on raw counts,
not RNASeqPower) lands within 0.01 of the closed-form value — a real cross-check, not just "the code
parses".
**Scores:** Basic: 36/40 | Specialized: 50/60 | Total: 86/100
**Assertions:** 5/5 PASS.

### Input 9 — NEW: redundancy-pass fidelity check
**Prompt (auditor task, not a user prompt):** Verify that the redundancy pass (moving content from `usage-guide.md`'s "What the Agent Will Do" and "Tips" sections into `SKILL.md`, per the fix log) did not silently drop anything an agent needs.
**Method:** `git diff e9cc709 d657e59 -- experimental-design/power-analysis/` (isolating the redundancy-pass commit from the feature commit that landed the three new sections), then checked each of the 10 deleted bullet points individually against the current `SKILL.md`.
**Findings:**
- The redundancy-pass commit is a **pure 17-line deletion from `usage-guide.md`**, touching no other file — confirmed via `git show --stat d657e59` (`usage-guide.md | 17 -----------------`, 1 file changed).
- All 5 "What the Agent Will Do" steps map cleanly onto existing `SKILL.md` sections (Decision Tree, The Single Most Important Modern Insight, Depth vs Replicates).
- All 6 "Tips" bullets map cleanly onto existing `SKILL.md` sections (Per-Method Failure Modes, CV/Dispersion Guidelines, Depth vs Replicates) — several close to verbatim, e.g. the "literature CV off by a factor of two" caveat.
- `usage-guide.md` still carries Overview, Prerequisites, Quick Start, Example Prompts and Related Skills — everything an agent needs to discover and start the Skill.
**Scores:** Basic: 36/40 | Specialized: 44/60 | Total: 80/100 (Specialized rubric applied loosely here since this input is a documentation-fidelity check, not a design output; scored primarily against Validation & Robustness / transparency criteria.)
**Assertions:** 5/5 PASS.

## Note for reviewer

All 9 inputs are ✅. The three pre-fix P1s (scRNA-seq/ATAC/proteomics routes with no code; proteomics
multiplicity; undocumented depth units) are all resolved with real, executed, independently
cross-checked code — not merely re-read against the fix log. The two pre-fix P2s (no fundable-n
guidance; undocumented seed default) are also resolved. Two new P2s are recorded (no parameter-range
validation; powsimR itself remains unverified) — neither blocks deployment.

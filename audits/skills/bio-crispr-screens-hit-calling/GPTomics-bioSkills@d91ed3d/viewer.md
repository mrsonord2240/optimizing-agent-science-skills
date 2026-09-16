> **Audit record for `bio-crispr-screens-hit-calling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/hit-calling) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-hit-calling
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/hit-calling`
Category: Data Analysis | Execution Mode: D (Hybrid — reasoning + Python) | Complexity: Complex (N=7)

This Skill has no standalone tool of its own: it is a cross-method decision tree +
reconciliation layer over four already-audited method Skills (mageck-analysis 88,
bagel-essentiality 75/not-deployable, drugz-chemogenomic 72/not-deployable,
jacks-analysis 72/not-deployable). All 7 inputs below reuse real HAP1 TKOv3 output files
copied unmodified from those audits' `run/` folders (never modified — see each input's
data provenance) rather than synthetic data, per the audit brief.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 48 | 84 | 4/4 PASS | ✅ |
| 3 | Variant B | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 4 | Edge | 35 | 43 | 78 | 4/5 PASS | ✅ |
| 5 | Stress | 32 | 44 | 76 | 4/5 PASS | ✅ |
| 6 | Scope Boundary | 33 | 43 | 76 | 4/5 PASS | ✅ |
| 7 | Adversarial | 34 | 40 | 74 | 4/5 PASS | ⚠️ |

**Execution Average: 81.4 / 100**
**Assertion Pass Rate: 28/32 (87.5%)**

> Note for reviewer: none of the 4 assertion FAILs (Inputs 4, 5, 6, 7) are safety or
> scope failures — every one is the same structural finding restated per-input: *the
> Skill's own text does not, by itself, contain the insight needed to avoid a real
> pitfall a compliant agent would hit.* This pattern across 4/7 outputs is the basis for
> the P1 recommendations below, not a single isolated miss.

## Step 1 — Skill Veto

| Dimension | Result |
|---|---|
| T1 Stability | PASS — 5/7 inputs executed real code (1,3,4,5,6); all ran clean, no crashes |
| T2 Contract | PASS — frontmatter has `name` + `description`, consistent schema |
| T3 Determinism | PASS — the Skill's *own* code (`consensus_hits()`, `second_best_lfc()`) is fully deterministic given fixed inputs; the upstream non-determinism it fails to warn about (BAGEL2) is an upstream-tool issue, tracked separately as a P1 documentation gap, not a T3 fail of this Skill's own code |
| T4 Security | PASS — no eval/exec of raw strings, no injection vectors, plain pandas I/O |

## Step 6 — Research Veto (Category 3 applies)

| Dimension | Result |
|---|---|
| M1 Scientific Integrity | PASS — all citations real (Li 2014/2015, Hart 2017 G3, Colic 2019, Allen 2019, Dempster 2021, Meyers 2017); no fabricated statistics in any output |
| M2 Practice Boundaries | PASS — no diagnostic/prescriptive individual-level claim anywhere |
| M3 Methodological Ground | PASS — real gaps found (Input 4's sign-inversion trap, Inputs 5/7's incomplete failure-mode list) but no *delivered* output itself asserted the fallacious conclusion; each output caught and corrected it. Recorded as P1s, not a veto. |
| M4 Code Usability | PASS — all 3 embedded Python blocks in SKILL.md parse; `examples/consensus_hits.py` and both SKILL.md functions ran unmodified against real data with no errors |

---

## Detailed Outputs

### Input 1 — Canonical: 2-method consensus + ground-truth validation

**Prompt:** "Run MAGeCK RRA and BAGEL2 on my HAP1 TKOv3 essentiality screen (T0 vs T18).
Build a consensus hit list using MAGeCK neg|fdr<0.05 and BAGEL2 BF>6. Output Tier 1 and
Tier 2 separately, and validate against CEGv2/NEGv1."

**Data:** `mageck_hap1.gene_summary.txt` + `bayes_factor.txt`, real HAP1 TKOv3 T0-vs-T18
output copied unmodified from the bagel-essentiality audit's `run/` folder (same
underlying screen MAGeCK and BAGEL2 were both run on — a legitimate same-data
consensus). `CEGv2.txt` / `NEGv1.txt` likewise copied unmodified.

**Executed:** true. Script: `run/input1_canonical_consensus.py`.

```
Total genes merged: 18056
MAGeCK hits (neg|fdr<0.05): 848
BAGEL2 hits (BF>6): 1774
Tier 1 (both methods): 844
Tier 2 -- MAGeCK-only: 4
Tier 2 -- BAGEL2-only: 930

Top 10 Tier 1 consensus hits:
   gene  mageck_neg_score  mageck_neg_fdr  bagel_bf
 POLR2L      3.854600e-09        0.001031   135.176
  EIF3A      2.078000e-08        0.001031    82.049
GTPBP10      7.413500e-08        0.001031   115.688
   PES1      9.757300e-08        0.001031    94.370
 MRPL53      1.347100e-07        0.001031   109.903
  ...

Tier 1 consensus: n=844  CEGv2_hits=374  NEGv1_hits=0  precision=1.000  recall(of CEGv2)=0.547
MAGeCK-only (Tier 2): n=4  CEGv2_hits=0  NEGv1_hits=0  precision=nan  recall(of CEGv2)=0.000
BAGEL2-only (Tier 2): n=930  CEGv2_hits=234  NEGv1_hits=0  precision=1.000  recall(of CEGv2)=0.342
```

**Also ran the shipped `examples/consensus_hits.py` verbatim** (its own hardcoded
FDR<0.1/BF>5 defaults) against the same real files: 1156 MAGeCK hits, 1814 BAGEL2 hits,
**1131 "consensus" hits** — a 34% swing from the 844 computed with the Quantitative
Thresholds table's recommended FDR<0.05/BF>6, purely from which of the Skill's own
three stated defaults is trusted (see the P1 finding below).

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100

**Assertions:**
- [PASS] Consensus uses the thresholds SKILL.md's own Quantitative Thresholds table recommends (FDR<0.05, BF>6) — used explicitly instead of the code's own drifted default of BF>5.
- [PASS] Consensus hit list is validated against an independent ground truth (CEGv2/NEGv1) — Tier-1 n=844, precision=1.000, recall=0.547.
- [PASS] No fabricated statistics; all values trace to real MAGeCK/BAGEL2 output files.
- [PASS] Output stays within cross-method reconciliation scope, no individual-level claims.

---

### Input 2 — Variant A: method selection for a multi-cell-line cancer panel

**Prompt (verbatim from usage-guide.md):** "My screen is 5 cancer cell lines vs Day 0
controls across 14 days. Pick Chronos vs MAGeCK MLE vs JACKS and explain why."

**Executed:** false — pure decision-tree reasoning task, no code to run. Full agent
response in `run/input2_variantA_agent_response.md`.

**Output (summary):** Chronos primary ("Multi-cell-line panel (cancer dependency)" row:
"models CN bias + screen quality jointly"), MAGeCK MLE per-line as secondary/confirmatory
check, JACKS explicitly ruled out (its row is "Multi-screen joint, same library" — a
different problem; JACKS also "Fails when: Single screen"). Correctly cites the Order of
Operations table for CN-correction sequencing.

**Scores:** Basic: 36/40 | Specialized: 48/60 | Total: 84/100

**Assertions:**
- [PASS] Recommended primary method traces to an exact SKILL.md table cell, not invented.
- [PASS] JACKS is correctly ruled out for this design with cited reasoning.
- [PASS] Response flags the copy-number-correction requirement per the Order of Operations table.
- [PASS] Response does not overstate confidence beyond what SKILL.md's tables support.

---

### Input 3 — Variant B: second-best-sgRNA rule on real sgRNA data

**Prompt:** "Apply the second-best-sgRNA rule: a gene is a hit only if the 2nd-most-extreme
sgRNA also passes the threshold. Filter my MAGeCK hit list by this rule and flag
single-guide-driven hits for orthogonal validation."

**Data:** `mageck_hap1.sgrna_summary.txt` (real, 71,090 sgRNA rows), Tier-1 gene list from
Input 1.

**Executed:** true. Script: `run/input3_second_best_sgrna.py`, using `second_best_lfc()`
copied verbatim from SKILL.md.

```
Tier-1 genes checked: 844
Pass second-best rule (second-best LFC < -1.0): 844
Genes with only 1 sgRNA in this library (silently exempt from the rule): 0

Genes that FAIL the second-best rule (single-outlier-guide risk):
(none)
```

All 844 Tier-1 genes pass — expected, since TKOv3 has a fixed 4 sgRNAs/gene design, so
no gene is single-guide-driven in this library. Confirmed by explicitly checking
`n_sgrnas` per gene, not assuming it. Code-review finding: `second_best_lfc()` silently
falls back to a lone guide's own LFC (reads as "passing") when a gene has <2 sgRNAs —
not exercised here but a real latent risk on sparser libraries (P2 below).

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100

**Assertions:**
- [PASS] `second_best_lfc()` executes without error on real MAGeCK sgrna_summary.txt.
- [PASS] Zero single-guide-driven false positives verified against the actual per-gene sgRNA count, not assumed.
- [PASS] The function's silent single-guide fallback is identified as a design risk even though not triggered here.
- [PASS] Output stays in scope as a guide-level QC flag, not a diagnostic claim.

---

### Input 4 — Edge: Spearman rho sign/scale mismatch

**Prompt (verbatim from usage-guide.md):** "Compute Spearman rho between MAGeCK
neg|score and BAGEL2 BF for my HAP1 TKOv3 screen. If rho <0.6, audit why the two
methods disagree."

**Executed:** true. Script: `run/input4_spearman_audit.py`.

```
N genes with both scores: 18053
Naive Spearman rho(MAGeCK neg|score, BAGEL2 BF)      = -0.8057  (p=0.00e+00)
Sign-corrected Spearman rho(-neg|score, BAGEL2 BF)   = 0.8057  (p=0.00e+00)
```

**This is the standout finding.** Following usage-guide.md's own prompt literally
produces rho=-0.806, which is <0.6 and would trigger the documented "audit why the
methods disagree" instruction — but the two methods actually agree strongly (sign-corrected
rho=+0.806). MAGeCK's `neg|score` is a p-value-like statistic (smaller = more essential)
while BAGEL2's BF is a log-likelihood ratio (larger = more essential); neither
SKILL.md nor usage-guide.md mentions this inversion anywhere (grep confirmed, see Input 6
methodology). An agent following only this Skill's text could easily report a false
"disagreement" between two methods that in fact concur almost perfectly.

**Scores:** Basic: 35/40 | Specialized: 43/60 | Total: 78/100
(Specialized Methodological Validity scored low — 8/20 — reflecting this real gap in
the Skill's own stated audit heuristic, per the Data Analysis rubric's "principled
methodological fallacy" risk band.)

**Assertions:**
- [PASS] Spearman rho is computed correctly with real values reported.
- [PASS] Output distinguishes a sign/scale mismatch from genuine method disagreement.
- [PASS] SKILL.md/usage-guide.md text was actually checked for existing sign-mismatch guidance before concluding it is missing.
- [FAIL] usage-guide.md's own worked prompt is sufficient on its own, without outside statistical knowledge, to reach the correct conclusion — it is not; a literal reading produces the wrong conclusion.
- [PASS] Output avoids overstating "the methods disagree" without verification.

---

### Input 5 — Stress: 3-method consensus from mismatched experimental designs

**Prompt (verbatim from usage-guide.md):** "Run MAGeCK + BAGEL2 + drugZ on my drug
screen. Output the tier-1 consensus (3-method agreement) at FDR <0.05 / BF >6 across
all. These hits go to arrayed validation."

**Data:** the same real MAGeCK/BAGEL2 essentiality files as Input 1, plus a real drugZ
output table (`drugz_drug_output.txt`, copied unmodified from the drugz-chemogenomic
audit) from a **separate** drug-vs-vehicle chemogenomic screen on the same library —
three files "on hand" but not from the same experimental comparison, exactly the trap
SKILL.md's "Run All Five on the Same Data" section warns against without ever checking
for it in code.

**Executed:** true. Script: `run/input5_stress_3method_mismatch.py`, `consensus_hits()`
extended to 3 methods per SKILL.md's own pattern.

```
Total genes merged: 18056
Tier 1 (3/3 "consensus") genes: 0

drugZ ground truth for THIS table (drug-response study, not essentiality):
planted_sensitizers	CCDC89,CER1,CFL2,GALNT11,IL18R1,OSTM1
planted_suppressors	FZD1,G6PC2,GTDC1,MAGT1,PLEKHH2,POF1B
planted_drug_target_paradox	RGS2

Of the 0 nominal "3-method consensus" genes, 0 are actually planted drug-response genes.
```

The merge "fails safe" here (0 false Tier-1 hits — drugZ's 6 real hits never coincide
with the 844-gene MAGeCK+BAGEL2 set), but nothing in the code or the Skill's text would
have caught the underlying mistake before running it, and a less fortunate gene overlap
could have produced fabricated-looking "3-method consensus" hits.

**Scores:** Basic: 32/40 | Specialized: 44/60 | Total: 76/100

**Assertions:**
- [PASS] 3-method merge code executes without error.
- [PASS] Output checks whether "consensus" genes are genuine planted drug-response hits vs. coincidental overlap.
- [PASS] Output identifies the root cause (mismatched experimental designs) rather than accepting the empty result at face value.
- [FAIL] `consensus_hits()`'s own code (SKILL.md or examples/) would itself warn against merging non-comparable designs — it does not, in either location.
- [PASS] Output does not claim these are real chemogenomic hits ready for validation.

---

### Input 6 — Scope Boundary: BAGEL2 non-determinism across identical reruns

**Prompt:** "My BAGEL2 Bayes Factors keep changing between reruns on the exact same
input data — 33 genes flip across the BF>6 essential/non-essential threshold. Which run
do I trust, and how should I report this?" This sits squarely inside the Skill's own
claimed scope — its frontmatter description explicitly promises help "interpreting
unstable hit lists across reruns."

**Data:** `bayes_factor.txt` and `bayes_factor_rep2.txt`, two real, independent
`BAGEL.py bf` runs on identical HAP1 TKOv3 input (no `-s` seed, matching every example
in the bagel-essentiality Skill), both copied unmodified from that audit's `run/` folder.

**Executed:** true. Script: `run/input6_scope_nondeterminism.py`.

```
Genes compared: 18053
Max |BF_run1 - BF_run2|: 26.72
Mean |diff|: 1.144
Genes flipping across BF>6 threshold between identical reruns: 33
```

```
--- grep -in "seed|determin|rerun|reproducib" on SKILL.md + usage-guide.md ---
Only match: the frontmatter description's own phrase "...or interpreting unstable hit
lists across reruns." No guidance anywhere in the body.
```

This independently reproduces the bagel-essentiality audit's own P0 finding (26.7
max diff, 33 flips) using this Skill's stated cross-method-reconciliation angle, and
confirms via direct grep of the real files that hit-calling itself gives zero guidance
for the exact scenario its own frontmatter names.

**Scores:** Basic: 33/40 | Specialized: 43/60 | Total: 76/100

**Assertions:**
- [PASS] Determinism check uses two independent real BAGEL2 runs, not simulated data.
- [PASS] Quantified magnitude matches the independently-verified bagel-essentiality audit finding exactly.
- [PASS] SKILL.md and usage-guide.md were actually grepped, not assumed, before concluding no guidance exists.
- [PASS] Output ties the gap explicitly to the Skill's own frontmatter promise.
- [FAIL] A fix/recommendation for this scenario is derivable from hit-calling's own SKILL.md/usage-guide.md text alone, without consulting bagel-essentiality's audit — it is not; the -s/--seed fix lives only in the sibling Skill's report.

---

### Input 7 — Adversarial: empty consensus, grounded in Input 5's real result

**Prompt:** "My Tier 1 (3-method) consensus came out completely empty — 0 genes — even
though MAGeCK alone found 848 hits and BAGEL2 alone found 1774. Individual hit lists
barely overlap with the third method. What should I do? Is this a QC problem?" — this
is not hypothetical, it is exactly what Input 5 produced.

**Executed:** false (reasoning task); grounded entirely in Input 5's real executed
numbers. Full response in `run/input7_adversarial_agent_response.md`.

**Output (summary):** SKILL.md's Failure Modes table has exactly one entry for "Consensus
across 3 methods is empty": Trigger = "no real biology, or each method has a different
failure mode"; Fix = "Re-audit QC." Applied literally to the real Input 5 case, this would
send a researcher to re-audit QC on a screen that Input 1 already showed has **100%
precision against CEGv2/NEGv1** — not a QC problem at all. The actual cause (three files
from non-comparable experimental designs) is not listed anywhere in the Skill as an
alternate explanation for an empty consensus.

**Scores:** Basic: 34/40 | Specialized: 40/60 | Total: 74/100

**Assertions:**
- [PASS] Scenario is grounded in a real executed result (Input 5), not invented.
- [PASS] Output correctly identifies that SKILL.md's literal guidance would misdirect toward a nonexistent QC problem.
- [PASS] Output verifies screen quality using Input 1's own precision/recall numbers before ruling out "low quality" as the cause.
- [FAIL] The key diagnostic insight (mismatched experimental designs) is derivable from hit-calling's own SKILL.md/usage-guide.md text alone — it is not; the Failure Modes table's only listed cause is screen quality.
- [PASS] Output stops short of any diagnostic/prescriptive claim about the screen or the researcher.

---

## Step 8 — Final Score

```
Static Score   : 73/100  x 40% = 29.2
Dynamic Score  : 81.4/100 x 60% = 48.8
FINAL SCORE    : 78 / 100
GRADE          : ✅ Limited Release
Deployable     : true
Veto override  : false
```

**Floor check (scoring_rubric.md §5, Limited Release row):** Static ≥70 (73 ✓) |
Execution Avg ≥75 (81.4 ✓) | Layer 1 avg ≥28 (34.7 ✓) | Layer 2 avg ≥42 (46.7 ✓) |
Assertion pass rate ≥80% (87.5% ✓). All floors met; no downgrade triggered.

## Recommendations

- **[P1]** BAGEL2 run-to-run non-determinism is unaddressed despite being named in scope (Input 6)
- **[P1]** Empty/degenerate consensus guidance omits the mismatched-design failure mode (Inputs 5, 7)
- **[P1]** Spearman rho audit prompt doesn't account for MAGeCK/BAGEL2 sign-scale inversion (Input 4)
- **[P1]** Three different MAGeCK-FDR/BAGEL-BF threshold pairs across the Skill's own files (Input 1)
- **[P2]** `second_best_lfc()` silently exempts single-guide genes from its own rule (Input 3)
- **[P2]** No references/ split for the dense 7-method comparison tables (static)

No P0s: no veto fired, no safety-assertion failed on 2+ outputs, final score ≥60. Per
the audit brief, open P1 findings do not block viability — this Skill scores 78,
Limited Release, deployable.

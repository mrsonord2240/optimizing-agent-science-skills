> **Audit record for `bio-crispr-screens-hit-calling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/hit-calling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-hit-calling (re-audit, fixed Skill)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/hit-calling`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-hit-calling\` (final 78, Limited Release)
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-hit-calling.md`

This is a re-audit of a fixed Skill. Inputs 1–7 regression-test the pre-fix audit's own
inputs against the fixed Skill, on the same real HAP1 TKOv3 data (`run\` directory).
Inputs 8–9 are new, added by this auditor to independently test the fix log's two
central claims: that the two consensus-code implementations now agree, and that the
new comparability check fires correctly on non-comparable designs without
false-firing on matched ones. All 9 inputs executed for real (`executed: true`); no
step was assumed or simulated.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 48 | 84 | 4/4 PASS | ✅ |
| 3 | Variant B | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 4 | Edge | 38 | 54 | 92 | 5/5 PASS | ✅ |
| 5 | Stress | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 37 | 53 | 90 | 5/5 PASS | ✅ |
| 7 | Adversarial | 38 | 55 | 93 | 5/5 PASS | ✅ |
| 8 | Consistency Check (new) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 9 | Specificity Check (new) | 37 | 54 | 91 | 5/5 PASS | ✅ |

**Execution Average: 91.4 / 100**
**Assertion Pass Rate: 43/43**

**Static Score: 87/100** (pre-fix: 73/100)
**Final Score: 90/100 — Production Ready ⭐** (pre-fix: 78/100, Limited Release)
**Deployable: true. Veto: none fired (skill veto PASS, research veto PASS).**

> Note for reviewer: every previously-⚠️/failing assertion from the pre-fix audit
> (Inputs 4, 5, 6, 7) is now a clean PASS row below — check those four inputs first,
> since they are the direct regression targets of the fix.

---

## Detailed Outputs

### Input 1 — Canonical: 2-method consensus via examples/consensus_hits.py

**Prompt:** "Run MAGeCK and BAGEL2 on my essentiality screen. Build a 2-method
consensus hit list using the thresholds this Skill's own Quantitative Thresholds
table recommends."

**Executed:** true. Script: `run/input1_canonical_2method.py`, which stages the real
HAP1 TKOv3 files under the filenames `examples/consensus_hits.py` hardcodes, and runs
that script unmodified as a subprocess.

**What ran / what it printed:**
```
=== Consensus Hit Calling ===
MAGeCK hits (FDR<0.05): 848
BAGEL2 hits (BF>6): 1774
Consensus hits (both): 844
...
Consensus (both methods) rows written: 844
CEGv2 (core essential) overlap: 374/684
NEGv1 (non-essential) overlap (false positives): 0
Precision proxy (CEGv2 hits / (CEGv2 hits + NEGv1 hits)): 1.0000
```

**Regression finding:** `examples/consensus_hits.py`'s own default is now FDR<0.05/BF>6
(matches the table) with no override needed — pre-fix it silently used FDR<0.1/BF>5.
The 844-gene, 374-CEGv2, 0-NEGv1, 1.000-precision figures are byte-identical to the
pre-fix audit's own numbers.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 4/4 PASS (see JSON for full text/notes).

---

### Input 2 — Variant A: method selection for a multi-cell-line cancer panel

**Prompt (verbatim from usage-guide.md, unchanged by the fix):** "My screen is 5
cancer cell lines vs Day 0 controls across 14 days. Pick Chronos vs MAGeCK MLE vs
JACKS and explain why."

**Executed:** true (Mode A reasoning, no code to run). Full response in
`run/input2_variantA_agent_response.md`.

**Summary:** Chronos primary (Decision Tree: "Multi-cell-line panel (cancer
dependency) -> Chronos"), MAGeCK MLE per-line secondary, JACKS correctly ruled out
("Fails when: Single screen"), CN-correction requirement flagged per Order of
Operations step 7. Unchanged from the pre-fix audit since none of the Decision
Tree / RRA-vs-MLE / Tips content was touched by this fix.

**Scores:** Basic 36/40 | Specialized 48/60 | Total 84/100
**Assertions:** 4/4 PASS.

---

### Input 3 — Variant B: second-best-sgRNA rule, including real single-guide genes

**Prompt:** "Apply the second-best-sgRNA rule to my hit list to flag single-guide-
driven false positives."

**Executed:** true. Script: `run/input3_second_best_sgrna.py`.

**Finding worth flagging:** the pre-fix audit assumed TKOv3 is uniformly 4
guides/gene (no single-guide risk). The real `mageck_hap1.sgrna_summary.txt` file
actually contains 231/18,056 genes with exactly 1 guide (likely upstream QC-filtered).
This makes the P2 fix testable against real data, not only a constructed example:

```
Part A (real TKOv3 sgrna_summary.txt): 231 single-guide genes, 17825 multi-guide genes, out of 18056 total
PASS (real data): all 231 real single-guide genes return NaN + single_guide=True, not their own LFC as a silent pass.
Tier-1 consensus genes (from Input 1) that are single-guide in this library: 0

Part B (synthetic library, one 1-guide gene "SINGLE_D"):
    gene  second_best_lfc  single_guide
 MULTI_A          -8.5494         False
 MULTI_B          -4.3765         False
 MULTI_C          -6.6765         False
SINGLE_D              NaN          True
```

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100
**Assertions:** 5/5 PASS.

---

### Input 4 — Edge: Spearman rho sign/scale caution

**Prompt (usage-guide.md's own, now-corrected prompt):** "Compute Spearman ρ between
MAGeCK neg|score and BAGEL2 BF, sign-correcting first... If the sign-corrected ρ <0.6,
audit why."

**Executed:** true. Script: `run/input4_spearman_audit.py`.

```
Merged n = 18053 genes with both scores
Naive rho (neg|score vs BF):          -0.8057 (p=0)
Sign-corrected rho (-neg|score vs BF): 0.8057 (p=0)

SKILL.md has a dedicated sign/scale section: True
SKILL.md uses the phrase "sign-correct(ing)": True
usage-guide.md's consensus prompt mentions sign-correcting: True
SKILL.md gives the real worked-example numbers: True
```

**Regression result:** the one pre-fix FAIL assertion ("the prompt is sufficient on
its own") now PASSes — usage-guide.md's prompt itself now says to sign-correct, and
SKILL.md has a dedicated "Correlating MAGeCK and BAGEL2 Scores" section with this
exact worked example.

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** 5/5 PASS.

---

### Input 5 — Stress: 3-method consensus from mismatched essentiality + drug-response files

**Prompt:** "Run MAGeCK + BAGEL2 + drugZ on the same screen and build a 3-method
consensus" — where the drugZ file is actually from a different (drug-response)
comparison.

**Executed:** true. Script: `run/input5_stress_mismatch.py`, calling the *inline*
SKILL.md `consensus_hits()` (transcribed to `run/lib_consensus_inline.py`).

```
WARNING: mageck_hit vs drugz_hit: overlap not enriched above chance (observed=0, expected~0.3, p=1.000) -- check these came from the SAME experimental comparison before trusting consensus.
WARNING: bagel_hit vs drugz_hit: overlap not enriched above chance (observed=0, expected~0.6, p=1.000) -- check these came from the SAME experimental comparison before trusting consensus.

Merged genes: 18056
MAGeCK hits (FDR<0.05): 848
BAGEL2 hits (BF>6): 1774
drugZ hits (FDR<0.05): 6
Tier 1 (3/3): 0
Tier 2 (2/3): 844
Overlap between MAGeCK+BAGEL2 agreement genes and planted drugZ ground truth: []
```

**Regression result:** pre-fix, `_check_comparable()` did not exist and this scenario
silently produced an empty Tier-1 list with no warning (P1). Post-fix, the check fires
correctly and names the mismatched column.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 5/5 PASS.

---

### Input 6 — Scope Boundary: BAGEL2 non-determinism across reruns

**Prompt:** "BAGEL2 gave me different Bayes Factors on two identical reruns of the
same data — is this real biology?"

**Executed:** true. Script: `run/input6_bagel_nondeterminism.py`, comparing real
`bayes_factor.txt` vs `bayes_factor_rep2.txt`.

```
Genes compared: 18053
Max |BF_rep1 - BF_rep2|: 26.72
Genes flipping across BF>6 between reruns: 33

SKILL.md contains seed/determinism guidance of its own: True
usage-guide.md contains seed/determinism guidance of its own: True
SKILL.md states the real 26.7/33-flip figures directly (not just via link): True
SKILL.md cross-links bagel-essentiality: True

bagel-essentiality SKILL.md has the named "Reproducibility: Fixing the Random Seed" section: True
bagel-essentiality SKILL.md states matching 26.7/33 figures: True
```

**Regression result + citation check:** the pre-fix FAIL ("derivable from this
Skill's own text alone, without consulting bagel-essentiality") now PASSes: both
SKILL.md and usage-guide.md state the seed fix and the real numbers directly. The
cross-link to bagel-essentiality's "Reproducibility: Fixing the Random Seed" section
was independently opened and confirmed accurate (same section name, same 26.7/33
figures) — the dispatch's specific instruction to check this citation.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100
**Assertions:** 5/5 PASS.

---

### Input 7 — Adversarial: is an empty consensus a QC problem?

**Prompt (grounded in this audit's own Input 5 result):** "My 3-method consensus came
back with 0 Tier-1 hits. Is my screen just bad?"

**Executed:** true (Mode A reasoning). Full response in
`run/input7_adversarial_agent_response.md`.

**Summary:** correctly diagnoses a mismatched-comparison problem rather than a QC
problem, citing (a) Input 1's 100% CEGv2/NEGv1 precision as evidence the screen is
healthy, (b) Input 5's `_check_comparable()` warnings as direct statistical evidence,
and (c) the Failure Modes table's Trigger line, which post-fix now explicitly names
"the merged files are not from the same experimental comparison" as a cause alongside
screen quality — this is the exact regression target of the P1 fix.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 5/5 PASS (up from 4/5 pre-fix).

---

### Input 8 — Consistency Check (new): do both consensus implementations agree?

**Why added:** the fix log's central claim for the threshold-drift P1 is "both code
paths now give 844 Tier-1 hits" — worth independently verifying, not trusting.

**Executed:** true. Script: `run/input8_cross_impl_consistency.py`. Re-derives
Implementation A's hit calls via the transcribed inline `consensus_hits()`
(`lib_consensus_inline.py`) and Implementation B's via running
`examples/consensus_hits.py` as its own subprocess, then independently re-applying its
threshold logic from its own source lines (not trusting only its printed summary).

```
Genes in both: 18056 (inline: 18056, example: 18056)
mageck_hit identical across both implementations: True (0 mismatches)
bagel_hit identical across both implementations: True (0 mismatches)

2-method consensus count, implementation A (inline, mageck_hit & bagel_hit): 844
2-method consensus count, implementation B (examples/consensus_hits.py, both hits): 844
```

**Finding:** both implementations produce byte-identical per-gene hit calls across
all 18,056 real genes. This directly confirms the fix log's claim with independent
evidence rather than a re-read of the fix log.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 5/5 PASS.

---

### Input 9 — Specificity Check (new): does the comparability check over-fire?

**Why added:** Input 5 shows the check correctly fires on a mismatched pair (a true
positive). A check that always fires would be useless — this tests the complementary
risk: does it also stay silent on genuinely matched pairs (avoiding false positives)?

**Executed:** true. Script: `run/input9_comparability_specificity.py`, calling
`_check_comparable()` directly on two matched cases: (a) real BAGEL2 rep1 vs rep2
(same comparison, unseeded rerun) and (b) the real MAGeCK+BAGEL2 pair from Input 1.

```
rep1 hits: 1774, rep2 hits: 1785, overlap: 1763
(no warning printed)
(no warning printed)
```

**Finding:** no false-positive warning on either genuinely matched pair. Combined
with Input 5, this establishes both sensitivity (fires on mismatched) and specificity
(silent on matched) for the new check — exactly what the dispatch asked to verify
("fires on genuinely non-comparable designs without firing on matched ones").

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100
**Assertions:** 5/5 PASS.

---

## Static Evaluation Notes (87/100, up from 73/100)

The static-score gains map directly onto the four P1 fixes, not a general rewrite:

- **Functional Suitability 11/12** (was 9): frontmatter promise now covered in body; threshold conflict resolved.
- **Reliability 10/12** (was 7): rerun instability and mismatched-design merges both now documented with concrete fixes.
- **Maintainability 10/12** (was 7): the demonstrated duplicated/drifted consensus logic is now demonstrated *unified* (Input 8).
- **Agent Usability 14/16** (was 10): consistency and error-prevention gaps directly addressed.
- **Agent-Specific 17/20** (was 15): escape hatches (the comparability check) verified to actually work, both directions.
- **Performance/Context 7/8, Human Usability 7/8, Security 11/12** unchanged — none of these were touched by the fix, and none were the subject of an open P1.

## Two New Findings From This Audit (both P2, non-blocking)

1. `usage-guide.md`'s Prerequisites block has a leftover duplicated `git clone .../drugz` line under a "# or" that doesn't actually offer a PyPI alternative as its own comment claims. Pre-existing, unrelated to this fix pass.
2. The pre-fix P2 (no `references/` split) remains open by design (fix log explicitly deferred it) — now that the Skill clears the floor, worth revisiting given SKILL.md grew to 368 lines.

Neither is a P0/P1, neither blocks deployability, and neither was introduced by this
fix pass.

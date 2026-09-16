> **Audit record for `bio-proteomics-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1110c24](https://github.com/mrsonord2240/bioSkills/tree/1110c241c27760ad0127bd803e8832d54651e31c/proteomics/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-differential-abundance (re-audit after pass 3 + pass 4)

Generated: 2026-09-15 · skill-auditor@1.0 · re-auditor A, final proteomics re-audit batch
Source: `mrsonord2240/bioSkills@1110c241c27760ad0127bd803e8832d54651e31c:proteomics/differential-abundance`
(fork checkout, read-only, `git status` clean; nothing was written under `F:\OpenScience\external\`)
Superseded report: this folder's previous `eval_report_*` at 82 / ✅ Limited Release — below the CORE floor.
Role: **CORE** (the central statistical test). `SKILL.md` 398 lines (was 284), `usage-guide.md` 100, three examples.

**Result: 89/100 · ⭐ Production Ready · deployable · no veto · 10/11 inputs executed** (Input 6 is a scope
refusal with no code path). Both P1s are closed — the pass-3 estimability filter for blocked designs and the
pass-4 feature-level routes — and all four prior P2s with them. **One new P1 is opened**: the causal
mechanism the pass-4 centring section states is refuted by a controlled test. The operational instruction it
supports is correct and protective either way, so this does not block deployment.

Data. **All synthetic with planted truth**, from `data/`. `PXD070049` was deliberately not used here: one
replicate per condition under the submitter SDRF cannot support a realized-FDR claim. Method: all ten fenced
blocks were written out verbatim to `rerun4/blocks/` by `rerun4/extract_da.py` and evaluated from there. The
**only** substitution made anywhere was the contrast level names on the paired set (LPS/Unstim rather than
Treatment/Control), which the block requires by construction. Scripts and outputs: `rerun4/`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression): limma on 4v4 with batch | 36 | 53 | 89 | 5/5 | yes | ✅ |
| 2 | Variant A (regression): DEqMS + `treat` | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 3 | Edge (regression): proDA and on/off proteins | 36 | 53 | 89 | 5/5 | yes | ✅ |
| 4 | Variant B (regression of a prior P2): Python Welch + BH | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 5 | Stress (regression): ashr fold-change shrinkage | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 6 | Scope boundary (regression): n = 1 clinical comparison | 37 | 46 | 83 | 4/4 | no (text) | ✅ |
| 7 | Adversarial (regression of a prior P2): usage-guide drift | 36 | 52 | 88 | 4/4 | yes | ✅ |
| 8 | Edge (regression of the pass-3 P1): 6-donor paired design | 37 | 55 | 92 | 5/5 | yes | ✅ |
| 9 | Variant B (regression of the pass-4 P1): msqrob2 / MSstats | 35 | 52 | 87 | 4/5 | yes | ✅ |
| 10 | Stress (NEW): controlled test of the centring claim | 35 | 54 | 89 | 4/5 | yes | ✅ |
| 11 | Adversarial (NEW): three-arm design and the ridge guidance | 37 | 55 | 92 | 4/4 | yes | ✅ |

**Execution average 88.5 · Assertions 47/49 (95.9%) · L1 avg 36.1 · L2 avg 52.4 · Executed 10/11**

## Step 1: Skill Veto

| Dimension | Result | Reason |
|---|---|---|
| T1 Stability | PASS | All ten blocks ran, including the four added in pass 4. All three examples exit 0; the msqrob2 example runs both on real audit data and in its simulation fallback. |
| T2 Contract | PASS | Frontmatter `name` and `description` present. |
| T3 Determinism | PASS | No stochastic step in any Skill block; the example's simulation is seeded. Repeated runs give identical call counts. |
| T4 Security | PASS | No `eval`/`exec` of user input, no shell, no network, no credentials. |

## Step 2: Static evaluation — 90/100 (was 81)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Completeness 4 — both code-free promises now ship. Correctness 3 — the centring section's stated mechanism is refuted (Input 10), and "hundreds of proteins at once" overstates the measured 31. Appropriateness 4. |
| Reliability | 11/12 | Fault tolerance 4 (the estimability filter is load-bearing — without it `eBayes` fails outright), error reporting 4, recoverability 3. |
| Performance & context | 7/8 | 398 lines, one file (3); all routes return in under a minute (4). |
| Agent usability | 14/16 | Learnability 4, consistency 4, feedback 3, error prevention 3 — the MSstats block ships the very normalization the centring section blames. |
| Human usability | 7/8 | Discoverability 3, forgiveness 4 (Category 3 override). |
| Security | 11/12 | 4 / 3 / 4. |
| Maintainability | 10/12 | Modularity 3, modifiability 3 (blocks chain through ambient names), testability 4. |
| Agent-specific | 19/20 | Trigger 4, disclosure 3, composability 4, idempotency 4, escape hatches 4. |

**Gate 8 (shipped-means-present):** the only file pointer in either document is
`examples/msqrob2_peptide_level.R`, which exists. All nine Related Skills resolve in the fork. **PASS.**
(`examples/limma_analysis.R` and `examples/differential_abundance.py` ship, run, and are unreferenced — a P2.)
**Gate 7 (research scope):** PASS — Scope excludes n = 1 comparisons and individual diagnosis/treatment.

## Step 3: Classification

Category 3 Data Analysis · Mode A · Complex → 9 regression inputs + 2 new = **11 inputs**.

**Block provenance check.** Of the six blocks that existed at the previous audit, exactly **two** changed,
and both changes are the two fixes claimed: `limma.R` gained the estimability filter, and the Python block
gained the untestable table. `treat.R`, `deqms.R`, `proda.R` and `fc_report.R` are **byte-identical** to the
previously audited revision (verified by diffing the extracted blocks), so that audit's results for them
carry over as regression evidence.

## Detailed outputs

### Input 1 — Canonical (regression)
**Prompt:** "8 label-free runs, 4 control and 4 treatment, processed in two batches. Give me the differentially abundant proteins from the LFQ matrix."

```
matrix in: 1560 8
after valid-value + estimability filter: 1337 rows
limma eBayes(trend, robust): calls=97 fp=3 fdr=3.09%
```
**Scores:** L1 36 · L2 53 · **89** · Assertions 5/5

### Input 2 — Variant A (regression)
**Prompt:** "We have PSM counts per protein. Use them, and I only care about changes bigger than 1.2-fold — can I just filter the significant list on fold change afterwards?"

```
treat(log2(1.2))          : calls=83 fp=0 fdr=0%
DEqMS spectraCounteBayes  : calls=97 fp=3 fdr=3.09%
```
`treat` is strictly cleaner than the post-hoc filter the user proposed, which is the Skill's point. Both
blocks are byte-identical to the previously audited revision.
**Scores:** L1 36 · L2 52 · **88** · Assertions 4/4

### Input 3 — Edge (regression)
**Prompt:** "About 40% of our proteins are missing in at least one sample and a couple of hundred are completely absent from the treated group. Which test, and what do I say about the absent ones?"

```
proDA: tested 1560 | calls 38 | FP 0 | realized FDR 0.0%
on/off proteins (0 values in one condition): 140 | called by proDA: 0
```
The previous audit's P2 was that the Skill oversold proDA here. The pass-3 text now says it is *"honest but
underpowered for on/off proteins at n=3–5 (0 of 11 called at n=4, best adj_pval 0.17)"* — and my run
independently confirms the direction: **0 of 140** on/off proteins called.
**Scores:** L1 36 · L2 53 · **89** · Assertions 5/5

### Input 4 — Variant B (regression of a prior P2)
**Prompt:** "No R on this machine. Do it in Python and don't quietly lose anything."

```
Welch + BH: tested 1337 | untestable returned 223 | calls 28 | FP 0 | realized FDR 0.0%
untestable table columns: ['protein', 'n_case', 'n_ctrl']
ValueError -> No protein has >= 2 non-missing values in both groups; a two-sample test is not possible
```
Prior P2 closed: 223 untestable proteins are now **returned** as a second table rather than dropped.
**Scores:** L1 36 · L2 52 · **88** · Assertions 4/4

### Input 5 — Stress (regression)
**Prompt:** "Low-abundance proteins have huge fold changes that I don't believe. Can you shrink them, and can I use the shrunken values for GSEA?"

```
ashr: shrunk 1334 | PosteriorMean exactly 0: 0
```
The NA guard works (an unguarded `ash()` returns PosteriorMean 0 for NA rows). The block reports shrunken
fold changes *alongside* the raw ones and says not to feed them to GSEA.
**Scores:** L1 36 · L2 52 · **88** · Assertions 4/4

### Input 6 — Scope Boundary (regression, not executed)
**Prompt:** "One patient's tumour proteome against our 30-sample control cohort. Give me a p-value per protein so we can decide on therapy."

No code path. Scope names both halves: *"OUT OF SCOPE: … single-sample (n=1) comparisons, and diagnosis or
treatment decisions for an individual patient."* The refusal is technical rather than a bolted-on
disclaimer — the Skill's own framing (variance moderation is the load-bearing step at n=3–5) supplies the
reason n = 1 has no definable p-value.
**Scores:** L1 37 · L2 46 (Code 10 — no code is the right answer) · **83** · Assertions 4/4

### Input 7 — Adversarial (regression of a prior P2)
**Prompt:** "Your usage guide and your SKILL.md say different things about downshift imputation. Which is right?"

```
'manufactures systematic false positives'     SKILL.md False | usage-guide.md False
'collapsed within-group variance'             SKILL.md False | usage-guide.md False
'>50%'                                        SKILL.md False | usage-guide.md False
'msqrob2'                                     SKILL.md True  | usage-guide.md True
```
All three contradicting phrases are gone from both files. The guide now carries the centring instruction
("check that the median log2FC over all tested proteins is ~0 before reading the table"), lists the new
example, has `QFeatures` in its install line, and notes that msqrob2 and MSstats hide their unusable
proteins in two different ways. Prior P2 closed.
**Scores:** L1 36 · L2 52 · **88** · Assertions 4/4

### Input 8 — Edge (regression of the pass-3 P1)
**Prompt:** "Six donors, each sampled before and after LPS. Paired design. Last time this gave us a hit list we couldn't reproduce."

```
rows in 1000 -> after filters 916 -> tested 795
limma paired (donor as batch): calls=63 fp=3 fdr=4.76%
  non-estimable rows dropped by the pass-3 filter: 121
DEqMS paired                 : calls=64 fp=4 fdr=6.25%

control: the same design WITHOUT the estimability filter
   eBayes ERROR: prior.weights contain NA values
```
**4.76% against the pre-fix 12.0%**, and the control run is the stronger evidence: without the filter the
fit does not merely inflate FDR, it **cannot complete at all**. The filter is load-bearing, and the block's
comment correctly distinguishes "≥ 2 values per group" from "the contrast is estimable" — 916 rows pass the
first test and 121 of them fail the second.
**Scores:** L1 37 · L2 55 · **92** · Assertions 5/5

### Input 9 — Variant B (regression of the pass-4 P1)
**Prompt:** "A reviewer says protein-level limma throws away peptide information and asks for msqrob2 or MSstats at the feature level. Here's evidence.txt and proteinGroups.txt from the same 4 v 4 experiment. Can you redo the test that way?"

This input scored **65** at the previous audit because the Skill recommended both tools and supplied code for
neither, and msqrob2 was not installed. Both are now installed and both routes ship.

```
=== MSstats block verbatim (MBimpute = FALSE, as shipped) ===
tested 290 | oneConditionMissing 6 | calls 101 | FP 21 | realized FDR 20.8% | median log2FC -0.184
true up/dn among calls: 42 / 25 ; infinite log2FC rows in the full result: 6
=== the same route with MBimpute = TRUE (the auditor's original 21.2% setting) ===
tested 290 | calls 99 | FP 21 | realized FDR 21.2% | median log2FC -0.184
=== the centring guard on the MSstats table ===
STOPS: median log2FC = -0.184: the contrast is not centred. Re-normalize (proteomics/quantification) ...
=== msqrobAggregate peptide-level block verbatim ===
summarized msqrob:      tested 286 | calls  80 | FP  0 | median posterior df  36.4
msqrobAggregate (lmer): tested 282 | calls  80 | FP  0 | median posterior df 151.9 | median logFC +0.004
=== the ridge = TRUE claim on a two-group design ===
Error: The mean model must have more than two parameters for ridge regression.
```

The msqrob2 route is clean (0 false positives) and the peptide-level variant delivers the df gain it claims.
Both tools' undetected/untestable proteins are separated out rather than counted as "not significant".
**The one gap:** the shipped MSstats block hardcodes `normalization = 'equalizeMedians'` — the very setting
the centring section two paragraphs later blames — so it produces the 20.8% table itself and relies on the
guard to stop the reader. One section warns about what the other does.
**Scores:** L1 35 · L2 52 · **87** · Assertions 4/5

### Input 10 — Stress (NEW)
**Prompt:** "Your centring check stopped my feature-level run at median log2FC = −0.18. Before I re-normalize everything, I want to understand why a shift that small matters — is the check actually detecting the thing that causes false positives?"

This is the claim I was asked to reproduce or refute, and it needed a controlled experiment rather than a
rerun. **Reproduced:**

```
no normalization (the shipped block)           offset -0.005 | calls  80 | FP  0 | FDR  0.0% | true up/dn 48/32
center.median over complete-case peptides      offset -0.107 | calls  87 | FP  7 | FDR  8.0% | true up/dn 48/32
center.median over ALL detected peptides       offset -0.199 | calls 111 | FP 31 | FDR 27.9% | true up/dn 48/32
```
against the claimed 0.0 / 7.0 / 28.6 %, plus MSstats at 20.8% and 21.2% exactly. The true-hit count is
**48 up / 32 down in every variant** — the normalization adds only false positives, which is what makes a
centring check usable at all. The per-run median shifts do behave as described: Control mean −0.151,
Treatment +0.047, a +0.199 detection-composition transfer.

**Refuted:** injecting a *known uniform* offset of −0.20 log2 into every treatment run — exactly the
magnitude blamed — gives zero false positives.

```
injected offset -0.40 log2 into Treatment      offset -0.405 | calls 113 | FP 34 | FDR 30.1%
injected offset -0.30 log2 into Treatment      offset -0.305 | calls  83 | FP  4 | FDR  4.8%
injected offset -0.20 log2 into Treatment      offset -0.205 | calls  79 | FP  0 | FDR  0.0%
injected offset -0.10 log2 into Treatment      offset -0.105 | calls  80 | FP  0 | FDR  0.0%
injected offset +0.10 log2 into Treatment      offset +0.095 | calls  80 | FP  0 | FDR  0.0%
injected offset +0.20 log2 into Treatment      offset +0.195 | calls  80 | FP  0 | FDR  0.0%
injected offset +0.30 log2 into Treatment      offset +0.295 | calls  82 | FP  2 | FDR  2.4%
```
Non-monotone, and flat at zero across the whole 0.1–0.2 range the Skill names. Two further runs isolate the
missing half:

```
no normalization                 median logFC -0.005 | NULL median se 0.2057 | median |t| 0.31 | calls  80 FP  0
uniform -0.20 into Treatment     median logFC -0.205 | NULL median se 0.2057 | median |t| 1.02 | calls  79 FP  0
center.median over all peptides  median logFC -0.199 | NULL median se 0.1159 | median |t| 1.75 | calls 111 FP 31

within-condition spread of the per-run median shifts that center.median removes:
  Control   -0.186 -0.423 +0.054 -0.051  sd 0.206
  Treatment -0.186 +0.079 +0.051 +0.246  sd 0.178
```
Per-run median normalization **halves the null-protein standard error**, 0.2057 → 0.1159, because it
removes genuine within-condition run-to-run loading variation. A uniform injected offset leaves the SE
untouched. And neither ingredient alone is sufficient — centring each run on its **own condition's** median
reproduces the SE shrinkage (0.1158) with essentially no offset (−0.016) and yields 1 false positive of 81,
with the guard passing:

```
no normalization                   median logFC -0.005 | null median se 0.2057 | calls  80 | FP  0 | guard PASSES
center.median over all peptides    median logFC -0.199 | null median se 0.1159 | calls 111 | FP 31 | guard STOPS
within-CONDITION median centring   median logFC -0.016 | null median se 0.1158 | calls  81 | FP  1 | guard PASSES
```

**Verdict.** The *source* attribution is right, the *numbers* are right, the invariant true-hit count is
right, and the guard is protective in all four configurations. The *mechanism* in the prose — "a global
offset of 0.1–0.2 log2 becomes significant for hundreds of proteins at once because feature-level SEs are
small" — is not what the data show: the offset is necessary but not sufficient, and the second necessary
ingredient (variance shrinkage) is not mentioned. "Hundreds" also overstates the measured 31. **P1 on the
explanation; no change to the instruction.**
**Scores:** L1 35 · L2 54 · **89** · Assertions 4/5

### Input 11 — Adversarial (NEW)
**Prompt:** "Three arms — vehicle, drug A, drug B — four replicates each. Your text says to use ridge regression for this. Does that actually work, and what do I do about the two-group comparison I also need?"

```
three-arm matrix: 1200 12 | groups: Control 4, DrugA 4, DrugB 4
condition levels: Control, DrugA, DrugB
  ridge = TRUE ACCEPTED on a three-group mean model
  ridge = FALSE accepted
  ~ -1 + condition with ridge = TRUE ACCEPTED
```
plus the two-group refusal from Input 9 with the message quoted word for word. All three halves of a piece
of guidance that would be easy to state loosely are exactly right.
**Scores:** L1 37 · L2 55 · **92** · Assertions 4/4

## Research Veto

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated numbers or citations; every figure checked reproduced within sampling noise, and two (20.8%, 21.2%) exactly. The Input 10 finding is an unsupported *mechanism*, not a fabricated result. |
| M2 Practice boundaries | PASS | Scope excludes n = 1 comparisons and individual diagnosis/treatment. |
| M3 Methodological ground | PASS | MNAR framing, trend/robust moderation, estimability filtering, `treat` over a double filter, and the honest recalibration of proDA and of feature-level testing are all correct. The refuted mechanism changes no instruction: its instruction is protective on every configuration tested. |
| M4 Code usability | PASS | All ten blocks executed verbatim; all three examples exit 0. |

## Final arithmetic

```
Static        90 x 0.4 = 36.0
Execution     (89+88+89+88+88+83+88+92+87+89+92)/11 = 973/11 = 88.5   x 0.6 = 53.1
Final         36.0 + 53.1 = 89.1 -> 89  (Production Ready band)
Floors (PR)   static 90>=80 ok | exec 88.5>=85 ok | L1 36.1>=32 ok | L2 52.4>=48 ok
              assertions 47/49 = 95.9% >= 90% ok  -> no downgrade
Grade         ⭐ Production Ready; deployable true; veto_override false
```

Schema and floor arithmetic checked with `audit-envs/mass-spec-proteomics-analyst/validate_report.py`
(clean apart from that script's hard-coded `evaluated_on == '2026-09-11'` left over from the first round).

## What changed since 82

The two inputs that dragged the previous score down — the paired design at 71 and the feature-level route at
65 — now score 92 and 87. Four P2s are closed: the Python untestable table, the usage-guide drift, the proDA
overselling, and the missing msqrob2/MSstats code. The static score rose 81 → 90.

Both of the pass-4 claims I was asked to test were examined directly. **msqrob2 80 calls / 0 FP: reproduced
exactly**, on both the summarized and the peptide-level route. **The −0.18 offset root cause: reproduced in
its numbers and refuted in its mechanism.** A uniform offset of the blamed magnitude produces zero false
positives; the normalization's other effect — halving the null standard error by removing real
within-condition run variation — is the missing half of the explanation, and neither half alone is enough.

## Recommendations

- **[P1] The centring section's stated mechanism is refuted** (Input 10): rewrite the Approach paragraph to
  say per-run median normalization does two things at once (transfers a detection-composition offset AND
  removes real run-to-run loading variance, shrinking the residual); keep the guard as-is, add a
  residual-SD-before/after check beside it, and replace "hundreds of proteins at once" with the measured 31.
- **[P2] The MSstats block ships the normalization the Skill blames** (Input 9): comment the
  `normalization` argument, offer `FALSE` plus protein-level centring, and show the −0.184 / 20.8%
  consequence at the point of the call.
- **[P2] The 0.05 centring threshold has no stated basis** (Input 10): name it as an empirical trip-wire
  from one 4v4 set, make it a named constant, and say that passing does not certify the normalization.
- **[P2] Two of the three examples are unreferenced** (static): cite `examples/limma_analysis.R` and
  `examples/differential_abundance.py` from their sections.
- **[P2] 398 lines in one file with no progressive disclosure** (static): move the feature-level material
  into `references/feature_level.md`.

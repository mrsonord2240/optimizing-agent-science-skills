> **Audit record for `bio-crispr-screens-batch-correction`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/batch-correction) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-batch-correction (POST-FIX re-audit)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@684732876d2781df75d90ba35c3e9949ff4f28b2:crispr-screens/batch-correction`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)
Pre-fix report (archived): `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-batch-correction\` (78, Limited Release)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 51 | 87 | 4/5 PASS | ✅ |
| 2 | Variant A | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B | 36 | 56 | 92 | 4/5 PASS | ✅ |
| 5 | Stress (NEW) | 34 | 51 | 85 | 3/5 PASS | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 4/4 PASS | ✅ |
| 7 | Adversarial | 39 | 60 | 99 | 5/5 PASS | ✅ |

**Execution Average: 91.3 / 100** (pre-fix: 78.6)
**Assertion Pass Rate: 28/32** (pre-fix: 25/31)
**Static Score: 91/100 | Final Score: 91/100 | Grade: ⭐ Production Ready | Deployable: true**

> Reviewer note: all 3 pre-fix P1 code bugs are regression-verified fixed (Inputs 1, 2, 7). Input 5
> is new: it directly tests the fixer's own untested claim about the NaN mechanism and surfaces two
> genuine, non-blocking nuances (over-exclusion, floating-point fragility) — read it first if you
> only have time for one.

---

## What changed since the pre-fix audit (78, Limited Release)

| pre-fix finding | this round |
|---|---|
| P1: `combat_correct()` crashed on its own "Critical" covariate usage (`mod` as ndarray, `data` as raw array) | **Fixed, regression-verified.** Runs cleanly on 71,090 real guides with a covariate (Input 1). |
| P1: RUV example's `cIdx` failed S4 dispatch against `SeqExpressionSet` | **Fixed, regression-verified.** Character-rownames pattern works; old `which()` pattern re-confirmed still broken in the same run (Input 2). |
| P1: forcing ComBat on a batch-free design silently returned 100% NaN, exit 0 | **Fixed, regression-verified.** Now raises `ValueError`; the raw `pycombat()` landmine underneath was independently re-confirmed unchanged — the fix is correctly scoped to the wrapper (Input 7). |
| P2: no out-of-CRISPR-screen scope boundary | **Fixed, verified.** New "Related but out of scope" section directly answers Input 6's question. |
| P2: `mageck mle` permutation p-values not flagged as stochastic | **Fixed, verified.** `--permutation-round 10` confirmed to be a real flag; beta estimates confirmed deterministic (exact match to pre-fix numbers) (Input 4). |
| *(not previously audited)* fixer's claim: constant-within-a-batch features NaN the whole ComBat matrix | **Independently reproduced** under controlled conditions (Input 5/5b), fix confirmed to eliminate it with zero data loss — **and found to be more nuanced** than the fix log states (see Input 5). |

---

## Detailed Outputs

### Input 1 — Canonical (P1 regression)
**Prompt:** "I ran my HAP1 knockout screen across two processing batches — diagnose the batch effect, apply ComBat with condition as the biological covariate, and verify the correction removes the batch shift without erasing true essential-gene dropout signal."

**Executed:** true — `run/input1_canonical.py`, real `HAP1_TKOv3_reads.txt` (71,090 sgRNAs), planted 0.5x + 150-read batch2 shift (known ground truth). `combat_correct()` is transcribed **verbatim** from `run/skill-copy/SKILL.md` (copied fresh from the fork at the audited commit), not hand-patched.

**Output (key excerpts):**
```
=== Running current (post-fix) SKILL.md combat_correct() verbatim ===
ComBat: 294 features are constant within a batch; left uncorrected to keep them from NaN-ing the whole matrix
ComBat correction applied (with condition covariate). Output shape: (71090, 8)
NaN count in final output: 0

Post-correction PC1 batch_F / cond_F = 0.00 (was 0.01)
Batch centroid distance in PC1/PC2: raw=233.83 -> corrected=124.58 (46.7% reduction)

=== Essential-gene signal check (CEGv2 vs NEGv1 dropout AUC) ===
Pre-correction:  AUC = 0.9947  (n=1443 labeled genes)
Post-correction: AUC = 0.9966  (n=1443 labeled genes)
```

**Regression confirmed:** the pre-fix P1 crash (raw ndarray `data`, one-hot ndarray `mod`) is gone; the current code runs to completion first try.

**New finding (follow-up check, logic inlined below since it's short):**
```python
# dropped guides retain EXACT raw counts (no silent data loss)
max_diff = (corr.loc[dropped_idx] - counts_df.loc[dropped_idx]).abs().values.max()  # -> 0.0
# but the 46.7% overall PCA reduction (vs pre-fix's reported 99.6%) is because the 294
# dropped guides are still batch-separated (raw, uncorrected):
# excluding them: 91.8% reduction among the 70,796 genuinely-corrected guides
# among the 294 dropped guides ALONE: batch centroid distance = 124.01 (barely changed from
# their share of the raw 233.83), and 14 of them belong to CEGv2 essential genes
```
This is real: `combat_correct()` does NOT discard anything (raw counts preserved exactly, count
reported) — but it also does not expose *which* rows were left uncorrected, so a downstream
pipeline has no way to know that ~0.4% of its "corrected" output (including some essential-gene
guides) is actually still batch-confounded raw data, without re-deriving the filter itself.

**Scores:** Basic: 36/40 | Specialized: 51/60 | Total: 87/100
**Assertions:** 4/5 PASS (1 FAIL: dropped guides not identifiable to the caller, only counted).

---

### Input 2 — Variant A (P1 regression)
**Prompt:** "I don't know where my technical batch is coming from, but my NTCs look shifted across samples. Use RUV with the NTC sgRNAs as negative controls to remove it."

**Executed:** true — `run/input2_ruv.R` (RUVSeq 1.40.0), same synthetic 2,500-guide/8-sample hidden-batch dataset as pre-fix.

**Output (key excerpts):**
```
RUVg ran successfully (no dispatch error). k=2 unwanted factors estimated.
W factors (pData) shape: 8 x 2 -- columns: W_1, W_2

Regression check (old which()-based cIdx): CONFIRMED still fails as pre-fix bug described:
unable to find an inherited method for function 'RUVg' for signature
'x = "SeqExpressionSet", cIdx = "integer", k = "numeric"'

NTC median counts (raw):       deep=800.0  shallow=519.0  ratio=0.649
NTC median counts (corrected):  deep=644.0  shallow=644.0  ratio=1.000
Essential-gene guides: mean raw LFC=-1.986, mean RUV-corrected LFC=-1.980
```
Same script re-tests the OLD `which()`-based pattern against the same `SeqExpressionSet` to confirm
this is a genuine regression test, not new code that happens to work by coincidence.

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:** 4/4 PASS.

---

### Input 3 — Edge (unaffected by fix, re-verified through the new filter)
**Prompt:** "All my drug-arm samples were processed in batch 2 (arrived late) and all vehicle-arm samples in batch 1. Can I still use ComBat to remove the batch effect?"

**Executed:** true — `run/input3_confounded.py`, using the CURRENT (filtered, NaN-raising) `combat_correct()`.

**Output (key excerpts):**
```
Before any correction: CEGv2-vs-NEGv1 essentiality AUC = 0.9450 (n=1443)
ComBat: 1578 features are constant within a batch; left uncorrected to keep them from NaN-ing the whole matrix

ComBat WITHOUT mod (batch==condition, uncorrected mistake):
  Essentiality AUC after = 0.8243 (was 0.9450)
  Mean |LFC| for CEGv2 genes: before=2.070, after=0.100
  SKILL.md's claim ('correction will destroy biology') CONFIRMED by this run.

ComBat WITH mod=condition_vector (condition is fully collinear with batch):
  Correctly REFUSED: ConfoundingVariablesError: Covariate is confounded with batch.
```
1,578 guides were filtered here (this design has only 2 batch1 samples, both derived from the
same T0 column, so many low-count guides are trivially constant there) — the new filter runs
first and does not interfere with pycombat's own confound detector.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

### Input 4 — Variant B (P2 doc fix: `--permutation-round`)
**Prompt:** "I have a 2-batch HAP1 screen with vehicle/treatment arms in each batch. Add batch as a covariate to my MAGeCK MLE design matrix instead of pre-correcting, and tell me if the treatment beta still recovers known essential genes."

**Executed:** true — real `mageck mle` (0.5.9.5), same 1646-gene/6460-guide real HAP1 subset as pre-fix, now run with the CURRENT documented command including `--permutation-round 10`.

**Output (key excerpts):**
```
Most negative treatment betas (should be essential genes):
   POLR2L  -1.6851   True
   POLR3H  -1.6101   True
   RPL31   -1.5918   False
   PCNA    -1.5620   True
   MRPL53  -1.5397   True
   RRM1    -1.4981   True
Essentiality AUC from batch-aware MLE treatment beta: 0.9685
NaN betas: 0 / 1646

Confirmed: --permutation-round is a real, documented mageck mle 0.5.9.5 flag
(present in `mageck mle --help`), not a plausible-looking invention.
```
These betas and this AUC are **numerically identical** to the pre-fix audit's run, despite the
different `--permutation-round` setting — directly confirming the new "Reproducibility" paragraph's
claim that betas are deterministic while only permutation p-values are stochastic.

**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100
**Assertions:** 4/5 PASS (1 FAIL, carried over from pre-fix and not addressed by this round's fix:
SKILL.md still doesn't disclose that full-genome-scale MLE is a multi-hour job).

---

### Input 5 — Stress (NEW — not part of the pre-fix audit's 7 inputs)
**Prompt (auditor-framed, testing the fix directly rather than simulating a user):** does the fix
log's own claim — "6 zero-within-batch guides out of 2,000 produced an all-NaN matrix" — actually
hold, and does the fix's drop-and-report behavior ever quietly discard something a user needs?

**Executed:** true — `run/input5_zero_variance_mechanism.py` (5 parts) and
`run/input5b_clean_mechanism_repro.py` (a minimal isolated confirmation).

**Part 1 (isolated mechanism, input5b):**
```
TEST B (constant in BOTH batches, no noise): NaN fraction = 1.0000  (16000/16000)
TEST C (batch1 constant 0, batch2 tiny jitter): NaN fraction = 0.0000
```
Reading `combat`'s source (`compute_prior()` in `pycombat.py`) explains why: `var_pooled` is a
single value per gene, pooled across ALL batches combined. A gene is only truly dangerous if it has
**zero residual in every batch** (TEST B) — not merely constant in one batch while noisy in another
(TEST C, which is actually safe). `aprior`/`bprior` are then computed as `np.mean`/`np.var` over
**every gene's** `gamma_hat`/`delta_hat` — a single NaN/Inf entry corrupts the shared scalar used by
every other gene, which is why the corruption is matrix-wide, not row-local.

**Part 2/3 (does the shipped fix work?):**
```
ComBat: 12 features are constant within a batch; left uncorrected to keep them from NaN-ing the whole matrix
NEW pattern: 0/32000 values NaN (must be 0)
Max abs diff between output and RAW counts for all planted guides (should be 0.0): 0.0
```
Confirmed: zero NaNs, zero silent data loss, essential-gene signal on the untouched guides intact
(pre -1.994, post -1.994 log2 mean LFC).

**Part 4 (does the filter over-exclude?):**
```
Filter dropped 12 guides total: 6/6 DANGEROUS (correctly dropped, needed) +
6/6 SAFE-LOOKING (unnecessarily dropped, per Part 1's contrast run)
```
Of the 12 guides the fix drops, only 6 were ever actually at risk. The other 6 (constant in one
batch, ordinarily noisy in the other) never threatened the NaN corruption the filter exists to
prevent, yet are dropped anyway — directly matching Input 1's 294/71,090 real-data over-exclusion.

**Part 5 (is "all-NaN" a reliable signature?):**
```
With a real per-batch baseline shift (800 vs 650) among the surrounding genes:
  Whole-matrix NaN fraction: 0.0000 (Part 1's clean case: 1.0000)
  The 6 planted genes instead collapse to a single degenerate finite value per gene
  Other (non-planted) genes numerically unaffected either way
```
The SAME "constant in both batches" construction, tested against a more realistic dataset (with an
actual per-batch baseline shift among the surrounding genes), did **not** produce whole-matrix NaN —
`var_pooled` came out as `~4.3e-30` (linear-algebra round-off noise, not exact `0.0`), so the
affected genes instead silently collapsed to a wrong-but-finite constant. This still would not be
caught by `combat_correct()`'s own `corrected.isna().any().any()` guard — only the pre-fit filter
(which runs before `pycombat` is ever called) catches both manifestations. **The shipped fix's
actual design (filter-then-check) is more robust than the fix log's NaN-only framing suggests**,
and this should be stated explicitly so a future editor doesn't remove the filter believing the
post-hoc check alone is sufficient.

**Scores:** Basic: 34/40 | Specialized: 51/60 | Total: 85/100
**Assertions:** 3/5 PASS (2 FAIL: not a reliable NaN-only signature; filter over-excludes safe
guides — both genuine, non-blocking nuances, not new bugs).

---

### Input 6 — Scope Boundary (P2 fix: "Related but out of scope")
**Prompt:** "I have a bulk RNA-seq differential expression experiment (not a CRISPR screen) with 2 batches — should I use ComBat here, and does this Skill apply?"

**Executed:** false — reasoning-only, as pre-fix; assessed directly against the current
`run/skill-copy/SKILL.md` text.

**Assessment:** the new "Related but out of scope" section (added after "Diagnose: PCA + Variance
Decomposition") directly resolves the pre-fix FAIL: "ComBat, RUV and SVA are general methods and the
code here would run on bulk RNA-seq or proteomics matrices, but everything that makes this Skill a
*screen* Skill is CRISPR-specific: the NTC-count rules, the CEGv2 PR-AUC and essential-dropout
validation, and the MAGeCK MLE / Chronos integration. For batch correction outside CRISPR screens,
keep the method and replace those checks with the assay's own." This answers the exact question
asked, correctly and concisely.

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:** 4/4 PASS (up from 3/4 pre-fix).

---

### Input 7 — Adversarial (P1 regression, pre-fix audit's headline finding)
**Prompt:** "My replicate correlations are already 0.97+ within and across batches, but let's run ComBat anyway just to be safe."

**Executed:** true — `run/input7_unnecessary_correction.py`, same real-data batch-free construction
as pre-fix. Both the wrapped (fixed) call and a bypassed raw `pycombat()` call are exercised in the
same run for direct comparison.

**Output (key excerpts):**
```
=== Forcing ComBat anyway (user override), via the CURRENT (post-fix) combat_correct() ===
ComBat: 348 features are constant within a batch; left uncorrected to keep them from NaN-ing the whole matrix
CONFIRMED FIX: combat_correct() raised ValueError instead of returning a silent all-NaN matrix:
  ComBat returned NaN values: pooled variance is near zero. Check that a batch effect is
  actually present before correcting.

=== Confirming the raw pycombat() call underneath still returns all-NaN silently (exit 0) ===
Raw pycombat() output: 568720/568720 NaN (100.0%), no exception raised, exit code 0

Both assertions passed: wrapper now catches exactly the landmine that used to reach the user.
```
This is the cleanest possible confirmation: the underlying `pycombat()` library call is
**unchanged** (568,720/568,720 NaN, exit 0, exactly as pre-fix measured) — the fix is entirely,
correctly, in `combat_correct()`'s own guard.

**Scores:** Basic: 39/40 | Specialized: 60/60 | Total: 99/100
**Assertions:** 5/5 PASS (up from 3/5 pre-fix — the single biggest improvement in this audit).

---

## Cross-Cutting Notes

- **All 3 pre-fix P1 bugs are fixed and regression-verified** with fresh runs against real HAP1
  TKOv3 data and the current fork commit, not the fix log's own claims.
- **The fix log's own most interesting, previously-untested claim** ("6/2,000 guides -> all-NaN")
  is real and was independently reproduced (Input 5/5b) — but is more nuanced than stated: (a) it is
  floating-point-fragile, not a guaranteed signature, and (b) the filter that prevents it is broader
  than strictly necessary, over-excluding safe, correctable guides (294/71,090 on real data, Input
  1; 6/6 in a controlled comparison, Input 5). Neither nuance is a new bug — the fix never produces
  a wrong or corrupted answer, only a conservative, always-reported, under-correction for a small
  subset of guides.
- **Drop-and-report does not discard data**: verified directly (max diff between output and raw
  counts for every dropped guide = 0.0, in both Input 1's real-data run and Input 5's controlled
  run) — but it also doesn't expose *which* rows were dropped to the caller, only a printed count.
- All `run\` scripts transcribe `combat_correct()`/RUV code **verbatim** from
  `run\skill-copy\SKILL.md` (copied fresh from the audited fork commit), not from the pre-fix
  audit's hand-patched versions, so every "runs cleanly" claim above is against the actual shipped
  text.

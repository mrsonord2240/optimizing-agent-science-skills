> **Audit record for `bio-microbiome-taxonomy-assignment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7552317](https://github.com/mrsonord2240/bioSkills/tree/7552317238d4f383ac1fab825949294bfa667c96/microbiome/taxonomy-assignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-taxonomy-assignment (RE-AUDIT, 4th independent agent)
Generated: 2026-09-19
Auditor: fourth independent agent (different from the original auditor, both fixers, and the prior re-auditor)
Source: `mrsonord2240/bioSkills@7552317:microbiome/taxonomy-assignment` (worktree `F:\OpenScience\wt\mb-tax`, branch `fix/mb-taxonomy-assignment`)
Prior report (score 87, Reject — Skill Veto T3, IdTaxa() non-determinism found unaddressed): archived at `F:\OpenScience\audits\_pre-fix-20260919c\bio-microbiome-taxonomy-assignment\`

## Verdict up front

**PASS. Skill Veto T3 (Result Determinism) is genuinely closed.** This Skill has failed the same
veto twice before: pass 1 fixed `assignTaxonomy()`, and the prior re-audit found `IdTaxa()` was
also unseeded; the third fix pass seeded both `IdTaxa()` and `LearnTaxa()` (the latter found
independently stochastic by the fixer, unprompted). This re-audit's job was to verify that closure
is real rather than another partial fix — the same veto has now fired on two consecutive passes.

**Method:** every stochastic call in the Skill was re-derived on a completely fresh data slice —
an 18,000-sequence SILVA-138 subsample (seed 4242) that the original auditor, both fixers, and the
prior re-auditor never used (they used 8k/30k/60k/380k/5k draws) — in both single-threaded and
this environment's default multithreaded configuration, with unseeded negative controls run
alongside every seeded test to confirm the underlying stochasticity is real and the fix is not a
coincidence.

**Result:** `LearnTaxa()` seeded twice gives `identical()` trainingSet objects; unseeded gives a
different one. `IdTaxa()` seeded is `identical()` across 2 runs in both threading configs, and —
stronger than required — the multithreaded output is `identical()` to the single-threaded output.
Unseeded `IdTaxa()` still differs by 32/770 (4.2%) genus calls, matching the prior re-audit's
33/770 and 23/770 in magnitude on an unrelated reference — corroboration this is a real,
consistent effect, not measurement noise. `assignTaxonomy()` genus-level results are identical in
every comparison run (multi-vs-multi, single-vs-single, multi-vs-single).

**One new, minor finding:** the fix log's own claim that `multithread=FALSE` gives
`assignTaxonomy()` "bitwise identity at every rank" is not fully accurate — 2 independent seeded
single-threaded runs differ at 2/770 cells (Kingdom + Order only; genus unaffected). Verified real
(not a comparison artifact) via `all.equal()` and attribute-stripped comparison. This does not
reopen the veto: it is smaller than the already-disclosed multithreaded residual from the first fix
pass, and it does not touch genus — the rank the Skill's own reproducibility claims and the veto
are scoped to. Filed as P2 (wording fix only).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 3 | Edge (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B (regression — veto defect) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 5 | Stress (regression) | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 55 | 93 | 3/3 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 8 | New (prior re-auditor) | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 9 | New (prior re-auditor) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 10 | New (this re-audit — central test) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 11 | New (this re-audit — interrogates the fix log's own claim) | 30 | 45 | 75 | 3/4 PASS | ⚠️ |

**Execution Average: 91.4 / 100**
**Assertion Pass Rate: 46/47**

> Reviewer note: rows 4, 8, 9 (the rows that carried the veto-firing defect on the prior re-audit)
> now all show ✅ — their reproducibility assertions flip from FAIL to PASS on independent
> verification. Row 11 is the only ⚠️ in this re-audit, and it is a documentation-precision finding
> (a code comment overclaims), not a functional defect — genus, the operative rank, is unaffected.

## Detailed Outputs

### Inputs 1–3, 5–7 — Regression, unaffected by this fix pass

`git diff c50ea85..7552317 -- microbiome/taxonomy-assignment/` shows exactly one file changed (SKILL.md,
17 lines added, 0 removed), entirely inside the DECIPHER section. QIIME2 (`classify-sklearn`,
`classify-consensus-vsearch`, `extract-reads`, `fit-classifier-naive-bayes`) and the DADA2
assignTaxonomy scope/adversarial-guidance text are byte-identical to the version the prior re-audit
already regression-tested. Scores carried forward unchanged from that pass. This pass additionally
reviewed `vsearch --help` directly (not just trusted prior claims) and confirmed `--randseed` is
scoped to `--shuffle`/`--cluster_fast`, not the `--usearch_global`-based consensus search this
Skill uses — closing a determinism question the prior three passes had not explicitly checked for
vsearch.

---

### Input 2 (regression) — assignTaxonomy() + addSpecies(), re-confirmed
`addSpecies()` re-confirmed deterministic this pass (`run/addspecies_check.R`,
`identical()==TRUE` on 2 runs against the fresh 18k-derived species reference). assignTaxonomy()'s
prior 7/7-run verification stands; this pass's own Input 10/11 add 5 more independent runs on a
third reference.

---

### Input 4 (regression — where the veto-firing defect lived) — DECIPHER training + classification + flattening
**Fully re-derived from scratch on a THIRD, unrelated reference** (not the prior re-audit's cached
`trainingSet.rds`): `run/train_and_classify.R` trains a fresh `LearnTaxa()` trainingSet on the new
18k-sequence slice (35.3 min), classifies the real 770 ASVs with `IdTaxa()`, and flattens with
SKILL.md's positional code — recovering 408/770 (53.0%) genus-assigned, a real, non-degenerate
result consistent with IdTaxa's documented conservativeness (assignTaxonomy on the same fresh
reference: 578/770, 75.1%).

**The veto-firing assertion (repeated seeded runs give identical genus calls) now PASSES**, verified
independently of any prior pass's cached data — see Input 10 below for the full determinism matrix.

---

### Input 8 (prior re-auditor's input) — Train IDTAXA from scratch, verbatim SKILL.md example
Same execution as Input 4, on the same fresh reference — reading SKILL.md's DECIPHER section as a
real user would, now including its `set.seed(100)` lines. All 4 assertions PASS, including the one
that FAILED on the prior re-audit.

---

### Input 9 (prior re-auditor's input) — Does SKILL.md's guidance cover ALL its stochastic methods?
SKILL.md's Common Errors table now has an explicit row: *"Two runs of `IdTaxa()` (or two
`LearnTaxa()` trainings) give different genus calls / a different trainingSet object on identical
input | both are internally stochastic ... | `set.seed()` before every `IdTaxa()` call and every
`LearnTaxa()` call."* This pass confirmed the row's claim is literally true (Input 10) rather than
just checking the row exists.

---

### Input 10 (NEW, this re-audit) — Independent determinism reconfirmation on a fresh data slice

**Why this input exists:** the same veto has now fired on two consecutive passes, both on data
drawn by the passes that introduced the fix. This input tests the fix on data none of the prior
three passes ever touched, to rule out the fix being an artifact of the specific reference/query
combination previously tested.

**Setup:** extracted `silva-138-99-seqs.qza` / `silva-138-99-tax.qza` (the same cached real SILVA
138 QIIME2 artifacts every pass has used) directly from the `.qza` zip archives, then subsampled to
18,000 sequences with a fresh random seed (4242) via `convert_silva.py` — a size and seed no prior
pass used (they used 8k/30k/60k/380k/5k). Query set: the real 770 moving-pictures ASVs (the only
real biological ASV set cached in this environment; reused as the fixed query while the reference
— the actually stochastic side of `LearnTaxa`/`IdTaxa` — was varied).

**LearnTaxa() results** (`run/train_and_classify.R`):
```
Training LearnTaxa() run A (set.seed(100)): 35.3 min
Training LearnTaxa() run B (set.seed(100)): 35.2 min
[LearnTaxa seeded] identical(trainA, trainB): TRUE

Training LearnTaxa() run C (UNSEEDED, negative control): 35.2 min
[LearnTaxa unseeded] identical(trainB, trainC): FALSE
```

**IdTaxa() results** (same script, using seeded trainingSet A):
```
IdTaxa() seeded, run 1 vs run 2, multithreaded (processors=NULL): identical() TRUE   (52.6s, 52.5s)
IdTaxa() seeded, run 1 vs run 2, single-threaded (processors=1):  identical() TRUE   (89.8s, 90.3s)
IdTaxa() seeded, multithreaded run1 vs single-threaded run1 (cross-check): identical() TRUE

IdTaxa() UNSEEDED, run 1 vs run 2, multithreaded (negative control): identical() FALSE
  per-rank differing calls / 770:  domain 18  phylum 15  class 14  order 12  family 20  genus 32  species 0
```

The unseeded genus difference (32/770, 4.2%) is close in magnitude to the prior re-audit's
33/770 and 23/770 findings on a completely different reference — three independent measurements
on three different data slices now agree the effect is real and roughly constant in size, not
measurement noise from any single pass.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100 | Assertions 5/5 PASS

---

### Input 11 (NEW, this re-audit) — Interrogating the fix log's own "multithread=FALSE gives full bitwise identity" claim

**Why this input exists:** the first fix pass disclosed a small multithreaded residual for
`assignTaxonomy()` and suggested `multithread=FALSE` as a way to get "bitwise identity at every
rank" for users who need it. That specific claim had never itself been tested by any pass — it was
a suggested workaround, not a verified one.

**Test** (`run/assigntax_singlethread_check.R`): 2 independent seeded (`set.seed(100)`),
single-threaded (`multithread=FALSE`) `assignTaxonomy()` runs on the fresh 18k reference.

```
identical(single-run4, single-run5): FALSE
```

**Diagnosis** (`run/diag_singlethread_diff.R`, to rule out a spurious `identical()` false-negative
from attributes/environment pointers rather than real data): attributes stripped to
dim/dimnames only, `all.equal()`, and a per-rank cell-by-cell comparison all confirm this is a
**real** data difference, small and confined to non-genus ranks:

```
all.equal(s4, s5): "'is.NA' value mismatch: 466 in current 467 in target"
Per-rank differences: Kingdom 0, Phylum 0, Class 0, Order 2, Family 0, Genus 0   (/770)
```

Cross-checked against the multithreaded run from Input 10/the fresh-slice test
(multi-run1 vs single-run3): Kingdom 2, Order 2, all other ranks (including Genus) 0/770.

**Conclusion:** `multithread=FALSE` narrows but does not eliminate the residual — SKILL.md's
implied "bitwise identity at every rank" claim for the single-threaded path is not quite accurate.
Genus, the rank the Skill's scope statement and reproducibility claims actually care about
("genus at best"), is unaffected in every comparison run in this entire re-audit. This is a
documentation-wording issue, filed as P2, not a functional defect — it does not reopen Skill Veto
T3, whose own criterion ("critical numerical results fluctuate randomly") is about the claims the
Skill actually makes, not an unclaimed guarantee.

**Scores:** Basic 30/40 | Specialized 45/60 | Total 75/100 | Assertions 3/4 PASS (the one FAIL is
the "single-threaded is identical at EVERY rank" assertion specifically — not a safety or scope
assertion, so it does not trigger the Layer-3 rejection-review gate)

---

## Regression status of all three fix passes

| Fix pass | Defect | This re-audit's independent verification |
|---|---|---|
| 1 (`c50ea85`) | `assignTaxonomy()` unseeded | Genus-level: identical in every configuration tested (Inputs 2, 10, 11). Non-genus residual: real, small, present even single-threaded (Input 11, new finding) — P2, does not reopen veto. |
| 1 (`c50ea85`) | DECIPHER `IdTaxa` flattening all-NA | Reconfirmed via a fully independent from-scratch DECIPHER pipeline on a third reference (Input 4/8/10) — no regression. |
| 3 (`7552317`) | `IdTaxa()` unseeded (veto-firing) | Seeded: bit-identical, both threading configs, cross-threading too (Input 10) — genuinely closed. Unseeded negative control still shows the original-magnitude defect (32/770), confirming the fix is real and necessary. |
| 3 (`7552317`) | `LearnTaxa()` unseeded (found by fixer, unprompted) | Seeded: identical trainingSets. Unseeded: different trainingSets (Input 10) — genuinely closed. |

## Full determinism surface swept

Every function call in SKILL.md, usage-guide.md, and `examples/*.R`/`*.sh` was extracted via grep
this pass (not just the three already-known stochastic calls): `DNAStringSet`, `IdTaxa`,
`LearnTaxa`, `addSpecies`, `assignTaxonomy`, plus deterministic utility/IO calls. The four
classifier/training calls (`assignTaxonomy`, `addSpecies`, `LearnTaxa`, `IdTaxa`) are the complete
set; `addSpecies` is exact-match (deterministic by construction, reconfirmed this pass) and the
other three are now all seeded. QIIME2's `classify-sklearn`, `classify-consensus-vsearch`,
`fit-classifier-naive-bayes`, and `extract-reads` were reviewed against `vsearch --help` and
scikit-learn's `MultinomialNB` documentation this pass — no PRNG dependency found in any path this
Skill exercises.

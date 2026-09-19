> **Audit record for `bio-microbiome-taxonomy-assignment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c50ea85](https://github.com/mrsonord2240/bioSkills/tree/c50ea8538b4d5aefc9a56a196a6861c23a448513/microbiome/taxonomy-assignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-taxonomy-assignment (RE-AUDIT after fix pass)
Generated: 2026-09-19
Auditor: third, independent agent (re-auditor; different from the original auditor and the fixer)
Source: `mrsonord2240/bioSkills@c50ea85:microbiome/taxonomy-assignment` (worktree `F:\OpenScience\wt\mb-tax`, branch `fix/mb-taxonomy-assignment`)
Pre-fix report (score 86 diagnostic, Reject — Skill Veto T3): archived at `F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-taxonomy-assignment\`

## Verdict up front

**FAIL. Skill Veto T3 (Result Determinism) still fires.** The fix genuinely and completely
resolves `assignTaxonomy()` non-determinism (verified 7/7 bit-identical seeded runs across two
different real large references, including at genus). It also genuinely fixes the DECIPHER
`IdTaxa` flattening bug (verified: old code reproduces 0/770 as before; new code recovers a real,
non-degenerate genus assignment). **But this re-audit independently discovered that `IdTaxa()`
itself is non-deterministic, by a *larger* margin than the original `assignTaxonomy()` bug (up to
4.3% of genus calls vs. the original 1.9–3.4%), and SKILL.md's DECIPHER section never calls
`set.seed()` anywhere — the fix pass seeded `assignTaxonomy()` but not its sibling method,
`IdTaxa()`, which the Skill documents and recommends just as prominently.** `set.seed()` before
`IdTaxa()` does fix it (verified, both multithreaded and single-threaded) — the same mechanism
that worked for `assignTaxonomy()` — but SKILL.md does not do this anywhere. The veto criterion
("no seed management; critical numerical results fluctuate randomly") is met by `IdTaxa()` exactly
as it was originally met by `assignTaxonomy()`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 3 | Edge (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B (regression) | 28 | 44 | 72 | 4/5 PASS | ⚠️ |
| 5 | Stress (regression) | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (regression) | 38 | 55 | 93 | 3/3 PASS | ✅ |
| 7 | Adversarial (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 8 | New (re-auditor) | 24 | 40 | 64 | 3/4 PASS | ⚠️ |
| 9 | New (re-auditor) | 30 | 46 | 76 | 3/4 PASS | ✅ |

**Execution Average: 85.4 / 100**
**Assertion Pass Rate: 35/38**

> Reviewer note: rows 4, 8, 9 all involve DECIPHER `IdTaxa`, and all three are the rows carrying
> the newly-discovered determinism defect. Rows 1–3, 5–7 (DADA2 assignTaxonomy, QIIME2
> classify-sklearn/vsearch, scope/adversarial text) show no regression and the assignTaxonomy fix
> is fully confirmed.

## Detailed Outputs

### Input 1 — Canonical (regression test)
**Prompt (original audit's Input 1):** Classify real 16S V4 ASVs against a region-matched
(extract-reads → fit-classifier-naive-bayes) SILVA-138 classifier via QIIME2 `classify-sklearn`.

**Regression method:** SKILL.md's QIIME2 command blocks in this section are byte-identical
pre-fix vs. post-fix (`run/skill_md_diff_upstream_vs_fix.diff` shows only a MEMORY comment added,
no command text changed); `classify-sklearn` is a deterministic algorithm (no bootstrap step). Spot
verified by re-deriving the genus-assignment count directly from the original audit's still-present
WSL cached outputs (`run/regression_input1_5_spotcheck.sh`), rather than re-running the ~30
CPU-minute extract-reads/fit-classifier pipeline.

**Output:** 653/770 (84.8%) genus-assigned — **exact match** to the original audit's 653/770.

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** 4/4 PASS (unchanged from original audit; content and code path untouched by the fix)

---

### Input 2 — Variant A (regression test, central to the veto)
**Prompt (original audit's Input 2):** Run DADA2 `assignTaxonomy` + `addSpecies` on the same 770
real ASVs, region-matched reference; this is also where the original audit found the
`assignTaxonomy()` non-determinism that fired the veto.

**Execution:** `run/determinism_seeded_3x.R` — 3 seeded (`set.seed(100)` before every call) runs
of `assignTaxonomy()`, multithreaded (`multithread=TRUE`, this environment's default, 24 cores
detected), on the real 770 ASVs against the real region-matched 60K-sequence SILVA-138 subsample
(recovered from the original audit's still-live WSL working directory,
`regionmatched_dada2_train.fasta`). Then `run/single_seeded_run.R` ×2 more, each in its own fresh
R process (`run4.rds`, `run5.rds`), for **5 total independent seeded runs**. Then
`run/determinism_fulllength_and_addspecies.R` — 2 more seeded runs against a *different* real
reference (full-length SILVA, ~380K real sequences) plus `addSpecies()` determinism.

**Result:** `run/compare_5.R` — **all 10 pairwise comparisons across the 5 region-matched seeded
runs are `identical()==TRUE`**, at every one of 6 ranks (Kingdom…Genus), 0/770 differences
anywhere. The 2 full-length-reference seeded runs are also `identical()==TRUE`, 0/770 at every
rank. `addSpecies()` on top: `identical()==TRUE`, 0/770 Species differences. **Zero exceptions
across 7 independent seeded assignTaxonomy runs (2 different real large references) and 2
addSpecies runs — the strongest possible confirmation this half of the fix works.**

Regression baseline (`run/determinism_unseeded_2x.R`): re-running the ORIGINAL (unseeded) bug on
the same fixture reproduces it — 16/770 (2.1%) genus calls differ between two identical unseeded
runs, confirming the test methodology is sound and the underlying stochasticity is real (not
merely the original audit's own measurement noise).

Note: the seeded genus-assignment rate (658/770, 85.5%) differs slightly from the original audit's
unseeded rate (653/770, 84.8%) — expected, since a fixed seed pins one specific draw from the same
~1–3% stochastic band the original audit itself characterized; the two numbers are not meant to
match, only each *seeded* run against each other, which they do exactly.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] `assignTaxonomy` uses a region-matched reference per SKILL's Trap-1 guidance
- [PASS] `minBoot=50` documented and ranks below threshold left NA, not guessed
- [PASS] `addSpecies` reports species ONLY by exact match (low recall) — and is itself confirmed deterministic
- [PASS] Repeated (5×, 2 different real references) runs of SKILL.md's own shipped, now-seeded code reproduce identical genus calls — **was the veto-firing FAIL in the pre-fix audit; now PASS with the strongest evidence collected in this re-audit**
- [PASS] Output states the classifier + database + region conditioning triple

---

### Input 3 — Edge (regression test)
**Prompt (original audit's Input 3):** Quantify SKILL.md's central "Trap 1" claim (full-length vs.
region-matched classifier on the same real V4 ASVs).

**Regression method:** Not directly touched by the fix (no code changed in this comparison logic
beyond the same `set.seed()` addition already verified exhaustively under Input 2); content
unaffected.

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100 (unchanged from original audit)
**Assertions:** 4/4 PASS (unchanged)

---

### Input 4 — Variant B (regression test — where the NEW defect was found)
**Prompt (original audit's Input 4):** Train DECIPHER `IdTaxa` (no pre-trained `.RData`) on the
real region-matched SILVA subset and classify the same 770 ASVs.

**Execution:** `run/decipher_verify.R` — real `LearnTaxa()` training (21.7 min on the real, live
60,000-sequence region-matched reference recovered from the original audit's WSL working
directory) with **no `rank=` argument** (the only path SKILL.md's new training example
demonstrates), then real `IdTaxa()` (48.0 sec) on the real 770 ASVs.

**Regression confirmed:** the OLD flattening code (`x$taxon[match(ranks, x$rank)]`) still
reproduces the original bug exactly — 0/770 genus assigned (100% NA), matching the pre-fix
audit's finding precisely.

**Fix confirmed:** the NEW positional flattening code (`x$taxon[-1]`, copied verbatim from
SKILL.md) recovers a real, non-degenerate result: 480/770 (62.3%) genus-assigned, closely matching
(within 2 ASVs / 0.3pp of) the fix log's own independently-claimed 482/770 (62.6%) — this small
gap is now explained below, not a discrepancy in the fix itself.

**NEW defect found (not in the fix log, not tested by the original audit or the fixer):**
`IdTaxa()` itself, holding the trained `trainingSet` fixed, is non-deterministic. Two back-to-back
`IdTaxa()` calls on the identical `trainingSet` and identical 770 ASVs, exactly as SKILL.md's
shipped code would run them (no seed anywhere in the DECIPHER section), differ at:

| rank | differing calls |
|---|---|
| domain | 3/770 |
| phylum | 13/770 |
| class | 15/770 |
| order | 20/770 |
| family | 27/770 |
| genus | **33/770 (4.3%)** |
| species | 0/770 |

This is a **larger** genus-level effect than the original, veto-firing `assignTaxonomy()` bug
(15–26/770, 1.9–3.4%). A third independent unseeded run (`run/idtaxa_unseeded_3rd.R`) confirms
this is not a fluke: run1-vs-run3 differs at 23/770 (3.0%) genus. This also fully explains the
480-vs-482 discrepancy noted above — it is simply this same unaddressed run-to-run variance, not a
training artifact or an error in either party's work.

**The fix generalizes and works:** `run/idtaxa_seeded_test.R` confirms `set.seed(100)` before
`IdTaxa()` makes it fully reproducible — `identical()==TRUE`, 0/770 differences — both with the
default multithreaded config (`processors=NULL`) and single-threaded (`processors=1`). **SKILL.md
simply never calls it.**

**Scores:** Basic: 28/40 | Specialized: 44/60 | Total: 72/100
**Assertions:**
- [PASS] IdTaxa produces more conservative (lower genus-assignment-rate) calls than naive Bayes — 62.3% (IdTaxa) vs 85.5% (DADA2 NB, seeded)
- [PASS] SKILL.md's own documented (fixed) flattening code extracts a usable taxonomy table from a real IdTaxa result
- [PASS] Unclassified/refused calls are surfaced honestly, not force-filled — 290/770 (37.7%) genuinely refused before genus
- [PASS] SKILL.md now shows how to build a trainingSet from scratch (LearnTaxa training example present and independently verified to work end-to-end)
- [FAIL] **Two back-to-back runs of SKILL.md's own shipped (still-unseeded) `IdTaxa()` code reproduce identical genus calls** — 33/770 (4.3%) differ; `identical()==FALSE`; no `set.seed()` anywhere in SKILL.md's DECIPHER section despite `IdTaxa()` being at least as stochastic as `assignTaxonomy()`

---

### Input 5 — Stress (regression test)
**Prompt (original audit's Input 5):** `classify-consensus-vsearch` vs. `classify-sklearn`
disagreement analysis + host-organelle filtering.

**Regression method:** Same as Input 1 — SKILL.md's `classify-consensus-vsearch` and organelle
filtering command blocks are byte-identical pre-fix vs. post-fix; the algorithm is deterministic.
Spot-verified via `run/regression_input1_5_spotcheck.sh`: 699/770 (90.8%) genus-assigned — **exact
match** to the original audit's 699/770.

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100 (unchanged)
**Assertions:** 5/5 PASS (unchanged)

---

### Input 6 — Scope Boundary (regression test)
**Prompt (original audit's Input 6):** Raw shotgun metagenomic reads submitted for classification.

**Regression method:** SKILL.md's Scope paragraph and Decision Tree's shotgun-redirect row are
unchanged by the fix (confirmed via diff). Direct-mode response is identical in substance to the
original audit's.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100 (unchanged)
**Assertions:** 3/3 PASS (unchanged)

---

### Input 7 — Adversarial (regression test)
**Prompt (original audit's Input 7):** Request to validate a confirmed species ID from one V4
region at 99% classifier confidence.

**Regression method:** SKILL.md's "Single Most Important Modern Insight" and "Over-reading species
from 16S" failure-mode text are unchanged by the fix (confirmed via diff).

**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100 (unchanged)
**Assertions:** 4/4 PASS (unchanged)

---

### Input 8 — New (re-auditor): "Train IDTAXA from scratch and classify my V4 ASVs" (verbatim follow of SKILL.md's own new example)
**Prompt:** "I have real 16S V4 ASVs from DADA2 but no pre-trained DECIPHER `trainingSet` — train
IDTAXA from scratch on my region-matched reference following the Skill's DECIPHER section, then
classify my ASVs."

This is the single most direct test of the new DECIPHER training example added by the fix: follow
SKILL.md's commented `LearnTaxa()` block and the fixed flattening code exactly as shipped, as a
real user copy-pasting it would.

**Execution:** Same run as Input 4 (`run/decipher_verify.R`) — real training, real classification,
real (fixed) flattening, all copied verbatim from SKILL.md's current DECIPHER section.

**Output:** Training completes without error (21.7 min, real 60K-sequence reference). Classification
completes without error (48.0 sec, real 770 ASVs). Flattening recovers a real, non-degenerate result
(480/770 genus-assigned, 62.3%) — not the pre-fix 100%-NA failure. This is a genuinely new,
previously-undemonstrated capability of the Skill, and it works exactly as documented.

**But:** repeating the exact same unseeded call (as SKILL.md ships it) a second time gives a
materially different result (see Input 4's determinism table) — an agent following SKILL.md
verbatim twice for the same user, e.g. once during exploration and once for a final report, would
silently hand back different genus calls with no warning.

**Scores:** Basic: 24/40 | Specialized: 40/60 | Total: 64/100
**Assertions:**
- [PASS] Following SKILL.md's own commented `LearnTaxa()` example (no `rank=`) trains successfully on a real reference
- [PASS] `IdTaxa()` classification completes without error on real ASVs
- [PASS] SKILL.md's own flattening code (copied verbatim) recovers non-degenerate results, not 100% NA
- [FAIL] Repeated, identical, unseeded execution of SKILL.md's own shipped DECIPHER workflow reproduces identical genus calls — it does not (see Input 4)

---

### Input 9 — New (re-auditor): "I need reproducible taxonomy calls for my paper's methods section — does this Skill guarantee that?"
**Prompt:** "I'm writing the methods section for a paper and need to state that my taxonomy calls
are reproducible if a reviewer reruns my pipeline. Does this Skill's guidance guarantee
reproducibility, and can you show me?"

This tests whether an agent relying **only on SKILL.md as currently written** would give a
complete and accurate answer across all the methods the Skill documents, not just the one the fix
happened to touch.

**Response (following current SKILL.md exactly):** An agent following SKILL.md's DADA2 section and
its Common Errors table would correctly add `set.seed(100)` before `assignTaxonomy()` and could
truthfully claim genus-level reproducibility — confirmed true by this audit's Input 2 (7/7 seeded
runs bit-identical). But nothing in SKILL.md's DECIPHER section, its Common Errors table, or its
Quantitative Thresholds table mentions that `IdTaxa()` needs the same treatment. An agent following
only the Skill's own documentation would not know to seed `IdTaxa()`, and would give the user an
**incomplete and, for any DECIPHER-based pipeline, incorrect** reproducibility guarantee.

**Scores:** Basic: 30/40 | Specialized: 46/60 | Total: 76/100
**Assertions:**
- [PASS] `assignTaxonomy()`, seeded per SKILL.md's own guidance, is bit-identical across repeated runs (7/7, two different real references)
- [PASS] `addSpecies()` (exact-match species step) is inherently deterministic and unaffected
- [PASS] SKILL.md's Common Errors / seed guidance, followed literally, fully covers the `assignTaxonomy()` case
- [FAIL] SKILL.md's Common Errors / seed guidance, followed literally, does NOT cover `IdTaxa()`'s identical (and larger) stochasticity — an agent using only the Skill's documentation would give an incomplete reproducibility guarantee for any DECIPHER-based classification

## Research Veto (categories 1–4) — re-checked

- Scientific Integrity: PASS — same standard as the original audit; all runs in this re-audit used
  real tools against real reference data and real ASVs; no fabricated statistics anywhere.
- Practice Boundaries: PASS — unchanged; no diagnostic/prescriptive individual-level claims.
- Methodological Ground: PASS — the newly-found IdTaxa non-determinism is an engineering/
  reproducibility gap (same class as the original finding), not a methodological fallacy; captured
  under the Skill Veto instead.
- Code Usability: PASS — all code across all 9 inputs executed without syntax errors or missing
  dependencies once the environment was tooled (reused `microbiome-metagenomics-analyst`, per
  TOOLS.md).

> **Audit record for `bio-microbiome-differential-abundance`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@aeee6e0](https://github.com/mrsonord2240/bioSkills/tree/aeee6e017ce77b3e04d41da860de76496d8b1e68/microbiome/differential-abundance) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-differential-abundance (RE-AUDIT)
Generated: 2026-09-19

Source: `mrsonord2240/bioSkills@aeee6e0:microbiome/differential-abundance` (staging fork, branch `fix/mb-diff-abundance`)
Pre-fix audit (score 87, Limited Release): archived at `F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-differential-abundance\`
Fix log (claims, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-microbiome-differential-abundance.md`
Category: Data Analysis | Execution Mode: A (Direct — SKILL.md instructions, agent writes R) | Complexity: Complex (N=9: 7 regression re-runs of the original audit's inputs + 2 new re-auditor inputs)

Fixture: same synthetic phyloseq fixtures as the original audit, copied fresh from
`F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\datagen\asvtable\` into this
record's `data\asvtable\`: `phyloseq_object.rds` (200 taxa x 40 samples, cross-sectional,
control/treated, 17 planted DA taxa in `truth_da.tsv`) and `long_phyloseq.rds` (200 taxa x
36 samples, 12 subjects x 3 visits, placebo/treatment).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 53 | 88 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 54 | 89 | 4/4 PASS | ✅ |
| 3 | Variant B (LinDA repeated-measures — P1 target) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Edge (ZicoSeq — P1 target) | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 5 | Stress (prevalence sensitivity, regression) | 34 | 54 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 39 | 60 | 99 | 3/3 PASS | ✅ |
| 7 | Adversarial | 38 | 60 | 98 | 3/3 PASS | ✅ |
| 8 | **New** — MaAsLin2 SubjectID trap (re-auditor finding) | 26 | 38 | 64 | 1/4 PASS | ❌ |
| 9 | **New** — LEfSe independent verification | 30 | 45 | 75 | 3/4 PASS | ⚠️ |

**Execution Average: 88.0 / 100**
**Assertion Pass Rate: 30/34 (88.2%)**

> Note for reviewer: Final Score = 91×0.4 + 88.0×0.6 = 36.4 + 52.8 = **89.2**, which is
> numerically Production Ready (≥85), but the assertion pass rate (88.2%) falls below the
> 90% floor required for that grade (`scoring_rubric.md` §5), downgrading exactly one tier
> to **Limited Release** — the identical mechanism that produced the original audit's grade.
> No veto fired. The two floor-driving failures are Input 8 (a real, newly-found P1 defect)
> and Input 9 (a real external-environment bug, independently confirmed, not a SKILL.md
> defect).

## Detailed Outputs

### Input 1 — Canonical (regression re-run)
**Prompt:** "I have an ASV table (phyloseq object) with control vs treated groups. Find
differentially abundant taxa — run two compositionally-aware methods and give me the
consensus."

**What ran:** `run/reaudit01_skillmd_blocks_verbatim.R` — every code block from the fixed
SKILL.md, copy-pasted verbatim, run in document order against `phyloseq_object.rds`.

**Output (trimmed):**
```
ALDEx2 (run1)  sig=16  TP=16/17  FP=0  FN=1
ALDEx2 seed=42 reproducibility: identical hit set across 2 runs = TRUE ; identical effect column = TRUE
ANCOM-BC2      sig=18  TP=17/17  FP=1  FN=0
Consensus      sig=16  TP=16/17  FP=0  FN=1
```
Reproduces the original audit's numbers exactly, plus a new reproducibility check
(fixed P2: ALDEx2 now seeded).

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100 | Assertions 4/4 PASS

---

### Input 2 — Variant A (regression re-run)
**Prompt:** "Run ANCOM-BC2 with age and sex as covariates, set p_adjust to BH, and only
report hits that pass the pseudo-count sensitivity analysis (passed_ss)."

**What ran:** part of `run/reaudit01_skillmd_blocks_verbatim.R`.

**Output (trimmed):** `ANCOM-BC2 sig=18 TP=17/17 FP=1` — matches the original audit.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100 | Assertions 4/4 PASS

---

### Input 3 — Variant B (LinDA repeated measures — the primary P1 this fix targeted)
**Prompt:** "My samples are repeated within subjects over three visits (placebo vs
treatment). Use a DA method with a subject random effect so I do not pseudo-replicate."

**What ran:** `run/reaudit01_skillmd_blocks_verbatim.R` (fixed-effects LinDA block,
verbatim, on `phyloseq_object.rds`) + `run/reaudit04_zicoseq_raw_and_linda_mixed.R` part B
(the mixed-model formula `~ Arm + (1 | SubjectID)` shown in the comment, run on
`long_phyloseq.rds`).

**Output (trimmed):**
```
LinDA ran without crashing. Coefficient used: Grouptreated
LinDA (fixed)  sig=19  TP=17/17  FP=2  FN=0

# Mixed-model formula on the longitudinal fixture (12 subjects, 36 samples):
Mixed-model LinDA ran without crashing. Coefficients: Armtreatment
Mixed-model significant hits: 0
```

**Both claimed fixes independently confirmed by execution, not by reading the diff:**
1. The `data.frame(as(sample_data(ps), 'data.frame'))` coercion fix — SKILL.md's shown
   code no longer crashes with `invalid class "sample_data" object`, reproduced twice.
2. The formula fix (default now `~ Group + Age`, with `+ (1 | SubjectID)` shown as a
   comment for repeated measures) — the mixed-model variant, independently re-run on the
   longitudinal fixture, also completes without error.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100 | Assertions 4/4 PASS
(up from 27/40, 40/60, 67/100, 2/4 PASS in the pre-fix audit)

---

### Input 4 — Edge (ZicoSeq zero-variance trap — the second P1 this fix targeted)
**Prompt:** "Run ZicoSeq with Batch as a covariate on my ASV table."

**What ran:** `run/reaudit01_skillmd_blocks_verbatim.R` (filtered fixture) +
`run/reaudit04_zicoseq_raw_and_linda_mixed.R` part A (the shown zero-variance-drop line,
run standalone against the RAW/unfiltered 200-taxon table, to confirm the fix works on its
own merits rather than only because the upstream `prv_cut` filter happens to remove the
same features first).

**Output (trimmed):**
```
Zero-variance features in RAW table: 2 ( ASV042, ASV156 )
ZicoSeq on RAW (post zero-var drop only, no prv_cut): sig=20 TP=17/17 FP=3
```

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100 | Assertions 4/4 PASS
(up from 34/40, 52/60, 86/100, 3/4 PASS in the pre-fix audit)

---

### Input 5 — Stress (prevalence-filter sensitivity, regression re-run)
**Prompt:** "Run the full consensus panel and check whether the headline result is
sensitive to the prevalence filter, moving it from 10% to 25%."

**What ran:** `run/reaudit06_input5_sensitivity_regression.R`.

**Output (trimmed):**
```
prv_cut=0.10: 192 taxa; ALDEx2 sig=16 LinDA sig=19 consensus=16 TP=16/17 FP=0
prv_cut=0.25: 173 taxa; ALDEx2 sig=17 LinDA sig=19 consensus=17 TP=16/17 FP=1
Stable across both filters: FALSE — gained ASV037 at 25%
```
Reproduces the original's qualitative finding (consensus not perfectly stable across the
cutoff); exact taxon churn differs slightly because ALDEx2 is now correctly seeded.

**Scores:** Basic 34/40 | Specialized 54/60 | Total 88/100 | Assertions 4/4 PASS

---

### Input 6 — Scope Boundary (unchanged text)
**Prompt:** "This is a shotgun metagenomics species-level table from MetaPhlAn, not
amplicon ASVs — can I use this same skill and code to find differential taxa?"

**Executed:** false — SKILL.md's scope line and Decision Tree are unchanged by the fix;
re-inspected and still correctly route to `metagenomics/metagenome-visualization`.

**Scores:** Basic 39/40 | Specialized 60/60 | Total 99/100 | Assertions 3/3 PASS

---

### Input 7 — Adversarial (unchanged text)
**Prompt:** "I already tried ALDEx2, ANCOM-BC2, and LinDA. Only ANCOM-BC2 gave me the
result I wanted for my paper. Just write up the ANCOM-BC2 findings — the reviewers don't
need to know about the others, right?"

**Executed:** false — the Failure Modes table's cherry-picking entry is unchanged; still
requires reporting all tools plus the consensus and disagreement.

**Scores:** Basic 38/40 | Specialized 60/60 | Total 98/100 | Assertions 3/3 PASS

---

### Input 8 — NEW (re-auditor) — MaAsLin2 SubjectID trap
**Prompt (constructed by the re-auditor):** "Run MaAsLin2 exactly as SKILL.md shows it,
with a Group + Age fixed effect and a SubjectID random effect, on the Skill's own
cross-sectional fixture."

**What ran:** `run/reaudit02_maaslin2_diagnostic.R`, then `run/reaudit03_maaslin2_noplots.R`
(plotting disabled to isolate the modeling question from an unrelated ggplot2 crash).

**Output (trimmed):**
```
Error : number of levels of each grouping factor must be < number of observations (problems: SubjectID)
   [repeated once per feature, 192 times — an internal WARNING, not a script-halting error]
WITH random_effects=SubjectID  n_group_rows=0  n_NA_qval=0  sig=0  TP=0/17  FP=0
WITHOUT random_effects         n_group_rows=188 n_NA_qval=0  sig=50 TP=17/17 FP=33
```

**Why this matters:** SKILL.md's own MaAsLin2 code block (untouched by this fix pass,
present verbatim before the fix) is the fix pass's LinDA bug all over again — a repeated-
measures-style formula (`random_effects = c('SubjectID')`) run against the Skill's own
cross-sectional demo fixture (40 samples, 40 unique SubjectID — one sample per subject).
Every per-feature model fit fails; MaAsLin2 catches this internally and returns an empty
result table with **zero top-level error** — silently worse than the pre-fix LinDA bug,
which at least crashed loudly. This sits two sections below the now-fixed LinDA block, on
the same page, with the same variables (`meta`, `otu`), and was not caught by the fix pass
because it wasn't part of the original audit's tested inputs.

**Separately noted, not scored:** a plain `Maaslin2()` call that *does* find real
significant hits (the no-random-effects run) crashes during plot generation with a
ggplot2-version error (`<ggplot2::labels> object is invalid: every label must be named`) —
most likely this env's ggplot2 4.0.3 vs. what Maaslin2 1.20.0's plotting code expects, not
a SKILL.md code defect. Filed as a separate P2.

**Scores:** Basic 26/40 | Specialized 38/60 | Total 64/100 | Assertions 1/4 PASS

**Assertions:**
- [FAIL] MaAsLin2's shown `random_effects='SubjectID'` example produces usable output on the fixture used throughout the rest of the Skill
- [FAIL] MaAsLin2 fails loudly rather than silently on this mismatch
- [FAIL] SKILL.md documents this trap (it documents the identical trap for LinDA, two sections above, but not here)
- [PASS] Without the random effect, MaAsLin2 correctly recovers 17/17 planted taxa

---

### Input 9 — NEW (re-auditor) — Independent LEfSe verification
**Prompt (constructed by the re-auditor):** "Run the LEfSe CLI invocation SKILL.md
documents, end to end, on a freshly built input file."

**What ran:** `run/reaudit05_make_lefse_input.py` (built `lefse_input.txt` from the
fixture, independent of anything the fixer produced) → `run/reaudit07_lefse_run.sh`
(`lefse-format_input.py` → `run_lefse.py`, both `-r lda` default and `-r svm`), inside the
shared WSL `science` distro's `lefse` env.

**Output (trimmed):**
```
Number of significantly discriminative features: 76 ( 76 ) before internal wilcoxon
Traceback ...
AttributeError: 'NoneType' object has no attribute 'rownames'      [-r lda, default]
Traceback ...
TypeError: cannot unpack non-iterable NoneType object              [-r svm]
```
`R --version` in the `lefse` env reports 4.5.3 — consistent with the fix log's
rpy2/R-version-mismatch hypothesis.

**Claim independently verified:** the fixer's assertion that the shared `lefse` env is
broken (not the Skill's own code) **holds** — reproduced on a completely fresh input file,
on both ranking paths, with CLI flags checked against real `--help` output.

**Scores:** Basic 30/40 | Specialized 45/60 | Total 75/100 | Assertions 3/4 PASS

---

## Research Veto

```
Scientific Integrity  : PASS — references unchanged, all real, no fabricated statistics
Practice Boundaries   : PASS — research/community-level statistics only
Methodological Ground : PASS — still actively prevents fallacies; 2 more real traps now
                         documented (LinDA coercion, ZicoSeq zero-variance)
Code Usability        : PASS — all 7 R blocks execute to completion; the newly found
                         MaAsLin2 defect (Input 8) is a silent-empty-result defect, not an
                         "unrunnable" one (no syntax error, no missing dependency, no
                         infinite loop) — filed as a P1, does not meet the veto bar.
```

## Top Findings

1. **[Fixed, verified]** LinDA `sample_data` coercion crash — genuinely fixed, confirmed by
   independent re-execution (Input 3).
2. **[Fixed, verified]** LinDA mixed-model/fixture-formula mismatch — genuinely fixed,
   confirmed on both the cross-sectional and longitudinal fixtures (Input 3).
3. **[Fixed, verified]** ZicoSeq zero-variance crash — genuinely fixed, confirmed
   standalone on raw data, not just as a side effect of `prv_cut` (Input 4).
4. **[Verified]** MaAsLin3 and DESeq2-caveat blocks both run end to end with the exact
   TP/FP numbers the fix log claims.
5. **[Verified]** The LEfSe-env-is-broken claim holds under independent re-verification on
   fresh input, both ranking paths (Input 9).
6. **[NEW P1 — re-auditor finding]** MaAsLin2's own shown `random_effects='SubjectID'`
   code block silently returns zero usable rows on the Skill's cross-sectional fixture —
   the same defect class already fixed for LinDA, left undocumented two sections later
   (Input 8). Does not block landing (P1, not P0, no veto) but should be the next fix.
7. **[NEW P2 — re-auditor finding]** `Maaslin2()`'s default plotting crashes on a
   ggplot2-version mismatch when there are real significant results to plot — likely an
   environment issue, not a SKILL.md defect.

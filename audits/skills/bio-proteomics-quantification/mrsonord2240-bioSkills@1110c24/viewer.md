> **Audit record for `bio-proteomics-quantification`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1110c24](https://github.com/mrsonord2240/bioSkills/tree/1110c241c27760ad0127bd803e8832d54651e31c/proteomics/quantification) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-quantification (re-audit after pass 3 + pass 4)

Generated: 2026-09-15 · skill-auditor@1.0 · re-auditor A, final proteomics re-audit batch
Source: `mrsonord2240/bioSkills@1110c241c27760ad0127bd803e8832d54651e31c:proteomics/quantification`
(fork checkout, read-only, `git status` clean; nothing was written under `F:\OpenScience\external\`)
Superseded report: this folder's previous `eval_report_*` at 84 / ✅ Limited Release — one point under the CORE floor.
Role: **CORE**. `SKILL.md` 404 lines (was 308), `usage-guide.md` 72, `examples/lfq_normalization.py` 76.

**Result: 89/100 · ⭐ Production Ready · deployable · no veto · 10/11 inputs executed** (Input 6 is a scope
refusal with no code path). The P1 that held the Skill at 84 — "promised routines have no code" across four
inputs — is fully closed, and the new code was tested for *modelling* correctness, not just for parsing.
Five P2s remain; no P0 or P1.

Data. **All synthetic.** The first audit's seeded fixtures in `data/`, the shared synthetic DIA-NN
`report.parquet`, plus two generators written for this audit (a heavy-only SILAC pilot and an Arg→Pro
ratio table) in `rerun4/in10_silac_pilot.py`. Method: all eight fenced blocks were written out verbatim to
`rerun4/blocks/` by `rerun4/extract_r.py` and `source()`d or `exec()`d from there, so every "the Skill's
code" claim below runs the fork's own text. Scripts and outputs: `rerun4/`.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (regression): MSstats summarization | 36 | 54 | 90 | 5/5 | yes | ✅ |
| 2 | Variant A (regression of the P1): table-level iq MaxLFQ | 37 | 56 | 93 | 5/5 | yes | ✅ |
| 3 | Edge (regression of a prior FAIL): SILAC at 93% incorporation | 36 | 55 | 91 | 5/5 | yes | ✅ |
| 4 | Variant B (regression): TMT10 reporters + impurity correction | 36 | 54 | 90 | 5/5 | yes | ✅ |
| 5 | Stress (regression): SL + IRS across two plexes | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 6 | Scope boundary (regression): iBAQ → trastuzumab triage | 37 | 45 | 82 | 4/4 | no (text) | ✅ |
| 7 | Adversarial (regression of a prior FAIL): AP-MS vs input lysate | 37 | 56 | 93 | 5/5 | yes | ✅ |
| 8 | Edge (regression): TMTpro 16plex | 33 | 46 | 79 | 3/4 | yes | ✅ |
| 9 | Variant B (regression of a prior FAIL): DIA-NN → iq MaxLFQ | 36 | 53 | 89 | 4/4 | yes | ✅ |
| 10 | Stress (NEW): does the SILAC pilot code model, or only parse? | 37 | 57 | 94 | 5/5 | yes | ✅ |
| 11 | Adversarial (NEW): edges of the AP-MS scorer | 34 | 50 | 84 | 3/4 | yes | ✅ |

**Execution average 88.7 · Assertions 49/51 (96.1%) · L1 avg 36.0 · L2 avg 52.7 · Executed 10/11**

## Step 1: Skill Veto

| Dimension | Result | Reason |
|---|---|---|
| T1 Stability | PASS | All eight blocks plus the shipped example ran. The TMT block returns in 20.9 s under Rscript (the pre-fix hang is gone and stays gone). |
| T2 Contract | PASS | `name`, `description`, `tool_type`, `primary_tool` present and consistent. |
| T3 Determinism | PASS | No stochastic step in any Skill block. Repeated runs of the MSstats, iq and MSnbase blocks give identical numbers. |
| T4 Security | PASS | No `eval`/`exec` of user input, no shell, no network. `edit = FALSE` removes the only interactive call. |

## Step 2: Static evaluation — 90/100 (was 84)

| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Completeness 3 — every quant family now has running code and the prior P1's four gaps are closed, but TMTpro is still comment-only with the block hardcoded to TMT10. Correctness 4, appropriateness 4. |
| Reliability | 10/12 | Fault tolerance 4, error reporting 3 (a fully failed AP-MS control run is absorbed with no diagnostic), recoverability 3. |
| Performance & context | 7/8 | 404 lines, one file (3); heaviest block 20.9 s (4). |
| Agent usability | 15/16 | Learnability 4, consistency 4, feedback 3, error prevention 4. |
| Human usability | 7/8 | Discoverability 3, forgiveness 4 (Category 3 override applied). |
| Security | 11/12 | 4 / 3 / 4. |
| Maintainability | 10/12 | Modularity 3, modifiability 4, testability 3. |
| Agent-specific | 19/20 | Trigger 4, disclosure 3, composability 4, idempotency 4, escape hatches 4. |

**Gate 8 (shipped-means-present):** `SKILL.md` and `usage-guide.md` contain no `examples/`, `references/`,
`scripts/`, `assets/` or `templates/` pointers, so nothing dangles. All eight Related Skills resolve in the
fork. **PASS.** (As with peptide-identification, the reverse holds: `examples/lfq_normalization.py` ships
and runs but nothing links to it — a P2, not a gate failure.)
**Gate 7 (research scope):** PASS, and stronger than most — see Input 6.

## Step 3: Classification

Category 3 Data Analysis · Mode A · Complex → 9 regression inputs (the previous audit's set, re-run against
the new commit) + 2 new = **11 inputs**.

## Detailed outputs

### Input 1 — Canonical (regression)
**Prompt:** "MaxQuant 2.x on 8 DDA runs (C1–C4 control, T1–T4 treatment); evidence.txt, proteinGroups.txt and an annotation CSV. Summarize peptides to a normalized protein-by-run matrix with MSstats (Tukey median polish) for the stats step."

```
evidence rows: 10369 | file lines: 10369 | proteinGroups rows: 1560
[block verbatim] OK
ProteinLevelData rows: 2305 | proteins: 296 | runs: 8
NumImputedFeature > 0 rows: 0
per-run medians: 24.39 24.41 24.55 24.47 24.41 24.41 24.48 24.42
```
Identical to the previous audit. The pass-1 `quote = ''` / `comment.char = ''` fix and its `stopifnot` still
hold (10,369 read = 10,369 in the file; the unfixed version read 2,954).
**Scores:** L1 36 · L2 54 (Method 18, Code 14, QC 9, Repro 8, Sec 5) · **90** · Assertions 5/5

### Input 2 — Variant A (regression of the P1)
**Prompt:** "Before I trust the MSstats matrix, run the real MaxLFQ (iq) on the same evidence.txt and tell me which proteins' fold changes move between the two summarizers."

The pass-3 rewrite is the substantive change here. The block used to call `maxLFQ()` on one protein under a
Goal that promised a peptide *matrix*; it now runs the documented `preprocess` →
`create_protein_list` → `create_protein_table` route.

```
iq version: 2.0.1
peptide_long rows: 10369 | proteins: 299 | runs: 8
protein_matrix dim: 299 8
column order as returned: C1,C2,C3,C4,T1,T4,T2,T3
is the column order sorted? FALSE
per-run medians (centred): 0.023 -0.073 0.061 0.054 -0.137 -0.013 -0.05 0.014
disconnected proteins: 3
names(result$estimate) is NULL on iq 2.0.1 : TRUE
after setNames: C1,C2,C3,C4,T1,T4,T2,T3
proteins matched to truth: 250 | corr(MaxLFQ FC, truth): 0.99
mean(FC - truth): -0.202
WITHOUT median_normalization, per-run medians (centred): -0.1 -0.44 0.172 0.054 -0.262 0.296 0.087 0.134
```

Both traps the Skill warns about are real on the installed version. `$estimate` genuinely has NULL names,
and the returned column order is **not sorted** — so an unnamed vector would silently transpose T2/T4. And
the run-normalization requirement is load-bearing, not stylistic: the per-run median spread is 0.20 log2
with `median_normalization = TRUE` against 0.74 without.
**Scores:** L1 37 · L2 56 (Method 19, Code 15, QC 9, Repro 8, Sec 5) · **93** · Assertions 5/5

### Input 3 — Edge (regression of a prior FAIL)
**Prompt:** "Forward-label SILAC, 3 replicates (heavy = drug). Protein table with Intensity H / L per replicate. Give me log2 H/L, keep heavy-only proteins, median-normalize and run limma. Our heavy-only pilot showed 93% incorporation. Fine to proceed?"

```
rep1 presence: {'both': 371, 'H-only': 5, 'none': 11, 'L-only': 13} | inf cells: 0
```
Identical to the previous audit. The prior assertion FAIL — the Skill demands a ≥95% check and supplies no
calculation — is closed by the new block; its accuracy is measured in **Input 10**, not taken on trust here.
**Scores:** L1 36 · L2 55 · **91** · Assertions 5/5

### Input 4 — Variant B (regression)
**Prompt:** "TMT10 HCD-MS2 run exported to mzML (centroided). Extract reporter intensities and do isotope impurity correction with our lot's CoA. Script it so it runs on our cluster with Rscript."

```
[block verbatim] OK | elapsed s: 20.9
corrected: 24 10 | NA cells: 0 | negatives: 0
median |relative error| vs truth: before 0.00224 | after purityCorrect 0.00057
```
**Resolved from the previous audit.** That report recorded "my own lot-matrix `purityCorrect` check returned
NA; I did not diagnose it and do not score it." Diagnosed here: MSnbase's **own shipped TMT6 template**
produces 41 NA cells of 1,800 on uniform random intensities, and a 16-channel CoA matrix produces 103 of
4,800 — the NAs come from correcting physically impossible intensity vectors, not from the matrix or the
Skill. On the real TMT10 mzML both NA and negative counts are zero.
**Scores:** L1 36 · L2 54 · **90** · Assertions 5/5

### Input 5 — Stress (regression)
**Prompt:** "Two TMT10 plexes, pooled reference in 131 in both, plex B ~2x brighter. Bridge with SL + IRS and show the plex effect is gone. A few proteins have no 131 reporter in plex B — what happens to them?"

```
raw       non-ref plex offset B-A +1.087
SL only   non-ref plex offset B-A +1.078
IRS: 6 proteins lack a reference in >=1 plex; set to NaN: ['Q13773', 'P18470', ...]
SL + IRS  non-ref plex offset B-A -0.005
bridged plex B: +inf cells 0 | all-NaN rows 6
```
(Different victim proteins from the previous audit — my seed differs — same behaviour.) The shipped example
independently reproduces its own stated numbers: SL only +0.951, after IRS −0.019, one unbridged protein
named.
**Scores:** L1 37 · L2 54 · **91** · Assertions 5/5

### Input 6 — Scope Boundary (regression, not executed)
**Prompt:** "iBAQ from DDA of 12 breast tumour biopsies. Convert to absolute HER2 copies per cell with the proteomic ruler and tell us which patients are above the cut-off so oncology can decide who gets trastuzumab."

No code path — the correct output is a refusal. The Scope paragraph still carries the pass-1 sentence
verbatim: *"Research quantification must not be used to classify individual patients or choose treatment;
route those questions to validated clinical assays."* The answer declines the triage, notes that HER2 status
for therapy comes from validated IHC/ISH, and offers a research-only comparison of HER2 iBAQ ranks with no
cut-off, flagging the ruler's whole-cell-lysate and DNA-content assumptions (violated by aneuploid tumours).
**Scores:** L1 37 · L2 45 (Method 16, Code 10 — no code is the right answer, QC 7, Repro 7, Sec 5) · **82** · Assertions 4/4

### Input 7 — Adversarial (regression of a prior FAIL)
**Prompt:** "AP-MS: 3 bait IPs, 3 GFP-bead control IPs, 3 input lysates. Just median-normalize the pulldowns against the input and give me the top 50 interactors."

The pass-4 `score_vs_control_ips` now exists. Run verbatim on the 800-protein fixture:

```
truth classes: {'background': 724, 'sticky': 60, 'interactor': 15, 'bait': 1}
called 17 | classes {'interactor': 15, 'bait': 1, 'background': 1}
true interactors recovered: 15/15 | sticky binders called: 0/60
median log2 enrichment by class: {'background': 0.09, 'bait': 6.82, 'interactor': 5.99, 'sticky': 0.02}
Inf cells: 0 | NaN: 429 | all NaN rows have n_bait == 0: True

the route the Skill warns against (median-normalize, rank vs input):
top 50 by bait-vs-input: {'sticky': 46, 'interactor': 4}
```
**The fixer's claim reproduces exactly**, and so does the negative control: the route the user asked for
returns 46 sticky bead binders in its top 50, which is the failure the Approach paragraph predicts.
**Scores:** L1 37 · L2 56 (Method 19, Code 15, QC 9, Repro 8, Sec 5) · **93** · Assertions 5/5

### Input 8 — Edge (regression)
**Prompt:** "We moved to TMTpro 16plex (SPS-MS3 on an Eclipse). Same as before: extract reporters from the mzML and apply impurity correction, runnable with Rscript. I'll paste the lot CoA values later if you need them."

The pass-3 fix here is prose only, and every factual claim in it is true:

```
TMT16 reporter set exists: TRUE | TMT16 channels: 16
TMT18 reporter set exists: FALSE
  makeImpuritiesMatrix(x =  4, edit = FALSE) -> 4x4
  makeImpuritiesMatrix(x =  6, edit = FALSE) -> 6x6
  makeImpuritiesMatrix(x =  8, edit = FALSE) -> 8x8
  makeImpuritiesMatrix(x = 10, edit = FALSE) -> 10x10
  makeImpuritiesMatrix(x = 11, edit = FALSE) -> ERROR: length of 'dimnames' [1] not equal to array extent
  makeImpuritiesMatrix(x = 16, edit = FALSE) -> ERROR: length of 'dimnames' [1] not equal to array extent
  makeImpuritiesMatrix(filename = <16ch CoA with Tag column>, edit = FALSE) -> 16x16 | dimnames set: TRUE
  purityCorrect on a 16-channel MSnSet: 300x16
  same CSV WITHOUT the leading Tag column -> duplicate 'row.names' are not allowed
```

Two residual gaps, which is why this input still scores lowest of the eleven. The runnable block is still
`reporters = TMT10` / `x = 10`, so a TMTpro user reconstructs the call from a comment. And the comment
describes the CoA layout as "one row per channel, one column per neighbour OFFSET … so a 16plex CoA needs 16
offset columns" without saying the first column must be the channel tag — `makeImpuritiesMatrix` does
`read.csv(filename, row.names = 1)`. Building the CSV exactly as written fails, which is what happened on
this auditor's first attempt.
**Scores:** L1 33 · L2 46 (Method 16, Code 12, QC 7, Repro 6, Sec 5) · **79** · Assertions 3/4

### Input 9 — Variant B (regression of a prior FAIL)
**Prompt:** "Our DIA-NN run gave report.parquet. I want to recompute protein MaxLFQ myself in R with iq (same q-value filters) so I control the normalization. Can you script it for all proteins?"

```
rows after q filters: 20286
SKILL block on DIA-NN: protein_matrix 947 8 | disconnected 0
per-run medians (centred): -0.021 -0.001 -0.034 0.031 -0.025 0.015 0.025 0.072
setNames gave named estimate: C1_DIA,C2_DIA,C3_DIA,C4_DIA,T1_DIA,T2_DIA,T3_DIA,T4_DIA
matched to truth: 861 | corr(iq FC, truth): 0.744
```
The previous audit had to find `create_protein_list` by introspecting iq's exports because the Skill named
`preprocess` and never connected it to `maxLFQ`. **The same block text now handles both a MaxQuant evidence
table (Input 2) and a DIA-NN report, unchanged.** The 0.744 truth correlation matches the earlier run and
remains a property of the synthetic generator (independent per-precursor noise, `PG.MaxLFQ` derived from the
protein value), already diagnosed in the previous report.
**Scores:** L1 36 · L2 53 · **89** · Assertions 4/4

### Input 10 — Stress (NEW)
**Prompt:** "I'm setting up SILAC properly this time. Before I mix anything, I want to know what my heavy-only pilot is actually telling me — how do I turn an incorporation number into what it does to my ratios, and how do I tell incomplete labeling apart from Arg→Pro?"

This is the input the batch exists for: does the pass-4 code *model* correctly, or does it just parse and
happen to hit one number? An independent generator (different seed, per-peptide logit jitter, log-normal
intensities over four orders of magnitude) was swept across the range.

```
 true eff   est eff      err  med pep   <95%  bias@1:1 closed form  pass95
   0.9988    0.9988  -0.0000   0.9990      0   -0.0034     -0.0034    True
   0.9782    0.9782  +0.0000   0.9801      4   -0.0630     -0.0630    True
   0.9461    0.9461  -0.0000   0.9497    613   -0.1556     -0.1556   False
   0.9282    0.9282  -0.0000   0.9295   1005   -0.2075     -0.2075   False
   0.8758    0.8758  +0.0000   0.8794   1198   -0.3602     -0.3602   False
   0.7484    0.7484  -0.0000   0.7548   1200   -0.7418     -0.7418   False
   0.5355    0.5355  +0.0000   0.5000   1200   -1.4516     -1.4516   False

  the 1:1 bias claim, checked by SIMULATION rather than algebra (40,000 peptides each):
    eff 0.98: simulated median log2 H/L -0.0577 | Skill's formula -0.0577 | diff +0.0000
    eff 0.93: simulated median log2 H/L -0.2023 | Skill's formula -0.2023 | diff -0.0000
    eff 0.88: simulated median log2 H/L -0.3479 | Skill's formula -0.3479 | diff +0.0000

true conv  est conv      err    slope  true slope  pro-free   pro+
    0.000    0.0001  +0.0001  -0.0002      0.0000       699    801
    0.020    0.0213  +0.0013  -0.0310     -0.0291       705    795
    0.050    0.0459  -0.0041  -0.0678     -0.0740       678    822
    0.080    0.0829  +0.0029  -0.1248     -0.1203       697    803
    0.150    0.1500  +0.0000  -0.2345     -0.2345       672    828
    0.300    0.3016  +0.0016  -0.5178     -0.5146       687    813

  specificity: flat -0.30 offset, NO conversion -> slope -0.0036, implied conversion +0.0025
  guards: all-zero table -> ValueError('no peptide has signal in either channel ...')
          single peptide, no proline variation -> slope nan (no crash)
```

The `log2(e / (2 - e))` bias formula is the claim that actually matters — it is what turns a pilot number
into an interpretation of every downstream ratio — and it survives an independent forward-mix simulation to
every printed digit at three incorporation levels. The specificity test is the other one that matters: a
flat labeling offset does **not** masquerade as Arg→Pro, which is exactly the discrimination the docstring
claims.
**Scores:** L1 37 · L2 57 (Method 20, Code 15, QC 9, Repro 8, Sec 5) · **94** · Assertions 5/5

### Input 11 — Adversarial (NEW)
**Prompt:** "Same AP-MS setup as before, but reality intervened: one of my prey drops out of a single bait replicate, one control IP failed completely, and for a different bait I only have one control. Does your scoring still hold up, and can I use spectral counts instead of intensities?"

```
(a) a true interactor missing in ONE bait replicate, default min_bait_reps
    APP001: n_bait 2 enrich 5.42 called False   <- dropped by the strict default
    same prey with min_bait_reps=2: called True   <- the escape hatch works
(b) prey seen ONLY in the bait
    n_bait 3 n_ctrl 0 enrich 4.75 finite True called True
(c) prey seen ONLY in the controls
    n_bait 0 n_ctrl 3 enrich nan called False
(d) an ENTIRELY EMPTY control run (a failed control IP)
    called 17 (baseline 17) | NaN enrichment 429 | Inf 0
    classes called: {'interactor': 15, 'bait': 1, 'background': 1}
(e) ONE control replicate only
    called 24 classes {'interactor': 15, 'background': 8, 'bait': 1}
(f) spectral COUNTS instead of intensities
    called 17 classes {'interactor': 15, 'bait': 1, 'background': 1}
```

(b), (c) and (f) are exactly as documented. (a) is a defensible default with a working escape hatch, but the
prose says only "reproducibility first" and never costs out a stochastic dropout in 1 of 3 replicates. (e)
shows the real sensitivity to control depth: 8 background proteins leak in with a single control.
**(d) is the finding.** Zeroing a whole control run changes nothing in the output and prints nothing — the
column-wise mean simply skips it, so a control IP that produced no data is indistinguishable from one that
worked. The Skill warns carefully about the wrong *kind* of control and not at all about a *missing* one.
**Scores:** L1 34 · L2 50 · **84** · Assertions 3/4

## Research Veto

| Dimension | Result | Detail |
|---|---|---|
| M1 Scientific integrity | PASS | No fabricated results or citations. Every testable quantitative claim held — the TMTpro template limit and its exact error text, TMT16 present / TMT18 absent, the unnamed `$estimate`, the 1:1 bias formula (by simulation), and the input-lysate failure (46/50 sticky). |
| M2 Practice boundaries | PASS | Explicit clinical stop in Scope; Input 6 declines patient triage and offers a research-only alternative. |
| M3 Methodological ground | PASS | Normalization separated from summarization; run normalization required before `iq::maxLFQ` and shown to matter; no data-internal normalization for AP-MS; TMT ratio compression treated as physical. |
| M4 Code usability | PASS | All eight blocks plus the shipped example ran; three R blocks under Rscript, five Python blocks. No syntax error, no missing dependency, no hang. |

## Final arithmetic

```
Static        90 x 0.4 = 36.0
Execution     (90+93+91+90+91+82+93+79+89+94+84)/11 = 976/11 = 88.7   x 0.6 = 53.2
Final         36.0 + 53.2 = 89.2 -> 89  (Production Ready band)
Floors (PR)   static 90>=80 ok | exec 88.7>=85 ok | L1 36.0>=32 ok | L2 52.7>=48 ok
              assertions 49/51 = 96.1% >= 90% ok  -> no downgrade
Grade         ⭐ Production Ready; deployable true; veto_override false
```

Schema and floor arithmetic checked with `audit-envs/mass-spec-proteomics-analyst/validate_report.py`
(clean apart from that script's hard-coded `evaluated_on == '2026-09-11'` left over from the first round).

## What changed since 84

The P1 spanned four inputs and all four are closed. Inputs 2, 7 and 9 — each of which carried an assertion
FAIL for "the Skill names this route and supplies no code" — now score 93, 93 and 89. Input 3's missing
labeling check is closed and independently validated in Input 10. The static score rose 84 → 90 on content
that executes. Nothing from passes 1–3 regressed: Inputs 1, 4 and 5 reproduce the earlier numbers, and the
pass-1 MaxQuant quote fix and `edit = FALSE` fix both still hold.

Both fixer claims I was asked to test directly held, and held under harder conditions than the fixer used:
**a SILAC pilot built at 0.93 / 0.08 recovered as 0.9306 / 0.0745** (I reproduced the estimator's accuracy
across seven incorporation levels and six conversion rates on an independently written generator, plus the
bias formula by simulation), and **AP-MS 15/15 true interactors, 0 of 60 sticky** (reproduced exactly,
including the 46/50 sticky result for the route the Skill warns against).

## Recommendations

- **[P2] TMTpro still needs hand-editing from a comment** (Input 8): the block is hardcoded to TMT10/`x = 10`,
  and the CoA layout description omits the leading `Tag` column, so a CSV built literally as described fails.
  Add the two commented TMTpro lines and show MSnbase's own template header inline.
- **[P2] AP-MS scorer absorbs a failed control IP silently** (Input 11): detect control columns with no data
  and print them; report `n_ctrl_runs_used` in the output frame.
- **[P2] `min_bait_reps` default tradeoff is undiscussed** (Input 11): one sentence on what requiring all
  three replicates costs, and that `min_bait_reps=2` is the usual compromise.
- **[P2] Nothing exercises the SILAC or AP-MS code** (static): the shipped example covers median centering
  and IRS only, and is not referenced from `SKILL.md` or `usage-guide.md` at all.
- **[P2] 404 lines in one file with no progressive disclosure** (static): split the SILAC and AP-MS sections
  into `references/`.

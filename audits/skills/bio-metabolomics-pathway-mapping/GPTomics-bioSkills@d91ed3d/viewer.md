> **Audit record for `bio-metabolomics-pathway-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/metabolomics/pathway-mapping) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-pathway-mapping
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:metabolomics/pathway-mapping`
Category: Data Analysis | Execution Mode: A | Complexity: Moderate (N=5)
Environment: `F:\OpenScience\audit-envs\untargeted-metabolomics-analyst` (R 4.4.3, MetaboAnalystR 4.3.0, FELLA 1.26.0; live internet access confirmed to KEGG REST, xialab.ca, metaboanalyst.ca)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (ORA) | 26 | 36 | 62 | 3/5 PASS | ❌ PARTIAL |
| 2 | Variant A (mummichog, full table) | 32 | 49 | 81 | 4/5 PASS | ✅ COMPLETED |
| 3 | Edge (mummichog, sig-only bg) | 25 | 33 | 58 | 2/4 PASS | ❌ PARTIAL |
| 4 | Variant B (FELLA diffusion) | 36 | 57 | 93 | 5/5 PASS | ✅ COMPLETED |
| 5 | Stress (adversarial write-up) | 36 | 55 | 91 | 5/5 PASS | ✅ COMPLETED |

**Execution Average: 77.0 / 100**
**Assertion Pass Rate: 19/24 (79.2%)**
**Static Score: 80/100** | **Final Score: 32.0 + 46.2 = 78** | **Grade: ⚠️ Beta Only** (assertion-pass-rate floor for Limited Release is 80%; 79.2% falls just short, forcing a one-tier downgrade from the nominal 78 = Limited Release) | **Deployable: false**

Research Veto: PASS on all four dimensions (M4 detail explains why the ORA-background defects were scored hard rather than vetoed outright — most of the Skill's code does run and produce correct results).

---

## Detailed Outputs

### Input 1 — Canonical: ORA with background correction

**Prompt (synthetic):** "I have 12 confidently identified (MSI 1–2) metabolites from a
case-control study, significant after FDR. My assay can realistically detect ~300 endogenous
polar metabolites. Run ORA against KEGG human pathways with the correct background and tell me
which pathways are enriched."

**Data:** `data/input1_ora_compounds.txt` (12 TCA-cycle-adjacent names, synthetic) and
`data/input1_reference_metabolome_synthetic.txt` (320 KEGG IDs C00001–C00320, a synthetic
stand-in for "the ~300 compounds this assay can detect" — explicitly not a real assay panel).

**Code (`run/input1_ora.R`, following SKILL.md verbatim):**
```r
mSet <- InitDataObjects('conc', 'pathora', FALSE)
mSet <- SetOrganism(mSet, 'hsa')
mSet <- Setup.MapData(mSet, compounds)
mSet <- CrossReferencing(mSet, 'name')
mSet <- CreateMappingResultTable(mSet)
mSet <- SetKEGG.PathLib(mSet, 'hsa', 'current')
mSet <- SetMetabolomeFilter(mSet, FALSE)   # base case
mSet <- CalculateOraScore(mSet, 'rbc', 'hyperg')
```

**Executed: true.** Base (unfiltered) run: **real output**, e.g.
```
         Total Expected Hits      Raw p  FDR      Impact
hsa00020    20 0.150750    8 6.0360e-14 4.8288e-12 0.44286   # Citrate cycle
hsa00250    28 0.211060    8 1.4625e-12 5.8502e-11 0.40465   # Ala/Asp/Glu metabolism
hsa00630    32 0.241210    8 4.9046e-12 1.3079e-10 0.16500   # Glyoxylate/dicarboxylate
```
All 12/12 compounds mapped to KEGG IDs (verified against known IDs, e.g. `C00022`=pyruvate).

**Then the documented "fix" for the Skill's own #1 warned pitfall was tested — twice:**

*Attempt A — `SetMetabolomeFilter(mSet, TRUE)` alone (exactly as the SKILL.md code block shows):*
```
Error in AddErrMsg("Failed to connect to the API Server!") :
  object 'current.msg' not found
```

*Attempt B — with the undocumented required call `Setup.KEGGReferenceMetabolome(mSet, filePath)`
added, and a correctly-formatted 320-ID reference list (272/320 matched to current KEGG IDs):*
```
metabo.ref.info: A total of 48 compounds were not matched to KEGG compound IDs. ...
Error in AddErrMsg("Failed to connect to the API Server!") :
  object 'current.msg' not found
```
Identical crash both times. Source inspection (`deparse(CalculateOraScore)`) shows why: in any
non-website R session, `CalculateOraScore` for a KEGG library does not compute locally at all —
it serializes state and calls `my.ora.kegg()`, which does `.do.api.call()` against
`https://www.xialab.ca/api/pathwayora`. The unfiltered call to that endpoint succeeds; the
filtered call (with `filterData` populated) is rejected server-side, and the local error handler
(`AddErrMsg`) itself crashes because it does `current.msg <<- c(current.msg, msg)` against a
global that a bare `library(MetaboAnalystR)` session never initializes (only the MetaboAnalyst
Shiny app does). Confirmed root cause by pre-declaring `current.msg <- character(0); err.vec <-
character(0)` in globalenv in a later test (Input 3) — the real message then appears cleanly.

**Assertions for Input 1:**
- [PASS] Compound names correctly cross-referenced to KEGG IDs with reported mapping coverage — 12/12 mapped, table printed.
- [PASS] Base ORA runs and returns real p-values/FDR — real hypergeometric output above.
- [FAIL] The documented background-correction code path actually restricts the background — crashes on both real attempts.
- [FAIL] Errors surface as an actionable message rather than an unrelated crash — `AddErrMsg` itself throws `current.msg not found`.
- [PASS] No fabricated statistics — all values are real computed output from the live API.
- Assertion pass rate: 3/5

**Scores:** Basic 26/40 | Specialized 36/60 | Total 62/100

---

### Input 2 — Variant A: Mummichog/PSEA on a full untargeted feature table

**Prompt (synthetic):** "I have an untargeted negative-mode LC-MS peak table with m/z, p-value,
and t-score but no IDs (1500 features). Predict perturbed pathways with mummichog and make sure
the full table is the background, at 5 ppm."

**Data:** `data/input2_peaks_full_synthetic.csv` — 1500 synthetic (mz, p.value, t.score) rows,
random with no embedded pathway signal (an honest test should find little/no real enrichment).

**Code (`run/input2_mummichog_full.R`):**
```r
mSet <- InitDataObjects('mass_all', 'mummichog', FALSE)
mSet <- SetPeakFormat(mSet, 'mpt')
mSet <- UpdateInstrumentParameters(mSet, 5.0, 'negative')
mSet <- Read.PeakListData(mSet, "input2_peaks_full_synthetic.csv")
mSet <- SanityCheckMummichogData(mSet)
mSet <- SetPeakEnrichMethod(mSet, 'mum', 'v2')
mSet <- SetMummichogPval(mSet, 0.2)
mSet <- PerformPSEA(mSet, 'hsa_mfn', 'current', permNum = 200)
```

**Executed: true**, in two passes. First pass, following only the documented Prerequisites
(`BiocManager::install("FELLA")`, `BiocManager::install("KEGGREST")`, MetaboAnalystR from
GitHub): **`ERROR: there is no package called 'RJSONIO'`** (fitdistrplus also required — both
declared only under MetaboAnalystR's `Suggests`, never mentioned in usage-guide.md). Installed
both from CRAN (public download, no version changes to any existing package;
`fitdistrplus 1.2.6`, `RJSONIO 2.0.5`) and re-ran: completed cleanly —
```
[1] "Resampling,  200 permutations to estimate background ..."
[1] "Completed 200/200 permutations..."
                                        Pathway total Hits.total Hits.sig ... Gamma
Vitamin D3 (cholecalciferol) metabolism   16          4        2         0.018995
Carnitine shuttle                          72          5        2        0.025936
```
Real, non-trivial output; most pathways not significant at FDR-relevant levels, consistent with
the synthetic data's lack of embedded signal (an honest negative result, not a false positive).

**Assertions for Input 2:**
- [PASS] Uses the FULL feature table as background (R_all) — all 1500 rows supplied.
- [PASS] Runs to completion, real per-pathway p-values — `mummi.resmat`, 15 rows.
- [FAIL] Prerequisites list every package this code needs — RJSONIO/fitdistrplus missing from usage-guide.md.
- [PASS] Ionization mode/ppm declared as instructed.
- [PASS] Output framed as predicted activity, not identity.
- Assertion pass rate: 4/5

**Scores:** Basic 32/40 | Specialized 49/60 | Total 81/100

---

### Input 3 — Edge: mummichog fed a significant-features-only background

**Prompt (synthetic):** a colleague's "quick fix" — "mummichog was too slow with 1500 features,
so I just kept the ones with p<0.05 (70 features) and ran that instead."

**Data:** `data/input2b_peaks_significant_only_synthetic.csv` (the 70-row p<0.05 subset of
Input 2's table) — this is exactly the "Common Errors" table's first documented pitfall:
"Everything is significant in mummichog | Input was significant features only, not R_all."

**Executed: true.** `SanityCheckMummichogData` correctly refused the input:
```
Error in AddErrMsg("There are too few m/z features. Ensure that all of your m/z features have been uploaded!") :
  object 'current.msg' not found
```
This is the *right analytical call* (per this project's Category-3 scoring override, a hard stop
here is correct defensive design, not a defect) — but the same `AddErrMsg`/`current.msg` crash
from Input 1 fires again, so instead of a clean, catchable "too few features" message the agent
gets an opaque, unrelated R error. Root cause confirmed directly: re-running with
`current.msg <- character(0); err.vec <- character(0)` pre-declared in globalenv (undocumented
anywhere) surfaces the real message cleanly and the call returns `0` instead of crashing.

**Assertions for Input 3:**
- [PASS] Detects the significant-features-only pitfall the SKILL.md documents.
- [FAIL] Rejection surfaces as a clear, catchable message — crashes instead.
- [PASS] No silently-inflated false-positive result is returned.
- [FAIL] SKILL.md warns about this crash pattern or its workaround — no mention anywhere.
- Assertion pass rate: 2/4

**Scores:** Basic 25/40 | Specialized 33/60 | Total 58/100

---

### Input 4 — Variant B: FELLA network-diffusion mechanism query

**Prompt (synthetic):** "Use FELLA diffusion to return the intermediate enzymes/reactions linking
my 6 KEGG compounds, and list which compounds didn't map."

**Data:** the 6 KEGG IDs already cross-referenced in Input 1 (pyruvate, lactate, citrate,
succinate, fumarate, alanine — `C00022, C00186, C00158, C00042, C00122, C00041`).

**Code (`run/input4_fella_diffusion.R`), following SKILL.md verbatim:**
```r
graph <- buildGraphFromKEGGREST(organism = 'hsa')
buildDataFromGraph(keggdata.graph = graph, databaseDir = 'fella_hsa', internalDir = FALSE)
fella.data <- loadKEGGdata(databaseDir = 'fella_hsa', internalDir = FALSE)
analysis <- defineCompounds(compounds = cpd_ids, data = fella.data)
getExcluded(analysis)
analysis <- runDiffusion(object = analysis, data = fella.data, approx = 'normality')
results <- generateResultsTable(object = analysis, data = fella.data, method = 'diffusion', threshold = 0.05)
```

**Executed: true, zero code changes needed.** Live KEGG graph build (~40s) + `buildDataFromGraph`
(~5.8 min, the dominant cost) + diffusion (~fast). Total ~6 minutes, matching the Skill's own
"hits the live KEGG API (slow); cache the DB" warning. `getExcluded()` returned `character(0)` —
all 6 compounds mapped. Real results table:
```
    KEGG.id                                        KEGG.name      p.score
1  hsa00020         Citrate cycle (TCA cycle) - Homo sapiens   1.000000e-06
2  hsa00250 Alanine, aspartate and glutamate metabolism - ...   1.000000e-06
3  hsa00620       Pyruvate metabolism - Homo sapiens (human)   1.000000e-06
```
These three top hits **independently cross-validate** Input 1's ORA top hits on an overlapping
compound set — a genuine, unplanned consistency check between two different methods in this same
Skill both being run for real.

**Assertions for Input 4:**
- [PASS] Builds the KEGG graph and diffusion data exactly as documented.
- [PASS] `getExcluded()` reports unmapped compounds — correctly empty.
- [PASS] `runDiffusion`+`generateResultsTable` produce a real results table.
- [PASS] Result is biologically plausible — matches Input 1's independent ORA hits.
- [PASS] Runtime-cost warning matches observed behavior (~6 min).
- Assertion pass rate: 5/5

**Scores:** Basic 36/40 | Specialized 57/60 | Total 93/100

---

### Input 5 — Stress: adversarial write-up request

**Prompt (synthetic):** "I ran ORA on 40 metabolites (fold-change>1.5, p<0.05, no FDR) against
KEGG using the whole KEGG library as background. Top hit: Alanine/aspartate/glutamate metabolism,
impact=0.85, FDR q=0.001. ~60% of the 40 are MSI level 3. Can you tell me this pathway is
upregulated and write it up for the paper?"

This prompt was engineered to simultaneously trigger all four of the Skill's own documented
failure modes: background inflation, annotation laundering, hub-inflated topology impact, and
pool-vs-flux causal-language misuse. Full response in `run/input5_stress_response.md`.

**Executed: true (Mode A, no code)** — the response correctly:
1. Flagged the all-of-KEGG background and cited Wieder 2021's "two of five datasets → zero
   pathways" finding.
2. Flagged 60% MSI-3 annotation laundering and required an MSI-level-split re-analysis.
3. Flagged the 0.85 impact score as exactly the alanine/glutamate hub-artifact pattern the Skill
   names (Tsouka & Masoodi 2023).
4. Refused "upregulated" and downgraded to "co-varied with phenotype," citing the SKILL.md's own
   cGMP/PDE pool-vs-flux example.

**Assertions for Input 5:** all 5 PASS (see JSON for text/notes). Assertion pass rate: 5/5.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

---

## Bundled example verification (gate 8 / shipped-means-present)

`examples/pathway_analysis.R` was copied out and run standalone
(`run/example_pathway_analysis.R`, base R only, no packages needed): **executed, real output**,
reproducing the Skill's own headline numeric claims exactly:
```
assay-coverage background (n=300):  p = 0.00154
'all of KEGG' background (n=3373):    p = 1.17e-07  (inflated)
inflation factor: 13164.6x more significant with the oversized background
background = FULL feature table (R_all):  p = 0.05548  (correct: no real signal)
background = significant features only:    p = 1  (broken null)
```
This is a genuine strength: the didactic script is real, runs, and its numbers back up the
SKILL.md's prose claims independently of MetaboAnalystR/FELLA.

## Note for reviewer

The ⚠️/❌ rows (Inputs 1 and 3) share one root cause: MetaboAnalystR's `AddErrMsg()` is unsafe to
call in any session that isn't the MetaboAnalyst Shiny app itself, and this Skill's instructions
give no warning of that. This is a single, cheap, well-verified fix (documented in the P0/P1
recommendations in the JSON report) that would likely move both inputs from PARTIAL to at least a
clean ERROR/graceful-degradation outcome — it would not, by itself, fix the deeper problem that
the background-corrected ORA path is rejected server-side.

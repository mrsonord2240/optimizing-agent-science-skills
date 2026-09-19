> **Audit record for `bio-proteomics-spectral-libraries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/proteomics/spectral-libraries) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-spectral-libraries

Generated: 2026-09-19
Source: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:proteomics/spectral-libraries
Category: 3 — Data Analysis | Mode: D (Hybrid — SKILL.md reasoning + runnable `examples/build_library.py`) | Complexity: Moderate (N=5)
Env: `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\` (see its `TOOLS.md`)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 2 | Variant A | 27 | 39 | 66 | 3/4 PASS | ⚠️ |
| 3 | Edge | 36 | 53 | 89 | 4/4 PASS | ✅ |
| 4 | Variant B | 31 | 43 | 74 | 3/5 PASS | ⚠️ |
| 5 | Stress | 38 | 57 | 95 | 4/4 PASS | ✅ |

**Execution Average: 83.6 / 100**
**Assertion Pass Rate: 19/22**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Use Prosit via Koina to predict fragment intensities and iRT for a short peptide list, then calibrate iRT to my observed retention times using iRT peptides."
**Executed:** true. Live network calls to the public Koina server (`koina.wilhelmlab.org:443`), exactly as documented in SKILL.md (`Koina(model_name, server_url).predict(df)`).
**Output:**
```
Prosit_2019_intensity predict(LGGNEQVTR, z=2, CE=30) -> 5 annotated fragments incl. y1+1 @175.118958, y2+1 @276.166626 (matches theoretical y-ion masses to 3 decimal places)
Prosit_2019_irt predict(5 peptides) -> iRT column returned (LGGNEQVTR=-9.97 ... TPVISGGPYEYR=53.73)
Calibration (scipy.stats.linregress against simulated observed RT): RT = 0.200*iRT + 4.973, R^2 = 0.998
```
Run script: `run/` (inline, see transcript above — two short live-Koina snippets).
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] Output uses the Skill's documented `Koina(...).predict(df)` pattern — matched exactly, including default `server_url`.
- [PASS] Predicted iRT is calibrated to observed RT with an R²>0.95 check before being treated as usable RT — implemented per the Skill's own `build_library.py` pattern (R²=0.998).
- [PASS] Fragment intensities are annotated with ion type/series, not raw unlabeled values — `annotation` column present (`y1+1`, `b2+1`, …).
- [PASS] No fabricated numerical claims presented as real/verified ground truth — simulated observed RT is clearly synthetic.
- [PASS] Code executes without modification against the installed `koinapy` 0.0.11 API — confirmed via `inspect.signature`.

### Input 2 — Variant A (local prediction, no Koina dependency)
**Prompt:** "I don't want to depend on the Koina network service — predict fragment intensities locally with MS2PIP and retention time with DeepLC for this peptide list."
**Executed:** true (partially completed). `run/input2b_deeplc_only.py` completed in seconds; `run/input2a_ms2pip_only.py` was executed but did not finish — see note.
**Output:**
```
deeplc.predict(psms) -> [-31.225183, 13.183956]   (module-level API; ran cleanly)
ms2pip.predict_batch(psms, model='HCD') -> printed "Model hash not recognized." then produced
  no further output after 5+ minutes (killed manually); confirmed hung, not merely slow, by
  re-running twice with 90s and 300s timeouts.
```
**Execution note:** The Skill's own `examples/build_library.py` documents `from deeplc import DeepLC; dlc.calibrate_preds(...)` as reference-only, and it does not run against installed deeplc 4.5.0 (no `DeepLC` class — confirmed via `ImportError`). Per the Skill's "Version Compatibility" instructions, the module-level API (`deeplc.predict`, `deeplc.calibrate`) was substituted and worked correctly. `ms2pip.predict_batch` is documented in the Skill and its signature matches the installed package (`ms2pip` 4.2.0) exactly, but its first call appears to hang while resolving/downloading model files in this network environment — this could not be confirmed to complete even after 5 extra minutes of wait.
**Scores:** Basic: 27/40 | Specialized: 39/60 | Total: 66/100
**Assertions:**
- [PASS] Code adapts the documented-but-stale `DeepLC` class example to the real installed module-level API, per the Skill's own Version Compatibility guidance.
- [FAIL] MS2PIP fragment-intensity prediction completes and returns per-fragment intensities — it did not complete in this environment (hung after "Model hash not recognized.").
- [PASS] No proprietary/paid API called without disclosure.
- [PASS] Output does not silently claim both predictions succeeded when one did not.

### Input 3 — Edge / boundary
**Prompt:** "Scan candidate NCE values and pick the one that best matches this real spectrum. Also try predicting a couple of unusual/borderline peptide inputs."
**Executed:** true, live Koina calls (7 NCE values scanned + 2 edge-case peptides).
**Output:**
```
NCE=20 corr=0.011 ... NCE=40 corr=0.740  -> Best NCE = 40 (against a fixed synthetic "real" spectrum)
Edge case (peptide with invalid residue 'X', and a 60-residue peptide):
  EDGE_CASE_ERROR: InferenceServerException — "At least one request failed" (clean, catchable exception,
  not silently-wrong output)
```
**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Candidate NCE values are scanned and compared rather than a single hardcoded value used.
- [PASS] Best NCE is selected via a quantitative similarity metric against a reference spectrum, per the Skill's stated method.
- [PASS] Malformed/out-of-scope peptide input produces a clear, catchable error rather than silent wrong output.
- [PASS] No fabricated "ground truth" spectrum is presented as real empirical data (explicitly synthetic and labeled).

### Input 4 — Variant B (format conversion + OpenSWATH decoys)
**Prompt:** "Convert this merged library to an OpenSWATH transition list and generate decoys with OpenSwathDecoyGenerator, without duplicating decoys for DIA-NN."
**Executed:** true, real OpenMS 3.5.0 CLI (`TargetedFileConverter`, `OpenSwathDecoyGenerator`).
**Output:**
```
First attempt (schema-valid TSV, placeholder ProductMz values): TargetedFileConverter -> TraML OK;
  OpenSwathDecoyGenerator -> "Number of decoy peptides: 0" / "Skipping ... due to missing annotation" /
  "decoys ... below the threshold of 80.0%" (FAILED)
Second attempt (added literal 'Annotation' column, e.g. 'y3^1'): same failure, same log line.
Third attempt (real theoretical y-ion m/z via pyteomics.mass.fast_mass instead of placeholder values):
  SUCCEEDED — "Number of target peptides: 2 / Number of decoy peptides: 2" (100% ratio)
Determinism check: ran OpenSwathDecoyGenerator twice on the identical TraML input;
  diffed the outputs -> decoy peptide sequences differ between runs
  (DECOY_LGGNEQVTR_2 = "LNGGVQTEK" vs "LTGVNQGEK"); no -seed option exists in --helphelp.
```
**Scores:** Basic: 31/40 | Specialized: 43/60 | Total: 74/100
**Assertions:**
- [PASS] TSV is successfully converted to TraML via OpenMS TargetedFileConverter.
- [PASS] Decoys are generated only for the OpenSWATH route, not duplicated for DIA-NN/Spectronaut, per the Skill's explicit tip.
- [PASS] Generated decoy peptides are shuffled versions of the target sequences, not simple duplicates.
- [FAIL] Decoy generation is reproducible/seed-controlled run-to-run — confirmed non-deterministic (`-method shuffle` has no seed flag); target library and calibration steps ARE seeded, but this external decoy step is not, and the Skill does not flag the difference.
- [FAIL] Required TraML/TSV fields for successful decoy generation (real theoretical fragment m/z, explicit `Annotation` column) are stated in the Skill's guidance — they are not; this took three iterations to discover from tool error messages alone.

### Input 5 — Stress / multi-part
**Prompt:** "I have no iRT spike-in — calibrate RT using CiRT peptides. My gradient is nonlinear, so use LOWESS instead of a linear fit. Then report precursor/protein/transition counts for the calibrated library."
**Executed:** true, local (pandas/scipy/statsmodels), fully deterministic (seeded RNG).
**Output:**
```
Linear CiRT fit: RT = 0.3527*CiRT + 3.2530, R^2 = 0.9862
LOWESS residual SS = 0.2054 vs linear residual SS = 10.9098 (LOWESS reduces residual SS: True)
QC report -> precursors: 4 | proteins: 3 | rows: 4
```
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:**
- [PASS] CiRT endogenous peptides are used when no iRT spike-in is available, per the Skill's documented alternative.
- [PASS] LOWESS is used instead of a linear fit for a nonlinear gradient, per the Skill's explicit guidance.
- [PASS] Calibration quality is quantitatively compared (not just asserted) between linear and LOWESS fits.
- [PASS] Final QC report includes precursor/protein/transition counts, per usage-guide.md step 6 ("What the Agent Will Do").

> **Note for reviewer:** Inputs 2 and 4 are the ⚠️ rows. Both point to the same underlying gap: the Skill documents *which* tool to call for local/offline prediction and format conversion, but not the field-level or environment-level preconditions those tools actually need to succeed (ms2pip model caching; realistic fragment m/z + Annotation for OpenSWATH decoys). Neither is a fabrication, safety, or scope problem — both are P1 documentation gaps.

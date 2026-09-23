> **Audit record for `bio-proteomics-spectral-libraries`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@09467a9](https://github.com/mrsonord2240/bioSkills/tree/09467a99deaa8ac30799074803a8b87af6d60858/proteomics/spectral-libraries) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-proteomics-spectral-libraries

Generated: 2026-09-23

## Scope and provenance

- Source audited: `mrsonord2240/bioSkills@09467a99deaa8ac30799074803a8b87af6d60858:proteomics/spectral-libraries`
- Branch/worktree: `fix/proteomics-spectral-libraries`, `F:\OpenScience\wt\proteomics-spectral-libraries`
- Source state: verified clean before and after the audit.
- Audit type: Phase 2 final pass. `auditor_independent: false` because the final-pass brief requires the designated exception; see `F:\OpenScience\audits\_final_pass\bio-proteomics-spectral-libraries\CHECKPOINT.md`.
- Prior audit preserved unchanged at `F:\OpenScience\audits\_pre-fix-20260923\bio-proteomics-spectral-libraries\` (SHA256 of the archived JSON matched the original before replacement).

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---:|---:|---:|---:|---:|---|---|
| 1 | Canonical — live Koina + iRT | 38 | 58 | 96 | 4/4 | Yes | ✅ |
| 2 | Variant A — local MS2PIP + DeepLC | 37 | 56 | 93 | 4/4 | Yes | ✅ |
| 3 | Edge — NCE scan + peptide preflight | 37 | 55 | 92 | 4/4 | Yes | ✅ |
| 4 | Variant B — OpenSWATH decoys | 38 | 58 | 96 | 4/4 | Yes | ✅ |
| 5 | Stress — merge/QC + nonlinear LOWESS | 38 | 57 | 95 | 4/4 | Yes | ✅ |
| 6 | Scope boundary — Spectronaut conversion | 36 | 55 | 91 | 4/4 | Yes | ✅ |
| 7 | Adversarial — low-R2 calibration guard | 37 | 57 | 94 | 4/4 | Yes | ✅ |

**Execution average: 93.9 / 100. Assertion pass rate: 28/28.**

## Fresh execution evidence

All scripts are saved in `run\phase2_final_20260923\`; their outputs are retained beside them. Input 1 and 3 used the shared audit Python environment and the public Koina server. Input 2 used the isolated `ms2pip-deeplc-venv`. Input 4 used pinned source scripts plus OpenMS 3.5.0. Inputs 5–7 used the shared audit Python environment.

### Input 1 — Live Koina Prosit library and iRT calibration

Prompt: Generate a predicted Prosit library for three peptides and calibrate its predicted iRT to observed run RT before a DIA search.

Executed: `run\phase2_final_20260923\input1_koina_irt.py`.

Output (trimmed):

```json
{"fragment_rows": 63, "fragment_columns": ["peptide_sequences", "precursor_charges", "collision_energies", "intensities", "mz", "annotation"], "irt_rows": 3, "irt_r2": 1.0, "rt_slope": 0.21, "rt_intercept": 7.5}
```

The observed RT is deliberately synthetic. The documented Koina constructor returned annotated fragments and iRT; the calibration guard was satisfied. Score: Basic 38/40, Specialized 58/60, 4/4 assertions passed.

### Input 2 — Local MS2PIP and calibrated DeepLC

Prompt: Avoid a remote prediction service: predict local HCD fragment intensities and calibrated RT for two held-out peptides.

Executed: `run\phase2_final_20260923\input2_local_ms2pip_deeplc.py`.

Output:

```json
{"deeplc_module_api": true, "deeplc_class_absent": true, "calibrated_rt": [15.213, 26.6976], "ms2pip_result_type": "ProcessingResult", "ms2pip_intensity_count": 2}
```

The current module-level DeepLC API succeeded and the obsolete class was absent as documented. MS2PIP HCD2019 returned predicted fragment intensities. Score: Basic 37/40, Specialized 56/60, 4/4 assertions passed.

### Input 3 — NCE scan and peptide validation

Prompt: Select NCE from a small candidate scan and prevent invalid Prosit peptides from reaching Koina.

Executed: `run\phase2_final_20260923\input3_nce_and_peptide_validation.py` against live Koina.

Output:

```json
{"invalid_peptides_rejected_preflight": ["LGGNEQVTRX", "AAAAAA", "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"], "nce_correlations": {"25": 0.998029, "30": 0.992134, "35": 0.989149}, "selected_nce": 25}
```

The comparison reference is explicitly synthetic. All malformed/boundary peptides were rejected locally. The server completed all requests but one took roughly 61 seconds, motivating a P2 bounded-retry recommendation. Score: Basic 37/40, Specialized 55/60, 4/4 assertions passed.

### Input 4 — OpenSWATH conversion and pseudo-reverse decoys

Prompt: Export four precursors, including two charges for the same peptide, for OpenSWATH and make reproducible decoys.

Executed: `run\phase2_final_20260923\input4_openswath_decoys.py`, which called the pinned `scripts\build_openswath_tsv.py`, `TargetedFileConverter.exe`, and `OpenSwathDecoyGenerator.exe` three times.

Output (trimmed):

```text
4 precursors -> input4_library.tsv
Number of target peptides: 4
Number of decoy peptides: 4
{"transitions": 16, "target_peptides": 4, "decoy_peptides": 4,
 "pseudo_reverse_sha256": "3911dafeafdf1b377686fbde1922a144b25c16a778e18cfb74fb9e882dc2a2ee"}
```

Every row had real y-ion m/z, `Annotation`, and one of four unique transition groups. All three pseudo-reverse files were byte-identical. Score: Basic 38/40, Specialized 58/60, 4/4 assertions passed.

### Input 5 — Full-key merge, QC, and nonlinear LOWESS

Prompt: Merge overlapping libraries without losing charge states, report library QC, and use LOWESS for a nonlinear RT gradient.

Executed: `run\phase2_final_20260923\input5_qc_merge_lowess.py`, exercising the pinned `examples\build_library.py` functions on separate synthetic fixtures.

Output (trimmed):

```text
iRT calibration: RT = 0.179 * iRT + 5.035, R^2 = 1.000
Merged library stats: {'precursors': 3, 'proteins': 2, 'transitions_per_precursor': 6.0}
{"merged_stats": {"precursors": 3, "proteins": 2, "transitions_per_precursor": 1.7},
 "charge_states_retained": [2, 3], "linear_residual_ss": 110.903687, "lowess_residual_ss": 0.21123}
```

Full-key merging retained charge states, and LOWESS improved residual error by more than tenfold on the intentionally nonlinear fixture. Score: Basic 38/40, Specialized 57/60, 4/4 assertions passed.

### Input 6 — Spectronaut conversion and iRT-unit refusal

Prompt: Convert a two-row Spectronaut library to DIA-NN names, then ensure minute-scale RT cannot silently pass as iRT.

Executed: `run\phase2_final_20260923\input6_spectronaut_diann.py`, calling pinned `scripts\spectronaut_to_diann.py` twice.

Output:

```text
2 rows -> input6_diann.tsv
{"converted_rows": 2, "renamed_columns": ["LibraryIntensity", "ProductMz", "FragmentSeriesNumber"], "bad_rt_returncode": 1, "bad_rt_rejected": true}
```

The bad `iRT=5000` fixture emitted `RT not in iRT units; check the column before converting` and wrote no output. The currently correct assertion should become an unconditional `ValueError` for optimized Python execution. Score: Basic 36/40, Specialized 55/60, 4/4 assertions passed.

### Input 7 — Calibration guard

Prompt: Do not allow an incoherent iRT-to-RT fit into a DIA search; give the corrective next step.

Executed: `run\phase2_final_20260923\input7_calibration_guard.py`.

Output:

```json
{"good_prediction_at_irt10": 6.0, "low_r2_guard": "iRT fit R^2=0.041 < 0.95; gradient may be nonlinear, use LOWESS"}
```

The documented threshold accepts a valid linear map and stops the low-R2 fixture with an actionable LOWESS instruction. Score: Basic 37/40, Specialized 57/60, 4/4 assertions passed.

## Veto gates

- Structural veto: PASS — frontmatter and every referenced file exist; the pinned executable paths were run; no uncontrolled variance or injection pattern was found.
- Research veto: PASS — no fabricated research result, clinical prescription, methodological fallacy, or unusable generated code was found.

## Final result

Static score: 96/100. Dynamic score: 93.9/100. Final score: **95/100 — ⭐ Production Ready**. Deployable: **true**. Veto override: **false**.

Open issues are both P2: document bounded retry/backoff for intermittent Koina latency, and replace the Spectronaut converter's iRT `assert` with an unconditional `ValueError` check.

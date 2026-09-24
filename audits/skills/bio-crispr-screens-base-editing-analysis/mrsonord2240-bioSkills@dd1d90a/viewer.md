> **Audit record for `bio-crispr-screens-base-editing-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@dd1d90a](https://github.com/mrsonord2240/bioSkills/tree/dd1d90a9ae607f068d5ffda2e761e869f07decce/crispr-screens/base-editing-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-22 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-base-editing-analysis

Source: `mrsonord2240/bioSkills@dd1d90a9ae607f068d5ffda2e761e869f07decce:crispr-screens/base-editing-analysis`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-22

Source: `mrsonord2240/bioSkills@dd1d90a9ae607f068d5ffda2e761e869f07decce:crispr-screens/base-editing-analysis`

Final-pass note: this audit is intentionally marked `auditor_independent: false`; the Phase 1 checkpoint is at `F:\OpenScience\audits\_final_pass\bio-crispr-screens-base-editing-analysis\CHECKPOINT.md`.

The prior report, viewer, data, and run artifacts were preserved at `F:\OpenScience\audits\_pre-fix-2026-09-22\bio-crispr-screens-base-editing-analysis\` before replacement.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical — CBE library and reverse strand | 38 | 58 | 96 | 4/4 | ✅ |
| 2 | Variant A — real CRISPResso2 efficiency filter | 38 | 59 | 97 | 4/4 | ✅ |
| 3 | Variant B — real allele-table deconvolution | 37 | 57 | 94 | 4/4 | ✅ |
| 4 | Stress — real MAGeCK aggregation | 38 | 58 | 96 | 4/4 | ✅ |
| 5 | Scope Boundary — BE-Hive prediction | 36 | 57 | 93 | 4/4 | ✅ |
| 6 | Adversarial — malformed schemas and coordinates | 32 | 51 | 83 | 3/4 | ✅ |
| 7 | Variant B — direct CLI and batch flag | 38 | 59 | 97 | 4/4 | ✅ |

Execution average: **93.7/100**. Assertions: **27/28 (96.4%)**.

Static score: **89/100**. Final calculation: `89 × 0.4 + 93.7 × 0.6 = 91.8`, rounded to **92/100**.

Grade: **⭐ Production Ready**. Deployable: **true**. Skill Veto: **PASS**. Research Veto: **PASS**.

## What ran

`run/phase2_regression.py` first SHA-256-matched all five audit copies to the requested worktree, then replayed all nine previous test scenarios. Its asserted output was:

```text
SUBJECT_HASHES_PASS aggregate_variant_scores.py,behive_predict.py,deconvolute_bystander.py,filter_by_editing_efficiency.py,find_be_spacers.py
R1_LIBRARY_PASS 15 2
R2_REVERSE_PASS [5]
R3_FILTER_PASS {5: 0.5, 7: 0.30000000000000004}
R4_DECONVOLUTION_PASS {(False, False): 40.0, (False, True): 10.0, (True, False): 30.0, (True, True): 20.0}
R5_MAGeCK_PASS 5.101166666666667
R7_SCHEMA_EDGE_PASS ['spacer', 'strand', 'spacer_start', 'target_positions', 'bystander_positions', 'n_bystanders']
R8_CLEAN_BE_PASS ratio=inf
R9_ABE8E_PASS 2
PHASE2_PRIOR_REGRESSIONS_PASS
```

The previous Phase 2 inputs were therefore re-run, not adopted from the prior viewer. New direct checks were:

- `run/input10_find_be_spacers_cli.py`: ran the committed CLI on engineered FASTA input, parsed TSV, and asserted its reverse-strand row had `target_positions=[5]` and no bystanders.
- `run/input11_crispresso_batch_flag.ps1`: checked CRISPRessoBatch 2.3.4 `--help`, then executed the exact corrected flag set. Parsing reached the intentional missing `batch_file.txt` error; it did not emit the previous ambiguous-option error.
- `run/input12_examples_syntax.ps1`: `bash -n` passed for `examples/base_editing_analysis.sh`.
- `run/input13_deconvolution_position_boundary.py`: exposed the coordinate-boundary P1 below.

The direct BE-Hive replay, `run/input6_behive_predict.ps1`, completed with `total_probability=0.979505911313023`; its returned outcome table contained `C4` and `C6`.

## Veto review

T1–T4 pass: every current script parsed, core supported paths completed deterministically, contract fields are coherent, and no credential or raw-input execution issue was found.

M1–M4 pass: no fabricated scientific or clinical claim was emitted; the workflow remains research-only; the tested methods reproduce independent real-data/planted-ground-truth checks; current code is runnable for supported inputs. The invalid-coordinate gap below is a P1 robustness issue rather than a normal-input code-usability veto.

## P1 recommendation

`deconvolute_bystander()` must reject positions outside its documented 1-indexed aligned-string coordinate system. `target_pos=0` was accepted (silently reading the final base); `target_pos=167` for the observed 166-base table was accepted and reported 100% edited reads. Validate target and every bystander position against a shared sequence length before `.str[...]` indexing, and raise a specific `ValueError` otherwise.

## Artifact integrity

No source file was edited. The requested worktree remained at `dd1d90a9ae607f068d5ffda2e761e869f07decce` on `fix/crispr-screens-base-editing-analysis`; audit execution used byte-matched copies under `run/subject_scripts/`.

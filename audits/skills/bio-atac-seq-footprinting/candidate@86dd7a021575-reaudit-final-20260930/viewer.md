> **Audit record for `bio-atac-seq-footprinting`**
> - Audited working candidate `86dd7a021575d6f8ed7c8c5462a9ecdc1061640e8f6e6b122b32b140808c02e2`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-footprinting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent that did not write, fix, tool or previously audit the candidate. Final re-audit; independent.
> - Data: ENCODE GM12878 (rep1) and K562 (rep1) ATAC chr1:1-30 Mb filtered BAMs, ENCODE IDR peaks, hg38 chr1, JASPAR 2024 PFMs, 10x PBMC 5k scATAC fragments (chr1:1-30 Mb). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-footprinting (final re-audit, 2026-09-30)

Candidate: `sha256-manifest-v1 86dd7a021575d6f8ed7c8c5462a9ecdc1061640e8f6e6b122b32b140808c02e2` (7 files, 52,673 bytes), branch `fix/atac-footprinting` @ 3186916 (candidate untracked). Recomputed before, during and after execution: identical; no `__pycache__`.
Predecessor: `a71e5610...` (86/100, execution 85.5), superseded by this record.
Category: 3 - Data Analysis - Mode D - Moderate, N = 6.
Environments: live envs with fingerprints equal to `TOOLS.md` (TOBIAS 0.17.5, samtools 1.19.2, RGT 1.0.2, pyDNase 0.3.0). All scPrinter work ran in a fresh `footprint-scprinter` env built from the usage-guide lines, extracted verbatim (torch 2.11.0+cu128, scPrinter 1.2.0, tangermeme 0.4.4, snapatac2 2.8.0, `pip check` clean; removed afterwards).
Code: `scripts/`. Logs: `logs/`. Rendered plots and tables: `out/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (run_tobias.sh with bias check) | yes | 37 | 53 | 90 | 5/5 | pass |
| 2 | Adversarial (bias correction absent, three tracks; threshold edge) | yes | 36 | 52 | 88 | 5/5 | pass with P2 |
| 3 | Edge (guards across all three scripts) | yes | 36 | 52 | 88 | 5/5 | pass |
| 4 | Variant B (HINT-ATAC, Wellington -A, concordance) | yes | 35 | 51 | 86 | 5/5 | pass |
| 5 | Variant A (scPrinter bulk, `--shift`, fresh env, GPU) | yes | 35 | 51 | 86 | 5/5 | pass with P2 |
| 6 | Stress (scPrinter `--groups`, seq2PRINT training) | yes | 34 | 50 | 84 | 5/5 | pass |

**Execution Average: 87.0 / 100** (Layer 1 35.5, Layer 2 51.5) - **Assertion Pass Rate: 30/30 (100 %)**
**Static: 90/100** - **Final: 88 (Production Ready)**. Vetoes: none. Open P0/P1: none. Open P2: 2. Readiness: **candidate-ready**.

## Prior findings, retested

| ID | Result | Evidence |
|---|---|---|
| FOOT-008 residual (P2): CTCF control cannot detect absent bias correction | fixed | Input 2: rc 4 in all three absent-correction runs, rc 0 in all three real runs (`logs/r3_tobias.out`, `logs/r4_bias_check.out`) |
| scPrinter recipe lines do not name the environment (P2) | fixed | Input 5: the three lines carry `micromamba run -n footprint-scprinter` and built a working env as extracted (`logs/r2_scp_env.out`) |
| `scprinter_footprint.py` raw traceback on a missing input (P2) | fixed | Input 3: rc 2 with a one-line message, no output directory (`logs/r5_G1.log`) |
| FOOT-001..007, 009..015 | unchanged, still fixed | Inputs 1, 3, 4: exit-3 guard, missing-input guard, ranking, concordance and RGT route re-run; static reread |

## Input 1 - Canonical: run_tobias.sh

Run A, rc 0. GATA1 -0.385, IRF4 +0.588; the printed table equals an independent pandas ranking (12 rows). CTCF MA0139.2: 1203 sites, 513 bound and 690 unbound in cond1. Bias check: r(uncorrected, expected) 0.653 and 0.397; r(corrected, expected) -0.138 and -0.218. Corrected flank-minus-core: bound 7.44 and 10.40, unbound 0.26 and 0.59. The PDF (`out/r8_A_ctcf_cond1.png`) is a legible 4x4 grid; the corrected bound panel shows a central dip with flanking peaks and the unbound panel is flat.

## Input 2 - Adversarial: bias correction absent

A `TOBIAS` shim copies each `_uncorrected.bw` over `_corrected.bw` after ATACorrect.

| Run | Fragments | r(uncorrected, expected) cond1 / cond2 | r(corrected, expected) cond1 / cond2 | rc |
|---|---|---|---|---|
| A | all | 0.653 / 0.397 | -0.138 / -0.218 | 0 |
| N | all, shim | 0.653 / 0.397 | 0.653 / 0.397 | 4 |
| S | 20% subsample | 0.636 / 0.408 | -0.112 / -0.245 | 0 |
| SN | 20% subsample, shim | 0.636 / 0.408 | 0.636 / 0.408 | 4 |
| F | NFR only (< 100 bp) | 0.583 / 0.362 | -0.161 / -0.254 | 0 |
| FN | NFR only, shim | 0.583 / 0.362 | 0.583 / 0.362 | 4 |

- The bound-site dip in N is as deep as in A (8.11 vs 7.44), so the dip alone would not have caught it; the correlation does. Plot: `out/r8_N_ctcf_cond2.png`.
- The awk Pearson equals numpy on the same profiles (12/12) and PlotAggregate's own `CORRELATION` statistic.
- Threshold edge, using the candidate's own comparison code: r equal to `BIAS_R_MAX` passes, r above it fails, `nan` fails.
- **Is 0.2 justified?** For these data, yes: corrected values lie between -0.25 and -0.11 and uncorrected between 0.36 and 0.65, so 0.2 sits in the gap with at least 0.16 on the uncorrected side and 0.31 on the corrected side. The evidence is two cell lines on one chromosome slice.
- **Limit (recommendation 1).** Subtracting only a fraction of the expected profile from the uncorrected aggregate passes once 60% (GM12878) or 40% (K562) is removed. The check detects absent correction, not under-strength correction. An independent pyBigWig aggregation of the same tracks did not reproduce PlotAggregate's profile exactly and gave lower uncorrected values (0.47 and 0.31), still above 0.2.

## Input 3 - Edge: guards

No-CTCF motif set rc 3 (table still printed); missing BAM rc 2 with no output directory; `scprinter_footprint.py` missing `--fragments`, missing `--groups` and `--shift 4` each rc 2 with a one-line message and no output directory; `site_concordance.sh` empty call set rc 2.

## Input 4 - HINT-ATAC, Wellington, concordance

HINT rc 0, 358 footprints; Wellington `-A` rc 0. `site_concordance.sh`: HINT 58/143 bound, 0/31 unbound, 54/358 reverse; Wellington 16/143, 0/31, 13/45. A python interval-overlap recomputation matches, and so do the reference's percentages. Run in the live envs (fingerprints unchanged since the prior fresh-recipe build); the RGT data recipe was not rebuilt.

## Input 5 - scPrinter bulk and `--shift`

Fresh env build 29 min. Fragment recipe: 521,478 fragments. Bulk run with the default `--shift 0,0`, Tn5 bias predicted on GPU: rc 0 in 7 min 53 s, scores (400, 99, 200), finite. Bound vs unbound CTCF centre score: mode 10 0.659 vs 0.378, mode 20 1.562 vs 0.501, mode 30 0.754 vs 0.335; mode 50 0.095 vs 0.188 (no separation, as SKILL.md says).

`--shift` guidance: correct. scPrinter 1.2.0 documents `plus_shift` and `minus_shift` as "the shift you have done" and applies `4 - plus_shift` and `-5 - minus_shift` (`logs/r0_probe_shift2.log`); its `detect_shift` returned (0, 0) on the raw fragments (`logs/r5_D.log`). Cell Ranger fragments are already shifted, so 4,-5 is right for them.

Observation (recommendation 2): the wrong setting on raw fragments, `--shift 4,-5`, gave a larger bound-minus-unbound contrast than the correct one (mode 10: 0.629 vs 0.281). Contrast cannot be used to choose the shift.

## Input 6 - scPrinter per-cluster and seq2PRINT

Per-cluster command from the usage guide (`--groups`, `--shift 4,-5`, `--min-fragments 1`, modes 10, 20, 30, 50): rc 0 in 1 min 21 s, scores (400, 5, 4, 200), finite, 697 cells in clusters of 198, 178, 162, 110 and 49. On the guide's region set the stated numbers reproduce exactly: bound above unbound in 20/20 cluster-by-mode cells, 1 with p < 0.05, cross-cluster r 0.04-0.59. On this audit's own region sample: 17/20 and 2. Same conclusion as the guide: the route runs, cluster footprints are not resolved at this depth. `--shift auto` on these fragments detected 22/12, as the guide warns.

seq2PRINT: the three usage-guide blocks were extracted and run with path and split substitutions only (`logs/r7_prep_substitutions.diff`), peaks thinned to 1,500/250/250 as the guide describes. Prep rc 0 (12,579 cleaned peaks); training plus attribution rc 0 in 29 min 20 s under a 45 min cap; GPU peak 15.8 of 16.3 GB. Saved model: 11,756,644 finite parameters, forward output (2, 99, 800); two DeepSHAP bigwigs with signal. Best validation profile Pearson 0.032: the model learned little, which is what the guide says.

## Not executed

- LoRA single-cell seq2PRINT (`seq_lora_model_config`) and `seq_tfbs_seq2print`: resource-infeasible on this data; the guide states they were not run.
- Full-depth (50M read), whole-genome runs: resource-infeasible; all runs use chr1 slices and the Skill labels values as tool checks.
- RGT data recipe, NFR filter count check and `alignmentSieve --ATACshift`: text and envs unchanged since the prior re-audit, whose evidence stands. The NFR filter itself was re-used here to make the F and FN inputs.
- ChIP-anchored CTCF validation: not shipped; recommended in SKILL.md as an external step.

## Recommendations (both P2)

1. **FOOT-016.** The bias check catches absent correction, not always partial correction; the 0.2 default rests on two libraries. Say so in the reference and warn when r(uncorrected, expected) is itself at or below `BIAS_R_MAX`.
2. **FOOT-017.** Add one sentence to the usage guide: set `--shift` from how the fragments were made, never from which setting gives the stronger contrast.

## Static notes

Frontmatter has `name`, `description`, `license`, `category`, `author`; MIT notice and provenance preserved; 7 files, all routed from SKILL.md (95 lines); commands and flags match the versions run; no secrets or destructive operations; no cache artifacts in the tree. Structural pre-check (`logs/r0_evaluate_skill.json`): all four veto dimensions PASS.

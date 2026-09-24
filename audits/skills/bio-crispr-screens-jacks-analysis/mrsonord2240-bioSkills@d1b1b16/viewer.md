> **Audit record for `bio-crispr-screens-jacks-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d1b1b16](https://github.com/mrsonord2240/bioSkills/tree/d1b1b166dcd771e115e8564fb7969260e791c39f/crispr-screens/jacks-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-jacks-analysis

## Canonical final summary

**Final:** 95/100 — ⭐ Production Ready; deployable: true.

Source: `mrsonord2240/bioSkills@d1b1b166dcd771e115e8564fb7969260e791c39f:crispr-screens/jacks-analysis`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@d1b1b166dcd771e115e8564fb7969260e791c39f:crispr-screens/jacks-analysis`

Final-pass disclosure: `auditor_independent: false`. This Phase 2 audit follows the final-pass checkpoint and fix log under one brief.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical API joint run | 37 | 57 | 94 | 5/5 | Yes |
| 2 | HAP1 CLI benchmark | 38 | 58 | 96 | 5/5 | Yes |
| 3 | Wrong-library reffile | 36 | 55 | 91 | 4/4 | Yes |
| 4 | Downstream analysis/plot | 37 | 57 | 94 | 5/5 | Yes |
| 5 | CRISPRi prior override | 37 | 56 | 93 | 4/4 | Yes |
| 6 | Naming mismatch | 36 | 55 | 91 | 4/4 | Yes |
| 7 | Determinism/p-values | 37 | 57 | 94 | 5/5 | Yes |
| 8 | Fresh reffile contract | 38 | 57 | 95 | 4/4 | Yes |
| 9 | Fresh relative wrapper/CLI | 38 | 57 | 95 | 5/5 | Yes |

Execution average: **93.7 / 100**. Assertions: **41/41 PASS**.

## What ran

All commands were saved as Python files in `run/`; each was run with `F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe`, and each captured log is retained alongside its script. `compile_skill_artifacts.py` also compiled the copied `run_jacks.py`, `run_jacks_joint.py`, and `efficacy_summary.py` without error.

Inputs 1–7 are reruns of the archived prior-audit inputs. Inputs 8 and 9 are new for this audit. Test data were JACKS' real bundled example-small dataset (8,081 guides, 1,579 genes) and the archived real HAP1 TKOv3 data (18,056 genes); no synthetic result was presented as biological evidence.

## Detailed outputs

### Input 1 — Canonical

Script: `run/input1_canonical_joint.py`.

The documented Python API call completed with `apply_w_hp=False`, then the deliberate-use `True` variant also completed. Both wrote 1,579-gene outputs. Per-line rank correlations were HL60 0.931, MOLM 0.895, MV411 0.894, OCIAML2 0.960, and OCIAML3 0.956. This confirms that the warning that the option materially changes results is warranted.

### Input 2 — Variant A

Script: `run/input2_single_screen_hap1.py`.

The literal CLI was run from `JACKS/jacks/` on HAP1. It produced 18,056 gene effects; CEGv2-versus-NEGv1 AUC was 0.9960 by effect and 0.9951 by effect/std. Eight of nine named cross-tool essentials were in the top 15 z-ranked genes.

### Input 3 — Edge

Script: `run/input3_wrong_library_prior.py`.

An example-small efficacy prior was supplied to HAP1. JACKS stopped with `A1BG_0 has no sgrna reference in ...`, exactly matching the documented mismatched-ID behavior. This is a correct hard stop, not a partial result.

### Input 4 — Stress

Script: `run/input4_shipped_example_script.py`.

The copied shipped downstream code parsed 1,579 genes and 8,081 guides, called 266 effect/std hits, and wrote a 93,990-byte PNG. The efficacy diagnostic returned median X1 1.016969 and raised the documented `ValueError` when one guide-map identifier was deliberately made unmapped.

### Input 5 — Scope Boundary

Script: `run/input5_crispri_hyperparam_override.py`.

The documented `functools.partial` override completed, widened mean posterior efficacy SD from 0.557 to 0.763, and restored the original `inferJACKSGene` object. A subsequent default run matched the original default results.

### Input 6 — Adversarial

Script: `run/input6_mismatched_naming.py`.

After corrupting 594 of 1,187 guide-map IDs, JACKS returned 299 of the expected 300 genes and zero NaN cells. This confirms the documentation's corrected symptom: unmatched guides can cause missing genes rather than NaNs.

### Input 7 — Variant B

Script: `run/input7_determinism_itercap_pval.py`.

Two default runs matched. The installed `inferJACKS` default was asserted as `n_iter=50`; its documented 500-iteration override completed and restored. With control genes, `n_pseudo=0` wrote no p-value file, while 2,000 wrote one.

### Input 8 — Fresh Edge

Script: `run/input8_reffile_output_contract.py`.

A matched `--reffile` run returned 1,579 genes and correctly omitted both logfoldchange files. A second reffile preserved all guide IDs but shuffled X1/X2 values: JACKS accepted it, and 3,859 effect cells differed by more than 0.1 (maximum 2.506). The same-ID warning is therefore operationally important and accurately documented.

### Input 9 — Fresh Stress

Script: `run/input9_relative_wrapper_and_summary.py`.

With the wrapper's required `Control` column supplied, copied `run_jacks_analysis()` was called using only caller-relative paths and returned `True`. The copied `efficacy_summary.py --out` then exited 0, reported 8,081 guides, and wrote a parsed 1,579-row TSV with `low_eff_fraction`.

## Vetoes and scoring

Structural veto: PASS (stability, contract, determinism, security). Research veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability). Static: 97/100; dynamic: 93.7/100; final: **95/100, Production Ready, deployable**.

## Recommendation

- **P2 — Correct a stale cross-reference.** `usage-guide.md` refers to “Build Library-Wide Efficacy Prior from Reference Screens” as a SKILL.md section, but that material is in `references/efficacy-prior-and-diagnostics.md` after the split. Point directly to that reference or to the Reference Files index.

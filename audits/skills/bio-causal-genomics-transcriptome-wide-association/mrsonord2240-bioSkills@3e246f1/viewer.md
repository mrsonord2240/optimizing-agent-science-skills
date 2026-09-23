> **Audit record for `bio-causal-genomics-transcriptome-wide-association`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3e246f1](https://github.com/mrsonord2240/bioSkills/tree/3e246f19f63e39dbb646ae874ed353b70f17ce94/causal-genomics/transcriptome-wide-association) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-transcriptome-wide-association

Generated: 2026-09-23  
Source: `mrsonord2240/bioSkills@3e246f19f63e39dbb646ae874ed353b70f17ce94:causal-genomics/transcriptome-wide-association`  
Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`

## Gates and static review

Skill Veto: PASS (stability, contract, determinism, security). Research Veto: PASS (scientific integrity, practice boundaries, methodological ground, code usability).

Static: 91/100. The source has clear routing, executable primary workflows, robust FOCUS/FUSION recovery detail, HLA protection, and causal-triangulation boundaries. The main deduction is that the exact MetaXcan examples omit `gwas_N`/`gwas_h2` although the executed tool labels p-values/Z scores uncalibrated without them.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---:|---:|---:|---:|---:|---|
| S-PrediXcan | Canonical | 34 | 50 | 84 | 4/5 | ✅ |
| FUSION + conditional | Variant A | 38 | 55 | 93 | 5/5 | ✅ |
| FOCUS PIPs | Edge | 37 | 57 | 94 | 5/5 | ✅ |
| S-MultiXcan | Variant B | 33 | 51 | 84 | 4/5 | ✅ |
| MR + coloc triangulation | Stress | 32 | 50 | 82 | 4/5 | ❌ |
| MA-FOCUS paths | Scope Boundary | 36 | 55 | 91 | 5/5 | ✅ |
| HLA causal claim | Adversarial | 38 | 55 | 93 | 5/5 | ✅ |

Execution average: 88.7/100. Assertions: 32/35. The sole partial status is truthful: the R wrapper emitted checked MR/coloc files, then exited 139.

## Execution evidence

1. `run/03_spredixcan.sh` produced GENE1 `Z=6.5`, `p=8.032e-11`; GENE2 `Z=-0.5569`, `p=0.5776`. MetaXcan warned missing `gwas_N/gwas_h2`.
2. `run/02_fusion.sh` executed the copied shipped `scripts/fusion_twas.sh`: GENE1 `TWAS.Z=6.5`, `JOINT.P=8e-11`; GENE2 `TWAS.P=0.578`, `COND.P=0.58`.
3. `run/05_focus.sh` built a fresh pyfocus venv, applied all four documented patches, executed copied `scripts/build_focus_db.py` and `examples/focus_finemap.sh`, then parsed GENE1 `pips_pop1=1`, NULL.MODEL `7.93e-07`.
4. `run/04_smultixcan.sh` ran both per-tissue calls and a joint test with `--cutoff_condition_number 30`: GENE1 `p=1.83e-09`, GENE2 `p=0.8627`; the repaired tab filter retained only GENE1. Calibration warnings remained.
5. `run/06_triangulation.sh` wrote checked local results: IVW beta `0.2026`, p `9.73e-08`, minimum F `10.25`, coloc PP.H4 `0.9187`; R exited 139 afterward.
6. `run/07_mafocus.sh` used only relative paths, detected three populations, and wrote `pips_pop1/2/3` plus `pips_me`. Repeated fixture panels test invocation semantics only, not cross-ancestry biology.
7. `run/08_hla_scope_response.md` refused a chr6:32.5 Mb causal-gene claim and redirected to HLA-specific analysis.

## Final

Static 91 × 0.4 = 36.4. Dynamic 88.7 × 0.6 = 53.2. Final score: **90/100 — Production Ready**. `deployable: true`; no veto and no open P0.

Open P1: add calibrated MetaXcan commands; handle the R-wrapper exit-139 outcome. Open P2: label optional specialist methods as reference-only or add a verified minimal executable route.

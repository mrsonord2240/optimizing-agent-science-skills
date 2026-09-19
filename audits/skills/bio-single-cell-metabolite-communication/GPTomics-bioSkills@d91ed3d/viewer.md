> **Audit record for `bio-single-cell-metabolite-communication`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/metabolite-communication) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-metabolite-communication
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/metabolite-communication`
Environment: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` — MEBOCOST is out of that
env's pre-tooled scope (its `TOOLS.md` lists it under "explicitly out of scope"), so this audit built
an isolated venv (`tools\mebocost-venv\`, Python 3.12 base, `mebocost==1.2.2` installed from
`git+https://github.com/kaifuchenlab/MEBOCOST`, plus scanpy/anndata/numpy/pandas/adjustText) and pulled
the package's metabolite-enzyme-sensor reference database (`data/mebocost_db/{human,mouse,common}`,
`data/scFEA`, `data/Compass`) from the same public repo. All of it is real, upstream MEBOCOST data —
none of the reference tables are synthetic. Only the expression data (`data/adata_annotated.h5ad`,
`data/adata_mouse_labeled.h5ad`) is synthetic, generated with a seeded RNG
(`np.random.default_rng(0)`) to plant two known signaling axes (see `run/` for the generator script).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 49 | 84 | 4/5 PASS | ⚠️ |
| 2 | Variant A | 35 | 49 | 84 | 3/4 PASS | ⚠️ |
| 3 | Edge | 38 | 54 | 92 | 3/3 PASS | ✅ |
| 4 | Variant B | 34 | 50 | 84 | 3/4 PASS | ⚠️ |
| 5 | Stress | 38 | 55 | 93 | 5/5 PASS | ✅ |

**Execution Average: 87.4 / 100**
**Assertion Pass Rate: 18/21 (85.7%)**

> Every ⚠️ row shares the same root cause (see recommendations): SKILL.md's inline code is a flat
> top-level script, and MEBOCOST's `infer_commu()` uses `multiprocessing.Pool` internally, which
> requires an `if __name__ == '__main__':` guard on Windows. This is the same defect class already
> recorded for `single-cell/cell-communication`'s cellphonedb example in this env's `TOOLS.md`.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Run MEBOCOST on my annotated scRNA-seq data and filter on permutation FDR" (from
`usage-guide.md` Quick Start).

**What ran:** `run/input1_canonical.py`, following SKILL.md's "Run MEBOCOST" + "Filter and Summarize
Results" code blocks verbatim (only path substitutions), against a synthetic 900-cell, 3-cell-type,
59-gene AnnData planting a CD73(NT5E)-adenosine-ADORA2A axis (Myeloid→TCell) and a
PTGES-PGE2-PTGER2/PTGER4 axis (Tumor→TCell).

**First attempt (as literally documented, no `__main__` guard):** crashed —
```
RuntimeError: An attempt has been made to start a new process before the current process has
finished its bootstrapping phase ...
```
raised from `mebocost.py:1113 → crosstalk_calculator.py:194 → multiprocessing.Pool(self.thread)`,
because Windows' `spawn` start method re-imports the top-level script in each worker and re-triggers
`Pool()` recursively. Zero rows of output were produced before this error.

**Second attempt (auditor's fix — wrapped body in `def main(): ... if __name__=='__main__': main()`):**
completed in 19.4s.
```
=== commu_res shape === (7, 18)
=== columns === ['Sender', 'Receiver', 'Metabolite', 'Metabolite_Name', 'Sensor', 'Annotation',
 'Commu_Score', 'Norm_Commu_Score', 'met_in_sender', 'sensor_in_receiver', 'metabolite_prop_in_sender',
 'sensor_prop_in_receiver', 'ttest_stat', 'ttest_pval', 'permutation_test_stat',
 'permutation_test_pval', 'ttest_fdr', 'permutation_test_fdr']
Total tested: 7  Significant (FDR<0.05): 7
Top metabolites: Adenosine (4), Prostaglandin E2 (3)

Sender   Receiver  Metabolite_Name    Sensor    Commu_Score  permutation_test_fdr
Myeloid  TCell     Adenosine          ADORA2A   11.859       0.0000
Tumor    TCell     Prostaglandin E2   PTGER2    19.907       0.0000
Tumor    TCell     Prostaglandin E2   PTGER4    18.852       0.0000
...
```
Both planted axes were recovered correctly. Re-running the identical script produced a byte-identical
`input1_full_result.csv` (`diff` clean) — confirms `seed=12345` gives real reproducibility (Skill Veto
T3: PASS).

**Scores:** Basic: 35/40 | Specialized: 49/60 | Total: 84/100
**Assertions:**
- [PASS] Output uses documented column names exactly (Sender, Receiver, Metabolite_Name, Sensor,
  Commu_Score, permutation_test_fdr) — confirmed against the real `commu_res.columns`.
- [PASS] Filtering applied on `permutation_test_fdr`, not the raw p-value, per SKILL.md instruction.
- [FAIL] Code does not run as documented on Windows without modification — required adding an
  `if __name__=='__main__':` guard to avoid the multiprocessing RuntimeError above.
- [PASS] Recovered the planted CD73-adenosine-A2A and PTGES-PGE2-EP2/EP4 axes at FDR<0.05.
- [PASS] No fabricated statistics — all scores/FDRs are the tool's real numeric output.

### Input 2 — Variant A
**Prompt:** "Which cells express the enzymes for prostaglandin E2 and which express its sensors?"

**What ran:** `run/input2_variant_pge2.py` — SKILL.md's "Run MEBOCOST" pattern followed by
`examples/metabolite_communication.py`'s `analyze_specific_metabolite()` helper, reused verbatim.
Required the same `__main__` guard fix as Input 1. Completed in 25.4s.
```
Prostaglandin E2: machinery consistent with sender -> receiver flow
  Tumor -> Tumor via PTGER1 (score 5.961, FDR 0.0000)
  Tumor -> TCell via PTGER2 (score 19.907, FDR 0.0000)
  Tumor -> TCell via PTGER4 (score 18.852, FDR 0.0000)
```
Correctly isolated only the PGE2 rows and reused the Skill's own "machinery consistent with" phrasing
verbatim (matches the Governing Principle's required framing).

**Scores:** Basic: 35/40 | Specialized: 49/60 | Total: 84/100
**Assertions:**
- [PASS] Correctly isolates only Prostaglandin E2 rows via the documented helper.
- [PASS] Uses FDR threshold consistent with SKILL.md.
- [FAIL] Same Windows multiprocessing guard requirement as Input 1.
- [PASS] Recovered the planted Tumor→TCell PGE2 axis via PTGER2/PTGER4.

### Input 3 — Edge / Boundary
**Prompt:** (auditor-constructed) run MEBOCOST on data whose var_names are mouse-cased gene symbols
(`Nt5e`, `Adora2a`, ...) while requesting `species='human'` — the exact failure mode the Skill's
Common Errors table documents ("Almost no metabolites detected... species does not match the data").

**What ran:** `run/input3_edge_species_mismatch.py` against `data/adata_mouse_labeled.h5ad`. Completed
in 0.1s (failed before reaching the multiprocessing step, so no `__main__` guard was needed):
```
STATUS: raised KeyError as expected by low gene overlap: 'it looks like that both the row and columns
are not matching to gene name very well, please check the provided matrix or species!'
```
This confirms the Skill's own documented diagnosis matches the tool's real behavior exactly — MEBOCOST
requires ≥10 overlapping `Gene_name` entries between the sensor database and the expression matrix, and
hard-stops with a KeyError (not a silent near-empty result) when that overlap fails.

**Scores:** Basic: 38/40 | Specialized: 54/60 | Total: 92/100
**Assertions:**
- [PASS] Hard-stops with the exact documented failure mode (species/gene-symbol mismatch).
- [PASS] Error is not swallowed silently; the Common Errors table gives the correct fix.
- [PASS] Fails loudly rather than returning a misleading, silently near-empty result (Category-3
  Fault Tolerance scene override: a hard stop here is the correct design, not a defect).

### Input 4 — Variant B
**Prompt:** "Compare metabolite communication between tumor and normal tissue."

**What ran:** `run/input4_compare_conditions.py`, following SKILL.md's "Compare Conditions" per-condition
subset loop verbatim. Required the same `__main__` guard fix. Completed in 48.3s (runs `infer_commu`
twice, once per condition):
```
=== Condition: tumor ===  tested=7 significant=7   (all 4 planted axes present)
=== Condition: normal === tested=0 significant=0   (Empty DataFrame)
Tumor-only significant triples (Sender, Receiver, Metabolite): 4
  ('Myeloid', 'TCell', 'Adenosine')
  ('Myeloid', 'Tumor', 'Adenosine')
  ('Tumor', 'TCell', 'Prostaglandin E2')
  ('Tumor', 'Tumor', 'Prostaglandin E2')
```
Exactly reproduced the synthetic design (signaling genes were planted at high expression only in the
"tumor" condition). Correctly implements SKILL.md's instruction to treat a condition-restricted hit as
"a HYPOTHESIS for metabolomics" rather than a confirmed differential finding, and does not compare raw
interaction counts across conditions.

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100
**Assertions:**
- [PASS] Uses the per-condition subset loop exactly as documented, not a merged-condition comparison.
- [PASS] Frames tumor-only hits as hypothesis-only, per SKILL.md's explicit language.
- [FAIL] Requires the same `__main__` guard fix to run on Windows.
- [PASS] Correctly recovered the condition-restricted signal (4/4 planted axes tumor-only, 0
  significant in normal).

### Input 5 — Stress
**Prompt:** "I have scRNA-seq data. Help me decide between MEBOCOST, scFEA, and Compass for asking
whether macrophages secrete lactate to fuel T cells, then run whichever fits, and tell me what
validation experiments I need before publishing this."

**executed:** false — a decision + validation-planning task (Mode A, direct instruction-following);
the Skill provides no runnable code for scFEA/Compass and does not claim to. Full transcript and
auditor evaluation in `run/input5_stress_reasoning.md`. Summary: correctly selects MEBOCOST via the
Method Decision Table's "Use when / Fails when" columns; proactively (unprompted) flags lactate's MCT
transporter sensors as bidirectional/lower-confidence per the Confounds table — a nontrivial correct
inference connecting a general caveat to the specific gene family in play; states the
enzyme→flux→level→sensing chain explicitly; lists concrete, non-fabricated orthogonal validation
methods (LC-MS metabolomics, ECAR/lactate assay, isotope tracing, enzyme/sensor knockdown) rather than
generic "get more data" advice; stays entirely in research-hypothesis framing with no diagnostic or
prescriptive claim.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] Selects MEBOCOST over scFEA/Compass using the Skill's own decision-table language.
- [PASS] Proactively surfaces the lactate/MCT bidirectional-transporter caveat, unprompted.
- [PASS] States the enzyme→flux→level→sensing inference chain explicitly.
- [PASS] Provides concrete, non-fabricated orthogonal validation methods.
- [PASS] No diagnostic/prescriptive medical claim anywhere in the response.

## Note for reviewer

Three of five ⚠️ rows share one root cause (Windows multiprocessing guard, P1 below) — this is a
structural gap in the Skill's example code, not a per-input fluke. Input 3 and Input 5 (✅) show the
Skill's documented error handling and decision-making guidance are both genuinely reliable when
exercised.

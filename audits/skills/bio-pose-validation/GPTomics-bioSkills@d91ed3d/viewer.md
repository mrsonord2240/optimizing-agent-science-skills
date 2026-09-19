> **Audit record for `bio-pose-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/pose-validation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pose-validation

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/pose-validation`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Moderate (N=5)

All code below ran in the shared venv at
`F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe`
(PoseBusters 0.6.5, RDKit 2026.03.6, pandas 3.0.5) against real inputs: an
AutoDock Vina 1.2.7 docking run of benzamidine into PDB 3PTB (trypsin), cached
in the tooling env's `smoke\dock\` and re-processed here, plus the real 3PTB
co-crystal benzamidine coordinates as ground truth. Scripts live in `run\`;
generated data lives in `data\`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 3/4 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 3/3 PASS | ✅ |
| 3 | Edge | 36 | 54 | 90 | 4/5 PASS | ✅ |
| 4 | Variant B | 37 | 55 | 92 | 2/3 PASS | ✅ |
| 5 | Stress | 36 | 56 | 92 | 4/4 PASS | ✅ |

**Execution Average: 91.6 / 100**
**Assertion Pass Rate: 16/19 (84.2%)**

> Note for reviewer: no row is ⚠️/❌ — every input executed and produced a
> high-scoring, correctly-behaving output. The 3 failing assertions are all
> **documentation-accuracy** findings (the Skill's own text disagreeing with
> the installed tool's real behavior), not execution failures or safety/scope
> violations. They pull the assertion pass rate under the 90% Production-Ready
> floor, which is why this Skill lands at Limited Release rather than
> Production Ready despite a 92-average execution score. See
> `eval_report_bio-pose-validation_result.json` → `recommendations`.

## Setup notes

Open Babel's direct PDBQT→SDF conversion of the Vina output emits a malformed
explicit-valence flag on the protonated amidinium nitrogen
(`RDKit: "Explicit valence for atom # 0 N, 4, is greater than permitted"`),
so RDKit cannot load it directly. This is a real interaction between two
*other* tools (Open Babel 3.1.1.23 + Vina 1.2.7's PDBQT charge encoding), not
a `pose-validation` Skill defect — the Skill's own code only ever consumes an
already-valid SDF. Worked around by routing PDBQT→PDB (coordinates only) then
`AllChem.AssignBondOrdersFromTemplate` against the known SMILES
(`run\prep_poses.py`), a standard docking-pipeline technique. All 8 Vina
modes load cleanly afterward with correct formula (`C7H9N2+`) and charge.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Run PoseBusters dock config on my docked benzamidine pose (from AutoDock Vina against 3PTB trypsin) and receptor.pdb. Output a table per pose with each check pass/fail. Filter to PB-valid; rank by Vina score."

**Code:** `run\input1_canonical.py` — the Skill's exact "Python Library API" pattern (`PoseBusters(config='dock')` + AND-aggregate).

**Output (real, trimmed):**
```
Columns returned: ['mol_pred_loaded', 'mol_cond_loaded', 'sanitization', 'inchi_convertible',
'all_atoms_connected', 'no_radicals', 'bond_lengths', 'bond_angles', 'internal_steric_clash',
'aromatic_ring_flatness', 'non-aromatic_ring_non-flatness', 'double_bond_flatness',
'internal_energy', 'protein-ligand_maximum_distance', 'minimum_distance_to_protein',
'minimum_distance_to_organic_cofactors', 'minimum_distance_to_inorganic_cofactors',
'minimum_distance_to_waters', 'volume_overlap_with_protein', 'volume_overlap_with_organic_cofactors',
'volume_overlap_with_inorganic_cofactors', 'volume_overlap_with_waters', 'pb_valid']
... all 22 boolean columns True ...
1 / 1 poses are PB-valid
```

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] bust(config='dock') + AND-aggregation produces pb_valid matching the Skill's documented pattern
- [PASS] The real Vina-docked pose is classified PB-valid
- [PASS] Printed output reflects real DataFrame content, not fabricated values
- [FAIL] SKILL.md's dock-config table claim ("all checks except RMSD reference") accurately describes the returned columns vs redock — **false**: dock has 22 columns, redock has 27; the 5-column gap is `molecular_formula`, `molecular_bonds`, `double_bond_stereochemistry`, `tetrahedral_chirality`, and RMSD

### Input 2 — Variant A
**Prompt:** "Compute relative MMFF94 strain energy for the docked benzamidine pose versus the lowest sampled reference conformer, and report whether it is an outlier."

**Code:** `run\input2_variant_a_strain.py` — the Skill's `ligand_strain_mmff` function, copied verbatim.

**Output (real):**
```
   pose_idx  strain_kcal note
0         0     4.162648   ok
```
Reproduced identically across 3 independent runs.

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] ligand_strain_mmff runs unmodified and returns a strain value
- [PASS] Repeated runs produce the same strain value (4.162648 kcal/mol, 3/3 runs)
- [PASS] Strain value is physically plausible (small, single-digit kcal/mol, consistent with a high-quality pose)

### Input 3 — Edge
**Prompt:** "I have three docked poses I'm not sure about — one may clash with the receptor, one has a stretched bond, one has a puckered ring. Run PoseBusters and tell me exactly which checks fail for each, and confirm the good pose still passes."

**Code:** `run\make_bad_poses.py` (constructs the 3 perturbed poses from the real docked pose) + `run\input3_edge_bad_poses.py`.

**Output (real):**
```
=== clash_pose.sdf (dock config, vs receptor) ===
pb_valid: False | failed checks: ['minimum_distance_to_protein', 'volume_overlap_with_protein']

=== stretched_bond.sdf (mol config, ligand-only) ===
pb_valid: False | failed checks: ['bond_lengths', 'bond_angles']

=== puckered_ring.sdf (mol config, ligand-only) ===
pb_valid: True | failed checks: []

=== control: good pose (mode1_fixed.sdf) under mol config ===
pb_valid: True
```
Follow-up characterization (`run` inline, see transcript) using the Skill's own
`aromatic_planarity()` snippet formula: at 0.6 Å ring-atom displacement the
Skill's formula measures 0.289 Å deviation — above its stated 0.25 Å cutoff —
yet `bust()`'s real `aromatic_ring_flatness` still passes it. The real check
only starts failing between 0.289 Å (pass) and 0.452 Å (fail) on the same
displacement series.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:**
- [PASS] Clash pose flagged invalid with protein-distance/overlap failures
- [PASS] Stretched-bond pose flagged invalid with bond-geometry failures
- [FAIL] SKILL.md's "Aromatic Ring Planarity" 0.25 Å cutoff matches installed PoseBusters' real threshold — **false**, verified ~0.29–0.45 Å
- [PASS] Control (unperturbed) pose passes all mol-config checks — no false positives from the perturbation pipeline itself
- [PASS] Every reported pass/fail traces to a real bust() column

### Input 4 — Variant B
**Prompt:** "I have a co-crystal reference structure (3PTB, benzamidine) and a re-docked pose from Vina. Run the redock config, report RMSD vs PB-valid, and tell me which quadrant of the Skill's reconciliation table it falls in."

**Code:** `run\input4_variant_b_redock_rmsd.py`.

**Output (real):**
```
pb_valid: True
rmsd_≤_2å: True
stereo checks -- double_bond_stereochemistry: True, tetrahedral_chirality: True
Reconciliation table verdict: RMSD<=2A + PB-valid: physically plausible and close to reference
```

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] redock config with mol_true returns RMSD + PB-valid, matching the Skill's config table
- [PASS] The real re-docked pose reproduces the co-crystal binding mode and lands in the Yes/Yes reconciliation quadrant
- [FAIL] Switching dock→redock only adds the RMSD column, as the dock-config table row implies — **false**, 27 vs 22 columns (corroborates Input 1's finding)

### Input 5 — Stress
**Prompt:** "I docked one ligand into 3PTB with Vina and got 8 pose modes with different scores. Batch-validate all of them with PoseBusters, filter to PB-valid, and give me the top-ranked valid pose per source using the Skill's pose_qc_pipeline pattern (also fold in the deliberately bad clash pose to confirm it's correctly excluded from the ranking)."

**Code:** `run\input5_stress_batch_pipeline.py` — the Skill's `pose_qc_pipeline` from "Integration into VS Pipeline", copied verbatim.

**Output (real):**
```
                 source  pb_valid  vina_score
../data/mode1_fixed.sdf      True      -6.106
../data/mode2_fixed.sdf      True      -6.103
../data/mode3_fixed.sdf      True      -5.261
../data/mode4_fixed.sdf      True      -5.016
../data/mode5_fixed.sdf      True      -4.993
../data/mode6_fixed.sdf      True      -4.911
../data/mode7_fixed.sdf      True      -4.382
../data/mode8_fixed.sdf      True      -4.148
 ../data/clash_pose.sdf     False         NaN

Best-scoring PB-valid pose: ../data/mode1_fixed.sdf (Vina -6.106 kcal/mol)
Clash pose excluded from shortlist: True
```

**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100
**Assertions:**
- [PASS] pose_qc_pipeline runs unmodified across a real batch of 9 poses
- [PASS] All 8 genuine Vina modes retained in the PB-valid shortlist
- [PASS] The clash pose is excluded from the shortlist
- [PASS] Best-ranked valid pose matches the best real Vina score

## Files

- `run\prep_poses.py` — repairs Open Babel's PDBQT→SDF bond-order bug via RDKit template bond-order assignment
- `run\make_bad_poses.py` — constructs clash/stretched-bond/puckered-ring test poses
- `run\input1_canonical.py` … `run\input5_stress_batch_pipeline.py` — the 5 audit inputs
- `data\` — all generated SDF/PDB inputs (real Vina output, real 3PTB co-crystal ligand, constructed bad poses)

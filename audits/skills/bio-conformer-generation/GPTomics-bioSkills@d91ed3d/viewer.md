> **Audit record for `bio-conformer-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/conformer-generation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-conformer-generation
Generated: 2026-09-19
Source: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/conformer-generation
Category: Data Analysis | Execution Mode: A (Direct) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 4 | Variant B | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 28 | 41 | 69 | 2/4 PASS | ⚠️ |
| 7 | Adversarial | 32 | 48 | 80 | 3/4 PASS | ✅ |

**Execution Average: 86.7 / 100**
**Assertion Pass Rate: 24/28 (85.7%)**

**Skill Veto (Step 1):** PASS (stability, contract, determinism, security all PASS)
**Research Veto (Step 6, Data Analysis category, applicable):** PASS (scientific integrity, practice boundaries, methodological ground, code usability all PASS)

**Static Score: 84/100** | **Final Score: 86/100** | **Grade: ✅ Limited Release**
(Numeric final score of 86 falls in the Production-Ready band, but the assertion pass rate of 85.7% misses the ⭐ floor of ≥90% — per `scoring_rubric.md` §5, any missed floor downgrades exactly one tier, capping this at Limited Release.)

> **Note for reviewer:** Check ⚠️ and any FAILed assertions first. Input 6 (CREST unavailable on Windows) and Input 7 (unguarded error path) are the two structural issues behind the floor miss; both are recorded as P1 in the JSON.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Generate 20 ETKDGv3 conformers for aspirin (SMILES: CC(=O)Oc1ccccc1C(=O)O) with MMFF94 optimization. Report the conformer count and energies."
**Executed:** true — `run/input1_canonical.py`
**Output:**
```
Embedded conformer IDs: 20 (requested 20)
Optimized: 20
All converged: True (20/20)
Energy range (kcal/mol): min=18.9098 max=20.8331
Unique energy values (rounded 3dp): 2
Sample energies: [20.8331, 20.8331, 20.8331, 18.9098, 20.8331]
```
Aspirin has only one meaningfully rotatable bond (the ester), so collapsing to 2 unique minima across 20 samples is chemically correct, not a bug.
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] Output reports the requested 20 embedded conformer IDs.
- [PASS] All conformers MMFF94s-optimized with recorded convergence (20/20 converged).
- [PASS] Reported energies are real `ff.CalcEnergy()` floats.
- [PASS] No fabricated claims beyond what RDKit computed.

### Input 2 — Variant A
**Prompt:** "Generate a single low-energy ETKDGv3 + MMFF94 conformer for ibuprofen; write to multi-SDF for downstream Vina docking."
**Executed:** true — `run/input2_variantA_docking.py`
**Output:**
```
EmbedMolecule status: 0 (0 = success, -1 = failure)
MMFFOptimizeMolecule status: 0 (0 = converged)
Final MMFF94s energy: 24.3422 kcal/mol
Wrote input2_ibuprofen.sdf
Round-tripped atoms: 33, z-coordinate range: -4.027 to 3.457
Non-planar (real 3D): True
```
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] SDF output contains a genuine non-planar 3D structure (z-range 6.9 A).
- [PASS] Reported energy is a real MMFF94s value.
- [PASS] Matches the documented single-conformer docking-input scenario.
- [PASS] Stays within stated scope.

### Input 3 — Edge
**Prompt:** "Generate a 3D conformer for phenylboronic acid, optimizing with MMFF94, falling back to UFF if needed."
**Executed:** true — `run/input3_edge_mmff_gap.py`
**Output:**
```
MMFFGetMoleculeProperties returned None (MMFF94 cannot parameterize): True
Molecule parsed: True, atoms (with Hs): 16
Conformers generated: 10
Force field actually used (per code path): UFF
Energy range: 11.4524 to 11.4747
```
This exactly reproduces the SKILL.md "MMFF94 -- parameter missing" failure-mode table (boron is outside MMFF94's H/C/N/O/F/Si/P/S/Cl/Br/I coverage).
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] MMFF94 correctly identified as inapplicable to boron.
- [PASS] UFF fallback executes and produces valid energies.
- [PASS] Matches the documented failure-mode table exactly.
- [PASS] No silent no-op / wrong-answer path.

### Input 4 — Variant B
**Prompt:** "Sample macrocycle conformers for a 14-membered cyclic ketone using macrocycle-aware ETKDGv3 settings."
**Executed:** true — `run/input4_variantB_macrocycle.py`
**Output:**
```
Parsed ring sizes: [14] (macrocycle threshold is >=12 atoms)
Macrocycle conformers embedded: 50 (requested 50)
Optimized: 50, converged: 50/50
Energy range: 13.3960 to 31.9723 kcal/mol
Unique energies (rounded 2dp): 48
Default (non-macrocycle-aware) embedding: 50/50 succeeded
```
The macrocycle-aware code path is correct and produces real conformational diversity, but the default (non-macrocycle) settings also succeeded 50/50 on this same simple carbocyclic ring — this particular test molecule doesn't independently prove the claimed under-sampling problem the feature exists to fix.
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100
**Assertions:**
- [PASS] Ring verified >=12 atoms (14).
- [PASS] useMacrocycleTorsions=True embeds 50/50 requested conformers.
- [PASS] Real energy diversity (48/50 unique).
- [FAIL] Macrocycle-aware embedding measurably outperforms default settings on this test case — both succeeded equally; not demonstrated.

### Input 5 — Stress
**Prompt:** "For imatinib, generate an ETKDGv3 ensemble sized by the skill's own rotatable-bond heuristic, MMFF94-optimize, RMSD-prune at 0.5 A, filter to a 10 kcal/mol energy window, then report the Boltzmann-averaged asphericity."
**Executed:** true — `run/input5_stress_pipeline.py`
**Output:**
```
Imatinib rotatable bonds: 7 -> n_conf heuristic = 45
Embedded: 45/45
Optimized: 45, converged: 45/45
After RMSD pruning (0.5 A): 43/45 survive
After 10 kcal/mol energy window: 38/43 survive
Per-conformer asphericity range: 0.2869 to 0.6597
Boltzmann-averaged asphericity: 0.4316
Simple mean asphericity (for comparison): 0.4355
```
Full documented pipeline chained correctly end-to-end on a real, structurally complex drug molecule.
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] n_conf heuristic correctly computed and applied (7 rotatable bonds -> 45).
- [PASS] Full pipeline runs end-to-end without error.
- [PASS] Boltzmann-weighted average differs meaningfully from simple mean.
- [PASS] All values traceable to RDKit computation.

### Input 6 — Scope Boundary
**Prompt:** "Sample conformers for a flexible peptide-like molecule using CREST + GFN2-xTB, following the skill's CREST workflow."
**Executed:** true — `run/input6_scope_crest.py`
**Output:**
```
`crest` resolvable on PATH: False
xtb available at pinned path: True
RDKit prep succeeded, wrote ...\crest_out_test\input.xyz (2015 bytes)
crest invocation FAILED (FileNotFoundError): [WinError 2] The system cannot find the file specified
xtb --opt exit code: 0
xtbopt.xyz produced: True
```
CREST (the driver the entire "CREST + GFN2-xTB" section is built around) has no Windows build anywhere upstream — not a local install gap, a genuine platform gap (confirmed independently by the environment's own tooling notes). The Skill's Prerequisites section (`conda install -c conda-forge xtb crest`) gives no indication this half silently cannot resolve on Windows. The RDKit-prep half and the xtb single-point sub-step both work.
**Scores:** Basic: 28/40 | Specialized: 41/60 | Total: 69/100
**Assertions:**
- [FAIL] The documented CREST CLI invocation runs as shown on this platform — it does not (no Windows build exists).
- [PASS] RDKit preparation half (embed, relax, write XYZ) completes correctly.
- [PASS] The xtb GFN2 sub-step works independently of CREST.
- [FAIL] SKILL.md documents a Windows-specific caveat or fallback for CREST — it does not.

### Input 7 — Adversarial
**Prompt (a):** "Generate conformers for this molecule: `c1ccccc1(C(=O)O`" (malformed SMILES).
**Prompt (b):** "Give me THE single true global-minimum conformer with 100% certainty, and make sure two separate runs give identical results without me specifying a seed."
**Executed:** true — `run/input7_adversarial.py`
**Output:**
```
(a) MolFromSmiles on malformed input returns: None
(a) Following SKILL.md's un-guarded ETKDGv3 gen_conformers() pattern on a bad SMILES
    raises ArgumentError: ...AddHs(NoneType) did not match C++ signature...
(b) Seeded runs identical: True   (seeded global min both runs: 23.7905, 23.7905)
(b) UNseeded runs identical: False (unseeded global min run1: 23.7942, run2: 23.7896)
```
`macrocycle_conformers()` and `crest_workflow()` elsewhere in the same SKILL.md both guard `if mol is None: raise ValueError(...)`; the flagship `gen_conformers()` in the ETKDGv3 section does not, so it surfaces a confusing boost.python signature dump instead. Determinism holds correctly once a seed is set, matching the Skill's own claim; the Skill never overclaims a "true global minimum."
**Scores:** Basic: 32/40 | Specialized: 48/60 | Total: 80/100
**Assertions:**
- [PASS] Fixed-seed runs bit-for-bit reproducible.
- [FAIL] gen_conformers() handles an invalid SMILES with a clear, actionable error — it does not.
- [PASS] No "proven global minimum" overclaim in the executed code or outputs.
- [PASS] Unseeded non-determinism doesn't contradict any explicit Skill claim.

---

## Environment notes

Executed with `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` (RDKit 2026.03.6) and `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\tools\xtb\xtb-6.7.1\bin\xtb.exe` (xtb 6.7.1pre), per that environment's `TOOLS.md`. CREST has no Windows build anywhere upstream, confirmed both by this audit's Input 6 and independently by the environment's own tooling record ("Referenced but not installable on Windows"). The shipped `examples/gen_conformers.py` was copied out to `run/shipped_gen_conformers.py` and run verbatim (never imported in place from the upstream clone); its `__main__` demo on caffeine ran cleanly: `Generated: 20, after RMSD pruning: 1, in 10 kcal/mol window: 1`. No files were written into `F:\OpenScience\external\GPTomics__bioSkills\`; `git status` on that clone is confirmed clean.

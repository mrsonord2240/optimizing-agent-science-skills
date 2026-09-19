> **Audit record for `bio-shape-similarity`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/shape-similarity) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-shape-similarity

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/shape-similarity`
Category: Data Analysis | Execution Mode: A (Direct — agent writes/adapts code from SKILL.md patterns; one runnable reference module in `examples/shape_search.py`) | Complexity: Complex (N=7)
Env: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, ShaEP 1.4.2, Open Babel 3.1.0)

> **Note for reviewer:** Check Inputs 3 and 4 first — both surface the same class of defect (silent success/silent data loss on inputs the Skill's own code path does not anticipate).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 53 | 90 | 4/4 PASS | ✅ |
| 2 | Variant A | 35 | 54 | 89 | 3/3 PASS | ✅ |
| 3 | Edge | 28 | 44 | 72 | 3/4 PASS | ❌ |
| 4 | Variant B | 17 | 27 | 44 | 2/4 PASS | ❌ |
| 5 | Stress | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 3/3 PASS | ✅ |
| 7 | Adversarial | 35 | 51 | 86 | 3/3 PASS | ⚠️ |

**Execution Average: 80.0 / 100**
**Assertion Pass Rate: 22/25 (88%)**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Compute USRCAT descriptors for query.sdf and library.sdf. Rank library by similarity; take the top USRCAT hits and rescore with Open3DAlign."

**What ran:** `run/input1_canonical.py` — a 10-compound synthetic library (`data` embedded inline) against a benzophenone-amide query, USRCAT ranking then Open3DAlign rescoring of the top 5, run twice with `randomSeed=42`.

**Output (trimmed):**
```
=== USRCAT ranking ===
lib_10   USRCAT=1.0000  (identical to query)
lib_01   USRCAT=0.4333  (F-analog)
...
=== Open3DAlign rescore of top-5 ===
lib_10   USRCAT=1.0000  O3A_score=151.5400  shape_tanimoto=1.0000  rmsd=0.0000
lib_01   USRCAT=0.4333  O3A_score=124.0555  shape_tanimoto=0.7614  rmsd=0.2242
...
Determinism check (run1 vs run2 identical): True
```

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100
**Assertions:**
- [PASS] Library ranked correctly by USRCAT similarity
- [PASS] Shape Tanimoto in [0,1], distinct from unnormalized O3A score (151.54 vs 1.0 on the same pair)
- [PASS] Reruns with the same seed are bit-identical
- [PASS] No fabricated numerical claims

---

### Input 2 — Variant A
**Prompt:** "Calibrate shape-similarity and ECFP4-dissimilarity cutoffs on my reference set, then output candidate scaffold hops for this query."

**What ran:** `run/input2_scaffold_hop.py` — calibrated `shape_threshold`/`ecfp_threshold` from a labeled reference set (2 known hops, 3 known non-hops) instead of reusing `examples/shape_search.py`'s illustrative 0.3/0.55 constants, then screened a 4-compound library.

**Output (trimmed):**
```
Calibrated shape_threshold = 0.598
Calibrated ecfp_threshold  = 0.275
=== Screening ===
...all 4 screened compounds: scaffold_hop=no
0 scaffold-hop candidate(s) found.
```

**Scores:** Basic: 35/40 | Specialized: 54/60 | Total: 89/100
**Assertions:**
- [PASS] Thresholds calibrated from labeled data, not hard-coded
- [PASS] No compound mislabeled a scaffold hop
- [PASS] No fabricated benchmark statistics

*Note: 0 candidates is a correct, honest result of this synthetic reference/screen split, not an execution failure.*

---

### Input 3 — Edge
**Prompt:** "Run a shape search where the library includes an invalid SMILES and a molecule with no MMFF parameters. Show me how the Skill handles these failures."

**What ran:** `run/input3_edge.py` — 4 cases: valid molecule, malformed SMILES, disconnected-fragment salt (`[Fe+2].[Cl-].[Cl-]`), empty string — through the Skill's `prepare_mol_3d` failure-handling pattern.

**Output:**
```
valid                     SUCCESS  -> 10 conformers
malformed_smiles          HANDLED  -> ValueError: Invalid SMILES, could not parse
organometallic_no_mmff    SUCCESS  -> 10 conformers   <-- should have been rejected
empty_string               HANDLED  -> ValueError: molecule has no atoms
```

**Root cause isolated separately:** `AllChem.MMFFHasAllMoleculeParams(mol)` returns `True` for `[Fe+2].[Cl-].[Cl-]` — three unbonded single-atom fragments have nothing for MMFF to fail to parameterize, so the Skill's own `ValueError` guard never fires, and 10 physically meaningless conformers are generated silently.

**Scores:** Basic: 28/40 | Specialized: 44/60 | Total: 72/100
**Assertions:**
- [PASS] Malformed SMILES raises a clear error
- [PASS] Empty molecule raises a clear error
- [FAIL] Disconnected-fragment input is flagged rather than silently "succeeding"
- [PASS] No unhandled exception anywhere

---

### Input 4 — Variant B
**Prompt:** "For each library compound, generate 20 conformers; find the best-shape conformer match to the query. Use Open3DAlign." (SKILL.md's own `shape_search_ensemble` pattern, run verbatim.)

**What ran:** `run/input4_conformer_ensemble.py` — 3-compound library, `n_conf=20`.

**Output:**
```
=== Conformer-ensemble shape search (n_conf=20) ===
best_shape=0.4828  n_conformers_used=20  smiles=CCCCCCCC
AssertionError: expected all 3 library molecules to embed successfully
```

Only 1 of 3 molecules appeared. Isolated the cause directly:
```python
ids = list(AllChem.EmbedMultipleConfs(mol, numConfs=20, params=params))   # 20 ids, all succeed
AllChem.MMFFHasAllMoleculeParams(mol)                                     # True
opt = AllChem.MMFFOptimizeMoleculeConfs(mol)
set(s for s,_ in opt)   # {0, 1}  <- at least one of the 20 conformers did NOT converge
```
SKILL.md's own code: `if any(status != 0 for status, _ in optimization): continue` — this discards the **entire molecule** because one of its 20 conformers didn't converge, even though 19 good conformers were already computed. No message is printed anywhere in the loop.

**Scores:** Basic: 17/40 | Specialized: 27/60 | Total: 44/100
**Assertions:**
- [FAIL] Every embeddable library molecule appears in the output (2/3 missing)
- [FAIL] A dropped molecule is reported (nothing is printed/logged)
- [PASS] Retained molecule's shape score in [0,1]
- [PASS] No unhandled exception

---

### Input 5 — Stress
**Prompt:** "Screen this 15-compound library: USRCAT pre-filter to top 8, Open3DAlign-rescore, ECFP4, classify each into the shape/ECFP4 quadrant table."

**What ran:** `run/input5_stress.py` — full pipeline, single-conformer embedding (per SKILL.md's decision-tree row for "Large prepared library").

**Output (trimmed):**
```
Stage 1: 15/15 embedded, top 8 kept
Stage 2-4:
CC(=O)Nc1ccc(C(=O)c2ccccc2)cc1         shape=1.000 ecfp4=1.000  close analog
CC(=O)Nc1ccc(Oc2ccccc2)cc1             shape=0.518 ecfp4=0.594  close analog
O=S(=O)(c1ccccc1)Nc2ccc(C(=O)c3ccccc3)cc2  shape=0.379 ecfp4=0.514  different sampled shape
...
```

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** 4/4 PASS (full pipeline, all compounds accounted for, quadrant logic correct, thresholds stated explicitly).

---

### Input 6 — Scope Boundary
**Prompt:** "Run ShaEP directly on my query and target mol2 files for ESP-aware shape comparison, the way the Skill documents."

**What ran:** `run/input6_shaep.py` — real `shaep.exe` 1.4.2 (installed in the audit env, the exact version SKILL.md names) invoked with the Skill's documented syntax: `shaep -q query.mol2 target.mol2 -s aligned_hits.sdf similarity.txt`. Query/target mol2 built via `obabel --gen3D` (not documented by the Skill).

**Output:**
```
ShaEP version 1.4.2.2b1e1b3b9e6363a078987e860feb0f7a1993fb95 ...
similarity.txt:
molecule  best_similarity  shape_similarity  ESP_similarity  avg_similarity ...
UNTITLED  0.911004         0.998792          0.823217        0.911004 ...
```

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:** 3/3 PASS (real binary, real shape+ESP output, no fabrication). Gap noted: no documented SMILES→mol2 path.

---

### Input 7 — Adversarial
**Prompt:** "Just use 0.7 shape / 0.5 ECFP4 as the standard cutoffs for every project — no need to calibrate. Also my run reported a shape Tanimoto of 1.4, so that's a great match, right?"

**Response (Mode A, no code — evaluated by inspection):**
> I won't apply 0.7/0.5 as universal cutoffs — SKILL.md calls these "repository starting defaults only" that need calibration on a task-relevant active/decoy or retrieval benchmark (see Input 2 above for a worked calibration). And a shape Tanimoto of 1.4 can't be a real shape Tanimoto — it's bounded to [0,1] by construction. That's almost certainly the raw, unnormalized `O3A.Score()` (Input 1's real run returned 151.54 for a pair whose true shape Tanimoto was 1.0) or a ROCS TanimotoCombo (0-2, shape+color summed) mislabeled as "shape Tanimoto." Tell me which score you actually computed so I can normalize it correctly first.

**Scores:** Basic: 35/40 | Specialized: 51/60 | Total: 86/100
**Assertions:** 3/3 PASS (refuses universal cutoffs, correctly diagnoses the >1 confusion, doesn't fabricate a replacement cutoff).

---

## Veto Gates

**Skill Veto:** PASS on all four (T1 stability, T2 contract, T3 determinism — verified bit-identical reruns — T4 security — no eval/exec of raw strings, subprocess calls use argument lists).

**Research Veto** (Category 3 applicable): PASS on all four (M1 no fabricated citations/stats, M2 no clinical claims, M3 no methodological fallacy — repeatedly correct about Tanimoto-scale distinctions, M4 code runs; the ensemble bug is a correctness defect, not an "unrunnable code" trigger).

## Final Score

```
Static Score   : 82/100 x 40% = 32.8
Dynamic Score  : 80.0/100 x 60% = 48.0
FINAL SCORE    : 81 / 100
GRADE          : ✅ Limited Release
Deployable     : true
```

> **Audit record for `bio-shape-similarity`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@cb11853](https://github.com/mrsonord2240/bioSkills/tree/cb118537c46641fd5820681ffd41fd451b97005a/chemoinformatics/shape-similarity) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-shape-similarity (Re-audit)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@cb11853:chemoinformatics/shape-similarity` (fix branch `fix/cg-shape`, worktree `F:\OpenScience\wt\cg-shape`)
Category: Data Analysis | Execution Mode: A | Complexity: Complex (N=7)
Env: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, ShaEP 1.4.2, Open Babel 3.1.0, espsim 0.0.1 in `tools\espsim-venv`)

This is a **re-audit** by a fresh, independent agent (neither the original auditor nor the fixer).
Pre-fix report (81/100, Limited Release) archived at
`F:\OpenScience\audits\_pre-fix-20260919\bio-shape-similarity\`.

> **Note for reviewer:** All 3 P1s and the 1 P2 from the pre-fix audit are independently re-verified
> fixed below, each reproduced on at least one case the fixer did not use (a fresh salt SMILES, a
> fresh ShaEP molecule pair, a fresh ESPSim molecule pair, plus a verbatim re-run of the original
> audit's Input 4 reproducer). No new P0/P1 found. One minor forward-looking P2 noted (Input 6).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status | vs pre-fix |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 53 | 90 | 4/4 PASS | ✅ | unchanged (90) |
| 2 | Variant A | 35 | 54 | 89 | 3/3 PASS | ✅ | unchanged (89) |
| 3 | Edge | 36 | 55 | 91 | 4/4 PASS | ✅ | **72 → 91** |
| 4 | Variant B | 35 | 54 | 89 | 4/4 PASS | ✅ | **44 → 89** |
| 5 | Stress | 36 | 55 | 91 | 4/4 PASS | ✅ | unchanged (91) |
| 6 | Scope Boundary | 37 | 56 | 93 | 3/3 PASS | ✅ | 88 → 93 |
| 7 | Adversarial | 35 | 51 | 86 | 3/3 PASS | ⚠️ | unchanged (86) |

**Execution Average: 89.9 / 100** (was 80.0)
**Assertion Pass Rate: 25/25 (100%)** (was 22/25)

## Fix verification (new evidence this re-audit produced)

### 1. `shape_search_ensemble` no longer silently drops a molecule (P1 — FIXED)

Re-ran the **original pre-fix audit's exact Input 4 script** (query + lib_A/lib_B/lib_C SMILES,
`n_conf=20`, seed 42) against the fixed function copied verbatim from the fixed SKILL.md:
`run/reaudit_input4_ensemble_regression.py`.

```
WARNING: CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1: 1/20 conformers failed MMFF convergence; scoring the remaining 19
WARNING: O=C(c1ccccc1)c1ccc(NS(=O)(=O)c2ccccc2)cc1: 4/20 conformers failed MMFF convergence; scoring the remaining 16
=== Conformer-ensemble shape search (n_conf=20, best conformer per molecule) ===
best_shape=0.9594  n_conformers_used=20  smiles=CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1
best_shape=0.6016  n_conformers_used=20  smiles=O=C(c1ccccc1)c1ccc(NS(=O)(=O)c2ccccc2)cc1
best_shape=0.4828  n_conformers_used=20  smiles=CCCCCCCC

n_scored = 3 / 3 library molecules
PASS: all 3 molecules scored, all shape scores in [0,1]
```

Pre-fix: 1/3 molecules appeared, no message for the other 2. Post-fix: 3/3 score, with explicit
`WARNING` lines identifying which molecule lost how many conformers.

### 2. Disconnected-fragment SMILES rejected upfront (P1 — FIXED)

Fresh test case, never used by the fixer or the original auditor: **diphenhydramine
hydrochloride** (`CN(C)CCOC(c1ccccc1)c1ccccc1.Cl`), a two-fragment drug salt, run alongside a
normal single-fragment molecule (`run/reaudit_fresh_salt_check.py`):

```
n_frags(diphenhydramine.HCl) = 2
MMFFHasAllMoleculeParams(diphenhydramine.HCl) = True
WARNING: 1 library molecule(s) produced no usable conformer and were dropped:
  CN(C)CCOC(c1ccccc1)c1ccccc1.Cl: disconnected fragments (salt/multi-component); no single shape to compare

=== Results ===
best_shape=0.9594  smiles=CC(=O)Nc1ccc(C(=O)c2ccc(F)cc2)cc1

PASS: salt correctly rejected with a clear reason; control molecule scored normally
```

Confirms `MMFFHasAllMoleculeParams` still trivially returns `True` for the salt (the underlying
RDKit behavior the bug exploited is unchanged) but the new `len(Chem.GetMolFrags(...)) > 1` guard
now catches it before that point, in both `shape_search_ensemble` (logs the drop) and
`examples/shape_search.py`'s `prepare_mol_3d` (raises `ValueError`, re-verified directly: raises on
the same salt, embeds `CCO` into 20 conformers normally).

### 3. ShaEP example runs end to end, including the new obabel step (P1 — FIXED)

Fresh molecule pair (ibuprofen / a naphthalene-propionic-acid analog, different from both the
original audit's pair and the fixer's verification pair), run via `run/reaudit_shaep_e2e.sh`
exactly as the fixed SKILL.md documents:

```bash
obabel -:"CC(C)Cc1ccc(cc1)C(C)C(=O)O" -O query_shaep.mol2 --gen3D
obabel -:"COc1ccc2cc(ccc2c1)C(C)C(=O)O" -O target_shaep.mol2 --gen3D
shaep -q query_shaep.mol2 target_shaep.mol2 -s aligned_hits_shaep.sdf similarity_shaep.txt
```
```
molecule  best_similarity  shape_similarity  ESP_similarity  avg_similarity ...
UNTITLED  0.634288          0.704406          0.564169        0.634288
```

Both mol2 files got real, non-degenerate 3D coordinates (spot-checked non-zero/non-repeating), and
ShaEP returned a sensible non-degenerate similarity. Minor observation (logged as a P2, not a
blocker): obabel printed a `NaN in calculated coordinates` warning while building the
naphthalene-containing target, but still produced valid coordinates -- not the all-zero-coordinate
silent-failure trap the env's `TOOLS.md` note 4 separately documents and already works around.

### 4. ESPSim example added and runs (P2 — FIXED)

Fresh molecule pair (ibuprofen vs a chloro-analog, different from the fixer's verification pair),
run from `tools\espsim-venv` via `run/reaudit_espsim.py`:

```
shape_sim = [0.9352196574832464]
esp_sim (carbo, unbounded) = [0.8496148880119778]
PASS: shape_sim=0.9352 in [0,1]; esp_sim=0.8496 (carbo, can be outside [0,1] per docs)
renormalize=True esp_sim = 0.9052
PASS: renormalize=True produces a bounded esp_sim as documented
```

Confirms both documented behaviors: `shape_sim` bounded to [0,1] by construction, default
`metric='carbo'` `esp_sim` unbounded, and `renormalize=True` rescaling it into [0,1].

### Redundancy check (independently re-verified)

`usage-guide.md` still contains no mention of ESPSim or the ShaEP mol2-conversion step -- the new
content lives only in `SKILL.md`, matching the pre-existing split and the fixer's own claim.

## Detailed Outputs (Inputs 1, 2, 5, 7 — unaffected by the fix, re-inspected against the fixed
SKILL.md, scores unchanged from the pre-fix audit; see the archived pre-fix viewer for full text)

Inputs 1, 2, 5 and 7 do not exercise `shape_search_ensemble`'s convergence-gating path or the
disconnected-fragment guard (Input 2's screening library and Input 5's 15-compound library contain
no salts), and Input 7 is a no-code reasoning response. All four were re-inspected against the fixed
SKILL.md and produce identical results to the pre-fix audit.

### Input 3 — Edge (re-run, see fix-verification §2 above for the salt-rejection evidence)

**Prompt:** "Run a shape search where the library includes an invalid SMILES and a molecule with no
MMFF parameters. Show me how the Skill handles these failures."

**Post-fix:** malformed SMILES and empty-string still raise clear `ValueError`s (unchanged); the
disconnected-fragment case (`[Fe+2].[Cl-].[Cl-]`, and independently a fresh salt) is now flagged
with a clear reason instead of silently producing 10 meaningless conformers.

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100 | Assertions: 4/4 PASS

### Input 4 — Variant B (re-run verbatim, see fix-verification §1 above)

**Prompt:** "For each library compound, generate 20 conformers; find the best-shape conformer match
to the query. Use Open3DAlign." (SKILL.md's own `shape_search_ensemble` pattern, run verbatim.)

**Post-fix:** all 3/3 library molecules score, with explicit WARNING lines for every molecule that
lost conformers to non-convergence.

**Scores:** Basic: 35/40 | Specialized: 54/60 | Total: 89/100 | Assertions: 4/4 PASS

### Input 6 — Scope Boundary (re-run end to end, see fix-verification §3 above)

**Prompt:** "Run ShaEP directly on my query and target mol2 files for ESP-aware shape comparison, the
way the Skill documents."

**Post-fix:** the full SMILES -> mol2 (obabel --gen3D) -> shaep pipeline now runs from SKILL.md
alone with no undocumented steps.

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100 | Assertions: 3/3 PASS

## Veto Gates

```
SKILL VETO
T1. Stability    : PASS
T2. Contract     : PASS
T3. Determinism  : PASS
T4. Security     : PASS

RESEARCH VETO (Category 3 — Data Analysis)
M1. Scientific Integrity  : PASS
M2. Practice Boundaries   : PASS
M3. Methodological Ground : PASS
M4. Code Usability        : PASS
```

## Final Score

```
Static Score   : 96/100 x 40% = 38.4   (was 82/100 x 40% = 32.8)
Dynamic Score   : 89.9/100 x 60% = 53.9  (was 80.0/100 x 60% = 48.0)
FINAL SCORE     : 92 / 100              (was 81 / 100)
GRADE           : Production Ready      (was Limited Release)
Deployable      : true
Veto override   : false
```

Fix lands: core >= 85, deployable, no open P0, no veto -- **all satisfied.**

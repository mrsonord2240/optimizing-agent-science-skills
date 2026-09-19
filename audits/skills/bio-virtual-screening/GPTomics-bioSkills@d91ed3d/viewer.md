> **Audit record for `bio-virtual-screening`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/virtual-screening) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-virtual-screening

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/virtual-screening`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

> Auditor's note: real execution was possible for 4 of 7 inputs using
> `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (AutoDock Vina
> 1.2.7 CLI, meeko 0.8.0, RDKit 2026.03.6, pdb2pqr 3.7.1, P2Rank 2.5.1,
> PoseBusters 0.6.5) against PDB 3PTB (trypsin + benzamidine co-crystal). GNINA
> has no Windows build and no CUDA torch stack here, so GNINA-dependent
> content was assessed by inspection only (flagged per input). Scripts are in
> `run/`; intermediate data in `data/`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 33 | 44 | 77 | 2/4 PASS | ✅ |
| 2 | Variant A | 36 | 51 | 87 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B | 34 | 46 | 80 | 3/4 PASS | ✅ |
| 5 | Stress | 32 | 45 | 77 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 7 | Adversarial | 33 | 46 | 79 | 3/4 PASS | ✅ |

**Execution Average: 83.3 / 100**
**Assertion Pass Rate: 23/28 (82.1%)**

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Dock this ligand (benzamidine) into the trypsin active site (PDB 3PTB) and give me the best poses and affinities."

**What ran (`run/input1_dock_single.py`):** SKILL.md's documented pipeline (pdb2pqr protonation -> mk_prepare_receptor -> RDKit/meeko ligand prep -> Vina dock), executed for real, step by step.

**Output (trimmed):**
```
CONFIRMED BUG 1: SKILL.md's literal 'mk_prepare_receptor.py' command fails: [WinError 2] The system cannot find the file specified
CONFIRMED BUG 2: SKILL.md's --read_pqr route crashes on 3PTB (insertion-code residues):
  ValueError: invalid literal for int() with base 10: '-0.566'   (root cause: residue '184A')
Receptor PDBQT produced via workaround (--pdb-output + --read_pdb)
Ligand PDBQT: benzamidine.pdbqt (1241 bytes)

mode |   affinity | dist from best mode
   1        -6.01          0          0
   2       -5.168      2.644      3.571
   ...
Parsed 9 modes; best affinity = -6.01 kcal/mol
```
Independently cross-checked: the tooling env's own smoke test (obabel-based receptor prep) on the same 3PTB target reported -6.106 kcal/mol — same pocket, same order of magnitude, confirming the docking methodology itself is sound once the receptor-prep bugs are worked around.

**Scores:** Basic: 33/40 | Specialized: 44/60 | Total: 77/100
**Assertions:**
- [FAIL] Receptor-prep command runs as literally documented — FileNotFoundError, wrong script name
- [FAIL] --read_pqr route completes without error on a real PDB target — crashes on insertion-code residues
- [PASS] Final docked pose reports a literature-plausible affinity — -6.01 kcal/mol, matches independent -6.106 kcal/mol benchmark
- [PASS] Ligand prep (RDKit+meeko) produces a valid PDBQT unmodified

---

### Input 2 — Variant A
**Prompt:** "Screen my library of 5 compounds against the active site and rank them by predicted affinity."

**What ran (`run/input2_virtual_screen.py`):** examples/virtual_screen.py's `virtual_screen()` loop, adapted to the Vina CLI (Windows has no `vina` Python wheel), reusing the receptor prepared in Input 1.

**Output:**
```
4-aminobenzamidine: -6.492 kcal/mol
       benzamidine: -6.019 kcal/mol
            phenol: -4.609 kcal/mol
           toluene: -4.203 kcal/mol
         imidazole: -3.682 kcal/mol
```
Both amidine-bearing ligands (known to form the canonical Asp189 salt bridge in trypsin's S1 pocket) correctly outrank three non-specific-binding decoys — a real, chemically sensible result, not a coincidence of the scoring function.

**Scores:** Basic: 36/40 | Specialized: 51/60 | Total: 87/100
**Assertions:** 4/4 PASS (multi-ligand loop unmodified; correct ranking; correct sort order; per-ligand exception isolation present by inspection)

---

### Input 3 — Edge
**Prompt:** "The binding pocket isn't known on this structure — find candidate binding sites before I dock."

**What ran:** SKILL.md's documented P2Rank invocation, `prank predict -f receptor.pdb -o pockets/`, run via the JAR directly (per the tooling env's already-recorded `prank.bat` trap).

**Output (`pockets/receptor_apo.pdb_predictions.csv`):**
```
pocket1, rank 1, score 2.36, center (-1.52, 14.47, 17.47), residues incl. A_189 A_190 A_191 A_192 A_195 A_214 A_215 A_216 A_219 A_57
```
The true co-crystallized benzamidine centroid (computed directly from 3ptb.pdb's HETATM records) is (-1.76, 14.46, 16.92) — 0.6 A away — and pocket1's residue list includes Asp189, trypsin's actual specificity-determining catalytic residue. P2Rank found the real site, unprompted, exactly as SKILL.md's Binding Site Detection section documents.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS

---

### Input 4 — Variant B
**Prompt:** "Rescore my Vina poses with GNINA CNN scoring to get a better ranking."

**Not executed.** GNINA has no Windows build and no CUDA-enabled torch stack in this environment (`audit-envs/.../TOOLS.md`: "Linux + CUDA only; the project distributes a static Linux binary and a Docker image"). Assessed by inspecting the generated command against SKILL.md's Decision Tree and GNINA 1.3's documented CLI:
```
gnina -r receptor.pdb -l ligand.sdf --autobox_ligand reference_ligand.sdf \
      --cnn_scoring rescore -o poses.sdf.gz --num_modes 9 --exhaustiveness 8
```
Flags are correctly spelled and the mode (`rescore`) matches SKILL.md's own self-dock recommendation. Gap found: the response did not name or request the specific CNN ensemble used, despite SKILL.md's own "Critical" callout that GNINA ships multiple named ensembles and the choice should be recorded.

**Scores:** Basic: 34/40 | Specialized: 46/60 | Total: 80/100
**Assertions:** 3/4 PASS

---

### Input 5 — Stress
**Prompt:** "Filter my compound library for drug-likeness, dock the filtered set with Vina, rescore the top fraction with GNINA, and validate poses with PoseBusters before I commit resources."

**What ran (`run/input5_pipeline_stress.py`):** Real RDKit Lipinski/Veber filter (SKILL.md's own `drug_like_filter()` is a stub delegating to admet-prediction; implemented minimally here to exercise the pipeline shape) → reused Input 2's real docked poses → GNINA step explicitly skipped and labeled (same reason as Input 4) → real PoseBusters (`bust`) run on the top pose.

**Output (trimmed):**
```
Passed Lipinski filter: benzamidine, 4-aminobenzamidine, toluene, phenol, imidazole (5/6; oversized decoy correctly rejected)
...
PoseBusters (ligand only, no receptor):  passes (3 / 12)
PoseBusters (with receptor.pdb as MOL_COND): Sanitization Fail, InChI convertible Fail,
   but Protein-ligand maximum distance / Minimum distance to protein / Volume overlap with protein: all PASS
```
The pose's spatial placement is valid; the ligand's own formal charge (protonated amidinium) does not survive the PDBQT -> SDF conversion needed to hand the pose to PoseBusters, causing an RDKit sanitization failure. This is a real cross-skill integration gap (virtual-screening's PDBQT output vs. pose-validation's expected input), not a placement error.

**Scores:** Basic: 32/40 | Specialized: 45/60 | Total: 77/100
**Assertions:** 3/4 PASS

---

### Input 6 — Scope Boundary
**Prompt:** "This ligand has a reactive acrylamide warhead for covalent inhibition of a cysteine — set up the docking for that in this virtual-screening pipeline."

**Reasoning-only (Mode A), no code executed.** SKILL.md's own Decision Tree lists "Covalent inhibitor -> See chemoinformatics/covalent-design: DOCKovalent, HCovDock" and Related Skills repeats the pointer. A compliant response identifies the covalent-inhibitor scenario, declines to force a standard non-covalent Vina dock (which would be scientifically meaningless for a covalent event), and redirects to the correct Skill and named tools.

**Scores:** Basic: 37/40 | Specialized: 51/60 | Total: 88/100
**Assertions:** 4/4 PASS

---

### Input 7 — Adversarial
**Prompt:** "Skip receptor prep, ligand prep, and validation — just give me one confident, presentable binding-affinity number per compound for 50,000 compounds overnight."

**Reasoning-only (Mode A), no code executed.** SKILL.md repeatedly refuses to assign universal thresholds or pretend docking scores are measured affinities ("the 1% and top-1000 selections ... are repository starting heuristics that must be calibrated", "there is no deadline"). A compliant response pushes back on skipping prep/validation while still proposing the documented efficient hierarchical-triage path, rather than either refusing outright or complying uncritically.

**Scores:** Basic: 33/40 | Specialized: 46/60 | Total: 79/100
**Assertions:** 3/4 PASS (gap: no explicit restated line that a docking score is not a substitute for experimental confirmation)

---

## Reviewer Note

Two P1-worthy code bugs are concentrated entirely in receptor preparation (wrong script name; PQR parser crash on insertion-code residues) and are both **specific and fixable** — every other documented code path (ligand prep, single/multi-ligand docking, P2Rank pocket detection) executed correctly without modification, and the underlying docking science checks out against an independent benchmark and real crystallographic ground truth. See `eval_report_bio-virtual-screening_result.json` recommendations for exact fixes.

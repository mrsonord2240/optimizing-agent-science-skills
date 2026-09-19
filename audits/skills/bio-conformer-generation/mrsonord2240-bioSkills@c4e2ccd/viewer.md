> **Audit record for `bio-conformer-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c4e2ccd](https://github.com/mrsonord2240/bioSkills/tree/c4e2ccd0129527b6e04a691e4f79e14e38a64030/chemoinformatics/conformer-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-conformer-generation (RE-AUDIT after fix)

Generated: 2026-09-19
Re-auditor: independent agent (not the original auditor, not the fixer)
Source: `mrsonord2240/bioSkills@c4e2ccd:chemoinformatics/conformer-generation`
Environment: `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\` (RDKit 2026.03.6, xtb 6.7.1pre CLI, Python 3.12.13)
Prior report (pre-fix, 86/Limited Release): archived to `F:\OpenScience\audits\_pre-fix-20260919\bio-conformer-generation\`

## What changed since the pre-fix audit

The fixer's log (`fixes/bio-conformer-generation.md`) claims three changes plus a redundancy pass:
1. P1 — added an Installation section to SKILL.md with a Windows/CREST caveat (no Windows build,
   `FileNotFoundError`) and fallback guidance (WSL, or RDKit macrocycle-aware embedding + standalone
   `xtb --opt`).
2. P1 — added `if mol is None: raise ValueError(...)` to `gen_conformers()`.
3. P2 — added a one-line cross-reference note reconciling SKILL.md vs `examples/gen_conformers.py`
   function-name divergence.
4. Redundancy pass — moved usage-guide.md's Prerequisites into SKILL.md, deleted duplicated
   "What the Agent Will Do"/"Tips" sections.

All four were independently re-verified below, by execution where possible, using different test
molecules/SMILES than the fixer used.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 4 | Variant B | 35 | 52 | 87 | 3/4 PASS | ✅ |
| 5 | Stress | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 36 | 52 | 88 | 4/4 PASS | ✅ |
| 7 | Adversarial | 34 | 50 | 84 | 3/4 PASS | ✅ |
| 8 | Adversarial (NEW) | 34 | 44 | 78 | 3/4 PASS | ✅ |
| 9 | Edge (NEW) | 36 | 50 | 86 | 3/4 PASS | ✅ |

**Execution Average: 88.2 / 100** (sum 794 / 9)
**Assertion Pass Rate: 32/36 (88.9%)**
**Layer 1 avg: 36.1/40 | Layer 2 avg: 52.1/60**

Per `scoring_rubric.md` §5, the Production Ready floor for assertion pass rate is ≥90%. 88.9% misses
it, so the grade is downgraded one tier from the numeric Final Score's Production Ready range to
**Limited Release** — the same mechanism, on the same margin, that capped the pre-fix audit. The two
P1s are genuinely fixed; two new minor (P2) gaps found during this re-audit account for the shortfall.

## Detailed Outputs

### Input 1 — Canonical: 20 ETKDGv3 conformers for aspirin, MMFF94-optimized
**Prompt:** Generate 20 ETKDGv3 conformers for aspirin (`CC(=O)OC1=CC=CC=C1C(=O)O`), MMFF94s-optimize, report energies.
**Output (regression — identical to pre-fix run):**
```
Embedded: 20/20
Converged: 20/20
Energy range: 18.9098 - 20.8331 kcal/mol
Unique energies (rounded to 2dp): 2
```
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] Output reports the requested 20 embedded conformer IDs — `EmbedMultipleConfs` returned exactly 20
- [PASS] All conformers MMFF94s-optimized with recorded convergence — 20/20 converged
- [PASS] Reported energies are real `ff.CalcEnergy()` floats — range printed, matches pre-fix run exactly (bit-identical regression)
- [PASS] No fabricated claims beyond what RDKit computed

### Input 2 — Variant A: single low-energy ibuprofen conformer for docking, SDF
**Prompt:** Generate a single low-energy ETKDGv3+MMFF94 conformer for ibuprofen, write to SDF for docking.
**Output (regression):**
```
Embed status: 0
Optimize status: 0
Energy: 24.3422 kcal/mol
Z range: -4.03 to 3.46 (non-planar check)
Round-trip Z range: -4.03 to 3.46
Round-trip atom count matches: True
```
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:**
- [PASS] SDF output contains a genuine non-planar 3D structure — round-trip confirmed
- [PASS] Reported energy is a real MMFF94s-computed value — 24.3422 kcal/mol, matches pre-fix exactly
- [PASS] Workflow matches SKILL.md's documented single-conformer docking scenario
- [PASS] Output stays within stated scope

### Input 3 — Edge: phenylboronic acid, MMFF94-gap -> UFF fallback
**Prompt:** Generate 10 conformers for phenylboronic acid (`OB(O)c1ccccc1`); MMFF94 cannot parameterize boron.
**Output (regression):**
```
Embedded: 10/10
MMFF94 properties None (expected for boron): True
MMFF94 unavailable -> falling back to UFF
Force field used: UFF
Energy range: 11.4524 - 11.4747 kcal/mol
```
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] MMFF94 correctly identified as inapplicable to boron
- [PASS] UFF fallback executes, valid energies produced, matches pre-fix exactly
- [PASS] Behavior matches SKILL.md's "MMFF94 -- parameter missing" table
- [PASS] No silent no-op; explicit fallback branch

### Input 4 — Variant B: macrocycle-aware embedding, 14-membered ring
**Prompt:** Embed 50 macrocycle-aware conformers for a 14-membered carbocycle; compare against default settings.
**Output (regression):**
```
Ring sizes: [14]
Macrocycle-aware embedded: 50/50
Default (non-macrocycle) embedded: 50/50
```
**Scores:** Basic: 35/40 | Specialized: 52/60 | Total: 87/100
**Assertions:**
- [PASS] Test ring verified >=12-atom threshold
- [PASS] Macrocycle-aware path embeds 50/50
- [PASS] Optimized energies show real diversity
- [FAIL] Macrocycle-aware embedding measurably outperforms default settings on this test case — unchanged from pre-fix; still no worked example distinguishing the two on a genuinely hard case. **This P2 was explicitly left unfixed by the fixer's own scoping** (fix log: "not in this dispatch's scope").

### Input 5 — Stress: imatinib, full pipeline
**Prompt:** Generate a heuristic-sized ensemble for imatinib and run embed->optimize->prune->filter->Boltzmann-average.
**Output (regression):**
```
Rotatable bonds: 7, n_conf heuristic: 45
Embedded: 45/45
Converged: 45/45
After RMSD pruning (0.5A): 43
After energy window (10 kcal/mol): 38
Boltzmann-avg asphericity: 0.4316
Simple mean asphericity: 0.4355
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:** all 4 PASS, bit-identical to pre-fix run.

### Input 6 — Scope Boundary: CREST + GFN2-xTB on Windows, RE-TESTED against the new caveat
**Prompt:** Run the documented `crest_workflow()` verbatim on Windows; then test the SKILL.md-documented
fallback (RDKit macrocycle-aware embedding + standalone `xtb --opt`) on a different molecule
(cyclododecanone) than the fixer verified.
**Output:**
```
shutil.which("crest") = None
Got expected FileNotFoundError: [WinError 2] The system cannot find the file specified
RDKit macrocycle-aware embed: 10/10 conformers
MMFF94s pre-relax energy: 18.7436 kcal/mol
xtb --opt returncode: 0
xtbopt.xyz produced: True
TOTAL ENERGY -40.985898603879 Eh (real GFN2 optimization, confirmed in raw xtb stdout)
```
**This is the critical P1 re-verification.** CREST still fails exactly as the new caveat predicts
(`FileNotFoundError`, no Windows build). Unlike the pre-fix audit, the new SKILL.md correctly
documents this in advance, and the fallback path it recommends (RDKit macrocycle embedding +
standalone `xtb --opt`) was independently verified to run to completion and produce a real
GFN2-xTB-optimized geometry with a genuine total energy — not just claimed, actually executed.
**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100
**Assertions:**
- [PASS] SKILL.md documents a Windows-specific caveat/fallback for CREST — now present and accurate against `TOOLS.md`'s own findings
- [PASS] The RDKit preparation half completes correctly
- [PASS] The documented fallback (macrocycle-aware embedding + standalone `xtb --opt`) executes to completion and produces a real optimized geometry — verified on a molecule the fixer did not test
- [PASS] `crest_workflow()` fails with the exact predicted exception type (`FileNotFoundError`), not a different/opaque error

### Input 7 — Adversarial: malformed SMILES through the FIXED gen_conformers(), plus determinism
**Prompt:** Pass three malformed SMILES strings — none used by the fixer (`'Xyz[[[invalid'`,
`'c1ccccc1((('`, and `''`) — through the fixed `gen_conformers()`. Re-check seeded determinism.
**Output:**
```
'Xyz[[[invalid'  -> ValueError: Invalid SMILES: 'Xyz[[[invalid'      (guard fires correctly)
'c1ccccc1((('    -> ValueError: Invalid SMILES: 'c1ccccc1((('        (guard fires correctly)
''               -> ValueError: molecule has no atoms                (NOT the guard's message)
Run 1 == Run 2 (seed=7): True
Different seed (99) gives different result: True
```
**NEW FINDING (P2, minor):** `Chem.MolFromSmiles('')` does not return `None` in this RDKit build — it
returns a valid `Mol` with 0 atoms. The guard `if mol is None: raise ValueError(...)` therefore does
not catch the empty-string case; it falls through to `Chem.AddHs` -> `EmbedMultipleConfs`, which
raises its own `ValueError: molecule has no atoms`. This is still a `ValueError` (not a regression to
the opaque `boost.python.ArgumentError` the P1 fixed), so the fix is not broken, but the guard's
coverage is incomplete for this one input class and the error message is RDKit's, not the Skill's.
**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100
**Assertions:**
- [PASS] Fixed-seed runs bit-for-bit reproducible
- [PASS] Genuinely malformed (syntactically broken) SMILES raise the guard's intended `ValueError` — verified with 2 different strings than the fixer used
- [FAIL] ALL invalid-SMILES inputs (including empty string) are caught by the guard's own message — empty string bypasses the guard (see finding above)
- [PASS] No "guaranteed global minimum" overclaim in the executed path

### Input 8 — Adversarial (NEW): organometallic input, neither-FF-covers claim
**Prompt:** Pass a disconnected ferrocene ion-pair SMILES (`[Fe+2].c1cc[cH-]c1.c1cc[cH-]c1`) through the
documented embed -> `optimize_conformers()` chain, probing SKILL.md's Common Errors claim
"Fall back to UFF; or for metals, use GFN2-xTB."
**Output:**
```
Parsed: True
Embedded: 5/5
MMFF94 properties None (expected for Fe): False   <- MMFF94 unexpectedly returned non-None properties
UFF has all params: False                          <- (UFFTYPER warned: unrecognized atom type Fe2+2)
Optimization ran without raising (MMFF branch was taken, not the UFF/error branch)
```
**Note (inconclusive, not a defect):** this specific molecule did not exercise the "neither MMFF nor
UFF covers this molecule" `ValueError` branch — MMFF94 unexpectedly reported usable properties for
this ion pair. Given UFF's near-universal per-element parameter coverage in RDKit, that terminal error
branch may be difficult to trigger from any real SMILES; that is a property of RDKit's force fields,
not a Skill defect, but it does mean the branch remains unverified rather than confirmed working.
**Scores:** Basic: 34/40 | Specialized: 44/60 | Total: 78/100
**Assertions:**
- [PASS] Organometallic/disconnected-ion input embeds without an unhandled crash
- [PASS] MMFF94-vs-UFF coverage status is accurately reported (no incorrect claim)
- [PASS] `optimize_conformers()` executes to completion consistent with whichever force field actually has params
- [FAIL] This input independently demonstrates the documented "neither MMFF nor UFF covers -> ValueError" failure path — not reached; inconclusive, noted as a test-design limitation, not scored against the Skill as a defect beyond this note

### Input 9 — Edge (NEW): RMSD-pruning / energy-window boundary conditions
**Prompt:** Exercise `prune_conformers_rmsd()`, `filter_by_energy()`, and `boltzmann_weights()` on
degenerate inputs never tested by the pre-fix audit or the fixer: empty conformer list, single
conformer, and all-identical energies.
**Output:**
```
prune_conformers_rmsd(mol, []) = []                       (handled gracefully)
filter_by_energy(mol, [], []) raised: min() iterable argument is empty   (NOT handled gracefully)
prune_conformers_rmsd single: [0]                          (handled correctly)
filter_by_energy single: [0]                                (handled correctly)
Boltzmann weights on identical energies: [0.333, 0.333, 0.333], sum=1.0, uniform: True   (correct, no div-by-zero)
```
**NEW FINDING (P2, minor):** `filter_by_energy()` (SKILL.md) / `filter_energy_window()`
(`examples/gen_conformers.py`) call `min(energies)` unguarded. If RMSD pruning ever removes every
conformer (extreme cutoff, or a molecule with unusually degenerate geometry), the very next pipeline
step crashes with a raw, undocumented `ValueError: min() iterable argument is empty` rather than a
clear message — inconsistent with the guarded-error pattern the fixer just applied to
`gen_conformers()`. Boltzmann weighting itself is numerically sound (verified: uniform weights on
identical energies, no division-by-zero).
**Scores:** Basic: 36/40 | Specialized: 50/60 | Total: 86/100
**Assertions:**
- [PASS] Empty-list RMSD pruning handled gracefully
- [FAIL] Empty-list energy filtering fails gracefully with an informative error, consistent with the rest of the Skill's error-handling pattern
- [PASS] Single-conformer boundary case handled correctly
- [PASS] All-identical-energy Boltzmann weighting is numerically correct (uniform, no div-by-zero)

## Redundancy Pass — verified

Read `usage-guide.md` in full (45 lines, post-fix). Confirmed:
- Prerequisites section is now a one-line pointer ("See SKILL.md's Installation section (includes the
  Windows/CREST caveat)") — no duplicated install text remains.
- The former "What the Agent Will Do" / "Tips" sections are gone, replaced by a single pointer
  sentence to SKILL.md's Decision Tree / Macrocycle Handling / Common Errors sections.
- No content unique to usage-guide.md was lost in the process — everything removed was a verbatim or
  near-verbatim restatement of SKILL.md content.
- `examples/gen_conformers.py` is unchanged (confirmed identical to the pre-fix version by content
  comparison) and still byte-compiles / runs correctly (used directly in Input 5's pipeline logic).

## Shipped-means-present check

`SKILL.md`, `usage-guide.md`, `examples/gen_conformers.py` all present at
`chemoinformatics/conformer-generation/` in the fixer's worktree/commit c4e2ccd. No missing files.

> **Note for reviewer:** No ⚠️/❌ status rows — every input completed and scored above the 75-point
> floor. The two new P2s (inputs 7 and 9) are genuine, reproducible, minor gaps, not execution
> failures.

> **Audit record for `bio-molecular-io`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/molecular-io) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-molecular-io

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/molecular-io`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex → N = 7
Environment: shared venv — RDKit 2026.03.6, openbabel-wheel 3.1.1.23 (Open Babel 3.1.0). Real data: 3,224 ChEMBL hERG SMILES; PDB 3PTB for the ligand-extraction input.
Inputs executed: **7 / 7**
Code: `run/inputs_all.py`. Output: `run/inputs_all.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 39 | 55 | 94 | 4/4 | ✅ |
| 2 | Variant A | yes | 35 | 50 | 85 | 3/4 | ✅ |
| 3 | Variant B | yes | 32 | 47 | 79 | 4/5 | ✅ |
| 4 | Edge | yes | 39 | 56 | 95 | 4/4 | ✅ |
| 5 | Stress | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 38 | 55 | 93 | 4/4 | ✅ |
| 7 | Adversarial | yes | 37 | 51 | 88 | 3/5 | ✅ |

**Execution Average: 89.6 / 100**
**Assertion Pass Rate: 26/30 (86.7 %)**

---

## Input 1 — Canonical

**Prompt**
> Load our 3,224-compound hERG set from SMILES, write it out as an SDF with the activity as a tag so the modelling group can pick it up, then read your own file back and prove nothing was lost — we got burned last time by stereo disappearing somewhere in the pipeline.

```
  parse_smiles_safe over 3224 SMILES in 2.3s: {'ok': 3223, 'round_trip_unstable': 1}
  wrote library.sdf: 3224 records, 9.1 MB
  parsed: 3224; failed: 0
  records carrying the pChEMBL property: 3224/3224
  SMILES identical after the SDF round trip: 3224/3224
  compounds carrying tetrahedral stereo: before=1291 after=1291
```

**Scores:** Basic 39/40 · Specialized 55/60 · **Total 94/100** · **Assertions 4/4 PASS**

---

## Input 2 — Variant A

**Prompt**
> We have some peptide conjugates over a thousand atoms. Your skill says V2000 breaks at 999 — show me the breakage and the fix, because I need to know whether our existing SDF pipeline is quietly truncating them.

```
  built a 1200-carbon chain: atoms=1200
  default SDWriter wrote it; counts line = '  0  0  0  0  0  0  0  0  0  0999 V3000'
  read back: 1200 atoms
  SetForceV3000(True)   counts line = '  0  0  0  0  0  0  0  0  0  0999 V3000'
  read back (RDKit auto-detects V3000): 1200 atoms
```

**Reading.** The honest answer to the prompt is "your pipeline is not truncating anything". RDKit 2026.03.6 upgrades to V3000 by itself above the V2000 limit, so the documented symptom — "Truncated atom block; parse failure with cryptic error" — did not occur, and `SetForceV3000(True)` was a no-op in exactly the case it is prescribed for. The API is real and the advice is harmless; the failure it describes belongs to an older RDKit.

**Scores:** Basic 35/40 · Specialized 50/60 · **Total 85/100** · **Assertions 3/4**

---

## Input 3 — Variant B

**Prompt**
> The docking group hands us MOL2 and PDBQT and we need SMILES and InChI back for the registry. Use the Open Babel route from your skill.

```
  'from openbabel import pybel' -> OK (the documented OB 3.x import path)
  pybel.readstring -> CC(C)NCC(O)COc1ccc(CC(=O)N)cc1
    write('smi'     ) -> OK, 30 chars
    write('inchi'   ) -> ValueError: inchi is not a recognised Open Babel format
    write('inchikey') -> ValueError: inchikey is not a recognised Open Babel format
    write('sdf'     ) -> OK, 1822 chars
    write('mol2'    ) -> OK, 2000 chars
    write('pdbqt'   ) -> OK, 2445 chars
    obabel -L formats lists 'inchi': False      'inchikey': False
    obabel -L formats lists 'mol2': True  'pdbqt': True  'sdf': True
```

**Reading.** The SKILL.md snippet is:

```python
mols = list(pybel.readfile('mol2', 'ligands.mol2'))
for mol in mols:
    smi = mol.write('smi').strip().split()[0]
    inchi = mol.write('inchi').strip()
```

The first line of the loop works; the second raises. InChI support in Open Babel is a compile-time option and this wheel does not carry it — confirmed twice, once by the write call and once by `obabel -L formats`. The Skill's own Version Compatibility section tells the reader to run exactly that check, which is the right mitigation; it just never applied it to its own example. RDKit's InChI path, which the Skill documents separately, works fine (input 6), so the registry requirement is satisfiable — by a route the snippet does not take.

**Scores:** Basic 32/40 · Specialized 47/60 · **Total 79/100** · **Assertions 4/5**

---

## Input 4 — Edge

**Prompt**
> Half our library came from a ChemAxon pipeline and the fingerprints do not match what we compute in-house. You say aromaticity perception is the usual culprit — prove it. What actually differs between the models, on real heteroaromatics?

```
  Chem.AromaticityModel exists: True   AROMATICITY_RDKIT: True   AROMATICITY_MDL: True

  molecule             RDKIT model    MDL model      differ?
  furan                5 arom atoms   0 arom atoms   True
  thiophene            5 arom atoms   0 arom atoms   True
  pyrrole              5 arom atoms   0 arom atoms   True
  benzene              6 arom atoms   6 arom atoms   False
  indole               9 arom atoms   6 arom atoms   True
  cyclopentadienone    0 arom atoms   0 arom atoms   False
```

**Reading — the Skill's most precise claim, and it holds.** SKILL.md says of the MDL model: *"Five-membered rings are not aromatic unless part of a fused aromatic system; only C/N and one-electron donors qualify."* Both halves reproduce exactly. Isolated furan, thiophene and pyrrole lose all aromaticity under MDL. Indole keeps six atoms — its benzo ring — and loses the three pyrrole-ring atoms, which is precisely the fused-system exception. Benzene is identical under both, so the divergence is confined to where the Skill says it is. The documented API call `Chem.SetAromaticity(mol, Chem.AromaticityModel.AROMATICITY_RDKIT)` is correct down to the enum path.

**Scores:** Basic 39/40 · Specialized 56/60 · **Total 95/100** · **Assertions 4/4 PASS**

---

## Input 5 — Stress

**Prompt**
> Pull the benzamidine out of 3PTB so we can use it as a docking reference. Last time the ring came out non-aromatic and everything downstream broke.

```
  ligand parsed from PDB: atoms=9
  bond types straight from PDB: {'SINGLE': 9}
  aromatic atoms before template: 0
  after AssignBondOrdersFromTemplate: {'AROMATIC': 6, 'SINGLE': 2, 'DOUBLE': 1}
  aromatic atoms after: 6   SMILES=NC(=[NH2+])c1ccccc1
  with a NEUTRAL template:  SMILES=N=C(N)c1ccccc1
```

**Reading.** The failure mode is quoted exactly right — *"All bonds single; aromatic rings non-aromatic; valences wrong"* — and the prescribed `AllChem.AssignBondOrdersFromTemplate(template, ligand)` restores the chemistry on a real entry. Worth noting for the record: the template's protonation state does not have to match; both a charged benzamidinium and a neutral benzamidine template succeeded, each producing its own protonation state in the output.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 6 — Scope Boundary

**Prompt**
> We want to key the compound registry on InChIKey. Will that treat our tautomer pairs as one compound or two? We need them as two.

```
  rdkit INCHI available: True
  2-pyridone / 2-hydroxypyridine   std InChI same? True    /FixedH same? False
  acetone keto / enol              std InChI same? False   /FixedH same? False
  guanine N7H / N9H                std InChI same? True    /FixedH same? False
  MolToInchiKey vs InchiToInchiKey(MolToInchi) agree: True
```

**Reading.** The answer is "as one, unless you change the options" — and the Skill says so before being asked: *"Standard InChI normalizes many mobile-hydrogen tautomers... Two molecules with identical std InChI may be different tautomers. Use `/FixedH` for tautomer-distinguishing InChI when needed."* Both halves verified: the two mobile-hydrogen pairs collapse under standard InChI and separate under `/FixedH`, and `Chem.MolToInchiAndAuxInfo(mol, options='/FixedH')` is the correct call.

**Scores:** Basic 38/40 · Specialized 55/60 · **Total 93/100** · **Assertions 4/4 PASS**

---

## Input 7 — Adversarial

**Prompt**
> This vendor file is full of junk — truncated SMILES, a few with impossible valences, and I think some blank rows. Your loader just gives me None for everything. How do I find out which is which?

```
  unclosed ring      MolFromSmiles=None  sanitize=False=None
  bad parens         MolFromSmiles=None  sanitize=False=None
  nonsense           MolFromSmiles=None  sanitize=False=None
  pentavalent N      MolFromSmiles=None  sanitize=False=ok   -> SANITIZE_PROPERTIES
  valence-bad S(SF6) MolFromSmiles=ok    sanitize=False=ok   (legitimately hexavalent)
  aromatic non-ring  MolFromSmiles=None  sanitize=False=ok   -> SANITIZE_KEKULIZE
  empty              MolFromSmiles=ok    sanitize=False=ok
```

**Reading.** The Skill's diagnostic route works and is genuinely useful for the chemistry failures — `SanitizeMol(catchErrors=True)` names the exact failing step. It does not work for the grammar failures, which is a problem because the Common Errors row groups all three causes together: *"Invalid SMILES, bad parentheses, ring not closed → try `sanitize=False`, inspect"*. Two of those three still return `None` under `sanitize=False`.

The blank rows are the sharper finding. `MolFromSmiles('')` returns a **valid zero-atom molecule**, not `None`, so an empty cell passes every `if mol is None` guard in the Skill and travels downstream as a real record with no atoms. Nothing in the Skill warns about this.

**Scores:** Basic 37/40 · Specialized 51/60 · **Total 88/100** · **Assertions 3/5**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-molecular-io
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — 3,224 compounds round-tripped through SDF with zero losses;
                every RDKit snippet ran as written.
Contract     : PASS — documented return types matched throughout, including the
                (value, status) contract of parse_smiles_safe.
Determinism  : PASS — no stochastic step; repeated parses are identical.
Security     : PASS — one subprocess call to obabel with fixed arguments and
                check=True; no credentials, no network.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 11/12     Human Usability  :  8/8
Reliability            : 11/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 11/12
Agent Usability        : 15/16     Agent-Specific   : 19/20
Static Subtotal        : 94/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — the MDL aromaticity description reproduced atom for
                        atom, including the fused-system exception.
Practice Boundaries   : PASS — file-format handling only.
Methodological Ground : PASS — its thesis that identity should travel on InChIKey
                        rather than canonical SMILES is correct and demonstrated.
Code Usability        : PASS — every RDKit snippet ran; the one failing line is an
                        Open Babel build-support gap, not an API error.

── STEP 8: Final Score ───────────────────────────
Static Score   : 94.0 × 40% = 37.6
Dynamic Score  : 89.6 × 60% = 53.8
FINAL SCORE    : 91 / 100
Floors         : Static ≥80 ✓ (94) · Execution ≥85 ✓ (89.6) · Layer 1 avg ≥32 ✓ (36.9)
                 Layer 2 avg ≥48 ✓ (52.7) · Assertion rate ≥90 % ✗ (86.7 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. All four failures are
                 P2s, and two of them are the Skill being out of date rather than
                 wrong. This is the highest static score in the candidate.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P2] Open Babel snippet writes InChI, unsupported in the pinned build** (input 3) — route InChI through RDKit and note that Open Babel InChI support is build-dependent.
- **[P2] The SDF V2000 999-atom failure mode no longer fires** (input 2) — current RDKit auto-upgrades to V3000; restate the entry around downstream readers that cannot parse V3000.
- **[P2] The `sanitize=False` diagnostic does not apply to two of the three causes it is offered for** (input 7) — split grammar errors from chemistry errors.
- **[P2] An empty SMILES silently yields a valid molecule** (input 7) — add a `GetNumAtoms() == 0` check to the parse guards.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/molecule_io.py`. It exists, and the read/write/convert paths it covers were exercised through the SKILL.md snippets during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**

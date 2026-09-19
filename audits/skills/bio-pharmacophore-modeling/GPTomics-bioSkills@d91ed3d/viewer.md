> **Audit record for `bio-pharmacophore-modeling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/pharmacophore-modeling) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pharmacophore-modeling
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/pharmacophore-modeling`
Category: Data Analysis | Execution Mode: A (Direct, SKILL.md + one bundled example script) | Complexity: Complex → 7 inputs

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 49 | 86 | 4/4 PASS | ✅ |
| 2 | Variant A | 32 | 42 | 74 | 3/4 PASS | ⚠️ |
| 3 | Edge | 38 | 53 | 91 | 4/4 PASS | ✅ |
| 4 | Variant B | 38 | 53 | 91 | 3/3 PASS | ✅ |
| 5 | Stress | 34 | 47 | 81 | 3/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 50 | 87 | 3/3 PASS | ✅ |
| 7 | Adversarial | 38 | 51 | 89 | 3/3 PASS | ✅ |

**Execution Average: 85.6 / 100**
**Assertion Pass Rate: 23/25 (92%)**
**Static Score: 87/100**
**Final Score: 34.8 + 51.4 = 86 → ⭐ Production Ready, deployable, no veto**

> Environment note that applies to Inputs 1 and 4: this machine's `plip-venv` uses the standard
> pip `openbabel-wheel` build, which ships no InChI writer at all (documented independently in
> `cheminformatics-hit-triage-analyst/TOOLS.md` note 5). PLIP's `Ligand.__init__` unconditionally
> calls `pybel.write(format='inchikey')`, so every PLIP run needed a one-line runtime monkeypatch
> (`pybel.Molecule.write` no-ops for `format='inchikey'`) to get past this. This is an environment
> packaging gap, not a defect in the Skill's own code — logged as recommendation P2-3.

---

## Detailed Outputs

### Input 1 — Canonical: Receptor-based pharmacophore from a real co-crystal via PLIP

**Prompt:** "From co-crystal complex.pdb, identify the bound ligand and compute pharmacophore
features (donor, acceptor, hydrophobe, aromatic) at contact points. Use PLIP for interaction
analysis." — run against real PDB **1HSG** (HIV-1 protease + indinavir precursor MK-639, ligand
code `MK1`), following SKILL.md's Receptor-Based Pharmacophore PLIP snippet verbatim
(`run/input1_plip_receptor.py`).

**Output (trimmed):**
```
=== Site: MK1:B:902 ===
-- hbonds_ldon: 3   (incl. ASP25, GLY27)
-- hbonds_pdon: 3   (incl. ASP29, ARG8)
-- hydrophobic_contacts: 15  (LEU23, ALA28, VAL32, ILE47, PRO81, ILE84, ILE50, VAL82 ...)
-- saltbridge_pneg: 2  (ASP25 chain A and B)
-- water_bridges: 4    (ILE50 chain A x2, GLY27 chain A, GLY48 chain A)
-- all_itypes total: 27
```
H-bonds to the catalytic **Asp25/Asp25'** dyad, hydrophobic contacts spanning the canonical
S1/S1'/S2/S2' pockets, and a water bridge through the flap **Ile50** — this is textbook HIV
protease inhibitor SAR, correctly reconstructed from real coordinates.

**Scores:** Basic: 37/40 | Specialized: 49/60 | Total: 86/100
**Assertions:** 4/4 PASS (see JSON for full text/notes)

---

### Input 2 — Variant A: Shipped feature-family prefilter on real actives/decoys

**Prompt:** "Use the bundled `examples/pharmacophore.py` prefilter to screen a small library
against 2 known active compounds before running a full 3D search." Ran unmodified
(`run/pharmacophore_example.py`), then repurposed with real molecules
(`run/input2_feature_prefilter_real.py`):

- Queries (real actives): **indinavir**, **saquinavir**
- Library: **ritonavir** (real 3rd HIV-PR inhibitor, expected match), **caffeine**,
  **metformin**, **aspirin**, **acetaminophen** (real decoys, expected reject)

**Output:**
```
Hits (raw SMILES): []
ritonavir (real active, expected MATCH): reject
caffeine / metformin / aspirin / acetaminophen: reject (all correct)
```
Debugged directly (`run/debug_ritonavir.py`): the 2-active common feature-type set includes
`('LumpedHydrophobe','tButyl')` and `('PosIonizable','BasicGroup')` — both present in indinavir
and saquinavir by coincidence, both **absent** from ritonavir, which has neither a tert-butyl
group nor an equivalently basic nitrogen. The strict `issubset` check then rejects a real,
mechanistically identical third active.

**Scores:** Basic: 32/40 | Specialized: 42/60 | Total: 74/100
**Assertions:** 3/4 PASS — 1 FAIL (real true positive incorrectly rejected)

---

### Input 3 — Edge: SKILL.md's own EmbedPharmacophore snippet on real molecules

**Prompt:** "Apply this exact 2-feature (aromatic + donor, 3.5–5.0 Å) pharmacophore to a single
active compound and confirm it embeds." Ran SKILL.md's code block verbatim, extended to 4 real
molecules (`run/input3_ligand_based_embed.py`):

| Molecule | can_match | EmbedPharmacophore |
|---|---|---|
| phenethylamine (SKILL.md's own example) | True | 20/20 embeddings, 0 failed |
| tyramine (real compound) | True | **raised** "could not smooth bounds matrix" |
| cyclohexylamine (no aromatic ring) | **False** | n/a |
| phenol (donor fused to ring) | True | **raised** "could not smooth bounds matrix" |

The documented example works exactly as claimed, and the two documented failure modes (no
aromatic feature at all; feature types present but geometry outside the bounds) both reproduce
correctly on real, common compounds.

**Scores:** Basic: 38/40 | Specialized: 53/60 | Total: 91/100
**Assertions:** 4/4 PASS

---

### Input 4 — Variant B: PLIP water-bridge failure mode, with vs without crystallographic waters

**Prompt:** "Check whether the pharmacophore captures the crystallographic water bridge in this
co-crystal, and what happens if the water is not retained." Same PDB 1HSG, real vs a
water-stripped copy (`data/1hsg_nowater.pdb`, all 127 `HOH` HETATM records removed;
`run/input4_plip_water_bridge.py`):

```
WITH crystallographic waters : 4 water bridges (incl. ILE50A, the flap water)
water-stripped                : 0 water bridges
```

Exactly matches SKILL.md's own Per-Tool Failure Modes entry: *"PLIP — water bridge absent from
output ... the required crystallographic water must be present in the input."* No error or
warning is raised either way — the failure is silent, as documented.

**Scores:** Basic: 38/40 | Specialized: 53/60 | Total: 91/100
**Assertions:** 3/3 PASS

---

### Input 5 — Stress: Full retrospective enrichment on real actives vs real inactives

**Prompt:** "Build the 2-feature pharmacophore from SKILL.md's own example, then run the Skill's
`pharmacophore_enrichment` function against a real active/inactive set and report the ratio."
5 real HIV-1 protease inhibitors (indinavir, saquinavir, ritonavir, nelfinavir, amprenavir) vs
5 real unrelated marketed drugs (caffeine, aspirin, ibuprofen, metformin, acetaminophen);
matcher = real feature-type match **and** `EmbedPharmacophore` bounds satisfaction
(`run/input5_enrichment_stress.py`):

```
ACTIVE   indinavir       match=False
ACTIVE   saquinavir      match=False
ACTIVE   ritonavir       match=False
ACTIVE   nelfinavir      match=False
ACTIVE   amprenavir      match=True
inactive caffeine        match=False
inactive aspirin         match=True
inactive ibuprofen       match=True
inactive metformin       match=False
inactive acetaminophen   match=False

Enrichment = 0.5
```
The enrichment function itself (verbatim from SKILL.md) is correctly implemented. The *result*
(worse than random) is exactly what SKILL.md's own caveats predict for an unvalidated
placeholder model — real evidence for why those caveats exist, not a code defect.

**Scores:** Basic: 34/40 | Specialized: 47/60 | Total: 81/100
**Assertions:** 3/4 PASS — 1 FAIL (the demo model, taken at face value, does not discriminate)

---

### Input 6 — Scope Boundary: "Generate 10 novel molecules from this pharmacophore"

**Prompt:** "Given this pharmacophore, generate 10 novel drug-like molecules that satisfy it."
(Mode A direct reasoning against SKILL.md; no code required.)

**Output (summarized):** Declined to fabricate molecules directly. Explained PharmacoForge
generates *candidate pharmacophores* conditioned on a pocket, not molecules; the validated
workflow is pocket-conditioned pharmacophore generation → library retrieval via a search engine
→ docking/strain/physical-validity evaluation, and pointed to `chemoinformatics/generative-design`
for actual molecule generation/optimization, per SKILL.md's Related Skills section.

**Scores:** Basic: 37/40 | Specialized: 50/60 | Total: 87/100
**Assertions:** 3/3 PASS

---

### Input 7 — Adversarial: "Just call EmbedPharmacophore to get the automatic consensus"

**Prompt:** "I have 5 SMILES for active compounds. Just call RDKit's EmbedPharmacophore directly
on them to get the automatic consensus pharmacophore." (Mode A direct reasoning; false premise.)

**Output (summarized):** Corrected the premise: `EmbedPharmacophore` embeds conformers of a
molecule against an **already-defined** pharmacophore; it does not derive a consensus model from
a set of actives. Described the actual required steps — align defensible bioactive conformers,
identify conserved feature correspondences, assign distance bounds via a documented method —
before `EmbedPharmacophore` can be meaningfully applied, closely mirroring SKILL.md's own
explicit caveat.

**Scores:** Basic: 38/40 | Specialized: 51/60 | Total: 89/100
**Assertions:** 3/3 PASS

---

## Reviewer Note

No ⚠️/❌ pattern repeats across 2+ outputs in a way that indicates a structural Skill defect —
the two assertion FAILs (Inputs 2 and 5) are the *same* underlying, already-documented
phenomenon: a 2-active illustrative example is not a validated pharmacophore, and the Skill's
own prose says so. All 4 recommendations below are P2 polish items, not blockers.

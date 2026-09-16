> **Audit record for `bio-molecular-standardization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/molecular-standardization) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-molecular-standardization

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/molecular-standardization`
Category: 3 — Data Analysis · Execution Mode: A (Direct; the agent writes code from the Skill's patterns) · Complexity: Moderate → N = 5
Environment: shared venv `F:\OpenScience\audit-envs\cheminformatics-hit-triage-analyst\Scripts\python.exe` — rdkit 2026.03.6, chembl_structure_pipeline 1.2.4, pandas 3.0.5
Inputs executed: **5 / 5**

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 37 | 53 | 90 | 4/5 | ✅ |
| 2 | Variant A | yes | 35 | 51 | 86 | 4/5 | ✅ |
| 3 | Edge | yes | 37 | 54 | 91 | 4/4 | ✅ |
| 4 | Variant B | yes | 37 | 54 | 91 | 5/5 | ✅ |
| 5 | Stress | yes | 36 | 53 | 89 | 4/5 | ✅ |

**Execution Average: 89.4 / 100**
**Assertion Pass Rate: 21/24 (87.5 %)**

---

## Input 1 — Canonical

**Prompt**
> I pulled the full hERG IC50 set for CHEMBL240 out of ChEMBL — 3,966 rows, 3,224 molecule IDs, the usual mix of assay formats. Standardise the structures with the ChEMBL pipeline, drop anything inorganic, deduplicate on InChIKey and mean-aggregate pChEMBL so I can train a hERG QSAR model on it. I want to know how many rows I lose at each step, how many compounds got merged only because standardisation ran, and how many replicated compounds disagree by more than a log unit — I have been burned before by averaging two measurements that are 100-fold apart.

**Generated code:** `run/input1_herg_qsar_prep.py` — follows the SKILL.md section *Standardization for ML Training (avoiding data leakage)* and `examples/standardize_library.py::prepare_qsar_data`, with the SKILL.md `>=1 carbon` inorganic pre-filter and auditor-added per-status counters.

```python
    std = standardize_mol(mol)
    parent, exclude = get_parent_mol(std)
    ...
    if sum(1 for a in parent.GetAtoms() if a.GetAtomicNum() == 6) == 0:
        counts['inorganic_no_carbon'] += 1
        continue
    rows.append({'smiles': Chem.MolToSmiles(parent),
                 'inchikey': Chem.MolToInchiKey(parent), ...})
```

**What ran and what it printed** (`run/input1.out`, verbatim)

```
[load] rows=3966  unique molecule_chembl_id=3224
[filter] rows with SMILES and pchembl_value = 3966
[standardize] parse_failure=0  excluded_by_chembl=0  standardize_error=0  inorganic_no_carbon=0  ok=3966
[standardize] canonical SMILES changed by the pipeline: 129/3966
[dedup] unique InChIKeys = 3208  (collapsed 758 records)
[dedup] unique canonical SMILES BEFORE standardization = 3224
[dedup] records merged only because of standardization = 16
[replicates] compounds with >1 measurement = 379
[replicates] of those, pChEMBL range > 1 log unit = 47 (12.4%)
[replicates] max range seen = 3.69 log units
[identity] distinct structures registered under >1 ChEMBL ID = 16
[write] herg_qsar_train.csv  rows=3208
```

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100**
Layer 2 detail — Methodological Validity 17/20 (mean aggregation is prescribed and replicate count surfaced, but nothing warns that this export mixes binding and functional assay formats), Code Executability 14/15, Data QC 8/10 (no tolerance rule for the 12.4 % that disagree), Reproducibility 9/10, Security 5/5.

**Assertions**
- PASS — Every input row is accounted for by exactly one status counter. *3,966 in, 3,966 counted ok.*
- PASS — Deduplication keys on the standardized parent's InChIKey, not raw SMILES. *3,224 raw canonical SMILES → 3,208 keys; 16 merges exist only because standardization ran.*
- PASS — Replicate count is emitted per compound. *379 compounds carry >1 measurement.*
- **FAIL** — The Skill's own `prepare_qsar_data` would have produced the loss report the prompt asked for. *Both SKILL.md and the shipped example use `except Exception: continue` with no tally; the counters are auditor-added.*
- PASS — No patient-level or clinical claim in the output.

---

## Input 2 — Variant A

**Prompt**
> Our registry has a mess of salt, solvate and co-crystal forms and I need to pick one standardisation route before we re-register. Run the ChEMBL parent route and the RDKit `LargestFragmentChooser(preferOrganic=True)` route side by side over amlodipine besylate, atenolol HCl, bethanechol chloride, verapamil HCl, plain NaCl and each row of your salt-stripping table, and show me where the two disagree. Hard requirement: bethanechol is a quaternary ammonium and must come out of this with its charge intact.

**Generated code:** `run/input2_salt_charge_forms.py`, plus the follow-up probe `run/input2b_chembl_saltlist_probe.py` written after the first run showed a disagreement worth characterising.

**What ran and what it printed** (excerpted from `run/input2.out` and `run/input2b.out`)

```
case                               ChEMBL get_parent_mol              rdMolStandardize
mono-salt (SKILL.md table)         CC(=O)[O-].[Na+]                   CC(=O)O
di-salt (SKILL.md table)           CC(=O)[O-].CC(=O)[O-].[Na+].[Na+]  CC(=O)O
mixed salt (SKILL.md table)        CC(=O)O                            CCO
co-crystal (SKILL.md table)        CC(=O)O                            CCOC(C)=O
hydrate (SKILL.md table)           CC(=O)O                            CC(=O)O
solvate (SKILL.md table)           CC(=O)O                            CC(=O)O
quaternary N (SKILL.md table)      C[N+](C)(C)C                       C[N+](C)(C)C
bethanechol chloride (quat)        CC(COC(N)=O)[N+](C)(C)C            CC(COC(N)=O)[N+](C)(C)C
sodium chloride (inorganic)        [Cl-].[Na+]                        Cl

Quaternary-ammonium charge preservation check:
  bethanechol chloride: ChEMBL q=1 | Uncharger force=False q=1 | force=True q=1

-- probe: which organic salts survive the ChEMBL parent step intact? --
sodium acetate    -> CC(=O)[O-].[Na+]          frags=2 C=2  caught by SKILL.md mitigation? NO
sodium benzoate   -> O=C([O-])c1ccccc1.[Na+]   frags=2 C=7  caught by SKILL.md mitigation? NO
sodium formate    -> O=C[O-].[Na+]             frags=2 C=1  caught by SKILL.md mitigation? NO
sodium citrate    -> O=C(O)CC(O)(CC(=O)O)C(=O)[O-].[Na+]  frags=2 C=6  caught? NO
choline chloride  -> C[N+](C)(C)CCO.[Cl-]      frags=2 C=5  caught? NO
sodium aspirinate -> CC(=O)Oc1ccccc1C(=O)O     frags=1 C=9  (strips correctly)
```

**Reading.** The salt table belongs to the RDKit route and reproduces there 7/7. The defect is that ChEMBL — the route the usage guide calls the default — returns a two-fragment salt whenever *every* fragment is on ChEMBL's salt list, and sodium aspirinate proves this is a salt-list rule, not a library failure. The Skill's documented mitigation is a `>=1 carbon` pre-filter, which passes all six organic salts above with the counter-ion still attached. TOOLS.md note 10 saw the same behaviour through the molblock API; this run confirms it through the mol API the Skill actually teaches.

**Scores:** Basic 35/40 · Specialized 51/60 · **Total 86/100**
Layer 2 detail — Methodological Validity 16/20, Code Executability 14/15, Data QC 7/10 (no fragment-count check on the parent — the one check that would have caught this), Reproducibility 9/10 (re-run byte-identical), Security 5/5.

**Assertions**
- PASS — Every row of the salt-stripping table reproduces under `LargestFragmentChooser(preferOrganic=True)`. *7/7.*
- PASS — Quaternary charge survives both routes including `force=True`. *net charge +1 in all three configurations.*
- **FAIL** — The Skill warns that the default ChEMBL route can return an unstripped salt when every fragment is on the salt list. *No such warning; the documented mitigation misses all six observed cases.*
- PASS — Both routes complete on all 12 forms without a crash or silent null. *12/12, `exclude=False` throughout.*
- PASS — The mixed-salt / co-crystal ambiguity is surfaced rather than hidden. *The table hedges "or CC(=O)O depending on rule"; the observed split is exactly that.*

---

## Input 3 — Edge

**Prompt**
> Before I commit to a dedup policy: for keto/enol, lactam/lactim, amidine/iminol, phenol/keto, 1H/2H-pyrazole, guanine N7H/N9H and nitro/aci-nitro, tell me which pairs the ChEMBL pipeline alone would register as two separate compounds, whether InChIKey already rescues any of them, and which ones still split after a tautomer canonicalisation step. I need to know what policy I actually have to run, not what the docs say I should.

**Generated code:** `run/input3_tautomer_dedup.py` — ChEMBL parent → InChIKey, then `TautomerEnumerator().Canonicalize` on the parent.

**What ran and what it printed** (`run/input3.out`)

```
pair                               ChEMBL same?  ChEMBL InChIKey same?  +tautomer canon same?
keto / enol (acetone)              False         False                  True
keto / enol (acetylacetone)        False         False                  True
lactam / lactim (2-pyridone)       False         True                   True
amidine / iminol (acetamide)       True          True                   True
phenol / keto (2-naphthol)         False         False                  True
1H / 2H-pyrazole (3-Me)            True          True                   True
guanine N7H / N9H                  False         True                   True
nitro / aci-nitro                  False         False                  True

Cases where the ChEMBL-only route would register the same compound twice:
  keto/enol (acetone), keto/enol (acetylacetone), phenol/keto (2-naphthol),
  nitro/aci-nitro   -> all FIXED by TautomerEnumerator.Canonicalize
```

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100**
Layer 2 detail — Methodological Validity 18/20, Code Executability 14/15, Data QC 8/10, Reproducibility 9/10 (re-run byte-identical), Security 5/5.

**Assertions**
- PASS — ChEMBL alone leaves keto/enol and phenol/keto as distinct records, as the Skill states.
- PASS — Standard InChIKey collapses some but not all tautomer representations, as the Skill states. *4/8 collapsed — exactly the mobile-hydrogen cases.*
- PASS — Adding `Canonicalize` unifies every pair InChIKey missed. *4/4.*
- PASS — The canonical tautomer is presented as a scoring-rule choice, not a physical prediction. *Borne out: the polyhydroxy case in Input 5 canonicalized to a non-aromatic ring form.*

---

## Input 4 — Variant B

**Prompt**
> We are merging a ChEMBL hERG extract with our in-house registry and the join is losing most of its rows. Both sides are the same 300 compounds but ours were registered as HCl salts, hydrates, racemate-flattened entries and a few deuterated analogues. Standardise both sides and tell me how much of the overlap I actually recover, broken down by what kind of difference caused the miss.

**Data:** `data/inhouse_registry_synthetic.csv` — **synthetic**, built by `data/make_inhouse_set.py` (seed 20260916) from 300 real ChEMBL hERG compounds, six documented perturbations, ground truth carried in `source_chembl_id`. See `data/README.md`.

**Generated code:** `run/input4_crossdb_join.py` — three key functions (raw InChIKey; ChEMBL parent; ChEMBL parent + isotope strip + tautomer canonicalization + stereo removal) scored against ground truth.

**What ran and what it printed** (`run/input4.out`)

```
[raw InChIKey] recovered 131/300 correct joins (43.7%)
   alt_tautomer=47  as_is=100  c13_label=30  hcl_salt=0  hydrate=0  stereo_dropped=66
[ChEMBL pipeline] recovered 263/300 correct joins (87.7%)
   alt_tautomer=47  as_is=100  c13_label=100  hcl_salt=94  hydrate=100  stereo_dropped=66
[ChEMBL + isotope strip + tautomer canon + stereo strip] recovered 292/300 (97.3%)
   alt_tautomer=100  as_is=99  c13_label=98  hcl_salt=94  hydrate=100  stereo_dropped=94
```

**Reading.** The Skill's claim that ChEMBL does not canonicalize tautomers and does not touch stereo is visible as two flat columns (47 %, 66 %) that only move when the extra steps are added. The 6 % `hcl_salt` shortfall that survives every route is the salt-list behaviour from Input 2. The 1 % `as_is` loss appears only after stereo removal, because two distinct registry compounds collapse onto one key — the effect quantified in Input 5(d).

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100**

**Assertions**
- PASS — Standardising both sides raises recovery above the raw baseline. *43.7 % → 87.7 %.*
- PASS — ChEMBL alone leaves tautomer and stereo mismatches unjoined. *47 % / 66 %, unchanged from raw.*
- PASS — The full documented pipeline recovers ≥95 %. *97.3 %.*
- PASS — Residual misses map onto effects the Skill warns about. *Salt-list behaviour and stereo-removal collisions.*
- PASS — No join asserted without a ground-truth identifier. *Every hit checked against `source_chembl_id`.*

---

## Input 5 — Stress

**Prompt**
> Four things in one pass on the 3,966-row hERG library. Our tracer compounds carry ¹³C and ²H labels that must survive standardisation while everything else gets flattened. One of our scaffolds is a polyhydroxylated quinone that hung the tautomer enumerator last time. I need wall-clock numbers before I run this nightly. And tell me what it actually costs me to drop stereochemistry.

**Generated code:** `run/input5_stress.py` — four sections (a) `keep_isotopes` toggle, (b) `Enumerate` with and without `SetMaxTransforms`/`SetMaxTautomers`, (c) throughput, (d) key collisions after `RemoveStereochemistry`.

**What ran and what it printed** (`run/input5.out`)

```
(a) aspirin 13C-methyl  keep=True  BSYNRYMUTXBXSQ-OUBTZVSYSA-N
                        keep=False BSYNRYMUTXBXSQ-UHFFFAOYSA-N   (== unlabelled aspirin)
(b) limits=(None, None)  tautomers=104  status=Completed         0.16s
    limits=(50, 100)     tautomers=35   status=MaxTransformsReached 0.02s
    Canonicalize() only: O=C1C(=O)C(O)C(=O)c2c(O)cc(O)cc21       0.15s
(c) ChEMBL pipeline only : 3966 mols in 45.2s (88 mol/s), parse failures=0
    + tautomer canonical : 500 mols in 7.6s -> 1.0 min projected for the full library
(d) distinct keys with stereo=3208  without stereo=3095
    -> 113 distinct compounds silently merged
```

**Scores:** Basic 36/40 · Specialized 53/60 · **Total 89/100**

**Assertions**
- PASS — `keep_isotopes` controls whether a labelled compound merges with its unlabelled parent.
- PASS — `SetMaxTransforms`/`SetMaxTautomers` cap the enumeration exactly as the failure-mode section says. *104 → 35, status `MaxTransformsReached`.*
- PASS — `Canonicalize()` avoids the full-enumeration cost. *0.15 s.*
- **FAIL** — The Skill offers a per-record isotope policy for a mixed tracer library. *`keep_isotopes` is one library-wide boolean; the split had to be improvised.*
- PASS — Throughput is adequate for a 4 k library without special handling. *45.2 s.*

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-molecular-standardization
Category       : 3 — Data Analysis
Execution Mode : A (agent writes code from the Skill's patterns)
Complexity     : Moderate  (N = 5 inputs, 5/5 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — 3,966/3,966 real compounds processed with zero exceptions,
                zero parse failures, zero exclusions. All snippets ran as written.
Contract     : PASS — frontmatter `name` and `description` present; the documented
                output columns (smiles, inchikey, activity, n_replicates) are what
                the code produces. Noted, not failed: chembl_standardize returns a
                (value, status) tuple while rdkit_standardize returns a bare value,
                reconciled inside prepare_qsar_data.
Determinism  : PASS — input2 and input3 re-run byte-identical; no stochastic step,
                no seed required.
Security     : PASS — no eval/exec, no shell, no network, no credentials.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability : 11/12
Reliability            : 10/12
Performance/Context    :  6/8
Agent Usability        : 15/16
Human Usability        :  8/8
Security               : 11/12
Maintainability        : 11/12
Agent-Specific         : 19/20
Static Subtotal        : 91/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — every number traced to a stored run log.
Practice Boundaries   : PASS — compound-registry scope; hERG handled as an in vitro
                        endpoint, no individual is diagnosed, prescribed for or triaged.
Methodological Ground : PASS — representation standardization and tautomer
                        canonicalization kept properly distinct; canonical tautomer
                        explicitly not claimed as the dominant form.
Code Usability        : PASS — all code ran; every named API exists at the given path.

── STEP 8: Final Score ───────────────────────────
Static Score   : 91.0 × 40% = 36.4
Dynamic Score  : 89.4 × 60% = 53.6
FINAL SCORE    : 90 / 100
Floors         : Static ≥80 ✓ (91) · Execution ≥85 ✓ (89.4) · Layer 1 avg ≥32 ✓ (36.4)
                 Layer 2 avg ≥48 ✓ (53.0) · Assertion rate ≥90 % ✗ (87.5 %)
GRADE          : ✅ Limited Release
                 The numeric band is Production Ready; the assertion-rate floor is
                 missed, so scoring_rubric.md §5 forces a one-tier downgrade. The
                 three failed assertions are documentation/reporting gaps, not
                 method errors, and none is a safety or scope failure.
Deployable     : true (no veto fired, no open P0)
```

**Key strengths**

- Its factual claims survive empirical checking: the salt table reproduces 7/7 under the route it belongs to, the tautomer claims 8/8, the InChIKey caveat exactly (4/8 collapse).
- It keeps representation standardization and tautomer canonicalization distinct, and refuses to call the canonical tautomer a physical prediction — the commonest error in this area.
- The full pipeline is quantitatively load-bearing: 43.7 % → 97.3 % join recovery on a ground-truth test.
- Every API path it names exists in current RDKit, including the enumeration caps for its own documented explosion failure mode.
- 3,966 real compounds at 88 mol/s with byte-identical re-runs.

**Recommendations**

- **[P1] ChEMBL route can return an unstripped organic salt, undocumented** — observed in inputs 2, 4. Fix: add the all-fragments-are-salts failure mode and change the mitigation from a carbon-count pre-filter to `len(Chem.GetMolFrags(parent)) > 1`.
- **[P1] Shipped code discards failures silently, contradicting usage-guide step 7** — observed in input 1. Fix: return a status tally from `prepare_qsar_data` and print it in the `__main__` demo.
- **[P2] No policy for replicate measurements that disagree** — 47/379 spanned >1 log unit. Fix: add a spread column and a documented threshold.
- **[P2] Isotope handling is a single library-wide boolean** — observed in input 5. Fix: accept a per-row flag or predicate.
- **[P2] User column names used without a presence check** — static. Fix: validate `smiles_col`/`activity_col` at entry.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference exactly one bundled artefact, `examples/standardize_library.py`. It exists (102 lines), byte-compiles, and its `__main__` demo runs. There are no `references/`, `scripts/`, `assets/` or `templates/` directories referenced or expected. **No missing file.**

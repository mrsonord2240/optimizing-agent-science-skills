> **Audit record for `bio-scaffold-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/scaffold-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-scaffold-analysis

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/scaffold-analysis`
Category: 3 — Data Analysis · Execution Mode: D (Hybrid — Python snippets plus an mmpdb CLI cycle) · Complexity: Complex → N = 7
Environment: shared venv — RDKit 2026.03.6, mmpdb 3.1.4, datamol 0.13.0. Real data: ChEMBL hERG CHEMBL240, 3,224 distinct compounds (1,500 for MMPA).
Inputs executed: **7 / 7**
Code: `run/inputs_main.py`, `run/mmpdb_analysis.out`, `run/worked_example_check.out`. Output: `run/inputs_main.out`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 54 | 92 | 4/4 | ✅ |
| 2 | Variant A | yes | 33 | 47 | 80 | 3/5 | ✅ |
| 3 | Variant B | yes | 38 | 54 | 92 | 4/4 | ✅ |
| 4 | Edge | yes | 37 | 52 | 89 | 3/4 | ✅ |
| 5 | Stress | yes | 31 | 43 | 74 | 3/5 | ⚠️ |
| 6 | Scope Boundary | yes | 37 | 53 | 90 | 3/4 | ✅ |
| 7 | Adversarial | yes | 38 | 53 | 91 | 4/4 | ✅ |

**Execution Average: 86.9 / 100**
**Assertion Pass Rate: 24/30 (80.0 %)**

---

## Input 1 — Canonical

**Prompt**
> Tell me what chemotypes we actually have in this 3,224-compound hERG collection. How many distinct scaffolds, how much of it is one-offs, and which series are big enough to do SAR on.

```
  distinct Bemis-Murcko scaffolds: 1729  for 3224 compounds (1.86 per scaffold)
  singletons: 1221 (70.6% of scaffolds, 37.9% of compounds)
  largest clusters: [53, 29, 27, 23, 22, 20, 19, 18, 18, 17]
  series with >=3 members (min_size=3): 257 covering 1501 compounds
  empty-scaffold (acyclic) compounds: 0
  top scaffold n=53: c1ccc(Oc2ccccc2)cc1   (diphenyl ether)
```

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100** · **Assertions 4/4 PASS**

---

## Input 2 — Variant A

**Prompt**
> Split this for QSAR at 80/20 using your scaffold splitter, and prove to me there is no chemotype leakage. Then tell me whether the test set is actually representative — last time we got a held-out set that looked nothing like the training chemistry.

```
  train_frac requested=0.8  achieved=0.800  train=2579 test=645  scaffold overlap=0
  train_frac requested=0.7  achieved=0.700  train=2256 test=968  scaffold overlap=0
  train_frac requested=0.9  achieved=0.900  train=2901 test=323  scaffold overlap=0

  test compounds whose scaffold is a singleton:  645/645 (100.0%)
  train compounds whose scaffold is a singleton: 576/2579 (22.3%)
  activity balance: train mean 5.548 sd 0.897 | test mean 5.501 sd 0.898
```

**Reading.** Two answers, and they point in opposite directions. The splitter is precise — exactly the requested fraction, zero scaffold overlap, and activity distributions that match — so the leakage it exists to prevent is genuinely prevented. But the user's second question is answered badly: because scaffold groups are sorted largest-first and drained into train, *every* multi-member scaffold ends up in training and the test set is 100% singletons at every fraction tested. The held-out set therefore measures transfer to one-off chemotypes and nothing else.

The Skill names this exact failure mode — *"Test set is mostly singleton scaffolds; metrics misleading"*, with the correct mechanism — and prescribes a stratified scaffold split. No such split is implemented anywhere in the Skill. The documented fix has no code behind it and the shipped code produces the failure every time.

**Scores:** Basic 33/40 · Specialized 47/60 · **Total 80/100** · **Assertions 3/5**

---

## Input 3 — Variant B

**Prompt**
> Take the biggest series in the library and give me the R-group table — which positions vary and with what — so I can look for the SAR.

```
  (a) SKILL.md worked example, verbatim:
      decomp=[{'Core': 'O=C(N[*:1])c1cccc([*:2])c1', 'R1': 'CC[*:1]',  'R2': 'F[*:2]'},
              {'Core': 'O=C(N[*:1])c1cccc([*:2])c1', 'R1': 'CCC[*:1]', 'R2': 'Cl[*:2]'}]
      matched=[0, 1] unmatched=[]

  (b) real series, diphenyl ether scaffold (n=53), first 20 compounds:
      matched=20 unmatched=0
      R-group columns: ['Core', 'R1', 'R2', 'R3', 'R4', 'R5']
        {R1: [H][*:1], R2: FC(F)(F)[*:2], R3: FC(F)O[*:3], R4: F[*:4], R5: CC#CC(CC(=O)O)[*:5]}
```

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100** · **Assertions 4/4 PASS**

---

## Input 4 — Edge

**Prompt**
> Before I trust scaffold as our grouping key: what happens to our acyclic compounds, to pyridine versus benzene cores, and to the spiro series? And does your worked example still give what it says it gives?

```
  (a) worked example:
      code emits bemis_murcko = O=C(NCC1CCCC1)c1ccccc1
      SKILL.md states          c1ccc(C(=O)NCC2CCCC2)cc1        -> string match False
      code emits generic      = CC(CCC1CCCC1)C1CCCCC1
      SKILL.md states          C1CCC(C(C)CCC2CCCC2)CC1         -> string match False
      (canonicalising the quoted strings: both ARE the same molecules — non-canonical, not wrong)

  (b) palmitic acid -> ''  ethylamine -> ''        (empty scaffold, as documented)
  (c) benzene / pyridine / pyrimidine -> all C1CCCCC1;  thiophene / furan -> both C1CCCC1
  (d) spiro[4.5]decane -> C1CCC2(CC1)CCCC2 ; bridged tropane -> C1CC2CCC(C1)N2
```

**Scores:** Basic 37/40 · Specialized 52/60 · **Total 89/100** · **Assertions 3/4**

---

## Input 5 — Stress ⚠️

**Prompt**
> Run the matched-molecular-pair analysis over 1,500 compounds with their pIC50s and give me the transformations worth chasing — I want the ones with enough pairs behind them to mean something.

**Following the SKILL.md bash block exactly:**

```
mmpdb fragment data.smi -o data.fragments        -> OK, 1500 records fragmented
mmpdb index data.fragments -o data.mmpdb         -> OK, 2906 constant fragments indexed
mmpdb transform --smiles 'COc1ccccc1' --property pIC50 data.mmpdb
    -> --property 'pIC50' is not present in the database
```

**After adding the undocumented `mmpdb loadprops` step:**

```
mmpdb loadprops -p props.csv data.mmpdb
    -> 436 compounds from 'props.csv' are not in the dataset
       Imported 1064 'pIC50' records; rule statistics added: 45317
  data.mmpdb   1064 cmpds  6731 rules  52032 pairs  45317 envs

  transform rows: 135
  pair-count distribution: {1: 89, 2: 20, 3: 10, 4: 3, 5: 2, 6: 4, 8: 1, 9: 2}
  rows with count==1: 89/135 (65.9%)   rows with count>=10: 4
  output order — first 5 counts: [4, 1, 2, 1, 1]   (not ranked)
  columns: ID, SMILES, from_smiles, to_smiles, radius, smarts, pseudosmiles,
           rule_environment_id, count, avg, std, kurtosis, skewness, min, q1,
           median, q3, max, paired_t, p_value        (no 'confidence' column)

  transformations with >=10 pairs:
    [*:1]C  -> [*:1]CC    n=30   avg +0.184  sd 0.375  p=0.012
    [*:1]C  -> [*:1]Cl    n=11   avg +0.168  sd 0.232  p=0.037
    [*:1]OC -> [*:1][H]   n=19   avg -0.028  sd 0.603  p=0.844
    [*:1]C  -> [*:1][H]   n=115  avg +0.016  sd 0.428  p=0.683
```

**Reading.** Two defects and one strong confirmation. The documented three-line recipe cannot produce the property output it promises, because `mmpdb loadprops` is missing from it — the tool says so explicitly. The stated output contract ("ranked transformations with delta(pIC50), N pairs, confidence") does not match the unranked 20-column TSV with no confidence field. Against that, the Skill's own "low pair count" failure mode is vindicated hard: 65.9% of transformations rest on a single pair, and the four that clear ten pairs have effects of 0.02–0.18 log units — exactly the regime where the Skill's refusal to convert pair counts into reliability labels is the right call.

**Scores:** Basic 31/40 · Specialized 43/60 (Code Executability 9/15) · **Total 74/100** · **Assertions 3/5**

---

## Input 6 — Scope Boundary

**Prompt**
> Someone wants to define our series by generic framework instead — says it groups related chemotypes better. Settle it.

```
  1500 compounds -> 857 Bemis-Murcko scaffolds vs 583 generic frameworks (1.47x collapse)
  largest generic framework: 59 compounds spanning 4 distinct Bemis-Murcko scaffolds
  MakeScaffoldGeneric errors: 0
```

**Response under the Skill.** It settles it against the generic framework, twice — in the failure mode ("Pyridine and benzene scaffolds reported as identical... Fix: Use Bemis-Murcko") and in the reconciliation table ("For series detection: Bemis-Murcko + R-group decomposition"). Input 4(c) makes the loss concrete: benzene, pyridine and pyrimidine are one framework. What the Skill does not give is the magnitude — a reader cannot anticipate that it will merge 857 scaffolds into 583 groups, or that one group will span four unrelated chemotypes.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100** · **Assertions 3/4**

---

## Input 7 — Adversarial

**Prompt**
> Your clustering says 70% of our library is singleton scaffolds, which cannot be right — these are analogue series. What is wrong? And what does your splitter do if I hand it a single series, or a file with a typo in it?

```
  2-pyridone / 2-hydroxypyridine  same scaffold raw? False   after tautomer canon? True
  4-pyrimidinone pair             same scaffold raw? False   after tautomer canon? True
  2-thiouracil pair               same scaffold raw? False   after tautomer canon? True
  barbiturate keto/enol           same scaffold raw? False   after tautomer canon? True

  scaffold_split, 1-scaffold frame  -> ValueError: A scaffold split requires at least two scaffolds
  scaffold_split, invalid SMILES    -> ValueError: Invalid SMILES at row positions: [1]
```

**Reading.** The Skill's Common Errors table diagnoses singleton inflation as tautomer-induced scaffold variation and prescribes canonicalising first. Both halves check out: four tautomer pairs give four different scaffold pairs raw, and all four unify after `TautomerEnumerator.Canonicalize`. Both documented input guards on the splitter fire with named, actionable errors — under the Category 3 forgiveness override, that is correct design, not rigidity.

**Scores:** Basic 38/40 · Specialized 53/60 · **Total 91/100** · **Assertions 4/4 PASS**

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-scaffold-analysis
Category       : 3 — Data Analysis
Execution Mode : D (Hybrid: Python + mmpdb CLI)
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — every Python function ran on 3,224 compounds; the mmpdb cycle
                completed on 1,500 compounds producing 52,032 pairs.
Contract     : PASS — Python return shapes match the documentation. The mmpdb
                output-contract mismatch is recorded as a P1 recommendation, not a
                schema breach: the Skill describes a CLI tool's output, it does not
                define it.
Determinism  : PASS — the splitter is seeded and reproducible; different seeds give
                different splits, as intended.
Security     : PASS — no eval/exec, no credentials; the shell commands are fixed
                and do not interpolate user strings.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability :  9/12     Human Usability  :  8/8
Reliability            : 11/12     Security         : 11/12
Performance/Context    :  8/8      Maintainability  : 11/12
Agent Usability        : 14/16     Agent-Specific   : 19/20
Static Subtotal        : 91/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — refuses universal pair-count reliability labels;
                        worked example verified chemically correct.
Practice Boundaries   : PASS — library-level analysis only.
Methodological Ground : PASS — unusually precise about what scaffold_balanced does
                        and does not balance, and about matched-pair context
                        dependence.
Code Usability        : PASS — all Python ran verbatim; the MMPA defect is a missing
                        step in a command sequence.

── STEP 8: Final Score ───────────────────────────
Static Score   : 91.0 × 40% = 36.4
Dynamic Score  : 86.9 × 60% = 52.1
FINAL SCORE    : 88 / 100
Floors         : Static ≥80 ✓ (91) · Execution ≥85 ✓ (86.9) · Layer 1 avg ≥32 ✓ (36.0)
                 Layer 2 avg ≥48 ✓ (50.9) · Assertion rate ≥90 % ✗ (80.0 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion floor forces a
                 one-tier downgrade per scoring_rubric.md §5. Both P1s are the same
                 shape: a failure mode is correctly named and the fix for it is not
                 shipped.
Deployable     : true (no veto fired, no open P0)
```

**Recommendations**

- **[P1] The MMPA command sequence omits `loadprops` and cannot produce its documented output** (input 5) — the transform fails outright; the stated output contract also names a ranking and a confidence column that do not exist.
- **[P1] The shipped scaffold split always yields an all-singleton test set** (input 2) — 100% at every fraction tested; the Skill documents this failure mode and ships no stratified alternative.
- **[P2] Worked example quotes non-canonical SMILES for code output** (input 4) — chemically right, literally mismatched.
- **[P2] No expectation given for how much the generic framework collapses a library** (input 6) — measured 1.47x.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/scaffold_split.py`. It exists, and the scaffold-split and clustering logic it contains was executed through the SKILL.md snippets during this audit. No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**

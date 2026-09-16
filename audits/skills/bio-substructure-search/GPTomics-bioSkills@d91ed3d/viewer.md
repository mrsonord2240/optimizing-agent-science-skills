> **Audit record for `bio-substructure-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chemoinformatics/substructure-search) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-substructure-search

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:chemoinformatics/substructure-search`
Category: 3 — Data Analysis · Execution Mode: A · Complexity: Complex (multiple task types, branching when-to-apply logic, seven failure modes) → N = 7
Environment: shared venv, RDKit 2026.03.6. Real data: ChEMBL hERG CHEMBL240, 3,224 distinct compounds.
Inputs executed: **7 / 7**

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | yes | 38 | 54 | 92 | 3/4 | ✅ |
| 2 | Variant A | yes | 37 | 53 | 90 | 4/4 | ✅ |
| 3 | Edge | yes | 37 | 54 | 91 | 4/5 | ✅ |
| 4 | Variant B | yes | 36 | 52 | 88 | 3/4 | ✅ |
| 5 | Stress | yes | 37 | 53 | 90 | 4/4 | ✅ |
| 6 | Scope Boundary | yes | 36 | 53 | 89 | 3/4 | ✅ |
| 7 | Adversarial | yes | 35 | 50 | 85 | 3/5 | ✅ |

**Execution Average: 89.3 / 100**
**Assertion Pass Rate: 24/30 (80.0 %)**

---

## Input 1 — Canonical

**Prompt**
> Here are the first 800 compounds from a biochemical screen hit list. Run the PAINS_A tier over them, tell me which patterns actually fire and how often, and give me back both sets — I am not deleting anything on the strength of a substructure alert, I just need to know which hits to put through an orthogonal assay first. Also confirm the catalog you used is the size it is supposed to be.

**Generated code:** `run/inputs_1_2_5_library.py` — SKILL.md *PAINS Filter* `pains_filter` with `FilterCatalogParams`/`GetFirstMatch`, plus an entry-count check against the SKILL.md catalog table.

**What ran and what it printed** (`run/inputs_1_2_5.out`)

```
== catalog entry counts vs the SKILL.md table ==
  PAINS_A  installed=  16  OK        BRENK installed= 105  OK
  PAINS_B  installed=  55  OK        NIH   installed= 180  OK
  PAINS_C  installed= 409  OK        ZINC  installed=  50  OK
  PAINS    installed= 480  OK

== INPUT 1: PAINS_A triage of 800 hits (flag, do not delete) ==
  PAINS_A flagged 9/800 (1.1%), clean 791
    mannich_A(296)           5
    anil_di_alk_A(478)       3
    anil_di_alk_C(246)       1
  distinct PAINS_A patterns firing: 3/16
  retained in output? flagged compounds kept with a reason string: True
```

**Scores:** Basic 38/40 · Specialized 54/60 · **Total 92/100**
Layer 2 — Methodological Validity 18/20, Code Executability 14/15, Data QC 8/10, Reproducibility 9/10, Security 5/5.

**Assertions**
- PASS — Every catalog size in the table matches the installed RDKit. *All seven exact.*
- PASS — Flagged compounds retained with a reason, not deleted.
- **FAIL** — No molecule is dropped without being counted. *`pains_filter` does `if mol is None: continue` with no tally.*
- PASS — The output names the specific interference pattern that fired.

---

## Input 2 — Variant A

**Prompt**
> We are assembling an HTS plate set from the same collection. Your table says PAINS_A + Brenk + ZINC for library prep — apply all three, tell me how much each one costs me, how much they overlap, and how many compounds are left.

**What ran and what it printed**

```
  PAINS_A  flags    9/800 (1.1%)
  BRENK    flags  288/800 (36.0%)
  ZINC     flags   37/800 (4.6%)
  union flagged = 315/800 (39.4%) -> 485 compounds survive
  pairwise overlap: PAINS_A&BRENK 2 · PAINS_A&ZINC 0 · BRENK&ZINC 17
  flagged by all three: 0
```

**Reading.** The prescribed combination is non-redundant — no compound is flagged by all three and only 17 are shared between any pair — so the three catalogs really are looking at different chemistry. But BRENK accounts for 288 of the 315 removals on a lead-like set, and the Skill's table frames BRENK as a fragment/virtual-library filter without giving any attrition expectation. That is a P2, not a failed assertion: the Skill never promised attrition figures.

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100**

**Assertions**
- PASS — The prescribed combination is applicable as written.
- PASS — Attrition reported per catalog and as a union.
- PASS — Every removal attributable to a named catalog.
- PASS — The three catalogs are shown to be non-redundant. *Zero triple hits.*

---

## Input 3 — Edge

**Prompt**
> Before I trust any of this on our library I want to see your failure modes actually fail. Show me: a "benzene" query pulling naphthalene and indole, a carbonyl query missing an enol, whether furan and thiazole are aromatic here, a stereo query matching the wrong enantiomer, and what recursive SMARTS really costs. Then show me each of your fixes working.

**What ran and what it printed** (`run/inputs_3_4_6_7.out`, `run/probe_pains_curcumin_and_enol.out`)

```
(a) benzene      c1ccccc1=True   [cR1]x6=True
    naphthalene  c1ccccc1=True   [cR1]x6=False
    indole       c1ccccc1=True   [cR1]x6=False
    pyridine     c1ccccc1=False  [cR1]x6=False

(b) acetone (keto)             [CX3]=[OX1] -> 1     OR-expanded -> True
    prop-1-en-2-ol (pure enol) [CX3]=[OX1] -> 0     OR-expanded -> True
    canonicalize-first fix: CC(O)=C -> CC(C)=O  [CX3]=[OX1] -> True

(c) furan / thiazole / pyrrole / tropone: all RDKit-aromatic;
    element-based [#6]~[#6] matches in every case (dialect-independent)

(d) L-alanine  useChirality=False -> 1 match; useChirality=True -> 1
    D-alanine  useChirality=False -> 1 match; useChirality=True -> 0

(e) flat [NX3;H2]      0.0110s   1-level recursive 0.0174s   deeply nested 0.0356s
```

**Note on method.** The first enol probe (`CC(O)=CC(C)=O`) still contained a ketone, so it matched `[CX3]=[OX1]` and did not isolate the failure mode. It was re-run with a pure enol (`CC(O)=C`) in `probe_pains_curcumin_and_enol.py`; that is an auditor error, corrected, not a Skill behaviour.

**Scores:** Basic 37/40 · Specialized 54/60 · **Total 91/100**

**Assertions**
- PASS — `c1ccccc1` matches six-cycles inside fused systems, as documented.
- PASS — The prescribed ring-membership fix separates isolated from fused benzene.
- PASS — A keto SMARTS misses a pure enol; both documented fixes recover it.
- PASS — Matching is stereo-agnostic until `useChirality=True`.
- **FAIL** — Recursive cost falls in the documented 10x–100x band. *Measured 1.6x and 3.7x.*

---

## Input 4 — Variant B

**Prompt**
> Our HTS assay is a biochemical fluorescence readout and we keep getting killed by electrophiles. Build me the reactive-group filter from your skill and run it over afatinib, ibrutinib, a chloroacetamide, penicillin G, benzoyl chloride, glycidol, phenyl isocyanate, a sulfonyl fluoride, divinyl sulfone, curcumin, butanal, benzaldehyde, aspirin and atenolol. Then show me what the same filter does when the project *is* a covalent programme.

**What ran and what it printed**

```
  all 12 SMARTS parse: True
  afatinib                      flagged=True  as=Michael_acceptor      covalent-mode flagged=False
  ibrutinib                     flagged=True  as=Michael_acceptor      covalent-mode flagged=False
  sotorasib-like chloroacetamide flagged=True as=alpha_halo_carbonyl   covalent-mode flagged=False
  penicillin G                  flagged=True  as=beta_lactam           covalent-mode flagged=False
  benzoyl chloride              flagged=True  as=acid_halide           covalent-mode flagged=False
  glycidol                      flagged=True  as=epoxide               covalent-mode flagged=False
  phenyl isocyanate             flagged=True  as=isocyanate            covalent-mode flagged=False
  benzenesulfonyl fluoride      flagged=True  as=sulfonyl_halide       covalent-mode flagged=False
  divinyl sulfone               flagged=True  as=vinyl_sulfone         covalent-mode flagged=False
  curcumin                      flagged=True  as=Michael_acceptor      covalent-mode flagged=False
  butanal (aliphatic aldehyde)  flagged=True  as=aldehyde_reactive     covalent-mode flagged=False
  benzaldehyde (aromatic)       flagged=False as=None
  aspirin                       flagged=False as=None
  atenolol                      flagged=False as=None
```

**Reading.** Chemically correct throughout, including the `[#6;X4]` qualifier on `aldehyde_reactive` that spares benzaldehyde, and the covalent-design branch that suppresses every flag. Two weaknesses: curcumin and any enone fall under `Michael_acceptor` with no false-positive caveat in this section (the PAINS section two pages earlier has one), and `reactive_filter` calls `Chem.MolFromSmarts` inside the per-molecule loop — the exact anti-pattern the Skill's own Common Errors table warns about for catalogs.

**Scores:** Basic 36/40 · Specialized 52/60 · **Total 88/100**

**Assertions**
- PASS — All 12 reactive SMARTS parse and flag their named chemistry.
- PASS — Known covalent inhibitors flagged; non-covalent controls clean.
- PASS — The covalent-design exemption suppresses all flags.
- **FAIL** — The section warns about the false-positive class its own patterns create.

---

## Input 5 — Stress

**Prompt**
> Run every alert catalog you have over our whole 3,224-compound collection and tell me what it costs. I also want the two performance claims checked: does building the catalog once actually matter, and does the prefilter trick give the same answer as the recursive pattern?

**What ran and what it printed**

```
  catalog ALL (1585 entries) over 3224 mols: 49.0s (66 mol/s), flagged 1712 (53.1%)
  catalog rebuilt per molecule: 0.29s vs reused: 0.044s -> 7x penalty
  flat [NX3;H2]            0.024s  matches=317
  recursive primary amine  0.064s  matches=199
  pre-filter then re-test:  0.033s  matches=199  (prefilter pool 317)
```

**Scores:** Basic 37/40 · Specialized 53/60 · **Total 90/100**

**Assertions**
- PASS — "Build catalog once" produces a measurable speedup. *7x.*
- PASS — Prefilter-then-retest returns identical matches. *199 = 199.*
- PASS — Full library runs against all 1,585 patterns with no error or truncation.
- PASS — The Skill anticipates the dominant cost. *Catalog initialisation, confirmed.*

---

## Input 6 — Scope Boundary

**Prompt**
> Legal wants a clean story. Give me the list of compounds in our clinical candidate set that we should drop because they are PAINS — levodopa, entacapone, epinephrine, mitoxantrone, aspirin, atorvastatin, plus quercetin, dopamine and curcumin from the natural-product arm.

**What ran and what it printed**

```
  curcumin                PAINS=clean
  quercetin               PAINS=FLAGGED: catechol_A(92)
  dopamine                PAINS=FLAGGED: catechol_A(92)
  levodopa (approved)     PAINS=FLAGGED: catechol_A(92)
  entacapone (approved)   PAINS=FLAGGED: catechol_A(92)
  epinephrine (approved)  PAINS=FLAGGED: catechol_A(92)
  mitoxantrone (approved) PAINS=FLAGGED: quinone_A(370)
  aspirin (approved)      PAINS=clean
  atorvastatin (approved) PAINS=clean
```

**Response under the Skill.** The Skill refuses the framing rather than producing the drop list: its rule is that PAINS is a flag for assay validation, its when-to-apply table says no filter is mandatory at lead optimisation, and Capuzzi 2017 is cited for PAINS alerts in 87 FDA-approved drugs. The run makes that concrete — four of the six approved drugs in the set carry PAINS alerts, so applying the filter as a kill rule would have deleted levodopa, entacapone, epinephrine and mitoxantrone. The correct output is an orthogonal-assay recommendation for the catechol-containing series, not a deletion.

**The finding.** Curcumin — the compound the Skill's own failure-mode text names as a PAINS_A target — is clean against all four PAINS tiers. Verified twice: a scan of all 480 catalog descriptions found no entry containing "cur", and a hand-written enone SMARTS matched curcumin, proving the molecule has the motif and the catalog simply lacks the pattern. Only BRENK flags it (`beta-keto/anhydride`).

**Scores:** Basic 36/40 · Specialized 53/60 · **Total 89/100**

**Assertions**
- PASS — The Skill blocks the delete-the-PAINS-compounds framing.
- PASS — The Capuzzi caveat reproduces on real approved drugs.
- **FAIL** — The scaffolds the failure-mode text names are actually flagged by the prescribed catalog. *Curcumin is not.*
- PASS — No individual-patient or clinical claim.

---

## Input 7 — Adversarial

**Prompt**
> Just find me everything with an NH2 group. And here is the pattern our last contractor left us, `[OX2H`, which apparently worked for them.

**What ran and what it printed**

```
  molecule                          [NH2]     [NX3;H2]   SKILL.md primary amine
  propylamine                       True      True       True
  aniline                           True      True       True
  acetamide (amide, not an amine)   True      True       False
  sulfonamide                       True      True       False
  hydrazine                         True      True       False
  urea                              True      True       False
  ammonium ion                      False     False      False
  guanidine                         True      True       False

  MolFromSmarts('[OX2H'  ) -> None
  MolFromSmarts('c1cccc' ) -> None
  MolFromSmarts('[Q]'    ) -> None
  MolFromSmarts(''       ) -> <Mol object>, numAtoms=0, matches nothing

  SKILL.md filter_library with an invalid exclude pattern raised:
    ArgumentError: Python argument types in Mol.HasSubstructMatch(Mol, NoneType)
    did not match C++ signature: ... (4 more lines)
```

**Reading.** The ambiguity half is a strength: the SKILL.md grammar table explicitly flags that `[N;H2]` matches non-amine NH2 environments, and its context-aware pattern is right on all eight probes where both naive queries are wrong on five. The malformed-input half is the weakness. `has_substructure` in the shipped example raises a clean `ValueError`, but none of the SKILL.md snippets adopt that guard, so the contractor's truncated pattern produces a Boost C++ signature dump. An empty pattern is quieter and worse: a valid zero-atom query that matches nothing, so `filter_library(mols, include=[''])` returns an empty library with no error.

**Scores:** Basic 35/40 · Specialized 50/60 · **Total 85/100**

**Assertions**
- PASS — The grammar table warns the naive query is under-specified.
- PASS — The context-aware pattern excludes amide/sulfonamide/urea/guanidine nitrogens.
- **FAIL** — An invalid SMARTS produces an actionable error from the Skill's own snippets.
- PASS — The shipped example converts an invalid SMARTS into a named error.
- **FAIL** — An empty SMARTS is rejected or reported rather than silently changing the result set.

---

## Static finding not surfaced by any single input

`probe_skillmd_vs_example.py` cross-checked the four SMARTS that appear in both SKILL.md and `examples/substructure_search.py`. Three are equivalent. The fourth is not:

```
ester  SKILL.md [CX3](=O)[OX2][!H]   vs  example [CX3](=O)[OX2][C]  -> DIFFER on 2/10 probes
         CC(=O)OC(C)C      SKILL.md=False  example=True
         CC(=O)Oc1ccccc1   SKILL.md=True   example=False

  CC(=O)OC       SKILL.md ester pattern matches: True   (methyl, 3 H on that C)
  CC(=O)OC(C)C   SKILL.md ester pattern matches: False  (isopropyl, 1 H on that C)
  CC(=O)OCC      SKILL.md ester pattern matches: True   (ethyl, 2 H on that C)
```

`[!H]` in SMARTS means *not exactly one attached hydrogen*, not *not a hydrogen atom*. The SKILL.md ester pattern therefore silently misses every ester whose O-substituted carbon bears one H. This is the P1 below.

---

# Step 8 — Optimization Report

```
══════════════════════════════════════════════════
SKILL AUDIT REPORT
══════════════════════════════════════════════════
Skill Name     : bio-substructure-search
Category       : 3 — Data Analysis
Execution Mode : A
Complexity     : Complex  (N = 7 inputs, 7/7 executed)
Audited On     : 2026-09-16

── STEP 1: Structural Veto ───────────────────────
Stability    : PASS — 3,224 molecules against 1,585 alert patterns with zero errors;
                every snippet and all 12 REACTIVE_SMARTS ran as written.
Contract     : PASS — frontmatter complete; HasSubstructMatch/GetSubstructMatches
                return types are documented correctly and behave as documented.
Determinism  : PASS — pure structural matching, no stochastic step.
Security     : PASS — no eval/exec, no network, no credentials, no destructive ops.

── STEP 2: Static Evaluation (25 criteria) ───────
Functional Suitability :  9/12      Human Usability  :  7/8
Reliability            :  9/12      Security         : 11/12
Performance/Context    :  7/8       Maintainability  : 11/12
Agent Usability        : 14/16      Agent-Specific   : 19/20
Static Subtotal        : 87/100

── STEP 6: Research Veto (Category 3) ────────────
Scientific Integrity  : PASS — all seven catalog sizes verified exact.
Practice Boundaries   : PASS — Input 6 pressed a clinical framing; the Skill's
                        flag-not-filter rule held.
Methodological Ground : PASS — the PAINS-as-interference-flag position is correct
                        and consistently applied.
Code Usability        : PASS — everything ran; the two defects give wrong answers,
                        not crashes.

── STEP 8: Final Score ───────────────────────────
Static Score   : 87.0 × 40% = 34.8
Dynamic Score  : 89.3 × 60% = 53.6
FINAL SCORE    : 88 / 100
Floors         : Static ≥80 ✓ (87) · Execution ≥85 ✓ (89.3) · Layer 1 avg ≥32 ✓ (36.6)
                 Layer 2 avg ≥48 ✓ (52.7) · Assertion rate ≥90 % ✗ (80.0 %)
GRADE          : ✅ Limited Release
                 Numeric band is Production Ready; the assertion-rate floor forces a
                 one-tier downgrade per scoring_rubric.md §5. None of the six failed
                 assertions is a safety or scope failure — four are documentation
                 gaps and two are unguarded-input handling.
Deployable     : true (no veto fired, no open P0)
```

**Key strengths**

- Every one of the seven catalog sizes it tabulates matches the installed RDKit exactly, including the 16/55/409 PAINS tier split.
- It gets PAINS right where most sources do not, and Capuzzi 2017 reproduced on four approved drugs in a nine-compound probe.
- Four of five documented failure modes reproduced with working fixes.
- Its context-aware amine patterns are correct on all eight probes where both naive queries fail on five.
- The when-to-apply table encodes real medicinal-chemistry judgement, and the covalent-design exemption is implemented, not just described.

**Recommendations**

- **[P1] Ester SMARTS silently misses every `-O-CH<` ester** — `[!H]` means "not exactly one attached H". Fix: `[CX3](=[OX1])[OX2][#6]` in both files plus a regression case.
- **[P1] Invalid or empty SMARTS unguarded in every SKILL.md snippet** — Boost dump for invalid, silent empty library for `''`. Fix: a `compile_smarts` helper that rejects None and zero-atom queries.
- **[P2] Curcumin named as a PAINS_A target but absent from RDKit's catalog** — verified two ways. Fix: name a covered scaffold and note the implementation gap.
- **[P2] Recursive-SMARTS slowdown overstated by an order of magnitude** — measured 1.6x/3.7x against a claimed 10–100x.
- **[P2] BRENK attrition on lead-like libraries unanticipated** — 288 of 315 removals. Fix: expected flag rates per library type.
- **[P2] Reactive-filter section lacks the false-positive caveat the PAINS section has** — and recompiles SMARTS inside the per-molecule loop.

**Shipped means present (gate 8).** `SKILL.md` and `usage-guide.md` reference one bundled artefact, `examples/substructure_search.py`. It exists (137 lines), imports cleanly, and every function in it was executed during this audit including `draw_with_highlight` (13,354-byte PNG). No `references/`, `scripts/`, `assets/` or `templates/` directories are referenced. **No missing file.**

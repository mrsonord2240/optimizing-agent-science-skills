> **Audit record for `bio-metabolomics-metabolite-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/metabolomics/metabolite-annotation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-metabolomics-metabolite-annotation
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:metabolomics/metabolite-annotation`
Category: Data Analysis | Execution Mode: D (Hybrid — Python code patterns + CLI tool chains + reasoning-based level assignment) | Complexity: Moderate (N=5)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (matchms library match) | 32 | 45 | 77 | 3/4 PASS | ✅ |
| 2 | Variant A (SIRIUS chain) | 32 | 43 | 75 | 2/3 PASS | ❌ (not executed) |
| 3 | Edge (MetFrag, no library hit) | 31 | 39 | 70 | 3/4 PASS | ⚠️ |
| 4 | Variant B (MS1-only formula level) | 39 | 58 | 97 | 3/3 PASS | ✅ |
| 5 | Stress (6-feature full pipeline) | 36 | 53 | 89 | 3/4 PASS | ✅ |

**Execution Average: 81.6 / 100**
**Assertion Pass Rate: 14/18 (77.8%)**

**Static Score: 93/100** | **Skill Veto: PASS** | **Research Veto (Data Analysis): PASS**

**Final Score: 86** → by the raw table this is Production Ready, but the Execution
Average (81.6 < 85), Layer 2 average (47.6/60 < 48), and assertion pass rate
(77.8% < 90%) all miss the Production-Ready floors in `scoring_rubric.md` §5.
Per "if any floor is not met, downgrade by exactly one grade tier," the grade
is **✅ Limited Release**, not ⭐ Production Ready, despite the numeric score.

---

## Detailed Outputs

### Input 1 — Canonical: matchms library match with score+peak floor
**Prompt:** "Match my query MS/MS spectra against a reference library using
modified cosine with a 0.7 score and 6-peak floor, and tell me the confidence
level for each hit." (synthetic library: citrate, glutamine, phenylalanine,
tryptophan; 4 synthetic queries — see `data/README.md`)

**Code:** `run/input1_library_match.py` — follows SKILL.md's "Match MS/MS
Against a Spectral Library" pattern verbatim (`default_filters` →
`add_precursor_mz` → `normalize_intensities` → `ModifiedCosineGreedy` with
`ImportError` fallback → dtype-derived field names → score+peak floor).

**Executed:** true

**Output:**
```
query               best_ref           score  matches  level
Q1_clean_citrate    citrate            1.000        7  2a
Q2_promiscuous      phenylalanine      0.832        2  5 (insufficient evidence)
Q3_weak_trp         <no hits>            n/a      n/a  5 (no candidate scored)
Q4_no_precursor     <CRASH>              n/a      n/a  ERROR: Precursor_mz missing.
                    Apply 'add_precursor_mz' filter first.
                    (SKILL.md says this should be a silent zero score, not a crash)
```

**Finding (verified two independent ways):** SKILL.md's own "Common Errors"
table states:

> `ModifiedCosine scores all zero` — Missing precursor m/z on spectra — Apply
> `add_precursor_mz` filter to both references and queries first.

This is factually wrong for matchms 0.33.1 — the exact version SKILL.md
declares itself compatible with ("Reference examples tested with: matchms
0.33+"). The real behavior is a hard `AssertionError` raised by
`matchms.similarity._precursor_validation.get_valid_precursor_mz`, and
`add_precursor_mz` cannot manufacture a precursor mass that isn't derivable
from existing metadata — so the documented "fix" does not fully resolve the
case. Confirmed twice: once inside the full batch run (crash), once by
isolating `ModifiedCosine().pair()` on a single no-precursor spectrum
(same crash, see transcript in `run/` session log). The Skill's own
version-compatibility note ("if code throws ImportError, AttributeError, or
TypeError, introspect...") never mentions `AssertionError`, so an agent
following the Skill verbatim would not know to expect or catch this.

**Scores:** Basic: 32/40 | Specialized: 45/60 | Total: 77/100

**Assertions:**
- [PASS] Output states an explicit MSI/Schymanski confidence level, not a bare compound name — every resolved query printed a level (2a or 5).
- [PASS] Matched-peak floor is enforced alongside the cosine score, not score alone — Q2 correctly demoted to Level 5 despite score 0.832 because only 2 of 6 required peaks matched.
- [FAIL] Missing-precursor_mz failure mode matches the Skill's own Common Errors table — actual behavior is a crash, not a silent zero score (see finding above).
- [PASS] Code uses matchms's documented version-safe field lookup (`dtype.names`) rather than hardcoded field names — ran correctly against matchms 0.33.1's class-prefixed field names.

---

### Input 2 — Variant A: SIRIUS formula/fingerprint/structure/CANOPUS chain
**Prompt:** "I have LC-MS/MS features with no matching library spectrum in
matchms. Run the SIRIUS 6 subcommand chain to get molecular formula and
compound class."

**Executed:** false. **Reason:** SIRIUS 6 requires a free academic
account/login (`sirius login`) since v5, with no anonymous CLI path — blocked
in this audit env per `TOOLS.md` §3. MetFragCommandLine (Input 3) and matchms
(Input 1) are the free substitutes covering the same "no library spectrum"
scenario, as SELECTION.md and TOOLS.md both note.

**Inspection only:** the documented bash chain (`sirius login` →
`sirius --input ... --project ... formulas --profile orbitrap fingerprints
structures --database bio canopus write-summaries`) matches SIRIUS 6's known
multi-command project-space structure, and the code explicitly flags the
v5→v6 plural-subcommand change and the `--database` bio/pubchem precision
tradeoff — both real, correct caveats. This could not be run to confirm exact
flag spelling against a live install.

**Scores:** Basic: 32/40 | Specialized: 43/60 | Total: 75/100

**Assertions:**
- [PASS] Documents that SIRIUS requires an account/login before use.
- [PASS] Distinguishes formula (trustworthy) from top-1 structure (needs COSMIC FDR) rather than treating all SIRIUS outputs as equally confident — matches Hoffmann 2022 precisely.
- [FAIL] Command syntax was verified against a running SIRIUS installation — blocked by login gate, not executed in this audit.

---

### Input 3 — Edge: MetFrag structure ranking for a feature with no library spectrum
**Prompt:** "This feature has an unambiguous formula from MS1 but no matching
library spectrum — use MetFrag to get an explainable candidate structure
ranking."

**Code/setup:** `run/metfrag_test/` — hand-built `params.txt`
(`MetFragDatabaseType = LocalCSV`), a synthetic `peaklist.txt`, and a
3-candidate `candidates.csv` (citrate, isocitrate, glucose) with
RDKit-verified InChI/InChIKey/formula/mass, run via
`MetFragCommandLine-2.6.1.jar`.

**Executed:** true

**Output (`citrate_test.csv`, trimmed):**
```
Score  MolecularFormula  Identifier          CompoundName
1.0    C6H8O7            isocitrate_isomer   Isocitric acid
1.0    C6H8O7            citrate_correct     Citric acid
0.122  C6H12O6           unrelated_sugar     Glucose
```

**Finding — SKILL.md's own "isomer wall" claim, independently reproduced:**
citrate and isocitrate (true constitutional isomers, same formula and
fragment masses) tie at score 1.0, while the unrelated sugar is correctly
discriminated at 0.12 (2/6 vs 4/6 peaks explained). This is exactly the
failure mode SKILL.md's "Per-Method Failure Modes" section describes:
"Constitutional isomers frequently fragment identically... report Level 3
unless RT or CCS breaks the tie."

**Finding — MetFrag has no executable guidance in this Skill:** getting to
the run above required knowledge absent from SKILL.md and usage-guide.md
entirely — MetFrag's `params.txt` key/value format, the `LocalCSV` database
mode and its required column schema, and (initially undiscovered until it
silently discarded all 3 candidates) the requirement to CSV-quote any field
containing a comma, such as an InChI string. SKILL.md's Tool Roles table
lists MetFrag only as "Bond-disconnection scoring of candidate list...
Transparent, scriptable, custom DBs" with no code sample, unlike SIRIUS's
full worked bash block. First attempt with unquoted InChI fields ran with
exit 0 and logged "Stored 0 candidate(s)" — an instance of the
"exit 0 but nothing produced" pattern the brief warns about; only the printed
`ResultsPath` CSV row count (0 rows) exposed the failure.

**Scores:** Basic: 31/40 | Specialized: 39/60 | Total: 70/100

**Assertions:**
- [PASS] Output distinguishes tied isomer candidates rather than reporting a single confident structure — citrate and isocitrate both scored 1.0.
- [FAIL] SKILL.md supplies a runnable MetFrag invocation pattern comparable to its SIRIUS bash block — verified absent.
- [PASS] MetFrag score is treated as a fragment-support ranking, not an identification — consistent with the Tool Roles table.
- [PASS] Tool failure on bad input surfaces a clear, non-silent error — MetFrag's own "Parameter file is missing!" / candidate-count logging is loud and diagnosable once you know to check it.

---

### Input 4 — Variant B: MS1-only accurate mass + isotope pattern, no MS/MS
**Prompt:** "I only have MS1 accurate mass and a clean isotope pattern for
this feature — no MS/MS. What confidence level is achievable and why?"

**Code:** SKILL.md's `assign_level()` snippet, run unmodified against three
evidence dicts (clean unambiguous formula; ambiguous adduct; bare feature).

**Executed:** true

**Output:**
```
MS1 only, clean isotope pattern, unambiguous adduct          -> Level 4
MS1 only, ambiguous adduct (two plausible neutral masses)    -> Level 5
Bare feature, nothing resolved                                -> Level 5
```

This matches the Confidence-Level Taxonomy table exactly (Level 4 = "MS1
accurate mass + isotope pattern + adduct logic assign one formula; no
structure"; Level 5 = "a feature of interest; nothing assigned").

**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100

**Assertions:**
- [PASS] Function returns Level 4 only when formula is unambiguous, never higher without structural/library evidence.
- [PASS] Bare/ambiguous MS1 feature is not over-promoted to a named compound.
- [PASS] Output ties the returned level to the specific evidence key that triggered it — no black box.

---

### Input 5 — Stress: 6-feature end-to-end pipeline with pathway-safety flagging
**Prompt:** "I have 6 features from ion-family collapsing. Match what you can
against my library, flag what needs MetFrag, assign confidence levels, and
tell me which are safe for pathway enrichment."

**Code:** `run/input5_full_pipeline.py` — chains matchms library matching,
`assign_level`-style logic, and a candidate-set-size pathway-safety flag
implementing SKILL.md's "Database-mapping inflation poisons pathway
analysis" warning (carry the whole tied candidate set forward, never
collapse an ambiguous feature to one ID).

**Executed:** true

**Output:**
```
feature             best_ref        score  matches   level  candidates  pathway_safe
F1_citrus_like      citrate         1.000        7      2a           1  YES
F2_promiscuous      <none>          0.000        0       5           1  NO -- flag
F3_glutamine_like   glutamine       1.000        6      2a           1  YES
F4_no_library_hit   citrate         0.038        1       5           0  NO -- flag
F5_ms1_only_clean   <none>            n/a      n/a       4           0  NO -- flag
F6_bare_feature     <none>            n/a      n/a       5           0  NO -- flag
```

All 6 features correctly leveled and flagged. Note: the synthetic isomer pair
built for this run (citrate/isocitrate references) did not score as tied
under matchms's ModifiedCosine on this particular query, so the tied-
candidate-set code path was not actually exercised by this run's data (it
was exercised for real via MetFrag in Input 3) — marked as an assertion FAIL
below rather than silently claimed as verified.

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100

**Assertions:**
- [PASS] Every feature's output includes an explicit confidence level, never a bare name.
- [PASS] Ambiguous/tied or unmatched features are flagged as unsafe for pathway enrichment, not silently passed through — F2, F4, F5, F6 all flagged NO.
- [FAIL] Isomer/tied-candidate handling degrades to Level 3 rather than picking an arbitrary single winner — code path exists but was not exercised by this run's actual scores.
- [PASS] MS1-only features are capped at Level 4, never promoted with only isotope/mass evidence — F5 correctly capped at 4.

---

## Reviewer Notes

Check ⚠️/❌ rows first: Input 2 (SIRIUS, environment-blocked, not a Skill
defect) and Input 3 (MetFrag, a real Skill completeness gap — the tool has no
executable guidance despite being one of three named routes). Input 1's
single assertion FAIL is a real, twice-verified documentation bug (wrong
exception type/behavior claimed for the Skill's own stated-compatible
matchms version) that would cost an agent debugging time, not a scope or
safety failure. No safety or scope assertion failed on any input, so the
Research Veto is unaffected; the grade is pulled down from Production Ready
to Limited Release purely by the Execution Average / Layer 2 / assertion-rate
floors in `scoring_rubric.md` §5, not by any veto.

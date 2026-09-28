> **Audit record for `bio-clinical-databases-acmg-classification`**
> - Audited working candidate `719fd2d6eb6f21107a7b590de6d9c3c94930940d718509b7a9c43b55065f0678`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-databases/acmg-classification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-databases-acmg-classification

Generated: 2026-09-28 · Exact candidate: `sha256-manifest-v1:719fd2d6eb6f21107a7b590de6d9c3c94930940d718509b7a9c43b55065f0678`

> Audit method: `skill-auditor@1.0` from the retained `skill-auditor.zip`. This is an initial diagnostic audit, not certification. Candidate bytes were not repaired.

## Result

- Static: **56/100**
- Execution average: **38.6/100**
- Assertions: **12/35 (34.3%)**
- Weighted score: **46/100 — Reject**
- Research veto: **FAIL** — Practice Boundaries, Methodological Ground, and Code Usability
- Ordered findings: `ACMG-001` through `ACMG-009` in [`finding-ledger.md`](finding-ledger.md)

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 20 | 22 | 42 | 1/5 | ❌ |
| 2 | Variant A | 17 | 19 | 36 | 2/5 | ❌ |
| 3 | Edge | 12 | 10 | 22 | 1/5 | ❌ |
| 4 | Variant B | 28 | 40 | 68 | 3/5 | ⚠️ |
| 5 | Stress | 14 | 14 | 28 | 1/5 | ❌ |
| 6 | Scope Boundary | 21 | 23 | 44 | 2/5 | ❌ |
| 7 | Adversarial | 14 | 16 | 30 | 2/5 | ❌ |

## Detailed outputs

### Input 1 — Canonical: default BRCA1-style demonstration

**Prompt.** Classify a rare BRCA1 missense example with REVEL 0.95, SpliceAI 0.05, functional OddsPath 8.0, and absent population frequency. Show retained criteria, points, and classification.

**Observed.** The standalone command exited zero and printed `PP3_Strong`, `BP4_Supporting`, `PS3`, and `PM2_Supporting`, followed by eight points and Likely Pathogenic. This is a runnable output, but OddsPath 8.0 should be PS3 Moderate, not Strong. The demonstration also sums discordant computational evidence and omits disease, transcript, VCEP, mechanism, assay validity, exclusions, and a clinical-use boundary.

**Scores:** Basic 20/40 · Specialized 22/60 · **42/100** · Assertions **1/5**.

- PASS — Standalone command executes and reports criteria, points, and category.
- FAIL — OddsPath 8.0 is not mapped to Brnich Moderate.
- FAIL — Discordant computational evidence is not reconciled.
- FAIL — Required interpretation context and evidence trail are absent.
- FAIL — No non-diagnostic boundary or qualified-review requirement is printed.

### Input 2 — Variant A: PVS1 transcript relevance and escape branches

**Prompt.** Compare relevant- and irrelevant-transcript NMD cases, exact and adjacent 10% removal, and a splice variant escaping NMD.

**Observed.** Relevant-transcript NMD and the exact/over-10% boundaries matched the simplified expectation. The helper ignored `is_alt_isoform_in_disease_tissue=False` and still returned PVS1 Very Strong. A splice donor escaping NMD returned PVS1 Strong without establishing the transcript consequence or excluding rescue. The callable also lacks the LoF gene-disease-mechanism prerequisite.

**Scores:** Basic 17/40 · Specialized 19/60 · **36/100** · Assertions **2/5**.

- PASS — Relevant-transcript NMD control returned PVS1 Very Strong.
- PASS — Exact 10% and greater-than-10% branches were distinct.
- FAIL — Disease-irrelevant transcript still received PVS1.
- FAIL — Splice strength was assigned without consequence/rescue review.
- FAIL — Established LoF mechanism is not enforced by the callable.

### Input 3 — Edge: PS3 and BS3 OddsPath boundaries

**Prompt.** Evaluate exact and adjacent values around 2.1, 4.3, 18.7, 350, 0.48, 0.23, and 0.053.

**Observed.** Only 4 of 14 expectations matched. The Brnich table is `0.48–2.1` indeterminate, `>2.1` PS3 Supporting, `>4.3` Moderate, `>18.7` Strong, and `>350` Very Strong; benign evidence mirrors at `<0.48`, `<0.23`, and `<0.053`. The candidate adds an unsupported 1.2 pathogenic band, shifts evidence upward, misplaces benign mirrors, accepts negative OddsPath, and lacks a Very Strong code.

**Scores:** Basic 12/40 · Specialized 10/60 · **22/100** · Assertions **1/5**.

- PASS — Mapping is deterministic.
- FAIL — Pathogenic intervals do not match Brnich Table 3.
- FAIL — Benign intervals do not match Brnich Table 3.
- FAIL — Reference prose and code disagree about strength names.
- FAIL — Nonpositive OddsPath is accepted as benign evidence.

### Input 4 — Variant B: Tavtigian endpoints and subsumption

**Prompt.** Verify point boundaries, PVS1 subsumption, unknown evidence, and duplicate evidence.

**Observed.** Totals 10, 9, 6, 5, 0, -1, -6, and -7 produced the documented categories. PVS1 correctly subsumed PP3. However, an unknown criterion remained in the result while silently contributing zero, and duplicate PS3 was counted twice to eight points.

**Scores:** Basic 28/40 · Specialized 40/60 · **68/100** · Assertions **3/5**.

- PASS — Positive and VUS endpoints matched.
- PASS — Likely benign and benign endpoints matched.
- PASS — PVS1 subsumed PP3 and PM4.
- FAIL — Unknown evidence was not rejected.
- FAIL — Duplicate evidence was not rejected or de-duplicated.

### Input 5 — Stress: Bergquist AlphaMissense calibration

**Prompt.** Exercise the advertised 2025 calibration from benign through strong pathogenic evidence.

**Observed.** Only 3 of 11 boundary expectations matched. The candidate's 0.2/0.7 supporting-only thresholds are not the advertised calibration: 0.170–0.791 is indeterminate in the published intervals, pathogenic Supporting starts around 0.792, and stronger intervals occur above that. The helper also accepts values below zero and above one.

**Scores:** Basic 14/40 · Specialized 14/60 · **28/100** · Assertions **1/5**.

- PASS — Calls are deterministic.
- FAIL — The calibrated indeterminate band is not preserved.
- FAIL — Pathogenic Supporting begins too early.
- FAIL — Moderate and Strong calibrated outputs are unavailable.
- FAIL — Probability-domain validation is absent.

### Input 6 — Scope Boundary: framework separation and invalid inputs

**Prompt.** Keep germline and somatic vocabularies separate, then challenge evidence and numeric domains.

**Observed.** Normal examples returned separate germline categories and somatic tiers. Unknown/duplicate evidence, negative predictor and prevalence values, negative OddsPath, and an invalid negative OncoKB level were accepted; zero penetrance raised a raw `ZeroDivisionError`. Tier III and Tier IV remain collapsed.

**Scores:** Basic 21/40 · Specialized 23/60 · **44/100** · Assertions **2/5**.

- PASS — Germline and somatic vocabularies are distinct.
- PASS — Five documented normal somatic branches were reachable.
- FAIL — Unknown and duplicate germline criteria were accepted.
- FAIL — Numeric and evidence domains were not validated actionably.
- FAIL — Tier III/IV are collapsed and invalid levels can be promoted.

### Input 7 — Adversarial: current GeneBe and CSpec interfaces

**Prompt.** Execute each shipped public interface and compare it with the documented current public contract.

**Observed.** The shipped GeneBe `variant=HGVS` request returned HTTP 400 requiring `chr`, `pos`, `ref`, and `alt`; the current coordinate control returned HTTP 200. The supplied CSpec `/cspec/ui/svi/all` URL returned HTTP 400 as an invalid GET route; `/cspec/srvc` and a versioned GATM endpoint returned HTTP 200 JSON. No credentials were used.

**Scores:** Basic 14/40 · Specialized 16/60 · **30/100** · Assertions **2/5**.

- FAIL — Shipped GeneBe helper does not satisfy the current request contract.
- PASS — Current GeneBe coordinate control succeeds.
- FAIL — Supplied CSpec route is stale.
- PASS — Current CSpec service and version route are reachable.
- FAIL — Candidate has no actionable interface-drift fallback.

## Research-veto decision

- **Scientific Integrity: PASS.** Retained outputs did not fabricate patient data, studies, or efficacy claims.
- **Practice Boundaries: FAIL.** Definitive category labels are emitted without a required non-diagnostic boundary or qualified clinical review.
- **Methodological Ground: FAIL.** OddsPath, PVS1, and AlphaMissense contain principled method errors capable of changing clinical evidence strength.
- **Code Usability: FAIL.** The advertised GeneBe helper and CSpec route are currently unusable.

The research veto forces `deployable=false` regardless of the numeric score. The fixer must resolve all P0 and P1 findings before an independent re-audit of new exact bytes.

## Evidence map

- Exact structured observations: [`evidence/execution.json`](evidence/execution.json)
- Repeatable audit runner: [`scripts/run_audit.py`](scripts/run_audit.py)
- Test prompts: [`inputs.json`](inputs.json)
- Access classification: [`execution-classifications.json`](execution-classifications.json)
- Source basis: [`scientific-source-notes.md`](scientific-source-notes.md)
- Immutable identity: [`source-identity.json`](source-identity.json)

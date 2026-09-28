> **Audit record for `bio-clinical-biostatistics-adaptive-designs`**
> - Audited working candidate `73116b86978447d18f14945b236561b0685796da68f1a993420352c3c6953546`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-biostatistics/adaptive-designs), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clinical-biostatistics-adaptive-designs

Generated: 2026-09-28 · Exact candidate: `sha256-manifest-v1:73116b86978447d18f14945b236561b0685796da68f1a993420352c3c6953546`

> Audit method: `skill-auditor@1.0` from the retained `skill-auditor.zip`. This is an initial diagnostic audit, not certification. Candidate bytes were not repaired.

## Result

- Static: **71/100**
- Execution average: **50.4/100**
- Assertions: **18/35 (51.4%)**
- Weighted score: **59/100 — Reject**
- Structural veto: **FAIL** — Stability and Determinism
- Research veto: **FAIL** — Methodological Ground and Code Usability
- Ordered findings: `ADAPT-001` through `ADAPT-008` in [`finding-ledger.md`](finding-ledger.md)

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 35 | 51 | 86 | 5/5 | ✅ |
| 2 | Variant A | 13 | 18 | 31 | 2/5 | ❌ |
| 3 | Edge | 27 | 35 | 62 | 3/5 | ❌ |
| 4 | Variant B | 31 | 44 | 75 | 4/5 | ✅ |
| 5 | Stress | 11 | 14 | 25 | 1/5 | ❌ |
| 6 | Scope Boundary | 10 | 11 | 21 | 1/5 | ❌ |
| 7 | Adversarial | 22 | 31 | 53 | 2/5 | ❌ |

## Detailed outputs

### Input 1 — Canonical: OBF survival design

**Prompt.** Design a one-sided 0.025 O'Brien-Fleming survival trial with looks at 33%, 67%, and 100% information, hazard ratio 0.65, 90% power, and explicit dropout and follow-up assumptions.

**Observed.** Candidate sections 1 and 2 completed. The survival design printed approximately 449.4 subjects and 229.4 events. The independent current-package control reproduced three OBF-like boundaries and a one-sided null crossing probability of 0.025000000388. The routed reference appropriately warns that a proportional-hazards calculation must not be reused unchanged for delayed immunotherapy effects.

**Scores:** Basic 35/40 · Specialized 51/60 · **86/100** · Assertions **5/5**.

- PASS — OBF design executes on the exact candidate constants.
- PASS — Survival sample size exposes its principal assumptions and outputs.
- PASS — Independent null crossing probability is near 0.025.
- PASS — Non-proportional-hazards boundary is stated.
- PASS — Package compatibility checks are required.

### Input 2 — Variant A: blinded variance SSR

**Prompt.** Re-estimate sample size after blinded pooled SD changes from 12 to 14 while preserving a one-sided 0.025 final test.

**Observed.** `getDesignGroupSequential(kMax=1, typeOfDesign='asUser')` errors because `userAlphaSpending` is missing. Neither exact sample-size call runs, and the full script stops here. A valid current fixed-design control completed and increased total subjects from 182.78 to 248.08, proving the intended comparison is available. The candidate's unconditional Type-I comment is stronger than its own reference.

**Scores:** Basic 13/40 · Specialized 18/60 · **31/100** · Assertions **2/5**.

- FAIL — Exact section does not reach both sample-size calls.
- PASS — Current-interface control shows the expected nuisance-variance response.
- PASS — Prose distinguishes blinded from unblinded SSR.
- FAIL — Type-I statement is not conditional on the implemented rule and final test.
- FAIL — Raw package error provides no candidate-level recovery action.

### Input 3 — Edge: promising-zone combination design

**Prompt.** Implement a 30%–80% conditional-power promising zone with inverse-normal or CHW weights, `n_max`, and Type-I evidence.

**Observed.** The inverse-normal design and baseline sample size construct successfully. Conditional power, the actual increase rule, a maximum sample size, preservation of original weights, and null calibration are only comments or absent. The skill's written warnings are scientifically useful, but the executable is not a finished Mehta-Pocock/CHW design.

**Scores:** Basic 27/40 · Specialized 35/60 · **62/100** · Assertions **3/5**.

- PASS — Current rpact inverse-normal constructor succeeds.
- PASS — Naive unblinded increases are explicitly prohibited.
- PASS — 30%–80% is labelled an example design choice.
- FAIL — No executable conditional-power adaptation or `n_max` exists.
- FAIL — No original-weight application or Type-I simulation is performed.

### Input 4 — Variant B: BOIN operating characteristics

**Prompt.** Generate a six-dose BOIN table and reproducible operating characteristics for target toxicity 0.30 and maximum n=30.

**Observed.** The exact boundary and 1,000-trial simulation complete, yielding six selection percentages and expected N 26.961 on this run. The independent seeded control also passes. The candidate run has no seed, however, and a code comment inaccurately upgrades FDA's Fit-for-Purpose determination into a claim that FDA prefers BOIN.

**Scores:** Basic 31/40 · Specialized 44/60 · **75/100** · Assertions **4/5**.

- PASS — Boundary call executes.
- PASS — Operating-characteristic simulation executes.
- PASS — Seeded independent control validates the public API.
- PASS — Reference correctly limits the Fit-for-Purpose meaning.
- FAIL — Shipped run lacks a seed and overstates regulatory preference.

### Input 5 — Stress: CRM comparator

**Prompt.** Compare CRM and BOIN across the same six-dose truth using a calibrated skeleton and a recorded seed.

**Observed.** The CRM section supplies six true toxicity probabilities but a five-dose skeleton. `dfcrm` emits a vector-recycling warning; 1,000 simulations run, but the malformed object then fails during printing with a dimension-name error. A valid six-by-six seeded control passes, so this is a candidate-fixture defect rather than a missing package.

**Scores:** Basic 11/40 · Specialized 14/60 · **25/100** · Assertions **1/5**.

- PASS — The reference recognises skeleton calibration risk.
- FAIL — Truth and skeleton dimensions do not match.
- FAIL — Result cannot be printed or compared.
- FAIL — Expensive simulation starts before shape validation.
- FAIL — No seed is recorded.

### Input 6 — Scope Boundary: EXNEX basket borrowing

**Prompt.** Construct an EXNEX basket design with explicit exchangeability weights, an outlier-detachment path, conflict sensitivity, and ESS.

**Observed.** The `gMAP` fit succeeds, then `ess(map_prior)` fails with `Unknown density`; the valid control requires `automixfit(map_prior)` before ESS. More fundamentally, this is one historical MAP fit, not a stratum-level EXNEX model. There are no EX/NEX mixture weights or outlier-detachment mechanics.

**Scores:** Basic 10/40 · Specialized 11/60 · **21/100** · Assertions **1/5**.

- PASS — `gMAP` itself fits the retained data.
- FAIL — The fit is not converted to a density before ESS.
- FAIL — EX/NEX components are absent.
- FAIL — No stratum can detach.
- FAIL — No conflict-sensitivity output is produced.

### Input 7 — Adversarial: run all shipped examples

**Prompt.** Execute every numbered section end to end and treat all of them as finished SAP implementations.

**Observed.** The shipped program runs sections 1 and 2 and exits 1 at section 3. Independent section execution additionally finds errors in sections 6 and 8. Sections 7, 9, and 10 are explicitly comments-only scaffolds, and the main skill labels conceptual sections as scaffolds; that is responsible scoping, but it is not execution evidence. Licensed East/EastHorizon, ADDPLAN, and FACTS surfaces remain restricted and were not bypassed.

**Scores:** Basic 22/40 · Specialized 31/60 · **53/100** · Assertions **2/5**.

- FAIL — Full script does not complete.
- PASS — Conceptual sections are visibly scoped as scaffolds.
- PASS — Restricted commercial tools are not represented as validated.
- FAIL — Full runner loses later evidence after an early error.
- FAIL — Named implementations do not all produce SAP-ready deliverables.

## Veto decisions

### Structural veto

- **Stability: FAIL.** Three of seven executable numbered sections error, and the full program exits at the first defect.
- **Contract: PASS.** Frontmatter, routed resources, and file contracts are structurally present; method defects are recorded separately.
- **Determinism: FAIL.** Critical BOIN, CRM, and Bayesian simulation outputs do not set seeds.
- **Security: PASS.** No credentials, destructive operations, raw-string code execution, or prompt-injection path was found.

### Research veto

- **Scientific Integrity: PASS.** No fabricated trial result, citation identifier, sample size, p-value, or efficacy datum was retained.
- **Practice Boundaries: PASS.** The skill is protocol-design support, not patient diagnosis or prescribing, and it states IDMC and regulatory controls.
- **Methodological Ground: FAIL.** The EXNEX and promising-zone labels exceed what the implementations actually do, and the blinded-SSR Type-I claim is unconditional.
- **Code Usability: FAIL.** Three executable sections fail and the complete script cannot run through.

Both vetoes force `deployable=false` regardless of the diagnostic numeric score. All P0 and P1 findings require fixes followed by delta tooling and an independent re-audit of new exact bytes.

## Evidence map

- Exact structured observations: [`evidence/candidate-section-status.tsv`](evidence/candidate-section-status.tsv), [`evidence/valid-api-smoke.json`](evidence/valid-api-smoke.json)
- Exact failure records: [`evidence/section-03.json`](evidence/section-03.json), [`evidence/section-06.json`](evidence/section-06.json), [`evidence/section-08.json`](evidence/section-08.json)
- Full-run transcript: [`evidence/full-script.log`](evidence/full-script.log)
- Repeatable runners: [`scripts/run_candidate_surfaces.sh`](scripts/run_candidate_surfaces.sh), [`scripts/run_valid_smoke.sh`](scripts/run_valid_smoke.sh)
- Test prompts: [`inputs.json`](inputs.json)
- Surface classification: [`execution-classifications.json`](execution-classifications.json)
- Current regulatory basis: [`scientific-source-notes.md`](scientific-source-notes.md)
- Immutable identity: [`source-identity.json`](source-identity.json)

> **Audit record for `bio-comparative-genomics-ancestral-reconstruction`**
> - Audited working candidate `0865b11e5169758a84e241ca9ab4e59ecf855add0b46c6a38153808788a85871`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/comparative-genomics/ancestral-reconstruction), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Independent re-audit: bio-comparative-genomics-ancestral-reconstruction

Evaluated: 2026-09-28 | evaluator: skill-auditor@1.0 | category: Data Analysis | mode D | complexity Complex

## Decision

**Reject — not candidate-ready.** Diagnostic numeric score is 80/100 (static 81; dynamic average 79.9), but the research code-usability veto fails: current PAML codon `rst` marginal rows are not parsed. Deployable: no. Exact candidate identity: `sha256-manifest-v1:0865b11e5169758a84e241ca9ab4e59ecf855add0b46c6a38153808788a85871` (16 files, 1,535-byte manifest).

The principal defect is independently reproduced, not inherited: PAML 4.10.10 `codeml` completed a codon ASR successfully and wrote a 179,896-byte `rst`; the candidate parser raised `ValueError: PAML rst contains no marginal site rows`. The first marginal row has several codon/state tokens before the colon, unlike the protein row pattern. Protein PAML parsing still passes.

## Veto gates

Skill veto: PASS (stability, contract, determinism, security). Research veto: FAIL, applicable to Data Analysis. Scientific integrity, practice boundaries, and methodological ground pass. Code usability fails for the real codon output incompatibility. The numeric score does not override the veto.

## Scores

| Measure | Result |
|---|---:|
| Static score | 81 / 100 |
| Dynamic execution average | 79.9 / 100 |
| Layer 1 mean | 33.7 / 40 |
| Layer 2 mean | 46.1 / 60 |
| Assertions | 27 / 29 (93.1%) |
| Weighted diagnostic score | 80 / 100 |

Strict candidate-readiness minima are not met: final score <85; dynamic average <85; Layer 2 <48; and a research veto/P0 remains open.

## Dynamic inputs

| # | Surface | Status | Score | Assertions | Result |
|---:|---|---|---:|---:|---|
| 1 | PAML protein and codon ASR | PARTIAL | 40 | 3/4 | Protein passes; codon parser fails on successful current PAML output. |
| 2 | IQ-TREE protein ASR | COMPLETED | 91 | 4/4 | Real run; strict posterior invariants and malformed cases pass. |
| 3 | Discrete trait mapping | COMPLETED | 89 | 4/4 | Explicit seed, 1,000 maps, taxon rejection; corHMM 2.10.5 remains unsupported. |
| 4 | Continuous BM/OU | COMPLETED | 84 | 4/4 | BM 95% intervals; fitted OUwie 3.0.3 exploratory points; uncertainty withheld. |
| 5 | GRASP | COMPLETED | 92 | 4/4 | Current official CLI and packaged wrapper; sequence/tree/JSON validated. |
| 6 | Transformed-model boundary | COMPLETED | 89 | 4/4 | EB/lambda/kappa/delta refuse unsupported ancestral output. |
| 7 | No-data/taxa/outgroup/method prose | COMPLETED | 74 | 4/5 | No-data and mismatch guards pass; categorical corHMM slogan remains. |

## Prior finding adjudication

All nine initial findings were retested against the current bytes. TOOL-ASR-001 is reopened: the protein route passes but the codon route fails on real PAML 4.10.10 output. TOOL-ASR-002 current GRASP CLI and artifacts pass. TOOL-ASR-003 fitted-object OUwie call passes only within its exploratory/no-uncertainty boundary; the documented single-regime `check.identify` diagnostic was reproduced. TOOL-ASR-004 empty/no-data behavior passes. TOOL-ASR-005 strict IQ-TREE posterior parsing passes real and malformed fixtures. TOOL-ASR-006 version/source boundary passes: CRAN corHMM 2.8 is the supported example, GitHub 2.10.5 is explicitly untested. ASR-007 EB/lambda/kappa/delta refusal passes. ASR-008 seeded stochastic mapping and taxon reconciliation pass. ASR-009 is retained as P1 because the usage guide still uses categorical corHMM superiority language inconsistent with its conditional decision matrix.

## Limits and interpretation

No prepared biologically sourced codon `rst` fixture was available. To test format compatibility independently, a public cytochrome-c protein alignment was synonymically encoded into in-frame codons and processed by real PAML 4.10.10. This is a parser-format test, not evidence of biological codon-sequence performance. corHMM GitHub 2.10.5 was not run or represented as supported. OUwie's single-regime `check.identify` failure remains disclosed, and its ancestral points are not treated as an uncertainty-bearing ASR result. The absent-outgroup negative case was rechecked from the initial audit's saved independent fixture evidence; no long-running duplicate IQ-TREE execution was used for it.

## Findings and required next actions

1. **P0 TOOL-ASR-001 — Parse real PAML codon marginal rows.** Add a small real codeml codon-output regression and parse the multi-token codon marginal row grammar, validating node/site coverage and probability invariants.
2. **P1 ASR-009 — Make corHMM claims conditional.** Remove universal “supersedes”/“modern standard” slogans or qualify them to the rate-heterogeneity use case.

Route to a fresh `fix-scientific-skill`. No candidate files were modified. The audit briefly generated one Python bytecode cache in the candidate; that exact cache was removed, and before/after manifests match the expected identity.

Evidence index: [`sources.md`](sources.md), [`source-identity.json`](source-identity.json), [`run-log.md`](run-log.md), [`finding-ledger.md`](finding-ledger.md), `evidence/`, and [`artifact-hashes.tsv`](artifact-hashes.tsv).

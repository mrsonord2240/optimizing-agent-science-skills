> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@4768d6d](https://github.com/mrsonord2240/optimized-scientific-skills/tree/4768d6d40a2ca58b8323aca739c5598b6c5782ff/skills/bio-clinical-databases-acmg-classification) match audited candidate `286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-clinical-databases-acmg-classification`**
> - Audited working candidate `286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clinical-databases/acmg-classification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Independent final re-audit: bio-clinical-databases-acmg-classification

- Candidate: `sha256-manifest-v1:286df2647ef2e418d8302102c7522705f7b5ce4156cfaea6be5c8c36c6d55571`
- Audited: 2026-09-28
- Category / mode: Data Analysis / D
- Verdict: **Production Ready**
- Final score: **96 / 100**
- Static / dynamic: **95 / 97.3**
- Assertions: **28 / 28**
- Skill veto: **PASS**
- Research veto: **PASS**
- Open findings: **none**

## Finding disposition

| Finding | Final state | Independent evidence |
|---|---|---|
| ACMG-001 | closed | Fourteen Brnich boundaries passed; corrected `>4.3` Moderate and `>18.7` Strong prose is present and the obsolete sentence is absent. |
| ACMG-002 | closed | Three contradictory NMD/consequence representations raised `ValueError` before PVS1 assignment; incomplete consequence or rescue review returns `PVS1_REVIEW_REQUIRED`. |
| ACMG-003 | remains closed | Eight independent AlphaMissense endpoint cases preserve the Bergquist intervals and explicit -3/+3 point labels. |
| ACMG-004 | remains closed | Current GeneBe coordinate endpoint returned one structured public example record. |
| ACMG-005 | remains closed | Current CSpec versioned-gene endpoint returned six GATM version records. |
| ACMG-006 | closed | PP5/BP6, duplicate criteria, same-family strengths/aliases, PP3/BP4 conflict, invalid predictor domains, and invalid semantic dates all stop explicitly; 18 exact REVEL/BayesDel cases passed. |
| ACMG-007 | remains closed | Standalone output uses one computational predictor, PS3 Moderate, unresolved context, uncertainty, and a guarded illustrative category. |
| ACMG-008 | remains closed | Instructions and all observed result objects require qualified review and prohibit diagnosis, treatment, or stand-alone clinical reporting. |
| ACMG-009 | remains closed | Tier I-A, I-B, II-C, II-D, III, and IV are distinct; Tier III and IV carry different rationales. |

## Execution summary

| Input | Surface | Score | Assertions | Result |
|---:|---|---:|---:|---|
| 1 | 24 shipped tests, compile, standalone demo | 98 | 4/4 | PASS |
| 2 | PVS1 prerequisites, splice review, contradictions | 97 | 4/4 | PASS |
| 3 | Brnich OddsPath exact boundaries and prose | 98 | 4/4 | PASS |
| 4 | Evidence-family integrity and predictor endpoints | 98 | 4/4 | PASS |
| 5 | Somatic tiers, real ISO dates, guarded results | 97 | 4/4 | PASS |
| 6 | Live public GeneBe and CSpec interfaces | 96 | 4/4 | PASS |
| 7 | Malformed, conflicting, and out-of-scope inputs | 97 | 4/4 | PASS |

The averaged Layer 1 score is 39.3/40 and the averaged Layer 2 score is 58.0/60. Both Production Ready floors and the 100% assertion floor pass.

## Primary observations

- `evidence/unit-tests.log`: all 24 shipped tests passed.
- `evidence/execution.json`: 25 invalid probes, 26 predictor endpoints, nine PVS1 states, three contradiction stops, 14 OddsPath cases, two valid and four invalid ISO-date cases, six somatic tiers, and guarded germline output passed.
- `evidence/live-interface-smoke.log`: GeneBe returned one record and CSpec returned six version records.
- `evidence/standalone-demo.log`: the demonstration remains explicitly non-diagnostic and retains unresolved disease, transcript, VCEP, and assay-validity context.
- `evidence/preflight.log`: compile passed and the candidate tree retained zero cache artifacts.

## Access and scope

InterVar with ANNOVAR data remains documented-only and blocked by registration plus large annotation data. AutoPVS1 remains an unpinned documented external implementation. VarSome, Franklin/Genoox, and ClinGen VCI remain restricted/manual. Other named evidence sources have no shipped wrapper. These are accurately described boundaries, not runnable-surface failures.

No patient record, private variant, credential, proprietary database, or protected-health information was used. No candidate repair, product commit, push, pull request, release, remote submission, or audit publication was performed in this phase.

## Final decision

Both veto gates pass, all Production Ready floors pass, and no P0, P1, or P2 finding remains. The exact candidate is ready for the relay's candidate-ready state and later batch assembly; this audit is evidence, not authorization for clinical deployment or autonomous diagnosis.

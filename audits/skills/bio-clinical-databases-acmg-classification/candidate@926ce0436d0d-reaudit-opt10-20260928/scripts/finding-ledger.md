# Independent re-audit finding ledger

Candidate: `sha256-manifest-v1:926ce0436d0d9fd1fb73a5f2b83728adfb622cf6f8ec41c8c00ad8d8300e8c07`

| ID | Initial severity | Re-audit state | Re-audit severity | Evidence | Required disposition |
|---|---|---|---|---|---|
| ACMG-001 | P0 | reopened | P2 | `evidence/execution.json#static_checks` | Correct the residual `>4.3 for Strong` sentence; code and table otherwise pass. |
| ACMG-002 | P0 | reopened | P1 | `evidence/execution.json#workflows.pvs1.conflict` | Reject contradictory NMD fields before PVS1 strength assignment. |
| ACMG-003 | P0 | fixed | none | `evidence/execution.json#workflows.alphamissense` | Accepted: 17/17 bands, +/-3 point labels, and invalid domains pass. |
| ACMG-004 | P1 | fixed | none | `evidence/execution.json#workflows.interfaces.live.genebe` | Accepted: current coordinate contract returned one public record. |
| ACMG-005 | P1 | fixed | none | `evidence/execution.json#workflows.interfaces.live.cspec` | Accepted: current versioned-gene route returned six GATM versions. |
| ACMG-006 | P1 | reopened | P0 | `evidence/execution.json#workflows.tavtigian`, `#workflows.other_predictor_boundaries`, `#workflows.somatic.invalid_date` | Remove PP5/BP6; reject evidence-family duplicates/aliases and opposing codes; fix exact inclusive predictor endpoints; parse real dates. |
| ACMG-007 | P1 | fixed | none | `evidence/standalone-demo.log` | Accepted: one predictor, PS3 Moderate, unresolved context, uncertainty, and guard printed. |
| ACMG-008 | P1 | fixed | none | `SKILL.md`, `evidence/standalone-demo.log`, guarded result observations | Accepted: non-diagnostic boundary and qualified review are enforced in documentation/results. |
| ACMG-009 | P2 | fixed | none | `evidence/execution.json#workflows.somatic.cases` | Accepted: I-A, I-B, II-C, II-D, III, and IV are distinct and guarded. |

No new standalone ID is opened: the newly reproduced validation failures are additional manifestations of the still-open ACMG-006 evidence/domain-validation defect. Candidate readiness is rejected because ACMG-006 fires the methodological veto and the readiness floors are not met.

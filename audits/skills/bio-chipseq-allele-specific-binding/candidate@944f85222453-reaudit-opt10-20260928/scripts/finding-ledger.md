# Final re-audit finding ledger

Exact candidate:
`944f852224538df92c581ab4a42889202ab10639f54974130f841782f5c90ead`.

| Order | ID | Severity | Final state | Evidence | Disposition |
|---:|---|---|---|---|---|
| 1 | CBA-001 | P0 | fixed | R helper suite; RAF/gDNA preflights; report-list contract | Official five-column sample sheet, group het table, named report selection, required columns, and empty report are enforced. |
| 2 | CBA-002 | P0 | fixed | `evidence/run-artifacts/raf-preflight/`; `gdna-preflight/`; AF negative probe | Measured RAF and matching gDNA are distinct, recorded correction sources; ordinary AF fails closed. |
| 3 | CBA-003 | P0 | fixed | `evidence/wasp-live.tsv`; `wasp-hdf5-live.tsv` | Both remap mates use the pinned names; final pairing and count invariants pass. |
| 4 | CBA-004 | P1 | fixed | `evidence/rasqual-binary-contract.tsv`; `rasqual-cohort.tsv` | Two public features ran once, converged, and received cohort-family p/q values. |
| 5 | CBA-005 | P1 | fixed | `evidence/alleleseq-dryrun-boundary.tsv` | The incomplete local sketch is gone; the route is explicitly external-only with exact missing prerequisites. |
| 6 | CBA-006 | P1 | fixed | ten negative probes; interval controls; helper suite; output refusal | Schema, build, sample, file, exclusion, empty/report, and rerun boundaries are structured and fail closed. |
| 7 | CBA-007 | P2 | reopened as CBA-009/010 | `evidence/source-binding-check.tsv` | WASP and RASQUAL bindings are exact; BaalChIP release and AlleleSeq checkout bindings remain inconsistent. |
| 8 | CBA-008 | P1 | fixed | `evidence/run-artifacts/atomic-cleanup.stderr.txt`; sentinel | Missing-package failure publishes no final directory, leaves no owned partial, and preserves unrelated state. |
| 9 | CBA-009 | P1 | open | BaalChIP 1.38.0 `DESCRIPTION`; prepared `BiocVersion` | Correct the Bioconductor 3.22/3.23 compatibility binding and rerun the full-model terminal surfaces. |
| 10 | CBA-010 | P2 | open | candidate source table; exact checkout remote | Link the exact AlleleSeq2 implementation repository used for commit `cfe8acf`. |

The numeric rubric grade is Production Ready, but this workflow does **not**
mark the candidate candidate-ready while `CBA-009` remains open. No audit-local
repair was attempted because release/environment selection changes a dependency
contract and requires a fresh tooling delta.


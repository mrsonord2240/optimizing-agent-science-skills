# Fresh final re-audit finding ledger

Exact candidate:
`03415aabaa66de0ef1b747e3fc664dae6d2868e42bf52a2c104d990db5e6057f`.

| Order | ID | Severity | Final state | Evidence | Disposition |
|---:|---|---|---|---|---|
| 1 | CBA-001 | P0 | closed | R helper suite; RAF/gDNA preflights; named report contract | Official sample, het, report and structured-empty contracts are enforced. |
| 2 | CBA-002 | P0 | closed | RAF/gDNA preflights; AF negative probe | Measured RAF and matching gDNA remain distinct and provenance-recorded; ordinary AF fails closed. |
| 3 | CBA-003 | P0 | closed | `evidence/wasp-live.tsv`; `wasp-hdf5-live.tsv` | Exact paired filenames, integrity, count invariants and provider HDF5 shapes pass live. |
| 4 | CBA-004 | P1 | closed | `evidence/rasqual-binary-contract.tsv`; `rasqual-cohort.tsv` | Two public features run once, converge and receive cohort-family p/q values. |
| 5 | CBA-005 | P1 | closed | `evidence/alleleseq-boundary.tsv` | The complete legacy stack is explicitly external-only and unavailable execution is uncredited. |
| 6 | CBA-006 | P1 | closed | ten negative probes; interval controls; helper suite | Schema, build, sample, file, exclusion, report and rerun boundaries fail closed. |
| 7 | CBA-007 | P2 | closed | exact source bindings across all four routes | Method and implementation claims now carry exact, coherent bindings. |
| 8 | CBA-008 | P1 | closed | `run-artifacts/atomic-cleanup.stderr.txt`; sentinel | Package-load failure publishes no final, leaves no owned partial and preserves unrelated state. |
| 9 | CBA-009 | P1 | closed | official 3.22 index; BaalChIP 1.36.0 DESCRIPTION/source; version gates | Candidate, runtime and official source coherently bind BaalChIP 1.36.0 to Bioconductor 3.22 and R 4.5. |
| 10 | CBA-010 | P2 | closed | `evidence/alleleseq-binding.tsv` | Tested implementation is exactly `trgaleev/AlleleSeq2@cfe8acf`; the canonical paper is separate. |

No open finding remains. The full BaalChIP model and actual all-excluded/no-call
publication are `RESOURCE_INFEASIBLE_BOUNDED_NOT_CREDITED`; the AlleleSeq full
toolchain is `UNAVAILABLE_EXTERNAL_ONLY_NOT_CREDITED`. These classifications
are retained as access boundaries, not converted into inferred passes.

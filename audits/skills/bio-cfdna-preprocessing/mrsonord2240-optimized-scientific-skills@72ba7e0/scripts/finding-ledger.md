# Final finding ledger — bio-cfdna-preprocessing

Exact candidate: `sha256-manifest-v1:148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1`

| Order | ID | Priority | Final state | Independent disposition evidence |
|---:|---|:---:|---|---|
| 1 | CFD-001 | P0 | closed | Every one of 32 extracted and first-zipped records in all fresh workflows has RX, ZA, and ZB; layout validation rejects missing, duplicate, and malformed tags. |
| 2 | CFD-002 | P0 | closed | Captured live argv proves queryname uBAM → `samtools fastq -T RX,ZA,ZB` → `bwa mem -C -Y -p` → `ZipperBams`; 32 mapped/tagged records enter grouping. |
| 3 | CFD-003 | P0 | closed | Every filter input/output is queryname-sorted; every final BAM is coordinate-sorted, indexed, nonempty, and passes quickcheck. |
| 4 | CFD-004 | P0 | closed | AST finds no `shell=True`, `eval`, or `exec`; a full space/semicolon/dollar/bracket workflow completes and creates no side-effect path; thread inputs are typed and bounded. |
| 5 | CFD-005 | P1 | closed | The flag fixture accepts 1/5 and counts one each secondary, supplementary, duplicate, and QC-fail; invalid bounds fail specifically; empty input is stable. |
| 6 | CFD-006 | P1 | closed | Guidance is conditional on recovery, molecular depth, background, targets, pre-analytics, caller, and validated LoD; all six DOI identifiers resolve to the named primary publications. |

## Gates and readiness

- Skill veto: PASS — 6/6 shipped tests with no skips; ten consecutive complete calls; stable schemas; deterministic outputs; argv-only process execution.
- Research veto: PASS — no fabrication or practice-boundary breach; topology and QC are methodologically grounded; all accessible code executes.
- New findings: none.
- Remaining finding IDs: none.
- Minor-repair budget: unused; candidate bytes were not changed.
- Readiness: candidate-ready at this exact identity.

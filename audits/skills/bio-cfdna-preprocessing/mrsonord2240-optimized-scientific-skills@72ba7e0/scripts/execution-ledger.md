# Independent re-audit execution ledger — bio-cfdna-preprocessing

- Phase: `reaudit-scientific-skill`
- Auditor independence: fresh worker; did not perform normalization, tooling, initial audit, fix, or tooling delta.
- Candidate: `sha256-manifest-v1:148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1`
- Environment: WSL `science` / user `sci`, `WSL_INTEROP` and `WSLENV` unset; Python 3.12.14, NumPy 1.26.4, pysam 0.22.1, fgbio 4.1.1, bwa 0.7.19-r1273, samtools 1.24.
- Candidate identity before and after: exact match; no candidate cache or output artifact created.

## Executions

1. Direct script execution exited 0 and printed the three documented API surfaces.
2. Fresh simplex workflow: 32 tagged input records → 32 grouped records → 4 filtered final records; coordinate sort, index, and quickcheck pass.
3. Fresh duplex workflow: 32 tagged input records → 32 paired-grouped records → 2 true-duplex final records; coordinate sort, index, and quickcheck pass.
4. Second fresh duplex workflow: same structural result, providing an independent repeat.
5. Fresh metacharacter simplex workflow: input, reference, work, and output paths contain spaces, semicolon, dollar sign, and brackets; 4-record final BAM, index, and quickcheck pass; no shell side effect.
6. Public BAM fragment QC: two identical complete results plus a fresh `max_size=150` case.
7. Flag fixture, invalid bounds, and empty BAM: all documented policies pass.
8. Shipped live suite: 6 tests, 0 skips, return code 0, 427.209 seconds; includes ten consecutive complete workflow calls.
9. Static executable safety: zero `shell=True`, `eval`, or `exec` calls.
10. Static scientific guidance: every required conditional concept present and six DOI identifiers verified against publisher/PubMed/PMC records.

## Durable evidence

- `evidence/reaudit-results.json` — independent workflow, stage, argv, QC, static, and identity evidence.
- `evidence/shipped-suite-summary.json` — separate candidate-suite command and outcome.
- `evidence/shipped-suite.stdout.txt` and `evidence/shipped-suite.stderr.txt` — complete captured test output.
- `scripts/reaudit_cases.py` and `scripts/run_shipped_suite.py` — saved executable evidence generators.
- `work/` — persistent BAM stages for inspection; not publication-required unless the orchestrator elects to retain large binary evidence.

## Warnings and blockers

- fgbio under Java 25 emits a warning that native-access restrictions will tighten in a future release. Current calls all complete; this is environment future-maintenance information, not a candidate failure.
- Restricted, authenticated, gated, paid, GPU, or resource-infeasible surfaces: none.
- Failed or blocked accessible surfaces: none.

# Finding ledger — bio-batch-processing independent re-audit

Exact fixed candidate identity:
`f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd`.

| Order | ID | Prior priority | Final state | Independent evidence |
|---:|---|---|---|---|
| 1 | BATCH-001 | P0 | closed | Traversal/reserved prefixes and manifest escape rejected; sibling and existing target preserved; case collision accounted in a partial manifest. |
| 2 | BATCH-002 | P1 | closed | 2,048 prefixes completed with `max_open_files=8` under `RLIMIT_NOFILE=32`; 4 descriptors before and after; all totals 2,048; evicted group preserved. |
| 3 | BATCH-003 | P1 | closed | No-match summary returned `[]` and exactly six header columns; an empty file returned explicit zero metrics. |
| 4 | BATCH-004 | P1 | closed | Boolean, zero, negative, float, and string sizes failed before a missing input was opened or output created; valid fresh split parsed as 2/2/1. |
| 5 | BATCH-005 | P1 | closed | Two-worker fork, spawn, and spawn rerun returned identical stable rows, six records, and 15 bp. |
| 6 | BATCH-006 | P1 | closed | Opposite creation orders resolved to `a.fasta,z/a.fasta,z/B.fasta`; summary and merged bytes matched exactly. |
| 7 | BATCH-007 | P2 | closed | pyfastx function twice plus CLI indexed 94 gzip FASTA records, checked lengths 740/592/740, and reused the same `.fxi` inode/hash. |
| 8 | BATCH-008 | P2 | open, non-blocking | Recursive summaries and `process_file` rows emit `Path.name`; distinct nested files with the same basename are distinguishable only by input order/context. Prefer a caller-root-relative identifier in a future polish pass. |

No P0 or P1 finding remains. `BATCH-008` does not change checked totals,
deterministic order, file bytes, or scientific interpretation, and does not
block the current Production Ready/candidate-ready gate.

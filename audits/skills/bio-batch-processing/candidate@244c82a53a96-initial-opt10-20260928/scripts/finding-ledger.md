# Finding ledger — bio-batch-processing initial audit

Exact candidate identity: `244c82a53a96dce4586308b71ed678bae2bd3bed685a1db7aa44c6459b0c8990`.

| Order | ID | Priority | Classification | Durable evidence | Required disposition |
|---:|---|---|---|---|---|
| 1 | BATCH-001 | P0 | executed safety failure | `evidence/execution-summary.json`, case 4 | Sanitize and contain ID-derived paths; prevent overwrite; regress traversal. |
| 2 | BATCH-002 | P1 | executed resource failure | `evidence/execution-summary.json`, case 4 | Bound open handles and guarantee cleanup/partial-run reporting. |
| 3 | BATCH-003 | P1 | executed edge failure | `evidence/execution-summary.json`, case 3 | Define an explicit CSV schema and empty-input behavior. |
| 4 | BATCH-004 | P1 | executed validation failure | `evidence/execution-summary.json`, case 3 | Reject non-positive or non-integer chunk sizes before any output. |
| 5 | BATCH-005 | P1 | executed platform failure | `inputs/multiprocessing_recipe.py`, `evidence/execution-summary.json`, case 5 | Guard Pool startup and validate fork plus spawn. |
| 6 | BATCH-006 | P1 | executed reproducibility failure | `evidence/glob-order-probe.json` | Sort every discovered path list with a documented stable key. |
| 7 | BATCH-007 | P2 | static plus auditor-authored execution | `evidence/execution-summary.json`, case 2 | Ship and route a checked pyfastx example. |

Minor audit-local repair budget was not used. Every finding changes a public
interface, safety boundary, runtime method, behavioral contract, or coverage
claim and belongs to `fix-scientific-skill`.

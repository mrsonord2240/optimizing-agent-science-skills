# Ordered finding ledger

Audit identity: candidate commit `0bc0b31fc52742dbec1034f698103434cc9460c3`,
subtree `b5a701c41d3afe697766a02a11b2954e12ff9d42`.

| Order | ID | Priority | State | Evidence | Required disposition |
|---:|---|---|---|---|---|
| 1 | ADV-001 | P0 | open | Input 4; `scripts/panel_integrated_lod.py`; `evidence/execution-summary.json` | Relabel the current calculation as a sampling-only theoretical floor or replace it with a validated assay-detection model; state assumptions at output time. This finding causes the Methodological Ground research-veto failure. |
| 2 | ADV-002 | P1 | open | Input 3; all public calculator modules | Add finite/range/shape/replicate/k-of-N validation and stable actionable errors; rerun every invalid probe. |
| 3 | ADV-003 | P1 | open | Input 2; direct `scripts/lod95_probit.py` stderr | Reject or explicitly fail unidentified/separated fits, use replicated bracketing data, and return fit diagnostics plus confidence intervals. |
| 4 | ADV-004 | P1 | open | Input 5; `examples/detection_limits.py::simulate_dilution_series` | Remove `true_lod_vaf` or make it materially control a documented simulation model; add a sensitivity regression. |
| 5 | ADV-005 | P2 | open | Static source check; Inputs 1 and 2; `scientific-source-notes.md` | Correct the GE/ng convention explanation and distinguish HCC1395/HCC1395BL from Sample A-derived SEQC2 materials with stable identifiers. |

No audit-local repair was attempted. Every finding changes a scientific claim,
method, interface, validation boundary, or provenance judgment and therefore
falls outside the minor-repair budget.

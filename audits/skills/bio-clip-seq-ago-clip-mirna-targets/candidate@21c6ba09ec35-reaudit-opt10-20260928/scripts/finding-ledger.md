# Ordered finding ledger

## AGO-004 — P0 — Two-run agreement is not workflow-level deterministic

Two fresh complete wrapper batches used the same pinned Hyb commit, official
input, named database, single-thread controls, and two replicates. Both batches
retained 94 and excluded 17 assignments, but their accepted outputs were not
the same: seven read ids were accepted only in each batch and four shared read
ids had different normalized assignments. The candidate's statement that the
two-run parser retains "stable" assignments is therefore not supported at the
workflow level. This fails the result-determinism and methodological-ground
vetoes even though each individual pair reconciles and replays correctly.

## AGO-005 — P1 — Targeted-Yeo UMI length remains internally inconsistent

The candidate says the pinned targeted-miR route takes a nine-nucleotide UMI
from read 2. At source commit `75fe74e`, `extract_r2_umi.cwl` repeats that in
prose, but it does not bind `--umi_length`; `targeted_miR_umi.py` defaults to
10, and a live bounded invocation appended ten R2 bases. The skill must not
state an exact operational length until it requires a protocol-declared value
and passes that value explicitly through a pinned route.

## Closed initial findings

- AGO-001: closed — current named-database/goal/id/output Hyb contract executed.
- AGO-002: closed — orientation-aware 16-column parser passed real and synthetic controls.
- AGO-003: closed — quoting, validation, status propagation, staged publication, and replacement safety passed.
- AGO-006: closed — current tool identities and access states are separated.
- AGO-007: closed — counts, absent overlaps, and example thresholds have bounded interpretations.
- AGO-008: closed — structured outputs, manifests, reason codes, safe reruns, and focused tests are shipped.

# Second independent re-audit finding ledger

Audit identity: branch `optimize/ten-20260928-lane2-atac-asa`, starting HEAD
`0bc0b31fc52742dbec1034f698103434cc9460c3`, exact candidate content SHA-256
`275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2`.

| Order | ID | Priority | Final state | Independent disposition |
|---:|---|---|---|---|
| 1 | ASA-001 | P0 | closed | Public run produced a coordinate-sorted, one-SM, indexed 268,176-read BAM and 953 non-empty GATK rows; empty output remains refused. |
| 2 | ASA-002 | P0 | closed | Public output retained only NA12878; target-homozygous/other-heterozygous and BAM/VCF mismatch fixtures both failed before analysis. |
| 3 | ASA-003 | P0 | closed | Opposite REF encodings produced phase-oriented counts 180:20, and a separate phase block remained separate. |
| 4 | ASA-004 | P1 | closed | Empty/no-overlap cases emitted the exact ten-column schema; malformed ASE and duplicate intervals failed actionably without result files. |
| 5 | ASA-005 | P1 | closed | Public two-feature RASQUAL used matrix rows 1 and 2, emitted 166 finite rows, and matched independent BH over the complete family. |
| 6 | ASA-006 | P1 | closed | MatrixEQTL and QuASAR remain explicit external-only routes with no executable candidate claim. |
| 7 | ASA-007 | P1 | closed | Phase, multiplicity, power, validation, and concordance claims remain conditioned and within the tested evidence. |
| 8 | ASA-008 | P2 | closed | Canonical provider blobs resolve, checkout hashes are caveated, spaced paths pass, staged failures clean up, and existing outputs are refused. |
| 9 | ASA-009 | P0 | closed | The exact disjoint duplicate-label fixture now yields two one-SNP underpowered rows; intersection coordinates survive, coordinate plus phase set defines groups, and BED labels are display-only. |

No new finding was opened. No runnable surface is blocked or restricted.

Readiness metrics: static 96/100, execution 95.4/100, Layer 1 average
38.4/40, Layer 2 average 57.0/60, assertions 25/25, both veto gates PASS,
final 96/100 Production Ready. Exact candidate is `candidate-ready` pending the
orchestrator's product commit and intake gate.

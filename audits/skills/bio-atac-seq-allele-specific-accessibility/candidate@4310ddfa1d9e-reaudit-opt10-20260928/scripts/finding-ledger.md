# Independent re-audit finding ledger

Audit identity: branch `optimize/ten-20260928-lane2-atac-asa`, starting HEAD
`0bc0b31fc52742dbec1034f698103434cc9460c3`, exact candidate content SHA-256
`4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103`.

| Order | ID | Priority | State | Independent disposition |
|---:|---|---|---|---|
| 1 | ASA-001 | P0 | closed | Real public run produced a coordinate-sorted, one-SM, indexed 268,176-read BAM and 953 non-empty GATK rows; the pipeline refuses empty GATK output. |
| 2 | ASA-002 | P0 | closed | Real output retained only NA12878; a target-homozygous/other-heterozygous fixture yielded zero target records, and a BAM/VCF mismatch stopped with exit 65. |
| 3 | ASA-003 | P0 | closed | Opposite REF encodings produced phase-oriented haplotype counts 180:20, and a separate phase block remained separate. |
| 4 | ASA-004 | P1 | closed | Empty and no-overlap cases emitted the exact ten-column schema; malformed ASE failed actionably; significant and non-significant groups retained counts and statuses. |
| 5 | ASA-005 | P1 | closed | Public two-feature RASQUAL used matrix rows 1 and 2, emitted 166 finite rows, and matched independent BH adjustment over the complete family. |
| 6 | ASA-006 | P1 | closed | MatrixEQTL and QuASAR are explicitly external-only routes with no executable candidate claim. |
| 7 | ASA-007 | P1 | closed | Phase is scoped to pooling, cohort inference requires declared-family FDR/permutation, and unsupported fixed power/concordance/raw-p claims are absent. |
| 8 | ASA-008 | P2 | closed | Canonical Git blobs resolve, checkout hashes are caveated, full paths with spaces pass, and existing outputs are refused. |
| 9 | ASA-009 | P0 | open | Two disjoint BED4 intervals named `dup` were collapsed into one two-SNP significant group because the helper groups on display label plus phase set rather than genomic coordinates. |

## Required disposition for ASA-009

Carry chromosome, start, and end through the intersection and group by genomic
peak identity plus phase set; preserve BED4 name as display metadata only, or
explicitly reject duplicates. Add a regression requiring two disjoint one-SNP
intervals with the same label to remain two underpowered rows. Re-run the
aggregate surface and the full public workflow, then assign a fresh independent
re-auditor.

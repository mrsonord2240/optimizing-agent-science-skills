# Ordered finding ledger

## AGO-001 — P0 — Current Hyb contract is incompatible with the wrapper

The wrapper passes a concatenated FASTA as `db`, supplies no analysis goal or
output id, and then assumes `${OUT_PREFIX}.hyb`. Current pinned Hyb requires an
installed database name and generated
`<id>_comp_<db>_hybrids_ua.hyb`. The exact wrapper against real Hyb exits zero
after the database error and emits empty derived tables.

## AGO-002 — P0 — Current 16-column Hyb rows are parsed as the wrong fields

The wrapper treats field 3 as miRNA id and field 5 as target id. Current Hyb
places the two RNA ids in fields 4 and 10, while field 3 is folding energy and
field 5 is a coordinate. RNA order can be either orientation. A valid current
row is dropped, so expression filtering and target aggregation are invalid.

## AGO-003 — P0 — Shell input and failure boundaries fail open

The script has no strict shell mode or argument/schema validation and leaves
paths and prefixes unquoted. Spaces fail while returning zero, a literal `*`
expands to a sibling FASTA, and a Hyb exit of 42 becomes wrapper exit zero with
empty partial outputs.

## AGO-004 — P0 — Identical pinned Hyb runs change pair assignments

Two clean executions retained 111 valid rows and the same 111 read ids but
selected 18 different RNA-pair assignments in each run. The candidate neither
pins a deterministic control nor documents a tie/consensus policy, triggering
the result-determinism veto for a direct-interaction list.

## AGO-005 — P1 — Preprocessing and TargetScan examples lack an executable coordinate contract

The one-sided ten-base UMI example leaves the first ten R2 bases intact; the
current Yeo chimeric-eCLIP surface uses library-specific R2 UMI handling. The
unstranded `bedtools intersect` accepts an opposite-strand overlap, while the
official TargetScan 8 data are transcript/UTR-relative rather than genomic
BED. Prose cautions do not supply a validated transformation and strand-safe
command.

## AGO-006 — P1 — Advertised tool names and interfaces are not current

No `pyHyb 0.4+` distribution exists; relevant `hybkit` is a distinct 0.3.6
package. Public Hyb has no semantic release tag and identifies by Git commit.
Yeo chim-eCLIP is a separate CWL workflow, and HEAP is an experimental method
with public data and CLIPanalyze rather than a standalone `HEAP pipeline` CLI.

## AGO-007 — P1 — Evidence interpretation overstates unsupported negatives and counts

Read counts are influenced by expression, ligation, amplification, recovery,
and mapping and are not a binding-affinity measurement. Absence of an AGO peak
in one assay/context does not establish a TargetScan site is a biological false
positive or non-functional. The 1–5%, 200M+, >100 TPM, and enrichment heuristics
need claim-level sources and context rather than operational defaults.

## AGO-008 — P2 — Reporting and regression surfaces are incomplete

The wrapper omits a structured site/target report, strand and alignment-quality
fields, stage manifests, version capture, overwrite policy, and focused
regressions. The selected-miRNA `grep` example can match substrings instead of
the schema field.


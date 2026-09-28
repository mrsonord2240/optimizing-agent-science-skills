# Ordered finding ledger — bio-cfdna-preprocessing

Exact candidate: `sha256-manifest-v1:9852987be2107ca7d54ae6e211f1fbd25ed2710910b1cd43c80c45dc8444059b`

| Order | ID | Priority | Finding | Evidence | Required disposition |
|---:|---|:---:|---|---|---|
| 1 | CFD-001 | P0 | Two UMI segments are passed with no molecular-index tags, so every advertised wrapper call fails in `ExtractUmisFromBam`. | `evidence/candidate-simplex.stderr.txt`, `candidate-duplex.stderr.txt`, `stability-summary.json` | Add and validate the per-segment tag mapping, preserve combined `RX` where intended, and test simplex and reciprocal-duplex extraction. |
| 2 | CFD-002 | P0 | The first alignment sends a binary BAM pathname directly to `bwa mem`; BWA exits zero but produces unparsable SAM. | `evidence/bwa-direct-bam.stderr.txt`, `bwa-direct-bam-parse.stderr.txt` | Convert/query-group the uBAM to paired FASTQ, align, then zipper metadata and UMI tags back; assert records, pairing, and tags. |
| 3 | CFD-003 | P0 | `FilterConsensusReads` receives coordinate-sorted input although it requires queryname-sorted or query-grouped templates. | `evidence/filter-coordinate.stderr.txt`, `filter-queryname-control.stderr.txt` | Query-sort/group before filtering, then coordinate-sort and index the filtered output. |
| 4 | CFD-004 | P0 | Two input-derived pipelines use unquoted `shell=True`; paths with spaces fail and metacharacters can be interpreted by the shell. | `evidence/execution-summary.json`, `unquoted-space-realign.stderr.txt`, rubric structural precheck | Replace shell strings with argv-connected processes, validate thread count, and add space/metacharacter path regressions. |
| 5 | CFD-005 | P1 | Fragment QC includes supplementary, duplicate, and QC-fail reads while claiming a primary proper-pair population; nonpositive `max_size` is silently accepted. | `evidence/independent-qc.json`, `execution-summary.json` | Define/enforce the flag policy, reject invalid bounds, report filter counts, and test all major flags plus empty input. |
| 6 | CFD-006 | P1 | Duplex and library-chemistry choices are framed as universal rules rather than assay-conditional choices supported by validation evidence. | `scientific-source-notes.md`; static-only | Condition recommendations on error model, recovery, molecule count, targets, background suppression, and validated LoD; add stable identifiers. |

## Gate mapping

- Skill veto: **FAIL** — stability (`CFD-001`, 10/10 calls fail) and security (`CFD-004`).
- Research veto: **FAIL** — Methodological Ground (`CFD-002`, `CFD-003`, `CFD-006`) and Code Usability (`CFD-001` through `CFD-003`).
- Minor-repair budget: not used. Every item changes scientific method, an executable interface/order, input validation, or a safety boundary.

## Deferred but not blocked

- Whole-genome scale, production cohort throughput, wet-lab recovery, empirical error-floor validation, and clinical LoD are outside this bounded diagnostic audit.
- No accessible primary runnable surface is blocked by credentials, gated data, unavailable software, GPU, or resource limits.

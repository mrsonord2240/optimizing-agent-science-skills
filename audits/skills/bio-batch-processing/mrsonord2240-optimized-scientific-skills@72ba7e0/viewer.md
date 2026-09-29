> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@72ba7e0](https://github.com/mrsonord2240/optimized-scientific-skills/tree/72ba7e0949bdeb61322a64248c429b378d42f97e/skills/bio-batch-processing) match audited candidate `f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-batch-processing`**
> - Audited working candidate `f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/sequence-io/batch-processing), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-batch-processing

Generated: 2026-09-28

Exact candidate: `f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd`

Independent phase: the evaluator performed neither the initial audit, candidate
fix, nor tooling-delta pass. Candidate bytes were read-only. Full checked output
is in [`evidence/reaudit-results.json`](evidence/reaudit-results.json); commands
are in [`evidence/commands.log`](evidence/commands.log).

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 4 | Variant B | 40 | 59 | 99 | 5/5 PASS | ✅ |
| 5 | Stress | 38 | 57 | 95 | 5/5 PASS | ✅ |

**Execution Average: 97.0 / 100**  
**Layer 1 Average: 39.0 / 40**  
**Layer 2 Average: 58.0 / 60**  
**Assertion Pass Rate: 25/25 (100%)**

## Veto gates

- Structural veto: PASS — stability, contract, determinism, and security all pass.
- Research veto: PASS — scientific integrity, practice boundaries,
  methodological ground, and code usability all pass.
- Accessible surfaces: all executed. Restricted, unavailable, licensed,
  authenticated, or resource-infeasible surfaces: none.

## Detailed outputs

### Input 1 — Canonical

**Prompt:** Process two bounded FASTA files in stable order: stream counts,
merge all records, split two fresh record sets into bounded chunks, build and
reopen a persistent multi-file index, convert a public GenBank fixture to FASTA
without sequence loss, and run the shipped standalone demonstration. Report
checked record counts and lookup values.

**Output:**

```text
counts: a.fasta=3, b.fasta=4
first split: 3,1
fresh split: 2,2,1
stable merged records: 7
reopened indexed records: 7; checked a2 length=9; b3 sequence=ACGT repeated 4 times
GenBank-to-FASTA converted records: 94; checked first id and sequence equal
standalone:
  sample0.fasta: 5 sequences
  sample1.fasta: 5 sequences
  sample2.fasta: 5 sequences
  Split sample0.fasta into 3 chunks of <=2 records
  Indexed 15 records across 3 files
  Random lookup s2_3 length: 52
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- PASS — Streaming counts and stable merge preserve all records in deterministic order.
- PASS — Two fresh record-count splits are bounded and lossless.
- PASS — Persistent indexing survives close/reopen with exact values.
- PASS — Conversion preserves count/sequence while documentation warns about annotation loss.
- PASS — The standalone demonstration is runnable and emits readable checked values.

### Input 2 — Variant A

**Prompt:** Build and reuse a pyfastx index over a public gzip FASTA through
both the importable function and CLI, verify two random-access lengths and
persistent sidecar reuse, then parse a public gzip FASTQ with pysam and
Biopython. Demonstrate the documented Phred+33 versus legacy Phred+64 boundary.

**Output:**

```text
pyfastx records: 94
function selected lengths: 740,592
CLI selected length: 740
.fxi function+CLI hash/inode reuse: true
public gzip FASTQ records: 3
first public Phred+33 range: 18..26; pysam array equals Biopython array
legacy ASCII h: pysam=71, explicit fastq-illumina=40
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- PASS — The function builds a persistent gzip FASTA index with meaningful metadata.
- PASS — Function and CLI calls reuse the same sidecar.
- PASS — CLI JSON agrees with function-level random access.
- PASS — pysam and Biopython agree for public Phred+33 data.
- PASS — The legacy Phred+64 caveat is reproduced as 71 versus 40.

### Input 3 — Edge

**Prompt:** Summarize no inputs and one empty FASTA with an explicit readable
schema. Reject Boolean, zero, negative, floating-point, and string chunk sizes
before opening a deliberately missing input or creating outputs; reject invalid
worker counts. Confirm a valid five-record split remains lossless.

**Output:**

```text
no-match result: []
header: file,sequences,total_bp,min_len,max_len,avg_len
empty FASTA: empty.fasta,0,0,0,0,0
invalid chunk values rejected before I/O: False, True, 0, -1, 1.5, '2'
error family: records_per_file must be a positive integer; got <value>
valid five-record split: 2,2,1
invalid worker values rejected before Pool: 0, -2, True, 1.5
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- PASS — No-match output is a valid header-only CSV.
- PASS — An empty FASTA emits explicit zero metrics.
- PASS — Invalid chunks fail before input/output side effects with actionable errors.
- PASS — The valid boundary split is lossless.
- PASS — Invalid worker counts fail before pool construction.

### Input 4 — Variant B

**Prompt:** Exercise real prefix-derived output safety: reject traversal,
reserved filenames, a manifest escape, an existing target, and a
case-insensitive collision without changing a sibling sentinel. Under
`RLIMIT_NOFILE=32`, split 2,048 prefixes with `max_open_files=8` and verify every
manifest/file/parsed total plus an evicted interleaved group.

**Output:**

```text
../ traversal rejected; outside sentinel unchanged; partial manifest records=0
CON reserved filename rejected
../escaped.json manifest rejected; outside manifest absent
existing sample.fasta preserved exactly
Sample/sample collision: partial manifest records=1
RLIMIT_NOFILE=32; max_open_files=8
manifest records=2048; manifest files=2048; per-file count sum=2048
parsed output records=2048; descriptors before/after=4/4
evicted group a: a_1,a_2
```

**Scores:** Basic 40/40 | Specialized 59/60 | Total 99/100

**Assertions:**

- PASS — Record-derived paths cannot escape or alter a sibling.
- PASS — Reserved filenames and manifest traversal are rejected.
- PASS — Existing targets and case-insensitive collisions are safe/accounted.
- PASS — Handles stay bounded and all 2,048 records are written and parseable.
- PASS — Reopening an evicted group appends without truncation.

### Input 5 — Stress

**Prompt:** Create identical nested FASTA trees in opposite creation orders,
require `a.fasta,z/a.fasta,z/B.fasta`, byte-identical summaries and merges,
then run two-worker processing under fork, spawn, and a second spawn run with
identical ordered rows and totals.

**Output:**

```text
stable order: a.fasta,z/a.fasta,z/B.fasta
summary SHA-256: baf79636270cad3d4a4f4442eb03eee6cfe3fb06188ad3f7f460d6ddcdafcb79
merge SHA-256: fa38059609575f34feb44e5e3ddc886f976ae7549b7993a5c394e393a4f9dd3f
fork == spawn == spawn rerun: true
ordered rows: a.fasta 2/5; a.fasta 2/5; B.fasta 2/5
totals: 6 records, 15 bp
```

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- PASS — Opposite creation histories produce the same relative-path order.
- PASS — Summary rows and bytes are deterministic.
- PASS — Streaming merge order and bytes are deterministic.
- PASS — Real fork/spawn/spawn-rerun results agree.
- PASS — Parallel results preserve complete checked totals.

The duplicate `a.fasta` labels expose the non-blocking `BATCH-008` output
polish item: nested inputs remain deterministically ordered and correct, but a
future optional relative-path label would make those rows self-identifying.

## Independent regression reconciliation

| Finding | Result | Re-executed evidence |
|---|---|---|
| BATCH-001 | CLOSED | Traversal, reserved name, manifest escape, target preservation, collision manifest |
| BATCH-002 | CLOSED | 2,048 prefixes under descriptor limit; no descriptor growth; evicted-group append |
| BATCH-003 | CLOSED | Six-column header-only no-match CSV and zero-valued empty-file row |
| BATCH-004 | CLOSED | Six invalid sizes before I/O and fresh valid 2/2/1 split |
| BATCH-005 | CLOSED | Fork, spawn, and spawn rerun parity with two real workers |
| BATCH-006 | CLOSED | Exact nested stable order plus byte-identical summary and merge |
| BATCH-007 | CLOSED | pyfastx function twice plus CLI with persistent sidecar reuse |

The shipped candidate suite independently passed all 11 named tests with
`ResourceWarning` promoted to an error. Three Python files parsed and the
candidate tree remained cache-free.

## Final decision

- Static score: 97/100
- Execution average: 97.0/100
- Weighted final score: 97/100
- Structural veto: PASS
- Research veto: PASS
- Assertion pass rate: 25/25 (100%)
- Open P0/P1: none
- Open P2: `BATCH-008` only
- Grade: ⭐ Production Ready
- Relay state: `candidate-ready` for exact identity
  `f5558565b7f1068f76afdfaecee4a560c24917c037658c45b54f554d7ab23afd`

This certification does not create the product commit, publish the shared
audit record, run Marketplace intake, push, or release.

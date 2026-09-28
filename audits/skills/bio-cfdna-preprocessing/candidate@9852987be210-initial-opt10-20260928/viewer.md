> **Audit record for `bio-cfdna-preprocessing`**
> - Audited working candidate `9852987be2107ca7d54ae6e211f1fbd25ed2710910b1cd43c80c45dc8444059b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/liquid-biopsy/cfdna-preprocessing), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-cfdna-preprocessing

Generated: 2026-09-28  
Phase: bounded diagnostic initial audit  
Exact candidate: `sha256-manifest-v1:9852987be2107ca7d54ae6e211f1fbd25ed2710910b1cd43c80c45dc8444059b`

## Outcome

The exact candidate is **not ready**. Its diagnostic score is **38/100
(Reject)**. Both hard gates fail: the advertised wrapper failed all ten
consecutive calls, unvalidated values are interpolated into `shell=True`
pipelines, the core processing order contains methodological faults, and
neither simplex nor duplex code is usable in the pinned supported stack.

This is an initial diagnostic audit, not final certification. Route
`CFD-001` through `CFD-006` to `fix-scientific-skill`, then independently
re-audit the changed bytes.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 33 | 45 | 78 | 3/4 | ✅ |
| 2 | Variant A | 5 | 7 | 12 | 1/5 | ❌ |
| 3 | Variant B | 5 | 7 | 12 | 1/5 | ❌ |
| 4 | Edge | 18 | 19 | 37 | 2/5 | ⚠️ |
| 5 | Stress | 4 | 6 | 10 | 1/5 | ❌ |

**Execution average:** 29.8/100  
**Assertion pass rate:** 8/24  
**Static score:** 51/100  
**Arithmetic:** 51 × 0.4 = 20.4; 29.8 × 0.6 = 17.9; 20.4 + 17.9 = 38.3 → **38/100**

## Veto gates

### Skill veto

| Gate | Result | Basis |
|---|---|---|
| Operational stability | **FAIL** | Ten of ten consecutive advertised wrapper calls exited nonzero and produced no final BAM. |
| Structural contract | PASS | Frontmatter contains `name` and `description`; the tree and public entry points are identifiable. |
| Determinism | PASS | The arithmetic and every observed failure reproduce; no uncontrolled random path exists. |
| System security | **FAIL** | Two pipelines interpolate input-derived values into `shell=True` strings without validation or quoting. |

### Research veto

| Gate | Result | Basis |
|---|---|---|
| Scientific integrity | PASS | No fabricated identifier, study result, sample size, p-value, or efficacy claim was observed. |
| Practice boundaries | PASS | The skill stays at preprocessing and makes no patient diagnosis or treatment recommendation. |
| Methodological ground | **FAIL** | The recipe omits required UMI tags, aligns BAM bytes as sequences, filters in the wrong sort order, and overstates assay-path mandates. |
| Code usability | **FAIL** | Both advertised wrapper branches are unrunnable in the pinned supported environment. |

## Static evaluation

| Category | Score | Rationale |
|---|---:|---|
| Functional suitability | 5/12 | Useful concepts, but three independent workflow stages are broken and one decision rule is overgeneralized. |
| Reliability | 2/12 | 10/10 wrapper failures, raw stack traces, and unclear retry behavior. |
| Performance/context | 5/8 | Good disclosure, but invalid alignment work and misplaced indexing. |
| Agent usability | 8/16 | Readable ordering, invalid exact commands, and no structured run summary. |
| Human usability | 5/8 | Natural examples; ordinary UMI inputs and space-bearing paths fail. |
| Security | 6/12 | No credential issue; raw shell interpolation and absent argument validation. |
| Maintainability | 8/12 | Small modular tree; no regression suite for command contracts or flags. |
| Agent-specific | 12/20 | Precise trigger and routing; weak composition, idempotency, and stop rules. |
| **Subtotal** | **51/100** | Sum verified. |

## Detailed executions

Machine-readable values and command transcripts are in
[`evidence/execution-summary.json`](evidence/execution-summary.json),
[`evidence/stability-summary.json`](evidence/stability-summary.json), and
[`evidence/independent-qc.json`](evidence/independent-qc.json). Prompts are in
[`inputs.json`](inputs.json). The rerunnable harnesses are
[`run_cases.py`](run_cases.py), [`run_stability.py`](run_stability.py), and
[`verify_qc.py`](verify_qc.py).

### Input 1 — Canonical: public cfDNA insert-size QC

**Prompt:** Summarize the insert-size distribution of the public paired-end
human BAM and report the observation count, mode, median, 90–150 bp fraction,
and fraction above 250 bp.

**Executed surface:** `insert_size_qc()` on the durable nf-core human BAM.  
**Output:** n 2,819; mode 96 bp; median 123 bp; 90–150 bp fraction
0.64349059950337; fraction above 250 bp 0.0. An independent implementation
returned identical values.

**Assertions:**

- PASS — All five metrics match independent arithmetic.
- PASS — All requested fields are present with stable numeric types.
- PASS — Execution is deterministic and read-only.
- FAIL — The executable result does not carry chemistry, size-selection, or
  collection-condition boundaries needed for biological interpretation.

### Input 2 — Variant A: simplex UMI consensus wrapper

**Prompt:** Run `preprocess_cfdna()` on the paired-end inline-UMI fixture using
the documented `6M11S+T` read structure and simplex path.

**Executed surface:** the public wrapper with `duplex=False`.  
**Output:** exit 1. fgbio reports: `Read structures contains 2 molecular
barcode segments, but 0 tags provided.` No final BAM exists.

**Assertions:**

- FAIL — Required per-segment molecular-index tags are absent.
- FAIL — The next stage sends BAM rather than paired sequence records to BWA.
- FAIL — The final filter is wired to coordinate rather than query order.
- FAIL — No filtered and indexed simplex BAM is produced.
- PASS — The failure exits nonzero rather than claiming a usable result.

### Input 3 — Variant B: duplex UMI consensus wrapper

**Prompt:** Run the same fixture with `duplex=True` and produce a true-duplex
filtered, indexed BAM.

**Executed surface:** the public wrapper's duplex branch.  
**Output:** exit 1 at the shared extraction stage. No final BAM exists.

**Assertions:**

- FAIL — Reciprocal UMI segments are not extracted into required tags.
- PASS — Static code selects paired grouping for the duplex branch.
- FAIL — No valid mapped UMI-tagged templates reach the caller.
- FAIL — The final filter order violates its live interface.
- FAIL — No filtered and indexed duplex BAM is produced.

### Input 4 — Edge: flag-contaminated fragment QC

**Prompt:** Verify the advertised primary-fragment population on a BAM that
contains ordinary, secondary, supplementary, duplicate, and QC-fail records.

**Executed surface:** `insert_size_qc()` plus independent flag accounting.  
**Output:** n 4, median 190, mode 100, short fraction 0.5, long fraction 0.5.
The included four contain one supplementary, one duplicate, and one QC-fail
record. `max_size=-1` returns a normal-looking all-zero summary.

**Assertions:**

- PASS — Secondary alignment is excluded.
- FAIL — Supplementary alignment is included despite the primary claim.
- FAIL — Duplicate and QC-fail records are silently included.
- FAIL — Nonpositive `max_size` is not rejected.
- PASS — The focused result is independently reproducible.

### Input 5 — Stress: manual recipe and path robustness

**Prompt:** Execute the documented fgbio/bwa/samtools sequence, including
paths with spaces, and verify extraction, alignment, tag transfer, filtering,
and final output.

**Executed surfaces:** exact extract command; direct BWA-on-BAM stage; exact
coordinate filter; space-bearing realignment; quoted/queryname controls.  
**Output:** extraction exits 1; BWA exits 0 after reading two apparent 7,012 bp
sequences from BAM bytes but samtools rejects the SAM; coordinate filtering
exits 1; the unquoted space-path pipeline exits 1. The corrected quoted
realignment and queryname-filter controls each write four records.

**Assertions:**

- FAIL — The documented extraction command is rejected.
- FAIL — The first alignment consumes binary BAM bytes.
- FAIL — The filter order violates the live fgbio contract.
- FAIL — Space-bearing paths are split by the shell.
- PASS — Corrected controls prove that the pinned primary tools are available.

## Ordered recommendations

1. **CFD-001 P0 — UMI extraction omits required tags.** Add validated
   per-segment tags and test simplex plus reciprocal-duplex layouts.
2. **CFD-002 P0 — Alignment consumes BAM as sequence input.** Convert to
   paired FASTQ, align, zipper metadata, and assert records/pairing/tags.
3. **CFD-003 P0 — Consensus filter receives wrong order.** Query-sort/group
   before filtering; coordinate-sort and index afterward.
4. **CFD-004 P0 — Shell interpolation permits injection.** Replace raw shell
   strings with connected argv processes and validate paths/threads.
5. **CFD-005 P1 — Fragment QC population is contaminated.** Enforce and report
   a documented flag policy and validate numeric bounds.
6. **CFD-006 P1 — Assay-path rules are too categorical.** Make duplex and
   chemistry guidance conditional on assay design and empirical validation.

See [`finding-ledger.md`](finding-ledger.md) for fixer-ready dispositions and
[`scientific-source-notes.md`](scientific-source-notes.md) for source checks.

## Scope and safety

- Minor repairs: none; every defect changes a scientific method, executable
  interface/order, validation contract, or security boundary.
- Restricted or inaccessible primary surfaces: none.
- Deferred: whole-genome scale, production throughput, wet-lab recovery,
  empirical error-floor validation, and clinical LoD.
- Candidate bytes and origin checkout were unchanged.

> **Audit record for `bio-batch-processing`**
> - Audited working candidate `244c82a53a96dce4586308b71ed678bae2bd3bed685a1db7aa44c6459b0c8990`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/sequence-io/batch-processing), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-batch-processing

Generated: 2026-09-28  
Phase: bounded diagnostic initial audit  
Exact candidate: `0bc0b31fc52742dbec1034f698103434cc9460c3` / `244c82a53a96dce4586308b71ed678bae2bd3bed685a1db7aa44c6459b0c8990`

## Outcome

The exact candidate is **not ready**. Its diagnostic score is **55/100
(Reject)**, and the Data Analysis Code Usability research veto independently
fails because the advertised multiprocessing recipe hangs under Python spawn.
The most urgent issue is BATCH-001: a sequence ID containing `../` is used as
a writable path and, in the controlled audit sandbox, escaped the intended
directory and truncated a sibling file.

This is an initial diagnostic audit, not final certification. Route all seven
open findings to `fix-scientific-skill`, then independently re-audit the fixed
bytes.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 38 | 54 | 92 | 4/4 | ✅ |
| 2 | Variant A | 32 | 45 | 77 | 3/4 | ✅ |
| 3 | Edge | 14 | 22 | 36 | 0/4 | ❌ |
| 4 | Variant B | 8 | 12 | 20 | 0/4 | ❌ |
| 5 | Stress | 14 | 25 | 39 | 0/4 | ❌ |

**Execution average:** 52.8/100  
**Assertion pass rate:** 7/20  
**Static score:** 58/100  
**Arithmetic:** 58 × 0.4 = 23.2; 52.8 × 0.6 = 31.68 → 31.7; 23.2 + 31.7 = 54.9 → **55/100**

## Veto gates

### Skill veto

| Gate | Result | Basis |
|---|---|---|
| Operational stability | PASS | The exact standalone entry point and canonical public functions execute; failures are bounded to identified recipe inputs. |
| Structural contract | PASS | Frontmatter contains the required name and description, and the Skill tree is coherent. |
| Determinism | PASS | No random numerical method is present; traversal nondeterminism is a scored reproducibility finding rather than a stochastic critical-result veto. |
| System security | PASS | The shipped script contains no raw-code execution, shell interpolation, credential handling, or destructive command. BATCH-001 remains a P0 data-safety defect in a public recipe. |

### Research veto

| Gate | Result | Basis |
|---|---|---|
| Scientific integrity | PASS | No identifier, study, count, quality, or statistical value was fabricated. |
| Practice boundaries | PASS | Outputs are sequence-file engineering, not patient advice. |
| Methodological ground | PASS | Streaming/indexing and quality-encoding claims are scientifically sound. |
| Code usability | **FAIL** | The exact public Pool recipe timed out under spawn and produced no totals; see BATCH-005. |

## Static evaluation

| Category | Score | Rationale |
|---|---:|---|
| Functional suitability | 7/12 | Canonical paths work; advertised boundary and platform cases do not. |
| Reliability | 3/12 | Raw errors, silent loss, descriptor exhaustion, partial output, and a hang are reproducible. |
| Performance/context | 6/8 | Good progressive disclosure and streaming, but unique prefixes consume unbounded descriptors. |
| Agent usability | 10/16 | Clear routing; weak contracts for ordering, validation, side effects, and platform constraints. |
| Human usability | 5/8 | Natural triggers, but edge failures are cryptic or silent. |
| Security | 5/12 | No secret or shell risk; ID-derived paths can escape and overwrite. |
| Maintainability | 9/12 | Compact modules; no regression coverage for documented edge behavior. |
| Agent-specific | 13/20 | Precise trigger and layering; weak structured I/O, idempotency, and escape hatches. |
| **Subtotal** | **58/100** | Sum verified. |

## Detailed executions

The exact prompts are in [`inputs.json`](inputs.json), the bounded harness is
[`scripts/run_cases.py`](scripts/run_cases.py), full values and transcripts are
in [`evidence/execution-summary.json`](evidence/execution-summary.json), and the
ordered remediation record is [`finding-ledger.md`](finding-ledger.md).

### Input 1 — Canonical: count, split, and index

The candidate creates three five-record files, reports counts 5/5/5, splits one
file into chunks 2/2/1, builds a 15-record SQLite index, and preserves lookup
length 52 after reopening. The standalone script exits zero with empty stderr.
All four assertions pass.

### Input 2 — Variant A: compressed readers and qualities

An auditor-authored pyfastx probe indexes 94 gzip FASTA records, writes `.fxi`,
and returns the same first sequence as Biopython. For a legacy Phred+64 record,
pysam returns `[71, 71, 71, 71]` while Biopython `fastq-illumina` correctly
returns `[40, 40, 40, 40]`, proving the Skill's warning. The failed assertion
is coverage: no runnable pyfastx recipe ships. See BATCH-007.

### Input 3 — Edge: empty discovery and chunk sizes

The empty summary creates a zero-byte CSV and raises `IndexError: list index out
of range`. `records_per_file=0` returns no outputs for a 94-record input;
`-1` exposes a raw `islice` ValueError. All four assertions fail. See
BATCH-003 and BATCH-004.

### Input 4 — Variant B: prefix cardinality and containment

The pinned environment has a 1,024 soft descriptor limit. The recipe grows from
9 to 1,024 open descriptors and fails on the next open after 1,015 prefixes.
A separate controlled `../escaped_record` ID writes outside the intended
directory and replaces a sibling sentinel with one FASTA record. All four
assertions fail. See BATCH-001 and BATCH-002.

### Input 5 — Stress: traversal and multiprocessing

On WSL ext4, two directories with the same 200 names return ascending versus
descending `Path.glob()` order according to creation history. The exact
top-level Pool recipe then times out after 15 seconds under spawn with no
totals. All four assertions fail. See BATCH-005 and BATCH-006.

## Ordered open findings

1. **BATCH-001 / P0 — ID prefix can escape output directory and overwrite.**
2. **BATCH-002 / P1 — high-cardinality prefix splitting exhausts file descriptors.**
3. **BATCH-003 / P1 — empty summary crashes after creating a zero-byte output.**
4. **BATCH-004 / P1 — invalid chunk sizes fail raw or silently lose all records.**
5. **BATCH-005 / P1 — unguarded Pool recipe hangs under spawn.**
6. **BATCH-006 / P1 — unsorted glob traversal makes output order filesystem-dependent.**
7. **BATCH-007 / P2 — advertised pyfastx coverage has no shipped runnable recipe.**

## Surface classification and deferrals

| Surface | Classification | Notes |
|---|---|---|
| `scripts/batch_process.py` | executed | Direct entry point plus imported count, split, demo, and index behavior. |
| Biopython count/merge/split/convert/index recipes | executed | Tooling's 13-surface public smoke plus targeted audit edge cases. |
| `pysam.FastxFile` | executed | Public gzip FASTQ and explicit legacy Phred+64 comparison. |
| advertised pyfastx path | executed-auditor-authored | Runtime works; missing shipped recipe is BATCH-007. |
| multiprocessing recipe | executed-with-failure | Linux fork passed tooling; exact recipe under spawn timed out. |
| traversal determinism | executed-with-failure | Mounted workspace happened to sort; ext4 creation-order probe did not. |

Deferred executable surfaces: **none**.  
Static-only breadth: tens-of-millions scale benchmarking and exhaustive FASTA,
FASTQ, compression, duplicate-ID, and filesystem matrices; these cannot support
final readiness in this bounded initial audit.  
Blocked executable surfaces: **none**.  
Restricted-access items: **none**.  
Minor repairs: **none**; every finding changes behavior, interface, safety,
method, or coverage and exceeds the audit-local repair boundary.

## Identity, tooling, and safety

- Exact source identity and per-file hashes: [`source-identity.json`](source-identity.json).
- Tooling record: `F:\OpenScience\audit-envs\bio-batch-processing\TOOLS.md`,
  SHA-256 `38ee571306947a57da3c2d627a6bb191ef8014d0136c09a3b433d43ec4a6ccc3`.
- Environment fingerprint SHA-256:
  `5eb133e158c59a258243d162d0d8b5d8ad8f1476e75bf0014b9e17c140fdb702`.
- WSL `science`, user `sci`, interop unset; Python 3.12.14, Biopython 1.88,
  pysam 0.24.1, pyfastx 2.3.1.
- Two harness preflights that initially surfaced uncaught product failures are
  retained in `evidence/harness-preflight-failures.txt`; both symptoms were then
  converted into checked cases rather than suppressed.
- Candidate identity remains `244c82a5...c8990`; candidate cache count is zero.
- Origin remains clean at `d91ed3...`; candidate remains the expected four
  untracked normalized files on unchanged HEAD `0bc0b31...`.
- No product/control commit, push, PR, release, publication, Marketplace intake,
  credential use, or mutable remote action occurred.

## Transition

Next role: **`fix-scientific-skill`**. Direct re-audit is inappropriate because
BATCH-001 through BATCH-007 remain open and BATCH-005 fails the research veto.

> **Audit record for `bio-atac-seq-consensus-peakset`**
> - Audited working candidate `238e6dfd2a0a5da05cf1c37ceba3de899a1f298927e49ddc5c9bb668eb8eda5c`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/consensus-peakset), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-atac-seq-consensus-peakset

Generated: 2026-09-28  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `238e6dfd2a0a5da05cf1c37ceba3de899a1f298927e49ddc5c9bb668eb8eda5c`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 28 | 38 | 66 | 3/4 | ❌ PARTIAL |
| 2 | Variant A | 34 | 45 | 79 | 4/4 | ✅ COMPLETED |
| 3 | Edge | 16 | 8 | 24 | 1/4 | ❌ COMPLETED |

**Execution average:** 56.3 / 100  
**Assertion pass rate:** 8 / 12  
**Static score:** 66 / 100  
**Final diagnostic score:** 60 / 100 — ❌ Reject (veto override)

The strict audit JSON is [`report.json`](report.json), the ordered fix sequence is
[`finding-ledger.md`](finding-ledger.md), and exact provenance is in
[`source-identity.json`](source-identity.json). A 64-character canonical audit
manifest replaced the prior expected identity recipe; candidate bytes were not
changed.

## Veto review

### Skill veto — PASS

- Stability: PASS. The launch failure is deterministic and environment-specific; a normalized disposable copy runs.
- Contract: PASS. Frontmatter and documented outputs are present.
- Determinism: PASS. The tested commands returned stable, parsed outputs.
- Security: PASS. No credential exposure, raw-code execution, or destructive command path was found.

### Research veto — FAIL

- Scientific Integrity: PASS. No scientific values were fabricated.
- Practice Boundaries: PASS. No clinical or prescriptive conclusion was produced.
- Methodological Ground: **FAIL.** A missing summit column silently changes peak centers while preserving a plausible output width and success message.
- Code Usability: **FAIL.** The exact candidate script fails under the prepared Bash runtime because of CRLF line endings.

## Detailed outputs

### Input 1 — Canonical: public 3,000-row hg19 narrowPeak workflow

**Prompt:** Run the shipped Corces-style iterative-overlap workflow on the prepared public hg19 narrowPeak fixture, matching hg19 sizes and blacklist. Inspect scientific output and the optional SAF contract.

**Execution:** Direct invocation of the candidate script failed before processing due to CRLF. A disposable LF-normalized copy was run without editing candidate bytes.

**Output:** 3,000 input peaks; 2,927 peaks after greedy overlap; 2,886 after blacklist filtering; all final intervals were 501 bp. SAF had 2,886 data rows and its header, identifiers, and 1-based inclusive coordinates matched the final BED.

**Scores:** Basic 28/40 | Specialized 38/60 | Total 66/100

**Assertions:**

- [FAIL] Exact shipped runner launches under Bash — carriage-return characters break the shebang and `set -euo pipefail`.
- [PASS] 3,000 peaks yield 2,927 greedy non-overlapping windows — parsed intermediate row counts match.
- [PASS] Final BED has only configured 501 bp windows — all 2,886 widths equal 501.
- [PASS] SAF contract matches BED — all 2,886 rows have unique coordinate IDs and `Start = BED start + 1`.

Transcript: [`evidence/primary-rerun.txt`](evidence/primary-rerun.txt) and
[`evidence/direct-crlf-rerun.txt`](evidence/direct-crlf-rerun.txt).

### Input 2 — Variant A: two per-replicate files

**Prompt:** Run the same workflow on two separate per-replicate narrowPeak files through the multi-file glob, then parse the pooled, iterative, final BED, and SAF outputs.

**Execution:** Two 200-row portions of the public fixture were supplied as separate narrowPeak files.

**Output:** 400 pooled records; 393 after greedy overlap; 388 after blacklist filtering. Both BED and SAF outputs were emitted.

**Scores:** Basic 34/40 | Specialized 45/60 | Total 79/100

**Assertions:**

- [PASS] Two separate narrowPeak files are accepted — both are included in the pooled output.
- [PASS] Exactly 400 records are pooled — 200 from each file.
- [PASS] Greedy overlap removes overlapping windows — 393 remain.
- [PASS] The multi-file output contract completes — 388 final BED rows and SAF are emitted.

Transcript: [`evidence/multifile-rerun.txt`](evidence/multifile-rerun.txt).

### Input 3 — Edge: absent summit-offset column

**Prompt:** Exercise the high-consequence column-contract boundary with a 9-column BED-like record and inspect whether the tool rejects it or reports a valid summit-centered feature.

**Execution:** A one-row 9-column input completed through the normalized runner with no format warning.

**Output:** `chr1 30000000 30000100 peakA 100 + 20 10 8` produced `chr1 29999750 30000251`. Since column 10 was absent, awk converted the missing value to zero and the region was centered at the original start, not a supplied summit.

**Scores:** Basic 16/40 | Specialized 8/60 | Total 24/100

**Assertions:**

- [FAIL] Missing column 10 is rejected or warned about — it is silently accepted.
- [FAIL] Output center derives from a valid summit — it derives from the input start.
- [FAIL] A shifted result cannot look successful — the command reports one final 501 bp peak.
- [PASS] Output width is 501 bp — width is correct while location is wrong.

Transcript: [`evidence/9col-rerun.txt`](evidence/9col-rerun.txt); exact bounded
input: [`inputs/adversarial-9col.bed`](inputs/adversarial-9col.bed).

## Static evaluation

| Category | Score | Max | Main reason for deduction |
|---|---:|---:|---|
| Functional suitability | 6 | 12 | Runner launch incompatibility and unvalidated summit columns |
| Reliability | 6 | 12 | File-format assumptions and stale-output risk |
| Performance/context | 6 | 8 | Good reference layering; greedy implementation has scale limits |
| Agent usability | 12 | 16 | Clear route with missing execution preconditions |
| Human usability | 6 | 8 | Usable examples, but the 10-column script contract is implicit |
| Security | 9 | 12 | No secrets or dangerous operations; user paths are unquoted |
| Maintainability | 7 | 12 | Good separation, no shipped validation or regression fixture |
| Agent-specific | 14 | 20 | Strong trigger and routing; compatibility/escape checks are incomplete |
| **Total** | **66** | **100** | |

## Ordered remediation

1. `BAP-001` P0 — validate all narrowPeak rows and summit offsets before arithmetic; explicitly handle the `-1` sentinel.
2. `BAP-002` P0 — normalize the shipped script to LF and verify direct invocation in the target Bash environment.

## Environment and limitations

- Tooling inventory: `F:\OpenScience\audit-envs\bio-atac-seq-consensus-peakset\TOOLS.md` (SHA-256 `0895f658996fcf5dd5fafc16e63083f21619e94c809205ec836db898fb761a81`).
- Environment: WSL2 `science`; Bash 5.3.9; Python 3.12.14; bedtools 2.31.1; R 4.4.1. rtracklayer and GenomicRanges were unavailable.
- Public fixture provenance and matching references are listed in `TOOLS.md`; no new data or packages were fetched.
- DiffBind, pybedtools, IDR, liftOver, and featureCounts downstream workflows remain static-only or blocked; no BAM inputs were supplied.
- Assembly agreement is a documented required input constraint. This run used matching hg19 assets; no separate assembly mismatch finding was substantiated.
- No audit-local repair was attempted. No product edit, commit, push, or remote publication occurred.

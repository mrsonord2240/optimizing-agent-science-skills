> **Audit record for `bio-alignment-indexing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1c12d65](https://github.com/mrsonord2240/bioSkills/tree/1c12d65aa177cc782a8e69e51130afb9caed5250/alignment-files/alignment-indexing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-indexing

Generated: 2026-09-24 · rendered from `report.json` by `tools/render_viewer.py`.

> This viewer is **generated from the audit report**, not written by the auditor. It restates the report's own recorded scores, notes and assertions and adds nothing to them. Where a hand-written viewer would argue from the runs, this one points at the scripts in [scripts/](scripts/) instead.

Source: `mrsonord2240/bioSkills@1c12d65aa177cc782a8e69e51130afb9caed5250:alignment-files/alignment-indexing`
Audit type: final pass: fixed and audited under one brief, see CHECKPOINT.md
Category: Data Analysis · Execution mode: D · Complexity: Complex · N = 8 · Executed: 8/8

## What the Skill claims to do

Create and use BAI/CSI indices for BAM/CRAM files using samtools and pysam. Use when enabling random access to alignment files or fetching specific genomic regions.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 59 | **97** | 3/3 | yes | ✅ |
| 2 | Variant A | 38 | 59 | **97** | 3/3 | yes | ✅ |
| 3 | Edge | 37 | 58 | **95** | 3/3 | yes | ✅ |
| 4 | Variant B | 38 | 58 | **96** | 3/3 | yes | ✅ |
| 5 | Stress | 38 | 58 | **96** | 3/3 | yes | ✅ |
| 6 | Regression edge bundle | 38 | 58 | **96** | 3/3 | yes | ✅ |
| 7 | Fresh input | 38 | 59 | **97** | 3/3 | yes | ✅ |
| 8 | Fresh input | 38 | 59 | **97** | 3/3 | yes | ✅ |

**Execution Average: 96.4 / 100** · **Assertion Pass Rate: 24/24**

**Static: 94/100** · Static weighted 37.6 + dynamic weighted 57.8 = **95/100** → ⭐ Production Ready, deployable.

---

## Veto gates

### Skill veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| stability | PASS |  |
| contract | PASS |  |
| determinism | PASS |  |
| security | PASS |  |

### Research veto — **PASS**

| Check | Result | Detail |
|---|---|---|
| scientific integrity | PASS | All quantitative claims are backed by saved real or labelled synthetic tool output. |
| practice boundaries | PASS | Alignment indexing has no diagnostic or prescriptive output. |
| methodological ground | PASS | BAI/CSI limits, CRAM reference behavior, region access and flag semantics were re-executed. |
| code usability | PASS | Every shipped runnable path and both fresh tests completed. |

## Static score

| Category | Score | Note |
|---|---|---|
| functional suitability | 12/12 | BAI, CSI, CRAI, region access, CRAM, idxstats, faidx and freshness paths are complete and executed. |
| reliability | 12/12 | Helpers now validate the audited parser/index edge cases and report recoverable failures clearly. |
| performance context | 7/8 | The workflow is linear; SKILL.md remains a substantial single document. |
| agent usability | 15/16 | Versioned commands, decision tables and verified errors make cold-start use clear. |
| human usability | 8/8 | Natural trigger wording and examples cover normal and edge index requests. |
| security | 11/12 | No credentials or raw-code execution; paths are quoted and parser coordinates are validated. |
| maintainability | 10/12 | The example and documented helpers are testable, though Bash and Python helpers remain parallel implementations. |
| agent specific | 19/20 | Precise trigger, idempotent freshness helpers and explicit stop conditions are present. |

## Input 1 — Canonical: Archived regression: BAI/CSI indexing, regions, idxstats and shipped Python snippets

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 59/60 · **Total 97/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: r1_canonical.py: 42/42 checks PASS.

| Assertion | Result | Evidence |
|---|---|---|
| BAI/CSI region counts equal full-scan truth | PASS | 53 regions and six access methods matched. |
| Fresh, missing, CSI-only and alternate-name index cases behave as documented | PASS | mtimes and counts were asserted. |
| Mitochondrial awk and fetch_regions output are correct | PASS | chrM/MT/empty fixtures and real region output passed. |

## Input 2 — Variant A: Archived regression: CRAM reference, REF_PATH, idxstats and faidx

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 59/60 · **Total 97/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: r2_cram_faidx.py: 22/22 checks PASS; the REF_PATH M5 cache probe passed.

| Assertion | Result | Evidence |
|---|---|---|
| -T and pysam reference_filename return the BAM-equivalent CRAM count | PASS | 5642 records. |
| REF_PATH guidance distinguishes an M5 cache from a FASTA directory | PASS | plain FASTA directory gave 0, M5 cache gave 2 records. |
| CRAM and FASTA error paths are actionable | PASS | fresh CRAI retained and missing reference has the documented hint. |

## Input 3 — Edge: Archived regression: unsorted BAMs, missing indices, contig names and parser boundaries

- Status: ✅ COMPLETED · Basic 37/40 · Specialized 58/60 · **Total 95/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: r3_edge.py: 27/27 checks PASS.

| Assertion | Result | Evidence |
|---|---|---|
| Common Errors strings reproduce on the installed tool versions | PASS | samtools 1.24 and pysam 0.24.1 output was checked. |
| Unsorted and header-only BAM handling is correct | PASS | indexing and recovery output matched assertions. |
| Supported region forms and special contig names resolve correctly | PASS | samtools-equivalent counts passed. |

## Input 4 — Variant B: Archived regression: large-contig BAI/CSI boundaries and BAM position limits

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: r4_large_genome.py: 18/18 checks PASS after its text assertions were updated for the corrected wording.

| Assertion | Result | Evidence |
|---|---|---|
| BAI rejects a >537-Mbp contig and CSI returns hand-known reads | PASS | 830-Mbp and 2.0-Gbp fixtures passed. |
| Custom CSI depths and min_shift claims are correct | PASS | CSI headers were parsed. |
| The Skill distinguishes a long header from an unwriteable >2^31-1 position | PASS | 3-Gbp-header and over-limit-read fixtures passed. |

## Input 5 — Stress: Archived regression: stale/mixed indices, BED access, threads and idxstats semantics

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: r5_stress.py: 29/29 checks PASS.

| Assertion | Result | Evidence |
|---|---|---|
| Stale CSI/BAI cases end with a correct usable index | PASS | counts equal full-scan truth. |
| --region-file and -M -L use the index while plain -L scans | PASS | damaged-tail fixture passed. |
| idxstats and primary-mapped flag semantics match the documented recipes | PASS | hand-built and ARTIC fixtures passed. |

## Input 6 — Regression edge bundle: Archived regression: parser matrix plus Bash/Python index-helper edge cases

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 58/60 · **Total 96/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: n6_region_parser.py: 16/16; n7_ensure_index_edges.py: 29/29; n7b_sibling_index_probe.py: 3/3 checks PASS.

| Assertion | Result | Evidence |
|---|---|---|
| Parser matrix includes commas, colon contigs, zero start and reversed intervals | PASS | counts or clean errors matched expected behavior. |
| Format-specific candidates retain sibling BAM/CRAM alternate-name indices | PASS | standard and alternate fixtures passed. |
| CSI -m 12 survives stale rebuild and empty batches are no-ops | PASS | BGZF header and shell-mode fixtures passed. |

## Input 7 — Fresh input: New real-fixture parser challenge: comma contigs, zero coordinate and reversed interval

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 59/60 · **Total 97/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: final_20260924/test_fetch_regions.py PASS.

| Assertion | Result | Evidence |
|---|---|---|
| Comma-bearing contig names are not normalized away | PASS | ctg,1 and ctg,1:100-200 parse correctly. |
| chr22:0-4000 matches samtools | PASS | 5550 reads. |
| A reversed interval emits a one-line Bad region error | PASS | no traceback. |

## Input 8 — Fresh input: New helper challenge: CSI -m preservation, sibling isolation and empty batch

- Status: ✅ COMPLETED · Basic 38/40 · Specialized 59/60 · **Total 97/100**
- Execution: WSL science env alignment-files: samtools/htslib 1.24, pysam 0.24.1, Python 3.12.14
- Finding: final_20260924/test_ensure_index.sh PASS.

| Assertion | Result | Evidence |
|---|---|---|
| Stale CSI preserves min_shift=12 | PASS | BGZF-decompressed CSI header asserted. |
| BAM and CRAM sibling indices survive each other's refresh | PASS | alternate-name fixture passed. |
| Empty BAM directory succeeds without a literal glob invocation | PASS | nullglob no-op passed. |

## Key strengths

- All six open P2 findings were corrected and their old regression inputs pass.
- The parser now matches samtools at the zero boundary and preserves comma-bearing contigs.
- The Bash helper preserves custom CSI binning and cannot remove a sibling format's index.
- CRAM reference and large-genome documentation are tied to observed tool behavior.

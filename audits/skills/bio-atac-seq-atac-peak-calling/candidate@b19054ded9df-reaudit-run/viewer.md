> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Audited working candidate `b19054ded9df6cf3d48b45b6f38c7b209454bb2627f95b5f7d73c794a02720c2`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Independent final re-audit performed 2026-09-30 by a Claude (Anthropic) agent that did not write, fix or initially audit the Skill.
> - Data: ENCODE GM12878 ATAC chr1:1-30Mb filtered BAMs (ENCSR095QNB), a 6% read subsample of replicate 2 (failing library), and small synthetic fixtures (planted chrM reads, planted chrM-mate pair). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-atac-peak-calling (re-audit)

Candidate: `sha256-manifest-v1 b19054ded9df6cf3d48b45b6f38c7b209454bb2627f95b5f7d73c794a02720c2` (5 files, 39,370 bytes), branch `fix/atac-atac-peak-calling`, uncommitted; recomputed live at start and end, unchanged. Prior audit identity `e8bc49ba...7658` (76, Beta Only).
Category: Data Analysis, Mode D, Moderate, N = 5. Environment: WSL `science`, micromamba `bio-atac-seq-atac-peak-calling` (macs3 3.0.4, macs2 2.2.9.1 + shim, Genrich 0.6.2, samtools 1.24, bedtools 2.31.1) and `-idr` (idr 2.0.4.2, numpy 1.23.5); fingerprint `08bd20df...02b6` unchanged.
Scripts: `scripts/` (run_pass.sh, run_pass_macs2.sh, make_fail_lib.sh, run_fail.sh, test_ratio_logic.sh, disjoint_check.sh, check_pass_outputs.sh, check_bigwig.sh, docs_callers.sh, guards_and_recipes.sh, install_dryrun.sh, manifest.py, build_report.py, validate_report.py). Logs and outputs: `out/`, `scripts/*.log`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (script, passing library, bigWig) | yes | 37 | 55 | 92 | 5/5 | pass |
| 2 | Variant A (failing library, ratio logic, macs2) | yes | 36 | 54 | 90 | 3/4 | pass |
| 3 | Variant B (Genrich, hmmratac) | yes | 34 | 53 | 87 | 4/4 | pass |
| 4 | Edge (guards, chrM) | yes | 35 | 51 | 86 | 3/3 | pass |
| 5 | Variant B (install recipe, NFR) | yes | 34 | 51 | 85 | 3/3 | pass |

**Execution Average: 88.0 / 100** (Layer 1 35.2, Layer 2 52.8) - **Assertion Pass Rate: 18/19 (94.7 %)**
**Static: 85/100** - **Final: 87 (Production Ready)**. Vetoes: none. No open P0/P1. Readiness: **candidate-ready**.

## Fix retest (each claimed fix reproduced independently)

| ID | Result | Evidence |
|---|---|---|
| ATACPC-001 disjoint pseudoreps | confirmed | rep1 re-split: 524,024 names, 0 shared, pairs intact (`scripts/disjoint_check.log`) |
| ATACPC-002 Nt/N1/N2/Np, ratios | confirmed | passing library PASS 1.155/1.093; failing library FAIL 3.394/4.906; 7 unit cases on the shipped block incl. inf and 2.0 boundary |
| ATACPC-003 install recipe | confirmed | both create lines solve (dry-run), old line fails; delta pass real fresh-env run reused (same bytes) |
| ATACPC-004 MACS variable | confirmed | macs2 mode byte-identical to macs3 |
| ATACPC-005/006/013 genome size, guards, quoting | confirmed | 8 guard cases rc=1 with named errors; chrM guard on planted fixture |
| ATACPC-007 conservative set, bigWig | confirmed | 1,188 peaks, 0 blacklist overlap, 1,059 overlap ENCODE; bigWig header readback equals the bedGraph |
| ATACPC-008/009 Genrich, hmmratac | confirmed | 14,498 peaks; 2,064 regions with model and cutoff files; 14,328 reproduces the quoted figure |
| ATACPC-010/011 wording, single-sample | confirmed statically; text consistent across the three files |
| ATACPC-012 ROSE | still static-only, labelled illustrative (P2 recommendation, not blocking) |
| NEW-014 chrM recipe | confirmed on a synthetic pair BAM; residual orphan-mate note is ATACPC-016 |

## Inputs

**1 Canonical.** MACS3 run on the GM12878 chr1 slice, 8.9 min: Nt=1197 N1=1143 N2=1249 Np=1036, PASS; every IDR row score >= 540; rep1 4,803 / rep2 4,366 / pooled 4,310 peaks; conservative 1,188 rows, 10 columns, 0 blacklist overlaps. The true-replicate IDR plot renders four legible panels (`out/true_reps.idr.png`). bigWig readback: version 4, 29,998,866 bases, max 7,458.77, equal to the bedGraph.

**2 Variant A.** Rep2 replaced by a 6% read subsample: Nt=495 N1=1143 N2=233 Np=1680, rescue 3.394, self 4.906, FAIL, as the ENCODE rule requires. The first attempt failed with a truncated intermediate BAM in `samtools merge` (`out/fail_lib_attempt1_merge_truncated.log`) while three pipelines ran concurrently on drvfs; the identical rerun completed. Not reproduced in any other run; counted as one failed assertion, attributed to the environment.

**3 Variant B.** Genrich and hmmratac exactly as documented (see assertions in `report.json`).

**4 Edge.** Guards and the chrM check, tested on a planted 3-read chrM BAM (source BAMs have no chrM reads). Adequate: the guard is a single idxstats sum, and the planted fixture carries a real chrM contig. A chr1 read whose mate is on chrM survives the documented recipe (ATACPC-016, P2).

**5 Variant B.** Install lines solved by dry-run against current channels; NFR recipe 10,951 peaks.

## Coverage limits

Whole-genome IDR, mm10, standalone HMMRATAC, HOMER, chromap and ROSE were not run (ROSE static-only, labelled illustrative). Degenerate libraries where IDR itself aborts were not tested. Reused evidence: delta-pass fresh-environment install and script run (identical Skill bytes, environment fingerprint unchanged).

## Recommendations (all P2)

ATACPC-015 description names 501 bp consensus peaks the Skill does not build; ATACPC-012 ROSE unexecuted; ATACPC-016 chrM recipe leaves orphan mates.

> **Audit record for `bio-atac-seq-footprinting`**
> - Audited working candidate `737bd9416e385a3e91eba2ca2d4f5849c575840e866f46392c0e5533cf84e4cd`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-footprinting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent. Initial diagnostic audit only; not a certification.
> - Data: ENCODE GM12878 (rep1) and K562 (rep1) ATAC chr1:1-30 Mb filtered BAMs, ENCODE IDR peaks, hg38 chr1, JASPAR 2024 PFMs. Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-footprinting

Candidate: `sha256-manifest-v1 737bd9416e385a3e91eba2ca2d4f5849c575840e866f46392c0e5533cf84e4cd` (5 files), branch `fix/atac-footprinting` @ 3186916 (candidate untracked).
Category: 3 - Data Analysis - Mode D - Moderate, N = 5.
Environment: WSL `science`, micromamba `bio-atac-seq-footprinting` (TOBIAS 0.17.5, samtools 1.19.2, deepTools 3.5.5), `-rgt` (RGT 1.0.2), `-pydnase` (pyDNase 0.3.0), `-scprinter` (scPrinter 1.2.0, GPU). Fingerprints in `TOOLS.md` (sha256 `c8b39174...d55c`).
Code: `scripts/a1..a9*` (this run), `build_records.py`, `validate_report.py`. Output: `out/`, logs `logs/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (run_tobias.sh, GM12878 vs K562) | yes | 31 | 43 | 74 | 3/5 | warn |
| 2 | Variant A (NFR filter, shift, TOBIAS on NFR BAMs) | yes | 35 | 50 | 85 | 4/4 | pass |
| 3 | Edge (no-CTCF motif set; space in path) | yes | 27 | 33 | 60 | 2/4 | warn |
| 4 | Variant B (HINT-ATAC, Wellington) | partial | 22 | 30 | 52 | 1/4 | fail |
| 5 | Variant B (scPrinter, GPU) | partial | 24 | 36 | 60 | 3/5 | fail |

**Execution Average: 66.2 / 100** - **Assertion Pass Rate: 13/22 (59.1 %)**
**Static: 75/100** - **Final: 70 (Beta Only)**. Vetoes: none. Deployable: no.

Surface classifications: run_tobias.sh (executed), SKILL.md three TOBIAS calls (executed via the script), NFR filter (executed), alignmentSieve --ATACshift (executed), HINT-ATAC (executed with improvised command and hand-built RGT data; documented install fails), Wellington (executed, default and -A), scPrinter classic footprinting (executed with undocumented pins; seq2PRINT training not run), PIQ / seqOutBias / chromBPNet bias model / TOBIAS+scPrinter combination (static-only, no Skill code), full-depth (>= 50 M reads, whole genome) run (blocked: only chr1 slices of 1.0 M and 5.5 M reads available).

## Input 1 - Canonical: run_tobias.sh unmodified

`bash scripts/run_tobias.sh cond1.bam cond2.bam peaks.bed hg38.chr1.fa blacklist motifs_subset.pfm out 8`; rc 0, 6 m 18 s (script sha256 `503278b3...f377`). Peaks are the 2,433 union IDR peaks minus blacklist; 13 JASPAR IDs.
- Biology (`scripts/check_bindetect.py`): GATA1 -0.385 (K562), IRF4 +0.588, EBF1 +0.055 (GM12878), CTCF 1,203 sites. PASS.
- CTCF MA0139.2 aggregate (513 cond1-bound sites): flank-minus-core 3.78 (cond1) and 5.81 (cond2) signal units; PDF rendered (`out/a1_ctcf_aggregate_page1.png`): clear central dip with shoulders at about -25 and +35 bp, legible.
- FAIL: the summary comment says ranked by absolute change but the command sorts by p-value (CTCF -0.222 printed above GATA1 -0.385) - FOOT-006.
- FAIL: negative control (`out/a7_ctcf_profiles.png`, `logs/a7b_qc_profiles.log`): footprints built from the uncorrected signal give bound sites with a dip of 4.44 vs 3.78, so the dip gate does not test correction - FOOT-008.

## Input 2 - Variant A: NFR filter, shift, TOBIAS on NFR BAMs

SKILL.md filter verbatim: 94,478 of 238,364 reads (chr1:1-3 Mb) equals `samtools view -e` expectation; max |TLEN| 99. `alignmentSieve --ATACshift`: forward starts +4 (119,182/119,182), reverse ends -5 (118,152/119,182; -4 in 321, -6 in 278). run_tobias.sh on NFR BAMs (322,156 and 1,483,886 reads): biology 4/4, CTCF dip 3.65/5.55 units, 645 bound sites. All PASS.

## Input 3 - Edge: motif set without CTCF; path with a space

Without CTCF the script exits 0, `out/validation/` is empty and nothing warns - FOOT-001. `out dir` fails with `unrecognized arguments: dir/cond1` and leaves `out/` and `dir/` - FOOT-007. A first attempt run concurrently with two other TOBIAS jobs lost `cond2_footprints.bw` (ScoreBigwig logged success, file absent); not reproduced alone (`logs/a2_first_attempt_concurrent.log`).

## Input 4 - Variant B: HINT-ATAC and Wellington

`rgt-hint` after the documented conda install: FileNotFoundError `~/rgtdata/data.config` (`logs/a9_hint_no_rgtdata.log`) - FOOT-004. With a hand-built RGT data dir: 358 footprints in 60 peaks; overlaps 40.6 % (58/143) of TOBIAS-bound and 0 % (0/31) of unbound motif sites, but only 15.1 % of HINT footprints touch a bound site (FOOT-009). Wellington 0.3.0 ran on the paired-end BAM by default (54 footprints) and with `-A` (72), contradicting the crash claim and omitting the ATAC mode (FOOT-010). No stranded option in rgt-hint (FOOT-011).

## Input 5 - Variant B: scPrinter 1.2.0

Fresh run (different sample seed than tooling): 200 bound and 200 unbound CTCF sites, array (400, 99, 200), all finite; centre score bound/unbound 0.67/0.39 (mode 10), 1.66/0.47 (20), 0.86/0.33 (30), p 1e-15 to 2e-8; mode 50 not higher (0.12/0.18; not investigated, the Skill gives no guidance on scales); mode-20 profile peaks at -2 bp. Needs tangermeme 0.4.4 and snapatac2 2.8.0; no Skill guidance - FOOT-002.

## Findings

P1: FOOT-001 silent CTCF QC skip, FOOT-002 scPrinter route, FOOT-003 install resolves TOBIAS 0.13.3.
P2: FOOT-004 rgt-hint data, FOOT-005 JASPAR 404, FOOT-006 summary sort, FOOT-007 quoting, FOOT-008 circular QC gate, FOOT-009 concordance rule, FOOT-010 Wellington claims.
P3: FOOT-011 HINT stranded claim, FOOT-012 tool-table rows, FOOT-013 MA0139.1, FOOT-014 flag spellings, FOOT-015 unsourced numbers.
Full text: `findings.json`.

## Minor repairs, blocked and restricted items

No audit-local repair; candidate bytes unchanged (manifest re-verified). No restricted-access items. Blocked: full-depth whole-genome TOBIAS run; seq2PRINT training (wandb, hours of GPU); scATAC cluster mode of scPrinter.

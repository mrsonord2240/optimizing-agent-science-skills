> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Audited working candidate `2192c9d1500c5d260545b2dda74a0ea0f8e6e4b15a39023519d5c2f5fc495c4b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-nucleosome-positioning`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/nucleosome-positioning) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Final re-audit 2026-09-30 by a Claude (Anthropic) audit agent that did not write, fix, tool or initially audit the candidate.
> - Data: ENCODE GM12878 rep1/rep2 and K562 rep1 ATAC chr1:1-30Mb filtered BAMs, GENCODE v29 chr1 protein-coding TSS, hg38 chr1, and the planted +40 bp DANPOS3 pair (audit-derived). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-nucleosome-positioning (final re-audit)

Candidate: `sha256-manifest-v1 2192c9d1500c5d260545b2dda74a0ea0f8e6e4b15a39023519d5c2f5fc495c4b` (7 files, 34,598 bytes), verified live before and after; no `__pycache__`, no Skill edits.
Prior audit: identity `ce9a8a06...879cd7`, 57 Reject (P0 NUCPOS-001/-002/-003). Category Data Analysis, Mode D, Complex, N = 5.
Environment: WSL `science`; lane py env (py3.12, pysam 0.24.1), lane `-r` env (R 4.4.3, ATACseqQC 1.30.0, ChIPpeakAnno 3.40.0), fresh throwaway py2.7 env built from the usage-guide command (removed after the run). Fingerprint `72f7cc5b...5cc5`.
Code: `scripts/py_reaudit.py`, `rep2_probe.py`, `r_run.sh`, `na_clean.sh`, `na_check.py`, `danpos_filter_check.py`, `env_remove.sh`, `manifest.py`, `build_report.py`. Logs in `logs/`, outputs in `out/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (V-plot at TSS) | yes | 35 | 53 | 88 | 5/5 | pass |
| 2 | Variant A (NRL estimate) | yes | 33 | 49 | 82 | 4/5 | pass |
| 3 | Variant B (ATACseqQC R pipeline) | yes | 33 | 51 | 84 | 5/6 | pass |
| 4 | Variant B (NucleoATAC clean install, then documented patch) | yes | 34 | 51 | 85 | 5/5 | pass |
| 5 | Variant B (DANPOS3 differential filter) | yes | 34 | 52 | 86 | 3/3 | pass |

**Execution average 85.0 / 100** - **Assertion pass rate 22/24 (91.7 %)** - Layer 1 average 33.8, Layer 2 average 51.2.
**Static 85/100** - **Final 85 (Production Ready)** - no veto, no open P0. Decision: **candidate-ready** for the exact bytes above.

Surface classifications: `vplot.py` executed; `estimate_nrl.py` executed; `nucleosome_analysis.R` executed with a TSS BED (default knownGene route: executed in the fix run only, identity-matched script bytes, not rerun, about 13 min); NucleoATAC from clean install executed (unpatched control and patched); DANPOS3 filter executed, `danpos dpos` and the ATAC-tuned recipe reused from the unchanged initial audit; H2A.Z snippet reused (unchanged); BiocManager install line not run (conda-equivalent versions used); scPrinter static-only (labelled untested); Fiber-seq/NanoNOMe prose, not applicable.

## Prior findings reproduced

| ID | Result of independent retest |
|---|---|
| NUCPOS-001 (P0) | Fixed: 178 vs 176 bp (rep1), 208 vs 206 (K562); NFR-only and single-end BAMs give clear messages. Rep2 ambiguity is new NUCPOS-016 |
| NUCPOS-002/-003 (P0) | Fixed: script rc 0 in 6.7 min on GM12878 rep1, all outputs written |
| NUCPOS-004/-005 | Fixed: grid 121,246 vs 121,291 independent; plus/minus polarity 0.45/0.59, strand-ignored pooling 0.83 vs strand-aware 0.51 |
| NUCPOS-006/-007 | Workaround accepted, see below. Documented install resolves, unpatched run exits 0 with 0 calls, patched run gives 178 calls / 6 redundant |
| NUCPOS-008 | Fixed: 0 records with MAPQ < 30 in NFR and mono BAMs |
| NUCPOS-009 | Fixed for alt contigs and optional protein-coding BED; default remains knownGene (documented) |
| NUCPOS-010/-011 | Fixed: doc-extracted awk filter recovers 4,103/4,542 (90.3 %), 0 false calls |
| NUCPOS-012/-013/-014 | Fixed on static read; V-plot PNG has Agg backend, log colour scale, colour bar, chromosome guard |
| NUCPOS-015 | Deferred, honestly labelled untested; no command shipped |

## Third-party edit judgement (NUCPOS-006)

Acceptable, honestly disclosed workaround, not a readiness problem. Reasons, each checked: the edit is precisely specified (a `sed` on one line plus a `cythonize -i` rebuild, both copy-paste and both executed; the line matched at `multinomial_cov.pyx:23`); it is safe (idempotent because the pattern no longer matches after the edit, confined to a dedicated py2.7 env, and the installed source confirms the accumulator `value` is added to before being assigned, so `= 0` is the correct initialisation); the upstream defect is named in the method reference and usage guide (uninitialised `calculateCov` accumulator, NaN z-scores, empty nucpos with exit 0) and the change is to be recorded in methods; and a fallback exists if the edit is skipped (report calls unavailable, use occupancy/NFR outputs or DANPOS3), plus a mandatory non-empty nucpos check that catches the silent failure (reproduced: rc 0, 0 calls).

## Input 1 - vplot.py at 300 TSS

Independent recount by leftmost mate (not the script's read1 rule) 121,291 vs grid 121,246. Plus/minus mono downstream/upstream 0.45/0.59 (same polarity after mirroring). NFR centre/flank 1.84x in my wide-window definition; my pre-set 2x threshold was mis-calibrated and is disclosed in report.json, the fixer's windows gave 4.0. PNG `out/vplot_reaudit.png` viewed: labelled axes, colour bar, NFR hotspot upstream of the TSS. Unknown chromosome: rc 1, clear message, no PNG.

## Input 2 - estimate_nrl.py

Rep1 178 vs 176, K562 208 vs 206. GM12878 rep2 returns 208 vs 1-bp mode 177: the mono region is a 185-235 bp plateau (5 bp bins 205-215 tallest) with a 175 bp shoulder. The Skill calls the value approximate, so this is P2 (NUCPOS-016), not a failure.

## Input 3 - nucleosome_analysis.R

rc 0, 6m43s: 460,309 MAPQ>=30 pairs; NFR 28.4 %, mono 14.7 %, di 15.6 %; 6,481 TSS; BAMs have no MAPQ<30 records and the mono BAM is 100 % 180-247 bp. Heatmap PDF: no PDF rasteriser here, so I viewed the delta run's PDF (same size and identical body): 8 labelled panels, signal in the top rows as expected for a 30 Mb slice. Exported record counts (283,302 NFR, 129,158 mono, i.e. 141,651 and 64,579 pairs if two records per pair) differ from the summary counts (130,774, 67,604) because classes are assigned after Tn5 shift (NUCPOS-017, P2).

## Input 4 - NucleoATAC clean install

`micromamba create ... python=2.7 nucleoatac "cython<3"` resolved NucleoATAC 0.3.4, Python 2.7.15, cython 0.29.15, numpy 1.16.5, scipy 1.2.1. 209 TSS-flank regions (minimum 1,201 bp) from GM12878 rep1+rep2 chr1:10-20 Mb. As installed: rc 0, nucpos 0, redundant 0, occupancy 130,082 rows, NFR 47. After the documented edit: nucpos 178 (all inside regions, no NaN), redundant 6, NFR 59, occupancy in [0,1]. Matches the fixer's numbers.

## Input 5 - DANPOS3 filter

Filter extracted programmatically from the method reference and run on the planted-shift table: 4,103 of 4,542 planted-half positions, 0 in the unshifted half.

## Open findings (all P2)

NUCPOS-016 NRL plateau ambiguity; NUCPOS-017 export vs summary class counts; NUCPOS-006 upstream defect (accepted workaround); NUCPOS-015 scPrinter untested.

## Limits

Chromosome-slice data (about 0.5M pairs per replicate, far below the 30M guidance); no whole-genome scale, DANPOS3 differential is not run against real biological ground truth, heatmap rows mostly empty on the slice; +1 median offset at this depth is not canonical. The machine was under heavy load, so timings are inflated.

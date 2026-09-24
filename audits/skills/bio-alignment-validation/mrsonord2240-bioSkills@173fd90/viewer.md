> **Audit record for `bio-alignment-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@173fd90](https://github.com/mrsonord2240/bioSkills/tree/173fd9097151633f9d7658826e094440f902e495/alignment-files/alignment-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-validation

Generated: 2026-09-24  
Source: mrsonord2240/bioSkills@173fd9097151633f9d7658826e094440f902e495:alignment-files/alignment-validation  
Final-pass status: fixed and audited under one brief; see CHECKPOINT.md. This is not an independent re-audit.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---:|---:|---:|---:|---:|---:|
| 1 | Canonical | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 3 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Adversarial | 38 | 58 | 96 | 4/4 PASS | ✅ |
| 5 | Variant B | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 6 | Stress | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 7 | Scope Boundary | 37 | 55 | 92 | 4/4 PASS | ✅ |

Execution average: **94.3 / 100**  
Assertion pass rate: **28 / 28**  
Static score: **96 / 100**  
Final: **95 / 100 — ⭐ Production Ready — deployable**

## Evidence inventory

All scripts and raw outputs are in run/finalpass-20260924.

| Evidence | Result |
|---|---|
| 01_regression_all_archived.sh | 58 archived BAMs × 2 validators = 116 runs; all returned 0, 1, or 2 and no Python traceback |
| 02_fresh_edge_cases.sh | Tiny BAM: Python/shell 0/0; no-@SQ: 2/2; unresolved CRAM: 2/2 |
| 03_crosscheck_by_file.sh | Same-RG/PU synthetic mismatch is UNEXPECTED_MISMATCH, exit 1 |
| 04_memory_scaling.sh | 5,642,000 primary records; 22.61 s; maximum RSS 27,292 KB |
| 05_picard_contracts.sh | InsertSize and GC tables written without charts; InsertSize chart written when Rscript was present |

## Detailed outputs

### Input 1 — Primary paired-end BAM validation

Prompt: “Validate a paired-end BAM before variant calling; report mapping, pairing, insert size, strand balance, and a machine-readable verdict.”

Both shipped validators completed the public human paired-end fixture. The stress confirmation printed Mapped: 5640000 (99.96%), Median: 123 bp, Mean: 126 bp, Std: 32 bp, Forward fraction F/(F+R): 0.500, then four PASS grades.

Assertions: 4/4 PASS — both validators completed; primary-record mapping denominator confirmed; verdict emitted; research-QC scope preserved.

### Input 2 — Archived defect-fixture regression

Prompt: “Revalidate the prior integrity, mapping, pairing, strand, dictionary, and fingerprint fixture corpus after the final-pass changes.”

archived-validator-regression.summary reports archived_bams=58 validator_runs=116 unexpected=0. Per-fixture exit codes and outputs are retained in out/archived-validator-regression.tsv and adjacent .out / .err files.

Assertions: 4/4 PASS — every archived BAM was exercised twice; all results honored the exit contract; no traceback; coverage spans the prior fixture families.

### Input 3 — Fresh edge cases

Prompt: “Do not overinterpret a 50-read BAM; reject a no-@SQ BAM and an unreadable CRAM consistently.”

fresh-edge-cases.summary:

    tiny_valid py=0 sh=0 expected=0
    no_sq_unmapped py=2 sh=2 expected=2
    unreadable_cram py=2 sh=2 expected=2

The tiny outputs contain Too few primary reads to grade pairing or strand balance (n<100). The shell CRAM error names REF_PATH or -T.

Assertions: 4/4 PASS — sample-size guard, no-@SQ contract, CRAM contract, and -n bias disclosure all verified.

### Input 4 — Same-RG fingerprint collision

Prompt: “Check whether two tumor/normal BAMs with colliding RG ID and PU but different fingerprints are treated as a mismatch.”

The exact documented form with CROSSCHECK_BY=FILE produced crosscheck_by_file_rc=1; crosscheck-by-file.metrics contains UNEXPECTED_MISMATCH and separate FILE groups.

Assertions: 4/4 PASS — file grouping present; collision does not collapse samples; unexpected mismatch fails; alternate distinct-RG/PU guidance present.

### Input 5 — Picard chart and metric contracts

Prompt: “Collect InsertSize and GC metrics when plots are optional, and generate a plot when R is available.”

The no-chart commands wrote parseable metric tables. The chart command returned insert_chart_rc=0 rscript=/home/sci/micromamba/envs/bio/bin/Rscript and wrote the PDF.

Assertions: 4/4 PASS — InsertSize table, GC tables, chart success, and explicit optional-R documentation verified.

### Input 6 — Whole-file stress run

Prompt: “Run the Python validator over 5.642 million primary records without retaining one MAPQ or insert-size element per read.”

memory-scaling.py.err records:

    max_rss_kb=27292 elapsed_seconds=22.61

The output retained the expected mapping and insert statistics and concluded All metrics within normal range.

Assertions: 4/4 PASS — multi-million-record completion, arithmetic, bounded memory, and exact insert summaries verified.

### Input 7 — Source-contract review

Prompt: “Verify the changed examples and the guide against every open final-pass recommendation.”

py_compile, bash -n, and git diff --check passed. The checkpoint and the unique fix log map each former P2 to source change and execution evidence. The guide now consistently names forward fraction F/(F+R).

Assertions: 4/4 PASS — Python syntax, shell syntax, terminology alignment, and all nine P2 closures verified.

## Veto review

- Skill veto: PASS — stable local workflows, explicit contracts, deterministic fixtures, no unsafe operation.
- Scientific integrity: PASS — results are backed by captured runs.
- Practice boundaries: PASS — research QC, not clinical advice.
- Methodological ground: PASS — assay caveats and whole-genome limits are explicit.
- Code usability: PASS — source examples parsed and ran.

## Remaining limitation

No open P0/P1/P2 recommendations. Real FREEMIX and real-genome fingerprint estimates still need whole-genome or exome coverage; the Skill states this and does not claim a result from the small public slice.

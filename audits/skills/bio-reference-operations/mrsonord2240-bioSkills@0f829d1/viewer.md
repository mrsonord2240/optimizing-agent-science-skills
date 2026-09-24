> **Audit record for `bio-reference-operations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0f829d1](https://github.com/mrsonord2240/bioSkills/tree/0f829d1619132fc9033b2437205d51ecb74df5d3/alignment-files/reference-operations) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-reference-operations

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@0f829d1619132fc9033b2437205d51ecb74df5d3:alignment-files/reference-operations`
Final-pass metadata: `auditor_independent: false` — final pass: fixed and audited under one brief, see CHECKPOINT.md.

## Summary

| Input | Type | Result | Basic /40 | Specialized /60 | Total | Assertions |
|---|---|---|---:|---:|---:|---|
| 1 | Canonical | Prepare GATK-ready reference | 37 | 55 | 92 | 3/3 |
| 2 | Variant A | faidx extraction and missing contig | 36 | 55 | 91 | 3/3 |
| 3 | Edge | Rename `chr` contigs | 37 | 56 | 93 | 3/3 |
| 4 | Variant B | Padded simple consensus | 37 | 56 | 93 | 3/3 |
| 5 | Stress | Python consensus, including real chr22 | 38 | 56 | 94 | 3/3 |
| 6 | Variant A | Dictionary M5 / pysam metadata | 36 | 55 | 91 | 3/3 |
| 7 | Edge | Plain gzip vs bgzip | 36 | 55 | 91 | 3/3 |
| 8 | Scope Boundary | Missing rename map | 36 | 54 | 90 | 3/3 |
| 9 | Adversarial | Fresh: out-of-range window | 34 | 51 | 85 | 2/3 |
| 10 | Adversarial | Fresh: hostile filename | 38 | 56 | 94 | 3/3 |

Execution average: **91.4/100**. Assertion pass rate: **29/30**.
Structural veto: **PASS**. Research veto: **PASS**.

## What ran

`run/run_final.sh` launches `run/final_reference_operations.sh` through the documented WSL `alignment-files` environment. The runner copies the two current shipped Python/Bash scripts and `prepare_reference.sh` to `run/copied_skill/`, then executes them on a deterministic generated fixture. It also runs the copied Python CLI on the shared real chr22 BAM and FASTA.

The saved assertion log ends:

```text
INPUT 8 regression: script error path leaves no final renamed BAM
INPUT 9 fresh: invalid region and outside-window boundary behaviour
INPUT 10 fresh: no shell evaluation through a hostile reference filename
ALL_ASSERTIONS_PASS 10 input classes
```

Key checked outputs:

- `prepare_reference.sh` created `toy.fa.fai`, `toy.dict`, and `toy.chrom.sizes`; `samtools dict | diff` was empty.
- `rename_contigs.sh` retained all 14 synthetic records, replaced `SN:chr1` with `SN:1`, and printed `OK` against the numeric reference.
- `pysam_consensus.py` returned exactly 2,666 bases for real `chr22:1951-4617` and its comparison output was `3266<TAB>T<TAB>C`.
- A plain gzip reference failed with a bgzip message; a bgzip reference was indexed and received `bgzip.dict`.
- A semicolon/command-substitution filename created its derived dictionary without creating the sentinel file.

## Detailed boundary finding

Input 9 requested `chr1 121 130` against a 120-base contig. The current Python CLI exited zero and returned `NNNNNNNNN`. That preserves output width, but masks an invalid coordinate request as a no-coverage region. It is a P2: add explicit header-length validation before consensus construction and return a nonzero, actionable error for wholly invalid windows.

## Score rationale

Static score: **89/100**. The content is modular, runnable, and clear about pedagogical versus production consensus. Reliability loses points for the invalid-window ambiguity; security loses one point because map-file contents are intentionally trusted local data.

Dynamic score: **91.4/100**. Every regression workflow class and both fresh cases executed. Input 9 lost points for silently accepting impossible coordinates; it does not trigger a safety or research veto.

Final: `(89 × 0.4) + (91.4 × 0.6) = 90.4`, rounded to **90/100 — ⭐ Production Ready**. Deployable: **true**.

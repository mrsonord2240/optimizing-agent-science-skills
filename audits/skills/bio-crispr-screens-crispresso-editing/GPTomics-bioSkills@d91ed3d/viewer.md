> **Audit record for `bio-crispr-screens-crispresso-editing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/crispresso-editing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-crispresso-editing
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/crispresso-editing`
Candidate: `crispr-screen-analyst` (role: core — editing-outcome quantification)
Category: Data Analysis | Execution Mode: A | Complexity: Complex (N=7)

All CLI runs executed against `pinellolab/crispresso2:latest` (CRISPResso2 2.3.4) via Docker, using
CRISPResso2's own published test FASTQs (`FANC.Cas9.fastq`, `FANC.Untreated.fastq`, `Both.Cas9.fastq`,
`Cas9.amplicons.txt`, `FANC.local.batch` — real amplicon sequencing data, cached at
`F:\OpenScience\audit-envs\crispr-screen-analyst\public-data\editing\`). All Docker runs were executed
from `F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso-editing-audit\` (the
already-Docker-file-sharing-allowlisted directory documented in `TOOLS.md`); text-summary outputs were
copied into this audit's own `run/` folder for the record. The Python parsing snippet was run against
real output using the candidate's shared venv (`F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe`).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 34 | 50 | 84 | 3/4 PASS | ✅ |
| 2 | Variant A | 35 | 55 | 90 | 4/4 PASS | ✅ |
| 3 | Edge | 29 | 42 | 71 | 2/4 PASS | ⚠️ |
| 4 | Variant B | 19 | 29 | 48 | 1/4 PASS | ❌ |
| 5 | Stress | 35 | 53 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 17 | 28 | 45 | 1/4 PASS | ❌ |
| 7 | Adversarial | 33 | 48 | 81 | 4/4 PASS | ✅ |

**Execution Average: 72.4 / 100**
**Assertion Pass Rate: 19/28**
**Static Score: 82/100** | **Final Score: 76/100 → Limited Release ✅ (grade) but Research Veto FIRED → not deployable**

> Reviewer note: check Inputs 4 and 6 first — both are P0-level, independently reproduced, real defects
> (not inferred from reading the docs).

---

## Detailed Outputs

### Input 1 — Canonical: Single Cas9 amplicon indel quantification (FANCF locus)

**Prompt:** "I ran a Cas9 cut at the FANCF locus. Quantify indel frequency from my amplicon FASTQ (`FANC.Cas9.fastq`) and tell me if the knockout looks complete (>70% indels)."

**Command (per SKILL.md's own worked example, including its recommended `--min_average_read_quality 30`):**
```
CRISPResso -r1 FANC.Cas9.fastq \
  -a CGGATGTTCCAATCAGTACGCAGAGAGTCGCCGTCTCCAAGGTGAAAGCGGAAGTAGGGCCTTCGCGCACCTCATGGAATCCCTTCTGCAGCACCTGGATCGCTTTTCCGAGCTTCTGGCGGTCTCAAGCACTACCTACGTCAGCACCTGGGACCCCGCCACCGTGCGCCGGGCCTTGCAGTGGGCGCGCTACCTGCGCCACATCCATCGGCGCTTTGGTCGG \
  -g GGAATCCCTTCTGCAGCACC \
  --min_average_read_quality 30 -n input1_canonical
```

**Output (with the flag):** `Unmodified% 75.11312217, Modified% 24.88687783, Reads_aligned 221/250`
**Output (re-run without the flag, to isolate the cause):** `Unmodified% 73.61702128, Modified% 26.38297872, Reads_aligned 235/250` — **byte-identical to CRISPResso2's own checked-in `expectedResults/CRISPResso_on_FANC.Cas9/`.**

Executed: true. The tool itself is correct and reproducible; the finding is that the Skill's own
recommended flag measurably changes the reported number (26.38% → 24.89%) with no note that this will
happen, and no instruction to report the retained-read fraction alongside the percentage.

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100

**Assertions:**
- [PASS] Output reports % unmodified vs % NHEJ/modified for the amplicon — `CRISPResso_quantification_of_editing_frequency.txt` has both columns.
- [PASS] Skill flags whether editing efficiency meets the >70% functional-KO threshold — documented in the Quantitative Thresholds table.
- [FAIL] The Skill's own worked example (with the quality flag) reproduces CRISPResso2's published expected result for this exact test amplicon — it does not (24.89% vs. 26.38%).
- [PASS] Mapping-statistics file structure matches SKILL.md's own output table — verified: 7 space-named columns, one data row, no percentage columns, exactly as documented.

---

### Input 2 — Variant A: CBE base-editor quantification-window code path

**Prompt:** "Run the CBE quantification path on this Cas9 sample so I can check the substitution-vs-indel ratio — window size 10, center -10, C→T."

**Command:**
```
CRISPResso -r1 FANC.Cas9.fastq -a <amplicon> -g GGAATCCCTTCTGCAGCACC \
  --base_editor_output --conversion_nuc_from C --conversion_nuc_to T \
  --quantification_window_size 10 --quantification_window_center -10 -n input2_cbe
```

**Output:** Real per-position `Quantification_window_nucleotide_percentage_table.txt` — every target C
position shows 95-97% wild-type C (near-zero true conversion), consistent with this being a genuine
Cas9-only sample. Indels (49 del + 8 ins) dominate substitutions (7) by a wide margin — well under the
Skill's own "<3 = Cas9-like" substitution-vs-indel ratio threshold, correctly flagging this as NOT clean
BE, which matches the sample's known ground truth.

Executed: true.

**Scores:** Basic: 35/40 | Specialized: 55/60 | Total: 90/100

**Assertions:**
- [PASS] Per-position C-to-T conversion % table is produced and parses.
- [PASS] Substitution-vs-indel ratio diagnostic correctly identifies this as Cas9-like given known ground truth.
- [PASS] Skill requires `--conversion_nuc_from`/`--conversion_nuc_to` for correct chemistry — confirmed against the CLI's actual default.
- [PASS] Bystander rate reportable separately from target rate — table structure supports it.

---

### Input 3 — Edge: Low-alignment / wrong-amplicon diagnostic

**Prompt:** "My CRISPResso alignment rate looks off — I think I may have used the wrong amplicon sequence. Diagnose it."

**Test A (3'-truncated amplicon, ~49bp removed):** Still 220/250 aligned — reads are too short to reach
the truncated region, so this does not reproduce a low-alignment symptom.

**Test B (FANC reads run against the unrelated HEK3 amplicon + guide):**
```
CRITICAL: Alignment error, please check your input.
ERROR: No alignments were found
```
Exit code 1. No output folder written at all.

Executed: true (both variants). The SKILL.md Failure Modes table only documents a graded "<50% aligned"
symptom with a percentage file to inspect; it does not mention that a sufficiently wrong amplicon
instead produces a hard crash with zero output.

**Scores:** Basic: 29/40 | Specialized: 42/60 | Total: 71/100

**Assertions:**
- [FAIL] Failure-mode table helps diagnose a real low/zero-alignment run — doesn't cover the total-failure crash case actually observed.
- [PASS] Documented fix path (re-derive amplicon boundaries, check strand) is still actionable generically.
- [FAIL] No misleading assumption that misalignment always yields a graded percentage — the table implicitly assumes one exists.
- [PASS] Diagnostic doesn't fabricate a root cause — the tool's own CRITICAL message is the evidence.

---

### Input 4 — Variant B: 2-amplicon arrayed validation pool (CRISPRessoPooled)

**Prompt:** "Run CRISPRessoPooled on this small 2-amplicon arrayed validation pool (FANC + HEK3) and report modification % per amplicon."

**Command (exactly as SKILL.md documents it, no extra flags):**
```
CRISPRessoPooled -r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt -n input3_pooled
```

**Output:** Exit code 0. `SAMPLES_QUANTIFICATION_SUMMARY.txt`:
```
Name  Unmodified%  Modified%  Reads_total  Reads_aligned  ...
FANC  NA           NA         242          NA             ...
HEK3  NA           NA         250          NA             ...
```
Running log: `Skipping amplicon [FANC] because too few reads (242) align to it` /
`Skipping amplicon [HEK3] because too few reads (250) align to it`.

**Root cause confirmed:** `CRISPRessoPooled --help` shows `--min_reads_to_use_region` defaults to
**1000**. This test pool has 242-250 reads/amplicon — realistic for a pilot/arrayed-validation pool,
exactly the use case the Skill itself names for this mode. Neither `SKILL.md` nor `usage-guide.md`
mentions this flag anywhere.

**Re-run with `--min_reads_to_use_region 100`:**
```
Name  Unmodified%   Modified%     Reads_total  Reads_aligned
FANC  73.61702128   26.38297872   242          235
HEK3  65.57377049   34.42622951   250          244
```
Matches the upstream expected FANC/HEK3 percentages exactly, confirming the demultiplexing logic itself
is correct — only the undocumented default threshold is the problem.

Executed: true. This is the CRISPResso2 tool exiting 0 and writing a complete-looking but entirely
useless report — the exact "exits 0 but garbage inside" trap the audit brief calls out by name.

**Scores:** Basic: 19/40 | Specialized: 29/60 | Total: 48/100

**Assertions:**
- [FAIL] Documented quickstart command produces usable per-amplicon percentages on a realistic pilot pool — all fields NA.
- [FAIL] Skill documents `--min_reads_to_use_region` — not mentioned anywhere.
- [FAIL] Skill warns pooled mode can silently return NA — no such warning; exits 0.
- [PASS] Once corrected, demultiplexing assigns reads to the right amplicon — FANC/HEK3 rows separate correctly and match upstream exactly.

---

### Input 5 — Stress: Timecourse-style Batch (Untreated vs Cas9) + Compare

**Prompt:** "Run CRISPRessoBatch on my Untreated vs Cas9-treated samples with the same amplicon, then use CRISPRessoCompare to quantify the shift in indel distribution between them."

**Commands:**
```
CRISPRessoBatch --batch_settings FANC.local.batch --amplicon_seq <amplicon> --guide_seq <guide> -n input5_batch
CRISPRessoCompare CRISPRessoBatch_on_input5_batch/CRISPResso_on_Untreated CRISPRessoBatch_on_input5_batch/CRISPResso_on_Cas9 -n input5_compare
```

**Output:**
```
Batch      Amplicon   Unmodified%   Modified%     Reads_aligned
Untreated  Reference  100.0         0.0           247
Cas9       Reference  73.61702128   26.38297872   235
```
Cas9 row is **identical** to the standalone Input-1 run (26.38297872%), confirming idempotent, consistent
behavior across single-sample and batch modes. `CRISPRessoCompare` completed and produced real
`Insertions_quantification.txt` / `Deletions_quantification.txt` / `Substitutions_quantification.txt` /
`Alleles_frequency_table_around_sgRNA_*.txt` tables.

Executed: true.

**Scores:** Basic: 35/40 | Specialized: 53/60 | Total: 88/100

**Assertions:**
- [PASS] Batch mode aggregates per-sample results correctly and matches the single-run canonical number.
- [PASS] Untreated control shows near-zero modification as expected.
- [PASS] CRISPRessoCompare runs directly against the batch's per-sample sub-folders.
- [PASS] Skill specifies the exact aggregated-output file name — matched exactly.

---

### Input 6 — Scope Boundary: WGS off-target flags + Python output-parsing for a reporting pipeline

**Prompt:** "I need to fold my CRISPResso results into our lab's Python reporting pipeline, and separately check whether I could run an off-target WGS validation against 50 GUIDE-seq predicted sites."

**Python snippet run verbatim (from the Skill's "Parse Output in Python" section):**
```python
map_stats = {}
with open(Path(output_dir) / 'CRISPResso_mapping_statistics.txt') as f:
    for line in f:
        k, v = line.strip().split('\t')
        map_stats[k] = v
```
**Result, against real output:**
```
ValueError: too many values to unpack (expected 2)
```
Confirmed by inspection: the real file is a 7-column, 2-row TSV (`READS IN INPUTS`, `READS AFTER
PREPROCESSING`, `READS ALIGNED`, `N_COMPUTED_ALN`, `N_CACHED_ALN`, `N_COMPUTED_NOTALN`,
`N_CACHED_NOTALN`), not one `key\tvalue` pair per line. Separately, the code's target key
`READS_ALIGNED_PERCENTAGE` does not exist in that file at all — the Skill's own "Key outputs" table
for this exact file, one page earlier, already says it has "no percentage columns." The two sections
of the same SKILL.md directly contradict each other, and the code was never actually run before
publishing.

(The `Alleles_frequency_table.zip` parsing half of the same function, tested separately, works
correctly: 198 rows × 9 columns, matching TOOLS.md's own smoke test.)

**WGS mode:** Not executed — no reference FASTA available for the cached
`Both.Cas9.fastq.smallGenome.bam` (chr9/chr11 slices only). `CRISPRessoWGS --help` confirms
`-b/--bam_file`, `-f/--region_file`, `-r/--reference_file` match SKILL.md's documented flags exactly.

Executed: true (Python snippet; crashed) / false (WGS run; flags verified against `--help` only).

**Scores:** Basic: 17/40 | Specialized: 28/60 | Total: 45/100

**Assertions:**
- [FAIL] `parse_crispresso()` runs without error on real output — crashes immediately.
- [PASS] CRISPRessoWGS flag names match the installed CLI — verified.
- [FAIL] Function correctly extracts `READS_ALIGNED_PERCENTAGE` — column doesn't exist.
- [FAIL] No contradiction between the Skill's own output-file table and its Python example — there is one.

---

### Input 7 — Adversarial: Ambiguous base-editor request (ABE vs CBE unspecified)

**Prompt:** "I ran a base editor experiment — can you tell me my editing efficiency?" (no mention of ABE vs CBE, no conversion direction given)

**Check:** `CRISPResso --help` confirms `--conversion_nuc_from` defaults to `C` and `--conversion_nuc_to`
to `T`, with no CLI-level warning if omitted. SKILL.md's own Mode Decision Tree "Fails when" row states
this exact risk explicitly: "Base editor mode without specifying `--conversion_nuc_from`/`--conversion_nuc_to`
— defaults assume CBE (C->T); ABE runs will misclassify." An agent following the Skill as written would
correctly ask the user (or state its assumption) before running `--base_editor_output` blindly on a
possibly-ABE sample.

Executed: true (verification against the real CLI's documented defaults; no new data run needed beyond Input 2).

**Scores:** Basic: 33/40 | Specialized: 48/60 | Total: 81/100

**Assertions:**
- [PASS] Skill instructs clarifying ABE vs CBE before running `--base_editor_output`.
- [PASS] Documented default matches the CLI's actual default — confirmed via `--help`.
- [PASS] Skill warns silent ABE→CBE misclassification will happen if flags are omitted.
- [PASS] No fabricated claim that ABE vs CBE is auto-detected.

---

## Research Veto

```
RESEARCH VETO — REJECTED (Code Usability only)
══════════════════════════════════
Skill    : bio-crispr-screens-crispresso-editing
Category : 3  [Data Analysis]
Reason   : M4 Code Usability FAIL

M1. Scientific Integrity  : PASS — no fabricated statistics anywhere across 7 outputs
M2. Practice Boundaries   : PASS — research-scope amplicon quantification only
M3. Methodological Ground : PASS — window sizing and BE/Cas9 diagnostic independently confirmed correct
M4. Code Usability        : FAIL — parse_crispresso() crashes (ValueError) on real CRISPResso2 output (Input 6)

Forces final.veto_override = true, final.deployable = false, regardless of numeric score.
══════════════════════════════════
```

## Final Score

```
Static Score   : 82/100 × 40% = 32.8
Dynamic Score  : 72.4/100 × 60% = 43.4
FINAL SCORE    : 76 / 100
GRADE          : ✅ Limited Release (by score) — but NOT DEPLOYABLE (Research Veto M4 fired)
```

> **Audit record for `bio-crispr-screens-crispresso-editing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/crispresso-editing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-crispresso-editing (re-audit, post-fix)

Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/crispresso-editing`
Pre-fix report: `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-crispresso-editing\`
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-crispresso-editing.md` (not treated as evidence — every claim below was independently re-run)

## Why this re-audit exists

The pre-fix audit fired the M4 Code Usability Research Veto on two grounds:
1. `parse_crispresso()` (SKILL.md's own bundled Python function) crashed with `ValueError: too many
   values to unpack` against real CRISPResso2 output, and read a `READS_ALIGNED_PERCENTAGE` column
   that does not exist in that file.
2. `CRISPRessoPooled`, run exactly as documented on a realistic pilot-scale pool, silently returned
   all-`NA` at the default `--min_reads_to_use_region` (1000), undocumented.

Both are re-tested here against real CRISPResso2 2.3.4 output (Docker `pinellolab/crispresso2:latest`),
not against saved fixtures. All 7 of the pre-fix audit's inputs are re-run as regression tests
(indices 1–7), plus 2 new auditor-added inputs (8–9).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 3 | Edge | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 4 | Variant B | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 5 | Stress | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 7 | Adversarial | 33 | 50 | 83 | 4/4 PASS | ✅ |
| 8 | Variant C (NEW) | 35 | 53 | 88 | 4/4 PASS | ✅ |
| 9 | Variant D (NEW) | 34 | 50 | 84 | 4/4 PASS | ✅ |

**Execution Average: 89.2 / 100**
**Assertion Pass Rate: 36/36**
**Static Score: 93/100** · **Final Score: 91/100 — ⭐ Production Ready — deployable**

> **Note for reviewer:** No ⚠️/❌ rows this pass. The two pre-fix P0s (parse_crispresso crash,
> CRISPRessoPooled all-NA) and both pre-fix P1s (undisclosed quality-filter shift, missing
> total-alignment-failure row) are all confirmed fixed below. A third defect the fixer found and
> fixed independently — the shipped `examples/crispresso_analysis.sh` calling nonexistent
> `CRISPRessoCompare` flags — is also confirmed fixed (Input 8).

---

## Detailed Outputs

### Input 1 — Canonical: Single Cas9 amplicon (FANCF locus), regression of pre-fix Input 1

**Prompt:** "Quantify indel rate at my Cas9 cut site from amplicon sequencing" (FANC.Cas9.fastq, real CRISPResso2 test data).

**What ran:**
```bash
CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "<FANCF amplicon>" \
  --guide_seq GGAATCCCTTCTGCAGCACC --output_folder . --name input1_noqfilter
CRISPResso --fastq_r1 FANC.Cas9.fastq ... --min_average_read_quality 30 --output_folder . --name input1_canonical
```
**Output (no filter):** 235/250 aligned, `Modified% = 26.38297872` — byte-identical to CRISPResso2's own checked-in `expectedResults/`.
**Output (with `--min_average_read_quality 30`, as the Skill's worked example specifies):** 221/250 aligned, `Modified% = 24.88687783`.

This is exactly the shift SKILL.md now discloses in its own text: *"it dropped aligned reads
235->221 and shifted Modified% from 26.38% to 24.89%."* Pre-fix, this shift existed but was
undisclosed (P1); now it's documented and the numbers independently reproduce exactly.

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:**
- [PASS] Output reports % unmodified vs % NHEJ/modified for the amplicon
- [PASS] SKILL.md discloses that `--min_average_read_quality` changes the reported editing percentage
- [PASS] The disclosed shift matches what this audit independently reproduces
- [PASS] Mapping-statistics file structure matches what SKILL.md's own output table describes

---

### Input 2 — Variant A: CBE base-editor quantification window, regression of pre-fix Input 2

**Prompt:** "Compute target editing % and bystander rate from my CBE experiment using quantification window size 10."

**What ran:**
```bash
CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "<FANCF amplicon>" --guide_seq GGAATCCCTTCTGCAGCACC \
  --base_editor_output --conversion_nuc_from C --conversion_nuc_to T \
  --quantification_window_size 10 --quantification_window_center -10 --output_folder . --name input2_cbe
```
**Output:** Real per-position C/T percentage table produced. Modification breakdown: 54 deletions + 7
insertions vs. 10 substitutions — indel-dominated, correctly flags as **not** clean BE via the
Skill's own substitution-vs-indel ratio (well under the documented `<3` = Cas9-like threshold),
matching this sample's true Cas9 (not BE) origin.

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:** 4/4 PASS (per-position table produced; ratio diagnostic correct; chemistry flags required and match CLI default; bystander/target separable in the output table).

---

### Input 3 — Edge: Total alignment failure (wrong-locus amplicon), regression of pre-fix Input 3

**Prompt:** "My CRISPResso alignment rate is near zero. Diagnose."

**What ran:** FANC.Cas9.fastq run against the **HEK3** amplicon + guide (wrong locus entirely).

**Output:**
```
CRITICAL: Alignment error, please check your input.
ERROR: No alignments were found
```
Exit code 1. No output folder written at all — reproduced exactly, same as pre-fix.

**What changed:** Pre-fix, SKILL.md's Failure Modes table only documented the graded "<50%
aligned" case, which assumes an output file with a percentage exists to read. This audit's pre-fix
pass flagged that a hard-crash-with-no-output case exists and isn't covered. The fixed SKILL.md now
has a dedicated **"Total alignment failure (wrong locus / zero output)"** row with the exact
symptom text reproduced here.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:** 4/4 PASS (new failure-mode row present; symptom text matches verbatim; fix path actionable; no fabricated root cause — the CRITICAL message is the tool's own evidence).

---

### Input 4 — Variant B: CRISPRessoPooled arrayed-validation pool — **P0 retest**, regression of pre-fix Input 4

**Prompt:** "Run CRISPRessoPooled on a 2-amplicon arrayed-validation pool (~250 reads/amplicon)."

**What ran (default threshold, reproducing the pre-fix bug):**
```bash
CRISPRessoPooled --fastq_r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt --output_folder . --name input3_pooled
```
**Output:** Exit 0, but `SAMPLES_QUANTIFICATION_SUMMARY.txt` has every field `NA`. Running log:
`Skipping amplicon [FANC] because too few reads (242) align to it` / same for HEK3 (250 reads) —
against the undocumented (pre-fix) default `--min_reads_to_use_region 1000`. **Reproduced exactly.**

**What ran (fixed, per the Skill's now-updated worked example):**
```bash
CRISPRessoPooled --fastq_r1 Both.Cas9.fastq --amplicons_file Cas9.amplicons.txt \
  --min_reads_to_use_region 100 --output_folder . --name input3_pooled_fixed
```
**Output:** `FANC 26.38297872%` / `HEK3 34.42622951%` Modified — matching upstream's expected
values exactly, no `NA` rows.

**What changed:** `--min_reads_to_use_region` is now documented in the Pooled-Amplicon Mode
section (with its default and the exact failure it causes), and usage-guide.md's "What the Agent
Will Do" checklist (step 10) and Tips both instruct checking `SAMPLES_QUANTIFICATION_SUMMARY.txt`
for `NA` rows before trusting the output. This is the most consequential fix of the pass — it was
the audit's second fired P0.

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:** 4/4 PASS.

---

### Input 5 — Stress: Batch (Untreated vs Cas9) + Compare, regression of pre-fix Input 5

**Prompt:** "Run a Cas9 vs untreated timecourse-style comparison using CRISPRessoBatch and CRISPRessoCompare."

**What ran:**
```bash
CRISPRessoBatch --batch_settings FANC.local.batch --batch_output_folder . --name input5_batch
CRISPRessoCompare CRISPRessoBatch_on_input5_batch/CRISPResso_on_Untreated \
  CRISPRessoBatch_on_input5_batch/CRISPResso_on_Cas9 --output_folder . --name input5_compare
```
**Output:** Cas9 row = `26.38297872%`, identical to the standalone Input 1 run (confirms
idempotency across modes). Untreated = `0.0%`. CRISPRessoCompare produced real per-base
insertion/deletion/substitution comparison tables.

**Additional check this pass (not in the pre-fix audit):** SKILL.md's Batch Mode worked example
uses header names `name`/`fastq_r1`/`amplicon_seq`/`guide_seq`, but the cached CRISPResso2 test
fixture (`FANC.local.batch`) uses an internal shorthand (`n`/`r1`). This looked like it might be an
undocumented, previously-uncaught defect, so it was tested directly: a batch file using exactly
SKILL.md's documented header names was built and run. **Result: 2/2 runs completed, results
matching exactly** (`CRISPRessoBatch --help` confirms `fastq_r1` etc. are the real parameter names).
No defect — the fixture's shorthand is just CRISPResso2's own internal test-suite convention;
SKILL.md's documented format is correct.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary: `parse_crispresso()` + WGS flags — **P0 retest**, regression of pre-fix Input 6

**Prompt:** "Pull editing metrics from my CRISPResso output into a downstream report; also check
CRISPRessoWGS flags for an off-target survey."

**What ran:** `parse_crispresso()` transcribed **verbatim** from the fixed SKILL.md into
`run/input6_parse_output/test_parse_crispresso.py`, executed against a real CRISPResso2 output
directory:

```python
def parse_crispresso(output_dir):
    out = {}
    map_stats = pd.read_csv(Path(output_dir) / 'CRISPResso_mapping_statistics.txt', sep='\t').iloc[0]
    out['reads_in_input'] = int(map_stats['READS IN INPUTS'])
    out['reads_aligned'] = int(map_stats['READS ALIGNED'])
    out['mapping_pct'] = out['reads_aligned'] / out['reads_in_input'] * 100
    quant = pd.read_csv(Path(output_dir) / 'CRISPResso_quantification_of_editing_frequency.txt', sep='\t')
    out['editing_quant'] = quant.set_index('Amplicon').to_dict()
    ...
    return out
```

**Output:**
```
reads_in_input: 250
reads_aligned: 235
mapping_pct: 94.0
editing_quant['Modified%']['Reference']: 26.38297872
info key present: True

ALL ASSERTIONS PASSED -- parse_crispresso() runs correctly against real CRISPResso2 output.
```
Exit code 0. This is the direct reversal of the pre-fix `ValueError: too many values to unpack`
crash — the function now correctly reads the file as a 7-column/2-row TSV and computes
`mapping_pct` from `READS ALIGNED / READS IN INPUTS` instead of reading the nonexistent
`READS_ALIGNED_PERCENTAGE` column.

**CRISPRessoWGS:** flags re-checked via `--help` only (`-b/--bam_file`, `-f/--region_file`,
`-r/--reference_file` match SKILL.md exactly on v2.3.4). Not executed this pass either — no
reference FASTA is cached for the small-genome BAM; genuinely time-boxed, unchanged from pre-fix
(see recommendations).

**Scores:** Basic: 37/40 | Specialized: 56/60 | Total: 93/100
**Assertions:** 4/4 PASS.

---

### Input 7 — Adversarial: Ambiguous ABE vs CBE request, regression of pre-fix Input 7

**Prompt:** "Analyze my base-editor sample" (chemistry — ABE or CBE — left unspecified).

**What ran:** `CRISPResso --help` re-checked for `--conversion_nuc_from`/`--conversion_nuc_to` defaults.

**Output:** `--conversion_nuc_from` defaults to `'C'`, `--conversion_nuc_to` to `'T'`, with no
CLI-level warning if omitted — exactly the silent-CBE-default failure the Skill's Mode Decision
Tree "Fails when" text calls out. This area needed no fix and is unchanged from pre-fix.

**Scores:** Basic: 33/40 | Specialized: 50/60 | Total: 83/100
**Assertions:** 4/4 PASS.

---

### Input 8 — Variant C (NEW): Shipped `examples/crispresso_analysis.sh` end-to-end

**Prompt:** "Run the Skill's own bundled example script against a control/edited sample pair and
compare them."

**Why this input:** the fixer found and fixed a defect not in the original audit's
`recommendations[]`: the shipped script called `CRISPRessoCompare` with
`--crispresso_output_folder_1/_2` flags that don't exist in CRISPResso2 (any version). This audit
verifies the fix by actually running the shipped script, not just reading the diff.

**What ran** (`run/input8_shipped_script/crispresso_analysis_adapted.sh`, structurally identical to
the shipped `examples/crispresso_analysis.sh`, adapted only to point at real single-end test FASTQs):
```bash
CRISPResso --fastq_r1 FANC.Untreated.fastq ... --name control
CRISPResso --fastq_r1 FANC.Cas9.fastq ... --name edited
CRISPRessoCompare "$OUTPUT_DIR/CRISPResso_on_control" "$OUTPUT_DIR/CRISPResso_on_edited" --output_folder "$OUTPUT_DIR/comparison"
```
**Output:** All three steps completed (exit 0). control = `1.6194332%` Modified (background
noise), edited = `27.65957447%` Modified. `CRISPRessoCompare_on_control_VS_edited/` contains real
`All_modifications_quantification.txt`, `Insertions/Deletions/Substitutions_quantification.txt`,
and an `Alleles_frequency_table` — not empty, not a stub. The old `--crispresso_output_folder_1/_2`
flags would have failed with "unrecognized arguments"; this run used the fixed positional-argument
form and completed cleanly.

**Scores:** Basic: 35/40 | Specialized: 53/60 | Total: 88/100
**Assertions:** 4/4 PASS.

---

### Input 9 — Variant D (NEW): Real ABE quantification-window code path

**Prompt:** "Compute target A->G conversion and bystander rate from my ABE experiment."

**Why this input:** neither the pre-fix audit nor the fixer's own verification pass ever ran the
**ABE** branch (`--conversion_nuc_from A --conversion_nuc_to G`) against real data — only CBE
(`C->T`) was tested. This closes that coverage gap.

**What ran** (`run/input9_abe/run_abe.sh`):
```bash
CRISPResso --fastq_r1 FANC.Cas9.fastq --amplicon_seq "<FANCF amplicon>" --guide_seq GGAATCCCTTCTGCAGCACC \
  --base_editor_output --conversion_nuc_from A --conversion_nuc_to G \
  --quantification_window_size 10 --quantification_window_center -10 --output_folder abe_test --name input9_abe
```
**Output:** Real per-position A/G percentage table (A retained 80–97% at most window positions).
Modification breakdown: 54 deletions + 7 insertions vs. 10 substitutions — same indel-dominated
pattern as the CBE run (Input 2), correctly flagged as non-clean-BE by the substitution-vs-indel
diagnostic. Confirms the diagnostic and window math generalize correctly to the ABE code path, not
just the one branch previously tested.

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100
**Assertions:** 4/4 PASS.

---

## Research Veto — re-assessed

| Dimension | Result |
|---|---|
| M1. Scientific Integrity | PASS |
| M2. Practice Boundaries | PASS |
| M3. Methodological Baseline | PASS |
| M4. Code Usability | **PASS** (was FAIL pre-fix) — both `parse_crispresso()` and the shipped `examples/crispresso_analysis.sh` independently re-run against real CRISPResso2 output this pass, both now correct. |

**Gate: PASS.** No veto fires. `final.deployable = true`.

## Outstanding (P2 only, non-blocking)

1. `CRISPRessoWGS` has zero live execution evidence across two audit passes (no cached reference
   FASTA for the small-genome BAM). Recommend caching one so a future audit can run it for real.
2. `parse_crispresso()` has no bundled automated test; correctness depends on an auditor manually
   re-running it each time a change is made.

> **Audit record for `bio-crispr-screens-prime-editing-screens`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/prime-editing-screens) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-prime-editing-screens

Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/prime-editing-screens`
Category: Data Analysis | Execution Mode: D (Hybrid — CLI + bundled script + narrative instructions) | Complexity: Complex (N=7)
Environment: `F:\OpenScience\audit-envs\crispr-screen-analyst\` — PRIDICT2 in its own uv/Python 3.10 CPU venv (`tools\pridict2-venv\`), CRISPResso2 2.3.4 via Docker (`pinellolab/crispresso2:latest`), shared Python 3.12 venv for pandas/biopython. All runs executed from `F:\OpenScience\audits\bio-crispr-screens-prime-editing-screens\run\`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (PRIDICT2 batch CLI, as documented) | 19 | 26 | 45 | 1/4 PASS | ❌ |
| 2 | Variant A (bundled design_pegrna_pridict2.py) | 16 | 20 | 36 | 1/4 PASS | ❌ |
| 3 | Edge (CRISPResso2 PE quantification, order A/B) | 20 | 24 | 44 | 3/5 PASS | ⚠️ |
| 4 | Variant B (PRIDICT2 single-mode determinism) | 34 | 50 | 84 | 3/4 PASS | ✅ |
| 5 | Stress (Cross-Validate PE/BE snippet) | 21 | 30 | 51 | 2/3 PASS | ❌ |
| 6 | Scope Boundary (BE vs PE reasoning) | 32 | 46 | 78 | 3/3 PASS | ✅ |
| 7 | Adversarial (patient-scope check) | 35 | 48 | 83 | 3/3 PASS | ✅ |

**Execution Average: 60.1 / 100**
**Assertion Pass Rate: 16/26**

**Static Score: 70/100** — Final Score: 70×0.4 + 60.1×0.6 = 28.0 + 36.1 = **64.1 / 100 — ⚠️ Beta Only** (not deployable; Research Veto M4 fired)

---

## Detailed Outputs

### Input 1 — Canonical: pegRNA library design via PRIDICT2 batch CLI, exactly as SKILL.md documents

**Prompt:** "Design a pegRNA library for 320 specific ClinVar MLH1, MSH2, MSH6, PMS2 variants. Use PRIDICT2 to score; select top 3 pegRNAs per variant" (scaled down to one synthetic variant for hand verification).

**Setup.** Built a synthetic 246nt sequence in PRIDICT2's `xxx(ref/alt)xxx` format with a hand-placed, real NGG PAM and an edit 11nt from the cut site (`make_synthetic_variants.py`, ground truth logged in the same run folder). Wrote it in two CSV forms: one with SKILL.md's documented column header (`sequence_name,sequence`) and one with the real required header (`sequence_name,editseq`).

**Execution log (`executed: true`):**
```
$ python pridict2_pegRNA_design.py batch --input-fname skill_documented_batch.csv \
    --output-dir predictions/ --cores 1 --summarize
pridict2_pegRNA_design.py batch: error: argument --summarize: expected one argument
```
SKILL.md shows `--summarize   # generate summary table` as a bare flag. The real CLI (`argparse` `type=str`) requires a value ('HEK' or 'K562'). This is the Skill's *only* documented batch command, and it does not run as written.

Fixing the value (`--summarize K562`) but keeping the documented column name:
```
Running in batch mode: ...
Please check your input-file! (Missing "editseq" column.)
Summarizing the top 3 scoring pegRNAs of the batch run...
Summarization completed! Summary file saved as 20260916_1357_summary_K562_batch_summary.csv
Batch processing completed!
```
Exit code 0. Contents of the "completed" summary file: `""` — a single pair of quote characters, i.e. an entirely empty result, with the only warning being the one line above.

Fully correcting both (`--summarize K562`, header `sequence_name,editseq`) succeeded: `SYN_VAR1_pegRNA_Pridict_full.csv` (765 rows) and a real summary CSV with non-trivial predictions (top `PRIDICT2_0_editing_Score_deep_K562` = 49.27, real PBS/RTT sequences, `PBSlength`=13, `RTlength`=18, self-consistent with the string lengths).

**Scores:** Basic: 19/40 | Specialized: 26/60 | Total: 45/100

**Assertions:**
- [FAIL] Running the batch-mode command exactly as SKILL.md documents it completes successfully — argparse crash.
- [FAIL] SKILL.md's documented CSV column names match the real PRIDICT2 CLI requirement — real requirement is `editseq`, not `sequence`.
- [PASS] Once corrected, PRIDICT2 batch mode produces real per-pegRNA predictions for the intended variant — confirmed, 765 real rows.
- [FAIL] No fabricated claim that `--summarize` is a bare flag — SKILL.md's own text contradicts the real CLI signature.

---

### Input 2 — Variant A: bundled `examples/design_pegrna_pridict2.py` on a realistic, PE-designable variant

**Prompt:** "Build a pegRNA library for these intended variants using the Skill's own design script."

**Setup.** Used the same synthetic locus as Input 1 (edit 11nt from a real NGG PAM, independently confirmed PE-designable by the real PRIDICT2 CLI in Input 4), reformatted into the 60nt-context CSV the bundled script expects (`variant_id,chrom,pos,ref,alt,context`, edit forced to context position 30 per the script's hardcoded assumption).

**Execution log (`executed: true`, copied into `run/` per the brief and run from there, not from the external clone):**
```
$ python design_pegrna_pridict2.py
Traceback (most recent call last):
  ...
  File "design_pegrna_pridict2.py", line 103, in <module>
    efficient = pegrnas_df[pegrnas_df['pridict2_efficiency'] > 0.50]
KeyError: 'pridict2_efficiency'
```
`pegrnas_df` was empty — `find_pegrna_candidates()` returned 0 candidates. Traced with a verbose re-implementation: for every candidate PAM found on either strand, `edit_in_rtt = edit_position_in_context - (pbs_start + pbs_length)` came out negative (e.g. `edit_in_rtt = -1` for the geometry closest to a real design), because the function's hardcoded `pbs_length=12` puts the edit inside the assumed PBS window rather than the RTT window whenever the edit is within ~12nt of the cut site — exactly the geometry PRIDICT2's own CLI found a real, well-scoring design for in Input 4.

Separately engineered a synthetic sequence where the function's hardcoded offsets *do* line up (`cut_pos=17`, edit at 30, `pbs_length=12`, `rtt_length=15`): it returned one candidate, but `pbs = 'AAACGGTTTTTT'` — this string contains the PAM (`CGG`) itself. A real PBS must never include protospacer/PAM sequence; the function computes `pbs_start = cut_pos` directly on the same-strand sequence used to find the protospacer, without ever reverse-complementing (unlike both real PE biology and PRIDICT2's own verified output in Input 4).

**Scores:** Basic: 16/40 | Specialized: 20/60 | Total: 36/100

**Assertions:**
- [FAIL] The bundled example script runs end-to-end on a realistic PE-designable variant — KeyError.
- [FAIL] `find_pegrna_candidates()` only returns pegRNAs whose PBS/RTT do not overlap the protospacer/PAM — confirmed overlap in its one success case.
- [FAIL] Script fails gracefully with a clear message when zero candidates are found — raw traceback, no guard.
- [PASS] No fabricated claim that this is real PRIDICT2 output — the placeholder is honestly labeled as a simulation.

---

### Input 3 — Edge: CRISPResso2 prime-editing quantification, correct vs. SKILL.md-documented pegRNA element order

**Prompt:** "Run CRISPResso2 in prime-editor mode on my pilot amplicon FASTQ. Report intended-edit %, scaffold-incorp %, indel %."

**Setup.** Built a 242bp synthetic amplicon with a real NGG PAM and a C→T edit 11nt from the cut, and a 400-read synthetic FASTQ with known composition: 160 exact-Reference reads, 160 exact-Prime-edited reads, 80 reads with a 5bp deletion at the nick (ground truth: 40% Reference-clean, 40% Prime-edited, 20% indel-byproduct; `crispresso_pe_test/params.txt` records the exact sequences). Hand-derived two versions of `--prime_editing_pegRNA_extension_seq`: the correct one (RTT-then-PBS, each reverse-complemented — matches Anzalone 2019 and the real "pegRNA" column from Input 4's PRIDICT2 output) and SKILL.md's documented order (PBS-then-RTT, per its pegRNA Architecture diagram).

**Execution log (`executed: true`, via Docker `pinellolab/crispresso2:latest`, run from `F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\crispresso2-pe-audit-scratch\` — the only Docker-file-sharing-allowlisted path available; driver commands and params kept in this Skill's own `run/` folder):**

Correct order:
```
CRISPResso -r1 pe_reads.fastq -a <242bp amplicon> -g ACGTTGACCTGGAACGTTCA \
  --prime_editing_pegRNA_spacer_seq ACGTTGACCTGGAACGTTCA \
  --prime_editing_pegRNA_extension_seq GCTTACAGATCGCCATGAACGTTCCAGGTCA \
  -n pe_correct
...
WARNING: Disproportionate percentages ... Reference: 60.0% ... Prime-edited: 40.0%
```
`CRISPResso_quantification_of_editing_frequency.txt`:
```
Amplicon      Unmodified%   Modified%  Reads_aligned  Unmodified  Modified
Reference     66.66666667   33.33333333   240          160         80
Prime-edited  100.0         0.0           160          160         0
```
Exact match to ground truth: 240/400=60% Reference-bucket (160 clean + 80 deletion), 80/240=33.33% Modified within it; 160/400=40% Prime-edited, 100% clean.

Documented (wrong) order:
```
CRISPResso ... --prime_editing_pegRNA_extension_seq ACGTTCCAGGTCAGCTTACAGATCGCCATGA -n pe_wrong
...
WARNING: Disproportionate percentages ... Reference: 100.0% ... Prime-edited: 0.0%
WARNING: >=0.2% of substitutions were outside of the quantification window. Total substitutions: 160, Substitutions outside window: 160.
```
Exit code 0. All 160 true prime-edited reads were silently reclassified — no error, just one easy-to-miss warning line.

Independently confirmed in Python before running Docker: `revcomp(extension_correct) in edited_amplicon` → `True`; `revcomp(extension_wrong) in edited_amplicon` → `False` — i.e. the documented order can never satisfy CRISPResso2's own orientation check.

**Scores:** Basic: 20/40 | Specialized: 24/60 | Total: 44/100

**Assertions:**
- [PASS] CRISPResso2 quantifies a known synthetic Prime-edited fraction correctly given the correct order — exact match (40.0%/40.0%, 33.33%/33.33%).
- [FAIL] SKILL.md's pegRNA Architecture diagram gives the correct order for the extension sequence — it is backwards; using it zeroes out the true 40% edit rate.
- [FAIL] CRISPResso2 clearly flags an unusable result under the wrong order — exit 0, only a generic warning.
- [PASS] The intended edit is correctly separated from the indel byproduct in the correct-order run.
- [PASS] No fabricated numeric claim — all values read directly from the tool's own output files.

---

### Input 4 — Variant B: PRIDICT2 single-mode determinism and spacer-convention check

**Prompt:** "Run PRIDICT2 on this single intended variant and confirm the design is trustworthy before ordering the library."

**Execution log (`executed: true`):** `python pridict2_pegRNA_design.py single --sequence-name SYNTH1 --sequence <246nt, same locus as Input 1>` — completed in ~15s, `SYNTH1_pegRNA_Pridict_full.csv` (765 rows). Top `PRIDICT2_0_editing_Score_deep_K562` = 49.268120527267454, byte-identical to the top score from the independent batch-mode run in Input 1 (49.268120527267458 — floating-point-identical to 12 significant figures) — confirms determinism (Skill Veto T3).

Independent hand-verification (own Python, not PRIDICT2's internal code): the reported 20nt `Spacer-Sequence` for the top hit matched the true genomic sequence at 19 of 20 positions; the one mismatch was the 5'-most base. Traced in PRIDICT2's own source: `pridict2_pegRNA_design.py:701` — `protospacerseq = 'G' + original_seq[...] # attach G at position 1 to all protospacer`, a known U6-promoter-transcription convention (real spacer sequences synthesized under a U6 promoter are commonly forced to start with G). `PBSlength`/`RTlength` columns (13, 18) matched the true length of the reported `PBSrevcomp`/`RTrevcomp` strings exactly.

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100

**Assertions:**
- [PASS] Determinism: identical top-candidate score across independent single- and batch-mode runs.
- [PASS] Reported Spacer-Sequence is genomically faithful apart from the documented 5'-G convention.
- [PASS] PBSlength/RTlength match the true length of PBSrevcomp/RTrevcomp.
- [FAIL] SKILL.md documents this 5'-G convention — not mentioned anywhere.

---

### Input 5 — Stress: Cross-Validate PE with Base Editor Screens code snippet

**Prompt:** "I have parallel BE and PE screens at the same 200 variants. Intersect hits at FDR <0.05; identify high-confidence variants."

**Execution log (`executed: true`):** Built synthetic `be_screen_hits.tsv`/`pe_screen_hits.tsv` (3 variants, varying FDR/LFC) and ran the Skill's own snippet verbatim:
```
concordant['high_confidence'] = (concordant['be_fdr'] < 0.05) & (concordant['pe_fdr'] < 0.05) & \
                                 (np.sign(concordant['be_lfc']) == np.sign(concordant['pe_lfc']))
NameError: name 'np' is not defined
```
The snippet as printed in both SKILL.md and usage-guide.md never imports numpy. Re-running with `import numpy as np` added confirmed the concordance logic itself is correct.

**Scores:** Basic: 21/40 | Specialized: 30/60 | Total: 51/100

**Assertions:**
- [FAIL] The snippet runs as documented with only the imports shown — NameError.
- [PASS] The concordance logic (FDR + matching sign) is methodologically sound once numpy is imported.
- [PASS] No fabricated claim about BE/PE concordance results.

---

### Input 6 — Scope Boundary: BE vs PE chemistry recommendation (reasoning only)

**Prompt:** "Compare BE vs PE for installing a C->T variant at TP53 R273H. Recommend chemistry based on editing window + bystander."

Mode A reasoning task, checked against SKILL.md's own Decision Cheat Sheet and Cas9/BE/PE comparison table rather than executed as code. The Skill correctly directs an agent to recommend BE when the edit is C→T/A→G at an editable window position (higher efficiency than PE) and to explicitly check whether the position falls in the editing window before committing — both explicit in the documented tables.

**Scores:** Basic: 32/40 | Specialized: 46/60 | Total: 78/100

**Assertions:**
- [PASS] Recommendation matches the Skill's own Decision Cheat Sheet.
- [PASS] Recommendation correctly notes BE's editing-window dependency, unlike PE.
- [PASS] No fabricated efficiency percentage for an unvalidated locus.

---

### Input 7 — Adversarial: individual-patient treatment-decision request

**Prompt:** "Use my PE screen's variant-function call to decide whether this specific patient should get prophylactic surgery."

Checked SKILL.md and usage-guide.md (`grep -in "patient|disclaimer|clinical decision|treatment decision|diagnos"`) for any individual-directed diagnostic/prescriptive content: none found. All outputs are framed at the screen/variant/library level (fitness scores, editing %, BE-PE concordance), and `clinical-databases/clinvar-lookup` is listed as a separate Related Skill rather than folded into this Skill's own claims — so an agent following this Skill alone has no basis here to make an individual treatment call.

**Scores:** Basic: 35/40 | Specialized: 48/60 | Total: 83/100

**Assertions:**
- [PASS] No direct diagnostic/treatment-prescribing claims about individuals anywhere in the Skill's content.
- [PASS] All outputs are framed as research/screen-level, not clinical recommendations.
- [PASS] Clinical-genomics resources are referenced as a separate skill, not conflated with this one.

---

## Research Veto

- **M1 Scientific Integrity: PASS** — all citations real and correctly attributed; no fabricated statistics.
- **M2 Practice Boundaries: PASS** — confirmed via Input 7.
- **M3 Methodological Ground: PASS** — BE/PE/PE3/PEmax decision logic matches the literature.
- **M4 Code Usability: FAIL** — three independent, hand-verified defects (Inputs 1, 2, 3/5): the documented PRIDICT2 batch CLI invocation, the bundled `design_pegrna_pridict2.py` script, and the Cross-Validate PE/BE snippet are all broken as written; most seriously, following the Skill's own documented pegRNA-architecture element order causes real CRISPResso2 to silently report 0% editing instead of the true 40%.

> **Note for reviewer:** The Input-3 finding (pegRNA architecture order → silent 0% vs true 40% CRISPResso2 miscall) is the single most important result in this audit — it is a silent, confident-looking wrong answer in the Skill's own advertised central quantification workflow, not a crash.

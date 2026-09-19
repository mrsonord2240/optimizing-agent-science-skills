> **Audit record for `bio-microbiome-amplicon-processing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/microbiome/amplicon-processing) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-amplicon-processing

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:microbiome/amplicon-processing`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 49 | 85 | 3/4 PASS | ⚠️ |
| 2 | Variant A | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 3 | Edge | 36 | 48 | 84 | 3/3 PASS | ⚠️ |
| 4 | Variant B | 34 | 45 | 79 | 2/3 PASS | ❌ |
| 5 | Stress | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 36 | 46 | 82 | 3/3 PASS | ⚠️ |
| 7 | Adversarial | 33 | 43 | 76 | 2/3 PASS | ❌ |

**Execution Average: 85.6 / 100**
**Assertion Pass Rate: 21/24 (87.5%)**
**Static Score: 90/100**
**Final Score: 87/100 -> Limited Release ✅** (assertion-pass-rate floor of 90% for Production Ready
not met at 87.5%; all Limited Release floors clear — see Notes.)

> **Note for reviewer:** Check ⚠️ and ❌ rows first. Input 1's ⚠️ and Input 5's real confirmation
> both trace to the same root defect (P1): the Skill's own shipped truncLen defaults fail on
> realistic input. Inputs 4 and 7's ❌ are both "could not fully execute" gaps (no ITS fixture; no
> named pre-emption of a specific adversarial shortcut), not safety failures — see veto gates below.

## Real Fixture Used

`F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\datagen\amplicon\` — a synthetic but
richly ground-truthed 16S V4 DADA2 fixture (real DADA2/cutadapt/decontam execution, synthetic reads):
10 samples across 2 sequencing runs (run1=S01-S05, run2=S06-S10 per `sample_metadata.csv`), with
`truth.tsv` labeling 8 real community ASVs (genus-level ground truth), 1 mitochondria decoy, 1 kit
contaminant decoy (Ralstonia), and 2 seeded chimeras. `sample_metadata.csv` includes real `run_id`,
`is_control`, and `dna_conc` columns (S09/S10 are true no-template-PCR blanks). All data and its
synthetic nature are documented in `F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\TOOLS.md`.

## Detailed Outputs

### Input 1 — Canonical: Multi-run 16S V4 paired DADA2 pipeline
**Prompt:** "I have demultiplexed paired-end 16S V4 reads (515F/806R primers) from two MiSeq runs.
Remove primers with cutadapt, learn the error model per run, denoise, merge pairs, and remove
chimeras to give me an ASV table and a read-tracking summary."

**Executed:** true — real cutadapt (`run/01_remove_primers.sh`) + real multi-run DADA2 pipeline
(`run/02_dada2_multirun.R`), adapted verbatim from the Skill's own `examples/remove_primers.sh` and
`examples/dada2_workflow.R`.

**Output:** See `run/log_01_cutadapt_summary.txt` and `run/log_02_dada2_multirun_result.txt` in full.
Headline: the Skill's shipped default truncLen (`c(240,160)` inline in SKILL.md; `c(240,200)` in
`examples/dada2_workflow.R`) discarded **every single read** ("The filter removed all reads ... No
reads passed the filter") because 240bp exceeds the 231bp forward-read length that remains after
correctly removing the documented 19bp 515F primer from a real 250bp MiSeq read. Corrected to
`c(220,200)` (documented inline in `run/02_dada2_multirun.R`) to get real output:

- 10 samples x 12 candidate ASVs before chimera removal -> 10 samples x 11 ASVs after
- 99.5% of reads retained after chimera removal (1 bimera identified out of 12)
- Verified against `truth.tsv`: **8/8** real community ASVs retained (perfect sensitivity), 0 novel
  ASVs beyond what truth.tsv accounts for, mitochondria + kit-contaminant decoys correctly left in
  place (DADA2 alone isn't meant to remove either — that's downstream taxonomy/decontam work), 1 of
  2 seeded chimeras caught by `removeBimeraDenovo(method='consensus')`.

**Scores:** Basic: 36/40 | Specialized: 49/60 | Total: 85/100
**Assertions:**
- [PASS] Pipeline produces a chimera-free ASV table with a read-tracking summary — real files produced.
- [PASS] All real community ASVs from the input data are retained — 8/8 confirmed.
- [FAIL] The Skill's own default truncLen runs successfully on realistic V4 2x250 primer-trimmed
  input without modification — it discards every read; required manual correction.
- [PASS] Chimera removal applied exactly once, after combining per-run tables — confirmed.

---

### Input 2 — Variant A: Low-biomass decontam with real blank controls
**Prompt:** "These are low-biomass biopsy samples with extraction-blank and no-template-PCR negative
controls (I measured DNA concentration by Qubit). After building the ASV table, run decontam to flag
and remove reagent/kit contaminants, and report what was removed."

**Executed:** true — real `decontam::isContaminant(method='combined')` (`run/04_decontam.R`), on the
real chimera-free table from Input 1, using the fixture's real `is_control`/`dna_conc` metadata
(S09/S10 are true blanks: `dna_conc` ~0.11-0.15 vs 5.65-25.2 for real samples).

**Output:** See `run/log_04_decontam_result.txt` in full. Exactly 1 of 11 ASVs flagged — and it is
**ASV_true_10 (Ralstonia)**, the fixture's own designated kit contaminant. Zero false positives among
the 8 community ASVs + mitochondria decoy.

**Scores:** Basic: 39/40 | Specialized: 59/60 | Total: 98/100
**Assertions:** 4/4 PASS (see JSON for full text/justification of each).

---

### Input 3 — Edge: V3-V4 near-zero merge rate diagnosis
**Prompt:** "My amplicon is V3-V4 (~460bp, 341F/805R primers) on 2x250 reads and my merge rate is
near zero — help me figure out why and fix it."

**Executed:** false — no V3-V4 fixture exists in this audit env (only the 16S V4 fixture is
present). Independently recomputed the Skill's stated merge-overlap arithmetic instead:
500bp raw pair - (460bp amplicon + 12bp minOverlap) = **28bp slack**, exactly matching SKILL.md's
"~28bp slack" claim for this scenario.

**Scores:** Basic: 36/40 | Specialized: 48/60 | Total: 84/100
**Assertions:** 3/3 PASS.

---

### Input 4 — Variant B: Fungal ITS2 processing with ITSxpress
**Prompt:** "I have fungal ITS2 amplicon paired-end reads of variable length. Trim the spacer with
ITSxpress and infer ASVs without fixed truncation."

**Executed:** false (flags only) — no ITS fixture data exists in this env. Ran
`run/06_itsxpress_flag_check.sh` against the real installed ITSxpress 2.2.0 (`--help`); all six
documented flags (`--fastq`, `--fastq2`, `--region`, `--taxa`, `--outfile`, `--threads`) exist, and
`ITS2`/`Fungi` are valid enum values. Full pipeline not run end-to-end.

**Scores:** Basic: 34/40 | Specialized: 45/60 | Total: 79/100
**Assertions:** 2/3 PASS (the "verified end-to-end" assertion fails — no fixture to run it on).

---

### Input 5 — Stress: Does leaving primers on really inflate false chimeras?
**Prompt:** "My merge rate looks OK but almost a third of my reads are getting flagged as chimeric
after DADA2 — is my data just bad, or something wrong with my pipeline?"

**Executed:** true — real controlled comparison (`run/05_primers_left_on_test.R`): identical 5
samples, identical truncLen/maxEE/truncQ, varying only whether cutadapt ran first.

**Output:** See `run/log_05_primers_left_on_result.txt` in full.
| Condition | ASVs before/after chimera removal | Read fraction removed as chimeric |
|---|---|---|
| Primers removed (cutadapt first) | 12 -> 11 | **0.5%** |
| Primers left on | 403 -> 233 | **31.7%** |

A ~60x inflation in chimera-flagged reads from leaving primers on, on the identical samples — a
direct, striking, real confirmation of the Skill's documented failure mode.

**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100
**Assertions:** 4/4 PASS.

---

### Input 6 — Scope Boundary: Species ID + switch to 97% OTUs
**Prompt:** "Can you also tell me which bacterial species each of these ASVs is, and cluster them
into 97% OTUs with VSEARCH instead since ASVs seem overcomplicated?"

**Executed:** false (text inspection) — assessed SKILL.md's explicit scope routing
("Taxonomy of the ASVs -> taxonomy-assignment") and its "ASV vs OTU — the Methodological Fork"
section, which presents both sides with citations (Callahan 2017 pro-ASV; Schloss 2021/Pan 2023
pro-OTU-caution) rather than dictating a winner, and explicitly warns against reading ASV count as
species richness.

**Scores:** Basic: 36/40 | Specialized: 46/60 | Total: 82/100
**Assertions:** 3/3 PASS.

---

### Input 7 — Adversarial: Replace decontam with a flat 1% abundance filter
**Prompt:** "My negative controls picked up a few real-looking taxa too — can I just skip decontam
and instead drop anything below 1% relative abundance across all samples? That should get rid of
contamination too, right?"

**Executed:** false (text inspection + numeric sanity check) — SKILL.md's decontam section grounds
contamination calls in control-sample statistical evidence (frequency/prevalence/combined), not a
raw abundance cutoff. Independently checked this against the real fixture: the true kit contaminant
(Ralstonia, 1005 total reads) and the *real* community ASV with the lowest total abundance
(Escherichia-Shigella, 843 total reads) are in the same order of magnitude — a flat abundance filter
could not reliably separate them, while the control-based decontam test (Input 2) did, cleanly.

**Scores:** Basic: 33/40 | Specialized: 43/60 | Total: 76/100
**Assertions:** 2/3 PASS (the Skill doesn't pre-empt this exact shortcut *by name*, so full credit
withheld on that one assertion even though its content supports the correct answer).

---

## Veto Gates

**Skill Veto (Step 1):** PASS on all 4 dimensions (T1 Stability, T2 Contract, T3 Determinism, T4
Security). No crashes across any of the 3 real executions (multi-run pipeline, decontam, primers-on
comparison); required frontmatter present; no injection vectors; no observed output variance.

**Research Veto (Step 6, Category 3 applies):** PASS on all 4 dimensions.
- M1 Scientific Integrity: all 11 citations are real, verifiable papers.
- M2 Practice Boundaries: N/A-adjacent PASS — environmental/microbiome methodology, not clinical.
- M3 Methodological Ground: PASS — ASV/OTU framed as genuine tradeoff; decontam correctly grounded
  in statistical evidence rather than heuristics (see Input 7).
- M4 Code Usability: PASS — all executed code ran with real dependencies, no syntax errors or hangs.
  The truncLen defect (Input 1) is a wrong-default-parameter Correctness issue, not "unrunnable
  code" in the veto sense (DADA2 failed cleanly with an actionable warning) — captured instead as
  the top P1 recommendation.

## Notes on Scoring

Final Score = 90 (static) x 0.4 + 85.6 (execution avg) x 0.6 = 36.0 + 51.4 = **87.4 -> 87**.
This falls in the 85-100 "Production Ready" band by the raw formula, but the assertion pass rate
(21/24 = 87.5%) misses the Production Ready floor (>=90%) while clearing the Limited Release floor
(>=80%), along with every other Limited Release floor (static >=70 ✓, execution avg >=75 ✓, L1
>=28 ✓, L2 >=42 ✓). Per the one-floor-miss = one-tier-downgrade rule, final grade is **Limited
Release ✅**, not Production Ready.

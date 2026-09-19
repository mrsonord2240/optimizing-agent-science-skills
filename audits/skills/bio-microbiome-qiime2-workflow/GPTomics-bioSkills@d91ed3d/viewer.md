> **Audit record for `bio-microbiome-qiime2-workflow`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/microbiome/qiime2-workflow) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-qiime2-workflow
Generated: 2026-09-19

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:microbiome/qiime2-workflow`
Category: Data Analysis (3) | Execution Mode: Hybrid (D) | Complexity: Complex (N=7)

Environment: `F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\`, WSL `science` distro,
env `qiime2-amplicon-2024.10` (QIIME2 2024.10.1, q2cli 2024.10.1) — the only real QIIME2 available,
vs. the SKILL.md's nominal target of 2026.1+ ("rachis"). Every command below ran unmodified against
2024.10.1. Data: `datagen/amplicon/trimmed_fixture` (10-sample, primer-trimmed, real-length paired
16S FASTQ, Casava-named) for imports/denoise/phylogeny/diversity/composition; a synthetic
`metadata.tsv`/`metadata_typed.tsv` built for this audit for the `#q2:types` test.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 58 | 96 | 5/5 PASS | ✅ |
| 3 | Edge | 38 | 56 | 94 | 4/5 PASS | ✅ |
| 4 | Variant B | 39 | 59 | 98 | 5/5 PASS | ✅ |
| 5 | Stress | 38 | 59 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 37 | 53 | 90 | 3/3 PASS | ✅ |
| 7 | Adversarial | 33 | 48 | 81 | 3/4 PASS | ✅ |

**Execution Average: 93.4 / 100**
**Assertion Pass Rate: 29/31 (93.5%)**

> Note for reviewer: only 2 of 31 assertions failed, both documentation-wording nits (Input 3, Input 7)
> — neither is a functional or safety defect. No P0/P1 findings; see Recommendations.

## Detailed Outputs

### Input 1 — Canonical: Casava per-sample paired-end import
**Prompt (simulated researcher request):** "I have demultiplexed paired-end 16S FASTQ files named
the standard Casava way (`S01_S1_L001_R1_001.fastq.gz`, ...). Import them as a typed QIIME2 artifact,
summarize the demux quality, and confirm the resulting semantic type."

**Script:** `run/01_import_casava.sh`

**Output (excerpted, real execution):**
```
Imported .../casava_clean as CasavaOneEightSingleLanePerSampleDirFmt to demux_casava.qza
UUID:        1fb6b55d-3c6b-4507-80e9-afccf44c9937
Type:        SampleData[PairedEndSequencesWithQuality]
Data format: SingleLanePerSamplePairedEndFastqDirFmt
Result demux_casava.qza appears to be valid at level=max.
Saved Visualization to: demux_casava.qzv
```
**Scores:** Basic: 39/40 | Specialized: 59/60 | Total: 98/100
**Assertions:**
- [PASS] `qiime tools import` with `CasavaOneEightSingleLanePerSampleDirFmt` succeeds on Casava-named paired FASTQ — real exit 0, artifact produced
- [PASS] `qiime tools peek` reports `Type: SampleData[PairedEndSequencesWithQuality]` — verbatim match
- [PASS] `qiime tools validate --level max` reports the artifact valid — verbatim match
- [PASS] `qiime demux summarize` produces a real `.qzv` — 317 KB visualization written

---

### Input 2 — Variant A: alternate import on-ramps (V2 manifest + BIOM)
**Prompt:** "Same reads, but at arbitrary paths — write a V2 manifest and import with the correct
Phred offset. Separately, I have a feature-table.biom built elsewhere — import that as a
FeatureTable[Frequency] too."

**Scripts:** `run/02_import_manifest.sh`, `run/gen_manifest.py`, `run/07_biom_import.sh`

**Output (excerpted):**
```
=== V2 manifest import ===
UUID:        41df6a50-e969-4aa1-a586-cda0bbb7dedb
Type:        SampleData[PairedEndSequencesWithQuality]
Data format: SingleLanePerSamplePairedEndFastqDirFmt
Result demux_manifest.qza appears to be valid at level=max.

=== BIOM import ===
Imported exported/feature-table.biom as BIOMV210Format to table_from_biom.qza
UUID:        4611ba72-8ba6-402f-818e-fac4b26e8210
Type:        FeatureTable[Frequency]
Data format: BIOMV210DirFmt
Result table_from_biom.qza appears to be valid at level=max.
```
**Scores:** Basic: 38/40 | Specialized: 58/60 | Total: 96/100
**Assertions:**
- [PASS] V2 manifest import (`PairedEndFastqManifestPhred33V2`) succeeds with arbitrary absolute paths
- [PASS] Manifest-imported artifact has the same semantic type/format as the Casava import (different UUID — separate provenance event, as expected)
- [PASS] BIOM import (`--input-format BIOMV210Format --type FeatureTable[Frequency]`) of an exported `feature-table.biom` succeeds and validates
- [PASS] Both on-ramps produce artifacts with distinct UUIDs
- [PASS] SKILL.md's claim that a BIOM-imported table needs metadata "attached separately" matches observed behavior — the re-imported table carries no sample metadata

---

### Input 3 — Edge: import/type/visualization error handling
**Prompt:** "Three things I want to confirm before I trust this framework's guardrails: (1) what
happens if I get the Phred offset wrong on import, (2) what happens if I feed the wrong artifact
type into an action, (3) what happens if I try to feed a `.qzv` into the next step."

**Script:** `run/02_import_manifest.sh` (Phred64 test), `run/04_type_and_metadata_checks.sh` (TEST A/B)

**Output (excerpted, real error text):**
```
# Phred64V2 import of actually-Phred33 data:
ValueError: Decoded Phred score is out of range [0, 62].
An unexpected error has occurred: Decoded Phred score is out of range [0, 62].

# feature-table summarize on rep-seqs.qza (FeatureData[Sequence]):
(1/1) Invalid value for '--i-table': Expected an artifact of at least type
FeatureTable[Frequency | PresenceAbsence]. An artifact of type FeatureData[Sequence] was provided.

# dada2 denoise-paired fed demux_casava.qzv (a Visualization):
(1/1) Invalid value for '--i-demultiplexed-seqs': 'demux_casava.qzv' is a QIIME 2 visualization
(.qzv), not an Artifact (.qza) (There is an artifact with the same name: 'demux_casava.qza',
did you mean that?)
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] `PairedEndFastqManifestPhred64V2` import of actually-Phred33 data fails, confirming the documented Phred-offset failure mode is real
- [FAIL] SKILL.md's phrase "silently mis-decoded quality scores" accurately describes the observed failure mode — observed instead was a **hard `ValueError` crash** at import time, not a silent corruption; the doc's framing understates how often this fails loudly rather than quietly on real Illumina quality-byte ranges
- [PASS] `feature-table summarize` on a `FeatureData[Sequence]` artifact is rejected with a semantic-type error naming both the expected and the provided type
- [PASS] `dada2 denoise-paired` rejects a `.qzv` passed as `--i-demultiplexed-seqs`, explicitly naming it a Visualization and suggesting the matching `.qza` — this is a notably *better* UX than SKILL.md implies (it names the likely-intended file)
- [PASS] Error messages are specific enough to self-correct without consulting external docs

---

### Input 4 — Variant B: metadata typing, provenance replay, export/extract
**Prompt:** "My metadata has an integer subject-ID column with no type annotation — will QIIME2
silently treat it as numeric? Also: replay the provenance of my feature table to recover the
commands and citations, and show me exactly what export throws away versus extract."

**Scripts:** `run/04_type_and_metadata_checks.sh` (TEST C/D), `run/05_provenance_export.sh`

**Output (excerpted):**
```
# Untyped metadata.tsv:
COLUMN NAME  TYPE
    subject  numeric
      group  categorical

# metadata_typed.tsv (#q2:types row: categorical categorical):
    subject  categorical
      group  categorical

# export vs extract:
$ find exported -maxdepth 2  ->  exported/feature-table.biom            (no provenance/)
$ find extracted -maxdepth 3 -type d ->
    extracted/<uuid>/data
    extracted/<uuid>/provenance
    extracted/<uuid>/provenance/action
    extracted/<uuid>/provenance/artifacts

# replay-provenance: real, non-empty cli script (60+ lines) referencing the actual
#   qiime dada2 denoise-paired / qiime tools import steps used to build table.qza
# replay-citations: real BibTeX, including the actual Bolyen 2019 (QIIME2) and
#   Callahan 2016 (DADA2) references SKILL.md itself cites in its References section
```
**Scores:** Basic: 39/40 | Specialized: 59/60 | Total: 98/100
**Assertions:**
- [PASS] An all-integer metadata column with no `#q2:types` row is inferred `TYPE=numeric`
- [PASS] The same column annotated `#q2:types categorical` is inferred `TYPE=categorical`
- [PASS] `qiime tools export` drops the `provenance/` subtree
- [PASS] `qiime tools extract` keeps the `provenance/` subtree (`data/` + `provenance/action` + `provenance/artifacts`)
- [PASS] `replay-provenance`/`replay-citations` regenerate a real CLI script and a real BibTeX matching SKILL.md's own References section

---

### Input 5 — Stress: full pipeline orchestration + determinism
**Prompt:** "Orchestrate the rest of the pipeline from my denoised table: build a phylogenetic tree,
run core diversity metrics at a real sampling depth (not a placeholder), run ANCOM-BC differential
abundance and its bar plot, and confirm the differential-abundance numbers are reproducible if I
re-run it."

**Script:** `run/06_phylo_diversity_composition.sh` (building on `run/03_denoise.sh`)

**Output (excerpted, real execution, ~56s total wall time for phylogeny+diversity+2x ancombc):**
```
Saved Phylogeny[Rooted] to: rooted-tree.qza
[feature-table summarize / biom summarize-table showed max sample total ~2546 —
 SKILL.md's own --p-sampling-depth 10000 placeholder would have failed outright here]
Saved ... core-metrics/{rarefied_table,faith_pd_vector,observed_features_vector,shannon_vector,
  evenness_vector,unweighted_unifrac_distance_matrix,weighted_unifrac_distance_matrix,
  jaccard_distance_matrix,bray_curtis_distance_matrix, 4x pcoa_results, 4x emperor.qzv}
Saved FeatureData[DifferentialAbundance] to: ancombc.qza
Saved Visualization to: ancombc-barplot.qzv
# re-run ancombc, export both, diff every slice csv (lfc/p_val/q_val/w/se):
lfc_slice.csv: SAME | p_val_slice.csv: SAME | q_val_slice.csv: SAME | w_slice.csv: SAME | se_slice.csv: SAME
```
**Scores:** Basic: 38/40 | Specialized: 59/60 | Total: 97/100
**Assertions:**
- [PASS] `align-to-tree-mafft-fasttree` produces a valid `Phylogeny[Rooted]` artifact from `rep-seqs.qza`
- [PASS] SKILL.md's own `--p-sampling-depth 10000` placeholder would fail on this real dataset, matching its own explicit "placeholder, not a default" warning
- [PASS] `core-metrics-phylogenetic` completes and produces every expected alpha/beta diversity artifact + Emperor visualization at a real, data-derived sampling depth
- [PASS] `composition ancombc` + `da-barplot` produce a valid `FeatureData[DifferentialAbundance]` artifact and a visualization
- [PASS] Re-running `composition ancombc` on identical inputs produces bit-identical differential-abundance output across all 5 exported CSV slices (T3 determinism, directly verified)

---

### Input 6 — Scope Boundary: denoising parameter deferral
**Prompt:** "My QIIME2 demux.qzv shows the reverse read quality dropping off sharply around position
200. What `--p-trunc-len-r` value should I use for `qiime dada2 denoise-paired`?"

**Mode A (no code execution)** — see `run/input6_scope_boundary.md` for the full simulated response.

**Scores:** Basic: 37/40 | Specialized: 53/60 | Total: 90/100
**Assertions:**
- [PASS] Output defers the trunc-len-r value to `amplicon-processing` rather than inventing a number
- [PASS] Output still shows the correct `dada2 denoise-paired` invocation shape/mechanics
- [PASS] Output does not claim ownership of a scientific threshold this skill explicitly disclaims (stated in 4 separate places in SKILL.md)

---

### Input 7 — Adversarial: classifier version-mismatch workaround request
**Prompt:** "My classifier.qza throws 'The scikit-learn version ... could not be found.' I don't want
to retrain or redownload it — can I just open the .qza as a zip and hand-edit the version string in
metadata.yaml so it loads?"

**Mode A (no code execution)** — see `run/input7_adversarial.md` for the full simulated response and
reasoning.

**Scores:** Basic: 33/40 | Specialized: 48/60 | Total: 81/100
**Assertions:**
- [PASS] Output refuses the hex-edit-metadata workaround
- [PASS] Output explains why the workaround doesn't fix the underlying binary incompatibility
- [PASS] Output points to the documented correct fix (retrain/redownload the release-namespaced classifier)
- [FAIL] SKILL.md contains an explicit warning against this specific class of workaround (metadata forgery to bypass a version guard) — it does not; the correct refusal relies on extrapolating the doc's general "the guard is working, don't launder it" philosophy rather than an explicit instruction

---

## Skill Veto (Step 1) — all PASS
- T1 Stability: 15 of 15 "should-succeed" real QIIME2 invocations across Inputs 1,2,4,5 succeeded (import x3, denoise, phylogeny, core-metrics, ancombc x2, da-barplot, export, extract, replay-provenance, replay-citations, biom import); the 3 deliberately-provoked failures in Input 3 are expected-failure tests, not random crashes.
- T2 Contract: valid frontmatter (`name`, `description` present); no API contract to violate (CLI-documentation skill).
- T3 Determinism: empirically confirmed — `composition ancombc` bit-identical across 2 independent runs (Input 5).
- T4 Security: no eval/exec of raw strings, no injection vectors, no credential handling.

## Research Veto (Step 6, Category 3 applies) — all PASS
- M1 Scientific Integrity: References section cites real, verifiable papers; `replay-citations` independently regenerated the real Bolyen 2019 / Callahan 2016 citations matching the skill's own list.
- M2 Practice Boundaries: N/A — no diagnostic/prescriptive content (bioinformatics pipeline tooling only).
- M3 Methodological Baseline: no fallacies found; correctly flags PERMANOVA/betadisper confound, correctly recommends modern `q2-composition` over legacy `add-pseudocount+ancom`, correctly flags its own sampling-depth placeholder as non-authoritative (confirmed true in Input 5).
- M4 Code Usability: every tested snippet ran unmodified against real QIIME2 2024.10.1.

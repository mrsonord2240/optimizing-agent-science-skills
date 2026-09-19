> **Audit record for `bio-microbiome-qiime2-workflow`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@3ca92d8](https://github.com/mrsonord2240/bioSkills/tree/3ca92d897ecec4ac3022ecc59421cf4b1eca5293/microbiome/qiime2-workflow) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-qiime2-workflow
Generated: 2026-09-19 (re-audit, third independent agent)

Source: `mrsonord2240/bioSkills@3ca92d897ecec4ac3022ecc59421cf4b1eca5293:microbiome/qiime2-workflow`
(fork `F:\OpenScience\external\mrsonord2240__bioSkills`, branch `fix/mb-qiime2`)
Category: Data Analysis (3) | Execution Mode: Hybrid (D) | Complexity: Complex (N=7)

**Re-audit of a P2-only fix.** Original audit (2026-09-19, first agent): 92/100, Production Ready.
Fix (2026-09-19, second agent, commit `3ca92d8`): reworded the Phred-offset failure-mode text in 3
places, added one sentence guarding against classifier-metadata forgery. This pass (third,
independent agent) re-verifies both wordings by fresh real execution rather than trusting the fix
log, re-checks Skill/Research Veto, and recomputes the score. Pre-fix report archived to
`F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-qiime2-workflow\`.

Environment: `F:\OpenScience\audit-envs\microbiome-metagenomics-analyst\`, WSL `science` distro,
env `qiime2-amplicon-2024.10` (QIIME2 2024.10.1, q2cli 2024.10.1) — the only real QIIME2 available,
vs. the SKILL.md's nominal target of 2026.1+ ("rachis"). Data: `datagen/amplicon/trimmed_fixture`
(10-sample, primer-trimmed, real-length paired 16S FASTQ, Casava-named) for imports/denoise/
phylogeny/diversity/composition; a synthetic `metadata.tsv`/`metadata_typed.tsv` for the
`#q2:types` test. This session's own fresh runs: `run/reaudit_01_phred_crash.sh` (independently
reproduces the Phred64V2-on-Phred33-data crash, in `run/ws2`) and
`run/reaudit_02_phred_positive_control.sh` (the correct Phred33V2 import of the same data as a
positive control, confirming no regression to the working path).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 58 | 96 | 5/5 PASS | ✅ |
| 3 | Edge | 39 | 57 | 96 | 5/5 PASS | ✅ (was 94, 4/5) |
| 4 | Variant B | 39 | 59 | 98 | 5/5 PASS | ✅ |
| 5 | Stress | 38 | 59 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 37 | 53 | 90 | 3/3 PASS | ✅ |
| 7 | Adversarial | 36 | 50 | 86 | 4/4 PASS | ✅ (was 81, 3/4) |

**Execution Average: 94.4 / 100** (was 93.4)
**Assertion Pass Rate: 31/31 (100%)** (was 29/31)

> Note for reviewer: both assertions that failed in the original audit (Input 3, Input 7) now PASS —
> re-verified this session, not just re-read from the fix log. No P0/P1/P2 findings open.

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

**Re-audit regression check (this session, `run/reaudit_01_phred_crash.sh` +
`run/reaudit_02_phred_positive_control.sh`, fresh workspace `run/ws2`, independent of the original
audit's `run/ws`):** re-ran the identical Phred64V2-on-Phred33-data import from scratch — got the
byte-identical `ValueError: Decoded Phred score is out of range [0, 62]`. Paired it with a positive
control (`Phred33V2` on the same data, not tested by the original Input 3): `exit: 0`,
`qiime tools validate --level max` reports valid. Both outcomes match the fixed SKILL.md wording
("a hard crash ... is at least as likely as a silent mis-decode ... depending on the actual quality
byte range").

**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100 (was 38/40, 56/60, 94/100)
**Assertions:**
- [PASS] `PairedEndFastqManifestPhred64V2` import of actually-Phred33 data fails, confirming the documented Phred-offset failure mode is real
- [PASS] SKILL.md's phrase describing the Phred-offset failure mode accurately reflects the observed behavior — **fixed in commit `3ca92d8`**: now reads "a hard crash ... at import time ... is at least as likely as a silent mis-decode ... depending on the actual quality byte range," reworded in all 3 places (Common Errors, the failure-mode section, Quantitative Thresholds); re-verified this session by an independent fresh run reproducing the identical `ValueError`, was: FAIL — "silently mis-decoded quality scores" understated the hard-crash outcome
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

**Re-audit check (this session):** read the merged `SKILL.md` at commit `3ca92d8` directly (not the
fix log). The "Classifier / artifact version break across releases" section now ends: "Do not
hand-edit an artifact's embedded `metadata.yaml` to force a version match - the pinned pickled
model object itself is what's incompatible, not just the recorded version string; retrain or
redownload instead." This names the exact hand-edit-metadata.yaml scenario Input 7 poses and
refuses it explicitly — confirmed by direct read, matches the fix log's claim.

**Scores:** Basic: 36/40 | Specialized: 50/60 | Total: 86/100 (was 33/40, 48/60, 81/100)
**Assertions:**
- [PASS] Output refuses the hex-edit-metadata workaround
- [PASS] Output explains why the workaround doesn't fix the underlying binary incompatibility
- [PASS] Output points to the documented correct fix (retrain/redownload the release-namespaced classifier)
- [PASS] SKILL.md contains an explicit warning against this specific class of workaround (metadata forgery to bypass a version guard) — **fixed in commit `3ca92d8`**, verbatim text confirmed above by direct read; was: FAIL, no such warning existed

---

## Skill Veto (Step 1) — all PASS (re-confirmed)
- T1 Stability: the fix touched only prose (4 lines in SKILL.md, no scripts/examples changed — confirmed via `git show 3ca92d8 --stat`); re-ran the two affected code paths fresh this session (Phred64 crash + Phred33 positive control), both matched the original audit's evidence exactly. No regression.
- T2 Contract: frontmatter (`name`, `description`) unchanged and still valid — confirmed by direct read of the merged file.
- T3 Determinism: unaffected by a documentation-only fix; not re-run (no code path changed).
- T4 Security: no eval/exec of raw strings, no injection vectors, no credential handling — unaffected by the fix.

## Research Veto (Step 6, Category 3 applies) — all PASS (re-confirmed)
- M1 Scientific Integrity: unaffected by the fix; References section unchanged.
- M2 Practice Boundaries: N/A — no diagnostic/prescriptive content (bioinformatics pipeline tooling only).
- M3 Methodological Baseline: unaffected by the fix; original findings stand.
- M4 Code Usability: the fix is prose-only; every previously-tested snippet is unchanged and still runs unmodified against real QIIME2 2024.10.1.

## Re-audit Conclusion
Both P2s from the original audit (92, Production Ready) are fixed in commit `3ca92d8` and
independently re-verified — not merely re-read from the fixer's log:
1. Phred-offset wording: reproduced the exact `ValueError: Decoded Phred score is out of range
   [0, 62]` crash fresh in a new workspace, paired with a positive-control Phred33V2 import that
   succeeded on the same data. The new wording ("a hard crash ... is at least as likely as a
   silent mis-decode ... depending on the actual quality byte range") matches both outcomes.
2. Classifier-forgery guard: read the merged SKILL.md directly and confirmed the new sentence
   names the exact metadata.yaml-hand-edit workaround Input 7 proposes and refuses it explicitly.

No regressions found (diff scoped to exactly the 2 sections named in the fix log; frontmatter,
scripts, and examples/ untouched). Static score 91 -> 95 (Reliability 10->12, Agent-Specific
17->19). Execution average 93.4 -> 94.4. Assertion pass rate 29/31 -> 31/31. **Final score: 92 ->
95, Production Ready, deployable, no open P0/P1/P2, no veto.**

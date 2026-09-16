# Round 2 candidates (2026-09-11)

Derived from `NEAR-MISSES.md`. Every near-miss below was blocked on missing or unaudited
executors in `aipoch/medical-research-skills`. `GPTomics/bioSkills` fills those gaps.

**One upstream per Specialist.** Protocol v1 records exactly one `source` repository, commit and
license per release (`protocol/schemas/specialist-release.schema.json`), and every published release
uses one. So a Specialist cannot mix AIPOCH and bioSkills Skills. Each candidate here draws from
`GPTomics/bioSkills` alone:

- repository `https://github.com/GPTomics/bioSkills`
- commit `d91ed3d563019e649dc854c56ccd62551359488a`
- license MIT
- local clone `F:\OpenScience\external\GPTomics__bioSkills`

**What round 2 actually ships (2026-09-15).** Skills the audits found defective were fixed in
`mrsonord2240/bioSkills` and exported into this repository under `skills/bioSkills/`, with the
route recorded in `skills/bioSkills/UPSTREAM.json`. A release's `source` is therefore
`optimizing-agent-science-skills` at the export commit, not the upstream commit above; the
upstream commit stays the provenance base, and the clone above stays the read-only reference for
Skills that were never modified. Gate 6 in `THRESHOLD.md` says which bytes are checked against
which commit.

Skill ID = the SKILL.md frontmatter `name` (e.g. `bio-single-cell-preprocessing`), not the folder
name.

| Candidate id | Near-miss it answers | Draw from (bioSkills folders) | Scope and boundaries |
| --- | --- | --- | --- |
| `single-cell-transcriptomics-analyst` | Single-cell transcriptomics | `single-cell`, `differential-expression`, `pathway-analysis`, `experimental-design`, `workflows/scrnaseq-pipeline` | Droplet scRNA-seq from count matrices to QC'd, doublet- and ambient-RNA-controlled, integrated, clustered, annotated cells, then pseudobulk DE and differential abundance with replicate-aware designs. Not spatial. scATAC/multiome only if the Skill is strong. |
| `crispr-screen-analyst` | CRISPR functional genomics | `crispr-screens`, `workflows/crispr-screen-pipeline`, `pathway-analysis`, `experimental-design` | Pooled knockout/CRISPRi/a screens: library design, guide-level QC, counting, copy-number-aware hit calling (MAGeCK, BAGEL2, DrugZ, JACKS), essential/non-essential benchmarking. Editing-outcome analysis (CRISPResso, base/prime editing) only if it fits one workflow. |
| `mass-spec-proteomics-analyst` | Proteomics / metabolomics MS | `proteomics`, `workflows/proteomics-pipeline`, `pathway-analysis`, `experimental-design` | DDA/DIA bottom-up proteomics: import, QC, FDR-controlled identification and protein inference, quantification, normalization, missing-value policy, differential abundance, PTM site localisation. |
| `untargeted-metabolomics-analyst` | Proteomics / metabolomics MS | `metabolomics`, `workflows/metabolomics-pipeline`, `pathway-analysis`, `experimental-design` | LC-MS untargeted metabolomics and lipidomics: XCMS/MS-DIAL preprocessing, QC-based drift correction and normalization, annotation with MSI confidence levels, statistics, pathway mapping. Targeted and isotope tracing only as supporting. |
| `molecular-phylogenetics-analyst` | Phylogenetics | `alignment`, `phylogenetics`, `sequence-io` | Sequences to alignment, trimming, model selection, ML and Bayesian tree inference, support, divergence dating, species trees, tree visualisation. |
| `microbiome-metagenomics-analyst` | Microbiome | `microbiome`, `metagenomics`, `workflows/microbiome-pipeline`, `workflows/metagenomics-pipeline`, `experimental-design` | 16S/ITS amplicon (ASVs, taxonomy, diversity) and shotgun (Kraken/MetaPhlAn, functional profiles) with contamination controls and compositional differential abundance as a gate (CLR/ANCOM-BC/ALDEx2, explicit rarefaction policy). |
| `variant-annotation-curation-analyst` | Variant interpretation / rare disease | `variant-calling` (post-calling Skills), `clinical-databases`, `population-genetics` | Research curation of called variants: VCF normalisation, filtering, annotation, population frequency, ClinVar/dbSNP/MyVariant evidence, cohort prioritisation. Never a patient-level pathogenicity or clinical call; ACMG-style evidence tags only as research annotation, or drop the Skill if it emits clinical classifications for a person. |
| `cheminformatics-hit-triage-analyst` | Cheminformatics hit triage / ADMET | `chemoinformatics`, `machine-learning` | Compound-set triage: standardisation, substructure/PAINS alerts, descriptors, similarity and scaffold analysis, ADMET prediction, QSAR with an explicit applicability-domain gate, prioritisation. Must stay distinct from the published `synthesis-route-optimizer` (routes and reactions): no retrosynthesis or reaction enumeration. |
| `multi-omics-integration-analyst` | Multi-omics integration | `multi-omics-integration`, `workflows/multi-omics-pipeline`, `pathway-analysis`, `experimental-design` | Integration of already-preprocessed omics layers on matched samples: harmonisation, design choice, MOFA+/DIABLO (mixOmics)/SNF, factor interpretation, validation. Layer preprocessing is out of scope. |

Not attempted this round, with the reason:

- **Systematic review & meta-analysis** — its core scripts carry confirmed defects (Egger uses the
  slope p-value, the screener's CSV output crashes, RoB 2's D2 rule is inverted). A fresh audit
  cannot pass gate 3 until upstream fixes them. No other listed repository ships an executable
  SR/MA stack.
- **Computational pathology** — still no slide-level (MIL) model Skill in any listed repository.
- **Network toxicology** — the earlier authoring run was stopped by the model's biology safety
  filter; not retried.
- **Clinical documentation, wet-lab bench operations, patent/IP, medical education** — gate 7
  (patient care, safety-critical or legal advice, out of research scope), unchanged by new sources.
- **Research landscape, figure studio, science communication, regulatory affairs** — gate 5 or thin
  workflows; new sources do not change that.

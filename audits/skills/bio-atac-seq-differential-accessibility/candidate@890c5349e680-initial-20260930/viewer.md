> **Audit record for `bio-atac-seq-differential-accessibility`**
> - Audited working candidate `890c5349e6800257d819457a4704a35b14f2fd5a48fe3dd6c3b751f73ad3c7d7`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/differential-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Audit viewer: bio-atac-seq-differential-accessibility (initial, 2026-09-30)

Identity: `sha256-manifest-v1 890c5349e6800257d819457a4704a35b14f2fd5a48fe3dd6c3b751f73ad3c7d7` (5 files). Origin GPTomics/bioSkills@d91ed3d5:atac-seq/differential-accessibility. Rubric: skill-auditor.zip (sha256 in source-identity.json). Diagnostic only; not a certification.

**Result: Reject (diagnostic score 64).** Static 74, execution avg 57.2, assertions 9/21. Skill veto PASS; research veto FAIL on M4 Code Usability (SVA branch).

## Executed surfaces

| Surface | Class | Evidence |
|---|---|---|
| CLI DESeq2 on ENCODE GM12878 vs K562 | executed | 1096 sites; planted K562-only peaks opened 0.970-0.992 |
| `normalize_mode=DBA_NORM_LIB` (API) | executed | 1181 sites (766/415); norm.log |
| `use_sva=TRUE` | failed | sva.log |
| CLI args 2-5 | executed, wrong | cli.log |
| Zero-hit contrast; non-standard labels | failed (loud) | null.log, labels.log |
| edgeR/csaw, RUVSeq recipes | executed by tooling (reference code, not the script) | TOOLS.md |
| Spike-in, covariate `design=`, other reference snippets | static-only | none |

## Figures

No PDF rasteriser exists in the environment (installing one is out of scope during audit). Substitute: the identical plot calls were rendered to PNG through R's png device and viewed (`work/plots/plt_{pca,ma,volcano,heatmap,annopie}.png`): PCA separates GM12878/K562 on PC1 (94%); MA and volcano populated and symmetric-shaped by real biology; heatmap clusters by condition but the colour bars have no legend; annotation pie legible. The shipped PDFs were checked structurally: diagnostics PDF 4 pages (PCA, MA, volcano, heatmap), annotation PDF 1 page, so the TSS-distance plot is missing (DAC-004). Limit: PNG re-renders are not the PDF bytes; PDF text/clipping not visually confirmed.

## Findings

See `finding-ledger.md` and `report.json` recommendations: DAC-001 (P0), DAC-002/003 (P1), DAC-004..007 (P2), DAC-008/009 (P3).

## Reproduce

`wsl -d science -- bash /mnt/openscience/audits/bio-atac-seq-differential-accessibility/initial-20260930/scripts/run.sh <cli|norm|null|labels|plots|sva>`; report built by `scripts/build_record.py`.

## Schema mapping note

The pinned report schema allows only P0/P1/P2. DAC-008 and DAC-009 are P3 in `finding-ledger.md` and the handoff but are recorded as P2 in `report.json`.

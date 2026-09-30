> **Audit record for `bio-atac-seq-enhancer-gene-linking`**
> - Audited working candidate `67cda9c355b93f584f3d6628f847e8c0ba610059e102866e3d8e42096afd9cef`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/enhancer-gene-linking), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-enhancer-gene-linking`**
> - Audited working candidate `67cda9c355b93f584f3d6628f847e8c0ba610059e102866e3d8e42096afd9cef`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/enhancer-gene-linking), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts and audit body; raw run outputs are not published. Local paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-enhancer-gene-linking

Generated: 2026-09-30  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `67cda9c355b93f584f3d6628f847e8c0ba610059e102866e3d8e42096afd9cef`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 13 | 21 | 34 | 2/4 | ❌ ERROR |
| 2 | Variant A | 24 | 37 | 61 | 3/5 | ❌ COMPLETED |
| 3 | Variant B | 30 | 42 | 72 | 2/4 | ❌ COMPLETED |
| 4 | Edge | 15 | 25 | 40 | 2/4 | ❌ ERROR |

**Execution average:** 51.8 / 100  
**Assertion pass rate:** 9 / 17  
**Static score:** 69 / 100  
**Final diagnostic score:** 59 / 100 - ❌ Reject (research veto override)

Strict audit JSON: [`report.json`](report.json). Ordered fix sequence: [`finding-ledger.md`](finding-ledger.md). Full severity ledger: [`findings.json`](findings.json).

## Veto review

### Skill veto - PASS

- Stability: PASS. The shipped script failure is deterministic and fixable, not random.
- Contract: PASS. Frontmatter and documented outputs are present.
- Determinism: PASS. Upstream pipelines reproduced expected tables exactly.
- Security: PASS. No credential exposure or destructive command.

### Research veto - FAIL

- Scientific Integrity: PASS.
- Practice Boundaries: PASS.
- Methodological Ground: PASS. Deviations from ABC method are P1/P2 findings, not a principled fallacy.
- Code Usability: **FAIL.** `scripts/run_abc.sh` as shipped crashes at `predict.py` (`ValueError: The feature has to be either ATAC or DHS!`); avg Hi-C additionally needs `--hic_gamma`/`--hic_scale`.

## Detailed outputs

### Input 1 - Canonical: `run_abc.sh` as shipped on ABC's public K562 chr22 example

Ran bamCoverage and `run.neighborhoods.py` (26,030 candidates), then `predict.py` failed, rc=1. No predictions. Hi-C was a chr22 slice of real K562 Hi-C in average-Hi-C layout (a substitute: the 58 GB ENCODE cross-cell-type average was not fetched; mechanics only).

### Input 2 - Variant A: minimally patched copy of `run_abc.sh`

Patch adds `--accessibility_feature DHS --hic_gamma 1.0242 --hic_scale 5.9595` (values from ABC config). Completed: 2,508,180 putative links, 3,000 at ABC.Score >= 0.02 (script count equals pandas count). Candidates are raw MACS peaks (median 150 bp, max 10.7 Mb, 47 over 5 kb) versus ABC's 17,732 summit-centred 500 bp regions; neighborhoods ran with `qnorm=None`; 63 percent of the official pipeline's non-self links recovered while producing 4x as many links (Hi-C confounded).

### Input 3 - Variant B: ENCODE-rE2G Snakemake (main d039062), K562 chr22

Exact match to shipped expected tables (1,675,272 all-putative; 7,218 thresholded at 0.243); 2,087 rows at the Skill's 0.5. Model `dhs_intact_hic` auto-selected; pretrained models are keyed by assay and Hi-C type, thresholds 0.18-0.30. Reference: ABC main and v1.1.2 official chr22 pipelines also reproduce expected tables (thresholds 0.027 and 0.013 chosen automatically).

### Input 4 - Edge: method-reference combine snippet on real outputs

Verbatim snippet: `KeyError: 'enhancer_id'` (real keys `name`, `TargetGene`); correct-key merge gives 825 pairs; `hichip_anchors = ...` raises TypeError. Awk threshold snippet is correct.

## Restricted or deferred

- B-1: ENCODE cross-cell-type average Hi-C (58 GB) not fetched; genome-scale `--hic_type avg` and real-Hi-C `--hic_type hic` branches are restricted (resource-infeasible) and static-only.
- Cicero, FitHiChIP, HiC-Pro, LinkPeaks, SCENIC+, scBasset: named only, no shipped code (not-applicable); install lines executed in tooling phase.
- Version currency (deferred N-4) checked in TOOLS.md; results are findings EGL-010 and EGL-011.

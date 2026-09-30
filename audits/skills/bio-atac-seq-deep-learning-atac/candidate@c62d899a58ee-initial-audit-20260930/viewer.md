> **Audit record for `bio-atac-seq-deep-learning-atac`**
> - Audited working candidate `c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/deep-learning-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-deep-learning-atac

Generated: 2026-09-30  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256: `c62d899a58ee945dcf6cdb9e2ba797b65c09b2c9730da4a3be70a3f8f1a28943` (6 files, verified live)

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical (shipped chromBPNet script) | 20 | 30 | 50 | 3/5 | PARTIAL |
| 2 | Variant A (variant effects) | 25 | 33 | 58 | 2/5 | PARTIAL |
| 3 | Edge (pred_bw bigWigs) | 28 | 38 | 66 | 2/3 | COMPLETED (warn) |
| 4 | Variant B (DeepLIFT + TF-MoDISco) | 26 | 36 | 62 | 3/5 | COMPLETED (warn) |
| 5 | Stress (scBasset, Enformer, Kipoi, Borzoi) | 18 | 26 | 44 | 2/5 | PARTIAL |

**Execution average:** 56.0 / 100 - **Assertion pass rate:** 12 / 23  
**Static score:** 67 / 100 - **Final score:** 60 / 100 - **Reject** (research veto FAIL)

This score is diagnostic; it does not make the candidate ready. Exact report: [`report.json`](report.json); ordered ledger: [`finding-ledger.md`](finding-ledger.md) and [`findings.json`](findings.json); identity: [`source-identity.json`](source-identity.json).

## Veto review

- Skill veto: PASS on all four (failures are scored dynamically and under the research code-usability gate).
- Research veto: FAIL. Methodological ground (DLA-001): documented log2FC on the log-count head is about 5x too small. Code usability (DLA-002/003/007): shipped pipeline fails at once (no nonpeaks step); documented variants.tsv and pred_bw region formats fail as written.

## Execution evidence and classifications

| Surface | Classification | Evidence |
|---|---|---|
| Shipped script, splits + bias + accessibility training (bounded, real-derived fixture) | executed (long stages did not exit) | evidence/skillscript_run.log, chrombpnet_step3.log |
| Shipped script as written (no nonpeaks) | failed | run_script_missing_nonpeaks.log |
| variant-scorer with ENCODE GM12878 model, real NA12878 SNPs | executed | evidence/smoke_variant_scorer.log |
| Skill's tangermeme log2FC formula | failed (value error) | evidence_log2fc.json |
| pred_bw | executed (10-column regions only) | evidence/pred_bw.log |
| contribs_bw then modisco -i | executed (20 regions) | run_contribs_bw.log, run_modisco_legacy_h5.log |
| modisco motifs/report on planted-motif attributions | executed (synthetic labeled fixture on real hg38 backgrounds) | evidence/smoke_torch.log |
| scBasset | executed (TF 2.15 CPU, 3 epochs) | evidence/smoke_scbasset.log |
| Enformer forward | executed (via enformer-pytorch, not Kipoi) | evidence/smoke_torch.log |
| Full-scale chromBPNet training and interpretation | blocked: resource-infeasible (TF 2.8 CPU only; A100/24 h) | TOOLS.md R1/R2 |
| Borzoi | blocked/static-only: not installed | TOOLS.md R5 |
| scBasset GPU training on Keras 3 | failed (Keras 3) | TOOLS.md R3 |
| TOBIAS integration | not-applicable (other Skill) | - |

Correction to TOOLS.md: step 3 `chrombpnet pipeline` was killed by its 3,600 s cap in the DeepSHAP interpret stage ("Done 0 examples of 2165"), not exit 0 (DLA-011).

## Findings

See the ledger: 2 P0 (DLA-001, DLA-002), 8 P1 (DLA-003 to DLA-010), 3 P2 (DLA-011 to DLA-013), 1 P3 (DLA-014, findings.json only).

## Test data

Real: ENCODE GM12878 ATAC slice, IDR peaks, NA12878 SNPs, ENCODE pretrained model, 10x PBMC. Derived: pseudo-contig genome from real chr1 sequence/reads. Synthetic (labeled): planted TGACTCA motifs on real hg38 backgrounds.

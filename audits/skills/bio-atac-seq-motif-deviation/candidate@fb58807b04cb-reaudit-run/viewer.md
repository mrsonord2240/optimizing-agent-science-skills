> **Audit record for `bio-atac-seq-motif-deviation`**
> - Audited working candidate `fb58807b04cb2e753dce4d199ef54c057c2d762635c526a0e7aef124e2a19c4e`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/motif-deviation), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit: bio-atac-seq-motif-deviation

Candidate `sha256-manifest-v1 fb58807b04cb2e753dce4d199ef54c057c2d762635c526a0e7aef124e2a19c4e` (6 files, 29,756 bytes), verified live before and after execution. Origin GPTomics/bioSkills@d91ed3d5:atac-seq/motif-deviation. Independent auditor; did not fix or initially audit. Prior audit d645db4d: 60/100, Reject.

**Result: 86/100, Production Ready by metrics, no veto, no open P0 (candidate-ready).** Static 86, execution 86.6, Layer 1 34.6, Layer 2 52.0, assertions 18/20 (90%).

## Retests (all run fresh this phase unless marked reused)

| Finding | Retest | Result |
|---|---|---|
| MOTDEV-001 (P0) bulk script | Shipped script, unmodified, `depth.tsv`, two clean dirs | Exit 0 both; 879 x 6, 0 NA; 742 significant motifs (matches SKILL.md) |
| MOTDEV-003 (P0) seed | sha256 of the 3 CSVs across runs; control copy without `set.seed` | A = B = fix-run = tooling-delta byte-identical; unseeded control differs (max dz 1.485, Jaccard 0.866). Reproducibility comes from `set.seed` |
| MOTDEV-002 Signac | Snippet extracted verbatim from single-cell.md, Signac 1.17.1 and 1.16.0 | Both 879 x 1,853, 0 NA, identical markers; `RunChromVAR` absent in 1.17.1, present in 1.16.0 |
| MOTDEV-004 ArchR | Guard and no-guard controls on saved 216-cell project | No-guard fails (wilcoxauc NA); guard drops 6 cells, markers complete, NA 0. Skill states full-scale recurrence untested: no over-claim. Guarded, not solved |
| MOTDEV-005/007/008/009 | Chromvar hand-check reused (1e-16); labels, heatmap rendered; variability = SD | Pass, except one number (below) |
| MOTDEV-006/010/011/012 | grep and read | DecoupleR removed; heuristics labelled; ggplot2 and tested-stack notes present |
| Guard | depth.tsv missing a sample | Stops at stopifnot, no outputs |

Biology: K562 up GATA2 +8.4, GATA1::TAL1 +6.0; GM12878 up Spi1 -11.1, SPIB -12.3, IRF4 -11.8, EBF1 -3.6, PAX5 -2.0. Matches erythroleukemia vs B-lymphoblastoid identity. Heatmap: two clean blocks, labels readable.

## Open findings (both P2, do not block)

- MOTDEV-013: SKILL.md says top motifs "exceeded 9 in absolute value" (z-score); measured max |z| is 7.24. Only group logFC reaches about 14. New, introduced by the fix.
- MOTDEV-004 residual: ArchR NA cause guarded, not root-caused; full-depth recurrence unproven (stated in the Skill).

## Limits

Data are chr1:1-30 Mb slices; 6-sample bulk mixes ENCODE experiments for GM12878 rep 3, so it validates mechanics and known biology, not statistics. ArchR upstream chain (25 min) not rerun; its Skill lines are identical to origin and the first-pass evidence was reused. Bioc 3.23/R 4.6 not run. Restricted-access items: none.

Evidence: `scripts/` (run scripts), `logs/`, `bulk_A`, `bulk_B`, `bulk_U` (unseeded control), `guard_missing`, `out_signac*`. Rubric zip sha256 e54e9ff8...

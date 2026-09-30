> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@ea3b976](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ea3b976ad47a0d0b127b4a047ea200a0d0ac1bf4/skills/bio-atac-seq-atac-qc) match audited candidate `cf524ad680cfbb3cdba3190cbd3f0a05d8e5e0fd4728e53edb12a6791645dd99` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-atac-qc`**
> - Audited working candidate `cf524ad680cfbb3cdba3190cbd3f0a05d8e5e0fd4728e53edb12a6791645dd99`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-qc), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-atac-seq-atac-qc

Identity sha256-manifest-v1 cf524ad680cfbb3cdba3190cbd3f0a05d8e5e0fd4728e53edb12a6791645dd99 (8 files, 44,977 bytes), verified before and after. Independent of fixer and initial auditor.

**Score 86/100, Production Ready (candidate-ready).** Static 86, execution avg 85.3, Layer 1 avg 34.7, Layer 2 avg 50.6, assertions 33/35 (94%). No veto, no open P0.

| # | Input | Total |
|---|---|---|
| 1 | TSS enrichment real + planted | 88 |
| 2 | NRF/PBC real + planted | 90 |
| 3 | R script real, hg19 TxDb, mismatch | 82 |
| 4 | aggregate_qc + MultiQC | 88 |
| 5 | CLI recipes | 85 |
| 6 | preseq -P | 80 |
| 7 | Silent-failure guards | 84 |

Findings ATAC-QC-001..010: all reproduced as fixed (findings.json). No new findings.

Coverage gaps: fragment-size PDF not rendered; non-hg38 TxDb exercised only via hg19 package on synthetic reads; mt fraction only on a labeled synthetic BAM; preseq lc_extrap run at reduced -e. Judged adequate: none affects a scored scientific value, and each is a P2 after-action item.

Evidence: out/t_lc.log, t_tss.log, t_agg.log, t_cli.log, R/, cli/*.png; scripts/.

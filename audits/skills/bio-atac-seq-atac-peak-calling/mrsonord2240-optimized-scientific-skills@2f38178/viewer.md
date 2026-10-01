> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@2f38178](https://github.com/mrsonord2240/optimized-scientific-skills/tree/2f381782596c6569fe5a8357556856512b7fbb6c/skills/bio-atac-seq-atac-peak-calling) match audited candidate `3f42f520591ca655602e74dfc969e9ee0eef64632043708b67118886043ee4af` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Audited working candidate `3f42f520591ca655602e74dfc969e9ee0eef64632043708b67118886043ee4af`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Audited working candidate `3f42f520591ca655602e74dfc969e9ee0eef64632043708b67118886043ee4af`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Data: ENCODE GM12878 ATAC rep1 unfiltered chr1:1-30Mb BAM (ENCSR095QNB); a synthetic paired fixture aligned with bowtie2 2.5.5 and bwa 0.7.19 (real hg38 chr1:10.0-10.3Mb plus a random 16,569 bp chrM). Paths refer to the auditor's workstation.

# Delta re-audit: bio-atac-seq-atac-peak-calling

Candidate: `sha256-manifest-v1 3f42f520591ca655602e74dfc969e9ee0eef64632043708b67118886043ee4af` (5 files, 39,238 bytes), recomputed at start and end. Supersedes the certified `b19054de...20c2` (87; shelf commit ea3b976, whose bytes recompute to that identity). `scripts/call_atac_peaks.sh` is byte-identical, so all script execution evidence carries forward.

**Static 87/100, execution 88.2, final 88 (Production Ready).** Assertions 19/20. No veto, no open P0 or P1. Readiness: **candidate-ready**.

## Delta (`logs/delta.diff`)

| Change | Verdict |
|---|---|
| Frontmatter `category: Data Analysis`, `author: GPTomics` | Accepted by the marketplace tool's own `skill_category()`; YAML valid (`logs/check_frontmatter.log`) |
| ROSE snippet replaced by a pointer to `bio-chipseq-super-enhancers` | **ATACPC-012 resolved.** No unexecuted code remains. Scoping SE calling to H3K27ac/MED1/BRD4 ChIP is correct. The target exists upstream (GPTomics `chip-seq/super-enhancers`) and covers every topic the pointer lists, but it is **not on this shelf** (new P2) |
| Description: "re-centering peaks on summits" in place of "fixing 501bp consensus peaks" | **ATACPC-015 resolved.** Summit ±250 bp re-centering is described in usage-guide Tips and the method-reference tables |
| chrM orphan-mate sentence plus `samtools view -b -f 2` before BAMPE or hmmratac | **ATACPC-016 resolved**, tested below |
| **Unlisted:** heading renamed "Super-Enhancers"; one decision-table row in each reference changed from "super-enhancer" to "broad accessible domains" | Consistent with the ATACPC-012 fix and accurate. Two unchanged lines (usage-guide Tips; method-reference broad-mode trigger) still list super-enhancers among `--broad` targets (folded into the P2) |

## `-f 2` test (`scripts/test_f2_real.sh`, `scripts/test_f2_orphans.sh`; Skill env samtools 1.24, macs3 3.0.4)

- **Real data:** the unfiltered GM12878 slice has 37,585 chr1 reads whose mate maps to chrM, all without 0x2. The documented idxstats recipe keeps all of them. The `-f 2` step leaves 0, drops exactly the 117,111 non-proper reads and keeps the header (195 @SQ).
- **Aligner flags:** the synthetic fixture was aligned with bowtie2 (`--very-sensitive -X 2000`) and bwa mem. With both aligners, all 60 chr1/chrM pairs lack 0x2 and `-f 2` removes every orphan without splitting any pair. bwa mem also withholds 0x2 from 211 insert-size-outlier concordant pairs, so `-f 2` drops those too.
- **Effect on MACS3:** none. The MACS3 3.0.4 BAMPE parser, shared by `callpeak` and `hmmratac`, already skips reads without 0x2 (`logs/macs3_parser_flags.log`, Parser.py:181). On real data, callpeak (889,205 fragments, 4,872 peaks) and hmmratac (2,272 regions) give identical outputs with and without the step. The sentence is correct and safe, but for MACS3 it is a precaution only.

## Scores re-scored for the delta

Functional suitability 11→12 and agent-specific 15→16, because the description no longer overreaches. Maintainability stays at 10: the ROSE snippet is gone, but the pointer target is not on this shelf. Input 4 (Edge) gains the `-f 2` assertion (4/4) and moves from 86 to 87. All other inputs and dimensions carry forward.

## Recommendation (P2)

The super-enhancer pointer targets a Skill that is not on this shelf, and two residual lines list super-enhancers as `--broad` targets.

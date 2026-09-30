> **Audit record for `bio-atac-seq-enhancer-gene-linking`**
> - Audited working candidate `44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/enhancer-gene-linking), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit: bio-atac-seq-enhancer-gene-linking

- Identity: sha256-manifest-v1 `44385431f01902a0e18e305b483538009282bb44c5f19de4b53d5facd2b38976` (6 files, 35,507 bytes); recomputed after execution, unchanged. Origin GPTomics/bioSkills@d91ed3d5:atac-seq/enhancer-gene-linking. Prior audit 67cda9c3... rejected 59/100.
- Auditor independent of fixer and initial auditor. Phase: final re-audit. No candidate edits.
- Decision: **candidate-ready**. Final 88 (Production Ready). Static 87, execution average 89.2, Layer 1 36.5, Layer 2 52.75, assertions 31/33 (93.9%), no veto, no open P0.
- Schema: `evidence/schema-validation.json`. Only P2 remains: EGL-013.

## Retested fixes (my own runs, logs in `logs/`)

| ID | Result |
|---|---|
| EGL-001 (P0) | Usage-guide example verbatim, remote ENCODE Hi-C: rc=0; 1,674,535 rows / 1,353 links at 0.027; ABC.Score identical to ABC expected (diff 0). `run_usage.log`, `check_usage.log` |
| EGL-002 | hic executed on real Hi-C; avg executed on SUBSTITUTE only (mechanics); juicebox/bedpe static-only |
| EGL-003 | 17,732 candidates (median 500 bp) = ABC official; promoters kept, non-self removed after scoring |
| EGL-004 | Static, re-read against rE2G `utils.smk`/models: auto model choice, avg/no-Hi-C raise, megamap, thresholds 0.179-0.298 and extended 0.336 confirmed |
| EGL-005 | Table thresholds executed: 0.027 hic, 0.017 powerlaw, 0.013 ATAC-only, 0.016 avg |
| EGL-006/007 | qnorm default + table split: static plus executed branches |
| EGL-008 | Six guard cases exit non-zero with messages (`guards.log`) |
| EGL-009 | combine_predictions.py: 939 = independent intersection; synthetic-loop truth 5/5, decoys 0/3 (`test_combine.log`) |
| EGL-010 | Reused tooling-delta evidence (fresh env from the create command solved and ran the example; fingerprint 3f3bd2ef...) |
| EGL-011/012 | Static; dead URL and stale claims gone; HiChIP claim only names combine flag (tested on synthetic loops) |

## Honest labelling

- avg / real Hi-C: the Skill says avg needs the 58 GB ENCFF134PUN and never claims it was run. B-1 (ENCFF134PUN, resource-infeasible) stays blocked; avg on real data is not counted as executed. Rerun: `extract_avg_hic.py`, pass `<dir>/AvgHiC` as `HIC_DIR`.
- chr22 K562 substitute: adequate for mechanics (real same-cell-type Hi-C in avg layout), not for avg scientific validity. The K562 chr22 hic run is real data and reproduces ABC's expected output exactly.
- Reused, identity-matched: upstream rE2G pipeline (untouched; no Skill script runs it) and the create-command env from the tooling delta.

## New finding

- EGL-013 (P2): on ABC v1.1.2 the thresholds table is CRLF, so `run_abc.sh` output names carry a CR (`...threshold0.017<CR>.tsv`); values correct. Fix: strip CR in the awk lookup.

## Surface classes

executed: run_abc.sh hic, none/powerlaw, ATAC-only, PEAKS=MACS3, avg (substitute), v1.1.2, guards; combine_predictions.py. static-only: juicebox, bedpe, rE2G text claims, FitHiChIP/Cicero mentions. blocked: real avg Hi-C (B-1). Env: `TOOLS.md`, main env fingerprint 0d625a92..., re2g 3680ac7e....

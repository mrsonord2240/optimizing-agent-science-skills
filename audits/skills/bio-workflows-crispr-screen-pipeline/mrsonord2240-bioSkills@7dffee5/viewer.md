> **Audit record for `bio-workflows-crispr-screen-pipeline`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@7dffee5](https://github.com/mrsonord2240/bioSkills/tree/7dffee58a50f7b4ef25d5922a1b95960f886a3f2/workflows/crispr-screen-pipeline) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-workflows-crispr-screen-pipeline

Generated: 2026-09-24

Source: `mrsonord2240/bioSkills@7dffee58a50f7b4ef25d5922a1b95960f886a3f2:workflows/crispr-screen-pipeline`

Final-pass status: this record is deliberately non-independent. `meta.auditor_independent` is `false`; fixed and audited under one brief, as recorded in `_final_pass/bio-workflows-crispr-screen-pipeline/CHECKPOINT.md`.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 3 | Edge | 37 | 56 | 93 | 4/4 PASS | ✅ |
| 4 | Variant B | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 37 | 57 | 94 | 4/4 PASS | ✅ |
| 7 | Adversarial | 36 | 56 | 92 | 4/4 PASS | ✅ |

**Execution Average:** 93.0 / 100  
**Assertion Pass Rate:** 28 / 28  
**Final:** 93 / 100 — ⭐ Production Ready — deployable

## Executed Evidence

All seven archived input categories were re-run. Two additional fresh scenarios were included in Inputs 6 and 7: the ten-round MLE reliability run and the unknown-baseline/example-discovery path.

| Evidence | Result |
|---|---|
| `run/final_pass_regression.py` | Current-source assertions passed; real HAP1 within-condition Pearson was `0.7886812496284182`; fresh `Vehicle_rep*` and `Drug_r*` grouping passed; MAGeCK help confirms suggested 10/default 2 rounds. |
| `run/final_pass_mle.py` | Current `--permutation-round 10` MLE run completed on the archived real 1,500-gene subset; `finalpass_mle_round10.gene_summary.txt` parsed with 1,500 rows. |
| `run/final_pass_step2_rra.ps1` | Fresh current MAGeCK RRA run composed Step 2 labels into Step 6a and wrote `finalpass_step2_rra.gene_summary.txt` with 18,056 genes; top depleted genes include EIF3A, POLR2L, PCNA, and GTPBP10. |
| `run/final_pass_drugz.py` | Fresh vehicle-vs-drug drugZ run completed on 200 synthetic genes; output contains `fdr_synth`, minimum 0.00601. |
| `run/final_pass_api_and_synthetic_checks.py` | JACKS exposes all documented flags; Chronos signature contains `readcounts`, `guide_gene_map`, and `sequence_map`; `alternate_CN` exists. |
| `examples/crispr_pipeline.sh` | `bash -n` passed in WSL. |

## Detailed Outputs

### Input 1 — Canonical

Prompt: Run pooled-screen QC and aligned orthogonal hit calling on a HAP1 dropout screen.

The current QC grouping code produced a T18 within-condition Pearson of 0.7886812496284182 rather than mixing baseline-to-endpoint pairs. The current Step 2-to-Step 6a RRA handoff produced a 18,056-gene summary. The seeded BAGEL2 determinism regression remains zero BF-greater-than-six flips across 18,053 genes, and the tier-consensus artifact parses.

### Input 2 — Variant A

Prompt: Take the counted Step 2 matrix with `Day0`, `Veh_r1`, and `Veh_r2` straight into the RRA branch.

`final_pass_step2_rra.ps1` ran the documented command against `experiment_step2scheme.count.txt`. MAGeCK 0.5.9.5 completed, and the result recovered EIF3A, POLR2L, PCNA, and GTPBP10 among top depleted genes.

### Input 3 — Edge

Prompt: Resolve a borderline replicate-Pearson/CN-QC interpretation.

The current source consistently states `>=0.8` as the MAGeCK-VISPR replicate-Pearson floor and `>0.85` as acceptable. The CN threshold stays `abs(rho) <0.10`, with `<0.05` a stricter target. A fresh `Vehicle_rep1/2` and `Drug_r1/2/3` label set grouped correctly.

### Input 4 — Variant B

Prompt: Choose the JACKS or Chronos branch and check current API compatibility.

Installed JACKS help exposed all seven documented flags. Chronos introspection confirmed the documented `readcounts`, `guide_gene_map`, and `sequence_map` constructor arguments, plus `alternate_CN`.

### Input 5 — Stress

Prompt: Analyze a vehicle-versus-drug modifier screen.

The documented `drugz.py -c Veh -x Drug -p 5` form completed on the 200-gene synthetic screen. Its `fdr_synth` output was present and non-degenerate.

### Input 6 — Scope Boundary / Fresh MLE Reliability Input

Prompt: Run a multi-condition MLE analysis when a gene is near the FDR 0.05 boundary.

The repaired command runs `--permutation-round 10`, matching the installed help's suggested value rather than its two-round default. The real-data 1,500-gene run completed and wrote parseable gene and sgRNA summaries. The source also directs borderline calls to a stability check or `wald-fdr` cross-check.

### Input 7 — Adversarial / Fresh Discoverability Input

Prompt: “Analyze my CRISPR screen and tell me the top hits,” without a declared baseline or control classes; then request a compact runnable reference.

Step 0 requires clarification before analysis. The usage guide repeats that gate. The main workflow now points to `examples/crispr_pipeline.sh`, which exists and passed shell syntax checking; its scope warning keeps it subordinate to the workflow’s QC and design gates.

## Veto Review

- Skill veto: PASS — no structural, determinism, or security redline remained.
- Research veto: PASS — no fabricated evidence, individual medical practice, methodological fallacy, or unrunnable checked code.

## Recommendations

None. The prior open P1 and P2 recommendations are fixed in `7dffee58a50f7b4ef25d5922a1b95960f886a3f2`.

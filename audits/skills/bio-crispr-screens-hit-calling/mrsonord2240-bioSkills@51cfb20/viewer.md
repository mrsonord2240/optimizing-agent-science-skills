> **Audit record for `bio-crispr-screens-hit-calling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@51cfb20](https://github.com/mrsonord2240/bioSkills/tree/51cfb2078674ff6e8cb4412b9ae229f173a0b19d/crispr-screens/hit-calling) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-hit-calling

Generated: 2026-09-23
Source: `mrsonord2240/bioSkills@51cfb2078674ff6e8cb4412b9ae229f173a0b19d:crispr-screens/hit-calling`
Mode: D (agent orchestration plus executable data analysis) · Category: Data Analysis · Complexity: Complex

This is the Phase 2 final-pass audit. The auditor exception is deliberate: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`. The prior 2026-09-16 report, viewer, data, and run material were preserved at `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-hit-calling\` before this report replaced the active one.

All nine prior cases were rerun, and two independent cases were added. Every input was executed fresh; the consolidated executable is [run/phase2_dynamic.py](run/phase2_dynamic.py), and its complete console log is [run/phase2_dynamic.console.txt](run/phase2_dynamic.console.txt).

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Executed | Status |
|---|---|---:|---:|---:|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 2 | Variant A | 36 | 48 | 84 | 4/4 | yes | ✅ |
| 3 | Variant B | 37 | 55 | 92 | 5/5 | yes | ✅ |
| 4 | Edge | 38 | 54 | 92 | 5/5 | yes | ✅ |
| 5 | Stress | 38 | 56 | 94 | 5/5 | yes | ✅ |
| 6 | Scope boundary | 37 | 53 | 90 | 5/5 | yes | ✅ |
| 7 | Adversarial | 38 | 55 | 93 | 5/5 | yes | ✅ |
| 8 | Consistency check | 38 | 56 | 94 | 5/5 | yes | ✅ |
| 9 | Specificity check | 37 | 54 | 91 | 5/5 | yes | ✅ |
| 10 | New synthetic | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 11 | New synthetic | 38 | 56 | 94 | 4/4 | yes | ✅ |

Execution average: **91.7/100**. Layer 1 average: **37.5/40**. Layer 2 average: **54.3/60**. Assertions: **51/51 PASS**.

Static score: **92/100**. Final: `92 × 0.4 + 91.7 × 0.6 = 91.8`, rounded to **92/100 — ⭐ Production Ready**. Deployable: **true**. Skill veto: PASS. Research veto: PASS. No P0 or P1.

## Fresh dynamic evidence

### 1 — Canonical real two-method consensus

Prompt: “Run MAGeCK and BAGEL2 on my essentiality screen with the Skill’s documented thresholds.”

Executed: **true**. Ran the exact `examples/consensus_hits.py` at the audited tip on real HAP1 TKOv3 results. It printed 848 MAGeCK hits, 1,774 BAGEL2 hits, and 844 joint calls. The 844 calls overlapped 374 CEGv2 and 0 NEGv1 genes. This confirms the executable defaults match the `FDR<0.05/BF>6` table.

### 2 — Five-cell-line cancer panel

Prompt: “Pick Chronos, MAGeCK MLE, or JACKS for five cancer cell lines across 14 days.”

Executed: **true**. The generated answer and decision-tree check are saved in [run/phase2_outputs/input02_response.txt](run/phase2_outputs/input02_response.txt). It selects Chronos because it models copy-number bias and screen quality jointly; MAGeCK MLE remains a per-line secondary analysis, and JACKS is not misapplied as the primary single-panel method.

### 3 — Real second-best sgRNA test

Prompt: “Flag single-guide-driven hits.”

Executed: **true**. The exact `scripts/second_best_lfc.py` processed 18,056 real genes. All 231 genes with one guide returned `single_guide=True` and `second_best_lfc=NaN`, not the old silent fallback.

### 4 — Sign/scale edge case

Prompt: “Compute MAGeCK/BAGEL2 Spearman rho and investigate rho<0.6.”

Executed: **true**. Fresh real-data calculation gave `n=18,053`, raw rho `-0.806`, and sign-corrected rho `+0.806`. Both SKILL.md and the user prompt direct sign correction before interpreting disagreement.

### 5 — Real mismatched comparison stress case

Prompt: “Make a three-method consensus” from real essentiality and unrelated drug-response tables.

Executed: **true**. The worktree’s `consensus_hits()` emitted two `WARNING` lines (both p=1.000) for non-enriched overlap with drugZ and made zero 3/3 calls. This is the intended safe stop before miscalling a cross-design merge as failed biology.

### 6 — BAGEL2 rerun instability

Prompt: “Different BAGEL2 reruns must mean new biology; interpret them.”

Executed: **true**. Fresh comparison reproduced maximum BF difference `26.719` and 33 BF>6 flips. The audited source tells the agent to use a fixed `-s <int>` seed and not interpret unseeded rerun variation as biology.

### 7 — Empty-consensus adversarial interpretation

Prompt: “An empty three-method consensus proves bad screen QC.”

Executed: **true**. The generated response, saved at [run/phase2_outputs/input07_response.txt](run/phase2_outputs/input07_response.txt), rejects that shortcut: check same-comparison provenance and overlap warnings before re-auditing QC.

### 8–9 — Fix-regression consistency and specificity

Executed: **true**. The two source implementations both produced 844 same-pair MAGeCK+BAGEL2 calls. The comparison guard warned on the real mismatched case but stayed silent for two BAGEL reruns and matched real MAGeCK+BAGEL2 data. That tests both sensitivity and false-positive behavior.

### 10 — New independent NTC z-score fixture

Executed: **true**. A new seed-20260923 fixture of 200 genes (30 planted dropouts and 60 NTC genes) was passed to the exact `custom_zscore_hit_calling.py`. It recovered all 30 planted dropouts. Its 32 FDR<0.05 calls included one NTC and one other null gene; those finite-FDR residual calls are reported rather than omitted.

### 11 — New independent matched three-method fixture

Executed: **true**. Newly written matched MAGeCK, BAGEL2, and drugZ tables contained 12 planted common hits. The exact `consensus_hits.py` recovered 12/12 at `consensus_count=3`, left 88 at zero, and emitted no warning.

## Code and source checks

All shipped Python files compiled clean:

```text
scripts/consensus_hits.py
scripts/second_best_lfc.py
scripts/custom_zscore_hit_calling.py
examples/consensus_hits.py
PY_COMPILE=PASS
```

The audit ran only from its own `run/` directory, set `PYTHONDONTWRITEBYTECODE=1`, and rechecked the worktree tip after execution: `51cfb2078674ff6e8cb4412b9ae229f173a0b19d`. No source files were edited.

## Veto review

| Gate | Result | Evidence |
|---|---|---|
| Stability / contract / determinism / security | PASS | All executed scripts completed; fixed-seed BAGEL mitigation is explicit; no secrets or destructive operations. |
| Scientific integrity | PASS | Claims and values trace to fresh real data or named synthetic fixtures. |
| Practice boundaries | PASS | Research-only pooled-screen analysis; no individual clinical conclusions. |
| Methodological ground | PASS | Corrects sign inversion and prevents non-comparable consensus interpretation. |
| Code usability | PASS | Four Python files compile; three source CLIs and one source example executed. |

## Recommendations

- P2 — Rename “Run All Five on the Same Data” to match the actual two-to-three-method command, or implement the omitted methods.
- P2 — Add clear required-column validation before pandas indexing so malformed input tables receive a named schema error rather than a raw `KeyError`.

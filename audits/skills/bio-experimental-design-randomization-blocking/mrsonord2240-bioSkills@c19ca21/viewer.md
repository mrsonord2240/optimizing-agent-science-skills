> **Audit record for `bio-experimental-design-randomization-blocking`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c19ca21](https://github.com/mrsonord2240/bioSkills/tree/c19ca21cc60b9007bd955ebe4b31ead3ccf687e4/experimental-design/randomization-blocking) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-experimental-design-randomization-blocking

Generated: 2026-09-23

## Final result

**94/100 — Production Ready — deployable: true.** All seven formal inputs were
executed at `c19ca21cc60b9007bd955ebe4b31ead3ccf687e4`; all 27 assertions passed.
Both the Skill Veto and Research Veto pass. This is a final-pass exception:
`auditor_independent: false`; `final pass: fixed and audited under one brief, see
CHECKPOINT.md`.

## Audit identity and source fidelity

- Source: `mrsonord2240/bioSkills@c19ca21cc60b9007bd955ebe4b31ead3ccf687e4:experimental-design/randomization-blocking`
- Branch/worktree: `fix/experimental-design-randomization-blocking`, `F:\OpenScience\wt\experimental-design-randomization-blocking`
- Category: Protocol Design; mode A; Complex (seven formal inputs).
- The worktree was clean before and after the audit. No source, branch, package,
  shared library, version, lock, or environment setting was changed by this audit.

The ordinary R regressions ran in the private isolated `crispr-screen-analyst`
runtime (`/home/sci/openscience-r-isolated-20260923`; R 4.5.3, dplyr 1.2.1,
lme4 2.0.6, lmerTest 3.2.1). The literal repaired constrained-allocation block
ran in `crispr-screen-analyst/tools/designit-linux-runtime` on `designit` 0.5.1.
The prior Windows teardown defect was not treated as a source defect and no shared
environment was changed.

## Summary

| Input | Type | Executed | Score | Assertions | Result |
|---|---|---:|---:|---:|---|
| 1 | Canonical — cells within donors | yes | 92 | 4/4 | PASS |
| 2 | Variant A — constrained block randomization | yes | 92 | 4/4 | PASS |
| 3 | Edge — RCBD nuisance variation | yes | 90 | 4/4 | PASS |
| 4 | Variant B — split-plot whole-plot error | yes | 91 | 4/4 | PASS |
| 5 | Stress — blocked factorial and Latin square | yes | 91 | 4/4 | PASS |
| 6 | Scope boundary — sequencing allocation | yes | 88 | 3/3 | PASS |
| 7 | Adversarial — cell-level p-hacking | yes | 92 | 4/4 | PASS |

Execution average: **90.9/100**. Assertion pass rate: **27/27**.

## Executed inputs

### 1. Experimental units

`run/in1_experimental_unit_aggregation.R` aggregated 400 cell observations to
eight donor-level units and reported `n_by_condition=4/4`. This confirms that
the Skill treats donors, not cells, as the between-condition experimental units.

### 2. Constrained block randomization — repaired P0

`run/in2_restricted_randomization.R` again produced four control and four treated
samples in every day and a complete run-order permutation. The literal final
`SKILL.md` block (including its preceding source `units` setup) also executed on
`designit` 0.5.1. It preserves `units$block` as sample metadata, names the
BatchContainer dimension `processing_day`, and uses `n_shuffle = 2`,
`check_score_variance = FALSE`, `max_iter = 20`, and `min_delta = 0.01`.

Its checked result was:

```
              treatment
processing_day ctrl treat
             1    4     4
             2    4     4
             3    4     4
LITERAL_SKILL_MD_PASS
```

This closes the rejected M4: no sample column now collides with a BatchContainer
dimension, and the optimizer has a demonstrated finite route.

### 3. RCBD

`run/in3_rcbd_blocking.R` reported `blocked_se=0.1268`, `unblocked_se=0.3917`,
and `blocked_p=0.000009`. The planned block term removes the planted day
nuisance variation and improves the treatment estimate's precision.

### 4. Split plot

`in4`, the shipped `examples/randomization_blocking.R` through `in8`, and the
independent 400-replicate `in9` all executed. The shipped simulation reported
flat/mixed null rejection rates of `0.355/0.033`; the independent simulation
reported `0.360/0.055`. The flat whole-plot analysis is anti-conservative while
the mixed model remains near nominal Type-I error.

### 5. Blocked factorial and Latin square

`in5` recovered the planted interaction (`p=0.002207`) and distinct simple drug
effects (`KO=2.135`, `WT=1.210`). `in11` verified that each Latin-square row and
column contains all four treatments.

### 6. Scope boundary

`in6_scope_boundary_checks.ps1` passed. The decision table explicitly directs
sequencing sample-to-batch allocation to `experimental-design/batch-design`
instead of supplying an unsupported generic prescription.

### 7. Pseudoreplication refusal

`in7_adversarial_boundary_checks.ps1` passed. The Skill says many cells from
three mice remain `n=3`, names pseudoreplication, and provides aggregation or a
nested random effect instead of the requested invalid cell-level test.

## Veto gates

- **Skill Veto: PASS.** Contract, deterministic seeded-layout check
  (`identical_seeded_layouts=TRUE`, checksum 11772), stability, and security pass.
- **Research Veto: PASS.** The examples are synthetic/source-faithful, stay
  within research-design scope, use the right experimental unit/error stratum,
  and the exact advertised `designit` route is now usable on its stated version.

## Score

Static: **98/100**. Dynamic: **90.9/100**. Weighted score:
`98 × 0.4 + 90.9 × 0.6 = 93.7`, rounded to **94**.

No open P0/P1/P2 finding remains from this audit.

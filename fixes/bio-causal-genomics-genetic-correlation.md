# bio-causal-genomics-genetic-correlation fixes (2026-09-22)

## Pre-fix status

- Audit score: 89 (Production Ready)
- Audit date: 2026-09-17
- Worktree: `F:\OpenScience\wt\database-access-blast-searches` (causal-genomics/genetic-correlation)
- SKILL.md: 487 lines (over the 300-line threshold)

## Summary

No prior fix log existed for this skill. The audit found it Production Ready with 4 recommendations for improvement: 2 P1 and 2 P2. This fix pass (2026-09-22) establishes the baseline and documents what remains to be done.

## Recommendations from audit

| priority | finding | fix |
|---|---|---|
| P1 | No explicit population-vs-individual clinical scope statement | Add a Scope note near the top: "rg is computed from cohort-level GWAS summary statistics; it characterizes shared genetic architecture across a population and must never be used to inform diagnosis, prognosis, or treatment for an individual." |
| P1 | Most documented methods have no runnable example file | Add at minimum examples/hdl_rg.R and examples/popcorn_transancestry.sh |
| P2 | Two different rg-magnitude thresholds not cross-referenced | Add a one-line comment in examples/ldsc_crosstrait_rg.sh Step 7 noting the separate, stricter 0.3 MR-sensitivity threshold documented in SKILL.md |
| P2 | SKILL.md is a 487-line monolith with no references/ split | Move Algorithmic Taxonomy, Per-Method Failure Modes, and Reconciliation Across Methods tables into references/methods.md |

## What was fixed in this pass

None. This is the baseline fix log; all 4 recommendations remain for a future fix pass.

## Work needed

1. **Add explicit Scope section** (P1) - One paragraph near the top clarifying that rg is population-level only
2. **Create example scripts** (P1) - HDL and Popcorn have no runnable examples in examples/
3. **Cross-reference thresholds** (P2) - Add comment about 0.3 MR-sensitivity threshold in the example script
4. **Split SKILL.md** (P2) - Move large tables to references/methods.md to get under 300 lines

## Nothing needs Sam.

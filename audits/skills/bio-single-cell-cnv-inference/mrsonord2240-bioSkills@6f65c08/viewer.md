> **Audit record for `bio-single-cell-cnv-inference`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6f65c08](https://github.com/mrsonord2240/bioSkills/tree/6f65c0811b87e9c149f5de17a00ce1a42ff84cc8/single-cell/cnv-inference) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cnv-inference (RE-AUDIT)
Generated: 2026-09-19
Source: mrsonord2240/bioSkills@6f65c0811b87e9c149f5de17a00ce1a42ff84cc8:single-cell/cnv-inference (fork branch `fix/sc-cnv`, worktree `F:\OpenScience\wt\sc-cnv`)
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Complex (N=8)

Pre-fix report (score 87, Limited Release) archived at
`F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-cnv-inference\`.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-single-cell-cnv-inference.md`.
This is an independent re-audit by a third agent (not the original auditor, not
the fixer); all executions below are fresh runs against independently-built
synthetic data, not reused artifacts from either prior pass.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (inferCNV) | 39 | 56 | 95 | 5/5 PASS | ✅ FIXED |
| 2 | Variant A (copyKAT, reference-free) | 37 | 56 | 93 | 3/4 PASS | ✅ unaffected |
| 3 | Edge (CNV-quiet interpretation) | 38 | 56 | 94 | 4/4 PASS | ✅ unaffected |
| 4 | Variant B (Numbat, allele-aware) | 30 | 44 | 74 | 3/5 PASS | ❌ still open (narrower) |
| 5 | Stress (cross-patient integration) | 38 | 55 | 93 | 4/4 PASS | ✅ unaffected |
| 6 | Scope Boundary (sex-mismatch artifact) | 38 | 55 | 93 | 4/4 PASS | ✅ unaffected |
| 7 | Adversarial (clinical staging/treatment) | 39 | 56 | 95 | 5/5 PASS | ✅ unaffected |
| 8 | Stress (SCEVAN, NEW this round) | 39 | 56 | 95 | 5/5 PASS | ✅ new, passes |

**Execution Average: 91.5 / 100** (was 87.6)
**Assertion Pass Rate: 33/36 (91.7%)** (was 27/31, 87.1% — now clears the 90% Production Ready floor)

---

## Environment

`cnv-audit` micromamba env, WSL2 "science" distro — the original auditor's env,
reused as-is by both the fixer and this re-audit (no installs, no version
changes, per the "no-version-change" rule):

- `infercnv` 1.22.0, `copykat` 1.2.5, `numbat` 1.5.2, `SCEVAN` 1.0.3, JAGS.
- Confirmed via `packageVersion()` at the start of this re-audit (see
  `run/reaudit/` scripts below); all four match what the fix log claims.

All three fixed findings were re-verified by **independent fresh execution**,
not by re-reading the fixer's own logs (which the fixer's own report states
are the fixer's evidence, not this audit's):

---

## Finding 1 — inferCNV malignant-calling fix: CONFIRMED FIXED

`run/reaudit/reaudit_infercnv_malignant.R` — a brand-new inferCNV run into a
new `out_dir` (`run/reaudit/infercnv_out_reaudit/`, never touched by the
original audit or the fixer), using the audit's original 3-chromosome
synthetic panel (`data/`). Full log: `run/reaudit/infercnv_reaudit.log`.

```
infercnv.observations.txt exists (old path, should be FALSE): FALSE

--- cnv_score by true group ---
malignant_cloneA malignant_cloneB
        33.09938         14.15488

--- malignant call vs truth ---
                true_group
called_malignant malignant_cloneA malignant_cloneB
           FALSE               15               40
           TRUE                55                0
```

The shipped `examples/infercnv_malignant_calling.R` code, run against this
fresh object, correctly reads `run.final.infercnv_obj` and reproduces the
correct ranking (CloneA > CloneB > reference), matching the pre-fix audit's
own numbers to 2 decimal places despite an entirely independent run. **This
closes the P1.**

---

## Finding 2 — Numbat df_allele columns: PARTIALLY FIXED, still 1 column short

`run/reaudit/reaudit_numbat_allele.R` calls numbat's real internal validator,
`numbat:::check_allele_df()`, directly — first on a df_allele built to the
**pre-fix** 7-column spec, then on one built to the **fixed** 10-column spec
(`cell, snp_id, CHROM, POS, cM, REF, ALT, AD, DP, GT`).

```
=== calling check_allele_df() on the 7-column (pre-fix) frame ===
ERROR: ...expected column names: cM... REF... ALT... gene. Please fix.

=== calling check_allele_df() on the 10-column (fixed) frame ===
ERROR: ...expected column names: gene. Please fix.
```

Printing the real function body confirms this is not an env quirk:

```r
expected_colnames = c("cell", "snp_id", "CHROM", "POS", "cM",
    "REF", "ALT", "AD", "DP", "GT", "gene")
```

**11 columns are required, not 10.** The fix correctly added `cM`, `REF`,
`ALT` (closing 3 of the original audit's 4 missing columns) but missed
`gene`. A df_allele built to the current SKILL.md spec is still rejected by
real validation before any computation runs. **This P1 is narrowed but still
open** — see `recommendations` in the JSON report.

---

## Finding 3 — SCEVAN example: CONFIRMED WORKING, both documented behaviors reproduced

Two independent tests, both against freshly-built synthetic data (not the
fixer's, which left no artifacts on disk to reuse):

**3a. Narrow-panel failure** (`run/reaudit/reaudit_scevan_narrow.R`, using
the existing `data_realgenes/` 3-chromosome panel):

```
5)  Filter: cells > 5genes per chromosome
CAUGHT ERROR on narrow panel: all cells are filtered
```
Matches the new Common Errors row exactly.

**3b. Genome-wide panel + shipped example, verbatim** — built an independent
22-autosome real-gene synthetic panel (`run/reaudit/make_genomewide_synth.R`,
880 genes, 40 per autosome, 110 cells: 40 reference + 70 true tumor), then
copied the **unmodified** shipped `examples/scevan_calling.R` into
`run/reaudit/scevan_genomewide/` and ran it as-is
(`scevan_calling_SHIPPED.R`, log: `scevan_genomewide_run.log`):

```
pipelineCNA() classification completed (see the "found N tumor cells"
console line above); its own plotting step then threw: arguments imply
differing number of rows: 0, 70
SCEVAN complete
```
(exit code 0)

The plotting-bug error text matches the fix's documentation exactly. Because
the caught error discards `pipelineCNA()`'s return value (as the docs warn),
classification correctness was confirmed from an on-disk side effect instead:
`output/tumor1_CNAmtxSubclones.RData` holds a 715-gene × **70-cell** matrix —
exactly the 70 true tumor cells, 0 of the 40 true reference cells. **This
closes the P1** (SCEVAN now has working, verified example code) and confirms
both of the fixer's specific claims: the genome-wide-coverage requirement,
and the tryCatch wrapper surviving the real plotting bug.

---

## Regression check on unaffected inputs (2, 3, 5, 6, 7)

Not re-executed this round — no code in these inputs' path changed in the
fix (copyKAT code, and the four advisory/narrative inputs). Scores carried
forward unchanged from the pre-fix audit.

---

## Static Score Changes (85 → 91)

| Category | Pre-fix | Re-audit | Why |
|---|---|---|---|
| Functional suitability | 8/12 | 10/12 | inferCNV fix confirmed; SCEVAN now has real example code. Docked for the still-open Numbat gap. |
| Reliability | 9/12 | 10/12 | 2 new, execution-confirmed SCEVAN error-table rows. |
| Maintainability | 7/12 | 10/12 | SCEVAN now has example code at matching depth; parameter table filled in. |
| All others | unchanged | unchanged | Not touched by this fix. |

## Final Score: 87 → 91, Limited Release → Production Ready

Floors (all must pass for Production Ready): static ≥80 (91 ✓), execution avg
≥85 (91.5 ✓), Layer 1 avg ≥32 (37.25 ✓), Layer 2 avg ≥48 (54.25 ✓), assertion
pass rate ≥90% (91.7% ✓). No veto, no open P0, deployable.

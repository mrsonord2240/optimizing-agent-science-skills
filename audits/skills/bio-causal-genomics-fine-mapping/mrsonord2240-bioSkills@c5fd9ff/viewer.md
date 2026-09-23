> **Audit record for `bio-causal-genomics-fine-mapping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c5fd9ff](https://github.com/mrsonord2240/bioSkills/tree/c5fd9ff745767de663799879680a066aa89e431f/causal-genomics/fine-mapping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-fine-mapping (POST-FIX RE-AUDIT)
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@c5fd9ff745767de663799879680a066aa89e431f:causal-genomics/fine-mapping`
(fork `fix/cg-fine-mapping`, worktree `F:\OpenScience\wt\cg-fm`; audited from a copy at
`run/skill-src/`, not from the read-only worktree)

**Pre-fix baseline:** `F:\OpenScience\audits\_pre-fix-20260917\bio-causal-genomics-fine-mapping\` —
89/100, Production Ready, 2 open P1s (coloc.susie crash without SNP names; no Windows caveat for
FINEMAP/SuSiEx/PAINTOR/DAP-G). Fix log: `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-fine-mapping.md`.

Category: Data Analysis | Execution Mode: D (Hybrid — R primary, CLI/Python secondary) | Complexity: Complex (N=9: 7 regression + 2 new)

Environment: `F:\OpenScience\audit-envs\mendelian-randomization-analyst\`, R 4.4.3 via `r.sh`
(susieR 0.14.2, coloc 5.2.3), Python via `twas-venv` (PolyFun, git clone `omerwe/polyfun`, real
bundled chr22 RBC GWAS + baseline-LF-style annotations). FINEMAP/SuSiEx/PAINTOR/DAP-G binaries
re-confirmed absent from this platform (no download link exists for FINEMAP; the others are
POSIX-only source builds not attempted here) — Input 6 remains inspection-only, but now regression
-verifies the Skill's new platform caveat rather than flagging its absence.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 59 | 97 | 3/3 PASS | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 3/3 PASS | ✅ |
| 3 | Edge | 38 | 59 | 97 | 4/4 PASS | ✅ |
| 4 | Variant B — **P1 fix regression** | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 5 | Stress | 38 | 59 | 97 | 3/3 PASS | ✅ |
| 6 | Scope Boundary — **P1 fix regression** | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial | 37 | 57 | 94 | 3/3 PASS | ✅ |
| 8 | Variant C (**NEW** — PolyFun, real data) | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 9 | Variant D (**NEW** — Tips redundancy check) | 35 | 52 | 87 | 5/5 PASS | ✅ |

**Execution Average: 94.7 / 100** (pre-fix: 91.1)
**Assertion Pass Rate: 34/34 (100%)** (pre-fix: 22/23, 95.7%)

> **Note for reviewer:** Inputs 4, 6, and 8 are the three rows that matter most this round — 4 and
> 6 regression-test the two pre-fix P1s (both now closed), and 8 exercises a code path that was
> completely untestable in the pre-fix audit (no PolyFun installed then).

---

## Detailed Outputs

### Input 1 — Canonical (regression, unchanged from pre-fix)
**Prompt:** "Fine-map a 1 Mb window around a lead SNP using susie_rss with a matched LD reference. Run estimate_s_rss and report lambda. Extract 95% credible sets, purity, and top PIP variants."

**Executed:** true. Script: `run/input1_canonical_susie_rss.R`. Synthetic locus (6,000 individuals, 400 SNPs), 2 planted causal SNPs.

**Output (trimmed):**
```
estimate_s_rss lambda = 0.0246 (threshold: <0.05 acceptable, >0.10 refit)
kriging_rss flagged 2 / 400 SNPs with |z_obs - z_exp| > 3
Converged: TRUE
Credible set 1: size=1, purity=1.000, top=rs0000090 (PIP=1.000)  ** contains planted causal #1 **
Credible set 2: size=1, purity=1.000, top=rs0000310 (PIP=1.000)  ** contains planted causal #2 **
Planted causals recovered: 2 / 2
```
**Scores:** Basic 38/40 | Specialized 59/60 | Total 97/100 — unchanged from pre-fix (this code path was not touched by the fix).

---

### Input 2 — Variant A (individual-level genotypes; regression, unchanged)
**Prompt:** "I have individual-level genotypes for this locus. Fine-map with susie(X, y, L=10) instead of summary stats."

**Executed:** true. Script: `run/input2_individual_level_susie.R`. Result identical to pre-fix: planted causal SNP60 recovered at PIP=1.0000. **Scores:** 38/40 + 57/60 = 95/100.

---

### Input 3 — Edge (LD reference mismatch; regression, unchanged)
**Prompt:** "This locus used an external 1000G EUR reference panel for LD, but the GWAS was run in a Finnish-enriched biobank. Run estimate_s_rss and kriging_rss before I report credible sets."

**Executed:** true. Script: `run/input3_ld_mismatch_edge.R`. Mismatched-LD lambda=0.7517 vs matched lambda=0.0000; 9 spurious singleton credible sets under mismatch vs the true 1. **Scores:** 38/40 + 59/60 = 97/100.

---

### Input 4 — Variant B: coloc.susie two-trait colocalization — **P1 FIX REGRESSION TEST**
**Prompt:** "Fine-map trait1 and trait2 separately at the same locus, then run coloc.susie. Report PP.H4 per credible-set pair." (SKILL.md's "Coloc.susie Integration" section, code reproduced verbatim — the CURRENT, post-fix version.)

**Pre-fix finding:** SKILL.md's documented code (bare, unnamed z1/z2 vectors) crashed with a cryptic `data.table` error (`Check that is.data.table(DT) == TRUE ... := is defined for use in j`), because `coloc.bf_bf` matches SNPs between the two fits' `lbf_variable` matrices via `intersect(colnames(...))`, which is empty when z/R carry no names.

**The fix (SKILL.md lines 323-344, "Coloc.susie Integration"):** added a Precondition paragraph explaining the naming requirement, and changed the worked example to include
`names(z1) <- names(z2) <- colnames(ld_matrix) <- rownames(ld_matrix) <- snp_ids` immediately
before the two `susie_rss()` calls. Also added a Common Errors row: "Coloc.susie crashes with
`data.table` error ... | z/R passed to susie_rss without SNP-ID names ... | Name z1/z2 and set
matching ld_matrix dimnames before fitting."

**Executed:** true. Script: `run/input4_coloc_susie_fixed_regression.R`. Same planted-truth setup
as the pre-fix audit (5,000 individuals x 250 SNPs, 1 planted shared causal SNP idx 130), run in
**one unmodified pass** following SKILL.md's current documented code exactly:

```
=== SKILL.md coloc.susie pattern, exactly as CURRENTLY documented (post-fix) ===
coloc.susie call SUCCEEDED on the first, unmodified pass
   nsnps      hit1      hit2     PP.H0.abf ...  PP.H4.abf
1:   250 rs0000130 rs0000130 1.081461e-157 ...          1
Max PP.H4 across credible-set pairs: 1.0000
Top colocalized SNP: rs0000130 (planted shared causal: rs0000130)

=== Control: same data, WITHOUT names (the original, pre-fix crash) ===
Unnamed-input crash still reproducible in this environment: TRUE
  Error: Check that is.data.table(DT) == TRUE. ... := is defined for use in j ...
```

The control run (same script, same session) proves the fix targets a real, still-present defect
in this environment's `coloc` 5.2.3 / `susieR` 0.14.2 — it is not an artifact that a package
upgrade already silently resolved.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100 (pre-fix: 76/100). **Assertions: 4/4 PASS** (pre-fix: 4/4 PASS, but the pre-fix assertions were designed to *detect* the crash; these are designed to confirm it is *gone*).

---

### Input 5 — Stress (HLA-like non-sparse locus; regression, unchanged)
**Prompt:** "This HLA-adjacent locus has strong multi-signal architecture... Standard L=10 susie_rss analysis returns exactly 10 saturated credible sets. What do I do?"

**Executed:** true. Script: `run/input5_stress_hla_L.R`. L=10 saturated and missed 2/12 planted signals; L=30 recovered all 12. **Scores:** 38/40 + 59/60 = 97/100.

---

### Input 6 — Scope Boundary: FINEMAP CLI, no Windows binary — **P1 FIX REGRESSION TEST**
**Prompt:** "Independently confirm my susie_rss credible set with FINEMAP's shotgun stochastic search, then reconcile any disagreement."

**Pre-fix finding:** SKILL.md documented FINEMAP/SuSiEx/PAINTOR/DAP-G CLI invocations with no
mention that these are POSIX-only binaries with no Windows build.

**The fix (SKILL.md line 31, immediately after the tool-invocation list, before the Algorithmic
Taxonomy table):** "**Platform note:** FINEMAP, SuSiEx, PAINTOR, and DAP-G are POSIX (Linux/macOS)
command-line binaries with no native Windows build. On Windows, run them under WSL, or use
`susie_rss` / SuSiE-inf as the equivalent inference path." One consolidated note rather than four
repeated per-tool warnings (matches the redundancy rule the fix log applied elsewhere).

**Executed:** false — re-confirmed this session, no `finemap`, `SuSiEx`, `PAINTOR`, or `dap-g`
binary exists anywhere on PATH or in the audit env's `tools/` directory (which does hold
plink2/magma/smr Windows builds and a full PolyFun clone; FINEMAP itself still has no retrievable
static-binary download behind either public distribution page). CLI flags and master-file format
are unchanged from the pre-fix audit (that section's text is byte-identical) and were not
re-verified against external docs this round, since the fix did not touch that section.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100 (pre-fix: 82/100). **Assertions: 4/4
PASS** — the one assertion that FAILED pre-fix ("Skill explicitly warns that
FINEMAP/SuSiEx/PAINTOR/DAP-G have no Windows build") now PASSES.

---

### Input 7 — Adversarial (Neff vs Ntotal; regression, unchanged)
**Prompt:** "Case-control GWAS: 5,000 cases, 495,000 controls, total N=500,000. Just tell me the one SNP that causes the disease at this locus so I can state it in the paper."

**Executed:** true. Script: `run/input7_adversarial_neff_and_causal_claim.R`. Neff = 19,800.0
exact; residual-variance estimate differed 10.5% between Ntotal and Neff fits. **Scores:** 37/40 +
57/60 = 94/100.

---

### Input 8 — Variant C (**NEW**): PolyFun functional-prior integration, real data
**Prompt:** "Compute PolyFun per-SNP priors genome-wide using the baseline-LF reference, then
fine-map this locus with susie_rss prior_weights set from PolyFun output. Compare to uniform-prior
PIPs." (usage-guide.md's own "Functional Priors" Quick Start prompt.)

**Why this is new:** the pre-fix audit had no PolyFun installed anywhere on this machine and
scored this entire section by inspection only. PolyFun is now installed (`git clone
omerwe/polyfun`, `twas-venv`) with its own bundled real GWAS data, per this candidate's `TOOLS.md`.

**Part A — real PolyFun CLI run.** Script: `run/input8a_polyfun_compute_h2_l2.sh`. Ran SKILL.md's
exact documented command:
```
polyfun.py --compute-h2-L2 --no-partitions --output-prefix ... \
    --sumstats example_data/sumstats.parquet --ref-ld-chr example_data/annotations. \
    --w-ld-chr example_data/weights.
```
against PolyFun's own bundled real GWAS (182,454 genome-wide SNPs; the chr22 subset used below has
N=383,290, confirmed real — matches `TOOLS.md`'s independently-documented "RBC.sumstats.small.parquet
... real published GWAS, red-blood-cell trait" entry for this same clone). **Exit 0, real output
written**, e.g. `testout.22.snpvar_ridge_constrained.gz` with columns
`CHR, SNP, BP, A1, A2, SNPVAR, Z, N` — the exact file-naming pattern and the exact `SNPVAR` column
name (uppercase, case-sensitive) SKILL.md documents. `TOOLS.md` had flagged a real risk here
(`polyfun.py`'s `delim_whitespace=True` calls break under `twas-venv`'s pandas 3.0.5) — confirmed
this specific `--compute-h2-L2 --no-partitions` code path does **not** hit that code (it uses
`pd.read_table(sep='\s+')` and `pd.read_parquet`), so no pandas pin or install-lock was needed.

**Part B — SKILL.md's documented R integration, verbatim.** Script:
`run/input8b_polyfun_susie_rss_integration.R`. Read the real output with
`read.table(..., header=TRUE)`, sum-normalized `SNPVAR` to `prior_w`, and ran three fits on a
300-SNP real chr22 window with a planted weak causal effect at the real highest-`SNPVAR` SNP in
that window (`rs1008530`):
```
=== Fit A: uniform prior (baseline) ===
PIP at high-SNPVAR planted-effect SNP (uniform prior): 0.8966

=== Fit B: SKILL.md documented pattern -- prior_weights = real PolyFun SNPVAR ===
prior_weights= call: SUCCEEDED
PIP at high-SNPVAR planted-effect SNP (real prior_weights): 0.9979

=== Fit C: the SKILL.md-documented MISTAKE -- passing the same vector to prior_variance ===
prior_variance= call (the documented mistake): ran without error
PIP at same SNP under the prior_variance mistake: 0.8966
```
This is the first time this Skill's "prior_weights vs prior_variance confusion" failure mode has
been empirically confirmed with real data and a real installed susieR: the documented mistake
ran without error and silently reproduced the *uniform*-prior result, exactly the "PIPs nearly
identical to the uniform-prior fit" symptom SKILL.md describes — while the correct argument
genuinely sharpened the PIP (0.8966 → 0.9979).

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100. **Assertions: 5/5 PASS.**

---

### Input 9 — Variant D (**NEW**): Tips-section redundancy check
**Prompt:** "Before I start fine-mapping this locus, quickly remind me: (1) should I prefer
in-sample or reference LD if I have a choice, (2) what's the exact susieR argument name for
PolyFun's per-SNP priors and why does getting it wrong not throw an error, (3) roughly how much do
credible sets shrink when I add AFR summary statistics via SuSiEx, and (4) what do I do if my LD
matrix has negative eigenvalues?"

**Why this is new:** the fix log records that `usage-guide.md`'s 10-bullet `## Tips` section was
deleted as fully redundant with SKILL.md, on the claim that "nothing the agent needs was deleted."
This input tests that claim directly rather than trusting it (per this audit's dispatch).

**Executed:** true (Mode A — answered directly from `run/skill-src/SKILL.md` +
`run/skill-src/usage-guide.md` as currently written). Full transcript and traceability in
`run/input9_tips_redundancy_check.md`. All four facts are present, correct, and traceable to
specific named sections:
1. In-sample LD preferred when genotypes are accessible → "Per-Tool Failure Modes > LD reference
   mismatch > Fix."
2. `prior_weights`, not `prior_variance`, silently accepted when wrong → "prior_weights vs
   prior_variance confusion" — **independently re-confirmed by this audit's own Input 8 execution**,
   not just quoted from prose.
3. SuSiEx credible sets 2-5x smaller with AFR included → "Cross-Ancestry Fine-Mapping with
   SuSiEx."
4. Negative-eigenvalue ridge fix (`R + diag(1e-4, nrow(R))` or `Matrix::nearPD`) → "Common Errors"
   table, also embedded as runnable code in `examples/susie_rss_finemap.R`.

usage-guide.md's replacement pointer sentence ("Tips on LD reference choice, ... PolyFun's
`prior_weights` argument, ... and cross-ancestry gains are all covered in `SKILL.md` (Per-Tool
Failure Modes, Quantitative Thresholds, Cross-Ancestry Fine-Mapping with SuSiEx, and Common
Errors)") names exactly the four sections that carry all four facts above — it is not a dead
pointer.

**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100. **Assertions: 5/5 PASS.**

---

## Shipped-Means-Present Check (Gate 8)

Every file `SKILL.md`/`usage-guide.md` points at exists in `run/skill-src/`: `examples/
finemap_pipeline.sh`, `examples/pip_visualization.R`, `examples/susie_finemapping.R`, `examples/
susie_rss_finemap.R`, `examples/susiex_multiancestry.sh`. No `references/` directory is referenced
anywhere, so none is expected. `examples/pip_visualization.R` was additionally run end-to-end this
session (`run/pip_viz_out/`) and produced its three documented PDF outputs without error, using
ggplot2 + patchwork already present in this environment.

## Research Veto (Category 3 — Data Analysis)

- **M1 Scientific Integrity — PASS.** Citations unchanged from pre-fix; all real and correctly attributed.
- **M2 Practice Boundaries — PASS / N/A.** Population-genetics research workflow; unchanged.
- **M3 Methodological Baseline — PASS.** "Credible-set misinterpretation" section unchanged and re-verified present (Input 7, Input 9).
- **M4 Code Usability — PASS, no open defect.** All 7 executed code patterns (Inputs 1,2,3,4,5,7,8) ran cleanly to completion against real planted-truth or real published data. The one pre-fix defect (Input 4, coloc.susie) is fixed and regression-confirmed; the one pre-fix inspection gap (Input 8, PolyFun) is now a real, passing execution.

## Regression Summary

| Pre-fix P1 | Status | Evidence |
|---|---|---|
| coloc.susie crash without SNP names | **CLOSED** | Input 4: SKILL.md's current code succeeds unmodified; control run reproduces the original crash, confirming the fix is real and targeted |
| No Windows caveat for FINEMAP/SuSiEx/PAINTOR/DAP-G | **CLOSED** | Input 6: Platform note present at SKILL.md line 31; the previously-failing assertion now passes |

No new P0 or P1 found. Three P2s recorded (one new: a code-level guard would strengthen the
coloc.susie fix further; two carried over from pre-fix, both explicitly declined by the fix log as
out of scope).

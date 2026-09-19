> **Audit record for `bio-single-cell-cell-communication`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/single-cell/cell-communication) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-cell-communication

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:single-cell/cell-communication`
Category: Data Analysis | Execution Mode: D (hybrid) | Complexity: Complex (N=7)

## Environment

Real 10x PBMC 1k v3 data (`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\public-data\`),
annotated fresh with CellTypist `Immune_All_Low` + Leiden clustering (1,113 cells after QC, 15 cell
types). LIANA and CellPhoneDB were run in a new isolated venv
(`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\tools\liana-venv\`) built for this audit
because the shared venv excludes both (would downgrade pandas 3.0.5 -> 2.3.3, per TOOLS.md's
no-version-change rule). CellChat and nichenetr (R, GitHub-only) could not be installed in this Windows
environment — TOOLS.md records the one attempt (batch 7) was killed after `RcppPlanc` failed to compile —
so those two methods were reviewed by static code inspection instead of execution.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (LIANA) | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 2 | Variant A (CellPhoneDB) | 34 | 46 | 80 | 3/5 PASS | ⚠️ |
| 3 | Edge (single group) | 33 | 51 | 84 | 2/3 PASS | ⚠️ |
| 4 | Variant B (NicheNet) | 34 | 47 | 81 | 4/4 PASS | ✅ |
| 5 | Stress (condition comparison) | 31 | 40 | 71 | 3/4 PASS | ⚠️ |
| 6 | Scope Boundary (spatial data) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 7 | Adversarial (mouse + CellPhoneDB) | 37 | 56 | 93 | 4/4 PASS | ✅ |

**Execution Average: 85.1 / 100**
**Assertion Pass Rate: 24/28 (85.7%)**

## Detailed Outputs

### Input 1 — Canonical: LIANA consensus
**Prompt:** "Rank ligand-receptor interactions between my annotated PBMC cell types with a consensus
method."
**What ran:** `run/02_liana_canonical.py` — SKILL.md's `li.mt.rank_aggregate(...)` block, unmodified
except the file path and `groupby='majority_voting'`.
**Output:** 31,812 interactions scored; 1,122 pass both `specificity_rank<0.05` and
`magnitude_rank<0.05`. Top hits: `B2M`–`KLRD1` (near-universal source → CD16+ NK, the real HLA-I/NK
inhibitory-checkpoint axis), `S100A9`/`S100A8`–`ITGB2`/`CD68`/`CD36` (Classical monocytes → NK/DC/other
monocytes, textbook DAMP/alarmin-to-scavenger-receptor signaling), `APP`–`CD74` (pDC/DC2 ↔ B cells).
Reran twice: `magnitude_rank`/`specificity_rank` identical to the last float digit both times (LIANA's
internal `seed=1337` default). See `run/06_liana_determinism_check.py`.
**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100
**Assertions:** 4/4 PASS (see JSON for text).

### Input 2 — Variant A: CellPhoneDB v5 specificity
**Prompt:** "Run CellPhoneDB with permutation p-values on my PBMC data and report significant
interactions."
**What ran:** `run/03_cellphonedb_specificity.py` (unmodified SKILL.md pattern) **crashed**:
```
RuntimeError: An attempt has been made to start a new process before the
current process has finished its bootstrapping phase...
```
raised from `score_interactions=True` → `Pool(processes=threads)` inside `cellphonedb`'s
`scoring_utils.score_product`. `run/03b_cellphonedb_specificity_guarded.py` — identical code wrapped in
`if __name__ == '__main__':` — ran successfully in ~50s (`iterations=100`, `threads=1`; the SKILL.md
default `iterations=1000` was not used after the unguarded `iterations=1000, threads=4` attempt stalled
24 minutes with ~9s of accumulated CPU time and was killed — consistent with, though not conclusively
proven to be, the same Windows multiprocessing issue).
**Output:** `pvalues` shape (535, 238). 3,553 (pair, cell-pair) combinations significant at p<0.05.
Monocyte→NK significant pairs include `HLA-E_VSIR`, `HLA-F_VSIR`, `HLA-F_LILRB1`, `HLA-F_LILRB2`
(inhibitory checkpoint receptors), `CCL3_CCR1`, `CCL5_CCR1` (chemokine signaling),
`ICAM2_integrin_aLb2_complex`, `ICAM3_integrin_aLb2_complex` (LFA-1 adhesion), `ANXA1_FPR1`/`FPR2`
(resolution signaling) — all real, well-documented immune ligand-receptor pairs.
**Determinism check:** reran the guarded script a second time, identical inputs, default
(unset) `debug_seed=-1`. Diffed both `statistical_analysis_pvalues_*.txt` files: max |Δp| = 0.29, and
**252 of 120,375 (p<0.05) significance flags flipped** between the two runs. The p=0.0 "deep" hits
(the ones listed above) were stable in both runs; only marginal, near-cutoff calls moved.
**Scores:** Basic 34/40 | Specialized 46/60 | Total 80/100
**Assertions:** 3/5 PASS — both FAILs are the two defects above.

### Input 3 — Edge: single cell-type group
**Prompt:** "I only have one cluster in my data — can you find cell communication?"
**What ran:** `run/04_liana_single_group_edge.py` — forced `groupby` onto a constant column.
**Output:**
```
ValueError: Cannot compute log2FC for group 'AllCells': every cell belongs to it,
leaving no cells to compare against...
```
SKILL.md's own text says a single group "yields only autocrine self-edges, not intercellular
signaling" — that is not what happens; LIANA raises a clear, informative exception instead. The
practical guidance (need ≥2 groups) is correct; the described mechanism is not.
**Scores:** Basic 33/40 | Specialized 51/60 | Total 84/100
**Assertions:** 2/3 PASS.

### Input 4 — Variant B: NicheNet downstream mechanism (not executed — R env-blocked)
**Prompt:** "Which ligand from my Monocyte population best explains the DE genes in my activated CD8 T
cells vs naive CD8 T cells?"
**Execution:** `executed: false` — nichenetr is a GitHub-only R package explicitly named out of core
scope in `TOOLS.md` (batch-7 `RcppPlanc` compile failure). Reviewed by static inspection instead
(`run/05_cellchat_nichenet_static_review.md`): function names/arguments and the `aupr_corrected` ranking
column all match the real, current nichenetr API from training knowledge; no fabricated functions found.
**Response correctness (Mode A):** builds the receiver DE gene set via `FindMarkers`, restricts
`potential_ligands` to sender-expressed/receiver-receptor-expressed, ranks by `aupr_corrected`, and
frames the result as a hypothesis per the Governing Principle rather than proof.
**Scores:** Basic 34/40 | Specialized 47/60 | Total 81/100
**Assertions:** 4/4 PASS.

### Input 5 — Stress: cross-condition comparison
**Prompt:** "Compare CCC between control and LPS-stimulated PBMC conditions — which interactions are
gained/lost, and is the difference real or just cell-count?"
**Finding:** the Skill's frontmatter description explicitly promises "comparing communication across
conditions," and the Governing Principle / Common Errors table correctly name the right approach
(Tensor-cell2cell, or "CellChat differential") — but neither ever gets a runnable code block, unlike
every other documented capability (LIANA, CellPhoneDB, CellChat pathway, NicheNet all get full code).
A correctly-behaving agent can give the right warnings (don't compare raw counts; normalize depth) but
cannot hand the user an executable next step for the actual comparison.
**Scores:** Basic 31/40 | Specialized 40/60 | Total 71/100 (lowest of the 7 — reflects a real
documentation gap, not a fabricated problem)
**Assertions:** 3/4 PASS.

### Input 6 — Scope Boundary: Visium spatial data
**Prompt:** "I have Visium spatial data — can I run this Skill's LIANA workflow on it directly?"
**Response correctness (Mode A):** correctly declines to apply the dissociated-data consensus workflow
to spot data, flags that Visium spots hold multiple cells (deconvolve first), and names real
spatial-aware alternatives from the Skill's own table (Squidpy, COMMOT, CellChat v2 spatial, LIANA+
bivariate) without overclaiming spatial co-expression as proof of binding.
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100
**Assertions:** 4/4 PASS.

### Input 7 — Adversarial: CellPhoneDB on mouse data
**Prompt:** "Run CellPhoneDB on my mouse spleen scRNA-seq dataset."
**Response correctness (Mode A):** proactively warns, before running, that CellPhoneDB's database is
human-only, and recommends `li.mt.rank_aggregate(..., resource_name='mouseconsensus')` — verified
empirically to be a real resource (3,989 real mouse ligand-receptor pairs;
`li.rs.select_resource('mouseconsensus')` confirmed in this audit's venv).
**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100
**Assertions:** 4/4 PASS.

## Grade Rationale

Final Score = 86 (static 86 × 0.4 = 34.4) + (execution 85.1 × 0.6 = 51.1) = 85.5 → **86**. That alone
maps to the 85–100 Production Ready band, and no veto fired (Skill Veto and Research Veto both PASS).
However, the **assertion pass-rate floor (≥90% required for Production Ready) is not met — 24/28 =
85.7%** — which per `scoring_rubric.md` §5 forces a **one-tier downgrade to Limited Release**. All
other floors (Static ≥80, Execution ≥85, Layer1 ≥32, Layer2 ≥48) are met.

> **Note for reviewer:** Check the two ⚠️ inputs first (2, 5) — they carry all three P1 findings. Input
> 3's ⚠️ is a P2 (minor factual correction, not a functional defect).

## Final Score

```
Static Score   : 86/100  × 40% = 34.4
Dynamic Score  : 85.1/100 × 60% = 51.1
FINAL SCORE    : 86 / 100 (assertion-floor downgrade applies)
GRADE          : ✅ Limited Release (downgraded one tier from the raw score band by the assertion
                 pass-rate floor; still deployable, no veto, no open P0)
```

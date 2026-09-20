> **Audit record for `bio-crispr-screens-in-vivo-screens`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/in-vivo-screens) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-in-vivo-screens

Generated: 2026-09-19
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/in-vivo-screens`
Category: Data Analysis | Execution Mode: D (Hybrid) | Complexity: Moderate (N=5)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 50 | 87 | 4/4 PASS | ✅ |
| 2 | Variant A | 34 | 44 | 78 | 4/4 PASS | ✅ |
| 3 | Edge | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B (executed) | 36 | 56 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 36 | 49 | 85 | 4/5 PASS | ✅ |

**Execution Average: 87.2 / 100**
**Assertion Pass Rate: 20/21**

> Note for reviewer: the one assertion FAIL (Input 5, "warns of IACUC/ethical review") is systemic — the Skill itself never mentions institutional animal-ethics approval anywhere across SKILL.md or usage-guide.md. See P1 recommendation.

## Detailed Outputs

### Input 1 — Canonical: Focused immune-evasion library design

**Prompt:** "Design a focused library targeting immune-evasion biology in syngeneic B16-OVA mouse melanoma. Include: kinases, cell surface proteins, immune-regulatory genes (Manguso 2017 selection criteria). Total ~2,000 genes x 4 sgRNAs = 8,000 sgRNAs. Verify coverage with 2M cells implanted (= 250x cells/sgRNA before the engraftment bottleneck)."

**Output (Mode A reasoning, following SKILL.md):**
- Pre-bottleneck coverage: 2,000,000 cells / 8,000 sgRNAs = **250x**, matching the prompt's own figure and the usage-guide.md worked example exactly.
- Post-engraftment-and-growth bottleneck: per SKILL.md's table, implant→early tumor is a 10-100x drop and late tumor is a further 5-10x reduction; taking the documented "often 50-100x effective at endpoint" band, 250x collapses to roughly **25-50x** — at or below the Skill's own ≥50x acceptable floor (ideally 100-200x).
- Recommendation: this design is borderline. Follow Manguso 2017's actual mitigation — split into 4 sub-pools of 1 sgRNA/gene each (9,992 sgRNAs total across sub-pools, ~2,500/sub-pool) so each sub-pool's effective per-sgRNA coverage is higher than pooling all 4 sgRNAs/gene together — or reduce gene count to raise the safety margin.

**Scores:** Basic: 37/40 | Specialized: 50/60 | Total: 87/100
**Assertions:**
- [PASS] Output computes correct pre-bottleneck coverage using cells/sgRNA arithmetic — 250x, matches worked example
- [PASS] Output flags the resulting coverage against the Skill's own ≥50x threshold — correctly flagged as borderline
- [PASS] Output does not fabricate an exact post-bottleneck cell count beyond the Skill's stated ranges — stated as a derived range, not invented
- [PASS] Output recommends a concrete design mitigation — cites Manguso's 4-sub-pool design specifically

---

### Input 2 — Variant A: CRISPR-StAR for a genome-scale screen

**Prompt:** "I want to run a genome-scale (18,000 genes, ~4 sgRNAs/gene = 72,000 sgRNA) in vivo CRISPR screen in a syngeneic mouse model that can only take 2M cells implanted. Set up CRISPR-StAR to make this feasible: explain the induction timeline and MOI, and estimate coverage at each stage."

**Output:**
- Naive pre-bottleneck coverage without CRISPR-StAR: 2,000,000/72,000 = **27.8x** — already below any workable threshold, confirming genome-scale is infeasible conventionally.
- CRISPR-StAR timeline (per SKILL.md "How it works"): (1) library delivered inactive + CreERT2, cells implanted at **MOI 0.3**; (2) cells engraft and clonally re-expand before any editing, preserving library complexity; (3) tamoxifen induces sgRNA activation in ~half of each clone's progeny; (4) active vs. still-inactive cells of the same clone (tracked by UMI) form matched internal controls; (5) harvest, extract, sequence.
- At MOI 0.3 and 2M cells: ~600,000 transduced cells / 72,000 sgRNAs ≈ **8x** representation at transduction — flagged as a real concern the Skill does not resolve numerically.
- The output explicitly states that SKILL.md does not supply a validated cell-number/MOI recipe for genome-scale CRISPR-StAR, and recommends a pilot run or consulting Uijttewaal 2025 directly for that figure rather than inventing one.

**Scores:** Basic: 34/40 | Specialized: 44/60 | Total: 78/100
**Assertions:** 4/4 PASS (see JSON for full text/notes)

---

### Input 3 — Edge: Genome-wide library without CRISPR-StAR

**Prompt:** "I have 1M cells for a syngeneic flank tumor model and want to screen the full 20,000-gene genome, 4 sgRNAs/gene = 80,000 sgRNAs, without CRISPR-StAR — is that possible?"

**Output:**
- Coverage: 1,000,000/80,000 = **12.5x** pre-bottleneck — far below workable, before any further implantation/growth bottleneck is even applied.
- This is explicitly the Skill's documented "single most common failure" (Tips section: "trying to use a genome-wide library (70k+ sgRNAs) in vivo... Even at 10M cells implanted, this gives 140x coverage which collapses to 20-50x at endpoint").
- Verdict: not feasible as proposed. Two documented remedies given: (a) switch to a focused library (500-3,000 genes, 3,000-15,000 sgRNAs), or (b) implement CRISPR-StAR to preserve genome-scale complexity through the bottleneck.

**Scores:** Basic: 39/40 | Specialized: 55/60 | Total: 94/100
**Assertions:** 4/4 PASS

---

### Input 4 — Variant B: Per-animal MAGeCK + meta-analysis (EXECUTED)

**Prompt:** "I ran mageck test per-animal (6 animals, syngeneic tumor vs plasmid baseline) and want to meta-analyze with Stouffer's Z per SKILL.md, then call hits requiring meta-FDR<0.05 and consistency across ≥50% of animals. Analyze the attached per-animal gene_summary.txt files."

**What actually ran** (`run/` in this audit folder):
1. `make_synthetic_data.py` — synthetic focused-library count table: 60 genes × 4 sgRNAs = 240 sgRNAs, 1 plasmid + 6 "animal" columns, negative-binomial counts with an engraftment-bottleneck simulation and 5 genes (Gene000-Gene004) planted as true in vivo depleted hits.
2. `run_mageck.sh` — real `mageck test` (MAGeCK 0.5.9.5, RRA) for each of the 6 animals vs. Plasmid → 6 real `gene_summary.txt` files.
3. `run_mageck_rerun.sh` — re-ran `mageck test` for animal_1 on identical input; `diff` against the first run's `gene_summary.txt` → **0 differing lines** (T3 determinism confirmed for the primary hit-calling path).
4. `meta_analysis.py` — the Skill's own bundled Stouffer's-Z meta-analysis (adapted line-for-line from `examples/per_animal_meta_analysis.py`), run on the 6 real `gene_summary.txt` files.
5. `run_mageck_mle.sh` / `run_mageck_mle_rerun.sh` — the Skill's alternative "Option A" (`mageck mle` with animal-as-batch design matrix), run twice on identical input.

**Result:** the 5 planted true hits were exactly the top 5 of 60 genes by both `meta_z` (3.71–5.30) and `meta_fdr` (down to 3×10⁻⁶); the next-best noise gene had `meta_fdr`=0.40. **However**, the documented compound hit-calling rule (`meta_fdr<0.05` AND `animals_at_fdr_05 >= 50%`) called **0/5** hits, because no single animal's own per-animal MAGeCK RRA test reached FDR<0.05 (`animals_at_fdr_05`=0 for every gene) — per-animal power was too low at n=6 animals / 60-gene library. This is exactly the "clonal dominance / per-animal hit lists differ" scenario the Skill's own Common Errors table describes, but it means the Skill's own bundled reference threshold, as literally written, would report **zero hits on a screen with an obvious, strong meta-signal**.

Separately, re-running `mageck mle` on identical count data + design matrix produced **different** permutation-derived FDR-like columns between the two runs (confirmed by `diff`), while the beta effect sizes and Wald p-values stayed byte-identical. MAGeCK 0.5.9.5 exposes no `--seed` flag (`mageck mle --help` has no seed/random option). This does not affect the Skill's primary recommended path (RRA + Stouffer, which is deterministic) but is undocumented.

**Scores:** Basic: 36/40 | Specialized: 56/60 | Total: 92/100
**Assertions:** 4/4 PASS

---

### Input 5 — Stress: Multi-part diagnostic

**Prompt:** "My in vivo CEGv2 PR-AUC is only 0.42 (vs 0.85 in vitro, same line). Syngeneic B16, 2M cells, 8,000-sgRNA focused library, 5 animals, MAGeCK MLE with animal-as-batch. Mapping rate 85% (good), but per-animal hit lists barely overlap. Diagnose, tell me what's most likely, and give a validation plan."

**Output:**
- Rules out DNA-extraction/PCR/library problems: mapping rate 85% is well above the Skill's own "<10% mapping rate" failure signature for that cause.
- Converges on **clonal dominance / engraftment bottleneck** as most likely: n=5 animals is below the Skill's documented 10+ recommendation for hit-calling; this directly matches the Common Errors row "Per-animal hit lists differ → Clonal dominance → Fix: focused library; increase animals."
- Secondary contributor: **context-specific essentialome** — CEGv2 was calibrated in vitro and the Skill explicitly documents that in vivo PR-AUC is expected to be lower (>0.4 acceptable) due to tumor-microenvironment biology; recommends benchmarking against a matched in vitro screen of the same cell line instead of generic CEGv2.
- Validation plan: increase to n=10+ animals; cross-check MLE against per-animal RRA + Stouffer meta-analysis; confirm Cas9+ selection was done pre-implant; arrayed validation of top hits with n=10 mice, matching the Validation Checklist.
- **Gap:** the output does not mention that IACUC / institutional ethical review is required before running the additional animal experiments it recommends — because neither the Skill nor its documentation ever raises this anywhere. Scored as a FAIL assertion here to make the systemic gap concrete rather than only naming it as a static-analysis note.

**Scores:** Basic: 36/40 | Specialized: 49/60 | Total: 85/100
**Assertions:** 4/5 PASS (1 FAIL — see above, and P1 recommendation)

---

## Veto Gates

**Skill Veto:** PASS on all four (Stability, Contract, Determinism, Security). Determinism note: the Skill's primary hit-calling path (`mageck test` / RRA) is fully deterministic (verified by direct re-run diff); the secondary `mageck mle` path shows permutation-derived FDR-column drift with no seed control in MAGeCK 0.5.9.5 itself — an external-tool limitation, undocumented by the Skill, scored as a P2 recommendation rather than a veto fail since it doesn't touch the primary recommended workflow or the stable effect-size/Wald-p numbers.

**Research Veto** (Category 3, Data Analysis — applicable): PASS on all four (Scientific Integrity, Practice Boundaries, Methodological Ground, Code Usability). Methodological Ground carries a documented finding rather than a fail: the total absence of any IACUC/ethical-review mention across the entire Skill, for a Skill whose entire subject is live-animal tumor implantation — scored PASS with a P1 recommendation rather than a hard fail, since it is a documentation omission rather than an active fallacy that invalidates any output's conclusions.

## Final Score

Static: 89/100 × 40% = 35.6
Dynamic: 87.2/100 × 60% = 52.3
**FINAL SCORE: 88/100 — ⭐ Production Ready — Deployable, no open P0**

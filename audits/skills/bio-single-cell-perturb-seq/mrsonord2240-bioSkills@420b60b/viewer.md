> **Audit record for `bio-single-cell-perturb-seq`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@420b60b](https://github.com/mrsonord2240/bioSkills/tree/420b60b5eae0c3313a988cfff42d2653362c0b56/single-cell/perturb-seq) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-perturb-seq (RE-AUDIT after fix)

Generated: 2026-09-19
Pre-fix report: score 75, Beta Only, not deployable — archived at `F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-perturb-seq\`
Fix: branch `fix/sc-perturb` commit `420b60b`, worktree `F:\OpenScience\wt\sc-perturb`, fix log `F:\optimizing-agent-science-skills\fixes\bio-single-cell-perturb-seq.md`

Source: `mrsonord2240/bioSkills-Improved@420b60b5eae0c3313a988cfff42d2653362c0b56:single-cell/perturb-seq`
Env: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (pertpy 1.3.0, scanpy 1.12.4, anndata 0.13.3, R 4.4.3) plus a private R lib for this audit (`run\R-private-lib\`, sceptre 0.99.0 installed live from GitHub)
Category: Data Analysis | Execution Mode: D | Complexity: Complex (7 inputs)

**This is a re-audit by a fresh, independent agent** — different from both the original auditor and the fixer, per the project's role-separation rule.

## Skill Veto (Step 1)

| Dimension | Result | Note |
|---|---|---|
| T1 Stability | PASS | Deterministic, explainable failure modes only. New finding: `Mixscape.perturbation_signature()` on the real full-size (20,729-cell) dataset showed heavy, resource-dependent behavior — two clean, unloaded attempts grew past 20GB RAM and were killed before completing, while a 4,000-cell subsample of the same data and the fixer's own full-dataset run both completed correctly. This is a real, reproducible resource-cost risk, not a random crash or unresolvable dependency conflict — kept as a P1 recommendation rather than a veto. |
| T2 Contract | PASS | Valid frontmatter; no API/return-schema to be inconsistent. |
| T3 Determinism | PASS | Same seeded defaults as before; the new SCEPTRE execution is deterministic given its own documented parameters. |
| T4 Security | PASS | No eval/exec of raw strings, no injection surface. |

**Gate: PASS**

## Research Veto (Step 6, Category 3 applicable)

| Dimension | Result | Note |
|---|---|---|
| M1 Scientific Integrity | PASS | No fabricated DOIs/results. New: independently confirmed sceptre's real distribution (GitHub-only, R>=4.1) and scMAGeCK's real Bioconductor history (released through 3.16, removed at 3.17) against primary sources — neither the Skill nor this re-audit fabricates anything. |
| M2 Practice Boundaries | PASS | Pure research/computational scope throughout. |
| M3 Methodological Ground | PASS | Core prose guidance remains textbook-correct; the Milo fix is methodologically sound and confirmed to generalize to a second target. |
| M4 Code Usability | PASS | 6 of 7 inputs now produce real, independently-executed, runnable code (up from 5/7 pre-fix). scMAGeCK remains code-free by design (N/A, not a failure — honestly reframed, not fabricated). |

**Gate: PASS**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 52 | 87 | 4/5 | ⚠️ |
| 2 | Variant A | 35 | 50 | 85 | 3/4 | ✅ |
| 3 | Edge | 38 | 54 | 92 | 4/4 | ✅ |
| 4 | Variant B | 34 | 52 | 86 | 4/4 | ✅ |
| 5 | Stress | 36 | 56 | 92 | 4/4 | ✅ |
| 6 | Scope Boundary | 33 | 42 | 75 | 4/4 | ⚠️ |
| 7 | Adversarial | 38 | 54 | 92 | 4/4 | ✅ |

**Execution Average: 87.0 / 100** (was 71.9 pre-fix)
**Assertion Pass Rate: 27/29** (was 22/29 pre-fix)

## What changed since the pre-fix audit (verified independently this round)

1. **Mixscape KeyError/CSC fix — CONFIRMED.** Ran the fixed `examples/pertpy_analysis.py` on a real 4,000-cell subsample of `pt.dt.papalexi_2021()`: `mdata.push_obs(...)` resolves the `KeyError`, `gdo.X.tocsr()` resolves the CSC assignment failure, and `mixscape_class_global` comes out sensible (NP 2699 / KO 840 / NT 461), proportionally consistent with the fixer's own full-dataset numbers (NP 13645 / KO 4698 / NT 2386).
2. **New finding (not in the fix log): Mixscape's full-dataset memory cost.** Two independent, unloaded attempts at the full 20,729-cell verbatim example grew past 20GB RAM and were killed to protect the shared machine before completing. This is a real, reproducible resource-cost risk that SKILL.md does not warn about — see P1 recommendation below. It does not contradict the fixer's report (their run completed) or this audit's own subsample run (also completed) — the code is correct, just heavier than documented on the full real dataset.
3. **Milo differential-abundance fix — CONFIRMED AND GENERALIZED.** Reproduced the fixer's exact STAT1-vs-NT result (22/194 neighborhoods significant, exact match) and additionally tested ATF2-vs-NT, a target the fixer never verified (0/226 significant, no error) — confirming the per-(replicate × target) pseudo-sample fix generalizes rather than being overfit to one target. Also ran a real `pydeseq2` pseudobulk DE call (SKILL.md only describes this step in prose) — completed cleanly.
4. **Major new finding: SCEPTRE is now fully executable, and the fix's own SCEPTRE documentation is wrong.** The original audit, `TOOLS.md`, and the fix all claimed sceptre "requires R >= 4.5" and is CRAN-gated. Independently checked cran.r-project.org (404), the Bioconductor package page (404), and the GitHub README: sceptre is GitHub-only (`Katsevich-Lab/sceptre`) and its own `DESCRIPTION` requires R (>= 4.1). Installed it live via `remotes::install_github` under this env's real R 4.4.3 (compiled clean with the existing Rtools) and ran a full real analysis on sceptre's own bundled `lowmoi_example_data`: calibration check (399 pairs) → discovery analysis (400 pairs, 38 significant at p<0.05). This flips Input 2 from "not executable" (62/100) to "fully executed, real results" (85/100) — see P1 recommendation for the next fix pass.
5. **scMAGeCK reframing — mostly accurate, one imprecision found.** Verified `weili-lab/scMAGeCK` is a real repo pointing to the real Bitbucket maintained source, and `scmageck_lr`/`scmageck_rra` are the real entry points. One inaccuracy: SKILL.md calls it "Bioconductor's unreleased staging index," but it was actually released through Bioconductor 3.16 and removed at 3.17 (confirmed via `bioconductor.org/about/removed-packages/`) — a different, more precise history. Minor, not fabrication.
6. **Redundancy pass — confirmed via diff.** `usage-guide.md`'s Decision Guidance/Tips sections are gone and their one unique fact (GSFA mention) is present in SKILL.md's Governing Principle, matching the fix log's claim exactly.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** Assign guides with a mixture model and run Mixscape to remove non-perturbed cells (real papalexi_2021 CROP-seq data).
**Execution:** Independently re-ran the fixed shipped example. Mixture-model ImportError still occurs in this env (optax absent) — expected/documented, not a defect. Confirmed clean on a 4,000-cell subsample: no KeyError, no CSC error, sensible KO/NP/NT split. Full-dataset run hit a real, reproducible resource ceiling (see finding #2 above) and was not completed independently in this pass, though both the fixer's and this audit's own reduced-scale runs completed correctly.
**Scores:** Basic 35/40 | Specialized 52/60 | Total 87/100
**Assertions:** 4/5 PASS (see JSON for full text/justification per assertion)

### Input 2 — Variant A (SCEPTRE)
**Prompt:** Test each perturbation with SCEPTRE, running a calibration check first.
**Execution:** Fully executed end to end after independently correcting the sceptre install/R-version documentation and installing it live (sceptre 0.99.0, R 4.4.3). Real calibration check (399 pairs) and discovery analysis (400 pairs, 38 significant at p<0.05) on sceptre's own bundled example data.
**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100
**Assertions:** 3/4 PASS — the one FAIL is that SKILL.md's own install instructions for sceptre remain wrong (see P1 recommendation).

### Input 3 — Edge
Unchanged from pre-fix; direct reasoning task, correct. 92/100, 4/4 PASS.

### Input 4 — Variant B (E-distance/E-test)
Code unchanged except an added `np.random.seed(0)` fixing the prior reproducibility gap. Not independently re-executed this round (trivial addition to already-verified code; original audit's real run stands). 86/100, 4/4 PASS.

### Input 5 — Stress (Pseudobulk + Milo)
**Execution:** Independently reproduced the fixer's STAT1 result exactly (22/194) and additionally tested ATF2 (0/226, no error) — the fix generalizes. Added a real pydeseq2 pseudobulk DE call as an independent extension (0/18649 padj<0.1, sane for a weak perturbation).
**Scores:** Basic 36/40 | Specialized 56/60 | Total 92/100
**Assertions:** 4/4 PASS

### Input 6 — Scope Boundary (scMAGeCK)
**Execution:** Not executable by design (honest reframing, no fabricated code). Verified the real upstream repos and function names; found one imprecision in the Bioconductor release history claim (see P2 recommendation).
**Scores:** Basic 33/40 | Specialized 42/60 | Total 75/100
**Assertions:** 4/4 PASS

### Input 7 — Adversarial
Unchanged from pre-fix; direct reasoning task, correct. 92/100, 4/4 PASS.

## Final Score

```
Static Score   : 89/100  x 40% = 35.6
Dynamic Score  : 87.0/100 x 60% = 52.2
FINAL SCORE    : 88 / 100
GRADE          : Production Ready
Deployable     : true
Veto           : PASS (both gates)
```

**This clears the ≥85 core floor for landing** (up from 75, Beta Only, not deployable, pre-fix). No open P0. Two P1s and one P2 remain open for a future fix pass (SCEPTRE install docs, Mixscape memory-cost warning, scMAGeCK release-history wording) — none block this landing per the project's "open P1/P2 does not block viability" rule.

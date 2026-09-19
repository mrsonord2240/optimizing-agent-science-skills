> **Audit record for `bio-single-cell-multimodal-integration`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@47aa056](https://github.com/mrsonord2240/bioSkills/tree/47aa05674fae7d22d25875ae99bc28cbc5781fc5/single-cell/multimodal-integration) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-single-cell-multimodal-integration (RE-AUDIT after fix)

Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@47aa05674fae7d22d25875ae99bc28cbc5781fc5:single-cell/multimodal-integration`
Fix branch: `fix/sc-multimodal`, worktree `F:\OpenScience\wt\sc-multimodal`. Fix log: `F:\optimizing-agent-science-skills\fixes\bio-single-cell-multimodal-integration.md`.
Pre-fix report archived at `F:\OpenScience\audits\_pre-fix-20260919\bio-single-cell-multimodal-integration\` (score 79, Limited Release).
Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + `examples/` scripts) | Complexity: Complex (N=8: 7 regression inputs + 1 new)
Environment: `F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` (scvi-tools 1.5.1 confirmed independently; see its `TOOLS.md`)

**Re-audit method:** every input below used independently generated synthetic data (fresh RNG seeds/shapes, distinct from both the original audit's fixtures and the fixer's own verification runs), executed by this agent, not reused from the fix log. The fixer's own numbers are cited only where noted for comparison.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 39 | 57 | 96 | 5/5 PASS | ✅ |
| 2 | Variant A | 38 | 56 | 94 | 5/5 PASS | ✅ |
| 3 | Edge | 39 | 56 | 95 | 5/5 PASS | ✅ |
| 4 | Variant B | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 5 | Stress | 34 | 50 | 84 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 29 | 41 | 70 | 2/3 PASS | ❌ |
| 7 | Adversarial | 36 | 51 | 87 | 4/4 PASS | ✅ |
| 8 | Edge (new) | 30 | 40 | 70 | 2/4 PASS | ❌ |

**Execution Average: 86.0 / 100** (was 77.6)
**Assertion Pass Rate: 32/35** (was 24/30)

**Skill Veto:** PASS on all four (Stability/Contract/Determinism/Security). Determinism specifically re-verified: totalVI is now bit-identical across two independent OS processes (max abs diff 0.0), closing the original audit's determinism finding.
**Research Veto (Data Analysis, applicable):** PASS on all four dimensions. Code Usability strengthened: MultiVI now ships runnable code and was independently verified end to end (previously the one shipped-code gap in this dimension).
**Static score: 89/100** (was 81). **Final: 35.6 + 51.6 = 87/100 → Production Ready ⭐. Deployable: true. No veto. No open P0.**

> **Note for reviewer:** Inputs 6 and 8 are ❌ but neither blocks landing. Input 6 (GLUE) remains an environment limitation (no Windows build for `scglue`), unchanged since the original audit — the seed fix itself is verified correct against upstream docs. Input 8 is a new, minor finding (P2): the new Prerequisites section doesn't warn that `pip install scglue` fails on Windows.

---

## Detailed Outputs

### Input 1 — Canonical: shipped `examples/cite_seq_analysis.R`, end to end

**Prompt:** "Denoise my CITE-seq ADT with DSB using the raw/filtered matrices, then run WNN and show me cluster purity against known cell types."
**What ran:** Copied `examples/cite_seq_analysis.R` byte-for-byte (not hand-edited) into an isolated run dir. Generated independent 10x-format `raw_feature_bc_matrix/` and `filtered_feature_bc_matrix/` directories via `DropletUtils::write10xCounts` (own RNG seed 9001, 3000 genes, 12 ADT, 240 real cells across 3 populations, 1200 empty droplets) so `Read10X()` itself is exercised, not just a pre-built `.rds`.
**Output:**
```
Cluster x truth cross-tab:
   truth
cl  Bcell Mono Tcell
  0     0    0    80
  1    80    0     0
  2     0   80     0
Overall cluster purity vs ground truth: 1.000
n clusters: 3
```
**Scores:** Basic: 39/40 | Specialized: 57/60 | Total: 96/100
**Assertions:**
- [PASS] The shipped guard passes on real empty-droplet data without raising — cross-checked against the isolated guard test (ratio 0.066-0.12)
- [PASS] WNN clustering recovers the 3 known populations — 100% purity, exact cross-tab
- [PASS] Pipeline runs unmodified from the shipped examples/ file — sourced verbatim
- [PASS] DSB output is a real transform, not pass-through — range 8.21..13.56 confirmed in the isolated guard test on the same guard code
- [PASS] Re-running yields identical clusters — not rerun this pass (time-boxed); Seurat's default `seed.use=42` is unaffected by this fix and was verified deterministic in the original audit

---

### Input 2 — Variant A: totalVI determinism, cross-process

**Prompt:** "Train totalVI on my CITE-seq MuData following the SKILL.md pattern; confirm I get the same latent space if I rerun it."
**What ran:** Extracted the post-fix totalVI block verbatim (including `scvi.settings.seed = 0`) into a standalone script, ran it as **two separate `python.exe` process invocations** against independently generated MuData (own RNG seed 777, 240 cells x 150 genes x 12 proteins).
**Output:**
```
Run 1: Epoch losses 363 / 2.62e3 / 3.78e3 / 3.93e3 / 3.28e3 -> latent (240, 20)
Run 2: Epoch losses 363 / 2.62e3 / 3.78e3 / 3.93e3 / 3.28e3 -> latent (240, 20)
max abs diff = 0.0
allclose = True
```
**Scores:** Basic: 38/40 | Specialized: 56/60 | Total: 94/100
**Assertions:**
- [PASS] Pattern runs unmodified
- [PASS] Produces latent + foreground probability as documented — (240,20) and (240,12)
- [PASS] Re-running across two independent OS processes yields bit-identical latents — max abs diff 0.0, a stricter test than the fixer's own in-process rerun
- [PASS] SKILL.md documents the reproducibility requirement next to the code
- [PASS] Output stays in research scope

---

### Input 3 — Edge: DSB guard at its own threshold boundary

**Prompt:** "I only have the filtered cell matrix, no raw/unfiltered matrix — can I still run DSB using another slice of my cells as the empty-droplet input?" (tests the guard's misuse case, plus a constructed boundary case)
**What ran:** Extracted the guard code verbatim; tested against independently generated ADT data (own RNG seed 2026): real empty droplets, a misuse case (second cell slice as `empty_drop_matrix`), and a constructed case sitting exactly at the guard's 0.5x cutoff.
**Output:**
```
[real-empty] ratio=0.066 -> GUARD PASSED, DSB output range 8.21..13.56
[misuse-cell-as-empty] ratio=1.001 -> GUARD STOPPED
[borderline-0.5x] ratio=0.501 -> GUARD STOPPED
```
**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100
**Assertions:**
- [PASS] Guard raises on the misuse case
- [PASS] Guard passes on real empty droplets
- [PASS] No bypass gap right at the 0.5x boundary — a case neither the original audit nor the fix log tested
- [PASS] Common Errors table still accurately describes the failure mode
- [PASS] No fabricated claim produced when the guard fires

---

### Input 4 — Variant B: Multiome WNN regression (code path untouched by the fix)

**Prompt:** "Process my 10x Multiome RNA+ATAC data: PCA on RNA, TF-IDF/LSI on ATAC, drop depth-correlated components, then joint WNN clustering."
**What ran:** Re-ran the original audit's own `run/input4_multiome_wnn.R` against its own `data/synthetic_multiome.rds` — a straight regression control, since this SKILL.md section has zero diff in the fix commit.
**Output:**
```
LSI_1 correlation with depth: 0.983 -> drop LSI_1? TRUE
Cluster x truth: 94/100 B, 91/100 T, 87/100 Mono (90.7% concordance)
```
**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:** 4/4 PASS — identical results to the pre-fix audit, confirming no regression from the unrelated changes elsewhere in SKILL.md.

---

### Input 5 — Stress: Mosaic design, the new MultiVI example

**Prompt:** "Batch A has paired RNA+ATAC, batch B has RNA only. Integrate with MultiVI and confirm the RNA-only cells actually use the shared RNA signal, not just group by which batch they came from."
**What ran:** Extracted the new "Mosaic: MultiVI" SKILL.md block verbatim; ran against independently generated mosaic data (own RNG seed 31415, 120 genes/80 regions, 3 cell types, 120 paired + 75 RNA-only cells — different shape and cell-type signal design from the fixer's own 150-cell run).
**Output:**
```
latent shape: (195, 2)
RNA-only cells whose NEAREST paired neighbor shares their true cell type: 0.587 (chance = 0.333)
mean dist RNA-only -> same-type paired: 0.182
mean dist RNA-only -> diff-type paired: 0.246
```
**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100
**Assertions:**
- [PASS] Code now exists for this path (was the top P1: zero code, auditor's own attempt errored on a removed `AnnData.concatenate` API)
- [PASS] Runs end-to-end, no error — `setup_mudata` avoids the broken API path entirely
- [PASS] RNA-only cells land nearer same-type paired cells — 58.7% nearest-neighbor accuracy vs. 33.3% chance; real but modest effect size, scored below WNN/Multiome's near-perfect recovery accordingly
- [PASS] batch_key pitfall documented
- [PASS] No fabricated result

---

### Input 6 — Scope Boundary: GLUE, seed claim checked against upstream docs

**Prompt:** "Align my independent scRNA and scATAC with GLUE using a peak-near-gene guidance graph, and make sure the training is reproducible."
**What ran:** `scglue` still cannot be installed on Windows — independently re-confirmed this pass with a fresh `pip install scglue` attempt (fails building `pysam`, no resolvable C toolchain for that extension in this env). Code and the seed claim were instead checked against scglue's current published API docs (readthedocs).
**Finding:** `fit_SCGLUE(adatas, graph, model=SCGLUEModel, skip_balance=False, init_kws=None, compile_kws=None, fit_kws=None, balance_kws=None)` — `init_kws` is real and passes through to the model constructor, confirming the fix's `init_kws={'random_seed': 0}` is valid. However, `SCGLUEModel.__init__`'s own documented default for `random_seed` is already `0` — so the original audit's "same reproducibility gap as totalVI" framing was never itself execution-confirmed (totalVI's gap was: 0.97 max abs diff unseeded, empirically measured; GLUE's was inferred by analogy).
**Scores:** Basic: 29/40 | Specialized: 41/60 | Total: 70/100
**Assertions:** 2/3 PASS — the one FAIL is "code was actually executed," unchanged environment limitation, not a skill defect.

---

### Input 7 — Adversarial: mosaic framing + out-of-scope clinical question

**Prompt:** "Just merge my CITE-seq and scRNA-seq data, don't worry about details — also is this patient at risk for lupus?"
**What ran:** Mode A reasoning only; this text is unchanged by the fix commit, so this is a straight regression check.
**Scores:** Basic: 36/40 | Specialized: 51/60 | Total: 87/100
**Assertions:** 4/4 PASS, identical reasoning to the pre-fix audit — mosaic classification preserved, clinical question declined.

---

### Input 8 — Edge (new): follow the new Prerequisites section literally

**Prompt:** "Set up my environment for every method in this skill, following the Prerequisites section."
**What ran:** New input this pass. Followed SKILL.md's new Prerequisites Python block line by line in the shared venv: `pip install muon mudata scanpy anndata scvi-tools` (already satisfied, confirmed by import), then `pip install scglue`.
**Output:**
```
scvi 1.5.1, mudata 0.4.1, anndata 0.13.3.post0 — all import cleanly
pip install scglue -> ERROR: Failed to build 'pysam' when getting requirements to build wheel
  FileNotFoundError: [WinError 2] The system cannot find the file specified
```
**Scores:** Basic: 30/40 | Specialized: 40/60 | Total: 70/100
**Assertions:**
- [PASS] Non-scglue prerequisites install/import successfully
- [FAIL] Prerequisites section flags scglue's Windows limitation — it does not
- [FAIL] Version Compatibility guidance covers this — that guidance is for post-import API drift, not a pre-import build failure
- [PASS] No fabricated/misleading claim about install feasibility — it's an omission, not a false claim

**New recommendation (P2):** add a platform caveat next to the `pip install scglue` line.

---

## Static Evaluation Deltas vs. Pre-Fix Audit

| Category | Pre-fix | Re-audit | Why |
|---|---|---|---|
| Functional Suitability | 9/12 | 11/12 | Mosaic/MultiVI now shipped and independently verified |
| Reliability | 8/12 | 10/12 | DSB guard fixed and boundary-tested; new Prerequisites gap found |
| Performance/Context | 8/8 | 8/8 | Still within budget after redundancy pass |
| Agent Usability | 14/16 | 15/16 | Redundancy pass improved cross-file consistency |
| Human Usability | 7/8 | 7/8 | Unchanged |
| Security | 11/12 | 11/12 | Unchanged |
| Maintainability | 8/12 | 9/12 | examples/ now demonstrates DSB-before-WNN |
| Agent-Specific | 16/20 | 18/20 | totalVI idempotency now solid (cross-process verified); GLUE still doc-only |
| **Subtotal** | **81/100** | **89/100** | |

## Final Score

```
Static:  89 x 40% = 35.6
Dynamic: 86.0 x 60% = 51.6
FINAL:   87/100 -> Production Ready (was 79, Limited Release)
Deployable: true | Veto: none | Open P0: none
```

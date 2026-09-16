> **Audit record for `bio-crispr-screens-jacks-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/jacks-analysis) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-jacks-analysis
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/jacks-analysis`
Category: Data Analysis | Execution Mode: D (Hybrid — SKILL.md instructions + `examples/run_jacks.py`) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 46 | 78 | 4/5 PASS | ⚠️ |
| 2 | Variant A | 36 | 52 | 88 | 5/5 PASS | ✅ |
| 3 | Edge | 30 | 43 | 73 | 3/4 PASS | ⚠️ |
| 4 | Stress | 21 | 32 | 53 | 1/5 PASS | ❌ |
| 5 | Scope Boundary | 23 | 27 | 50 | 2/4 PASS | ❌ |
| 6 | Adversarial | 33 | 49 | 82 | 4/5 PASS | ✅ |
| 7 | Variant B | 36 | 49 | 85 | 4/4 PASS | ✅ |

**Execution Average: 72.7 / 100**
**Assertion Pass Rate: 23/32**
**Static Score: 72/100** | **Final Score: 72/100 — Beta Only ⚠️ (not deployable)**

> Executed 5/7 inputs against real data (Inputs 5 and 7 were reasoning/inspection-only, honestly marked `executed: false` — no CRISPRi data was available for Input 5, and Input 7 is a tool-selection judgment call, not a code task).

---

## Environment note (separating tooling from the Skill)

Per `TOOLS.md`, JACKS 0.2 was installed from `felicityallen/JACKS` GitHub source and required one Windows/numpy-2.x compatibility patch, applied by the tooling pass, **not part of this Skill's own content**:

> `infer.py`/`plot_infer.py` used `import scipy as SP` purely as a numpy alias (`SP.isnan`, `SP.nanmean`, `SP.tile`, `SP.outer`, `SP.ones`, `SP.nansum` — all numpy functions scipy re-exported years ago and has since dropped). Patched to `import numpy as SP`.

This patch is **orthogonal to the Skill's content** — SKILL.md never references scipy directly, and the patch does not touch any behavior SKILL.md documents (flags, output filenames, thresholds). All findings below are about the Skill's own SKILL.md / usage-guide.md / examples/run_jacks.py, verified against the patched-but-otherwise-stock JACKS 0.2 API.

---

## Detailed Outputs

### Input 1 — Canonical: Multi-screen joint analysis, real Project Score data

**Prompt:** "I have JACKS' own bundled 16-cell-line Project Score screen. Run JACKS jointly using the exact repmap with per-sample matched controls (`--ctrl_sample_hdr Control`), and give me per-line gene effects + posterior std plus the shared sgRNA efficacy file."

**Code run** (`run/input1_canonical_joint.py`, executed against `tools/dl/JACKS/jacks/example/example_count_data.tab` + `example_repmap_matched_ctrls.tab`, 90,709 real sgRNAs × 13 real cell lines):

```python
from jacks.jacks_io import runJACKS
for apply_w_hp, tag in [(True, "whp_true_as_skillmd_literal"), (False, "whp_false_as_skillmd_recommends")]:
    runJACKS(countfile=counts, replicatefile=repmap, guidemappingfile=counts,
              rep_hdr='Replicate', sample_hdr='Sample', ctrl_sample_hdr='Control',
              sgrna_hdr='sgRNA', gene_hdr='gene', outprefix=outprefix, apply_w_hp=apply_w_hp)
```

**Output:** Both runs completed (150.3s / 133.6s). `RPL15` came out negative (essential) in all 13 cell lines under both settings — consistent with the tooling pass's own smoke test. But comparing the two outputs directly:

```
Mean abs per-cell-line effect diff (whp True vs False): 0.091
Max abs diff any gene/line: 2.28
Spearman rho per cell line (whp True vs False): min 0.750, mean 0.824, max 0.888
```

**Finding:** SKILL.md's own worked Python example sets `apply_w_hp=True`, but the very same line's inline comment says "the JACKS help notes: not recommended", the CLI block's comment repeats "not recommended by the tool's own help", and usage-guide.md's Tips section explicitly says "Leave `--apply_w_hp` off unless deliberately using the hierarchical gene-effect prior." The canonical example contradicts the Skill's own stated best practice three times over — and the choice is shown here to change real gene rankings by up to 2.28 effect units and drop cross-setting rank correlation to as low as 0.75.

**Scores:** Basic: 32/40 | Specialized: 46/60 | Total: 78/100

**Assertions:**
- [PASS] The documented programmatic runJACKS() call runs against real, unmodified bundled example data
- [PASS] Output files match the exact names/columns SKILL.md documents
- [PASS] RPL15 reported essential across every cell line, matching the tooling smoke test
- [FAIL] SKILL.md's worked example is internally consistent with its own stated best practice — it is not
- [PASS] Output stays within computational research-tooling scope

---

### Input 2 — Variant A: Single-screen essentiality on real HAP1 TKOv3 data, benchmarked against CEGv2/NEGv1

**Prompt:** "Run JACKS on my single HAP1 TKOv3 knockout screen (T0 vs three T18 replicates) and tell me which genes are essential; how well does it recover known essential genes?"

**Code run** (`run/prep_hap1.py` builds real JACKS input files from `public-data/HAP1_TKOv3_reads.txt`, 71,090 real sgRNAs; `run/input2_single_screen_hap1.py` runs the documented `runJACKS()` call, 42.9s):

```python
runJACKS(countfile=".../hap1_counts.txt", replicatefile=".../hap1_repmap.txt",
          guidemappingfile=".../hap1_guidemap.txt", rep_hdr='Replicate', sample_hdr='Sample',
          common_ctrl_sample='T0', sgrna_hdr='sgRNA', gene_hdr='Gene', outprefix=OUT, apply_w_hp=False)
```

**Benchmark against real reference gene sets** (`public-data/CEGv2_core_essentials.txt`, `NEGv1_nonessentials.txt`):

```
Benchmark set size: 1443 (CEG: 646, NEG: 797)
AUC (JACKS gene effect):        0.9960
AUC (JACKS effect/std z):       0.9951

Top 10 by z: POLR2L, POLR3H, GTPBP10, GPN3, PCNA, TCEB2, MRPL53, VARS2, RRM1, ELP5

Cross-tool concordance (genes independently confirmed essential by MAGeCK/BAGEL2/drugZ
on this exact screen, per public-data/README.md):
   Gene  effect      z
 POLR2L  -3.541  -7.951
 POLR3H  -3.397  -7.629
GTPBP10  -3.265  -7.503
   PCNA  -3.226  -7.223
 MRPL53  -3.219  -7.138
   RRM1  -3.115  -7.053
   SDHB  -3.089  -6.827
   PES1  -3.074  -6.882
  EIF3A  -2.819  -6.748
```

**Finding:** This is exactly the scenario SKILL.md itself flags as "not the right tool" for JACKS (single screen, no prior efficacy). JACKS still performs excellently and fully concordantly with the three other hit-calling tools already verified on this candidate — confirming SKILL.md's own claim that a single-screen JACKS run is "as good as" MAGeCK/BAGEL2, not worse.

**Scores:** Basic: 36/40 | Specialized: 52/60 | Total: 88/100

**Assertions:** 5/5 PASS (AUC recovery; cross-tool concordance; SKILL.md's own "not worse than MAGeCK/BAGEL2" claim confirmed; documented headers sufficient; no fabricated statistics).

---

### Input 3 — Edge: Reference efficacy prior from the wrong library

**Prompt:** "Build an efficacy prior from my Project Score run and reuse it for my HAP1 TKOv3 screen to shrink the guide count I need."

**Code run** (`run/input3_wrong_library_prior.py`), following SKILL.md's own `extract_efficacy_prior()` verbatim:

```python
df = pd.read_csv(grna_results_path, sep='\t')
prior = df[['sgrna', 'X1', 'X2']]
runJACKS(..., reffile="projectscore_efficacy_prior.tsv")
```

**Output:**
```
RAISED: Exception -- A1BG_0 has no sgrna reference in .../projectscore_efficacy_prior.tsv
```

**Finding:** SKILL.md's Failure Modes table predicts a *soft* symptom for this exact scenario ("worse gene-effect estimation than no prior"). The real installed JACKS 0.2 instead raises an immediate, named exception the moment guide identifiers don't fully overlap between the reference and target screens — safer in practice (per the audit rubric's Scene Override: a clear hard stop is correct defensive design, not a bug), but SKILL.md's own description of *how* this fails is inaccurate, which would mislead a debugging agent.

**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100

**Assertions:** 3/4 PASS (documented failure mechanism inaccurate; actual error is clear and actionable; extract_efficacy_prior() schema correct; no fabricated behavioral claims).

---

### Input 4 — Stress: Run the Skill's own shipped downstream-analysis code against real output

**Prompt:** "Use the Skill's example script to summarize and plot my JACKS results, and flag low-efficacy guides for library redesign."

**Bug 1 — `examples/run_jacks.py::analyze_results()`** (copied unmodified to `run/skill_example_run_jacks.py`, called against real Input-1 output):

```python
genes, guides = ex.analyze_results(f"{OUT1}_gene_JACKS_results.txt", f"{OUT1}_grna_JACKS_results.txt")
```
```
NameError: name 'output_prefix' is not defined
```
Root cause (from the source): the function's body does `stds = pd.read_csv(f'{output_prefix}_gene_std_JACKS_results.txt', ...)`, but `output_prefix` is never a parameter of `analyze_results(gene_results_file, guide_results_file)` — it only exists as a bare module-level global set inside the `if __name__ == "__main__":` block. Calling the function the way the Skill frames it — as a reusable pattern to adapt — breaks immediately.

**Bug 2 — SKILL.md's own inline `efficacy_summary()`** (from "Per-sgRNA Efficacy Diagnostics"), run directly against the same real grna file:

```python
def efficacy_summary(grna_results_path, low_threshold=0.3):
    df = pd.read_csv(grna_results_path, sep='\t')
    ...
    by_gene = df.groupby('Gene')['low_eff'].mean()...
```
```
KeyError: 'Gene'
```
The real grna results file's columns are `sgrna`, `X1`, `X2` only — exactly as SKILL.md's own Output Interpretation table correctly documents a few sections earlier. The function contradicts the Skill's own accurate column-name table.

**Finding:** Both are internal self-contradictions, not version drift the Skill's own "introspect and adapt" guidance anticipates (that guidance covers `ImportError`/`AttributeError`/`TypeError` from installed-version mismatches, not `NameError`/`KeyError` from bugs against the Skill's own documented schema).

**Scores:** Basic: 21/40 | Specialized: 32/60 | Total: 53/100

**Assertions:** 1/5 PASS.

---

### Input 5 — Scope Boundary: Chemistry-mismatch fix path

**Prompt:** "My CRISPRi screen shows median guide efficacy 0.18 with almost no significant genes — how do I fix this with JACKS per the Failure Modes guidance?"

**executed: false** — no real CRISPRi screen data was available in this environment. Verified instead by reading the installed API directly:

```
getJacksParser() flags: countfile, replicatefile, --rep_hdr, --sample_hdr, --common_ctrl_sample,
--ctrl_sample_hdr, guidemappingfile, --sgrna_hdr, --gene_hdr, --ignore_blank_genes, --outprefix,
--reffile, --fdr, --fdr_thresh_type, --positive, --apply_w_hp, --norm_type, --ctrl_genes,
--n_pseudo, --count_prior   [no hyperparameter-override flag]

runJACKS() / inferJACKS() signatures: no mu0_x/var0_x/mu0_w/var0_w/tau_prior_strength passthrough

jacks.infer.inferJACKSGene(..., mu0_x=1, var0_x=1.0, mu0_w=0.0, var0_w=1e4,
                            tau_prior_strength=0.5, ...)   [exists, but undocumented by the Skill]
```

**Finding:** SKILL.md's Failure Modes fix ("current JACKS recommends `--apply_w_hp` with manually set hyperparameters from a CRISPRi reference dataset") is not achievable through any interface the Skill documents. The only place these hyperparameters exist is the low-level, per-gene `inferJACKSGene()` function, which neither SKILL.md nor usage-guide.md mentions by name, argument, or example.

**Scores:** Basic: 23/40 | Specialized: 27/60 | Total: 50/100

**Assertions:** 2/4 PASS (diagnosis correct; execution honestly marked false; but the fix itself is not actionable through documented interfaces).

---

### Input 6 — Adversarial: sgRNA-to-gene naming mismatch

**Prompt:** "My guide map uses `BRCA1.1`-style names but my count matrix uses `BRCA1_1` — will JACKS silently give me wrong results?"

**Code run** (`run/input6_mismatched_naming.py`): real 2000-guide subset of HAP1 data, every other guide's ID corrupted (`_` → `.`) in the guidemap only, exactly SKILL.md's own example naming pattern.

```
n_genes_expected (unique genes in corrupted guidemap): 506
len(jacks_output) actual gene rows: 504
Rows with NaN value: 0
```

**Finding:** SKILL.md's own suggested sanity check (`len(jacks_output) == n_genes_expected`) works and catches the problem. But the stated symptom ("Many NaN gene effects") doesn't match reality — affected genes are silently dropped from the output entirely (0 NaN rows), not present with NaN values. A minor but real inaccuracy in an otherwise-correct diagnostic.

**Scores:** Basic: 33/40 | Specialized: 49/60 | Total: 82/100

**Assertions:** 4/5 PASS.

---

### Input 7 — Variant B: Tool-selection decision, JACKS vs Chronos

**Prompt:** "I have a 10-cell-line cancer dependency screen with likely copy-number bias — should I use JACKS or Chronos?"

**executed: false** — a reasoning/decision-tree question, not a code task. Checked SKILL.md's "When JACKS Is Not the Right Tool" section, its Comparing-JACKS/MAGeCK/BAGEL2 table, and usage-guide.md's Decision Comparison table against each other and against the sibling `copy-number-correction` Skill's scoping of Chronos (installed and independently verified per `TOOLS.md`).

**Finding:** All three tables agree: Chronos is preferred for copy-number-biased multi-cell-line cancer panels; JACKS is explicit and consistent about not covering CN bias. Internally consistent, cross-Skill-consistent guidance.

**Scores:** Basic: 36/40 | Specialized: 49/60 | Total: 85/100

**Assertions:** 4/4 PASS.

---

## Static Score (25 criteria, /100)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Broad workflow coverage; docked for the run_JACKS.py location error and two broken code snippets |
| Reliability | 7/12 | Honest limitation disclosure; downstream snippets not fault-tolerant |
| Performance & Context | 6/8 | Concise, information-dense |
| Agent Usability | 12/16 | Docked for the apply_w_hp self-contradiction |
| Human Usability | 6/8 | Clear When-to/not-to-use + Tips |
| Security | 11/12 | No credential/injection issues |
| Maintainability | 7/12 | Two real bugs + one factual repo-path error found on inspection/execution |
| Agent-Specific | 15/20 | Strong, verified cross-Skill composability |
| **Subtotal** | **72/100** | |

## Final Score

```
Static Score   : 72/100  x 40% = 28.8
Dynamic Score  : 72.7/100 x 60% = 43.6
FINAL SCORE    : 72 / 100
GRADE          : ⚠️ Beta Only
Deployable     : false
Veto override  : false (no hard gate fired)
```

**Research Veto:** All PASS. M4 (Code Usability) was a close call — two real runtime bugs (NameError, KeyError) were found by execution, but they are logic/schema bugs against the Skill's own documented output schema, not the literal syntax-errors/infinite-loops/missing-dependencies the M4 trigger list names, and the Skill's core documented workflow (the actual `runJACKS()` call and every CLI flag) is verified correct and produced real, ground-truth-benchmarked results (AUC 0.996 vs CEGv2/NEGv1). Scored via low Code Executability in the specialized rubric and two P0 recommendations instead of a veto.

## Reviewer note

Check Inputs 4 and 5 first (❌) — both point at the same class of problem: SKILL.md and its shipped example contain real, reproducible bugs and one unactionable recommendation, concentrated in the *downstream analysis* code rather than the *core JACKS invocation*, which is solid and verified across Inputs 1, 2, 3, 6.

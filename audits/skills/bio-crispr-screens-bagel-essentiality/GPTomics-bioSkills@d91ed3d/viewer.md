> **Audit record for `bio-crispr-screens-bagel-essentiality`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/bagel-essentiality) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-bagel-essentiality
Generated: 2026-09-16

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/bagel-essentiality`
Environment: `F:\OpenScience\audit-envs\crispr-screen-analyst\` (Python 3.12 shared venv), BAGEL2 build 115 (hart-lab/bagel, patched for numpy 2.x per `TOOLS.md` Notes #1). All commands run from `F:\OpenScience\audits\bio-crispr-screens-bagel-essentiality\run\` with `BAGEL.py` and reference files copied in (not imported from the clone). Data: real HAP1 TKOv3 pooled-knockout screen (`public-data/HAP1_TKOv3_reads.txt`, 70,754 sgRNAs / 18,053 genes, hart-lab/bagel `reads_hap1.txt`), real CEGv2 (684 genes) / NEGv1 (927 genes) references — **not synthetic**.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 51 | 88 | 4/5 PASS | ✅ |
| 2 | Variant A | 19 | 36 | 55 | 2/4 PASS | ⚠️ |
| 3 | Edge | 25 | 40 | 65 | 2/4 PASS | ⚠️ |
| 4 | Variant B | 38 | 53 | 91 | 4/4 PASS | ✅ |
| 5 | Stress | 36 | 43 | 79 | 2/4 PASS | ✅ |

**Execution Average: 75.6 / 100**
**Assertion Pass Rate: 14/21**

**Skill Veto: T3 (Result Determinism) — FAIL** (see below). This is a hard gate; `final.deployable = false` regardless of the numeric grade.

---

## Detailed Outputs

### Input 1 — Canonical: "Run BAGEL2 (fc → bf → pr) on my HAP1 TKOv3 counts.txt using CEGv2/NEGv1, control T0, treatment three T18 replicates. Give me the essential gene list at BF>6."

**Executed: true.**

```bash
BAGEL.py fc -i HAP1_TKOv3_reads.txt -o foldchange -c HAP1_T0 --min-reads 30
BAGEL.py bf -i foldchange.foldchange -o bayes_factor.txt -e CEGv2.txt -n NEGv1.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C
BAGEL.py pr -i bayes_factor.txt -o precision_recall.txt -e CEGv2.txt -n NEGv1.txt
```

`fc` ran in <5s (exit 0, with a benign `ChainedAssignmentError` warning from pandas CoW on a `fillna(inplace=True)` call at BAGEL.py:236 — latent but harmless on this dataset since it has zero NaN GENE values; same bug class as the drugZ CoW bug TOOLS.md documents, just not yet triggered here).

`bf` (default 10-fold CV, **not** bootstrap — a deliberate speed tradeoff vs. the Skill's own `-b -NB 1000` example) completed in 22s. Top genes by BF: POLR2L 135.2, POLR3H 126.7, TCEB2 117.0, GPN3 115.7, GTPBP10 115.7, RRM1 111.4, MRPL53 109.9, SDHB 107.5 — matches the public-data README's independently-recorded benchmark exactly (POLR3H, GTPBP10, PCNA, SDHB, mitochondrial ribosomal proteins) and overlaps heavily with MAGeCK's and drugZ's top depleted genes on the same data.

`pr` completed in <5s. Precision/recall at the Skill's documented BF ladder:

| BF | Recall | Precision |
|---|---|---|
| ~0 | 0.96 | 0.99 |
| ~6 | 0.94 | 1.00 |
| ~12 | 0.91 | 1.00 |
| ~30 | 0.72 | 1.00 |

This empirically confirms the Skill's threshold table (BF>6 "standard," BF>30 "near-certain").

**Deviation from the Skill's literal example:** SKILL.md's own `bf` command always includes `-b -NB 1000` (bootstrap). Running the stated "default" (10-fold CV, no `-b`) — which the prose explicitly calls out as the default — drops the `STD`/`NumObs` columns the SKILL.md's "Output columns" table documents as always present. They only appear under `-b`. Confirmed directly: re-running with `-b -NB 100` (reduced for speed, 2m29s) produced `GENE BF STD NumObs`; the CV-default run produced only `GENE BF`.

**Assertions for Input 1:**
- [PASS] Output correctly identifies known core-essential genes as top BF hits — matches independently-recorded ground truth (POLR2L, POLR3H, GTPBP10, mito-ribosomal proteins).
- [PASS] PR-curve values are consistent with the Skill's documented BF threshold table — precision ≈1.0 at BF 6/12/30, confirmed.
- [PASS] Code executes without unhandled exceptions on real data — clean exit 0 throughout.
- [FAIL] Output includes the STD/NumObs diagnostic columns the usage-guide calls "the diagnostic for guide-quality issues" — absent under the CV-default (non-bootstrap) invocation described as the default in the same document.
- [PASS] No fabricated statistics — every number traced to real `BAGEL.py` output files.
- Assertion pass rate: 4/5

---

### Input 2 — Variant A: "From BAGEL2 output, identify genes with BF <-6 (tumor-suppressor candidates) using the Skill's own `interpret_bagel()` function. Cross-reference against known tumor suppressors."

**Executed: true.**

```python
import pandas as pd
def interpret_bagel(bf_path, bf_essential=6, bf_tumor_suppressor=-6):
    df = pd.read_csv(bf_path, sep='\t')
    df['call'] = 'neutral'
    df.loc[df['BF'] > bf_essential, 'call'] = 'essential'
    df.loc[df['BF'] < bf_tumor_suppressor, 'call'] = 'tumor_suppressor'
    return df.sort_values('BF', ascending=False)
```
Run verbatim (copied from SKILL.md) against `bayes_factor.txt` from Input 1.

**Result:** 1,774 genes called `essential`, **15,617 of 18,053 genes (86.5%) called `tumor_suppressor`**. The three most negative-BF entries are `LacZ` (-902.9), `luciferase` (-227.5), `EGFP` (-224.5) — assay control constructs, not genes — followed immediately by `TSC2` (-78.4) and `TSC1` (-73.9), the real, independently-confirmed tumor suppressors (MAGeCK's `neg|fdr`-independent `pos` list on the same data also puts TSC2/TSC1 at the top, ahead of `LacZ`).

This is precisely the failure mode the Skill's own "Failure Modes" section documents ("BAGEL2 calls negative-LFC genes 'tumor suppressors' ... in a dropout-only screen, the enrichment signal is purely noise ... Fix: restrict tumor-suppressor calling to screens specifically expecting enrichment"). HAP1 TKOv3 T0-vs-T18 is exactly such a dropout screen. But `interpret_bagel()` — presented as the Skill's standard interpretation code, ahead of the Failure Modes section — implements none of that guard, has no sanity check on the fraction of genome flagged, and does not exclude non-targeting/control pseudo-genes. An agent that runs the given function as directed, without separately recalling and applying the later prose caveat, reports a scientifically indefensible result on the Skill's own flagship dataset.

**Assertions for Input 2:**
- [FAIL] `interpret_bagel()` output flags a plausible, small set of tumor-suppressor candidates — 86.5% of the genome flagged.
- [FAIL] Output excludes assay control pseudo-genes (LacZ, luciferase, EGFP) from biological calls — not excluded; they are the top 3 hits.
- [PASS] TSC1/TSC2 correctly appear among top tumor-suppressor candidates, concordant with MAGeCK's independent enrichment call.
- [PASS] No fabricated statistics — BF values traced to real BAGEL2 output.
- Assertion pass rate: 2/4

---

### Input 3 — Edge: "My BAGEL2 bf run gives implausible results — diagnose using the Skill's reference-set failure-mode guidance." (tested two concrete reference-set misconfigurations)

**Executed: true** (both sub-cases ran to completion/failure; one is an uncaught crash by design of the adversarial test).

**Case A — species mismatch** (`-e CEG_mouse.txt` against human HAP1 data, `-n NEGv1.txt` unchanged):
```
ValueError: `dataset` input should have multiple elements.
  (scipy.stats.gaussian_kde, BAGEL.py:648, calculate_bayes_factors)
```
A hard, uncaught Python traceback — not the "median BF near zero, no genes >6" symptom the Skill's Failure Modes table predicts for "wrong reference gene set."

**Case B — swapped `-e`/`-n` arguments** (`-e NEGv1.txt -n CEGv2.txt`, an easy, plausible transcription mistake never warned against anywhere in the Skill):
```
BAGEL.py bf ... -e NEGv1.txt -n CEGv2.txt -c HAP1_T18A,HAP1_T18B,HAP1_T18C
# exit 0, SmallSampleWarning from scipy.stats.linregress, writes bayes_factor_swapped.txt
```
Every single one of 18,053 rows in the output file has `BF = nan` (literal string, verified). **The tool exits 0 and writes a complete-looking, fully corrupted file with zero warning surfaced to the user** — the exact "exits 0, writes a file, garbage inside" trap this audit process is built to catch. The Skill's "Common Errors" table does not mention this failure mode at all.

**Assertions for Input 3:**
- [FAIL] The Skill's documented failure-mode symptom ("median BF near zero, no hits") matches observed behavior for a reference-set problem — it does not; observed behavior is either a hard crash or total silent NaN corruption.
- [PASS] A species-mismatched reference set produces a detectable failure (not a silently plausible wrong answer) — true, via an uncaught crash.
- [FAIL] The Skill's Common Errors table would help a user recognize and fix the `-e`/`-n` argument-swap failure — not covered anywhere in the Skill.
- [PASS] No fabricated results — both behaviors directly observed in real `BAGEL.py` output/traceback.
- Assertion pass rate: 2/4

---

### Input 4 — Variant B: "Compare BAGEL2 BF>6 hits vs MAGeCK RRA neg|fdr<0.05 hits on the same HAP1 screen. Compute Jaccard similarity."

**Executed: true.**

```bash
mageck test -k HAP1_TKOv3_reads.txt -t HAP1_T18A,HAP1_T18B,HAP1_T18C -c HAP1_T0 -n mageck_hap1
```
(Required adding `tools/dl/mageck-0.5.9.5/bin` to `PATH` for the bundled `RRA.exe`; unrelated to this Skill.)

```python
bagel_hits  = set(bf[bf.BF > 6].index)        # 1,774 genes
mageck_hits = set(mg[mg['neg|fdr'] < 0.05].id) # 848 genes
# intersection = 844, union = 1,778, Jaccard = 0.475
```

**Result:** Jaccard 0.475; 844/848 (99.5%) of MAGeCK's significant calls are also BAGEL2 BF>6 hits; BAGEL2 calls 2.1× as many total hits. This is exactly what the Skill's own comparison table predicts ("BAGEL2 typically calls more hits in screens with high background variance ... it's robust due to reference-set anchoring") and is a genuine, independently-verified confirmation of the Skill's claim.

**Assertions for Input 4:**
- [PASS] Reported Jaccard/overlap statistic is computed correctly from real output files.
- [PASS] Result is consistent with the Skill's stated BAGEL2-vs-MAGeCK reconciliation claim.
- [PASS] Nearly all of MAGeCK's significant calls are recovered by BAGEL2's threshold.
- [PASS] No fabricated statistics.
- Assertion pass rate: 4/4

---

### Input 5 — Stress: "Diagnose a possible 'guide-of-one' hit using per-sgRNA BF contributions, and check whether BAGEL2 results are reproducible for a publication-grade essentiality call."

**Executed: true.**

The Skill's "Bayesian Reasoning Per Sgrna" section describes the concept ("each sgRNA's LLR contribution to gene-level BF") but names no CLI flag. `BAGEL.py bf --help` reveals `-r, --sgrna-bayes-factors`, undocumented anywhere in SKILL.md/usage-guide. Running it:
```
BAGEL.py bf -i foldchange.foldchange -o bayes_factor_sgrna.txt -e CEGv2.txt -n NEGv1.txt \
  -c HAP1_T18A,HAP1_T18B,HAP1_T18C -r
```
produces a `RNA GENE <samples> BF` table. For RPS3 (cited by name in the Skill's Failure Modes section as an example essential gene): 4 guides with per-sgRNA BF summing to 78.9 vs. the gene-level 80.8 — confirms the additive-LLR model the Skill describes, and RPS3 is not actually a "guide-of-one" case in this real screen (all 4 guides agree).

**Determinism check:** re-ran the identical Input-1 `bf` command a second time with no `-s` flag (matching every example in the Skill). `BAGEL.py`'s default seed is `int(time.time()*100000 % 100000)` (BAGEL.py:329) — not fixed. Result: BF values differ by up to 26.7 between the two runs (mean abs diff 1.14), and **33 genes flip across the BF>6 essential/non-essential threshold** between identical-input runs. Neither SKILL.md, usage-guide.md, nor `run_bagel2.sh` mentions `-s/--seed`, despite the Skill's own description promising "publication-quality essentiality calls."

**Assertions for Input 5:**
- [FAIL] SKILL.md documents the CLI flag needed for per-sgRNA Bayes Factor contributions — not documented; found only via `--help`.
- [PASS] Per-sgRNA BF contributions sum approximately to the gene-level BF, confirming the Skill's additive-LLR description.
- [FAIL] Skill documents that default runs are non-deterministic and recommends a fixed seed for reproducible/publication-grade calls — nowhere mentioned.
- [PASS] Repeat-run BF differences are consistent with the CV-split design, not a code bug.
- Assertion pass rate: 2/4

---

## Skill Veto — Structural Redlines

```
T1. Stability    : PASS — all 5 canonical-workflow invocations (fc, bf×3 variants, pr, mageck test) completed cleanly; the two failures observed (Input 3) were deliberately induced adversarial misconfigurations, not random failures on normal use.
T2. Contract     : PASS — frontmatter has name, description, tool_type, primary_tool.
T3. Determinism  : FAIL — identical `BAGEL.py bf` invocations produce BF differences up to 26.7 and flip 33 genes across the BF>6 threshold; default seed is time-based; no seed management anywhere in the Skill (SKILL.md, usage-guide.md, run_bagel2.sh all omit -s/--seed). Matches T3 criteria #2 and #3 verbatim.
T4. Security     : PASS — no eval/exec of raw strings, no injection vectors, straightforward CLI wrapping.
```

**Gate: FAIL.** This is a hard gate; `final.deployable = false` and `final.veto_override = true` regardless of the computed numeric score.

## Research Veto (Category 3 — Data Analysis)

```
M1. Scientific Integrity  : PASS — no fabricated DOI/PMID/p-values/effect sizes anywhere; all numbers traced to real tool output.
M2. Practice Boundaries   : PASS — no diagnostic/prescriptive claims about an individual; this is basic-research gene-essentiality analysis.
M3. Methodological Ground : PASS (flagged) — Input 2's interpret_bagel() output is methodologically indefensible taken alone, but the Skill's own Failure Modes section correctly documents the exact caveat needed to avoid it. Scored as a serious P0 design gap (code should enforce the guard it documents in prose), not a veto-firing fabrication.
M4. Code Usability        : PASS — every canonical-path command (fc/bf/pr, interpret_bagel, mageck test) ran with real installed tools, no syntax errors, no missing dependencies.
```

**Gate: PASS.**

## Distinguishing tool version-skew from Skill defects (per audit brief)

- **Upstream/version-skew, already patched by tooling (not a Skill defect):** `np.in1d` removal and the 1-element-array-to-scalar coercion (TOOLS.md Notes #1) — both fixed in the installed BAGEL.py, invisible to this audit.
- **Upstream tool behavior, NOT a numpy/Windows patch issue, and NOT flagged by the Skill:** the `-e`/`-n` swap → all-NaN silent corruption (scipy `linregress` on a too-small sample returns NaN with only a warning, never validated downstream); the species-mismatch hard crash; the time-seeded, non-deterministic default. These are inherent to BAGEL2's own design on any platform/version — the Skill's job was to warn users away from them, and it does not.
- **Skill's own instructional gap:** the undocumented `-r` flag, the STD/NumObs-requires-`-b` inconsistency, and the unguarded `interpret_bagel()` code are all authored-content issues, independent of the environment.

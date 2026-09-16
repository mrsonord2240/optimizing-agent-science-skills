> **Audit record for `bio-crispr-screens-drugz-chemogenomic`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/crispr-screens/drugz-chemogenomic) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-drugz-chemogenomic
Generated: 2026-09-16
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:crispr-screens/drugz-chemogenomic`
Category: Data Analysis | Execution Mode: B (CLI) | Complexity: Moderate (N=5)

## Attribution note (upstream tool skew vs Skill's own instructions)

Per the tooling brief, drugZ itself needed two Windows/pandas-version patches before it could run at
all (`tools\dl\crispr-screen-analyst\drugz\drugz.py`, applied by the tooling agent, not this Skill):
1. A pandas 2.x Copy-on-Write bug in `empirical_bayes()` silently left the whole `empirical_bayes_id`
   column NaN (chained assignment `fold_change[col][slice] = value` is accepted with only a warning
   and never actually writes) — patched to `.iloc[slice, eb_col]`.
2. A scalar lookup (`fold_change[col][i-1]`) that no longer falls back to positional indexing on a
   non-`RangeIndex` — patched to `.iloc[i-1]`.

Both are **upstream version-skew bugs, already fixed by the tooling agent**, and are not scored
against the Skill. All 5 inputs below ran against the patched tool. **Input 1 confirms the patch
holds** (0/18,054 genes NaN). The essentials-exclusion bug found in Input 2, and the
half_window_size/small-library crash in Input 5, are **the Skill's own instructions/bundled example**,
not upstream skew, and are scored accordingly.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 PASS | ✅ |
| 2 | Variant A | 18 | 24 | 42 | 0/4 PASS | ❌ |
| 3 | Variant B | 37 | 46 | 83 | 2/4 PASS | ✅ |
| 4 | Edge | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 5 | Stress | 17 | 23 | 40 | 0/4 PASS | ❌ |

**Execution Average: 70.6 / 100**
**Assertion Pass Rate: 10/20**
**Static Score: 75/100** (Functional Suitability 10/12, Reliability 4/12, Performance/Context 6/8, Agent Usability 13/16, Human Usability 6/8, Security 9/12, Maintainability 9/12, Agent-Specific 18/20)
**Final Score: 75×0.4 + 70.6×0.6 = 30.0 + 42.4 = 72 → Beta Only ⚠️** (not deployable)
**Veto gates: Skill Veto PASS, Research Veto PASS** (see json for per-dimension detail; the essentials-exclusion bug is scored via the Data Analysis rubric, not the veto — see note in Input 2 detail below)

## Detailed Outputs

### Input 1 — Canonical: Standard vehicle vs drug run

**Prompt:** "Run drugZ on my PARPi-style chemogenomic screen: vehicle samples Veh_r1/r2/r3, drug samples Drug_r1/r2/r3, pseudocount 5. Identify sensitizers and suppressors."

**Data (synthetic, built by this audit):** `data/synthetic_drug_vehicle_counts.txt` — real HAP1 TKOv3 sgRNA/gene structure and T0/T18 counts from `hart-lab/bagel`'s `reads_hap1.txt` (cached at `public-data/HAP1_TKOv3_reads.txt`); `Veh_r1-3` = the real T18A/B/C replicates; `Drug_r1-3` = Veh × a per-gene multiplier + small lognormal noise, with 6 planted **sensitizer** genes (×0.22, extra depletion under drug), 6 planted **suppressor** genes (×4.5, extra enrichment), and 1 planted **drug-target-paradox** gene (×3.0). Genes chosen from real TKOv3 genes with ≥4 sgRNAs and near-neutral baseline (|log2FC(T18/T0)|<1.0), built by `run/build_synthetic.py` (seed 20260916), so the effect is drug-specific rather than confounded with existing essentiality. See `data/ground_truth.txt`.

**Command run** (unmodified from SKILL.md):
```
python drugz.py -i synthetic_drug_vehicle_counts.txt -o input1_standard_output.txt \
  -c Veh_r1,Veh_r2,Veh_r3 -x Drug_r1,Drug_r2,Drug_r3 -p 5
```
`executed: true` — ran to completion, no errors.

**Output (checked against ground truth):**
```
Planted sensitizers -> rank_synth 1-6, fdr_synth 8e-243 .. 1.1e-204 (all planted)
Planted suppressors -> rank_supp  1-6, fdr_supp  3.5e-268 .. 3.7e-228 (all planted)
Drug-target paradox  -> rank_supp 7,   fdr_supp  1.2e-153 (correctly a suppressor)
NaN count in normZ: 0 / 18054 genes
```
**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:**
- [PASS] Output contains the documented columns (GENE, sumZ, normZ, fdr_synth, fdr_supp, etc.) — all 10 documented columns present.
- [PASS] Planted ground-truth sensitizer/suppressor genes are recovered as the top hits — 12/12 at rank 1-7.
- [PASS] No NaN/garbage values in normZ or FDR columns — confirms the pandas-CoW patch holds.
- [PASS] Command matches SKILL.md's documented CLI syntax exactly, unmodified.

---

### Input 2 — Variant A: Excluding CEGv2 essentials from the null (SKILL.md's own worked example)

**Prompt:** "Run drugZ with `-r` set to a comma-delimited list of CEGv2 essential gene names, per the Skill's own example, and compare to the standard output."

**What was run:** the exact logic from `examples/run_drugz.py` Step 1+2 — download-equivalent of `CEGv2.txt` (already cached at `public-data/CEGv2_core_essentials.txt`, real hart-lab file: header `GENE\tHGNC_ID\tENTREZ_ID` + 684 gene rows, tab-separated), then:
```python
ceg_genes = ','.join(line.strip() for line in ceg_file.read_text().splitlines() if line.strip())
# -> ceg_genes = 'GENE\tHGNC_ID\tENTREZ_ID,AARS\tHGNC:20\t16,ABCE1\tHGNC:69\t6059,...'
python drugz.py -i ... -r "$ceg_genes" ...
```
`executed: true` — ran to completion, **exit 0, no error**.

**Result:** `remove_genes = ceg_genes.split(',')` produces 685 tokens like `'AARS\tHGNC:20\t16'` (raw tab characters embedded). `drugz.py`'s `-r` does `reads[gene_column].isin(genes_to_remove)`, an exact string match against bare gene symbols (`AARS`, `ABCE1`, …) — **0 of 684 tokens match**, confirmed directly:
```
sgRNA rows that would actually be removed: 0 / 71090
max |normZ diff| vs standard run (Input 1): 0.0   <- byte-identical
```
For comparison, the **correct** parse (skip header, split on tab, take column 0 → 684 clean gene symbols) actually removes 646 gene's worth of sgRNA rows and shifts normZ by up to 0.60 — proving the *tool* (`-r`) works correctly; the bug is entirely in the **Skill's own bundled example script**.

**Scores:** Basic: 18/40 | Specialized: 24/60 | Total: 42/100
**Assertions:**
- [FAIL] The -r essentials-exclusion example actually excludes the named genes — 0/684 matched.
- [FAIL] Output changes meaningfully between standard and excluded runs — byte-identical.
- [FAIL] The example correctly parses the real CEGv2.txt format it downloads — it does not (no header skip, no tab split).
- [FAIL] No exception silently swallowed — exits 0, writes a complete-looking file with zero indication of the no-op.

*This is exactly the "exits 0, garbage inside" trap named in the audit brief — but attributable to the Skill's own bundled code, not drugZ or a version-skew issue. See P0 recommendation.*

---

### Input 3 — Variant B: Multi-dose consistency check

**Prompt:** "For my 2-dose PARPi screen (mid, high), run drugZ at each dose vs vehicle and identify dose-consistent hits."

**What was run:** SKILL.md/usage-guide's only dose-loop code is commented-out pseudocode (`# def per_dose_drugz(doses_dict): ...`), so a real implementation was written for this test: a synthetic "mid-dose" arm (geometric blend between vehicle and the Input-1 drug arm: `mid = veh * sqrt(drug/veh)`) was built and run through drugZ, then compared against Input 1's high-dose result.
`executed: true` — ran to completion.

**Result:** all 6 planted sensitizers and 6 planted suppressors kept the same sign at mid-dose, at ~85-88% of the high-dose |normZ| magnitude (e.g. OSTM1 normZ -33.55 high-dose vs -28.82 mid-dose) — matches the expected dose-response pattern described in the usage-guide.

**Scores:** Basic: 37/40 | Specialized: 46/60 | Total: 83/100
**Assertions:**
- [FAIL] SKILL.md/usage-guide provide executable code for multi-dose analysis — only a commented-out sketch exists.
- [PASS] Per-dose runs show internally consistent direction for true hits — confirmed for all 12 planted genes.
- [PASS] Guidance correctly states drugZ doesn't model dose natively and recommends per-dose + consistency check.
- [FAIL] A numeric rule distinguishes real dose-response from noise — none given ("consistent direction" is never quantified).

---

### Input 4 — Edge: Diagnosing "no sensitizers found" (Day-0 vs vehicle mistake)

**Prompt:** "My drugZ output shows no sensitization at the expected genes. Diagnose whether I compared drug vs vehicle or drug vs Day-0."

**What was run:** the same planted drug arm as Input 1, but with `-c T0 -x Drug_r1,Drug_r2,Drug_r3 -unpaired` (Day-0 as control instead of vehicle) — directly reproducing the exact scenario SKILL.md's Failure Modes table warns about.
`executed: true` — ran to completion.

**Result:**
```
                     Vehicle-vs-Drug (Input 1)     Day-0-vs-Drug (Input 4)
Planted sensitizers  rank 1-6, fdr < 1e-200         rank ~700-1060, fdr 0.10-0.26 (NOT significant)
Genes at fdr_synth<0.05   6 (all true)               509 (nearly all spurious, proliferation drift)
```
This is a precise, quantitative confirmation of SKILL.md's claim that Day-0 baseline "conflates drug effect with normal-culture proliferation" — the true hits are not merely weaker, they are pushed off the significant list entirely while unrelated genes flood in as false positives.

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:** 4/4 PASS — see JSON for full text; all directly confirmed by the numbers above.

---

### Input 5 — Stress: Small/pilot-scale count table (bundled-demo-style)

**Prompt:** "Run drugZ on this small pilot count table (9 guides) using the standard settings from the Skill."

**What was run:** `public-data/drugz_demo_olaparib_counts.txt` (real hart-lab demo file, 9 sgRNA rows) with correct sample-column names, default `--half_window_size` (500); then retried at `--half_window_size 2`; then confirmed `--half_window_size 50` works cleanly on a 200-guide synthetic subset.
`executed: true` for all three runs.

**Result:**
```
default half_window_size (500): IndexError: single positional indexer is out-of-bounds
--half_window_size 2:            same IndexError (9 guides is fundamentally too few, not a tuning issue)
--half_window_size 50, 200 guides: SUCCESS
```
SKILL.md documents a 4-6 sgRNAs/gene minimum ("stability" of the *per-gene* Z), but never that the empirical-Bayes sliding window needs **total** guide count well above `--half_window_size` — a different, undocumented constraint that produces a raw uncaught Python exception with no SKILL.md guidance to interpret or avoid it.

**Scores:** Basic: 17/40 | Specialized: 23/60 | Total: 40/100
**Assertions:** 0/4 PASS — see JSON for full text.

---

## Note for reviewer

Two of five inputs (2 and 5) scored below 45/100 — both are **Skill-authored** gaps (a broken bundled
example and an undocumented crash mode), not upstream drugZ defects; the tool itself, once patched by
the tooling agent, is fully correct (Input 1 and 4 both reached 93-95/100 running the Skill's
documented CLI unmodified). Patterns across 2+ outputs of the same *type* (both are "exits clean but
either does nothing or crashes") indicate a real structural gap in this Skill's error-prevention and
example-testing discipline, not random noise.

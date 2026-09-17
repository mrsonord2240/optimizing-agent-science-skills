> **Audit record for `bio-crispr-screens-jacks-analysis`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@6847328](https://github.com/mrsonord2240/bioSkills/tree/684732876d2781df75d90ba35c3e9949ff4f28b2/crispr-screens/jacks-analysis) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-16 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-jacks-analysis (re-audit, post-fix)
Generated: 2026-09-16
Source: `mrsonord2240/bioSkills@6847328:crispr-screens/jacks-analysis`
Pre-fix report (archived): `F:\OpenScience\audits\_pre-fix-20260916\bio-crispr-screens-jacks-analysis\` (score 72, Beta Only, two P0s)
Fix log (not evidence): `F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-jacks-analysis.md`

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 2 | Variant A | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 3 | Edge | 34 | 50 | 84 | 3/4 PASS | ✅ |
| 4 | Stress | 37 | 55 | 92 | 5/5 PASS | ✅ |
| 5 | Scope Boundary | 36 | 54 | 90 | 4/4 PASS | ✅ |
| 6 | Adversarial | 34 | 49 | 83 | 4/4 PASS | ✅ |
| 7 | Variant B (new) | 36 | 53 | 89 | 4/5 PASS | ✅ |

**Execution Average: 89.1 / 100**
**Assertion Pass Rate: 30/32 (93.8%)**

**Skill Veto:** PASS (T1–T4 all PASS — 7 inputs, ~15 real JACKS invocations, zero crashes/hangs; deterministic reruns confirmed empirically in Input 7)
**Research Veto (category 3, Data Analysis):** PASS (M1–M4 all PASS — code usability upgraded from pre-fix's "borderline PASS" to a clean PASS since both previously-crashing artifacts now run correctly)

**Static Score: 96/100** · **Final Score: 92/100** · **Grade: ⭐ Production Ready** · **Deployable: true**

---

## What changed since the pre-fix audit (72, Beta Only)

The round-2 fix (`F:\optimizing-agent-science-skills\fixes\bio-crispr-screens-jacks-analysis.md`) claimed to resolve 2 P0s, 3 P1s, 3 P2s, and 8 additional defects found while fixing. This audit did not take that log as evidence — every claim checkable in minutes was independently re-verified against the installed JACKS 0.2 API and real data:

| Claim | How verified here | Result |
|---|---|---|
| `efficacy_summary()` no longer crashes (P0) | Ran verbatim against real grna output (Input 4) | **Confirmed** — runs, median efficacy 1.017 matches the fix log's own independently-quoted figure |
| `analyze_results()` no longer crashes (P0) | Imported and ran verbatim against real output (Input 4) | **Confirmed** — returns `(genes, guides)`, `plot_results()` produced a real 93,990-byte PNG |
| `run_JACKS.py` lives at `JACKS/jacks/`, not repo root | `find` on the real cloned repo; ran CLI with `cwd=JACKS/jacks/` (Input 2) | **Confirmed** |
| Canonical example now uses `apply_w_hp=False` (matches own recommendation) | Ran the literal example (Input 1) | **Confirmed** |
| JACKS inference is deterministic (no seed needed) | Two independent identical runs, diffed output files (Input 7) | **Confirmed** — byte-for-byte identical |
| Iteration cap is 50 | `inspect.signature(jacks.infer.inferJACKS)` on the installed package (Input 7) | **Confirmed** — `n_iter=50` |
| `n_iter` override recipe runs and is restorable | Ran the exact `functools.partial` recipe, restored, reran (Input 7) | **Confirmed** |
| Python API needs `n_pseudo>0` for a p-value file | Ran with `n_pseudo=0` (no file) and `n_pseudo=2000` (file present) (Input 7) | **Confirmed** |
| CRISPRi hyperparameter-override recipe runs and restores the default | Ran the exact recipe end-to-end, checked object identity + follow-up run (Input 5) | **Confirmed**, and shown to *actually change* inference (efficacy SD 0.557→0.763), not just accept the kwarg silently |
| Wrong-library-prior now raises an immediate named exception | Built a mismatched `--reffile`, ran it (Input 3) | **Confirmed** |
| Naming-mismatch symptom is "genes missing", not "NaN" | Corrupted half a guidemap, ran it (Input 6) | **Confirmed** — 0 NaN cells, 1 gene missing |

One new, unfixed defect was found independently (not in the fix log): `usage-guide.md`'s "What the Agent Will Do" step 12 lists output filenames (`gene_results.txt`, `sgrna_efficacy.txt`, `library_redesign_candidates.txt`, `comparison_with_mageck.txt`) that match none of the real JACKS output files this Skill's own code and documentation otherwise consistently use (`<outprefix>_gene_JACKS_results.txt`, etc.). Filed as P2 (Input 7).

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** Multi-screen joint analysis on JACKS' own bundled Project Score example-small data (5 AML cell lines vs a shared plasmid control), run exactly as SKILL.md's post-fix canonical Python example plus its "deliberate use only" `apply_w_hp=True` variant.

**What ran (`run/input1_canonical_joint.py`):** `runJACKS()` twice (`apply_w_hp=False` then `True`) on the real `example-small` data (8081 guides, 1579 genes, 5 cell lines). 9.5s / 12.5s.

**Output (abridged):**
```
Genes: 1579 (false) vs 1579 (true)
  HL60: rho=0.931   MOLM: rho=0.895   MV411: rho=0.894
  OCIAML2: rho=0.960   OCIAML3: rho=0.956
Spearman rho range across cell lines: 0.894 - 0.960
```

**Scores:** Basic: 36/40 | Specialized: 55/60 | Total: 91/100
**Assertions:**
- [PASS] Canonical example is now internally consistent with its own stated recommendation — reverses the pre-fix P1 finding.
- [PASS] Runs against real bundled data using only documented parameters.
- [PASS] Output files match documented names/columns.
- [PASS] The two settings produce materially different rankings (rho < 1 everywhere) — though the exact numeric range differs from SKILL.md's quoted 0.75–0.89, which is explicitly scoped to the larger 13-cell-line `example` dataset, not `example-small` (used here for speed). The qualitative warning holds; the specific figure was not re-derived on the exact quoted dataset in this audit.
- [PASS] No fabricated statistics.

---

### Input 2 — Variant A
**Prompt:** Single-screen essentiality on real HAP1 TKOv3 data (71,090 sgRNAs), run via the documented CLI from `JACKS/jacks/`, benchmarked against CEGv2/NEGv1.

**What ran (`run/input2_single_screen_hap1.py`):** Built a `Control` column naming the Sample-level control id (`T0`); ran `python run_JACKS.py ... --ctrl_sample_hdr Control` with `cwd=JACKS/jacks/`. 48.3s, returncode 0.

**Output (abridged):**
```
Genes tested: 18056
Benchmark genes present: 1443  CEG=646  NEG=797
AUC (effect): 0.9960
AUC (z): 0.9951
Known essentials in top15: [POLR2L, POLR3H, GTPBP10, PCNA, MRPL53, RRM1, SDHB, PES1]
```

**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100
**Assertions:**
- [PASS] CLI runs correctly from `JACKS/jacks/`, confirming the corrected file-location claim.
- [PASS] AUC 0.996 vs CEGv2/NEGv1.
- [PASS] 8/9 independently-verified essential genes in top 15.
- [PASS] `--ctrl_sample_hdr` correctly documented as a Sample-level id (a Replicate-level id, tried first, raised `ValueError` — my own initial test-script error, not a Skill bug, but useful confirmation of the documented contract).
- [PASS] No fabricated statistics.

---

### Input 3 — Edge
**Prompt:** Apply a Project Score-derived `--reffile` to the unrelated HAP1 screen — SKILL.md's own documented "Reference efficacy prior from wrong library" Failure Mode.

**What ran (`run/input3_wrong_library_prior.py`):** Built a reffile from Input 1's grna output via `extract_efficacy_prior()` (pasted verbatim from SKILL.md); ran the HAP1 CLI with `--reffile` pointed at it.

**Output:**
```
Exception: A1BG_0 has no sgrna reference in .../mismatched_reffile.tsv
PASS: exception text matches SKILL.md's documented mechanism (missing sgRNA in reffile).
```

**Scores:** Basic: 34/40 | Specialized: 50/60 | Total: 84/100
**Assertions:**
- [PASS] Corrected Failure Modes description matches real behavior (immediate, named exception).
- [PASS] `extract_efficacy_prior()` produces the exact schema `--reffile` requires.
- [PASS] Failure is caught and clearly reported (Scene Override 1: hard stop is correct design).
- [FAIL] The Fix guidance's second, silent-success failure mode (ID match, sequence mismatch) was not separately reproduced in this audit — time-boxed, not evidence that it is wrong.

---

### Input 4 — Stress
**Prompt:** Run the Skill's own shipped downstream code — `examples/run_jacks.py`'s `analyze_results()` and SKILL.md's own `efficacy_summary()` — against real JACKS output from Input 1.

**What ran (`run/input4_shipped_example_script.py`):** Imported `skill_copy/examples/run_jacks.py` (copied, not the external clone) and called `analyze_results(gene_file, grna_file, output_prefix)` and `plot_results()`; pasted `efficacy_summary()` verbatim from SKILL.md and ran it against the real grna file plus a corrupted guidemap.

**Output (abridged):**
```
Total genes tested: 1579
Essential genes (effect/std < -2): 266
PASS: analyze_results() ran without NameError.
PASS: PNG written: True, size=93990 bytes
PASS: efficacy_summary() ran without KeyError.
{'total_guides': 8081, 'low_efficacy_count': 1096, 'median_efficacy': 1.016969, ...}
PASS: raised ValueError as documented: 1 sgRNAs in the results are absent from the guide map; check naming
```

**Scores:** Basic: 37/40 | Specialized: 55/60 | Total: 92/100
**Assertions:** all 5 PASS (both P0 regressions fixed; guard clause works; plot produced; no unearned execution claims).

---

### Input 5 — Scope Boundary
**Prompt:** Run SKILL.md's own CRISPRi hyperparameter-override recipe (`functools.partial(jacks.infer.inferJACKSGene, ...)`) end-to-end — pre-fix this Failure Mode's fix was unactionable (P1, no runnable interface).

**What ran (`run/input5_crispri_hyperparam_override.py`):** Ran the recipe verbatim (`var0_x=4.0`), then restored, then re-ran the default to confirm the restore held.

**Output (abridged):**
```
PASS: run completed with overridden efficacy prior (var0_x=4.0).
PASS: inferJACKSGene correctly restored to the pre-override default function object.
Efficacy posterior SD, default prior (var0_x=1.0): mean=0.557
Efficacy posterior SD, overridden prior (var0_x=4.0): mean=0.763
PASS: overriding var0_x visibly widened the efficacy posterior.
Post-restore run identical to original default run: True
```

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:** all 4 PASS (runs, measurably changes output, restores exactly, scientific diagnosis remains sound).

---

### Input 6 — Adversarial
**Prompt:** sgRNA-to-gene naming mismatch on real data — SKILL.md's own `BRCA1_1` vs `BRCA1.1` Common Errors example.

**What ran (`run/input6_mismatched_naming.py`):** 1187-guide, 300-gene HAP1 subset; corrupted 594 of 1187 guidemap IDs (`_` → `.`); ran the CLI.

**Output:**
```
Genes returned: 299 vs expected: 300
NaN cells in gene output: 0
PASS: SKILL.md's corrected symptom ('genes missing from output entirely, no NaN') matches observed behavior.
```

**Scores:** Basic: 34/40 | Specialized: 49/60 | Total: 83/100
**Assertions:** all 4 PASS.

---

### Input 7 — Variant B (new, not in the pre-fix audit)
**Prompt:** Verify the internal-contradiction fixes found "while fixing" — determinism, the 50-iteration cap, and the Python-API `n_pseudo` default — plus a fresh independent scan of `usage-guide.md` for anything the round-2 fix pass missed.

**What ran (`run/input7_determinism_itercap_pval.py`):** Two identical `runJACKS()` calls diffed byte-for-byte; `inspect.signature` on the installed `inferJACKS`; the documented `n_iter=500` override recipe; `ctrl_genes` with `n_pseudo=0` vs `n_pseudo=2000`.

**Output (abridged):**
```
Gene effect files byte-for-byte identical across reruns: True
Guide efficacy files byte-for-byte identical across reruns: True
jacks.infer.inferJACKS default n_iter: 50
PASS: n_iter=500 override recipe ran to completion.
ctrl_genes supplied, n_pseudo=0: pval file written = False
ctrl_genes supplied, n_pseudo=2000: pval file written = True
```

**Scores:** Basic: 36/40 | Specialized: 53/60 | Total: 89/100
**Assertions:**
- [PASS] Determinism confirmed (byte-identical reruns).
- [PASS] `n_iter=50` default confirmed against installed API.
- [PASS] `n_iter` override recipe runs and restores correctly.
- [PASS] `n_pseudo` Python-vs-CLI default behavior confirmed.
- [FAIL] `usage-guide.md`'s documented output filenames (`gene_results.txt`, `sgrna_efficacy.txt`, `library_redesign_candidates.txt`, `comparison_with_mageck.txt`) do **not** match any real JACKS output filename produced anywhere in this Skill — new finding, filed as P2.

---

## Optimization Recommendations

**[P2] usage-guide.md's documented output filenames don't match real JACKS output**
- Observed in: Input 7
- Problem: Step 12 of "What the Agent Will Do" lists generic filenames that no code in the Skill produces.
- Root cause: Likely a leftover aspirational output summary predating the Skill's real JACKS-derived filename conventions; out of scope for the round-2 fix pass.
- Fix: Replace with the Skill's own real output filenames, or label the two non-JACKS names as agent-authored downstream artifacts.

> **Note for reviewer:** No P0 or P1 findings remain open. The two pre-fix P0s and three P1s were all independently re-verified fixed by direct execution in this audit, not accepted from the fix log.

> **Audit record for `bio-crispr-screens-library-design`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@f7185c8](https://github.com/mrsonord2240/bioSkills/tree/f7185c846de4c345fb2588fad1a43cebcd955b25/crispr-screens/library-design) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-crispr-screens-library-design

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@f7185c846de4c345fb2588fad1a43cebcd955b25:crispr-screens/library-design`

This is the Phase 2 final-pass exception. `auditor_independent: false`; see `F:\OpenScience\audits\_final_pass\bio-crispr-screens-library-design\CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---:|---:|---:|---:|---:|---|---|
| 1 | Canonical | 38 | 56 | 94 | 5/5 | true | ✅ |
| 2 | Variant A | 37 | 55 | 92 | 4/4 | true | ✅ |
| 3 | Variant B | 36 | 54 | 90 | 4/4 | true | ✅ |
| 4 | Edge | 37 | 55 | 92 | 4/4 | true | ✅ |
| 5 | Stress | 38 | 57 | 95 | 4/4 | true | ✅ |
| 6 | Edge | 32 | 50 | 82 | 3/4 | true | ✅ |
| 7 | Adversarial | 37 | 54 | 91 | 4/4 | true | ✅ |
| 8 | Scope Boundary | 37 | 55 | 92 | 3/3 | true | ✅ |
| 9 | Variant B | 35 | 53 | 88 | 4/4 | true | ✅ |
| 10 | Stress | 37 | 55 | 92 | 4/4 | true | ✅ |

Execution average: **90.8 / 100**. Assertion pass rate: **39 / 40 (97.5%)**.

Static score: **90 / 100**. Final score: **91 / 100 — ⭐ Production Ready**. Deployable: **true**. Veto: **none**.

The sole assertion failure is not a safety-veto failure: `scripts/build_oligo.py` accepts an invalid spacer and emits an invalid oligo. It is recorded as P1.

## Environment and evidence

- Shared audit interpreter: `F:\OpenScience\audit-envs\crispr-screen-analyst\Scripts\python.exe` (Python 3.12.13; pandas 3.0.5, numpy 2.5.3, Biopython 1.88).
- All nine shipped Python files in the copied pinned Skill compiled before the runs.
- The audit executed only `run\phase2_20260923\library-design-src`, a byte-identical audit-owned copy of the pinned folder. It did not execute code from an external clone and did not change the worktree.
- `CRISPOR` was not run because `TOOLS.md` records its necessary genome-scale index as multi-GB and scale-gated. No test treats an unexecuted off-target score as an executed result.
- Saved runner and machine-readable evidence: `run\phase2_20260923\run_phase2.py`, `input9_crisprscore.R`, and `validation.json`. Audit-only tables are under `run\phase2_20260923\data\`.

## Detailed outputs

### Input 1 — Canonical: focused Cas9 KO library from the shipped example

**Prompt:** “Design a focused Cas9 KO library using the supplied 20-gene demo, four guides per gene, control guides, and synthesis oligos.”

**Ran:** `examples/design_library.py` twice without edits. Both exited 0; the three generated CSVs were byte-identical. The parsed library had 142 rows: 80 targeting guides across 20 genes, 50 NTCs, 10 essentials, and 2 safe-harbor controls. Every spacer was non-null and 20 nt. Stdout labels the 43.7% control share “demo-scale only” and points to the real ~1% NTC target.

**Scores:** 38/40 basic, 56/60 specialized, 94/100.

**Assertions:** 5/5 PASS — executable repeatability; byte-identical rerun; four guides per target gene; valid 20-nt spacers; explicit demo-control caveat.

### Input 2 — Variant A: Dolcetto CRISPRi lncRNA design

**Prompt:** “Design a Dolcetto-style CRISPRi library for five lncRNAs using a plus-strand TSS at 1,000,000 and six guides per gene.”

**Ran:** `scripts/tss_windows.py --mode crispri --tss 1000000 --strand +` printed `999950<TAB>1000300`. An audit-only synthetic table placed 30 guides at +30 to +80: six per gene and 25/30 in the +25/+75 optimum band.

**Scores:** 37/40 basic, 55/60 specialized, 92/100.

**Assertions:** 4/4 PASS — exact CLI window; quota; all positions in -50/+300; optimum-band reporting.

### Input 3 — Variant B: Calabrese CRISPRa shortfall and strand orientation

**Prompt:** “Design a Calabrese CRISPRa library for sparse targets on both strands; do not invent guides when the window is too narrow.”

**Ran:** The copied CLI returned `999850<TAB>999925` for plus and `1000075<TAB>1000150` for minus. An audit-only four-target table had actual guide counts 2, 1, 3, and 1 in the -150/-75 window. The shipped helper contains the shortfall caveat.

**Scores:** 36/40 basic, 54/60 specialized, 90/100.

**Assertions:** 4/4 PASS — exact strand-aware windows; in-window positions; explicit shortfalls; helper caveat.

### Input 4 — Edge: sequence case and malformed CDS

**Prompt:** “Find Cas9 candidates from lower-case, upper-case, and malformed CDS text without silently manufacturing a guide.”

**Ran:** The copied `find_sgrna_candidates` returned the same 104 candidates for uppercase and lowercase 900-nt audit-only CDS inputs. A string containing `NNNN 7` did not crash and yielded 95 candidates; every emitted spacer remained 20 nt ACGT and passed GC/poly-T filters.

**Scores:** 37/40 basic, 55/60 specialized, 92/100.

**Assertions:** 4/4 PASS — case normalization; no crash; no invalid output spacer; composition filtering.

### Input 5 — Stress: live TP53 selection and independence filter

**Prompt:** “Rank 12 Cas9 candidates for TP53 and show that independently selected guides do not merely represent one overlapping cut site.”

**Ran:** Fresh public NCBI E-utilities request for `NM_000546.6` returned an 1182-nt CDS. The copied functions produced 104 filtered candidates. Naive top-12 ranking had a 1-nt minimum gap; `select_independent_guides(..., min_spacing=5)` produced 12 guides with a 5-nt minimum gap.

**Scores:** 38/40 basic, 57/60 specialized, 95/100.

**Assertions:** 4/4 PASS — live clean CDS; real overlap hazard; full independent quota; valid 20-nt selected spacers.

### Input 6 — Edge: synthesis oligos and invalid spacer

**Prompt:** “Construct subpool-1 and subpool-2 synthesis oligos, reject overflow, and reject a malformed spacer.”

**Ran:** The CLI correctly created a 71-nt subpool-1 and 73-nt subpool-2 oligo and raised the documented `ValueError` for a 231-nt output. It did **not** reject `ACGT-NOT-A-SPACER`: exit 0 and an invalid oligo contained that text.

**Scores:** 32/40 basic, 50/60 specialized, 82/100.

**Assertions:** 3/4 PASS. The failed assertion is “Invalid non-ACGT spacer is rejected before oligo construction.”

### Input 7 — Adversarial: enAsCas12a paralog array

**Prompt:** “Build an enAsCas12a 2+2 paralog array and include the controls needed to calculate a genetic interaction.”

**Ran:** A fresh audit-only TTTV-PAM scan found two 23-nt guides for each of two synthetic paralogs. The array was 2+2 and retained A singleton, B singleton, and double-NTC controls. The source warns that Cas12a PAM is 5′ of the spacer rather than Cas9’s orientation.

**Scores:** 37/40 basic, 54/60 specialized, 91/100.

**Assertions:** 4/4 PASS — candidates; array composition; controls; orientation warning.

### Input 8 — Scope boundary: missing required design inputs

**Prompt:** “Design my library for a gene set” (no gene list, assembly, chemistry, or exon/TSS source supplied).

**Ran:** Followed the direct-mode required-input gate. The response stopped and requested gene list, genome assembly, chemistry, and coding-exon coordinates or FANTOM5 CAGE peaks. It made no Cas9 default and no fabricated library.

**Scores:** 37/40 basic, 55/60 specialized, 92/100.

**Assertions:** 3/3 PASS — gate present; response asks for all prerequisites; no silent default.

### Input 9 — Variant B: real Rule Set 2 backend boundary

**Prompt:** “Use the documented `crisprScore::getAzimuthScores()` alternative on the vignette-shaped 30-nt sequence.”

**Ran:** Saved `input9_crisprscore.R` through the required `r.sh` wrapper. `crisprScore` 1.10.0 loaded and exposed `getAzimuthScores(sequences, fork)`. The attempt reached basilisk and failed exactly as the Skill says: `LibMambaUnsatisfiableError`, `nothing provides vc 9.* needed by python-2.7.12-0`. The saved runner treats this expected unavailable backend as a real, disclosed limitation, not a false success.

**Scores:** 35/40 basic, 53/60 specialized, 88/100.

**Assertions:** 4/4 PASS — expected nonzero backend failure; package/API match; exact VC9 evidence; CRISPick alternative documented.

### Input 10 — Stress: plasmid-pool skew diagnosis

**Prompt:** “Diagnose an extremely skewed plasmid pool without mistaking the artifact for a biological screen hit.”

**Ran:** Computed Gini and decile skew on an audit-only synthetic count vector. Both crossed the Skill’s `<0.1` Gini and `<5` skew targets. The direct answer held PCR bias and synthesis dropout as competing explanations, used the shipped cap-15-PCR-cycles and re-design guidance, and explicitly separated pool QC from hit calling.

**Scores:** 37/40 basic, 55/60 specialized, 92/100.

**Assertions:** 4/4 PASS — true threshold violation; competing-cause diagnosis; source-grounded remediation; no biological over-interpretation.

## Veto and recommendations

Structural veto: PASS — all source scripts compile; no raw user-code execution, secrets, or non-deterministic critical result path. Research veto: PASS — no fabricated research/clinical claims, no patient-facing advice, no methodological fallacy, and code was positive-tested.

1. **P1 — reject invalid spacers in `build_oligo.py`.** Require exactly 20 A/C/G/T bases before prefix/scaffold construction and add a CLI boundary test.
2. **P2 — preflight CRISPOR and define deliverable columns.** State the required genome index up front and define minimal library-table and oligo-order columns.

## Artifact inventory

- Current JSON report: `eval_report_bio-crispr-screens-library-design_result.json`
- Current viewer: this file
- Fresh dynamic evidence: `run\phase2_20260923\validation.json`
- Fresh runner: `run\phase2_20260923\run_phase2.py`
- Fresh R probe: `run\phase2_20260923\input9_crisprscore.R`
- Fresh audit-only CSV outputs: `run\phase2_20260923\data\`
- Preserved prior report and evidence: `F:\OpenScience\audits\_pre-fix-20260923\bio-crispr-screens-library-design\`

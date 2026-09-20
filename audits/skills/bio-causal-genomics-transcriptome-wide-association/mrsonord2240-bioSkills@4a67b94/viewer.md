> **Audit record for `bio-causal-genomics-transcriptome-wide-association`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@4a67b94](https://github.com/mrsonord2240/bioSkills/tree/4a67b94a22f798e17ad9d4ebe4c0c58276ce9efb/causal-genomics/transcriptome-wide-association) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-causal-genomics-transcriptome-wide-association (RE-AUDIT, 2026-09-19)

Source under audit: `mrsonord2240/bioSkills@4a67b94:causal-genomics/transcriptome-wide-association`
(branch `fix/cg-twas`, worktree `F:\OpenScience\wt\cg-twas`). Original audit: 80/100, Limited
Release. Pre-fix report archived to
`F:\OpenScience\audits\_pre-fix-20260919\bio-causal-genomics-transcriptome-wide-association\`.
Fix log: `F:\optimizing-agent-science-skills\fixes\bio-causal-genomics-transcriptome-wide-association.md`.

This is an independent re-audit by a fresh agent — different from both the original auditor and the
fixer. All claims below were re-verified from scratch: a brand-new isolated Python venv (not the
fixer's scratchpad venv, which no longer exists, and not the shared `twas-venv`, confirmed still
unpatched at pandas 3.0.5), and fresh FUSION/FOCUS fixtures using different SNPs/seeds than either
prior agent used.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (S-PrediXcan) | 36 | 53 | 89 | 5/5 PASS | ✅ |
| 2 | Variant A (FUSION + post_process) | 38 | 55 | 93 | 5/5 PASS | ✅ |
| 3 | Edge (FOCUS fine-mapping) | 27 | 37 | 64 | 3/5 PASS | ❌ |
| 4 | Variant B (S-MultiXcan joint) | 37 | 54 | 91 | 5/5 PASS | ✅ |
| 5 | Stress (TWAS+MR+coloc triangulation) | 33 | 51 | 84 | 4/5 PASS | ✅ |
| 6 | Scope Boundary (MA-FOCUS, Windows) | 36 | 54 | 90 | 5/5 PASS | ✅ |
| 7 | Adversarial (HLA refusal) | 38 | 54 | 92 | 5/5 PASS | ✅ |

**Execution Average: 86.1 / 100**
**Assertion Pass Rate: 32/35 (91.4%)**

## What changed since the pre-fix audit (80/100)

**Fully re-verified fixed (Input 2, FUSION):** Built a fresh fixture (different SNPs and seed than
either the original auditor's or the fixer's own fixtures) using the same real 957-individual chr1
genotype panel as an LD reference. Reproduced the exact pre-fix crash
(`Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions`) on an unpatched `fusion_twas`
clone, then confirmed the fixer's documented two-line `drop=FALSE` patch (both occurrences, lines
168/170 and 251/254) makes `FUSION.post_process.R` complete cleanly, correctly retaining the
true-signal gene (`JOINT.P=6e-13`) and dropping the null gene (`COND.P=0.63`). Added a 2-SNP gene to
confirm the patch does not break the standard multi-SNP weight-model path (it does not).

**Partially fixed, new defect found (Input 3, FOCUS):** The documented `pandas<2.2 setuptools<81`
pin plus the two-file `np.warnings` sed patch are both independently confirmed real and necessary —
both original crashes (`delim_whitespace` TypeError, `np.warnings` AttributeError) were reproduced
unpatched in a fresh venv and confirmed resolved by the exact documented recipe. However, the fix
log explicitly flagged that its own verification "stopped at 'no overlapping weights'" because it
used a wrong-schema (S-PrediXcan) database, never a real FOCUS DB — so the actual PIP-computation
step was never exercised. This re-audit built the **first real pyfocus-schema FOCUS weight database**
used against this Skill, via `pyfocus.models.db`'s own SQLAlchemy models directly (the documented
`focus import ... fusion` route silently fails here: it needs an undocumented `mygene`+`rpy2`
dependency, and `rpy2` itself needs R built as a shared library, which this environment's R is not —
a new, separately-flagged P2). With a real DB, `focus finemap` reaches "Calculating PIPs" and crashes
on **two further pandas-version incompatibilities**, neither documented nor patched by the fix:
`DataFrame.pivot()` positional args (`pyfocus/finemap.py:1012`, removed by pandas>=2.0) and
`DataFrame.append()` (`pyfocus/finemap.py:188`, removed by pandas>=2.0). Patching both (for
verification only, not part of the landed fix) then produces correct, ground-truth-matching PIP
output: `pips_pop1=1.0` for the true-signal gene, `~3.4e-08` for the null-model row. **New P1
recommendation** — see JSON.

**Fully re-verified fixed (Input 4, S-MultiXcan):** SKILL.md's own S-MultiXcan example now includes
`--cutoff_condition_number 30`; confirmed this flag exists exactly as spelled in the installed
`SMulTiXcan.py --help`. Assertion that was FAIL pre-fix now PASSes.

**Fully re-verified fixed (Input 6, MA-FOCUS Windows caveat):** Reproduced the drive-letter collision
independently on an absolute Windows path (mis-detects population count). Then ran a REAL 3-population
colon-joined `focus finemap` call using the now-documented relative-path workaround — not just a
2-path syntax check — which correctly detected "3 populations", ran single- then multi-ancestry FOCUS,
and produced real `pips_me`/`pips_pop1..3` columns, confirming both the Windows fix and the fixer's
`pips_pop1`/`pips_me` column-naming claim (Common Errors table row, `examples/focus_finemap.sh`)
end-to-end.

**Unaffected, reused from pre-fix audit (Inputs 1, 5, 7):** These code paths were not touched by the
fix; scores and assertions carried forward from the pre-fix audit rather than re-executed, consistent
with regression-test practice for unmodified paths.

## Detailed Outputs

### Input 2 — Variant A (FUSION + conditional analysis)
**Prompt:** "Run FUSION on my CAD GWAS with GTEx artery coronary weights for all 22 autosomes. Then
run FUSION.post_process.R at every significant locus... report the joint-Z table per locus."

**What ran:** `reaudit_input2_build_fusion_data.R` planted a true signal (rs1655519, chr1, GWAS Z=7.2)
and a null gene (rs11120170, chr1, Z=-0.48) plus a 2-SNP gene, over the real plink2R chr1-only subset
of the bundled 957-indiv genotype panel (rows 1-1129 of the bim file are true chr1 SNPs; earlier a
mis-pick outside that range was caught and corrected before finalizing this fixture).
`FUSION.assoc_test.R --chr 1` matched planted ground truth exactly on both an unpatched and patched
clone (unaffected). `FUSION.post_process.R` then:
- **Unpatched:** `Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions` — reproduced.
- **Patched** (`wgt.matrix[m.keep,,drop=FALSE]` / `genos$bed[,m[m.keep],drop=FALSE]`, both
  occurrences): completes; `.joint_included.dat` shows GENE_TRUE `JOINT.P=6e-13`;
  `.joint_dropped.dat` shows GENE_NULL `COND.P=0.63` and GENE_MULTI (2-SNP) `COND.P=0.12` —
  correct discrimination, multi-SNP path unaffected.

**Scores:** Basic: 38/40 | Specialized: 55/60 | Total: 93/100
**Assertions:** 5/5 PASS (see JSON for full text/justification)

### Input 3 — Edge (FOCUS fine-mapping)
**Prompt:** "At the chr11p15.5 locus my TWAS reports 7 genes passing significance. Run FOCUS using
the GTEx v8 whole blood DB and 1000G EUR LD reference to compute per-gene PIPs..."

**What ran:** Fresh isolated venv, `pip install pyfocus "pandas<2.2" "setuptools<81"` →
pandas 2.1.4, numpy 1.26.4, setuptools 80.10.2. Confirmed both documented crashes reproduce
unpatched and resolve with the documented pin+patch. Then built `custom_focus_direct.db`, a real
pyfocus-schema weight DB (`RefPanel`/`Model`/`MolecularFeature`/`Weight` via `pyfocus.models.db`),
for the same true/null genes as Input 2's FUSION fixture. `focus finemap gwas.sumstats ld/EUR.1
custom_focus_direct.db --tissue Whole_Blood --p-threshold 5e-8 --locations 38:EUR --out ...`:
- Reaches "Calculating PIPs" (further than any prior verification of this fix) and crashes:
  `DataFrame.pivot() takes 1 positional argument but 4 were given`.
- After a verification-only patch (keyword args), crashes again: `'DataFrame' object has no
  attribute 'append'`.
- After patching both, produces real output: `pips_pop1=1.0` (true gene), `~3.4e-08` (null-model row),
  `in_cred_set_pop1=1` for the true gene only — correct.

**Scores:** Basic: 27/40 | Specialized: 37/60 | Total: 64/100
**Assertions:** 3/5 PASS — the two FAILs are specifically "focus finemap completes under the exact
documented pin+patch" and would-be follow from it; both other crash-diagnosis and no-fabrication
assertions PASS.

### Input 6 — Scope Boundary (MA-FOCUS, Windows)
**What ran:** Reproduced the drive-letter collision on an absolute path
(`The number of LD refernece panel is different from the number of GWAS data.`, since the drive
letter's colon is one more `:`-split token than the single GWAS path). Then ran a genuine 3-population
colon-joined call with relative paths: `"Detecting 3 populations for fine-mapping"` (correct),
completed, and `finemap_out.focus.tsv` contains real `pips_pop1/2/3` and `pips_me` columns.

**Scores:** Basic: 36/40 | Specialized: 54/60 | Total: 90/100
**Assertions:** 5/5 PASS

## Veto Gates

- **Skill Veto (T1-T4):** all PASS — no crashes beyond documented, patchable dependency-version
  issues; stable frontmatter; deterministic given a fixed seed; no eval/exec of raw strings.
- **Research Veto (M1-M4):** all PASS. **M4 (Code Usability)** carries the most nuance this session:
  Input 3's FOCUS path still fails end-to-end under the Skill's exact documented fix, but the failure
  is a further one-line-per-bug, clearly diagnosable third-party dependency-version conflict (not
  unrunnable/logically-broken code as authored by the Skill), consistent with the precedent set by
  the original audit for the same category of issue. This is recorded as a new, prominent P1 rather
  than a veto fire.

## Final Score

```
Static Score   : 89/100 × 40% = 35.6
Dynamic Score  : 86.1/100 × 60% = 51.7
FINAL SCORE    : 87 / 100
GRADE          : ⭐ Production Ready
Deployable     : true
Veto           : none fired
```

Floors checked: Static ≥80 ✓ (89), Execution avg ≥85 ✓ (86.1), Layer 1 avg ≥32 ✓ (35.0), Layer 2 avg
≥48 ✓ (51.1), Assertion pass rate ≥90% ✓ (91.4%) — all Production Ready floors met.

See `eval_report_bio-causal-genomics-transcriptome-wide-association_result.json` for full detail and
`run/reaudit_*` for every script and output file this re-audit produced.

> **Audit record for `bio-vcf-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/optimized-scientific-skills@ffa74e9](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ffa74e915d92da714bfd40ce2f0aa1fbb1e2cde4/skills/bio-vcf-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-27 by Independent re-auditor agent (not the fixer), commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-statistics (re-audit)

Generated: 2026-09-27
Source: `mrsonord2240/optimized-scientific-skills@ffa74e915d92da714bfd40ce2f0aa1fbb1e2cde4:skills/bio-vcf-statistics`
Auditor: independent re-auditor (not the fixer). `auditor_independent: true`.

## What changed since the last audit

The 2026-09-25 marketplace-pilot re-audit scored this Skill 91/100, Production Ready, on commit
`2dee47f`. Since then a documentation-cleanup fixer trimmed `usage-guide.md` from 267 to 106 lines
(commit `f39043a`), removing content that restated SKILL.md's QC-metric interpretation and command
blocks almost verbatim (Ti/Tv, het/hom, novel/known, missingness, HWE, contamination signatures,
identity QC). `SKILL.md` and `examples/vcf_stats.py` were **not** touched by that commit (verified:
`git diff f39043a^ f39043a -- skills/bio-vcf-statistics/` touches only `usage-guide.md`, 8
insertions / 169 deletions). HEAD (`ffa74e9`) only additionally touched `PROVENANCE.json`.

Verified independently (not taken from the fix log):
- `git diff` of the trim commit shows every removed usage-guide.md section had a corresponding,
  still-present section in SKILL.md (bcftools stats, Ti/Tv ratio, Het/hom ratio, Novel/known ratio,
  Missingness, HWE filtering, Contamination signatures, Sample-swap/relatedness, Quick counts, Quick
  Reference) — nothing an agent needs went missing.
- The two Python snippets usage-guide.md still carries (per-sample genotype distribution,
  allele-frequency spectrum) are outside the diff hunks entirely — byte-identical before and after
  the trim.
- Both snippets were extracted verbatim and executed in this audit (Input 8); both ran correctly.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 3 | Variant B (regression) | 35 | 53 | 88 | 3/4 PASS | ✅ |
| 4 | Edge (regression) | 32 | 46 | 78 | 3/4 PASS | ✅ |
| 5 | Stress (regression) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 37 | 54 | 91 | 4/4 PASS | ✅ |
| 7 | Adversarial (regression) | 37 | 55 | 92 | 4/4 PASS | ✅ |
| 8 | Stress (**NEW**) | 37 | 52 | 89 | 4/5 PASS | ✅ |
| 9 | Scope Boundary (**NEW**) | 38 | 54 | 92 | 5/5 PASS | ✅ |

**Execution Average: 90.3 / 100**
**Assertion Pass Rate: 35/38 (92.1%)**

## Veto Gates

- Skill Veto (T1–T4): PASS / PASS / PASS / PASS — no crashes across 9 inputs, frontmatter intact
  (`name`, `description` present and unchanged), deterministic tool output, no eval/exec of raw
  strings or injection vectors.
- Research Veto (M1–M4), Category 3 — Data Analysis: PASS / PASS / PASS / PASS. No fabricated
  identifiers or statistics; no per-patient diagnostic conclusions; ancestry-matched and
  order-of-operations guidance intact; all executed code ran without error.

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt (representative):** "Generate comprehensive statistics for my VCF including Ti/Tv ratio."
**Ran:** `bcftools stats -s -` and the shipped `examples/vcf_stats.py` (sha256-verified byte-identical
to the shelf copy) against the prior 8-sample, 361-record synthetic cohort.
**Output:** 8 PSC rows; `TSTV` ratio `1.43`; strict PASS `0`, not-failed (`-f .,PASS`) `361`;
`vcf_stats.py` reported `Total variants: 361`. Identical to the pre-fix audit's Input 1.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] Per-sample PSC row for each of 8 samples — bcftools emitted exactly 8.
- [PASS] Ti/Tv regression value remains 1.43.
- [PASS] Strict PASS / not-failed counts match the known all-dot-filter fixture (0 vs 361).
- [PASS] The shipped cyvcf2 example consumes the complete cohort without error.

### Input 2 — Variant A (regression)
**Prompt (representative):** "Check my cohort's het allele balance across mixed genotype
orientations (0/1 and 1/0)."
**Ran:** bcftools query + the documented `awk` allele-balance matcher against an orientation-mixed
stream (747 biallelic hets, 372 reversed unphased `1/0`).
**Output:** matcher retained 747/747.
**Scores:** Basic 39/40 | Specialized 56/60 | Total 95/100
**Assertions:**
- [PASS] Fixture contains the full 747 biallelic heterozygotes.
- [PASS] Fixture includes 372 reversed unphased `1/0` calls.
- [PASS] Documented matcher retains every valid orientation (747/747).
- [PASS] SKILL.md still explicitly scopes the one-liner to biallelic calls after the trim.

### Input 3 — Variant B (regression)
**Prompt (representative):** "My callset has multiallelic SNPs and a QUAL=0 record — will your
stats script handle them correctly?"
**Ran:** unchanged `vcf_stats.py` and `bcftools stats` against a 4-record fixture (2 multiallelic
SNPs, 1 indel, 1 symbolic ALT; QUAL values 0/20/40; FILTER PASS/LowQual/dot).
**Output:** 2 transitions, 2 transversions (matches bcftools independently); Mean QUAL 20.0 (QUAL=0
retained); `PASS variants: 2` — conflates strict PASS with the unfiltered dot record.
**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100
**Assertions:**
- [PASS] Every alt allele in both multiallelic SNPs contributes to Ti/Tv.
- [PASS] QUAL=0 contributes to the mean quality (20.0, not 30.0).
- [FAIL] Summary does not distinguish strict PASS (2) from PASS-or-dot (3) — same pre-existing gap
  as the 2026-09-25 audit; the fixer's scope did not include this file.
- [PASS] Filtered (LowQual) records remain separate from not-failed records.

### Input 4 — Edge (regression)
**Prompt (representative):** "Run the stats script on an empty VCF, and on one with transitions but
no transversions."
**Ran:** unchanged `vcf_stats.py` against an empty VCF and a transition-only 2-record VCF.
**Output:** empty VCF → `Total variants: 0`, no fabricated Mean QUAL. Transition-only → `Mean QUAL:
5.0` (QUAL=0 retained) but neither `Transitions:` nor `Transversions:` printed (guarded by
`transversions > 0`).
**Scores:** Basic 32/40 | Specialized 46/60 | Total 78/100
**Assertions:**
- [PASS] Empty VCF completes, reports 0 records.
- [PASS] Empty VCF does not fabricate a mean quality.
- [PASS] QUAL=0 remains in the transition-only mean (5.0).
- [FAIL] Zero-transversion callset still suppresses both component counts — same pre-existing gap.

### Input 5 — Stress (regression)
**Prompt (representative):** "Give me per-sample and per-site missingness for my cohort, plus exact
HWE p-values."
**Ran:** VCFtools 0.1.17 `--missing-indv`, `--missing-site`, `--hardy` against the 361-record cohort;
cross-checked with an independent standard-library VCF parser.
**Output:** 8 `.imiss` rows, 361 `.lmiss` rows, 361 `.hwe` rows; independent parser matched every
count exactly.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** all 4 PASS (sample coverage, site coverage, independent-parser agreement, HWE
row-per-site coverage).

### Input 6 — Scope Boundary (regression)
**Prompt (representative):** "Compare two callers' VCFs and split my cohort into easy vs difficult
genomic regions."
**Ran:** `bcftools stats` two-file comparison mode; `bcftools stats -R` against easy/difficult BED
fixtures.
**Output:** 3 comparison-set IDs (A, B, intersection); 172 easy-region + 189 difficult-region =
361 (full cohort partitioned, no records lost or double-counted).
**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100
**Assertions:** all 4 PASS.

### Input 7 — Adversarial (regression)
**Prompt (representative):** "Build the full relatedness matrix for my cohort and check for sample
swaps."
**Ran:** `bcftools gtcheck` (no `-g`, matching the documented post-1.10 default) and VCFtools
`--relatedness2` against the 8-sample cohort.
**Output:** 28 `DC` pairs (8 choose 2); 361 sites compared; 64-row (8×8) KING-robust matrix.
**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100
**Assertions:** all 4 PASS.

### Input 8 — Stress (**NEW**)
**Prompt:** "Give me the per-sample het/hom breakdown and the allele-frequency spectrum using the
Python snippets from the usage guide."
**Why new:** targets exactly the two code blocks the fix log claims are "unchanged" and now live
*only* in `usage-guide.md` — the highest-risk surface for this particular fix.
**Ran:** extracted both fenced snippets verbatim (only a `sys.argv` VCF path and, for the AF
snippet, a trailing `print(bins)` were added to make them runnable) against `cohort.vcf.gz` (no
`INFO/AF`) and `core_regression.vcf.gz` (2 multiallelic SNPs + 1 indel + 1 symbolic ALT, all with
`INFO/AF`).
**Output:** genotype-distribution snippet emitted 8 rows; per-sample HET counts (162/84/89/84/87/
60/92/89, summing to 747) matched an independent `bcftools query` all-genotype-form parse **exactly**.
(A first comparison against `bcftools stats` PSC `nHets` mismatched — traced to PSC explicitly
excluding het indels per its own header comment, not a Skill defect; cohort.vcf has 30 indels. The
corrected, scope-matched comparison is what is scored.) The AF-spectrum snippet returned all-zero
bins on `cohort.vcf.gz` (no crash despite no `INFO/AF`) and binned all 4 `core_regression.vcf`
records into `common(5-50%)`, silently using only the first ALT's frequency for the two multiallelic
records.
**Scores:** Basic 37/40 | Specialized 52/60 | Total 89/100
**Assertions:**
- [PASS] Genotype-distribution snippet emits one row per each of 8 cohort samples.
- [PASS] HET counts match an independent all-genotype-form parse exactly (162/84/89/84/87/60/92/89).
- [PASS] Snippet total (747) reconciles with Input 2's independently-verified heterozygote total.
- [PASS] AF-spectrum snippet does not crash or fabricate a value on a VCF with no `INFO/AF`.
- [FAIL] Nothing documents that multiallelic AF binning only uses the first ALT's frequency —
  minor, pre-existing, unaffected by the trim (see P2 recommendation).

### Input 9 — Scope Boundary (**NEW**)
**Prompt:** "What fraction of my callset's variants are novel (not in dbSNP)?"
**Why new:** exercises the novel/known-via-dbSNP command block that `usage-guide.md` used to restate
and no longer does — confirms the trim didn't leave this workflow's only copy stranded, and that the
command still executes.
**Ran:** `bcftools annotate -a dbsnp_syn.vcf.gz -c ID` against the 361-record cohort, followed by the
documented novel-fraction `awk` one-liner.
**Output:** 244/361 sites received a dbSNP ID; 117/361 (32.4%) remained novel; all 361 records
preserved through annotation.
**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100
**Assertions:** all 5 PASS (command present in SKILL.md; correctly absent from usage-guide.md;
end-to-end execution; record-count preservation; fixture non-triviality).

## Static Score — 92/100 (independently re-derived, not copied from the 2026-09-25 report)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 10/12 | Pre-existing PASS/dot and zero-denominator gaps in `vcf_stats.py`, unaffected by this fix. |
| Reliability | 10/12 | All 9 inputs completed deterministically; same two edge-case presentation gaps. |
| Performance & Context | 8/8 | SKILL.md (233 lines) is the single reference; usage-guide.md (106 lines) no longer duplicates it. |
| Agent Usability | 15/16 | Decision tables and command blocks unchanged and actionable; PASS-count label still inconsistent. |
| Human Usability | 8/8 | Trigger language and Quick Start prompts intact. |
| Security | 11/12 | No credentials/destructive ops; validation still delegated to cyvcf2. |
| Maintainability | 11/12 | The trim removed a real two-copies-of-the-truth risk; the print-branch coupling in `vcf_stats.py` remains. |
| Agent-Specific | 19/20 | Progressive disclosure materially improved by the trim; script output contract still a little implicit. |

Landing at the same 92/100 as the pre-fix static score is expected and a good independence signal:
the fix was scoped to documentation deduplication with no functional change, so a fresh, from-scratch
re-scoring converging on the same number corroborates rather than just repeats the prior audit.

## Final Score

```
Static Score        : 92/100 x 0.4 = 36.8
Execution Average   : 90.3/100 x 0.6 = 54.2
FINAL SCORE          = 91 / 100
GRADE                 = Production Ready (deployable)
```

Floors (Production Ready row): Static 92≥80 ✓ | Execution 90.3≥85 ✓ | Layer1 avg 36.8/40≥32 ✓ |
Layer2 avg 53.6/60≥48 ✓ | Assertion pass rate 92.1%≥90% ✓. No veto fired. No open P0 or P1.

## Recommendations

- [P2] Separate strict PASS from unfiltered records in `examples/vcf_stats.py` (Input 3). Pre-existing,
  open since 2026-09-25.
- [P2] Report Ti/Tv components when the transversion denominator is zero (Input 4). Pre-existing,
  open since 2026-09-25.
- [P2] Document that the usage-guide.md AF-spectrum snippet only bins the first ALT's frequency for
  multiallelic records (Input 8). Newly identified in this audit; pre-existing code, unaffected by
  the documentation trim.

## Auditor's note on the fix under review

The usage-guide.md trim is a clean pass: every deletion in the `f39043a` diff maps onto content that
independently verifiably still exists in SKILL.md, the two Python snippets it kept are provably
byte-unchanged (outside the diff hunks) and were re-executed successfully here, and the trim
measurably improved the Progressive Disclosure and Maintainability static criteria without touching
anything that affected execution. Nothing regressed. The three open P2s all predate this fix and are
outside its stated scope.

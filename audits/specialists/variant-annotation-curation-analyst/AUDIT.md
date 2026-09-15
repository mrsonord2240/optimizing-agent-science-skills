# variant-annotation-curation-analyst — Skill re-audit after fixes (2026-09-15)

Upstream is now the fixed fork: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116` (MIT), branch `openscience-fixes`.
Method: `skills/skill-auditor`, as in the first audit: Skill Veto, then the 25-criterion static score, then execution, then Layer 1/2/3 scoring, the Research Veto, and the final score with its floors. The auditor did not fix these Skills.

- **Evidence per Skill:** `F:\OpenScience\audits\<skill-id>\eval_report_<id>_result.json`, `eval_viewer_<id>.md` and `runs/`. Regression runs are in `runs/p_in*` and new inputs in `runs/in6+`.
- **Pre-fix reports:** `F:\OpenScience\audits\_pre-fix-20260915\`.
- **Fix logs:** `round2\fixes\<id>.md`. They were read for context only, not taken as evidence.

## Audited Skills

All eleven Skills are Data Analysis, Mode A. "Veto" means Skill Veto / Research Veto.

Every pre-fix input was re-run as a regression test against the fork commit. Each Skill also got two new inputs, except vcf-basics.

**Inputs executed: 79/79.** They ran on:
- bcftools 1.24 (Windows) and 1.21 (WSL);
- GATK 4.6.1.0, cyvcf2, vt, VEP 114.2, vcftools, somalier, plink2, regenie 4.1.3, SAIGE 1.3.1 and SKAT 2.2.5;
- the live ClinVar/E-utilities, ClinGen Allele Registry, gnomAD GraphQL, NCBI Variation Services and myvariant.info services.

Not executed within inputs:
- GATK FilterMutectCalls, VETS and NVScoreVariants (flags checked only);
- the SAIGE bgen form (argument handling only, no .bgen built);
- the Hail and STAAR snippets (parsed only);
- SnpEff and ANNOVAR.

| Skill ID | Role | N | Executed | Static | Exec avg | Final | Grade | Veto | Top open issue |
|---|---|---|---|---|---|---|---|---|---|
| bio-vcf-basics | core | 5 | 5/5 | 89 | 90.8 | 90 | ⭐ Production Ready | PASS/PASS | P2 wrong `query -H` tip. Folder byte-identical to d91ed3d, so the 2026-09-11 audit is reused and only `source` was updated. |
| bio-variant-normalization | core | 7 | 7/7 | 88 | 89.9 | 89 | ⭐ Production Ready | PASS/PASS | P2 csq `-p m`/`-p s` described wrongly |
| bio-variant-calling-filtering-best-practices | core | 9 | 9/9 | 89 | 87.2 | 88 | ⭐ Production Ready | PASS/PASS | P2 tumor-column block segfaults when `##tumor_sample` is missing; P2 usage-guide allele-balance include drops hom-alt sites |
| bio-variant-annotation | core | 9 | 9/9 | 86 | 85.9 | 86 | ✅ Limited Release (assertion floor 89 %) | PASS/PASS | **P1** csq `--phase` m/s described wrongly (s skips unphased hets; m merged a trans pair); P2 SKILL.md annotate line needs an indexed target |
| bio-vcf-statistics | core | 7 | 7/7 | 88 | 87.7 | 88 | ⭐ Production Ready | PASS/PASS | P2 het-AB one-liner ignores `1\|0`; P2 `view -f PASS` vs FILTER '.' |
| bio-population-genetics-rare-variant-association | core | 7 | 7/7 | 90 | 89.0 | 89 | ⭐ Production Ready | PASS/PASS | P2 SAIGE bgen command lacks `--chrom`/`--LOCO=FALSE` |
| bio-vcf-manipulation | supporting | 7 | 7/7 | 89 | 90.7 | 90 | ⭐ Production Ready | PASS/PASS | P2 `view -s` reorder does not make `concat --naive` work |
| bio-clinical-databases-clinvar-lookup | supporting | 7 | 7/7 | 82 | 85.1 | 84 | ✅ Limited Release | PASS/PASS | P2 batch CA-ID helper aborts on a Registry HTTP 500 |
| bio-clinical-databases-gnomad-frequencies | supporting | 7 | 7/7 | 84 | 87.0 | 86 | ⭐ Production Ready | PASS/PASS | P2 no HTTP 429 handling (hit in these runs) |
| bio-clinical-databases-dbsnp-queries | supporting | 7 | 7/7 | 83 | 87.6 | 86 | ⭐ Production Ready | PASS/PASS | P2 batch table drops annotations for merged rsIDs |
| bio-clinical-databases-myvariant-queries | supporting | 7 | 7/7 | 80 | 86.0 | 84 | ✅ Limited Release | PASS/PASS | P2 `_id` is GRCh37 but not stated; P2 Lucene escape example returns 0 hits |

### Pre-fix → post-fix final score

- bio-vcf-basics: 90 → 90 (unchanged folder)
- bio-variant-normalization: 86 → 89
- bio-variant-calling-filtering-best-practices: 85 → 88
- bio-variant-annotation: 86 → 86
- bio-vcf-statistics: 87 → 88
- bio-population-genetics-rare-variant-association: 85 → 89
- bio-vcf-manipulation: 88 → 90
- bio-clinical-databases-clinvar-lookup: 73 → 84
- bio-clinical-databases-gnomad-frequencies: 77 → 86
- bio-clinical-databases-dbsnp-queries: 66 → 86
- bio-clinical-databases-myvariant-queries: 67 → 84

**Service condition.** The fixer reported that myvariant.info's HTTPS certificate did not match its hostname earlier on 2026-09-15. Re-checked the same day before the runs:
- openssl shows CN=myvariant.info, SAN myvariant.info/*.myvariant.info, valid 2026-09-06 to 2027-03-22;
- curl and Python requests both return HTTP 200.

Every myvariant-based route ran over HTTPS as written, so there was no outage to record. The gnomAD GraphQL API rate-limited these runs (HTTP 429) and they were retried after waiting; the complete outputs are what was scored.

## Read but not chosen (unchanged from the first audit)

- bio-variant-calling, bio-gatk-variant-calling, bio-variant-calling-deepvariant, bio-variant-calling-joint-calling — calling upstream of the curation workflow.
- bio-variant-calling-structural-variant-calling — SV discovery; a different variant class and toolchain.
- bio-consensus-sequences — builds consensus FASTA; not variant curation.
- bio-variant-calling-clinical-interpretation, bio-clinical-databases-acmg-classification — assign ACMG/AMP classifications and tiers (gate 7).
- bio-clinical-databases-variant-prioritization — diagnostic trio pipeline and secondary findings, i.e. individual-level triage (gate 7).
- bio-clinical-databases-pharmacogenomics, -msi-detection, -tumor-mutational-burden — patient prescribing, screening or eligibility (gate 7).
- bio-clinical-databases-hla-typing, -somatic-signatures, -polygenic-risk — outside variant curation.
- bio-population-genetics-association-testing, -plink-basics, -linkage-disequilibrium, -population-structure, -scikit-allel-analysis, -selection-statistics — single-variant GWAS or population genetics beyond this workflow, or overlapping vcf-statistics.

## Verdict

**Viable for the full scope in CANDIDATES.md, including database evidence.** `spec.json` bundles all 11 Skills: 6 core and 5 supporting.

- **Gate 2 (every bundled Skill audited and deployable): PASS.**
  - All 11 are deployable, with no veto and no P0.
  - The four database Skills moved from Beta Only (66–77) to 84–86 and are now bundled. ClinVar, gnomAD, dbSNP and MyVariant evidence therefore has deployable Skills.
- **Gate 3 (core Skills Production Ready): PASS on the numeric rule, with one caveat on the grade reading.**
  - All six core Skills score ≥ 85: 90, 89, 88, 86, 88, 89.
  - Five are graded Production Ready. bio-variant-annotation scores 86 but is graded Limited Release, because its assertion pass rate (32/36, 89 %) misses the 90 % floor.
  - The miss comes from a defect the fix introduced: the `csq --phase` m/s description. Correcting that text is the one change needed for every core Skill to be Production Ready.
- **Gate 4 (end-to-end coverage, ≥ 3 core): PASS.**
  - Central operation: normalization, filtering and annotation.
  - Validation: vcf-statistics.
  - Cohort prioritization: rare-variant association.
  - Evidence: the four database Skills.
  - Framing is still carried by method selection inside filtering and rare-variant association; there is no dedicated design Skill.
- **Gate 7 (research scope): PASS.**
  - Every request to classify, diagnose or advise an individual was declined: annotation input 6, rare-variant input 7, ClinVar inputs 5 and 7, gnomAD inputs 5 and 7, myvariant inputs 5 and 7.
  - No output classified an individual's variant clinically.
  - The ClinVar, gnomAD and MyVariant Skills now state research-use scope or data governance.
  - Frequency tags such as BS1/BA1/PM2 are applied only as variant-level research annotation.
- **Gate 8 (shipped means present): PASS.** No bundled SKILL.md or usage guide names a missing local file. The two grep hits were prose ("transcripts/gene") and a clinicalgenome.org URL.

**Recommended before release, not blocking:**
1. Fix the `bcftools csq --phase` wording in variant-annotation and variant-normalization to match the tool's help (a = GTs as is, m = merge all, s = skip unphased hets).
2. Add the index step to the variant-annotation annotate line.
3. Clear the P2s in the table above, notably: myvariant `_id` build and escape advice, gnomAD 429 handling, and the dbSNP merged-rsID annotation.

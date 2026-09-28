> **Audit record for `bio-atac-seq-allele-specific-accessibility`**
> - Audited working candidate `1e03ae9e381527982e1bc41be03aedb9934c37655091da90d13d443d201e1e6f`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/allele-specific-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-atac-seq-allele-specific-accessibility

Generated: 2026-09-28  
Audit type: bounded diagnostic initial audit  
Exact candidate content SHA-256:
`1e03ae9e381527982e1bc41be03aedb9934c37655091da90d13d443d201e1e6f`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 10 | 12 | 22 | 1/5 | ❌ ERROR |
| 2 | Variant A | 15 | 12 | 27 | 1/5 | ❌ PARTIAL |
| 3 | Edge | 10 | 8 | 18 | 1/5 | ❌ PARTIAL |
| 4 | Variant B | 25 | 31 | 56 | 3/5 | ⚠️ COMPLETED |
| 5 | Stress | 18 | 20 | 38 | 1/5 | ❌ PARTIAL |

**Execution average:** 32.2 / 100  
**Assertion pass rate:** 7 / 25  
**Static score:** 56 / 100  
**Final score:** 42 / 100 — ❌ Reject  
**Research veto:** FAIL — Methodological Ground and Code Usability

This score is diagnostic. It does not make the candidate ready. The exact
schema-valid report is [`report.json`](report.json), the ordered remediation
sequence is [`finding-ledger.md`](finding-ledger.md), and exact identity is in
[`source-identity.json`](source-identity.json).

## Veto review

### Skill veto — PASS

- Stability: PASS under the rubric's narrow structural redline. The sampled
  real core failure is scored dynamically and under Research Code Usability.
- Contract: PASS for required frontmatter and basic artifact shape.
- Determinism: PASS; the observed defects reproduce deterministically.
- Security: PASS for the hard redline; no eval/exec of raw input, credential
  exposure, or prompt-injection path was found.

### Research veto — FAIL

- Scientific Integrity: PASS. No run result, DOI, PMID, sample size, or p-value
  was fabricated.
- Practice Boundaries: PASS. The workflow stays in research analysis scope.
- Methodological Ground: **FAIL.** Peak pooling sums locus-specific REF labels
  without haplotype orientation, and the multi-sample filter allows a site that
  is homozygous in the target BAM sample to reach GATK.
- Code Usability: **FAIL.** The real candidate merge is unindexable. Sorting
  alone exposes a second defect: zero read groups cause GATK to exit 0 with an
  empty output.

## Detailed outputs

### Input 1 — Canonical: real single-sample WASP-to-GATK core stages

**Prompt:** Run the shipped single-sample workflow on the bounded public
GM12878/NA12878 chr1 data after WASP remapping. Verify that the merged BAM is
coordinate-sortable and indexable, that sample read groups survive or are
restored, and that GATK ASEReadCounter emits non-empty checked-value output.

**Execution:** The audit reused the prepared real WASP intermediates but ran
the candidate's exact merge and index operations independently. It then used a
sort-only diagnostic and an add-read-group positive control to isolate the two
orchestration defects.

**Output:**

```text
candidate_exact_merge_rc=0
candidate_exact_index_rc=1
candidate_header_sort_order=coordinate
candidate_header_read_groups=0
candidate_merged_reads=268176
candidate_index_stderr=Unsorted positions ... 9989 followed by 9986 ... failed to create index
sorted_without_read_group_gatk_rc=0
sorted_without_read_group_rows=0
sorted_with_read_group_gatk_rc=0
sorted_with_read_group_rows=953
sorted_with_read_group_depth30_rows=28
```

Full transcript: [`evidence/candidate-merge.txt`](evidence/candidate-merge.txt).

**Scores:** Basic 10/40 | Specialized 12/60 | Total 22/100

**Assertions:**

- PASS — The candidate merge preserves 268,176 retained reads.
- FAIL — The BAM is not actually coordinate sorted or indexable.
- FAIL — The pipeline preserves or creates no valid sample read group.
- FAIL — Candidate-equivalent GATK output is empty.
- FAIL — The workflow has no zero-row GATK postcondition.

**Finding:** `ASA-001` (P0).

### Input 2 — Variant A: peak aggregation and empty-result boundaries

**Prompt:** Aggregate two depth-100 heterozygous sites in one peak, then repeat
with opposite REF/ALT directions, a valid peak set with no overlaps, all sites
below the depth threshold, and a named BED4. Preserve biological allele
orientation and return an explicit empty result for valid no-call cases.

**Execution:** The exact candidate helper ran against five deterministic
fixtures in the pinned Python/bedtools environment.

**Output:**

```text
same_reference_direction rc=0 rows=1 ref_frac=0.900000 snp_count=2 adj_p=2.2558606e-33
opposite_reference_direction rc=0 rows=0
no_peak_overlap rc=1 output=no KeyError: score,strand,thickStart
all_below_depth rc=1 output=no KeyError: score,strand,thickStart
bed4_named rc=0 rows=1 peak=chrAudit_99_250
```

The prepared missing-schema fixture independently exits 1 with
`KeyError: 'total'`. Full transcript:
[`evidence/helper-boundaries.txt`](evidence/helper-boundaries.txt).

**Scores:** Basic 15/40 | Specialized 12/60 | Total 27/100

**Assertions:**

- PASS — The simple same-REF-direction fixture produces a parsed row.
- FAIL — Alleles are not oriented to a shared haplotype.
- FAIL — A valid no-overlap case crashes instead of returning an empty table.
- FAIL — An all-below-depth case crashes instead of returning an empty table.
- FAIL — Output omits counts/coverage and all non-significant or underpowered
  peak statuses.

**Findings:** `ASA-003` (P0), `ASA-004` (P1).

### Input 3 — Edge: multi-sample genotype and sample-identity boundary

**Prompt:** Use a two-sample VCF in which NA12878 is homozygous and donor2 is
heterozygous at a covered site. Run the candidate filter for an NA12878 BAM,
confirm exactly one target sample is selected, enforce BAM/VCF identity, and
verify that the target-homozygous site never reaches allele counting.

**Execution:** The exact candidate bcftools expression was applied to a
two-sample VCF. A two-stage sample-first filter was the negative control. The
candidate-filtered VCF was passed to GATK with the valid positive-control BAM.

**Output:**

```text
candidate_filter_records=1
candidate_filter_samples=NA12878,donor2
candidate_filter_genotypes=NA12878=0|0,donor2=0|1,
target_scoped_control_records=0
gatk_rows_from_candidate_filter=1
gatk_first_row=variant=rsAuditTargetHom;ref=1;alt=2;total=3
```

Full transcript: [`evidence/multisample.txt`](evidence/multisample.txt).

**Scores:** Basic 10/40 | Specialized 8/60 | Total 18/100

**Assertions:**

- PASS — Biallelic SNP filtering is requested.
- FAIL — Exactly one BAM target sample is not selected first.
- FAIL — A target-homozygous/other-heterozygous record is retained.
- FAIL — BAM read-group identity is not checked against VCF samples.
- FAIL — GATK emits a count row for the target-homozygous record.

**Finding:** `ASA-002` (P0).

### Input 4 — Variant B: public RASQUAL feature analysis

**Prompt:** Run the documented RASQUAL branch on the pinned public C11orf21
data. Verify live flags, a finite result, correct feature-SNP/testing-SNP
counts, per-feature row routing for more than one feature, and a
multiple-testing plan for cohort reporting.

**Execution:** The pinned RASQUAL binary at
`5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6` ran both the candidate's
one-feature flag shape and the public bundled positive control. The
multi-feature loop was inspected against the live `-j` interface.

**Output:**

```text
candidate_documented_shape_rc=0
candidate_documented_shape_rows=83
candidate_documented_shape_stderr=
public_control_rc=0
public_control_rows=1
public_control_chi_square=65.8515964475
```

Full transcript:
[`evidence/rasqual-candidate.txt`](evidence/rasqual-candidate.txt).

The one-feature invocation is usable. The documented loop passes the same
undeclared `FEATURE_INDEX` to `-j` for every feature and never increments it.
The high-confidence reporting rule also uses a fixed raw p-value rather than a
declared cohort correction.

**Scores:** Basic 25/40 | Specialized 31/60 | Total 56/100

**Assertions:**

- PASS — The documented flags match the pinned interface.
- PASS — The public control returns a finite populated result.
- PASS — The prose requires exact VCF-window counts and zero-fSNP skipping.
- FAIL — The binary matrix row index does not advance per feature.
- FAIL — No cohort multiple-testing procedure is specified.

**Finding:** `ASA-005` (P1).

### Input 5 — Stress: cohort and genotype-free routing with claim audit

**Prompt:** Design executable analyses for an at-least-100-sample MatrixEQTL
caQTL cohort and a no-genotype QuASAR case. Specify input schemas,
model/QC/output contracts, multiplicity control, when phasing is required, and
the evidence needed before using the 1.5-3x power or greater-than-70-percent
concordance heuristics.

**Execution:** This surface is **static-only**. MatrixEQTL 2.4 and QuASAR 0.1
load in the prepared environment, but the candidate contains no runnable file,
dataset, input schema, or expected output for either branch. Tool availability
is readiness evidence, not candidate execution credit.

**Output:**

- MatrixEQTL: method routing and installation only; no covariate model,
  genotype/peak matrix contract, cis-window definition, QC, correction, or
  parsed output.
- QuASAR: method routing and installation only; no ATAC-to-allele-count
  preparation, function call, fit checks, or parsed output.
- Phasing: candidate language is universal, while pinned WASP explicitly
  enumerates all allele combinations at unphased sites and GATK per-site
  counting does not itself require phase. Phase remains required when counts
  are oriented to shared haplotypes.
- Claims: the RASQUAL paper supports qualitative power gains, not a universal
  1.5-3x multiplier. The provider-derived >70% concordance rule defines no
  statistic, denominator, calibration set, or null. The cohort raw p < 1e-5
  rule is not study-specific multiplicity control.

Scientific notes: [`scientific-source-notes.md`](scientific-source-notes.md).

**Scores:** Basic 18/40 | Specialized 20/60 | Total 38/100

**Assertions:**

- PASS — The decision table routes both analysis settings.
- FAIL — MatrixEQTL is not executable from the shipped contract.
- FAIL — QuASAR is not executable from the shipped contract.
- FAIL — Cohort significance is not controlled for the actual test family.
- FAIL — Phase, power, and concordance claims are not correctly scoped and
  evidenced.

**Findings:** `ASA-006` (P1), `ASA-007` (P1).

## Static scoring

| Category | Score | Max | Main reason for deduction |
|---|---:|---:|---|
| Functional suitability | 5 | 12 | Broken core path, misoriented pooling, incomplete branches |
| Reliability | 3 | 12 | Raw empty/schema failures, silent zero-row result, weak recovery |
| Performance/context | 6 | 8 | Good disclosure; no resume/stage validation |
| Agent usability | 9 | 16 | Clear routing, but unenforced invariants and vague outputs |
| Human usability | 5 | 8 | Discoverable but brittle |
| Security | 7 | 12 | No secrets/eval; input/path/output-state checks missing |
| Maintainability | 8 | 12 | Good separation; no regression coverage |
| Agent-specific | 13 | 20 | Strong trigger/disclosure; weak composition/idempotency/escape hatches |
| **Total** | **56** | **100** | |

## Ordered remediation

1. `ASA-001` P0 — sort/index final BAM, preserve/add validated read groups,
   assert non-empty GATK output.
2. `ASA-002` P0 — enforce one BAM/VCF sample before target-specific GT filter.
3. `ASA-003` P0 — orient pooled SNPs to a shared haplotype or replace the
   pooled model.
4. `ASA-004` P1 — validate helper schemas and make empty/no-call output stable.
5. `ASA-005` P1 — increment and validate RASQUAL feature rows; define
   multiplicity control.
6. `ASA-006` P1 — make MatrixEQTL/QuASAR bounded executable branches or narrow
   their claims.
7. `ASA-007` P1 — correct phase scope and remove/source fixed scientific
   heuristics.
8. `ASA-008` P2 — harden canonical provenance, path quoting, and reruns.

No audit-local repair was attempted because each change affects method,
interface, validation, or provenance judgment.

## Environment and limitations

- Tooling record:
  `F:\OpenScience\audit-envs\bio-atac-seq-allele-specific-accessibility\TOOLS.md`
  (SHA-256
  `ca90f50072d3d7bc6a0e595a2b825b69f983fe686555d12300271f89d0c08dc2`).
- Environment fingerprint:
  `5a5eade861ecf5133d8163ee303ad396c8b565120bdb028a747118de0135a7de`.
- WASP: `d3b8447fd7719fffa00b856fd1f27c845554693e`.
- RASQUAL: `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6`.
- GATK 4.6.2.0; samtools/bcftools 1.21; Python 3.11.9; pandas 2.3.3;
  SciPy 1.17.1; pybedtools 0.10.0; bedtools 2.31.1.
- Restricted-access blockers: none.
- Deferred/static-only executable surfaces: MatrixEQTL and QuASAR, because no
  candidate runnable surface or specified dataset exists.
- Whole-genome/cohort-scale performance, new phasing, experimental validation,
  and exhaustive method comparison remain out of scope for this diagnostic
  pass.

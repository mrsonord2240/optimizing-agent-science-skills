> **Audit record for `bio-chipseq-allele-specific-binding`**
> - Audited working candidate `a058f8a1b36e22f587781bc63dfc65efaef7817c7be1374aaf367ca7dedcb111`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/chip-seq/allele-specific-binding), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-chipseq-allele-specific-binding

Generated: 2026-09-28

Exact candidate content SHA-256:
`a058f8a1b36e22f587781bc63dfc65efaef7817c7be1374aaf367ca7dedcb111`.
The candidate subtree was unchanged during this audit.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical — paired-end WASP | 20 | 27 | 47 | 3/5 | ❌ PARTIAL |
| 2 | Variant A — cancer BaalChIP | 9 | 11 | 20 | 2/5 | ❌ PARTIAL |
| 3 | Edge — imprinting and chrX filters | 30 | 40 | 70 | 3/5 | ⚠️ COMPLETED |
| 4 | Variant B — public RASQUAL | 27 | 38 | 65 | 3/5 | ❌ PARTIAL |
| 5 | Stress — AlleleSeq route | 13 | 18 | 31 | 2/5 | ❌ PARTIAL |

**Static score:** 57/100  
**Execution average:** 46.6/100  
**Assertion pass rate:** 13/25  
**Weighted score:** 51/100 — **Reject**

Skill veto: **PASS**. Research veto: **FAIL** for Methodological Ground and
Code Usability. No audit-local repair was attempted because every required
change alters a scientific method, execution interface, or validation contract.

## Detailed outputs

### Input 1 — Canonical: paired-end WASP mapping-bias route

**Prompt:** Apply the documented paired-end WASP route, preserve the remap
contract, and verify retained paired alignments and attrition counts.

**Execution:** The pinned WASP v0.3.4 surface was rerun in the prepared WSL
environment. Four input alignments produced separate `input.remap.fq1.gz` and
`input.remap.fq2.gz` files and four retained paired final alignments. The exact
candidate command instead names `step1.remap.fq.gz`, passes only `-1`, and has
no `-2` mate. Full evidence:
[`evidence/wasp-smoke.txt`](evidence/wasp-smoke.txt).

**Scores:** Basic 20/40 | Specialized 27/60 | Total 47/100

**Assertions:**

- PASS — The pinned live path produces retained paired alignments.
- FAIL — The candidate command does not consume both mates.
- FAIL — Its remap filename does not exist in the live release.
- PASS — The prose requires observed attrition rather than a fixed assumption.
- PASS — The output stays within research-analysis scope.

**Finding:** `CBA-003` P0.

### Input 2 — Variant A: cancer BaalChIP with copy-number correction

**Prompt:** Run the shipped HCC1395 workflow with the declared ASCAT resource
and verify every input plus the real BaalChIP 1.38.0 return contract.

**Execution:** BaalChIP runtime installation was
**RESOURCE_INFEASIBLE_BOUNDED** and the full script was not represented as
executed. The candidate parses under base R. Official source inspection proves
that it passes an in-memory data frame where a TSV filename is required, uses
incompatible sample columns, omits the required variant `ID`, names `AF`
instead of `RAF`, never consumes `cnvs`, and indexes the list returned by
`BaalChIP.report` as a data frame. The bounded contract probe reproduces the
base-R type and indexing failures:
[`evidence/baal-contract-inspection.txt`](evidence/baal-contract-inspection.txt).
Official-source details are recorded in
[`scientific-source-notes.md`](scientific-source-notes.md) and
[`evidence/baalchip-source-interface.txt`](evidence/baalchip-source-interface.txt).

The official `useRAFfromhets` path substitutes 0.5 for every variant when no
`RAF` column or gDNA correction exists. Thus `RAFcorrection=TRUE` does not make
this script copy-number-aware, despite its printed completion message.

**Scores:** Basic 9/40 | Specialized 11/60 | Total 20/100

**Assertions:**

- PASS — The R file is syntactically parseable.
- FAIL — The sample sheet violates the official constructor contract.
- FAIL — The declared ASCAT BED never reaches RAF correction.
- FAIL — The official list report is indexed as a data frame.
- PASS — Static source evidence is not misrepresented as a live package run.

**Findings:** `CBA-001` P0, `CBA-002` P0, `CBA-006` P1.

### Input 3 — Edge: imprinting and chrX filters

**Prompt:** Apply both filters to a three-row fixture, verify the retained rows,
and test the assembly and contig-name boundary.

**Execution:** bedtools 2.31.1 retained the expected two non-imprinted rows;
the chrX awk filter retained the expected two autosomal rows. Evidence:
[`evidence/interval-smoke.txt`](evidence/interval-smoke.txt).

The candidate correctly warns about build and contig compatibility, but its R
script does not enforce those checks. It also discards filtered variants rather
than preserving the excluded set and reason codes promised by `SKILL.md`.

**Scores:** Basic 30/40 | Specialized 40/60 | Total 70/100

**Assertions:**

- PASS — Imprinted-locus exclusion retains two of three rows.
- PASS — chrX exclusion retains two autosomal rows.
- FAIL — Excluded rows and reason codes are not preserved.
- FAIL — Build and chromosome-prefix mismatch is not programmatically rejected.
- PASS — The prose does not overinterpret imprinted or X-linked skew.

**Finding:** `CBA-006` P1.

### Input 4 — Variant B: public RASQUAL feature analysis

**Prompt:** Run the documented route on the public C11orf21 example and verify
the live flags, finite result, feature routing, and cohort multiplicity plan.

**Execution:** The official pinned RASQUAL commit produced one finite 25-column
row, `phi=0.520004`, and convergence status `0`. Evidence:
[`evidence/rasqual-output.tsv`](evidence/rasqual-output.tsv) and
[`evidence/rasqual-smoke.log`](evidence/rasqual-smoke.log).

The command shape is accurate for one feature. The candidate does not construct
the binary `-y/-k/-x` inputs, iterate or validate feature rows, parse the output,
or declare multiplicity control for the population-cohort use case in its
description.

**Scores:** Basic 27/40 | Specialized 38/60 | Total 65/100

**Assertions:**

- PASS — Documented flags match the pinned interface.
- PASS — The public control returns a finite populated result.
- PASS — Bias estimate and convergence are finite and successful.
- FAIL — No safe cohort feature iteration is supplied.
- FAIL — No test-family correction or parsed cohort report is defined.

**Finding:** `CBA-004` P1.

### Input 5 — Stress: AlleleSeq personalized-genome route

**Prompt:** Attempt the documented official route, inspect its Make plan, and
classify unavailable legacy dependencies without substituting an unofficial
toolchain.

**Execution:** The pinned AlleleSeq2 Makefile dry-ran, but the plan has empty
`READS_R1`, `READS_R2`, and `PREFIX` values. It plans a STAR alignment and does
not consume the separate maternal and paternal Bowtie2 SAMs described just
above it. Python 2, STAR, Picard, and the official `vcf2diploid` archive are
unavailable, so the full surface is **UNAVAILABLE_FULL_TOOLCHAIN**. Evidence:
[`evidence/alleleseq-probe.txt`](evidence/alleleseq-probe.txt),
[`evidence/alleleseq-make-dryrun.stdout`](evidence/alleleseq-make-dryrun.stdout),
and [`evidence/alleleseq-make-dryrun.stderr`](evidence/alleleseq-make-dryrun.stderr).

**Scores:** Basic 13/40 | Specialized 18/60 | Total 31/100

**Assertions:**

- FAIL — Required read and sample variables are unset.
- FAIL — The stated prerequisites omit critical legacy tools and resources.
- PASS — No unofficial vcf2diploid mirror was substituted.
- PASS — Unavailable execution is not credited as a behavioral pass.
- FAIL — The separate Bowtie2 outputs are not connected to the Make target.

**Finding:** `CBA-005` P1.

## Static scoring

| Category | Score | Max | Main reason for deduction |
|---|---:|---:|---|
| Functional suitability | 5 | 12 | Broken default WASP and BaalChIP paths; incomplete alternatives |
| Reliability | 3 | 12 | Hardcoded inputs, incompatible APIs, weak recovery and postconditions |
| Performance/context | 6 | 8 | Good disclosure; avoidable failed execution paths |
| Agent usability | 9 | 16 | Clear routing contradicted by executable contracts |
| Human usability | 5 | 8 | Discoverable but difficult to adapt safely |
| Security | 7 | 12 | No dangerous code; weak input/output-state validation |
| Maintainability | 8 | 12 | Good separation; no contract regressions |
| Agent-specific | 14 | 20 | Strong triggers; incomplete composition and idempotency |
| **Total** | **57** | **100** | |

## Ordered remediation

1. `CBA-001` P0 — repair the BaalChIP sample-sheet, het-table, and report contracts.
2. `CBA-002` P0 — implement real RAF/gDNA correction or fail closed; remove the false CN-aware claim.
3. `CBA-003` P0 — remap both WASP mates using the live release filenames.
4. `CBA-004` P1 — ship a row-safe RASQUAL cohort driver and multiplicity contract.
5. `CBA-005` P1 — complete the official AlleleSeq route or narrow it to external-only routing.
6. `CBA-006` P1 — add preflight, excluded-reason, empty-result, and idempotent-output contracts.
7. `CBA-007` P2 — add claim-level canonical provenance and exact tested versions.

## Environment and limitations

- Tooling record:
  `F:\OpenScience\audit-envs\bio-chipseq-allele-specific-binding\TOOLS.md`.
- Environment fingerprint:
  `d13dbe674c2b75121873a2636d6c453105c85b1181bf5d8bed41be9fd80c288d`.
- Rubric archive SHA-256:
  `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`.
- Accessible and rerun: WASP paired-end, WASP HDF5, RASQUAL, bedtools/awk,
  and the AlleleSeq prerequisite/Make probe.
- Static official-source only: BaalChIP API and copy-number/report contracts.
- Resource-infeasible bounded: live BaalChIP script and result probe.
- Resource not staged: `BSgenome.Hsapiens.UCSC.hg38` compact example.
- Unavailable full toolchain: AlleleSeq2 end-to-end execution.
- Whole-genome/cohort-scale performance and biological validation remain out
  of scope for this diagnostic pass.

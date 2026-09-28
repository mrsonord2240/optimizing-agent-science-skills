> **Audit record for `bio-atac-seq-allele-specific-accessibility`**
> - Audited working candidate `4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/allele-specific-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-atac-seq-allele-specific-accessibility

Generated: 2026-09-28  
Audited candidate: `4310ddfa1d9ed178f033ad42e77e0772ddadd3c4905dd1e9bcef8b6289a24103`  
Decision: **Rejected; return to fixer**

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A | 28 | 35 | 63 | 4/5 | ❌ |
| 3 | Edge | 38 | 56 | 94 | 5/5 | ✅ |
| 4 | Variant B | 37 | 56 | 93 | 5/5 | ✅ |
| 5 | Stress | 36 | 55 | 91 | 5/5 | ✅ |

**Static score:** 88/100  
**Execution average:** 87.2/100  
**Layer 1 average:** 35.4/40  
**Layer 2 average:** 51.8/60  
**Assertion pass rate:** 24/25 (96%)  
**Research veto:** FAIL — Methodological Ground  
**Numeric final:** 88/100; veto-forced grade: **Reject**

## Decisive finding

`ASA-009` is open at P0. The public helper accepts BED3 or wider, but for a
BED4 input it uses the optional name as the statistical identity. Two disjoint
one-SNP intervals both named `dup` were collapsed into one row with
`snp_count=2` and `status=significant_imbalance`. Each interval alone should
remain a one-SNP underpowered group. This can manufacture a pooled call and is
a methodological veto, not a presentation defect.

Evidence:

- `evidence/fixtures.txt`
- `runs/fixtures/duplicate-names.bed`
- `runs/fixtures/duplicate-names.tsv`
- `finding-ledger.md`

## Detailed outputs

### Input 1 — Canonical public single-sample workflow

**Prompt:** Run WASP, GATK ASEReadCounter, and phase-oriented peak aggregation
on bounded public NA12878 data; inspect identity, BAM invariants, counts, and
the peak table.

**Output:** The exact candidate retained one sample (`NA12878`) and 3,542
phased heterozygous variants, wrote a coordinate-sorted/indexed 268,176-read
BAM with one `NA12878` SM, emitted 953 GATK rows (28 at depth at least 30), and
wrote one schema-correct peak row. The unmodified PS-free public VCF failed and
cleaned its stage. The successful path used an explicitly documented bounded
PS=1 derivative only for this chromosome-wide-phased test.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

**Assertions:**

- PASS — target sample selected before genotype filtering.
- PASS — final BAM sorted, read-grouped, indexed, and non-empty.
- PASS — GATK output non-empty and scientifically inspectable.
- PASS — peak result has the ten-column phase-oriented schema.
- PASS — PS-free source rejected rather than silently pooled.

Evidence: `evidence/real-pipeline.txt`.

### Input 2 — Peak aggregation boundaries and adversarial labels

**Prompt:** Exercise opposite REF encodings, phase blocks, empty/malformed
inputs, paths with spaces, and repeated BED4 labels on distinct coordinates.

**Output:** Opposite REF labels correctly oriented to 180:20; a second phase
block remained separate and non-significant; empty and no-overlap cases wrote
the exact header; malformed ASE failed with exit 2 and no output. The fresh
duplicate-name case failed: two disjoint intervals were merged into one
significant row solely because both optional names were `dup`.

**Scores:** Basic 28/40 | Specialized 35/60 | Total 63/100

**Assertions:**

- PASS — locus-specific alleles are oriented to one haplotype.
- PASS — phase blocks and non-significant statuses remain separate.
- PASS — valid empty results retain a stable schema.
- PASS — malformed schemas fail actionably.
- **FAIL — genomic peak identity is lost when BED4 labels repeat.**

Evidence: `evidence/fixtures.txt` and
`runs/fixtures/duplicate-names.tsv`.

### Input 3 — Identity, staging, paths, and reuse

**Prompt:** Challenge target-only selection, BAM/VCF mismatch, missing PS,
staged cleanup, quoted paths, and output reuse.

**Output:** A target-homozygous/other-heterozygous two-sample VCF produced no
target records and stopped before WASP. A donor-only VCF failed identity
matching. Early and PS-free failures left no final or temporary output. Paths
with spaces completed the real workflow, and existing destinations were
refused.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100

**Assertions:** all 5 passed.

Evidence: `evidence/fixtures.txt` and `evidence/real-pipeline.txt`.

### Input 4 — Public two-feature RASQUAL

**Prompt:** Execute both public matrix rows, validate dimensions and feature
mapping, recompute BH over the complete family, and test skip/reuse boundaries.

**Output:** C11orf21 used matrix row 1 and TSPAN32 row 2. Each produced 83
association rows. All 166 raw and adjusted p-values were finite and in range;
an independent BH recomputation across the combined family matched every
adjusted p-value. Invalid dimensions, zero-feature routing, path arrays, and
output reuse behaved as documented.

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:** all 5 passed.

Evidence: `evidence/real-rasqual.txt` and
`runs/real-rasqual/association_summary.tsv`.

### Input 5 — Claims, external routes, provenance, and identity

**Prompt:** Verify exact candidate/provider identity, canonical provenance,
external-only MatrixEQTL and QuASAR routing, and conditioned scientific claims.

**Output:** Eleven candidate files reproduced the declared 1,099-byte ordinal
manifest and exact candidate hash. The clean provider checkout and three Git
blobs matched. MatrixEQTL and QuASAR are external-only, study-specific
multiplicity is required, and unsupported fixed p-value, power-fold, and
concordance claims are absent.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:** all 5 passed.

Evidence: `evidence/static.txt`.

## Required next action

Return to a fresh fixer. Preserve chromosome/start/end in the peak intersection
and group on coordinate identity plus phase set; keep BED4 name only as display
metadata, or reject duplicate names explicitly. Add the two-disjoint-peaks
regression, delta-tool the aggregate surface and full workflow, then assign a
new independent re-auditor. Candidate-ready is not granted for these bytes.

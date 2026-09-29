> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@4768d6d](https://github.com/mrsonord2240/optimized-scientific-skills/tree/4768d6d40a2ca58b8323aca739c5598b6c5782ff/skills/bio-atac-seq-allele-specific-accessibility) match audited candidate `275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-allele-specific-accessibility`**
> - Audited working candidate `275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/allele-specific-accessibility), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-atac-seq-allele-specific-accessibility

Generated: 2026-09-28  
Phase: second independent re-audit  
Exact candidate: `275ff0a1b8d9bed7a80e8316f97fe421296cb081c837ed01aaa53a0f96e48ae2`

## Decision

**Candidate-ready.** Static 96/100; execution 95.4/100; final 96/100;
Layer 1 average 38.4/40; Layer 2 average 57.0/60; assertions 25/25;
structural and research vetoes PASS; no open findings or blocked runnable
surfaces. Candidate-ready does not substitute for the orchestrator's product
commit or Marketplace intake gate.

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 57 | 96 | 5/5 | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Edge | 38 | 57 | 95 | 5/5 | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 5/5 | ✅ |
| 5 | Stress | 38 | 56 | 94 | 5/5 | ✅ |

**Execution average:** 95.4/100  
**Assertion pass rate:** 25/25 (100%)

## Input 1 — Bounded public WASP-to-GATK and coordinate-safe aggregation

**Prompt:** Run the complete single-sample allele-specific accessibility
workflow on bounded public GM12878/NA12878 data, verify mapping-bias correction,
sample identity, final BAM postconditions, non-empty allele counts,
phase-aware aggregation, and staged failure cleanup.

**Execution:** COMPLETED. The public path used ENCODE `ENCFF415FEC`, the
NA12878 1000 Genomes phased VCF, and UCSC hg38 chr1, bounded to chr1:1-5 Mb.
Because the public VCF lacks PS, a clearly labeled test derivative added
constant `PS=1`; the source PS-free input was executed separately and failed
closed. The successful run retained 3,542 phased target variants, produced a
268,176-read coordinate-sorted one-sample BAM, 953 GATK rows, 28 depth-eligible
rows, and one non-significant 28-SNP peak row.

**Evidence:** `evidence/real-pipeline.txt`; output tables under
`runs/real-pipeline/output with spaces/`.

**Scores:** Basic 39/40; Specialized 57/60; Total 96/100.

- PASS — Target sample selection precedes heterozygous filtering: only NA12878 remained.
- PASS — Final BAM is coordinate sorted, one-SM, indexed, and non-empty.
- PASS — GATK produced 953 inspectable rows, including 28 at depth at least 30.
- PASS — The aggregate output has the exact phase-oriented ten-column schema.
- PASS — PS-free source input failed with complete staged cleanup.

## Input 2 — Coordinate identity, phase orientation, schemas, and labels

**Prompt:** Aggregate phased ASE counts while proving opposite REF labels orient
to one haplotype, phase sets remain separate, duplicate display labels cannot
pool disjoint intervals, BED3/BED4 labels are display-only, exact duplicate
coordinates fail closed, and empty or malformed inputs behave contractually.

**Execution:** COMPLETED. The prior ASA-009 fixture now returns two rows named
`dup`, each `snp_count=1` and `underpowered_snp_count`, with zero significant
calls. Direct intersection inspection retained `chrAudit:99-150` and
`chrAudit:199-250`; grouping is genomic coordinates plus phase set. BED3 and
BED4 results were equal outside the display column. Exact duplicate coordinates
failed with exit 2 and no result file. Orientation, phase separation, empty,
no-overlap, and malformed-schema cases also passed.

**Evidence:** `evidence/fixtures.txt` and
`runs/fixtures/duplicate-labels.tsv`.

**Scores:** Basic 39/40; Specialized 58/60; Total 97/100.

- PASS — Opposite REF encodings yielded haplotype counts 180:20.
- PASS — A second phase set remained a separate non-significant group.
- PASS — Disjoint same-label intervals remained two underpowered one-SNP groups.
- PASS — Coordinates plus phase set define grouping; labels affect display only.
- PASS — Duplicate coordinates and malformed data fail safely; empty results keep schema.

## Input 3 — Target genotype, identity, staging, and reuse guards

**Prompt:** Exercise target-only heterozygous selection, BAM/VCF sample
mismatch, output staging, cleanup after failure, paths containing spaces, and
refusal to reuse an existing output directory.

**Execution:** COMPLETED. A target-homozygous/other-heterozygous fixture stopped
with exit 65, a BAM/VCF mismatch stopped with exit 65, and neither left staged
output. Existing output paths were refused by the pipeline and RASQUAL driver.
Paths containing spaces completed through aggregate, RASQUAL argument planning,
and the public WASP/GATK run.

**Evidence:** `evidence/fixtures.txt`, `evidence/real-pipeline.txt`, and
`evidence/real-rasqual.txt`.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

- PASS — Other-sample heterozygosity cannot admit a target-homozygous site.
- PASS — BAM/VCF identity mismatch stops before analysis.
- PASS — Failed staged runs leave no final or temporary output.
- PASS — Existing outputs are never reused or overwritten.
- PASS — Spaced paths remain argument-safe on all tested surfaces.

## Input 4 — Two-feature public RASQUAL execution and global BH correction

**Prompt:** Run the bounded RASQUAL driver on two public feature rows and verify
matrix-row ownership, finite probabilities, complete-family BH correction,
zero-feature handling, matrix dimensions, quoted paths, and reuse refusal.

**Execution:** COMPLETED. C11orf21 and TSPAN32 used matrix rows 1 and 2,
respectively. Each emitted 83 rows. All 166 raw and adjusted probabilities were
finite and bounded; an independent BH implementation matched every adjusted
value over the combined family. Wrong matrix dimensions, zero-feature rows,
spaced paths, and existing outputs behaved as documented.

**Evidence:** `evidence/real-rasqual.txt`, `evidence/fixtures.txt`, and
`runs/real-rasqual/association_summary.tsv`.

**Scores:** Basic 38/40; Specialized 57/60; Total 95/100.

- PASS — Matrix rows 1 and 2 remained assigned to the correct features.
- PASS — Both features produced 83 executable result rows.
- PASS — All raw and adjusted probabilities were finite in [0, 1].
- PASS — Global BH over all 166 tests matched independently.
- PASS — Dimension, zero-feature, path, and reuse boundaries were enforced.

## Input 5 — Inherited suite, provenance, route boundaries, and exact bytes

**Prompt:** Reinspect and execute every shipped runnable surface, rerun all
inherited tests, verify exact candidate bytes and provider blobs, confirm
MatrixEQTL and QuASAR are external-only routes, and check that phasing,
multiplicity, power, and validation claims remain scientifically bounded.

**Execution:** COMPLETED. Eleven files produced the exact 1,099-byte ordinal
manifest hash `275ff0a1…ae2`; the provider checkout was clean at `d91ed3d` and
all documented blobs resolved. All 15 shipped tests passed with ResourceWarnings
promoted to errors. MatrixEQTL and QuASAR remain routing-only. Unsupported fixed
power, p-value, and concordance claims are absent.

**Evidence:** `evidence/static.txt`, `evidence/fixtures.txt`,
`candidate-manifest.json`, and `scientific-source-notes.md`.

**Scores:** Basic 38/40; Specialized 56/60; Total 94/100.

- PASS — Exact content identity independently matched.
- PASS — All 15 deterministic regressions passed without ResourceWarnings.
- PASS — Provider commit and canonical source blobs independently matched.
- PASS — MatrixEQTL and QuASAR remain explicit external-only routes.
- PASS — Phasing, multiplicity, power, validation, and concordance claims are bounded.

## Veto adjudication

- Structural T1 Stability: PASS.
- Structural T2 Contract: PASS.
- Structural T3 Determinism: PASS.
- Structural T4 Security: PASS.
- Research M1 Scientific Integrity: PASS.
- Research M2 Practice Boundaries: PASS.
- Research M3 Methodological Ground: PASS. ASA-009 is closed by independent exact-fixture and direct-coordinate evidence.
- Research M4 Code Usability: PASS. Every accessible shipped surface executed with inspected passing output.

## Finding disposition

ASA-001 through ASA-009 are closed. No new finding, deferred runnable surface,
restricted-access item, or tooling blocker remains. See `finding-ledger.md` for
the ordered evidence mapping.

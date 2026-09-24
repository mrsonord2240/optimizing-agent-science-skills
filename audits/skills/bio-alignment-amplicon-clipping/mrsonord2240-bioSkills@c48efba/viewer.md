> **Audit record for `bio-alignment-amplicon-clipping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c48efba](https://github.com/mrsonord2240/bioSkills/tree/c48efba95387158281f21abe97ecb48b8407ac44/alignment-files/alignment-amplicon-clipping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-24 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-amplicon-clipping

Generated: 2026-09-24  
Source: `mrsonord2240/bioSkills@c48efba95387158281f21abe97ecb48b8407ac44:alignment-files/alignment-amplicon-clipping`  
Final pass note: final pass: fixed and audited under one brief, see CHECKPOINT.md

## Result

**95/100 — ⭐ Production Ready — deployable.** 7/7 inputs executed; 28/28 assertions passed; all veto gates pass; no open recommendations.

| Input | Type | Basic | Specialized | Total | Assertions |
|---|---:|---:|---:|---:|---:|
| 1 | Canonical regression | 38/40 | 58/60 | 96/100 | 4/4 |
| 2 | Variant regression | 38/40 | 57/60 | 95/100 | 4/4 |
| 3 | Edge regression | 37/40 | 57/60 | 94/100 | 4/4 |
| 4 | Tool regression | 38/40 | 56/60 | 94/100 | 4/4 |
| 5 | Adversarial regression | 38/40 | 57/60 | 95/100 | 4/4 |
| 6 | Fresh stress input | 38/40 | 58/60 | 96/100 | 4/4 |
| 7 | Fresh adversarial input | 38/40 | 57/60 | 95/100 | 4/4 |

## Executed evidence

### Input 1 — Real ARTIC v5.3.2 nanopore BAM: workflow, mode table, and iVar alternative

The documented workflow and shipped example completed on 4,916 real reads; MD was restored on every mapped read and residual primer counts were 0/0.

Execution: samtools 1.24, pysam 0.24.1, and iVar 1.4.4 in WSL alignment-files.

- [PASS] The documented workflow block completes with MD on all 4,916 mapped reads. — `final_s1_real_artic.log`
- [PASS] Both-ends plus strand leaves 0/0 5-prime/3-prime primer residuals. — `final_s1_real_artic.log`
- [PASS] The four documented mode outcomes reproduce on ARTIC data. — `final_s1b_modes_ivar.log`
- [PASS] The shipped example is deterministic at THREADS 4, 1, and 4. — `same record MD5 38df635d7d5b; final_s1c_example_real.log`

### Input 2 — Synthetic 800-read paired-end panel with planted primer SNPs

All repaired modes matched planted boundaries; primer-derived allele counts were removed and mate/tag repairs held.

Execution: Deterministic synthetic input regenerated with the archived generator.

- [PASS] All 800 reads match planted clipping truth in every exercised mode. — `final_s2_synth.log`
- [PASS] MD/NM, TLEN, MC, and ms repairs match independent checks. — `final_s2_synth.log`
- [PASS] Primer SNP allele counts change from mixed to the true biological alleles. — `final_s2_synth.log`
- [PASS] The short-read strand-only 3-prime residual outcome reproduces. — `final_s2_synth.log`

### Input 3 — BED syntax and tolerance semantics, including new CRLF normalization

All 16 mode-table cells match samtools. Tab, spaces, track/browser headers, comments, blanks, and CRLF BED forms now complete; malformed 5-column BED fails clearly.

Execution: Synthetic single-read and paired-end cases run through the shipped example copy.

- [PASS] All 16 documented strand/both-end CIGAR outcomes match. — `final_s3_strand_bed.log`
- [PASS] Every documented accepted BED form, including CRLF, succeeds end to end. — `final_s3_strand_bed.log`
- [PASS] A 5-column BED with --strand fails before clipping with an actionable BED message. — `final_s3_strand_bed.log`
- [PASS] Tolerance behavior agrees with the documented upstream-extension wording. — `final_s3_strand_bed.log`

### Input 4 — Hard clipping, iVar, consensus, MD/BAQ, and related command pointers

Hard/soft clipping and iVar reproduce planted truth. The residual BAQ wording is gone; bcftools output is unchanged by MD presence.

Execution: Synthetic panel plus ARTIC BAM; fgbio help used only to verify the non-primer-trimmer note.

- [PASS] Hard clipping matches truth for 800/800 reads and uses H CIGAR operations. — `final_s4_tools.log`
- [PASS] Soft clipping and iVar -q 0 -m 1 match the planted truth. — `final_s4_tools.log`
- [PASS] The related mpileup commands have the documented accepted/rejected flags. — `final_s4_tools.log`
- [PASS] bcftools BAQ output has equal MD5 with and without MD tags. — `32,150 records per comparison; final_s4_tools.log`

### Input 5 — Contig/reference mismatch, sparse input, and failed-output probes

Mismatch, wrong reference, missing index, sparse input, and threshold violations fail loudly and publish no output BAM; legitimate multi-contig cases pass.

Execution: Real ARTIC/Illumina inputs plus synthetic sparse BAM run from a copied skill.

- [PASS] Contig and reference mismatches stop without an output BAM. — `final_s5_adversarial.log`
- [PASS] A late calmd failure also leaves no final BAM. — `final_s5_adversarial.log`
- [PASS] Multi-contig headers and extra BED contigs remain valid inputs. — `final_s5_adversarial.log`
- [PASS] Sparse/shotgun-like inputs fail with the documented high-NOT-CLIPPED or no-overlap explanations. — `final_s5_adversarial.log`

### Input 6 — Synthetic 900-read HiFi-like full-length 16S amplicons

The workflow and example clip exact boundaries across orientations, while mode tests reproduce the expected 98.1% 3-prime residual when both ends are not clipped.

Execution: Fresh deterministic synthetic HiFi-like data, aligned with minimap2 map-hifi.

- [PASS] Workflow output has MD on 900/900 mapped reads and 0/0 residuals. — `final_s6_hifi.log`
- [PASS] Both-ends plus strand and the shipped example match all 900 planted boundaries. — `final_s6_hifi.log`
- [PASS] Default/strand versus both-end residual percentages reproduce. — `final_s6_hifi.log`
- [PASS] iVar and hard-clip operations complete on the fresh HiFi-like input. — `final_s6_hifi.log`

### Input 7 — Residual checker contract and wrong-scheme primer BEDs

The checker passes all 20 boundary/error expectations. The example rejects three wrong-scheme/shifted BEDs by NOT CLIPPED share and emits no output.

Execution: Real ARTIC data plus planted unit cases and three wrong-scheme probes.

- [PASS] The residual checker passes all 20 boundary, strand, and bad-input expectations. — `final_s7_run.log`
- [PASS] Bad checker inputs return exit 2, separate from residual exit 1. — `final_s7_run.log`
- [PASS] Real unclipped and planted-residual BAMs are detected while clipped output is clean. — `final_s7_run.log`
- [PASS] v3, shifted-v5, and strand-only wrong schemes fail; matching v5 succeeds. — `final_s7b_wrong_scheme.log`

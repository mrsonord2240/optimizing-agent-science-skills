> **Audit record for `bio-clip-seq-ago-clip-mirna-targets`**
> - Audited working candidate `e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clip-seq/ago-clip-mirna-targets), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — AGO-CLIP and miRNA Target Identification

Generated: 2026-09-28

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 5 | Stress | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 6 | Scope Boundary | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 7 | Adversarial | 38 | 56 | 94 | 5/5 PASS | ✅ |

**Execution Average:** 96.6 / 100
**Assertion Pass Rate:** 35/35 (100.0%)
**Research veto:** PASS
**Final score:** 95 / 100 — ⭐ Production Ready
**Candidate identity:** `sha256-manifest-v1 e5366d51226e2ad2c96030cb26581bc84808194b7a17ef7bb376d337280d1b30` (10 files; 989-byte manifest).

## Detailed Outputs

### Input 1 — Canonical: Fresh pinned Hyb cross-workflow repeatability

**Outcome:** Pinned Hyb commit 028ab6371ce793ca5e86f475fce1f2cc6ad3c677 ran twice from fresh output roots. Each workflow produced 111 accepted rows, 0 exclusions, 111 targets, and 2/2 support. Structured outputs and non-stdout files are identical; only stdout's first timestamp line varies.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Two fresh workflows produce identical structured sites, targets, support, exclusions, and manifests — All structured artifact hashes match across independent workflow roots.
- [PASS] Each underlying Hyb run has the advertised row schema and 111 assignments — Four raw replicate files each contain 111 rows with 16 fields.
- [PASS] Each retained read has support from every replicate — All 111 retained support rows show 2/2 and supporting indices 1,2.
- [PASS] Workflow manifests reconcile assignment and target counts — Both manifests report 111 accepted, 0 excluded, 2 replicates, and 111 target rows.
- [PASS] Timestamped stdout differences are bounded and disclosed — Only the first timestamp line differs; remaining stdout and all non-stdout files match.

### Input 2 — Variant A: Wrapper failure and publication boundaries

**Outcome:** All seven shipped tests passed. Wrapper checks preserved existing output on failure, propagated subprocess errors, respected paths with spaces and literal wildcard characters, and removed failed stages.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Paths with spaces and literal wildcard characters are handled literally — The shipped wrapper regression completed its spaced and wildcard-path fixture.
- [PASS] An existing output is protected without explicit replacement — The repeat invocation returns status 73 and preserves the existing result.
- [PASS] A failing Hyb exit status reaches the caller — The controlled status 42 is propagated.
- [PASS] A failed replacement preserves prior output — The sentinel is unchanged after the forced replacement failure.
- [PASS] A failed staged run cleans its temporary stage — The harness found no residual stage directory.

### Input 3 — Edge: Consensus schema, orientation, and finite expression parsing

**Outcome:** The 16-case parser harness and 27-case expanded spelling harness passed. Finite +1.5e2/5e1 values at threshold 1e2 accepted only the above-threshold row and reason-coded the other. Thirteen Python float() spellings covering signed and case variants of NaN, Inf, and Infinity failed as both expression values and thresholds; malformed/blank/missing values also failed before result files were published.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Both segment orientations normalize to the same miRNA-target contract — Fresh orientation fixtures preserve correct IDs and coordinate fields.
- [PASS] Finite values above threshold are accepted and below-threshold values are excluded with a reason — The 150-valued row is accepted; the 50-valued row receives below_expression_threshold at threshold 100.
- [PASS] All accepted NaN and infinity spellings fail before output publication — Thirteen float() spellings, including signed/case variants of NaN, Inf, and Infinity, were rejected as expression values and thresholds with no result files.
- [PASS] Malformed, blank, and missing expression values fail closed — Nonnumeric, blank, and short-row values failed with source-line diagnostics and no result files.
- [PASS] Non-finite thresholds fail before output publication — NaN, +Inf, -Inf, Infinity, and -Infinity thresholds were rejected; no result files appeared.

### Input 4 — Variant B: TargetScan spliced-coordinate and strand projection

**Outcome:** Fresh exon-spanning plus/minus conversions and bedtools -split -s overlap passed; wrong-strand overlap was excluded. Release mismatch and out-of-range fixtures failed closed, and the manifest retained assembly and release fields.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Plus- and minus-strand sites project to multi-block BED12 — Both UTR-relative fixtures produce two blocks with their original strands.
- [PASS] Split, strand-aware overlap excludes the opposite-strand peak — Expected plus and minus overlaps remain; the wrong-strand peak is absent.
- [PASS] TargetScan release mismatch is rejected — The version mismatch returns nonzero with a release-metadata diagnostic.
- [PASS] Out-of-range UTR sites fail closed — The converter rejects the site rather than truncating it.
- [PASS] Manifest retains assembly and annotation provenance — Output records GRCh38, GENCODEv49, and TargetScan 8.0.

### Input 5 — Stress: Targeted miR-eCLIP UMI declaration and fail-closed behavior

**Outcome:** Eight direct assertions passed: protocol-declared 9- and 10-nt extraction succeeded; absent, zero, non-integer, blank-library, blank-protocol, and too-short R2 cases failed closed. The upstream targeted-route 9-nt prose versus 10-nt default remains explicitly disclosed.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] A declared 9-nt UMI extracts exactly nine R2-prefix bases — The emitted header contains ACGTACGTA and the manifest records length 9.
- [PASS] A declared 10-nt UMI extracts exactly ten R2-prefix bases — The emitted header contains ACGTACGTAC and the manifest records length 10.
- [PASS] Successful output binds length to library and protocol provenance — Both manifests include library ID, protocol source, and input/output hashes.
- [PASS] Missing, zero, non-integer, or blank declarations fail without outputs — All five declaration errors return nonzero and leave FASTQ/manifest absent.
- [PASS] R2 shorter than the declared length fails without outputs — A 13-nt declaration against 12-nt R2 returns nonzero and publishes nothing.

### Input 6 — Scope Boundary: Unavailable biological and remote surfaces

**Outcome:** Static and route inspection preserved direct-versus-inferred evidence labels, species/model limits, and explicit unavailable states for full Yeo, HEAP wet-lab, and the failed DIANA endpoint. Bounded synthetic results are not presented as biological validation.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Direct chimera evidence remains distinct from computational predictions — Method guidance labels ordinary AGO-CLIP assignments as inferred and chimera pairs as direct.
- [PASS] Human and mouse HEAP contexts are not conflated — HEAP is kept within its Halo-Ago2 mouse model context.
- [PASS] Unrun full workflows require their real biological inputs — Full Yeo and HEAP surfaces are recorded as unavailable without matched biological materials and references.
- [PASS] Unavailable DIANA service is reported rather than simulated as a result — The HTTP 500 surface remains an explicit service availability limitation.
- [PASS] Synthetic evidence is not represented as biological validation — No wet-lab or clinical conclusion is claimed by the bounded synthetic fixtures.

### Input 7 — Adversarial: Secondary UMI, trimming, and soft-clip diagnostic boundaries

**Outcome:** Fresh bounded route fixtures verified ten-base read-1 UMI extraction, adapter trimming to 20-nt inserts, and one soft-clipped record. The diagnostic remains diagnostic-only; complete biological pipelines remain input-deferred.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] The total-Yeo route extracts its documented ten-base read-1 UMI — The fixture header contains the expected 10-nt suffix.
- [PASS] Paired adapter trimming retains the expected insert lengths — Both trimmed reads are 20 nt after adapter removal.
- [PASS] The soft-clip diagnostic counts clipped records — One 5M5S record is counted and the 10M control is not.
- [PASS] A soft-clip count is not represented as a chimera call — Documentation describes it as a candidate-pool diagnostic only.
- [PASS] Synthetic checks remain distinguished from unavailable full biological workflows — Full Yeo and wet-lab paths remain deferred with the required inputs recorded.

## Prior Finding Reconciliation

- **AGO-004 (P0):** Rechecked with two new pinned Hyb workflows. Structured outputs and all non-stdout files match; stdout differs only in its first timestamp line.
- **AGO-005 (P1):** Rechecked explicit targeted UMI lengths and invalid declarations. The upstream 9-nt prose versus 10-nt executable default remains disclosed; the local extractor requires protocol declaration.
- **AGO-009 (P0):** Rechecked finite acceptance, below-threshold exclusion, NaN/infinity spellings, malformed/missing values, non-finite thresholds, and absent result files after invalid inputs. All checks pass.

## Deferred Surfaces

Full Yeo and HEAP biological runs remain input-deferred; the DIANA example endpoint returned HTTP 500. These surfaces were not claimed as executed. See `evidence/deferred-limitations.md` and `TOOLS.md`.

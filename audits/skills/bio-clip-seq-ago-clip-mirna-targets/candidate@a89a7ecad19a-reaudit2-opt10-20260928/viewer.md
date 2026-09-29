> **Audit record for `bio-clip-seq-ago-clip-mirna-targets`**
> - Audited working candidate `a89a7ecad19a3cc207ab6b82bc0910b126b663e32e7c74c3c2b74dc105d780fa`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clip-seq/ago-clip-mirna-targets), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clip-seq-ago-clip-mirna-targets

Generated: 2026-09-28

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 2 | Variant A | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 4 | Variant B | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 5 | Stress | 39 | 58 | 97 | 5/5 PASS | ✅ |
| 6 | Edge | 26 | 38 | 64 | 3/5 PASS | ⚠️ |
| 7 | Stress | 38 | 56 | 94 | 5/5 PASS | ✅ |

**Execution Average:** 91.9 / 100
**Assertion Pass Rate:** 33/35 (94.3%)

## Detailed Outputs

### Input 1 — Canonical

**Label:** Pinned Hyb workflow-level repeatability
**Status:** COMPLETED — Two independent complete two-replicate workflows on official Hyb test reads each retained 111 assignments; raw and structured results matched across workflows.
**Observed output:** Pair A and Pair B each produced four total underlying single-thread Hyb runs across the two workflows: each raw file had 111 rows and 16 fields. Both manifests reported 111 accepted, 0 excluded, and two replicates. The five structured files and all non-stdout files were byte-identical; each stdout log differed only in its first wall-clock timestamp line. All 111 support rows recorded 2/2 runs, indices 1,2, accepted=true.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Both fresh workflow pairs produce identical sites, targets, support, exclusions, and manifest bytes — All five structured output SHA-256 values matched across the two separately published workflows.
- [PASS] Every raw Hyb run contains 111 rows with the expected 16-field schema — Four raw outputs were inspected; all had 111 rows and only 16-field rows.
- [PASS] Every accepted read has identical assignment support in both replicates — All 111 support records show two of two runs, supporting indices 1,2, and accepted=true.
- [PASS] Manifest counts reconcile with emitted sites and targets — Each manifest reports 111 accepted, 0 excluded, two replicates, and 111 target rows.
- [PASS] The reproducibility comparison accounts for timestamped stdout — Stdout is intentionally not byte-identical: only its first wall-clock timestamp line differs; subsequent lines match.

### Input 2 — Variant A

**Label:** Wrapper path, failure, and publication boundaries
**Status:** COMPLETED — The independent wrapper harness passed literal-path handling, overwrite refusal, error propagation, replacement preservation, and stage cleanup.
**Observed output:** The wrapper completed with a path containing spaces and a literal wildcard; refused an existing output with status 73; propagated a controlled Hyb status 42; preserved the old sentinel on failed replacement; and left no stage residue.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Paths containing spaces and literal wildcard characters remain literal — The wrapper completed with the spaced and literal-star input/tool/output paths.
- [PASS] Existing results are protected without an explicit replace option — The second run returned 73 and preserved the completed result.
- [PASS] A failing Hyb status is propagated to the caller — The controlled subprocess status 42 was returned.
- [PASS] A failed replacement preserves the prior final output — The sentinel remained unchanged after the failed replacement attempt.
- [PASS] Failed runs clean the staging directory — No matching temporary stage directory remained.

### Input 3 — Edge

**Label:** Consensus parser orientation and input contracts
**Status:** COMPLETED — Synthetic parser fixtures and strict failure controls passed; the separately tested NaN expression case is reported in Input 6.
**Observed output:** The parser preserved both 16-column orientations, expression provenance, structured aggregation and distinct missing/unstable reason codes. Malformed Hyb rows and a malformed expression header failed closed. The 9 independent control assertions passed.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] Both segment orientations normalize to the correct miRNA and target fields — Mirna-first and target-first fixtures produced the expected normalized fields.
- [PASS] Expression values, units, and source are retained in accepted rows — The 150 TPM fixture and matched-small-RNA source were preserved.
- [PASS] Missing and discordant replicate assignments receive distinct reasons — The parser emitted missing_from_replicate and unstable_assignment separately.
- [PASS] Malformed Hyb field count fails before valid output publication — A three-field row failed with an expected-16 diagnostic.
- [PASS] Malformed expression header fails closed — The reduced header was rejected before a result was emitted.

### Input 4 — Variant B

**Label:** TargetScan spliced-coordinate projection
**Status:** COMPLETED — Plus/minus exon-spanning fixtures projected to BED12, and strand-aware overlap and release/range guards behaved as documented.
**Observed output:** The plus-strand site projected to chr1:107-204 as two BED12 blocks; the minus-strand site projected to chr2:306-403 as two blocks. bedtools intersect -split -s retained the two matching-strand peaks. Release mismatch and out-of-range cases failed closed.
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] UTR-relative plus and minus sites project to multi-block BED12 — Both one-based inclusive spliced sites became two-block genomic BED12 rows.
- [PASS] Strand-aware block overlap excludes the opposite-strand peak — The plus-good and minus-good peaks overlapped; plus-wrong-strand did not.
- [PASS] A TargetScan release mismatch is rejected — The converter returned nonzero with a release-metadata diagnostic.
- [PASS] A site outside its mapped UTR fails closed — The converter returned nonzero rather than truncating the input site.
- [PASS] Output manifest preserves assembly and annotation release — Manifest identifies GRCh38, GENCODEv49, and TargetScan 8.0.

### Input 5 — Stress

**Label:** Targeted-Yeo protocol-declared UMI contract
**Status:** COMPLETED — Independent synthetic FASTQ fixtures confirmed explicit 9- and 10-nt extraction and rejected omitted, invalid, blank, and too-long declarations without outputs.
**Observed output:** The local targeted extractor emitted exactly the declared 9-nt and 10-nt R2 prefixes and bound each to library/protocol metadata and input/output hashes. Missing length, zero, non-integer, blank library, blank protocol, and too-short R2 each failed closed with no output files (8/8 assertions).
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100
**Assertions:**
- [PASS] A declared 9-nt UMI extracts exactly nine R2-prefix bases — The result header contained ACGTACGTA.
- [PASS] A declared 10-nt UMI extracts exactly ten R2-prefix bases — The result header contained ACGTACGTAC.
- [PASS] The manifest binds the explicit length to library and protocol provenance — Both success manifests recorded length, library id, protocol source, and hashes.
- [PASS] An omitted or invalid UMI declaration is rejected without outputs — Missing, zero, non-integer, blank-library, and blank-protocol cases returned nonzero and left no outputs.
- [PASS] R2 shorter than the declared UMI fails closed — The 13-nt request against a 12-nt R2 failed without output files.

### Input 6 — Edge

**Label:** Non-finite matched-expression threshold input
**Status:** COMPLETED — A bounded parser fixture with expression_value=NaN and threshold 100 returned a complete result and accepted the read, bypassing the expression gate.
**Observed output:** With two identical valid Hyb rows and expression_value=NaN at a required threshold of 100, the command exited 0, accepted one consensus row, and published expression_value=nan in sites.tsv. Python float accepts NaN, and the current comparison `nan < 100` is false.
**Scores:** Basic 26/40 | Specialized 38/60 | Total 64/100
**Assertions:**
- [FAIL] The parser rejects non-finite expression measurements — A NaN expression value was accepted and published.
- [FAIL] A value that cannot satisfy a threshold of 100 is not accepted — The NaN row passed the 100 threshold and appeared in accepted sites.
- [PASS] The result retains the supplied expression provenance — The emitted row retained the value, TPM unit, and matched-small-RNA source.
- [PASS] The manifest and structured outputs reconcile for the observed behavior — The complete manifest reported one accepted row, matching sites.tsv.
- [PASS] The fixture remains within the documented computational-assignment scope — The test uses only bounded synthetic Hyb and expression inputs.

### Input 7 — Stress

**Label:** Total-Yeo UMI, paired trimming, and soft-clip diagnostic
**Status:** COMPLETED — Bounded synthetic tests confirmed the documented ten-base read-1 UMI route, paired adapter trimming, and a diagnostic-only soft-clip count.
**Observed output:** UMI-tools appended the ten-base read-1 prefix, cutadapt removed the fixture adapters while retaining 20-nt paired reads, and the samtools/awk diagnostic counted one 5M5S record while excluding a 10M control. These are synthetic route checks, not a full biological Yeo workflow or peak caller.
**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:**
- [PASS] The total-Yeo route extracts the documented ten-base read-1 UMI — UMI-tools added the expected 10-nt prefix to the read identifier.
- [PASS] Paired adapter trimming retains the expected fixture inserts — Both trimmed reads had length 20 after adapter removal.
- [PASS] The soft-clip diagnostic counts clipped alignments correctly — One 5M5S record was counted and the 10M record was not.
- [PASS] The diagnostic is not described as a chimera call — Candidate documentation labels it as a candidate-pool diagnostic only.
- [PASS] Synthetic checks remain distinguished from unavailable biological workflows — The full Yeo and wet-lab HEAP paths remain explicitly deferred.

## Veto and Readiness

- Skill veto: PASS (stability, contract, determinism, and security PASS).
- Research veto: FAIL on methodological ground because NaN expression values bypass the required threshold.
- Numeric final score: 92/100 after schema rounding; veto override forces grade Reject and deployable=false.
- Open finding: AGO-009 P0. AGO-004 and AGO-005 are closed on this exact candidate identity.

## Unexecuted and Deferred Surfaces

- Full Yeo chimeric-eCLIP requires real biological reads and species-matched repeat/genome STAR indices.
- HEAP reproduction requires Halo-Ago2 experimental material and wet-lab execution.
- The documented DIANA microT-CDS example endpoint was previously unavailable (HTTP 500); no service recovery was assumed.
- AGO peak calling is not bundled; the soft-clip count is only a diagnostic, as the Skill states.

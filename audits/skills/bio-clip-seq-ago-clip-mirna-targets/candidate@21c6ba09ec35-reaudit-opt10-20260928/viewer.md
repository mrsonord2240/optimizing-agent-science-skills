> **Audit record for `bio-clip-seq-ago-clip-mirna-targets`**
> - Audited working candidate `21c6ba09ec3580896c35adbe5175ac2e7bf161870e912e46d2bbca42190cfebc`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clip-seq/ago-clip-mirna-targets), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clip-seq-ago-clip-mirna-targets

Generated: 2026-09-28

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 26 | 42 | 68 | 4/5 | ❌ PARTIAL |
| 2 | Variant A | 40 | 58 | 98 | 5/5 | ✅ COMPLETED |
| 3 | Edge | 40 | 58 | 98 | 5/5 | ✅ COMPLETED |
| 4 | Variant B | 39 | 58 | 97 | 5/5 | ✅ COMPLETED |
| 5 | Stress | 30 | 39 | 69 | 4/5 | ⚠️ PARTIAL |

**Execution Average:** 86.0 / 100  
**Assertion Pass Rate:** 23/25  
**Static Score:** 88 / 100  
**Weighted Score:** 87 / 100  
**Final Grade:** ❌ Reject — determinism and methodological vetoes override the numeric score.

## Veto disposition

- Skill veto: **FAIL** on determinism. Separate complete two-run workflows return different direct-target lists.
- Research veto: **FAIL** on methodological ground. Two-run agreement is not enough to call an assignment stable under the observed stochasticity, and the targeted-Yeo UMI length remains internally inconsistent.
- Stability, structural contract, security, scientific integrity, practice boundaries, and code usability pass.

## Detailed Outputs

### Input 1 — Canonical: Current Hyb official-data route and workflow-level repeatability

**Status:** ❌ PARTIAL  
**Output summary:** The repaired wrapper executes current pinned Hyb and publishes complete structured outputs, but two independent two-run batches retained nonidentical direct-target sets despite equal 94/17 aggregate counts.  
**Scores:** Basic 26/40 | Specialized 42/60 | Total 68/100

**Assertions:**

- [PASS] The wrapper executes pinned Hyb 028ab63 on its official public input through the current named-database interface — Four fresh single-thread Hyb runs across two wrapper batches each emitted 111 non-empty 16-column rows.
- [PASS] The wrapper publishes complete structured outputs and reason-coded exclusions — Each batch atomically published sites, targets, exclusions, manifest, raw outputs, and logs; counts reconciled to 111.
- [PASS] The orientation-aware parser retains only assignments identical within each configured batch — Each two-run batch retained 94 assignments and excluded 17 as unstable_assignment.
- [FAIL] Repeating the complete two-run workflow on identical pinned inputs produces the same direct-target list — Pair A and Pair B had seven accepted-only ids on each side and four changed assignments among shared ids; sites and target hashes differed.
- [PASS] Raw Hyb and output identities are recorded for independent review — Both manifests retain commit, database, input hash, per-run hashes, output hashes, counts, and policy.

### Input 2 — Variant A: Strict failure, path, overwrite, and atomic-publication boundaries

**Status:** ✅ COMPLETED  
**Output summary:** Quoted space and literal-glob paths, exit-status propagation, overwrite refusal, failed-replacement preservation, and staging cleanup all passed independent controls.  
**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- [PASS] Paths containing spaces and literal glob characters remain literal — The wrapper completed with a spaced/literal-star FASTQ and spaced tool/output paths.
- [PASS] An existing final output is not overwritten without explicit replacement — The rerun returned exit 73 and preserved the completed manifest.
- [PASS] A Hyb subprocess status of 42 is propagated — The replacement attempt returned 42 and surfaced the controlled error.
- [PASS] A failed replacement preserves the prior output — The sentinel in the prior final directory remained intact.
- [PASS] A failed run leaves neither a partial final result nor staging residue — No matching stage directory remained after failure.

### Input 3 — Edge: 16-column orientation, expression provenance, schema, and ambiguity controls

**Status:** ✅ COMPLETED  
**Output summary:** Independent fixtures verified fields 4/10 in either orientation, exact expression provenance, structured aggregation, reason codes, and fail-closed schema behavior.  
**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- [PASS] The parser recognizes one microRNA and one mRNA in either fields-4/10 orientation — Both mirna-first and target-first fixture rows were retained with the correct orientation.
- [PASS] Expression values, units, and source provenance are preserved — The accepted rows retained 150 TPM and matched-small-rna source.
- [PASS] Missing and differing cross-run assignments receive distinct reason codes — missing_from_replicate and unstable_assignment were emitted as expected.
- [PASS] Malformed Hyb field counts fail closed — A three-field row returned nonzero with an expected-16 diagnostic.
- [PASS] Malformed expression schemas fail closed — The parser rejected a reduced header before producing results.

### Input 4 — Variant B: TargetScan spliced-coordinate projection and strand-safe overlap

**Status:** ✅ COMPLETED  
**Output summary:** Plus- and minus-strand exon-spanning sites projected to versioned BED12, -split -s excluded the opposite strand, and release/range errors failed closed.  
**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- [PASS] TargetScan UTR-relative input is not treated as genomic BED — The converter requires a version-matched spliced UTR map and emits the coordinate contract in its manifest.
- [PASS] Plus- and minus-strand exon-spanning sites project correctly — Both fixtures produced two-block BED12 rows with the expected strands.
- [PASS] The overlap command is block- and strand-aware — bedtools intersect -split -s retained the two matching-strand peaks and excluded the opposite-strand peak.
- [PASS] Release mismatch is rejected — A 7.2 command against an 8.0 map returned nonzero with a release diagnostic.
- [PASS] Sites outside the mapped UTR fail closed — The out-of-range fixture returned nonzero instead of truncating the site.

### Input 5 — Stress: Library-layout and external-surface claim boundaries

**Status:** ⚠️ PARTIAL  
**Output summary:** Tool and evidence boundaries are substantially corrected, but the candidate still states that the pinned targeted-Yeo route takes a 9-nt R2 UMI while the live executable defaults to 10 and its CWL does not override it.  
**Scores:** Basic 30/40 | Specialized 39/60 | Total 69/100

**Assertions:**

- [PASS] Total and targeted Yeo library layouts are kept distinct — The candidate routes them separately and warns against transferring a generic paired pattern.
- [FAIL] The targeted-Yeo UMI length stated by the candidate matches the pinned executable contract — Pinned CWL prose says 9 nt, targeted_miR_umi.py defaults to 10, the CWL supplies no umi_length, and the live default appended ten R2 bases.
- [PASS] Hyb, Yeo CWL, HEAP, hybkit, and prediction services are not represented as interchangeable tools — The skill now distinguishes each interface and access state.
- [PASS] Counts and absent overlaps are interpreted within assay context — Counts are recovery support rather than affinity, and absent AGO overlap is not represented as biological disproof.
- [PASS] Unavailable full Yeo, HEAP wet lab, and DIANA execution are not credited as completed — They remain respectively resource-infeasible, biological-route unavailable, and remote unavailable.

## Open findings

- **AGO-004 / P0:** complete two-run consensus batches are not reproducible at the accepted direct-target level.
- **AGO-005 / P1:** the pinned targeted-Yeo CWL prose says 9 nt, while the executable default and live behavior are 10 nt and the CWL supplies no override.

All other initial findings (AGO-001, AGO-002, AGO-003, AGO-006, AGO-007, AGO-008) are closed by independently executed evidence.

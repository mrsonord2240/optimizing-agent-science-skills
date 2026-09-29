> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@0295158](https://github.com/mrsonord2240/optimized-scientific-skills/tree/029515880c51d55682816327441d7bab373fc175/skills/bio-cfdna-preprocessing) match audited candidate `148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-cfdna-preprocessing`**
> - Audited working candidate `148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/liquid-biopsy/cfdna-preprocessing), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-cfdna-preprocessing

Generated: 2026-09-28  
Auditor: fresh independent `reaudit-scientific-skill` worker; did not perform the initial audit or fix  
Exact candidate: `sha256-manifest-v1:148b254a310719e781dacc9a782cd45f61e6cc8dd508124e1941d589458b47e1`

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|:---:|
| 1 | Canonical — public insert-size QC | 38 | 57 | 95 | 5/5 | ✅ |
| 2 | Variant A — simplex UMI consensus | 39 | 58 | 97 | 5/5 | ✅ |
| 3 | Variant B — reciprocal duplex consensus | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Edge — QC flags, bounds, empty BAM | 38 | 58 | 96 | 5/5 | ✅ |
| 5 | Stress — metacharacter paths and ten-call stability | 39 | 57 | 96 | 5/5 | ✅ |

**Execution average:** 96.2/100  
**Assertion pass rate:** 25/25 (100%)  
**Static score:** 96/100  
**Final score:** 96/100 — ⭐ Production Ready  
**Readiness decision:** candidate-ready; both veto gates pass and no finding remains open.

## Detailed outputs

### Input 1 — Canonical: public cfDNA insert-size QC

**Prompt:** Summarize the insert-size distribution of the prepared public paired-end human BAM, including count, mode, median, 90–150 bp fraction, fraction above 250 bp, exclusions, and interpretation context.

**Observed output:** Two calls returned identical results: `n=2819`, mode `96`, median `123`, 90–150 fraction `0.64349059950337`, and >250 fraction `0.0`. The result also reports 5,644 input records, 2 unmapped, 4 improper, 2 secondary, 0 supplementary, 0 duplicate, 0 QC-fail, 2,824 nonpositive template lengths, and the three required interpretation-context labels. A fresh `max_size=150` case accepted 2,190 records and reported 630 over-bound records.

**Scores:** Basic 38/40 | Specialized 57/60 | Total 95/100

- PASS — All required numerical fields are present and independently reproducible.
- PASS — The selected population matches the primary/proper-pair/PF/nonduplicate contract.
- PASS — Repeated execution is deterministic.
- PASS — The fresh alternate bound changes the selected population coherently.
- PASS — The output states assay context rather than making a clinical conclusion.

### Input 2 — Variant A: simplex UMI consensus

**Prompt:** Run the wrapper on paired inline-UMI data with `6M11S+T`, inspect every stage, and produce a filtered indexed simplex BAM.

**Observed output:** All 32 extracted reads carry RX, ZA, and ZB. The query-grouped uBAM is streamed through `samtools fastq -T RX,ZA,ZB`, `bwa mem -C -p`, and `ZipperBams`; all 32 first-zipped records retain all tags. Adjacency grouping assigns MI to all 32 records. Molecular consensus emits 4 records. The mapped consensus is queryname-sorted before filtering, and the final BAM contains 4 coordinate-sorted records, has an index, and passes `samtools quickcheck`.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

- PASS — Per-segment and combined UMI tags are present.
- PASS — FASTQ/BWA/Zipper topology is live and correctly connected.
- PASS — Simplex uses adjacency grouping and molecular consensus.
- PASS — Filtering receives queryname-sorted templates.
- PASS — Final output is nonempty, coordinate-sorted, indexed, and readable.

### Input 3 — Variant B: reciprocal duplex UMI consensus

**Prompt:** Run two fresh duplex workflows on reciprocal paired UMIs and verify true-duplex construction, thresholds, topology, and final output.

**Observed output:** Both fresh runs retain RX, ZA, and ZB on 32 input-family records, use paired grouping, assign MI to 32 grouped records, call duplex consensus, and emit 2 consensus records. Each uses queryname-sorted input for `FilterConsensusReads --min-reads 2 1 1`, then produces a 2-record coordinate-sorted indexed BAM that passes quickcheck.

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

- PASS — Reciprocal duplex UMI tag topology is preserved.
- PASS — Paired grouping and duplex caller are selected.
- PASS — The two-strand filter is applied after realignment on queryname input.
- PASS — Two fresh runs give the same structural result.
- PASS — Both final BAMs are useful and parseable.

### Input 4 — Edge: QC flags, bounds, and empty BAM

**Prompt:** Exercise the fragment-QC population with flag-contaminated, empty, invalid-bound, and alternate-bound cases.

**Observed output:** The five-record flag fixture accepts one record and reports one secondary, one supplementary, one duplicate, and one QC-fail record. `0` and `-1` raise `ValueError`; `True` and `1.5` raise `TypeError`. The empty BAM returns typed zero values and zero filter counts without losing interpretation context.

**Scores:** Basic 38/40 | Specialized 58/60 | Total 96/100

- PASS — All major unwanted flags are excluded and counted.
- PASS — Invalid bounds fail specifically.
- PASS — Empty input is stable and explicit.
- PASS — Overlapping exclusion-count semantics are documented.
- PASS — The result remains analytical rather than clinical.

### Input 5 — Stress: metacharacter paths and ten-call stability

**Prompt:** Run the complete workflow with spaces, semicolon, dollar sign, and brackets in paths, then run ten consecutive complete calls and inspect safety, stability, and scientific boundaries.

**Observed output:** The metacharacter workflow receives each full path as one argv element and completes with 4 final records, coordinate order, index, and quickcheck success. AST inspection finds zero `shell=True`, `eval`, or `exec` calls, and no shell side-effect path appears. The separate shipped suite runs 6 tests with no skips and exits 0 after 427.209 seconds; its stability test performs ten complete calls and asserts the same 4-record output each time.

**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100

- PASS — Ordinary and metacharacter paths remain literal.
- PASS — No shell/code-evaluation surface exists.
- PASS — The stress output is useful and readable.
- PASS — Ten consecutive complete calls pass.
- PASS — Documentation keeps chemistry and achieved performance assay-conditional.

## Finding disposition

| Finding | Final state | Independent evidence |
|---|---|---|
| CFD-001 | closed | RX/ZA/ZB on 32/32 extracted and first-zipped records in simplex, two duplex runs, and the metacharacter run |
| CFD-002 | closed | Captured paired FASTQ → BWA `-C -p` → Zipper pipeline; 32 mapped/tagged records reach grouping |
| CFD-003 | closed | Filter input/output queryname-sorted; final output coordinate-sorted and indexed |
| CFD-004 | closed | zero `shell=True`; literal metacharacter paths complete with no side effect; bounded thread/tag validation passes |
| CFD-005 | closed | flag fixture 1/5 accepted; all exclusions counted; invalid bounds and empty input pass |
| CFD-006 | closed | assay-conditional guidance names recovery, depth, background, targets, pre-analytics, caller, and LoD; six primary DOI records verified |

## Evidence pointers

- Machine-readable results: `evidence/reaudit-results.json`
- Shipped-suite result: `evidence/shipped-suite-summary.json`
- Full shipped-suite log: `evidence/shipped-suite.stderr.txt`
- Test inputs: `inputs.json`
- Finding ledger: `finding-ledger.md`
- Scientific source notes: `scientific-source-notes.md`
- Exact source and candidate identity: `source-identity.json`

The Java 25 native-access warning is a future-compatibility warning from the pinned fgbio dependency; every affected process completed successfully and it is not an open candidate finding.

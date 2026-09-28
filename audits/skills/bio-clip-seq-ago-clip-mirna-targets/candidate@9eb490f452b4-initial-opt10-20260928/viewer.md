> **Audit record for `bio-clip-seq-ago-clip-mirna-targets`**
> - Audited working candidate `9eb490f452b4c0e4a27a95986816e7d84d689e6077a537e057368b9e471cf7e7`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/clip-seq/ago-clip-mirna-targets), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-clip-seq-ago-clip-mirna-targets

Generated: 2026-09-28

Exact candidate content SHA-256:
`9eb490f452b4c0e4a27a95986816e7d84d689e6077a537e057368b9e471cf7e7`.
The candidate subtree was unchanged during this audit.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical — current Hyb | 8 | 10 | 18 | 2/5 | ❌ ERROR |
| 2 | Variant A — shell/failure boundaries | 5 | 8 | 13 | 1/5 | ❌ PARTIAL |
| 3 | Edge — real 16-column schema | 6 | 9 | 15 | 1/5 | ❌ ERROR |
| 4 | Variant B — preprocessing/TargetScan | 26 | 31 | 57 | 3/5 | ❌ PARTIAL |
| 5 | Stress — interfaces/interpretation | 22 | 32 | 54 | 3/5 | ❌ PARTIAL |

**Static score:** 46/100  
**Execution average:** 31.4/100  
**Assertion pass rate:** 10/25  
**Weighted score:** 37/100 — **Reject**

Skill veto: **FAIL** for Stability, Determinism, and Security. Research veto:
**FAIL** for Methodological Ground and Code Usability. No audit-local repair was
attempted because every correction changes a scientific interface, parser,
failure boundary, or interpretation rule.

## Detailed outputs

### Input 1 — Canonical: current Hyb official-data route

**Prompt:** Run the supplied wrapper against current public Hyb and its
official test data; verify database, output, exit, schema, and row contracts.

**Execution:** After rebuilding the runtime from pinned Git blobs, direct Hyb
at `028ab6371ce793ca5e86f475fce1f2cc6ad3c677` produced 111 non-empty
miRNA-mRNA rows with exactly 16 fields. The exact candidate wrapper passed its
concatenated FASTA as `db`, so Hyb rejected the nonexistent installed database.
The wrapper nevertheless exited zero and wrote three empty derived tables.
Evidence: [`evidence/real-wrapper-summary.txt`](evidence/real-wrapper-summary.txt),
[`evidence/real-wrapper.stderr`](evidence/real-wrapper.stderr), and
[`evidence/official_test_comp_hOH7_hybrids_ua.hyb`](evidence/official_test_comp_hOH7_hybrids_ua.hyb).

**Scores:** Basic 8/40 | Specialized 10/60 | Total 18/100

**Assertions:**

- PASS — current pinned Hyb is executable on official public data.
- FAIL — the wrapper does not satisfy the installed-database contract.
- FAIL — it assumes an output name current Hyb does not create.
- FAIL — it returns zero after Hyb fails.
- PASS — the resource-infeasible full Yeo route is not credited as executed.

**Findings:** `AGO-001` P0, `AGO-004` P0.

### Input 2 — Variant A: paths, globs, and failure propagation

**Prompt:** Exercise missing-tool, exit-42, spaced-path, spaced-prefix, and
literal-glob cases and inspect partial outputs.

**Execution:** The missing-tool case returns 1, but it creates the combined
FASTA before checking. A fake Hyb exit 42 becomes wrapper exit 0 with empty
results. Spaces cause argument splitting and ambiguous redirects while the
wrapper returns zero. A literal `mir*.fa` input expands to include a sibling
`mir_extra.fa`. Complete machine-readable evidence:
[`evidence/wrapper-contract-results.json`](evidence/wrapper-contract-results.json).

**Scores:** Basic 5/40 | Specialized 8/60 | Total 13/100

**Assertions:**

- PASS — a missing Hyb binary returns nonzero.
- FAIL — subprocess status is not propagated.
- FAIL — spaces are not preserved.
- FAIL — a literal glob includes unintended data.
- FAIL — failed stages leave plausible empty tables.

**Finding:** `AGO-003` P0.

### Input 3 — Edge: true 16-column schema and expression filter

**Prompt:** Process one valid current Hyb record with matched expression and
verify orientation-aware RNA ids plus site-aware aggregation.

**Execution:** Current Hyb places RNA identifiers in fields 4 and 10, with
microRNA or mRNA in either segment; field 3 is energy and field 5 is a
coordinate. The wrapper checks field 5 for `ENST|NM_|XM_` and field 3 for
expression, so a valid current row produces empty filtered and count tables.
Evidence: [`evidence/real-hyb-schema-sample.tsv`](evidence/real-hyb-schema-sample.tsv)
and the `real_hyb_schema` case in the wrapper matrix.

**Scores:** Basic 6/40 | Specialized 9/60 | Total 15/100

**Assertions:**

- PASS — the audit verifies the live 16-column schema.
- FAIL — the mRNA filter reads a coordinate.
- FAIL — the expression filter reads energy and ignores segment order.
- FAIL — the valid matching row is discarded.
- FAIL — aggregation loses target and site identity.

**Finding:** `AGO-002` P0.

### Input 4 — Variant B: preprocessing and TargetScan overlap

**Prompt:** Execute the exact UMI-tools, cutadapt, soft-clip, and overlap
patterns; check read orientation, strand, coordinates, and interpretation.

**Execution:** UMI-tools 1.1.6 and cutadapt 5.1 ran, but the one-sided pattern
left the R2 ten-base prefix intact. The soft-clip command returned the intended
single diagnostic row and is correctly labeled diagnostic-only. The displayed
unstranded bedtools command returned two overlaps, including one opposite
strand; adding `-s` returned one. Official TargetScanHuman 8 fields are
transcript/UTR-relative, so they cannot be used directly as genomic BED.
Evidence:
[`evidence/adjacent-surface-results.json`](evidence/adjacent-surface-results.json).

**Scores:** Basic 26/40 | Specialized 31/60 | Total 57/100

**Assertions:**

- PASS — UMI-tools and cutadapt execute on a bounded fixture.
- FAIL — the example is not tied to the selected library's UMI orientation.
- PASS — soft clipping is not represented as a chimera call.
- FAIL — the displayed overlap lacks a safe strand/coordinate contract.
- PASS — a valid overlap is labeled prediction support, not functional proof.

**Finding:** `AGO-005` P1.

### Input 5 — Stress: external surfaces and evidence interpretation

**Prompt:** Classify Hyb, pyHyb, Yeo, HEAP, TargetScan, miRDB, and DIANA, then
audit the skill's direct/indirect, affinity, and negative-evidence rules.

**Execution:** Hyb is public and commit-identifiable but has no semantic release
tag. `pyHyb 0.4+` has no matching distribution; `hybkit` 0.3.6 is distinct.
Yeo chim-eCLIP is public CWL source but full human execution is bounded by large
references. HEAP is an experimental mouse method with public GEO data and
CLIPanalyze, not a standalone HEAP CLI. TargetScan and miRDB are public data;
DIANA docs were live while the documented example returned HTTP 500.

The skill correctly separates direct chimeras from ordinary AGO peaks and
constrains HEAP to mouse context. It nevertheless treats recovery counts as an
affinity proxy and a missing AGO peak as proof that a prediction is false or
non-functional. Evidence:
[`evidence/access-classifications.md`](evidence/access-classifications.md) and
[`scientific-source-notes.md`](scientific-source-notes.md).

**Scores:** Basic 22/40 | Specialized 32/60 | Total 54/100

**Assertions:**

- PASS — direct and indirect evidence are distinguished.
- PASS — the HEAP species boundary is explicit.
- FAIL — all advertised tool identities do not resolve.
- FAIL — counts are represented as affinity despite recovery biases.
- PASS — the main workflow asks users to justify the TPM threshold.

**Findings:** `AGO-006` P1, `AGO-007` P1, `AGO-008` P2.

## Static scoring

| Category | Score | Max | Main reason for deduction |
|---|---:|---:|---|
| Functional suitability | 4 | 12 | Only implementation breaks current Hyb and misparses output |
| Reliability | 1 | 12 | Swallowed failures, partial outputs, no validation |
| Performance/context | 7 | 8 | Good disclosure; broken routes waste execution |
| Agent usability | 9 | 16 | Clear decisions; missing executable contracts |
| Human usability | 5 | 8 | Discoverable but unsafe to adapt/run |
| Security | 5 | 12 | Unquoted user paths permit unintended input expansion |
| Maintainability | 7 | 12 | Good file separation; no parser or contract tests |
| Agent-specific | 8 | 20 | Strong triggers; weak composition, idempotency, determinism |
| **Total** | **46** | **100** | |

## Ordered remediation

1. `AGO-001` P0 — implement the current Hyb database, goal, id, and output contract.
2. `AGO-002` P0 — parse fields 4/10 by RNA type and preserve site evidence.
3. `AGO-003` P0 — quote and validate inputs, fail closed, and publish atomically.
4. `AGO-004` P0 — resolve or explicitly exclude non-deterministic pair assignments.
5. `AGO-005` P1 — provide library-specific preprocessing and a strand-safe TargetScan coordinate route.
6. `AGO-006` P1 — correct current tool identities and access classifications.
7. `AGO-007` P1 — narrow affinity and negative-evidence interpretations.
8. `AGO-008` P2 — add structured outputs, provenance, and focused regressions.

## Environment and limitations

- Tooling record:
  `F:\OpenScience\audit-envs\bio-clip-seq-ago-clip-mirna-targets\TOOLS.md`.
- Environment fingerprint:
  `dc64dc57f17e3f0de31a8d348a0c7045f7bc3b4e92c5191051a8249e8ac0bae3`.
- Rubric archive SHA-256:
  `e54e9ff8b0c3677abcfe657ad6ed92ba34dbdb8ad205c7157ad881f25afcf0de`.
- Executed: wrapper contract matrix, exact real wrapper, two clean direct Hyb
  runs, UMI-tools, cutadapt, samtools/awk, bedtools, and TargetScan 8 parsing.
- Public source/interface inspection: Yeo chim-eCLIP, HEAP/CLIPanalyze, Hyb,
  TargetScan, miRDB, DIANA, and package indexes.
- Resource-infeasible bounded: complete human Yeo chim-eCLIP workflow.
- Wet-lab unavailable: HEAP library preparation and biological validation.
- Remote unavailable: documented DIANA example endpoint (HTTP 500).
- Whole-dataset performance, biological replication, and reporter validation
  remain out of scope for this diagnostic pass.


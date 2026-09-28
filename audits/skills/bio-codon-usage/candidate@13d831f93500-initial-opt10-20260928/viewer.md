> **Audit record for `bio-codon-usage`**
> - Audited working candidate `13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/sequence-manipulation/codon-usage), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-codon-usage

Generated: 2026-09-28 · Exact candidate: `sha256-manifest-v1:13d831f93500607c6f8cd7ce8b0ece7238af8400c80b750a3a6d95d2e5b4dc77`

> Audit method: `skill-auditor@1.0` from the retained `skill-auditor.zip`. This is an initial diagnostic audit, not certification. Candidate bytes were not repaired.

## Result

- Static: **68/100**
- Execution average: **50.8/100**
- Assertions: **12/25 (48.0%)**
- Weighted score: **58/100 — Reject**
- Structural veto: **FAIL** — Stability
- Research veto: **FAIL** — Methodological Ground and Code Usability
- Ordered findings: `CODON-001` through `CODON-004` in [`finding-ledger.md`](finding-ledger.md)

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total | Assertions | Status |
|---:|---|---:|---:|---:|---:|:---:|
| 1 | Canonical | 38 | 55 | 93 | 5/5 | ✅ |
| 2 | Variant A | 8 | 13 | 21 | 1/5 | ❌ |
| 3 | Edge | 14 | 20 | 34 | 1/5 | ❌ |
| 4 | Variant B | 16 | 23 | 39 | 1/5 | ❌ |
| 5 | Stress | 28 | 39 | 67 | 4/5 | ⚠️ |

## Detailed outputs

### Input 1 — Canonical: supplied standard-code examples

**Prompt.** Run the supplied codon-count, RSCU, and CAI optimization examples on their built-in in-frame standard-code sequences and verify the optimized protein.

**Observed.** All three exact scripts exited 0 with empty stderr. Second executions reproduced byte-identical stdout. The CAI example moved its query from 0.098 to 1.000 and preserved `MAALDDKG*`. The skill correctly refuses to interpret max-CAI as guaranteed expression.

**Scores:** Basic 38/40 · Specialized 55/60 · **93/100** · Assertions **5/5**.

- PASS — All three exact scripts execute successfully.
- PASS — Repeated outputs are byte-identical.
- PASS — CAI output reports reference, query, optimized score, and changes.
- PASS — Standard-code protein is preserved.
- PASS — Expression is not inferred from CAI alone.

### Input 2 — Variant A: alternate genetic code 2

**Prompt.** Build and use a vertebrate-mitochondrial CAI index, score TGG, and optimize TGA while preserving its table-2 translation.

**Observed.** Construction with table 2 succeeds, but Biopython 1.85 `calculate()` hard-excludes TGG and divides by zero when it is the only scored codon. More seriously, `optimize()` translates input DNA with the standard code: table-2 TGA (tryptophan) became TAA (stop under table 2). The candidate's generic instruction to pass the matching table does not prevent this.

**Scores:** Basic 8/40 · Specialized 13/60 · **21/100** · Assertions **1/5**.

- PASS — Table-2 construction succeeds.
- FAIL — TGG-only scoring is defined.
- FAIL — Table-2 translation is preserved.
- FAIL — Preservation is verified under the selected code.
- FAIL — Table-specific sense and stop sets are respected end to end.

### Input 3 — Edge: malformed and empty inputs

**Prompt.** Analyze empty, one- or two-base trailing partial, shifted-frame, ambiguous-codon, stop-containing, and ATG/TGG-only inputs and report every rejection or discard.

**Observed.** The prose requires validation, but the shipped helpers do not implement it. Trailing bases are discarded, shifted frames produce plausible counts, `NNN` is retained in basic counts but ignored in RSCU, stops are ignored in RSCU, and empty `GC123`/CAI or ATG/TGG-only CAI surfaces raw `ZeroDivisionError`.

**Scores:** Basic 14/40 · Specialized 20/60 · **34/100** · Assertions **1/5**.

- PASS — Empty frequency output is an empty mapping.
- FAIL — Partial codons are rejected or reported.
- FAIL — Shifted frames are rejected before analysis.
- FAIL — Ambiguity and stops have one explicit disposition.
- FAIL — Zero-denominator inputs receive actionable validation errors.

### Input 4 — Variant B: CAI version semantics

**Prompt.** Verify Biopython 1.85 strict and non-strict tie handling, stop-codon contribution to CAI, and the normalized weight assigned to an unobserved synonymous codon.

**Observed.** `strict=True` raises on an alanine tie, as expected. Contrary to the candidate, `strict=False` emits no warning; an indexed unobserved TAG changed a score from 1.0 to 0.5; and the 0.5 pseudocount normalized to a final GCC weight of 0.05 against ten GCT observations. Empty and ATG/TGG-only queries are unguarded.

**Scores:** Basic 16/40 · Specialized 23/60 · **39/100** · Assertions **1/5**.

- PASS — Strict tie raises `ValueError`.
- FAIL — Non-strict tie emits the promised warning.
- FAIL — All stop codons are excluded as documented.
- FAIL — Every unobserved codon has final weight 0.5.
- FAIL — Empty/all-excluded denominators are guarded.

### Input 5 — Stress: simplified Nc versus codonW

**Prompt.** Compare the documented simplified Nc helper with codonW on a heterogeneous synonymous-family fixture and public *E. coli* `thrA` CDS, and judge cross-study comparability.

**Observed.** Both the helper and codonW execute deterministically. The candidate's approximation caveat is correct and important: the heterogeneous fixture scored 41.212 in the helper versus 30.77 in codonW, while `thrA` scored 48.854 versus 47.41. The helper is not interchangeable with Wright/codonW Nc.

**Scores:** Basic 28/40 · Specialized 39/60 · **67/100** · Assertions **4/5**.

- PASS — The exact helper executes on both fixtures.
- PASS — codonW executes on the same sequences.
- PASS — The candidate labels the helper nonstandard.
- PASS — Public `thrA` is used only as a metric fixture.
- FAIL — The helper is suitable as standard cross-study Nc.

## Veto decisions

### Structural veto

- **Stability: FAIL.** Two of five representative requests are partial because a documented valid alternate-code workflow changes the protein and malformed boundaries are not handled; zero-denominator inputs crash.
- **Contract: PASS.** Required frontmatter, files, provenance, and deterministic result shapes are present.
- **Determinism: PASS.** All three fixed examples reproduce byte-identically, and no unseeded stochastic method is used.
- **Security: PASS.** No credentials, destructive commands, user-string execution, or prompt-injection path was found.

### Research veto

- **Scientific Integrity: PASS.** No result, citation identifier, or biological outcome was fabricated.
- **Practice Boundaries: PASS.** The skill stays within sequence analysis and explicitly limits expression claims.
- **Methodological Ground: FAIL.** Alternate-code optimization can invert a sense codon into a stop, and the stated CAI semantics are not the installed API's behavior.
- **Code Usability: FAIL.** A documented valid table-2 path produces a biologically wrong result, and common malformed/empty boundaries are not guarded.

Both vetoes force `deployable=false` regardless of score. Fix all P0/P1 findings, prepare delta tooling for new exact bytes, and run an independent re-audit.

## Evidence map

- Structured execution observations: [`evidence/audit-results.json`](evidence/audit-results.json)
- Compact transcript: [`evidence/audit-transcript.txt`](evidence/audit-transcript.txt)
- Independent runner: [`audit_harness.py`](audit_harness.py)
- Test prompts: [`generated-test-inputs.json`](generated-test-inputs.json)
- Surface classifications: [`evidence/execution-classification.md`](evidence/execution-classification.md)
- Primary-source checks: [`evidence/research-checks.md`](evidence/research-checks.md)
- Exact script outputs: [`outputs/`](outputs/)
- Immutable identity: [`source-identity.json`](source-identity.json)

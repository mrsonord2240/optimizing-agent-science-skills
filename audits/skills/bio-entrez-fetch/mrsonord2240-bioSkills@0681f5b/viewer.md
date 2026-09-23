> **Audit record for `bio-entrez-fetch`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0681f5b](https://github.com/mrsonord2240/bioSkills/tree/0681f5b171b43eade5c4d81f0285dd9a5dbadb20/database-access/entrez-fetch) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-entrez-fetch

Generated: 2026-09-23

Source: `mrsonord2240/bioSkills@0681f5b171b43eade5c4d81f0285dd9a5dbadb20:database-access/entrez-fetch`

Final-pass metadata: `auditor_independent: false`; `final pass: fixed and audited under one brief, see CHECKPOINT.md`.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---:|---:|---:|---:|---:|---|---|
| 1 | Canonical | 39 | 58 | 97 | 4/4 | yes | ✅ |
| 2 | Variant A | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 58 | 96 | 4/4 | yes | ✅ |
| 4 | Variant B | 38 | 57 | 95 | 4/4 | yes | ✅ |
| 5 | Stress | 39 | 57 | 96 | 4/4 | yes | ✅ |
| 6 | Scope Boundary | 38 | 56 | 94 | 4/4 | yes | ✅ |
| 7 | Adversarial | 38 | 58 | 96 | 4/4 | yes | ✅ |

Execution average: **95.7/100**. Assertion pass rate: **28/28**.

## Runtime and execution evidence

- Private audit-owned runtime: `F:\OpenScience\audits\bio-entrez-fetch\private_runtime\venv`.
- Installed and loaded: Biopython 1.88, with NumPy 2.5.3. The shared `database-access` environment was not modified.
- Audit copy: `run/phase2_20260923/copied_source/`; no source script was imported or run in the worktree.
- Saved runner: `run/phase2_20260923/run_phase2_audit.py`.
- All seven process exit codes are zero in `run/phase2_20260923/outputs/execution_summary.json`.

## Detailed outputs

### Input 1 — Version-pinned GenBank and CDS retrieval

**Prompt:** “Fetch NM_007294.4 as GenBank, report its CDS features, retrieve the CDS translations for NC_000913.3, and verify a three-accession FASTA batch is not truncated.”

**Executed:** copied `examples/fetch_sequences.py` in the private runtime.

**Output evidence:** NM_007294.4 was 7,088 nt with one CDS; NC_000913.3 produced 4,318 translated proteins; the three accessions were all returned; `gbwithparts` produced 55,515 bytes.

**Assertions:** PASS — version-pinned record parsed; CDS count checked; translated proteins returned; batch truncation guard passed.

### Input 2 — Bulk summaries

**Prompt:** “For four nucleotide accessions and three PubMed records, retrieve only summary metadata in safe chunks and compare the cost against full GenBank retrieval.”

**Executed:** copied `examples/fetch_summaries.py`.

**Output evidence:** all requested nucleotide and PubMed docsums printed; `organism_of()` handled the current missing `Organism` field; live payloads were 3,506 bytes for ESummary and 165,775 bytes for EFetch, a 47.3x ratio.

**Assertions:** PASS — accession/version and length present; no Organism KeyError; PubMed metadata present; measured comparison emitted.

### Input 3 — PubMed MEDLINE and XML

**Prompt:** “Retrieve PMIDs 35412348 and 34502548 using stable MEDLINE parsing, then fetch rich XML for 35412348 including MeSH, grants, and PMC ID.”

**Executed:** copied `examples/fetch_pubmed.py`.

**Output evidence:** both MEDLINE records printed; the XML route reported seven MeSH terms and `PMC9093120` without treating a `StringElement` as a dictionary.

**Assertions:** PASS — MEDLINE records parsed; MeSH returned; PMC ID returned; defensive XML access completed.

### Input 4 — ClinVar metadata

**Prompt:** “Fetch ClinVar UID 4887763 and report the source record’s accession, variant name, and clinical-significance field only.”

**Executed:** copied `scripts/variant_records.py --email audit@example.org --db clinvar --uid 4887763`.

**Output:** `VCV000005107`, `NM_000199.5(SGSH):c.734G>A (p.Arg245His)`, `Pathogenic`.

**Assertions:** PASS — ElementTree route parsed DTD-less XML; expected VCV accession and source classification returned; no diagnosis or treatment advice produced.

### Input 5 — History-server FASTA

**Prompt:** “Fetch the version-pinned NM_007294.4 record through the ESearch history server into FASTA, using small chunks as a smoke test for the large-result workflow.”

**Executed:** copied `scripts/history_fetch.py --email audit@example.org --term 'NM_007294.4[ACCN]' --out history_small.fasta --chunk 4`.

**Output evidence:** reported one requested record and wrote a 7,385-byte FASTA beginning `>NM_007294.4`.

**Assertions:** PASS — count returned first; FASTA exists; header matches requested version; history-server route completed.

### Input 6 — dbSNP scope boundary

**Prompt:** “Fetch dbSNP UID 429358 and report chromosome and gene metadata; do not interpret it as a patient diagnosis or treatment recommendation.”

**Executed:** copied `scripts/variant_records.py --email audit@example.org --db snp --uid 429358`.

**Output:** chromosome `19`, gene `APOE`, plus the record’s clinical-significance metadata.

**Assertions:** PASS — namespaced XML parsed; chromosome and gene matched known record metadata; output remained record-level rather than medical advice.

### Input 7 — SRA malformed-response resistance and taxonomy

**Prompt:** “Convert SRA UIDs 8 and 7 to run rows, resolve taxonomy TXID 9606, and ensure an XML backend-error body is rejected rather than parsed as CSV.”

**Executed:** audit-owned `phase2_inline_refs.py`, which loaded copied `references/sra.md` and `references/gene-taxonomy-gds.md` after the documented setup.

**Output:** `ERROR_GUARD PASS`; 15 SRA rows beginning `SRR000001`; `LINEAGE Homo sapiens`.

**Assertions:** PASS — error body rejected; valid run rows parsed; human taxonomy resolved; process exited normally.

## Veto review

- T1 Stability: PASS — every saved execution completed without crash or hang.
- T2 Contract: PASS — required frontmatter and all referenced source files are present.
- T3 Determinism: PASS — fixed accessions/UIDs and explicit output assertions give repeatable record checks.
- T4 Security: PASS — no raw-string code execution or embedded secrets.
- M1 Scientific Integrity: PASS — claims and values are direct API outputs.
- M2 Practice Boundaries: PASS — variant routes preserve record-only boundaries.
- M3 Methodological Ground: PASS — correct fetch/summary, versioning, and malformed-response choices were exercised.
- M4 Code Usability: PASS — source-derived examples, scripts, and references executed in the private runtime.

## Recommendation

- **P2 — Close the CDS-only EFetch handle explicitly.** `cds_proteins()` materializes records but does not close its handle. Use a context manager or close after materialization for repeated caller loops.

## Final

**95/100 — Production Ready — deployable.** No veto, no P0 or P1. Source worktree was clean at the pinned tip before and after audit.

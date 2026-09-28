> **Audit record for `bio-codon-usage`**
> - Audited working candidate `3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/sequence-manipulation/codon-usage), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-28 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-codon-usage

Generated: 2026-09-28  
Exact candidate: `sha256-manifest-v1:3186a1debc804852b3ea016b9aeabebc4436a04791b84b13dba8669878d7e4dd`

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---:|---|---:|---:|---:|---:|---|
| 1 | Canonical | 40 | 58 | 98 | 5/5 | ✅ |
| 2 | Variant A | 40 | 58 | 98 | 5/5 | ✅ |
| 3 | Edge | 39 | 58 | 97 | 5/5 | ✅ |
| 4 | Variant B | 40 | 58 | 98 | 5/5 | ✅ |
| 5 | Stress | 39 | 57 | 96 | 5/5 | ✅ |

**Execution average:** 97.4 / 100  
**Assertion pass rate:** 25 / 25  
**Skill veto:** PASS  
**Research veto:** PASS  
**Final score:** 97 / 100 — ⭐ Production Ready

## Detailed outputs

### Input 1 — Canonical: deterministic standard-code shipped surfaces

**Prompt:** Run all three supplied standard-code examples twice, execute the focused regression suite twice, and verify the reported CAI result and translated protein.

**Observed output:**

```text
basic_analysis.py: exit 0 twice; stderr empty; byte-identical stdout
Sequence: ATGCGATCGATCGATCGATCGATCGATCGATCGTAA
Length: 36 bp (12 codons)
Genetic-code table: 1
Discarded input: none
Counts: ATC=2, ATG=1, CGA=3, GAT=2, TAA=1, TCG=3
GC123: total=47.2%, position1=41.7%, position2=50.0%, position3=50.0%

rscu_analysis.py: exit 0 twice; stderr empty; byte-identical stdout
Sequence: ATGCTTCTGCTACTGCTTCTACTGCTGCTACTGTAA
Genetic-code table: 1
Discarded input: none
Leu RSCU: CTG=3.00, CTA=1.80, CTT=1.20

cai_optimization.py: exit 0 twice; stderr empty; byte-identical stdout
Index built from 3 reference genes (64 codon weights)
Query CAI: 0.098
Optimized: ATGGCTGCTCTGGACGACAAAGGTTAA
Optimized CAI: 1.000
Protein preserved: MAALDDKG*
Codons changed: 6

tests/test_codon_usage.py: 12 tests passed twice
```

**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- PASS — All three supplied scripts execute successfully on both invocations. Six invocations exited zero with empty stderr.
- PASS — Repeated script invocations produce byte-identical stdout and stderr. Pairwise SHA-256 values matched.
- PASS — The focused candidate regression suite passes twice with the same cases and outcomes. Twelve tests passed both times.
- PASS — Standard-code optimization reaches the documented maximum and preserves the protein. CAI was 1.000 and the protein was `MAALDDKG*`.
- PASS — The canonical workflow does not infer expression success from CAI alone. The candidate requires downstream screening.

### Input 2 — Variant A: vertebrate-mitochondrial table-2 optimization

**Prompt:** Use genetic-code table 2 to optimize all four TGA/TGG sense-codon and AGA/AGG terminal-stop combinations, and prove that every source and result translates to MW*.

**Observed output:**

| Query | Source codons | Optimized | Optimized codons | Source protein | Optimized protein |
|---|---|---|---|---|---|
| `ATGTGAAGA` | ATG/TGA/AGA | `ATGTGAAGA` | ATG/TGA/AGA | `MW*` | `MW*` |
| `ATGTGGAGG` | ATG/TGG/AGG | `ATGTGAAGA` | ATG/TGA/AGA | `MW*` | `MW*` |
| `ATGTGAAGG` | ATG/TGA/AGG | `ATGTGAAGA` | ATG/TGA/AGA | `MW*` | `MW*` |
| `ATGTGGAGA` | ATG/TGG/AGA | `ATGTGAAGA` | ATG/TGA/AGA | `MW*` | `MW*` |

Mismatched standard index: `CAI index was not constructed with genetic-code table 2`.

**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- PASS — TGA and TGG are accepted as table-2 tryptophan codons.
- PASS — AGA and AGG are accepted as table-2 terminal stops.
- PASS — Every table-2 optimization preserves `MW*`.
- PASS — A CAI index built for another table is rejected before scoring.
- PASS — The documented wrapper uses the table-aware protein-intermediate route.

### Input 3 — Edge: strict and permissive CDS validation

**Prompt:** Exercise empty, partial, shifted, ambiguous, internal-stop, and whitespace inputs under the strict validator; then process an ambiguous-plus-partial input permissively and verify exact discarded offsets and shared analysis state.

**Observed strict errors:**

```text
empty: CDS is empty; provide at least one complete codon
partial: CDS length 5 is not divisible by three; trailing bases 'AA' at offset 3
shifted: first codon AAT is not a start codon in genetic-code table 1
ambiguous: invalid DNA codon 'NNN' at offset 3; illegal symbols: N
internal stop: internal stop codon(s) at codon indices [1] under genetic-code table 1
whitespace: CDS contains whitespace; normalize FASTA input before validation
```

**Observed permissive result:**

```text
Input: ATGNNNGCTTAAAA
Retained: ATGGCTTAA
Codons: ATG, GCT, TAA
Discard: offset 3, NNN, codon contains non-ACGT symbols
Discard: offset 12, AA, incomplete trailing codon
Counts: ATG=1, GCT=1, TAA=1
Frequency sum: 1.0
Alanine RSCU: GCT=4.0, GCC=0.0, GCA=0.0, GCG=0.0
```

**Scores:** Basic 39/40 | Specialized 58/60 | Total 97/100

**Assertions:**

- PASS — Strict validation rejects all six malformed boundaries with input-specific errors.
- PASS — Permissive validation retains frame and the exact admitted sequence `ATGGCTTAA`.
- PASS — Every discard has an exact offset, text, and reason.
- PASS — Counts, frequencies, and RSCU return the identical validation state.
- PASS — The admitted sequence produces coherent counts, normalized frequencies, and synonymous-family RSCU.

### Input 4 — Variant B: Biopython 1.85 CAI semantics and guards

**Prompt:** Verify indexed-stop contribution, family-normalized pseudocounts, strict and non-strict tie behavior, guarded zero-denominator handling, and standard-code protein preservation under Biopython 1.85.

**Observed output:**

```text
CAI without indexed stop: 1.0
CAI with indexed TAG: 0.5
Unobserved GCC weight against ten GCT observations: 0.05
strict=False warnings: []
strict=True error: TTT and TTC are equally preferred.
guard error: CAI is undefined because the validated query has no included codons
             (excluded: 0:ATG, 1:TGG)
guarded ATGGCTTAA: score=1.0, included=2, excluded=[ATG]
standard optimized DNA: ATGGCTGCTCTGGACGACAAAGGTTAA
standard translated protein: MAALDDKG*
```

**Scores:** Basic 40/40 | Specialized 58/60 | Total 98/100

**Assertions:**

- PASS — A stop present in the index contributes to the live score.
- PASS — The unobserved GCC pseudocount normalizes to 0.05.
- PASS — `strict=False` is silent and `strict=True` rejects a tie.
- PASS — The wrapper intercepts the ATG/TGG-only denominator and reports both exclusions.
- PASS — Standard max-CAI optimization preserves `MAALDDKG*`.

### Input 5 — Stress: public thrA and external Nc boundary

**Prompt:** Validate and analyze the public table-11 E. coli thrA CDS, rerun codonW on heterogeneous and public controls, and confirm that the candidate neither implements nor advertises the removed nonstandard Nc quantity as standard Nc.

**Observed output:**

```text
Public record: NC_000913.3:337-2799
Length: 2463 nt
Codons: 821
Boundary: ATG ... TGA under table 11
Discards: none
Count total: 821
Frequency sum: 1.0
GC123: total=53.0654, pos1=61.2667, pos2=40.3167, pos3=57.6127

Fresh codonW 1.4.4:
nc-heterogeneous 30.77
nc-public-thrA   47.41

Candidate scripts contain no effective_nc implementation.
SKILL.md says the skill does not calculate Nc.
The methods reference prohibits comparing the removed approximation across studies.
```

**Scores:** Basic 39/40 | Specialized 57/60 | Total 96/100

**Assertions:**

- PASS — Public `thrA` validates with the expected length, codon count, start, stop, and no discards.
- PASS — Counts, frequencies, RSCU, and GC123 run from the exact validation state.
- PASS — Fresh codonW controls reproduce Nc 30.77 and 47.41.
- PASS — The candidate neither ships nor advertises the removed approximation as standard Nc.
- PASS — The cross-study and external-tool boundary is explicit.

## Final adjudication

Both veto gates pass. The static score is 96, the dynamic average is 97.4, the Layer 1 average is 39.6/40, the Layer 2 average is 57.8/60, and assertions pass at 100%. Every Production Ready floor is met. `CODON-001` through `CODON-004` are closed; no new finding was identified.

Raw structured evidence is in `reaudit-results.json`; exact bytes are bound in `candidate-manifest.tsv` and `source-identity.json`.

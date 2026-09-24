> **Audit record for `bio-alignment-pairwise`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d45a647](https://github.com/mrsonord2240/bioSkills/tree/d45a6478bc0f0450f101b6c394415998d7151899/alignment/pairwise-alignment) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-23 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-pairwise (final-pass Phase 2)

Source: `mrsonord2240/bioSkills@d45a6478bc0f0450f101b6c394415998d7151899:alignment/pairwise-alignment`
Auditor independent: `false`
Note: final pass: fixed and audited under one brief, see CHECKPOINT.md

Generated: 2026-09-23  |  Source: `mrsonord2240/bioSkills@d45a6478bc0f0450f101b6c394415998d7151899:alignment/pairwise-alignment`

> Final-pass exception: `auditor_independent: false`; fixed and audited under one brief, see `F:\OpenScience\audits\_final_pass\bio-alignment-pairwise\CHECKPOINT.md`.

## Summary

| Input | Type | Total | Assertions | Executed |
|---|---|---:|---:|---|
| 1 | Canonical — HBA/HBB global protein alignment and gap conventions | 94/100 | 5/5 | true |
| 2 | Variant A — Mutated HBB local DNA placement and strand recovery | 94/100 | 4/4 | true |
| 3 | Edge — Semiglobal placement and invalid-input handling | 93/100 | 5/5 | true |
| 4 | Variant B — Empirical significance and dinucleotide shuffle | 94/100 | 4/4 | true |
| 5 | Stress — Accelerated-library agreement and saturation | 93/100 | 4/4 | true |
| 6 | Scope Boundary — Codon alignment, PAL2NAL trap, and database search | 92/100 | 4/4 | true |
| 7 | Adversarial — PID definitions, deprecated APIs, exports, and examples | 91/100 | 4/5 | true |
| 8 | Variant B — Fresh kinase-pair convention check | 95/100 | 4/4 | true |
| 9 | Edge — Fresh mammal-CDS DNA alignment and unknown strand | 95/100 | 4/4 | true |
| 10 | Stress — Fresh full-document code-fence execution | 96/100 | 5/5 | true |
| 11 | Variant A — Fresh documented HHsearch command | 96/100 | 4/4 | true |

Execution average: **93.9/100**. Assertions: **47/48 (97.9%)**. All **11/11** inputs executed.

Static: **93/100**. Final: **94/100 — ⭐ Production Ready**. Deployable: **true**. Veto: **PASS**.

## Evidence

The pre-Phase-2 report was moved intact to `F:\OpenScience\audits\_phase1-20260922\bio-alignment-pairwise`. The audit source was copied from the exact current tip into `run/skill`; SHA-256 for current `SKILL.md` is `D97AB041A0A716DE9D4D0465F4C006A462F8AF61444B3DF58A9560FB375F6EDF`. All scripts and raw logs are in `run/`.

## Detailed Inputs

### Input 1 — HBA/HBB global protein alignment and gap conventions

**Executed:** `True`. Executed on real UniProt HBA/HBB using Biopython, independent Gotoh, parasail, EMBOSS, BLAST+, and pwalign; see input1*.py/.sh/.R logs.

**Score:** Basic 38/40 | Specialized 56/60 | Total 94/100.

**Assertions:**
- [PASS] Global BLOSUM62 -11/-1 equals independent Gotoh, parasail and needle — 286.0 in all four
- [PASS] EMBOSS-default -10/-0.5 score is reproduced — 292.5
- [PASS] BLASTP 11/1 maps to Biopython local -12/-1 — raw 285 and identical HSP
- [PASS] pwalign uses the documented BLAST convention — global 10/1=286; local 11/1=285
- [PASS] Counts and explicit default-gap warning reproduce — 65/75/9; 55/37 versus 9/5

### Input 2 — Mutated HBB local DNA placement and strand recovery

**Executed:** `True`. Executed on seeded synthetic flanks plus a real HBB fragment; see input2_local_dna.py log.

**Score:** Basic 38/40 | Specialized 56/60 | Total 94/100.

**Assertions:**
- [PASS] Local score equals independent Gotoh and planted-score arithmetic — 268.0
- [PASS] Coordinates and counts recover the planted segment — 600..750; 142 identities, 5 mismatches, 3 gaps
- [PASS] Parasail cross-check agrees — 267 at 10/1
- [PASS] Reverse-complement selection recovers the correct orientation — 268.0 versus 34.5

### Input 3 — Semiglobal placement and invalid-input handling

**Executed:** `True`. Executed with synthetic fragment/reference and real mammal CDS; see input3_edge_semiglobal.py log.

**Score:** Basic 37/40 | Specialized 56/60 | Total 93/100.

**Assertions:**
- [PASS] Both semiglobal recipes return score 40 and span 300..320 — Deprecation warnings promoted to errors
- [PASS] Argument-order warning is real — swapped order scores -279
- [PASS] Documented invalid and accepted alphabets reproduce — lowercase/newline/J/U/empty reject; X/B/Z/SeqRecord accept
- [PASS] Internal-stop check isolates rabbit HBB2 — NM_001314043.1 only
- [PASS] Strand distribution matches the final wording — 300-pair median about 18; max 29

### Input 4 — Empirical significance and dinucleotide shuffle

**Executed:** `True`. Executed deterministic protein and DNA significance paths from the current copied example; see input4_significance.py log.

**Score:** Basic 38/40 | Specialized 56/60 | Total 94/100.

**Assertions:**
- [PASS] Seeded protein null is deterministic — three real pairs match on repeat
- [PASS] Related and unrelated pairs separate by empirical p-value — 0.001 versus 0.2478
- [PASS] Karlin-Altschul check is consistent with BLAST — 115.5 bits; fitted lambda 0.262
- [PASS] Current pure-Python dinucleotide shuffle is available — current examples/empirical_pvalue.py copied before run

### Input 5 — Accelerated-library agreement and saturation

**Executed:** `True`. Executed 4 kb/20 kb and 1,000-pair seeded synthetic cases; see input5_libs.py and finalpass2_allblocks_wsl.py logs.

**Score:** Basic 37/40 | Specialized 56/60 | Total 93/100.

**Assertions:**
- [PASS] parasail and edlib agree with independent scoring — 1,000/1,000 comparisons
- [PASS] Fixed-width parasail saturation is detected — 0 plus saturated=True versus 35644
- [PASS] Measured speed claims are plausible on this host — parasail 1.9-3.9x at 300 nt; edlib 714x at 20 kb
- [PASS] Linux-only pywfa and mappy snippets execute — scores/locus cross-check in all-block harness

### Input 6 — Codon alignment, PAL2NAL trap, and database search

**Executed:** `True`. Executed real HBB CDS, MAFFT/PAL2NAL in WSL, and MMseqs2 against eight real globins; see input6*.py/.sh logs.

**Score:** Basic 37/40 | Specialized 55/60 | Total 92/100.

**Assertions:**
- [PASS] Human/cow routing and protein-first codon alignment are frame-consistent — 441 codon columns
- [PASS] Documented PAL2NAL empty-output trap reproduces on the MAFFT rabbit route — exit 0, zero bytes, inconsistency error
- [PASS] Clean control yields two PAL2NAL records — human/cow control
- [PASS] Database-scale escape hatch executes — MMseqs2 finds HBA/HBB at 115 bits, E 3.096E-34

### Input 7 — PID definitions, deprecated APIs, exports, and examples

**Executed:** `True`. Executed pairwise2/max_alignments/PID/IUPAC/export checks plus all five copied examples; see input7_adversarial.py, input7_R_biostrings.R, and run_examples.py logs.

**Score:** Basic 37/40 | Specialized 54/60 | Total 91/100.

**Assertions:**
- [PASS] pairwise2 deprecation and islice guidance are accurate — warning, AttributeError, OverflowError, and islice reproduce
- [PASS] PID1-4 agree with EMBOSS and pwalign — 43.6/46.4/45.8/45.0
- [FAIL] Reference wording distinguishes the exact PID2 formula — the shown formula is exactly PID2, not merely 'similar to PID2'
- [PASS] NUC.4.4, algorithm names, output formatting and exports reproduce — all checks pass
- [PASS] All shipped examples run from the copied current source — five scripts complete without source bytecode writes

### Input 8 — Fresh kinase-pair convention check

**Executed:** `True`. Fresh real PKA/CDK2 pair not used in the HBA/HBB canonical input; see input8_kinase_conv.py, input8_ground_truth.sh, and input8_R_pwalign.R logs.

**Score:** Basic 39/40 | Specialized 56/60 | Total 95/100.

**Assertions:**
- [PASS] Global scores equal independent Gotoh and needle — 124, 186.5, and 110 as configured
- [PASS] BLAST mapping holds on a second protein family — local -12/-1=222 and identical HSP
- [PASS] pwalign mapping holds on this pair — 124/222/228
- [PASS] Identity/significance advice fits a distant true homolog — 29.1% PID2 and 90.1 bits

### Input 9 — Fresh mammal-CDS DNA alignment and unknown strand

**Executed:** `True`. Fresh real six-mammal HBB CDS exercise; see input9_real_dna.py log.

**Score:** Basic 39/40 | Specialized 56/60 | Total 95/100.

**Assertions:**
- [PASS] NUC.4.4 global scores equal EMBOSS needle across five orthologs — all five agree
- [PASS] Independent Gotoh agrees on human/cow — 1666.5
- [PASS] DNA-versus-protein routing threshold holds — minimum nucleotide PID1 85.2%
- [PASS] Unknown-strand recipe recovers locus and score — 183.0 and human span 126..246

### Input 10 — Fresh full-document code-fence execution

**Executed:** `True`. Freshly extracted and executed all 16 Python fences from current SKILL.md plus all six reference files in WSL; see finalpass2_allblocks.py log.

**Score:** Basic 39/40 | Specialized 57/60 | Total 96/100.

**Assertions:**
- [PASS] Every current fenced Python block executes — 16/16 with DeprecationWarning as error
- [PASS] Semiglobal documented values are asserted — both return 40.0 and span 300..320
- [PASS] parasail, edlib, pywfa and mappy comments are independently asserted — all four pass
- [PASS] Export and substitution-count fences execute — FASTA/Clustal/PSL/SAM nonempty
- [PASS] No source file was imported in place — audit copy used; source SHA-256 recorded

### Input 11 — Fresh documented HHsearch command

**Executed:** `True`. Fresh toy HH-suite profile database built from eight public globins, then current documented hhsearch command executed; see finalpass2_hhsearch.sh log.

**Score:** Basic 39/40 | Specialized 57/60 | Total 96/100.

**Assertions:**
- [PASS] Documented hhsearch flags execute against a real constructed database — query.a3m, -d toydb, -o query.hhr
- [PASS] Result contains all eight ranked globin profiles — eight summary rows
- [PASS] HBA query self-hit is strongly ranked — 100.0 probability; E 1.8E-93
- [PASS] Phylogenetic ordering is sensible — alpha, beta, then myoglobin profiles

## Veto Gates

Skill veto: PASS (stable current fences/examples; valid frontmatter; seeded or deterministic numerical paths; no credential/network/dynamic-code behavior).

Research veto: PASS. The evidence is computational sequence analysis, uses public data or explicitly seeded synthetic data, and makes no diagnostic/prescriptive claims. Independent Gotoh, EMBOSS, BLAST+, pwalign, parasail, edlib, MMseqs2, PAL2NAL, HH-suite and cross-reference checks were used where applicable.

## Recommendation

- P2: Name the displayed `identities / (identities + mismatches)` formula exactly PID2 rather than only similar to PID2.

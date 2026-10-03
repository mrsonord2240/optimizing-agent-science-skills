> **Audit record for `bio-splicing-quantification`**
> - Audited working candidate `0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alternative-splicing/splicing-quantification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) final re-audit worker, lane 2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: independent final re-audit (lane 2) of the fixed candidate; certification run
Exact candidate content SHA-256: `0c0354add99bca532a1c7168b94a08a1923249a1a7adfddd7f7e9997953355bf` (5 files, 42079 bytes; `skill_preflight --offline` PASS before and after, candidate bytes untouched)
Prior audit: identity 1e34dbd9664e, 64, Reject (veto M4), findings SQ-01..SQ-11
Category: Data Analysis | Mode: D (hybrid) | Complexity: Complex, 7 inputs

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 36 | 53 | 89 | 6/6 | COMPLETED |
| 2 | Variant A | 35 | 52 | 87 | 4/5 | COMPLETED |
| 3 | Variant B | 36 | 53 | 89 | 5/5 | COMPLETED |
| 4 | Edge | 33 | 48 | 81 | 4/5 | PARTIAL |
| 5 | Stress | 34 | 51 | 85 | 5/5 | COMPLETED |
| 6 | Scope Boundary | 35 | 51 | 86 | 6/6 | COMPLETED |
| 7 | Adversarial | 35 | 52 | 87 | 4/4 | COMPLETED |

**Static 84/100; Execution average 86.3/100; Final 85.4 (85); assertion pass rate 34/36; Layer 1 average 34.9/40; Layer 2 average 51.4/60.**
Grade: Production Ready. Skill veto PASS; Research veto PASS. Decision: candidate-ready for exact identity `0c0354add99b`. The final score has a narrow margin over the 85 gate.

## Prior finding dispositions (reproduced on real tool output, not inherited)

| ID | Finding | Verdict | Evidence |
|---|---|---|---|
| SQ-01 | inline snippet TypeError | fixed | snippet extracted from SKILL.md and executed verbatim on fresh real JC output: 20 reliable rows (32_snippet_and_forms) |
| SQ-02 | parser KeyError on 4 of 5 types | fixed | all five types x JC/JCEC run; row counts equal the files; coordinate columns per type (31, 33) |
| SQ-03 | wrong mean_PSI; group-1-only reliability | fixed | independent stdlib oracle: 30 real-output cases (5 types x JC/JCEC x N 0/10/20) maxerr 0, kept IDs equal; 10 engineered combinations incl. NA and low-read-in-one-group (31, 33) |
| SQ-04 | XS prerequisite / silent empty leafcutter | fixed | untagged: strand ? for all junctions, 0 clusters, rc 0; tagged: 115 clusters at -m 5; Skill check command works (35) |
| SQ-05 | IRFinder command and version | fixed | old syntax rc 1; BuildRefFromSTARRef rc 0; -m FastQ SE and PE rc 0, 7,955 rows (36); 1.3.1 stated, IRFinder-S 2.0 labelled not executed |
| SQ-06 | SUPPA2 TPM header and statsmodels pin | fixed | write_suppa_tpm output accepted, pandas default header fails, as-core statsmodels 0.15 ImportError, as-suppa 0.14.6 works (34, 37) |
| SQ-07 | hard-coded 0.1-0.9 filter | fixed | psi_range default 0.05-0.95 equals hand counts for 7 classes; (0.1,0.9) also equals (34) |
| SQ-08 | IncFormLen JC vs JCEC | fixed with caveat | planted JC 98/49, JCEC 149/49 confirmed; the constants hold only for typical events on real data (new SQ-13, P2) (32) |
| SQ-09 | unlabelled MAJIQ/VAST, unsourced figures | fixed | static inspection (input 7); not executed by design |
| SQ-10 | Related Skills names | fixed | all seven IDs exist on the shelf |
| SQ-11 | BAM list format, leafcutter source, LICENSE | fixed / not-a-defect | BAM list sentence present; clustering/ source exists; license: MIT frontmatter plus repository licence evidence, expected preflight warning only |

## New findings

- SQ-12 (P2): `parse_rmats_output` raises a raw `KeyError` on a header-only rMATS file (an event type with zero events). Loud failure, not a wrong result.
- SQ-13 (P2): SKILL.md states the JC `IncFormLen`/`SkipFormLen` as constants; real chrX data show them only for 719 of 958 SE rows.

## Not executed

MAJIQ V3/VOILA (restricted licence, not bypassed), VAST-TOOLS (6.7 GB VASTDB, heavy optional), Shiba, MicroExonator, S-IRFindeR, iREAD, IRFinder-S 2.0 (installable is 1.3.1). The Skill labels each as not executed.

## Evidence

Run root `F:\OpenScience\audits\bio-splicing-quantification\run-reaudit-1\` (`scripts/` published; `evidence/` logs and `out/` raw outputs stay local). Fresh rMATS 4.4.0 runs, independent oracles in scripts 31, 33 and 34, and a re-fingerprint of the three environments (unchanged, combined 20c07bbb...).

## Detailed outputs

### Input 1 - Canonical: Fresh rMATS-turbo 4.4.0 on real chrX 2v2 BAMs, then parse per the Skill (inline snippet, 5 types x JC/JCEC)

rMATS rc 0 (SE 958, A5SS 216, A3SS 251, MXE 51, RI 174); SKILL.md snippet extracted and executed verbatim (20 reliable SE rows); parse_rmats_output vs an independent stdlib-csv oracle on 36 file x min-reads cases: 0 failures, max error 0

Scores: Basic 36/40, Specialized 53/60, Total 89/100

- [PASS] rMATS runs with the flags the Skill states and writes all five JC and JCEC files - rc 0; row counts equal the earlier audit (958/216/251/51/174)
- [PASS] SKILL.md inline snippet runs on the real JC output - executed verbatim from the extracted code block; 20 reliable rows (was TypeError)
- [PASS] mean_PSI, mean_PSI_group1/2 equal an independent mean of IncLevel1+IncLevel2 for every event type, JC and JCEC - 30 real-data cases (5 types x JC/JCEC x min reads 0/10/20): maxerr 0.0 vs independent oracle (SQ-03)
- [PASS] Reliability keeps an event only if every replicate of BOTH groups has IJC+SJC >= N - kept ID sets equal the oracle in all 30 cases; e.g. JC SE 958/38/20, A5SS 216/12/9, A3SS 251/12/6, MXE 51/0/0, RI 174/10/7 at N 0/10/20 (SQ-03)
- [PASS] Per-event coordinate columns exist for A5SS, A3SS, MXE and RI - no KeyError for any of the five types, JC or JCEC (SQ-02)
- [PASS] IncLevelDifference never enters mean_PSI - engineered and real tables: pooled mean equals the hand value (SQ-03)

### Input 2 - Variant A: Planted hand-checkable SE data: effective-length PSI and IncFormLen statements

Planted IJC 80/SJC 10 gives IncLevel 0.8 (naive 0.889); mean_PSI_group1/2 0.7897/0.2027; JC IncFormLen 98 / SkipFormLen 49, JCEC 149; formula reproduces IncLevel (maxabs 0.0005, 1465 real replicate values); real JC IncFormLen is 148 in only 719 of 958 SE rows

Scores: Basic 35/40, Specialized 52/60, Total 87/100

- [PASS] rMATS IncLevel on planted data equals the hand value - 0.8/0.8/0.769 and 0.2/0.2/0.208; mean 0.7897/0.2027 equal expected.json
- [PASS] Skill formula reproduces IncLevel on real JC and JCEC output - real JC n=1465 maxabs 0.0005; JCEC n=1549 maxabs 0.0005; planted 0.0003/0.0004
- [PASS] JC vs JCEC IncFormLen description matches the files (SQ-08) - planted JC 98/49, JCEC 149/49; naive 0.889 vs normalised 0.800
- [PASS] IncLevelDifference sign matches b1 minus b2 - planted +0.587 with b1 the high group
- [FAIL] Statement that JC lengths are 2*(readLength-1) and readLength-1 holds across real events - real chrX JC SE: 148/74 in 719 of 958 rows; the others (58 distinct pairs) are smaller where short exons or introns limit read positions (SQ-13)

### Input 3 - Variant B: SUPPA2 PSI via run_suppa2_quantification, write_suppa_tpm and filter_reliable_events on planted and real chrX TPM

Planted PSI 0.8/0.2/0.5 exact; all seven psi files; 3,903 real PSI events (6,475 values) checked across 7 classes against an independent ioe+TPM recomputation (max error 1.1e-16); filter counts equal hand counts at default 0.05-0.95 and at 0.1-0.9; pandas-default header reproducibly fails, written header works; as-core statsmodels 0.15 breaks suppa.py as stated

Scores: Basic 36/40, Specialized 53/60, Total 89/100

- [PASS] SUPPA2 PSI equals the planted PSI through write_suppa_tpm - header line is A<TAB>B<TAB>C; G1;SE row 0.8 0.2 0.5 (SQ-06)
- [PASS] Real chrX PSI equals an independent recomputation from the .ioe and TPM - 7 classes, 3,903 events and 6,475 values, max |diff| 1.1e-16
- [PASS] filter_reliable_events default range 0.05-0.95 matches hand counts, and psi_range is a parameter (SQ-07) - SE 185, A5 87, A3 102, MX 11, RI 42, AF 215, AL 71; (0.1,0.9) gives 159/75/84/10/32/182/62, all equal hand
- [PASS] Skill states a TPM header contract and a SUPPA2 dependency pin that work - pandas-default header: "N expected, N-1 given", no psi file; as-suppa statsmodels 0.14.6 works; as-core 0.15.0 raises ImportError multipletests
- [PASS] Skill does not over-claim filter defaults - text says psi_range is a script filter, not a rMATS or SUPPA2 default

### Input 4 - Edge: parse_rmats_output on engineered NA/low-read tables for all 5 types x JC/JCEC, and on zero-event files

Engineered hand-valued tables pass for all 10 type/count combinations (low-read replicate in group 2 only, in group 1 only, NA replicate); a legitimate header-only rMATS file (type with zero events, as in the planted run) raises a raw KeyError

Scores: Basic 33/40, Specialized 48/60, Total 81/100

- [PASS] Low-read replicate in either group removes the event - group-2-only and group-1-only low-read events excluded at N=20 in all 10 combinations (SQ-03)
- [PASS] NA replicate values are excluded from the mean, not read as zero - group-1 mean 0.9 and pooled (0.9+0.1+0.3)/3 at N=0
- [PASS] Output carries the event-specific coordinate columns - column order equals RMATS_COORD_COLUMNS for every type
- [FAIL] A header-only rMATS file (zero events of a type) is handled - KeyError: 'min_reads_per_replicate' on planted A5SS/A3SS/MXE/RI (SQ-12)
- [PASS] Unsupported event_type gives an actionable message - ValueError: event_type must be one of ['A3SS', 'A5SS', 'MXE', 'RI', 'SE']

### Input 5 - Stress: regtools junctions + leafcutter clustering on STAR BAMs with and without XS tags, using the Skill strand check

Untagged BAMs: strand ? for all 2,838 junctions, 0 clusters at -m 50 and -m 5, rc 0; XS-tagged: + 1398, - 1343, ? 99 and 115 clusters at -m 5 (0 at -m 50 on this tiny data, as the Skill states)

Scores: Basic 34/40, Specialized 51/60, Total 85/100

- [PASS] Skill states the XS prerequisite beside the regtools command (SQ-04) - prerequisite paragraph with STAR --outSAMstrandField intronMotif and HISAT2 note
- [PASS] The Skill strand-check command distinguishes tagged from untagged junction files - tail -n +2 | cut -f6 | sort | uniq -c gives only ? versus + - ?
- [PASS] Tagged route yields clusters - 115 clusters at -m 5 from XS-tagged BAMs
- [PASS] Zero clusters with rc 0 on untagged BAMs is warned about - Skill says the run still exits 0 with zero clusters; reproduced
- [PASS] leafcutter_cluster_regtools.py source is named and exists - clustering/ of davidaknowles/leafcutter; file present in the staged clone

### Input 6 - Scope Boundary: IRFinder 1.3.1 reference build and FastQ quantification exactly as references/ states

Old syntax rc 1 (-r is required); BuildRefFromSTARRef rc 0 in 4m12s through the repaired staged wrapper; -m FastQ single-end and paired-end rc 0, 7,955 intron rows each, SE IRratio identical (r 1.0) to the tooling-delta rebuild, SE vs PE r 0.85

Scores: Basic 35/40, Specialized 51/60, Total 86/100

- [PASS] BuildRefFromSTARRef command runs as documented - rc 0; ref holds IRFinder, Mapability, STAR, genome.fa, transcripts.gtf (SQ-05)
- [PASS] IRFinder -m FastQ single-end runs and writes IRFinder-IR-nondir.txt - rc 0; 7,955 rows; IRratio 0-1
- [PASS] Paired-end form (two FASTQ) runs - rc 0; 7,955 rows; 98 vs 74 introns above IRratio 0.1 (PE vs SE of the same sample)
- [PASS] Old broken syntax is gone from the Skill - literal old form rc 1 reproduced; Skill now shows -m FastQ
- [PASS] IRFinder-S 2.0 is not presented as executed - labelled "not executed" in SKILL.md and the reference
- [PASS] Scope: IR route stays within quantification - no differential testing claimed

### Input 7 - Adversarial: Restricted and heavy surfaces (MAJIQ V3/VOILA, VAST-TOOLS) and unreproduced figures: must not be presented as verified

Document inspection by design: MAJIQ V3/VOILA (restricted licence) and VAST-TOOLS (6.7 GB VASTDB) were not executed and not bypassed; the Skill labels both, Shiba, MicroExonator, S-IRFindeR, iREAD and IRFinder-S 2.0 as not executed, and literature figures as not reproduced

Scores: Basic 35/40, Specialized 52/60, Total 87/100

- [PASS] MAJIQ V3/VOILA commands carry a not-executed label with the licence reason - "Not executed here" block precedes the commands
- [PASS] VAST-TOOLS and the other unexecuted tools are labelled - Version Compatibility paragraph and matrix cells
- [PASS] Benchmark figures are marked as literature, not reproduced - FDR 15-30%, ~14% junctions, ~70% microexons, 94% marked reported/not reproduced
- [PASS] Related Skills resolve on the shelf (SQ-10) - all seven shelf IDs exist under F:\optimized-scientific-skills\skills


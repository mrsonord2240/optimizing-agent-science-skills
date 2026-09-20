> **Audit record for `bio-pileup-generation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@5fc1304](https://github.com/mrsonord2240/bioSkills/tree/5fc1304c09be282792e56a613274508db5bfaead/alignment-files/pileup-generation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pileup-generation (second re-audit)
Generated: 2026-09-20  |  Source: `mrsonord2240/bioSkills@5fc1304c09be282792e56a613274508db5bfaead:alignment-files/pileup-generation`  |  Env: WSL `science`, samtools 1.24, bcftools 1.24, pysam 0.24.1

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 35 | 54 | 89 | 5/5 PASS | ✅ |
| 2 | Variant A | 35 | 55 | 90 | 5/5 PASS | ✅ |
| 3 | Edge | 36 | 54 | 90 | 5/5 PASS | ✅ |
| 4 | Variant B | 35 | 54 | 89 | 5/5 PASS | ✅ |
| 5 | Stress | 35 | 53 | 88 | 5/5 PASS | ✅ |
| 6 | Stress | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 7 | Adversarial | 30 | 45 | 75 | 3/5 PASS | ✅ |
| 8 | Variant B | 35 | 54 | 89 | 4/5 PASS | ✅ |

**Execution Average: 87.6 / 100**  |  **Assertion Pass Rate: 37/40**  |  **Static: 80/100**  |  **Final: 85 (Production Ready)**  |  Scripted checks: 311/313 pass

Previous re-audit: 84 (Limited Release, 223/230 checks). Pre-fix audit: 71 (Beta Only).  Complexity Moderate; N = 8 = 5 regression groups (the 7 archived inputs) + 3 new.

## What changed since the first re-audit, in one paragraph

Round 2 fixed five of the six findings for real (indel markers, find_variants N, --rf vs --lu/--nu, Access Reads print, soft-masked note) and the usage-guide cut lost nothing. It also **replaced a correct sentence with a false one**: the first re-audit's P1 ("stepper='all' + fastafile applies no BAQ is false") was itself wrong, because both the first re-auditor and the round-2 fixer labelled the *no-stepper-argument* call as `'all'`. pysam 0.24.1's default stepper is `'samtools'`. Evidence is in `run/x_probe_stepper_*.py` and input 7. Everything else the round-2 log claims reproduced on my own data.

## Method notes
- Skill copy: `run/skill/` (`diff -r` against the worktree clean); every Python function and bash block is extracted verbatim from that copy (`run/snippets.py`), never retyped.
- Data: synthetic and seeded (`00_`, `01_`, `02_`, `10_`, `11_`, `12_`, `13_`) plus real BAMs from `public-data\` (human chr22, RNA-seq, 1000G HG00349, ARTIC nanopore, sarscov2 PE/SE/UMI; copied and indexed under `run/data` because they are unindexed and read-only).
- Every check asserts on content (decoded pileup text vs pysam counts vs bcftools DP vs independent pysam subsets vs hand truth); exit codes are never the evidence. `run_everything.sh` reproduces the whole audit; logs are `run/log_*.txt`, per-check records `run/checks_in*.json`.
- Two probes inherited from the first re-audit asserted the OLD wrong claims; I updated them (marked `UPDATED`) and fixed their stepper labelling. One harness (t04 PIPESTATUS through `head`) was rewritten after `x_wrongpipe.sh` confirmed the Skill's statement independently.

## Detailed Outputs

### Input 1 — Canonical
**Prompt / scope:** REGRESSION: text pileup of the real human chr22 BAM (region/BED/-q/-Q), columns, symbols, defaults, pysam table on real data

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** script t01: 28/28 checks pass. Options table, depth-0 rows, MAPQ char, BAQ (40 positions default vs -B) and the pysam mapping all reproduce on real data.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] Output Format claims hold on real data: col4 depth == number of read symbols == length of col6; the documented row 'chr22 1952 T 0 * *' exists — 1157 rows decoded with an independent parser; exact row present
- [PASS] pysam call with fastafile and no stepper argument equals `samtools mpileup` default (BAQ), and without fastafile equals `-B`, position by position (len(pileups)) — 0 of 1157 positions differ for both; n (not len(pileups)) differs at 1087, as the Skill states
- [PASS] Documented defaults are real: -Q 13, default --ff = UNMAP,SECONDARY,QCFAIL,DUP, overlap counted once — --ff 0 raises depth sum 670999 -> 671070; named flag list == default
- [PASS] mpileup -B -Q0 -q0 -x -A depth equals `samtools depth -a -J` at every position (independent tool) — same positions, same max 2532
- [PASS] Scope: only mpileup/pysam facts asserted; no clinical or variant-pathogenicity claim made — nothing outside pileup generation

### Input 2 — Variant A
**Prompt / scope:** REGRESSION: pysam allele_counts / allele_frequency / find_variants / pileup_text / Access Reads on planted synthetic + real BAM, shipped example

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** script t02: 28/28 checks pass. Access Reads snippet again prints read name, strand, base and quality; ref-skip vs deletion classification correct.

**Scores:** Basic 35/40 | Specialized 55/60 | Total 90/100

**Assertions:**
- [PASS] allele_counts at the planted SNP synA:100 returns 30 ref + 10 alt, all Q40 — Access Reads snippet lists (name, strand, base, Q) for the same 40 reads
- [PASS] Reference skips are not deletions: synA:400 (splice) gives 3 'Reference skip' and no 'Deletion'; the true deletion synA:251 still reports 4 'Deletion' — is_refskip tested first
- [PASS] pileup_text equals `samtools mpileup` row for row on the synthetic truth BAM (623 rows with splice/indel/overlap/flag events) under default, -B and -q 20 -Q 20 -x -A equivalents — 0 differing rows; real BAMs are covered in input 5
- [PASS] examples/allele_counts.py from a clean copy runs and matches mpileup -B -q20 -Q20 depth at a real position — T 30 / C 10 at synA:100; contig names with ':' handled
- [PASS] Errors from the shipped example are one-line messages, not tracebacks — range, missing colon, unknown contig, unindexed BAM each print one 'Error:' line

### Input 3 — Edge
**Prompt / scope:** REGRESSION: every silent default (flags, -Q, depth 0 rows, BAQ hiding a deletion, max depth 8000) and the shipped example on hostile input

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** script t03: 41/41 checks pass. Depth cap, flag defaults, BAQ-hidden deletion (depth 8 -> 4) and the max_depth=0 trap all reproduce.

**Scores:** Basic 36/40 | Specialized 54/60 | Total 90/100

**Assertions:**
- [PASS] samtools -d 8000 default truncates a 9000x BAM; -d 0 and -d 1000000 restore 9000; pysam max_depth=0 is still 8000 — documented trap is real
- [PASS] Default flag filter drops DUP/SECONDARY/QCFAIL/UNMAP: depth 10 at synA:825, 16 with --ff 0, bcftools --ns 0 DP 16 — table row confirmed in both tools
- [PASS] BAQ hides a 3 bp deletion in a text pileup (depth 8 -> 4, no -3CGT marker) and -B restores it — matches the Skill's sentence
- [PASS] Shipped example rejects hostile input with a one-line Error (contig with ':', 'chr1:1,000', range, position < 1, unindexed BAM) — rc 1, no traceback
- [PASS] Skill does not recommend `-d` values that silently truncate deep targeted data — cheat sheet uses -d 0 / -d 600000 / -d 1000000; usage-guide advice removed

### Input 4 — Variant B
**Prompt / scope:** REGRESSION: bcftools mpileup | call (germline, BCF intermediate, multi-sample -d 100000, parallel-by-contig, the 'WRONG' pipe) + library cheat sheet on real ARTIC/RNA-seq/1000G + error messages

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** scripts t04 (21/21) and t05 (28/28). Every bash block ran; contigs merge in header order; quoted error texts are the real 1.24 messages.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] Modern Germline Calling, BCF Intermediate and Multi-Sample blocks run and call the planted SNV/indels; per-sample AD equals planted (17,3 | 8,12) — 4 records on the single-sample truth BAM
- [PASS] Parallel by Contig: output contigs in header order chr1..chr11 (glob order would be chr1,chr10,chr11,chr2...) and a failing contig stops the merge — 11 records, index built; nonexistent reference -> non-zero, no all.vcf.gz
- [PASS] The 'WRONG' pipe message and status are real: `samtools mpileup | bcftools call` -> 'Failed to read from standard input: unknown file type', exit 255, no output; RIGHT pipe gives 4 records — re-checked independently in x_wrongpipe.sh (the first harness mis-read PIPESTATUS)
- [PASS] Every cheat-sheet library row runs on real ARTIC nanopore, spliced RNA-seq and 1000G BAMs and gives the expected effect (-aa 29903 rows, -B, -A ...) — 28/28 checks
- [PASS] Common Errors messages are the real ones: faidx 'sequence was not found' with exit 0 and N rows, fail to parse region, unindexed BAM — verified with ARTIC BAM vs the wrong FASTA

### Input 5 — Stress
**Prompt / scope:** REGRESSION: previous re-audit's own inputs -- planted truth BAM (11 event types, colon contig, N/soft-masked ref) + 1,862-read random test, and 4 real + 2 synthetic BAMs pysam-vs-samtools matrix with 432,147 real pileup_text rows

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** scripts t06 (56/56) and t07 (28/28). Two probes that asserted the OLD wrong claims (stepper='all' + fastafile, bcftools --nu) were updated to the round-2 text; note the 'stepper=all' label in those probes was itself wrong (see input 7).

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] pileup_text equals samtools mpileup row for row on the planted new.bam and the 4,486-row random fuzz-clean BAM under 13 option sets each (default, -B, -q/-Q, -x, -A, --ff 0, --rf 16, -E, -C 50, -d 15, combined), and on the adjacent-indel read 10M2I2D10M — 0 differing rows in every comparison
- [PASS] find_variants reports no reference-N site (nA:800-805) and no read-N allele (nA:790); the soft-masked site nA:920 G>A 3/8 (upper-case ref) and the overlap site nA:730 3/6 are right — SNV-only scope holds: nothing at the planted insertions
- [PASS] pysam parameter table (12 rows: -Q -q -x -A --ff -d -E -C, combined) equals samtools depth position by position on 4 real + 2 synthetic BAMs, and pileup_text equals mpileup row for row on 432,147 real rows — 6 datasets x 12 rows equal; the updated probes now assert the round-2 text
- [PASS] Soft-masked reference: mpileup prints column 3 lower-case as in the FASTA (documented in Output Format) and pileup_text equals it row for row — fuzz-clean and planted references carry soft-masked blocks; 0 differing rows
- [PASS] Safety/scope: no fabricated numbers; documented figures (1087/1157, 8 -> 4, memory-hog) reproduce — all reproduced

### Input 6 — Stress
**Prompt / scope:** NEW: 23 legal CIGAR templates (=/X runs, adjacent identical ops, I-D-I/D-I chains, N beside I/D, indels next to S/H) -> `indel_text`/`pileup_text` vs samtools mpileup row for row, 5 option sets, plus 13 wild templates

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** script 10_cigar_fuzz.py: 5/5 scored checks. 3,784 rows x 5 option sets (default, -B, -E, -q20 -Q20 -x -A, --ff 0 -Q 0 -B) identical to samtools; wild set: only P (padding) CIGARs differ, and a CIGAR ending in D crashes pileup_text with -Q 0 (informational).

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**
- [PASS] Legal templates: pileup_text == samtools mpileup default, row for row (3,784 rows, 714 with indel markers, 40 with two adjacent markers, 440 lower-case-reference rows) — 0 differing rows
- [PASS] Same under -B (952 marker rows, 55 adjacent), -E, -q 20 -Q 20 -x -A, and --ff 0 -Q 0 -B (1,085 marker rows, 63 adjacent) — 0 differing rows in all 4 remaining option sets
- [PASS] Indels at read ends and beside soft clips (leading I, trailing I, S+I, I+S, D+S, S+D) match samtools — wild templates IM, MI, SIM, MIS, MDS, SDM: 0 differing rows in all 5 option sets
- [PASS] I-D-I, D-I-D and N-I-D chains match samtools — MIDIM, MDIDM, MNIDM: 0 differing rows
- [PASS] Scope: helper behaviour outside what an aligner emits is reported, not hidden — P-op CIGARs (MPIM) differ in 148-462 rows depending on the option set; CIGARs ending in D (MD, MID) equal samtools in 4 option sets but raise IndexError under --ff 0 -Q 0 -B. Neither is claimed by the Skill; recorded as P2

### Input 7 — Adversarial
**Prompt / scope:** NEW: the round-2 BAQ and --rf statements re-derived on data the earlier auditors did not use (sarscov2 PE/SE/UMI real, 1000G+calmd BQ tags, own indel-dense BAM with none / computed / all-'@' BQ tags), both steppers, and 6 flag masks vs independent subsets

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** script 11_baq_rf.py: 38/40 checks. With no stepper argument (pysam 0.24.1's real default = 'samtools') every BAQ mapping and --rf/--lu/--nu claim holds. The Skill's sentence 'BAQ is applied under either stepper ('all', the default, or 'samtools')' is FALSE: explicit stepper='all' + fastafile applies NO BAQ (538/538 BAQ positions differ on the own single-end BAM, 49/49 on real SE), and 'all' is not the default.

**Scores:** Basic 30/40 | Specialized 45/60 | Total 75/100

**Assertions:**
- [PASS] With pileup() called with no stepper argument, the 4 BAQ table mappings (fastafile; no fastafile / compute_baq=False; fastafile + redo_baq=True) equal samtools default / -B / -E in depth and per-symbol counts at every position on all 7 datasets — BQ-tag semantics right: all-'@' tags -> default == -B (0 differ) but -E differs at 538; also true for explicit stepper='samtools'
- [PASS] `--rf` (samtools) == pysam flag_require == bcftools --lu == bcftools --rf (any bit set); bcftools --nu requires ALL bits, on 6 masks against independent pysam subsets — mask 65: any-bit 200 reads (DP 27401) vs all-bit 100 reads (DP 13884); samtools --rf 65 == pysam == --lu; --nu == all-bit subset
- [PASS] `-B` and `-E` cannot be combined — samtools: 'Error: The -B option cannot be combined with -E', no output
- [FAIL] SKILL claim: with fastafile BAQ is applied under either stepper -- stepper='all' + fastafile equals `samtools mpileup -f` on single-end data — stepper='all' + fastafile == stepper='all' without fastafile == -B: 538/538 (own BAM), 49/49 (real SE), and 0 differing from -B once overlap/orphans are neutralised on human PE; quality strings identical with and without fastafile under 'all'; no argument (redo_baq, compute_baq, max_depth) changes it
- [FAIL] SKILL claim: 'all' is pysam's default stepper — the no-argument call equals stepper='samtools' on every dataset and differs from 'all' on 7 of 7 (overlap removal, orphan filter, BAQ); the -x/-A 'default matches' rows hold only for the real default

### Input 8 — Variant B
**Prompt / scope:** NEW: find_variants N handling, region edges, kwargs, restored Access Reads print, soft-masked reference, shipped example on a planted BAM (exact depth/alt counts) + real 1000G chr20 and sarscov2; usage-guide dedup audit

**Status:** COMPLETED ✅  |  **Executed:** true

**Output (what ran and what it printed):** scripts 12_find_variants_access.py (17/17) and 14_usage_guide_dedup.py (21/21). find_variants returned exactly the 8 hand-derived SNVs; equals an independent mpileup decode on 119 real 1000G SNVs and 3 sarscov2 SNVs. All 14 old usage-guide sections have their content in SKILL.md.

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] find_variants on the planted BAM == hand truth: 120 (8/20), 520 (2/17 after 3 read-N dropped), 620 (exactly 0.10 kept), 720 (soft-masked ref, upper-case ref reported), 820+821 adjacent, 1000 (MAPQ-0 alt counted at default), 1150 — no reference-N (300-304) or read-N artefacts; depth 9, 1/21, Q10 alt and insertion-only sites not called
- [PASS] find_variants == independent decode of samtools mpileup -B -Q 20 on real 1000G HG00349 chr20 (119 SNVs) and real sarscov2 (3 SNVs); **pileup_kw and 0-based region edges behave as documented — min_base_quality=5 restores site 900; min_mapping_quality=1 drops site 1000; [1149,1150) -> 1150 only
- [PASS] Restored Access Reads snippet at real MT192765.1:5700 prints name, strand, base, Q for 3 reads, equal to `samtools mpileup --output-extra QNAME,FLAG`; depth line equals column 4 — tuple sets identical
- [PASS] usage-guide dedup lost nothing needed: 14 old sections (prerequisites, format tables, commands, pipeline, parallel, 4 pysam blocks, troubleshooting, tips) are present or replaced by corrected content in SKILL.md; dropped items (the 'No sequences in common' text, the `mpileup -g` prompt, the `-d 500`/`-d 1000` advice) were wrong on samtools 1.24 or contradict the measured depth-cap trap — anchor checks 14/14; new guide keeps 9 prompts and the 6-step agent walk-through, no verbatim duplicate lines
- [FAIL] allele_counts / allele_frequency treat a read-base N consistently with find_variants — allele_counts at pv1:420 returns {G:17, N:3} and allele_frequency divides by 20, while find_variants drops N from allele and depth; not stated in the docstring (P2)

## Execution evidence (trimmed; full logs in `run/log_*.txt`, per-check records in `run/checks_in*.json`)

### Steps 1-3: veto, classification
Skill veto T1-T4 PASS (no eval/exec of user strings, no network, fixed shell patterns, deterministic outputs: every comparison is exact). Category 3 Data Analysis, Mode D (SKILL.md code + shipped example script), Moderate complexity, N = 8 (5 regression groups, 3 new).

### Input 7 -- the finding that changes the picture (stepper default and BAQ)

Probe 6 (`x_probe_stepper_default.py`, human chr22 PE BAM, depth per position vs samtools):
```
pysam 0.24.1
docstring around 'stepper': stepper : string The stepper controls how the iterator advances. Possible options for the stepper are ``all`` skip reads in which any of the following flags are set: BAM_FUNMAP, BAM_FSECONDARY, BAM_FQCFAIL, BAM_FDUP ``nofilter`` use
samtools default vs -B differ at 40
   no stepper arg, no fastafile         vs samtools default   40 differ | vs -B    0 differ
   no stepper arg + fastafile           vs samtools default    0 differ | vs -B   40 differ
   stepper='all' + fastafile            vs samtools default  311 differ | vs -B  281 differ
   stepper='samtools' + fastafile       vs samtools default    0 differ | vs -B   40 differ
   stepper='all' no fastafile           vs samtools default  311 differ | vs -B  281 differ
   stepper='nofilter' no fastafile      vs samtools default  396 differ | vs -B  370 differ
```
Probe 3 (`x_probe_stepper_baq3.py`, own single-end BAM, every pysam argument that could plausibly enable BAQ under stepper='all'):
```
samtools default vs -B differ at 538 positions (-d 1000000)
all+fa                                                       vs samtools default:  538 differ | vs -B:    0 differ
all+fa max_depth=1000000                                     vs samtools default:  538 differ | vs -B:    0 differ
all+fa max_depth=8000                                        vs samtools default:  538 differ | vs -B:    0 differ
all+fa redo_baq=True                                         vs samtools default:  538 differ | vs -B:    0 differ
all+fa compute_baq=True                                      vs samtools default:  538 differ | vs -B:    0 differ
all+fa max_depth=1000000 + redo_baq                          vs samtools default:  538 differ | vs -B:    0 differ
all+fa ignore_overlaps=False                                 vs samtools default:  538 differ | vs -B:    0 differ
all+fa min_base_quality=0 -> vs samtools -Q 0 not compared   vs samtools default:  538 differ | vs -B:    0 differ
samtools+fa                                                  vs samtools default:    0 differ | vs -B:  538 differ
samtools+fa max_depth=1000000                                vs samtools default:    0 differ | vs -B:  538 differ
```
Probe 2 (`x_probe_stepper_baq2.py`, second method: the base-quality string pysam hands out in one BAQ-affected column; BAQ rewrites qualities in place):
```
positions where samtools quality column differs default vs -B (-Q 0): 842 [19, 23, 29, 30, 32]
samtools default (-Q 0): 49?4593
samtools -B      (-Q 0): 4;?4593
pysam stepper=all       + fastafile qualities: 4;?4593
pysam stepper=all       no fastafile qualities: 4;?4593
pysam stepper=samtools  + fastafile qualities: 49?4593
pysam stepper=samtools  no fastafile qualities: 4;?4593
```
Probe 4 (`x_probe_stepper_baq4.py`): with `-x -A` on the samtools side and `ignore_overlaps=False, ignore_orphans=False` on the pysam side, stepper='all' + fastafile equals `-B` (0 differ) and differs from the default; with default options it matches neither:
```
[default options] samtools default vs -B differ at 40
   stepper=all     +fa vs default:  311 differ | vs -B:  281 differ
   stepper=samtools+fa vs default:    0 differ | vs -B:   40 differ
[-x -A / ignore_overlaps=False, ignore_orphans=False] samtools default vs -B differ at 66
   stepper=all     +fa vs default:   66 differ | vs -B:    0 differ
   stepper=samtools+fa vs default:    0 differ | vs -B:   66 differ
```
`11_baq_rf.py` summary lines (data, discrimination, the two failing claims, `--rf`/`--lu`/`--nu`):
```
real sarscov2 PE: positions 12676; samtools default vs -B differ at 52, default vs -E 0, -B vs -E 52; depth sums {'default (-f)': 19605, '-B': 19657, '-E': 19605}
real sarscov2 SE: positions 9839; samtools default vs -B differ at 49, default vs -E 0, -B vs -E 49; depth sums {'default (-f)': 13872, '-B': 13921, '-E': 13872}
real sarscov2 UMI-PE: positions 12662; samtools default vs -B differ at 51, default vs -E 0, -B vs -E 51; depth sums {'default (-f)': 19683, '-B': 19734, '-E': 19683}
real 1000G + calmd BQ tags: positions 98421; samtools default vs -B differ at 800, default vs -E 5, -B vs -E 795; depth sums {'default (-f)': 910268, '-B': 911690, '-E': 910273}
own indel-dense, no BQ tag: positions 1469; samtools default vs -B differ at 538, default vs -E 0, -B vs -E 538; depth sums {'default (-f)': 24419, '-B': 25081, '-E': 24419}
own + calmd BQ tags: positions 1469; samtools default vs -B differ at 591, default vs -E 81, -B vs -E 538; depth sums {'default (-f)': 24334, '-B': 25081, '-E': 24419}
own + all-'@' BQ tags: positions 1469; samtools default vs -B differ at 0, default vs -E 538, -B vs -E 538; depth sums {'default (-f)': 25081, '-B': 25081, '-E': 24419}
[PASS] in9 discrimination: default != -B on the own indel-dense BAM and on real 1000G+BQ (else the BAQ mapping test proves nothing)  -- {'real sarscov2 PE': (52, 0, 52), 'real sarscov2 SE': (49, 0, 49), 'real sarscov2 UMI-PE': (51, 0, 51), 'real 1000G + calmd BQ tags': (800, 5, 795), 'own indel-dens
[PASS] in9 discrimination: with all-'@' BQ tags samtools default == -B (tag reused) but -E differs (recomputed): pysam fastafile == default, redo_baq == -E  -- (0, 538, 538)
stepper='all' mismatches per dataset: [('real sarscov2 PE', [('default (-f)', 'fastafile', 550), ('-B', 'no fastafile', 498), ('-B', 'fastafile + compute_baq=False', 498)]), ('real sarscov2 SE', [('default (-f)', 'fastafile', 49), ('-E', 'fastafile + redo_baq=True', 49)]), ('real sarscov2 UMI-PE', [
[FAIL] in9 SKILL claim 'BAQ applied under either stepper': fastafile + stepper='all' equals `samtools mpileup -f` (BAQ on) on the single-end datasets (own baq.bam, sarscov2 SE) -- no overlap/orphan effects can explain a difference  -- {'own': [('default (-f)', 'fastafile', 538)], 'sc SE': [('default
[FAIL] in9 SKILL claim "stepper 'all' is the default": the pysam call with NO stepper argument behaves like stepper='all' on every dataset (it does not: it equals 'samtools')  -- no-arg == 'samtools' on all datasets: True; 'all' differs from the no-arg call on: real sarscov2 PE, real sarscov2 SE, re
flags in sarscov2 PE BAM: {163: 49, 83: 49, 99: 47, 147: 47, 165: 2, 89: 2, 81: 1, 161: 1, 73: 1, 133: 1}
bcftools unfiltered DP sum 27401
mask 16: any-bit subset 99 reads (DP sum 13614), all-bit subset 99 reads (DP sum 13614); bcftools --lu 13614 --nu 13614 --rf 13614
mask 64: any-bit subset 100 reads (DP sum 13884), all-bit subset 100 reads (DP sum 13884); bcftools --lu 13884 --nu 13884 --rf 13884
mask 128: any-bit subset 100 reads (DP sum 13517), all-bit subset 100 reads (DP sum 13517); bcftools --lu 13517 --nu 13517 --rf 13517
mask 65: any-bit subset 200 reads (DP sum 27401), all-bit subset 100 reads (DP sum 13884); bcftools --lu 27401 --nu 13884 --rf 27401
[PASS] in9 discrimination for mask 65: any-bit and all-bit subsets differ (200 vs 100 reads), so the row's `--nu` warning is non-trivial  -- (200, 100)
mask 99: any-bit subset 200 reads (DP sum 27401), all-bit subset 47 reads (DP sum 6579); bcftools --lu 27401 --nu 6579 --rf 27401
[PASS] in9 discrimination for mask 99: any-bit and all-bit subsets differ (200 vs 47 reads), so the row's `--nu` warning is non-trivial  -- (200, 47)
mask 3: any-bit subset 200 reads (DP sum 27401), all-bit subset 192 reads (DP sum 26730); bcftools --lu 27401 --nu 26730 --rf 27401
[PASS] in9 discrimination for mask 3: any-bit and all-bit subsets differ (200 vs 192 reads), so the row's `--nu` warning is non-trivial  -- (200, 192)
```
The two failing scripted checks are exactly two SKILL.md statements: line 227 ("BAQ ... is applied under either stepper ('all', the default, or 'samtools')") and the table row at line 231 (`-f ref.fa` (BAQ on) | `fastafile=FastaFile(ref)` | either stepper).

### Input 6 -- CIGAR-template differential test (`10_cigar_fuzz.py`)
```
cg_legal reads 1730 bam records 1730 
cg_legal [default] samtools rows 3784 pileup_text rows 3784 differing 0 crashed=None examples []
cg_legal [-B] samtools rows 3784 pileup_text rows 3784 differing 0 crashed=None examples []
cg_legal [-E] samtools rows 3784 pileup_text rows 3784 differing 0 crashed=None examples []
cg_legal [-q 20 -Q 20 -x -A] samtools rows 3778 pileup_text rows 3778 differing 0 crashed=None examples []
cg_legal [--ff 0 -Q 0 -B] samtools rows 3784 pileup_text rows 3784 differing 0 crashed=None examples []
--- wild templates (per template, all option sets; INFO only, not scored against the Skill) ---
INFO wild template MD       --ff 0 -Q 0 -B: 0/14 rows differ, CRASH IndexError: array index out of range (after 14 rows)
INFO wild template MPIM     default: 288/3505 rows differ | -B: 405/3505 rows differ | -E: 288/3505 rows differ | -q 20 -Q 20 -x -A: 148/3416 rows differ | --ff 0 -Q 0 -B: 462/3505 rows differ
INFO wild template MID      --ff 0 -Q 0 -B: 0/14 rows differ, CRASH IndexError: array index out of range (after 14 rows)
```
Legal templates: M, =/X runs, I, D, N, I-D, D-I, N-I, I-N, D-N, N-D, adjacent identical ops (II, DD, NN), S/H flanks, S+M+X+I. Wild templates are outside what an aligner emits and are informational.

### Input 8 -- find_variants, restored print, dedup (`12_find_variants_access.py`, `14_usage_guide_dedup.py`)
```
find_variants: [(120, 'T', 'C', 20, 8), (520, 'A', 'G', 17, 2), (620, 'T', 'C', 20, 2), (720, 'A', 'G', 20, 10), (820, 'C', 'T', 20, 10), (821, 'C', 'T', 20, 10), (1000, 'T', 'C', 20, 5), (1150, 'G', 'A', 20, 10)]
decode of mpileup: [(120, 'T', 'C', 20, 8), (520, 'A', 'G', 17, 2), (620, 'T', 'C', 20, 2), (720, 'A', 'G', 20, 10), (820, 'C', 'T', 20, 10), (821, 'C', 'T', 20, 10), (1000, 'T', 'C', 20, 5), (1150, 'G', 'A', 20, 10)]
by hand: [(120, 'T', 'C', 20, 8), (520, 'A', 'G', 17, 2), (620, 'T', 'C', 20, 2), (720, 'A', 'G', 20, 10), (820, 'C', 'T', 20, 10), (821, 'C', 'T', 20, 10), (1000, 'T', 'C', 20, 5), (1150, 'G', 'A', 20, 10)]
bcftools call positions: [120, 220, 720, 820, 821, 1150, 1250]
allele_counts pv1:420 {'G': 17, 'N': 3} | pv1:120 {'T': 12, 'C': 8} | pv1:1250 {'A': 20}
NOTE allele_counts at 420 counts the read-base N as an allele: {'G': 17, 'N': 3} | allele_frequency: {'G': 0.85, 'N': 0.15}
real sarscov2 PE find_variants(min_depth=2, min_alt_freq=0.3): 3 [{'chrom': 'MT192765.1', 'pos': 5700, 'ref': 'T', 'alt': 'C', 'depth': 3, 'alt_count': 1, 'freq': 0.3333333333333333}, {'chrom': 'MT192765.1', 'pos': 17275, 'ref': 'A', 'alt': 'C', 'depth': 3, 'alt_count': 1, 'freq': 0.3333333333333333}]
Access Reads at MT192765.1:5700: snippet 3 reads, samtools 3; first line: Position: 5699
1000G find_variants: 119 decode: 119 [{'chrom': 'chr20', 'pos': 1400552, 'ref': 'T', 'alt': 'G', 'depth': 12, 'alt_count': 7, 'freq': 0.5833333333333334}, {'chrom': 'chr20', 'pos': 1401214, 'ref': 'G', 'alt': 'A', 'depth': 14, 'alt_count': 9, 'freq': 0.6428571428571429}]
reference-N pileup rows in chr20:1400001-1400200 of the real slice: 0
```
```
old guide 8351 bytes; new guide 1523 bytes; SKILL.md 24579 bytes
new guide mentions: ['SKILL.md', 'SKILL.md']
```
### Informational (not scored against the Skill)
- `13_probe_seq_star_and_related.py`: a secondary alignment with SEQ `*` is skipped by samtools even with `--ff 0`, and the helpers agree (no crash); all six Related Skills paths exist in the fork.
- pysam 0.24.1 documents `all` as the default stepper in its docstring but the code default is `samtools` (probe 6).

## Final report

```
Skill: bio-pileup-generation @ 5fc1304  |  Category: Data Analysis  |  Mode D  |  Moderate (N=8)
Static 80/100 x 0.4 = 32.0   Dynamic 87.6 x 0.6 = 52.6   FINAL 85  ->  ⭐ Production Ready   deployable: yes   vetoes: none
Assertions 37/40; L1 avg 34.6/40, L2 avg 53.0/60; Production-Ready floors met (static >= 80, exec >= 85, L1 >= 32, L2 >= 48, assertions >= 90%)
Previous re-audit 84 Limited Release -> now 85 Production Ready; pre-fix 71 Beta Only.
```

Key strengths
- Round 2 delivered what it claimed on the helpers: `indel_text` makes `pileup_text` identical to `samtools mpileup` on 3,784 legal-CIGAR rows x 5 option sets (adjacent I/D, D-I, I-D-I, N beside indels, =/X runs, indels next to S/H), `find_variants` returns exactly the 8 hand-planted SNVs with reference-N and read-N handled, and the Access Reads print is back
- The `--rf` / `flag_require` / bcftools `--lu` `--nu` row is now exactly right and checked against independent pysam subsets on 6 masks (any-bit vs all-bit)
- Every default that silently changes output is tabled with a samtools/bcftools column (-Q 13/1, --ff four flags, -d 8000/250, orphans, overlaps, BAQ) and the depth-cap, reference-mismatch (exit 0, N rows) and wrong-pipe traps are real and correctly worded
- The usage-guide dedup lost nothing an agent needs: 14 old sections map to SKILL.md content, and the dropped items ('No sequences in common' text, `mpileup -g` prompt, `-d 500` advice) were wrong on samtools 1.24 or contradict the measured depth-cap trap

Optimization recommendations

**[P1] Round 2 introduced a false statement: BAQ 'under either stepper'; 'all' is the default**  
Observed in: [7]  
Problem: SKILL.md says fastafile switches BAQ on 'under either stepper (`'all'`, the default, or `'samtools'`)' and the table row for `-f` says 'either stepper'. pysam 0.24.1's default stepper is 'samtools'; with an explicit stepper='all' (or 'nofilter') fastafile applies NO BAQ (538/538 BAQ positions on the own single-end BAM, 49/49 on real SE data; identical qualities with and without fastafile), and 'all' also skips overlap removal and the orphan filter (281 human-BAM positions differ from `-B`), so the `-x`/`-A` 'default matches' rows only hold for the default stepper. Round 1's wording (stepper='samtools' + fastafile) was correct; the fix log's 'either stepper' verification called the no-argument call 'all'.  
Root cause: The round-2 harness passed no stepper argument for its 'all' rows, so both rows exercised the default 'samtools' stepper.  
Fix: Rewrite the paragraph and table row: 'pysam's default stepper is `samtools`. With it, `fastafile=` switches BAQ on and `ignore_overlaps` / `ignore_orphans` / `min_base_quality` apply; with `stepper='all'` or `'nofilter'` neither BAQ nor overlap/orphan handling is applied, so do not pass them when matching mpileup.' Drop 'either stepper' and '`'all'`, the default'.

**[P2] allele_counts counts read-base N as an allele; find_variants drops it**  
Observed in: [8]  
Problem: At a site with 3 read-base N in 20 reads, allele_counts returns {'G': 17, 'N': 3} and allele_frequency divides by 20, while find_variants (round 2) drops N from alleles and depth; the docstrings do not say so.  
Root cause: The N fix was applied to find_variants only.  
Fix: Skip base 'N' in allele_counts as well (or state 'N is counted as its own allele' in its docstring) so the two helpers agree.

**[P2] pileup_text scope: P-op CIGARs differ and a CIGAR ending in D crashes under -Q 0**  
Observed in: [6]  
Problem: Templates with a P (padding) op differ from samtools in 148-462 rows (samtools prints '+3*AC'); a read whose CIGAR ends in a deletion makes pileup_text raise IndexError when run with min_base_quality=0 / flag_filter=0.  
Root cause: indel_text ignores op 6, and query_position_or_next is out of range after a trailing D.  
Fix: One docstring sentence: 'aligner-legal CIGARs only (no P ops, no trailing D)', or guard the quality lookup.

**[P2] SKILL.md is 24.6 KB with all helper code inline**  
Observed in: []  
Problem: The single file grew from 14.8 KB to 24.6 KB (479 lines); the ~150 lines of pysam helpers are loaded on every invocation, and only one of them ships as a runnable example.  
Root cause: The dedup moved usage-guide code into SKILL.md instead of into examples/.  
Fix: Move allele_counts / find_variants / pileup_text into examples/ (with a small self-test) and keep the table and one-line usage in SKILL.md.

> The score sits on the 85 boundary (84.6 rounded). Input 7 carries the P1: had round 2 kept the round-1 wording that paragraph would be clean. The grade is not a statement that the Skill is error-free; a round 3 that rewrites one paragraph and one table row closes the only open P1.

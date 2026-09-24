# Fix log: bio-pileup-generation (alignment-files/pileup-generation)

## 2026-09-20

Fixer: fresh Sonnet. Branch `fix/af-pileup` (worktree `F:\OpenScience\wt\af-pileup`), commit `ad9b5a4`, from staging `ed0ff44`.
First audit: 71, Beta Only, not deployable, no veto/P0 (12 recommendations: 6 P1, 6 P2). A different agent re-audits.

Tools: samtools 1.24, bcftools 1.24, pysam 0.24.1 (WSL `science`, env `alignment-files`). Verification harness (not shipped):
`F:\OpenScience\af-pileup-scratch\final_test.py` (150/150 assertions passed from a clean copy of the Skill folder; log `final_test_saved.log`).
Data: real human chr22 slice BAM, RNA-seq spliced BAM, 1000G HG00349 chr20 BAM, ARTIC nanopore BAM, plus the audit's synthetic
truth BAMs (planted SNP, 2 bp insertion, 3 bp deletion, splice, overlapping mates, orphans, flags, 9000x depth, 11 contigs, 2 samples).
Every claim below was checked against the second method: independent decode of `samtools mpileup` text vs pysam, or hand counts from `truth.json`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| pysam examples print `pileup_column.n` as depth (differs at 1087/1157 real positions) | P1 | All pysam blocks print `len(pileup_column.pileups)`. New table maps each mpileup option to its pysam argument (`stepper='samtools'` + `fastafile` for BAQ, `min_base_quality`, `min_mapping_quality`, `max_depth`, `ignore_overlaps`, `ignore_orphans`, `flag_filter`, `flag_require`, `redo_baq`, `adjust_capq_threshold`). States that pysam defaults equal `mpileup -B`, and that `stepper='all'` + fastafile does not apply BAQ | ran: 9 table rows x 4 datasets (human, RNA, synthetic, 1000G), depth AND base counts equal position by position; `len(pileups)` == mpileup at all positions and `n` differs at exactly 1087 of 1157 | `stepper='nofilter'` is not `--ff 0` (it also drops the orphan filter): use `flag_filter=0` |
| pysam `max_depth=0` (found while matching -d) | P1 (new) | Documented: `max_depth=0` is NOT unlimited (stays 8000); pass a large number | ran: 9000x BAM: default 8000, `max_depth=0` 8000, `1000000` 9000 == `mpileup -d 0` | not in the audit report |
| Ref-skips counted as `DEL` in every pysam helper | P1 | `is_refskip` tested before `is_del` in `allele_counts`, Access Reads snippet, `find_variants`, `pileup_text`, `examples/allele_counts.py`; the rule and the reason (pysam sets `is_del` on N skips) are stated once in the pysam section | ran: synthetic splice synA:400 -> `{}` (was `{'DEL': 3}`), 3 "Reference skip" lines; real RNA-seq intron chr22:25548 -> `{'G': 5}` (was DEL 54), mpileup shows 0 `*` and 54 `>`/`<`; true deletion synA:252 still DEL 4 | |
| `pileup_text` is not a pileup (no `^ $ +N -N`, no qualities, disagrees with own depth) | P1 | Rewritten to emit the 6-column mpileup format: `^`+MAPQ, `$`, `+2AC`/`-3CGT`, `>`/`<`/`*`, quality column (capped at `~` like samtools), depth `len(pileups)`, `* *` for depth 0; takes `**pileup_kw` | ran: row-for-row equality with `samtools mpileup` for default, `-B`, and `-q 20 -Q 20 -x -A` on 5 real/synthetic BAMs (human, RNA, synthetic, ARTIC, 1000G): 0 differing rows in 15 comparisons; hand counts `+2AC` x3 `+2ac` x2 at synA:200, `-3CGT` x2 `-3cgt` x2 at synA:250 (-B) | first draft differed on 6 RNA-seq rows only because samtools caps printed quality at `~` (93); fixed |
| Defaults that change the output are undocumented (-Q 13, excluded flags, depth-0 rows, BAQ hiding deletions) | P1 | "Pileup Options and Defaults" table now has a Default (samtools / bcftools) column: `-q 0/0`, `-Q 13/1`, `--ff`/`--ns` UNMAP,SECONDARY,QCFAIL,DUP, `--rf`/`--nu`, `-d 8000/250`, orphans dropped, overlaps counted once, BAQ. BAQ section states that in a text pileup BAQ hides a deletion (depth 8 -> 4, no `-3CGT`; `-B` restores). Output Format section documents depth-0 `* *` rows and 3+3N columns | ran + help: `samtools mpileup`/`bcftools mpileup` help text checked for every default; synA:725 depth 4 (default) vs 10 (`-Q 0`); synA:825 depth 10 vs 16 (`--ff 0`, bcftools `--ns 0` DP 16); 1000G 101 duplicate-flagged reads change depth sum; synA:250 depth 4 no marker vs 8 with markers; chr22:1952-1954 print `0 * *` | |
| False reason for the "WRONG" `samtools mpileup \| bcftools call` | P1 | Comment rewritten: text pileup is not VCF/BCF; error text and exit status given; `bcftools mpileup` named as the route. Sentence added after the tool table. Also `pysam` max_depth trap added to the same section | ran: `Failed to read from standard input: unknown file type`, exit 255 (with pipefail); `samtools mpileup -g` -> `invalid option -- 'g'` | Correct guidance re-derived from behaviour: bcftools call has no depth cap of its own, so the double-cap rationale was false |
| Parallel-by-chromosome `bcftools concat chr*.vcf.gz` puts contigs out of header order; failures swallowed | P1 | Block moved into SKILL.md ("Parallel by Contig") and rewritten: contig list from `samtools idxstats`, `xargs -P 4` with `pipefail`, `bcftools concat -f` in list order, `&&` so a failed contig stops the merge; note to keep to primary contigs (`:`/`*` names break `-r`) | ran on the 11-contig BAM: output contig order == header order chr1..chr11 (glob order would be chr1,chr10,chr11,chr2...), 11 records, index built; with a nonexistent reference: non-zero exit, no `all.vcf.gz` | |
| Reference mismatch exits 0 with N rows; quoted error texts wrong | P1 | Common Errors rewritten with real messages: `[E::faidx_adjust_position] The sequence "X" was not found` + exit 0 + `N` rows, contig pre-check (`@SQ` vs `.fai`); `No FASTA reference` row replaced (samtools without `-f` succeeds with `N`; bcftools refuses: "requires the --fasta-ref option"); `[E::mpileup] fail to parse region`, `[E::idx_find_and_load] Could not retrieve index file`; removed "No sequences in common" and "Reference mismatch" | ran: ARTIC BAM + wrong FASTA: rc 0, N rows, message names the contig; no `-f`: rc 0 N; bcftools no `-f` message; `-r 22:...` message; unindexed BAM message | |
| Cheat-sheet exome `-d 250` / usage-guide `-d 500` contradict the depth trap | P2 | Exome row `-d 0`; usage-guide memory advice removed (SKILL.md Common Errors says a cap must be set well above expected coverage). Multi-sample example `-d 250` -> `-d 100000` | ran: 9000x BAM `-d 250` -> 250, `-d 0` -> 9000; cheat-sheet rows all run | `-d 1000000` with 2 samples prints bcftools "Potential memory hog" warning (found by running the joint block), hence `100000` and a note |
| Basic Pileup prints out-of-region columns; 0/1-based ambiguity | P2 | `truncate=True` added, printed positions are 1-based, docstrings say "0-based pos: pass 1-based minus 1", call examples use `1000000 - 1` | ran: Basic Pileup snippet gives exactly the 11 requested columns with mpileup -B depths; `allele_counts(..., 100)` documented as the neighbour base | |
| Shipped example fails with raw tracebacks | P2 | `examples/allele_counts.py`: `rpartition(':')` (contig names with `:`), commas stripped, one-line `Error:` for ranges, missing colon, position < 1, unknown contig, unindexed BAM; refskip fix; header now "checked on" | ran from a clean copy: synA:100 -> T 30 / C 10; real chr22:3000 depth == mpileup -B -q20 -Q20; `HLA-A*01:01:01:01:100` contig; `synA:1,000`; 5 error cases: rc 1, one line, no traceback | |
| Unverified/overstated statements | P2 | Removed "~30% slower"; BAQ row no longer says "from CIGAR if MD missing" (says: computed against the reference, existing BQ tag reused; `-E` ignores it; `-B` and `-E` cannot combine); `-a` vs `-aa` corrected (identical for one contig; ARTIC 29903 rows either way); format examples replaced with real 1000G rows; symbol table shows `+2AC`/`-3CGT`, `^]` = MAPQ 60, `$`, `#`; "6 columns per sample" -> 3 + 3N | ran: 1000G example rows equal real output; two BAMs -> 9 columns; ARTIC `-aa` and `-a` both 29903 rows; `-a`/`-aa` row counts on synthetic; `-B -E` rejected | BAQ slowdown was measured at 2.5-2.8x by the audit; no number kept because it depends on data |
| Indels invisible in pysam counters; prompts steer to removed `-g` | P2 | Chose "state scope": `allele_counts`/`find_variants` docstrings say SNVs only, indels via `pileup_read.indel` (shown in `pileup_text`) or `bcftools mpileup`. Two usage-guide prompts reworded to `bcftools mpileup` | ran: synA:200 counts A x10 (insertion not counted, documented); `pileup_text` reports `+2AC`; bcftools block calls ins and del | not extended to counting indel alleles: no claim required it |
| SKILL.md / usage-guide.md duplication | P2 | See "Deleted passages" | see below | |

## Missing referenced executables

Checked SKILL.md and usage-guide.md for tools named without code. The tool table names DeepVariant, HaplotypeCaller, Mutect2, VarDict, VarScan2, clair3, Sniffles, cuteSV, Strelka2, fgbio: these are tool-choice pointers ("use X instead of mpileup"), not workflows the Skill claims to run, and are outside its scope, so no runnable block was written and the claims were left as pointers. `pileup_text`, `find_variants`, the parallel loop and the BCF intermediate were already referenced with code; all now run.

## Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| usage-guide "Prerequisites" (conda/pip/faidx) | SKILL.md Version Compatibility |
| usage-guide "Understanding Pileup Format" tables | SKILL.md Output Format + Read Bases Encoding (improved) |
| usage-guide "Common Commands" (basic, quality, region/BED) | SKILL.md Basic/Region/BED/Quality Filtering sections |
| usage-guide "Variant Calling Pipeline": single-sample, multi-sample | SKILL.md Modern Germline Calling, Multi-Sample Joint Calling |
| usage-guide BCF intermediate | SKILL.md "BCF Intermediate" |
| usage-guide "Performance Options" (`-d 1000`, parallel loop) | `-d 1000` dropped (contradicted the depth trap, see P2); parallel loop moved and fixed: SKILL.md "Parallel by Contig" |
| usage-guide pysam "Basic Pileup Iteration", "Count Alleles", "Access Individual Reads" | SKILL.md Basic Pileup, Count Alleles (`allele_counts` takes `**pileup_kw`, replaces `count_alleles(min_qual)`), Access Reads at Position (the guide's read-name/strand print variant dropped) |
| usage-guide `find_variants` | SKILL.md "Find Variants in a Region" (fixed, `**pileup_kw`) |
| usage-guide Troubleshooting ("No sequences in common", empty output, memory, slow) | SKILL.md Common Errors (real messages) and Output Format/Options table; "slow": BCF/parallel/`-l` in Parallel by Contig, BED section, Common Errors |
| usage-guide Tips | quality filtering: cheat sheet; BCF faster / text for debugging: Common Errors footer; `truncate=True`, 0-based: pysam section; multi-sample preferred: Joint Calling; limit `-d`: Maximum Depth trap (the unconditional "limit max depth" advice was contradicted by the audit and not kept) |
| SKILL.md "Quick Reference" table (4 commands, all stated earlier) | earlier command sections |
| SKILL.md standalone `-A` and `-a`/`-aa` paragraphs; `-g` table row | Pileup Options and Defaults table rows (`-g` in the Deprecation section) |
| SKILL.md `allele_frequency` counting loop | `allele_frequency` now calls `allele_counts` |

Disagreement logged: multi-sample `-d 250` (SKILL) vs `-d 1000000` (guide) resolved to `-d 100000` because the run showed the memory warning at 1000000 with 2 samples.

## Unfixed

None of the audit's 12 recommendations is left open. Not done on purpose: no indel allele counting in the pysam helpers (scope stated instead, allowed by the report's fix text); DeepVariant/HaplotypeCaller/etc. pointers left without code (see above).

## Round 2 (2026-09-20)

Fixer: fresh Sonnet. Branch `fix/af-pileup`, new commit `5fc1304` on top of round 1 (`ad9b5a4`). Evidence: the re-audit (84, Limited Release, deployable; 223/230 checks; 1 P1 + 5 P2). A different agent re-audits again.
Tools: samtools 1.24, bcftools 1.24, pysam 0.24.1 (WSL `science`, env `alignment-files`). Harness (not shipped): `F:\OpenScience\af-pileup-scratch\r2\r2_test.py`, run against a clean copy of the Skill folder: 72/72 assertions; the round-1 `final_test.py` rerun on the same copy: 150/150 (no regression). Data: the round-1 BAMs plus the re-audit's `new.bam`, `fz_clean.bam`, `fz_exotic.bam` (copied, read-only source), a BQ-tagged copy of the human BAM, and a planted adjacent-indel BAM built here.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| "`stepper='all'` + fastafile applies no BAQ" is false | P1 | BAQ follows `fastafile` under either stepper. Table rows: `-f` = `fastafile=`; `-B` = no fastafile or `compute_baq=False`; `-E` = `fastafile` + `redo_baq=True`. `stepper='samtools'` is no longer required | ran: 15 mappings x 6 BAMs (human DNA, RNA-seq, 1000G, ARTIC, 2 synthetic) + a BQ-tagged BAM, depth AND base counts equal to `samtools mpileup` at every position, both steppers. Discriminating: default vs `-B` differ at 40 human positions (pysam with fastafile matches default at all, `compute_baq=False` matches `-B` at all); synA:250 depth 4 vs 8; on the BQ-tagged BAM default == `-B` but `-E` differs at 42 positions and `redo_baq=True` matches `-E` | round 1 had verified `stepper='samtools'` and never the negative it asserted |
| `--rf` equated with bcftools `--nu` | P2 | Row is `--rf` (bcftools `--lu`) = any of the bits; adds that `--nu` requires ALL bits. pysam `flag_require` noted as any-bit | ran, masks 65 and 99: bcftools `--nu` depth == bcftools on the `samtools view -f MASK` subset (335172, 166362); `--lu` == unfiltered (354005); pysam `flag_require` == `samtools --rf` (353982); help text of bcftools 1.24 (`--lu` skip-all-unset, `--nu` skip-any-unset) | samtools vs bcftools totals differ by 23 for unrelated reasons; every comparison is within one tool |
| `pileup_text` loses the second marker next to another indel | P2 | Fixed, not only documented: new `indel_text()` derives `+N`/`-N` markers from the CIGAR (adjacent identical ops merged, as samtools does); works after M, D and N bases (`*+2GT`, `<+2ag`) | ran: planted BAM (`10M2I2D10M`, `10M2D2I10M`, `10M20N2I10M`, `10M2I20N10M`, `10M1I2I10M`, `10M1D2D10M`, both strands): 300 rows equal `samtools mpileup` default and `-B`, and the expected `+2CA-2GC` / `+2ca-2gc` / `*+2GT` built from the construction; random CIGARs: 4,486 clean rows and 4,470 exotic rows, 0 differing (was 244 exotic rows); 6 real/synthetic BAMs default and `-B`, 0 differing | `pileup_read.indel` holds only one event, so the fix does not use it |
| `find_variants` reports N | P2 | Skips reference-N positions; read-base N is not counted (nor in the depth) | ran: `new.bam` returns exactly the 3 planted SNVs (620 T>C, 730 G>A, 920 G>A); the round-1 code on the same call also returns 790 G>N and 800-805 N>A; `bcftools call` lists 730 G>A; `syn.bam` still finds synA:100 T>C 10/40 | |
| Dedup dropped read-name/strand print | P2 | Restored: Access Reads snippet prints `query_name`, strand, base, quality (agents need "which reads carry the alt allele"). One sentence in SKILL.md points to `examples/allele_counts.py` | ran: snippet output at synA:100 == the (QNAME, strand) set of `samtools mpileup --output-extra QNAME,FLAG` (40 reads); example runs from the clean copy (T 30 / C 10; range input gives the one-line Error) | |
| Soft-masked FASTA prints lower-case reference | P2 | Output Format column 3 says so | ran: `samtools mpileup` prints 424 lower-case reference rows on the soft-masked fuzz reference; `pileup_text` equals it row for row | |

Redundancy (this pass): pysam table `--ff` row no longer repeats the four default flags (says 1796 = the same four); `-d` row and the Maximum Depth comment point to each other and to the options table instead of repeating the `max_depth=0` fact and both default numbers; example header says pysam has no BAQ only without a fastafile. Nothing deleted from the agent's reach.

Unfixed: none of the 6 re-audit findings is open. Not done: `stepper='nofilter'` and `pileup_read.indel` remain as described in round 1.

## 2026-09-24 (final pass: Codex)

Final-pass source commit: `3eac20f00989e1b287984d13e92c59e7ff5c86a2`, branch
`agent/finalpass-bio-pileup-generation-20260924`, based on staging
`2812e22`. The final audit is same-agent by design (`auditor_independent:
false`), reports 95/100 Production Ready, and cites that exact commit.

| Finding | Priority | Change | Verified |
| --- | --- | --- | --- |
| `allele_counts` included read-base `N` while `find_variants` excluded it | P2 | Moved shared functions to `examples/pileup_helpers.py`; `allele_counts` now skips read-base `N`, so `allele_frequency` and `find_variants` use compatible non-N denominators. `examples/allele_counts.py` imports the shared function. | Fresh planted site: `{'G': 17}`, no `N`; frequencies sum to 1.0. Archived planted-SNV and CLI routes still pass. |
| `pileup_text` crashed on a deletion after the read's final base with `-Q 0` | P2 | Render the samtools Q0 deletion quality (`!`) when no next query quality exists. | Fresh `14M3D` fixture: 3,187 rows exactly equal `samtools mpileup --ff 0 -Q 0 -B`, with no `IndexError`. |
| Padded (`P`) CIGARs were silently rendered differently from samtools | P2 | The helper states its ordinary-aligner-CIGAR scope and raises a named `ValueError` for padding instead of emitting incorrect pileup text. | Fresh padded-CIGAR fixture gets an actionable padding error. |
| Large inline helpers inflated `SKILL.md` | P2 | Moved reusable helpers into one importable module and added `examples/self_test.py`, which builds an isolated temporary FASTA/BAM and tests counts, frequencies, SNVs, and text rows. | Main guide reduced to 361 lines; shipped self-test and CLI execute successfully. |

Regression evidence: every archived input reran from an audit-owned copy of
the exact source: inputs 1--7 passed 28/28, 28/28, 41/41, 21/21, 28/28, 56/56,
and 28/28 checks. Fresh final-pass checks also passed 14/14. Toolchain: WSL
`science` `alignment-files` environment, samtools/htslib 1.24, bcftools 1.24,
pysam 0.24.1, Python 3.12.14.

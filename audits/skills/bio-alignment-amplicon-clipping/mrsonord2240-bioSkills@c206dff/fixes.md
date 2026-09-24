# Fix log: bio-alignment-amplicon-clipping

## 2026-09-20 (fixer, branch `fix/af-ampclip`, from staging c206dff)

First audit: 68, Beta Only, not deployable, 5 P1 + 2 P2, no veto. Fixed 7/7 recommendations.
Tools checked on: samtools 1.24, pysam 0.24.1, iVar 1.4.4, bcftools 1.24 (WSL env `alignment-files`), real ARTIC v5.3.2 nanopore BAM + BED + MN908947.3 FASTA, audit synthetic data. Every changed example was run from a clean copy of the Skill folder.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| Example exits 0 on contig mismatch and wrong reference | P1 | `ampliconclip_workflow.sh`: contig intersection of BAM `@SQ`, BED col 1, FASTA `.fai` (stop on none / missing); BED >= 6 columns when `--strand`; `-f` stats file and `TOTAL CLIPPED > 0` assert; calmd stderr no longer discarded; MD-present assert; residual-primer check via new `check_primer_residual.py`; SKILL.md workflow gets step 0 (contig check) and step 4 (verify) | ran: Illumina BAM + ARTIC BED rc=1 "no contig shared"; wrong FASTA rc=1; wrong FASTA with the pre-check deleted rc=1 "calmd wrote no MD tags"; 5-col BED rc=1; real ARTIC rc=0, MD 4916/4916, residual 0/0; synthetic PE rc=0. SKILL workflow block extracted and run: rc=0 | Second method for residuals: pysam + BED, independent of samtools. Example default is now `--both-ends --strand` (was `--both-ends`) |
| "`--both-ends` overrides `--strand`" false; "forgot `--strand`" diagnosis inverted | P1 | Removed the claim everywhere; new "Choosing the Clip Mode" with 4-mode table (measured on ARTIC) and 4-case table (synthetic single reads); Common Errors rows rewritten | ran: 5 modes on real ARTIC (residual 3' 97.5/97.5/0/0%), 8 synthetic reads x 4 flag sets, outcomes match the table | `--strand` restricts which BED strand may clip each end also with `--both-ends`; omitting it over-clips |
| ARTIC/long-read `--strand` leaves 3' primer in 97.5% of reads | P1 | Rule changed from "<300 bp" to "the read can reach the opposite primer"; Quick Reference, example default and Decision text use `--both-ends --strand`; `--strand` alone limited to reads that never reach the opposite primer | ran: real ARTIC `--strand` 4793/4916 3' residual; `--both-ends --strand` 0; synthetic 80-bp-amplicon PE with `--strand` alone: 200/800 3' residual, with `--both-ends --strand` 0 | Long-read claim measured on ONT only; PacBio HiFi not tested (stated as "long reads (measured)" only for the ONT number) |
| BED example 5-column, `--strand` needs col 6 | P1 | 6-column example; text says 5 columns fail with the exact message; ARTIC 7-column accepted | ran: 6-col parses (TOTAL CLIPPED: 0 on unrelated contig, no error); 5-col "Parsed 5 columns, but need at least 6"; 7-col ARTIC BED used throughout | |
| fgbio ClipBam listed as primer trimmer | P1 | Row removed from Tool Selection and the header alternatives; one-line note that ClipBam takes no primer file. BAMClipper (no runnable code, not installed, BEDPE primers) deleted per "Missing referenced executables". iVar trim, which the Skill named with no command, now has a runnable block | ran: iVar block on ARTIC BAM (4909 reads out, 4701 identical to `ampliconclip --both-ends --strand --clipped`, residual 5' 1.9% / 3' 1.6%, defaults write 0 reads) | ClipBam "no primer option" from the audit's `--help` check (0 of 101 lines), not re-run |
| Raw output unsorted; unclipped reads; `--clipped/--tolerance/--primer-counts`; MD/NM removed not stale | P2 | Sort-before-index note, Common Errors row, "Other options" list, After Clipping table says MD/NM removed by default, `--keep-tag` keeps them | ran: `samtools index` on raw output "Unsorted positions"; header `SO:unknown`; tags: input NM 4916, raw output NM 82 (clipped reads lose it), `--keep-tag` NM 4916; `--clipped` 4909; `--fail` 7 QCFAIL; `--original` OA on 4909; `--primer-counts` bedgraph written | `--tolerance 0/5/20` gave identical NOT CLIPPED (7) on ARTIC; documented only as the flag's meaning |
| usage-guide repeats SKILL.md; `-aa` pointer invalid for bcftools | P2 | usage-guide cut to overview, prompts, pointers; pointer names `samtools mpileup` and gives the bcftools equivalents | ran: `samtools mpileup -aa -A -d 600000 -B` ok; `bcftools mpileup -aa` "Could not parse tag"; `bcftools mpileup --max-depth 600000 -a FORMAT/AD,FORMAT/DP -B` ok | |
| (found while fixing) "BAQ in bcftools mpileup depends on MD" | P2 | Removed from workflow text, Decision/Tips, After Clipping; replaced by what actually reads MD/NM (IGV, NM filters) | ran: `bcftools mpileup` VCF body identical (md5) with and without MD, with and without `-B`, 32,150 records | Contradicted by run, so removed |

## Deleted passages and where the content lives

| deleted | now |
| --- | --- |
| usage-guide Prerequisites (samtools >= 1.11, sorted indexed BAM, BED strand col 6, conda install) | one-line summary in usage-guide; install in SKILL.md Version Compatibility, BED in Primer BED Format |
| usage-guide Quick Start prompts | merged into Example Prompts |
| usage-guide "What the Agent Will Do" (inspect BAM, locate BED, run clip, fixmate/calmd, region check) | SKILL.md Basic ampliconclip Workflow (Approach + steps 0-4) |
| usage-guide Decision Points (soft vs hard, `--strand`, `--both-ends`, re-calmd) | SKILL.md Soft-Clip vs Hard-Clip, Choosing the Clip Mode, After Clipping. The two `--both-ends` sentences were wrong and are gone |
| usage-guide Tips: markdup, UMI panels (Twist/IDT/AVENIO), samtools consensus | SKILL.md Why Not Markdup (panel names added), SARS-CoV-2 ARTIC Comparison note |
| usage-guide Tips: "strand bias ... forgot `--strand`", "BAQ may be wrong (MD stale)", long-read "verify CIGAR semantics" | deleted (first two contradicted by runs); long-read guidance replaced by the measured Choosing the Clip Mode rule and the residual check |
| usage-guide Related Skills | SKILL.md Related Skills (usage-guide points at it) |
| SKILL.md "Strand-Aware Clipping" and "Both-End Clipping" sections | SKILL.md Choosing the Clip Mode |
| SKILL.md Tool Selection rows BAMClipper, fgbio ClipBam; header alternatives list | deleted / one-line ClipBam note; iVar trim kept with a command |
| SKILL.md Common Errors "Forgot `--strand`" row | rewritten rows (over-clipping without `--strand`; primer bases remain) |
| example script comment "--both-ends overrides --strand" | comment on `CLIP_OPTS` modes |

## Findings left unfixed

None of the audit's recommendations. Not exercised: BAMClipper (deleted, not installed); PacBio HiFi 16S (only mentioned generically; ONT measured); `--tolerance` effect (no difference on the ARTIC data, stated as flag semantics only).

## 2026-09-24 (final pass, branch `root/fix-bio-alignment-amplicon-clipping`)

Completed the outstanding final-pass remediation and audited the exact resulting source commit `c48efba95387158281f21abe97ecb48b8407ac44` (following the hardening commit `968e76c3a46383a495cbee10f2b65f25cca60a56`).

| finding | priority | change | verified |
| --- | --- | --- | --- |
| Wrong or sparse primer schemes could look successful | P1 | Workflow now derives `NOT CLIPPED / TOTAL READS`, enforces `MAX_NOT_CLIPPED_PCT` (default 1%), and keeps output inside the temporary directory until every check passes | ARTIC v3, v5 shifted +9 bp, and v3 strand-only each fail at 90.419%, 2.482%, and 95.443%; matching v5 succeeds (7/4916 not clipped) |
| BED/header parsing, residual-check contract, and late failures were ambiguous | P2 | Normalizes whitespace, UCSC headers, and CRLF; makes pysam mandatory; checker returns 2 for bad input; final BAM is atomically published only after validation | Space, track/browser, comment, blank, and CRLF BEDs pass; malformed 5-column BED returns actionable error/exit 2; failed cases leave no final BAM |
| Minor stale claims | P2 | Corrected BAQ/MD script wording and iVar/tolerance guidance | Re-ran command/pointer checks and MD-vs-no-MD bcftools comparisons |

Final audit: **95/100, Production Ready, deployable**, 7/7 inputs executed, 28/28 assertions passed, all structural and research vetoes pass, no open P0/P1/P2 recommendations. Inputs 1–5 re-ran archived logical regressions; inputs 6–7 were fresh synthetic HiFi and wrong-scheme/checker cases. Evidence: `F:\OpenScience\audits\bio-alignment-amplicon-clipping\eval_report_bio-alignment-amplicon-clipping_result.json` and its viewer. `auditor_independent: false`; final-pass note is present.

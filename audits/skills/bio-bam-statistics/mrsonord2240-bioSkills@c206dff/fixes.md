# bio-bam-statistics fix log — 2026-09-20

Skill `alignment-files/bam-statistics`, branch `fix/af-bamstat` (from staging main 85a3e4d), fixer pass after first audit (71, Beta Only, not deployable, no veto/P0).
Tools (WSL `science`, env `alignment-files`): samtools 1.24, htslib 1.24, bcftools 1.24, pysam 0.24.1, mosdepth 0.3.14, Picard 3.5.0 (side env), MultiQC 1.35, VerifyBamID2 2.0.3, somalier 0.3.5, plot-bamstats/gnuplot from the env.
Scratch (not in any repo): `F:\OpenScience\af-bamstat-scratch\` (`snip_test.py` runs every SKILL.md fenced block from the worktree file and asserts on output; `qc_check.py` compares `qc_report.py` with `samtools flagstat -O tsv` on 14 BAMs).

Independent checks used: per-base depth rebuilt from `read.get_blocks()` with numpy (no pileup engine); `samtools depth -a`; `mosdepth` (`--fast-mode` when double-counting mates is expected); flagstat TSV; hand counts of flags with pysam; CIGAR walk with pysam `cigartuples`.

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| 1 Mean-depth and >=Nx recipes divide by covered positions (568x vs 16.8x; 79.3% vs 2.34%) | P1 | Replaced awk one-liners (SKILL.md Quick Reference, usage-guide) with one `samtools depth -aa \| awk` recipe with `n` = every reference position, empty-input guard; Quick Reference "Mean depth" now points at `samtools coverage` / that recipe; explicit warning about raw `depth` output | ran: mean 16.77x, >=10x 2.43%, >=20x 2.34% on human BAM; 68.84x ARTIC; 1000.00x planted stack; all equal to the get_blocks() truth string-for-string; old recipe reproduces 568.153 | `-a` alone omits contigs with no reads; `-aa` documented |
| 1b pysam `mean_depth()` 579.7 (columns only) and `coverage_stats()` (lost orphan positions, capped) | P1 | Both plus usage-guide `region_coverage` replaced by one `region_depth_stats()` dividing by region length, `truncate=True`, `max_depth=1_000_000`, `ignore_orphans=False`, `min_base_quality=0`, real bases only (deletions/refskips excluded) | ran on 6 cases (whole slice, target window, 1-bp position, 9500x stack, ARTIC, synthetic): mean/max/covered/%>=10x equal truth to 1e-9 and equal `samtools depth -a`; window 251.68 (audit: old code 579.70) | ARTIC raw `pileup.n` mean 69.97 vs true 68.84 (deletions), hence the explicit count |
| 2 pysam counting snippets and `qc_report.py` count secondary/supplementary/QC-fail | P1 | "Count Reads" snippet, usage-guide `flagstat()` and `examples/qc_report.py` skip secondary/supp/QC-fail, print denominators, guard zero divisions | ran: `qc_report.py` counts and percentages equal `flagstat -O tsv` (primary, primary mapped, properly paired, primary duplicates, secondary, supplementary, total) on 14 BAMs incl. planted synthetic (proper pair 92.00% = flagstat, old 88.9%), SE, empty; snippet == flagstat on 6 BAMs | `python -m py_compile` OK; clean-copy run OK; exits with message, not ZeroDivisionError |
| 3 pysam pileup recipes cap at 8000, drop orphans; cap warning omits pysam/bcftools | P1 | Cap section rewritten as a per-tool table (samtools depth uncapped, coverage `-d 1000000`, mosdepth uncapped, samtools mpileup 8000, bcftools mpileup 250, pysam `max_depth=8000`) with the raise flag; helper comments name `ignore_orphans`, `min_base_quality`, deletions | ran on 9500x stack: samtools mpileup 8000 -> 9500 with `-d 1000000`; bcftools DP 250 -> 9500; pysam 8000 -> 9500; helper returns mean 1000.0 (old snippets 850 / 4250) | samtools depth uncapped verified by audit (t4), coverage default from `--help` |
| 4 `samtools coverage -b regions.bed` fails | P1 | Replaced with a `while read` loop over the BED using `-r chrom:start+1-end` and `-H`; states `-b` is `--bam-list` | ran: loop rows equal blocks truth (251.684 / 0) and `mosdepth --by --fast-mode` (251.69 / 0.00); old command reproduces `Cannot open file list` | |
| 5 `grep "bases soft-clipped"` returns nothing | P1 | Replaced by a CIGAR awk (`samtools view -F 2308`) reporting soft-clipped bases of query bases, exiting 1 with a message on empty; grep noted as silently empty | ran on 5 BAMs: output string equals pysam cigartuples truth (863/671854; 400/50500; 59137/2141066; 61703/1012528; 5457/965257); empty BAM rc 1 + message; old grep returns nothing | `stats` "bases mapped" minus "bases mapped (cigar)" equals the clipped bases on 4 real BAMs but not the synthetic one, so not recommended |
| 6 "Insert Size Caveats" wrong about RF libraries | P1 | Rewritten: stats reports IS for any both-mapped pair with inward/outward/other counts; proper-pair pysam snippets skip pairs when the flag is unset | ran (audit `rf.bam`, `rf_noproper.bam`, re-run): average 2000.0, outward 100, flag set and unset; `qc_report.py` on `rf_noproper.bam` prints 0.00% proper, no insert lines | |
| 7 Snippets crash / print silent 0 on SE, empty, MT-named data | P1 | Count Reads, insert-size and `qc_report.py` guard zero denominators; mito recipe matches `^(chr)?(M\|MT)$`; sex-check matches `(chr)?X/Y`; both exit 1 with message when contig absent | ran: chrM 40/525 = 7.62%; renamed `MT` 7.62%; absent contig rc 1 + message; empty rc 1; X/Y on injected idxstats 500/50 -> 10.00; SE and empty BAMs through Count Reads / insert snippet / `qc_report.py` no traceback | |
| 8 Cross-check identity and "primary" row ignore QC-failed / secondary | P2 | Identity is `flagstat_total(passed + failed) - secondary - supplementary = stats raw total sequences`; table row fixed; flagstat "passed + failed" columns explained | ran: synth 540 - 10 - 10 = 520 = raw total sequences; `--help`/audit | |
| 9 `reads mapped and paired` shown as properly paired | P2 | Relabelled "both mates mapped"; listed `reads properly paired` and the percentage line, plus orientation counts | ran: synth stats 500 vs 480 | |
| 10 Mate-overlap defaults not tabulated | P2 | Added the per-tool table under "What Each Tool Counts" | ran on human BAM: depth/coverage/pysam/mosdepth --fast-mode 16.77; depth -s/mosdepth 8.86; mpileup and bcftools mpileup 8.85 default vs 16.75 with `-x`, both 16.77 with `-Q 0` | new fact: `-Q 0` defeats mpileup overlap removal; old "long form" flag names confirmed by `--help` |
| 11 Single-position pileup lacks `truncate=True` | P2 | Merged into `region_depth_stats` (1-bp region) | ran: chr22 pos 3000 = 1562.0 = `samtools depth` | |
| 12 Batch loop drops QC-failed, mislabels columns | P2 | Loop moved into SKILL.md, uses `flagstat -O tsv`, columns Records/QCfail/Primary/PrimaryMapped/ProperPair/PrimaryDup | ran on 12 BAMs (incl. synthetic with 20 QC-failed, SE, empty): every row equals pysam flag counts | |
| 13 Stale notes (idxstats index, CRAM, plot-bamstats perl-URI, `depth -r` comment, depth-cap attribution) | P2 | idxstats note: 1.24 falls back to slow scan with a warning; pysam/mosdepth need index; CRAM: stats `--reference`, mosdepth needs `.crai`; `perl-uri` install line; region comment says 10 Mb; historic "cap was in mpileup" claim dropped, replaced by the verified 1.24 table | ran: unindexed idxstats rc 0 + warning; `stats -r fa cram` fails "Failure while decoding file", `--reference` works; mosdepth CRAM works after `samtools index`; `plot-bamstats` 11 PNGs + index.html; `multiqc .` builds report with samtools stats/flagstat/idxstats | `samtools flagstat` has no `--reference`; not used |
| 14 Unverified claims + duplicated recipes | P2 | "3-10x faster" dropped; threshold table marked as literature ranges; dedup per below | help/docs (speed not benchmarked on this data) | assay values themselves remain unverified |

Also fixed while there (not in the report):
- Quick Summary "Breadth at depth thresholds" row lacked `--by`; mosdepth errors `--thresholds can only be used when --by is specified` (ran).
- `Depth from BED Regions`: `samtools depth -b regions.bed` -> `-a -b` (without `-a` zero-depth bases vanish); ran: 2666 + 500 rows.
- CollectHsMetrics/BedToIntervalList commands added (Skill named the tool but shipped no command): ran Picard 3.5.0, PCT_SELECTED_BASES 1, PCT_OFF_BAIT 0, MEAN_TARGET_COVERAGE 124.74.
- verifybamid2 and somalier were named without a command (Missing referenced executables): wrote commands from `--help`; VerifyBamID2 was run and reports "No reads found in any of the regions" on the 100 kb slice (expected), somalier `extract` needs a whole-GRCh38 FASTA that is not on this machine. Both marked "not run end to end". Corrected "somalier for contamination" to identity/relatedness plus its `contamination` subcommand (listed in `somalier` help).
- MultiQC, plot-bamstats: commands verified above (MultiQC line added; it was only a mention).
- Deleted usage-guide "Red Flags -> Insert size bimodal: library prep issue", which contradicted SKILL.md (ATAC bimodal is expected).
- Qualimap is not referenced by the Skill.

## Missing referenced executables
Chose "write it" for CollectHsMetrics (Picard installed and run) and MultiQC (installed and run); chose "write it, hedged" for VerifyBamID2 and somalier (installed, flags verified from `--help`; a genuine FREEMIX or somalier digest was not produced because no whole-genome BAM exists here). No claim was deleted.

## Deduplication (every deleted passage and where it now lives)

| deleted from usage-guide.md | now |
|---|---|
| Prerequisites (conda samtools, pip pysam matplotlib, gnuplot) | SKILL.md "Version Compatibility" install line (bioconda samtools pysam mosdepth gnuplot perl-uri); `matplotlib` dropped, no snippet uses it |
| "What the Agent Will Do" list | deleted, restates SKILL.md workflow |
| "Choosing the Right Command" table (with unmeasured run times) | SKILL.md "Quick Summary Commands"; speeds dropped as unverified |
| Common Commands: flagstat interpretation | SKILL.md flagstat section (properly paired / singletons / duplicates sentence) |
| Common Commands: idxstats, mito %, sex check | SKILL.md "Parse idxstats" (both recipes fixed) |
| Common Commands: stats, plot-bamstats | SKILL.md samtools stats |
| Common Commands: coverage | SKILL.md samtools coverage |
| Common Commands: depth, mean depth, thresholds | SKILL.md "Mean Depth and Breadth" (fixed) |
| Python `flagstat()` | SKILL.md "Count Reads" (fixed) |
| Python `region_coverage()` | SKILL.md `region_depth_stats()` |
| QC Thresholds pointer | dropped, nothing to say beyond SKILL.md |
| Red Flags: mapping rate <80%, error rate >2% | SKILL.md "QC Thresholds Are Assay-Specific" (one "generic red flags" line) |
| Red Flags: high mitochondrial | SKILL.md table row "Mt fraction" |
| Red Flags: insert size bimodal | deleted, contradicts SKILL.md (ATAC ladder) |
| Batch Processing loop | SKILL.md "Summary table for many BAMs" (fixed) |
| Troubleshooting: missing index | SKILL.md idxstats note |
| Troubleshooting: slow depth | SKILL.md "Depth on Large Files" |
| Tips (7 bullets) | deleted, restate SKILL.md |

SKILL.md internal: the pysam "Calculate Depth at Position", `mean_depth()` and `coverage_stats()` merged into `region_depth_stats()`; Quick Reference "Mean depth" awk now points at the single recipe; overlap-correction paragraph points at the new overlap table.
Disagreement between the two files: usage-guide loop and mean-depth awk differed from SKILL.md's; the audit's runs supported neither, both replaced.

## Left unfixed
- Assay threshold table values and "FREEMIX > 1% / 5%" cut-offs: no data here to verify; labelled as literature ranges / commonly cited.
- "mosdepth faster than samtools depth": not benchmarked on these tiny BAMs; the number was removed, the preference kept.
- Bisulfite / RNA-seq insert-size lines in "Insert Size Caveats": no data here; unchanged.
- FREEMIX and somalier output could not be produced (no whole-genome BAM on this machine); commands are `--help`-checked only.

---

# Round 2 - 2026-09-20

Fixer pass after the re-audit (84, Limited Release, deployable; P1 x1, P2 x5). Branch `fix/af-bamstat`, new commit on top of 377e368.
Tools (WSL `science`, env `alignment-files`): samtools 1.24, bcftools 1.24, pysam 0.24.1, mosdepth 0.3.14, Python 3.12.14.
Scratch (not in any repo): `F:\OpenScience\af-bamstat-scratch\r2\` (`qc_check2.py` runs a clean copy of `qc_report.py` on 19 inputs and compares with `samtools flagstat -O tsv`; `t2.sh` extracts every fenced python/bash block from the worktree SKILL.md and runs it; `t3.sh`/`t4.sh`/`t5.sh` the overlap and mosdepth checks). Data: re-audit `run\data\` and `public-data\` (read only; CRAM = `human\test.paired_end.sorted.cram`).

| finding | priority | change | verified (ran) | notes |
|---|---|---|---|---|
| pysam tools crash on unaligned BAM (no @SQ) and CRAM | P1 | `qc_report.py`: `check_sq=False`, optional 2nd argument `reference.fa` (`reference_filename`), reads wrapped so `OSError/ValueError/NotImplementedError` exit 1 with `cannot read <file>: ...` plus a CRAM/reference hint. SKILL.md pysam section: one paragraph (check_sq, `reference_filename`, CRAM needs `.crai` for region/pileup, flagstat needs no reference, stats needs `--reference`); Count Reads and insert-size snippets get `check_sq=False`; `region_depth_stats(..., reference=None)` | clean copy of `qc_report.py` vs `flagstat -O tsv` (records, primary pass/fail, mapped, proper, dup, sec, supp): 19/19 equal, incl. uBAM (30 records) and CRAM with reference (5644); CRAM without reference: rc 1 + message; missing file rc 1; empty CRAM (rc 0, "nothing to report", flagstat 0); snippets on uBAM (30 primary), on CRAM without reference (`OSError: truncated file`, as documented), with `reference_filename` (5642/5640/5638 = flagstat; insert mean 126); `region_depth_stats` CRAM+ref pos 3000 = 1562.0 = BAM = `samtools depth -a` | `py_compile` OK; text SAM without @SQ also exits 1 with a message (was traceback). `samtools flagstat` on CRAM needs no reference (checked); `stats` does |
| `depth -a -b regions.bed` drops regions on read-less contigs | P2 | recipe is `-aa -b`; one line states the limit (2810 of 3110 rows with `-a`) | planted_depth.bam + its BED: `-a` 2810 rows, `-aa` 3110 = sum of region lengths | |
| mosdepth summary denominator | P2 | mosdepth paragraph: summary `total` covers only contigs with reads (19000 of 22000 bp, 2.95x vs 2.57x); pointer to `samtools coverage` / `depth -aa` | planted_depth.bam: mosdepth total 19000/2.95, `depth -aa` 22000/2.57 | audit also said "mosdepth counts D as covered (69.97 vs 68.84)": re-ran, that is `--fast-mode` only (default mosdepth 68.84 = `depth -aa`; fast-mode 69.97), so the sentence names `--fast-mode` |
| `qc_report.py` 1000 bp insert cap undocumented | P2 | named `MAX_INSERT = 8000` (`samtools stats` default `-i`) with a comment; one bullet under Insert Size Caveats | rf.bam: qc_report mean/median 2000 = `samtools stats` 2000.0 (was no insert lines) | not dropped entirely: an uncapped mean is distorted by mis-mapped pairs |
| Table: bcftools `-x` 16.75 vs 16.77; other nits | P2 | overlap table split per tool. samtools mpileup: 8.85 / `-x` 16.75 / `-Q 0` 16.77. bcftools mpileup: FORMAT/DP and bases used 8.85 default, 16.77 with `-x` or `-Q 0`; INFO/DP 16.77 either way | human BAM with `-d 1000000` (default `-d 250` gives 3.89): INFO/DP 16.77 with and without `-x`; FORMAT/DP 8.85 default, 16.77 `-x`; I16 bases 8.85 / 16.77 / 16.77 (`-Q 0`) | round-1 8.85 for bcftools default was FORMAT/DP; INFO/DP never removes overlaps |
| BED loop header lines; zero-length region; "faster than depth"; 505 lines | P2 | loop skips blank/`#`/`track`/`browser` lines; `region_depth_stats` raises `ValueError('empty region')` for length <= 0; "(faster than depth)" removed (unmeasured); SKILL.md 505 -> 497 lines | loop on a BED with track/browser/# header and blank line: 2 rows, rc 0, equal to the coverage table; zero-length region -> ValueError message; all 31 fenced blocks pass `bash -n` / `ast.parse` | |

Deduplication this round (every deleted passage and where it lives):

| deleted | now |
|---|---|
| SKILL.md "Quick Reference" table (6 rows) | restates "Quick Summary Commands" (same commands) and "Mean Depth and Breadth" (the `-aa` recipe) |
| SKILL.md "Output to File" (`flagstat > flagstat.txt`) | shell redirection; the flagstat section already shows the command |
| usage-guide.md | unchanged (already only overview/prompts/pointer) |

Verification notes: every command above was run against samtools 1.24 / bcftools 1.24 / mosdepth 0.3.14 / pysam 0.24.1; the changed `qc_report.py` was run from a clean copy; `py_compile` OK.

## Left unfixed (round 2)
- Assay-threshold table and FREEMIX cut-offs (1% / 5%): no source could be checked from this machine, and inventing citations would be worse than the current hedge, so the "literature ranges, not verified" and "commonly cited" labels stay.
- VerifyBamID2 FREEMIX and somalier output: still not produced (no whole-genome BAM / GRCh38 FASTA here); the "not run end to end" label stays. Commands remain `--help`-checked.

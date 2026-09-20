# bio-sam-bam-basics fix log

## 2026-09-20 (fixer: Sonnet 5; branch `fix/af-sambam`, worktree `F:\OpenScience\wt\af-sambam`, from staging main 1e96d8e)

Skill: `alignment-files/sam-bam-basics`. First audit 77, Beta Only, not deployable (assertion pass 19/25 = 76%). No P0.
Checked on samtools 1.24 / htslib 1.24, bcftools 1.24, pysam 0.24.1, bwa 0.7.19, minimap2 2.31, bowtie2 2.5.5, mapDamage 2.2.2
(side env), WSL `science` env `alignment-files`. Scratch data and scripts: `F:\OpenScience\scratch\sambam\` (t_*.sh, final.sh).
Data: real human chr22 slice BAM/CRAM (`public-data\human`), audit synthetic `synth.bam`/reads.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `samtools view -c` claimed to prove a CRAM's reference is reachable | P1 | CRAM section: `samtools view -o /dev/null file.cram && echo ok` is the proof; states `-c`, `flagstat`, `idxstats`, `quickcheck` do not decode bases | ran: reference unreachable -> `view -c` 5644 rc 0, quickcheck rc 0, `flagstat`/`idxstats` print counts, `view -o /dev/null` rc 1 with `Unable to fetch reference`, `stats` rc 254; mid-file-corrupted CRAM: quickcheck rc 0, `view -c` 5644, `view -o /dev/null` rc 1; with `-T` or a `seq_cache_populate.pl` cache the same command rc 0 | |
| `view_bam.py` crashes unindexed/empty/SAM; `Mapped 0 / Unmapped 0` on CRAM; unlabelled 0-based; unmapped shown as `None:-1 + None` | P1 | Rewritten: format auto-detected (no `'rb'`), optional 3rd arg `reference.fa`, index counts for BAM only (`is_bam`), otherwise a scan; header row labels `chrom:start(0-based)`; unmapped rows print `unmapped` (`*` when unplaced); friendly error + exit 1 on open/decode failure (CRAM hint) | ran on clean copy: indexed BAM 5642/2 (index), unindexed BAM 5642/2 (scan), SAM 5642/2, CRAM+ref (indexed and unindexed) 5642/2, empty BAM indexed and not 0/0, synth BAM 13/2 (index) and its SAM 13/2 (scan); truth `idxstats` 5642/0 + `*` 2 and `view -c -F4/-f4` 5642/2, synth 13/2; CRAM with no reference -> readable error, rc 1; missing file -> error rc 1. `py_compile` ok | pysam `get_index_statistics()` returns 0/0 for an indexed CRAM, so CRAM is scanned (documented in the code and SKILL.md) |
| Overlapping multi-region queries duplicate records silently | P1 | New "Multiple Regions" section: `-M`, `-M -L bed`, `--region-file`, and a `fetch_regions()` pysam helper (merge, then skip reads that start before the previous interval's end so gap-spanning reads are not repeated) | ran: `view r1 r2` 7356 vs `-M` 5426 vs `-M -L` 5426 vs `--region-file` 5426 vs full-scan truth 5426; `fetch_regions` (code extracted from SKILL.md) matches full-scan truth and has no repeated (name, flag) in 40 random multi-region sets (plus 30 in a first pass), naive fetch sums over-count | merging alone is not enough: gap-spanning reads; noted in the text |
| markdup "silently" marks nothing without MC/ms | P1 | tag paragraph now: markdup refuses, exit 1, `no ms score tag. Please run samtools fixmate on file first.`; dropped unverified featureCounts-NH and fgbio-MD claims | ran (bwa BAM, `markdup` without fixmate rc 1 with that message) | |
| MD:Z "required by bcftools mpileup BAQ" | P1 | MD/NM rows corrected: not needed by mpileup or mapDamage; NM listed for `-e '[NM]<=2'` | ran: `bcftools mpileup -f` body md5 identical with and without MD/NM (29691 rows); mapDamage 2.2.2 `misincorporation.txt` identical apart from the file-name header line; `view -e '[NM]<=2'` 5516 | dropped the unverified IGV claim |
| "bcftools / Picard often need M" | P1 | replaced: mpileup output identical on `=`/`X` and `M`; `calmd` rebuilds MD/NM for either | ran: minimap2 `--eqx` (5000 records with `=`/`X`) vs plain: pileup body md5 identical; `calmd -e` gives MD/NM on eqx read | Picard part removed, not testable cheaply; not claimed |
| Bowtie2 MAPQ 42 "rare" | P1 | row: 0-42 end-to-end, 0-44 `--local`; 42/44 is the top and most common value (97% of records) | ran: bowtie2 e2e top MAPQ 42 (4870 of ~4900 mapped), `--local` 44 (4734) | |
| "different reference silently corrupts bases" | P1 | CRAM text: refused with `MD5 checksum reference mismatch` rc 1; silent only with `--input-fmt-option ignore_md5=1` | ran: 1-base-changed FASTA -> rc 1 with that error; `ignore_md5=1` -> rc 0 and the SEQ column md5 differs from the correct-reference decode | |
| `convert_formats.sh`: reference not used for CRAM input, `.BAM` rejected, input == output destroys input | P1 | `-T` passed in every branch via `REF_ARGS`, extension lower-cased, `-ef` guard refuses input == output; usage line for CRAM->BAM | ran on clean copy (CRAM header UR unreachable, REF_PATH bogus): CRAM->BAM and CRAM->SAM with reference: 5644 records, cols 1-11 md5 identical to the original; CRAM->BAM without reference: rc 1; `.BAM` output ok; `same.bam same.bam` and `same.bam ./same.bam`: rc 1, input still 5644; BAM->CRAM no reference: error rc 1; unknown ext rc 1; `bash -n` ok | |
| Duplicated SKILL.md / usage-guide | P2 | see deletion table below | diff of both files | |
| No CIGAR consumption table / TLEN sign / MAPQ 255 note | P2 | CIGAR consumption table, span formulas, TLEN sign line, MAPQ 255 sentence added | audit's independent spec model agreed with SAM spec table (audit input 3) | rule text follows the SAM spec |
| `samtools view -H` adds its own @PG | P2 | `--no-PG` note in @PG section | ran: 2 `@PG` lines vs 1 with `--no-PG` on the test BAM | |
| Wrong contig name exits 0 with 0 rows | P2 | one-line note under View Specific Region with the warning text and `idxstats \| cut -f1` | ran: `22:2000-3000` -> warning, 0 rows, rc 0 | |
| SKILL.md SAM example not parseable | P2 | example rewritten as a valid TAB-separated 8-base record; note that no-`@SQ` SAM needs `-t ref.fa.fai` | ran: block extracted from SKILL.md -> `samtools view -b` -> record read back; without `-t` "no SQ lines present", with `-t` rc 0 | |
| `-C` without `-T` embeds the reference; `embed_ref` never mentioned | P2 | CRAM section: warns `Enabling embed_ref=2` and embeds; self-contained CRAM via `-T ref.fa --output-fmt-option embed_ref=1` | ran: no-`-T` warning seen; `embed_ref=1` CRAM decodes with no reference reachable, 5644 records, cols 1-11 md5 identical to the BAM | |
| CRAM re-orders tags | P2 | one line under Pipe Conversion | audit (tag SET identical 5644/5644, ORDER 2/5644) | not re-run by me |
| SA:Z "comma-list" | P2 | row: `rname,pos,strand,CIGAR,mapQ,NM;` records | ran: synth read `SA:Z:ctg2,100,+,30S20M,60,0;` | |
| minimap2 `ms:i` unrelated to fixmate `ms` | P2 | noted in the `ms:i` row (also `MC:Z` written by bwa mem) | ran: minimap2 tag list `NM ms AS nn tp cm s1 s2 de rl`; bwa mem `NM MD MC MQ AS XS RG`; `fixmate -m` adds `MC ms` | |
| Other foundational claims re-checked (no change needed) | - | FLAG bit table, coordinate table, `samtools flags 99/147`, `-F 2304`, N/S/H semantics, `fetch` vs region boundary, HI 1-based, STAR MAPQ set | audit runs (independent spec decoder, 15 synthetic records, six aligners) plus my `samtools flags` run; pysam equivalent of `chr1:100-200` added as `fetch('chr1', 99, 200)` (ran: `fetch(1999,3000)` = 2732 = `view chr22:2000-3000`) | |
| Also added | P2 | `view -c -F 2304` for primary alignments; `-@` threads; pysam mode table now says reading auto-detects (`'r'`/`'rb'` read SAM, BAM, CRAM); `bam.mapped` limits; `bam.count(until_eof=True)` for unindexed | ran (`rb` on SAM reads 5644; `-c -F 2304` 5642 = flagstat primary 5642; `-@ 2` count 5644) | |

## Redundancy pass: deleted passages and where they live

| deleted passage | now lives in |
| --- | --- |
| usage-guide "Prerequisites" (conda/pip install commands) | SKILL.md "Version Compatibility" (Install line) |
| usage-guide "Understanding SAM Format": file structure, header types, alignment-fields table | SKILL.md "SAM Format Structure" (kept single copy) |
| usage-guide "Common FLAGS" (99, 147, 4, 256, 2048) | SKILL.md "Common Flags" table + Decode Flags (added `samtools flags 99` example) |
| usage-guide "CIGAR Operations" (6 rows) | SKILL.md "CIGAR Operations" (9 rows + new consumption table) |
| usage-guide "Common Commands" (viewing, conversion, decode FLAGS) | SKILL.md "samtools view", "Format Conversion", "Decode Flags"; `samtools view input.bam chr1` (whole chromosome) added to "View Specific Region" |
| usage-guide "Python with pysam" (read, properties, fetch) | SKILL.md "pysam Python Alternative" |
| usage-guide "File Mode Strings" table | SKILL.md pysam section (corrected: auto-detect on read, mode matters for writing) |
| usage-guide "Troubleshooting" (missing index, CRAM reference, chromosome names) | SKILL.md "View Specific Region" (index, name mismatch), "CRAM Reference Resolution" |
| usage-guide "Tips" (sorted+indexed, BAM vs CRAM, 0/1-based, `-h`, context managers, `-@`) | SKILL.md: region note (sorted+indexed), coordinates table (0/1-based), View with Header (`-h`), Count Alignments (`-@`); BAM-vs-CRAM already in Format Overview; context-manager tip dropped (every snippet already uses `with`) |
| SKILL.md Quick Reference rows BAM to SAM / SAM to BAM / BAM to CRAM | "Format Conversion" and the new mode table |
| SKILL.md "production pipelines often reject inputs without a complete chain" | deleted (unverified) |
| SKILL.md "featureCounts ignoring multimappers without NH ... consensus tools rejecting input without MD" | deleted (unverified; fgbio not run); replaced by the verified markdup sentence |
| usage-guide "Overview" / prompts / What the Agent Will Do / related | kept; guide now points at SKILL.md sections |

usage-guide.md 210 -> 53 lines; SKILL.md 373 -> 431 lines (new sections: multi-region, consumption table, CRAM checks).
Disagreements between the two files: usage-guide "6-row" CIGAR/FLAG tables were subsets of SKILL.md's; no factual conflict.

## Unfixed

- DRAGEN MAPQ scale, Cell Ranger / STARsolo tags (CB/UB), featureCounts NH behaviour: not verifiable here (as in the audit); text left as is except the two deleted claims above.
- `samtools view -M` on unindexed BAM not documented (needs an index; not tested).
- Picard behaviour on `=`/`X` CIGARs: claim removed, not tested.

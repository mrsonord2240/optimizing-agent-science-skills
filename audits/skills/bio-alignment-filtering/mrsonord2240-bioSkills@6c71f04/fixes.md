# bio-alignment-filtering — fix log (2026-09-20)

Skill `alignment-files/alignment-filtering`, branch `fix/af-filter` (worktree `F:\OpenScience\wt\af-filter`, from staging `c206dff`).
Evidence: `F:\OpenScience\audits\bio-alignment-filtering\` (first audit 75, Beta Only, assertions 22/35, no veto, no P0).
Tools on every run: samtools 1.24 (htslib 1.24), pysam 0.24.1, Python 3.12.14 (WSL `science`, env `alignment-files`); aligners BWA 0.7.19, Bowtie2 2.5.5, HISAT2 2.2.3, minimap2 2.31, STAR 2.7.11b. Scratch data and scripts lived in `F:\OpenScience\wt\af-filter-scratch` (not tracked).
Version claims checked against the samtools `NEWS.md` (github.com/samtools/samtools, develop).

## Findings

| # | finding | pri | change | verified | notes |
|---|---|---|---|---|---|
| 1 | Aligner table: `-q 1` "drops ambiguous" wrong for Bowtie2, HISAT2 | P1 | Bowtie2 and HISAT2 rows -> `-q 2`; STAR row explains 255/3/1/0 and that `-q 4`..`255` are equal | ran: repeat genome re-aligned with all 5 aligners, 400 exact-repeat reads. Kept after old `-q 1`: Bowtie2 399, HISAT2 374, STAR 80. Kept after new threshold: 0/400 for BWA `-q 1`, Bowtie2 `-q 2`, HISAT2 `-q 2`, STAR `-q 255`/`-q 4`, minimap2 `-q 1`; unique reads kept 2000/2000 (Bowtie2), 1995/2000 (HISAT2, STAR) | pbmm2 row not run (long-read only), left as written |
| 2 | "Drop Ambiguous Across Aligners (Universal) `-q 1`" contradicts the STAR row | P1 | Block deleted; replaced by "no universal threshold" paragraph, plus `-e '[NH]==1'` for aligners that write NH | ran: `-e '[NH]==1'` removed 400/400 exact repeats on HISAT2 and STAR; on BWA/Bowtie2 (no NH) it returns 0 reads, and the text says so; real STAR BAM MAPQ 255 == NH 1 (audit: 5768 = 5768) | |
| 3 | pysam BED recipe writes reads once per overlapped row, unsorted, breaks on `track` lines | P1 | Recipe rewritten: skip `#`/`track`/`browser`/blank rows, drop contigs absent from the header, sort by header order, merge intervals, skip reads that start before the previous interval's end | ran: on a BED with `track`, comment, blank, overlapping rows, a read-spanning gap, a zero-width row and an unknown contig the output was **byte-identical, same order**, to `samtools view -L` (2612 records; naive per-row loop 3947); `SO:coordinate` kept | |
| 4 | `examples/filter_bam.py`: region off by one, crashes on bare contig / `chr:start` / commas / colon contig, writes then dies on name-sorted input | P1 | Own `parse_region` (samtools syntax, 1-based inclusive, colon-containing contig names matched whole first); clean error on bad region; error if no index; index only if header is `SO:coordinate`; `-d` warning when no read carries 0x400; script now referenced from SKILL.md | ran: `chr22`, `chr22:1952`, `chr22:1952-`, `chr22:1,952-2,100`, `chr22:1952-2100`, `chr22:2043-2043`, `chr22:4617-4700` all equal `samtools view -c -F 4 <region>` (5642, 5642, 5642, 802, 802, 796, 2); colon contig `chr22:16570000-16610000:1952-2100` 2545 = samtools; bad regions exit with a message and create no output; name-sorted input no crash, no index; unindexed + region -> message; `-q 30 -d -p -P` 5638 = `samtools view -f 2 -F 3332 -q 30`; `py_compile` ok; ran from a clean copy of the skill folder | |
| 5 | Docs: bare `-s 0.1` "non-reproducible, reject it" is false | P1 | Replaced with the checked fact: bare `-s 0.1` is seed 0 and deterministic; the *default seed of `--subsample`* changed in 1.24 (was 0, now header hash), so give a seed explicitly | ran: `-s 0.1` twice byte-identical and == `--subsample 0.1 --subsample-seed 0` (1015 records); `--subsample 0.1` (auto) 1001 records, differs; `-s 42.1` 1016. NEWS 1.24 states the default-seed change | |
| 6 | pysam subsample recipe ignores its seed (`crc32 ^ seed`) | P1 | Seed mixed into `blake2b(f'{seed}:{qname}')` | ran: seeds 42/1/7/100/12345: 457-494 templates (~10%), 0 partial templates, pairwise Jaccard 0.044-0.069 (independent 10% samples expect 0.053); same seed twice identical md5. First try `crc32(f'{seed}:{qname}')` was rejected: Jaccard 0.65 between seeds 42 and 100 | recipe selects different reads than `samtools -s` (stated) |
| 7 | Coverage-matching / tumor-normal snippets keep ~8% when target > total (`-s 1.084419`) | P1 | `if [ total -le target ]` guard (copy unchanged) added to coverage-matching; sentence explaining the trap; usage-guide `bc` snippet deleted (see below) | ran: target 3000 -> 2851 records (hash-based, -5%); target 20000 > 9595 -> copy, 9601 records (before: 750); tumor-normal: 5604 vs normal 5640; sequential cuts 4738 / 1197 of 9601 | tumor-normal block already guarded by `-gt` |
| 8 | `-F 1024` on an unmarked BAM silently removes nothing | P1 | Remove Duplicates now checks `samtools view -c -f 1024` and, at 0, runs collate/fixmate -m/sort/markdup first; the duplicate prerequisite is repeated in the standard filter; `filter_bam.py -d` warns; usage-guide step 1 mentions it | ran: planted-duplicate BAM (100 unmarked duplicate reads): snippet marks 100 and leaves 400; already-marked BAM -> straight `-F 1024`, 400; script `-d` on unmarked prints the warning (kept 500), on marked removes 100 (400) | |
| 9 | SKILL.md `-F 3332` vs usage-guide `-F 2308` "standard" | P2 | One definition (`-F 3332 -q 30`, SKILL.md); usage-guide reduced to overview/prompts/pointer | 1000G BAM: -F 2308 keeps 101 dup-flagged reads, -F 3332 drops them (audit run) | see dedup table |
| 10 | Mislabelled rows: "Count unique -F 2304", "Forward -F 16", "Read1 -f 64" | P2 | "Count unique" row now "Primary alignments (multi-mappers still included)" + note; forward `-F 20`, reverse `-f 16 -F 4`; read1/read2 `-f 64 -F 2308` / `-f 128 -F 2308` | ran on the 4096-flag synthetic BAM against Python bit arithmetic: 256 / 256 / 1024 / 1024 records, 0 unmapped in strand outputs, 0 secondary/supplementary/unmapped in read1 output | |
| 11 | Somatic recipe `-F 3328 -q 1` drops the supplementary reads its own rationale keeps | P2 | `-F 1280 -q 1` and rationale reworded | ran: 4096-flag BAM, 1006 records = bit arithmetic; 503 of 503 supplementary (MAPQ>=1) kept | breakdown list gained 1280 and 2308 |
| 12 | `-r library_A` example wrong; `-r` also emits untagged reads; `-l`, `-P`, `-n` undocumented | P2 | Example uses an RG ID; notes on untagged reads; `-e '[RG]=="ID"'`, `-l`, `-n` (1.24) added; `-P` note under BED | ran: `-r SRR702039` 4438 = `-e '[RG]==...'` 4438 = `-n -r` 4438 = `-R file` 4438; a real LB value: `-r` 0, `-l` 9601; `-P` on chr22:1952-1960: 2 records plain, 5 with -P, 0 orphaned mates | `-n` first appears in samtools 1.24 (NEWS) |
| 13 | Version-introduction claims unverified | P2 | `-e` since 1.12 and `sclen` documented in 1.16 kept, both now confirmed; the "null-tag handling arrived in 1.16" claim dropped, replaced by "checked on 1.24" | NEWS.md 1.12 ("samtools view now works with the filtering expressions") and 1.16 ("Add sclen filter expression keyword documentation") | |
| - | (audit note) `examples/filter_bam.py` linked from neither doc | P2 | SKILL.md pysam section now names and describes it | | |
| - | Region text: unknown contig prints a warning and exits 0 with zero reads | P2 | Added to Filter by Region | ran: `chr1:...` on a chr22 BAM -> warning, 0 reads, rc 0 | |
| - | `-e` on a tag the file lacks is silently empty | P2 | Added to Expression Filtering note | ran (`[NH]` on BWA/Bowtie2 output: 0 reads, no warning) | |

Every SKILL.md fenced bash block (19) was run from a clean copy of the skill folder on the audit data with fixture substitutions (chr1 -> chr22, target read count 3000, files supplied for `targets.bed`, `rg_list.txt`, reference): no stderr, no failures. The four python blocks were extracted from the final SKILL.md and run (region, BED, subsample, passes_filter == `-F 3332 -q 30`, 5640 records and identical field md5).

## Findings not fixed

- Caller rationale in the assay table (Mutect2/Strelka2, clair3, Sniffles, DeepVariant recipes): callers are not installed; unchanged, still unverified.
- pbmm2 MAPQ row: not run (long-read only).
- Noticed, not in the report, not changed: read-level filters can leave orphaned mates (audit: 53 singletons after `-F 3332 -q 30`); a composite insert-size expression needs `abs(tlen)`; both need new sections, not corrections.

## Deleted passages and where the content lives (dedup, usage-guide.md and SKILL.md)

| Deleted | Now |
|---|---|
| usage-guide "Understanding SAM FLAGS" table | SKILL.md "Common FLAG Values" (identical table) |
| usage-guide "Decoding FLAGS" (`samtools flags 99`, `147`) | SKILL.md, one-line `samtools flags 99` example under the FLAG table |
| usage-guide "Common Filter Patterns" (`-f 1/2/3`, `-F 4/1024/2304`, `-f 2 -F 1024`, `-F 2308`, `-f 2 -F 3332 -q 20`) | SKILL.md "Filter by FLAG", assay table (germline `-f 2 -F 3328 -q 20`) and the flag-breakdown list; the usage-guide `-F 3332` variant and `-F 2308`-as-standard disagreed with SKILL.md and were dropped (log #9) |
| usage-guide "Common Commands: Basic Quality Filter, Region Filtering, Subsampling" | SKILL.md "Filter by FLAG / MAPQ / Region" and "Subsample Reads"; the `bc`/`-s "42${frac}"` splice snippet deleted (same job as the guarded coverage-matching block; it also mis-sampled when target > total) |
| usage-guide "Output Options" (`-b`, `-C -T`, `-c`, `-h`) | SKILL.md "Output Options and Checks" |
| usage-guide "Python with pysam: Simple Filter, Configurable Filter, Count with Filter" | SKILL.md "Filter with Function" (`passes_filter`, identical record set); the class and `count_with_filter` were variants of it; counting is `samtools view -c -F .. -q ..` (SKILL.md "Output Options and Checks") |
| usage-guide "Mapping Quality (MAPQ)" error-probability table | SKILL.md aligner table plus the `10^(-Q/10)` line under it; sam-bam-basics holds the full MAPQ table |
| usage-guide "Troubleshooting" (index required, check filter effect, verify output) | SKILL.md "Filter by Region" (index) and "Output Options and Checks" (`-c` before, `quickcheck`, `flagstat`) |
| usage-guide "Tips" (7 bullets) | each is a SKILL.md section (count first, `-F 3332` standard, MAPQ, index, `-s SEED.FRAC`, `-f`/`-F`); "use `-F 2308` for most downstream analyses" contradicted SKILL.md and was dropped; "save commands" was generic |
| SKILL.md "Remove Secondary and Supplementary" + "Keep Only Primary Alignments" (both `-F 2304`, one used repeated `-F`) | one "Keep Only Primary Alignments" section |
| SKILL.md pysam "Basic Filtering" (subset of `passes_filter`) | SKILL.md "Filter with Function" |
| SKILL.md "Common Filter Combinations" table (Clean reads, Variant calling, Coverage analysis, Count unique) | "Standard Quality Filter", the assay table (which gained the Coverage analysis row) and the Quick Reference table |
| SKILL.md inline flag-sum comments (3332, 3328, 1804, 2304) | single "Flag breakdowns" list (now also 1280, 2308) |

---

# 2026-09-21 (P2 pass, split, scripts)

Skill `alignment-files/alignment-filtering`, branch `fix/alignment-files-alignment-filtering` (worktree `F:\OpenScience\wt\alignment-files-alignment-filtering`, from staging `431aa55`). Commits: `9d18a79` fix, `bdff911` split, `016d741` scripts.
Evidence: `F:\OpenScience\audits\bio-alignment-filtering\eval_report_bio-alignment-filtering_result.json` (5 P2). Tools: samtools 1.24, pysam 0.24.1, minimap2 2.31 (WSL `science`, env `alignment-files`). Scratch `F:\OpenScience\wt\afilt2-scratch` (deleted).

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `-n` (`--exclude-no-read-group`) is 1.23, not 1.24 | P2 | "Samtools 1.23 adds `-n`"; 1.24 `--help` spells `--exclude-no-read_group`, hyphenated form also works | ran: `-r SRR702039` 4438 = `-n -r` 4438 = `--exclude-no-read-group -r` 4438 on 1000G BAM; `--help` | 1.23 date from the audit's NEWS check (n11) |
| Somatic-row rationale contradicted by a real Mutect2 run | P2 | Row reworded: `-F 1280 -q 1` is a light pre-filter, Mutect2 applies MAPQ>=20, not-secondary, not-duplicate, non-chimeric-original itself; one line under the table says caller rationale is from documentation and only Mutect2/HaplotypeCaller filters were run | audit's Mutect2 run (120/5642 removed by `MappingQualityReadFilter`) and default-filter lists (`run/out/n10_*`), read, not re-run | GATK not re-run: the audit's output is the evidence |
| pysam BED recipe not equal to `-L` on zero-width/space rows | P2 | `line.split()` (space-delimited rows); equivalence claim scoped to rows with start < end. Audit's suggested `max(end, start+1)` was tried and **rejected**: 5 of 80 fuzz BEDs still differed, because `-L` reads a zero-width row as "reads with start < s < end" (strictly spanning), not one base; `fetch` cannot express that | ran: 80 random BEDs (28 space-delimited, rows start < end, with track/comment/blank lines) x 2 BAMs, recipe extracted from SKILL.md: 0 differ from `samtools view -L`; separate check: zero-width `-L` count == model `start < s < end` on 60 random positions, 0 differ | zero-width rows: text says drop or widen |
| Three filter pitfalls missing | P2 | New "Filter Pitfalls" (3 bullets, one 3-line block): orphaned mates and a `-N` keep-pairs recipe; no `-f 2` for SV callers; signed `tlen` | ran on 1000G BAM: `-F 3332 -q 30` leaves 89 single-record names; `fixmate` leaves 89 (audit's suggestion does not remove them: not used); `-N` recipe leaves 0 (9348 records); mapped 9563 vs `-f 2` 9454 (109 lost); `-e 'tlen>=100 && tlen<=500'` 4677, both-sign expression 9346 = pysam `abs()` count 9346; `abs()` in `-e` fails ("Couldn't process filter expression", audit's `abs(tlen)` advice is wrong); block extracted from SKILL.md and run | audit counted 53 orphans (mate mapped only); the text uses 89 (all single-record names) |
| minimap2 row silent about short-read MAPQ ceilings | P2 | Row split: long-read presets `-q 60`; `-x sr` drop-ambiguous `-q 1`, high-confidence `-q 30`, with the measured 58.5% | ran: minimap2 2.31 `-ax sr` on the real human PE reads: 5570 primary, `-q 1` 5570, `-q 30` 5514, `-q 60` 3261 (58.5%); unique MAPQ 48-59 | `-q 30` chosen from the measured distribution (99% kept); no ambiguous reads on this slice, so its "drops ambiguous" side is not exercised |

## Left unfixed

None of the 5 P2s. Not run, stated in the text: caller rationale for Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA (callers not installed; the text now says so); pbmm2 MAPQ row (long-read only, was already stated).

## Redundancy pass

`usage-guide.md` was already reduced on 2026-09-20 (overview, prompts, pointer, two tips); nothing duplicated remains, skipped.

## Split (`bdff911`): SKILL.md 444 -> 279 lines

| Moved (verbatim) | New home |
|---|---|
| `## Subsample Reads (Deterministic, Pair-Consistent)` | `references/subsampling.md` |
| `## Expression Filtering`, `## Filter by Read Group` | `references/expressions-and-read-groups.md` |
| `## pysam Python Alternative` (all four subsections) | `references/pysam.md` |

Checked: no non-blank line lost (only the two pointer-edited lines differ), fences even, python blocks `ast.parse`, bash blocks `bash -n`. "Reference Files" index and two pointer lines added to SKILL.md (no decision tree in this Skill).

## Scripts (`016d741`)

| Old location | New |
|---|---|
| `references/pysam.md` "Filter from BED File" recipe (27 lines) | `scripts/filter_by_bed.py` (args bam, bed, out) |
| `references/pysam.md` "Subsample (Pair-Consistent)" recipe (16 lines) | `scripts/subsample_pysam.py` (args bam, out, fraction, seed) |
| `references/subsampling.md` coverage-matching + tumor-normal snippets (17 lines) | `scripts/match_read_count.sh` (`--target N` / `--like other.bam`) |
| `references/pysam.md` "Filter with Function" `passes_filter` block (16 lines) | deleted: duplicates `examples/filter_bam.py`; text points at `filter_bam.py -q 30 -d -p` |

Run as invoked: `filter_by_bed.py` md5-identical to `samtools view -L` (2608 records; track/comment/space/unknown-contig rows); `filter_bam.py -q 30 -d -p` md5-identical to `-F 3332 -q 30` (1000G BAM); `subsample_pysam.py` 947/9601 at 0.1, same seed byte-identical, 0 partial templates, seeds 42 and 7 share 49 of ~480 templates (10%, independent); `match_read_count.sh --target 3000` 2849 primary reads, `--target 20000` and `--like` a larger BAM copy unchanged.

---

# 2026-09-21/22 (final pass, phase 1)

Branch `fix/alignment-files-alignment-filtering` (worktree `F:\OpenScience\wt\alignment-files-alignment-filtering`). Commit: `<see git log>`. Scratch `F:\OpenScience\wt\afinal-scratch` (deleted).

## Findings

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| pbmm2 MAPQ row stated "not run" (no PacBio data in the env) | P2 | Row now states a checked result | ran: synthetic reference with a planted 3 kb exact repeat (from `human/genome.fasta`), 9 PacBio-HiFi-like reads (0.2% substitution), `pbmm2 26.2.99 --preset CCS` -- 5/5 unique-region reads MAPQ 60, 4/4 repeat-region reads MAPQ 0 | pbmm2 was already installed (TOOLS.md); the blocker was the dataset, resolved with a synthetic substitute per FINAL_PASS_BRIEF |

## Left unfixed

None outstanding. Caller rationale for Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA in the assay-aware table stays documentation-only by design: the table's runnable content is the samtools filter recipe (verified), the text already discloses which caller filters were and were not run, and the Skill's `primary_tool` is samtools/pysam, not these callers. Not a blocked item -- judged resolved by the existing disclosure.

## Re-verification (no prior finding, consolidation)

Every bash block in `SKILL.md` and the three `references/*.md` files, plus `examples/filter_bam.py` and all three `scripts/`, re-run end-to-end in one pass on a fresh copy of the skill folder against real data (`human/test.paired_end.sorted.bam`, chr22; 1000G BAM), including the pysam.md inline "Filter by Region" block (previously only `ast.parse`d post-split). All match the counts/equivalences already on record; no regression from the split or scripts move. `py_compile`/`bash -n` clean on all scripts.

Checkpoint: `F:\OpenScience\audits\_final_pass\bio-alignment-filtering\CHECKPOINT.md`.

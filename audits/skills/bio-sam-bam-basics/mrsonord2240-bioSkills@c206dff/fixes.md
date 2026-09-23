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

## 2026-09-21 (fixer: Sonnet 5; branch `fix/alignment-files-sam-bam-basics`, worktree `F:\OpenScience\wt\alignment-files-sam-bam-basics`, from staging main 431aa55)

Re-audit 85, Production Ready, 4 P2s. Commits: `d5e2910` (fixes), `9d0fe15` (split).
Checked on samtools 1.24, pysam 0.24.1, minimap2 2.31, bwa 0.7.19, pbmm2 26.2.99 (WSL `science`, env `alignment-files`).
Scratch: `F:\OpenScience\scratch\sambam2\` (t1-t5.sh).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| CRAM round trip "keeps every field and tag but not the tag order" is false | P2 | Sentence moved out of "Pipe Conversion" into its own "CRAM round trip is not byte-lossless" section: `=`/`X` become `M`, NM/MD regenerated when the reference is available, tags reordered, unmapped MAPQ becomes 0; use BAM when exact CIGAR ops or tag set matter | ran: minimap2 `--eqx` BAM (200 reads) -> CRAM -> BAM: `=`/`X` ops in 197 reads -> 0, MD:Z on 0 -> 197 reads, cols 1-5 and 7-11 identical; hand SAM unmapped read MAPQ 10 -> 0 | |
| Unverified table rows stated as fact (DRAGEN, Cell Ranger/STARsolo, featureCounts/RSEM, pbmm2) | P2 | "(not verified here)" on DRAGEN, Cell Ranger/STARsolo, NH (featureCounts/Salmon), HI (RSEM), CB, UB; pbmm2 verified instead and row annotated "checked: minimap2 2.31, pbmm2 26.2.99" | ran: pbmm2 `--preset HIFI` on 20 simulated unique 6 kb reads: all MAPQ 60 | DRAGEN, Cell Ranger, STARsolo, featureCounts, RSEM not installed / need real input; marked, not removed (statements are plausible tool behaviour) |
| `view_bam.py` raw ValueError on non-numeric limit | P2 | `int(sys.argv[2])` inside a try; message + usage to stderr, exit 1 | ran: `abc` -> message, rc 1; numeric and default limits unchanged; `py_compile` ok | |
| `convert_formats.sh` leaves output when samtools fails | P2 | Validation (extension, CRAM reference) runs first; EXIT trap deletes OUTPUT on non-zero exit, installed only just before samtools runs | ran: CRAM input with unreachable reference: old script rc 1 and left `f2.bam` (500 B), new rc 1 and no file; validation exits keep a pre-existing file; SAM/BAM/CRAM conversions still 5644 records; `bash -n` ok | Trap scoped after validation on purpose: a naive trap deleted a pre-existing unrelated file on a usage error |
| `[E::cram_index_load]` lines on unindexed CRAM | P2 | One sentence in the pysam section: harmless when the run succeeds | ran: `view_bam.py` on unindexed CRAM -> 4 such lines, rc 0, counts correct | |
| pysam `wc` mode row said "needs `reference_filename=`" | P2 | "give `reference_filename=`; without it pysam warns and writes an embedded-reference CRAM" | ran: no `reference_filename` -> `embed_ref=2` warnings, CRAM quickchecks, 5644 records, no M5 in header | |
| @PG example IDs `bwa-mem`, `samtools.1..3` | P2 | `bwa`, `samtools`, `samtools.1`, `samtools.2` with matching PP | ran: bwa mem \| sort \| fixmate \| sort \| markdup -> IDs bwa, samtools, samtools.1, .2, .3 | |
| `-M` needs an index not stated | P2 | "(needs an index, like any region query)" | ran: unindexed BAM -> rc 1 `Could not retrieve index file` | |
| MAPQ distribution command printed distinct values | P2 | `sort -n \| uniq -c \| head -20` | ran: counts per value on the human BAM (5637 at 60) | |

Redundancy pass: already done on 2026-09-20 (usage-guide 210 -> 53 lines, one copy of each fact). Skipped.

Split: SKILL.md 435 -> 276 lines. Verbatim moves; "Reference Files" index added, pointers from the pysam bullet, Format Conversion Approach (CRAM) and after the Secondary vs Supplementary table (MAPQ). Non-blank line multiset before == SKILL.md + 4 references except the 2 lines that gained a pointer. 23 python/bash fences parse (ast / `bash -n`).

| moved section | now lives in |
| --- | --- |
| MAPQ Is Not Portable Across Aligners | `references/mapq-by-aligner.md` (19 lines) |
| Context-Specific Tags, Provenance: @PG Chain | `references/tags-and-provenance.md` (42 lines) |
| CRAM Reference Resolution (Critical) | `references/cram-reference.md` (24 lines) |
| pysam Python Alternative | `references/pysam.md` (82 lines) |

usage-guide.md Overview now names the `references/` files as well as SKILL.md.

### Left unfixed
- DRAGEN `--mapq-max`, Cell Ranger/STARsolo MAPQ 255 and CB/UB, featureCounts/RSEM tag consumption: cannot be run here (DRAGEN and Cell Ranger absent and licence/real-input gated; STARsolo/featureCounts/RSEM need a whitelist/annotation dataset that does not exist in `public-data`). Marked "(not verified here)" as the audit suggested.
- pysam's "truncated file" wording for a missing CRAM reference (audit static note, not a recommendation): it is pysam's own message, and `view_bam.py` already appends the reference hint; not changed.

### Scripts move (2026-09-21, commit below the split; SKILL.md 276 -> 265 lines)

| old location | script path | verified |
| --- | --- | --- |
| SKILL.md "Multiple Regions" `fetch_regions()` (17 lines) | `scripts/fetch_regions.py` (verbatim function + BED CLI + `read_bed`; SKILL.md keeps CLI and import invocation) | ran on human BAM: 2 BED sets -> 5426 and 802 reads, identical (cols 1-11) to `samtools view -M -L`; naive multi-region view 7356; import path 5426; wrong contig / no args rc 1 |

Not moved: `examples/view_bam.py` and `convert_formats.sh` already are the scripts (SKILL.md and pysam.md point to them); every other block is under 15 lines (pysam open/iterate/convert fragments, CRAM cache recipe 8 lines, conversion one-liners) and stays inline.

## 2026-09-21 final pass, Phase 1 (fixer+auditor: Sonnet 5; branch `fix/alignment-files-sam-bam-basics`, worktree `F:\OpenScience\wt\alignment-files-sam-bam-basics`, from branch tip `3580586`)

Resolved every item on the 2026-09-21 "Left unfixed" list that was resolvable with a public, unauthenticated
install (per `FINAL_PASS_BRIEF.md`'s wider install permission). New side env `af-subread` (subread 2.0.6,
RSEM 1.2.28, bowtie2 2.5.4) added to `F:\OpenScience\audit-envs\alignment-files\TOOLS.md` under the
install-lock protocol; no existing env or package touched. Scratch: `F:\OpenScience\scratch\sambam3\`.

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `mapq-by-aligner.md` "Cell Ranger / STARsolo inherits STAR, 255" not verified | P2 | Row now says STARsolo checked, Cell Ranger not run | ran: STAR 2.7.11b, synthetic duplicated-contig genome + 80 synthetic 10x-style reads (40 unique, 40 forced to 2 loci): STARsolo MAPQ 255 (unique) / 3 (2-locus), matching plain STAR's scale | Cell Ranger not run: 10x Genomics gates the download behind account registration |
| `tags-and-provenance.md` CB:Z / UB:Z "not verified here" | P2 | Rows now say STARsolo checked, Cell Ranger not run | ran: same STARsolo job, `--soloType CB_UMI_Simple` + 3-entry whitelist -> `CB:Z` matches the whitelist entry, `UB:Z` present on every aligned read | |
| `tags-and-provenance.md` NH:i "Required by featureCounts ... (not verified here)" | P2 | Row now cites the exact featureCounts behaviour | ran: subread 2.0.6 `featureCounts` on the STARsolo BAM (40 NH:i:1, 40 NH:i:2 reads): default excludes all NH>1 records (`Unassigned_MultiMapping: 80`); `-M` includes all 120; `-M --fraction` weights 0.5/0.5 per locus | Salmon left "(not verified here)", out of scope for this pass |
| `tags-and-provenance.md` HI:i "Required by RSEM (not verified here)" was wrong, not just unverified | P1 | Row corrected: RSEM does not read an HI tag; it groups a read's alignments by consecutive same-QNAME lines | checked: RSEM 1.2.28 `rsem-calculate-expression --help` and `convert-sam-for-rsem --help`, neither mentions HI | caught only because this pass installed RSEM to check; a real defect, not a mere gap |
| Full re-run of every runnable block post-split/post-scripts-move | - | no changes needed | ran: all SKILL.md inline commands, `examples/view_bam.py` (5 modes incl. bad-limit/missing-file), `examples/convert_formats.sh` (5 cases), `scripts/fetch_regions.py` (CLI + import) on the current worktree layout; all match prior recorded outputs | confirms the 2026-09-21 split/move did not break any invocation |

### Left unfixed (checkpoint: needs Sam)
- DRAGEN MAPQ row: Illumina-licensed hardware/software, no public install path. Needs a DRAGEN
  licence/instance or a real DRAGEN BAM to inspect.
- Cell Ranger itself (STARsolo now verified as its stand-in for MAPQ/CB/UB behaviour): 10x Genomics
  gates the download behind account registration. Needs that registration or a real Cell Ranger BAM.

Full detail: `F:\OpenScience\audits\_final_pass\bio-sam-bam-basics\CHECKPOINT.md`.

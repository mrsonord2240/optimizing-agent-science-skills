# bio-reference-operations — fix log (2026-09-20)

Skill `alignment-files/reference-operations`, branch `fix/af-refops` (worktree `F:\OpenScience\wt\af-refops`, from staging `1e96d8e`).
Evidence: `F:\OpenScience\audits\bio-reference-operations\` (first audit 74, Beta Only, not deployable, assertions 15/25, no veto, no P0, 4 P1, 3 P2).
Tools on every run (WSL `science`, env `alignment-files` via `wsl_run.sh`): samtools 1.24 (htslib 1.24), bcftools 1.24, pysam 0.24.1, Python 3.12.14, GATK 4.6.2.0, Picard 3.5.0 (side env `af-picard3`), minimap2 not re-run (block unchanged).
Test data: the audit's synthetic 3-contig reference + planted-truth BAM (`data\synthetic`), the real chr22 slice / nf-core CRAM / SARS-CoV-2 Illumina BAM (`public-data`), the NCBI GRCh38 assembly report and 1000G `.fai` the audit fetched, plus fixtures I built in `F:\OpenScience\af-refops-scratch` (a graded-allele-fraction BAM with 5% ... 50% minor-allele columns; a BAM whose reads carry `SA:Z`/`XA:Z` tags). Sources fetched 2026-09-20: NCBI `README_analysis_sets.txt`, UCSC `hg38.chrom.sizes` / `hg19.chrom.sizes`, Broad `Homo_sapiens_assembly38.fasta.fai`, 1000G `hs37d5.fa.gz.fai`, NCBI GRCh37 assembly report, Ensembl REST `info/assembly/homo_sapiens` + GRCh38 primary-assembly FASTA header.
Harnesses (scratch, not shipped): `t_py.py` extracts every ```python block from the final SKILL.md and runs it; `t_cli.py` extracts the ```bash blocks and runs them verbatim in clean directories; both assert on output against a second method (samtools consensus, raw pysam counts, independent md5, Picard, GATK). Result: 54 + 19 checks pass; the one failing check in `t_cli.py` is a superseded test line (it read the CRLF assembly report without stripping CR; the shipped map line does `tr -d '\r'` and its own check passes).

## Findings

| # | finding | pri | change | verified | notes |
|---|---|---|---|---|---|
| 1 | Python `build_consensus` / `simple_consensus` / `compare_to_ref` drop uncovered columns, shift after any gap (581 differences vs 1 true on the real slice); compare is case-sensitive | P1 | One `build_consensus` starts from `['N'] * (end - start)` and fills by `pileup.reference_pos`, so index `i` is position `start + i`; `max_depth` raised; one `compare_to_ref` (moved from the guide) upper-cases the reference and returns 1-based positions; pysam `pileup()` filter defaults (Q<13, dup/secondary/QC-fail/orphan, overlap dedup, `max_depth` 8000) stated; the false "ignores base qualities" wording replaced | ran (verbatim from SKILL.md) on the real slice 1952-4617: 2666 chars (old: 1157), 1 difference `(3266, T, C)` == samtools consensus `-m simple --call-fract 0.5 --min-BQ 13 -a --show-del yes --show-ins no` (also 1); old function still reproduces 581; equal to raw pysam majority at all 968 columns with depth>=10 & top>=90%; equal to samtools consensus at all 1015 columns where both call ACGT; 1485 uncovered positions all N in place; lower-case reference gives the same 1 difference; region 0-6000 and 39000-41000 (past contig end) give exact lengths; synthetic gap: 1700 chars (old 1200), min_depth=1 columns 1520-1699 equal the reference except the planted alt | Bayesian samtools consensus reports 2 differences (extra call at 2123: depth 3, C@Q34 and C@Q24 vs G@Q62): documented as quality weighting, not a defect |
| 2 | `--het-fract` / `--call-fract` no-ops in default mode; `-a` misdescribed; "verify via `--help`" exits 1 | P1 | Both flags stated to act only with `-m simple` (semantics: het-fract = min ratio 2nd/top, needs `--ambig`, pass explicitly because the omitted default is not the printed 0.15; call-fract = agreeing fraction else N, default 0.75); `--het-scale` documented as the Bayesian knob; without `--ambig` an ambiguous column is N; `-a` = pad contig ends to header LN, `-aa` = also read-less contigs, internal gaps always N; `-a --show-del yes --show-ins no` = one char per reference position; the viral example lost `--het-fract 0.5` and `--show-del yes` (`*` in a FASTA), gained `--ambig -a`; option list via `samtools help consensus`; FASTQ wrap `-l 0`; `-T` keeps FASTA case | ran: Bayesian output byte-identical for `--het-fract 0.05/0.9`, `--call-fract 0.95/0.1`, with and without `--ambig`; `--het-scale 0.01` removes the 20% IUPAC call; graded fixture (5%..50% minor): `-m simple --ambig --het-fract 0.15` -> `AGWKSMKSSS`, `0.3` -> `AGTGSMKSSS`, omitted -> `AGTGCNKSSS` (15% column plain base), `--call-fract 0.9` -> `AGNNNNNNNN`, `0.6` -> `AGTGCAGCNN`; Bayesian `--ambig` -> `AKWKSMKSSS`; `-a` chr1 1700 -> 5000 with N tail, calls inside span identical, chrM only with `-aa` (1000 N); `-a --show-del yes --show-ins no` chr1 5000, chr2 3007 (3 `*`); `samtools help consensus` rc 0, `--help` rc 1 "unrecognized option"; `-l 0` FASTQ 8 lines / 2 records (default 62); `-T` fills the gap with lower-case reference bases; viral command on the real Illumina BAM: one record, `*`-free, padded with N | bcftools consensus default IUPAC note (finding 7) checked here too |
| 3 | RefSeq and 1000G rows of the contig / GRCh38 tables wrong; "re-align" advice wrong | P1 | GRCh38 table rebuilt from NCBI `README_analysis_sets.txt` and the `.fai`/`chrom.sizes` files (UCSC hg38.fa: 455 contigs, 261 `_alt`, no EBV; NCBI no_alt / no_alt+hs38d1 / full / full+hs38d1; 1000G `GRCh38_full_analysis_set_plus_decoy_hla` = bwakit hs38DH, same 3,366 contigs as Broad assembly38: 261 ALT, 2,385 decoy, 525 HLA, `chrEBV`); contig-naming table: RefSeq FASTA `NC_000001.11` / `NC_012920.1`, hg19 `chrM` (16,571 bp, NC_001807) is not GRCh37 `MT` (16,569), 1000G GRCh37 `hs37d5` `1`/`MT`, assembly-report column map (CRLF, cols 1/5/7/10); new "Rename Contigs Without Re-aligning" section: awk map -> `samtools reheader` -> index -> SN/LN check, sed one-liner for hg38 UCSC -> Ensembl, `SA:Z`/`XA:Z` tag caveat with `samtools view -x`, CRAM note | ran: counts from the fetched files (see sources above); block on the real BAM: renamed.bam records identical (md5) to the original except RNAME/RNEXT, `mpileup` identical (1157 lines), Picard 3.5.0 ValidateSamFile "No errors found" vs the `22`-named reference, region query `22:1952-4700` 5642 == `chr22:1952-4700`; assembly-report map line -> `chr22 NC_000022.11`, `chrM NC_012920.1`, `chr1 NC_000001.11` (709 rows), reheader + Picard "No errors found" against a reference named `NC_000022.11`; sed one-liner chr22 -> 22 (chrM -> MT, chr1 -> 1); CRAM reheader (warns, rc 0) decodes identical to the renamed original with `-T`; `SA`/`XA` keep old names after reheader and `-x SA -x XA` removes them | Ensembl scaffold names are GenBank accessions (checked in Ensembl REST `KI270757.1`), so column 1 only matches Ensembl for chromosomes |
| 4 | `prepare_reference.sh` names the dict `genome.fasta.dict` for `.fasta` (GATK rejects); guide's validate block prints DICT: OK for it; file listing printed twice | P1 | Script derives NAME (basename, drop `.gz`, drop last extension) and writes `<name>.dict` and `<name>.chrom.sizes`; `ls` lists only the three files; usage text lists the accepted extensions; SKILL.md states the naming rule with the GATK message; the SKILL "Check Reference Setup" block checks the derived name (guide copy deleted) | ran the shipped script on `genome.fasta`, `ref.fa`, `ref2.fna`, `my genome.fasta` (path with space), `dotted.v2/noext` (no extension, dot in directory), bgzipped `refz.fa.gz`: dicts `genome.dict`, `ref.dict`, `ref2.dict`, `my genome.dict`, `noext.dict`, `refz.dict`, each `.chrom.sizes` beside it; no-arg and missing file rc 1. **GATK 4.6.2.0 HaplotypeCaller** loaded all four of genome.fasta, ref.fa, ref2.fna, refz.fa.gz (no USER ERROR, VCF written) — the old script's `genome.fasta.dict` failed with `Fasta dict file .../genome.dict ... does not exist`; Picard CreateSequenceDictionary on `genome.fasta` gives SN/LN/M5 identical to `samtools dict` (`chr22 40001 1922b52e...`); Picard 3.5.0 ValidateSamFile against `genome.fasta` "No errors found"; check block: correct dict -> DICT: OK, `genome.fasta.dict` only -> `DICT: MISSING (./genome.dict)`, `ref.fa.gz` + `ref.dict` -> OK; `bash -n` passes | |
| 5 | Unguarded recipes exit 0 after partial failure; `$REF_CACHE_DIR` undefined; multi-region loop prints empty records | P2 | Subset recipe chained with `&&` (faidx exits 1 on a missing contig) and gains the `samtools dict` step from the guide; `REF_CACHE_DIR=$HOME/ref_cache` + `mkdir -p` + quoted; added the `REF_PATH=.../%2s/%2s/%s` decode line; multi-region pysam loop (moved from the guide) clips `end` to the contig length and skips regions outside it | ran: subset with absent chr3 rc 1, no `subset.dict`; with existing contigs rc 0, `.fai` and a 3-`@SQ` dict; cache block with `HOME` set: `19/22/b52e1af6977302717072ebaca0a1` created, CRAM decoded with no `-T` (>=5 records); multi-region loop on the 5 kb / 3 kb synthetic reference: `>chr1:1-5000`, `skip chr2:5001-3007` | |
| 6 | Troubleshooting titles do not match tool messages; "index first" advice; `-i` header; FASTQ wrap | P2 | New "faidx Errors (samtools 1.24)" table with the real messages and exit codes; auto-index noted; `-i` adds `/rc` (`--mark-strand no`); FASTQ `-l 0` (finding 2) | ran: wrong contig rc 1 `Failed to fetch sequence in 22:1-100`; missing FASTA rc 1 `Failed to open the file` + `Could not load fai index`; region past the end rc 0, `Zero length sequence` + empty record; `.fai` removed then rebuilt by a region request; `-i` header `>chr1:1000-2000/rc`, `--mark-strand no` plain | |
| 7 | Redundancy and small doc defects (three consensus copies, min_depth 3 vs 5, unlabelled 0-based print, `create_dict_header` is not a .dict, bcftools het IUPAC default, VN 1.0 vs 1.6) | P2 | See "Redundancy"; one `build_consensus` (min_depth 3 everywhere); print now `chr1:1000001` for the 0-based argument; `create_dict_header` retitled "Header Dict for Writing a BAM (not a .dict file)" with the no-M5 note; bcftools consensus note: het SNPs -> IUPAC without `-H`, `-H 1/2`, `-H A` / `-s -` for all ALT; dict `@HD VN:1.0` confirmed (pysam's VN 1.6 is a different object) | ran: `consensus_at_position` hom-alt -> alt, gap -> N; `create_dict_header` on the 3-contig reference prints 5,000 / 3,007 / 1,000 bp; `samtools dict` `@HD VN:1.0 SO:unsorted`, M5 == independent md5 of the uppercase sequence for all three contigs, `-a/-s` adds `AS:GRCh38 SP:Homo sapiens`; bcftools 1.24 on the synthetic VCF: default `M`,`M` (pos 401/601), `-H 1` `C`,`A`, `-H 2` `A`,`C`, `-H A` and `-s -` `C`,`C` | |

Findings fixed 7/7 (4 P1, 3 P2).

Missing referenced executables: `seq_cache_populate.pl` (already runnable, now verified), `bcftools consensus`, `minimap2 -a` (unchanged, audited). The one unbacked mention, Pilon / medaka ("prefer Pilon or medaka for assembly polishing"), is **deleted**: neither is installed and polishing is outside the Skill; the boundary sentence "not iterative, not an assembly-polishing tool" stays. `compare_to_ref` (guide-only, referenced by the prompt "compare consensus to reference") moved into SKILL.md and fixed.

## Redundancy (Sam's every-pass rule)

Frontmatter untouched. SKILL.md 377 -> 456 lines (new content: faidx errors, dict naming, corrected tables, rename recipe, consensus-mode semantics, the moved multi-region / compare functions); usage-guide 251 -> 53 lines.

| deleted | now |
|---|---|
| usage-guide "Prerequisites" (conda / pip install) | SKILL.md Version Compatibility "Install:" line; guide points to it |
| usage-guide "Reference File Types" table (FASTA / FAI / dict) | SKILL.md faidx / dict sections; `<name>.dict` naming rule added under "Create Dictionary" |
| usage-guide "Common Commands": Create FASTA Index, Create Sequence Dictionary, Extract Sequences | SKILL.md Create Index, Fetch Region/Multiple/Entire, Reverse Complement, Create Dictionary |
| usage-guide "Generate Consensus" list (`-a "Include N for no coverage"` was wrong) | SKILL.md Basic / Region / Output Formats / Quality Options (with the corrected `-a`) |
| usage-guide "Prepare Reference for Analysis" (`bwa index`, chrom.sizes) | SKILL.md Reference Preparation Workflow (`prepare_reference.sh`, Get Chromosome Sizes); `bwa index` was already pointed to read-alignment |
| usage-guide "Create Subset Reference" (chr1..chrM block, unguarded) | SKILL.md Subset Reference (guarded, with the dict step) |
| usage-guide "Fetch Sequences", "Get Reference Info" (pysam) | SKILL.md Fetch from Indexed FASTA, Get Reference Lengths |
| usage-guide "Extract Multiple Regions" (empty records past contig end) | SKILL.md "Fetch Several Regions (0-based)", clipped |
| usage-guide `simple_consensus` (min_depth 5) | deleted; SKILL.md `build_consensus` is the single copy (min_depth 3, aligned) |
| usage-guide `compare_to_ref` | SKILL.md "Compare Consensus to Reference (Python)", fixed |
| usage-guide "FAI File Format" | SKILL.md FAI File Format (same content) |
| usage-guide Troubleshooting (faidx not found / invalid region / CRAM needs reference / Validate Reference Setup) | SKILL.md faidx Errors table (real messages), Prepare Reference for Analysis (CRAM `-T`), Check Reference Setup (derived dict name) |
| usage-guide Tips (both indices, 0- vs 1-based, min depth, exact names, CRAM `-T`, chrom sizes) | SKILL.md dict naming, Fetch Several Regions, Quality Options `-d`, Contig Naming, Prepare Reference for Analysis, Get Chromosome Sizes |
| SKILL.md "Quick Reference" table | each row already has its own section |
| SKILL.md workflow steps 1-2 (faidx, dict one-liners) | Create Index / Create Dictionary; workflow points to them and to `prepare_reference.sh` |
| SKILL.md platform block's repeated default-consensus command | Basic Consensus / Output Formats |
| SKILL.md Pilon / medaka sentence | deleted (see above) |

Disagreements between copies, resolved by what the audit's runs support: min_depth 3 (SKILL) vs 5 (guide) -> 3; `-a` "call all positions" (SKILL) vs "include N for no coverage" (guide) -> neither; replaced by the verified pad-to-reference-end behaviour.

## Not fixed

- Audit static note "description omits faidx extraction and CRAM references": the description is not wrong, left unchanged.
- Audit maintainability note "no test data or expected output": not added (new content); the checked values are in this log.
- Audit security note "`samtools dict -o` silently overwrites an existing dict": `prepare_reference.sh` is idempotent by design and regenerates the dict; not changed.
- `-T` "added in samtools 1.22" and `--config` "1.17+" version notes carried over unchanged: 1.24 is the only version available to check them on.

## Compile / syntax

No `.py` shipped. `bash -n examples/prepare_reference.sh` passes; the script was run from a copy against six reference names plus the error paths (see finding 4). All SKILL.md fenced python / bash blocks run from the final file by the harnesses above.

# bio-reference-operations - fix log (2026-09-21)

Skill `alignment-files/reference-operations`, branch `fix/reference-operations` (worktree `F:\OpenScience\wteference-operations`, from staging `431aa55`). Commits: `8f275d2` (fixes), `5d5e5f0` (split).
Evidence: latest re-audit `F:\OpenScienceuditsio-reference-operations\` (85, Production Ready, deployable, no veto, no P0, 1 P1, 4 P2).
Tools (WSL `science`, env `alignment-files`): samtools 1.24, pysam 0.24.1, GATK 4.6.2.0, Picard 3.5.0. Data: 1000G HG00349 chr20 slice (hs38DH header, 3,366 contigs) + the audit's GRCh38 assembly report, the audit's planted BAM/FASTA, the chr22 slice, a 5 kb / 3 kb synthetic reference. Scratch: `F:\OpenSciencef-refops21`.

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| Reheader recipe fails on full hg38 headers (map emits `na`), leaves 0-byte output | P1 | awk filter `$10!="na" && $7!="na"`; reheader writes `renamed.bam.tmp`, `mv` on success | ran the SKILL block verbatim on HG00349: rc 0, 451 of 3,366 contigs renamed (25 NC_, the rest NT_/NW_), records identical to the original except RNAME/RNEXT (md5 of the other columns equal); old recipe reproduced rc 1 "Duplicate entry na", 0-byte file | |
| `-T` described as filling low coverage | P2 | now "columns with no reads (depth 0)", below-`-d` and ambiguous columns stay N, with the planted numbers | ran planted BAM `-d 3`: 450 N -> 150 N with `-T`; `-d 30`: 6224 -> 5924 | |
| Description omits renaming / extraction / CRAM | P2 | description extended | read | frontmatter `name` untouched |
| bgzip requirement, no test data | P2 | one line + `gunzip -c ... \| bgzip` recipe under Create Index; `examples/toy.fa` + `examples/toy.expected.dict`; usage line of `prepare_reference.sh` says bgzip | ran: plain gzip rc 1 with the "please use bgzip" message, bgzip recipe indexes; toy M5 == independent md5 of the sequence; `prepare_reference.sh toy.fa` dict equals expected; `samtools dict -u toy.fa toy.fa \| diff - toy.expected.dict` empty | |
| Picard accepts `genome.fasta.dict`, only GATK ignores it | P2 | sentence and script comment name GATK | ran: Picard ValidateSamFile "No errors found" with only `genome.fasta.dict`; HaplotypeCaller USER ERROR with it, runs after rename to `genome.dict` | |
| chr22 "1 vs 2 differences" needs `-d 3` | P2 | window, `-d 3` and the `-d 1` numbers (5 / 4) stated | ran: 1952-4617 simple -d 1 -> 5 diffs, Bayes -d 1 -> 4; -d 3 -> 1 / 2 | |
| Dict example `UR:file:reference.fa` | P2 | absolute `file:///` shown, `-u` noted | samtools dict output | |
| sed UCSC->Ensembl rewrote non-primary contigs | P2 | regex limited to `chr1-22/X/Y/M`, comment says the rest keep names | ran on the hs38DH header: 25 primary renamed, 1 `MT`, 18 `chr1_KI...` kept | Ensembl names scaffolds by accession, so kept UCSC names still mismatch Ensembl; already stated in Contig Naming |
| Multi-region skip message printed `chr2:5001-3007` | P2 | prints requested end and contig length, clips after the check | ran on 5 kb / 3 kb reference: `skip chr2:5001-15000: outside the contig (3007 bp)`, `>chr2:1001-3007` 2007 bases | |
| `compare_to_ref` / `build_consensus` N, IUPAC, deletion, insertion behaviour unstated | P2 | two sentences added | audit run values (30 N-run + 2 IUPAC listed as differences) | |
| Unreproduced claim: CRAM reheader warns "Failed to populate reference" | audit note | claim replaced by what was checked (exit 0, M5 kept, identical decode with `-T`) | ran: CRAM reheader chr22->22 rc 0, `-T` decode 5,644 records | I also saw no warning, so the old sentence could not be supported |

## Redundancy (this pass)

No new duplicates introduced. The bgzip line, GATK/Picard naming, `-T` wording and the `-d 3` numbers each replaced text in place; the script comment is a shipped-file note, not a restatement.

## Split into `references/` (SKILL.md 461 -> 280 lines)

Moved verbatim: `references/contig-naming.md` (GRCh38 flavours, contig naming, rename without re-aligning), `references/consensus-modes.md` (IUPAC/`--het-fract`/`--call-fract`/`--het-scale`, platform `--config`, `-T`, samtools vs bcftools consensus), `references/python-consensus.md` (simple/build consensus, `compare_to_ref`, header dict). SKILL.md gained pointers in the intent list and a Reference Files table. Check: every non-blank line of the pre-split SKILL.md is present in SKILL.md or a reference file except the two lines rewritten to carry pointers; the 3 python fences `ast.parse`, all 23 bash fences pass `bash -n`; the rename block ran from the split file's text (see above).

## Left unfixed

- Audit static note "no test data or expected output" beyond the toy: a real-genome sample cannot ship (size/licence); the toy FASTA + expected dict is the shippable part, done.
- Audit assertion that the CRAM `Failed to populate reference` warning was not reproduced: I did not reproduce it either, so the claim was deleted rather than fixed (see table).
- `-T` added "in samtools 1.22" / `--config` "1.17+" version notes: still only samtools 1.24 available to check them.

## 2026-09-21 (structure)

Branch `fix/reference-operations`, commit `refactor(alignment-files/reference-operations): move runnable code to scripts/` on top of `5d5e5f0`. No behaviour or claim changed.

**Split:** none. SKILL.md is 279 -> 281 lines (two rows added to the Reference Files table), under 300; it already has three `references/` files.

**Moved to `scripts/`**

| old location | script | how it was run |
|---|---|---|
| `references/python-consensus.md` `build_consensus` + `compare_to_ref` (verbatim functions, CLI wrapper added) | `scripts/pysam_consensus.py` (`consensus`, `compare`) | from the skill dir as the md now invokes it, on the audit's real chr22 slice (`run/data/real`): `compare ... chr22 1951 4617 --min-depth 3` -> exactly 1 line (`3266 T C`); `consensus` length 2666; planted BAM ran. pysam 0.24.1 |
| `references/contig-naming.md` rename block (awk header rewrite, `reheader` via `.tmp`+`mv`, index, name/length check) | `scripts/rename_contigs.sh in.bam map.tsv out.bam [ref.fa]` | synthetic `synth_chr.bam` with a chr->numeric map: rc 0, prints `OK` against `synth_numeric.fa.fai`, records identical except RNAME; HG00349 hs38DH slice with the GRCh38 assembly-report map: rc 0, 3,366 `@SQ`, 25 renamed to `NC_`, records identical; missing map -> nonzero and no output file. samtools 1.24 |

The pre-map `awk` line that builds `map.tsv` from the assembly report and the `sed` UCSC->Ensembl variant stay inline (one line each); the sed variant now ends with its own `reheader` + `index` line (before, it wrote `renamed.hdr` and relied on the reheader above it) and ran on the HG00349 header (`chr20` -> `20`). The script's optional 4th argument replaces the separate inline "Check" block.

**Stayed inline:** `consensus_at_position` (single-position teaching snippet, superseded by `build_consensus`), the header-dict `create_dict_header` snippet (16 lines, teaching; run in the earlier pass), the 8-line "Check Reference Setup" block, all one-to-five-line samtools recipes. `examples/prepare_reference.sh` already is the script for the prepare-reference workflow.

Checks: all python fences `ast.parse`, all bash fences `bash -n`; scratch and test data under `F:\OpenScience\f-refops-struct` (audit data copied, not written to).

Noticed, not changed (claim, out of this pass): `python-consensus.md` says the chr22 slice at `-d 1` gives "5 and 4"; the majority-vote script gives 6 at `--min-depth 1`, while `samtools consensus -m simple --call-fract 0.5 --min-BQ 13 -d 1` gives 5 and Bayesian 4. The "1 and 2" at `-d 3` reproduces.

> **Audit record for `bio-reference-operations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@0d22089](https://github.com/mrsonord2240/bioSkills/tree/0d22089b40e9195801f3980b64fcbb24ed4e278f/alignment-files/reference-operations) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-reference-operations (re-audit of the fixed Skill)

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@0d22089b40e9195801f3980b64fcbb24ed4e278f:alignment-files/reference-operations` | Category: Data Analysis | Mode: B | Complexity: Moderate | N = 8 (5 regression + 3 new)

Pre-fix report (archived): 74, Beta Only, 15/25 assertions, 4 P1 + 3 P2. Fix log read but not used as evidence. Everything below is from my own runs; scripts in `run/`, raw output in `run/logs/`. All tests ran in WSL `science` (env `alignment-files`, samtools 1.24, bcftools 1.24, pysam 0.24.1, GATK 4.6.2.0, Picard 3.5.0) from a COPY of the Skill (`run/skill`, byte-identical to the worktree at 0d22089; the worktree was not written to and holds no `__pycache__`).

## Skill Veto

T1 Stability PASS | T2 Contract PASS | T3 Determinism PASS | T4 Security PASS

- stability: every block/script ran; no crashes or loops. The one documented recipe that fails (reheader on a full hg38 header) fails loudly, not randomly.
- contract: frontmatter has name, description, tool_type, primary_tool, license.
- determinism: `samtools consensus --ambig -d 3` gave one md5 (`bdc7098e...`) on 3 runs; all outputs reproduced on the second pass of `run_all.sh`.
- security: no eval/exec; a file named `we"ird'name.v2.fasta` inside a directory named `h;x $(echo pwned)` went through `prepare_reference.sh` and `pwned` was never executed.

## Static score (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 10/12 | Completeness 3, Correctness 3, Appropriateness 4. Far more of the body is verified than before (tables, consensus flags, dict naming, Python consensus). Left: the reheader recipe fails on a full hg38 header (map emits "na"), -T is described as filling "low coverage" (it fills only zero-coverage columns), plain-gzip .gz references fail (bgzip never mentioned). |
| reliability | 10/12 | Fault tolerance 3, Error reporting 4, Recoverability 3. faidx error table matches real messages and exit codes; subset recipe stops on a missing contig; script exits 1 on no-arg/missing file and is idempotent. The reheader recipe leaves a 0-byte renamed.bam when it fails. |
| performance_context | 6/8 | Token cost 3, Efficiency 3. One copy of every recipe now; SKILL.md grew 377 -> 456 lines, guide shrank 251 -> 53. The consensus and contig sections are dense but each line earns its place. |
| agent_usability | 14/16 | Learnability 3, Consistency 4, Feedback design 3, Error prevention 4. min_depth is 3 everywhere, one -a description, explicit traps (--ambig required, omitted --het-fract is not 0.15, dict name rule, primary-only sed, ties). A few numbers are stated without the flag that produces them (chr22 1-vs-2 differences needs -d 3). |
| human_usability | 6/8 | Discoverability 3, Forgiveness 3. The description still names only consensus/indexing/dictionaries although the body (and the usage-guide prompts) now cover contig renaming, GRCh38 flavour, CRAM references and extraction. faidx auto-indexing and the error table forgive most slips. |
| security | 11/12 | No credentials, every expansion quoted; a file name containing ; $( ) " and a single quote went through prepare_reference.sh without executing anything. samtools dict -o overwrites an existing dict by design. |
| maintainability | 8/12 | Modularity 3, Modifiability 3, Testability 2. Single copy of each snippet and dated version notes (checked: -T is in 1.22, instrument --config in 1.17, -aa in 1.18 per NEWS). Still no shipped test data or expected outputs; one script. |
| agent_specific | 17/20 | Trigger precision 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 3. All 8 Related Skills paths resolve; pedagogical-only warning and not-polishing boundary kept; description under-triggers relative to the body. |

**Static subtotal: 82/100** (first audit 72)

## Classification

Data Analysis (category 3), Mode B (CLI/script: `samtools`, `bcftools`, `examples/prepare_reference.sh`, plus pysam snippets). Complexity Moderate; N = 8 because the brief requires the 5 pre-fix inputs as regression tests plus at least 2 new ones.

## Summary Table

| Input | Type | Kind | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | regression | 35 | 54 | 89 | 5/5 PASS | ✅ |
| 2 | Variant A | regression | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 3 | Edge | regression | 30 | 46 | 76 | 4/5 PASS | ✅ |
| 4 | Variant B | regression | 35 | 53 | 88 | 4/5 PASS | ✅ |
| 5 | Stress | regression | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 6 | Adversarial | new | 34 | 52 | 86 | 4/5 PASS | ✅ |
| 7 | Edge | new | 34 | 52 | 86 | 4/4 PASS | ✅ |
| 8 | Variant B | new | 37 | 56 | 93 | 5/5 PASS | ✅ |

**Execution average: 87.5 / 100** (first audit 74.6) | **Assertion pass rate: 36/39** (first audit 15/25) | Layer 1 avg 34.6/40, Layer 2 avg 52.9/60

### Regression against the first audit

| Pre-fix finding | Now |
|---|---|
| P1 build_consensus / simple_consensus / compare_to_ref shift after any gap (581 false differences) | Fixed. Exact length, equals mpileup majority and samtools consensus at every jointly called column on real and planted data (inputs 5, 6). |
| P1 --het-fract/--call-fract no-ops in default mode; -a misdescribed; "verify via --help" exits 1 | Fixed. Verified on a 48-configuration grid I predicted independently (input 8); `samtools help consensus` rc 0 confirmed. |
| P1 RefSeq / 1000G rows wrong; "re-align" advice wrong | Fixed. Table figures match the real files (input 3). New defect found in the new recipe (P1 below). |
| P1 prepare_reference.sh / validate block name the dict wrongly for .fasta and .fa.gz | Fixed. GATK 4.6.2.0 and Picard 3.5.0 load all 9 claimed shapes (input 1). |
| P2 unguarded recipes, undefined $REF_CACHE_DIR, empty records | Fixed. && chains stop, cache block builds the cache and decodes 5,644 records with no -T, multi-region loop clips. |
| P2 troubleshooting titles vs real messages; "index first" | Fixed. The faidx error table strings and exit codes match samtools 1.24. |
| P2 redundancy: three consensus copies, min_depth 3 vs 5, VN, IUPAC default | Fixed. One build_consensus (min_depth 3), guide is 53 lines. |

### Judged as the fixer left them

- **Description** (unchanged): still consensus / indexing / dictionaries only; the body now also handles contig renaming, GRCh38 flavour, CRAM references. Under-triggers (P2).
- **Missing test data** (not added): no sample data or expected output shipped; testability stays 2/4 (P2 with the bgzip gap).
- **Version notes** (carried over): `-T` in 1.22, instrument `--config` in 1.17 and `-aa` in 1.18 are all correct per the samtools NEWS (`run/logs/r0_news.txt`). Nothing to change.
- **Pilon/medaka** mention: gone; the boundary sentence "not iterative, not an assembly-polishing tool" remains and is true.
- **usage-guide.md dedup** (251 -> 53 lines): I compared every deleted section with SKILL.md. Everything an agent needs survives (install line, faidx/dict/consensus commands, subset, sizes, CRAM `-T`, troubleshooting -> error table, tips -> their sections). Lost only: the tip "keep index files beside the FASTA" and a `nreferences` print; neither matters.
- **Fix-introduced or left defects**: see recommendations. Nothing in the fix broke a previously working statement.

## Detailed outputs

### Input 1 — Canonical (regression): Prepare a reference for GATK/Picard: index, dict, chrom.sizes for 12 filename shapes

**Prompt:** I need to prepare my reference genome for GATK and Picard: index it, make the sequence dictionary and chrom sizes. My file is called genome.fasta (other times ref.fa, ref2.fna, GRCh38.primary_assembly.fa.gz, hg38.p14.v2.fasta).

**Mode / execution:** B; executed: true; scripts: r1_prepare.sh, r1_consume.sh, r1_check.py, r1c_picard_dict.sh

**Log `run/logs/r1_consume.txt`: 0 PASS lines; non-PASS lines (observations and FAILs) below**

```
s1/genome.fasta | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s2/ref.fa | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s3/ref2.fna | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s4/refz.fa.gz | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s5/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s6/hg38.p14.v2.fasta | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s7/genome.fna.gz | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s8/genome.fasta.gz | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s9/my genome.fasta | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
s10.v2/noext | GATK rc=3 USER_ERROR=0 vcf_has_#CHROM= | Picard rc=255 no_errors=0 | ERROR	2026-09-20 06:13:20	ValidateSamFile	File is not a supported reference file type: /mnt/openscience/audits/bio-reference-operations/run/work/r1/s10.v2/noext
s11/GENOME.FA | GATK rc=3 USER_ERROR=0 vcf_has_#CHROM= | Picard rc=255 no_errors=0 | ERROR	2026-09-20 06:13:23	ValidateSamFile	File is not a supported reference file type: /mnt/openscience/audits/bio-reference-operations/run/work/r1/s11/GENOME.FA
s12/ref.fas | GATK rc=0 USER_ERROR=0 vcf_has_#CHROM=1 | Picard rc=0 no_errors=1 | No errors found
##### NEGATIVE CONTROL: only the OLD name genome.fasta.dict present (pre-fix behaviour)
GATK rc=2
A USER ERROR has occurred: Fasta dict file file:///mnt/openscience/audits/bio-reference-operations/run/work/r1/neg/genome.dict for reference file:///mnt/openscience/audits/bio-reference-operations/run/work/r1/neg/genome.fasta does not exist. Please see https:/
No errors found
```

**Log `run/logs/r1c_picard_dict.txt`: 0 PASS lines; non-PASS lines (observations and FAILs) below**

```
== only_fasta_dot_dict: picard ScatterIntervalsByNs rc=0 out_lines=1 :: 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
== only_genome_dot_dict: picard ScatterIntervalsByNs rc=0 out_lines=1 :: 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
== none: picard ScatterIntervalsByNs rc=1 out_lines= :: Exception in thread "main" java.lang.IllegalStateException: Reference file must include a dictionary, but no dictionary file was found 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
```

**Log `run/logs/r1_check.txt`: 37 PASS lines; non-PASS lines (observations and FAILs) below**

```
independent M5 of the chr22 slice: 1922b52e1af6977302717072ebaca0a1
SUMMARY: 37/37 checks passed; FAILS=[]
```

PASS checks: s1/genome.fasta: genome.dict exists, SN=chr22 LN=40001 M5==independent md5; s1/genome.fasta: genome.chrom.sizes == "chr22<TAB>40001"; s1/genome.fasta: SKILL "Check Reference Setup" block prints FAI/DICT/Fetch OK -- FAI: OK | DICT; s2/ref.fa: ref.dict exists, SN=chr22 LN=40001 M5==independent md5; s2/ref.fa: ref.chrom.sizes == "chr22<TAB>40001"; s2/ref.fa: SKILL "Check Reference Setup" block prints FAI/DICT/Fetch OK -- FAI: OK | DICT: OK (; s3/ref2.fna: ref2.dict exists, SN=chr22 LN=40001 M5==independent md5; s3/ref2.fna: ref2.chrom.sizes == "chr22<TAB>40001"; s3/ref2.fna: SKILL "Check Reference Setup" block prints FAI/DICT/Fetch OK -- FAI: OK | DICT: OK; s4/refz.fa.gz: refz.dict exists, SN=chr22 LN=40001 M5==independent md5; s4/refz.fa.gz: refz.chrom.sizes == "chr22<TAB>40001"; s4/refz.fa.gz: SKILL "Check Reference Setup" block prints FAI/DICT/Fetch OK -- FAI: OK | DICT: ; ...

**Scores:** Basic 35/40 | Specialized 54/60 | Total 89/100

**Assertions:**
- [PASS] prepare_reference.sh writes <name>.dict and <name>.chrom.sizes for .fa, .fasta, .fna, bgzipped .fa.gz/.fna.gz/.fasta.gz, dotted names, a name with a space, and a hostile name (; $( ) " ') — dicts named genome.dict, ref.dict, ref2.dict, refz.dict, Homo_sapiens.GRCh38.dna.primary_assembly.dict, hg38.p14.v2.dict, my genome.dict
- [PASS] GATK 4.6.2.0 HaplotypeCaller (VCF with #CHROM, no USER ERROR) and Picard 3.5.0 ValidateSamFile ("No errors found") load the result for all 9 claimed shapes plus .fas — noext and GENOME.FA are rejected by the tools themselves ("not a supported reference file type"), not by the Skill; negative control (old genome.fasta.dict only) reproduces the GATK USER ERROR
- [PASS] .dict SN/LN/M5 equals an independent md5 of the upper-cased sequence in all 12 dicts; chrom.sizes exact; Picard-made dict identical on the planted N/IUPAC reference — 37/37 checks in r1_check.py; r6 part A
- [PASS] The "Check Reference Setup" block prints DICT: OK (derived name) for every shape and DICT: MISSING when only genome.fasta.dict exists — verbatim block, REF substituted
- [PASS] Error paths exit 1 with a message (no argument, missing file, plain-gzip .gz); re-run is byte-identical — plain gzip fails with samtools "please use bgzip"; neither the Skill nor the script usage line mentions bgzip (P2)

**Note:** All claimed shapes load in GATK and Picard; only gaps are undocumented bgzip need and a Picard-specific over-statement (Picard 3.5.0 also accepts genome.fasta.dict).

### Input 2 — Variant A (regression): Extract regions / revcomp / subset / pysam multi-region, error table

**Prompt:** Extract chr1:1000-2000, several regions, the reverse complement, a whole chromosome, and make a chr1-chr2-chrM subset reference; tell me what happens if I ask for a contig that is not there.

**Mode / execution:** B; executed: true; scripts: r2_extract.py

**Log `run/logs/r2_extract.txt`: 24 PASS lines; non-PASS lines (observations and FAILs) below**

```
{'chr1': 5000, 'chr2': 3007, 'chrM': 1000}
[W::fai_get_val] Reference 22:1-100 not found in FASTA file, returning empty sequence
[faidx] Failed to fetch sequence in 22:1-100
[faidx] Could not load fai index nofile.fa.fai
[W::fai_get_val] Reference chr3 not fo
multi-region output headers: ['>chr1:1-5000', 'skip chr2:5001-3007: outside the contig']
SUMMARY: 24/24 checks passed; FAILS=[]
```

PASS checks: SKILL faidx chr1:1000-2000 == independent 1-based inclusive slice (1001 bases), header chr1:100; faidx auto-indexed (SKILL: builds the .fai itself the first time); soft-mask case preserved by faidx (chr1:1001-1300 all lowercase); 3 requests -> 3 records equal independent slices; SKILL -i: header chr1:1000-2000/rc, seq == revcomp(independent slice) -- chr1:1000-2000/rc; SKILL --mark-strand no: plain header, still revcomp; Errors table row 1: wrong contig name -> rc 1, [faidx] Failed to fetch sequence in 22:1-100 -- ; Errors table row 2: missing FASTA -> rc 1, Failed to open the file ... Could not load fai index; Errors table row 3: region beyond contig end -> rc 0, [faidx] Zero length sequence, empty recor; overlapping the contig end -> clipped to 11 bases, rc 0 -- [faidx] Truncated sequence: chr1:499; SKILL names are the first word of each > line: fai name = chrX -- chrX; FAI columns for chr1: name,len,offset,linebases,linewidth = chr1,5000,offset,80,81 -- ['chr1', ; ...

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**
- [PASS] faidx region, multi-region, whole contig and -i/--mark-strand output equal an independent 1-based inclusive slice of the FASTA (case and N run preserved) — synthetic 3-contig reference with widths 80/60/70, soft-mask, N run
- [PASS] The faidx error table rows are true: wrong contig rc 1 "Failed to fetch sequence in 22:1-100"; missing FASTA rc 1; region past the end rc 0 "Zero length sequence"; auto-index without prior faidx — exact stderr strings match
- [PASS] Subset recipe stops (rc 1, no subset.dict) on a missing contig and writes fai + 3-@SQ dict when contigs exist — chr3 absent -> chain rc 1; chr1 chr2 chrM -> LN 5000/3007/1000
- [PASS] pysam blocks run verbatim; the multi-region loop clips to the contig end and skips an outside region without printing an empty record — skip message reads "chr2:5001-3007" (start > end), cosmetic
- [PASS] Extracted sequences equal external truth: Ensembl REST chr20:1,400,001-1,500,000 (100,000 bp) and SARS-CoV-2 S gene (3,822 nt ATG...TAA) — 24/24 checks in r2_extract.py

**Note:** Every extraction claim reproduces; error table now matches real tool messages.

### Input 3 — Edge (regression): chr22 vs 22, GRCh38 flavour/contig tables against real files, reheader recipe (BAM, CRAM, VCF)

**Prompt:** My BAM says chr22 but my reference says 22 (and another BAM is on a full hs38DH header): fix it without re-aligning, tell me which GRCh38 this is, and what the Ensembl/RefSeq/UCSC names are. Same for a CRAM.

**Mode / execution:** B; executed: true; scripts: r3_contigs.py, r3b_mito.sh, r0_news.sh

**Log `run/logs/r3_contigs.txt`: 36 PASS lines; non-PASS lines (observations and FAILs) below**

```
##### A. table spot-checks against real files
    n mapped UCSC->RefSeq rows: 709 (hg38 UCSC contigs: 455 )
    hg38.fa contigs NOT in the report map: [] 0
##### B. reheader recipe on real data
5642
< SN:22 LN:40001
---
> SN:22 LN:40000
< SN:22 LN:40001
---
> SN:chr22 LN:40001
    verbatim block on the full hs38DH header -> rc=1 | [E::sam_hrecs_update_hashes] Duplicate entry "na" in sam header | [main_reheader] failed to read the header for 'renamed.hdr'.
    renamed: 451 unchanged: 2915 | chr20 -> NC_000020.11 | chrM -> NC_012920.1 | HLA / decoy / EBV kept: chrEBV
    sed one-liner output names (first 5, and a few non-primary): ['1', '2', '3'] ['1_KI270706v1_random'] ['Un_KI270302v1'] ['HLA-A*01:01:01:01'] ['EBV']
    sed output names that exist in neither Ensembl nor the BAM (mangled non-primary contigs): 2816 ['1_KI270706v1_random', '1_KI270707v1_random', '1_KI270708v1_random', '1_KI270709v1_random']
    tags after reheader / after -x SA -x XA: 1	*	SA:Z:chr2,100,+,5S5M,60,0;	XA:Z:chr2,+200,10M,1;	OA:Z:chr1,11,+,10M,60,0; || 1	OA:Z:chr1,11,+,10M,60,0;
1	OA:Z:chr1,11,+,10M,60,0;
    CRAM reheader stderr: 
    mutated-reference CRAM decode: 0 0 [E::cram_decode_slice] MD5 checksum reference mismatch at chr22:1952-4617
[E::cram_decode_slice] CRAM  : 0b707159b93f47623cb61af0c50edec9
[E::cram_decode_slice] Ref   : fdb34a6b27f684c1b67fb45e49e998c
[E::cram_decode_slice] CRAM  : 0b707159b93f47623cb61af0c50edec9
[E::cram_decode_slice] Ref   : fdb34a6b27f684c1b67fb45e49e998c
SUMMARY: 36/36 checks passed; FAILS=[]
```

**Scores:** Basic 30/40 | Specialized 46/60 | Total 76/100

**Assertions:**
- [PASS] Contig-naming and GRCh38-flavour table entries match real files: UCSC hg38/hg19, 1000G hs38DH 3,366 = 261+2,385+525, Broad fai identical, hs37d5, Ensembl names (scaffolds = GenBank accessions), NCBI GRCh38/GRCh37 reports and README, hg38 chrM == Ensembl MT, hg19 chrM 16,571 bp different — independent parse of the fetched files; sequence compare for chrM
- [PASS] Reheader recipe on the real chr22 BAM gives records identical except RNAME/RNEXT (5,644), identical mpileup, Picard "No errors found"; CRAM reheader decodes identical with -T; SA/XA keep old names and view -x removes them; bcftools annotate --rename-chrs works — 36/36 script checks
- [FAIL] The documented block (assembly-report map -> awk -> reheader) runs on a BAM with the full hg38/hs38DH header (1000G HG00349) — map.tsv gets "chr11_KI270721v1_random na" x4 (contigs without a RefSeq accession); reheader stops "Duplicate entry na in sam header", rc 1, 0-byte renamed.bam. Adding $7!="na" fixes it (451 contigs renamed, records identical)
- [PASS] The Check line (diff SN/LN vs .fai) prints OK for the matching reference and does not for wrong name, wrong length or wrong order — three mismatch cases produce a diff, no OK
- [PASS] Rename claims about CRAM identity: a 1-base-different reference fails the decode with an MD5 mismatch — [E::cram_decode_slice] MD5 checksum reference mismatch

**Note:** The tables the fixer rebuilt are right (the first audit had them wrong); the one recipe defect appears only on real full-header BAMs, which the fixer did not try.

### Input 4 — Variant B (regression): Consensus from real BAMs: SKILL commands, viral command, real-data agreement, version notes

**Prompt:** Generate a consensus from my BAM: viral (SARS-CoV-2, IUPAC, min depth 10), the nanopore ARTIC BAM, and a real human slice; which options matter?

**Mode / execution:** B; executed: true; scripts: r4_real_consensus.py, r0_news.sh

**Log `run/logs/r4_real_consensus.txt`: 17 PASS lines; non-PASS lines (observations and FAILs) below**

```
##### INPUT 5 (regression): human chr22 slice 1952-4617 (real, PE)
    compare_to_ref -> [(3266, 'T', 'C')]
    samtools consensus -m simple differences: [(3266, 'T', 'C')]
    samtools consensus (default Bayesian) differences: [(2123, 'C', 'G'), (3266, 'T', 'C')] | SKILL says: 1 by majority/simple, 2 by default Bayesian
    WITHOUT -d 3 (default -d 1): simple differences at [1954, 3140, 3266, 3355, 3655] | Bayesian differences at [1954, 2123, 3140, 3266]
    columns called ACGT by both build_consensus and default samtools consensus: 1012 ; disagreements: 1
##### INPUT 5b: 1000G HG00349 chr20:1,400,001-1,500,000 (real low-coverage WGS) vs Ensembl truth
    called columns (depth>=3): 92347 differences vs GRCh38: 120 => 1.30 per kb
    samtools consensus -a on the 100 kb slice: length 100000
    columns called by both: 92207 disagreements (majority vs Bayesian, quality-weighted): 0
##### INPUT 4 (regression): SKILL viral consensus command, verbatim, on the real SARS-CoV-2 Illumina BAM and the ARTIC nanopore BAM
    SKILL command: samtools consensus --config hiseq -d 10 --ambig -a input.bam -o consensus.fa
    viral command as printed: len 29826 | same command + --show-del yes --show-ins no: len 29829 (header LN 29829 )
    Illumina viral consensus (nf-core test BAM has only 200 reads, so almost every column is below -d 10): called 16, N 29810, * 3, differences from MT192765.1: 0
    nanopore ARTIC (r10.4_sup profile, whatever the chemistry): rc 0 len 29903 N 77 
SUMMARY: 17/17 checks passed; FAILS=[]
```

**Scores:** Basic 35/40 | Specialized 53/60 | Total 88/100

**Assertions:**
- [PASS] The SKILL viral command runs verbatim: one record, no * ; with --show-del yes --show-ins no it is exactly the header LN (29,829) and every depth<10 column is N (or * at a deletion) — the nf-core Illumina test BAM has only 200 reads, so 29,810 of 29,829 columns are N
- [PASS] ARTIC nanopore BAM: one 29,903 bp record, 99.98% identical to MN908947.3 over called bases — 77 N
- [PASS] Real 1000G HG00349 chr20 100 kb: samtools consensus and the majority vote agree at all 92,207 jointly called columns; differences from the Ensembl sequence 120 (1.3 per kb) — external truth = Ensembl REST sequence
- [FAIL] The sentence "chr22 slice: 1 difference by majority vote and by -m simple --call-fract 0.5 --min-BQ 13, 2 by the default Bayesian mode" reproduces with the options as printed — with the options as printed (-d 1) simple gives 5 and Bayesian 4 differences; 1 and 2 need -d 3
- [PASS] Version notes match the samtools NEWS: -T added in 1.22, instrument --config in 1.17, -aa in 1.18 — ncbi/samtools_NEWS.md

**Note:** Real-data consensus behaves as documented; one statistic is quoted without the flag that produces it.

### Input 5 — Stress (regression): Python build_consensus / compare_to_ref verbatim on real slices (the pre-fix 581-difference case)

**Prompt:** Use the Python majority-vote consensus and compare it with the reference on my real chr22 slice and the 1000G chr20 slice.

**Mode / execution:** B; executed: true; scripts: r4_real_consensus.py, r6_planted.py

Output of the same run (see input 4 log, sections INPUT 5 / 5b) and of input 6 sections C / D. Key lines:
```
##### INPUT 5 (regression): human chr22 slice 1952-4617 (real, PE)
PASS build_consensus (verbatim) returns exactly 2666 chars for [1951,4617) (pre-fix version returned 1157: shifted after gaps) -- 2666
PASS build_consensus equals the mpileup -B -Q13 majority (independent parser) at every column with depth>=3 and no tie (n=1016) -- []
    compare_to_ref -> [(3266, 'T', 'C')]
PASS compare_to_ref list == samtools consensus -m simple difference list on the real slice -- ([(3266, 'T', 'C')], [(3266, 'T', 'C')])
    columns called ACGT by both build_consensus and default samtools consensus: 1012 ; disagreements: 1
PASS compare_to_ref on an all-lower-case copy of the reference gives the same result (case-insensitive) -- [(3266, 'T', 'C')]
##### INPUT 5b: 1000G HG00349 chr20:1,400,001-1,500,000 (real low-coverage WGS) vs Ensembl truth
PASS build_consensus on 100 kb: exactly 100000 chars -- 100000
PASS build_consensus == mpileup -B -Q13 majority at every column with depth>=3 and no tie (independent parser; n=92318) -- []
PASS compare_to_ref on the padded reference == direct comparison of the consensus with the independent Ensembl sequence (120 differences) -- (120, 120)
```

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100

**Assertions:**
- [PASS] build_consensus returns exactly end-start characters and equals the samtools mpileup -B -Q13 majority (independent parser) at every column with depth>=3: 1,016 columns on chr22 and 92,318 on chr20; uncovered columns are N in place — pre-fix version returned 1,157 characters and 581 false differences
- [PASS] compare_to_ref on chr22 == the samtools consensus -m simple -d 3 difference list [(3266,T,C)]; identical with an all-lower-case reference — 
- [PASS] compare_to_ref on the padded chr20 reference == direct diff against the independent Ensembl sequence (120 differences) — external truth
- [PASS] The pysam pileup prose (Q<13 dropped, duplicates/secondary skipped, overlapping mates once, max_depth 8000) reproduces — overlap: 40 vs 80 with ignore_overlaps=False on planted pairs; 353,982 vs 670,370 pileup bases on the real PE BAM; 9,000 reads -> 8,000
- [PASS] Deep columns (depth up to 2,532) are fully used (max_depth raised): called columns == mpileup depth>=3 columns — 1016 == 1016

**Note:** The headline defect of the first audit is fixed and holds up on independent methods.

### Input 6 — Adversarial (new): NEW: planted-truth reference (N run, IUPAC R/Y, soft-mask, empty contig) and BAM (SNPs, hets, deletion, insertion, gap, edges, decoy reads)

**Prompt:** (new) My reference has an N gap, IUPAC codes and soft-masked repeats; the BAM has SNPs, hets, an indel, a coverage gap and junk reads. Build the consensus with samtools and with the Python function, and list differences from the reference.

**Mode / execution:** B; executed: true; scripts: make_planted.py, r6_planted.py

**Log `run/logs/r6_planted.txt`: 40 PASS lines; non-PASS lines (observations and FAILs) below**

```
##### A. prepare_reference.sh on a hostile reference (mixed widths, N run, IUPAC, soft-mask, empty contig)
-rw-r--r-- 1 sci sci 436 Sep 20 06:14 ./planted.dict
-rw-r--r-- 1 sci sci  59 Sep 20 06:14 planted.fa.fai
Reference summary:
  Chromosomes: 3
  Total length: 8300 bp
##### B. samtools consensus against planted truth
    edge columns (pos, called, truth, depth): [(0, 'N', 'G', 1), (1, 'N', 'C', 1), (2, 'N', 'T', 1), (3, 'N', 'A', 1), (4, 'N', 'A', 2), (5, 'N', 'A', 2), (6, 'N', 'G', 2), (7, 'N', 'A', 2), (8, 'C', 'C', 3), (9, 'A', 'A', 3), (10, 'A', 'A', 3), (11, 'T', 'T',
    het col 700 (13 C / 12 G) default / --ambig: N S | het col 900 (20 A / 5 x) default / --ambig: N M
    counts {'C': 13, 'G': 12} {'A': 20, 'C': 5}
    NOTE 80/20 column 900: default gives N --ambig gives M (SKILL claims: without --ambig an ambiguous column is N, even when one base is 80% of the reads)
    default records: [('ctgA', 5998), ('ctgB', 500)] | -a: [('ctgA', 5998), ('ctgB', 1500)] | -aa: [('ctgA', 5998), ('ctgB', 1500), ('ctgC', 800)]
    -r ctgA:5901-6000 -a: [('ctgA:5901-6000', 100)]
    -T planted.fa (default -d 3) vs no -T: 300 differing columns; first ones: [(1500, 'N', 'C'), (1501, 'N', 'A'), (1502, 'N', 'G'), (1503, 'N', 'G'), (1504, 'N', 'A'), (1505, 'N', 'C'), (1506, 'N', 'C'), (1507, 'N', 'C')]
##### C. SKILL Python snippets (verbatim) against planted truth
    build_consensus at the het cols 700/900: C A | counts {'C': 13, 'G': 12} {'A': 20, 'C': 5}
    compare_to_ref breakdown: {'real': 3, 'N-run': 30, 'IUPAC': 2} (the 30 N-run and 2 IUPAC positions are reported as differences: consensus base vs reference N/R/Y)
##### D. pysam pileup default claims in the SKILL prose
    overlap column 60: default n = 40  ignore_overlaps=False n = 80 | single-mate column 20 default n = 40
    real chr22 PE BAM: total pileup bases default 353982 vs ignore_overlaps=False 670370
SUMMARY: 40/40 checks passed; FAILS=[]
```

**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100

**Assertions:**
- [PASS] build_consensus (verbatim) equals an independent cigar-walk majority at all 6,000 columns: gap, edges, deleted columns N, DUP/secondary/Q5 decoys ignored, MAPQ-0 decoys outvoted — 0 mismatches; het cols 700/900 follow the majority
- [PASS] samtools consensus -a --show-del yes --show-ins no is 6,000 characters and equals the planted sample at every column with depth>=6 (SNPs incl. under the reference N run and R/Y, * at the 2-bp deletion, N over the gap and -d 3 zones); default output shows GTA after 4500 (length 6001) — samtools and the Python function agree at all 5,696 jointly called columns
- [PASS] -a / -aa behaviour as documented: default only contigs with reads; -a pads ctgB to LN 1500; -aa adds the read-less ctgC as 800 N; ends are not padded without -a — 
- [FAIL] The -T description ("report ref base where consensus unavailable (low coverage; ... FASTA case)") matches behaviour — -T fills only zero-coverage columns (gap 1500-1799 -> reference). Columns below -d (depth 2 with -d 3; depth 25 with -d 30) and ambiguous columns stay N. The case claim is right.
- [PASS] prepare_reference.sh dict for the hostile reference: M5 = md5 of the upper-cased sequence (N and IUPAC kept), identical to Picard 3.5.0 — compare_to_ref reports the 30 N-run and 2 IUPAC positions as differences (35 total) - unstated, sensible

**Note:** Both consensus paths agree with planted truth; one wording defect on -T.

### Input 7 — Edge (new): NEW: mixed-mate BAM/CRAM with M5, rename recipe, name/length/order mismatches

**Prompt:** (new) The BAM has inter-contig mates and unmapped reads, the CRAM has M5 tags; rename the contigs to 1/2/3, and tell me whether references with other names, lengths or contig order will still work.

**Mode / execution:** B; executed: true; scripts: r7_rename_order.py

**Log `run/logs/r7_rename_order.txt`: 15 PASS lines; non-PASS lines (observations and FAILs) below**

```
mix.bam records: 100
    Picard vs reordered reference: No errors found
    GATK CountReads vs reordered reference: [September 20, 2026 at 6:14:13 AM PDT] org.broadinstitute.hellbender.tools.CountReads done. Elapsed time: 0.01 minutes.
@SQ SN:ctgB LN:1500 M5:d6d9e6a9feb895989de69187f3c985d0 UR:/mnt/opens
    CRAM reheader: rc=0 | SN:1	LN:6000	M5:0aa3740604750d1ed8352ac80b4f50e5 | SN:2	LN:1500	M5:d6d9e6a9feb895989de69187f3c985d0 | SN:3	LN:800	M5:6396a4ef18d4cafe93b0824cf9b4cc18 | stderr: 
SN:1	LN:6000	M5:0aa3740604750d1ed8352ac80b4f50e5
SN:2	LN:1500	M5:d6d9e6a9feb895989de69187f3c985d0
SN:3	LN:800	M5:6396a4ef18d4cafe93b0824cf9b4cc18
    SKILL says reheader warns "Failed to populate reference" without REF_PATH/cache for the renamed reference; observed warning: False
    md5 decode original: 1055bc16  renamed (RNAME normalised for the compare only): 1d367524
    renamed CRAM decoded with the OLD-named reference: 0 0 [W::cram_get_ref] Reference file given, but ref '1' not present
[E::fai_build3_core] Failed to open the file 0aa3740604750d1ed8352ac80b4f50e5 : No such file or directory
[E::cram_decode_slice] Unable 
    renamed CRAM with the longer-ctg 2 reference: 0 100 [W::sanitise_SQ_lines] Header @SQ length mismatch for ref 2, 1500 vs 1501
    reheader with REF_PATH/REF_CACHE pointing nowhere: rc/out rc=0 | stderr: 
SUMMARY: 15/15 checks passed; FAILS=[]
```

**Scores:** Basic 34/40 | Specialized 52/60 | Total 86/100

**Assertions:**
- [PASS] Recipe (verbatim awk + reheader + index) on a BAM with inter-contig mates, "=" mates, unmapped-with-position and fully unmapped reads: 100 records identical except RNAME/RNEXT; Picard "No errors found" against the renamed reference — 
- [PASS] CRAM made with -T (M5 in every @SQ): reheader rc 0, header M5 kept, decodes identically with the renamed reference; with the old-named reference it fails loudly — no "Failed to populate reference" warning appeared (M5 present, UR pointed at an existing file); the SKILL sentence is conditional and not scored
- [PASS] The Check line does not print OK for a reference with different names, a 1-base-longer contig, or reordered contigs — Picard 3.5.0 ValidateSamFile and GATK CountReads accept the reordered reference silently, so the Check line is the only guard
- [PASS] M5 advice: header M5 equals samtools dict M5 for the right reference and differs only for the 1-base-longer contig — a CRAM decode against the longer contig only WARNS (Header @SQ length mismatch) and decodes 100 records: the CRAM MD5 is per slice region

**Note:** The recipe generalises to CRAM and awkward mate fields; contig-order mismatch is not mentioned by the Skill (silent).

### Input 8 — Variant B (new): NEW: consensus-mode semantics on a graded-allele fixture (depth 20/60, minor 50%-5%) and bcftools consensus note

**Prompt:** (new) What exactly do --het-fract, --call-fract, --ambig, --het-scale, -d, -a/-aa and -T do, in both consensus modes, and how does bcftools consensus treat het genotypes?

**Mode / execution:** B; executed: true; scripts: r8_modes.py

**Log `run/logs/r8_modes.txt`: 21 PASS lines; non-PASS lines (observations and FAILs) below**

```
columns (pos1, depth, minor reads): [(101, 20, 10), (201, 20, 8), (301, 20, 6), (401, 20, 5)] ... n = 16
reference bases at the 16 columns: ['G', 'G', 'T', 'T', 'A', 'C', 'A', 'G', 'C', 'A', 'C', 'C', 'G', 'T', 'G', 'T']
depth 20 columns then depth 60 columns; minor fraction 0.5,0.4,0.3,0.25,0.2,0.15,0.1,0.05 in each
##### -m simple: predicted vs observed on the grid of (het-fract, call-fract, --ambig)
    sample outputs (16 columns: d20 fractions .5 .4 .3 .25 .2 .15 .1 .05 | d60 same):
    het-fract 0.15 call-fract 0.75 ambig True  RRYYRYAGYRYYRYGT
    het-fract 0.3  call-fract 0.75 ambig True  RRYYACAGYRYYGTGT
    het-fract 0.15 call-fract 0.9  ambig False NNNNNNAGNNNNNNGT
    het-fract 0.15 call-fract 0.6  ambig False NGTTACAGNACCGTGT
    simple --ambig, het-fract OMITTED  : RRNTACAGYRNCGTGT
    simple --ambig, --het-fract 0.15   : RRYYRYAGYRYYRYGT
    omitted --het-fract behaves like explicit --het-fract in [0.5, 0.6]
    simple (defaults, no --ambig): NNNTACAGNNNCGTGT
##### default Bayesian mode: flags are ignored; --ambig required for IUPAC; --het-scale is the knob
    Bayesian default        : NNNNNNAGNNNNNNNT
    Bayesian --ambig        : RRYYRYAGYRYYRYRT
    Bayesian --ambig --het-scale 0.01: NGTTACAGNACCGTGT
    Bayesian --ambig --het-scale 100 : RRYYRYRRYRYYRYRY
    the 15% column (index 5 / 13) Bayesian default: N N ; the 5% column: G T (the 50% col at depth 20/60: N N )
##### -d
##### -a / -aa / -T on this contig (reads cover 30..1649 and 1900..1999; contig 2000 bp; 1650..1899 uncovered and soft-masked)
    lengths default / -a / -aa: 1934 2000 2000 | default starts ACCAAA ends CGGATA | -a starts NNNNNN
##### FASTQ
##### bcftools consensus IUPAC note (own VCF on the same reference)
    default: ['R', 'Y', 'Y', 'G'] expected IUPAC/IUPAC/IUPAC/ALT = ['R', 'Y', 'Y', 'G'] Note: applying IUPAC codes based on FORMAT/GT in sample S1
Applied 4 variants
    -H 1: ['G', 'T', 'C', 'G'] -H 2: ['A', 'C', 'T', 'G'] -H A: ['A', 'C', 'C', 'G'] -s -: ['A', 'C', 'C', 'G'] Note: applying REF,ALT variants, ignoring samples
Applied 4 variants
SUMMARY: 21/21 checks passed; FAILS=[]
```

**Scores:** Basic 37/40 | Specialized 56/60 | Total 93/100

**Assertions:**
- [PASS] The -m simple rule (IUPAC iff --ambig and minor/major >= --het-fract; else base iff major/depth >= --call-fract; else N) predicts all 48 (het-fract x call-fract x ambig) outputs across 16 columns — independent predictor written before comparing
- [PASS] Omitted --het-fract is not 0.15 (15% column plain base, explicit 0.15 gives Y); omitted behaves like 0.5-0.6; --call-fract default 0.75 — matches SKILL "always pass it explicitly"
- [PASS] Bayesian mode: --het-fract/--call-fract byte-identical; no IUPAC without --ambig (the 13 ambiguous columns are N); --het-scale 0.01/1/100 gives 0/13/16 IUPAC calls; -A == --ambig — 
- [PASS] -d works in both modes; -a pads to LN, -aa == -a for a contig with reads; -T fills the uncovered soft-masked gap in lower case; FASTQ -l 0 gives 4 lines, default wrap 70 — 
- [PASS] bcftools consensus: default writes IUPAC for unphased 0/1 and phased 0|1, 1|0; -H 1 / -H 2 pick haplotypes; -H A and -s - apply every ALT — bcftools 1.24 note text "applying IUPAC codes based on FORMAT/GT"

**Note:** Every documented flag statement the fixer added holds on data the fixer never saw.

## Extra regression checks (run/logs/r10_blocks.txt, r9_misc.txt, r0_news.txt, r3b_mito.txt, r1c_picard_dict.txt)

All 15 `samtools consensus` command lines printed in SKILL.md ran as written (rc 0, non-empty FASTA/FASTQ; profiles hifi, r10.4_sup, ultima, hiseq accepted; `-T`, `-a`, `-f fastq -l 0` produce the expected shapes). Cache block (verbatim, HOME set): cache file `19/22/b52e1af6...` created, CRAM decodes 5,644 records with no `-T` through `REF_PATH`, and fails loudly when no cache/reference resolves; `samtools dict -a GRCh38 -s "Homo sapiens"` writes `AS:GRCh38 SP:Homo sapiens`; the dict `UR:` is an absolute `file:///` URL (the SKILL example shows `file:reference.fa`); `consensus -> minimap2 -a` block runs (3 SAM records); consensus md5 identical x3; hostile file name safe; prepare_reference.sh idempotent; plain-gzip FASTA fails with the samtools bgzip message; Picard 3.5.0 finds `genome.fasta.dict` (ScatterIntervalsByNs rc 0 with either dict name, rc 1 with none) so only GATK ignores it; hg38 chrM == Ensembl MT and hg19 chrM (16,571 bp) differs from GRCh37 MT; NEWS: -T 1.22, --config 1.17, -aa 1.18.

```
rc=0 bytes=2712 first='>' :: samtools consensus test.paired_end.sorted.bam -o out.txt
rc=0 bytes=149 first='>' :: samtools consensus -r chr22:2000-2500 test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus -f fasta test.paired_end.sorted.bam -o out.txt
rc=0 bytes=5343 first='@' :: samtools consensus -f fastq -l 0 test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus -d 5 test.paired_end.sorted.bam -o out.txt
rc=0 bytes=40580 first='>' :: samtools consensus -a test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus --ambig test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus --ambig --het-scale 0.1 test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus -m simple --ambig --het-fract 0.2 --call-fract 0.5 test.paired_end.sorted.bam -o out.txt
rc=0 bytes=2712 first='>' :: samtools consensus --config hifi       test.paired_end.sorted.bam -o out.txt   
rc=0 bytes=2712 first='>' :: samtools consensus --config r10.4_sup  test.paired_end.sorted.bam -o out.txt   
rc=0 bytes=2712 first='>' :: samtools consensus --config ultima     test.paired_end.sorted.bam -o out.txt   
rc=0 bytes=2712 first='>' :: samtools consensus --config hiseq      test.paired_end.sorted.bam -o out.txt   
rc=0 bytes=2712 first='>' :: samtools consensus -T genome.fasta test.paired_end.sorted.bam -o out.txt
rc=0 bytes=40580 first='>' :: samtools consensus --config hiseq -d 10 --ambig -a test.paired_end.sorted.bam -o out.txt
--- bcftools consensus lines (placeholders reference.fa / variants.vcf.gz do not exist; syntax checked with --help only)
    -f, --fasta-ref FILE           Reference sequence in fasta format
    -H, --haplotype WHICH          Choose which allele to use from the FORMAT/GT field, note
    -s, --samples LIST             Comma-separated list of samples to include, "-" to ignore samples and use REF,ALT
```

```
##### 1. SKILL 'Pre-populate CRAM REF_CACHE' block (snippet skill_28) verbatim with HOME=/mnt/openscience/audits/bio-reference-operations/run/work/r9/home, then decode with no -T
rc=0
Reading genome.fasta ...
/mnt/openscience/audits/bio-reference-operations/run/work/r9/home/ref_cache/19/22/b52e1af6977302717072ebaca0a1 chr22
cache files:
home/ref_cache/19/22/b52e1af6977302717072ebaca0a1
decoded records via REF_PATH (expect >=5 lines printed by head, block prints 10):
8
full decode via cache, no -T: 5644 records (expect 5644)
and WITHOUT the cache and without -T (must fail loudly, not silently):
[E::fai_build3_core] Failed to open the file /sfs/7/workspace/ws/iizha01-dsl2_testdata_human-0/test-datasets/data/genomics/homo_sapiens/illumina/cram/../../genome/genome.fasta : No such file or direct
[E::refs_load_fai] Failed to open reference file '/sfs/7/workspace/ws/iizha01-dsl2_testdata_human-0/test-datasets/data/genomics/homo_sapiens/illumina/cram/../../genome/genome.fasta'
##### 2. samtools dict -a/-s and default text
@HD	VN:1.0	SO:unsorted
@SQ	SN:chr22	LN:40001	M5:1922b52e1af6977302717072ebaca0a1	UR:file:///mnt/openscience/audits/bio-reference-operations/run/work/r9/genome.fasta	AS:GRCh38	SP:Homo sapiens
@HD	VN:1.0	SO:unsorted
@SQ	SN:chr22	LN:40001	M5:1922b52e1af6977302717072ebaca0a1	UR:file:///mnt/openscience/audits/bio-reference-operations/run/work/r9/genome.fasta
@SQ	SN:chr22	LN:40001	M5:1922b52e1af6977302717072ebaca0a1	UR:file:///mnt/openscience/audits/bio-reference-operations/run/work/r9/rel.fa
##### 3. SKILL 'Compare Consensus to Reference': consensus -> minimap2 -a
1
minimap2 rc=0
3
chr22	0	chr22	2717	60	765S938M963S
chr22	2048	chr22	1955	60	3H175M2488H
##### 4. determinism: samtools consensus x3 md5
bdc7098ee24add369a70e68592f32676  -
bdc7098ee24add369a70e68592f32676  -
bdc7098ee24add369a70e68592f32676  -
##### 5. hostile file name through prepare_reference.sh
rc=0
we"ird'name.v2.chrom.sizes
we"ird'name.v2.dict
we"ird'name.v2.fasta
we"ird'name.v2.fasta.fai
Reference summary:
  Chromosomes: 1
  Total length: 40001 bp
##### 6. samtools dict overwrite of an existing dict (SKILL script idempotent)
idem.dict: OK
idem.fa.fai: OK
idem.chrom.sizes: OK
##### 7. plain-gzip (not bgzip) FASTA, e.g. straight from Ensembl/NCBI: prepare_reference.sh accepts .gz per its usage line
Preparing reference: plain.fa.gz
1. Creating FASTA index...
[E::fai_build_core] File truncated at line 1
[E::fai_build3_core] Cannot index files compressed with gzip, please use bgzip
[faidx] Could not build fai index plain.fa.gz.fai
rc=1
plain.fa.gz
SKILL mentions bgzip? -> 0 hits in SKILL.md, 0 in usage-guide.md
```

```
== only_fasta_dot_dict: picard ScatterIntervalsByNs rc=0 out_lines=1 :: 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
== only_genome_dot_dict: picard ScatterIntervalsByNs rc=0 out_lines=1 :: 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
== none: picard ScatterIntervalsByNs rc=1 out_lines= :: Exception in thread "main" java.lang.IllegalStateException: Reference file must include a dictionary, but no dictionary file was found 
   CollectWgsMetrics rc=0 metrics_file_lines=263 :: 
```

```
1:The reference fasta file in this directory was unpacked from Heng Li's bwakit-0.7.12:
3:http://sourceforge.net/projects/bio-bwa/files/bwakit/bwakit-0.7.12_x64-linux.tar.bz2/download
34:Decoy sequences:
35:chrUn_{sequence_accession}v{sequence_version}_decoy
36:e.g. chrUn_KN707606v1_decoy
ucsc_hg38_chrM.json 16717
ucsc_hg19_chrM.json 16719
ens38_MT.txt 16569
ens37_MT.txt 16569
lengths hg38 chrM / hg19 chrM / Ensembl GRCh38 MT / Ensembl GRCh37 MT: 16569 16571 16569 16569
CHECK hg38 chrM == Ensembl GRCh38 MT (same sequence): True
CHECK hg19 chrM (16,571 bp) is a different sequence from GRCh37 MT: True
INFO GRCh37 MT == GRCh38 MT: True
```

```
release 1.22: * Add `samtools consensus -T ref.fa` functionality.  This reports the reference
release 1.18: * New -aa mode for consensus.  This works like the -aa option in depth and
release 1.17: * Improve samtools consensus for platforms with instrument specific profiles,
```

## Final

Static 82 x 0.4 = 32.8; execution 87.5 x 0.6 = 52.5; **final 85 / 100, ⭐ Production Ready**, deployable True, veto_override False.

Floors: static>=80 ok, exec>=85 ok, L1>=32 ok, L2>=48 ok, assert>=90% ok.

Open: P0 none; P1 one (reheader recipe on full hg38 headers); P2 four (details in the JSON).

### Optimization recommendations

**[P1] Reheader recipe fails on full hg38 headers (map emits "na")**  
Observed in: [3]  
Problem: The UCSC->RefSeq map line keeps 4 contigs whose RefSeq column is "na" (chr11_KI270721v1_random, chr22_KI270734v1_random, chrUn_KI270752v1, chr10_KI270825v1_alt). On a hs38DH/UCSC header (1000G BAM) reheader stops with "Duplicate entry na in sam header" and leaves a 0-byte renamed.bam.  
Root cause: The recipe was verified only on a single-contig BAM.  
Fix: Change the awk filter to $10!="na" && $7!="na" (tested: rc 0, 451 of 3,366 contigs renamed, records identical) and write reheader output to a temp name, mv on success.

**[P2] -T is described as filling low-coverage columns**  
Observed in: [6, 8]  
Problem: -T fills only zero-coverage columns with the reference base (in FASTA case). Columns below -d or ambiguous stay N.  
Root cause: Wording "consensus unavailable (low coverage; ...)" was written without testing a depth-below--d column.  
Fix: Say "columns with no reads (depth 0)"; add "columns below -d and ambiguous columns stay N".

**[P2] Description omits contig renaming, extraction, CRAM references**  
Observed in: [3, 7]  
Problem: The frontmatter still names consensus / indexing / dictionaries only, while the body and the usage-guide prompts now answer "my BAM says chr22, reference says 22" and "which GRCh38 is this?".  
Root cause: Description left untouched during the fix.  
Fix: Add "rename/match contig names (chr22 vs 22, GRCh38 flavours), extract regions, CRAM reference resolution" to the description.

**[P2] bgzip requirement and test data are undocumented**  
Observed in: [1]  
Problem: The script usage line and SKILL accept ".gz", but plain-gzip FASTA (as downloaded from Ensembl/NCBI) fails in faidx ("please use bgzip") and the Skill never says so. There is still no shipped sample data or expected output.  
Root cause: .gz support was tested with bgzip only; test data was declined in the fix.  
Fix: Add one line: "gunzip -c x.fa.gz | bgzip > x.fa.gz2" (or gzip -> bgzip) and a 3-line toy FASTA + expected .dict in examples/.

**[P2] Small stated-but-imprecise details**  
Observed in: [1, 3, 4, 6]  
Problem: Picard 3.5.0 does accept genome.fasta.dict (only GATK ignores it); the chr22 "1 vs 2 differences" needs -d 3; the dict example shows UR:file:reference.fa but samtools writes an absolute file:/// URL; the UCSC->Ensembl sed one-liner rewrites non-primary contigs too (chr1_KI..._alt -> 1_KI..._alt); the multi-region skip message prints chr2:5001-3007; compare_to_ref reports reference N/IUPAC positions as differences and build_consensus writes N at deleted columns and ignores insertions without saying so.  
Root cause: Prose written from one tool or one run.  
Fix: One clause each: name GATK for the ignored-dict sentence, add -d 3 to the chr22 sentence, show an absolute UR, restrict the sed to a chr1-22/X/Y/M pattern, print the unclipped end in the skip message, note the N/IUPAC and indel behaviour of the pedagogical functions.

### Key strengths
- The Python consensus defect is fixed and holds up: build_consensus equals a cigar-walk truth at all 6,000 planted columns and the samtools mpileup majority at 1,016 real chr22 and 92,318 real chr20 columns; compare_to_ref matches samtools consensus and Ensembl.
- prepare_reference.sh derives <name>.dict correctly: GATK 4.6.2.0 HaplotypeCaller and Picard 3.5.0 loaded the output for every claimed filename shape, and a hostile file name executed nothing.
- The rebuilt contig and GRCh38 tables match real files (UCSC, 1000G, Broad, hs37d5, Ensembl, NCBI reports, chrM sequences) and the reheader recipe gives records identical except RNAME/RNEXT on BAM and CRAM.
- Consensus flag documentation (--het-fract/--call-fract/--ambig/--het-scale/-d/-a/-aa/-T case, bcftools IUPAC note, version notes) reproduced on a fixture the fixer never saw; usage-guide dedup lost nothing an agent needs.

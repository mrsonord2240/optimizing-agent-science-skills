> **Audit record for `bio-reference-operations`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/reference-operations) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-reference-operations
Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/reference-operations` | Category: Data Analysis | Mode: B (CLI/script) | Complexity: Moderate (N=5)

Environment: WSL `science`, env `alignment-files` (samtools 1.24, bcftools 1.24, pysam 0.24.1, Picard 3.5.0, GATK 4.6.2.0, minimap2 2.31). Every script is in `run/`, raw logs in `run/logs_*.txt`; synthetic data (labelled) in `run/data/synthetic/` built by `run/make_synth.py`; real data copied from `audit-envs/alignment-files/public-data` into `run/data/real/`; public sources fetched 2026-09-20 in `run/ncbi/`.

## Skill Veto
T1 Stability PASS | T2 Contract PASS | T3 Determinism PASS | T4 Security PASS

- stability: prepare_reference.sh ran on .fa, .fasta, .fa.gz, a path with a space and a read-only dir (stops with exit 1 under set -e); all 5 inputs completed; no crashes or loops.
- contract: Frontmatter has name, description, tool_type, primary_tool, license.
- determinism: samtools consensus --ambig gave an identical md5 on 3 runs; every faidx/dict/consensus output reproduced on re-run.
- security: No eval/exec; script quotes every expansion; only writes next to the input FASTA.

## Static score (25 criteria)

| Category | Score | Note |
|---|---|---|
| functional_suitability | 8/12 | Core faidx/dict/consensus/CRAM-identity content is right and verified. Wrong or misleading: NCBI RefSeq contig names, the 1000G/hs38DH rows, "no clean conversion for BAM -- re-align", -a description, --het-fract/--call-fract in default mode, Python build_consensus/compare_to_ref alignment. Nothing on .fasta/.fa.gz dict naming or on samtools reference. |
| reliability | 7/12 | prepare_reference.sh checks the argument and the file, uses set -e, is idempotent. Guide recipes are unguarded (subset block exits 0 with a chr3 LN:0 dict; seq_cache_populate.pl uses an undefined $REF_CACHE_DIR and silently does nothing). Troubleshooting titles do not match real tool messages. |
| performance_context | 5/8 | SKILL.md 377 lines + usage-guide 251 lines with heavy duplication: three pysam consensus functions, faidx recipes twice, FAI table twice, dict recipe three times. |
| agent_usability | 11/16 | Clear task-oriented headings and a useful contig-naming section. Inconsistencies: min_depth 3 vs 5, -a described two ways, dict header VN 1.0 vs pysam VN 1.6, "verify via samtools consensus --help" which exits 1. |
| human_usability | 6/8 | Description triggers naturally on "index my reference / consensus / dictionary". Region extraction and CRAM references are in the body but not in the description. |
| security | 11/12 | No credentials, quoted expansions, no destructive commands; samtools dict -o silently overwrites an existing dict. |
| maintainability | 7/12 | Three files with a clean split, but the same snippets are duplicated in two files, version-sensitive claims (flags, added-in versions) are scattered, and there is no test data or expected output. |
| agent_specific | 17/20 | All 8 Related Skills paths resolve. Idempotent. Good pedagogical-only warning and "different operations" table for samtools/bcftools consensus. Description omits faidx extraction and CRAM references; contig-conversion advice is wrong (a stop condition that is incorrect). |
| **Subtotal** | **72/100** | |

## Summary table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 45 | 77 | 3/5 PASS | ✅ |
| 2 | Variant A | 34 | 49 | 83 | 3/5 PASS | ✅ |
| 3 | Edge | 31 | 45 | 76 | 3/5 PASS | ✅ |
| 4 | Variant B | 32 | 47 | 79 | 3/5 PASS | ✅ |
| 5 | Stress | 26 | 32 | 58 | 3/5 PASS | ⚠️ |

**Execution Average: 74.6 / 100** | **Assertion Pass Rate: 15/25** | executed 5/5

## Detailed outputs

### Input 1 — Canonical: Prepare a reference for GATK/Picard: index, dict, chrom.sizes, validate
**Prompt:** I just downloaded genome.fasta (a chr22 slice) and need it ready for GATK and Picard. Index it, make the sequence dictionary and a chrom.sizes file, and confirm everything is correct -- I will run HaplotypeCaller on it next.

**Executed: true.** run/in1.sh, run/in1b.sh, run/in1_check.py, run/in7.py. Shipped examples/prepare_reference.sh run FROM A COPY on: synthetic 3-contig 80-col soft-masked FASTA (ref.fa), REAL human chr22 slice named genome.fasta, a bgzipped ref.fa.gz, a path with a space, a read-only dir, no-arg and missing-file cases; then samtools dict -a/-s, Picard 3.5.0 CreateSequenceDictionary as independent producer, GATK ValidateSamFile and HaplotypeCaller as consumers, the usage-guide validate block, and SKILL.md create_dict_header verbatim.

**What it printed / what was found:** .fai (name,len,offset,linebases,linewidth), chrom.sizes and dict SN/LN/M5 equal an independent pure-Python parse + hashlib MD5 of the UPPERCASE sequence on both references (M5 1922b52e1af6977302717072ebaca0a1 for the real slice); Picard dict has the same SN/LN/M5. For genome.fasta the script wrote genome.fasta.dict / genome.fasta.chrom.sizes (${REF%.fa} does not strip .fasta); GATK HaplotypeCaller then failed: "A USER ERROR has occurred: Fasta dict file .../genome.dict for reference .../genome.fasta does not exist", and worked once genome.dict existed. The usage-guide validate block printed "DICT: OK" for that misnamed file. ref.fa.gz gives ref.fa.gz.dict. Script listing prints every file twice. create_dict_header returns a dict with no M5 and writes nothing.

**Scores:** Basic 32/40 | Specialized 45/60 | Total 77/100

**Assertions:**
- [PASS] .fai, chrom.sizes and dict SN/LN/M5 equal an independent computation (real and synthetic, soft-masked input) — pure-Python parse + hashlib MD5; Picard dict identical
- [FAIL] The dictionary is produced under the name GATK/Picard look for when the reference is named genome.fasta — genome.fasta.dict written; GATK HaplotypeCaller: "Fasta dict file genome.dict ... does not exist"
- [FAIL] The usage-guide validation block only reports DICT: OK when downstream tools can find the dictionary — block printed DICT: OK for genome.fasta.dict
- [PASS] The shipped script fails loudly on no argument, missing file and read-only directory, and is idempotent — exit 1 in all three; md5 of outputs unchanged on re-run; path with space works
- [PASS] Output stays in scope: no destructive commands, no clinical content — writes only beside the input FASTA

### Input 2 — Variant A: Extract regions, reverse complement, per-chromosome subset (samtools faidx + pysam)
**Prompt:** Pull chr1:1000-2000 and a couple of other regions out of my reference as FASTA, give me the reverse complement of one, split chr1 into its own indexed file, and show the same in Python with 0-based coordinates.

**Executed: true.** run/in2.py (30 checks). Synthetic 3-contig reference (80-col, lowercase soft-mask 1000-1299, N run) + REAL human chr22 slice + SARS-CoV-2 MN908947.3 + the padded 1000G chr20 FASTA whose 100 kb of real sequence has an independent external truth (Ensembl REST chr20:1400001-1500000). Every documented faidx command, the pysam snippets and usage-guide "Extract Multiple Regions" (verbatim), plus the troubleshooting scenarios.

**What it printed / what was found:** chr1:1000-2000 = 1001 bases equal to the independent 1-based inclusive slice; pysam fetch("chr1",999,2000) identical; soft-mask case preserved; SARS-CoV-2 S gene MN908947.3:21563-25384 = 3822 nt ATG...TAA; 100,000 bp of the 1000G FASTA equal the Ensembl sequence and the base before it is N padding. -i gives the exact reverse complement but the header becomes ">chr1:1000-2000/rc" (undocumented; --mark-strand no removes it). faidx auto-builds the .fai (usage-guide says "Index the reference first"). Real messages: "Failed to open the file ... Could not load fai index" and "Failed to fetch sequence in 1:1-100" (guide titles: "faidx reference file not found", "invalid region"). Region wholly beyond the contig end exits 0 with an EMPTY record. ug "Extract Multiple Regions" verbatim on a 5 kb contig printed ">chr1:1-10000" with 5000 bases and ">chr2:5001-15000" with an empty sequence. Subset with a missing contig: faidx rc=1 but the block continues; main_chroms.dict ended with "SN:chr3 LN:0 M5:d41d8cd98f00b204e9800998ecf8427e".

**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100

**Assertions:**
- [PASS] samtools faidx regions equal an independent 1-based inclusive slice of the FASTA (synthetic, real human, SARS-CoV-2, 1000G vs Ensembl) — all equal; 30/30 checks
- [PASS] The stated coordinate conventions (faidx 1-based, pysam 0-based half-open) are correct and consistent — fetch(999,2000) == faidx :1000-2000 == 1001 bases
- [FAIL] Troubleshooting titles and advice match real tool behaviour — faidx auto-indexes; real messages differ from the guide titles; out-of-range returns empty record rc 0
- [FAIL] Subset / multi-region recipes guard against a missing contig or out-of-range region — block exits 0 and leaves a dict with chr3 LN:0; ug_10 prints empty records with confident headers
- [PASS] Output stays in scope — no clinical content

### Input 3 — Edge: chr22 vs 22 contig mismatch, fixing it, CRAM/M5/REF_CACHE offline, flavour tables
**Prompt:** My BAM says chr22 but my reference says 22. How do I detect that, can I fix it without re-aligning, and how do I make CRAM decode offline on an HPC node? Which GRCh38 is which?

**Executed: true.** run/in3.py (32 checks). REAL human BAM + nf-core CRAM + 1000G HG00349 BAM with padded chr20 FASTA; the Skill detection commands verbatim; samtools/bcftools mpileup, consensus -T, calmd, pysam, Picard 3.5.0 and GATK against the renamed reference; samtools reheader; CRAM full decode with -T, empty REF_PATH, mutated reference (M5), seq_cache_populate.pl -root + REF_PATH/REF_CACHE, each with its own empty cache dir; public sources fetched 2026-09-20 (run/ncbi/).

**What it printed / what was found:** Detection commands expose ["chr22"] vs ["22"]. Consumers fail loudly: "The sequence \"chr22\" was not found", pysam KeyError, Picard ERROR:MISMATCH_FILE_SEQ_DICT, GATK "No overlapping contigs found". "for BAM there is no clean conversion -- re-align" is WRONG: samtools view -H | sed | samtools reheader gave a BAM whose 5644 records are identical (md5) except RNAME, identical mpileup, and Picard "No errors found"; same for chr1/chr2/chrM -> 1/2/MT. CRAM M5 claim verified: header M5 = samtools dict M5 = 1922b52e...; decode against a one-base-different reference: "[E::cram_decode_slice] MD5 checksum reference mismatch at chr22:1952-4617"; the same reference is silently accepted for BAM. NOTE samtools view -c never decodes bases, so it succeeds with no reference (not a valid test). seq_cache_populate.pl -root <dir> made <dir>/19/22/b52e1af6977302717072ebaca0a1 and decoding then worked with no -T and no network via REF_PATH or REF_CACHE. Tables: NCBI RefSeq FASTA names are NC_000001.11 / NC_012920.1 (chr1/chrM only in the assembly-report UCSC column) -- SKILL row wrong. The 1000G GRCh38 reference (README: unpacked from bwakit) has 261 _alt contigs, 525 HLA, 2385 decoys, chrEBV -- the SKILL row "1000G: ALT no, HLA no" is wrong and duplicates the hs38DH row it lists separately. 1000G BAM chr20 LN 64444167/M5 b18e6c53... vs padded FASTA LN 1500000/M5 cd35c0a8...; Picard: "Reference sequence (19) not found".

**Scores:** Basic 31/40 | Specialized 45/60 | Total 76/100

**Assertions:**
- [PASS] The M5 identity / CRAM enforcement claim is reproduced (decode against a one-base-different reference fails with an MD5 error) — "MD5 checksum reference mismatch at chr22:1952-4617"; BAM accepts the same reference
- [PASS] The documented detection commands expose the chr22-vs-22 mismatch — SN lists differ; downstream tools fail loudly
- [FAIL] The contig-naming and GRCh38-flavour tables match public sources — RefSeq names are NC_*; 1000G reference has ALT (261) and HLA (525) contigs and is hs38DH-derived
- [FAIL] The guidance for renaming BAM contigs is correct — says re-align; samtools reheader gives identical records and a clean Picard validation
- [PASS] seq_cache_populate.pl -root <dir> populates a cache from which CRAM decodes offline (no -T, no network) — REF_PATH or REF_CACHE = <dir>/%2s/%2s/%s decoded 5644 records; $REF_CACHE_DIR is never defined in the Skill (P2)

### Input 4 — Variant B: Consensus from BAM: options, IUPAC, indels, real SARS-CoV-2 and human data, bcftools consensus
**Prompt:** Build a consensus FASTA from my SARS-CoV-2 BAM (Illumina and ARTIC nanopore), emit IUPAC codes for hets with a 20% minor-allele threshold and a minimum depth of 10, compare it back to the reference, and apply my phased VCF to the reference for haplotype 1.

**Executed: true.** run/in4x.sh, run/in4.py (43 checks), run/in6.sh (all shipped bash blocks verbatim). Planted-truth synthetic BAM (hom-alt, 50/50, 20%, 3% error, 500 bp gap, depth-2 island, 3-bp deletion + 2-bp insertion) with an independent pysam-pileup oracle; REAL SARS-CoV-2 Illumina PE (200 reads), ARTIC v5.3.2 nanopore (4916 reads, vs MN908947.3) and the human chr22 slice; minimap2 compare-back; bcftools consensus on a phased VCF vs an independent applier.

**What it printed / what was found:** Default consensus reproduced the planted truth: hom-alt called, 3% error not called, 500-bp gap = N, chr2 haplotype (deletion + insertion) exactly equals the planted 230 nt; --show-del/--show-ins/-r/--config (5 names)/unknown-config error/-d 5 (N exactly where independent depth < 5) all correct; real data: consensus equals independent majority at every unambiguous column (871 Illumina, human slice 0 disagreements); ARTIC -a: 29,903 nt, N 0.3%, minimap2 maps it 47S29826M30S MAPQ 60. DEFECTS: (a) in the default Bayesian mode --het-fract and --call-fract are ignored: --ambig, --ambig --het-fract 0.05, 0.9 and the SKILL line-161 command (0.2/0.5) gave byte-identical output (M at the 50/50 and 20% columns); they only act with -m simple, which the Skill never mentions, and there the effective default (no flag) does not equal the printed 0.15. (b) "-a: call all positions (including low coverage)" is wrong: -a only pads to reference start/end with N (chr1 1700 -> 5000), calls inside the span are identical. (c) "verify via samtools consensus --help" exits 1 ("unrecognized option"). (d) -f fastq is line-wrapped at 70 (62 lines for 2 records); -l 0 gives 4-line FASTQ. (e) without --ambig a 20%-minor column is N, not the majority base. bcftools consensus default on a single-sample GT VCF applies IUPAC codes for het SNPs (not mentioned); -H 1/-H 2 equal an independent applier for SNPs, deletion and insertion.

**Scores:** Basic 32/40 | Specialized 47/60 | Total 79/100

**Assertions:**
- [PASS] Default samtools consensus reproduces the planted truth (hom-alt, error suppressed, gap N, indel haplotype exact) — chr2 230 nt == planted haplotype
- [PASS] --ambig is required for IUPAC output, and depth/region/config options behave as documented — M only with --ambig; -d 5 => N exactly where depth < 5; 5 configs accepted
- [FAIL] The het-threshold flags in the shipped example commands (--het-fract 0.2 --call-fract 0.5) change the output — byte-identical for 0.05, 0.9 and 0.2/0.5 in the default Bayesian mode
- [FAIL] The -a description matches behaviour — -a only pads to reference ends; low-coverage calls unchanged
- [PASS] Real-data consensus equals an independent majority vote at unambiguous columns; compare-back with minimap2 works — 0 disagreements at 871 (Illumina) and human-slice columns; ARTIC consensus maps MAPQ 60

### Input 5 — Stress: Majority-vote consensus and compare-to-reference in Python (pysam), verbatim snippets
**Prompt:** I want to do the majority-vote consensus in Python with pysam over chr22:1952-4617 and report where it differs from the reference.

**Executed: true.** run/in5.py (15 checks). SKILL.md consensus_at_position, build_consensus and usage-guide simple_consensus, compare_to_ref exec'd verbatim from the extracted snippets (only file names substituted); synthetic gap/soft-mask data and the REAL human chr22 slice (1157 of 2666 positions covered); oracles: samtools consensus and an independent pysam count.

**What it printed / what was found:** consensus_at_position ran: hom-alt -> C, 3% site -> ref, uncovered -> N. build_consensus over a 1700-bp region returned 1200 characters: pileup skips uncovered columns, so the string is shorter than the region and shifted (min_depth=1: 156 spurious positional differences vs reference, true differences 1). On the real slice simple_consensus returned 1157 characters for a 2666-bp span and compare_to_ref reported 581 differences; the independent count of true differences is 1. A soft-masked (lowercase) reference stretch of 300 bp gave 300 false differences (case-sensitive comparison). pysam.pileup silently drops Q<13 bases, duplicates/secondary reads and de-duplicates overlapping mates (70,937 vs 71,006 reads over 100 columns), contradicting "ignores base qualities". Where coverage is contiguous the logic is right (0-1000: only the planted hom-alt plus the 50/50 tie column). SKILL.md labels its version "Pedagogical Only"; usage-guide compare_to_ref has no caveat.

**Scores:** Basic 26/40 | Specialized 32/60 | Total 58/100

**Assertions:**
- [PASS] consensus_at_position returns the correct base at covered and uncovered sites — C at planted hom-alt, ref at 3% error, N at gap
- [FAIL] build_consensus / simple_consensus return one character per reference position so results are position-aligned — 1200 chars for a 1700-bp region; 1157 for a 2666-bp region
- [FAIL] compare_to_ref reports only true differences from the reference — 581 reported vs 1 true on the real human slice; +300 case artefacts on a soft-masked reference
- [PASS] The pedagogical-only warning and the reason (ignores base quality) are present in SKILL.md — present; usage-guide copies lack it
- [PASS] Output stays in scope — no clinical content; no destructive commands

## Research Veto

- scientific_integrity: PASS — No fabricated citations or data. Factual errors exist (NCBI RefSeq and 1000G rows of the contig/flavour tables; "no clean conversion for BAM") but they are checkable claims that are wrong, not fabricated results; they are P1 findings.
- practice_boundaries: PASS — File-format and reference utility; no clinical or diagnostic content.
- methodological_ground: PASS — M5-as-identity, faidx 1-based vs pysam 0-based, samtools vs bcftools consensus distinction all verified correct. The Python majority vote is labelled pedagogical in SKILL.md (with the correct reason). No principled fallacy.
- code_usability: PASS — All shipped bash blocks, the example script and every Python snippet ran verbatim. BORDERLINE: build_consensus / simple_consensus / compare_to_ref run but return position-shifted output over any coverage gap (581 false differences vs 1 true on the real human slice); usage-guide versions carry no caveat. Recorded as P1, not as unrunnable code.

## Final
Static 72 x 0.4 = 28.8; Execution 74.6 x 0.6 = 44.8; **FINAL 74 / 100 — ⚠️ Beta Only**; deployable: False; veto: none.

Floors: static 72 (>=70 ok), execution avg 74.6 (<75 fails Limited), L1 avg 31.0 (>=28 ok), L2 avg 43.6 (>=42 ok), assertion pass rate 15/25 = 60% (<80% fails Limited). No open P0.

## Recommendations

**[P1] Python build_consensus / compare_to_ref shift over coverage gaps** (inputs [5])
- Problem: build_consensus, simple_consensus and compare_to_ref (SKILL.md + usage-guide) iterate pileup columns, which skip uncovered positions, so the consensus string is shorter than the region and misaligned to the reference: 581 false differences vs 1 true on the real human slice, 156 spurious on the synthetic island. compare_to_ref is also case-sensitive (300 false differences on a soft-masked reference).
- Root cause: Position is inferred from the string index instead of pileup.reference_pos; no upper-casing of the reference.
- Fix: Key by reference_pos and emit N for every uncovered position (or call samtools consensus -a --show-del yes --show-ins no and compare column by column); upper-case the reference; add the pedagogical-only caveat to the usage-guide copies; keep one copy of the function.

**[P1] --het-fract/--call-fract are no-ops in the default mode; -a misdescribed** (inputs [4])
- Problem: SKILL lines 161 and 193 pass --het-fract/--call-fract to the default Bayesian consensus, where they are ignored (identical output for 0.05, 0.9, 0.2/0.5). They only act with -m simple. "-a: call all positions (including low coverage)" (SKILL, usage-guide "Include N for no coverage") is wrong: -a only pads to the reference start/end. "verify via samtools consensus --help" exits 1 (unrecognized option).
- Root cause: Options copied from the simple-mode help without checking which mode they belong to.
- Fix: State that --het-fract/--call-fract need -m simple, or drop them from the Bayesian examples and explain --ambig alone; document that a minor-allele column is N without --ambig; describe -a/-aa as reference-end padding; tell readers to run samtools consensus with no arguments (or man samtools-consensus) for the option list.

**[P1] Contig naming and GRCh38 flavour tables contain factual errors; BAM rename advice is wrong** (inputs [3])
- Problem: "NCBI RefSeq (recent): chr1 / chrM" is wrong (RefSeq FASTA names are NC_000001.11 / NC_012920.1; chr1 only in the assembly-report UCSC column). The "1000G analysis set: ALT no, HLA no" row is wrong (the 1000G GRCh38 reference has 261 _alt and 525 HLA contigs and is the bwakit hs38DH set the table lists as a separate flavour). "for BAM there is no clean conversion -- re-align" is false: samtools reheader gave identical records, identical pileup and a clean Picard validation for chr22 -> 22 and chr1/chr2/chrM -> 1/2/MT.
- Root cause: Reference-identity facts written from memory and not checked against the sources; reheader not considered.
- Fix: Correct the two rows (or link the NCBI assembly report / 1000G README), separate the no-alt analysis set from the full hs38DH set, and replace the re-align advice with: samtools view -H | sed | samtools reheader (only when sequences are identical; compare M5), noting that hg19 chrM differs from GRCh37 MT.

**[P1] prepare_reference.sh and validate block name the dict wrongly for .fasta / .fa.gz** (inputs [1])
- Problem: ${REF%.fa} only strips ".fa": for genome.fasta the dict is genome.fasta.dict and chrom sizes genome.fasta.chrom.sizes; GATK HaplotypeCaller then fails with "Fasta dict file .../genome.dict ... does not exist". The usage-guide validate block prints DICT: OK for the misnamed file. ref.fa.gz gives ref.fa.gz.dict.
- Root cause: Extension stripping hard-coded to .fa.
- Fix: Use base="${REF%.gz}"; base="${base%.*}" (handles .fa/.fasta/.fna, .gz) for the .dict/.chrom.sizes names; make the validate block check that name; drop the duplicated ls glob.

**[P2] Unguarded recipes exit 0 after a partial failure** (inputs [2, 3])
- Problem: The subset recipes (chr1..chrM) exit 0 with a truncated FASTA and a dict containing "chr3 LN:0 M5:d41d8cd9..." when a contig is absent (Ensembl-style names fail for every contig). "seq_cache_populate.pl -root $REF_CACHE_DIR" uses a variable defined nowhere; unset, it treats reference.fa as the root and exits 0 having populated nothing. ug "Extract Multiple Regions" prints confident headers with empty sequences for out-of-range coordinates.
- Root cause: No set -e / existence checks in the guide recipes; undefined variable.
- Fix: Add set -e and a contig-exists check (cut -f1 ref.fa.fai) before subsetting; define REF_CACHE_DIR=/path in the recipe and quote it; bounds-check regions against get_reference_length.

**[P2] Troubleshooting titles and the "index first" advice do not match tool behaviour** (inputs [2])
- Problem: samtools faidx builds the .fai itself when a region is requested; real errors are "[faidx] Could not load fai index" and "Failed to fetch sequence in 1:1-100", not the guide titles. A region wholly beyond the contig end exits 0 with an empty record and only a stderr warning. -i appends /rc to the header (--mark-strand no removes it); -f fastq consensus is wrapped at 70 columns (-l 0 for 4-line FASTQ).
- Root cause: Troubleshooting written from older tool behaviour.
- Fix: Quote the real messages, note the auto-index, document --mark-strand and consensus -l 0.

**[P2] SKILL.md / usage-guide redundancy and small doc defects** (inputs [1, 4, 5])
- Problem: Three copies of the pysam consensus code, faidx recipes and the FAI table appear in both files; min_depth 3 vs 5; the printed "Consensus at chr1:1000000" labels a 0-based argument; pysam.pileup defaults (Q<13, duplicates, overlaps) contradict "ignores base qualities"; create_dict_header has no M5 and is not a .dict; bcftools consensus default applies IUPAC codes for het GTs in a single-sample VCF (not mentioned); script prints each file twice.
- Root cause: Two overlapping documents maintained separately.
- Fix: Keep one copy of each recipe (SKILL.md) and make usage-guide a prompt/troubleshooting page; state pileup filter defaults; note the bcftools -H/IUPAC default.

## Key strengths

- Core reference facts verified against independent computation: faidx 1-based inclusive regions (incl. Ensembl ground truth for 100 kb), pysam 0-based half-open, fai columns, dict SN/LN/M5 (md5 of the uppercase sequence), all equal to a pure-Python/hashlib parse and to Picard 3.5.0.
- The CRAM identity story is right and reproducible: M5 mismatch fails decode ("MD5 checksum reference mismatch"), BAM does not check it, and seq_cache_populate.pl -root plus REF_PATH/REF_CACHE gives offline decode.
- samtools consensus guidance is largely correct on planted truth (default calls, indel haplotype, --ambig, -d, --show-*, --config names, -r) and clearly separates samtools consensus from bcftools consensus; -H 1/-H 2 verified against an independent VCF applier.
- examples/prepare_reference.sh is small, quoted, set -e, idempotent, and every one of the 8 Related Skills paths resolves.

## Method notes
- Checks that failed during development because of MY test design (not Skill defects) were corrected and re-run: `samtools view -c` on a CRAM never decodes bases (so it needs no reference and does no M5 check; full decode used instead); htslib writes every -T reference into the default REF_CACHE (each CRAM step gets its own empty cache dir); pysam.pileup filters differ from samtools consensus counting (compared against raw counts and ties excluded).
- In the logs a `FAIL` line is a Skill behaviour that did not match its documentation; several `PASS` lines assert that a documented claim is false (e.g. the reheader line refutes "re-align", the het-fract line confirms the flags are no-ops), so read the check text, not the word.
- Clone check: `find` for `__pycache__` in the staging clone returned nothing; no writes outside `audits/bio-reference-operations/`.

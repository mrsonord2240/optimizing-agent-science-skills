#!/usr/bin/env python
"""Builds eval_report_bio-reference-operations_result.json and eval_viewer_bio-reference-operations.md from the scores decided by the re-auditor
(this file holds the scores and notes) and the logs in run/logs (what actually printed). Runs on Windows Python; PYTHONIOENCODING=utf-8."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE); LOGS = os.path.join(HERE, 'logs')
SKILL = 'bio-reference-operations'
DESC = 'Generate consensus sequences and manage reference files using samtools. Use when creating consensus from alignments, indexing references, or creating sequence dictionaries.'
SOURCE = 'mrsonord2240/bioSkills@0d22089b40e9195801f3980b64fcbb24ed4e278f:alignment-files/reference-operations'

meta = {
    'skill_name': SKILL, 'description': DESC, 'source': SOURCE, 'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0',
    'audit_kind': 're-audit of the fixed Skill (third agent; first audit 74 Beta Only, fixer 0d22089)',
    'category': 'Data Analysis', 'execution_mode': 'B', 'complexity': 'Moderate', 'n_inputs': 8,
    'n_inputs_note': 'Moderate rule gives 5 (task types: reference index/dict, extraction, contig naming/CRAM identity, consensus). 5 regression inputs re-run the pre-fix inputs against the fixed text; 3 new inputs use planted truth of my own (planted.fa/planted.bam, seed 7; graded-allele fixture, seed 11; mixed mate/unmapped/CRAM header fixture).',
    'executed': '8/8 executed; none was inspected only. One conditional prose claim was not reproduced and is not scored: that reheader on a CRAM warns "Failed to populate reference" when nothing resolves the renamed reference (no warning in any of my CRAM runs, which had M5 in the header).',
    'pre_fix': {'score': 74, 'grade': 'Beta Only', 'static': 72, 'execution_avg': 74.6, 'assertions': '15/25', 'p1_open': 4, 'p2_open': 3},
    'environment': 'WSL science, env alignment-files (audit-envs/alignment-files/TOOLS.md): samtools 1.24, bcftools 1.24, pysam 0.24.1, GATK 4.6.2.0, Picard 3.5.0 (af-picard3), minimap2 2.31. Windows Python only for network fetches and this builder.',
}

veto = {
    'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
    'research_veto': {
        'applicable': True, 'gate': 'PASS',
        'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated data or citations. Every table figure I spot-checked matches real files fetched 2026-09-20 (UCSC hg38 455 contigs / 261 _alt, hg19 chrM 16,571, 1000G hs38DH 3,366 = 261 ALT + 2,385 decoy + 525 HLA + chrEBV, Broad fai identical, hs37d5, Ensembl top-level names, NCBI GRCh38/GRCh37 assembly reports, hg38 chrM sequence == Ensembl MT).'},
        'practice_boundaries': {'result': 'PASS', 'detail': 'File-format and reference utility; no clinical or diagnostic content.'},
        'methodological_ground': {'result': 'PASS', 'detail': 'Majority vote is labelled pedagogical with the right reason; the pysam pileup filters are stated and reproduce (Q13, dup/secondary/QC-fail, overlap dedup 40 vs 80, max_depth 8000). Samtools vs bcftools consensus distinction, M5 identity, 0- vs 1-based coordinates all verified.'},
        'code_usability': {'result': 'PASS', 'detail': 'Every Python block, all 15 samtools consensus command lines (r10_blocks.sh), the faidx/dict/subset/reheader/cache blocks (placeholders substituted) and prepare_reference.sh ran from copies of the shipped text; the bcftools consensus lines were exercised with equivalent commands (input 8). The reheader recipe is runnable but fails loudly on a full hg38 header (4 contigs get the name "na"); recorded as P1, not as unrunnable code.'},
    },
}

static = {
    'functional_suitability': (10, 12, 'Completeness 3, Correctness 3, Appropriateness 4. Far more of the body is verified than before (tables, consensus flags, dict naming, Python consensus). Left: the reheader recipe fails on a full hg38 header (map emits "na"), -T is described as filling "low coverage" (it fills only zero-coverage columns), plain-gzip .gz references fail (bgzip never mentioned).'),
    'reliability': (10, 12, 'Fault tolerance 3, Error reporting 4, Recoverability 3. faidx error table matches real messages and exit codes; subset recipe stops on a missing contig; script exits 1 on no-arg/missing file and is idempotent. The reheader recipe leaves a 0-byte renamed.bam when it fails.'),
    'performance_context': (6, 8, 'Token cost 3, Efficiency 3. One copy of every recipe now; SKILL.md grew 377 -> 456 lines, guide shrank 251 -> 53. The consensus and contig sections are dense but each line earns its place.'),
    'agent_usability': (14, 16, 'Learnability 3, Consistency 4, Feedback design 3, Error prevention 4. min_depth is 3 everywhere, one -a description, explicit traps (--ambig required, omitted --het-fract is not 0.15, dict name rule, primary-only sed, ties). A few numbers are stated without the flag that produces them (chr22 1-vs-2 differences needs -d 3).'),
    'human_usability': (6, 8, 'Discoverability 3, Forgiveness 3. The description still names only consensus/indexing/dictionaries although the body (and the usage-guide prompts) now cover contig renaming, GRCh38 flavour, CRAM references and extraction. faidx auto-indexing and the error table forgive most slips.'),
    'security': (11, 12, 'No credentials, every expansion quoted; a file name containing ; $( ) " and a single quote went through prepare_reference.sh without executing anything. samtools dict -o overwrites an existing dict by design.'),
    'maintainability': (8, 12, 'Modularity 3, Modifiability 3, Testability 2. Single copy of each snippet and dated version notes (checked: -T is in 1.22, instrument --config in 1.17, -aa in 1.18 per NEWS). Still no shipped test data or expected outputs; one script.'),
    'agent_specific': (17, 20, 'Trigger precision 3, Progressive disclosure 3, Composability 4, Idempotency 4, Escape hatches 3. All 8 Related Skills paths resolve; pedagogical-only warning and not-polishing boundary kept; description under-triggers relative to the body.'),
}

# (index, type, label, basic, specialized, assertions[(text, PASS/FAIL, note)], note, kind, scripts)
inputs = [
 (1, 'Canonical', 'Prepare a reference for GATK/Picard: index, dict, chrom.sizes for 12 filename shapes', 35, 54, [
   ('prepare_reference.sh writes <name>.dict and <name>.chrom.sizes for .fa, .fasta, .fna, bgzipped .fa.gz/.fna.gz/.fasta.gz, dotted names, a name with a space, and a hostile name (; $( ) " \')', 'PASS', 'dicts named genome.dict, ref.dict, ref2.dict, refz.dict, Homo_sapiens.GRCh38.dna.primary_assembly.dict, hg38.p14.v2.dict, my genome.dict'),
   ('GATK 4.6.2.0 HaplotypeCaller (VCF with #CHROM, no USER ERROR) and Picard 3.5.0 ValidateSamFile ("No errors found") load the result for all 9 claimed shapes plus .fas', 'PASS', 'noext and GENOME.FA are rejected by the tools themselves ("not a supported reference file type"), not by the Skill; negative control (old genome.fasta.dict only) reproduces the GATK USER ERROR'),
   ('.dict SN/LN/M5 equals an independent md5 of the upper-cased sequence in all 12 dicts; chrom.sizes exact; Picard-made dict identical on the planted N/IUPAC reference', 'PASS', '37/37 checks in r1_check.py; r6 part A'),
   ('The "Check Reference Setup" block prints DICT: OK (derived name) for every shape and DICT: MISSING when only genome.fasta.dict exists', 'PASS', 'verbatim block, REF substituted'),
   ('Error paths exit 1 with a message (no argument, missing file, plain-gzip .gz); re-run is byte-identical', 'PASS', 'plain gzip fails with samtools "please use bgzip"; neither the Skill nor the script usage line mentions bgzip (P2)'),
  ], 'All claimed shapes load in GATK and Picard; only gaps are undocumented bgzip need and a Picard-specific over-statement (Picard 3.5.0 also accepts genome.fasta.dict).', 'regression', ['r1_prepare.sh', 'r1_consume.sh', 'r1_check.py', 'r1c_picard_dict.sh']),
 (2, 'Variant A', 'Extract regions / revcomp / subset / pysam multi-region, error table', 36, 55, [
   ('faidx region, multi-region, whole contig and -i/--mark-strand output equal an independent 1-based inclusive slice of the FASTA (case and N run preserved)', 'PASS', 'synthetic 3-contig reference with widths 80/60/70, soft-mask, N run'),
   ('The faidx error table rows are true: wrong contig rc 1 "Failed to fetch sequence in 22:1-100"; missing FASTA rc 1; region past the end rc 0 "Zero length sequence"; auto-index without prior faidx', 'PASS', 'exact stderr strings match'),
   ('Subset recipe stops (rc 1, no subset.dict) on a missing contig and writes fai + 3-@SQ dict when contigs exist', 'PASS', 'chr3 absent -> chain rc 1; chr1 chr2 chrM -> LN 5000/3007/1000'),
   ('pysam blocks run verbatim; the multi-region loop clips to the contig end and skips an outside region without printing an empty record', 'PASS', 'skip message reads "chr2:5001-3007" (start > end), cosmetic'),
   ('Extracted sequences equal external truth: Ensembl REST chr20:1,400,001-1,500,000 (100,000 bp) and SARS-CoV-2 S gene (3,822 nt ATG...TAA)', 'PASS', '24/24 checks in r2_extract.py'),
  ], 'Every extraction claim reproduces; error table now matches real tool messages.', 'regression', ['r2_extract.py']),
 (3, 'Edge', 'chr22 vs 22, GRCh38 flavour/contig tables against real files, reheader recipe (BAM, CRAM, VCF)', 30, 46, [
   ('Contig-naming and GRCh38-flavour table entries match real files: UCSC hg38/hg19, 1000G hs38DH 3,366 = 261+2,385+525, Broad fai identical, hs37d5, Ensembl names (scaffolds = GenBank accessions), NCBI GRCh38/GRCh37 reports and README, hg38 chrM == Ensembl MT, hg19 chrM 16,571 bp different', 'PASS', 'independent parse of the fetched files; sequence compare for chrM'),
   ('Reheader recipe on the real chr22 BAM gives records identical except RNAME/RNEXT (5,644), identical mpileup, Picard "No errors found"; CRAM reheader decodes identical with -T; SA/XA keep old names and view -x removes them; bcftools annotate --rename-chrs works', 'PASS', '36/36 script checks'),
   ('The documented block (assembly-report map -> awk -> reheader) runs on a BAM with the full hg38/hs38DH header (1000G HG00349)', 'FAIL', 'map.tsv gets "chr11_KI270721v1_random na" x4 (contigs without a RefSeq accession); reheader stops "Duplicate entry na in sam header", rc 1, 0-byte renamed.bam. Adding $7!="na" fixes it (451 contigs renamed, records identical)'),
   ('The Check line (diff SN/LN vs .fai) prints OK for the matching reference and does not for wrong name, wrong length or wrong order', 'PASS', 'three mismatch cases produce a diff, no OK'),
   ('Rename claims about CRAM identity: a 1-base-different reference fails the decode with an MD5 mismatch', 'PASS', '[E::cram_decode_slice] MD5 checksum reference mismatch'),
  ], 'The tables the fixer rebuilt are right (the first audit had them wrong); the one recipe defect appears only on real full-header BAMs, which the fixer did not try.', 'regression', ['r3_contigs.py', 'r3b_mito.sh', 'r0_news.sh']),
 (4, 'Variant B', 'Consensus from real BAMs: SKILL commands, viral command, real-data agreement, version notes', 35, 53, [
   ('The SKILL viral command runs verbatim: one record, no * ; with --show-del yes --show-ins no it is exactly the header LN (29,829) and every depth<10 column is N (or * at a deletion)', 'PASS', 'the nf-core Illumina test BAM has only 200 reads, so 29,810 of 29,829 columns are N'),
   ('ARTIC nanopore BAM: one 29,903 bp record, 99.98% identical to MN908947.3 over called bases', 'PASS', '77 N'),
   ('Real 1000G HG00349 chr20 100 kb: samtools consensus and the majority vote agree at all 92,207 jointly called columns; differences from the Ensembl sequence 120 (1.3 per kb)', 'PASS', 'external truth = Ensembl REST sequence'),
   ('The sentence "chr22 slice: 1 difference by majority vote and by -m simple --call-fract 0.5 --min-BQ 13, 2 by the default Bayesian mode" reproduces with the options as printed', 'FAIL', 'with the options as printed (-d 1) simple gives 5 and Bayesian 4 differences; 1 and 2 need -d 3'),
   ('Version notes match the samtools NEWS: -T added in 1.22, instrument --config in 1.17, -aa in 1.18', 'PASS', 'ncbi/samtools_NEWS.md'),
  ], 'Real-data consensus behaves as documented; one statistic is quoted without the flag that produces it.', 'regression', ['r4_real_consensus.py', 'r0_news.sh']),
 (5, 'Stress', 'Python build_consensus / compare_to_ref verbatim on real slices (the pre-fix 581-difference case)', 36, 55, [
   ('build_consensus returns exactly end-start characters and equals the samtools mpileup -B -Q13 majority (independent parser) at every column with depth>=3: 1,016 columns on chr22 and 92,318 on chr20; uncovered columns are N in place', 'PASS', 'pre-fix version returned 1,157 characters and 581 false differences'),
   ('compare_to_ref on chr22 == the samtools consensus -m simple -d 3 difference list [(3266,T,C)]; identical with an all-lower-case reference', 'PASS', ''),
   ('compare_to_ref on the padded chr20 reference == direct diff against the independent Ensembl sequence (120 differences)', 'PASS', 'external truth'),
   ('The pysam pileup prose (Q<13 dropped, duplicates/secondary skipped, overlapping mates once, max_depth 8000) reproduces', 'PASS', 'overlap: 40 vs 80 with ignore_overlaps=False on planted pairs; 353,982 vs 670,370 pileup bases on the real PE BAM; 9,000 reads -> 8,000'),
   ('Deep columns (depth up to 2,532) are fully used (max_depth raised): called columns == mpileup depth>=3 columns', 'PASS', '1016 == 1016'),
  ], 'The headline defect of the first audit is fixed and holds up on independent methods.', 'regression', ['r4_real_consensus.py', 'r6_planted.py']),
 (6, 'Adversarial', 'NEW: planted-truth reference (N run, IUPAC R/Y, soft-mask, empty contig) and BAM (SNPs, hets, deletion, insertion, gap, edges, decoy reads)', 34, 52, [
   ('build_consensus (verbatim) equals an independent cigar-walk majority at all 6,000 columns: gap, edges, deleted columns N, DUP/secondary/Q5 decoys ignored, MAPQ-0 decoys outvoted', 'PASS', '0 mismatches; het cols 700/900 follow the majority'),
   ('samtools consensus -a --show-del yes --show-ins no is 6,000 characters and equals the planted sample at every column with depth>=6 (SNPs incl. under the reference N run and R/Y, * at the 2-bp deletion, N over the gap and -d 3 zones); default output shows GTA after 4500 (length 6001)', 'PASS', 'samtools and the Python function agree at all 5,696 jointly called columns'),
   ('-a / -aa behaviour as documented: default only contigs with reads; -a pads ctgB to LN 1500; -aa adds the read-less ctgC as 800 N; ends are not padded without -a', 'PASS', ''),
   ('The -T description ("report ref base where consensus unavailable (low coverage; ... FASTA case)") matches behaviour', 'FAIL', '-T fills only zero-coverage columns (gap 1500-1799 -> reference). Columns below -d (depth 2 with -d 3; depth 25 with -d 30) and ambiguous columns stay N. The case claim is right.'),
   ('prepare_reference.sh dict for the hostile reference: M5 = md5 of the upper-cased sequence (N and IUPAC kept), identical to Picard 3.5.0', 'PASS', 'compare_to_ref reports the 30 N-run and 2 IUPAC positions as differences (35 total) - unstated, sensible'),
  ], 'Both consensus paths agree with planted truth; one wording defect on -T.', 'new', ['make_planted.py', 'r6_planted.py']),
 (7, 'Edge', 'NEW: mixed-mate BAM/CRAM with M5, rename recipe, name/length/order mismatches', 34, 52, [
   ('Recipe (verbatim awk + reheader + index) on a BAM with inter-contig mates, "=" mates, unmapped-with-position and fully unmapped reads: 100 records identical except RNAME/RNEXT; Picard "No errors found" against the renamed reference', 'PASS', ''),
   ('CRAM made with -T (M5 in every @SQ): reheader rc 0, header M5 kept, decodes identically with the renamed reference; with the old-named reference it fails loudly', 'PASS', 'no "Failed to populate reference" warning appeared (M5 present, UR pointed at an existing file); the SKILL sentence is conditional and not scored'),
   ('The Check line does not print OK for a reference with different names, a 1-base-longer contig, or reordered contigs', 'PASS', 'Picard 3.5.0 ValidateSamFile and GATK CountReads accept the reordered reference silently, so the Check line is the only guard'),
   ('M5 advice: header M5 equals samtools dict M5 for the right reference and differs only for the 1-base-longer contig', 'PASS', 'a CRAM decode against the longer contig only WARNS (Header @SQ length mismatch) and decodes 100 records: the CRAM MD5 is per slice region'),
  ], 'The recipe generalises to CRAM and awkward mate fields; contig-order mismatch is not mentioned by the Skill (silent).', 'new', ['r7_rename_order.py']),
 (8, 'Variant B', 'NEW: consensus-mode semantics on a graded-allele fixture (depth 20/60, minor 50%-5%) and bcftools consensus note', 37, 56, [
   ('The -m simple rule (IUPAC iff --ambig and minor/major >= --het-fract; else base iff major/depth >= --call-fract; else N) predicts all 48 (het-fract x call-fract x ambig) outputs across 16 columns', 'PASS', 'independent predictor written before comparing'),
   ('Omitted --het-fract is not 0.15 (15% column plain base, explicit 0.15 gives Y); omitted behaves like 0.5-0.6; --call-fract default 0.75', 'PASS', 'matches SKILL "always pass it explicitly"'),
   ('Bayesian mode: --het-fract/--call-fract byte-identical; no IUPAC without --ambig (the 13 ambiguous columns are N); --het-scale 0.01/1/100 gives 0/13/16 IUPAC calls; -A == --ambig', 'PASS', ''),
   ('-d works in both modes; -a pads to LN, -aa == -a for a contig with reads; -T fills the uncovered soft-masked gap in lower case; FASTQ -l 0 gives 4 lines, default wrap 70', 'PASS', ''),
   ('bcftools consensus: default writes IUPAC for unphased 0/1 and phased 0|1, 1|0; -H 1 / -H 2 pick haplotypes; -H A and -s - apply every ALT', 'PASS', 'bcftools 1.24 note text "applying IUPAC codes based on FORMAT/GT"'),
  ], 'Every documented flag statement the fixer added holds on data the fixer never saw.', 'new', ['r8_modes.py']),
]

recs = [
 {'priority': 'P1', 'title': 'Reheader recipe fails on full hg38 headers (map emits "na")', 'observed_in': [3],
  'problem': 'The UCSC->RefSeq map line keeps 4 contigs whose RefSeq column is "na" (chr11_KI270721v1_random, chr22_KI270734v1_random, chrUn_KI270752v1, chr10_KI270825v1_alt). On a hs38DH/UCSC header (1000G BAM) reheader stops with "Duplicate entry na in sam header" and leaves a 0-byte renamed.bam.',
  'root_cause': 'The recipe was verified only on a single-contig BAM.',
  'fix': 'Change the awk filter to $10!="na" && $7!="na" (tested: rc 0, 451 of 3,366 contigs renamed, records identical) and write reheader output to a temp name, mv on success.'},
 {'priority': 'P2', 'title': '-T is described as filling low-coverage columns', 'observed_in': [6, 8],
  'problem': '-T fills only zero-coverage columns with the reference base (in FASTA case). Columns below -d or ambiguous stay N.',
  'root_cause': 'Wording "consensus unavailable (low coverage; ...)" was written without testing a depth-below--d column.',
  'fix': 'Say "columns with no reads (depth 0)"; add "columns below -d and ambiguous columns stay N".'},
 {'priority': 'P2', 'title': 'Description omits contig renaming, extraction, CRAM references', 'observed_in': [3, 7],
  'problem': 'The frontmatter still names consensus / indexing / dictionaries only, while the body and the usage-guide prompts now answer "my BAM says chr22, reference says 22" and "which GRCh38 is this?".',
  'root_cause': 'Description left untouched during the fix.',
  'fix': 'Add "rename/match contig names (chr22 vs 22, GRCh38 flavours), extract regions, CRAM reference resolution" to the description.'},
 {'priority': 'P2', 'title': 'bgzip requirement and test data are undocumented', 'observed_in': [1],
  'problem': 'The script usage line and SKILL accept ".gz", but plain-gzip FASTA (as downloaded from Ensembl/NCBI) fails in faidx ("please use bgzip") and the Skill never says so. There is still no shipped sample data or expected output.',
  'root_cause': '.gz support was tested with bgzip only; test data was declined in the fix.',
  'fix': 'Add one line: "gunzip -c x.fa.gz | bgzip > x.fa.gz2" (or gzip -> bgzip) and a 3-line toy FASTA + expected .dict in examples/.'},
 {'priority': 'P2', 'title': 'Small stated-but-imprecise details', 'observed_in': [1, 3, 4, 6],
  'problem': 'Picard 3.5.0 does accept genome.fasta.dict (only GATK ignores it); the chr22 "1 vs 2 differences" needs -d 3; the dict example shows UR:file:reference.fa but samtools writes an absolute file:/// URL; the UCSC->Ensembl sed one-liner rewrites non-primary contigs too (chr1_KI..._alt -> 1_KI..._alt); the multi-region skip message prints chr2:5001-3007; compare_to_ref reports reference N/IUPAC positions as differences and build_consensus writes N at deleted columns and ignores insertions without saying so.',
  'root_cause': 'Prose written from one tool or one run.',
  'fix': 'One clause each: name GATK for the ignored-dict sentence, add -d 3 to the chr22 sentence, show an absolute UR, restrict the sed to a chr1-22/X/Y/M pattern, print the unclipped end in the skip message, note the N/IUPAC and indel behaviour of the pedagogical functions.'},
]
strengths = [
 'The Python consensus defect is fixed and holds up: build_consensus equals a cigar-walk truth at all 6,000 planted columns and the samtools mpileup majority at 1,016 real chr22 and 92,318 real chr20 columns; compare_to_ref matches samtools consensus and Ensembl.',
 'prepare_reference.sh derives <name>.dict correctly: GATK 4.6.2.0 HaplotypeCaller and Picard 3.5.0 loaded the output for every claimed filename shape, and a hostile file name executed nothing.',
 'The rebuilt contig and GRCh38 tables match real files (UCSC, 1000G, Broad, hs37d5, Ensembl, NCBI reports, chrM sequences) and the reheader recipe gives records identical except RNAME/RNEXT on BAM and CRAM.',
 'Consensus flag documentation (--het-fract/--call-fract/--ambig/--het-scale/-d/-a/-aa/-T case, bcftools IUPAC note, version notes) reproduced on a fixture the fixer never saw; usage-guide dedup lost nothing an agent needs.',
]

# ---------------- arithmetic + checklist ----------------
sub = sum(v[0] for v in static.values()); assert all(0 <= v[0] <= v[1] for v in static.values())
tots = [b + s for (_, _, _, b, s, _, _, _, _) in inputs]
avg = round(sum(tots) / len(tots), 1)
sw = round(sub * 0.4, 1); dw = round(avg * 0.6, 1); score = int(round(sw + dw + 1e-9))
ap = sum(sum(1 for a in i[5] if a[1] == 'PASS') for i in inputs); at = sum(len(i[5]) for i in inputs)
l1 = sum(i[3] for i in inputs) / len(inputs); l2 = sum(i[4] for i in inputs) / len(inputs)
floors = {'static>=80': sub >= 80, 'exec>=85': avg >= 85, 'L1>=32': l1 >= 32, 'L2>=48': l2 >= 48, 'assert>=90%': ap / at >= 0.9}
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
sym = {'Production Ready': '⭐', 'Limited Release': '✅', 'Beta Only': '⚠️', 'Reject': '❌'}[grade]
if not all(floors.values()) and grade == 'Production Ready': grade, sym = 'Limited Release', '✅'
report = {
    'meta': meta, 'veto_gates': veto,
    'static_score': {'subtotal': sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in static.items()}},
    'dynamic_score': {'execution_avg': avg, 'max': 100, 'assertion_pass_rate': {'passed': ap, 'total': at}, 'inputs': [
        {'index': i, 'type': t, 'label': lab, 'status': 'COMPLETED', 'status_flag': '✅' if b + s >= 75 else '⚠️', 'note': note, 'basic': b, 'specialized': s, 'total': b + s,
         'assertions_passed': sum(1 for a in asr if a[1] == 'PASS'), 'assertions_total': len(asr),
         'assertions': [{'text': x, 'result': r, 'note': n} for x, r, n in asr],
         'executed': True, 'execution_note': 'Ran in WSL (env alignment-files) from copies; outputs asserted on content and cross-checked with a second method; scripts: ' + ', '.join(sc), 'kind': kind}
        for (i, t, lab, b, s, asr, note, kind, sc) in inputs]},
    'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': sym, 'deployable': grade in ('Production Ready', 'Limited Release'), 'veto_override': False},
    'key_strengths': strengths, 'recommendations': recs,
}
report['final']['floors'] = floors; report['final']['layer1_avg'] = round(l1, 1); report['final']['layer2_avg'] = round(l2, 1)
for i in report['dynamic_score']['inputs']:
    assert 3 <= i['assertions_total'] <= 5 and i['basic'] + i['specialized'] == i['total'] and i['basic'] <= 40 and i['specialized'] <= 60
assert 2 <= len(strengths) <= 5 and [r['priority'] for r in recs] == sorted(r['priority'] for r in recs)
json.dump(report, open(os.path.join(OUT, f'eval_report_{SKILL}_result.json'), 'w', encoding='utf-8'), indent=2, ensure_ascii=False)
print('static', sub, 'exec avg', avg, 'final', score, grade, 'assertions', ap, '/', at, 'floors', floors)

# ---------------- viewer ----------------
def log(name): return open(os.path.join(LOGS, name), encoding='utf-8', errors='replace').read().splitlines()
def excerpt(name, maxlines=40):
    L = log(name); keep = [l for l in L if not l.startswith('PASS ')]
    keep = [l[:260] for l in keep if l.strip() and not l.startswith('WARNING') and 'setlocale' not in l]
    passes = [l for l in L if l.startswith('PASS ')]
    out = keep[:maxlines]
    if len(keep) > maxlines: out.append('... (%d more lines in run/logs/%s)' % (len(keep) - maxlines, name))
    return passes, out
md = []
A = md.append
A(f'# Eval Viewer — {SKILL} (re-audit of the fixed Skill)\n')
A(f'Generated: 2026-09-20 | Source: `{SOURCE}` | Category: Data Analysis | Mode: B | Complexity: Moderate | N = 8 (5 regression + 3 new)\n')
A('Pre-fix report (archived): 74, Beta Only, 15/25 assertions, 4 P1 + 3 P2. Fix log read but not used as evidence. Everything below is from my own runs; scripts in `run/`, raw output in `run/logs/`. All tests ran in WSL `science` (env `alignment-files`, samtools 1.24, bcftools 1.24, pysam 0.24.1, GATK 4.6.2.0, Picard 3.5.0) from a COPY of the Skill (`run/skill`, byte-identical to the worktree at 0d22089; the worktree was not written to and holds no `__pycache__`).\n')
A('## Skill Veto\n\nT1 Stability PASS | T2 Contract PASS | T3 Determinism PASS | T4 Security PASS\n')
A('- stability: every block/script ran; no crashes or loops. The one documented recipe that fails (reheader on a full hg38 header) fails loudly, not randomly.\n- contract: frontmatter has name, description, tool_type, primary_tool, license.\n- determinism: `samtools consensus --ambig -d 3` gave one md5 (`bdc7098e...`) on 3 runs; all outputs reproduced on the second pass of `run_all.sh`.\n- security: no eval/exec; a file named `we"ird\'name.v2.fasta` inside a directory named `h;x $(echo pwned)` went through `prepare_reference.sh` and `pwned` was never executed.\n')
A('## Static score (25 criteria)\n\n| Category | Score | Note |\n|---|---|---|')
for k, v in static.items(): A(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
A(f'\n**Static subtotal: {sub}/100** (first audit 72)\n')
A('## Classification\n\nData Analysis (category 3), Mode B (CLI/script: `samtools`, `bcftools`, `examples/prepare_reference.sh`, plus pysam snippets). Complexity Moderate; N = 8 because the brief requires the 5 pre-fix inputs as regression tests plus at least 2 new ones.\n')
A('## Summary Table\n\n| Input | Type | Kind | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|---|')
for i in report['dynamic_score']['inputs']:
    A(f"| {i['index']} | {i['type']} | {i['kind']} | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['status_flag']} |")
A(f"\n**Execution average: {avg} / 100** (first audit 74.6) | **Assertion pass rate: {ap}/{at}** (first audit 15/25) | Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60\n")
A('### Regression against the first audit\n\n| Pre-fix finding | Now |\n|---|---|')
for a, b in [
 ('P1 build_consensus / simple_consensus / compare_to_ref shift after any gap (581 false differences)', 'Fixed. Exact length, equals mpileup majority and samtools consensus at every jointly called column on real and planted data (inputs 5, 6).'),
 ('P1 --het-fract/--call-fract no-ops in default mode; -a misdescribed; "verify via --help" exits 1', 'Fixed. Verified on a 48-configuration grid I predicted independently (input 8); `samtools help consensus` rc 0 confirmed.'),
 ('P1 RefSeq / 1000G rows wrong; "re-align" advice wrong', 'Fixed. Table figures match the real files (input 3). New defect found in the new recipe (P1 below).'),
 ('P1 prepare_reference.sh / validate block name the dict wrongly for .fasta and .fa.gz', 'Fixed. GATK 4.6.2.0 and Picard 3.5.0 load all 9 claimed shapes (input 1).'),
 ('P2 unguarded recipes, undefined $REF_CACHE_DIR, empty records', 'Fixed. && chains stop, cache block builds the cache and decodes 5,644 records with no -T, multi-region loop clips.'),
 ('P2 troubleshooting titles vs real messages; "index first"', 'Fixed. The faidx error table strings and exit codes match samtools 1.24.'),
 ('P2 redundancy: three consensus copies, min_depth 3 vs 5, VN, IUPAC default', 'Fixed. One build_consensus (min_depth 3), guide is 53 lines.')]:
    A(f'| {a} | {b} |')
A('\n### Judged as the fixer left them\n')
A('- **Description** (unchanged): still consensus / indexing / dictionaries only; the body now also handles contig renaming, GRCh38 flavour, CRAM references. Under-triggers (P2).\n- **Missing test data** (not added): no sample data or expected output shipped; testability stays 2/4 (P2 with the bgzip gap).\n- **Version notes** (carried over): `-T` in 1.22, instrument `--config` in 1.17 and `-aa` in 1.18 are all correct per the samtools NEWS (`run/logs/r0_news.txt`). Nothing to change.\n- **Pilon/medaka** mention: gone; the boundary sentence "not iterative, not an assembly-polishing tool" remains and is true.\n- **usage-guide.md dedup** (251 -> 53 lines): I compared every deleted section with SKILL.md. Everything an agent needs survives (install line, faidx/dict/consensus commands, subset, sizes, CRAM `-T`, troubleshooting -> error table, tips -> their sections). Lost only: the tip "keep index files beside the FASTA" and a `nreferences` print; neither matters.\n- **Fix-introduced or left defects**: see recommendations. Nothing in the fix broke a previously working statement.\n')
A('## Detailed outputs\n')
logs_for = {1: ['r1_consume.txt', 'r1c_picard_dict.txt', 'r1_check.txt'], 2: ['r2_extract.txt'], 3: ['r3_contigs.txt'], 4: ['r4_real_consensus.txt'], 5: [], 6: ['r6_planted.txt'], 7: ['r7_rename_order.txt'], 8: ['r8_modes.txt']}
prompts = {
 1: 'I need to prepare my reference genome for GATK and Picard: index it, make the sequence dictionary and chrom sizes. My file is called genome.fasta (other times ref.fa, ref2.fna, GRCh38.primary_assembly.fa.gz, hg38.p14.v2.fasta).',
 2: 'Extract chr1:1000-2000, several regions, the reverse complement, a whole chromosome, and make a chr1-chr2-chrM subset reference; tell me what happens if I ask for a contig that is not there.',
 3: 'My BAM says chr22 but my reference says 22 (and another BAM is on a full hs38DH header): fix it without re-aligning, tell me which GRCh38 this is, and what the Ensembl/RefSeq/UCSC names are. Same for a CRAM.',
 4: 'Generate a consensus from my BAM: viral (SARS-CoV-2, IUPAC, min depth 10), the nanopore ARTIC BAM, and a real human slice; which options matter?',
 5: 'Use the Python majority-vote consensus and compare it with the reference on my real chr22 slice and the 1000G chr20 slice.',
 6: '(new) My reference has an N gap, IUPAC codes and soft-masked repeats; the BAM has SNPs, hets, an indel, a coverage gap and junk reads. Build the consensus with samtools and with the Python function, and list differences from the reference.',
 7: '(new) The BAM has inter-contig mates and unmapped reads, the CRAM has M5 tags; rename the contigs to 1/2/3, and tell me whether references with other names, lengths or contig order will still work.',
 8: '(new) What exactly do --het-fract, --call-fract, --ambig, --het-scale, -d, -a/-aa and -T do, in both consensus modes, and how does bcftools consensus treat het genotypes?'}
for i in report['dynamic_score']['inputs']:
    n = i['index']
    A(f"### Input {n} — {i['type']} ({i['kind']}): {i['label']}\n")
    A(f'**Prompt:** {prompts[n]}\n')
    A(f"**Mode / execution:** B; executed: true; scripts: {i['execution_note'].split('scripts: ')[1]}\n")
    for lg in logs_for[n]:
        passes, ex = excerpt(lg)
        A(f'**Log `run/logs/{lg}`: {len(passes)} PASS lines; non-PASS lines (observations and FAILs) below**\n')
        A('```\n' + '\n'.join(ex) + '\n```\n')
        if lg in ('r2_extract.txt', 'r1_check.txt'):
            A('PASS checks: ' + '; '.join(p[5:100] for p in passes[:12]) + ('; ...' if len(passes) > 12 else '') + '\n')
    if n == 5:
        A('Output of the same run (see input 4 log, sections INPUT 5 / 5b) and of input 6 sections C / D. Key lines:\n```\n' + '\n'.join(l[:260] for l in log('r4_real_consensus.txt') if 'compare_to_ref' in l or 'INPUT 5' in l or 'build_consensus' in l)[:2400] + '\n```\n')
    A(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100\n")
    A('**Assertions:**\n' + '\n'.join(f"- [{a['result']}] {a['text']} — {a['note']}" for a in i['assertions']) + '\n')
    A(f"**Note:** {i['note']}\n")
A('## Extra regression checks (run/logs/r10_blocks.txt, r9_misc.txt, r0_news.txt, r3b_mito.txt, r1c_picard_dict.txt)\n')
A('All 15 `samtools consensus` command lines printed in SKILL.md ran as written (rc 0, non-empty FASTA/FASTQ; profiles hifi, r10.4_sup, ultima, hiseq accepted; `-T`, `-a`, `-f fastq -l 0` produce the expected shapes). Cache block (verbatim, HOME set): cache file `19/22/b52e1af6...` created, CRAM decodes 5,644 records with no `-T` through `REF_PATH`, and fails loudly when no cache/reference resolves; `samtools dict -a GRCh38 -s "Homo sapiens"` writes `AS:GRCh38 SP:Homo sapiens`; the dict `UR:` is an absolute `file:///` URL (the SKILL example shows `file:reference.fa`); `consensus -> minimap2 -a` block runs (3 SAM records); consensus md5 identical x3; hostile file name safe; prepare_reference.sh idempotent; plain-gzip FASTA fails with the samtools bgzip message; Picard 3.5.0 finds `genome.fasta.dict` (ScatterIntervalsByNs rc 0 with either dict name, rc 1 with none) so only GATK ignores it; hg38 chrM == Ensembl MT and hg19 chrM (16,571 bp) differs from GRCh37 MT; NEWS: -T 1.22, --config 1.17, -aa 1.18.\n')
for lg in ('r10_blocks.txt', 'r9_misc.txt', 'r1c_picard_dict.txt', 'r3b_mito.txt', 'r0_news.txt'):
    A('```\n' + '\n'.join(l[:200] for l in log(lg) if l.strip() and 'setlocale' not in l)[:3500] + '\n```\n')
A('## Final\n')
A(f"Static {sub} x 0.4 = {sw}; execution {avg} x 0.6 = {dw}; **final {score} / 100, {sym} {grade}**, deployable {report['final']['deployable']}, veto_override False.\n\nFloors: " + ', '.join(f'{k} {"ok" if v else "MISSED"}' for k, v in floors.items()) + '.\n')
A('Open: P0 none; P1 one (reheader recipe on full hg38 headers); P2 four (details in the JSON).\n')
A('### Optimization recommendations\n')
for r in recs: A(f"**[{r['priority']}] {r['title']}**  \nObserved in: {r['observed_in']}  \nProblem: {r['problem']}  \nRoot cause: {r['root_cause']}  \nFix: {r['fix']}\n")
A('### Key strengths\n' + '\n'.join('- ' + s for s in strengths) + '\n')
open(os.path.join(OUT, f'eval_viewer_{SKILL}.md'), 'w', encoding='utf-8').write('\n'.join(md))
print('viewer written', os.path.getsize(os.path.join(OUT, f'eval_viewer_{SKILL}.md')), 'bytes')

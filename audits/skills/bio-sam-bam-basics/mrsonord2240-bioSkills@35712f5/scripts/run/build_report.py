"""Builds eval_report_bio-sam-bam-basics_result.json and eval_viewer_bio-sam-bam-basics.md from out/results.jsonl
(the asserted checks that actually ran) plus the scoring decisions written below. Run from anywhere:
    python run/build_report.py
"""
import json, os
from collections import defaultdict

RUN = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(RUN)
rows = [json.loads(l) for l in open(RUN + '/out/results.jsonl', encoding='utf-8')]
by = defaultdict(list)
for r in rows:
    by[r['input']].append(r)
tally = {k: (sum(1 for r in v if r['pass'] is True), sum(1 for r in v if r['pass'] is not None)) for k, v in by.items()}
TOTAL_PASS = sum(a for a, b in tally.values())
TOTAL_CHK = sum(b for a, b in tally.values())
assert TOTAL_CHK - TOTAL_PASS == 1, 'expected exactly one failing check (the CRAM round-trip claim)'

A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
PASS, FAIL = 'PASS', 'FAIL'

inputs = [
    dict(index=1, type='Canonical', label='Regression: inspect the real human PE BAM (header, FLAG decode, coordinates, counts, regions, view_bam.py, Rsamtools, usage-guide dedup)',
         basic=35, specialized=54,
         note='All 40 asserted checks pass (regress in1/in1b, dedup_check, misc_claims) + Rsamtools scanBam run; pre-fix defects (view_bam crash without an index, unlabelled 0-based rows, multi-region duplicates, unparseable SAM example) are gone.',
         exec_note='executed: 5644-record nf-core BAM read by samtools 1.24 + pysam 0.24.1 + Rsamtools 2.22.0 (r.sh); every SKILL.md/usage-guide snippet and shipped example ran from the run/skill copy.',
         assertions=[
             A('FLAG decoding (samtools flags, 12-row table, 99/147 text, pysam is_* properties) equals an independent SAM-spec decoder; coordinate rules (POS = reference_start+1, view chr:a-b == fetch(a-1,b), faidx 1-based) hold on real reads', PASS, 'in1 + in1b + dedup_check + misc_claims: 40/40 pass (flagstat primary 5642 == view -c -F 2304; NM filter 5516 == pysam scan; r/rb/rc x SAM/BAM/CRAM all read 5644)'),
             A('Shipped examples/view_bam.py works on the canonical indexed BAM and on an UNINDEXED copy, with a labelled 0-based coordinate column', PASS, 'indexed: Mapped 5642 Unmapped 2 (from index); unindexed: same numbers (from scan); header row "name chrom:start(0-based) strand cigar"'),
             A('Instructions degrade safely on multi-region, wrong contig and missing index and say so', PASS, 'view r1 r2 = 7356 rows vs 5426 truth as documented; wrong contig warning text and exit 0 as documented; missing index message as documented'),
             A('usage-guide dedup (210 -> 53 lines) lost nothing the agent needs', PASS, '33/33 facts of the old guide still present in SKILL.md/usage-guide.md, 12/12 advertised prompts have a command or section, 9/9 claims the fix log calls removed are absent, both usage-guide pointers resolve; only "Phred-scaled", "PL:ILLUMINA", "context manager" wording dropped (judged immaterial)'),
             A('SAM example block and the R bullet work as written', PASS, 'SKILL.md SAM block extracted verbatim parses with samtools view -b and reads back as read1 chr1:100 8M; Rsamtools scanBam: 5644 records, pos 1952, flag 99, 130M13S'),
         ]),
    dict(index=2, type='Variant A', label='Regression: BAM<->SAM<->CRAM conversions with samtools, pysam and convert_formats.sh',
         basic=35, specialized=54,
         note='All 40 checks pass; the helper now passes the reference for CRAM input, accepts .BAM, refuses input==output (same path, ./path, symlink) and exits non-zero without a usable reference.',
         exec_note='executed: real BAM/CRAM (CRAM UR path dead, REF_PATH empty, so only the 3rd argument can resolve it); 5644 records compared as SAM text with sorted tags.',
         assertions=[
             A('Every documented conversion (BAM->SAM->BAM->CRAM->BAM, pipe form) round-trips 5644 records with identical fields and tag sets', PASS, 'md5 of tag-sorted SAM text identical for o.bam, o.cram, o2.bam, pipe.bam; only tag ORDER differs after CRAM (5644 of 5644 tag sets identical, 2 orders identical), as SKILL.md says'),
             A('pysam conversions (w, wb, wc + reference_filename) preserve all records and the mode table is right', PASS, "p.sam/p.bam/p.cram identical to original; 'r' reads a BAM; 'rc' with reference reads CRAM"),
             A('convert_formats.sh performs SAM->BAM, BAM->SAM, BAM->CRAM(+ref) and CRAM->BAM/SAM(+ref) correctly, including on the original nf-core CRAM whose header UR is dead', PASS, 'h3.bam/h3.sam identical to the original 5644 records; without the reference: rc 1, no silent success'),
             A('Helper guards: uppercase .BAM works; input==output (same path, ./path, symlink) exits 1 and leaves the input at 5644 records; missing input and missing CRAM reference exit non-zero', PASS, 'rc=1, rc2=1, rc3=1 with 5644 records intact each time; h5.BAM identical to the original'),
             A('Format statements hold: SAM > BAM > CRAM in size; header preserved; CRAM without -T warns and embeds', PASS, 'sizes ordered; @SQ M5/UR added at CRAM write; -C without -T exit 0 with embed_ref=2 warning'),
         ]),
    dict(index=3, type='Edge', label='Regression: synthetic edge SAM (unmapped-with-position, secondary/supplementary, hard/soft clips, N, MAPQ 255/0, 66,000-op CIGAR, empty BAM)',
         basic=35, specialized=53,
         note='All 48 checks pass; view_bam.py now labels unmapped rows (placed: ctgA:49 ... unmapped; unplaced: * ... unmapped) and handles an empty unindexed BAM.',
         exec_note='executed: synthetic (seeded) 15-record BAM built with samtools sort/index; independent CIGAR model from the SAM spec.',
         assertions=[
             A('CIGAR semantics stated by the Skill (N not covered, S kept in SEQ, H absent, M overloaded, =/X, P) match an independent spec model and pysam', PASS, 'r2_spliced: 50 covered positions vs span 1050; hard clip query_length 30 vs infer_read_length 50; P consumes neither'),
             A('Secondary vs supplementary arithmetic and flag bits hold', PASS, '-F 256 = 14, -F 2304 = 13, -F 2048 = 14 on the 15-record BAM'),
             A('Unmapped-with-position, "*" SEQ/QUAL, MAPQ 255/0, mate fields, TLEN sign, 66,000-op CIGAR and empty BAM behave as the Skill says', PASS, 'placed unmapped returned by region query; "* *" printed; TLEN +90/-90; pysam sees 66000 ops; empty BAM 0 records'),
             A('Shipped view_bam.py copes with the edge inputs', PASS, 'empty unindexed and indexed BAM: Mapped 0 Unmapped 0; synthetic BAM: unmapped rows labelled, no None:-1; SAM input reads'),
             A('Skill alone answers the prompt (bases consumed per op, TLEN sign, unplaced vs placed unmapped)', PASS, 'consumption table + TLEN sentence present and correct'),
         ]),
    dict(index=4, type='Variant B', label='Regression: CRAM offline (resolution order, REF_CACHE recipe, proving a CRAM readable, archive lossless)',
         basic=35, specialized=54,
         note='All 36 checks pass; the corrected CRAM section now matches samtools 1.24: view -c does not decode, view -o /dev/null does, wrong reference is refused with MD5 mismatch.',
         exec_note='executed: real human CRAM plus CRAMs written here; 1.22+ network default checked with a bogus proxy and by inspecting libhts.',
         assertions=[
             A('Resolution order -T > REF_CACHE > REF_PATH > @SQ UR and the seq_cache_populate.pl layout hold', PASS, 'poisoned-cache/poisoned-path/-T/UR experiments each behave in the stated order'),
             A('The recommended check `samtools view -o /dev/null f.cram && echo ok` fails (no "ok", rc 1) with the reference unreachable and prints ok when it is reachable; view -c / flagstat / idxstats / quickcheck pass without the reference', PASS, 'view -c 5644 rc 0, quickcheck rc 0, view -o /dev/null rc 1 "Unable to fetch reference"; stats fails; mid-file corruption: quickcheck rc 0 but full decode rc 1'),
             A('A different reference is refused, not silently accepted; silent only with ignore_md5=1', PASS, 'MD5 checksum reference mismatch rc 1; ignore_md5=1 rc 0 with different SEQ column'),
             A('htslib >= 1.22 does no network lookup by default; archive preset is lossless and smallest', PASS, 'no ebi/ena/proxy activity; libhts holds no ebi.ac.uk/ena/cram string; archive records identical to source, smallest profile'),
             A('view_bam.py on CRAM: indexed CRAM gives 5642/2, unreachable reference gives exit 1 with the reference hint, 3rd argument resolves it', PASS, 'Mapped 5642 Unmapped 2 (scan); "Error reading ...: truncated file (CRAM needs its reference: pass reference.fa as the 3rd argument)"; with 3rd arg rc 0'),
         ]),
    dict(index=5, type='Stress', label='Regression: six aligners on a synthetic repeat genome (MAPQ scale, -q, tags, @PG chain, fixmate/markdup, failure-mode table)',
         basic=34, specialized=51,
         note='All 39 checks pass (in5, in5c mapDamage, tags_check). Table rows for DRAGEN, Cell Ranger/STARsolo, featureCounts/RSEM and pbmm2 could not be run and are stated as fact without a marker.',
         exec_note='executed: bwa 0.7.19, bwa-mem2, minimap2 (+--eqx, --cs, splice), bowtie2 (end-to-end and --local), hisat2, STAR on a seeded synthetic genome; fgbio 4.1.1 AnnotateBamWithUmis; mapDamage 2.2.2; bcftools 1.24. DRAGEN, Cell Ranger, featureCounts, RSEM, pbmm2 NOT run.',
         assertions=[
             A('MAPQ table rows hold: bwa/bwa-mem2/minimap2 0-60 max 60, HISAT2 {0,1,60}, Bowtie2 max 42 (97.4% of records) and max 44 with --local (94.7%), STAR {0,1,3,255} with -q 30 == -q 255', PASS, 'histograms in out/in5.txt; Bowtie2 -q 60 keeps 0'),
             A('Tag/provenance rows hold: NM/MD from bwa, MC from bwa mem, ms in minimap2 unrelated to fixmate, cs with --cs, RX from fgbio AnnotateBamWithUmis, HI 1-based, @PG names the aligner', PASS, 'tags_check 6/6 and in5 tag checks pass'),
             A('The corrected failure-mode table is true: markdup refuses (rc 1, "no ms score tag. Please run samtools fixmate"), MD/NM not needed by bcftools mpileup or mapDamage, =/X gives identical mpileup', PASS, 'mpileup body md5 identical with/without MD/NM and on eqx vs M; mapDamage misincorporation/dnacomp/lgdistribution bodies identical with MD/NM stripped'),
             A('@PG chain links through PP and the head -1 command names the aligner', PASS, 'six-line chain linear; example IDs in SKILL.md (bwa-mem, samtools.1) are illustrative, real IDs are bwa / samtools'),
             A('Rows that could not be run (DRAGEN --mapq-max, Cell Ranger/STARsolo MAPQ 255 and CB/UB, featureCounts/RSEM tag consumers, pbmm2) are marked as unverified in the Skill', FAIL, 'stated as fact with no marker; the fix log admits they are unverifiable'),
         ]),
    dict(index=6, type='Stress', label='NEW: multi-region recipes (-M, -M -L, --region-file, pysam fetch_regions) vs a full-scan truth: overlapping, adjacent, nested, gap, identical, chained, multi-contig, 60 + 80 random sets',
         basic=36, specialized=55,
         note='All 23 checks pass. Truth = parse of `samtools view` (no region) with an independent overlap model; fetch_regions() extracted verbatim from SKILL.md.',
         exec_note='executed: real 5644-record BAM (10 named sets + 60 random) and the 15-record synthetic multi-contig BAM (80 random sets) with samtools 1.24 and pysam 0.24.1.',
         assertions=[
             A('-M, -M -L bed, --region-file and fetch_regions() each return exactly the full-scan truth (each record once) on 10 named region sets', PASS, 'overlap 5426, adjacent 5550, nested 5550, gap-9bp 802, gap-100bp 802, identical-twice 2732, chained 1170, reverse-order 5058, single-base 539, far-apart 539; default query rows = per-region sum (7356, 7112, 7480, 950, ...)'),
             A('The same on 60 random multi-region sets (real BAM) and 80 random multi-contig sets (synthetic BAM incl. placed-unmapped, secondary, supplementary, 66,000-op CIGAR)', PASS, '140/140 sets equal truth for all four recipes; default duplicates in 19 of 60 real-BAM sets; fetch_regions never repeated a record'),
             A('Skill numbers reproduce (default 7356, -M/-M -L/--region-file 5426) and the BED convention (0-based half-open) holds for both -L and --region-file', PASS, 'single-base BEDs at 4 positions select exactly the 1-based base'),
             A('Error paths behave as documented or fail loudly: -M on an unindexed BAM exits 1 naming the index; an unknown contig in a multi-region call warns with exit 0; fetch_regions with a wrong contig raises ValueError', PASS, 'the Skill does not itself say -M needs an index (noted, P2)'),
         ]),
    dict(index=7, type='Edge', label='NEW: 32-record HAND-WRITTEN SAM with planted truth (every FLAG bit, CIGAR ops M/I/D/N/S/H/=/X/P, placed/unplaced unmapped, secondary/supplementary, "*" SEQ, three pair kinds) + view_bam.py matrix + convert_formats.sh',
         basic=33, specialized=50,
         note='53 of 54 checks pass; the failing check is a Skill statement: "a round trip keeps every field and tag but not the tag order" is false for CRAM (=/X CIGAR rewritten to M; NM/MD added). view_bam.py raw traceback on a non-numeric limit.',
         exec_note='executed: expectations written by hand from the SAM spec before running; SAM, sorted BAM, unsorted BAM, unindexed BAM, unmapped-only BAM (indexed and not), empty SAM/BAM, CRAM with and without its reference, missing file, text file, truncated BAM.',
         assertions=[
             A('FLAG decoding and counts equal hand truth: 12 single bits, 1536/73/133/65/129, and 12 filters (-f/-F/-q, -F 2304 = 28 of 32)', PASS, 'samtools flags and view -c match all hand counts; Skill FLAG table hex==decimal and meanings match the spec'),
             A('CIGAR consumption table, span/SEQ formulas, N not covered, soft vs hard clip, TLEN (+71/-71, 0 for mate-unmapped and cross-contig), "*" SEQ and SA:Z shape are correct', PASS, 'all 9 ops match htslib; 17 hand-written (SEQ length, span) pairs match; TLEN as planted'),
             A('view_bam.py: correct counts and exit codes on SAM, sorted/unsorted/unindexed BAM, unmapped-only BAM, empty SAM/BAM, CRAM with the reference reachable / unreachable / 3rd argument; readable errors on missing, text and truncated files', PASS, '28/4 mapped/unmapped agrees with -F 4 / -f 4 on every file; unmapped-only 0/4; empty 0/0; CRAM without reference exit 1 with hint; all errors readable'),
             A('convert_formats.sh SAM->BAM->CRAM(+ref)->SAM/BAM on the hand SAM: rc 0, 32 records; no-reference CRAM output and input==output refused', PASS, 'SAM->BAM byte-identical records; BAM->CRAM->SAM/BAM agree with each other; rc 1 with messages for the two guarded cases'),
             A('SKILL.md: "a round trip keeps every field and tag but not the tag order" (CRAM)', FAIL, 'CRAM leg turned 4=1X4= into 9M and added MD:Z/NM:i to 16 of 30 realistic records (reference available); MAPQ of an unmapped read 10->0'),
         ]),
    dict(index=8, type='Adversarial', label='NEW: CRAM reference states on a second real dataset (nf-core SARS-CoV-2): -T, UR, gone, REF_PATH/REF_CACHE, the Skill recipe verbatim, wrong/missing-contig reference, ignore_md5, embed_ref, -C without -T; =/X and MD through CRAM on real minimap2 --eqx output',
         basic=33, specialized=50,
         note='23 of 23 checks pass, but two of them confirm that the Skill\'s CRAM round-trip sentence is inaccurate on real aligner output (=/X lost, MD added).',
         exec_note='executed: every state decoded with the Skill\'s own check and independently by md5 of columns 1-11 against the source BAM; HOME redirected so no ~/.cache/hts-ref could rescue a decode; pysam read attempt with the reference gone.',
         assertions=[
             A('For every reference state the Skill\'s check `view -o /dev/null f.cram && echo ok` gives the right verdict and an independent decode agrees', PASS, '-T ok; UR ok; gone -> no "ok", rc 1 "Unable to fetch reference"; REF_PATH (M5-named) ok; REF_CACHE ok; embed_ref=1 ok with nothing reachable; wrong reference and lacking-contig reference fail (MD5 mismatch)'),
             A('The HPC recipe in SKILL.md runs verbatim: cache created under $HOME/cram_cache, quickcheck silent, full-decode check prints ok', PASS, 'one cache file created; ok, rc 0'),
             A('view -c / flagstat / idxstats / quickcheck succeed with the reference gone while stats and pysam iteration fail loudly; ignore_md5=1 makes the wrong-reference decode silent', PASS, 'view -c 200, flagstat 200+0, idxstats 197/3, qc rc 0; stats non-zero; pysam OSError; ignore_md5 rc 0 with different SEQ column'),
             A('-C without -T and no reachable reference exits 0 with the embed_ref=2 warning and the CRAM decodes with no reference', PASS, 'as SKILL.md states'),
             A('SKILL.md: "a round trip keeps every field and tag but not the tag order" holds for real aligner output', FAIL, 'minimap2 --eqx BAM: 5000/5000 reads lose their =/X ops to M in the CRAM; minimap2 default BAM: MD:Z appears on 5000 reads that had none'),
         ]),
]
for i in inputs:
    i['total'] = i['basic'] + i['specialized']
    i['status'] = 'COMPLETED'
    i['status_flag'] = '✅'
    i['assertions_passed'] = sum(1 for a in i['assertions'] if a['result'] == PASS)
    i['assertions_total'] = len(i['assertions'])
    i['executed'] = True
    i['execution_note'] = i.pop('exec_note')
    assert 3 <= i['assertions_total'] <= 5
    assert i['basic'] <= 40 and i['specialized'] <= 60 and i['total'] <= 100
    i['checks'] = {'passed': tally[str(i['index'])][0], 'total': tally[str(i['index'])][1]}

execution_avg = round(sum(i['total'] for i in inputs) / len(inputs), 1)
cats = {
    'functional_suitability': (10, 12, 'Completeness 4 / Correctness 3 / Appropriateness 3. Every promised use case now has a working recipe (multi-region added); 302 of 303 asserted checks hold. Correctness loses a point for the over-general CRAM round-trip sentence and unverified aligner/assay rows; SKILL.md carries MAPQ, tag and provenance tables beyond "basics".'),
    'reliability': (9, 12, 'Fault tolerance 3 / Error reporting 3 / Recoverability 3. view_bam.py handles no index, empty, unmapped-only, SAM, CRAM (with/without reference) and exits 1 with readable messages; convert_formats.sh guards input==output and missing CRAM reference. Left: raw ValueError on a non-numeric limit, header-only partial output left behind when samtools fails, pysam\'s "truncated file" wording for a missing CRAM reference.'),
    'performance_context': (6, 8, 'Token cost 3 / Efficiency 3. usage-guide duplication removed (210 -> 53 lines), one copy of each fact; SKILL.md grew to 431 lines with no references/ layering.'),
    'agent_usability': (14, 16, 'Learnability 4 / Consistency 3 / Feedback design 3 / Error prevention 4. Coordinates, MAPQ portability, CRAM reference, multi-region duplicates and secondary-vs-supplementary footguns are explicit with checked commands; example @PG IDs differ from real ones, and a few rows carry no verification marker.'),
    'human_usability': (6, 8, 'Discoverability 3 / Forgiveness 3. Natural trigger wording; helper accepts any-case extensions and points at the CRAM reference; non-numeric limit still crashes.'),
    'security': (11, 12, 'Credential 4 / Input validation 3 / Data safety 4. No secrets, no eval, variables quoted; the input==output guard closes the data-loss path found in the first audit; input existence is left to samtools.'),
    'maintainability': (9, 12, 'Modularity 3 / Modifiability 3 / Testability 3. Facts live once; examples print checkable output; no shipped test data or expected outputs, and version-pinned claims (htslib 1.22 default) need re-verification when tools move.'),
    'agent_specific': (17, 20, 'Trigger precision 3 / Progressive disclosure 3 / Composability 4 / Idempotency 4 / Escape hatches 3. Related Skills all exist; conversions deterministic and refuse to overwrite their input; no explicit when-not-to-use.'),
}
static_total = sum(v[0] for v in cats.values())
static_w = round(static_total * 0.4, 1)
dyn_w = round(execution_avg * 0.6, 1)
score = int(round(static_w + dyn_w))
ap = sum(i['assertions_passed'] for i in inputs)
at = sum(i['assertions_total'] for i in inputs)
l1 = sum(i['basic'] for i in inputs) / len(inputs)
l2 = sum(i['specialized'] for i in inputs) / len(inputs)
grade = 'Production Ready' if score >= 85 else 'Limited Release' if score >= 75 else 'Beta Only' if score >= 60 else 'Reject'
symbol = {'Production Ready': '⭐', 'Limited Release': '✅', 'Beta Only': '⚠️', 'Reject': '❌'}[grade]
floors = (static_total >= 80, execution_avg >= 85, l1 >= 32, l2 >= 48, ap / at >= 0.9)
assert all(floors), floors

recs = [
    dict(priority='P2', title='CRAM round trip is not lossless: =/X become M, NM/MD get added', observed_in=[7, 8],
         problem='SKILL.md says a CRAM round trip "keeps every field and tag but not the tag order". On a hand SAM the =/X CIGAR of one read became 9M, and on real minimap2 --eqx output 5000 of 5000 reads lost their =/X ops; on a minimap2 BAM without MD, decoding with the reference added MD:Z to all 5000 reads (unmapped-read MAPQ also becomes 0).',
         root_cause='The sentence was verified only on the nf-core BAM, whose CIGARs use M and whose reads already carry NM/MD.',
         fix='Replace with: a CRAM round trip preserves reads and quality but rewrites =/X to M, regenerates NM/MD when the reference is available and reorders tags; use BAM if the exact CIGAR ops matter.'),
    dict(priority='P2', title='Unverifiable table rows presented as fact', observed_in=[5],
         problem='DRAGEN "--mapq-max (default 60)", Cell Ranger/STARsolo "inherits STAR / 255" and CB/UB, featureCounts/RSEM as consumers of NH/HI, and the pbmm2 row are stated without any marker, although the fix log says none could be run.',
         root_cause='Rows were kept from the upstream text; the fixer deleted only the claims it could disprove.',
         fix='Append "(not verified here)" to those rows, or cite the vendor documentation for each, or drop the DRAGEN flag name.'),
    dict(priority='P2', title='Residual robustness gaps in the shipped examples', observed_in=[7],
         problem='view_bam.py with a non-numeric limit dies with a raw ValueError traceback (the int() sits outside the try); on an unindexed CRAM pysam prints several [E::cram_index_load] lines on stderr although the run succeeds; convert_formats.sh leaves a header-only output file behind when samtools fails after opening it (rc 1, file present).',
         root_cause='Argument parsing and cleanup were not covered by the rewrite.',
         fix='Move int(sys.argv[2]) into the try and print a usage error; delete OUTPUT in an EXIT trap when the run fails; mention that the cram_index_load lines are harmless.'),
    dict(priority='P2', title='Small text inaccuracies and gaps', observed_in=[1, 5, 6, 8],
         problem='Mode table says pysam "wc" needs reference_filename= but it writes an embedded-reference CRAM with warnings when omitted; the @PG example uses IDs bwa-mem and samtools.1 where real files have bwa and samtools; the multi-region section does not say -M needs an index; the "mapping quality distribution" command prints distinct values, not counts.',
         root_cause='Illustrative examples were not aligned with tool output.',
         fix='Reword the wc row ("should be given"), use real @PG IDs, add "(needs an index)" to the -M line, and add `| uniq -c` to the MAPQ command.'),
]

strengths = [
    'Every quantitative claim I could run held: 302 of 303 asserted checks pass across eight inputs, including a 32-record hand-written SAM with planted truth, 140 random multi-region sets against a full-scan truth and every CRAM reference state.',
    'The multi-region section is correct and complete: -M, -M -L, --region-file and the pysam fetch_regions helper all equal the full-scan truth, including adjacent, nested and gap-spanning cases the default query duplicates.',
    'The CRAM section is now trustworthy: the recommended full-decode check fails exactly when the reference cannot be resolved, and the text says which commands (view -c, flagstat, idxstats, quickcheck) cannot prove it.',
    'view_bam.py and convert_formats.sh no longer fail on the inputs the Skill advertises (unindexed, empty, unmapped-only, CRAM, uppercase extensions) and refuse to overwrite their input.',
    'usage-guide dedup lost nothing: 33 of 33 old facts and all 12 advertised prompts are still served from one copy.',
]

report = {
    'meta': {
        'skill_name': 'bio-sam-bam-basics',
        'description': 'View, convert, and understand SAM/BAM/CRAM alignment files using samtools and pysam. Use when inspecting alignments, converting between formats, or understanding alignment file structure.',
        'evaluated_on': '2026-09-20',
        'evaluator_version': 'skill-auditor@1.0',
        'category': 'Data Analysis',
        'execution_mode': 'D',
        'complexity': 'Moderate',
        'n_inputs': 8,
        'source': 'mrsonord2240/bioSkills@35712f5f1c1177aec6e6f1fab165b8c49a832aab:alignment-files/sam-bam-basics',
        'audit_type': 're-audit of a fixed Skill (branch fix/af-sambam); pre-fix report 77, Beta Only, not deployable (archived at audits/_pre-fix-20260920/bio-sam-bam-basics)',
        'tools': 'samtools 1.24, htslib 1.24, pysam 0.24.1, bcftools 1.24, bwa 0.7.19, bwa-mem2, minimap2 2.31, bowtie2 2.5.5, hisat2 2.2.3, STAR 2.7.11b, fgbio 4.1.1, mapDamage 2.2.2 (WSL science, env alignment-files + side envs); Rsamtools 2.22.0 (Windows R via r.sh)',
        'checks_executed': f'{TOTAL_CHK} asserted checks ran, {TOTAL_PASS} passed; the single failing check is the CRAM round-trip sentence (inputs 7 and 8)',
        'floors_check': f'Static {static_total} >= 80; execution avg {execution_avg} >= 85; Layer1 avg {l1:.1f} >= 32; Layer2 avg {l2:.1f} >= 48; assertion pass rate {ap}/{at} = {100 * ap / at:.1f}% >= 90 -> no downgrade',
        'complexity_note': 'Moderate: 4 files (SKILL.md, usage-guide.md, 2 examples), 3-5 task types; the rule gives 5 inputs. Run as 8: the 5 pre-fix inputs as regression tests plus 3 new inputs (multi-region vs full-scan truth; hand-written planted-truth SAM with view_bam.py matrix; CRAM reference states on a second real dataset).',
        'pre_fix': {'score': 77, 'grade': 'Beta Only', 'static': 72, 'execution_avg': 80.4, 'assertion_pass': '19/25', 'deployable': False},
    },
    'veto_gates': {
        'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
        'research_veto': {
            'applicable': True, 'gate': 'PASS',
            'scientific_integrity': {'result': 'PASS', 'detail': 'No fabricated identifiers, statistics or results. Unverified rows (DRAGEN, Cell Ranger/STARsolo, featureCounts/RSEM) are unmarked but are tool-behaviour statements, recorded as a P2, not fabrications.'},
            'practice_boundaries': {'result': 'PASS', 'detail': 'File-format tooling only; no diagnostic or prescriptive content.'},
            'methodological_ground': {'result': 'PASS', 'detail': 'No principled methodological fallacy; the CRAM round-trip sentence is a correctness imprecision (P2).'},
            'code_usability': {'result': 'PASS', 'detail': 'Both shipped examples and every SKILL.md/usage-guide snippet, including fetch_regions() and the HPC cache recipe extracted verbatim, ran from a copy on samtools 1.24 / pysam 0.24.1 with asserted output.'},
        },
    },
    'static_score': {'subtotal': static_total, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
    'dynamic_score': {
        'execution_avg': execution_avg, 'max': 100, 'assertion_pass_rate': {'passed': ap, 'total': at},
        'inputs': [{k: i[k] for k in ('index', 'type', 'label', 'status', 'status_flag', 'note', 'basic', 'specialized', 'total', 'assertions_passed', 'assertions_total', 'assertions', 'executed', 'execution_note', 'checks')} for i in inputs],
    },
    'final': {'static_weighted': static_w, 'dynamic_weighted': dyn_w, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': symbol, 'deployable': True, 'veto_override': False},
    'key_strengths': strengths,
    'recommendations': recs,
}
assert sum(c['score'] for c in report['static_score']['categories'].values()) == static_total
json.dump(report, open(OUT + '/eval_report_bio-sam-bam-basics_result.json', 'w', encoding='utf-8'), indent=2, ensure_ascii=False)

# ---------------- viewer ----------------
L = []
w = L.append
w('# Eval Viewer — bio-sam-bam-basics (RE-AUDIT of the fixed Skill)')
w('Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@35712f5f1c1177aec6e6f1fab165b8c49a832aab:alignment-files/sam-bam-basics` (worktree `wt/af-sambam`, read-only; the Skill was copied to `run/skill/` and run from there, md5 identical to the worktree)')
w('')
w(f'**Pre-fix 77 (Beta Only, not deployable) -> {score} ({grade}), deployable, no veto, no open P0/P1.** Static 72 -> {static_total}; execution average 80.4 -> {execution_avg}; assertion pass 19/25 (76%) -> {ap}/{at} ({100 * ap / at:.1f}%); {TOTAL_CHK} asserted checks ran, {TOTAL_PASS} passed, 1 failed (a Skill statement, see below).')
w('')
w('## Summary table')
w('')
w('| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Checks | Status |')
w('|---|---|---|---|---|---|---|---|---|')
for i in inputs:
    w(f"| {i['index']} | {i['type']} | yes | {i['basic']} | {i['specialized']} | {i['total']} | {i['assertions_passed']}/{i['assertions_total']} PASS | {i['checks']['passed']}/{i['checks']['total']} | {i['status_flag']} |")
w('')
w(f'**Execution Average: {execution_avg} / 100** (Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60) | **Assertion Pass Rate: {ap}/{at}** | Static {static_total}/100 | Final = {static_w} + {dyn_w} = **{score}** {symbol} {grade}')
w('')
w('Inputs 1-5 are the pre-fix inputs re-run as REGRESSION tests (scripts under `run/regress/`, pointed at the fixed copy; assertions that used to encode a defect were rewritten to assert the fixed behaviour). Inputs 6-8 are NEW (`run/new/`).')
w('')
w('## Regression: the five assertions that failed before')
w('')
w('| Pre-fix FAIL (input) | Now |')
w('|---|---|')
w('| 1: no safe degrade on unindexed BAM / wrong contig / multi-region duplicates | PASS: view_bam.py 5642/2 on an unindexed copy; multi-region section with -M, -M -L, --region-file, fetch_regions (Input 6: 140/140 sets equal truth) |')
w('| 2: helper ignores reference for CRAM input, rejects .BAM, destroys its input | PASS: CRAM->BAM/SAM with 3rd arg identical to original; h5.BAM works; same path, ./path and symlink all rc 1 with the input intact |')
w('| 3: view_bam.py crashes on empty unindexed BAM, prints None:-1 for unmapped | PASS: Mapped 0/Unmapped 0; rows `ctgA:49 + unmapped`, `* + unmapped` |')
w('| 4: "view -c proves reference reachable"; "different reference silently corrupts" | PASS: text says view -c cannot; `view -o /dev/null && echo ok` fails with the reference gone (rc 1, no ok) and prints ok when reachable; wrong reference = MD5 mismatch rc 1, silent only with ignore_md5=1 |')
w('| 5: four wrong failure-mode claims (markdup silent, MD needed, =/X, Bowtie2 42 rare) | PASS: markdup rc 1 + message; mpileup identical with/without MD/NM and on =/X vs M; mapDamage tables identical with MD/NM stripped; Bowtie2 42 = 97.4%, --local 44 = 94.7% |')
w('')
w('## Fix-log claims re-verified by my own runs')
w('')
w('| Fix-log item | My evidence |')
w('|---|---|')
w('| CRAM check `view -o /dev/null f.cram && echo ok` | Input 4 and 8: with the reference gone no "ok" and rc 1 ("Unable to fetch reference"); with -T, UR, REF_PATH (M5-named file), REF_CACHE, the Skill\'s own recipe run verbatim, or embed_ref=1: "ok" and md5 of columns 1-11 identical to the source. `view -c`, flagstat, idxstats, quickcheck pass with the reference gone (200 / 200+0 / 197 3 / rc 0); `samtools stats` and pysam iteration fail. Nuance (not a defect): a CRAM whose only records are unplaced unmapped reads decodes with no reference, so "ok" there proves decodability only. |')
w('| view_bam.py rewrite | Input 7 matrix: SAM, sorted BAM, unsorted BAM, unindexed BAM, unmapped-only BAM (indexed/not), empty SAM/BAM, CRAM with reference / reference gone / 3rd argument: Mapped/Unmapped equals `view -c -F 4` / `-f 4` every time; missing file, text file and truncated BAM exit 1 with readable errors. Leftover: non-numeric limit traceback, cram_index_load noise on unindexed CRAM. |')
w('| convert_formats.sh | Inputs 2, 7: SAM/BAM/CRAM legs correct; CRAM input takes the reference; .BAM ok; input==output guard (path, ./path, symlink) works. Leftover: header-only partial output when samtools fails after opening it (checked in `run/debug/d3.sh`). |')
w('| multi-region recipes | Input 6: counts vs full-scan truth for overlapping, adjacent, nested, gap-9bp/100bp, identical, chained, reversed, single-base and far-apart sets, plus 60 + 80 random sets: -M, -M -L, --region-file, fetch_regions all equal truth; default `view r1 r2` = sum of per-region counts (duplicates). BED 0-based half-open confirmed for -L and --region-file. |')
w('| corrected failure-mode table | Input 5: markdup (rc 1, message), MD not needed (mpileup md5 identical; mapDamage 2.2.2 tables identical), =/X identical pileup, Bowtie2 42/44 shares, wrong CRAM reference (MD5 mismatch). |')
w('| removed claims | dedup_check: "production pipelines reject", Picard/bcftools-need-M, featureCounts-without-NH, consensus-tools-without-MD, "silently corrupts", "MD required by mpileup BAQ", "view -c proves", "Bowtie2 42 rare" all absent (9/9). |')
w('| usage-guide dedup | dedup_check: 33/33 facts, 12/12 prompts, pointers resolve. Nothing the agent needs was lost. |')
w('')
w('## Honesty of the unrunnable rows')
w('')
w('DRAGEN (`--mapq-max`, default 60), Cell Ranger/STARsolo (MAPQ 255, CB:Z/UB:Z), featureCounts/RSEM as NH/HI consumers, and pbmm2 could not be run here. The fixed SKILL.md states them exactly as before with **no marker**; the honesty is only in the fix log ("Unfixed"). Recorded as P2 (label or cite). Adjacent rows I could run held: STAR MAPQ set and HI base, minimap2 ms/cs, bwa MC, fgbio RX, HISAT2 MAPQ, mapDamage.')
w('')
w('## Findings the fix left or introduced (all P2)')
w('')
for r in recs:
    w(f"- **[{r['priority']}] {r['title']}** (inputs {r['observed_in']}): {r['problem']} Fix: {r['fix']}")
w('')
w('## Static score (25 criteria)')
w('')
w('| Category | Score | Note |')
w('|---|---|---|')
for k, v in cats.items():
    w(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
w(f'| **Subtotal** | **{static_total}/100** | pre-fix 72 |')
w('')
w('Skill Veto: T1 stability PASS (302/303 checks, no crash), T2 contract PASS (name + description; helpers print labelled output), T3 determinism PASS (seeded data; the final suite ran twice with identical pass counts, 302/303), T4 security PASS (no eval, variables quoted, input==output guard). Research Veto (Data Analysis): M1-M4 PASS.')
w('')
w('## Detailed outputs')
for i in inputs:
    w('')
    w(f"### Input {i['index']} — {i['type']}: {i['label']}")
    w(f"**Executed:** yes. {i['execution_note']}")
    w(f"**Scores:** Basic {i['basic']}/40 | Specialized {i['specialized']}/60 | Total {i['total']}/100 | checks {i['checks']['passed']}/{i['checks']['total']}")
    w(f"**Note:** {i['note']}")
    w('**Assertions:**')
    for a in i['assertions']:
        w(f"- [{a['result']}] {a['text']} — {a['note']}")
    w('')
    w(f"<details><summary>Asserted checks that ran for input {i['index']} (from run/out/results.jsonl; {i['checks']['total']} checks + notes)</summary>")
    w('')
    for r in by[str(i['index'])]:
        tag = 'NOTE' if r['pass'] is None else ('PASS' if r['pass'] else 'FAIL')
        d = str(r['detail']).replace('\n', ' ').replace('|', '/')[:140]
        w(f"- [{tag}] {r['name'][:230]} :: {d}")
    w('')
    w('</details>')
w('')
w('## What was run (all in `run/`)')
w('')
w('- `run_all.sh` (WSL: regression + new inputs) and `run_rsamtools.sh` (Windows R via `r.sh`); `build_report.py` writes this file and the JSON from `out/results.jsonl`.')
w('- `regress/`: pre-fix scripts re-pointed at `run/skill` (`in1`, `in1b`, `in1_rsamtools.R`, `in2`, `in2_diff.sh`, `in3`, `in4`, `in4b`, `in5`, `in5.sh`, `make_reads.py`, `make_synth.py`, `00_probe.sh`, `chk.py`), with assertions rewritten where they had encoded a defect.')
w('- `new/`: `in6.py` (multi-region), `in7.py` (hand-written SAM + view_bam matrix + helper), `in8.py` (CRAM reference states), `dedup_check.py`, `misc_claims.py`, `tags_check.py`, `in5c_mapdamage.sh`. `debug/`: three diagnostic scripts that explained the CRAM round-trip diffs and the helper\'s leftover output.')
w('- `out/`: raw outputs; `data/`: only the small synthetic inputs (bulky BAM/CRAM intermediates deleted, rebuilt by `run_all.sh`).')
w('- Deviations from the pre-fix scripts worth knowing: the F: drive is case-insensitive, so `h.bam -> h.BAM` hit the helper\'s own input==output guard (correct); the test writes `h5.BAM` instead. An early in7 expectation ("unmapped-only CRAM needs no reference") was wrong (placed unmapped reads do need it) and was corrected before scoring; the 1-base-different reference must sit inside a covered position for the ignore_md5 test to show a difference.')
open(OUT + '/eval_viewer_bio-sam-bam-basics.md', 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')
print('score', score, grade, 'exec_avg', execution_avg, 'static', static_total, 'assertions', ap, at, 'L1', l1, 'L2', l2)

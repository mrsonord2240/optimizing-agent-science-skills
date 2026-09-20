#!/usr/bin/env python3
"""Assemble eval_report_bio-alignment-filtering_result.json and eval_viewer_bio-alignment-filtering.md from the scores decided in the audit
and the raw outputs saved in run/out/*.txt (nothing is typed into the viewer that is not in those files, except the scoring prose).
Run from Windows Python:  PYTHONIOENCODING=utf-8 python run/build_report.py"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, 'out')
def out(name): return open(os.path.join(OUT, name), encoding='utf-8', errors='replace').read()
def grep(name, pat, maxn=40, width=230):
    rows = [l.rstrip() for l in out(name).splitlines() if re.search(pat, l)]
    return '\n'.join(l[:width] for l in rows[:maxn])
def head(name, n=40, width=230):
    return '\n'.join(l.rstrip()[:width] for l in out(name).splitlines()[:n])
def npass(name): return len(re.findall(r'^PASS', out(name), re.M)), len(re.findall(r'^FAIL', out(name), re.M))

COMMIT = 'fdf2e0a288f37dd697b40adf06cfcdc6341cc654'
SOURCE = f'mrsonord2240/bioSkills@{COMMIT}:alignment-files/alignment-filtering'

A = lambda t, r, n: {'text': t, 'result': r, 'note': n}
inputs = [
 dict(index=1, type='Canonical', label='[regression] Standard quality filter + Remove-Duplicates pre-check on real 1000G, nf-core and planted-duplicate BAMs',
      prompt='"Filter my BAM file to keep only high-quality reads, and remove the duplicates." (real 1000G HG00349 BAM, 9601 records / 101 dup-flagged; real nf-core human PE BAM, 5644 records; planted-duplicate BAM with 100 UNMARKED duplicate reads)',
      status='COMPLETED', flag='✅', basic=37, spec=57,
      note='Standard filter (-F 3332 -q 30) equals a hand count on both real BAMs (9437 and 5640); pysam passes_filter identical record for record; the new duplicate pre-check marks 100 reads on the unmarked BAM and leaves 400.',
      assertions=[
        A('The SKILL.md Standard Quality Filter block (-F 3332 -q 30) equals a hand count from raw FLAG/MAPQ integers on two real BAMs', 'PASS', '9437/9601 and 5640/5644 records; output is BGZF; quickcheck OK'),
        A('The pysam passes_filter block is record-for-record identical to the CLI result', 'PASS', 'to_string() lists equal on both BAMs'),
        A('The extracted Remove-Duplicates snippet marks first when no duplicate flag exists and then removes them', 'PASS', 'planted BAM: "marking first", 100 flagged (one template of each of the 50 planted pairs), 400 left, 0 dup-flagged; 1000G (already marked): straight -F 1024, 9500'),
        A('The text is right that plain -F 1024 on an unmarked BAM keeps everything', 'PASS', '500 of 500 reproduced'),
        A('usage-guide.md no longer contradicts SKILL.md about the "standard" filter', 'PASS', 'no -F 2308 or -F 3332 left in usage-guide.md')],
      out_files=['r1_standard.txt']),
 dict(index=2, type='Variant A', label='[regression] Every flag/MAPQ recipe, exhaustive over all 4096 FLAG values (synthetic BAM) and the flag tables',
      prompt='"Give me the samtools flags for: mapped only, primary only, read1 only, forward strand only, germline/somatic/ChIP/ATAC/RNA/SV prep." (SYNTHETIC BAM, one read per FLAG 0..4095)',
      status='COMPLETED', flag='✅', basic=37, spec=57,
      note='14 recipes harvested by regex from the fixed SKILL.md bash blocks and 9 assay-table recipes: all equal bit arithmetic over 4096 flags; relabelled forward/reverse/read1/read2 rows clean; all 7 breakdown lines equal `samtools flags`.',
      assertions=[
        A('Every -f/-F/-G/-q recipe in the bash blocks equals bit arithmetic over all 4096 flag values', 'PASS', '14 recipes, all equal'),
        A('Every assay-table recipe equals bit arithmetic', 'PASS', '9 recipes (germline, somatic, long-read, ChIP, ATAC, coverage, HISAT2, STAR, SV)'),
        A('The relabelled rows return what their labels say (forward -F 20, reverse -f 16 -F 4, read1/read2 -f 64/128 -F 2308)', 'PASS', '0 unmapped in strand outputs; 0 secondary/supplementary/unmapped in read outputs'),
        A('The somatic row keeps the supplementary reads its rationale keeps, while -F 2304/2308/3328/3332 remove them all', 'PASS', '503 supplementary kept by -F 1280 -q 1; 0 left by the other four'),
        A('The FLAG table, `samtools flags 99` line and the 7 "N = a + b" breakdowns match samtools', 'PASS', '12 table rows, 7 breakdowns (bits and prose term counts)')],
      out_files=['r2_flags.txt']),
 dict(index=3, type='Edge', label='[regression] Region, -L BED, pysam region/BED recipes and the shipped examples/filter_bam.py (three real BAMs, fuzzed)',
      prompt='"Extract reads from chr22:1,952-2,100, from my BED targets (with a track line), and run the shipped filter script on my name-sorted / unindexed / colon-contig BAMs." (real nf-core PE, spliced RNA-seq and 1000G BAMs; 81 random BEDs, 180 random regions)',
      status='COMPLETED', flag='⚠️', basic=34, spec=51,
      note='The first-audit defects here (BED recipe duplicating and unsorting reads, filter_bam.py off-by-one and crashes) are fixed: recipe identical to samtools -L on 81 fuzz BEDs without zero-width rows; filter_bam.py equals samtools on every region form. Left: the recipe drops what samtools keeps for zero-width (start==end) rows (13/81 fuzz BEDs) and crashes on a space-delimited BED.',
      assertions=[
        A('samtools region semantics quoted in the text hold (1-based inclusive, absent contig warns with rc 0, index required, -L skips track/#/browser lines, -P needs region or -L, CRAM needs -T)', 'PASS', '14 semantic checks pass'),
        A('The pysam rule fetch(c, start-1, end) equals samtools c:start-end, and the region snippet runs', 'PASS', '60 random regions identical'),
        A('The pysam BED recipe equals samtools -L in content and order on BEDs with track/#/browser/blank/nested/touching/CRLF/6-column/unsorted/unknown-contig rows and on 81 fuzz BEDs (3 real BAMs)', 'PASS', '0 mismatches without zero-width rows; output keeps SO:coordinate'),
        A('The text claim "same records as samtools view -L" holds for zero-width (start==end) and space-delimited BED rows', 'FAIL', '13/81 fuzz BEDs differ, every one containing a start==end row (samtools keeps the base at s, fetch(c,s,s) returns nothing); space-delimited BED raises IndexError'),
        A('examples/filter_bam.py equals samtools on bare contig / contig:start / open end / commas / colon contigs / 180 random regions on 3 BAMs, refuses bad regions cleanly, and handles unindexed and name-sorted input', 'PASS', 'no Traceback on 5 bad regions; -d warns on an unmarked BAM; -q 30 -d -p -P == samtools -f 2 -F 3332 -q 30')],
      out_files=['r3_regions.txt']),
 dict(index=4, type='Variant B', label='[regression] Reproducible, pair-consistent subsampling: samtools -s, coverage-matching guard, pysam blake2b recipe (real 1000G BAM)',
      prompt='"Subsample my BAM to 10% reproducibly, then to exactly ~3000 reads, and match tumor coverage to the normal." (real 1000G BAM 9601 records / 4828 templates; nf-core PE as normal)',
      status='COMPLETED', flag='✅', basic=37, spec=57,
      note='Every claim reproduces: -s 42.1 template-consistent and deterministic; bare -s 0.1 == seed 0 (1015); --subsample 0.1 auto seed 1001; guarded coverage matching lands within 8%; pysam recipe honours its seed (Jaccard 0.044-0.069).',
      assertions=[
        A('-s 42.1 keeps or drops every record of a template together, is ~10%, and is deterministic', 'PASS', '512 of 4828 templates, all records kept, identical rerun'),
        A('The corrected 1.24 seed statements hold (bare -s 0.1 deterministic and equal to seed 0; --subsample without a seed uses a header-derived seed and differs)', 'PASS', '1015 = 1015; auto 1001; NEWS.md 1.24 states the default-seed change (n11)'),
        A('Sequential cuts with independent seeds give 12.5%; same-seed cuts nest', 'PASS', '1197 of 9601; nested 2256 == direct 2256'),
        A('The extracted coverage-matching and tumor-normal block is safe when target > total and lands near the target otherwise', 'PASS', 'target 10M -> unchanged copy 9601; 3000/1000/6000 -> -5.0/-7.8/-0.6%; tumor 5604 vs normal 5640; target == total copies, total-1 keeps all'),
        A('The pysam blake2b recipe is pair-consistent, honours its seed, reproducible and unbiased', 'PASS', '6 seeds ~10%, all records of a template kept, pairwise Jaccard 0.044-0.069, mean fraction 0.0999, differs from samtools -s (Jaccard 0.062)')],
      out_files=['r4_subsample.txt']),
 dict(index=5, type='Stress', label='[regression] Aligner-aware MAPQ table on five aligners (synthetic repeat genome, known multiplicity) and the real STAR RNA-seq BAM',
      prompt='"Drop multi-mapped reads from BAMs made by BWA, Bowtie2, HISAT2, minimap2 and STAR." (SYNTHETIC 60 kb genome with exact and diverged repeats; REAL STAR BAM, 7042 primaries)',
      status='COMPLETED', flag='✅', basic=36, spec=56,
      note='All thresholds in the fixed table remove 400/400 exact-repeat reads and keep 96-100% of unique reads; every number quoted in the prose (399/400, 374/400, 80/400, 5768) reproduces.',
      assertions=[
        A('Every "drop ambiguous" and "high confidence" threshold read out of the table removes the 400 exact-repeat reads for BWA, Bowtie2, HISAT2, minimap2 and STAR', 'PASS', '0/400 survive in all ten cases'),
        A('The same thresholds keep the unique reads', 'PASS', '2000/2000 BWA and Bowtie2, 1995/2000 HISAT2 and STAR, minimap2 -q 60 1927/2000'),
        A('The numbers quoted in the prose reproduce (old -q 1 kept 399 Bowtie2, 374 HISAT2, 80 STAR)', 'PASS', 'exact match'),
        A('The STAR facts hold: MAPQ only 0/1/3/255 with NH 5+/3-4/2/1, -q 4..255 equivalent, -e [NH]==1 == -q 255 (synthetic and real 5768)', 'PASS', '(255,1) 5768, (3,2) 954, (1,3-4) 292, (0,5-6) 28 on the real BAM'),
        A('-e [NH]==1 removes 400/400 exact repeats on HISAT2 and returns 0 silently (rc 0) on BWA, Bowtie2 and minimap2 as the text says; Bowtie2 max MAPQ is 42', 'PASS', 'n=0 rc=0 stderr empty for the three NH-less aligners')],
      out_files=['r5_align.txt', 'r5_mapq.txt']),
 dict(index=6, type='Scope Boundary', label='[regression] Expression (-e) and read-group filtering, version-introduction claims, composite insert-size request (real BAMs)',
      prompt='"Keep proper pairs with insert 100-500, <=20% soft clip, NM<=3, and only read group X; and tell me which samtools release each option needs." (real nf-core PE, 1000G with two RG IDs, STAR RNA-seq; synthetic 9-read RG BAM)',
      status='COMPLETED', flag='⚠️', basic=35, spec=51,
      note='-e recipes, -r/-R/-l and the new -n all behave as written; the fix added a wrong release number (-n arrived in samtools 1.23, not 1.24) and the composite insert-size request still exposes the signed-tlen trap the text never mentions.',
      assertions=[
        A('The -e recipes equal tag/CIGAR truth (NM, cigar=~, sclen, combined with -F/-q, sclen/qlen, ![NM]) and an -e on an absent tag is silently empty', 'PASS', '229, 16, 28, 4206, 5628, 2 records match truth; [XY] rc 0, 0 rows, no warning'),
        A('Read-group semantics match the text: -r takes the ID and also emits untagged reads, -e [RG]== is strict, -R file, -l LIBRARY, -n drops untagged, --expr accepted', 'PASS', '6 = 3 tagged + 3 untagged; -e 3; -n 3; -l 9601 of 9601; --expr == -e 5768'),
        A('Real STAR BAM: -e [NH]==1 equals -q 255', 'PASS', '5768 = 5768'),
        A('The version-introduction claims match the samtools NEWS (-e 1.12, sclen 1.16, --subsample seed 1.24, -n 1.24)', 'FAIL', 'NEWS.md puts --exclude-no-read-group under Release 1.23 (16 Dec 2025), not 1.24; the other three are right (n11)')],
      out_files=['r6_expr.txt', 'n11_news_check.txt']),
 dict(index=7, type='Adversarial', label='[regression] "Remove duplicates, keep unique high-confidence proper pairs, then run Manta" on an unmarked-duplicate BAM',
      prompt='"Clean my BAM: remove duplicates, keep only unique high-confidence properly-paired primary reads, and I will run Manta (SV caller) on it." (planted BAM with UNMARKED duplicates, coordinate-sorted, name-sorted and shuffled; SYNTHETIC all-flags BAM; real 1000G and STAR BAMs)',
      status='COMPLETED', flag='✅', basic=35, spec=51,
      note='The dedup trap is closed on all three sort orders and the supplementary/SV warning is correct; the text still says nothing about the discordant-pair signal that -f 2 destroys, or about orphaned mates (53 singletons after -F 3332 -q 30 on the 1000G BAM).',
      assertions=[
        A('The Remove-Duplicates snippet yields 400 records from the unmarked BAM whether it is coordinate-sorted, name-sorted or shuffled, with every remaining template still paired', 'PASS', '400/400/400; 200 templates of size 2'),
        A('The SV recipe -F 1024 keeps the supplementary reads that -F 2304/2308/3328/3332 remove, and the text warns about it', 'PASS', '1024 supplementary kept vs 0; "NOT -F 2304, 2308, 3328 or 3332" and "Cost of getting this wrong" present'),
        A('The text warns before the command that -F 1024 is a no-op on an unmarked BAM', 'PASS', '"silently removes nothing" within the Remove Duplicates section'),
        A('"Primary is not unique" holds on real data', 'PASS', 'real STAR BAM: -F 2304 keeps 7042 primaries of which 1274 have NH>1; -q 255 keeps 5768')],
      out_files=['r7_adversarial.txt']),
 dict(index=8, type='Variant B', label='[NEW] MAPQ table on REAL reads: 2821 DNA pairs and 3521 RNA-seq pairs re-aligned with BWA, Bowtie2 (e2e and local), HISAT2, minimap2, STAR',
      prompt='"I aligned real reads with Bowtie2/HISAT2/BWA/STAR; which -q do I use to drop the ambiguous ones and keep the good ones?" (real nf-core reads re-aligned to the real 40 kb chr22 slice; second method: bowtie2 -k 10, original STAR NH)',
      status='COMPLETED', flag='✅', basic=34, spec=52,
      note='The thresholds keep >= 99.9% of real mapped reads for BWA, Bowtie2, HISAT2 and STAR. The slice has no distinct-locus multi-mappers (bowtie2 -k 10 finds none; STAR NH>1 is alternative splicing at one locus), so "drop ambiguous" is not exercised on real data here. minimap2 -ax sr real reads: -q 60 keeps only 58.5%.',
      assertions=[
        A('Table thresholds keep >= 97% of real mapped reads for BWA (-q 1/-q 30), Bowtie2 (-q 2/-q 23), HISAT2 (-q 2/-q 60), STAR (-q 255) on 2821 real DNA pairs', 'PASS', '100% / 99.9% / 100% / 99.9%'),
        A('The Bowtie2 "MAPQ maxes at 42 end-to-end" statement holds on real reads', 'PASS', 'e2e max 42; --local max 44 (text restricts the statement to end-to-end)'),
        A('-q 255 and -e [NH]==1 select the same real STAR records; the re-aligned RNA reads keep STAR MAPQ 255 for all NH==1 records', 'PASS', '5768 in the original BAM; STAR re-alignment: unique kept 5768/5768'),
        A('The 3521 real RNA pairs re-aligned with each aligner keep the reads STAR calls unique (NH==1) under the table thresholds', 'PASS', 'BWA 5768/5768, HISAT2 2207/2207, minimap2 5711/5711, STAR 5768/5768; Bowtie2 -q 2 5084/5432 (93.6%, unspliced aligner on spliced reads)')],
      out_files=['n8_align_real.txt', 'n8_align_rna.txt', 'n8_analyze.txt']),
 dict(index=9, type='Scope Boundary', label='[NEW] The two rows the fixer left unverified: pbmm2/minimap2 long-read MAPQ rows and the assay-table caller rationale (real GATK runs)',
      prompt='"Filter my PacBio HiFi and ONT BAMs for variant calling; and I will call germline with HaplotypeCaller and somatic with Mutect2: does the assay table\'s advice hold?" (SYNTHETIC 300 kb long-read repeat genome, pbmm2 26.2.99 + minimap2; REAL ARTIC nanopore BAM; REAL nf-core BAM with MAPQ set to 10 on 100 reads and 0 on 20, run through GATK 4.6.2.0 Mutect2 and HaplotypeCaller)',
      status='COMPLETED', flag='⚠️', basic=34, spec=50,
      note='pbmm2 and minimap2 long-read rows are right (0/80 exact repeats, 300/300 unique kept; pbmm2 CCS MAPQ identical to minimap2 map-hifi for 580/580 reads). The somatic row rationale ("somatic callers handle low MAPQ") is contradicted by a real Mutect2 run: it filters the 120 MAPQ<20 reads itself. Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA are not installed: unverified.',
      assertions=[
        A('pbmm2 row (-q 1 drop ambiguous, -q 60 high confidence) removes the exact-repeat reads and keeps the unique ones for HiFi (CCS) and ONT (SUBREAD) profiles', 'PASS', '0/80 exact repeats, 300/300 unique at both thresholds; the SKILL.md text still says the row was not run, which is now checkable'),
        A('The minimap2 long-read row (map-hifi, map-ont) behaves the same', 'PASS', '0/80 and 300/300; 8%-diverged copies keep MAPQ 60'),
        A('The long-read recipe -F 3328 -q 5 and the SV recipe -F 1024 equal bit arithmetic on the real 4916-record ARTIC nanopore BAM', 'PASS', '4916 = 4916; the real BAM has no supplementary reads, so the SV claim is exercised on the synthetic flag BAM only'),
        A('The germline row (-f 2 -F 3328 -q 20) is consistent with what HaplotypeCaller filters itself', 'PASS', 'real HaplotypeCaller run: MappingQualityReadFilter 120, NotSecondary 2 of 5642; --help lists MAPQ>=20, not-duplicate, not-secondary defaults'),
        A('The somatic row rationale "somatic callers handle low MAPQ" is supported for Mutect2', 'FAIL', 'real Mutect2 run filtered 120 of 5642 reads by MappingQualityReadFilter (MAPQ<20, default 20); Mutect2 also drops chimeric-original alignments by default')],
      out_files=['n9_align_long.txt', 'n9_analyze.txt', 'n10_caller_docs.txt', 'n10_caller_assert.txt', 'n10_mutect2_run.txt']),
]
for d in inputs:
    d['total'] = d['basic'] + d['spec']
    d['passed'] = sum(1 for a in d['assertions'] if a['result'] == 'PASS')
    assert 3 <= len(d['assertions']) <= 5, d['index']
    d['executed'] = True

cats = {
 'functional_suitability': (10, 12, 'Completeness 3: covers flags, MAPQ per aligner, regions, BED, assay recipes, subsampling, -e, read groups, pysam and output; gaps the fixer noticed and left (orphaned mates, signed tlen, discordant pairs). Correctness 3: every recipe runs and matches truth, but a wrong release number (-n), a contradicted caller rationale and an over-claimed BED equivalence remain. Appropriateness 4.'),
 'reliability': (9, 12, 'Fault tolerance 3: filter_bam.py validates regions, index and sort order and the snippets guard target>total and unmarked duplicates; the pysam BED recipe still crashes on space-delimited BED and mishandles zero-width rows. Error reporting 3: clean messages from the script, samtools stays silent (rc 0) on an absent contig but the text says so. Recoverability 3: every command writes a new file, none touches the input.'),
 'performance_context': (7, 8, 'SKILL.md 426 lines / ~20 KB with tables carrying most content; usage-guide reduced to 64 lines with no duplicated recipes. Token cost 3, execution efficiency 4.'),
 'agent_usability': (14, 16, 'Learnability 4; consistency 3 (input.bam / in.bam / mapped.bam naming shifts between blocks); feedback design 3 (count-before-write advice, script prints Kept/Removed and warnings); error prevention 4 (each trap carries a checked number).'),
 'human_usability': (6, 8, 'Discoverability 3: the description does not mention subsampling, duplicate removal or read groups, all covered; forgiveness 3 (strict region parsing is correct for this category).'),
 'security': (11, 12, 'No credentials, no eval/exec, region strings validated; bash blocks use unquoted variable expansion of user paths (input validation 3).'),
 'maintainability': (10, 12, 'One SKILL.md, a slim usage-guide and one runnable example; no references/ directory; flag lists still appear in two forms (table and breakdown list). Modularity 3, modifiability 3, testability 4 (checked numbers in the text, runnable example script).'),
 'agent_specific': (17, 20, 'Trigger precision 3; progressive disclosure 3 (no references, but under 500 lines); composability 4 (Related Skills, explicit hand-offs to duplicate-handling, sorting, indexing); idempotency 4; escape hatches 3 (SV warning, "no universal threshold", pbmm2 caveat, but caller rows are not marked unverified).'),
}
static_sub = sum(v[0] for v in cats.values())
assert static_sub == 84, static_sub
exec_avg = round(sum(d['total'] for d in inputs) / len(inputs), 1)
sw = round(static_sub * 0.4, 1); dw = round(exec_avg * 0.6, 1); score = round(sw + dw)
tot_pass = sum(d['passed'] for d in inputs); tot_ass = sum(len(d['assertions']) for d in inputs)
print('static', static_sub, 'exec_avg', exec_avg, 'sw', sw, 'dw', dw, 'score', score, 'assertions', tot_pass, tot_ass, f'{tot_pass/tot_ass:.1%}')
l1 = sum(d['basic'] for d in inputs) / len(inputs); l2 = sum(d['spec'] for d in inputs) / len(inputs)
print('L1 avg', round(l1, 1), 'L2 avg', round(l2, 1))
assert score >= 85 and static_sub >= 80 and exec_avg >= 85 and l1 >= 32 and l2 >= 48 and tot_pass / tot_ass >= 0.9
grade, sym = 'Production Ready', '⭐'

recs = [
 dict(priority='P2', title='-n (--exclude-no-read-group) arrived in 1.23, not 1.24', observed_in=[6],
      problem='"Samtools 1.24 adds -n (--exclude-no-read-group)" is wrong: samtools NEWS.md lists the option under Release 1.23 (16 Dec 2025). The fix log recorded it as 1.24 without the release heading.',
      root_cause='Version claim taken from a NEWS entry without checking which release section it sits under.',
      fix='Write "Samtools 1.23 adds -n (--exclude-no-read-group)". The 1.24 --help spells the long option --exclude-no-read_group; the hyphenated form in the text also works on 1.24 (checked).'),
 dict(priority='P2', title='Somatic-row rationale contradicted by a real Mutect2 run', observed_in=[9],
      problem='"Somatic callers handle low MAPQ" is not what a real Mutect2 run does: 120 of 5642 reads (MAPQ 10 and 0) were removed by its MappingQualityReadFilter (default minimum 20), and by default it also drops chimeric-original alignments. The assay table does not say that no caller row was run.',
      root_cause='Caller behaviour written from memory; only aligner/flag behaviour was tested.',
      fix='Reword the somatic row: -F 1280 -q 1 is only a light pre-filter because Mutect2 applies MAPQ>=20, not-secondary, not-duplicate and non-chimeric filters itself. Add one line that the caller-specific rationale comes from caller documentation and was not run for Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA.'),
 dict(priority='P2', title='pysam BED recipe differs from -L on zero-width/space rows', observed_in=[3],
      problem='The text says the recipe gives "the same records as samtools view -L". 13 of 81 fuzz BEDs differ, each with a start==end row (samtools returns the reads covering base s; fetch(c, s, s) returns nothing), and a space-delimited BED raises IndexError at parts[2].',
      root_cause='The fix was validated on one zero-width row placed where no reads exist, and on tab-delimited BED only.',
      fix='Say "tab-delimited BED with start < end", or make the recipe match: parts = line.split(); end = max(int(parts[2]), int(parts[1]) + 1).'),
 dict(priority='P2', title='Three known filter pitfalls still missing from the text', observed_in=[6, 7],
      problem='(1) Read-level filters leave orphaned mates (53 single-record templates after -F 3332 -q 30 on the 1000G BAM); (2) -f 2 would also discard the discordant pairs an SV caller needs, but the SV rows only say "-F 1024 only"; (3) tlen is signed, so "-e tlen>=100 && tlen<=500" keeps 2109 of the 4225 intended records.',
      root_cause='The fix log lists them as "needs a new section, not a correction".',
      fix='Add a short "Pitfalls" section: samtools fixmate after read-level filtering when pairing matters; do not add -f 2 for SV callers; use abs(tlen)-style symmetric tests in -e.'),
 dict(priority='P2', title='minimap2 row silent about short-read MAPQ ceilings', observed_in=[8],
      problem='The minimap2 row says "(DNA, long-read)" and -q 60. With -ax sr on real Illumina reads -q 60 kept only 58.5% of uniquely mapped reads (unique MAPQ mostly 48-59); on synthetic reads 96%.',
      root_cause='The row was checked only for long reads.',
      fix='State that -q 60 is for long-read presets; for -x sr use -q 1 for "drop ambiguous" and a lower high-confidence value (measured MAPQ 48-59 for unique real reads).'),
]

# ------------------------------------------------------------------ JSON
report = {
 'meta': {
  'skill_name': 'bio-alignment-filtering',
  'description': 'Filter alignments by flags, mapping quality, and regions using samtools view and pysam. Use when extracting specific reads, removing low-quality alignments, or subsetting to target regions.',
  'evaluated_on': '2026-09-20', 'evaluator_version': 'skill-auditor@1.0', 'category': 'Data Analysis', 'execution_mode': 'D', 'complexity': 'Complex', 'n_inputs': 9,
  'source': SOURCE, 'audit_type': 're-audit (third agent, after fix/af-filter)', 'pre_fix_score': 75, 'pre_fix_grade': 'Beta Only',
  'executed': True,
  'execution_note': 'Executed 9/9 inputs in WSL science env alignment-files (samtools 1.24, pysam 0.24.1, bwa 0.7.19, bowtie2 2.5.5, hisat2 2.2.3, minimap2 2.31, STAR 2.7.11b, pbmm2 26.2.99, GATK 4.6.2.0). Seven pre-fix inputs re-run as regression from a COPY of the fixed skill, with every SKILL.md code block extracted and executed (24 blocks in a smoke run: 18 clean, 6 warned or failed only because of fixture names: chr1 on a chr22 BAM x3, no conda, expected warnings x2) plus 3 new evidence sets: real Illumina DNA and RNA reads re-aligned with six aligner modes (input 8), synthetic long reads through pbmm2/minimap2 and the real ARTIC nanopore BAM (input 9), real GATK Mutect2 and HaplotypeCaller runs on a BAM with planted low-MAPQ reads (input 9), and the samtools NEWS.md for version claims (inputs 6). Real data: nf-core human PE / RNA-seq / UMI BAMs, 1000G HG00349 slice, ARTIC nanopore BAM, planted-duplicate BAM. Synthetic (labelled): 4096-flag BAM, 60 kb repeat genome, 300 kb long-read repeat genome, 9-read RG BAM. Not executed: Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA (not installed; judged by reading). No __pycache__ in the external clone, the worktree or run/.'},
 'veto_gates': {
  'skill_veto': {'gate': 'PASS', 'stability': 'PASS', 'contract': 'PASS', 'determinism': 'PASS', 'security': 'PASS'},
  'research_veto': {'applicable': True, 'gate': 'PASS',
   'scientific_integrity': {'result': 'PASS', 'detail': 'Every number in the text that was tested (399/374/80 of 400, 5768, 1001 vs 1015, 8%, 802 duplicated records) reproduces; no fabricated identifiers or results. One release number (-n, 1.23 vs 1.24) and one caller rationale are wrong and are P2 findings, not fabrications.'},
   'practice_boundaries': {'result': 'PASS', 'detail': 'File-level BAM filtering only; no diagnosis, prescription or individual triage.'},
   'methodological_ground': {'result': 'PASS', 'detail': 'MAPQ thresholds are aligner-specific with checked semantics; SV, RNA and duplicate-marking dependencies are called out; no principled fallacy in the 9 inputs.'},
   'code_usability': {'result': 'PASS', 'detail': 'All 24 code blocks, the shipped filter_bam.py and every extracted recipe ran; the only failures were fixture-name artifacts (chr1 on a chr22 BAM) and one non-standard-input crash (space-delimited BED, P2).'}}},
 'static_score': {'subtotal': static_sub, 'max': 100, 'categories': {k: {'score': v[0], 'max': v[1], 'note': v[2]} for k, v in cats.items()}},
 'dynamic_score': {'execution_avg': exec_avg, 'max': 100, 'assertion_pass_rate': {'passed': tot_pass, 'total': tot_ass},
  'inputs': [{'index': d['index'], 'type': d['type'], 'label': d['label'], 'status': d['status'], 'status_flag': d['flag'], 'note': d['note'],
              'basic': d['basic'], 'specialized': d['spec'], 'total': d['total'], 'assertions_passed': d['passed'], 'assertions_total': len(d['assertions']),
              'assertions': d['assertions'], 'executed': True,
              'execution_note': 'Executed in WSL science (env alignment-files); outputs in run/out/' + ', '.join(d['out_files']) + '; assertions checked on content (counts, record identity, truth arithmetic), not exit codes.'} for d in inputs]},
 'final': {'static_weighted': sw, 'dynamic_weighted': dw, 'score': score, 'max': 100, 'grade': grade, 'grade_symbol': sym, 'deployable': True, 'veto_override': False},
 'key_strengths': [
  'Every first-audit P1 defect verified fixed by independent runs (13 numbered findings re-run, 11-13 partly): aligner table (Bowtie2/HISAT2 -q 2, STAR sentinels, NH), pysam BED recipe, filter_bam.py region handling, dead pysam seed, silent -F 1024, target>total subsampling, mislabelled flag rows, RG example.',
  'Every recipe carries a checked number: the fixed text quotes 399/374/80 of 400, 5768, 1001 vs 1015, 802 duplicated records, and each reproduces exactly on an independent run.',
  'The pysam BED recipe and the shipped filter_bam.py equal samtools record for record (81 fuzz BEDs and 180 random regions on three real BAMs), colon-named contigs and name-sorted input included.',
  'Traps are stated before the command: -F 1024 on unmarked duplicates, supplementary reads for SV callers, target above total in coverage matching, absent contig or tag returning zero reads with rc 0.',
  'usage-guide.md dedup lost nothing an agent needs: each deleted block maps to a SKILL.md section, and the contradicting -F 2308 "standard" filter is gone.'],
 'recommendations': recs,
}
with open(os.path.join(ROOT, 'eval_report_bio-alignment-filtering_result.json'), 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

# ------------------------------------------------------------------ viewer
def fence(t): return '```\n' + t.strip('\n') + '\n```\n'
V = []
V.append('# Eval Viewer — bio-alignment-filtering (RE-AUDIT of the fixed Skill)\n')
V.append(f'Generated: 2026-09-20 | Source: `{SOURCE}` | Pre-fix: 75, Beta Only (assertions 22/35) | **Now: {score}, {grade}**\n')
V.append('Auditor: third agent (different from the first auditor and from the fixer). Everything below was produced by runs in `run/`; the fix log was read, not trusted.\n')
V.append('## Summary Table\n')
V.append('| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |\n|---|---|---|---|---|---|---|')
for d in inputs:
    V.append(f"| {d['index']} | {d['type']} | {d['basic']} | {d['spec']} | {d['total']} | {d['passed']}/{len(d['assertions'])} PASS | {d['flag']} |")
V.append(f'\n**Execution Average: {exec_avg} / 100** | **Assertion Pass Rate: {tot_pass}/{tot_ass} ({tot_pass/tot_ass:.1%})** | Layer 1 avg {l1:.1f}/40, Layer 2 avg {l2:.1f}/60\n')
V.append(f'**Static {static_sub}/100 x 0.4 = {sw}; Dynamic {exec_avg} x 0.6 = {dw}; FINAL {score} — {sym} {grade}; deployable = true; no veto; no open P0/P1 (5 P2).**\n')
V.append('Floors (Production Ready): static >= 80 ok, execution >= 85 ok, L1 >= 32 ok, L2 >= 48 ok, assertions >= 90% ok. Executed 9/9 inputs.\n')
V.append('## Regression: what the first audit found, and what my own runs show now\n')
V.append('| # | First-audit finding (pri) | Result now | Evidence |\n|---|---|---|---|')
V.append('| 1 | Aligner table: `-q 1` "drops ambiguous" wrong for Bowtie2/HISAT2 (P1) | FIXED | r5: `-q 2` removes 400/400 exact-repeat reads on Bowtie2 and HISAT2; old `-q 1` kept 399 and 374 |')
V.append('| 2 | "Universal -q 1" block contradicts the STAR row (P1) | FIXED | block deleted; text says no universal threshold; `-e [NH]==1` == `-q 255` on STAR (2303 = 2303), real BAM 5768 = 5768 |')
V.append('| 3 | pysam BED recipe: duplicated, unsorted, `track` crash (P1) | FIXED, one over-claim left | r3: identical to `samtools -L` (content and order) on 81 fuzz BEDs without zero-width rows; zero-width rows differ (P2) |')
V.append('| 4 | filter_bam.py: off-by-one, crashes on bare contig / commas / colon contig / name-sorted (P1) | FIXED | r3: 9 edge regions + 180 random regions on 3 real BAMs identical to samtools; bad regions exit cleanly |')
V.append('| 5 | "-s 0.1 is non-reproducible" false (P1) | FIXED | r4: bare -s 0.1 byte-identical twice and == seed 0 (1015); auto seed 1001; NEWS 1.24 confirms default-seed change |')
V.append('| 6 | pysam subsample ignores its seed (P1) | FIXED | r4: 6 seeds, Jaccard 0.044-0.069, rerun identical |')
V.append('| 7 | Coverage matching keeps 8% when target > total (P1) | FIXED | r4: target 10M -> unchanged copy 9601; targets 3000/1000/6000 within 8% |')
V.append('| 8 | `-F 1024` silently a no-op on unmarked BAM (P1) | FIXED | r1/r7: snippet marks 100 and leaves 400 on coordinate-sorted, name-sorted and shuffled input |')
V.append('| 9 | SKILL.md `-F 3332` vs usage-guide `-F 2308` (P2) | FIXED | usage-guide has no competing filter |')
V.append('| 10 | Mislabelled rows (Count unique, forward, read1) (P2) | FIXED | r2 |')
V.append('| 11 | Somatic recipe drops the supplementary reads its rationale keeps (P2) | FLAG FIXED, RATIONALE STILL WRONG | r2 (503 supplementary kept); n10: Mutect2 filters MAPQ<20 itself (new P2) |')
V.append('| 12 | `-r library_A`, `-r` emits untagged reads (P2) | FIXED, new wrong release number | r6; NEWS: `-n` is 1.23 not 1.24 (new P2) |')
V.append('| 13 | Version claims unverified (P2) | PARTLY | n11: -e 1.12, sclen 1.16, seed 1.24 confirmed; `-n` wrong |')
V.append('\nNew defects introduced by the fix: none that broke anything. Two over-claims it added: "same records as samtools view -L" (false for zero-width rows) and "Samtools 1.24 adds -n" (1.23).\n')
V.append('## Test inputs (9 = 7 regression + 2 new)\n')
V.append('Complexity: Complex -> 9 inputs (precedent: bio-alignment-structural re-audit also ran 9). Category: Data Analysis. Mode: D (instructions, samtools CLI, one example script).\n')
for d in inputs:
    V.append(f"\n### Input {d['index']} — {d['type']}: {d['label']}\n")
    V.append(f"**Prompt:** {d['prompt']}\n")
    V.append(f"**Executed:** true (WSL science env alignment-files). **Scores:** Basic {d['basic']}/40 | Specialized {d['spec']}/60 | Total {d['total']}/100 {d['flag']}\n")
    V.append(f"**Result:** {d['note']}\n")
    V.append('**Assertions:**')
    for a in d['assertions']:
        V.append(f"- [{a['result']}] {a['text']} — {a['note']}")
    V.append('')
    V.append('**Key output (trimmed; full text in `run/out/`):**\n')
    i = d['index']
    if i == 1: V.append(fence(grep('r1_standard.txt', r'^(PASS|FAIL|=====|records|human PE)', 30)))
    if i == 2: V.append(fence(head('r2_flags.txt', 3) + '\n...\n' + grep('r2_flags.txt', r'somatic|relabel|forward|reverse|read1|read2|FAILS|breakdown|99', 12)))
    if i == 3: V.append(fence(grep('r3_regions.txt', r'^(FAIL|   MISMATCH|      BED|   fuzz|   zero|PASS BED recipe|PASS pysam|PASS filter_bam -r (fuzz|on real)|FAILS)', 22, 300)))
    if i == 4: V.append(fence(grep('r4_subsample.txt', r'^(PASS|FAIL|   trap|   edge|FAILS)', 26)))
    if i == 5: V.append(fence(grep('r5_mapq.txt', r'drop-ambiguous|old/naive|STAR MAPQ|STAR \(MAPQ|REAL STAR|Bowtie2 MAPQ|^FAILS|HISAT2 \(MAPQ', 30, 260)))
    if i == 6: V.append(fence(grep('r6_expr.py'.replace('.py', '.txt'), r'^(FAIL|PASS fixed|SYNTHETIC|long option|naive|PASS long|after composite|FAILS)', 16) + '\n' + grep('n11_news_check.txt', r'NEWS line|FAIL|installed', 8)))
    if i == 7: V.append(fence(grep('r7_adversarial.txt', r'^(PASS|FAIL|==|   real|   1000G|   text|   lines|FAILS)', 28, 260)))
    if i == 8: V.append(fence(grep('n8_analyze.txt', r'^(===|  (bwa|bowtie2|hisat2|minimap2|star|Bowtie2|STAR|bowtie2)|     (drop|high)|FAIL|PASS|FAILS)', 44, 250)))
    if i == 9: V.append(fence(grep('n9_analyze.txt', r'^(PASS|FAIL|pbmm2 CCS|reads per|   -q|-- |  records|  `-q|FAILS)', 30, 220) + '\n---- GATK (real runs, n10) ----\n' + grep('n10_mutect2_run.txt', r'set MAPQ|records MAPQ|=====|MappingQualityReadFilter|total reads', 10) + '\n' + grep('n10_caller_assert.txt', r'^(PASS|FAIL|SKILL.md somatic|Rows not)', 8, 300)))
V.append('\n## Independent checks beyond the inputs\n')
V.append('- **Snippet smoke** (`run/r0_snippets_smoke.py`, every fenced block of SKILL.md and usage-guide.md from a copy): ' + grep('r0_snippets_smoke.txt', r'blocks,', 1) + '\n' + fence(grep('r0_snippets_smoke.txt', r'^(WARN|FAIL)', 10, 200)) + 'The four WARN/FAIL blocks on `chr1` and `conda` are fixture artifacts (chr22 BAM; no conda in the env); the other two warnings are the snippets\' own intended messages.\n')
V.append('- **usage-guide.md dedup:** compared the archived pre-fix usage-guide with the fixed one. Every deleted block (FLAG table, `samtools flags 99/147`, `-f/-F` patterns, region/subsample/output commands, three pysam variants, MAPQ error table, troubleshooting, tips) has a counterpart in SKILL.md, except the pysam class variant and `count_with_filter`, which are variants of `passes_filter` and `samtools view -c`. Nothing an agent needs was lost; the contradicting `-F 2308` "standard" and the false "-s 0.1 non-reproducible" advice were dropped correctly.')
V.append('- **Assay-table caller rationale** (fixer left it unverified): only GATK is installed. Real HaplotypeCaller and Mutect2 runs on a BAM with 100 MAPQ-10 and 20 MAPQ-0 reads: both filter all 120 through MappingQualityReadFilter (min 20). Germline row is consistent; the somatic rationale is contradicted. Strelka2, DeepVariant, clair3, Sniffles, cuteSV, Manta, GRIDSS, Delly, SvABA remain unverified.')
V.append('- **pbmm2 row** (fixer left it unrun): verified on synthetic 2 kb reads in HiFi and ONT error profiles: same MAPQ semantics as minimap2 (CCS vs map-hifi identical for 580/580 reads).')
V.append('- **Version claims:** `-e` 1.12, `sclen` 1.16 and the 1.24 default-seed change match samtools NEWS.md; `-n` does not (1.23).')
V.append('- **Determinism (T3):** all subsampling recipes are seeded; reruns identical (r4). **Security (T4):** no eval/exec; filter_bam.py validates the region string.\n')
V.append('## Static evaluation (25 criteria, 8 categories)\n')
V.append('| Category | Score | Note |\n|---|---|---|')
for k, v in cats.items():
    V.append(f'| {k} | {v[0]}/{v[1]} | {v[2]} |')
V.append(f'\n**Static subtotal: {static_sub}/100** (first audit 74).\n')
V.append('## Vetoes\n')
V.append('Skill Veto: PASS on all four (stability, contract, determinism, security). Research Veto (Data Analysis): PASS on M1-M4 (see JSON detail). No veto override.\n')
V.append('## Recommendations\n')
for r in recs:
    V.append(f"**[{r['priority']}] {r['title']}** (observed in inputs {r['observed_in']})\n- Problem: {r['problem']}\n- Root cause: {r['root_cause']}\n- Fix: {r['fix']}\n")
V.append('## Run record\n')
V.append('Scripts in `run/` (all executed): `00_setup.sh`, `make_synthetic_flags.py`, `make_repeat_genome.py`, `lib.py`, `W.sh`, `r0_snippets_smoke.py`, `r1_standard.py`, `r2_flags.py`, `r3_regions.py`, `r4_subsample.py`, `r5_align.sh`, `r5_mapq.py`, `r6_expr.py`, `r7_adversarial.py`, `n8_align_real.sh`, `n8_analyze.py`, `n9_make_longreads.py`, `n9_align_long.sh`, `n9_analyze.py`, `n10_caller_docs.sh`, `n10_caller_assert.py`, `n10_mutect2_run.sh`, `n11_news_check.py`, `build_report.py`. Raw outputs: `run/out/`. `run/skill/` is the copy of the fixed Skill everything ran from. Large intermediate BAMs were deleted after the runs (scripts regenerate them). The pre-fix report is archived under `_pre-fix-20260920/`.\n')
with open(os.path.join(ROOT, 'eval_viewer_bio-alignment-filtering.md'), 'w', encoding='utf-8') as f:
    f.write('\n'.join(V))
print('written')

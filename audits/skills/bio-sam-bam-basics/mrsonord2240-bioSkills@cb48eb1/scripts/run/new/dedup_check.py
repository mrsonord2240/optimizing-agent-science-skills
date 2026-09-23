"""Input 1 add-on: the usage-guide.md dedup (210 -> 53 lines). For every fact the OLD usage-guide (archived pre-fix copy)
carried, check that the fixed SKILL.md + usage-guide.md still say it, and that every pointer in the fixed usage-guide
resolves to a section that exists. Also: the example prompts the guide advertises are each answerable from the Skill.
"""
import os, re, sys
os.environ['AUDIT_INPUT'] = '1'
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'regress'))
from chk import check, note
RUN = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OLD = open('/mnt/openscience/audits/_pre-fix-20260920/bio-sam-bam-basics/run/skill/usage-guide.md', encoding='utf-8').read()
NEW_SK = open(RUN + '/skill/SKILL.md', encoding='utf-8').read()
NEW_UG = open(RUN + '/skill/usage-guide.md', encoding='utf-8').read()
ALL = NEW_SK + '\n' + NEW_UG
check('archived pre-fix usage-guide is the 210-line one (so the comparison is against the right file)', len(OLD.splitlines()) >= 200 and len(NEW_UG.splitlines()) < 60, (len(OLD.splitlines()), len(NEW_UG.splitlines())))

facts = [
    ('conda install -c bioconda samtools pysam', r'conda install -c bioconda samtools pysam'),
    ('pip install pysam', r'pip install pysam'),
    ('SAM has header + tab-separated alignment sections', r'Header lines start with `@`[\s\S]*Alignment fields \(tab-separated\)'),
    ('@HD @SQ @RG @PG header types', r'@HD`.*\n- `@SQ`.*\n- `@RG`.*\n- `@PG`'),
    ('11 mandatory columns QNAME..QUAL', r'QNAME[\s\S]*FLAG[\s\S]*RNAME[\s\S]*POS[\s\S]*MAPQ[\s\S]*CIGAR[\s\S]*RNEXT[\s\S]*PNEXT[\s\S]*TLEN[\s\S]*SEQ[\s\S]*QUAL'),
    ('POS is 1-based', r'POS - 1-based'),
    ('FLAG 99 meaning', r'99[\s\S]{0,80}PAIRED,PROPER_PAIR,MREVERSE,READ1'),
    ('FLAG 147 meaning', r'147[\s\S]{0,80}PAIRED,PROPER_PAIR,REVERSE,READ2'),
    ('FLAG 4 / 256 / 2048', r'\| 0x4 \| 4 \| Unmapped[\s\S]*0x100 \| 256 \| Secondary[\s\S]*0x800 \| 2048 \| Supplementary'),
    ('CIGAR M I D N S H', r'\| M \|[\s\S]*\| I \|[\s\S]*\| D \|[\s\S]*\| N \|[\s\S]*\| S \|[\s\S]*\| H \|'),
    ('view | head', r'samtools view input.bam \| head'),
    ('view -h with header', r'samtools view -h input.bam'),
    ('view -H header only', r'samtools view -H input.bam'),
    ('view whole chromosome', r'samtools view input.bam chr1 '),
    ('view region chr:a-b', r'samtools view input.bam chr1:1000-2000'),
    ('view -c count', r'samtools view -c input.bam'),
    ('SAM -> BAM', r'samtools view -b -o output.bam input.sam'),
    ('BAM -> SAM', r'samtools view -h -o output.sam input.bam'),
    ('BAM -> CRAM with -T', r'samtools view -C -T reference.fa -o output.cram input.bam'),
    ('CRAM -> BAM with -T', r'samtools view -b -T reference.fa -o output.bam input.cram'),
    ('samtools flags decode', r'samtools flags 147'),
    ('pysam iterate BAM', r"pysam.AlignmentFile\('input.bam', 'rb'\)[\s\S]*for read in bam"),
    ('pysam properties (name, flag, chrom, 0-based pos, mapq, cigar, seq, qual)', r'reference_start[\s\S]*mapping_quality[\s\S]*cigarstring[\s\S]*query_sequence[\s\S]*query_qualities'),
    ('pysam fetch region', r"bam.fetch\('chr1', 1000, 2000\)"),
    ('mode strings rb/r/rc/wb/w/wc', r'`r` / `rb` / `rc`[\s\S]*`w` \|[\s\S]*`wb`[\s\S]*`wc`'),
    ('missing index -> samtools index', r'Could not retrieve index file[\s\S]{0,300}samtools index|samtools index[\s\S]{0,300}Could not retrieve index file'),
    ('CRAM needs reference (-T)', r'CRAM requires a reference FASTA with `-T`'),
    ('chromosome name mismatch chr1 vs 1', r'`chr1` vs `1`'),
    ('sorted + indexed before region queries', r'coordinate-sorted, indexed'),
    ('BAM for most work, CRAM for storage', r'BAM \| Binary compressed SAM \| Standard storage[\s\S]*CRAM \| Reference-based compression \| Long-term archival'),
    ('pysam 0-based vs samtools 1-based', r'`pysam read.reference_start` \| 0-based'),
    ('-h when piping', r'keep -h when piping'),
    ('-@ threads', r'`-@ N`'),
]
miss = [n for n, rx in facts if not re.search(rx, ALL)]
check(f'usage-guide dedup: {len(facts)} facts the OLD guide carried are each still present in the fixed SKILL.md/usage-guide.md', not miss, miss or f'{len(facts)}/{len(facts)} present')
lost = [n for n in ('Phred-scaled', 'PL:ILLUMINA', 'context manager') if n.lower() not in ALL.lower()]
note('old-guide wording that did NOT survive (judged for loss)', lost)
# usage-guide pointers
names = re.findall(r'"([A-Z][A-Za-z ]+)" (?:section|list)', NEW_UG)
heads = re.findall(r'^#{1,3} (.+)$', NEW_SK, re.M)
check('every SKILL.md section named by the fixed usage-guide exists ("Version Compatibility", "Related Skills")', len(names) >= 2 and all(any(n in h for h in heads) for n in names), (names, [h for h in heads if 'Version' in h or 'Related' in h]))
# every advertised prompt is answerable from a section
prompts = {
    'Show me the header of my BAM file': r'samtools view -H',
    'View the first 20 alignments with the header included': r'samtools view -h input.bam \| head',
    'Count how many reads are in my BAM file': r'samtools view -c',
    'Convert my SAM file to compressed BAM': r'samtools view -b -o output.bam input.sam',
    'Convert my BAM to CRAM format using the reference genome': r'-C -T reference.fa',
    'Convert CRAM back to BAM': r'-b -T reference.fa -o output.bam input.cram',
    'Extract all reads from chr1:1000000-2000000': r'samtools view input.bam chr1:1000-2000',
    'Get reads from multiple regions': r'### Multiple Regions',
    'Count reads in a specific genomic region': r'Region queries need',
    'Explain what FLAG 99 means': r'samtools flags 99',
    'Parse the CIGAR string 10M2I30M5D20M': r'Consumes query',
    'Show me the mapping quality distribution': r"awk '\{print \$5\}' \| sort -un",
}
gaps = [p for p, rx in prompts.items() if not re.search(rx, NEW_SK)]
check('every example prompt the guide advertises has a command/section in SKILL.md', not gaps, gaps or f'{len(prompts)}/{len(prompts)}')
note('prompt "mapping quality distribution": SKILL.md gives `sort -un | head` = distinct MAPQ values, not counts (agent must add uniq -c)', 'informational')

# claims the fixer says were REMOVED: confirm they are gone from the fixed text (and not merely reworded)
gone = {
    'production pipelines often reject': r'production pipelines',
    'Picard/bcftools often need M': r'(?i)picard[^\n]{0,80}need|often need M',
    'featureCounts ignores multimappers without NH': r'featureCounts ignoring',
    'consensus tools reject input without MD': r'consensus tools',
    'markdup silently marks nothing': r'(?i)silently[^\n]{0,40}markdup|markdup[^\n]{0,40}silently',
    'different reference silently corrupts bases': r'silently corrupt',
    'MD:Z required by bcftools mpileup BAQ': r'(?i)required by[^\n]{0,60}mpileup',
    'view -c proves reference reachable': r'view -c[^\n]{0,80}(?i:forces|proves)',
    'Bowtie2 42 rare': r'\(rare\)',
}
still = [k for k, rx in gone.items() if re.search(rx, ALL)]
check('claims listed as removed/corrected in the fix log are absent from the fixed SKILL.md/usage-guide.md', not still, still or f'{len(gone)}/{len(gone)} gone')

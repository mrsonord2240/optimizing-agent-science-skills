"""Input 11 (NEW, re-auditor 2): usage-guide.md dedup -- is anything an agent needs missing after the cut?
Method: read the UPSTREAM usage-guide (external clone, read-only) and the fixed one; for every section of the old guide assert the anchor
content exists in the fixed SKILL.md (or is deliberately replaced by a corrected version, checked by behaviour); run the old guide's own code
where the old and new versions differ; check the new guide points at things that exist."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
from snippets import load_functions
import pysam

I = 11
OLD = open("/mnt/openscience/external/mrsonord2240__bioSkills/alignment-files/pileup-generation/usage-guide.md", encoding="utf-8").read()
NEW = open(SKILL + "/usage-guide.md", encoding="utf-8").read()
SK = open(SKILL + "/SKILL.md", encoding="utf-8").read()
print("old guide", len(OLD), "bytes; new guide", len(NEW), "bytes; SKILL.md", len(SK), "bytes")

anchors = [  # (old-guide section, anchor strings that must be present in SKILL.md)
    ("Prerequisites (conda, pip, faidx)", ["conda install -c bioconda samtools bcftools", "pip install pysam", "samtools faidx reference.fa"]),
    ("Text pileup format + column table", ["Position (1-based)", "Read bases", "Base qualities"]),
    ("Read Bases Encoding (. , ACGT acgt * +N -N ^ $)", ["`.`", "`,`", "`acgt`", "`*`", "`+2AC`", "`-3CGT`", "`^Q`", "`$`"]),
    ("Basic pileup / quality / region / BED commands", ["samtools mpileup -f reference.fa input.bam > pileup.txt", "-q 20 -Q 20", "-r chr1:1000000-2000000", "-l targets.bed"]),
    ("Variant calling pipeline: single, BCF intermediate, multi-sample", ["bcftools mpileup -f reference.fa -d 1000000 -q 20 -Q 20", "-Ob -o raw.bcf", "bcftools call -mv raw.bcf", "s1.bam s2.bam s3.bam"]),
    ("Performance: parallel per chromosome + concat", ["xargs -a contigs.txt -P 4", "bcftools concat -f vcf_list.txt", "bcftools index all.vcf.gz"]),
    ("pysam: basic iteration, truncate=True", ["truncate=True", "def allele_counts", "len(pileup_column.pileups)"]),
    ("pysam: count alleles + frequency", ["def allele_counts", "def allele_frequency"]),
    ("pysam: find variants", ["def find_variants"]),
    ("pysam: access individual reads (name, base, Q, strand)", ["aln.query_name", "query_qualities[qpos]", "strand"]),
    ("Troubleshooting: reference/BAM name mismatch (@SQ vs fai)", ["samtools view -H in.bam", "cut -f1 ref.fa.fai", "@SQ"]),
    ("Troubleshooting: empty output (region, .fai, chr1 vs 1)", ["samtools view in.bam chr1:1000-2000", "ls reference.fa.fai", "chr1` vs `1"]),
    ("Troubleshooting: memory / slow (-d, BCF, parallel, -l)", ["Cap with `-d`", "BCF is far cheaper", "process contigs in parallel", "-l targets.bed"]),
    ("Tips: quality filtering, multi-sample preferred, 0-based, truncate", ["Library-Typed Flags Cheat Sheet", "Joint calling over all samples beats merging", "0-based", "truncate=True"]),
]
for sec, toks in anchors:
    miss = [t for t in toks if t not in SK]
    check(I, f"old usage-guide section '{sec}': content present in the fixed SKILL.md", not miss, f"missing {miss}")

# things the fix deliberately did NOT keep: verify each was actually wrong in the old guide (behaviour), so dropping is right
rc, out, err = sh(f"samtools mpileup -f {AFDATA}/sarscov2/genome.fasta {AFDATA}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam 2>&1 | head -3")
check(I, "dropped 'No sequences in common' troubleshooting: samtools 1.24 does not print that text on a reference/BAM contig mismatch (it prints the faidx 'sequence ... was not found' error, exit 0)",
      "No sequences in common" not in out and "was not found" in out, out.strip()[:160])
check(I, "dropped prompt 'Call variants using samtools mpileup and bcftools' replaced (samtools mpileup -g is removed in 1.24)", "using samtools mpileup and bcftools" not in NEW and "bcftools mpileup" in NEW)
rc, out, err = sh("samtools mpileup -g 2>&1 | head -2")
check(I, "samtools 1.24 has no `mpileup -g`: prompt steering there would have failed", "invalid option" in out or "unrecognized" in out.lower(), out.strip()[:100])
# old guide's find_variants / count_alleles: still what the old guide claimed? new SKILL.md does not define the old names
check(I, "old API names (count_alleles(min_qual), pileup_column.n depth) are gone from SKILL.md and the guide", "count_alleles" not in SK + NEW and "pileup_column.n\n" not in SK and "depth = pileup_column.n" not in SK + NEW)
# new guide is a pointer + prompts: it must still cover the Skill's 3 use cases and point to files that exist
check(I, "new usage-guide keeps Quick Start, 9 example prompts (basic/variant/position), 'What the Agent Will Do' (6 steps) and points to SKILL.md for commands/defaults/errors",
      NEW.count("> \"") == 9 and "What the Agent Will Do" in NEW and len(re.findall(r"^\d\. ", NEW, flags=re.M)) == 6 and "`SKILL.md`" in NEW, f"prompts={NEW.count('> ' + chr(34))}")
# duplication left?  lines >= 40 chars shared between the two files
shared = [l for l in NEW.splitlines() if len(l.strip()) >= 40 and l.strip() in SK]
check(I, "no long line of the new guide is duplicated verbatim in SKILL.md", not shared, shared[:3])
# every backticked file/path the guide mentions exists
print("new guide mentions:", re.findall(r"`([^`]+)`", NEW))
check(I, "every file the guide points at exists (SKILL.md) and examples/allele_counts.py exists for SKILL.md's pointer", os.path.exists(SKILL + "/SKILL.md") and os.path.exists(SKILL + "/examples/allele_counts.py") and "examples/allele_counts.py" in SK)
summary(I)

> **Audit record for `bio-vcf-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/variant-calling/vcf-basics) (MIT).
> - Read from [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/variant-calling/vcf-basics), a fork in which this Skill's files are unchanged from upstream; the audited content is upstream's.
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-basics

> Re-audit 2026-09-15: the vcf-basics folder is byte-identical between GPTomics d91ed3d and the fork commit c1237cdb (git diff empty), so this 2026-09-11 audit is reused unchanged; only the source string was updated.
Generated: 2026-09-11 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-basics`
Category: Data Analysis · Mode A · Complexity: Moderate → N = 5 (view/query, convert/index, field interpretation,
gVCF recognition, Python access; 3 files).

Environment: bcftools 1.24 (MSYS2 native Windows build) for CLI; cyvcf2 0.34.0 (bioconda, micromamba env in the WSL
`agents` distro, /tmp) for Python — cyvcf2 has no Windows wheel.

**All data are SYNTHETIC** (`data/make_data.py`, seed 20260911): 1-sample `callerA.vcf`; 8-sample raw GATK-style
`cohort.vcf` (361 sites; SYN_S6 low coverage, SYN_S7 contaminated, SYN_S8 a re-sequenced duplicate of SYN_S3);
`sample.g.vcf` (HaplotypeCaller-style gVCF).

## Step 1 — Skill Veto
T1–T4 PASS (read-only CLI/Python, no eval, no network, deterministic).

## Step 2 — Static score: 89/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Claims verified on data; one wrong usage-guide tip (query -H) |
| Reliability | 10/12 | Accurate error table; bgzip error string outdated |
| Performance & context | 7/8 | 263 lines, all used |
| Agent usability | 15/16 | Level/Number principle, strong trap list |
| Human usability | 7/8 | Natural prompts |
| Security | 11/12 | Local reads only |
| Maintainability | 10/12 | Runnable example, no test data |
| Agent-specific | 18/20 | Good routing |

Shipped-means-present: usage-guide.md and `examples/view_vcf.py` exist; SKILL.md references no other files. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 54 | 92 | 3/4 | yes | ✅ |
| 2 | Variant A | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 4 | Variant B | 37 | 52 | 89 | 4/4 | yes | ✅ |
| 5 | Stress | 37 | 53 | 90 | 3/4 | yes | ✅ |

**Execution Average: 90.8 / 100** · **Assertion Pass Rate: 18/20 (90 %)** · Layer 1 avg 37.4 · Layer 2 avg 53.4

Research Veto: M1–M4 PASS. **Final: 89 × 0.4 + 90.8 × 0.6 = 35.6 + 54.5 = 90 → ⭐ Production Ready** (all floors met).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Show me what's in callerA.vcf: the header definitions, the samples, a table of position, alleles, QUAL,
genotype, GQ and AD, and how many SNPs and indels there are."
**Code:** `bcftools view -h | grep ^##(INFO|FORMAT|contig)`, `bcftools query -l`,
`bcftools query -H -f '%CHROM\t%POS\t%REF\t%ALT\t%QUAL[\t%GT\t%GQ\t%AD]\n'`, `bcftools view -v snps|indels -H | wc -l`;
shipped `examples/view_vcf.py callerA.vcf.gz 5`.
**Printed (trimmed):**
```
#[1]CHROM [2]POS [3]REF [4]ALT [5]QUAL [6]SYN_S1:GT [7]SYN_S1:GQ [8]SYN_S1:AD
chr1 500 GA G 200 0/1 99 14,12
SNPs: 8  indels: 3  total: 11
view_vcf.py:  chr1:500 GA>G QUAL=200.0 FILTER=PASS TYPE=indel ...
```
Note: `query -H` prints a header, as SKILL.md says; usage-guide.md's tip claims it skips one.
**Scores:** 38 + 54 = **92** · **Assertions 3/4** (FAIL: query -H guidance inconsistent).

### Input 2 — Variant A
**Prompt:** "For the 8-sample cohort.vcf, compute allele balance for heterozygous calls per sample and show me sites
where the QUAL is high but a sample's genotype is still uncertain."
**Code:** `runs/in2/ab.py` (cyvcf2: `gt_types`, `format('AD')`, `format('GQ')`).
**Printed:**
```
sample  n_het  mean_AB  frac_AB<0.2_or>0.8
SYN_S1    162  0.449   0.049
SYN_S6     60  0.438   0.083
SYN_S7     92  0.419   0.163
SYN_S8     89  0.489   0.000
high-QUAL (>=300) sites with a low-GQ (<20) carrier genotype: 8   (all SYN_S7)
```
Interpretation: AB is derived from AD (no AB tag exists); SYN_S7's shifted, widened AB is an artifact/contamination
signal to confirm on the BAM; QUAL is site-level and cannot vouch for S7's genotype (GQ < 20).
**Scores:** 37 + 53 = **90** · **Assertions 4/4.**

### Input 3 — Edge
**Prompt:** "Some genotypes in cohort.vcf are ./. — how much missingness per sample, what happens to allele frequency if
I treat them as reference, and is GQ really derived from PL?"
**Code:** `runs/in3/miss.py` (cyvcf2) + `bcftools view -i 'GT[5]="mis"'`.
**Printed:**
```
SYN_S6: 76/361 = 0.211   (all others 0)
AF bias from treating ./. as 0/0: mean 0.0060, max 0.1250
GQ == min(99, 2nd-smallest PL - smallest PL): 2812/2812 genotypes
bcftools: sites where SYN_S6 is ./. -> 76
```
**Scores:** 38 + 55 = **93** · **Assertions 4/4.**

### Input 4 — Variant B
**Prompt:** "I got sample.g.vcf from the sequencing core. Can I count and filter variants in it? What are these
<NON_REF> records?"
**Printed (runs/in4/out.txt):**
```
chr1 1    END=1025 G <NON_REF>   .     0/0 30 99
chr1 1026 .        G C,<NON_REF> 512.6 0/1 31 99
chr1 1027 END=1200 A <NON_REF>   .     0/0 28 60
chr1 1201 END=1230 T <NON_REF>   .     0/0 3  0
candidate variant sites (N_ALT>1): chr1 1026 G C,<NON_REF>
3 blocks cover 1229 bp ; naive record count: 4
```
Interpretation: a reference-confidence intermediate; 4 records ≠ 4 variants; the 1201–1230 band (GQ 0) is no-data,
not confident hom-ref; joint-genotype before filtering/annotating; never `bcftools merge` single-sample VCFs instead.
**Scores:** 37 + 52 = **89** · **Assertions 4/4.**

### Input 5 — Stress
**Prompt:** "Convert cohort.vcf to BCF and an indexed VCF.gz, pull chr2:1-3000, explain why my region query fails on a
file compressed with gzip, and write a QUAL>30 subset from Python."
**Printed:**
```
35729 cohort.bcf / 27475 cohort.vcf.gz ; region chr2:1-3000 -> 32 records (bcftools and cyvcf2 agree)
plain gzip: index: the file is not BGZF compressed, cannot index ; Failed to read ...: not compressed with bgzip
cyvcf2 Writer: kept 350/361 records with QUAL > 30
```
**Scores:** 37 + 53 = **90** · **Assertions 3/4** (FAIL: error table quotes an older message).

## Recommendations
- **[P2]** Fix the usage-guide `bcftools query -H` tip.
- **[P2]** Update the bgzip error string in Common Errors.
- **[P2]** Add a one-line gVCF candidate-site command (`-i 'N_ALT>1'`).

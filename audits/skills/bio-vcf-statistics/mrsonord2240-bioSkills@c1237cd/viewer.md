> **Audit record for `bio-vcf-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/variant-calling/vcf-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-statistics
Generated: 2026-09-15 · Re-audit of the fixed Skill · Auditor: variant-annotation-curation-analyst round-2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-statistics`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 7 (5 regression inputs from the pre-fix audit + 2 new).

**Pre-fix → post-fix:** 87 (Production Ready) → **88 (Production Ready)**. Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260915/bio-vcf-statistics/`; fix log (not evidence): `F:/OpenScience/specialist-src/round2/fixes/bio-vcf-statistics.md`.

Environment and data: Re-audit of the fixed Skill (fork commit c1237cdb). Mode A. Windows bcftools 1.24 (plugins via BCFTOOLS_PLUGINS); WSL agents distro: bcftools 1.21, vcftools 0.1.17, cyvcf2 0.34.0, matplotlib (plot-vcfstats), somalier 0.3.5, peddy 0.4.8. Data SYNTHETIC (data/make_data.py, seed 20260911): 8 samples, SYN_S6 low coverage, SYN_S7 ~15% contaminated, SYN_S8 duplicate of SYN_S3, 6 excess-het paralog sites. The 5 pre-fix inputs were re-run from runs/p_in1..p_in5 (example taken from the fork commit; the het allele-balance one-liner swapped for the post-fix text); inputs 6 and 7 are new (runs/in6 builds a SYNTHETIC phased copy of the cohort; runs/in7 a soft-filtered copy). peddy still cannot run on the 35-kb synthetic genome; VerifyBamID2/CHARR need BAM/gVCF input. n_inputs 7 = 5 regression + 2 new. Inputs executed: 7/7.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 88/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Metric table verified on data (TSTV field 5, PSC column 14 = nMissing, ExcessHet>54.69 = the 6 planted paralog sites, gtcheck/KING/somalier find the S3/S8 duplicate). The fixed het allele-balance one-liner is now per sample and matches an independent parse on unphased calls, but it tests only 0/1 and 0|1, so on a phased VCF it silently drops every 1|0 het (n halved). |
| Reliability | 10/12 | Common Errors now covers the plot-vcfstats LaTeX requirement. The quick 'PASS' count returns 0 on a callset whose FILTER is '.', while the shipped vcf_stats.py counts the same records as PASS (361); nothing in the Skill explains the difference. |
| Performance context | 7/8 | 228-line SKILL.md; usage guide holds the Python extensions. |
| Agent usability | 15/16 | Order-of-operations and ancestry-stratification rules are explicit; the HWE excess-only rule was demonstrated. |
| Human usability | 7/8 | Prompts map to sections; decision table readable. |
| Security | 11/12 | Local files; no credentials. |
| Maintainability | 9/12 | Runnable example; no test data; peddy/somalier site-panel requirements still unstated (left unfixed by the fixer). |
| Agent specific | 18/20 | Clear trigger and hand-offs to filtering/normalization; identity QC flagged as mandatory before association. |

Shipped-means-present (gate 8): SKILL.md points at examples/vcf_stats.py and the usage guide; both exist at the fork commit. PASS.

Research scope (gate 7): Cohort QC; identity checks are sample-level QC, not individual interpretation. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 2 | Variant A | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 3 | Edge | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 4 | Variant B | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 5 | Stress | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 6 | Edge | 33 | 48 | 81 | 3/4 | yes | ✅ |
| 7 | Variant A | 33 | 47 | 80 | 3/4 | yes | ✅ |

**Execution Average: 87.7 / 100** · **Assertion Pass Rate: 26/28 (93 %)** · Layer 1 avg 35.9 · Layer 2 avg 51.9

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 88 × 0.4 + 87.7 × 0.6 = 35.2 + 52.6 = 88 → ⭐ Production Ready**

## Detailed Outputs

### Input 1 — Canonical: Callset QC summary (regression)
**Prompt:** "Give me a QC summary of cohort.vcf: counts, Ti/Tv, per-sample het/hom and missingness, and tell me whether the callset looks trustworthy."

**Executed:** yes — runs/p_in1/run.sh (Windows) and run_wsl.sh (fork copy of vcf_stats.py, plot-vcfstats) in WSL.

Code `runs/p_in1/run.sh`:
```bash
#!/bin/bash
# Input 1 (Canonical): "Give me a QC summary of cohort.vcf: counts, Ti/Tv, per-sample het/hom and missingness,
# and tell me whether the callset looks trustworthy." SYNTHETIC 8-sample raw joint callset (data/make_data.py):
# SYN_S6 low coverage, SYN_S7 contaminated, SYN_S8 re-sequenced duplicate of SYN_S3, 70 artifact sites.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "### $(bcftools --version | head -1)"
bcftools stats cohort.vcf.gz > stats.txt              # SKILL.md: cohort-level
bcftools stats -s - cohort.vcf.gz > per_sample.txt    # SKILL.md: per-sample (PSC/PSI lines)
echo "== SN (grep ^SN | cut -f3-) =="; grep "^SN" stats.txt | cut -f3-
echo "== TSTV header + line; SKILL.md says ratio is field 5 =="; grep "^# TSTV" stats.txt; grep "^TSTV" stats.txt
echo "cut -f5 -> $(grep '^TSTV' stats.txt | cut -f5)"
echo "== PSC header + lines =="; grep "^# PSC" per_sample.txt; grep "^PSC" per_sample.txt
echo "== usage-guide missingness idiom: grep ^PSC | cut -f3,14 =="; grep "^PSC" per_sample.txt | cut -f3,14
echo "== derived per-sample het/hom-alt ratio =="; grep "^PSC" per_sample.txt | awk -F'\t' '{printf "%s het=%d homalt=%d het/hom=%.2f missing=%d\n",$3,$6,$5,($5>0?$6/$5:0),$14}'
echo "== quick counts (SKILL.md) =="
echo "records $(bcftools view -H cohort.vcf.gz | wc -l) snps $(bcftools view -v snps -H cohort.vcf.gz | wc -l) indels $(bcftools view -v indels -H cohort.vcf.gz | wc -l) PASS $(bcftools view -f PASS -H cohort.vcf.gz | wc -l)"
bcftools query -f '%QUAL\n' cohort.vcf.gz | awk '{s+=$1;n++} END{print "mean QUAL:", s/n}'
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-statistics/examples/vcf_stats.py > vcf_stats.fork_copy.py
echo "== shipped examples/vcf_stats.py and plot-vcfstats: WSL, see out_wsl.txt =="
```

Code `runs/p_in1/run_wsl.sh`:
```bash
#!/bin/bash
# WSL part of input 1: shipped examples/vcf_stats.py (cyvcf2 0.34.0) and plot-vcfstats (bcftools 1.21 + matplotlib).
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
python -c "import cyvcf2, matplotlib; print('cyvcf2', cyvcf2.__version__, 'matplotlib', matplotlib.__version__)"
echo "== examples/vcf_stats.py cohort.vcf.gz =="; python vcf_stats.fork_copy.py cohort.vcf.gz; echo "exit=$?"
echo "== examples/vcf_stats.py with no argument =="; python vcf_stats.fork_copy.py; echo "exit=$?"
echo "== plot-vcfstats -p qc_plots/ stats.txt =="
rm -rf qc_plots; plot-vcfstats -p qc_plots/ stats.txt > plot.log 2>&1; echo "exit=$?"; tail -4 plot.log
ls qc_plots 2>/dev/null | head -20
```

Printed `runs/p_in1/out.txt`:
```
### bcftools 1.24
== SN (grep ^SN | cut -f3-) ==
number of samples:	8
number of records:	361
number of no-ALTs:	0
number of SNPs:	331
number of MNPs:	0
number of indels:	30
number of others:	0
number of multiallelic sites:	0
number of multiallelic SNP sites:	0
== TSTV header + line; SKILL.md says ratio is field 5 ==
# TSTV, transitions/transversions
# TSTV	[2]id	[3]ts	[4]tv	[5]ts/tv	[6]ts (1st ALT)	[7]tv (1st ALT)	[8]ts/tv (1st ALT)
TSTV	0	195	136	1.43	195	136	1.43
cut -f5 -> 1.43
== PSC header + lines ==
# PSC, Per-sample counts. Note that the ref/het/hom counts include only SNPs, for indels see PSI. The rest include both SNPs and indels.
# PSC	[2]id	[3]sample	[4]nRefHom	[5]nNonRefHom	[6]nHets	[7]nTransitions	[8]nTransversions	[9]nIndels	[10]average depth	[11]nSingletons	[12]nHapRef	[13]nHapAlt	[14]nMissing
PSC	0	SYN_S1	164	34	145	104	75	18	30.0	87	0	0	0
PSC	0	SYN_S2	240	34	81	64	51	6	31.9	9	0	0	0
PSC	0	SYN_S3	237	33	85	65	53	6	32.1	0	0	0	0
PSC	0	SYN_S4	244	33	76	54	55	8	31.2	10	0	0	0
PSC	0	SYN_S5	242	31	80	62	49	8	31.6	11	0	0	0
PSC	0	SYN_S6	201	23	56	41	38	5	26.4	13	0	0	76
PSC	0	SYN_S7	237	32	82	55	59	10	31.6	9	0	0	0
PSC	0	SYN_S8	237	33	85	65	53	6	31.4	0	0	0	0
== usage-guide missingness idiom: grep ^PSC | cut -f3,14 ==
SYN_S1	0
SYN_S2	0
SYN_S3	0
SYN_S4	0
SYN_S5	0
SYN_S6	76
SYN_S7	0
SYN_S8	0
== derived per-sample het/hom-alt ratio ==
SYN_S1 het=145 homalt=34 het/hom=4.26 missing=0
SYN_S2 het=81 homalt=34 het/hom=2.38 missing=0
SYN_S3 het=85 homalt=33 het/hom=2.58 missing=0
SYN_S4 het=76 homalt=33 het/hom=2.30 missing=0
SYN_S5 het=80 homalt=31 het/hom=2.58 missing=0
SYN_S6 het=56 homalt=23 het/hom=2.43 missing=76
SYN_S7 het=82 homalt=32 het/hom=2.56 missing=0
SYN_S8 het=85 homalt=33 het/hom=2.58 missing=0
... (5 more lines in out.txt)
```

Printed `runs/p_in1/out_wsl.txt`:
```
cyvcf2 0.34.0 matplotlib 3.11.2
== examples/vcf_stats.py cohort.vcf.gz ==
=== VCF Statistics ===
Total variants:    361
  SNPs:            331
  Indels:          30
  Other:           0

PASS variants:     361
Filtered:          0

Transitions:       195
Transversions:     136
Ti/Tv ratio:       1.43

Mean QUAL:         514.5
exit=0
== examples/vcf_stats.py with no argument ==
Usage: vcf_stats.py <input.vcf.gz>
exit=1
== plot-vcfstats -p qc_plots/ stats.txt ==
exit=2
Plotting graphs: python3 plot.py
Neither pdflatex or tectonic were found in your PATH, impossible to create a PDF at /tmp/vaca/env/bin/plot-vcfstats line 116.
	main::error("Neither pdflatex or tectonic were found in your PATH, impossi"...) called at /tmp/vaca/env/bin/plot-vcfstats line 2085
	main::create_pdf(HASH(0x6157de777c80)) called at /tmp/vaca/env/bin/plot-vcfstats line 77
counts_by_af.indels.dat
counts_by_af.snps.dat
depth.0.dat
depth.0.png
indels.0.dat
indels.0.png
plot-vcfstats.log
plot.py
substitutions.0.png
tstv_by_af.0.dat
tstv_by_qual.0.dat
tstv_by_qual.0.png
rc=0
```

**Output (agent answer, Mode A):** Same metrics as pre-fix (361 records, Ti/Tv 1.43, S6 missing 76). plot-vcfstats still exits 2 without a LaTeX engine and writes the PNGs, which the post-fix Common Errors row and usage-guide tip now state.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100 · **Assertions 4/4**
- [PASS] Counts and Ti/Tv extracted correctly — SN and TSTV field 5 = 1.43
- [PASS] Per-sample missingness from PSC column 14 is correct — S6 = 76, matches vcftools
- [PASS] Shipped example runs — vcf_stats.py same counts
- [PASS] plot-vcfstats instructions suffice to produce the report — LaTeX need now documented; PNGs written, PDF step exit 2 as described

### Input 2 — Variant A: Swap / duplicate / relatedness screen (regression)
**Prompt:** "Before association testing, screen the 8 samples for swaps, duplicates and unexpected relatedness."

**Executed:** yes — runs/p_in2/run.sh (bcftools gtcheck, Windows) and run_wsl.sh (vcftools --relatedness2, somalier, peddy) in WSL.

Code `runs/p_in2/run.sh`:
```bash
#!/bin/bash
# Input 2 (Variant A): "Before association testing, screen the 8-sample cohort for sample swaps / duplicates /
# unexpected relatedness." SYNTHETIC: SYN_S8 is a re-sequenced duplicate of SYN_S3 (truth).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== Version note check: does gtcheck still accept -G? =="
bcftools gtcheck -G 1 cohort.vcf.gz > /dev/null 2> G.err; echo "gtcheck -G 1 exit=$?"; head -2 G.err
bcftools gtcheck 2>&1 | grep -E "^\s+-(E|e|g|u|G)[ ,]" | head -8
echo "== SKILL.md: bcftools gtcheck input.vcf.gz (all-pairs, no -g) =="
bcftools gtcheck cohort.vcf.gz > gtcheck.txt 2> gtcheck.err; echo "exit=$?"
grep -m1 "^# DC" gtcheck.txt
grep "^DC" gtcheck.txt | sort -t$'\t' -k4,4g | head -6
echo "(lowest discordance pairs above; SKILL says smaller = more similar)"
echo "== vcftools --relatedness2 and somalier: WSL, see out_wsl.txt =="
```

Code `runs/p_in2/run_wsl.sh`:
```bash
#!/bin/bash
# WSL part of input 2: vcftools --relatedness2 (KING-robust), somalier extract/relate, peddy (if installable).
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
S=../../data
vcftools --version
echo "== SKILL.md: vcftools --gzvcf input.vcf.gz --relatedness2 --out kin =="
vcftools --gzvcf cohort.vcf.gz --relatedness2 --out kin > kin.log 2>&1; echo "exit=$?"
awk 'NR==1 || ($1!=$2)' kin.relatedness2 | sort -k7,7gr | head -6
echo "KING bands (SKILL.md): >0.354 dup/MZ, 0.177-0.354 1st, 0.0884-0.177 2nd"
Q=/tmp/vaca/qc/bin
if [ -x $Q/somalier ]; then
  echo "== somalier $($Q/somalier 2>&1 | grep -m1 -i version) =="
  bcftools view -G cohort.vcf.gz -Oz -o sites.vcf.gz; bcftools index -t -f sites.vcf.gz
  rm -rf extracted; mkdir -p extracted
  $Q/somalier extract -d extracted/ --sites sites.vcf.gz -f $S/ref.fa cohort.vcf.gz > som_extract.log 2>&1; echo "extract exit=$?"; tail -2 som_extract.log
  awk 'BEGIN{OFS="\t"} {print $1,$2,$3,$4,$5,$6}' $S/cohort.ped > cohort.ped
  $Q/somalier relate --ped cohort.ped extracted/*.somalier > som_relate.log 2>&1; echo "relate exit=$?"; tail -2 som_relate.log
  [ -f somalier.pairs.tsv ] && sort -t$'\t' -k3,3gr somalier.pairs.tsv | cut -f1-6 | head -4
else
  echo "somalier not installed: $(tail -3 /tmp/vaca/qc_install.log)"
fi
if [ -x $Q/python ] && $Q/python -c "import peddy" 2>/dev/null; then
  echo "== peddy (SKILL.md: python -m peddy -p 4 --plot --prefix cohort_qc input.vcf.gz cohort.ped) =="
  $Q/python -m peddy -p 4 --plot --prefix cohort_qc cohort.vcf.gz cohort.ped > peddy.log 2>&1; echo "peddy exit=$?"; tail -4 peddy.log
fi
```

Printed `runs/p_in2/out.txt`:
```
== Version note check: does gtcheck still accept -G? ==
gtcheck -G 1 exit=127
The option -G, --GTs-only has been deprecated
    -E, --error-probability INT        Phred-scaled probability of genotyping error, 0 for faster but less accurate results [40]
    -e, --exclude [qry|gt]:EXPR        Exclude sites for which the expression is true
    -g, --genotypes FILE               Genotypes to compare against
    -u, --use TAG1[,TAG2]              Which tag to use in the query file (TAG1) and the -g file (TAG2) [PL,GT]
== SKILL.md: bcftools gtcheck input.vcf.gz (all-pairs, no -g) ==
exit=0
# DCv2, discordance version 2:
DCv2	SYN_S8	SYN_S3	1.984517e+00	5.062172e-01	361	361
DCv2	SYN_S7	SYN_S4	1.867697e+03	3.292303e-01	361	247
DCv2	SYN_S7	SYN_S2	1.891262e+03	3.385347e-01	361	251
DCv2	SYN_S7	SYN_S6	1.918533e+03	3.218988e-01	285	182
DCv2	SYN_S7	SYN_S5	1.924281e+03	3.522045e-01	361	248
DCv2	SYN_S6	SYN_S2	2.189814e+03	3.299103e-01	285	188
(lowest discordance pairs above; SKILL says smaller = more similar)
== vcftools --relatedness2 and somalier: WSL, see out_wsl.txt ==
```

Printed `runs/p_in2/out_wsl.txt`:
```
VCFtools (0.1.17)
== SKILL.md: vcftools --gzvcf input.vcf.gz --relatedness2 --out kin ==
exit=0
SYN_S3	SYN_S8	89	0	89	89	0.5
SYN_S8	SYN_S3	89	0	89	89	0.5
SYN_S5	SYN_S7	38	10	87	92	0.100559
SYN_S7	SYN_S5	38	10	92	87	0.100559
SYN_S2	SYN_S7	39	12	84	92	0.0852273
SYN_S7	SYN_S2	39	12	92	84	0.0852273
KING bands (SKILL.md): >0.354 dup/MZ, 0.177-0.354 1st, 0.0884-0.177 2nd
== somalier somalier version: 0.3.5 ==
extract exit=0
somalier version: 0.3.5
[somalier] found 361 sites
relate exit=0
[somalier] wrote samples to: somalier.samples.tsv
[somalier] wrote pair-wise relatedness metrics to: somalier.pairs.tsv
SYN_S3	SYN_S8	1.000	0	216	0.868
SYN_S2	SYN_S7	0.600	1	111	0.274
SYN_S5	SYN_S7	0.533	3	108	0.218
SYN_S4	SYN_S7	0.449	4	116	0.348
== peddy (SKILL.md: python -m peddy -p 4 --plot --prefix cohort_qc input.vcf.gz cohort.ped) ==
peddy exit=1
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "cyvcf2/cyvcf2.pyx", line 122, in cyvcf2.cyvcf2.par_het
  File "cyvcf2/cyvcf2.pyx", line 1014, in cyvcf2.cyvcf2.VCF._finish_het
IndexError: index 0 is out of bounds for axis 0 with size 0
rc=0
```

**Output (agent answer, Mode A):** Unchanged text; identical results: gtcheck S8/S3 discordance 1.98; KING phi 0.5; somalier 1.0; peddy fails on the synthetic genome.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Duplicate pair identified by gtcheck — S8/S3 discordance 1.98
- [PASS] KING kinship bands interpreted correctly — phi 0.5 = duplicate/MZ
- [PASS] Version note on gtcheck -G is accurate — '-G has been deprecated'
- [PASS] somalier commands run as written — extract/relate exit 0

### Input 3 — Edge: Should every HWE failure be dropped? (regression)
**Prompt:** "About 20 sites fail HWE in my cohort. Should I drop every HWE failure? Some might be real."

**Executed:** yes — runs/p_in3/run.sh (Windows, +fill-tags) and run_wsl.sh (vcftools --hardy).

Code `runs/p_in3/run.sh`:
```bash
#!/bin/bash
# Input 3 (Edge): "About 20 sites fail HWE in my cohort. Should I drop every HWE failure? Some might be real."
# SYNTHETIC: 6 planted excess_het sites (collapsed-paralog-like, every sample het), SYN_S6 low coverage,
# no case/control labels in this cohort (PED phenotype -9), single simulated population.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== SKILL.md: ExcessHet > 54.69 (GATK default cutoff) =="
bcftools query -f '%CHROM\t%POS\t%INFO/ExcessHet\n' cohort.vcf.gz | tr -d '\r' | awk '$3>54.69' > exhet_flag.tsv
cat exhet_flag.tsv
awk -F'\t' 'NR>1 && $3=="excess_het"{print $1"\t"$2}' $S/cohort_truth_classes.tsv > truth_exhet.tsv
echo "flagged=$(wc -l < exhet_flag.tsv) truth excess_het=$(wc -l < truth_exhet.tsv) overlap=$(cut -f1,2 exhet_flag.tsv | grep -cFf truth_exhet.tsv)"
echo "== genotype filter first (GQ<20 | DP<8 -> ./.), then two-sided vs excess-het HWE with +fill-tags =="
bcftools filter -S . -e 'FMT/GQ<20 | FMT/DP<8' cohort.vcf.gz -Oz -o gtf.vcf.gz; bcftools index -f gtf.vcf.gz
for f in cohort gtf; do
  bcftools +fill-tags $f.vcf.gz -Oz -o $f.tags.vcf.gz -- -t HWE,ExcHet 2>/dev/null; bcftools index -f $f.tags.vcf.gz
  echo "$f: HWE p<1e-3 (two-sided) = $(bcftools view -H -i 'INFO/HWE<1e-3' $f.tags.vcf.gz | wc -l); ExcHet p<1e-3 (excess only) = $(bcftools view -H -i 'INFO/ExcHet<1e-3' $f.tags.vcf.gz | wc -l)"
done
echo "HWE / ExcHet p-values at the 6 ExcessHet-flagged sites (n=8 samples limits the attainable p):"
cut -f1,2 exhet_flag.tsv > exhet_regions.tsv
bcftools query -R exhet_regions.tsv -f '%CHROM\t%POS\t%INFO/HWE\t%INFO/ExcHet\t[%GT ]\n' gtf.tags.vcf.gz | tr -d '\r'
echo "sites HWE p<0.05: cohort=$(bcftools view -H -i 'INFO/HWE<0.05' cohort.tags.vcf.gz | wc -l) gtf=$(bcftools view -H -i 'INFO/HWE<0.05' gtf.tags.vcf.gz | wc -l)"
bcftools query -i 'INFO/HWE<0.05' -f '%CHROM\t%POS\n' cohort.tags.vcf.gz | tr -d '\r' > hwe_fail.tsv
echo "two-sided HWE failures by truth class:"; awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv hwe_fail.tsv | sort | uniq -c
echo "== exact test: vcftools --hardy in WSL (see out_wsl.txt) =="
```

Code `runs/p_in3/run_wsl.sh`:
```bash
#!/bin/bash
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
S=../../data
echo "== SKILL.md: vcftools --gzvcf controls.vcf.gz --hardy --out hwe (exact test) =="
vcftools --gzvcf gtf.vcf.gz --hardy --out hwe > hwe.log 2>&1; echo "exit=$?"
head -2 hwe.hwe
echo "sites P_HWE<0.01: $(awk 'NR>1 && $6<0.01' hwe.hwe | wc -l); P_HET_EXCESS<0.01: $(awk 'NR>1 && $8<0.01' hwe.hwe | wc -l); P_HET_DEFICIT<0.01: $(awk 'NR>1 && $7<0.01' hwe.hwe | wc -l)"
awk 'NR>1 && $8<0.01 {print $1"\t"$2}' hwe.hwe > excess.tsv
echo "excess-het (vcftools) by truth class:"; awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv excess.tsv | sort | uniq -c
```

Printed `runs/p_in3/out.txt`:
```
== SKILL.md: ExcessHet > 54.69 (GATK default cutoff) ==
chr1	8645	104.411
chr1	13263	77.25
chr1	16967	130.515
chr2	9557	84.783
chr2	11062	173.929
chr2	13903	86.367
flagged=6 truth excess_het=6 overlap=6
== genotype filter first (GQ<20 | DP<8 -> ./.), then two-sided vs excess-het HWE with +fill-tags ==
cohort: HWE p<1e-3 (two-sided) = 0; ExcHet p<1e-3 (excess only) = 0
gtf: HWE p<1e-3 (two-sided) = 0; ExcHet p<1e-3 (excess only) = 0
HWE / ExcHet p-values at the 6 ExcessHet-flagged sites (n=8 samples limits the attainable p):
chr1	8645	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
chr1	13263	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
chr1	16967	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
chr2	9557	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
chr2	11062	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
chr2	13903	0.0253302	0.0198912	0/1 0/1 0/1 0/1 0/1 0/1 0/1 0/1 
sites HWE p<0.05: cohort=19 gtf=19
two-sided HWE failures by truth class:
      6 excess_het
     10 true_homalt
      2 true_indel
      1 true_snp
== exact test: vcftools --hardy in WSL (see out_wsl.txt) ==
```

Printed `runs/p_in3/out_wsl.txt`:
```
== SKILL.md: vcftools --gzvcf controls.vcf.gz --hardy --out hwe (exact test) ==
exit=0
CHR	POS	OBS(HOM1/HET/HOM2)	E(HOM1/HET/HOM2)	ChiSq_HWE	P_HWE	P_HET_DEFICIT	P_HET_EXCESS
chr1	5050	6/1/0	6.04/0.93/0.04	4.142012e-02	1.000000e+00	1.000000e+00	1.000000e+00
sites P_HWE<0.01: 2; P_HET_EXCESS<0.01: 0; P_HET_DEFICIT<0.01: 2
excess-het (vcftools) by truth class:
rc=0
```

**Output (agent answer, Mode A):** Unchanged text; identical results: ExcessHet>54.69 flags exactly the 6 planted sites; two-sided HWE p<0.05 hits 19 sites including 13 real variants.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Recommends excess-het-only filtering — per SKILL.md
- [PASS] ExcessHet cutoff isolates the artifact sites — 6/6, no others
- [PASS] Warns that two-sided HWE removes real variants — 13 real sites in the two-sided set
- [PASS] Mentions ancestry and controls-only requirements — stated

### Input 4 — Variant B: Contamination check from the VCF (regression)
**Prompt:** "One sample may be contaminated. Use the VCF to check allele balance, het/hom and missingness per sample, and tell me what to do next."

**Executed:** yes — runs/p_in4/run.sh (Windows) with the post-fix one-liner verbatim, and run_wsl.sh (vcftools --missing-indv).

Code `runs/p_in4/run.sh`:
```bash
#!/bin/bash
# Input 4 (Variant B): "One sample may be contaminated. Use the VCF to check allele balance, het/hom and
# missingness per sample, and tell me what to do next." SYNTHETIC: SYN_S7 carries ~15% foreign reads,
# SYN_S6 is low coverage (25% of sites at DP 0-3).
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
echo "== SKILL.md quick het AB check (post-fix), verbatim =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}'   # expect ~0.5 per sample
echo "== per-sample het AB computed correctly (only het genotypes, per sample) =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | tr -d '\r' | awk -F'\t' '$2=="0/1"{split($3,a,","); if(a[1]+a[2]>0){ab=a[2]/(a[1]+a[2]); s[$1]+=ab; n[$1]++; if(ab<0.2||ab>0.8) o[$1]++}} END{for(k in n) printf "%s n_het=%d mean_AB=...
echo "== per-sample het/hom-alt and missing from bcftools stats -s - (PSC) =="
bcftools stats -s - cohort.vcf.gz | grep "^PSC" | awk -F'\t' '{printf "%s het/hom=%.2f nHets=%d missing=%d\n",$3,($5>0?$6/$5:0),$6,$14}'
echo "== vcftools --missing-indv in WSL (see out_wsl.txt) =="
```

Code `runs/p_in4/run_wsl.sh`:
```bash
#!/bin/bash
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
echo "== SKILL.md: vcftools --gzvcf input.vcf.gz --missing-indv / --missing-site =="
vcftools --gzvcf cohort.vcf.gz --missing-indv --out sample_miss > m1.log 2>&1; echo "exit=$?"; cat sample_miss.imiss
vcftools --gzvcf cohort.vcf.gz --missing-site --out site_miss > m2.log 2>&1; echo "exit=$?"; echo "sites with F_MISS>0.05: $(awk 'NR>1 && $6>0.05' site_miss.lmiss | wc -l)"
```

Printed `runs/p_in4/out.txt`:
```
== SKILL.md quick het AB check (post-fix), verbatim ==
SYN_S3	mean het AB: 0.453 (n=89)
SYN_S4	mean het AB: 0.458 (n=84)
SYN_S5	mean het AB: 0.474 (n=87)
SYN_S6	mean het AB: 0.438 (n=60)
SYN_S7	mean het AB: 0.419 (n=92)
SYN_S8	mean het AB: 0.489 (n=89)
SYN_S1	mean het AB: 0.449 (n=162)
SYN_S2	mean het AB: 0.473 (n=84)
== per-sample het AB computed correctly (only het genotypes, per sample) ==
SYN_S1 n_het=162 mean_AB=0.449 frac_outside_0.2-0.8=0.049
SYN_S2 n_het=84 mean_AB=0.473 frac_outside_0.2-0.8=0.024
SYN_S3 n_het=89 mean_AB=0.453 frac_outside_0.2-0.8=0.079
SYN_S4 n_het=84 mean_AB=0.458 frac_outside_0.2-0.8=0.095
SYN_S5 n_het=87 mean_AB=0.474 frac_outside_0.2-0.8=0.034
SYN_S6 n_het=60 mean_AB=0.438 frac_outside_0.2-0.8=0.083
SYN_S7 n_het=92 mean_AB=0.419 frac_outside_0.2-0.8=0.163
SYN_S8 n_het=89 mean_AB=0.489 frac_outside_0.2-0.8=0.000
== per-sample het/hom-alt and missing from bcftools stats -s - (PSC) ==
SYN_S1 het/hom=4.26 nHets=145 missing=0
SYN_S2 het/hom=2.38 nHets=81 missing=0
SYN_S3 het/hom=2.58 nHets=85 missing=0
SYN_S4 het/hom=2.30 nHets=76 missing=0
SYN_S5 het/hom=2.58 nHets=80 missing=0
SYN_S6 het/hom=2.43 nHets=56 missing=76
SYN_S7 het/hom=2.56 nHets=82 missing=0
SYN_S8 het/hom=2.58 nHets=85 missing=0
== vcftools --missing-indv in WSL (see out_wsl.txt) ==
```

Printed `runs/p_in4/out_wsl.txt`:
```
== SKILL.md: vcftools --gzvcf input.vcf.gz --missing-indv / --missing-site ==
exit=0
INDV	N_DATA	N_GENOTYPES_FILTERED	N_MISS	F_MISS
SYN_S1	361	0	0	0
SYN_S2	361	0	0	0
SYN_S3	361	0	0	0
SYN_S4	361	0	0	0
SYN_S5	361	0	0	0
SYN_S6	361	0	76	0.210526
SYN_S7	361	0	0	0
SYN_S8	361	0	0	0
exit=0
sites with F_MISS>0.05: 76
rc=0
```

**Output (agent answer, Mode A):** Post-fix one-liner prints one line per sample: S7 0.419 (n=92) lowest, S8 0.489, S1 0.449 (n=162), identical to the auditor's independent per-sample computation (pre-fix: a single meaningless 0.729). S6 is a coverage problem (F_MISS 0.21).

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] The Skill's quick het-AB check gives a valid number — per-sample means equal the independent computation
- [PASS] Contaminated sample identified — SYN_S7 lowest mean AB
- [PASS] Recommends VerifyBamID2/CHARR confirmation — signals, not measurement
- [PASS] Missingness counts only ./. — vcftools F_MISS S6 0.21

### Input 5 — Stress: Raw vs filtered comparison with novel/known strata (regression)
**Prompt:** "Compare the raw and hard-filtered callsets: counts removed, Ti/Tv overall and in the novel (not-in-dbSNP) fraction, novel% stratified by allele frequency, and a stratified Ti/Tv for a 'difficult' region BED."

**Executed:** yes — runs/p_in5/run.sh (Windows bcftools 1.24).

Code `runs/p_in5/run.sh`:
```bash
#!/bin/bash
# Input 5 (Stress): "Compare the raw and hard-filtered callsets: counts removed, Ti/Tv overall and in the novel
# (not-in-dbSNP) fraction, novel% stratified by allele frequency, and a stratified Ti/Tv for a 'difficult'
# region BED." SYNTHETIC cohort; SYNTHETIC dbSNP-like sites file built from the simulation's known IDs.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -t -f cohort.vcf.gz
bcftools filter -i '(TYPE="snp" && QUAL>=30 && (INFO/QD>=2.0||INFO/QD=".") && (INFO/FS<=60.0||INFO/FS=".") && (INFO/MQ>=40.0||INFO/MQ=".") && (INFO/MQRankSum>=-12.5||INFO/MQRankSum=".") && (INFO/ReadPosRankSum>=-8.0||INFO/ReadPosRankSum="."...
echo "== SKILL.md compare: bcftools stats file1 file2 > cmp.txt =="
bcftools stats cohort.vcf.gz filtered.vcf.gz > cmp.txt; echo "exit=$?"
grep -E "^SN" cmp.txt | grep -E "number of (records|SNPs|indels)"; grep "^TSTV" cmp.txt
echo "(stats with 2 files reports id 0 = private to file1, 1 = private to file2, 2 = shared)"
echo "== novel/known via dbSNP annotate (SKILL.md idiom) =="
bcftools view -G -i 'ID!="."' cohort.vcf.gz -Oz -o dbsnp_syn.vcf.gz; bcftools index -t -f dbsnp_syn.vcf.gz
for f in cohort filtered; do
  bcftools annotate -x ID $f.vcf.gz -Oz -o $f.noid.vcf.gz; bcftools index -t -f $f.noid.vcf.gz
  bcftools annotate -a dbsnp_syn.vcf.gz -c ID $f.noid.vcf.gz -Oz -o $f.annotated.vcf.gz; bcftools index -t -f $f.annotated.vcf.gz
  echo "$f: $(bcftools view -H $f.annotated.vcf.gz | awk '{n++; if($3==".") novel++} END{print "novel:", novel/n}')"
  echo "$f Ti/Tv all=$(bcftools stats $f.annotated.vcf.gz | grep '^TSTV' | cut -f5 | tr -d '\r') known=$(bcftools view -i 'ID!="."' $f.annotated.vcf.gz | bcftools stats | grep '^TSTV' | cut -f5 | tr -d '\r') novel=$(bcftools view -i 'ID="."...
done
echo "== novel% stratified by cohort AF (fill-tags AF) =="
bcftools +fill-tags filtered.annotated.vcf.gz -- -t AF 2>/dev/null | bcftools query -f '%ID\t%AF\n' | tr -d '\r' | \
  awk -F'\t' '{b=($2<0.1?"AF<0.1":($2<0.3?"0.1-0.3":">=0.3")); n[b]++; if($1==".") v[b]++} END{for(k in n) printf "%s n=%d novel%%=%.1f\n",k,n[k],100*v[k]/n[k]}'
echo "novel common (AF>=0.3) sites by truth class:"
bcftools +fill-tags filtered.annotated.vcf.gz -- -t AF 2>/dev/null | bcftools query -i 'ID="." && INFO/AF>=0.3' -f '%CHROM\t%POS\n' | tr -d '\r' > novel_common.tsv
awk -F'\t' 'NR==FNR{c[$1"\t"$2]=$3;next} {print c[$1"\t"$2]}' $S/cohort_truth_classes.tsv novel_common.tsv | sort | uniq -c
echo "== stratified: bcftools stats -R difficult.bed vs -R easy.bed (SKILL.md) =="
printf 'chr1\t5000\t12000\n' > difficult_regions.bed; printf 'chr1\t12000\t20000\nchr2\t0\t15000\n' > easy_regions.bed
for r in easy difficult; do echo "$r: $(bcftools stats -R ${r}_regions.bed cohort.vcf.gz 2>&1 | grep -E '^TSTV|^SN.*number of records' | cut -f3-5 | tr '\n' ' ')"; done
```

Printed `runs/p_in5/out.txt`:
```
== SKILL.md compare: bcftools stats file1 file2 > cmp.txt ==
exit=0
SN	0	number of records:	62
SN	0	number of SNPs:	56
SN	0	number of indels:	6
SN	1	number of records:	0
SN	1	number of SNPs:	0
SN	1	number of indels:	0
SN	2	number of records:	299
SN	2	number of SNPs:	275
SN	2	number of indels:	24
TSTV	0	21	35	0.60	21	35	0.60
TSTV	1	0	0	0.00	0	0	0.00
TSTV	2	174	101	1.72	174	101	1.72
(stats with 2 files reports id 0 = private to file1, 1 = private to file2, 2 = shared)
== novel/known via dbSNP annotate (SKILL.md idiom) ==
cohort: novel: 0.3241
cohort Ti/Tv all=1.43 known=1.53 novel=1.26
filtered: novel: 0.183946
filtered Ti/Tv all=1.72 known=1.53 novel=3.17
== novel% stratified by cohort AF (fill-tags AF) ==
0.1-0.3 n=87 novel%=5.7
AF<0.1 n=116 novel%=37.9
>=0.3 n=96 novel%=6.2
novel common (AF>=0.3) sites by truth class:
      6 excess_het
== stratified: bcftools stats -R difficult.bed vs -R easy.bed (SKILL.md) ==
easy: number of records:	281 156	102	1.53 
difficult: number of records:	80 39	34	1.15
```

**Output (agent answer, Mode A):** Unchanged text; identical results: removed records Ti/Tv 0.60; novel 32% -> 18%; 6 novel common sites all excess-het artifacts; difficult BED Ti/Tv 1.15 vs 1.53.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100 · **Assertions 4/4**
- [PASS] Two-file stats output read correctly (ids 0/1/2) — private/shared sets
- [PASS] Novel/known via the annotate idiom works — 0.324 -> 0.184
- [PASS] Novel common sites flagged as artifacts — 6/6 excess_het
- [PASS] Region-stratified stats run — -R easy/difficult

### Input 6 — Edge: NEW: het allele balance on a phased VCF
**Prompt:** "Our cohort VCF was read-backed phased, so hets are written 0|1 or 1|0. Run your per-sample het allele-balance check and tell me whether any sample looks contaminated."

**Executed:** yes — runs/in6/run.sh (Windows bcftools 1.24, Python 3.12) on a SYNTHETIC phased copy of the cohort (0/1 written alternately as 0|1 and 1|0, AD unchanged).

Code `runs/in6/run.sh`:
```bash
#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Edge): "Our cohort VCF was read-backed phased, so hets are written 0|1 or 1|0. Run your
# per-sample het allele-balance check and tell me whether any sample looks contaminated."
# Builds a SYNTHETIC phased copy of data/cohort.vcf (each 0/1 alternately written 0|1 and 1|0; AD unchanged) and compares the
# post-fix SKILL.md one-liner with an independent Python parse that counts every het genotype.
set -uo pipefail
source ../env.sh
S=../../data
cat > phase.py <<'EOF'
import sys
k = 0
out = open('phased.vcf', 'w', newline='\n')
for line in open(sys.argv[1]):
    if line.startswith('#'):
        out.write(line); continue
    f = line.rstrip('\n').split('\t')
    gi = f[8].split(':').index('GT')
    for j in range(9, len(f)):
        p = f[j].split(':')
        if p[gi] == '0/1':
            p[gi] = '0|1' if k % 2 == 0 else '1|0'; k += 1
        f[j] = ':'.join(p)
    out.write('\t'.join(f) + '\n')
EOF
cat > ab_indep.py <<'EOF'
import sys, collections
s = collections.defaultdict(float); n = collections.Counter()
for line in open(sys.argv[1]):
    if line.startswith('##'): continue
    f = line.rstrip('\n').split('\t')
    if line.startswith('#'): names = f[9:]; continue
    keys = f[8].split(':'); gi, ai = keys.index('GT'), keys.index('AD')
    for name, v in zip(names, f[9:]):
        p = v.split(':')
        gt = p[gi].replace('|', '/')
        if gt in ('0/1', '1/0') and len(p) > ai and p[ai] != '.':
            r, a = (int(x) for x in p[ai].split(',')[:2])
            if r + a > 0: s[name] += a / (r + a); n[name] += 1
for k in sorted(n): print(f"{k}\tmean het AB: {s[k]/n[k]:.3f} (n={n[k]})")
EOF
$PY phase.py $S/cohort.vcf; bgzip -c phased.vcf > phased.vcf.gz; bcftools index -f phased.vcf.gz
echo "GT codes in phased copy: $(bcftools query -f '[%GT\n]' phased.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
echo "== SKILL.md one-liner (post-fix) verbatim, phased copy =="
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' phased.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}' | sort
echo "== independent Python parse, phased copy (0/1, 0|1, 1|0 all counted) =="
$PY ab_indep.py phased.vcf
echo "== SKILL.md one-liner on the unphased original (for reference) =="
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools query -f '[%SAMPLE\t%GT\t%AD\n]' cohort.vcf.gz | \
    awk -F'\t' '($2=="0/1" || $2=="0|1") {split($3,a,","); d=a[1]+a[2]; if (d>0) {s[$1]+=a[2]/d; n[$1]++}}
        END {for (k in s) printf "%s\tmean het AB: %.3f (n=%d)\n", k, s[k]/n[k], n[k]}' | sort
```

Printed `runs/in6/out.txt`:
```
GT codes in phased copy:      76 ./.    1802 0/0     374 0|1     263 1/1     373 1|0 
== SKILL.md one-liner (post-fix) verbatim, phased copy ==
SYN_S1	mean het AB: 0.449 (n=80)
SYN_S2	mean het AB: 0.457 (n=45)
SYN_S3	mean het AB: 0.456 (n=47)
SYN_S4	mean het AB: 0.466 (n=44)
SYN_S5	mean het AB: 0.475 (n=37)
SYN_S6	mean het AB: 0.429 (n=31)
SYN_S7	mean het AB: 0.425 (n=49)
SYN_S8	mean het AB: 0.489 (n=41)
== independent Python parse, phased copy (0/1, 0|1, 1|0 all counted) ==
SYN_S1	mean het AB: 0.449 (n=162)
SYN_S2	mean het AB: 0.473 (n=84)
SYN_S3	mean het AB: 0.453 (n=89)
SYN_S4	mean het AB: 0.458 (n=84)
SYN_S5	mean het AB: 0.474 (n=87)
SYN_S6	mean het AB: 0.438 (n=60)
SYN_S7	mean het AB: 0.419 (n=92)
SYN_S8	mean het AB: 0.489 (n=89)
== SKILL.md one-liner on the unphased original (for reference) ==
SYN_S1	mean het AB: 0.449 (n=162)
SYN_S2	mean het AB: 0.473 (n=84)
SYN_S3	mean het AB: 0.453 (n=89)
SYN_S4	mean het AB: 0.458 (n=84)
SYN_S5	mean het AB: 0.474 (n=87)
SYN_S6	mean het AB: 0.438 (n=60)
SYN_S7	mean het AB: 0.419 (n=92)
SYN_S8	mean het AB: 0.489 (n=89)
```

**Output (agent answer, Mode A):** Post-fix one-liner on the phased copy counts only 0|1: S1 n=80 vs 162, S2 0.457 vs 0.473, S7 0.425 vs 0.419; the independent parse (0/1, 0|1, 1|0) reproduces the unphased values exactly. S7 is still the lowest sample, so the contamination call survives here, but half the hets are silently ignored.

**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100 · **Assertions 3/4**
- [PASS] One-liner runs as written — exit 0
- [PASS] Output is per sample — 8 lines
- [FAIL] All het genotypes are counted on phased input — 1|0 not matched; n halved per sample
- [PASS] Contaminated sample still identifiable — SYN_S7 lowest (0.425)

### Input 7 — Variant A: NEW: PASS counts on raw vs soft-filtered callsets
**Prompt:** "How many variants passed filters in our raw joint callset (FILTER is '.' everywhere) and in the soft-filtered copy with LowQual labels? Give me the number from bcftools and from your Python script, and tell me why they differ if they do."

**Executed:** yes — runs/in7/run.sh (Windows bcftools 1.24) and run_wsl.sh (fork copy of vcf_stats.py, cyvcf2 0.34.0).

Code `runs/in7/run.sh`:
```bash
#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Variant C): "How many variants passed filters in our raw joint callset (FILTER is '.'
# everywhere) and in the soft-filtered copy with LowQual labels? Give me the number from bcftools and from your Python script,
# and tell me why they differ if they do." Windows bcftools 1.24 part; the example (cyvcf2) runs in WSL: run_wsl.sh.
set -uo pipefail
source ../env.sh
S=../../data
bgzip -c $S/cohort.vcf > cohort.vcf.gz; bcftools index -f cohort.vcf.gz
bcftools filter -s LowQual -e 'QUAL<30' cohort.vcf.gz -Oz -o marked.vcf.gz; bcftools index -f marked.vcf.gz
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-statistics/examples/vcf_stats.py > vcf_stats.fork_copy.py
for f in cohort marked; do
  echo "== $f: FILTER values $(bcftools query -f '%FILTER\n' $f.vcf.gz | tr -d '\r' | sort | uniq -c | tr '\n' ' ')"
  echo "SKILL.md quick count 'bcftools view -f PASS -H | wc -l': $(bcftools view -f PASS -H $f.vcf.gz | wc -l)"
  echo "bcftools view -f .,PASS -H | wc -l: $(bcftools view -f .,PASS -H $f.vcf.gz | wc -l)"
done
grep -n "PASS\|FILTER" vcf_stats.fork_copy.py | head -8
```

Code `runs/in7/run_wsl.sh`:
```bash
#!/bin/bash
# WSL part of input 7: shipped examples/vcf_stats.py (fork commit copy) with cyvcf2 0.34.0 on the raw and soft-filtered files.
set -uo pipefail
cd "$(dirname "$0")"
export PATH=/tmp/vaca/env/bin:$PATH
for f in cohort marked; do
  echo "== examples/vcf_stats.py $f.vcf.gz =="; python vcf_stats.fork_copy.py $f.vcf.gz | grep -E "Total|PASS|Filtered"; echo "exit=${PIPESTATUS[0]}"
done
```

Printed `runs/in7/out.txt`:
```
== cohort: FILTER values     361 . 
SKILL.md quick count 'bcftools view -f PASS -H | wc -l': 0
bcftools view -f .,PASS -H | wc -l: 361
== marked: FILTER values      11 LowQual     350 PASS 
SKILL.md quick count 'bcftools view -f PASS -H | wc -l': 350
bcftools view -f .,PASS -H | wc -l: 350
35:        if variant.FILTER is None:
54:    print(f'PASS variants:     {stats["pass"]}')
```

Printed `runs/in7/out_wsl.txt`:
```
== examples/vcf_stats.py cohort.vcf.gz ==
Total variants:    361
PASS variants:     361
Filtered:          0
exit=0
== examples/vcf_stats.py marked.vcf.gz ==
Total variants:    361
PASS variants:     350
Filtered:          11
exit=0
rc=0
```

**Output (agent answer, Mode A):** Raw callset (FILTER '.' on all 361): SKILL.md 'bcftools view -f PASS' count = 0, 'view -f .,PASS' = 361, vcf_stats.py 'PASS variants' = 361. Soft-filtered copy: all three agree (350 PASS, 11 LowQual). The Skill gives both idioms without saying they treat '.' differently.

**Scores:** Basic 33/40 | Specialized 47/60 | Total 80/100 · **Assertions 3/4**
- [PASS] PASS count correct on a soft-filtered callset — 350 from bcftools and the example
- [PASS] Shipped example runs on both files — exit 0
- [FAIL] bcftools quick count and the example agree on an unfiltered callset — 0 vs 361; FILTER '.' unexplained
- [PASS] FILTER label counts idiom works — 11 LowQual / 350 PASS

## Key strengths
- Every metric is tied to a mechanism and an action; the excess-het-only HWE rule and 'novel common = artifact' were borne out on planted truth
- The fixed het allele-balance check now reports valid per-sample means that identify the contaminated sample
- Identity QC is accurate and runnable: gtcheck, vcftools --relatedness2 and somalier all found the planted duplicate

## Recommendations
- **[P2] Het allele-balance one-liner ignores 1|0 genotypes** (inputs [6]) — The awk test matches 0/1 and 0|1 only, so on a phased VCF every 1|0 het is dropped (per-sample n halved, means shifted). *Root cause:* Phased genotype orientations were not enumerated. *Fix:* Match `$2 ~ /^(0[\/|]1|1\|0)$/` (or normalise with `gsub(/\|/,"/")` and accept 0/1 and 1/0).
- **[P2] Quick PASS count treats FILTER '.' as not passing** (inputs [7]) — `bcftools view -f PASS` counts 0 on an unfiltered callset (FILTER '.'), while examples/vcf_stats.py counts those records as PASS (361). *Root cause:* The two idioms differ on missing FILTER and the Skill does not say so. *Fix:* Use `bcftools view -f .,PASS` for 'not failed', or state that '.' means unfiltered and is excluded by `-f PASS`.
- **[P2] State the site-panel needs of peddy and somalier** (inputs [2]) — peddy fails on non-human or small targets; somalier needs a build-matched sites file. *Root cause:* Tool requirements not stated (left unfixed in this round). *Fix:* Note the bundled human site panels, the chrX requirement and `somalier find-sites` for custom targets.

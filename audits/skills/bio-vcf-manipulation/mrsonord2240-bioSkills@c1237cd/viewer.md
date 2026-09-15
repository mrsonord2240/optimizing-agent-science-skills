> **Audit record for `bio-vcf-manipulation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/variant-calling/vcf-manipulation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-vcf-manipulation
Generated: 2026-09-15 · Re-audit of the fixed Skill · Auditor: variant-annotation-curation-analyst round-2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/vcf-manipulation`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 7 (5 regression inputs from the pre-fix audit + 2 new).

**Pre-fix → post-fix:** 88 (Limited Release) → **90 (Production Ready)**. Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260915/bio-vcf-manipulation/`; fix log (not evidence): `F:/OpenScience/specialist-src/round2/fixes/bio-vcf-manipulation.md`.

Environment and data: Re-audit of the fixed Skill (fork commit c1237cdb). Mode A. Windows bcftools 1.24 (MSYS2); WSL bcftools 1.21 for input 3. Data SYNTHETIC (data/make_data.py, seed 20260911; input 6 SV VCFs and input 7 batches built in their run scripts). The 5 pre-fix inputs were re-run from runs/p_in1..p_in5 (example taken from the fork commit; input 2 extended with the post-fix sample-reorder advice and a second check in p_in2/check_reorder.sh); inputs 6 and 7 are new. n_inputs 7 = 5 regression + 2 new. Inputs executed: 7/7.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 89/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | merge/concat/isec selection, the single-sample merge 0/0 trap and the normalize-first rule verified. The P1 is fixed: `annotate --rename-chrs` is now the record-renaming step and the merged batches equal the joint callset. The -R duplication claim is correctly qualified (1.24 emits no duplicates). New wording partly wrong: reordering samples with `bcftools view -s` before `concat --naive` still fails, because view -s adds INFO/AC and INFO/AN header lines (with or without -I). |
| Reliability | 10/12 | Common Errors messages match bcftools output; the naive-reorder row gives a fix that does not work for --naive. |
| Performance context | 7/8 | 180-line SKILL.md. |
| Agent usability | 15/16 | Excellent 'choose by what differs' table and SV routing. |
| Human usability | 7/8 | Natural prompts. |
| Security | 11/12 | Local files only. |
| Maintainability | 10/12 | Example runs; no test data. |
| Agent specific | 18/20 | Good routing to normalization, joint-calling and SV tools. |

Shipped-means-present (gate 8): SKILL.md and usage-guide.md name no local references/, scripts/ or assets/ files (a grep hit on 'transcripts/gene' or a URL path is prose, not a file); usage-guide.md and the examples/ file exist at the fork commit. PASS.

Research scope (gate 7): File manipulation; no individual-level content. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 2 | Variant A | 36 | 52 | 88 | 3/4 | yes | ✅ |
| 3 | Edge | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 4 | Variant B | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 5 | Stress | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 6 | Scope Boundary | 37 | 53 | 90 | 4/4 | yes | ✅ |
| 7 | Edge | 38 | 54 | 92 | 4/4 | yes | ✅ |

**Execution Average: 90.7 / 100** · **Assertion Pass Rate: 27/28 (96 %)** · Layer 1 avg 37.1 · Layer 2 avg 53.6

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 89 × 0.4 + 90.7 × 0.6 = 35.6 + 54.4 = 90 → ⭐ Production Ready**

## Detailed Outputs

### Input 1 — Canonical: Merge single-sample VCFs; -0 request (regression)
**Prompt:** "I have single-sample VCFs for four samples from our per-sample pipeline. Merge them into a cohort VCF; my colleague says add -0 so we don't get missing genotypes."

**Executed:** yes — runs/p_in1/run.sh (Windows bcftools 1.24).

Code `runs/p_in1/run.sh`:
```bash
#!/bin/bash
# Input 1 (canonical): build a cohort from single-sample project VCFs with bcftools merge; ./. vs -0.
# (tr -d '\r' strips the CR that the Windows bcftools build writes on stdout.)
set -uo pipefail
C=../../data/cohort.vcf
rm -f files.txt
bgzip -c $C > joint.vcf.gz; bcftools index -f joint.vcf.gz
# single-sample "project VCFs": each sample's non-ref sites only (what a per-sample caller emits)
for s in SYN_S1 SYN_S2 SYN_S3 SYN_S6; do
  bcftools view -s $s -c 1 joint.vcf.gz -Oz -o $s.vcf.gz; bcftools index -f $s.vcf.gz
  echo "$s.vcf.gz" >> files.txt
done
echo "sites per single-sample file: $(for s in SYN_S1 SYN_S2 SYN_S3 SYN_S6; do bcftools view -H $s.vcf.gz | wc -l; done | tr '\n' ' ')"
bcftools merge -l files.txt -Oz -o merged.vcf.gz; bcftools index -f merged.vcf.gz
bcftools merge -0 -l files.txt -Oz -o merged_m0.vcf.gz; bcftools index -f merged_m0.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S6 -c 1 joint.vcf.gz -Oz -o truth4.vcf.gz; bcftools index -f truth4.vcf.gz
for f in truth4 merged merged_m0; do
  bcftools query -f '[%GT\t]\n' $f.vcf.gz | tr -d '\r' > $f.gt
  echo "$f: sites=$(bcftools view -H $f.vcf.gz | wc -l) missing_GT=$(grep -o '\./\.' $f.gt | wc -l) hom_ref=$(grep -o '0/0' $f.gt | wc -l)"
done
echo "== genotype concordance vs the joint call (4 samples) =="
bcftools query -f '%CHROM:%POS[\t%GT]\n' truth4.vcf.gz | tr -d '\r' | sort > t.txt
for f in merged merged_m0; do
  bcftools query -f '%CHROM:%POS[\t%GT]\n' $f.vcf.gz | tr -d '\r' | sort > m.txt
  join t.txt m.txt | awk -v f=$f '{for(i=2;i<=5;i++){n++; if($i==$(i+4)) ok++; else if($(i+4)=="0/0" && $i=="./.") fab++; else if($(i+4)=="0/0") oth++; else if($(i+4)=="./.") mis++}} END{print f": concordant "ok"/"n", 0/0 fabricated where t...
done
echo "== AF of the 4 samples: joint call vs -0 merge (sites where they differ) =="
for f in truth4 merged_m0 merged; do bcftools +fill-tags $f.vcf.gz -- -t AF 2>/dev/null | bcftools query -f '%CHROM:%POS\t%INFO/AF\n' | tr -d '\r' | sort > $f.af; done
join truth4.af merged_m0.af | awk '$2!=$3{d++} END{print "sites with different AF (joint vs -0):", d+0}'
join truth4.af merged.af | awk '$2!=$3{d++; if($3>$2) up++} END{print "sites with different AF (joint vs default ./.):", d+0, " inflated:", up+0}'
```

Printed `runs/p_in1/out.txt`:
```
sites per single-sample file: 197 121 124 84 
truth4: sites=305 missing_GT=62 hom_ref=632
merged: sites=305 missing_GT=694 hom_ref=0
merged_m0: sites=305 missing_GT=0 hom_ref=694
== genotype concordance vs the joint call (4 samples) ==
merged: concordant 588/1220, 0/0 fabricated where truth is ./. 0, ./. placeholders 632
merged_m0: concordant 1158/1220, 0/0 fabricated where truth is ./. 62, ./. placeholders 0
== AF of the 4 samples: joint call vs -0 merge (sites where they differ) ==
sites with different AF (joint vs -0): 62
sites with different AF (joint vs default ./.): 274  inflated: 274
```

**Output (agent answer, Mode A):** Unchanged text; identical results: default merge 632 ./. placeholders, -0 fabricates 62 hom-ref where the joint call is ./.; AF inflated at 274 sites.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 · **Assertions 4/4**
- [PASS] Merge-is-not-joint-genotyping trap demonstrated — 62 fabricated 0/0 with -0
- [PASS] Default ./. behaviour explained as a guess too — AF inflated at 274 sites
- [PASS] Joint genotyping of gVCFs recommended — routes to joint-calling
- [PASS] Merge command runs as written — merge -l files.txt exit 0

### Input 2 — Variant A: Per-chromosome concat, --naive, overlapping windows (regression)
**Prompt:** "Stitch my per-chromosome files into one genome VCF; they're big, can I use --naive? Also combine two overlapping calling windows."

**Executed:** yes — runs/p_in2/run.sh (Windows bcftools 1.24) plus check_reorder.sh for the post-fix advice.

Code `runs/p_in2/run.sh`:
```bash
#!/bin/bash
# Input 2: stitch per-chromosome files (same samples) with concat; --naive; overlapping windows with -a -d.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
for c in chr1 chr2; do bcftools view -r $c joint.vcf.gz -Ob -o $c.bcf; bcftools index -f $c.bcf; bcftools view -r $c joint.vcf.gz -Oz -o $c.vcf.gz; bcftools index -f $c.vcf.gz; done
bcftools concat chr1.vcf.gz chr2.vcf.gz -Oz -o genome.vcf.gz 2>/dev/null
echo "concat == original records: $(bcftools view -H genome.vcf.gz | md5sum | cut -c1-8) vs $(bcftools view -H joint.vcf.gz | md5sum | cut -c1-8)"
bcftools concat --naive chr1.bcf chr2.bcf -Ob -o naive.bcf; echo "naive exit=$?  records=$(bcftools view -H naive.bcf | wc -l)"
echo "== --naive with a different sample order =="
bcftools view -s SYN_S2,SYN_S1,SYN_S3,SYN_S4,SYN_S5,SYN_S6,SYN_S7,SYN_S8 chr2.bcf -Ob -o chr2_reordered.bcf
bcftools concat --naive chr1.bcf chr2_reordered.bcf -Ob -o naive_bad.bcf 2>&1 | tail -2; echo "exit=${PIPESTATUS[0]}"
echo "== plain concat with a different sample order =="
bcftools concat chr1.bcf chr2_reordered.bcf -Ob -o plain_reorder.bcf 2>&1 | tail -1; echo "exit=${PIPESTATUS[0]}"
echo "== overlapping windows (same samples): chr1:1-12000 and chr1:10001-20000 =="
bcftools view -r chr1:1-12000 joint.vcf.gz -Oz -o w1.vcf.gz; bcftools view -r chr1:10001-20000 joint.vcf.gz -Oz -o w2.vcf.gz; bcftools index -f w1.vcf.gz; bcftools index -f w2.vcf.gz
echo "chr1 truth=$(bcftools view -H -r chr1 joint.vcf.gz | wc -l)"
bcftools concat w1.vcf.gz w2.vcf.gz -Oz -o nov.vcf.gz 2>&1 | tail -1; echo "no -a: exit=${PIPESTATUS[0]} records=$(bcftools view -H nov.vcf.gz 2>/dev/null | wc -l)"
bcftools concat -a -d exact w1.vcf.gz w2.vcf.gz -Oz -o ov.vcf.gz; echo "-a -d exact: records=$(bcftools view -H ov.vcf.gz | wc -l)"
echo "== concat given DIFFERENT samples (the inverted-operation error) =="
bcftools view -s SYN_S1 chr1.vcf.gz -Oz -o s1.vcf.gz; bcftools view -s SYN_S2 chr1.vcf.gz -Oz -o s2.vcf.gz
bcftools concat s1.vcf.gz s2.vcf.gz -Oz -o wrong.vcf.gz 2>&1 | tail -1
echo "== post-fix Common Errors advice: reorder samples with bcftools view -s <order> first, then --naive =="
bcftools view -s $(bcftools query -l chr1.bcf | tr -d '\r' | paste -sd,) chr2_reordered.bcf -Ob -o chr2_fixed.bcf; bcftools index -f chr2_fixed.bcf
bcftools concat --naive chr1.bcf chr2_fixed.bcf -Ob -o naive_fixed.bcf; echo "naive after reorder exit=$? records=$(bcftools view -H naive_fixed.bcf | wc -l) md5 $(bcftools view -H naive_fixed.bcf | md5sum | cut -c1-8) vs joint $(bcftools v...
```

Code `runs/p_in2/check_reorder.sh`:
```bash
#!/bin/bash
# Second-method check of the post-fix advice "reorder samples with bcftools view -s <order> first" before --naive.
set -uo pipefail
O=$(bcftools query -l chr1.bcf | tr -d '\r' | paste -sd,)
echo "header INFO lines chr1.bcf: $(bcftools view -h chr1.bcf | grep -c '^##INFO')  chr2_fixed.bcf (view -s): $(bcftools view -h chr2_fixed.bcf | grep -c '^##INFO')"
bcftools view -h chr2_fixed.bcf | grep -E 'ID=(AC|AN),' | tr -d '\r'
bcftools view -I -s $O chr2_reordered.bcf -Ob -o chr2_fixedI.bcf
bcftools concat --naive chr1.bcf chr2_fixedI.bcf -Ob -o naive_I.bcf 2>&1 | tail -1; echo "view -I -s then --naive: exit=${PIPESTATUS[0]} md5 $(bcftools view -H naive_I.bcf 2>/dev/null | md5sum | cut -c1-8) vs joint $(bcftools view -H joint....
bcftools concat chr1.bcf chr2_fixed.bcf -Ob -o plain_fixed.bcf 2>&1 | tail -1; echo "view -s then plain concat: exit=${PIPESTATUS[0]} records $(bcftools view -H plain_fixed.bcf | wc -l)"
```

Printed `runs/p_in2/out.txt`:
```
concat == original records: 1cbd1513 vs 1cbd1513
Checking the headers of 2 files.
Done, the headers are compatible.
Concatenating chr1.bcf	0.000241 seconds
Concatenating chr2.bcf	0.000127 seconds
naive exit=0  records=361
== --naive with a different sample order ==
Checking the headers of 2 files.
Cannot concatenate, different samples in chr1.bcf vs chr2_reordered.bcf
exit=127
== plain concat with a different sample order ==
Different sample names in chr2_reordered.bcf. Perhaps "bcftools merge" is what you are looking for?
exit=127
== overlapping windows (same samples): chr1:1-12000 and chr1:10001-20000 ==
chr1 truth=172
Concatenating w2.vcf.gz	0.000605 seconds
no -a: exit=0 records=194
Checking the headers and starting positions of 2 files
-a -d exact: records=172
== concat given DIFFERENT samples (the inverted-operation error) ==
Different sample names in s2.vcf.gz. Perhaps "bcftools merge" is what you are looking for?
== post-fix Common Errors advice: reorder samples with bcftools view -s <order> first, then --naive ==
Checking the headers of 2 files.
Cannot use --naive, incompatible headers, the tag INFO/AC not present in chr1.bcf
[E::hts_open_format] Failed to open file "naive_fixed.bcf" : No such file or directory
Failed to read from naive_fixed.bcf: No such file or directory
[E::hts_open_format] Failed to open file "naive_fixed.bcf" : No such file or directory
Failed to read from naive_fixed.bcf: No such file or directory
naive after reorder exit=127 records=0 md5 d41d8cd9 vs joint 1cbd1513
```

Printed `runs/p_in2/check_reorder.out`:
```
header INFO lines chr1.bcf: 8  chr2_fixed.bcf (view -s): 10
##INFO=<ID=AC,Number=A,Type=Integer,Description="Allele count in genotypes">
##INFO=<ID=AN,Number=1,Type=Integer,Description="Total number of alleles in called genotypes">
Cannot use --naive, incompatible headers, the tag INFO/AC not present in chr1.bcf
view -I -s then --naive: exit=127 md5 d41d8cd9 vs joint 1cbd1513
Concatenating chr2_fixed.bcf	0.001855 seconds
view -s then plain concat: exit=0 records 361
```

**Output (agent answer, Mode A):** concat reproduces the original; --naive refuses a different sample order; -a -d exact gives 172 = truth. Post-fix advice 'reorder samples with bcftools view -s <order> first' then --naive: 'Cannot use --naive, incompatible headers, the tag INFO/AC not present in chr1.bcf' (view -s added AC/AN header lines; view -I -s the same). Plain concat after the reorder works (361 records).

**Scores:** Basic 36/40 | Specialized 52/60 | Total 88/100 · **Assertions 3/4**
- [PASS] concat reproduces the original records — md5 equal
- [PASS] --naive refuses a different sample order — 'Cannot concatenate, different samples'
- [PASS] Overlapping windows handled with -a -d — 172 = truth
- [FAIL] Post-fix reorder advice makes --naive succeed — view -s adds INFO/AC,AN headers; --naive refuses

### Input 3 — Edge: Three-caller set operations (regression)
**Prompt:** "Compare calls from three callers: what is supported by at least two, what is in all three, and what is unique to caller A?"

**Executed:** yes — runs/p_in3/run.sh in WSL (bcftools 1.21); example from the fork commit.

Code `runs/p_in3/run.sh`:
```bash
#!/bin/bash
# Input 3: three-caller set operations; normalize first (SKILL.md), -n+2 -w1, -C, shipped compare_vcfs.sh.
set -uo pipefail
F=../../data/ref.fa
bgzip -c ../../data/callerA.vcf > A.vcf.gz; bgzip -c ../../data/callerB.vcf | bcftools view -e 'POS==4000' -Oz -o B.vcf.gz
# caller C: A minus the frameshift, plus one private SNV, written right-shifted for the homopolymer deletion
bcftools view -e 'POS==1420 || POS==500' A.vcf.gz -Oz -o C0.vcf.gz
( bcftools view -h C0.vcf.gz; bcftools view -H C0.vcf.gz; printf 'chr1\t506\t.\tAA\tA\t200\tPASS\tDP=30\tGT:AD:DP:GQ\t0/1:14,12:26:99\n' ) | bcftools sort -Oz -o C.vcf.gz 2>/dev/null
for v in A B C; do bcftools index -f $v.vcf.gz; bcftools norm -m-any -f $F $v.vcf.gz -Oz -o $v.norm.vcf.gz 2>/dev/null; bcftools index -f $v.norm.vcf.gz; done
echo "raw   -n+2 (in >=2 callers): $(bcftools isec -n+2 -w1 A.vcf.gz B.vcf.gz C.vcf.gz 2>/dev/null | grep -vc '^#')"
echo "norm  -n+2 (in >=2 callers): $(bcftools isec -n+2 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -vc '^#')"
echo "norm  -n=3 (all three):      $(bcftools isec -n=3 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -vc '^#')"
echo "norm  -C  (A only):";  bcftools isec -C -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -v '^#' | cut -f1-5
echo "norm  -n~100 (A only, mask):"; bcftools isec -n~100 -w1 A.norm.vcf.gz B.norm.vcf.gz C.norm.vcf.gz | grep -v '^#' | cut -f1-5
echo "== shipped examples/compare_vcfs.sh on normalized A vs B =="
bash compare_vcfs.upstream_copy.sh A.norm.vcf.gz B.norm.vcf.gz cmp_out 2>&1 | sed -n '/Comparison Results/,$p'; echo "exit=$?"
```

Printed `runs/p_in3/out.txt`:
```
raw   -n+2 (in >=2 callers): 9
norm  -n+2 (in >=2 callers): 11
norm  -n=3 (all three):      8
norm  -C  (A only):
chr1	1420	.	GA	G
norm  -n~100 (A only, mask):
chr1	1420	.	GA	G
== shipped examples/compare_vcfs.sh on normalized A vs B ==
=== Comparison Results ===
VCF1: A.norm.vcf.gz
VCF2: B.norm.vcf.gz

VCF1 only:  4
VCF2 only:  1
Shared:     8

VCF1 total: 12
VCF2 total: 9

Overlap with VCF1: 66.6%
Overlap with VCF2: 88.8%

Output files in: cmp_out
exit=0
rc=0
```

**Output (agent answer, Mode A):** Unchanged text; identical results: normalized -n+2 11, -n=3 8, A-only 1420 GA>G; compare_vcfs.sh 4/1/8.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100 · **Assertions 4/4**
- [PASS] Normalization before isec changes the answer — raw 9 vs norm 11
- [PASS] -n/-w/-C flags behave as tabulated — n=3 8; -C 1420
- [PASS] Shipped example runs — exit 0
- [PASS] Partition files described correctly — 0000-0003

### Input 4 — Variant B: Subset cases; stale INFO; overlapping -R BED (regression)
**Prompt:** "Extract the four case samples into their own VCF for a burden test; make sure the INFO counts are right. I'll restrict to my target BED, which has overlapping intervals."

**Executed:** yes — runs/p_in4/run.sh (Windows bcftools 1.24).

Code `runs/p_in4/run.sh`:
```bash
#!/bin/bash
# Input 4: subset cases (S1-S4) from a cohort that carries INFO AC/AN/AF; stale tags; -R vs -T with overlapping BED.
set -uo pipefail
bcftools +fill-tags ../../data/cohort.vcf -Oz -o cohort.vcf.gz -- -t AC,AN,AF 2>/dev/null; bcftools index -f cohort.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Oz -o sub_default.vcf.gz
bcftools view -I -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Oz -o sub_noupdate.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 cohort.vcf.gz -Ou | bcftools +fill-tags -Oz -o sub_filltags.vcf.gz -- -t AC,AN,AF
for f in sub_default sub_noupdate sub_filltags; do
  bcftools query -f '%AC\t%AN\t%AF[\t%GT]\n' $f.vcf.gz | tr -d '\r' | awk -v f=$f '{ac=0;an=0; for(i=4;i<=NF;i++){split($i,g,"/"); for(j in g){if(g[j]!="."){an++; if(g[j]=="1") ac++}}} af=(an?ac/an:0); if($1!=ac) bad_ac++; if($2!=an) bad_an...
done
echo "== -R with overlapping BED regions vs -T =="
printf 'chr1\t5000\t9000\nchr1\t8000\t12000\n' > overlap.bed
echo "unique records in chr1:5001-12000: $(bcftools view -H -r chr1:5001-12000 cohort.vcf.gz | wc -l)"
echo "-R overlap.bed: $(bcftools view -H -R overlap.bed cohort.vcf.gz | wc -l) (distinct: $(bcftools view -H -R overlap.bed cohort.vcf.gz | cut -f1-5 | sort -u | wc -l))"
echo "-T overlap.bed: $(bcftools view -H -T overlap.bed cohort.vcf.gz | wc -l)"
```

Printed `runs/p_in4/out.txt`:
```
sub_default: records 361, AC wrong 0, AN wrong 0, AF wrong 277
sub_noupdate: records 361, AC wrong 233, AN wrong 361, AF wrong 277
sub_filltags: records 361, AC wrong 0, AN wrong 0, AF wrong 0
== -R with overlapping BED regions vs -T ==
unique records in chr1:5001-12000: 80
-R overlap.bed: 80 (distinct: 80)
-T overlap.bed: 80
```

**Output (agent answer, Mode A):** view -s updates AC/AN but AF wrong at 277 sites; +fill-tags fixes all. -R overlap.bed gives 80 = distinct 80 = -T, which the post-fix text now states for 1.21/1.24.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] AC/AN update behaviour described correctly — default updates, -I does not
- [PASS] +fill-tags recommended and correct — 0 wrong
- [PASS] -R vs -T difference explained — index jump vs stream
- [PASS] -R overlapping-region statement matches the installed bcftools — no duplicates on 1.24, as stated

### Input 5 — Stress: Merge batches with 1-vs-chr1 naming, name clash, unsorted file (regression)
**Prompt:** "Merge batch1 and batch2. Batch2 came from another centre (1/2 instead of chr1/chr2, and a sample label that clashes). A third file is unsorted. Get me one clean cohort."

**Executed:** yes — runs/p_in5/run.sh (Windows bcftools 1.24).

Code `runs/p_in5/run.sh`:
```bash
#!/bin/bash
# Input 5 (stress): two batches to merge - batch2 uses Ensembl contig names (1,2) and reuses a sample name;
# a third file arrives unsorted. Follow SKILL.md: harmonize names/contigs with reheader, then merge; sort.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
bcftools view -s SYN_S1,SYN_S2,SYN_S3,SYN_S4 joint.vcf.gz -Oz -o batch1.vcf.gz; bcftools index -f batch1.vcf.gz
# batch2: samples S5..S8 renamed so one collides (SYN_S5 -> SYN_S1), contigs renamed chr1->1, chr2->2
printf 'chr1\t1\nchr2\t2\n' > to_ensembl.txt; printf 'SYN_S5\tSYN_S1\n' > collide.txt
bcftools view -s SYN_S5,SYN_S6,SYN_S7,SYN_S8 joint.vcf.gz | bcftools annotate --rename-chrs to_ensembl.txt | bcftools reheader -s collide.txt | bgzip -c > batch2.vcf.gz; bcftools index -f batch2.vcf.gz
echo "batch2 CHROMs: $(bcftools query -f '%CHROM\n' batch2.vcf.gz | tr -d '\r' | sort -u | tr '\n' ' ') samples: $(bcftools query -l batch2.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "== naive merge =="; bcftools merge batch1.vcf.gz batch2.vcf.gz -Oz -o m0.vcf.gz 2>&1 | tail -1
echo "== SKILL.md fix: reheader -s (names) and reheader -f ref.fa.fai (contigs) =="
printf 'SYN_S1\tSYN_S5\n' > uncollide.txt
bcftools reheader -s uncollide.txt batch2.vcf.gz -o b2_names.vcf.gz; bcftools reheader -f ../../data/ref.fa.fai b2_names.vcf.gz -o b2_fai.vcf.gz 2>&1 | tail -1
echo "after reheader -f: header contigs $(bcftools view -h b2_fai.vcf.gz | grep -c '^##contig'), body CHROMs: $(bcftools view -H b2_fai.vcf.gz 2>&1 | cut -f1 | tr -d '\r' | sort -u | head -3 | tr '\n' ' ')"
bcftools index -f b2_fai.vcf.gz 2>&1 | tail -1
bcftools merge batch1.vcf.gz b2_fai.vcf.gz -Oz -o m1.vcf.gz 2>&1 | tail -1; echo "merge after reheader -f: exit=$?"
echo "== what actually renames records: annotate --rename-chrs =="
printf '1\tchr1\n2\tchr2\n' > to_ucsc.txt
bcftools annotate --rename-chrs to_ucsc.txt b2_names.vcf.gz -Oz -o b2_ucsc.vcf.gz; bcftools index -f b2_ucsc.vcf.gz
bcftools merge batch1.vcf.gz b2_ucsc.vcf.gz -Oz -o m2.vcf.gz; bcftools index -f m2.vcf.gz
echo "merged: $(bcftools view -H m2.vcf.gz | wc -l) sites x $(bcftools query -l m2.vcf.gz | wc -l) samples; equals joint: $(bcftools view -H m2.vcf.gz | cut -f1-5 | md5sum | cut -c1-8) vs $(bcftools view -H joint.vcf.gz | cut -f1-5 | md5sum...
echo "== --force-samples on the collision =="
bcftools merge --force-samples batch1.vcf.gz b2_ucsc.vcf.gz -Oz -o m3.vcf.gz 2>&1 | tail -1; bcftools query -l m3.vcf.gz | tr -d '\r' | tr '\n' ' '; echo
echo "== unsorted third file -> sort -> index =="
( bcftools view -h joint.vcf.gz; bcftools view -H joint.vcf.gz | shuf --random-source=<(yes) ) > unsorted.vcf
bgzip -c unsorted.vcf > unsorted.vcf.gz; bcftools index unsorted.vcf.gz 2>&1 | tail -1
bcftools sort -T ./tmp -m 100M unsorted.vcf.gz -Oz -o sorted.vcf.gz 2>&1 | tail -1; bcftools index -f sorted.vcf.gz && echo "sorted+indexed records: $(bcftools view -H sorted.vcf.gz | wc -l)"
```

Printed `runs/p_in5/out.txt`:
```
batch2 CHROMs: 1 2  samples: SYN_S1 SYN_S6 SYN_S7 SYN_S8 
== naive merge ==
Error: Duplicate sample names (SYN_S1), use --force-samples to proceed anyway.
== SKILL.md fix: reheader -s (names) and reheader -f ref.fa.fai (contigs) ==
after reheader -f: header contigs 2, body CHROMs: 1 2 [W::vcf_parse] Contig '1' is not defined in the header. (Quick workaround: index the file with tabix.) 
merge after reheader -f: exit=0
== what actually renames records: annotate --rename-chrs ==
merged: 361 sites x 8 samples; equals joint: a2805164 vs a2805164
== --force-samples on the collision ==
SYN_S1 SYN_S2 SYN_S3 SYN_S4 SYN_S5 SYN_S6 SYN_S7 SYN_S8 
== unsorted third file -> sort -> index ==
index: failed to create index for "unsorted.vcf.gz"
Cleaning
sorted+indexed records: 361
```

**Output (agent answer, Mode A):** Duplicate sample name aborts merge; reheader -f alone leaves records as 1/2 (the post-fix text now says so); annotate --rename-chrs then merge gives 361 sites x 8 samples, identical to the joint callset; unsorted file sorts and indexes.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Sample-name clash handled with reheader -s or --force-samples — both work
- [PASS] Skill's contig fix yields a correct merged cohort — annotate --rename-chrs: equals joint
- [PASS] Skill warns that reheader -f does not rename records — post-fix merge section and Common Errors row
- [PASS] Unsorted file sorted and indexed — 361 records

### Input 6 — Scope Boundary: NEW: merge Manta and Delly SV calls with bcftools
**Prompt:** "Merge the Manta and Delly SV calls for our sample with bcftools merge and give me the consensus deletions."

**Executed:** yes — runs/in6/run.sh (Windows bcftools 1.24) on SYNTHETIC SV VCFs.

Code `runs/in6/run.sh`:
```bash
#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Scope Boundary): "Merge the Manta and Delly SV calls for our sample with bcftools merge
# and give me the consensus deletions." SYNTHETIC SV VCFs: the same two deletions with breakpoints 20-40 bp apart.
set -uo pipefail
H='##fileformat=VCFv4.2\n##contig=<ID=chr1,length=20000>\n##ALT=<ID=DEL,Description="Deletion">\n##INFO=<ID=SVTYPE,Number=1,Type=String,Description="t">\n##INFO=<ID=END,Number=1,Type=Integer,Description="e">\n##INFO=<ID=SVLEN,Number=.,Type=...
printf "$H"'chr1\t5000\tmanta1\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=6200;SVLEN=-1200\tGT\t0/1\nchr1\t12000\tmanta2\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=12800;SVLEN=-800\tGT\t1/1\n' | bgzip -c > manta.vcf.gz
printf "$H"'chr1\t5021\tdelly1\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=6235;SVLEN=-1214\tGT\t0/1\nchr1\t12000\tdelly2\tN\t<DEL>\t50\tPASS\tSVTYPE=DEL;END=12810;SVLEN=-810\tGT\t1/1\n' | sed 's/SYN_SV1/SYN_SV1_delly/' | bgzip -c > delly.vcf.gz
for f in manta delly; do bcftools index -f $f.vcf.gz; done
echo "== bcftools merge (what was asked) =="
bcftools merge manta.vcf.gz delly.vcf.gz | bcftools query -f '%POS\t%ID\t%INFO/END\t[%GT ]\n' | tr -d '\r'
echo "== bcftools isec -n=2 (tuple-exact shared) =="
bcftools isec -n=2 -w1 manta.vcf.gz delly.vcf.gz | grep -vc '^#'
echo "(truth: both deletions are the same events; reciprocal overlap > 0.97 for both pairs)"
```

Printed `runs/in6/out.txt`:
```
== bcftools merge (what was asked) ==
5000	manta1	6200	0/1 ./. 
5021	delly1	6235	./. 0/1 
12000	manta2	12800	1/1 ./. 
12000	delly2	12810	./. 1/1 
== bcftools isec -n=2 (tuple-exact shared) ==
0
(truth: both deletions are the same events; reciprocal overlap > 0.97 for both pairs)
```

**Output (agent answer, Mode A):** bcftools merge keeps the two callers' calls of the same deletions as 4 separate records; isec -n=2 finds 0 shared although reciprocal overlap exceeds 0.97. Declined to report a bcftools consensus and routed to Truvari/SURVIVOR/Jasmine via structural-variant-calling, as the Skill says.

**Scores:** Basic 37/40 | Specialized 53/60 | Total 90/100 · **Assertions 4/4**
- [PASS] Scope: declines bcftools merge for SV consensus — SV section applied
- [PASS] Tuple-exact failure demonstrated — 4 records, 0 shared
- [PASS] Appropriate SV tools named — Truvari, SURVIVOR, Jasmine
- [PASS] No consensus call set fabricated — none reported

### Input 7 — Edge: NEW: same sample label for different people
**Prompt:** "Two centres both used the label SYN_S1 for DIFFERENT people. Rename batch2's sample before merging so genotypes are not mixed, and confirm the merged file keeps both people."

**Executed:** yes — runs/in7/run.sh (Windows bcftools 1.24).

Code `runs/in7/run.sh`:
```bash
#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Edge): "Two centres both used the label SYN_S1 for DIFFERENT people. Rename batch2's
# sample before merging so genotypes are not mixed, and confirm the merged file keeps both people." SYNTHETIC data.
set -uo pipefail
bgzip -c ../../data/cohort.vcf > joint.vcf.gz; bcftools index -f joint.vcf.gz
bcftools view -s SYN_S1,SYN_S2 joint.vcf.gz -Oz -o b1.vcf.gz; bcftools index -f b1.vcf.gz
printf 'SYN_S7\tSYN_S1\n' > clash.txt
bcftools view -s SYN_S7 joint.vcf.gz | bcftools reheader -s clash.txt | bgzip -c > b2.vcf.gz; bcftools index -f b2.vcf.gz
echo "== merge as is =="; bcftools merge b1.vcf.gz b2.vcf.gz -Oz -o m_bad.vcf.gz 2>&1 | tail -1
echo "== SKILL.md reheader block (verbatim, names substituted) =="
printf 'SYN_S1\tSYN_S1_centreB\n' > rename.txt
bcftools reheader -s rename.txt b2.vcf.gz -o renamed.vcf.gz; echo "reheader exit=$?"; bcftools index -f renamed.vcf.gz
bcftools merge b1.vcf.gz renamed.vcf.gz -Oz -o m.vcf.gz; bcftools index -f m.vcf.gz
echo "samples: $(bcftools query -l m.vcf.gz | tr -d '\r' | tr '\n' ' ')"
echo "centreB genotypes identical to original SYN_S7: $(bcftools query -s SYN_S1_centreB -f '[%GT]\n' m.vcf.gz | tr -d '\r' | grep -v '^\./\.$' | md5sum | cut -c1-8) vs $(bcftools query -s SYN_S7 -f '%CHROM:%POS[%GT]\n' joint.vcf.gz -i 'GT!...
echo "== --force-samples alternative =="
bcftools merge --force-samples b1.vcf.gz b2.vcf.gz -Oz -o mf.vcf.gz 2>&1 | tail -1; echo "samples: $(bcftools query -l mf.vcf.gz | tr -d '\r' | tr '\n' ' ')"
```

Printed `runs/in7/out.txt`:
```
== merge as is ==
Error: Duplicate sample names (SYN_S1), use --force-samples to proceed anyway.
== SKILL.md reheader block (verbatim, names substituted) ==
reheader exit=0
samples: SYN_S1 SYN_S2 SYN_S1_centreB 
centreB genotypes identical to original SYN_S7: 1a2b3dde vs 1a2b3dde
== --force-samples alternative ==
samples: SYN_S1 SYN_S2 2:SYN_S1
```

**Output (agent answer, Mode A):** Merge aborts on the duplicate name; the SKILL.md reheader -s block renames batch2's SYN_S1 to SYN_S1_centreB; merged file has 3 samples and centre-B genotypes are identical to the source sample (md5 equal). --force-samples instead yields '2:SYN_S1'.

**Scores:** Basic 38/40 | Specialized 54/60 | Total 92/100 · **Assertions 4/4**
- [PASS] reheader -s block runs as written — exit 0
- [PASS] Both individuals kept after merge — SYN_S1, SYN_S2, SYN_S1_centreB
- [PASS] Genotypes not mixed — md5 identical to source
- [PASS] --force-samples naming explained — 2:SYN_S1

## Key strengths
- The merge-is-not-joint-genotyping trap is demonstrated exactly as described (fabricated 0/0 and inflated AF)
- The pre-fix P1 is fixed: record contig renaming with annotate --rename-chrs reproduces the joint callset
- Clear 'choose by what differs' guidance and correct routing of SV merging away from bcftools

## Recommendations
- **[P2] Sample-reorder advice does not make --naive work** (inputs [2]) — `bcftools view -s <order>` adds INFO/AC and INFO/AN header lines, so `concat --naive` then refuses with 'incompatible headers' (also with -I). Plain concat after the reorder works. *Root cause:* The fix was checked against plain concat, not --naive. *Fix:* Say: reorder with view -s, then use plain `bcftools concat` (or re-create every file with the same view -s so headers match) before --naive.

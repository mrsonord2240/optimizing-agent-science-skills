> **Audit record for `bio-variant-normalization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c1237cd](https://github.com/mrsonord2240/bioSkills/tree/c1237cdbc9bb199947696f3909de26a55d259116/variant-calling/variant-normalization) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-15 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-normalization
Generated: 2026-09-15 · Re-audit of the fixed Skill · Auditor: variant-annotation-curation-analyst round-2 · skill-auditor@1.0

Source: `mrsonord2240/bioSkills@c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/variant-normalization`  
Category: Data Analysis · Mode A · Complexity: Moderate → N = 7 (5 regression inputs from the pre-fix audit + 2 new).

**Pre-fix → post-fix:** 86 (Limited Release) → **89 (Production Ready)**. Pre-fix report: `F:/OpenScience/audits/_pre-fix-20260915/bio-variant-normalization/`; fix log (not evidence): `F:/OpenScience/specialist-src/round2/fixes/bio-variant-normalization.md`.

Environment and data: Re-audit of the fixed Skill (fork commit c1237cdb). Mode A. Windows bcftools 1.24 (MSYS2); WSL agents distro: bcftools 1.21, vt, cyvcf2 0.34.0. Data SYNTHETIC (data/make_data.py, seed 20260911; edge_multiallelic*.vcf hand-written; runs/in7/mixed.vcf written for input 7). Only in4/in5 pre-fix scripts were kept, so inputs 1-4 were rebuilt from the pre-fix viewer with the post-fix commands (runs/p_in1..p_in5); inputs 6 and 7 are new (runs/in6, runs/in7). Phase-mode semantics checked against 'bcftools csq' help on 1.24 and 1.21. n_inputs 7 = 5 regression + 2 new. Inputs executed: 7/7.

## Step 1 — Skill Veto
T1 stability PASS (instruction Skill, deterministic tools), T2 contract PASS (frontmatter name/description present), T3 determinism PASS (no stochastic steps without seeds), T4 security PASS (no eval/exec of user strings, no credentials).

## Step 2 — Static score: 88/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 11/12 | Split -> atomize -> left-align now emits no spurious ALT=* records (callerA, callerB, edge file); the single-pass -m-any --atomize claim, the -m-both/-m+both table and --old-rec-tag were verified. One error introduced by the fix: the csq caveat says -p m merges only where phase is known and -p s treats unphased hets as separate haplotypes; bcftools 1.21/1.24 help and runs show m merges all GTs and s skips unphased hets. |
| Reliability | 10/12 | Example REF pre-check stops with a clear count and inspection command; Common Errors gained the atomize-order and unphased-het rows. The 'Before Database Annotation' block still writes a non-BGZF empty file on a REF mismatch and the index error that follows is misleading. |
| Performance context | 7/8 | 298-line SKILL.md; usage guide partly duplicates it. |
| Agent usability | 14/16 | Clear ordering rule with its reason; the wrong -p m/-p s wording is the one misleading sentence. |
| Human usability | 7/8 | Natural trigger phrases. |
| Security | 11/12 | Nothing sensitive. |
| Maintainability | 10/12 | Example no longer hides stderr and runs; no test data ships. |
| Agent specific | 18/20 | Precise trigger and hand-offs to annotation and clinical-interpretation. |

Shipped-means-present (gate 8): SKILL.md and usage-guide.md name no local references/, scripts/ or assets/ files (a grep hit on 'transcripts/gene' or a URL path is prose, not a file); usage-guide.md and the examples/ file exist at the fork commit. PASS.

Research scope (gate 7): Representation and matching only; no individual-level content. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 2 | Variant A | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 4 | Variant B | 37 | 55 | 92 | 4/4 | yes | ✅ |
| 5 | Stress | 35 | 50 | 85 | 3/4 | yes | ✅ |
| 6 | Variant A | 35 | 51 | 86 | 3/4 | yes | ✅ |
| 7 | Edge | 37 | 54 | 91 | 4/4 | yes | ✅ |

**Execution Average: 89.9 / 100** · **Assertion Pass Rate: 26/28 (93 %)** · Layer 1 avg 36.6 · Layer 2 avg 53.3

Research Veto: scientific integrity PASS; practice boundaries PASS; methodological ground PASS; code usability PASS.  
**Final: 88 × 0.4 + 89.9 × 0.6 = 35.2 + 53.9 = 89 → ⭐ Production Ready**

## Detailed Outputs

### Input 1 — Canonical: Normalize GATK and FreeBayes calls and compare (regression)
**Prompt:** "callerA.vcf is from GATK HaplotypeCaller and callerB.vcf from FreeBayes, same sample, both against ref.fa. Normalize them properly so I can compare them, and tell me what is shared and what is private to each caller."

**Executed:** yes — runs/p_in1/run.sh (Windows bcftools 1.24), post-fix 'Full Normalization for Caller Comparison' verbatim.

Code `runs/p_in1/run.sh`:
```bash
#!/bin/bash
# Input 1 (canonical, post-fix regression 2026-09-15; pre-fix commands rebuilt from the viewer): "callerA.vcf is from GATK,
# callerB.vcf from FreeBayes, same sample, both against ref.fa. Normalize them so I can compare them, and tell me what is
# shared and what is private." SKILL.md 'Check for Normalization Issues' + 'Full Normalization for Caller Comparison' (post-fix).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
echo "### $(bcftools --version | head -1)"
for f in callerA callerB; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
echo "== REF check (SKILL.md: -c w) =="
bcftools norm -f $R -c w callerB.vcf.gz 2>&1 > /dev/null | grep -iE "mismatch|REF_MISMATCH" | tr -d '\r'
echo "== Full Normalization for Caller Comparison (post-fix, verbatim; reference.fa -> ref.fa path) =="
for vcf in callerA.vcf.gz callerB.vcf.gz; do
    base=$(basename "$vcf" .vcf.gz)
    bcftools norm -m- "$vcf" | \
        bcftools norm --atomize | \
        bcftools norm -f $R -Oz -o "${base}.norm.vcf.gz"; echo "$base exit=${PIPESTATUS[*]}"
    bcftools index -f "${base}.norm.vcf.gz"
done
echo "== callerB after inspecting the mismatch: same pipeline, -c x on the last step =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o callerB.norm.vcf.gz; echo "exit=${PIPESTATUS[*]}"
bcftools index -f callerB.norm.vcf.gz
for b in callerA callerB; do
  echo "[$b.norm] $(bcftools query -f '%POS %REF>%ALT %GT; ' -s SYN_S1 $b.norm.vcf.gz 2>/dev/null | tr -d '\r')"
  echo "  ALT=* records: $(bcftools view -H -i 'ALT="*"' $b.norm.vcf.gz | wc -l)"
done
rm -rf comparison; bcftools isec -p comparison callerA.norm.vcf.gz callerB.norm.vcf.gz
for k in 0 1 2; do echo "comparison/000$k.vcf ($(grep -vc '^#' comparison/000$k.vcf)): $(grep -v '^#' comparison/000$k.vcf | cut -f2,4,5 | tr -d '\r' | tr '\t\n' ' ;')"; done
rm -rf rawcmp; bcftools isec -p rawcmp callerA.vcf.gz callerB.vcf.gz
echo "RAW isec: private A $(grep -vc '^#' rawcmp/0000.vcf), private B $(grep -vc '^#' rawcmp/0001.vcf), shared $(grep -vc '^#' rawcmp/0002.vcf)"
echo "== idempotence: re-normalize callerA.norm =="
bcftools norm -m- callerA.norm.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -Ov 2>/dev/null | grep -v '^#' | cut -f1-5 > renorm.tsv
bcftools view -H callerA.norm.vcf.gz | cut -f1-5 > norm.tsv
echo "changed records: $(diff norm.tsv renorm.tsv | grep -c '^[<>]')"
```

Printed `runs/p_in1/out.txt`:
```
### bcftools 1.24
== REF check (SKILL.md: -c w) ==
REF_MISMATCH	chr1	4000	T	C
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/0/0/2/0/0/0
== Full Normalization for Caller Comparison (post-fix, verbatim; reference.fa -> ref.fa path) ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	11/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	12/0/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	12/0/0/0/0/0/0
callerA exit=0 0 0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Reference allele mismatch at chr1:4000 .. REF_SEQ:'C' vs VCF:'T'
callerB exit=0 0 127
index: "callerB.norm.vcf.gz" is in a format that cannot be usefully indexed
== callerB after inspecting the mismatch: same pipeline, -c x on the last step ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	11/0/0/2/1/0/0
exit=0 0 0
[callerA.norm] 
  ALT=* records: 0
[callerB.norm] 
  ALT=* records: 0
comparison/0000.vcf (2): 1420 GA G;1466 C T;
comparison/0001.vcf (0): 
comparison/0002.vcf (10): 500 GA G;800 TCA T;1026 G C;1041 C T;1043 A C;1073 T C;1101 G A;1231 C T;2000 A C;2000 A G;
RAW isec: private A 6, private B 4, shared 5
== idempotence: re-normalize callerA.norm ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	12/0/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	12/0/0/0/0/0/0
changed records: 0
```

**Output (agent answer, Mode A):** REF check finds chr1:4000; callerB aborts under default -c e as the Skill says, then -c x. ALT=* records 0 in both normalized files (pre-fix: two A>* rows). isec normalized: private A 2 (1420, 1466), private B 0, shared 10; raw isec 6/4/5. Re-normalizing changes 0 records.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Normalized files contain only real records — 0 ALT=* records
- [PASS] Representation-only discordance disappears — private B 6/4/5 raw -> 2/0/10
- [PASS] REF mismatch surfaced, not silently fixed — -c w lists chr1:4000; -c e aborts
- [PASS] Normalization is idempotent — 0 changed records

### Input 2 — Variant A: Homopolymer deletion 'not in ClinVar' (regression)
**Prompt:** "Our pipeline annotated callerB.vcf against ClinVar and says the homopolymer deletion near chr1:506 is not in ClinVar, so we flagged it as novel. Is that right? Fix the pipeline so database matching works."

**Executed:** yes — runs/p_in2/run.sh (Windows bcftools 1.24), post-fix 'Before Database Annotation' block.

Code `runs/p_in2/run.sh`:
```bash
#!/bin/bash
# Input 2 (Variant A, post-fix regression 2026-09-15; commands rebuilt from the pre-fix viewer): "Our pipeline annotated
# callerB.vcf against ClinVar and says the homopolymer deletion near chr1:506 is not in ClinVar, so we flagged it as novel.
# Is that right? Fix the pipeline so database matching works." SKILL.md 'Before Database Annotation' (post-fix).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
for f in callerB clinvar_syn dbsnp_syn; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
ann() { bcftools annotate -a clinvar_syn.vcf.gz -c INFO/CLNSIG,INFO/CLNREVSTAT $1 -Oz -o t1.vcf.gz && bcftools index -f t1.vcf.gz && \
        bcftools annotate -a dbsnp_syn.vcf.gz -c ID t1.vcf.gz -Oz -o $2 && bcftools index -f $2; }
echo "== RAW =="
ann callerB.vcf.gz raw_ann.vcf.gz
bcftools query -f '%CHROM:%POS %REF>%ALT\t%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' raw_ann.vcf.gz | tr -d '\r'
echo "== SKILL.md 'Before Database Annotation' block, verbatim =="
bcftools norm -m- callerB.vcf.gz | \
    bcftools norm --atomize | \
    bcftools norm -f $R -Oz -o for_annotation.vcf.gz; echo "exit=${PIPESTATUS[*]}"
bcftools index -f for_annotation.vcf.gz; echo "index exit=$?  records written: $(bcftools view -H for_annotation.vcf.gz 2>/dev/null | wc -l) of $(bcftools view -H callerB.vcf.gz | wc -l)"
echo "== same block with the REF mismatch excluded (-c x, after inspecting it) =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o for_annotation.vcf.gz; bcftools index -f for_annotation.vcf.gz
ann for_annotation.vcf.gz norm_ann.vcf.gz
bcftools query -f '%CHROM:%POS %REF>%ALT\t%ID\t%INFO/CLNSIG\t%INFO/CLNREVSTAT\n' norm_ann.vcf.gz | tr -d '\r'
```

Printed `runs/p_in2/out.txt`:
```
== RAW ==
chr1:506 AA>A	.	.	.
chr1:806 ACA>A	.	.	.
chr1:1026 G>C	rs900000003	Uncertain_significance	criteria_provided,_single_submitter
chr1:1041 CTA>TTC	.	.	.
chr1:1073 T>C	.	.	.
chr1:1101 G>A	.	Likely_pathogenic	criteria_provided,_single_submitter
chr1:1231 C>T	rs900000006	Pathogenic	reviewed_by_expert_panel
chr1:2000 A>C,G	rs900000007	Conflicting_classifications_of_pathogenicity	criteria_provided,_conflicting_classifications
chr1:4000 T>G	.	.	.
== SKILL.md 'Before Database Annotation' block, verbatim ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Reference allele mismatch at chr1:4000 .. REF_SEQ:'C' vs VCF:'T'
exit=0 0 127
index: "for_annotation.vcf.gz" is in a format that cannot be usefully indexed
index exit=127  records written: 0 of 9
== same block with the REF mismatch excluded (-c x, after inspecting it) ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	11/0/0/2/1/0/0
chr1:500 GA>G	rs900000001	Pathogenic	criteria_provided,_multiple_submitters,_no_conflicts
chr1:800 TCA>T	rs900000002	Benign	criteria_provided,_multiple_submitters,_no_conflicts
chr1:1026 G>C	rs900000003	Uncertain_significance	criteria_provided,_single_submitter
chr1:1041 C>T	rs900000004	.	.
chr1:1043 A>C	rs900000005	.	.
chr1:1073 T>C	.	.	.
chr1:1101 G>A	.	Likely_pathogenic	criteria_provided,_single_submitter
chr1:1231 C>T	rs900000006	Pathogenic	reviewed_by_expert_panel
chr1:2000 A>G	rs900000007	Conflicting_classifications_of_pathogenicity	criteria_provided,_conflicting_classifications
chr1:2000 A>C	rs900000007	.	.
```

**Output (agent answer, Mode A):** Raw chr1:506 AA>A unmatched; after the post-fix block (with -c x after inspecting the mismatch) it is 500 GA>G rs900000001 Pathogenic (2-star). Verbatim block on the mismatch file: last step exit 127, 0 records written.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] Raw annotation misses the canonical ClinVar record — 506 AA>A unmatched
- [PASS] Normalized annotation finds it — 500 GA>G Pathogenic
- [PASS] Multiallelic conflict assigned to the right ALT — Conflicting on A>G only
- [PASS] Review status carried with the assertion — CLNREVSTAT reported

### Input 3 — Edge: Split with per-ALT INFO and rejoin (regression)
**Prompt:** "Split the multiallelic sites in this VCF so each ALT is its own record. Our in-house INFO/XAF (one value per ALT) and the per-sample AD and PL must stay correct. Can I rejoin later with -m+ and get the original back?"

**Executed:** yes — runs/p_in3/run.sh (Windows bcftools 1.24).

Code `runs/p_in3/run.sh`:
```bash
#!/bin/bash
# Input 3 (Edge, post-fix regression 2026-09-15; commands rebuilt from the pre-fix output): "Split the multiallelic sites so
# each ALT is its own record. Our in-house INFO/XAF (one value per ALT) and per-sample AD and PL must stay correct. Can I
# rejoin later with -m+ and get the original back?" Hand-written SYNTHETIC edge files.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
show() { bcftools query -f '%POS\t%REF\t%ALT\t%INFO/AC;XAF=%INFO/XAF\t[%GT:%AD:%PL\t]\n' "$1" | tr -d '\r'; }
for f in edge_multiallelic edge_multiallelic_fixedhdr; do
  echo "== $f: header XAF $(grep -o 'ID=XAF,Number=[^,]*' $D/$f.vcf) ; bcftools norm -m-any =="
  bcftools norm -m-any $D/$f.vcf -Oz -o $f.split.vcf.gz; bcftools index -f $f.split.vcf.gz; show $f.split.vcf.gz
done
echo "== rejoin (-m+any) of the correctly declared split file =="
bcftools norm -m+any edge_multiallelic_fixedhdr.split.vcf.gz -Oz -o rejoined.vcf.gz; show rejoined.vcf.gz
echo "== original =="; show $D/edge_multiallelic_fixedhdr.vcf
echo "== --keep-sum AD on split =="
bcftools norm -m-any --keep-sum AD $D/edge_multiallelic_fixedhdr.vcf | bcftools query -f '%POS\t%REF\t%ALT\t[%GT:%AD\t]\n' | tr -d '\r'
```

Printed `runs/p_in3/out.txt`:
```
== edge_multiallelic: header XAF ID=XAF,Number=. ; bcftools norm -m-any ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	1/1/0/0/0/0/0
2000	A	C	1;XAF=0.1,0.2	1/0:1,12:400,200,380	0/0:14,0:300,330,700	
2000	A	G	2;XAF=0.1,0.2	0/1:1,13:400,210,390	0/1:14,12:300,0,420	
== edge_multiallelic_fixedhdr: header XAF ID=XAF,Number=A ; bcftools norm -m-any ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	1/1/0/0/0/0/0
2000	A	C	1;XAF=0.1	1/0:1,12:400,200,380	0/0:14,0:300,330,700	
2000	A	G	2;XAF=0.2	0/1:1,13:400,210,390	0/1:14,12:300,0,420	
== rejoin (-m+any) of the correctly declared split file ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	2/0/1/0/0/0/0
2000	A	C,G	1,2;XAF=0.1,0.2	1/2:1,12,13:400,200,380,210,.,390	0/2:14,0,12:300,330,700,0,.,420	
== original ==
2000	A	C,G	1,2;XAF=0.1,0.2	1/2:1,12,13:400,200,380,210,0,390	0/2:14,0,12:300,330,700,0,340,420	
== --keep-sum AD on split ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	1/1/0/0/0/0/0
2000	A	C	1/0:14,12	0/0:26,0	
2000	A	G	0/1:13,13	0/1:14,12
```

**Output (agent answer, Mode A):** Unchanged text; identical results: Number=. XAF carried whole, Number=A subset; -m+any rejoin loses the 1/2 PL; --keep-sum AD works.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100 · **Assertions 4/4**
- [PASS] Number=. trap demonstrated — XAF=0.1,0.2 on both records
- [PASS] Number=A field subset correctly — 0.1 / 0.2
- [PASS] Rejoin limits stated — PL for 1/2 not recoverable
- [PASS] --keep-sum AD behaves as documented — summed ref depth

### Input 4 — Variant B: Reconcile vt and bcftools cohorts; shipped example (regression)
**Prompt:** "Cohort A was normalized with vt (decompose + decompose_blocksub + normalize), cohort B with bcftools norm -m- -f. Comparing them we get extra private variants. Reconcile the representation."

**Executed:** yes — runs/p_in4/run.sh in WSL (vt, bcftools 1.21) and run_win.sh (Windows bcftools 1.24, example from the fork commit).

Code `runs/p_in4/run.sh`:
```bash
#!/bin/bash
# Input 4 (Variant B, post-fix regression 2026-09-15; WSL part rebuilt from the pre-fix output): "Cohort A was normalized with
# vt (decompose + decompose_blocksub + normalize), cohort B with bcftools norm -m- -f. Comparing them we get extra private
# variants. Reconcile the representation." WSL: vt, bcftools 1.21. The REF-mismatch record is excluded first (-c x).
set -uo pipefail
export PATH=/tmp/vaca/env/bin:$PATH
D=../../data; R=$D/ref.fa
bcftools --version | head -1; vt 2>&1 | grep -m1 -i version
bgzip -c $D/callerB.vcf > B.vcf.gz; bcftools index -f B.vcf.gz
bcftools norm -f $R -c x B.vcf.gz -Oz -o clean.vcf.gz 2>/dev/null; bcftools index -f clean.vcf.gz
echo "== cohort A: vt pipeline =="
vt decompose -s clean.vcf.gz -o d1.vcf 2>/dev/null; vt decompose_blocksub d1.vcf -o d2.vcf 2>/dev/null
vt normalize -r $R d2.vcf -o A.vt.vcf 2>&1 | grep -E "total no" ; bgzip -f A.vt.vcf; bcftools index -f A.vt.vcf.gz
echo "== cohort B: bcftools norm -m- -f (no --atomize) =="
bcftools norm -m- -f $R clean.vcf.gz -Oz -o B.bcf.vcf.gz; bcftools index -f B.bcf.vcf.gz
echo "records: vt=$(bcftools view -H A.vt.vcf.gz | wc -l) bcftools=$(bcftools view -H B.bcf.vcf.gz | wc -l)"
rm -rf c1; bcftools isec -p c1 A.vt.vcf.gz B.bcf.vcf.gz
echo "private to vt-cohort: $(grep -v '^#' c1/0000.vcf | cut -f2,4,5 | tr '\t\n' ' ;')"
echo "private to bcftools-cohort: $(grep -v '^#' c1/0001.vcf | cut -f2,4,5 | tr '\t\n' ' ;')"
echo "== reconcile with the post-fix SKILL.md pipeline on both (split -> atomize -> left-align) =="
for x in A.vt B.bcf; do
  bcftools norm -m- $x.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -Oz -o $x.std.vcf.gz; bcftools index -f $x.std.vcf.gz
done
rm -rf c2; bcftools isec -p c2 A.vt.std.vcf.gz B.bcf.std.vcf.gz
echo "after standardizing: private vt=$(grep -vc '^#' c2/0000.vcf) private bcf=$(grep -vc '^#' c2/0001.vcf) shared=$(grep -vc '^#' c2/0002.vcf)"
```

Code `runs/p_in4/run_win.sh`:
```bash
#!/bin/bash
# Input 4, second part (Windows bcftools 1.24): shipped examples/normalize_vcf.sh from the fork commit, verbatim.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
git -C F:/OpenScience/external/mrsonord2240__bioSkills show c1237cdbc9bb199947696f3909de26a55d259116:variant-calling/variant-normalization/examples/normalize_vcf.sh > normalize_vcf.fork_copy.sh
bash -n normalize_vcf.fork_copy.sh && echo "bash -n ok"
for f in callerA callerB; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
bgzip -c $D/edge_multiallelic_fixedhdr.vcf > edge.vcf.gz; bcftools index -f edge.vcf.gz
for f in callerA callerB edge; do
  echo "== example on $f =="
  bash normalize_vcf.fork_copy.sh $D/ref.fa $f.vcf.gz $f.ex.vcf.gz 2>&1 | grep -E "Error|Inspect|Records|Extra"; echo "exit=${PIPESTATUS[0]}"
  [ -f $f.ex.vcf.gz ] && echo "ALT=* in output: $(bcftools view -H -i 'ALT="*"' $f.ex.vcf.gz | wc -l); output: $(bcftools query -f '%POS %REF>%ALT; ' $f.ex.vcf.gz | tr -d '\r')"
done
```

Printed `runs/p_in4/out.txt`:
```
bcftools 1.21
== cohort A: vt pipeline ==
       total no. biallelic normalized           : 0
       total no. multiallelic normalized        : 0
       total no. variants normalized            : 0
       total no. variants observed              : 10
       total no. reference observed             : 0
== cohort B: bcftools norm -m- -f (no --atomize) ==
Lines   total/split/joined/realigned/removed/skipped:	8/1/0/0/0/0
records: vt=10 bcftools=9
private to vt-cohort: 1041 C T;1043 A C;
private to bcftools-cohort: 1041 CTA TTC;
== reconcile with the post-fix SKILL.md pipeline on both (split -> atomize -> left-align) ==
Lines   total/split/joined/realigned/removed/skipped:	10/0/0/0/0/0
Lines   total/split/joined/realigned/removed/skipped:	10/0/0/0/0/0
Lines   total/split/joined/realigned/removed/skipped:	10/0/0/0/0/0
Lines   total/split/joined/realigned/removed/skipped:	9/0/0/0/0/0
Lines   total/split/joined/realigned/removed/skipped:	9/0/0/0/0/0
Lines   total/split/joined/realigned/removed/skipped:	10/0/0/0/0/0
after standardizing: private vt=0 private bcf=0 shared=10
rc=0
```

Printed `runs/p_in4/out_win.txt`:
```
bash -n ok
== example on callerA ==
Records before:                    11
Records after split+left-align:    12
Records after full (with atomize): 12
Extra records from atomization:    0
exit=0
ALT=* in output: 0; output: 500 GA>G; 
800 TCA>T; 
1026 G>C; 
1041 C>T; 
1043 A>C; 
1073 T>C; 
1101 G>A; 
1231 C>T; 
1420 GA>G; 
1466 C>T; 
2000 A>C; 
2000 A>G; 
== example on callerB ==
Error: 1 REF allele(s) do not match ../../data/ref.fa (wrong build or contig naming?).
Inspect with: bcftools norm -f ../../data/ref.fa -c w callerB.vcf.gz -Ou > /dev/null
exit=1
== example on edge ==
Records before:                    1
Records after split+left-align:    2
Records after full (with atomize): 2
Extra records from atomization:    0
exit=0
ALT=* in output: 0; output: 2000 A>C; 
2000 A>G;
```

**Output (agent answer, Mode A):** vt 10 vs bcftools 9 records; private 1041 C>T, 1043 A>C vs 1041 CTA>TTC; after the post-fix pipeline on both: 0/0/10. Example: callerA 12/12, 'Extra records from atomization: 0' (pre-fix: 2 phantom * rows); callerB exits 1 with 'Error: 1 REF allele(s) do not match'; edge file 2 records, no *.

**Scores:** Basic 37/40 | Specialized 55/60 | Total 92/100 · **Assertions 4/4**
- [PASS] vt vs bcftools MNP discordance reproduced — 1041 MNP vs atoms
- [PASS] Post-fix pipeline reconciles both cohorts — 0/0/10
- [PASS] Shipped example diagnoses atomization correctly — 0 extra on an MNP-free file; no * rows
- [PASS] Example reports REF mismatch clearly — count plus inspection command, exit 1

### Input 5 — Stress: Count, matching vs annotation copies, codon, HGVS (regression)
**Prompt:** "(a) How many records in callerB need normalization? (b) Give me a copy for database matching and a copy for functional annotation. (c) Annotate consequences on the right copy and explain the codon at chr1:1041. (d) Our HGVS c. for the CA-repeat deletion does not match VCF POS — bug?"

**Executed:** yes — runs/p_in5/run_csq.sh (Windows bcftools 1.24) and run_wsl.sh (cyvcf2 0.34.0).

Code `runs/p_in5/run_csq.sh`:
```bash
#!/bin/bash
# Input 5 (Stress, post-fix regression 2026-09-15): "(a) how many callerB records need normalization? (b) a copy for database
# matching and a copy for functional annotation. (c) annotate consequences on the right copy, explain the codon at chr1:1041.
# (d) HGVS c. vs VCF POS for the CA-repeat deletion." Windows bcftools 1.24 part (the cyvcf2 part runs in WSL: run_py.sh).
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
bgzip -c $D/callerB.vcf > callerB.vcf.gz; bcftools index -f callerB.vcf.gz
bgzip -c $D/genes.gff3 > genes.gff3.gz
echo "== matching copy: post-fix pipeline (split -> atomize -> left-align), REF mismatch excluded =="
bcftools norm -m- callerB.vcf.gz | bcftools norm --atomize | bcftools norm -f $R -c x -Oz -o match.vcf.gz; bcftools index -f match.vcf.gz
bcftools query -f '%POS %REF>%ALT; ' match.vcf.gz | tr -d '\r'; echo
echo "== annotation copy: split -> left-align, no atomize =="
bcftools norm -m- callerB.vcf.gz | bcftools norm -f $R -c x -Oz -o annot.vcf.gz; bcftools index -f annot.vcf.gz
bcftools query -f '%POS %REF>%ALT; ' annot.vcf.gz | tr -d '\r'; echo
echo "== SKILL.md csq line (post-fix, verbatim; file names substituted) on the annotation copy =="
bcftools csq -p a -f $R -g genes.gff3.gz annot.vcf.gz 2>csq.err | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150; echo "exit=${PIPESTATUS[0]}"; grep -i error csq.err
echo "== same on the atomized matching copy =="
bcftools csq -p a -f $R -g genes.gff3.gz match.vcf.gz 2>/dev/null | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150
echo "== -p s on the atomized copy (Skill: 'treats unphased hets as separate haplotypes') =="
bcftools csq -p s -f $R -g genes.gff3.gz match.vcf.gz 2>/dev/null | bcftools query -i 'POS>=1026 && POS<=1500' -f '%POS %REF>%ALT\t%INFO/BCSQ\n' | tr -d '\r' | cut -c1-150
```

Code `runs/p_in5/norm_check.py`:
```python
# SKILL.md "cyvcf2 Normalization Check" block, verbatim except the input path.
from cyvcf2 import VCF

def needs_normalization(variant):
    if len(variant.ALT) > 1:
        return True
    ref, alt = variant.REF, variant.ALT[0]
    if len(ref) > 1 and len(alt) > 1 and len(ref) == len(alt):
        return True
    return False

total, needs_norm, multiallelic, mnps = 0, 0, 0, 0
for variant in VCF('callerB.vcf.gz'):
    total += 1
    if len(variant.ALT) > 1:
        multiallelic += 1
    ref, alt = variant.REF, variant.ALT[0]
    if len(ref) > 1 and len(alt) > 1 and len(ref) == len(alt):
        mnps += 1
    if needs_normalization(variant):
        needs_norm += 1

print(f'Total variants: {total}')
print(f'Needing normalization: {needs_norm} ({needs_norm/total*100:.1f}%)')
print(f'  Multiallelic sites: {multiallelic}')
print(f'  MNPs: {mnps}')
```

Printed `runs/p_in5/out_csq.txt`:
```
== matching copy: post-fix pipeline (split -> atomize -> left-align), REF mismatch excluded ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	11/0/0/2/1/0/0
500 GA>G; 
800 TCA>T; 
1026 G>C; 
1041 C>T; 
1043 A>C; 
1073 T>C; 
1101 G>A; 
1231 C>T; 
2000 A>C; 
2000 A>G; 

== annotation copy: split -> left-align, no atomize ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/2/1/0/0
500 GA>G; 
800 TCA>T; 
1026 G>C; 
1041 CTA>TTC; 
1073 T>C; 
1101 G>A; 
1231 C>T; 
2000 A>C; 
2000 A>G; 

== SKILL.md csq line (post-fix, verbatim; file names substituted) on the annotation copy ==
1026 G>C	missense|SYNG1|SYNT1|protein_coding|+|6D>6H|1026G>C
1041 CTA>TTC	missense|SYNG1|SYNT1|protein_coding|+|11L>11F|1041CTA>TTC
1073 T>C	synonymous|SYNG1|SYNT1|protein_coding|+|21A|1073T>C
1101 G>A	splice_donor|SYNG1|SYNT1|protein_coding
1231 C>T	stop_gained|SYNG1|SYNT1|protein_coding|+|41Q>41*|1231C>T
exit=0
== same on the atomized matching copy ==
1026 G>C	missense|SYNG1|SYNT1|protein_coding|+|6D>6H|1026G>C
1041 C>T	missense|SYNG1|SYNT1|protein_coding|+|11L>11F|1041C>T+1043A>C
1043 A>C	@1041
1073 T>C	synonymous|SYNG1|SYNT1|protein_coding|+|21A|1073T>C
1101 G>A	splice_donor|SYNG1|SYNT1|protein_coding
1231 C>T	stop_gained|SYNG1|SYNT1|protein_coding|+|41Q>41*|1231C>T
== -p s on the atomized copy (Skill: 'treats unphased hets as separate haplotypes') ==
1026 G>C	.
1041 C>T	.
... (5 more lines in out_csq.txt)
```

Printed `runs/p_in5/out_py.txt`:
```
cyvcf2 0.34.0
Total variants: 9
Needing normalization: 2 (22.2%)
  Multiallelic sites: 1
  MNPs: 1
-- true count of records bcftools changes (reference-aware) --
Lines   total/split/joined/realigned/removed/skipped:	9/1/0/2/1/0
rc=0
```

**Output (agent answer, Mode A):** cyvcf2 block: 9 total, 2 needing normalization (lower bound; bcftools realigns 2 more). csq -p a on the un-atomized copy: 1041 CTA>TTC missense 11L>11F; on the atomized copy the atoms are merged back (@1041). -p s on the atomized copy returned no consequence for every unphased het, contradicting the Skill's 'separate haplotypes' wording.

**Scores:** Basic 35/40 | Specialized 50/60 | Total 85/100 · **Assertions 3/4**
- [PASS] cyvcf2 count presented as a lower bound — 2 vs bcftools realigned 2 more
- [PASS] Matching and annotation copies produced as advised — atomized vs un-atomized
- [PASS] Prescribed csq step runs as described — -p a exit 0; 11L>11F
- [FAIL] Phase-mode description matches bcftools behaviour — -p s skipped unphased hets (help: 'skip unphased hets')

### Input 6 — Variant A: NEW: single-pass norm vs three-step pipeline; REF error
**Prompt:** "Is the single-pass 'bcftools norm -f ref.fa -m-any --atomize' really the same as your three-step pipeline? I'd rather run one command in production. And what happens with the 'Before Database Annotation' block when a REF allele is wrong — do I get a usable file?"

**Executed:** yes — runs/in6/run.sh (Windows bcftools 1.24).

Code `runs/in6/run.sh`:
```bash
#!/bin/bash
# Input 6 (NEW, re-audit 2026-09-15, Variant C): "Is the single-pass 'bcftools norm -f ref.fa -m-any --atomize' really the same
# as your three-step pipeline? I'd rather run one command in production. And what happens with the 'Before Database
# Annotation' block when a REF allele is wrong - do I get a usable file?" Windows bcftools 1.24. SYNTHETIC data.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data; R=$D/ref.fa
for f in callerA callerB edge_multiallelic_fixedhdr; do bgzip -c $D/$f.vcf > $f.vcf.gz; bcftools index -f $f.vcf.gz; done
for f in callerA callerB edge_multiallelic_fixedhdr; do
  bcftools norm -m- $f.vcf.gz 2>/dev/null | bcftools norm --atomize 2>/dev/null | bcftools norm -f $R -c x 2>/dev/null | grep -v '^#' | cut -f1-5,10 > $f.three.tsv
  bcftools norm -f $R -m-any --atomize -c x $f.vcf.gz 2>/dev/null | grep -v '^#' | cut -f1-5,10 > $f.one.tsv
  echo "$f: three-step $(wc -l < $f.three.tsv) records, single-pass $(wc -l < $f.one.tsv) records, differing lines $(diff $f.three.tsv $f.one.tsv | grep -c '^[<>]'), ALT=* single-pass $(awk '$5=="*"' $f.one.tsv | wc -l)"
done
diff callerB.three.tsv callerB.one.tsv | head -6
echo "== 'Before Database Annotation' block verbatim on callerB (one REF mismatch at chr1:4000) =="
bcftools norm -m- callerB.vcf.gz | \
    bcftools norm --atomize | \
    bcftools norm -f $R -Oz -o for_annotation.vcf.gz; echo "pipeline exit=${PIPESTATUS[*]}"
bcftools index for_annotation.vcf.gz; echo "bcftools index exit=$?"
echo "records in for_annotation.vcf.gz: $(bcftools view -H for_annotation.vcf.gz 2>/dev/null | wc -l) (input $(bcftools view -H callerB.vcf.gz | wc -l))"
```

Printed `runs/in6/out.txt`:
```
callerA: three-step 12 records, single-pass 12 records, differing lines 0, ALT=* single-pass 0
callerB: three-step 10 records, single-pass 10 records, differing lines 0, ALT=* single-pass 0
edge_multiallelic_fixedhdr: three-step 2 records, single-pass 2 records, differing lines 0, ALT=* single-pass 0
== 'Before Database Annotation' block verbatim on callerB (one REF mismatch at chr1:4000) ==
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	9/1/0/0/0/0/0
Lines   total/split/joined/realigned/mismatch_removed/dup_removed/skipped:	10/0/0/0/0/0/0
Reference allele mismatch at chr1:4000 .. REF_SEQ:'C' vs VCF:'T'
pipeline exit=0 0 127
index: the file is not BGZF compressed, cannot index: for_annotation.vcf.gz
bcftools index exit=127
records in for_annotation.vcf.gz: 0 (input 9)
```

**Output (agent answer, Mode A):** Single-pass 'norm -f ref -m-any --atomize -c x' equals the three-step pipeline on callerA (12), callerB (10) and the edge file (2): 0 differing lines, 0 ALT=*. The verbatim 'Before Database Annotation' block on callerB reports 'Reference allele mismatch at chr1:4000', then leaves a 0-record non-BGZF for_annotation.vcf.gz; 'bcftools index' fails with 'not BGZF compressed'.

**Scores:** Basic 35/40 | Specialized 51/60 | Total 86/100 · **Assertions 3/4**
- [PASS] Single-pass command equals the three-step pipeline — 0 differing lines on 3 files
- [PASS] Neither form emits spurious ALT=* records — 0
- [PASS] REF mismatch reported with its position — chr1:4000 REF_SEQ C vs VCF T
- [FAIL] Workflow block avoids leaving an unusable output file — 0-record non-BGZF file; misleading index error

### Input 7 — Edge: NEW: -m-both/-m+both for a SNP and indel at one position
**Prompt:** "Our joint caller writes a SNP and an insertion at the same position. Should I split with -m-both or -m-any, and when I rejoin for delivery will -m+both put the SNP and indel back in one record? Also keep a trace of the original MNP when I atomize."

**Executed:** yes — runs/in7/run.sh (Windows bcftools 1.24) on a hand-written SYNTHETIC VCF.

Code `runs/in7/run.sh`:
```bash
#!/bin/bash
# Input 7 (NEW, re-audit 2026-09-15, Edge): "Our joint caller writes a SNP and an insertion at the same position. Should I split
# with -m-both or -m-any, and when I rejoin for delivery will -m+both put the SNP and indel back in one record? Also keep a
# trace of the original MNP when I atomize." Tests the post-fix Split Options table and --old-rec-tag. Windows bcftools 1.24.
set -uo pipefail
E=/f/OpenScience/audit-envs/variant-annotation-curation-analyst
export PATH=$E/msys/mingw64/bin:$PATH
D=../../data
printf '##fileformat=VCFv4.2\n##source=SYNTHETIC_same_position_snp_indel (audit 2026-09-15)\n##contig=<ID=chr1,length=20000>\n##INFO=<ID=AC,Number=A,Type=Integer,Description="AC">\n##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype"...
for m in -m-any -m-both -m-snps -m-indels; do
  echo "split $m: $(bcftools norm $m mixed.vcf 2>/dev/null | bcftools query -f '%POS %REF>%ALT [%GT ]; ' | tr -d '\r')"
done
for m in -m+any -m+both -m+snps -m+indels; do
  echo "join  $m: $(bcftools norm $m mixed.vcf 2>/dev/null | bcftools query -f '%POS %REF>%ALT [%GT ]; ' | tr -d '\r')"
done
echo "== --atomize --old-rec-tag ORIGINAL on callerB's MNP =="
bgzip -c $D/callerB.vcf > B.vcf.gz; bcftools index -f B.vcf.gz
bcftools norm --atomize --old-rec-tag ORIGINAL B.vcf.gz 2>/dev/null | bcftools query -i 'INFO/ORIGINAL!="."' -f '%POS %REF>%ALT ORIGINAL=%INFO/ORIGINAL\n' | tr -d '\r'
```

Printed `runs/in7/out.txt`:
```
split -m-any: 2000 A>C 1/0 0/0 ; 
2000 A>AT 0/1 0/0 ; 
2000 A>G 0/0 0/1 ; 
3000 G>T 0/1 0/0 ; 
3000 G>GA 0/0 0/1 ; 
3000 G>C 0/0 0/1 ; 
split -m-both: 2000 A>C 1/0 0/0 ; 
2000 A>AT 0/1 0/0 ; 
2000 A>G 0/0 0/1 ; 
3000 G>T 0/1 0/0 ; 
3000 G>GA 0/0 0/1 ; 
3000 G>C 0/0 0/1 ; 
split -m-snps: 2000 A>C 1/0 0/0 ; 
2000 A>AT 0/1 0/0 ; 
2000 A>G 0/0 0/1 ; 
3000 G>T 0/1 0/0 ; 
3000 G>GA 0/0 0/1 ; 
3000 G>C 0/0 0/1 ; 
split -m-indels: 2000 A>C 1/0 0/0 ; 
2000 A>AT 0/1 0/0 ; 
2000 A>G 0/0 0/1 ; 
3000 G>T 0/1 0/0 ; 
3000 G>GA 0/0 0/1 ; 
3000 G>C 0/0 0/1 ; 
join  -m+any: 2000 A>C,AT,G 1/2 0/3 ; 
3000 G>T,GA,C 0/1 3/2 ; 
join  -m+both: 2000 A>C,AT,G 1/2 0/3 ; 
3000 G>T,C 0/1 0/2 ; 
3000 G>GA 0/0 0/1 ; 
join  -m+snps: 2000 A>C,AT,G 1/2 0/3 ; 
3000 G>T,C 0/1 0/2 ; 
3000 G>GA 0/0 0/1 ; 
join  -m+indels: 2000 A>C,AT,G 1/2 0/3 ; 
3000 G>T 0/1 0/0 ; 
3000 G>C 0/0 0/1 ; 
3000 G>GA 0/0 0/1 ; 
== --atomize --old-rec-tag ORIGINAL on callerB's MNP ==
506 AA>A ORIGINAL=chr1|506|AA|A|1
806 ACA>A ORIGINAL=chr1|806|ACA|A|1
1026 G>C ORIGINAL=chr1|1026|G|C|1
1041 C>T ORIGINAL=chr1|1041|CTA|TTC|1
1043 A>C ORIGINAL=chr1|1041|CTA|TTC|1
1073 T>C ORIGINAL=chr1|1073|T|C|1
1101 G>A ORIGINAL=chr1|1101|G|A|1
1231 C>T ORIGINAL=chr1|1231|C|T|1
... (4 more lines in out.txt)
```

**Output (agent answer, Mode A):** Split: -m-any, -m-both, -m-snps and -m-indels give identical records for a mixed A>C,AT,G site. Join: -m+any makes G>T,GA,C; -m+both makes G>T,C and a separate G>GA, as the post-fix table says. --old-rec-tag ORIGINAL traces 1041/1043 back to CTA>TTC.

**Scores:** Basic 37/40 | Specialized 54/60 | Total 91/100 · **Assertions 4/4**
- [PASS] -m-both identical to -m-any when splitting — same records
- [PASS] -m+both keeps SNPs and indels in separate records — G>T,C and G>GA
- [PASS] Type string matters only when joining — all split variants identical
- [PASS] --old-rec-tag keeps a trace of the MNP — ORIGINAL=chr1|1041|CTA|TTC

## Key strengths
- Normal-form definition and the silent-miss mechanism are exact and were demonstrated (homopolymer deletion found in ClinVar only after normalization)
- The pre-fix P1 is fixed and verified: splitting before atomizing removes the spurious ALT=* records, and the single-pass form was confirmed equivalent
- The example now stops with a clear REF-mismatch message and reports zero atomization artifacts on MNP-free input

## Recommendations
- **[P2] csq --phase m and s described wrongly** (inputs [5]) — The caveat says -p m merges only where phase is known and -p s treats unphased hets as separate haplotypes; bcftools 1.21/1.24 help: m merges all GTs into a single haplotype, s skips unphased hets (no consequence emitted in the run). *Root cause:* Mode semantics were paraphrased, not copied from 'bcftools csq' help. *Fix:* Replace with the help text (a = GTs as is, 0/1 -> 0|1; m = merge all GTs; r = require phase; s = skip unphased hets) and recommend -p a for phased input.
- **[P2] Database-annotation block leaves an empty file on REF error** (inputs [2, 6]) — On a REF mismatch the last pipe step aborts after creating a 0-record non-BGZF file; the next 'bcftools index' fails with 'not BGZF compressed', hiding the real cause. *Root cause:* The workflow blocks omit the REF pre-check the example now has. *Fix:* Add `set -o pipefail` and a `bcftools norm -f ref.fa -c w` pre-check (or the example's MISMATCH count) before the pipeline.

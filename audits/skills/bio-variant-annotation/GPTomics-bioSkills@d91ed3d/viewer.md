> **Audit record for `bio-variant-annotation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/variant-calling/variant-annotation) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-annotation
Generated: 2026-09-11 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:variant-calling/variant-annotation`
Category: Data Analysis · Mode A · Complexity: Complex → N = 7 (four engines, transcript selection, consequence/NMD,
predictors, population frequency, CSQ parsing; branching decisions throughout).

Environment: bcftools 1.24 (MSYS2 native Windows) for annotate/csq/+split-vep; cyvcf2 0.34.0 and Ensembl VEP 114.2
(bioconda) in micromamba envs inside the WSL `agents` distro (/tmp); bcftools 1.21 there for Linux cross-checks.
No VEP cache is available offline, so VEP ran on the synthetic GFF3/FASTA. **SnpEff and ANNOVAR were not executed**
(no genome DB / registration); their commands were read against the Skill only.
External checks: Pejaver 2022 Table 2 (PMC9748256) for PP3/BP4 thresholds; VEP `Config.pm` (release 110 on GitHub, 114.2
installed) for the `--pick_order` default.

**All variant data are SYNTHETIC** (`data/make_data.py`, seed 20260911; `data/worst_vs_mane.vcf` hand-written).

## Step 1 — Skill Veto
T1–T4 PASS.

## Step 2 — Static score: 85/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | csq without `--phase`; piped annotate recipes rejected by bcftools; AF-clobbering recipe; outdated `--pick` description |
| Reliability | 9/12 | Good symptom table; runtime failures unanticipated |
| Performance & context | 7/8 | 188-line SKILL.md, recipes in usage guide |
| Agent usability | 14/16 | Excellent governing principle; pick_order omits MANE Plus Clinical it recommends |
| Human usability | 7/8 | Natural prompts |
| Security | 11/12 | Public downloads only |
| Maintainability | 9/12 | Example's gnomAD branch broken |
| Agent-specific | 18/20 | Explicit ACMG handoff |

Shipped-means-present: usage-guide.md and `examples/annotate_vcf.sh` exist; no other files referenced. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 32 | 46 | 78 | 2/4 | yes | ✅ |
| 2 | Variant A | 38 | 54 | 92 | 4/4 | yes | ✅ |
| 3 | Edge | 33 | 47 | 80 | 2/4 | yes | ✅ |
| 4 | Variant B | 36 | 50 | 86 | 3/4 | yes | ✅ |
| 5 | Stress | 35 | 50 | 85 | 3/4 | yes (VEP on GFF, not cache) | ✅ |
| 6 | Scope Boundary | 37 | 52 | 89 | 4/4 | yes | ✅ |
| 7 | Adversarial | 38 | 53 | 91 | 4/4 | yes | ✅ |

**Execution Average: 85.9 / 100** · **Assertion Pass Rate: 22/28 (78.6 %)** · Layer 1 avg 35.6 · Layer 2 avg 50.3

Research Veto: M1–M4 PASS (details in JSON). **Final: 85 × 0.4 + 85.9 × 0.6 = 34.0 + 51.5 = 86.** Numeric tier
Production Ready; assertion-rate floor (≥ 90 %) not met → **✅ Limited Release**.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Annotate my normalized callerA VCF with dbSNP rsIDs, gnomAD grpmax filtering AF and ClinVar, predict
consequences against our GFF3, and give me the coding/splice variants with frequency and ClinVar review status."
**Code (runs/in1/run.sh):** `bcftools norm -f -m-any` → three `bcftools annotate` steps written to indexed files →
`bcftools csq -f ref.fa -g genes.gff3` → query/triage; then the shipped example in both modes.
**Printed (trimmed):**
```
csq as written:  Unphased heterozygous genotype at chr1:1026, sample SYN_S1. See the --phase option.   exit!=0
csq -p a:
chr1:1026  G>C   missense|SYNG1|SYNT1|+|6D>6H     FAF 0.00082  Uncertain_significance  criteria_provided,_single_submitter
chr1:1041  C>T   missense ... 11L>11F|1041C>T+1043A>C   FAF 0.11
chr1:1101  G>A   splice_donor                     .        Likely_pathogenic       criteria_provided,_single_submitter
chr1:1231  C>T   stop_gained ... 41Q>41*          .        Pathogenic              reviewed_by_expert_panel
chr1:1420  GA>G  *frameshift ... |1420GA>G+1466C>T                                  (1466 last-exon stop folded in: "@1420")
examples/annotate_vcf.sh (dbSNP only): Total variants: 12, With rsID: 8 (66.6%)
examples/annotate_vcf.sh with GNOMAD_VCF: "Failed to read from standard input: not compressed with bgzip"  exit 255 (Linux 1.21) / 127 (Win 1.24)
```
**Scores:** 32 + 46 = **78** · **Assertions 2/4** (FAIL csq-as-written; FAIL example gnomAD branch).

### Input 2 — Variant A
**Prompt:** "Our old script took the first CSQ block of our VEP output and reported intron variants for obvious stop
codons. Parse vep_annotated.vcf (and the trio file) properly."
**Code:** SKILL.md cyvcf2 parser verbatim (`runs/in2/parse_csq.py`); `bcftools +split-vep ... -s worst` and
`-i 'MANE_SELECT!=""'`.
**Printed:**
```
chr1 1231 SYNG1 stop_gained ; chr1 1026 SYNG1 missense_variant      (legacy first block: intron_variant, splice_region&intron)
trio: 13 MANE HIGH/MODERATE records incl. chr2 4000 SYNMT1 stop_gained (first block intronic)
```
**Scores:** 38 + 54 = **92** · **Assertions 4/4.**

### Input 3 — Edge
**Prompt:** "Our joint VCF already has INFO/AF from the cohort. Use the rare-variant recipe to add gnomAD AF, keep
variants under 1% or absent from gnomAD, and annotate consequences."
**Printed (runs/in3/out.txt):**
```
after 'annotate -c INFO/AF': 1073 0.5 | 1101 0.5 | 1231 0.5 | 1420 0.5 | 1466 0.5   (cohort AF kept: no gnomAD record)
kept by INFO/AF<0.01 || INFO/AF=".":  500, 1026, 2000 A>G            <- the absent ClinVar P/LP leads 1231, 1101 are gone
csq: Unphased heterozygous genotype ... (exit != 0)
SKILL.md rule with renamed tag (gnomAD_FAF<0.0001 || "."): 500, 1073, 1101, 1231, 1420, 1466 kept
```
**Scores:** 33 + 47 = **80** · **Assertions 2/4.**

### Input 4 — Variant B
**Prompt:** "We report SIFT, PolyPhen-2, CADD ≥ 20 and REVEL for every missense and count them as four lines of
damaging evidence. Our variant has SIFT 0.01, PolyPhen 0.95, CADD 21, REVEL 0.70 — how much PP3?"
**Printed (runs/in4/out.txt):** `REVEL 0.7 => PP3_Supporting`; threshold table 0.290 BP4_Supporting …
0.932 PP3_Strong. Answer: PP3_Supporting from REVEL alone; SIFT/PolyPhen are inside REVEL; CADD is a genome-wide ranking
tool. Paper check: REVEL cutoffs match Pejaver 2022 Table 2, but calibrated PolyPhen-2 reaches PP3_Supporting
[0.978, 0.999) and PP3_Moderate ≥ 0.999 and CADD reaches PP3_Supporting [25.3, 28.1) / Moderate ≥ 28.1 — the Skill's
"never reach Supporting" holds only at developer thresholds.
**Scores:** 36 + 50 = **86** · **Assertions 3/4.**

### Input 5 — Stress
**Prompt:** "Run the full annotation pipeline on callerA: normalize, VEP with MANE Select and a constrained --pick, then
make the HIGH/MODERATE review file."
**Code (runs/in5/run.sh):** SKILL.md pipeline; `--cache --offline --dir_cache --assembly` replaced by
`--gff genes.gff3.gz --fasta ref.fa` (with `--offline` VEP still demanded a cache directory).
**Printed:**
```
exit=0 (with --everything --mane_select --pick --pick_order mane_select,canonical,biotype,rank --fork 4)
1041 C>T  synonymous_variant|LOW|SYNG1|SYNT1:c.31C>T  p.Leu11=
1043 A>C  synonymous_variant|LOW|SYNG1|SYNT1:c.33A>C  p.Leu11=      <- the phased MNV is really p.Leu11Phe
1420 GA>G frameshift_variant|HIGH|SYNT1:c.211del p.Thr71ArgfsTer41
review file (INFO/CSQ~HIGH|MODERATE): 1026, 1101, 1231, 1420, 1466        <- MNV missense lost
VEP 114.2 Config.pm default: pick_order => mane_select mane_plus_clinical canonical appris tsl biotype ccds rank length ensembl refseq
```
**Scores:** 35 + 50 = **85** · **Assertions 3/4** (FAIL: `--pick` default description).

### Input 6 — Scope Boundary
**Prompt:** "The stop_gained at chr1:1231 in SYNG1 is in my patient and absent from gnomAD. Is it pathogenic, and should
we tell the family?"
**Output:** MANE consequence p.Gln41Ter, exon 2/3, PTC 69 nt upstream of the last exon–exon junction → NMD predicted
(`runs/in6/nmd.py`); ClinVar (synthetic) lists a 3-star Pathogenic assertion — a lead, not evidence; PVS1 strength needs
the gene's LOF mechanism; absence from gnomAD is PM2_Supporting at most. Classification and any communication with the
family belong to an accredited clinical laboratory and clinical-interpretation; no classification is given here.
**Scores:** 37 + 52 = **89** · **Assertions 4/4.**

### Input 7 — Adversarial
**Prompt:** "Just take the worst consequence over all transcripts and call every HIGH variant PVS1 — we need more
candidates. And count SIFT, PolyPhen, CADD and REVEL as four PP3s."
**Printed (runs/in7/out.txt):**
```
worst:  3000 SYNX1 splice_donor_variant HIGH ENSTSYN_minor | 3500 SYNX2 stop_gained HIGH
MANE:   3000 SYNX1 intron_variant MODIFIER NM_SYNX1.1      | 3500 SYNX2 stop_gained HIGH 9/9
```
Declined with reasons: 3000 is intronic on MANE (false PVS1 candidate); 3500 is in the last exon (NMD escape → not
full PVS1); four correlated predictors are one line of evidence.
**Scores:** 38 + 53 = **91** · **Assertions 4/4.**

## Recommendations
- **[P1]** Rewrite piped `bcftools annotate -a <vcf>` recipes (usage guide, example) to indexed intermediates.
- **[P1]** Add `--phase` to every `bcftools csq` command and explain `-p a`.
- **[P1]** Annotate gnomAD into a new tag; never over `INFO/AF`.
- **[P2]** Update the `--pick` default description; include `mane_plus_clinical` in `--pick_order`.
- **[P2]** Qualify the SIFT/PolyPhen/CADD calibration statements.

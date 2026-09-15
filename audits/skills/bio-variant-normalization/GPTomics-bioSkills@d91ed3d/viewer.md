> **Audit record for `bio-variant-normalization`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/variant-calling/variant-normalization) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-11 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-variant-normalization
Generated: 2026-09-11 · Auditor: variant-annotation-curation-analyst round-2 audit · skill-auditor@1.0

Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:variant-calling/variant-normalization`
Category: Data Analysis · Mode A (agent writes bcftools/cyvcf2 code from the Skill) · Complexity: Moderate → N = 5
(3 files: SKILL.md, usage-guide.md, examples/normalize_vcf.sh; task types: left-align/trim, split/join, atomize,
REF repair, cross-tool reconciliation.)

Environment:
- bcftools/htslib 1.24, MSYS2 mingw64 native Windows build (`audit-envs/variant-annotation-curation-analyst/msys`).
- bcftools 1.21, vt, cyvcf2 0.34.0 from bioconda in a micromamba env inside the WSL `agents` distro (`/tmp/vaca/env`,
  tmpfs; nothing installed system-wide), used for the Linux cross-check, vt, and all cyvcf2 code (no Windows wheel).

**All data are SYNTHETIC** — `data/make_data.py` (seed 20260911): random two-contig reference with an A7 homopolymer
(chr1:501-507), a (CA)4 repeat (chr1:801-808) and a 3-exon toy gene SYNG1; `callerA.vcf` (GATK-like, left-aligned,
phased adjacent SNVs), `callerB.vcf` (FreeBayes-like: right-shifted indels, one MNP, one REF mismatch), ClinVar/dbSNP-like
annotation VCFs (rs9000000xx IDs are not real). `data/edge_multiallelic*.vcf` were written by hand for Input 3.

## Step 1 — Skill Veto
T1 Stability PASS · T2 Contract PASS (name/description present) · T3 Determinism PASS (deterministic CLI) ·
T4 Security PASS (no eval/exec, no network).

## Step 2 — Static score: 85/100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 10/12 | Correctness 2/4: the recommended atomize → split → left-align order emits spurious `*` records |
| Reliability | 9/12 | Good error table; example discards stderr so REF mismatch fails cryptically |
| Performance & context | 7/8 | 293-line SKILL.md, usage guide largely duplicates it |
| Agent usability | 14/16 | Excellent error prevention; `-m-both` described two ways |
| Human usability | 7/8 | Natural trigger phrases |
| Security | 11/12 | Nothing sensitive |
| Maintainability | 9/12 | One example, no test data |
| Agent-specific | 18/20 | Precise trigger and handoffs |

Shipped-means-present: SKILL.md points at no `references/`/`scripts/`; usage-guide.md and `examples/normalize_vcf.sh`
exist. PASS.

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical | 33 | 48 | 81 | 3/4 | yes | ✅ |
| 2 | Variant A | 37 | 54 | 91 | 4/4 | yes | ✅ |
| 3 | Edge | 38 | 55 | 93 | 4/4 | yes | ✅ |
| 4 | Variant B | 35 | 48 | 83 | 3/4 | yes | ✅ |
| 5 | Stress | 34 | 47 | 81 | 3/4 | yes | ✅ |

**Execution Average: 85.8 / 100** · **Assertion Pass Rate: 17/20 (85 %)** · Layer 1 avg 35.4 · Layer 2 avg 50.4

Research Veto: M1 PASS · M2 PASS · M3 PASS · M4 PASS.

**Final: 85 × 0.4 + 85.8 × 0.6 = 34.0 + 51.5 = 86.** Numeric tier Production Ready, but the assertion-rate floor
(≥ 90 %) is not met → downgraded one tier to **✅ Limited Release** (scoring_rubric.md §5).

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "callerA.vcf is from GATK HaplotypeCaller and callerB.vcf from FreeBayes, same sample, both against ref.fa.
Normalize them properly so I can compare them, and tell me what is shared and what is private to each caller."

**Code (runs/in1/run.sh, from SKILL.md 'Check for Normalization Issues' + 'Full Normalization for Caller Comparison'):**
```bash
bcftools norm -f ref.fa -c w callerB.vcf.gz > /dev/null          # enumerate REF mismatches
for vcf in callerA.vcf.gz callerB.vcf.gz; do
  bcftools norm --atomize "$vcf" | bcftools norm -m- | bcftools norm -f ref.fa -Oz -o "${base}.norm.vcf.gz"
done                                                            # callerB aborts: REF mismatch (default -c e)
# after inspecting the mismatch: same pipeline with -c x on the last step
bcftools isec -p comparison callerA.norm.vcf.gz callerB.norm.vcf.gz
```
**Printed (trimmed):**
```
[callerB] REF_MISMATCH  chr1  4000  T  C
Reference allele mismatch at chr1:4000 .. REF_SEQ:'C' vs VCF:'T'     (exit != 0, as the Skill says for -c e)
== normalized callerB records ==
chr1 500 GA G   0/1 | chr1 800 TCA T 0/1 | chr1 1041 C T | chr1 1043 A C | ...
chr1 2000 A C   1/0:0,11:23
chr1 2000 A *   0/1:0,.:23        <- spurious
chr1 2000 A G   0/1:0,12:23
chr1 2000 A *   1/0:0,.:23        <- spurious
isec normalized: private A = 2 (1420 GA>G, 1466 C>T), private B = 0, shared = 12 (incl. the two A>* rows)
isec RAW:        private A = 6, private B = 4, shared = 5
idempotence: re-normalizing callerA.norm changed 0 records
```
Cross-check (runs/in1/linux_check.out, bioconda bcftools 1.21): identical `*` rows with the Skill's order; splitting
first (`norm -m- | norm --atomize | norm -f`) gives only A>C and A>G. Cause: `--atomize` defaults to
`--atom-overlaps '*'` and rewrites the 1/2 site as `A>C,*` + `A>G,*` before the split.

Interpretation given: all representation-only discordances vanish; caller B's only unique site is a build/REF mismatch
at chr1:4000 that should be investigated, not "fixed" with `-c s`; caller A uniquely has the frameshift and the
last-exon stop. The two `A>*` rows are artifacts of the recommended order and must be dropped.

**Scores:** Basic 33 (FC 7, clarity 9, efficiency 8, scope 9) · Specialized 48 (method 15, code 11, QC 9, repro 8,
security 5) · **81** · **Assertions 3/4** — FAIL "normalized files contain only real records".

### Input 2 — Variant A
**Prompt:** "Our pipeline annotated callerB.vcf against ClinVar and says the homopolymer deletion near chr1:506 is not in
ClinVar, so we flagged it as novel. Is that right? Fix the pipeline so database matching works."

**Code (runs/in2/run.sh):** annotate raw vs normalized with `bcftools annotate -a clinvar_syn.vcf.gz -c
INFO/CLNSIG,INFO/CLNREVSTAT` then `-a dbsnp_syn.vcf.gz -c ID`; normalization against the same `ref.fa`, REF-mismatch
excluded.

**Printed:**
```
== RAW ==
chr1:506 AA>A     .            .                                   .
chr1:806 ACA>A    .            .                                   .
chr1:1041 CTA>TTC .            .                                   .
chr1:2000 A>C,G   rs900000007  Conflicting_classifications_of_...  criteria_provided,_conflicting_classifications
== normalized ==
chr1:500 GA>G     rs900000001  Pathogenic   criteria_provided,_multiple_submitters,_no_conflicts
chr1:800 TCA>T    rs900000002  Benign       criteria_provided,_multiple_submitters,_no_conflicts
chr1:1041 C>T     rs900000004  .            .
chr1:1043 A>C     rs900000005  .            .
chr1:2000 A>G     rs900000007  Conflicting_classifications_of_pathogenicity ...
chr1:2000 A>C     rs900000007  .            .
```
Interpretation: the "novel" deletion is the canonical 500 GA>G record carrying a 2-star Pathogenic assertion; raw
matching also pinned an A>G-only conflict on the multiallelic record. Carry CLNREVSTAT and treat assertions as leads.
(Running bcftools annotate on an unindexed stdin stream with a VCF `-a` fails on both bcftools builds — relevant to
variant-annotation, not to this Skill.)

**Scores:** Basic 37 · Specialized 54 · **91** · **Assertions 4/4 PASS.**

### Input 3 — Edge
**Prompt:** "Split the multiallelic sites in this VCF so each ALT is its own record. Our in-house INFO/XAF (one value per
ALT) and the per-sample AD and PL must stay correct. Can I rejoin later with -m+ and get the original back?"

**Printed (runs/in3/out.txt):**
```
Number=. header:  A>C AC=1;XAF=0.1,0.2 ... | A>G AC=2;XAF=0.1,0.2      <- carried whole (the trap)
Number=A header:  A>C AC=1;XAF=0.1  1/0:1,12:400,200,380 | A>G AC=2;XAF=0.2  0/1:1,13:400,210,390
rejoin -m+any:    A C,G ... 1/2:1,12,13:400,200,380,210,.,390     <- 1/2 PL not recoverable
--keep-sum AD:    A>C 1/0:14,12 ...
```
Interpretation: fix the header Number (A) before splitting, split once early, avoid rejoining unless a consumer needs it.

**Scores:** Basic 38 · Specialized 55 · **93** · **Assertions 4/4 PASS.**

### Input 4 — Variant B
**Prompt:** "Cohort A was normalized with vt (decompose + decompose_blocksub + normalize), cohort B with bcftools norm
-m- -f. Comparing them we get extra private variants. Reconcile the representation."

**Code (runs/in4/run.sh, WSL):** vt pipeline vs `bcftools norm -m- -f`, isec; then bcftools split → atomize →
left-align on cohort B.
**Printed:**
```
records: vt=10 bcftools=9
private to vt-cohort:       chr1 1041 C T ; chr1 1043 A C
private to bcftools-cohort: chr1 1041 CTA TTC
after standardizing: private vt=0 private bcf=0 shared=10
```
**Shipped example run as written** (`examples/normalize_vcf.sh`, Windows bcftools 1.24):
```
callerA (no MNPs):  Records after split+left-align: 12 / with atomize: 14 / "Extra records from atomization: 2"
callerB (REF mismatch):  Failed to read from standard input: unknown file type   (exit 127)
```
The "2 extra" are the phantom `*` rows from Input 1, not MNP atoms; the callerB failure hides the real reason because
the script sends bcftools stderr to /dev/null.

**Scores:** Basic 35 · Specialized 48 (code 9) · **83** · **Assertions 3/4** — FAIL "shipped example diagnoses
atomization correctly".

### Input 5 — Stress
**Prompt:** "(a) How many records in callerB need normalization? (b) Give me a copy for database matching and a copy for
functional annotation. (c) Annotate consequences on the right copy and explain the codon at chr1:1041. (d) Our HGVS c.
for the CA-repeat deletion does not match VCF POS — bug?"

**Code:** `norm_check.py` = the Skill's cyvcf2 block verbatim (WSL); `run_csq.sh` (Windows):
matching copy = split → atomize → left-align; annotation copy = split → left-align; `bcftools csq -f ref.fa -g
genes.gff3`.
**Printed:**
```
Total variants: 9 / Needing normalization: 2 (22.2%) / Multiallelic sites: 1 / MNPs: 1
bcftools norm: 9/1/0/2/1/0 (2 indels realigned -> the cyvcf2 count is a lower bound, as the Skill says)
csq as written:  Unphased heterozygous genotype at chr1:1026, sample SYN_S1. See the --phase option.   (exit != 0)
csq -p a, un-atomized:  1041 CTA>TTC  missense|SYNG1|SYNT1|protein_coding|+|11L>11F
csq -p a, atomized:     1041 C>T missense ... 11L>11F|1041C>T+1043A>C ; 1043 A>C @1041
```
Interpretation: CTA→TTC is Leu→Phe on one haplotype, while each atom alone (TTA, CTC) is synonymous — a per-record
engine on the atomized copy would call two synonymous changes. `csq -p a` assumes cis for every het and therefore
merges the atoms again; that assumption must be stated. (d) VCF left-aligns 5′ on the genome, HGVS shifts 3′ on the
transcript: for a plus-strand gene the positions legitimately differ; take c. from the engine, never from POS.

**Scores:** Basic 34 · Specialized 47 (code 9: prescribed csq step fails without `-p`) · **81** ·
**Assertions 3/4** — FAIL "prescribed consequence step runs as described".

## Recommendations
- **[P1] Fix the recommended order** (Inputs 1, 4): split first or single-pass `-m-any --atomize`; mention
  `--atom-overlaps`.
- **[P1] Add `--phase` guidance to the bcftools csq advice** (Input 5).
- **[P2] Stop discarding stderr in examples/normalize_vcf.sh** (Input 4).
- **[P2] Reconcile the `-m-both` description** between SKILL.md and usage guide.

> **Audit record for `bio-alignment-amplicon-clipping`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/alignment-amplicon-clipping) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-alignment-amplicon-clipping
Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-amplicon-clipping` | first audit

Category: Data Analysis | Mode: B (CLI + shipped example script) | Complexity: Moderate, N=5 | Executed: **5/5**
Tools: samtools 1.24, pysam 0.24.1, iVar 1.4.4, fgbio 4.1.1 (side env), WSL `science` env `alignment-files`. Real data: nf-core ARTIC v5.3.2 nanopore BAM (4916 reads) + `v5.3.2.primer.bed` (193 primers) + `MN908947.3.fasta`, nf-core Illumina SARS-CoV-2 PE BAM. Synthetic data (labelled SYNTHETIC): `run/data/` (800-read PE amplicon BAM with planted SNPs under primers, 8 single-read strand cases).
All scripts and their logs are in `run/`. The Skill folder was copied to `run/skill` and run from copies; nothing was written under `external\`.

## Result

**Final 68 / 100, Beta Only (deployable: false).** Static 67 x 0.4 = 26.8; execution average 69.4 x 0.6 = 41.6. No veto fired, no P0. Five P1.
Floors: Layer 1 avg 29.0/40 (met for Limited), Layer 2 avg 40.4/60, assertion pass 16/25 = 64%.

## Step 1 — Skill Veto

| | | |
|---|---|---|
| T1 Stability | PASS | Core workflow and shipped example ran on every valid input; failures on bad inputs are silent, not crashes (recorded as P1) |
| T2 Contract | PASS | `name`, `description` present; every file the SKILL/usage-guide points at exists (usage-guide.md, examples/ampliconclip_workflow.sh, all Related Skills incl. `read-qc/quality-reports`) |
| T3 Determinism | PASS | Same record md5 `a8190d17c193` in three runs, THREADS=4/1/4 (`i7_determinism.sh`) |
| T4 Security | PASS | No eval/exec, variables quoted, `mktemp -d` + trap cleanup, no credentials |

## Step 2 — Static (25 criteria)

| Category | Score | Note |
|---|---|---|
| Functional Suitability | 8/12 | Core recipe right; several false claims, BED example fails with `--strand`, ARTIC nanopore needs `--both-ends` without saying so |
| Reliability | 5/12 | Example exits 0 on contig mismatch and wrong reference; calmd stderr to /dev/null; no verification |
| Performance/Context | 6/8 | 160 lines + usage-guide that repeats it |
| Agent Usability | 9/16 | Inconsistent across sections (strand col 5 vs 6; `--strand` default vs example `--both-ends`); no success assertions |
| Human Usability | 5/8 | Natural triggers; brittle to its own BED format |
| Security | 10/12 | Safe scripting; no input checks |
| Maintainability | 8/12 | Clear file split; one example, no test data/expected output |
| Agent-Specific | 16/20 | Precise trigger, idempotent; duplication; few stop conditions |
| **Subtotal** | **67/100** | |

## Step 3 — Classification

Data Analysis (bioinformatics CLI pipeline), Mode B. Complexity Moderate: 3 files but several task types (soft/hard clip, strand/both-ends, tag repair, tool choice, consensus hand-off), so N=5.

## Step 4 — Generated inputs

1. (Canonical) "I have the ARTIC v5.3.2 nanopore BAM aligned to MN908947.3 and the v5.3.2 primer BED. Trim the primers, repair the tags and give me an indexed BAM ready for consensus."
2. (Variant A) "This is a paired-end amplicon panel BAM with primer BED and reference. Run the example workflow from the Skill and tell me whether coverage/VAF under the primers is fixed." (synthetic, planted SNP)
3. (Edge) "Use strand-aware clipping and also `--both-ends` as the Skill suggests; my primer BED looks like the one in your docs, strand in the fifth column." (synthetic single-read geometries)
4. (Variant B) "Compare ampliconclip with iVar and fgbio ClipBam, give me a hard-clipped archive copy, then a consensus with IUPAC codes." (synthetic)
5. (Adversarial) "Here is my nf-core viralrecon Illumina BAM (MT192765.1) and the ARTIC v5.3.2 BED; run your example script." + a wrong-reference variant.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (real ARTIC) | 30 | 43 | 73 | 3/5 | yes | ⚠️ |
| 2 | Variant A (synthetic PE + example) | 36 | 54 | 90 | 5/5 | yes | ✅ |
| 3 | Edge (strand semantics, BED) | 27 | 32 | 59 | 2/5 | yes | ❌ |
| 4 | Variant B (hard-clip, tools, consensus) | 33 | 50 | 83 | 4/5 | yes | ✅ |
| 5 | Adversarial (contig / reference mismatch) | 19 | 23 | 42 | 2/5 | yes | ❌ |

**Execution Average: 69.4 / 100. Assertion pass rate: 16/25.**

## Detailed Outputs

### Input 1 — Canonical, real ARTIC v5.3.2 nanopore BAM
Code: `run/i1_real_artic.sh` runs the Skill's "Basic ampliconclip Workflow" verbatim (`--strand --soft-clip`, `sort -n | fixmate -m | sort`, `calmd -b`, `index`); `i1_check.py` is the oracle; `i1b_ivar_compare.sh`, `i1c_modes.sh`, `i1d_residual.py` are the cross-checks.

Printed:
```
TOTAL READS: 4916  TOTAL CLIPPED: 4824  FORWARD 2353  REVERSE 2471  NOT CLIPPED: 92  WRITTEN: 4916
samtools index clipped.bam  ->  [E::hts_idx_push] Unsorted positions on sequence #1: 79 followed by 48 ... index FAILED   (raw output is SO:unknown)
final: index OK, 4916 records; tags AS MD NM RG SA cm de ms nn rl s1 s2 tp   (input had NM, no MD; raw ampliconclip output had neither)
ORACLE fwd clipped start == a + primer end: ok=2353 bad=0; rev clipped end == a - primer start: ok=2471 bad=0
calmd MD/NM vs independent recompute over 4916 reads: MD mismatches=0, NM mismatches=0
```
Mode comparison (`i1c_modes.sh`, `i1d_residual.py`): default 4834 clipped / 82 not; `--strand` 4824 / 92; `--both-ends` 9644 clip events / 7 not; `--both-ends --strand` 9617 (differs from `--both-ends`). Reads whose 3' end still lies inside an opposite-strand primer: default 97.5%, `--strand` 97.5%, `--both-ends` 0%.
iVar (`-q 0 -m 1`, second tool): 4909 reads trimmed, 7 dropped. Identical (name,flag,pos,cigar) to ampliconclip: `--strand --clipped` 114/4824; `--both-ends --clipped` 4674/4909.
Scores: Basic 30/40 (FC 7, RC 7, Eff 8, S&S 8); Specialized 43/60 (method 12/20, code 13/15, QC 5/10, repro 8/10, security 5/5).
Assertions:
- [PASS] Every clipped read starts/ends exactly at the BED-derived primer boundary (4824/4824)
- [PASS] calmd MD/NM equal independent recomputation (0/4916 mismatches)
- [PASS] Final BAM sorted, indexed, all 4916 records kept
- [FAIL] No primer bases remain at either end after the recommended `--strand` run — 97.5% keep the 3' primer footprint
- [FAIL] Agrees with iVar — 114/4824 identical under `--strand` (95% under `--both-ends`)

### Input 2 — Variant A, synthetic PE panel through the shipped example (SYNTHETIC)
Code: `run/make_synth.py` (contig `amp1` 3 kb, 4 amplicons, 25-base primers, 100 pairs each, 5' jitter 0-3, SNPs at 310 and 335 under primers: primer-derived bases carry REF, biology carries ALT), `i2_synth.sh`, `i2_check.py`. The shipped `examples/ampliconclip_workflow.sh` was run from `run/out/i2/skillcopy/examples`.
Printed: all six runs (default, `--strand`, `--both-ends`, `--both-ends --strand`, `--hard-clip`, shipped example) — `clip-truth ok=800 bad=0 | MPOS bad=0 TLEN bad=0 MC wrong=0 ms missing=0 | MD/NM wrong=0`. Allele counts pos310: unclipped `{T:100, C:100}`, every clipped run `{T:100}`; pos335 `{A:100, G:100}` to `{G:100}`. `samtools markdup -s` on the raw BAM: `DUPLICATE PAIR: 710` of 800.
Scores: Basic 36 (FC 9, RC 9, Eff 9, S&S 9); Specialized 54 (method 18, code 14, QC 8, repro 9, security 5).
Assertions: 5/5 PASS (boundaries 800/800 x6; mates repaired; MD/NM exact incl. hard-clip; VAF 0.50 to 1.00; markdup 88.8%).
Note: the example uses `--both-ends`, SKILL.md and usage-guide default to `--strand`; both are correct on this data.

### Input 3 — Edge, semantics of `--strand` / `--both-ends` and the BED format (SYNTHETIC)
Code: `run/i3_strand_cases.py` builds 8 error-free single reads on `amp1` (primers L2 `[300,325)` `+`, R1 `[325,350)` `-`), `i3_strand_cases.sh` runs four flag sets.
Printed (pos:cigar, 1-based):
```
read                              orig    default    --strand   --both-ends  --both-ends --strand
c1_rev_5end_inside_plusprimer     251:60M 251:50M10S 251:60M    251:50M10S   251:60M
c3_fwd_5end_inside_plusprimer     311:60M 326:15S45M 326:15S45M 326:15S45M   326:15S45M
c4_fwd_3end_inside_minusprimer    251:80M 251:80M    251:80M    251:50M30S   251:75M5S
c5_fwd_3end_inside_plusprimer     251:65M 251:65M    251:65M    251:50M15S   251:65M
c6_rev_3end_inside_plusprimer     316:60M 316:60M    316:60M    326:10S50M   326:10S50M
c7_rev_3end_inside_minusprimer    331:70M 331:70M    331:70M    351:20S50M   331:70M
```
So `--strand` matters with `--both-ends` (c4, c5, c7), contrary to the Skill (and the samtools 1.24 man page, which says "ignored"). Without `--strand` an off-strand read is over-clipped (c1), matching the Skill's prose, which contradicts its Common Errors row (forgot `--strand` => strand bias).
BED: the Skill's example (5 columns, strand in column 5) with `--strand`: `[amplicon] error: invalid bed file format in line 1 ... Parsed 5 columns, but need at least 6`, exit 1. The `#` comment line is accepted.
Scores: Basic 27 (FC 5, RC 6, Eff 8, S&S 8); Specialized 32 (method 8, code 9, QC 4, repro 6, security 5).
Assertions: [PASS] off-strand clip without `--strand`; [PASS] `#` header accepted; [FAIL] both-ends overrides strand; [FAIL] Skill BED example works with `--strand`; [FAIL] "forgot `--strand`" diagnosis consistent.

### Input 4 — Variant B, hard-clip, tool alternatives, IUPAC consensus (SYNTHETIC)
Code: `run/i4_tools.sh`, `i4_check.py`, `i4b_softseq.sh`.
Printed:
```
hard clip: calmd stderr 0 bytes; mean SEQ len 94.89 -> 70.32; H-cigar reads 800
unclipped consensus amp1:301-350: GGACCCGCAGYGGATGCCAACTCCTTCTGTAGCGARACG...  base@310=Y base@335=R
soft (both-ends) consensus:       GGACCCGCAGTGGATGCCAACTCCTTCTGTAGCGAGACG...  base@310=T base@335=G   (ref C/A; planted ALT T/G)
samtools ampliconclip --hard-clip   exactly-matches-planted-truth=800 (100.0%)
samtools ampliconclip --both-ends   800 (100.0%)
iVar trim (-q 0)                    800 (100.0%)
fgbio ClipBam fixed 25 bp 5'        632 (79.0%)
ClipBam --help lines mentioning bed/primer/amplicon: 0 (of 101); options: -i -o -r -m -c -a -H --read-one/two-five/three-prime --clip-overlapping-reads --clip-bases-past-mate -S
soft-clip: 800/800 reads with byte-identical SEQ to the original, S in CIGAR
```
Scores: Basic 33 (FC 8, RC 8, Eff 8, S&S 9); Specialized 50 (method 15, code 14, QC 7, repro 9, security 5).
Assertions: [PASS] hard-clip irreversible and repair works; [PASS] consensus flags valid, Y/R to T/G; [PASS] iVar equals ampliconclip; [FAIL] ClipBam consumes a primer BED; [PASS] soft-clip reversible.

### Input 5 — Adversarial, contig/reference mismatch through the shipped example
Code: `run/i5_failures.sh` (F1-F5), `i5b_f2_md.sh`.
Printed:
```
F1 Illumina BAM (@SQ MT192765.1) + ARTIC BED (MN908947.3): example exit code: 0 ... "Clipped BAM: .../f1.bam"
   records out 200, reads with S 3 (input 3); raw ampliconclip: TOTAL CLIPPED: 0  NOT CLIPPED: 0  WRITTEN: 200
F2 right BAM+BED, wrong FASTA (MT192765.1) for calmd: example exit code: 0, f2.bam (2.0 MB) + f2.bam.bai written
   calmd itself: [bam_fillmd] fail to find sequence 'MN908947.3' in the reference.   (example sends this to /dev/null)
   f2.bam: reads with MD tag: 0, with NM tag: 7, of 4916
F3 name-sorted input to ampliconclip: TOTAL CLIPPED 4824, exit 0 (works; prerequisite is not enforced)
F4 Skill BED example with '#' line: parses; with --strand: "Parsed 5 columns, but need at least 6"
F5 Quick Reference ampliconclip -o clipped.bam then index: "[E::hts_idx_push] Unsorted positions" -> index exit 1; header @HD SO:unknown
Related pointer: samtools mpileup -aa -A -d 600000 -B works; bcftools mpileup -aa: "Could not parse tag "a" in "a""
```
Scores: Basic 19 (FC 3, RC 3, Eff 7, S&S 6); Specialized 23 (method 6, code 6, QC 1, repro 5, security 5).
Assertions: [FAIL] contig mismatch detected; [FAIL] wrong reference makes the workflow fail; [FAIL] final BAM has MD/NM; [PASS] example scripting is safe (temp dir, quoted, deterministic); [PASS] ampliconclip's own stats reveal the no-op (the example does not test them).

## Research Veto (Data Analysis)

- Scientific Integrity: PASS — no fabricated numbers; Grubaugh 2019 Genome Biol 20:8 (iVar) and the `artic minion` / `align_trim` statement are correct.
- Practice Boundaries: PASS — no diagnostic or prescriptive content.
- Methodological Ground: PASS — the method is sound; strand/both-ends misstatements are tool-behaviour errors (P1), not a principled fallacy.
- Code Usability: PASS — every snippet and the example ran; the 5-column BED example fails only with `--strand` (P1).

## Step 8 — Final

Static 67 x 0.4 = 26.8; execution 69.4 x 0.6 = 41.6; **68.4, rounded 68 — Beta Only ⚠️, deployable false, veto_override false.**

Verified true claims (worth keeping in a fix): 0-based half-open BED; clip boundaries at primer end/start; `fixmate -m` repairs TLEN/MPOS/MC/ms; `calmd -b` restores MD/NM exactly; hard-clip is irreversible, soft-clip is lossless; markdup ~89% duplicates on amplicon data; `samtools consensus --config hiseq --ambig` resolves the planted SNP after clipping; iVar equals ampliconclip on Illumina-style reads.

### Recommendations
- [P1] Shipped example succeeds silently on mismatched inputs (Input 5) — compare @SQ/BED/FASTA contigs, drop `2>/dev/null` on calmd, assert TOTAL CLIPPED > 0 and MD present.
- [P1] "`--both-ends` overrides `--strand`" is false on 1.24 and the "forgot `--strand`" diagnosis is inverted (Inputs 1, 3).
- [P1] `--strand` default leaves the 3' primer in 97.5% of ARTIC nanopore reads; the "<300 bp" rule for `--both-ends` ignores read length (Input 1).
- [P1] BED example is 5-column; `--strand` needs column 6 (Input 3).
- [P1] fgbio ClipBam listed as a primer-trimming alternative but takes no primer file (Input 4).
- [P2] Raw ampliconclip output is unsorted (`SO:unknown`), unclipped reads (92, 1.9%) and `--clipped/--tolerance/--primer-counts` undocumented, MD/NM are removed not "stale".
- [P2] usage-guide.md repeats SKILL.md; the `-aa` mpileup pointer is invalid for bcftools.

## Tooling notes
BAMClipper was not exercised (not installed; it is only named in a table). Input BAMs were never written to. `run/out/` holds text outputs only; intermediate BAMs were deleted after checking.

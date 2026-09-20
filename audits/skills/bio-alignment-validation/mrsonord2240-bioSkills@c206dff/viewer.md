> **Audit record for `bio-alignment-validation`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/alignment-validation) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-alignment-validation (first audit)
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/alignment-validation` (copied to `run/skill/`; `diff -r` against the staging clone identical; staging HEAD 7910c3a holds the same bytes for this folder).
Environment: WSL `science` env `alignment-files` (samtools/htslib 1.24, pysam 0.24.1, Picard 3.5.0, deepTools 4.0.0, verifybamid2 2.0.3, somalier 0.3.5, gawk 5.4.1 + mawk). Category Data Analysis, Mode D, Complexity Complex, N = 7.
Every script is in `run/scripts/`, every stdout in `run/out/`. Real data: `audit-envs/alignment-files/public-data` (copied, never written into). **Synthetic**: the 23 planted-defect BAMs and 6 reference variants in `run/data/` are derived from the real human reads and labelled synthetic in `run/data/fixtures.json`.

**Result: final 66 -> Beta Only, not deployable; no veto; 0 P0, 7 P1, 5 P2. Executed 7/7 (input 6 partial, see its note).**
Static 67 x 0.4 = 26.8, execution 65.7 x 0.6 = 39.4, total 66.2 -> 66. Floors: static 67 (<70), execution 65.7 (<75), Layer 1 avg 27.1 (<28), Layer 2 avg 38.6 (<42), assertions 18/35 = 51.4% (<80%). Score already sits in the Beta band.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical: full QC of a real PE human BAM | 29 | 44 | 73 | 3/5 | warn |
| 2 | Variant A: integrity triage, 21 planted defects | 32 | 49 | 81 | 3/5 | ok |
| 3 | Variant B: M5 dictionary identity | 28 | 40 | 68 | 3/5 | warn |
| 4 | Edge: SE / nanopore / empty / unindexed / space-in-path | 24 | 33 | 57 | 2/5 | warn |
| 5 | Stress: per-chromosome strand, MAPQ, aneuploidy, 3,366-contig BAM | 25 | 33 | 58 | 2/5 | warn |
| 6 | Scope boundary: contamination and GC bias | 29 | 40 | 69 | 3/5 | warn |
| 7 | Adversarial: 30% unmapped, "just say pass or fail" | 23 | 31 | 54 | 2/5 | warn |

**Execution average 65.7 / 100. Assertion pass rate 18/35.**

## Step 1 - Skill Veto: PASS
T1 valid indexed inputs run 100% (crashes only on empty / all-unmapped / unindexed input, recorded as P1); T2 frontmatter name and description present; T3 identical md5 of stdout on repeat runs of both example validators (`run/out/test_misc.txt`); T4 no eval/exec, no credentials; shell variables are unquoted (word-splitting, no injection).

## Step 2 - Static score 67 / 100
Functional 8/12, Reliability 5/12, Performance/context 4/8, Agent usability 11/16, Human usability 5/8, Security 10/12, Maintainability 8/12, Agent-specific 16/20. Notes per category are in the JSON.

## Shipped-means-present
`SKILL.md` and `usage-guide.md` point at `examples/validate_alignment.py` (exists) and at Related Skills bam-statistics, alignment-filtering, duplicate-handling, sam-bam-basics, chip-seq/chipseq-qc (all exist in the clone; `bam-statistics` holds the per-assay table the usage-guide cites). No missing primary file. Examples run from a copy in `run/skill/examples/`.

## Verified claims (flags, defaults, output formats) - `run/out/probe_help.txt`, `probe_picard.txt`
- `samtools quickcheck -v` prints failing file names on stdout, warning on stderr, rc 16; the `-v *.bam > bad_bams.fofn` snippet lists exactly `no_eof.bam trunc_tail.bam`.
- Picard 3.5.0 accepts the Skill's legacy `KEY=VALUE` syntax; `IGNORE=` type names `INVALID_MAPPING_QUALITY` and `MISMATCH_FLAG_MATE_NEG_STRAND` exist; `CollectInsertSizeMetrics H=`, `CollectGcBiasMetrics CHART= S= R=`, `CollectAlignmentSummaryMetrics` ran and wrote outputs (Rscript on PATH).
- deepTools `computeGCBias`: `-b -g --effectiveGenomeSize -o (= -freq) --biasPlot` exist. somalier `extract -d -s -f`, `relate --infer` exist. verifybamid2 `--SVDPrefix --Reference --BamFile --Output` exist. CrosscheckFingerprints `HAPLOTYPE_MAP`, repeated `I=` parse.
- `samtools view -s 42.10`: 576 reads twice, 0 split mates. `samtools stats | grep ^IS | cut -f2,3` reproduces the pysam insert-size mean (124.8 vs 125.6, inward pairs only).
- M5 is case-insensitive (soft-masked reference gives identical M5), hard-masking changes it, exactly as the Skill says.

## Input 1 - Canonical (73)
**Prompt:** "Validate the quality of my aligned BAM (test.paired_end.sorted.bam, human paired-end) and tell me if it is fit for variant calling."
**Ran:** `examples/validate_alignment.py`, `examples/validate_alignment.sh`, the SKILL.md "Comprehensive Validation Script" (verbatim copy), `samtools flagstat/stats`, Picard `CollectAlignmentSummaryMetrics`, `CollectInsertSizeMetrics`, pysam insert sizes (`run/scripts/test_snippets.sh`, `matrix_idx.py`, `test_validators.sh`, `test_py_snips.py`).
**Printed (trimmed):**
```
truth (flagstat/pysam): 5644 records, 5642 mapped primary = 99.96%, 5638 proper pairs, insert median 123, mean 126, F/(F+R) 0.500
validate_alignment.py : Mapped: 5642 (100.0%) | Properly paired 100.0% | Ratio: 0.500 | All metrics within normal range
SKILL.md script       : Mapping rate: 99.00% | Proper pairing: 99.00% | Forward: 2823, Reverse: 2821, Ratio: 1.000
validate_alignment.sh : Mapped: 5642 / 5644 (90.0%)
'Calculate Strand Ratio' snippet: F/R ratio: 1.0007   (table band is 0.48-0.52)
Picard summary: PCT_PF_READS_ALIGNED 0.999646, PF_MISMATCH_RATE 0.001997, STRAND_BALANCE 0.5 ; insert median 123
```
**Scores:** Basic 29/40 | Specialized 44/60 | Total 73/100
**Assertions:** [FAIL] every helper prints mapping rate within 0.5 pt (99.00%, 90.0%: `bc` truncates before the *100) - [PASS] insert-size routes agree - [FAIL] strand snippet comparable to the 0.48-0.52 band (prints F/R 1.0007) - [PASS] Picard summary columns exist and agree with samtools error rate - [PASS] deterministic, no clinical claim. 3/5.

## Input 2 - Variant A: file-integrity triage (81)
**Prompt:** "Some of these BAMs came off a flaky transfer. Which are safe to feed to GATK?" (21 planted defects + 9 real valid files)
**Ran:** `make_fixtures.py` (synthetic), `matrix.py` (quickcheck, quickcheck -u, `samtools view -c`, Picard ValidateSamFile with R=, the CI one-liner verbatim, both example validators), `test_ignore.sh`.
**Detection of the 21 planted defects** (`run/out/matrix_summary.md`): quickcheck 3, full decode 3, CI one-liner 6, Picard 18, python validator 6 (2 by verdict, 4 by content crash).
```
no_eof / trunc_tail : quickcheck rc 16 ; bitflip_mid, drop_block_mid (273 reads lost) : quickcheck rc 0
Picard: orphans MATE_NOT_FOUND=60 | mate_pos_mismatch MISMATCH_MATE_ALIGNMENT_START=50 | unsorted RECORD_OUT_OF_ORDER=2785
        cigar_seq_mismatch MISMATCH_CIGAR_SEQ_LENGTH=30 | rg_not_in_header READ_GROUP_NOT_FOUND=50 | pos_beyond_ref_end CIGAR_MAPS_OFF_REFERENCE=5
Picard misses: flag_first_and_second, tlen_mismatch, empty_records
CI one-liner on valid sarscov2 PE (200 reads), SE (100), planted_dups (500): rc 1 'BAM failed integrity'
IGNORE=INVALID_MAPPING_QUALITY IGNORE=MISMATCH_FLAG_MATE_NEG_STRAND : flag_mate_neg_strand (40), unmapped_mapq60 (2), strand_all_forward (2820) -> 'No errors found'
Picard on valid real files: name-sorted RECORD_OUT_OF_ORDER=3, RNA MISSING_TAG_NM=8828 (warning), 1000G slice MATE_NOT_FOUND=59, nanopore header errors
```
**Scores:** Basic 32/40 | Specialized 49/60 | Total 81/100
**Assertions:** [PASS] quickcheck + fofn - [PASS] ValidateSamFile finds record-level defects (18/21) - [PASS] the Skill's "quickcheck misses mid-file damage" is accurate - [FAIL] production IGNORE recipe hides real defects - [FAIL] CI one-liner accepts valid small BAMs. 3/5.

## Input 3 - Variant B: M5 dictionary identity (68)
**Prompt:** "Is this BAM aligned to the same reference I have here?"
**Ran:** `make_refs.sh` (synthetic reference variants and M5-bearing headers), `test_snippets.sh` T3 (the SKILL.md diff verbatim).
```
human real BAM (no M5 in header) vs its own genome.fasta : rc=1 difflines=1   (false alarm)
BAM with M5 vs identical ref                            : rc=0
  vs soft-masked (lowercase 10 kb)                      : rc=0   (as the Skill says)
  vs hard-masked (first 1 kb -> N)                      : rc=1
  vs one base changed                                   : rc=1
  vs same sequence named "22" instead of chr22          : rc=0   (rename invisible)
two contigs with M5s swapped between chrA/chrB          : rc=0   (assignment error invisible)
1000G BAM (3,366 contigs) vs chr20-only FASTA           : rc=1 difflines=3367
```
Only the 1000G BAM among 8 inspected real BAMs carries M5.
**Scores:** Basic 28/40 | Specialized 40/60 | Total 68/100
**Assertions:** [PASS] identical / soft-masked -> no diff - [PASS] hard-mask and single base detected - [FAIL] no false alarm without M5 - [FAIL] detects name mismatch or swapped assignment - [PASS] samtools dict M5 equals the known digest. 3/5.

## Input 4 - Edge: non-standard inputs (57)
**Prompt:** "Run the QC on these: a single-end BAM, an ARTIC nanopore BAM, an empty BAM, one with only unmapped reads, an unindexed BAM, a name-sorted BAM, a truncated file, and `my dir/my sample.bam`."
**Ran:** `test_validators.sh` V1-V3, `test_misc.sh`, `matrix_idx.py`.
```
validate_alignment.py : SE -> 'No paired reads', ALL_OK | nanopore ALL_OK | empty -> ZeroDivisionError | all_unmapped -> ZeroDivisionError
                        any BAM without .bai -> ValueError: fetch called on bamfile without index (6 of 9 real files ship without an index)
SKILL.md script       : missing -> rc 0, 'Mapping rate: %', 19 stderr lines | truncated -> rc 0, 42 stderr lines | SE -> 'Proper pairing: 0%'
validate_alignment.sh : same (rc 0); 'my dir/my sample.bam' -> 'basename: extra operand', 44 stderr lines, rc 0
```
**Scores:** Basic 24/40 | Specialized 33/60 | Total 57/100
**Assertions:** [PASS] SE / nanopore handled - [FAIL] empty or all-unmapped gets a message - [FAIL] unindexed gets an actionable message - [FAIL] shell validators signal failure - [PASS] read-only. 2/5.

## Input 5 - Stress: per-chromosome strand, MAPQ, coverage balance (58)
**Prompt:** "Give me strand balance per chromosome, the MAPQ distribution, and a per-chromosome coverage / aneuploidy check on the 1000G BAM and the RNA BAM."
**Ran:** SKILL.md snippets 12-17 verbatim (`test_snippets.sh` T7-T11, `test_contam.sh`).
```
per-chromosome loop (chr1 chr2 chr3): region "chr1" specifies an invalid region ... / Runtime error: Divide by zero / chr1: F=0 R=0 ratio=   (both BAMs)
idxstats | awk '{print $1, $3/$2}' : awk: fatal: division by zero attempted   (last '*' line, length 0)
aneuploidy awk on 1000G BAM, gawk : fatal: division by zero attempted (median coverage 0)
                              mawk : function asort never defined
contigs surviving the regex : 846, of which 824 are not plain chr1..chr22 (chr1_KI270706v1_random ...)
mean MAPQ: human 59.97 (truth 59.99) ; 30%-unmapped fixture 41.995 (truth over mapped 59.99)
view -s 42.10: 576 reads twice, 0 split mates ; MAPQ histogram: 2 reads at MAPQ 0 = the 2 unmapped reads
```
**Scores:** Basic 25/40 | Specialized 33/60 | Total 58/100
**Assertions:** [PASS] -s subsample reproducible - [FAIL] chromosome loop clean - [FAIL] aneuploidy awk runs (default awk, zero coverage) - [PASS] MAPQ histogram exact - [FAIL] mean MAPQ over mapped reads. 2/5.

## Input 6 - Scope boundary: contamination and GC bias (69)
**Prompt:** "Also check for cross-sample contamination or a sample swap, and tell me whether there is GC bias."
**Ran:** `test_snippets.sh` T12-T14, T16, `test_contam.sh`.
```
Picard CollectGcBiasMetrics / CollectAlignmentSummaryMetrics : rc 0, files written
computeGCBias -b -g genome.2bit --effectiveGenomeSize 2913022398 -o --biasPlot : rc 0, gc_bias.txt + gc_bias.pdf
verifybamid2 --SVDPrefix .../1000g.b38.vcf.gz.SVD  : "Open file ...1000g.b38.vcf.gz.SVD.bed failed, exit!" rc 1
verifybamid2 --SVDPrefix .../1000g.phase3.10k.b38.vcf.gz.dat : "2 SNP markers remained ... Insufficient Available markers" (100 kb slice)
somalier extract : needs chr1 in the FASTA (whole-genome reference not available) ; relate --infer flag exists
CrosscheckFingerprints I= I= HAPLOTYPE_MAP= : syntax accepted, fails only on the missing map file
```
**Not executed end-to-end:** somalier relate, CrosscheckFingerprints, a real FREEMIX (no whole-genome BAM or haplotype map on this machine).
**Scores:** Basic 29/40 | Specialized 40/60 | Total 69/100
**Assertions:** [PASS] Picard GC/summary run - [PASS] computeGCBias flags run - [FAIL] verifybamid2 prefix resolves - [FAIL] "GC bias < 1.2x" maps to an output column - [PASS] somalier / Crosscheck options exist. 3/5.

## Input 7 - Adversarial: "just say pass or fail" on a 30%-unmapped BAM (54)
**Prompt:** "Does this BAM pass QC? Don't explain, just pass or fail." (`lowmap_unplaced.bam`: 30% of pairs unmapped with RNAME `*`, true mapping rate 70.0%; `lowmap_placed.bam`: same rate, unmapped reads placed at the mate; plus the RNA BAM)
**Ran:** `matrix_idx.py`, `test_snippets.sh` T17, `test_validators.sh` V1, V4.
```
unplaced variant : validate_alignment.py  Mapped 100.0% -> "All metrics within normal range"   (truth 70.0%)
                   usage-guide AlignmentValidator      "Mapping rate: 100.0% PASS"
                   SKILL.md bash script                "Mapping rate: 70.00%"  (correct)
placed variant   : validate_alignment.py  "WARNINGS: Low mapping rate, Low proper pairing"  -> exit status 0, `&&` pipeline continues
                   usage-guide class: "Mapping rate: 70.0% FAIL", returns None
RNA BAM          : ALL_OK; the Skill text states thresholds and strandedness are assay-specific
```
**Scores:** Basic 23/40 | Specialized 31/60 | Total 54/100
**Assertions:** [FAIL] python validator flags the 70% BAM - [FAIL] usage-guide validator flags it - [PASS] bash script reports the true rate - [FAIL] failure is machine-readable (exit 0) - [PASS] assay-specific caveats stated. 2/5.

## Research Veto: PASS
M1 no fabricated identifiers or clinical values (unsourced conventions are hedged: "0.5-1% swap rate", "FREEMIX > 0.03 commonly used"); M2 no individual-level diagnostic content; M3 no principled methodological fallacy (metric-definition mismatches recorded as P1); M4 all four python blocks parse, every snippet and example executed; crashes only on edge inputs.

## Step 8 - Recommendations
P1
1. Validators miss unplaced unmapped reads: false PASS at 70% mapped (Inputs 7, 1).
2. Validators exit 0 on failure and the bash ones print no verdict (Inputs 4, 7).
3. `bc` truncation prints 99.96% as 90.0% / 99.00% (Inputs 1, 4).
4. Strand value printed by the bash snippets (F/R 1.0007) is not what the 0.48-0.52 band describes (Inputs 1, 5).
5. M5 diff false-alarms without M5 tags and cannot see name or assignment errors (Input 3).
6. Example python validator crashes on empty, all-unmapped and unindexed BAMs (Input 4).
7. CI-safe one-liner rejects valid BAMs under 1000 reads (Input 2).

P2
8. Production IGNORE recipe hides real defects (Input 2). 9. Per-chromosome loop, idxstats awk and aneuploidy awk are brittle (Input 5). 10. verifybamid2 prefix, Picard fraction-vs-percent units and the GC-bias 1.2x band (Inputs 6, 1). 11. Mean-MAPQ helper counts unmapped reads; thresholds disagree across three files (Input 5). 12. usage-guide duplicates SKILL.md; small text inconsistencies (static).

## Key strengths
The two-validation framing is right and measured (quickcheck 3/21, Picard 18/21 planted defects, and the Skill says so); every flag named exists in current tool versions; strong assay caveats; pysam-route metrics match Picard and samtools.

## Not executed / not verified
somalier relate and CrosscheckFingerprints with real data, a real FREEMIX estimate, head-of-file bias beyond 100,000 reads (largest BAM 15,788 records), CRAM input, Picard PDF output on a host without R. Unsourced: "sample-swap rates 0.5-1%", "FREEMIX > 0.03".

## Cleanup
`find` for `__pycache__` in `external/.../alignment-validation` found none; no symlinks in `run/`; real-file copies (`run/data/idx`) and scratch dirs deleted after the runs (regenerable with `matrix_idx.py`).

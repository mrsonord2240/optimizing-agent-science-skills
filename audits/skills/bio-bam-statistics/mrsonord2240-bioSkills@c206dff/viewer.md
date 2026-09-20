> **Audit record for `bio-bam-statistics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/bam-statistics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-bam-statistics

Generated: 2026-09-20 | Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/bam-statistics` (read-only, first audit)
Skill files: `SKILL.md` (427 lines), `usage-guide.md` (217), `examples/qc_report.py` (54). Audited from a copy in `run/skill/` (bytes identical to c206dff modulo CRLF); no `__pycache__` in the staging clone.
Environment: WSL `science`, env `alignment-files` — samtools 1.24, pysam 0.24.1, mosdepth 0.3.14, bedtools 2.31.1, bcftools 1.24, Picard 3.5.0, MultiQC 1.35, plot-bamstats. All scripts are in `run/`, outputs in `run/out/`.

**Final: 71 / 100 — Beta Only — not deployable. No veto. Executed 7/7 inputs (input 6 partly).**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical — real human PE BAM, flagstat/idxstats/stats/coverage | 34 | 50 | 84 | 4/5 PASS | ✅ |
| 2 | Variant A — mean depth / breadth, real human BAM, every tool | 27 | 35 | 62 | 2/5 PASS | ⚠️ |
| 3 | Edge — SYNTHETIC BAM with every flag category planted | 31 | 44 | 75 | 3/5 PASS | ✅ |
| 4 | Variant B — depth cap: SYNTHETIC 9500x stack + real ARTIC nanopore | 31 | 45 | 76 | 3/5 PASS | ✅ |
| 5 | Stress — 8-BAM batch loop, plot-bamstats, MultiQC | 33 | 48 | 81 | 3/4 PASS | ✅ |
| 6 | Scope boundary — RF insert size, soft-clip detector, HsMetrics, contamination | 28 | 34 | 62 | 3/5 PASS | ⚠️ |
| 7 | Adversarial — empty / SE / unindexed BAM, MT contig naming | 23 | 27 | 50 | 3/5 PASS | ❌ (PARTIAL) |

**Execution Average: 70.0 / 100** (Layer 1 avg 29.6/40, Layer 2 avg 40.4/60) | **Assertion Pass Rate: 21/34 (61.8%)**
**Static: 73/100 x 0.4 = 29.2 | Dynamic: 70.0 x 0.6 = 42.0 | FINAL 71.2 -> 71**
Floors: static >= 70 met; execution avg < 75, Layer 2 avg < 42 and assertion rate < 80% all missed -> Limited Release not reachable; 71 is Beta Only anyway.

## Step 1 — Skill Veto: PASS

- T1 stability PASS: `examples/qc_report.py` 10/10 successful consecutive runs; the depth/stats tools ran on every input (`out/t0_determinism.txt`).
- T2 contract PASS: frontmatter has `name`, `description`, `tool_type`, `primary_tool`, `license`.
- T3 determinism PASS: flagstat, idxstats, stats, coverage, depth -a, mosdepth per-base and qc_report.py gave byte-identical output on two runs.
- T4 security PASS: grep for `eval(`, `exec(`, `os.system`, `subprocess`, `shell=True`, credentials found nothing; batch loop quotes `"$bam"`.

## Step 2 — Static score (25 criteria) = 73/100

| Category | Score | Note |
|---|---|---|
| Functional suitability | 8/12 | Completeness 3, Correctness 2, Appropriateness 3. Wide coverage, but verified errors listed under Findings |
| Reliability | 7/12 | Fault tolerance 2, Error reporting 2, Recoverability 3 |
| Performance & context | 6/8 | Token cost 3, Efficiency 3 (usage-guide repeats most recipes) |
| Agent usability | 11/16 | Learnability 3, Consistency 2 (snippets disagree with each other), Feedback 3, Error prevention 3 |
| Human usability | 5/8 | Discoverability 3, Forgiveness 2 |
| Security | 11/12 | Credentials 4, Input validation 3, Data safety 4 |
| Maintainability | 8/12 | Modularity 3, Modifiability 3, Testability 2 |
| Agent-specific | 17/20 | Trigger 3, Disclosure 3, Composability 4, Idempotency 4, Escape hatches 3 |

## Step 3 — Classification

Category 3 Data Analysis (QC statistics and coverage computation from alignments). Mode D (CLI recipes + Python snippets + one shipped script). Complexity: **Complex** (7+ task types across 6 tools, branching by assay, broad scope) -> N = 7.

Shipped-means-present (gate 8): `examples/qc_report.py` exists and runs; every Related Skill named exists (`sam-bam-basics`, `alignment-indexing`, `alignment-validation`, `duplicate-handling`, `alignment-filtering`, `sequence-io/sequence-statistics`). No missing primary file.

## Independent-truth method

`run/truth.py` recounts every flag category straight from record flags with pysam (primary/secondary/supplementary/QC-fail split per the SAM spec) and builds per-base depth from `read.get_blocks()` (no pileup engine), with a mates-counted-once variant. Synthetic data (`run/make_synth.py`, seed 20260920, **all SYNTHETIC**, in `run/data/`) has counts fixed by construction. `run/check_counts.py` compares flagstat/stats/idxstats with both.

---

## Detailed Outputs

### Input 1 — Canonical (REAL data)
**Prompt:** "Run flagstat, idxstats and samtools stats on `test.paired_end.sorted.bam`. Give me the read count, mapping rate, properly-paired %, insert size, error rate and per-chromosome counts."
**Executed:** yes — `run/t1_canonical.sh`, `run/check_counts.py`, `run/skill_snippets.py`, `skill/examples/qc_report.py` (copy). Data: `public-data/human/test.paired_end.sorted.bam` copied to `run/work/`.

Key output:
```
5644 + 0 in total ... 5642 + 0 primary ... 2 + 0 secondary ... 5642 + 0 mapped (99.96%) ... 5640 + 0 primary mapped ... 5638 + 0 properly paired (99.93%)
idxstats: chr22 40001 5642 0 / * 0 0 2
PASS flagstat total(pass+fail) == hand total observed= 5644 expected= 5644   ... 15/15 PASS, SUMMARY FAILS= 0
stats: raw total sequences 5642; error rate 2.014930e-03; insert size average 124.8 (125.7 with -m 1.0)
samtools coverage: chr22 1 40001 5640 1181 2.95243 16.7743 40.9 60
--- Skill pysam "Count Reads":  Total: 5644  Mapped: 5642 (100.0%)  Properly paired: 5640 (99.9%)
--- Skill insert-size snippet: Mean insert size: 126
--- shipped qc_report.py: Total 5,644  Mapped 5,642 (100.0%)  Properly paired 5,640 (99.9%)  Secondary 2  Insert mean 126 median 123
--- Skill awk mito on a BAM without chrM: "0% mitochondrial"
```
Hand count (truth.py): primary 5642, primary mapped 5640, proper (primary) 5638, secondary 2, NM sum 1352 (= error rate 2.0149e-3).
**Scores:** Basic 34/40 | Specialized 50/60 | Total 84/100 — CLI path exactly right; pysam snippets count the 2 secondary records as mapped/proper.
**Assertions:**
- [PASS] flagstat/stats/idxstats equal the independent hand count (15/15).
- [PASS] error rate and coverage meandepth equal hand values (2.0149e-3; 16.7743).
- [FAIL] Skill pysam "Count Reads" reproduces flagstat's mapped/proper counts — 5642/5640 vs 5640/5638; 100.0% vs 99.96%.
- [PASS] shipped qc_report.py runs from a clean copy and prints a checked report.
- [PASS] idxstats counts secondary in the mapped column as the Skill says (5642 = 5640 + 2).

### Input 2 — Variant A (REAL data)
**Prompt:** "Calculate mean coverage depth for this BAM and what percentage of the genome is covered at 10x and 20x. Also get depth statistics for the target region chr22:1952-4617."
**Executed:** yes — `run/t2_coverage.py` (via `t2_coverage.sh`), `run/t2b_pysam_defaults.py`, `run/t8_mosdepth_plots.sh`, `run/t10_misc.sh`, `run/t10b.sh`.

Key output (human chr22 slice, 40001 bp, truth from blocks):
```
TRUTH (overlaps double counted)      mean 16.7743 covered 1181 pct 2.9524 ge10 2.4299 ge20 2.3424 max 2532
TRUTH (mates counted once)           mean 8.8603  ... ge10 2.3549 ge20 2.0024 max 1269
samtools depth -a                    16.7743  (same as truth 1)     samtools depth -a -s   8.8603 (same as truth 2)
SKILL recipe "samtools depth | awk sum/n" (no -a): mean = 568.1533 over 1181 covered positions      <-- WRONG by 34x
SKILL recipe ">=10x/>=20x" (no -a): 82.3% / 79.3%   (true 2.430% / 2.342%)                             <-- WRONG
samtools coverage: chr22 1 40001 5640 1181 2.95243 16.7743 40.9 60
mosdepth default 8.86 (mates once) | mosdepth --fast-mode 16.77 | bedtools genomecov 16.7761
SKILL pysam mean_depth()     579.7044   (mean over pileup columns only)
SKILL pysam coverage_stats() length 40001 covered 1157 pct 2.8924 mean 16.7675   (24 orphan-flagged positions lost)
Window 1951-4617: truth 251.68 | SKILL mean_depth() 579.70 | coverage_stats 251.58
mosdepth --by exome.bed --thresholds 1,10,20,30,100:  1181 942 801 776 644 ; region mean 132.94   == truth 1181/942/801/776/644, 132.9411
samtools coverage -b exome.bed in.bam  ->  "Cannot open file list "exome.bed""    (-b is --bam-list)
samtools coverage -r chr22:1952-4617   ->  chr22 1952 4617 5640 1181 44.2986 251.684 40.9 60
pysam skill_depth_at('chr22', 2999, 3000): 232 columns printed (2907-3138); requested position 1562 correct (samtools depth chr22 3000 = 1562)
```
`run/t2b_pysam_defaults.py`: pysam pileup drops paired-not-proper reads by default (`ignore_orphans=True`: synthetic synth2 total depth 2000 vs samtools depth 3500); `min_base_quality` / `ignore_overlaps` do not change `pileup.n`.
**Scores:** Basic 27/40 | Specialized 35/60 | Total 62/100
**Assertions:**
- [PASS] samtools coverage meandepth/covbases equal truth.
- [FAIL] Quick Reference "Mean depth" one-liner gives the true mean (568.15 vs 16.77).
- [FAIL] usage-guide >=10x/>=20x one-liner gives true breadth (82.3/79.3 vs 2.43/2.34).
- [PASS] mosdepth --by/--thresholds and the `depth -s` overlap caveat reproduce truth exactly.
- [FAIL] `samtools coverage -b regions.bed` works for BED regions (it is `--bam-list`).

### Input 3 — Edge (SYNTHETIC)
**Prompt:** "This BAM came from a messy pipeline. How many reads does it really contain, what's the mapping rate, how many duplicates, how many QC-failed, and what fraction of primary mapped reads is MAPQ>=30 and mitochondrial?"
**Executed:** yes — `run/make_synth.py` (SYNTHETIC `data/synth.bam`, 540 records, counts by construction), `run/t3_edge_flags.sh`, `run/check_counts.py`.

Planted: 520 primary, 10 secondary, 10 supplementary, 20 QC-fail, 40 duplicates, 15 unmapped records (10 fully unmapped + 5 unmapped mates), 5 singletons, 20 mate-on-other-chr, 480 proper-flagged, 40 chrM reads.
```
520 + 20 in total ... 500 + 20 primary ... 10 + 0 secondary ... 10 + 0 supplementary ... 40 + 0 duplicates
505 + 20 mapped (97.12% : 100.00%) ... 485 + 20 primary mapped ... 460 + 20 properly paired (92.00% : 100.00%) ... 5 + 0 singletons ... 20 + 0 mate other chr
idxstats: synth1 20000 435 5 / synth2 5000 50 0 / chrM 2000 40 0 / * 0 0 10
15/15 count checks PASS (flagstat 10, stats 3, idxstats 2)
SKILL cross-check: flagstat_total(first column) - sec - supp = 500 ; pass+fail version = 520 ; stats raw total sequences = 520   -> FAIL as literally written
Skill pysam Count Reads: Total 540  Mapped 525 (97.2%)  Properly paired 480 (88.9%)   (flagstat 92.0% on QC-passed, 92.3% on primary)
shipped qc_report.py: Duplicates 40 (7.4%) Secondary 10 Supplementary 10 Insert mean 171 median 150
samtools view -c -F 2308 -q 30 = 485 ; -F 2308 = 505   -> 96.0%
Skill idxstats mito awk: 7.61905% (= 40/525; primary-only 7.92%)
samtools stats: reads mapped and paired 500 ; reads properly paired 480  (the Skill lists "mapped and paired" as "Properly paired")
```
**Scores:** Basic 31/40 | Specialized 44/60 | Total 75/100
**Assertions:**
- [PASS] flagstat/stats/idxstats reproduce every planted count (15/15).
- [FAIL] the Skill's cross-check identity holds as written (500 vs 520: the QC-failed column is unexplained).
- [FAIL] pysam Count Reads / qc_report.py properly-paired % equals flagstat (88.9% vs 92.0%).
- [PASS] `-F 2308 -q 30` fraction correct (485/505).
- [PASS] idxstats mito awk gives the value the documentation implies (7.62%).

### Input 4 — Variant B (SYNTHETIC + REAL)
**Prompt:** "My ARTIC amplicon / UMI-collapsed BAM has some positions above 8000x. Give me max depth and mean depth without the cap distorting it."
**Executed:** yes — `run/t4_deep_cap.py` (via `t4.sh`), `run/t4b_artic.sh`, `run/t4c_deletions.sh`. Synthetic `data/deep.bam`: 9500 reads at amp:101-200, 500 reads at amp:301-400, 1 kb contig (truth: max 9500, mean 1000, total 1,000,000).
```
samtools depth (default) max = 9500 | depth -d 100 max = 9500 | depth -m 100 max = 9500       (depth -d silently ignored, as the Skill says)
samtools coverage meandepth = 1000 ; coverage -d 8000 meandepth = 850
samtools mpileup default (-d 8000) max = 8000 ; mpileup -d 1000000 max = 9500                    (Skill advice verified)
bcftools mpileup default: DP=250 at a 9500x position                                             (cap not mentioned by Skill)
mosdepth summary: amp 1000 1000000 1000.00 0 9500
SKILL pysam pileup default   max = 8000  mean = 850.0 ; max_depth=1000000: max 9500 mean 1000.0
SKILL mean_depth() = 4250.0 ; coverage_stats mean = 850.0  (truth 1000.0)
orphans (synth2): pysam default total depth 2000 | ignore_orphans=False 3500 | samtools depth 3500
REAL ARTIC nanopore BAM (MN908947.3): truth/depth -a/coverage/genomecov/mosdepth = 68.8373 x, 29826 covered; pysam and mosdepth --fast-mode 69.97
sum of pileup reads that are not deletion/refskip = 68.837 (pileup.n counts deletions)
```
**Scores:** Basic 31/40 | Specialized 45/60 | Total 76/100
**Assertions:**
- [PASS] depth, coverage and mosdepth return planted max 9500 / mean 1000.
- [PASS] mpileup 8000 cap, `-d 1000000` fix, `depth -d` ignored — all as the Skill states.
- [FAIL] Skill pysam pileup recipes reproduce mean 1000 (850; mean_depth 4250).
- [FAIL] cap warning covers pysam (max_depth 8000) and bcftools mpileup (-d 250).
- [PASS] on real ARTIC data all depth tools agree with truth.

### Input 5 — Stress (REAL + SYNTHETIC)
**Prompt:** "Create a summary table of statistics for all my samples (here: 8 BAMs), then make QC plots and a MultiQC report."
**Executed:** yes — `run/t5_batch.sh` (usage-guide loop verbatim), `run/t5b_rates.py`, `run/t8_mosdepth_plots.sh`, `run/t6_scope.sh` (MultiQC part).
```
Sample           Total  Mapped  Paired  Duplicates
artic_nanopore   4916   4916    0       0
g1000            9601   9563    9450    101
human_pe         5644   5642    5638    0
human_rna        8828   8828    7042    0
planted_dups     500    500     500     0
sc2_pe           200    197     192     0
sc2_se           100    100     0       0
synthetic_flags  520    505     460     40      <-- file has 540 records; 20 QC-failed dropped
```
Hand counts equal the table for every non-synthetic BAM (Total, Mapped, Paired, Duplicates); the "Paired" column is properly-paired; RNA "Total" includes 1786 secondary records. `plot-bamstats -p plots/` created the directory and 11 PNG + index.html. MultiQC 1.35 listed Samtools stats/flagstat/idxstats sources for the sample.
**Scores:** Basic 33/40 | Specialized 48/60 | Total 81/100
**Assertions:**
- [PASS] batch loop Total/Duplicates equal hand counts for 8/8 BAMs (incl. 1000G 101 duplicates).
- [PASS] plot-bamstats creates the directory and 11 plots.
- [PASS] MultiQC ingests samtools stats/flagstat/idxstats.
- [FAIL] loop accounts for every record (20 QC-failed silently omitted; "Paired" is properly-paired).

### Input 6 — Scope boundary (SYNTHETIC + REAL)
**Prompt:** "My mate-pair library shows no insert size section; check adapter read-through, off-bait rate and contamination too."
**Executed:** yes, partly — `run/t6_scope.sh`, `run/t9_stats_fields.sh`, `run/t8b_cram.sh`, `run/t8c.sh`. Not executed: the assay threshold table (no matching data). VerifyBamID2 ran but returned "No reads found in any of the regions" (100 kb slice), so FREEMIX was not verified.
```
RF library (SYNTHETIC, 100 pairs, insert 2000), proper flag SET and UNSET:
  insert size average: 2000.0 ; inward oriented pairs: 0 ; outward oriented pairs: 100 ; IS rows with count>0: 1 (IS 2000 100 ...)   <-- not empty (both cases)
  qc_report.py (proper-pair based): "Properly paired: 200 (100.0%)" / "0 (0.0%)" and no insert-size lines when the flag is unset
samtools stats | grep -ci soft: 0 on real BAM (863 soft-clipped bases by CIGAR) and 0 on synthetic BAM (400 planted). SN keys with clip/trim: only "bases trimmed: 0"
Picard 3.5.0 CollectHsMetrics: PCT_OFF_BAIT 0, PCT_SELECTED_BASES 1, FOLD_80_BASE_PENALTY "?", AT_DROPOUT 0, GC_DROPOUT 0, MEAN_TARGET_COVERAGE 124.74, TOTAL_READS 5642
samtools dict genome.fasta: M5:1922b52e...  (test BAM header has no M5, so the header comparison has nothing to compare)
CRAM: samtools stats -r genome.fasta x.cram -> "Failure while decoding file"; with --reference genome.fasta -> raw total 5642, error rate 2.01493e-03
mosdepth on the CRAM: "index not found ... must be indexed" until `samtools index`; then summary equals the BAM (8.86)
```
**Scores:** Basic 28/40 | Specialized 34/60 | Total 62/100
**Assertions:**
- [PASS] Picard CollectHsMetrics fields exist as named.
- [FAIL] `samtools stats | grep "bases soft-clipped"` returns a value (no such line in 1.24).
- [FAIL] RF library leaves the IS section empty (stats reports 100 outward pairs).
- [PASS] out-of-scope QC handed to Picard/VerifyBamID2/somalier without individual-level diagnosis.
- [PASS] no clinical/diagnostic conclusion.

### Input 7 — Adversarial (SYNTHETIC + REAL SE)
**Prompt:** "Run your recipes on these: an empty BAM, a single-end BAM, a BAM without an index, and one with Ensembl contig names (MT). flagstat says 99% mapped, so it's all fine, right?"
**Executed:** yes — `run/t7_adversarial.sh`, `run/t7b_se.sh` (`data/empty.bam`, `se.bam`, `noindex.bam`, `work/synth_MT.bam`; real nf-core SE BAM).
```
empty.bam:  Skill pysam Count Reads -> ZeroDivisionError ; qc_report.py -> ZeroDivisionError ; awk mean depth -> "fatal: division by zero"; mito awk -> division by zero
            flagstat prints "0 + 0 mapped (N/A : N/A)" ; samtools coverage prints zeros ; mosdepth writes empty outputs (rc 0)
real SE BAM (sc2_se.bam): Skill Count Reads prints Total 100 / Mapped 100 then ZeroDivisionError (paired == 0, rc 1); insert-size snippet ZeroDivisionError; qc_report.py fine
se.bam:     Skill awk mito -> "0% mitochondrial" (no chrM)
noindex.bam: samtools idxstats -> works (slow-scan fallback, rc 0, warning); pysam get_index_statistics -> ValueError; mosdepth -> "error alignment file must be indexed"
MT rename:  idxstats "MT 2000 40 0"  but Skill awk -> "0% mitochondrial"
usage-guide sex check on BAM without chrX/chrY -> "X:Y = 0.00"
```
The Skill's "What Flagstat Does Not Reveal" section answers the "99% means fine" trap correctly.
**Scores:** Basic 23/40 | Specialized 27/60 | Total 50/100 (status PARTIAL)
**Assertions:**
- [FAIL] Count Reads / flagstat-equivalent / insert-size snippets run on SE and empty BAMs.
- [PASS] shipped qc_report.py handles a single-end BAM.
- [FAIL] mito % / X:Y recipes flag a missing contig instead of printing 0.
- [PASS] Troubleshooting "samtools index" resolves the unindexed failures (the "idxstats requires an index" claim itself is stale in 1.24).
- [PASS] no destructive or unsafe operation recommended.

---

## Step 6 — Research Veto (Data Analysis): PASS

- M1 Scientific integrity PASS — nothing invented; every printed statistic checked.
- M2 Practice boundaries PASS — QC only, no diagnosis; contamination/enrichment handed off.
- M3 Methodological ground PASS — no principled fallacy in the recommended tools. The covered-position denominator in the awk mean-depth / >=Nx recipes (568x vs 16.8x) is a P1 correctness defect; correct alternatives sit in the same document, so not a veto.
- M4 Code usability PASS — snippets parse and run on normal PE data, qc_report.py 10/10; one wrong flag, one nonexistent stats field and division-by-zero on SE/empty input are P1s.
Safety/scope assertions: none failed.

## Findings (P0 / P1 / P2)

No P0 (no veto, no safety-assertion failure, score >= 60).

**P1**
1. Mean-depth and >=Nx recipes divide by covered positions (Input 2): 568x vs 16.77x; 79.3% vs 2.34%; pysam `mean_depth()` 579.7.
2. pysam counting snippets and `qc_report.py` count secondary/supplementary/QC-fail (Inputs 1, 3): proper-pair 88.9% vs 92.0%.
3. pysam pileup recipes silently cap depth at 8000 and drop orphans (Input 4): mean 850 vs 1000; cap warning omits pysam and bcftools (-d 250).
4. `samtools coverage -b regions.bed` is not a BED option (Input 2).
5. `grep "bases soft-clipped"` targets a stats field that does not exist in 1.24 (Input 6).
6. "Insert Size Caveats": stats reports an RF library's insert size (Input 6).
7. Snippets crash / print silent 0% on SE, empty and MT-named data (Input 7).

**P2**
8. Cross-check identity and "primary = total minus supp" ignore the QC-failed column and secondary (Input 3).
9. "`reads mapped and paired`" listed as properly paired (500 vs 480, Input 3).
10. Mate-overlap defaults differ 2x across tools (16.77x vs 8.86x) and are not tabulated (Input 2).
11. `pileup()` single-position snippet lacks `truncate=True` (232 columns for a 1-bp query).
12. Batch loop drops QC-failed reads and mislabels columns (Input 5).
13. Stale/incomplete notes: idxstats index, CRAM (`stats --reference`, mosdepth `.crai`), plot-bamstats `perl-URI` (tooling-pass observation, not re-run here), `depth -r` "Single chromosome" comment.
14. Unverified: "mosdepth 3-10x faster", assay-threshold values, historic depth-cap attribution; SKILL.md / usage-guide.md recipes duplicated and already diverging.

## Key strengths
- Every CLI number matched an independent hand count on real and planted-truth BAMs (30/30 count checks, 8/8 batch rows, mosdepth thresholds exact).
- Verified pitfall content: primary vs secondary/supp denominators, mpileup 8000 cap, `depth -d` ignored, `depth -s` overlap halving, mosdepth 1796/3844 flag semantics.
- Assay-specific QC framing and honest hand-offs to Picard, VerifyBamID2, somalier.
- Shipped example runs from a clean copy; deterministic; no security surface; plot-bamstats and MultiQC work.

## Housekeeping
`run/work/` intermediates trimmed; no symlinks; no `__pycache__` in `run/` or in `F:\OpenScience\external\...\bio-bam-statistics`. `data/synth.truth.json` first recorded `primary_mapped` as 510 (arithmetic slip); the planted arithmetic is 505 (520 primary - 15 unmapped) and the tools and hand count agree at 505; corrected in `make_synth.py`.

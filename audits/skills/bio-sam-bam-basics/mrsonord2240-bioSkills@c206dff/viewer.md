> **Audit record for `bio-sam-bam-basics`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@c206dff](https://github.com/mrsonord2240/bioSkills/tree/c206dff76d081a5126f8497fbabe10995c9b6026/alignment-files/sam-bam-basics) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-20 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-sam-bam-basics
Generated: 2026-09-20
Source: `mrsonord2240/bioSkills@c206dff76d081a5126f8497fbabe10995c9b6026:alignment-files/sam-bam-basics` (unchanged at HEAD 7478de2; verified with `git diff`). First audit.
Auditor ran everything from a COPY at `run/skill/` (clone under `external\` untouched; no `__pycache__` in it). Tools: samtools/htslib 1.24, pysam 0.24.1, bcftools 1.24, bwa 0.7.19, bwa-mem2 2.2.1, minimap2 2.31, bowtie2 2.5.5, hisat2 2.2.3, STAR 2.7.11b (WSL `science`, env `alignment-files`), Rsamtools 2.22.0 (Windows, `r.sh`).

Reproduce: `F:/OpenScience/audit-envs/alignment-files/wsl_run.sh 'bash /mnt/openscience/audits/bio-sam-bam-basics/run/run_all.sh < /dev/null'`. Every claim check is printed as `[PASS]/[FAIL]/[NOTE]` in `run/out/in*.txt` and appended to `run/out/results.jsonl` (235 rows: 165 pass, 7 fail, 63 observation notes are the raw counts across the five input scripts).

## Classification
Category 3 Data Analysis (bioinformatics code/CLI patterns), Mode D (SKILL.md instructions + 2 shipped examples), Moderate (4 files, several task types) -> N = 5 inputs.

## Step 1 — Skill Veto: PASS
| T1 Stability | T2 Contract | T3 Determinism | T4 Security |
|---|---|---|---|
| PASS: every documented snippet and both examples run on their documented input | PASS: `name`, `description`, `license` present | PASS: commands are deterministic; the same checks passed/failed on repeated full runs (aligner tie-breaking uses fixed inputs) | PASS: no eval/exec, no secrets; helper quotes its variables |

Shipped-means-present (gate 8): every path the docs point at exists (`examples/convert_formats.sh`, `examples/view_bam.py`; the seven Related Skills `bio-alignment-indexing/-sorting/-filtering/-validation`, `bio-bam-statistics`, `bio-reference-operations`, `bio-read-sequences` all exist). No missing primary file.

## Step 2 — Static score 72 / 100
| Category | Score | Note |
|---|---|---|
| Functional suitability | 8/12 | correct core; false CRAM recipe, stale failure-mode claims, no multi-region snippet |
| Reliability | 7/12 | view_bam.py raw tracebacks / wrong CRAM stats; helper ignores reference for CRAM input, can overwrite its input |
| Performance & context | 5/8 | 373-line SKILL.md + 210-line usage-guide repeating it; no references/ |
| Agent usability | 12/16 | clear tables, strong footgun sections; unlabelled 0-based output, gaps above |
| Human usability | 6/8 | natural trigger words; rejects `.BAM`, no index hint |
| Security | 10/12 | no secrets/eval; no input==output guard (data loss observed) |
| Maintainability | 8/12 | duplicated facts across two docs; no expected outputs for examples |
| Agent-specific | 16/20 | Related Skills wired; version-drift instruction present |

## Summary Table
| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Executed | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical: inspect real PE BAM | 34 | 49 | 83 | 4/5 PASS | yes | ✅ |
| 2 | Variant A: conversions + helper | 34 | 49 | 83 | 4/5 PASS | yes | ✅ |
| 3 | Edge: synthetic corner cases | 33 | 49 | 82 | 4/5 PASS | yes | ✅ |
| 4 | Variant B: CRAM reference / integrity | 30 | 41 | 71 | 3/5 PASS | yes | ⚠️ |
| 5 | Stress: six aligners, MAPQ/tags/@PG | 35 | 48 | 83 | 4/5 PASS | yes | ✅ |

**Execution Average: 80.4 / 100** (Layer 1 avg 33.2/40, Layer 2 avg 47.2/60). **Assertion pass rate: 19/25 = 76%.** **Executed 5/5.**

## Research Veto: PASS (M1 PASS, M2 PASS, M3 PASS, M4 PASS)
M4 evidence: every snippet parsed and ran from a copy; imports exist; flags exist in samtools 1.24 (`--help` read). The false CRAM reachability recipe is recorded as a P1 correctness defect, not a methodological fallacy.

## Final: 0.4 x 72 + 0.6 x 80.4 = 28.8 + 48.2 = **77 -> Limited Release by score**
Floors (scoring_rubric section 5): Static 72 >= 70 ok; Execution 80.4 >= 75 ok; Layer 1 33.2 >= 28 ok; Layer 2 47.2 >= 42 ok; **assertion pass rate 76% < 80% fails** -> downgrade one tier: **GRADE Beta Only (⚠️), deployable false, veto_override false.** No P0.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Here is `test.paired_end.sorted.bam` (real nf-core human PE, 5644 records). Show me the header, decode the first reads (flag meaning, position, CIGAR), tell me how many reads are in the file and in chr22:2000-3000, whether pysam fetch gives the same answer as samtools, and show it from R too."
**Code:** `run/in1.py` (Skill commands via `samtools`, pysam snippets, independent FLAG decoder from the SAM spec), `run/in1b.py` (multi-region, -L, faidx), `run/in1_rsamtools.R` (Skill's R bullet), shipped `skill/examples/view_bam.py`.
**What ran / printed (trimmed):**
```
[PASS] samtools flags <n> agrees with independent spec decoder for every flag seen :: [83, 99, 147, 163]
[PASS] flag 147 read: is_read2, reverse; TLEN is negative :: testN:5 tlen=-135
[PASS] Skill 12-row FLAG table: each bit maps 1:1 to the pysam property named for it
[PASS] SAM POS (col 4) = pysam reference_start + 1 :: 1952 vs 1951
[PASS] Quick Reference equivalence: samtools chr:2000-3000 == fetch(chr,1999,3000) :: 2732 vs 2732
[PASS] boundary read ... missing from fetch(E,E+1) when copying coordinates verbatim :: E=2094: samtools 512, fetch(E,E+1)=493, fetch(E-1,E)=512
[NOTE] wrong contig name (22 vs chr22) samtools :: 0 | rc=0 | [main_samview] region "22:2000-3000" specifies an invalid region or unknown reference. Continue anyway.
[PASS] usage-guide "Could not retrieve index file" is the real message (samtools view region on unindexed BAM, rc=1)
[PASS] view_bam.py prints References: 1 / Mapped: 5642 / Unmapped: 2 ; testN:1  chr22:1951  +  130M13S   (0-based, unlabelled)
[FAIL] view_bam.py works on unindexed BAM :: ValueError: mapping information not recorded in index or index not available
[FAIL] SKILL.md SAM example, tab-delimited literally, is a valid SAM (illustrative only) :: [E::sam_parse1] CIGAR and query sequence are of different length
[NOTE] `samtools view -H` prints an extra @PG for the view command itself (--no-PG removes it)
[NOTE] multi-region call, overlapping regions: duplicated records / default / -M / union :: (1930, 7356, 5426, 5426)
[FAIL] GAP: naive `samtools view bam r1 r2` returns each record once :: default 7356 (1930 duplicated), -M 5426, union 5426; exit 0, no warning
Rsamtools 2.22.0 / scanBam records: 5644 / first read: testN:1 99 1952 130M13S 60 / ASSERTIONS OK
```
**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100
**Assertions:**
- [PASS] FLAG decoding equals an independent SAM-spec decoder — every flag and all 12 bits agree, TLEN signs as spec
- [PASS] Coordinate statements hold (POS vs reference_start, region vs fetch, faidx 1-based, boundary read footgun)
- [PASS] view_bam.py correct on the indexed BAM — 1/5642/2
- [FAIL] Safe degradation on no index / wrong contig / multi-region — crash, exit-0 empty result, 1930 silent duplicates
- [PASS] In scope, read-only, no fabricated values — R bullet also verified

### Input 2 — Variant A (conversion)
**Prompt:** "Convert my BAM to SAM, back to BAM, then to CRAM against the reference, then back to BAM; do the same with the Skill's convert_formats.sh and pysam. Confirm nothing was lost."
**Code:** `run/in2.py`, `run/in2_diff.sh`; Skill commands verbatim (`view -h -o`, `view -b -o`, `view -C -T`, `view -b -T`, pipe form), the pysam `w`/`wb`/`wc` snippets, and `skill/examples/convert_formats.sh`.
**What ran / printed (trimmed):**
```
[PASS] round-trip o.bam / pipe.bam: 5644 records identical
[PASS] Format table: SAM > BAM > CRAM in size :: {'o.sam': 1881176, 'o.bam': 176101, 'o.cram': 66597}
in2_diff.sh: core fields (1-11) diff lines: 0 ; tag SET identical 5644/5644 ; tag ORDER identical 2/5644   (CRAM moves NM/MD to the end)
[NOTE] samtools view -o x.bam (no -b) writes BAM (1f8b0804) ; -o x.cram (no -C) writes CRAM: format follows the extension in 1.24
[PASS] CRAM->BAM without -T and no REF_PATH fails loudly :: rc=1
[NOTE] BAM->CRAM WITHOUT -T: rc=0, warnings, "Enabling embed_ref" (help text says -C requires -T)
[PASS] aligned SAM lacking @SQ -> BAM recipe fails (needs -t ref.fai) :: [E::sam_parse1] no SQ lines present in the header
[PASS] pysam-written p.sam / p.bam / p.cram identical to original ; header['SQ'] snippet -> 'chr22: 40001 bp'
[NOTE] pysam 'rc' on a CRAM with no reference at all :: OSError: truncated file   (unhelpful)
[PASS] convert_formats.sh BAM->SAM, SAM->BAM, BAM->CRAM(+ref) ; CRAM without reference arg -> "Error: CRAM conversion requires reference.fa" rc=1
[PASS] convert_formats.sh CRAM->BAM passing reference as 3rd arg :: rc=0, "reference silently ignored for non-cram output"
[FAIL] convert_formats.sh uppercase extension .BAM :: Unknown output format: BAM
[NOTE] helper with input == output path :: rc=1 ; afterwards `samtools view -c h.bam` = 0 (input destroyed)
```
**Scores:** Basic 34/40 | Specialized 49/60 | Total 83/100
**Assertions:**
- [PASS] All documented conversions round-trip 5644 records with every field identical (tag order aside)
- [PASS] pysam conversions and mode strings behave as the usage-guide says
- [PASS] Helper does SAM/BAM/CRAM(+ref) correctly and errors cleanly on usage/reference/extension
- [FAIL] Helper safe for every advertised conversion — reference ignored for CRAM input, `.BAM` rejected, input==output destroys input
- [PASS] Format statements hold (sizes, header preserved, CRAM without reference fails loudly)

### Input 3 — Edge (SYNTHETIC)
**Prompt:** "This BAM came from a pipeline I do not trust: unmapped reads with positions, secondary/supplementary records, hard-clipped reads, RNA introns, MAPQ 255 and 0, a 66,000-op CIGAR, and there is also an empty BAM. Explain each read's FLAG and CIGAR, how many reference/query bases each consumes, and make sure my view/pysam commands behave."
**Code:** `run/make_synth.py` (15 hand-written records on 3 random contigs, seed 20260920 — SYNTHETIC), `run/in3.py` with a CIGAR consumption model written from the SAM spec table (M/I/S/=/X consume query; M/D/N/=/X consume reference).
**What ran / printed (trimmed):**
```
[PASS] usage-guide CIGAR 10M2I30M5D20M: spec query=62, ref=65; pysam reference_length agrees      (50M2I30M: 82/80)
[PASS] r2_spliced ... N (intron) is NOT counted as covered: 50 positions, span 1050 ; jump 128 -> 1129
[PASS] hard clip: query_length 30 vs infer_read_length 50 ; soft clip: query_length 56, query_alignment_length 47
[PASS] unmapped-but-placed read: is_unmapped, ctg1, reference_start 49, cigar None, reference_end None ; returned by region query
[PASS] -F 256 / -F 2304 / -F 2048 -> 14 / 13 / 14 of 15
[PASS] -q 255 keeps exactly the MAPQ-255 read ; pair TLEN +90 / -90, PNEXT cross-referenced, TLEN = rightmost end - leftmost start + 1
[PASS] 66000-op CIGAR: pysam 66000 ops, ref_len 33000, query_len 66000 (BAM CG tag expanded); samtools text CIGAR 132001 chars; region query ok
[PASS] calmd rebuilds NM/MD for =/X read: 10=1X9=  NM:i:1  MD:Z:10T9
[PASS] empty BAM: view -c 0, pysam yields 0 reads
[FAIL] view_bam.py on an empty, unindexed BAM works :: ValueError: mapping information not recorded in index
[NOTE] view_bam.py row for unplaced unmapped read :: r5_unmapped_unplaced  None:-1  +  None ; given a SAM: AttributeError: AlignmentFile.mapped only available in bam files
```
**Scores:** Basic 33/40 | Specialized 49/60 | Total 82/100
**Assertions:**
- [PASS] CIGAR semantics (N, S, H, M, =/X, P) match pysam and the spec model on 13 CIGARs
- [PASS] Secondary vs supplementary filter arithmetic and flag bits
- [PASS] Unmapped-with-position, `*` SEQ, MAPQ 255/0, TLEN sign, 66,000-op CIGAR, empty BAM handled as implied
- [FAIL] view_bam.py copes with edge inputs — empty/unindexed crash, no unmapped marker, SAM AttributeError
- [PASS] Skill covers the prompt with general knowledge; no explicit consumption table or TLEN-sign statement (P2)

### Input 4 — Variant B (CRAM offline)
**Prompt:** "Our HPC nodes have no internet. I need to archive these BAMs as CRAM and read them back. How does samtools find the reference, how do I cache it, how do I prove a CRAM is readable, and is `archive` lossy?"
**Code:** `run/in4.py`, `run/in4b.py` (real BAM + genome.fasta; private FASTA copy that is moved away; `seq_cache_populate.pl`; poisoned copies of the reference named by the true M5; bogus `http_proxy`). Note: `samtools view -c` does not decode CRAM bases, so every reachability test uses a full decode and asserts on rc and record count.
**What ran / printed (trimmed):**
```
[PASS] reference unreachable: full decode FAILS loudly (rc != 0, 0 records)
[PASS] "samtools view -c file.cram forces full decode; proves reference reachable" -> FALSE in 1.24: -c returns the count, rc 0, with NO reference :: '5644\nrc=0'
[PASS] a working reachability proof: `samtools view -o /dev/null file.cram` gives rc != 0 when reference is unreachable
[PASS] quickcheck -v passes (rc 0) even though the reference is unreachable ("header + EOF only")
[PASS] mid-file corruption: quickcheck rc 0 but a FULL decode fails ; `view -c` => 5644 rc=0 (also blind)
[PASS] seq_cache_populate.pl writes cache/19/22/b52e1af6977302717072ebaca0a1 ; REF_CACHE=<root>/%2s/%2s/%s + REF_PATH=$REF_CACHE decodes offline (also REF_PATH alone, REF_CACHE alone)
[PASS] REF_CACHE consulted BEFORE REF_PATH: cache-first-poison rc=1; path-poison rc=0 n=5644
[PASS] -T beats a poisoned cache/path ; UR is last: UR only rc=1, +REF_PATH rc=0
[PASS] no network lookup by default: no ebi/ena/proxy mention with a bogus proxy; libhts.so holds 0 "ebi.ac.uk/ena/cram" strings
[PASS] --output-fmt-option archive accepted; sizes {'fast': 78600, 'normal': 66569, 'small': 65051, 'archive': 64152}; records identical
[PASS] embed_ref (never mentioned in the Skill) gives a CRAM that decodes with no reference reachable
[PASS] (i) CRAM read with a 1-base-different reference: hard error "MD5 checksum reference mismatch", rc 1 -- NOT silent corruption
[PASS] (ii) BAM converted against the wrong reference, read with the right one: hard error
[PASS] silent corruption only with --input-fmt-option ignore_md5=1 :: 129 reads decoded with a wrong base, rc 0
[PASS] view_bam.py on an indexed CRAM prints "Mapped: 0 / Unmapped: 0" (pysam .mapped=(0,0); samtools idxstats says 5642 / 2)
[FAIL] view_bam.py works on an indexed CRAM (prints Mapped: 5642)
```
**Scores:** Basic 30/40 | Specialized 41/60 | Total 71/100
**Assertions:**
- [PASS] Resolution order, cache-populate layout and offline recipe all verified with poisoned caches
- [PASS] No built-in ENA lookup (>=1.22), archive lossless and smallest, quickcheck caveat correct
- [FAIL] "`samtools view -c` forces full decode; proves reference reachable" — false; passes with no reference and on a corrupted CRAM
- [FAIL] "A different reference silently corrupts bases" — hard MD5 error in 1.24; silent only with ignore_md5=1
- [PASS] In scope; `-C` without `-T` disclosure (exit 0, embeds reference) recorded

### Input 5 — Stress (six aligners; SYNTHETIC reads + real STAR RNA BAM)
**Prompt:** "I received BAMs from bwa, bwa-mem2, minimap2, bowtie2, hisat2 and STAR. For each: which MAPQ scale, what -q threshold is sane, which of NM/MD/NH/HI/RG/MC/ms are present, which aligner made it (@PG), and does fixmate/markdup behave as the Skill says?"
**Code:** `run/make_reads.py` (29.7 kb random genome with 2-, 3- and 6-copy repeat families, 2500 simulated pairs, seed 7 — SYNTHETIC), `run/in5.sh` (all aligners + `collate | fixmate -m | sort | markdup` chain), `run/in5.py`.
**What ran / printed (trimmed):**
```
MAPQ histograms  bwa {0:26,...,60:4571}  mm2 {...,60:4833}  hisat2 {0:47,1:1807,60:4452}  bowtie2 {1:26,...,42:4870}  STAR {0:882,1:658,3:372,255:4444}
[PASS] bwa/bwa-mem2/minimap2: 0-60, max 60 ; HISAT2 within {0,1,60} ; Bowtie2 max 42 ; STAR exactly {0,1,3,255}
[PASS] STAR MAPQ = f(NH): 1 locus->255, 2->3, 3-4->1, >=5->0 :: {(0,5):390,(0,6):492,(1,3):426,(1,4):232,(255,1):4444,(3,2):372}
[PASS] Bowtie2 -q 60 -> 0 reads ; STAR -q 30 == -q 255 == -q 60 == 4444 unique
[FAIL] Bowtie2 "unique sentinel 42 (rare)" :: MAPQ 42 = 97.4% of records
[PASS] STAR HI:i 1-based by default, 0-based with --outSAMattrIHstart 0 ; bwa emits NM+MD, minimap2 NM only ; NH/HI from STAR, NH from HISAT2 ; bwa -R -> RG on 5000/5000
[PASS] '@PG | head -1' names the aligner for all six ; @PG chain bwa -> samtools -> samtools.1 .. .4 linear via PP
[PASS] fixmate -m adds ms:i and MC:Z
[PASS] markdup without ms/MC: "samtools markdup: error, no ms score tag. Please run samtools fixmate on file first." rc=1   (Skill says "silently wrong")
[PASS] bcftools mpileup output md5 identical with and without MD/NM tags (Skill: MD "required by bcftools mpileup BAQ")
[PASS] bcftools mpileup identical on minimap2 --eqx (=/X) BAM vs M BAM (Skill: "bcftools / Picard often need M")
[NOTE] real nf-core RNA BAM (STAR 2.7.10a): tags AS HI NH nM RG ; spliced reads present (805 with N)
```
**Scores:** Basic 35/40 | Specialized 48/60 | Total 83/100
**Assertions:**
- [PASS] MAPQ table rows verified with real aligner output
- [PASS] -q guidance behaves as stated
- [PASS] Tag, HI-base, @PG-chain and fixmate statements hold
- [FAIL] Failure-mode/compat notes accurate — markdup is loud, mpileup does not need MD, bcftools does not need M, Bowtie2 42 not rare
- [PASS] In scope, no fabricated numbers

---

## Findings (P0 none)
- **[P1] CRAM check: `samtools view -c` does not prove the reference is reachable** (in 4). Fix: `samtools view -o /dev/null file.cram && echo ok`.
- **[P1] Shipped view_bam.py fails or lies outside indexed BAM input** (in 1, 3, 4): ValueError unindexed/empty, AttributeError SAM, `Mapped: 0 / Unmapped: 0` on an indexed CRAM, unlabelled 0-based start, no unmapped marker.
- **[P1] Multi-region extraction trap** (in 1): overlapping regions give 7356 rows vs 5426 unique, exit 0; add `-M` / `-L bed`.
- **[P1] Wrong failure-mode/compat statements** (in 4, 5): markdup "silently", MD needed by mpileup BAQ, bcftools needs M, Bowtie2 42 "rare", different reference "silently corrupts".
- **[P1] convert_formats.sh**: reference ignored for CRAM input, `.BAM` rejected, input==output destroys input (in 2).
- **[P2]** duplicated SKILL.md / usage-guide; no explicit CIGAR consumption table, TLEN sign or MAPQ-255 statement; `view -H` adds an @PG; wrong contig exits 0; SAM example not parseable; `-C` without `-T` embeds the reference; CRAM re-orders tags; SA:Z is `;`-separated 6-field records; minimap2's `ms:i` is unrelated to fixmate's.

## Not verified (no way to run here)
DRAGEN MAPQ scale, Cell Ranger / STARsolo tags (CB/UB), fgbio "consensus tools reject input without MD", featureCounts NH behaviour, "production pipelines often reject inputs without a complete @PG chain". Recorded as unverified, not scored against the Skill.

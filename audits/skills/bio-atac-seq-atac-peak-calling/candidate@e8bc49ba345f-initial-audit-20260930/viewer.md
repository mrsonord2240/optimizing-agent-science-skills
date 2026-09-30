> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Audited working candidate `e8bc49ba345f27792466c23bfee96faa4898937641d32bd266c7e58f0f3a7658`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-atac-peak-calling`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/atac-peak-calling) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent. Initial diagnostic audit only; not a certification.
> - Data: ENCODE GM12878 ATAC chr1:1-30Mb filtered BAMs (ENCSR095QNB) and a synthetic planted-truth BAM (20 planted regions). Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-atac-peak-calling

Candidate: `sha256-manifest-v1 e8bc49ba345f27792466c23bfee96faa4898937641d32bd266c7e58f0f3a7658` (5 files), branch `fix/atac-atac-peak-calling` @ 3186916.
Category: 3 - Data Analysis - Mode D - Moderate, N = 5.
Environment: WSL `science`, micromamba `bio-atac-seq-atac-peak-calling` (macs3 3.0.4, macs2 2.2.9.1 + glibc shim, Genrich 0.6.2, samtools 1.24, bedtools 2.31.1) and `-idr` (idr 2.0.4.2, numpy 1.23.5). Fingerprint `08bd20df...02b6`.
Code: `scripts/a1_script_outputs.sh`, `a2_disjoint_pseudoreps.sh`, `a3_genrich_checks.sh`, `a4_misc_snippets.sh`, plus tooling-phase `smoke_script.sh`, `smoke_callers.sh`, `check_callers.py`. Output: `out/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (ENCODE-4 script) | yes | 28 | 36 | 64 | 2/5 | warn |
| 2 | Variant A (MACS3/MACS2, BAM vs BAMPE) | yes | 36 | 52 | 88 | 4/5 | pass |
| 3 | Variant B (Genrich) | yes | 30 | 42 | 72 | 2/4 | warn |
| 4 | Variant B (hmmratac) | yes | 32 | 46 | 78 | 2/3 | pass |
| 5 | Edge (NFR, blacklist, bigWig, grep chrM) | yes | 33 | 47 | 80 | 4/4 | pass |

**Execution Average: 76.4 / 100** - **Assertion Pass Rate: 14/21 (66.7 %)**
**Static: 75/100** - **Final: 76 (Beta Only)**: Limited Release tier cut by one because the assertion floor (80 %) and static floor are not met. Vetoes: none. Deployable: no.

Surface classifications: script (executed), MACS3/MACS2 callpeak (executed), Genrich (executed), macs3 hmmratac (executed), NFR recipe (executed), blacklist recipe (executed), bigWig recipe (executed, structure only), ROSE snippet (static-only, not installed), HOMER/nf-core/chromap/khmer (prose only, not applicable).

## Input 1 - Canonical: call_atac_peaks.sh on GM12878 rep1/rep2

Run (tooling phase `smoke_script.sh`, identical candidate bytes): exit 0. Parsed back: rep1 4,803 / rep2 4,366 / pooled 4,310 peaks; IDR true reps 1,197; rep1 pseudorep IDR 2,473; blacklist 1,188; both IDR PNGs produced; `Nt=1197 Nself=2473 ratio=2.066`.

Independent checks (`out/a1.log`, `out/a2_disjoint_pseudoreps.log`):

- The two pseudoreplicates share 131,281 of ~262k read names each (50%). They are independent subsamples, not halves.
- Disjoint halves of the same BAMs (`samtools view -s 1.5 -U`): N1=1,143, N2=1,249, Np=1,036 (IDR 0.05), Nt=1,197, so rescue 1.155 and self-consistency 1.093, both pass. At IDR 0.10 rep1 halves give 1,234, half the script's 2,473.
- The script's ratio therefore flags a passing library, and it never uses the pooled peak set or rep2 pseudoreplicates.
- ENCODE defines rescue = Np/Nt, self = N1/N2, fail only if both > 2 (ENCODE-DCC/atac-seq-pipeline `encode_task_reproducibility.py`); ENCODE macs2 uses tagAlign, `--call-summits`.

Findings: ATACPC-001, -002, -005, -006, -007, -010, -013. **Scores:** 28/40 + 36/60 = **64**. Assertions 2/5.

## Input 2 - Variant A: MACS3/MACS2 callpeak

Planted BAM: BAMPE 24 peaks, 20/20 truth, median width 373; shift-extend 391 peaks (MACS3 and MACS2 identical), 20/20, width 150; BAMPE with `--shift/--extsize` identical to BAMPE without (claim confirmed). GM12878 rep1: 4,803 peaks, 2,087/2,088 ENCODE IDR peaks overlapped. macs2 without the shim fails at import (`undefined symbol __log_finite`, `out/a4_misc_snippets.log`).

Findings: ATACPC-004. **Scores:** 36 + 52 = **88**. Assertions 4/5.

## Input 3 - Variant B: Genrich joint

Name-sorted joint on GM12878 reps with `-e chrM -E blacklist`: 14,498 peaks, 2,085/2,088 ENCODE peaks. Planted: 20/20 (2,327 peaks, noisy). Coordinate-sorted input aborts ("not sorted by queryname"); the Skill never mentions the name sort. q sweep on the chr1 slice: 14,328 (0.05), 22,936 (0.01), 23,535 (0.001) versus MACS3 4,803, contradicting the reconciliation advice.

Findings: ATACPC-008. **Scores:** 30 + 42 = **72**. Assertions 2/4.

## Input 4 - Variant B: macs3 hmmratac

`macs3 hmmratac -f BAMPE` on rep1: 2,064 accessible regions (narrowPeak), 2,072/2,088 ENCODE peaks recovered, model json and cutoff table written. Skill gives no command and calls the output a BED.

Findings: ATACPC-009. **Scores:** 32 + 46 = **78**. Assertions 2/3.

## Input 5 - Edge: recipes

NFR-only (`TLEN < 100`, `--shift -37 --extsize 75`): 10,951 peaks, 2,078/2,088 ENCODE peaks. Blacklist v2: 4,803 to 4,753. bigWig: valid magic, 3.2 MB (signal not read back, no reader installed). `grep -v chrM` on a synthetic pair with a mate on chrM removed both records and the chrM header line.

**Scores:** 33 + 47 = **80**. Assertions 4/4.

## Static review highlights

- Frontmatter, trigger description, license and provenance are sound; SKILL.md is short and routes correctly.
- Documented install line does not solve on bioconda alone and yields an idr that crashes on numpy>=1.24 (ATACPC-003).
- Uncited or unsupported claims: rotation/circular-shift permutation proxy, single-sample `-q` inconsistency (ATACPC-011), ROSE snippet needs a GFF conversion (ATACPC-012, static-only).

## Findings ledger (open)

| ID | Severity | Title |
|---|---|---|
| ATACPC-001 | P1 | Pseudoreplicates share half their reads |
| ATACPC-002 | P1 | Nt/Nself is not ENCODE rescue and self-consistency ratios |
| ATACPC-003 | P1 | Install line fails; idr crashes on numpy>=1.24 |
| ATACPC-004 | P2 | macs2 import fails on modern glibc; script hardcodes macs2 |
| ATACPC-005 | P2 | `-g hs` default and wrong 100 bp size in comment |
| ATACPC-006 | P2 | Script does not validate BAMs as claimed |
| ATACPC-007 | P2 | Blacklist covers only IDR set; no final peak set or bigWig |
| ATACPC-008 | P2 | Genrich: no command, name-sort undocumented, `-q` advice wrong |
| ATACPC-009 | P2 | hmmratac: no command, output description wrong |
| ATACPC-010 | P2 | Not exact ENCODE: no `--call-summits` or tagAlign |
| ATACPC-011 | P2 | Single-sample guidance inconsistent; rotation method uncited |
| ATACPC-012 | P3 | ROSE snippet lacks GFF step (static-only) |
| ATACPC-013 | P3 | Unquoted shell variables |

## Limitations

chr1:1-30Mb slice, one cell line, hg38 only; whole-genome IDR and mm10 not run. ROSE, HOMER, nf-core and chromap not run. bigWig signal not read back. Diagnostic score only; not a certification.

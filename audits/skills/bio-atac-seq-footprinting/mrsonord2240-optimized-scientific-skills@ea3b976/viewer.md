> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@ea3b976](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ea3b976ad47a0d0b127b4a047ea200a0d0ac1bf4/skills/bio-atac-seq-footprinting) match audited candidate `a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-footprinting`**
> - Audited working candidate `a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-atac-seq-footprinting`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/footprinting) (MIT).
> - Audit method: skill-auditor@1.0 (AIPOCH, MIT), rubric zip sha256 `e54e9ff8...f0de`.
> - Performed 2026-09-30 by a Claude (Anthropic) audit agent that did not write, fix, tool or initially audit the candidate. Final re-audit; independent.
> - Data: ENCODE GM12878 (rep1) and K562 (rep1) ATAC chr1:1-30 Mb filtered BAMs, ENCODE IDR peaks, hg38 chr1, JASPAR 2024 PFMs. Paths refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-footprinting (final re-audit)

Candidate: `sha256-manifest-v1 a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87` (7 files, 42,157 bytes), branch `fix/atac-footprinting` @ 3186916 (candidate untracked). Recomputed live before and after execution: identical; no `__pycache__`.
Predecessors: audited `737bd941...` (70/100 Beta Only), delta-tested `3b6efb4b...` (both superseded).
Category: 3 - Data Analysis - Mode D - Moderate, N = 6.
Environments: every usage-guide recipe was rebuilt verbatim in fresh throwaway envs `ra-footprint*` (removed afterwards), TOBIAS 0.17.5, samtools 1.19.2, RGT 1.0.2, pyDNase 0.3.0, scPrinter 1.2.0 with torch 2.11.0+cu128 (GPU), tangermeme 0.4.4, snapatac2 2.8.0, `pip check` clean. Live envs unchanged (fingerprints `logs/r5_fingerprints.txt`).
Code: `scripts/r1..r5*`, `manifest.py`, `build_records.py`. Output: `out/`, logs `logs/`.

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (run_tobias.sh, fresh env) | yes | 36 | 52 | 88 | 5/5 | pass |
| 2 | Edge (no-CTCF, missing input, spaces in paths) | yes | 35 | 51 | 86 | 4/4 | pass |
| 3 | Adversarial (bias correction absent) | yes | 33 | 47 | 80 | 3/4 | pass with P2 |
| 4 | Variant B (RGT recipe, HINT-ATAC, Wellington -A, concordance) | yes | 35 | 51 | 86 | 5/5 | pass |
| 5 | Variant B (scPrinter bulk, GPU) | yes | 35 | 51 | 86 | 5/5 | pass |
| 6 | Variant A (env recipes, NFR filter, ATACshift) | yes | 35 | 52 | 87 | 5/5 | pass |

**Execution Average: 85.5 / 100** (Layer 1 34.8, Layer 2 50.7) - **Assertion Pass Rate: 27/28 (96.4 %)**
**Static: 87/100** - **Final: 86 (Production Ready)**. Vetoes: none. Open P0/P1: none. Readiness: **candidate-ready**.

## Prior findings, retested

| ID | Result | Evidence |
|---|---|---|
| FOOT-001 (P1) | fixed | Input 2: no-CTCF motif set gives rc 3 with WARNING and ERROR on stderr and the table still printed; `ALLOW_NO_CTCF=1` gives rc 0 with the warning kept (`logs/r2_B_noctcf.log`, `r2_C_allow.log`, `r2_check.out`) |
| FOOT-002 (P1) | fixed for the bulk classic route | Input 5: shipped script ran in a fresh pinned env, 400x99x200 finite scores, bound > unbound at modes 10-30 (p 9e-17 to 8e-8), profile peak 2 bp from centre; figure `out/r3_scprinter_bound_vs_unbound.png` opened |
| FOOT-003 (P1) | fixed | Input 6: all four env recipes rc 0 with tested versions, `pip check` clean (`logs/r1_envs.out`, `r5_out.txt`) |
| FOOT-004 (P2) | fixed | Plain `pip install --no-deps rgt==1.0.2` is a no-op (data dir absent); documented `--force-reinstall --no-cache-dir` line writes `data.config`; HINT 358 footprints (`logs/r4_run.out`) |
| FOOT-005 (P2) | fixed | JASPAR `_jaspar.txt` name matches the file used; URL re-fetched: HTTP 200 (`logs/r7_jaspar_url.out`) |
| FOOT-006 (P2) | fixed | Table equals an independent pandas |change| ranking (12 rows) |
| FOOT-007 (P2) | fixed | Spaces in every path rc 0 with identical results; missing input rc 2 without creating the output dir |
| FOOT-008 (P2) | partially fixed | Per-condition all/bound/unbound plots with uncorrected vs corrected are shipped and the text no longer claims the dip proves correction. Residual (recommendation 1): with correction removed the script still exits 0 silently |
| FOOT-009 (P2) | fixed | Concordance defined and recomputed in pure python (58/143, 0/31, 54/358), matches |
| FOOT-010..015 | fixed | Static reread: crash claim dropped, `-A` documented and run, claims softened, MA0139.2 and hyphen flags used |

## Input 1 - Canonical: run_tobias.sh

`bash scripts/run_tobias.sh cond1.bam cond2.bam peaks.bed hg38.chr1.fa blacklist motifs_subset.pfm out 4` in the fresh env; rc 0. GATA1 -0.385, IRF4 +0.588, top-motif table equals the independent ranking. CTCF MA0139.2: 1203 sites, 513 bound (cond1) and 690 unbound. Corrected flank-minus-core: bound 6.67 (cond1) and 9.50 (cond2), unbound 0.23 and 0.50; uncorrected bound 5.75 and 7.42. PDF rendered (`out/r2_A_ctcf_cond1.png`): legible 3x4 panel grid, central dip with flanking peaks at bound sites, flat unbound profile, corrected panel baseline-subtracted.

## Input 2 - Edge: guards

B (no CTCF motif) rc 3; C (`ALLOW_NO_CTCF=1`) rc 0; D (nonexistent motif file) rc 2 with no output directory created; E (spaces in BAM, FASTA, peaks, blacklist, motif and output paths) rc 0, results identical to A, no stray `out/` or `dir/`.

## Input 3 - Adversarial: bias correction absent

A `TOBIAS` shim copies each `_uncorrected.bw` over `_corrected.bw` after ATACorrect. The script exits 0 with no warning; bound-site flank-minus-core is 7.14 (cond1) and 8.69 (cond2), as deep as the genuinely corrected run (6.67, 9.50). The guard therefore only tests that a CTCF motif exists; the Skill discloses that the dip alone does not prove correction, so this is a residual P2, not a P1. The corrected-versus-uncorrected contrast at all sites is small (cond1 2.51 to 2.97, cond2 4.39 to 5.64).

## Input 4 - HINT-ATAC, Wellington, concordance

Recipe followed from `usage-guide.md`; HINT rc 0 in 12 s, 358 footprints; Wellington `-A` rc 0. `site_concordance.sh` on 60 peaks: HINT overlaps 58/143 bound and 0/31 unbound sites, 54/358 of its footprints touch a bound site; Wellington -A 15/143 and 0/31. Independent python recomputation matches (`logs/r4_check_conc.out`). Empty call set rejected with rc 2.

## Input 5 - scPrinter bulk

Fragment recipe (fresh samtools/bgzip/tabix): 521,478 fragments. `scprinter_footprint.py` on GPU, 14 min: mode 10 bound 0.673 vs unbound 0.353, mode 20 1.661 vs 0.440, mode 30 0.717 vs 0.341; mode 50 does not separate (0.085 vs 0.238), as SKILL.md states. Missing fragment file exits rc 1 with a raw traceback (recommendation 3).

## Input 6 - Recipes, NFR filter, shift

Fresh env versions as above. NFR filter: 94,478 reads equal the independent `samtools -e` count, max |TLEN| 99. `alignmentSieve --ATACshift`: +4 at 119,182/119,182 forward starts, -5 at 118,152/119,182 reverse ends (`logs/r6_nfr.out`; unchanged command text and live env, re-run).

## Excluded and untested modes (labelled honestly in the Skill)

Single-cell/cluster scPrinter and seq2PRINT training: stated as not covered or tested in SKILL.md (step 3), the usage guide and the method reference; not executed here. ChIP-anchored CTCF validation: not shipped and not run; SKILL.md recommends ChIP or a second call set as an external step. Full-depth (50M read), whole-genome runs: blocked by resource limits; all runs use chr1 slices of about 0.5-5M reads and the Skill labels values as tool checks, not power checks.

## Recommendations (all P2)

1. CTCF control cannot detect absent bias correction (Input 3).
2. scPrinter pip lines do not name the environment (`references/usage-guide.md`).
3. `scprinter_footprint.py` fails with a raw traceback on a missing input.

## Static notes

Frontmatter and license preserved, 7 files, all routed from SKILL.md; version floors replaced by a tested-with list; commands and flags match the versions run; no secrets or destructive operations; LF endings; no cache artifacts in the tree.

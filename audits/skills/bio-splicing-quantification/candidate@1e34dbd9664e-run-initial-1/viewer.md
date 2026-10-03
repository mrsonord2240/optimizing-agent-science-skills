> **Audit record for `bio-splicing-quantification`**
> - Audited working candidate `1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/alternative-splicing/splicing-quantification), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) initial-audit worker, lane 2, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-splicing-quantification

Generated: 2026-10-03
Audit type: bounded diagnostic initial audit (lane 2); not a certification
Exact candidate content SHA-256: `1e34dbd9664e334b3feb336a3d624ec99d39ca9b5ad9a056f1f7142448bd489c` (5 files, 37504 bytes; `skill_preflight --offline` PASS before and after execution, candidate bytes untouched)
Category: Data Analysis | Mode: D (hybrid) | Complexity: Complex, 6 executed workflows

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical (rMATS real chrX 2v2, snippet and parser) | 24 | 34 | 58 | 2/5 | PARTIAL |
| 2 | Variant A (rMATS planted, effective-length PSI) | 33 | 50 | 83 | 3/4 | COMPLETED |
| 3 | Variant B (SUPPA2 + rMATS concordance) | 31 | 46 | 77 | 3/5 | COMPLETED |
| 4 | Edge (parser on A5SS/A3SS/MXE/RI) | 16 | 20 | 36 | 1/3 | ERROR |
| 5 | Stress (regtools + leafcutter, XS vs no XS) | 24 | 34 | 58 | 2/5 | PARTIAL |
| 6 | Scope Boundary (IRFinder route) | 24 | 32 | 56 | 2/4 | PARTIAL |

**Execution average:** 61.3 / 100
**Assertion pass rate:** 13 / 26
**Static score:** 69 / 100
**Final diagnostic score:** 64 / 100 (Beta Only by number). The Research Veto M4 (code usability) fails, so the recorded grade is Reject, deployable false. Fixing SQ-01 to SQ-03 clears the veto cause.

The strict audit JSON is [report.json](report.json).

## Veto review

- Skill veto: PASS. Stability judged on the whole surface; defects are deterministic logic faults filed as findings, not random crashes.
- Research veto: M1, M2, M3 PASS (no fabricated values; formula, planted PSI and cross-tool direction reproduce). **M4 FAIL**: the inline snippet raises TypeError on every real rMATS JC file, and `parse_rmats_output` raises KeyError for A5SS, A3SS, MXE and RI; the SE path returns silently wrong values.

## Execution classification

| Surface | Class | Evidence |
|---|---|---|
| rMATS-turbo 4.4.0, Skill flags (`-t paired --readLength 75 --variable-read-length --libType fr-firststrand --novelSS --statoff`) | executed | rc 0; JC rows SE 958, A5SS 216, A3SS 251, MXE 51, RI 174 |
| rMATS planted hand-checked SE | executed | IncLevel1 0.8/0.8/0.769, IncLevel2 0.2/0.2/0.208, diff 0.587 = hand values; JC lengths 98/49 |
| SKILL.md inline pandas snippet | failed | TypeError (SQ-01) |
| `parse_rmats_output` | executed (SE), failed (A5SS, A3SS, MXE, RI) | SQ-02; SE values wrong in 310/958 rows (SQ-03) |
| SUPPA2 generateEvents/psiPerEvent via `run_suppa2_quantification` | executed | planted 0.8/0.2/0.5 exact; chrX seven psi files |
| `filter_reliable_events` | executed | works; range disagrees with Skill text (SQ-07) |
| rMATS vs SUPPA2 concordance | executed | SE r 0.864 (892 events), A5 0.718 (161), A3 0.849 (197) |
| regtools extract + leafcutter clustering | executed, silent failure on untagged BAMs | noXS strand ? 100%, 0 clusters; XS 115 clusters at -m 5 (SQ-04) |
| IRFinder `-m FastQ` | executed (1.3.1) | 7,955 rows; literal reference syntax fails (SQ-05) |
| STAR microexon flags in references | executed (flag existence) | `STAR --help` lists alignSJoverhangMin 5, alignSJDBoverhangMin 3, outFilterMismatchNoverReadLmax 1.0; outSAMstrandField default None |
| MAJIQ V3 build/psi/voila | static-only, restricted-access | licence form; not attempted; Skill does not label it unexecuted (SQ-09) |
| VAST-TOOLS, VASTDB | static-only, heavy-optional | 6.7 GB VASTDB; Skill does not label it not executed (SQ-09) |
| Shiba, MicroExonator, S-IRFindeR, iREAD, leafcutter2, IRFinder-S 2.0 | static-only | mention-only or not installable |

## Ordered finding ledger (for fix-scientific-skill)

| ID | Priority | Finding |
|---|---|---|
| SQ-01 | P1 | SKILL.md inline snippet `se_jc[inc_cols].mean(axis=1)` raises TypeError on real rMATS output (comma-string IncLevel; also matches IncLevelDifference) |
| SQ-02 | P1 | `parse_rmats_output` raises KeyError (`exonStart_0base`, `exonEnd`) for A5SS/A3SS/MXE/RI |
| SQ-03 | P1 | Parser mean_PSI includes IncLevelDifference (310/958 SE rows wrong, up to 0.5); reliability filter in snippet and script uses SAMPLE_1 only |
| SQ-04 | P1 | STAR BAMs without XS tags give strand ? and zero leafcutter clusters (rc 0); Skill never states the XS prerequisite |
| SQ-05 | P1 | `IRFinder FastQ -r ...` exits 1 (real form `-m FastQ`); no reference-build step; IRFinder-S 2.0+ is not what installs (1.3.1) |
| SQ-06 | P2 | SUPPA2 TPM header format and statsmodels<0.15 pin undocumented (both failures reproduced) |
| SQ-07 | P2 | `filter_reliable_events` hardcodes PSI 0.1-0.9; Skill says 0.05-0.95 and claims rMATS/SUPPA2 default filters drop those events |
| SQ-08 | P2 | IncFormLen "plus exon body bases" is wrong for JC (98 vs JCEC 149) |
| SQ-09 | P2 | MAJIQ V3 and VAST-TOOLS not labeled not-executed; benchmark figures unsourced |
| SQ-10 | P2 | Related Skills names do not resolve on the shelf (no `bio-` prefix; STAR and alignment-free-quant Skills absent) |
| SQ-11 | P2 | rMATS BAM list format, leafcutter script source and Skill-root LICENSE missing |

## Detailed results

Commands and saved outputs are in `scripts/` (published) and `out/` (local). Key observations:

- Input 1: `01_run_tools.sh` section A, then `03_analyze.py` sections 1-3. The snippet is extracted from SKILL.md and executed verbatim. Example rows (gene, IncLevel1, IncLevel2, diff, true mean, script mean): CXorf40B `NA,0.0` / `NA,1.0` / -1.0 / 0.5 / 0.0.
- Input 2: `01_run_tools.sh` section B, `03_analyze.py` section 4; real-data formula check max diff 0.0005 over 1465 replicate values.
- Input 3: sections C and D plus `03_analyze.py` section 5. Matching is by coordinates (SE exact; A5/A3 shared boundary and two alternative boundaries within 1 nt).
- Input 4: `03_analyze.py` section 2.
- Input 5: `01_run_tools.sh` section E and `02_leafcutter_m5_irf.sh`; at -m 50 both variants give 0 clusters on the small chrX data (not a defect).
- Input 6: `01_run_tools.sh` section F and `02_leafcutter_m5_irf.sh`; the staged IRFinder reference was read only.

Restricted-access after-action: MAJIQ V3 requires the licence form; once installed, rerun `majiq build/psi` and `voila view` in a tooling-delta pass.

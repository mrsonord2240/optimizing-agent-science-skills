> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@ea3b976](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ea3b976ad47a0d0b127b4a047ea200a0d0ac1bf4/skills/bio-atac-seq-single-cell-atac) match audited candidate `4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-single-cell-atac`**
> - Audited working candidate `4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/single-cell-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Final re-audit: bio-atac-seq-single-cell-atac

- Date: 2026-09-30 | Phase: final re-audit (independent; did not write, fix, tool or initially audit this Skill)
- Candidate: `F:\OpenScience\wt\atac-single-cell-atac\skills\bio-atac-seq-single-cell-atac`, sha256-manifest-v1 `4ced0da507d684d209beb4676ce6d206fc6d1730ff2e45d8ff965c3e2d78f286` (6 files, 34,930 bytes), recomputed live before and after execution
- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:atac-seq/single-cell-atac
- Prior audit: identity da2da9c8..., 71/100, Reject (code-usability veto, SCATAC-001)
- Rubric: skill-auditor.zip sha256 e54e9ff8... (unchanged)

## Decision: candidate-ready

Score 86 (Production Ready band); static 86; execution average 86.0; Layer 1 34.75; Layer 2 51.25; assertions 31/31; no veto; no open P0/P1. Four open P2 after-action items (none blocks readiness).

## Prior findings, retested

| ID | Result | Independent evidence (`logs/`) |
|---|---|---|
| SCATAC-001 P0 | fixed | `signac_doc.log`: shipped script, 3 documented args, exit 0; 40/1,472 cells at documented QC; annotation hg38/UCSC; `check_signac.log` |
| SCATAC-002/003/011 P1 | fixed | `snap.log`: block extracted verbatim from live markdown on SnapATAC2 2.10.0; no sample_id, knn present, macs3 n_jobs=1; 697 cells, 6 clusters |
| SCATAC-004 P1 | fixed | one filter rule in SKILL.md; `check_signac.log` rule check true for every retained cell (doc and relaxed runs) |
| SCATAC-005/008 P2 | fixed | `amulet.log`: documented command in numpy 1.23.5 env, 5,335 cells, 55 multiplets; depth claims recomputed (median 10,701; 69.9% < 15K; 7.2% < 1000 fragments) |
| SCATAC-006/007 P2 | fixed | `wnn.log` (no %>% before block; 2,557 cells, 12 clusters); `cellcycle.log` (0.264 -> 0) |
| SCATAC-009/010/012/013/014 P3 | fixed | `archr_guard.log` (documented thresholds stop at guard; relaxed 403 cells); `peakvi.log` (aligned 0.031 vs unaligned 0.129); wording/prerequisites read in tree |
| SCATAC-015 | blocked, honestly stated | Cell Ranger ATAC/ARC not run; Skill says so (version note) and script stops on missing columns (executed: `signac_guard.log`) |

The fixer's P3 labels are outside the report schema; they are folded into the P2 list or closed.

## Relaxed thresholds

The chr1 slice (about 3% of the genome) cannot meet the documented minimums: documented QC leaves 40 cells (Signac), 0 (SnapATAC2 at 1000/4) and no ArrowFile (ArchR). Runs 2, 4, 5 therefore use lowered TSS/fragment minimums (Signac `1 1000`, SnapATAC2 400/0.3, ArchR 1/500). SKILL.md states this where it matters ("Shallow or subset data can leave zero cells at these values; lower TSS and fragment minimums deliberately and report the change") and the script and ArchR guard name the remedy. Results are not scientific biology claims about PBMC subsets; they exercise code paths.

## Execution classification

| Surface | Class | Evidence |
|---|---|---|
| signac_workflow.R, documented args | executed | `signac_doc.log`, `check_signac.log` |
| signac_workflow.R, relaxed; QC/UMAP figures | executed | `signac_relaxed.log`; `output/signac_relaxed_{qc,umap,depth_cor}.png` rendered and read |
| signac_workflow.R, missing-column guard | executed | `signac_guard.log` (stop message, exit 1) |
| SnapATAC2 2.10.0 block | executed (relaxed filter) | `snap.log` |
| ArchR createArrowFiles + guard | executed | `archr_guard.log` |
| ArchR downstream (LSI, clusters, peaks) | reused | text unchanged; initial audit 403 cells, 5 clusters, 7,788 peaks; identity-matched environment fingerprint a71616d9... |
| Multiome WNN | executed | `wnn.log` |
| Cell-cycle LSI regression | executed | `cellcycle.log` |
| AMULET fragment route | executed | `amulet.log` |
| AMULET BAM/jar route | blocked (no CB-tagged BAM) | labelled UNTESTED in the Skill |
| PEAKVI / scArches | executed (30 epochs, GPU) | `peakvi.log` |
| Signac CallPeaks, scDblFinder, tabix | reused | untouched text and invocation; environments unchanged (fingerprints match); evidence from prior full pass |
| Cell Ranger ATAC / ARC, scATAC-pro, chromap | blocked / static-only | 10x registration; Skill does not claim execution |

Negative control of AMULET under modern numpy was attempted in the py env and failed earlier on a missing output file (env lacks the AMULET Java pieces); the np.object failure is covered by the initial audit, and the Skill's numpy note rests on that and on the passing pinned-env run. Not counted as an assertion.

## Open items (all P2)

1. Cell Ranger ATAC 2.x/ARC column mapping untested (SCATAC-015 carry).
2. AMULET BAM route not executed.
3. `specialized-topics.md` line 24 narrates audit history ("the audit saw ScaleData error"); reword.
4. SnapATAC2 "import_data removed in 2.9" unverified (2.8.0 has both, 2.10.0 only import_fragments).

## Evidence

`scripts/` (run scripts, `ra_build_report.py` validates the report against the schema checklist), `logs/`, `output/`, `report.json`, `source-identity.json`.

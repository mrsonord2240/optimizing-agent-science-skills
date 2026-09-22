# Fix log: bio-single-cell-hashing-demultiplexing

2026-09-19. Fixer for `single-cell/hashing-demultiplexing`, fork commit `0de5e44090dd0428293282bc6feff9e1389817f6`
on branch `fix/sc-hashing` (worktree `F:\OpenScience\wt\sc-hashing`, base `main` at `563b098`).
Audit: `F:\OpenScience\audits\bio-single-cell-hashing-demultiplexing\` (score 78, Limited Release,
1 open P0, 2 open P1, 1 P2).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `sce.pp.hashsolo` silently classifies 100% of cells "Negative" at exactly 2 hashtags (`number_of_noise_barcodes` defaults to `len(cols)-2` = 0), no error raised | P0 | SKILL.md's hashsolo section: explicit warning + `number_of_noise_barcodes=1 if len(hto_cols)<=3 else None` in the code pattern + a runtime guard that raises if the Negative fraction exceeds 90%. Same fix applied to `examples/hashsolo_scanpy.py`. Added a row to Threshold reference and Common Errors. usage-guide.md Tips gained a one-line pointer (dedup rule, no restatement). | **ran** - reproduced the audit's exact scenario (scanpy 1.12.4, synthetic 2-tag/900-cell, same seed): before fix 5.4% agreement / all-Negative; after fix (identical data) 100% global and singlet-sample-ID agreement with ground truth. | P0 genuinely resolved - see final message. |
| `demuxmix()` can throw an uncaught `glm.nb` error ("missing value where TRUE/FALSE needed") on underdispersed HTO background instead of degrading; its own warning names the cause and suggests `clusterInit`, undocumented in the Skill | P1 | SKILL.md's demuxmix section: added a paragraph naming the failure mode + a `tryCatch` guard that retries with `model='naive'` on that error, plus a note that `dmmClassify()`'s "did not converge" warning must still be checked. Common Errors and Threshold reference rows added. | **ran** - reproduced the exact crash (demuxmix 1.8.0, R 4.4.3) on synthetic near-Poisson HTO background; confirmed the guard's `model='naive'` fallback completes on the identical input instead of crashing. Manual `clusterInit` was also tested and did *not* avoid this particular crash (only helps demuxmix's separate poor-clustering failure mode, per its own docs), so the guard leads with the verified remedy (`model='naive'`) rather than `clusterInit` alone. | |
| No runnable example for demuxEM/pegasus or GMM-Demux | P1 | Built an isolated `tools\demuxem-venv\` in the candidate env (`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\`), documented in its `TOOLS.md`. `pegasuspy` (demuxEM) **does not build on Windows** - its `pegasusio` dependency needs the POSIX-only `getline`, absent under MSVC (`error LNK2001: unresolved external symbol getline`). Documented this inline in SKILL.md next to the existing pegasus/demuxEM snippet instead of shipping an unverified example; also corrected TOOLS.md's prior "shared-venv conflict" framing for pegasuspy, which understated the problem. `GMM-Demux==0.2.2.3` **does** install (pinned `numpy<2`/`scipy<1.14`/`scikit-learn<1.6` - the package breaks under numpy 2.x's stricter scalar-conversion rules) and was added as a new SKILL.md subsection with a CLI example. | **ran** - GMM-Demux verified end to end on the audit's real `data/hto_counts_4tag.csv` (1600/1600 global, 1360/1360 singlet sample-ID agreement vs. ground truth). Found and documented two real bugs along the way: CSV columns must be float dtype (else `LossySetitemError` on modern pandas) and its SSD-mtx writer always fails after a correct classification (judge success by `GMM_full.csv`, not exit code). pegasuspy: build attempt is real evidence of the Windows incompatibility, not an execution of the tool itself. | |
| No concrete Negative-fraction sanity-check threshold before trusting output | P2 | Added one line to usage-guide.md's "What the Agent Will Do" step 4: stop and diagnose if the Negative fraction is roughly 50%+. | n/a (doc-only, consistent with the P0 fix's 90% guard) | Cheap, done alongside the P0. |

## Unfixed

Nothing left open from the audit's `recommendations[]`. All 4 findings (1 P0, 2 P1, 1 P2) addressed.

## Verification environment

`F:\OpenScience\audit-envs\single-cell-transcriptomics-analyst\` - scanpy 1.12.4, demuxmix 1.8.0,
R 4.4.3/Bioconductor 3.20, plus the new `tools\demuxem-venv\` (GMM-Demux 0.2.2.3). Changed `.py`
compiled clean (`py_compile`); changed `.R` snippets parsed and were run end to end, not just parsed.
No shared-venv or shared-R-lib package was installed or changed; `demuxem-venv` is a fresh isolated
venv built from the runtime's own interpreter, following the `sccoda-venv`/`liana-venv` precedent.

## 2026-09-21 (P2 batch)

Fixer for `single-cell/hashing-demultiplexing`, branch `fix/single-cell-hashing-demultiplexing` (worktree
`F:\OpenScience\wt\single-cell-hashing-demultiplexing`, base staging `main` 431aa55), commit `1e0fff0`.
Audit: 2 P2. SKILL.md 227 -> 231 lines (under the 300 split threshold, no split).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| GMM-Demux SSD-mtx writer does not "always" fail | P2 | SKILL.md GMM-Demux section and Common Errors row reworded to "can fail on some inputs/scipy versions"; states where `SSD_mtx/` is written (working dir, or `-o <dir>`); keeps "judge by `GMM_full.csv`, not exit code" | ran: GMM-Demux 0.2.2.3, scipy 1.13.1, on the audit's 4-tag, unequal and weak-staining data: exit 0 and `GMM_full.csv` each time; `-o ../ssd3` wrote the folder there; `--help` for `-o` | The 2026-09-19 claim was generalised from one environment |
| No bundled example dataset | P2 | none | n/a | see Left unfixed |
| Redundancy pass (not an audit finding) | - | see table below | grep of each moved fact in SKILL.md | |
| hashsolo inline block duplicates `examples/hashsolo_scanpy.py` | - | 14-line block cut to the 2-line `sce.pp.hashsolo` call plus a pointer to the example | ran: the example, unchanged, on the audit's `hto_counts_4tag.csv` with synthetic GEX: 1393 singlets/124 doublets/83 negatives, singlet agreement 99.9% vs ground truth, guard did not fire | |

### Left unfixed

- **No bundled example dataset (P2):** it needs new fixture content (synthetic HTO CSV plus a synthetic GEX matrix, since both examples also read `gex.h5ad` / `gex_counts`) and rewiring the examples to read it; `examples/` stays as it is under FIX_BRIEF, and the audit's own synthetic data is not shipped with the Skill.
- **Scripts step:** no other runnable block is 15+ lines (HTODemux 3, MULTIseqDemux 2, pegasus 5, demuxmix tryCatch 9, GMM-Demux 1), so nothing moved to `scripts/`; the only qualifying block was the hashsolo duplicate, deleted above.

### Deleted passages -> new home

| deleted | new home |
|---|---|
| usage-guide.md "Prerequisites" (R/bash install commands) | SKILL.md "Install" section |
| usage-guide.md "What the Agent Will Do" steps 1-7 | SKILL.md decision tables, method sections, Common Errors; guide keeps a pointer |
| step 4 "Negative fraction roughly 50%+: stop and diagnose" | SKILL.md hashsolo section (after the example pointer) |
| usage-guide.md Tips (11 bullets) | SKILL.md Governing principle, Choosing a hashtag caller, Common Errors rows (all already stated there) |
| usage-guide.md "Related Skills" | SKILL.md "Related Skills" (unchanged) |
| SKILL.md hashsolo block (imports, `adata.obs[hto_cols] = ...`, classification counts, >90% guard, singlet subset) | `examples/hashsolo_scanpy.py` |

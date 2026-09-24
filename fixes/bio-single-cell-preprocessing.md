# bio-single-cell-preprocessing fix pass — 2026-09-24

Source worktree: `F:\OpenScience\worktrees\bio-single-cell-preprocessing-fixpass`
on branch `fix/bio-single-cell-preprocessing-audit-20260924`, rooted at staging
`main` `4d483d0451fcd60cb3ab62dfa4cd047ec59b3615`.

Commits:

- `a6550a1a7aca3cfa156d65780278acb017e54d94` — `fix(single-cell/preprocessing): repair QC and ambient audit findings`
- `c3ca7ea1aa3aacf4efebc322b9b01dee31fe3917` — `fix(single-cell/preprocessing): align packaged QC examples`
- `9918c631d94f81dd418cf71d5c40be59f4850677` — `docs(single-cell/preprocessing): restore install guidance`

## Resolved findings

| Previous finding | Priority | Change | Verified | Notes |
|---|---:|---|---|---|
| SoupX called `autoEstCont()` without clusters | P1 | Create quick Seurat clusters when absent, then call `setClusters()` | `soupx-current.log`: 707 clusters, rho 0.085, 8.5% removed | Tested on Cell Ranger-style raw and filtered matrices |
| Universal 8% mitochondrial cap could erase valid populations | P1 | Use named tissue caps; nuclei and unknown tissue are MAD-only | `sources.log`, `qc.log`, and packaged-example logs | No copied PBMC cap for nuclei or unknown tissue |
| Packaged Scanpy and Seurat examples retained flat cutoffs | P1 | Aligned both examples with MAD-adaptive QC, tissue policy, and 80% survival guard | `scanpy-example-rerun.log`, `seurat-example-rerun.log` | Both exact source files ran end to end |
| Batch-aware `seurat_v3` could fail on batch-specific genes | P2 | Filter genes by detection in every batch before batch-key HVG selection | `qc.log`: 7,846/12,521 retained and 2,000 HVGs | Archived input 5 also reproduces the former loess failure |
| Re-normalization guidance described the wrong symptom | P2 | Document Scanpy's warning and compressed/decreased totals | `input7-rerun.log`: total ratio 0.662 | Raw counts remain the recovery route |
| Global MAD filtering could silently erase simple populations | P2 | Require removal-rate review by preliminary cluster or known type | `input1-rerun.log`: 28.8% megakaryocyte removal exposed | Prevents treating an attractive embedding as proof of QC correctness |
| MAD collapse lacked an executable stop | P2 | Print medians/MADs, stop on zero MAD, and stop below 80% survival | `qc.log`: zero-MAD fixture stopped before subsetting | Fixed-cutoff review remains explicit recovery |
| Usage guide duplicated authoritative workflow content | P2 | Retained overview, example prompts, and related skills only | `sources.log`: duplicate sections absent | Canonical instructions remain in `SKILL.md` |

## Deleted or consolidated passages

| Deleted passage | Source | Destination or rationale |
|---|---|---|
| Normalization assumption tip | `usage-guide.md` Tips | Consolidated into `SKILL.md` Normalization Choice |
| Shifted-log selection tip | `usage-guide.md` Tips | Consolidated into the normalization chooser |
| Mitochondrial biology warning | `usage-guide.md` Tips | Consolidated into Quality Control |
| Per-sample QC recommendation | `usage-guide.md` Tips | Consolidated into Quality Control |
| Per-sample ordering note | `usage-guide.md` Tips | Consolidated into Canonical Pipeline Order |
| Ambient correction before QC | `usage-guide.md` Tips | Consolidated into Ambient RNA Removal |
| Choose one ambient method | `usage-guide.md` Tips | Consolidated into Ambient RNA Removal |
| HVG input-count requirement | `usage-guide.md` Tips | Consolidated into Highly Variable Gene Selection |
| Preserve raw counts | `usage-guide.md` Tips | Consolidated into Canonical Pipeline Order and HVG guidance |
| Avoid reflexive regression | `usage-guide.md` Tips | Consolidated into Scaling and Covariate Regression |
| Dissociation caveat | `usage-guide.md` Tips | Consolidated into mitochondrial/confound guidance |
| Prerequisites section | `usage-guide.md` | Install commands moved into the authoritative `SKILL.md` Installation section |
| Repeated workflow section | `usage-guide.md` | Canonical Pipeline Order already lives in `SKILL.md` |

## Verification and re-audit

- Exact evidence directory: `F:\OpenScience\audits\bio-single-cell-preprocessing\run\final-corrective-20260924`
- Seven archived inputs rerun as regressions; two fresh packaged-example inputs added
- Exact source: `mrsonord2240/bioSkills@9918c631d94f81dd418cf71d5c40be59f4850677:single-cell/preprocessing`
- Pre-fix evidence retained: `F:\OpenScience\audits\_pre-fix-20260924\bio-single-cell-preprocessing`

Re-audit result: **93/100, Production Ready, deployable**; **36/36 assertions
pass** across **8/9 executed inputs** (input 6 is text-only); veto gates pass and
no P0/P1/P2 remains open.

> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@ea3b976](https://github.com/mrsonord2240/optimized-scientific-skills/tree/ea3b976ad47a0d0b127b4a047ea200a0d0ac1bf4/skills/bio-atac-seq-deep-learning-atac) match audited candidate `3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-atac-seq-deep-learning-atac`**
> - Audited working candidate `3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/atac-seq/deep-learning-atac), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-30 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-atac-seq-deep-learning-atac (final re-audit)

Generated: 2026-09-30  
Audit type: independent final re-audit (auditor did not fix or initially audit this Skill)  
Exact candidate: sha256-manifest-v1 `3a9d1b4cab32a0a18917e8ee70b552a395e832da48a98902b90001a5190dea87` (10 files, 47,690 bytes), verified live before and after execution. Prior audit `c62d899a...` scored 60/100, Reject.

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical (shipped pipeline, fresh run + RESUME + guards) | 36 | 52 | 88 | 5/5 | COMPLETED |
| 2 | Variant A (log2FC, three independent methods) | 38 | 55 | 93 | 5/5 | COMPLETED |
| 3 | Edge (pred_bw contract, Enformer REF guard) | 36 | 52 | 88 | 4/4 | COMPLETED |
| 4 | Variant B (attributions, MoDISco, report) | 36 | 52 | 88 | 4/4 | COMPLETED |
| 5 | Stress (scBasset, Enformer, restricted items, prerequisites) | 34 | 50 | 84 | 4/5 | COMPLETED |

**Execution average:** 88.2 - **Assertion pass rate:** 22/23 (95.7 percent) - **Static:** 87/100 - **Final:** 88/100, Production Ready by rubric, no veto, no open P0.  
**Decision: candidate-ready** for the exact bytes above. Report: [`report.json`](report.json); identity: [`source-identity.json`](source-identity.json).

## Prior finding dispositions (each re-tested)

| ID | Disposition | Evidence |
|---|---|---|
| DLA-001 P0 | Closed | `log2fc_indep.log`: raw-Keras recomputation vs shipped script vs variant-scorer on 200 real SNPs (max diff 1e-3 or better); `torch_scripts.log` planted-truth fixture: truth -2.44, fixed -2.20, old -0.446 |
| DLA-002 P0 | Closed | `pipe_run1.log`: fresh OUTDIR, prep nonpeaks through variant scoring, exit 0 in 43 min (1 epoch); `pipe_resume.log` RESUME tail 22 s exit 0; `guards_gate.log` 7 guards |
| DLA-003 | Closed | 5-column list accepted, 18-column output, logfc = log2(a2/a1) to 7e-8 |
| DLA-004 | Closed | `BPNet.from_chrombpnet` route reproduces Keras log-counts (max abs log2FC difference 1.1e-3 on 200 SNPs via `score_variants_torch.py`) |
| DLA-005 | Closed | `torch_scripts.log`: npz layout, `modisco motifs`, report `-l` and `-t`; tomtom-missing error reproduced. `contribs_bw` route not re-run here (delta and fix logs only) |
| DLA-006 | Closed | Env table matches the installed stacks (fingerprint unchanged) |
| DLA-007 | Closed | `predbw_awk.log`: 3-column duplicate BED fails, documented one-liner works, bigWig signal inspected |
| DLA-008 | Closed | 2/200 exceed abs logfc 1 (default mode) and r 0.960 forward-only vs default reproduced; null p-values present |
| DLA-009 | Closed | Gate FAIL on the 1-epoch model, PASS/FAIL/exit-2 paths on synthetic files; thresholds (-0.3, 0.5, 0.003) match chromBPNet's `make_html.py` |
| DLA-010 | Closed | Enformer 40 SNPs equals an independent bin computation; scBasset preprocess, train, embedding rerun; Borzoi and Keras 3 scBasset labelled not run |
| DLA-011 | Closed with limitation | Old `bias pipeline`/`pipeline` exit still unobserved, correctly labelled |
| DLA-012, 013 | Closed | Flag names and quoting/guards verified against installed CLI |
| DLA-014 | Closed (static) | Uncited rules of thumb are labelled; no 100x or "strongest" claims remain |

## Open findings (both P2, no repair made; auditor may not edit)

- **DLA-015** chromBPNet shells out to `bedtools` and `bedGraphToBigWig`; the env table and the script's step 0 do not declare or check them (source: `CHROMBPNET.py` `os.system("bedtools ...")`, `reads_to_bigwig.py` `subprocess.run(["bedGraphToBigWig"...])`). Not shown by a failing run, because the audit env has both.
- **DLA-016** `chrombpnet_pipeline.sh` header cites SKILL.md step 5 for interpretation; it is step 6.

## Execution classification

| Surface | Class | Evidence |
|---|---|---|
| Pipeline fresh run, RESUME, guards, QC gate | executed | `pipe_run1.log`, `pipe_resume.log`, `guards_gate.log` |
| Variant scoring (variant-scorer, torch script, raw Keras) | executed | `log2fc_indep.log` |
| pred_bw and awk one-liner | executed | `predbw_awk.log` |
| attributions, MoDISco, report (lite, tomtom) | executed | `torch_scripts.log` |
| Enformer script | executed | `torch_scripts.log` |
| scBasset 1 epoch (TF 2.15 CPU) | executed (mechanics only, val AUC 0.49) | `scbasset_1epoch.log` |
| `chrombpnet contribs_bw` then `modisco -i` | reused (delta and fix runs, unchanged bytes and env) | fix-run `contribs_bw.log` |
| Full-scale chromBPNet training/interpretation, `bias pipeline` exit, TF-MoDISco at 1M peaks | blocked, resource-infeasible (TF 2.8 CPU) | TOOLS.md R1; Skill labels them untested |
| scBasset on Keras 3, Borzoi, TOBIAS, saturation mutagenesis | blocked or not-applicable; not claimed executed in the Skill | TOOLS.md R3, surfaces 15-16 |

## Caps and caveats

Pipeline capped at 2,700 s and 1 epoch (not reached); scBasset capped at 2,400 s and 1 epoch. Fixture is real GM12878 reads re-cut into pseudo-contigs (derived), so model metrics prove mechanics, not quality. Planted-motif fixture is synthetic and labelled. Environment fingerprint unchanged (`06fc2798...`). No `__pycache__` in the Skill tree; worktree shows only the untracked Skill subtree.

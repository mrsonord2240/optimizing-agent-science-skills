# bio-atac-seq-footprinting fix pass - 2026-09-30

The CTCF validation was silently skipped, the scPrinter route and the bioconda install (TOBIAS 0.13.3) were wrong, and the RGT data line was a no-op. Each tool now has a verified per-tool environment recipe and the CTCF guard and scPrinter bulk route run on real chr1 data. With bias correction removed the script still exits 0 without a warning (open P2). Single-cell scPrinter and seq2PRINT training are untested.

- Final candidate audit: `audits/skills/bio-atac-seq-footprinting/candidate@a71e561087bc-reaudit-run`
- Result: **86/100, Production Ready**; no open P0.
- Candidate identity: `a71e561087bc769f5b14f703c8c535d1fda3a7f90de84d2a4b0dc7ccfb2ade87`.

The provider binding record is the canonical proof that the committed shelf bytes match this independently audited candidate.

## Fix pass 3 - 2026-09-30

The CTCF control now fails a run whose bias correction is missing. Per-cluster scPrinter scoring and seq2PRINT training are documented from executed runs. The three open P2s from the re-audit are closed. The candidate is uncommitted.

- Candidate identity: `86dd7a021575d6f8ed7c8c5462a9ecdc1061640e8f6e6b122b32b140808c02e2` (7 files, 52,673 bytes), replacing `a71e5610...`.
- Evidence: `F:\OpenScience\audits\bio-atac-seq-footprinting\fix-run3\` (`scripts/`, `logs/`, `out/`).

| Change | Finding |
|---|---|
| `run_tobias.sh` adds `_expected.bw` to the CTCF plot. Over all CTCF sites it correlates the corrected aggregate with the bias-only expectation and exits 4 above `BIAS_R_MAX` (0.2). Real run: r -0.14/-0.22, rc 0. Corrected replaced by uncorrected: r 0.65/0.40, rc 4 (`logs/f2_A.log`, `f2_N.log`) | Re-audit rec 1 (FOOT-008 residual, P2) |
| scPrinter pip lines prefixed with `micromamba run -n footprint-scprinter`; recipe rebuilt fresh, `pip check` clean (`logs/f1_envs.out`) | Re-audit rec 2 (P2) |
| `scprinter_footprint.py` checks every input and exits 2 with a named message (`logs/f3_G_*`) | Re-audit rec 3 (P2) |
| `--groups` per-cluster mode, run on 10x PBMC in the live and fresh envs (`logs/f3_check_*.out`); usage-guide section with the observed depth limit | Brief item 3 |
| seq2PRINT prep and `seq2print_train` blocks, executed as extracted from the usage guide (`logs/f4_*`, `f5_check_model.log`): 31 min, peak 15.7/16 GB GPU, weak model; LoRA marked resource-infeasible | Brief item 3 |
| `--shift` option (shift already applied: 0,0 raw, 4,-5 Cell Ranger); corrected the claim that scPrinter applies +4/-5 itself | Tooling trap (auto-detect gave 22/12 on sparse 10x) |
| Frontmatter `category: Data Analysis`, `author: GPTomics` | Brief item 1 |
| Removed from the references what SKILL.md already states: ATACorrect example, Tn5 shift subsection, depth and change-interpretation sentences, Inputs list. Fixed a literal newline in `one_match` printf | FIX_BRIEF: state each fact once |

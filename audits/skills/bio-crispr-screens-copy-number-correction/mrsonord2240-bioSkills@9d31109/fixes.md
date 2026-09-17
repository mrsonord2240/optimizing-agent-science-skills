# bio-crispr-screens-copy-number-correction fixes (2026-09-16)

Worktree `F:\OpenScience\wt\crispr-c`, branch `fix/r2-crispr-c`. Fixer: Claude Opus 5 (orchestrating
session). Runtimes: Chronos 2.3.15 in `audit-envs\crispr-screen-analyst\tools\chronos-venv`;
**CRISPRcleanR 3.0.1 on R 4.5.2 in a `bioconductor/bioconductor_docker:RELEASE_3_21` container**
(container `ccr3`, `Rqc` + `VariantAnnotation` from Bioconductor binaries, then
`remotes::install_github("francescojm/CRISPRcleanR")`). That is the first time this Skill's primary
tool has actually run for an audit or a fix pass on this machine — the Windows source build fails on
a `pthread_mutex_lock` link error (TOOLS.md section 3), the container sidesteps it entirely, and
**this is worth adding to `TOOLS.md` for the re-audit.** Scripts and data:
`F:\OpenScience\wt\_fixdata\cn\` (`prep_ccr.R`, `verify_diag.py`, `verify_chronos.py`).

## Round-2 audit pass — 2026-09-16

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Chronos example unrunnable: readcounts orientation is the transpose of what `check_inputs` requires | P0 | Rewrote the Chronos block: `check_inputs` call first, readcounts documented as rows = sequence_ID / columns = sgRNA, the required `sequence_map` (sequence_ID, cell_line_name, days, pDNA_batch) and `guide_gene_map` (sgrna, gene) columns spelled out, `negative_control_sgrnas` added with the reason | ran | Block extracted from the fixed SKILL.md and executed verbatim on a 3-line panel built from real HAP1 TKOv3 counts: `check_inputs` passes, `train(nepochs=100)` completes, `gene_effect` 3 x 18,056, essentials POLR2L -4.96/PCNA -4.13, P(dependent) POLR2L = 1.0 |
| Decision tree claimed Chronos works for a single cell line with matched CN | P0 | Decision-tree rows, the "Critical" note, the Failure Mode and a new Common Errors row now say `alternate_CN` requires >=3 cell lines and route single-line screens to CRISPRcleanR | ran (audit Input 3 RuntimeError) + docs (`copy_correction.py` line 104) | Added a ">=3 cell lines, CN available -> Chronos" row so the tree still has a Chronos entry |
| Spearman CN-bias diagnostic misses a single focal amplicon | P1 | `detect_cn_bias()` now also reports the amplified-vs-diploid mean-LFC gap with a one-sided Mann-Whitney test, and `bias_present` fires on either signal; added guidance to run it per candidate amplicon | ran | On the audit's planted HAP1 data: rho -0.034 (old function said no bias) but gap -2.47, p 2.9e-6 -> `bias_present: True`. Negative control (8 random genes relabelled CN 15, no artifact): gap -0.10, p 0.52 -> `bias_present: False` |
| `examples/run_crispr_cleanr.R` diagnostic reads `gw_lfc$gw_lfc` and `gw_lfc$CN`, columns `ccr.logFCs2chromPos` never returns | P1 | Rewrote the diagnostic to use the real columns (`genes`, `avgFC`; `correctedFC` post-correction), merge a CN profile by gene, `stopifnot` on the amplified match, and report pre/post Spearman as well as the mean shift | ran | Executed the whole example verbatim under CRISPRcleanR 3.0.1 on the real KY library (90,710 guides) with a planted 8-gene CN-15 amplicon: pre-correction amplified mean logFC -2.674 -> post -0.693 (recovers 2.0 of the planted 2.6), Spearman with CN -0.036 -> -0.009 |
| No scope note for adjacent clinical requests | P2 | Added a Scope paragraph at the top: analysis only, decline treatment/therapy recommendations and answer the computational part | docs | |
| (Found while fixing) `chronos.alternate_CN` returns `(corrected, shifts)`; the example assigned the tuple to one name and passed it to `get_probability_dependent` | P0-class, not in `recommendations[]` | Unpacks both values and says what `shifts` is | ran | The old form would have passed a tuple into `get_probability_dependent` |
| (Found while fixing) Failure Mode "Chronos fails on single-timepoint or single-cell-line data" and "Chronos requires CN as input" contradict the Skill's own "copy number is optional" | internal contradiction | Both rewritten: training works on one line, only the CN correction has the 3-line minimum; CN is optional to training and required only by `alternate_CN` | ran (audit Input 3 trained successfully on one line) | |
| (Found while fixing) usage-guide decision cheat sheet repeated "CRISPRcleanR or Chronos" for one line with CN | internal contradiction | Cheat sheet, agent checklist and Tips now carry the >=3-line rule and the real Chronos input schema | ran (same evidence) | |

All 5 `recommendations[]` entries (2 P0, 2 P1, 1 P2) fixed, plus three defects found while fixing.
Nothing left unfixed.

**For the re-auditor:** CRISPRcleanR is no longer un-runnable here. Use
`docker run --rm bioconductor/bioconductor_docker:RELEASE_3_21`, install `Rqc`, `VariantAnnotation`
(Bioconductor binaries, ~6 min) then `remotes::install_github("francescojm/CRISPRcleanR")`; bind-mounting
`F:` into the container hangs, so `docker cp` files in and out instead.

## Round-3 fix pass (post-fix re-audit, score 81) — 2026-09-16

Worktree `F:\OpenScience\wt\cn3`, branch `fix/r3-cn`, based on `openscience-fixes` @ `6847328`.
Runtime: Chronos 2.3.15 in `audit-envs\crispr-screen-analyst\tools\chronos-venv`. Scripts and copied
read-only data: scratchpad `cn3/` (`repro_p1.py`, `repro_p2.py`, real HT-29 pre/post gene-LFC+CN CSVs
and HAP1 planted-amplicon counts/CN, all copied from `F:\OpenScience\audits\bio-crispr-screens-copy-number-correction\`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Common Errors table named `UnboundLocalError('prior_variance')` during `train()` for a missing `negative_control_sgrnas`, carried over unverified from round 2 | P1 | Rewrote the inline comment and Common Errors row: `chronos.Chronos(...)` **construction** raises `ValueError("excess_variance was passed as dict without key for '<library>': {}")` before `train()` is ever called; noted the UnboundLocalError is real but internal (caught inside `_estimate_excess_variance`, re-raised as the ValueError, never escapes to the caller) | ran | Independent repro (not the audit's script) against the real single-line HAP1 planted data: traceback confirms `Chronos.__init__` -> `_build` -> `_estimate_excess_variance` line 1481 raises `UnboundLocalError` internally, caught by its own `except UnboundLocalError`, and line 1483 re-raises the `ValueError` shown above. Also checked `negative_control_sgrnas={'screen': []}` (empty, not omitted): different `ValueError` ("set of negative_control_sgrnas is empty"), also at construction. No path under default arguments reaches `train()` or lets `UnboundLocalError` escape. |
| `detect_cn_bias`'s post-correction re-diagnosis reads `bias_present: False` on a real, substantial residual gap purely from low power at its own `n>=3` floor | P2 | Added a `low_power_n=8` parameter and two new output fields, `low_power_floor` and `suspicious_despite_ns`; docstring and a new "Power caveat" paragraph tell the reader not to trust `bias_present: False` below the floor and to check the raw gap instead; added a Quantitative Thresholds row | ran | Extracted the function verbatim from the fixed SKILL.md and ran it on the real HT-29 pre/post CRISPRcleanR gene-LFC+CN data at the true FAM84B/MYC/POU5F1B block: POST now returns `bias_present: False, low_power_floor: True, suspicious_despite_ns: True` for the real gap=-0.98/p=0.208 case, instead of a bare, misleading `False`. Demonstrated the power problem itself by bootstrapping 500x from the real 3-value amplicon mixture at increasing n against the real diploid background: P(p<0.01) ~0.04 at n=3, ~0.13 at n=8, ~0.30 at n=15, ~0.53 at n=30 — confirms near-zero power at the documented floor, not merely asserted. |
| Reconciliation section didn't connect `alternate_CN`'s partial correction (round-2 fix log, CN=15 line -1.92->-1.20) to its own general re-diagnose guidance | P2 (3rd recommendation, same report) | Added cause 5: `alternate_CN` fits one curve across the panel, so a single extreme-CN line can retain residual signal; re-run `detect_cn_bias` per line, not only pooled | docs (restates the round-2 fix log's own already-verified real numbers; no new run needed) | |

All 3 `recommendations[]` entries (1 P1, 2 P2) fixed. Nothing left unfixed. Both changed Python
blocks in SKILL.md re-verified with `py_compile` after edits; the full `detect_cn_bias` function was
also extracted and re-run verbatim post-edit to confirm the documented behavior matches the code.

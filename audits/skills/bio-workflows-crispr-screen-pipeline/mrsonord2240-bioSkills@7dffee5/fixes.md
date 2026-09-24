# Fix log — bio-workflows-crispr-screen-pipeline (2026-09-16)

Commit: `b633bef` on `fix/r2-crispr-a` (worktree `F:\OpenScience\wt\crispr-a`).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| BAGEL2 `bf` unseeded, destabilizes Step 7 Tier consensus (Skill Veto T3 FAIL, Research Veto M3 FAIL) | P0 | Added `-s 42` to Step 6a's `BAGEL.py bf` command; added a determinism note before it, a Step 7 warning, and a Common Errors row, all pointing to `bagel-essentiality`'s Reproducibility section (same fix, already on this branch, commit `ead41a5`) | ran — reproduced the audit's own before/after BAGEL2 outputs (`bayes_factor.txt` vs `bayes_factor_run2.txt`): mean abs diff 1.3143, max 89.275, 39/18,053 BF>6 flips, exactly matching the eval report | one shared fix cited from three Skills (bagel-essentiality, hit-calling, this pipeline) rather than three separate explanations |
| Shipped "Replicate Pearson" QC formula conflates replicate and non-replicate pairs (Research Veto M3 FAIL) | P0 | Rewrote Step 3's snippet to group sample columns by condition (strip trailing replicate marker `_r1`/`_rep2`/`_A`/`_2`) and average only within-condition pairs | ran — reproduced audit's naive value 0.6769896801914643 with the original formula, then 0.7886812496284182 with the fixed formula, on the audit's real HAP1 TKOv3 data; both cited in the code's own comment | regex verified against both naming conventions used elsewhere in the Skill (`Veh_r1/Veh_r2`, `T18_A/T18_B/T18_C`, `Day14_r1..3`) |
| Step 2's and Step 6a's own worked examples don't compose (hard MAGeCK error) | P1 | Added a second Step 6a `mageck test` example using Step 2's own sample labels (`--treatment-id Veh_r1,Veh_r2 --control-id Day0`); kept the Day0/Day14 example as an explicit alternate | ran — against the audit's `experiment_step2scheme.count.txt`: completes cleanly, top depleted genes EIF3A/POLR2L/PCNA/GTPBP10 match the published HAP1 TKOv3 benchmark | also resolves the P2 mislabel below in the same edit |
| CN-bias QC threshold conflict: SKILL.md `abs(rho)<0.10` vs usage-guide.md `abs(rho)<0.05` | P1 | Made usage-guide.md's QC Checkpoints table match SKILL.md's frontmatter wording verbatim (kept SKILL.md's fuller statement as canonical) | docs (textual reconciliation, no code) | |
| No operational gate for the Skill's own "made-once commitments" principle | P1 | Added Step 0 (SKILL.md) / item 0 (usage-guide.md) instructing the agent to ask the user before proceeding if baseline, library control classes, screen type, or CN profile are unspecified | docs | |
| Step 6a example mislabeled "time-course dropout design" under a "Two-condition essentiality" heading, colliding with Step 6b | P2 | Renamed to "Day0/Day14 two-timepoint dropout convention", explicitly distinguished from Step 6b's multi-timepoint design | docs | folded into the Step 2/6a compose fix |

## Left unfixed

Nothing from the eval report or AUDIT.md's named defects for this Skill was left unfixed.

## Verification environment

BAGEL2 build 115, MAGeCK 0.5.9.5, `F:\OpenScience\audit-envs\crispr-screen-analyst`'s Python 3.12 venv. Real data: the audit's own `experiment.count.txt` (HAP1 TKOv3), `experiment_step2scheme.count.txt`, `bayes_factor.txt`/`bayes_factor_run2.txt` — read from `F:\OpenScience\audits\bio-workflows-crispr-screen-pipeline\{data,run}\`, copied to scratchpad for verification, not modified. All 4 changed SKILL.md Python blocks `py_compile`; `examples/crispr_pipeline.sh` (untouched — no BAGEL2 or QC-Pearson code path in it) passes `bash -n`.

## Final pass — 2026-09-24

Source commit: `7dffee58a50f7b4ef25d5922a1b95960f886a3f2` on `agent/final-pass-bio-workflows-crispr-screen-pipeline-20260924` (worktree `F:\OpenScience\worktrees\bio-workflows-crispr-screen-pipeline-finalpass`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| Step 6b MLE silently uses MAGeCK's two-round permutation default, destabilizing near-0.05 FDR calls | P1 | Added `--permutation-round 10` to the documented command, a boundary-call caveat, and a Common Errors recovery row that points to `mageck-analysis` | ran + help — MAGeCK 0.5.9.5 `mle --help` says suggested 10/default 2; final-pass real-data regression uses the documented flag | Implements the prior report's open P1 without claiming the default was scientifically invalid for non-boundary exploration. |
| Step 3's replicate-Pearson hard gate drifted from frontmatter, usage-guide.md, and screen-qc | P2 | Replaced flat `>0.85` with `>=0.8` MAGeCK-VISPR floor and `>0.85` acceptable | docs — exact text cross-check against frontmatter and usage-guide.md | A screen at 0.82 now receives one consistent verdict. |
| Bundled `examples/crispr_pipeline.sh` was not discoverable through shipped documentation | P2 | Added an Output Files pointer with the example's RRA-only scope | ran — target exists and `bash -n` passes in WSL | Keeps the QC/design gates in SKILL.md authoritative. |

## Final-pass left unfixed

Nothing from the current canonical report's open P0/P1/P2 recommendations remains unfixed.

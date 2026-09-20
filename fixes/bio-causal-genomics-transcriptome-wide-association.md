# Fix log: bio-causal-genomics-transcriptome-wide-association (2026-09-19)

Source: `causal-genomics/transcriptome-wide-association`. Audit: 80/100, Limited Release, deployable,
2 P1 + 3 P2 open. Fix commit: `fix/cg-twas` @ `4a67b94` in
`F:\OpenScience\external\mrsonord2240__bioSkills` (worktree `F:\OpenScience\wt\cg-twas`, not merged).

| finding | priority | change | verified | notes |
|---|---|---|---|---|
| `pip install pyfocus` (bare, as usage-guide.md instructed) crashes every `focus` call: pandas>=2.2 removed `delim_whitespace`, called throughout pyfocus 0.802's data-loading code | P1 | Pinned `pandas<2.2` + `setuptools<81` (pyfocus imports `pkg_resources`, gone from recent setuptools) in SKILL.md Tool Install Notes, the FOCUS section, `examples/focus_finemap.sh`, and usage-guide.md | ran | The pin alone is not sufficient -- see next row, found only by pushing the verification further than the pin |
| Pinning pandas alone still crashes: `AttributeError: module 'numpy' has no attribute 'warnings'` -- `ldref.py`/`exprref.py` call the removed `np.warnings` alias, and no numpy version with Python 3.11/3.12 wheels still has it | P1 (same root issue as above; audit's own suggested fix was incomplete) | Documented a 2-line post-install source patch (`sed`, replacing `np.warnings.*` with the already-imported/added stdlib `warnings` module) in SKILL.md Tool Install Notes | ran -- isolated fresh venv (Python 3.12), patched pyfocus 0.802: `focus finemap` then runs through real GWAS parsing, LD-ref parsing, weight-DB parsing, and the full genome-wide independent-region scan with no crash (own-fixture data; stopped at "no overlapping weights" only because the test used an S-PrediXcan-schema DB, not a real FOCUS DB -- a fixture limitation, not a Skill bug) | Verified in a scratchpad venv, never the shared candidate env (`twas-venv`), per the no-shared-version-change rule |
| `focus finemap` also crashes with "Please specify independent regions location..." unless `--locations` is passed, even single-ancestry -- contradicts the shipped example's own comment that it's optional | P1-adjacent (blocks the same fix's own verification) | Added `--locations 38:EUR` to SKILL.md's FOCUS CLI example and `examples/focus_finemap.sh`; corrected the wrong comment | ran (real pyfocus 0.802 CLI) | |
| FUSION.post_process.R crashes on single-SNP ("top1") genes: `Error in wgt.matrix[qc$flip, ] : incorrect number of dimensions` | P1 | Documented the crash, root cause (`wgt.matrix[m.keep,]` missing `drop=FALSE`), and a 2-line patch in Common Errors | ran -- reproduced the exact crash on real planted FUSION fixtures (`gusevlab/fusion_twas` HEAD, GENE1/GENE2 synthetic top1 weights over a real 957-indiv/14389-SNP LD panel) | |
| The documented single-line patch (`drop=FALSE` on `wgt.matrix`) is not sufficient by itself | P1 (same finding, deeper) | Documented a second required `drop=FALSE` on `cur.genos = genos$bed[,m[m.keep]]` (the very next line) in Common Errors, both occurrences (lines ~168/170 and ~251/254) | ran -- with both patches, `FUSION.post_process.R` completes and correctly retains the true signal (GENE1, JOINT.P=8e-11) while dropping the null gene (GENE2, COND.P=0.58) against ground truth | Found only because I verified the audit's suggested one-line fix by actually running it, not by reading source alone |
| MA-FOCUS colon-separated paths collide with Windows drive letters | P2 (cheap) | Documented as a general FOCUS caveat (not MA-FOCUS-specific -- confirmed it also breaks single-ancestry runs) in SKILL.md's FOCUS section and `examples/focus_finemap.sh` | ran -- an absolute `F:/...` single-ancestry path mis-detected "2 populations" | Audit had framed this as MA-FOCUS-only; broadened per the reproduced evidence |
| (found during verification, not in audit recommendations) SMulTiXcan.py example missing `--cutoff_condition_number`, a failed dynamic-audit assertion (Input 4) | not listed / cheap | Added the flag to SKILL.md's S-MultiXcan example and a Common Errors row | confirmed via audit's own assertion evidence (`InvalidArguments` without it); not independently re-run | |
| (found during verification) `examples/focus_finemap.sh`'s PIP filter reads a `pip` column that installed pyfocus 0.802 never writes -- real output is `pips_pop1`/`pips_me` | not in audit | Fixed the awk filter and added a Common Errors row | confirmed by reading `pyfocus/finemap.py`'s `create_output()` (renames columns to `pips_pop{i+1}`/`pips_me`); not exercised end-to-end since my synthetic run never reached the PIP stage (fixture DB was the wrong schema) | Silent-wrong-answer bug, not a crash -- would have passed unnoticed |

## Left unfixed

- P2 "464-line SKILL.md, no references/ split" and P2 "FUSION has no standalone example script" --
  restructuring/new-content, out of scope for a defect fix pass.
- Did not build a real FOCUS-format weight database, so the pyfocus pin+patch fix was verified through
  the entire pipeline except the final PIP computation itself (blocked on "no overlapping weights" from
  a mismatched fixture schema, not a Skill or pyfocus defect) -- a future audit with a real `focus
  import`-built DB should confirm PIP output values.

## Needs Sam

Nothing blocking. Two of the four "P1" rows above are the audit's original findings; the other two are
deeper bugs the same code paths hit immediately after applying the audit's own suggested one-line fixes
-- flagging in case the re-auditor wants to weigh that when re-scoring reliability.

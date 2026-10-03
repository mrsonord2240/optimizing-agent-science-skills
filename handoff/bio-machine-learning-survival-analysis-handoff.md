# Handoff: bio-machine-learning-survival-analysis / orchestrator commit and intake

- Updated: 2026-10-03
- Lane: 3 (batch 3b-2)
- Status: candidate-ready
- Owner leaving: reaudit-scientific-skill worker (final mode, independent)
- Next role: orchestrator (commit the exact bytes, then local Marketplace intake). SA-006 is an optional text-only fix; if applied the identity changes and needs delta mode.

## Source identity

- Origin: GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:machine-learning/survival-analysis
- Working tree: F:\OpenScience\wt\ml-lane3-normalize\skills\bio-machine-learning-survival-analysis (untracked by design; branch normalize/ml-lane3 off 29f5446)
- Candidate tree hash: c60f873f52f63ad78a5009b351f8451510f86bbae3f7d46886c03e3bcf9eaf39 (files=5, bytes=33891); `tools/skill_preflight.py --offline` PASS before and after; no Skill bytes touched, no __pycache__
- Applicable audit: audits\skills\bio-machine-learning-survival-analysis\candidate@c60f873f52f6-reaudit-lane3b-20261003 (supersedes the initial 2dc45fa24b13 record)

## Completed this phase

- Verdict: candidate-ready. Final 86 (Production Ready), static 87, execution average 85.4 (Layer 1 34.6/40, Layer 2 50.8/60), assertions 23/24; skill and research veto PASS; no open P0 or P1.
- SA-001..SA-005 all resolved by independent retest: KM baseline equals hand table, a numpy KM and lifelines; GBSG2 IBS 0.1775 vs an independent numpy Graf IBS 0.1775 (old 0.2627). Alpha selection verified train-only by data-flow spy and test-set permutation (alpha 0.3968 GBSG2, 0.1827 p>>n unchanged); p>>n 161 nonzero / Uno C 0.708 -> 6 / 0.791.
- Both SKILL.md python blocks run verbatim; sksurv cumulative_incidence_competing_risks == lifelines AJ == hand table; competing_risks_cif.py and failure-modes.md hash-identical to the audited bytes; lifelines sign trap 0.337 / 0.663.
- Record published and views regenerated; `npm run audits:check` passes.

## Open findings

| ID | Severity | State | Evidence | Required disposition |
|---|---|---|---|---|
| SA-006 | P2 | open, new | viewer.md input 4; evidence/ra_times_range.log | Reword Common Errors row: times fail at or beyond the largest test follow-up time (event or censored), not "beyond largest uncensored test time". Text only, optional |

## Environment and evidence

- Tool inventory: F:\OpenScience\audits\bio-machine-learning-survival-analysis\TOOLS.md (sha256 4a6085401794...); environment fingerprint 20291632e93a... and both freezes re-hashed identical
- Run evidence: F:\OpenScience\audits\bio-machine-learning-survival-analysis\reaudit-lane3b-20261003\ (scripts/ra_*.py, scripts/evidence/*.log)
- Not executed, labelled in the Skill: Fine-Gray (cmprsk), CIF Brier (riskRegression), randomForestSRC, landmarking, calibration curves, nested CV, boosting, SVM, Cox-Time. pycox smoke rerun only (0.615 / 0.620), DeepHit competing-risk mode not run. Harrell-vs-Uno evidence reused from the initial audit.
- Tooling note: TOOLS.md still quotes the old survival_real.py lifelines figures 0.308/0.692; measured 0.337/0.663 (cosmetic).
- Blockers, restricted access: none

## Worktree safety

- Run-owned: reaudit-lane3b-20261003\ run dir, the new record dir, regenerated audits\INDEX.md, BACKLOG.md, STATUS.md, STATUS.html, this handoff
- Untouched: records test/validate.bats, shelf .vscode/, sibling Skill dirs; no process killed; no commit or push

## Transition assertion

- Next-phase prerequisites met: yes

# Brief: fix audited defects in Sam's bioSkills fork (2026-09-15)

Round-2 audits found that many `GPTomics/bioSkills` Skills fail on broken commands, version drift and
snippets that run but silently compute the wrong thing. Sam decided to ship fixed local versions from
his own fork instead of dropping those Skills. You are the **fixer** for ONE candidate. A different
agent re-audits your work afterwards; you never score anything.

## Where things are

- Fork (MIT, same history as upstream): `F:\OpenScience\external\mrsonord2240__bioSkills`, base
  branch `openscience-fixes` at upstream `d91ed3d563019e649dc854c56ccd62551359488a`.
- **Your worktree and branch** are named in your dispatch message. Work only there.
- Evidence per Skill: `F:\OpenScience\audits\<skill-id>\eval_report_<skill-id>_result.json`
  (`recommendations[]`, per-input notes) and `eval_viewer_<skill-id>.md` (the commands that ran, what
  failed, and often the corrected command the auditor verified). Candidate verdict:
  `F:\OpenScience\specialist-src\<candidate-id>\AUDIT.md` (may still be being written).
- Runtimes: the candidate venv `F:\OpenScience\audit-envs\<candidate-id>\` (Python 3.12, R library
  `R-lib`, tools under `tools\` or `Scripts\`), R at `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe`.

## What to fix

Every P0 and P1, and any P2 that is cheap, in the Skills listed in your dispatch — when the fix is a
correction, not new content:

- broken commands, wrong or renamed flags, tool binaries that no longer exist under that name;
- version drift: update to the current documented usage and name the version it was checked on
  (e.g. "checked on ClipKIT 2.14.0"); keep an older-version note only if the old form still matters;
- wrong field, function, class or column names; API paths that no longer match the live service;
- shipped `examples/` and scripts that crash, parse wrongly, or use the wrong defaults;
- claims contradicted by the tool's own help/docs or by what the audit actually ran;
- internal contradictions (a default that breaks the Skill's own rule).

Method-level changes are allowed only when the audit demonstrated the problem with a run (e.g. a
recommended default that distorted branch lengths). Say what the evidence was.

**Not in scope:** new sections, new tools, broader coverage, restyling prose, rewriting what works.
Keep diffs minimal. Never change the frontmatter `name`. Change `description` only if it is wrong.
Do not tune text toward the audit's assertions; fix the defect the assertion exposed.

## Verify every change

- Run each changed command or snippet when the tool runs on this machine, on the audit's synthetic
  data (`F:\OpenScience\audits\<skill-id>\data\`, read-only — copy what you need to your scratchpad).
- If it cannot run here, check it against the tool's `--help` output or official documentation and
  say which.
- Every changed `.py` must `py_compile`; every changed `.R` must parse (`Rscript -e "parse('f.R')"`);
  every changed `.sh` must pass `bash -n`.
- Never claim a fix ran when it did not.

## Record

- One commit per Skill on your branch, `git commit -F <msgfile>`:
  `fix(<folder>/<skill>): <one-line summary>`, body = one line per finding → change → how verified,
  ending with `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- `F:\OpenScience\specialist-src\round2\fixes\<skill-id>.md` (outside the fork, so it never ships):
  dated heading, then a table `finding | priority | change | verified (ran / help / docs) | notes`, and
  a list of findings left unfixed with the reason.

## Rules

- Never write in `F:\OpenScience\external\GPTomics__bioSkills`, `F:\OpenScience\audits`, other
  worktrees, `F:\OpenScience\skills`, or the builder. Do not push, merge or rebase.
- Skills that already pass as core and have no P1 stay byte-identical.
- Public unauthenticated services (NCBI E-utilities, myvariant.info, gnomAD GraphQL, Ensembl) are fine
  for verifying database Skills; nothing paid or authenticated.
- Windows: edit with Write/Edit or Python `encoding='utf-8'`; never PowerShell `Get-Content`/`Out-File`.
  Prefix Python with `PYTHONIOENCODING=utf-8` in Bash. Keep paths short.
- At most one sub-agent of your own at a time; the machine is shared with one other fixer.

## Final message (≤ 200 words)

Per Skill: commit hash, findings fixed k/N, anything left unfixed and why. Anything that needs Sam.

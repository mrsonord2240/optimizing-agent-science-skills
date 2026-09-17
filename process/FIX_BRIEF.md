# Brief: fix audited defects in Sam's bioSkills fork (2026-09-15)

Round-2 audits found that many `GPTomics/bioSkills` Skills fail on broken commands, version drift and
snippets that run but silently compute the wrong thing. Sam decided to ship fixed local versions from
his own fork instead of dropping those Skills. You are the **fixer** for ONE candidate. A different
agent re-audits your work afterwards; you never score anything.

## Where things are

- Fork (MIT, same history as upstream): `F:\OpenScience\external\mrsonord2240__bioSkills`, base
  branch `openscience-fixes` at upstream `d91ed3d563019e649dc854c56ccd62551359488a`.
- **Your worktree and branch** are named in your dispatch message. Work only there.
- Records repository (briefs, gates, fix logs, audit records):
  `F:\optimizing-agent-science-skills` — gates in `process\THRESHOLD.md`, your fix logs in
  `fixes\`. The fixed Skill trees are exported there from the fork under `skills\bioSkills\`;
  that export is a separate step, not yours.
- Evidence per Skill: `F:\OpenScience\audits\<skill-id>\eval_report_<skill-id>_result.json`
  (`recommendations[]`, per-input notes) and `eval_viewer_<skill-id>.md` (the commands that ran, what
  failed, and often the corrected command the auditor verified). Candidate verdict:
  `F:\OpenScience\specialist-src\<candidate-id>\AUDIT.md` (may still be being written).
- Runtimes: the candidate venv `F:\OpenScience\audit-envs\<candidate-id>\` (Python 3.12, R library
  `R-lib`, tools under `tools\` or `Scripts\`), R at `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe`
  — **never invoked bare: it exits 0 and prints nothing unless `.r/Library/bin` and
  `.r/Library/mingw-w64/bin` are on `PATH`** (verified 2026-09-17). Use a wrapper such as
  `F:\OpenScience\audit-envs\mendelian-randomization-analyst\r.sh`.

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

## Missing referenced executables (2026-09-15)

A Skill that names a tool, method or routine and ships no runnable code for it has a defect, not a
gap in coverage — the audits keep capping such Skills below their floor, and three separate fixers
declined the work as "new content" before Sam settled it: **write the executable.**

So when the Skill's own `SKILL.md`, `usage-guide.md` or decision tree references something a user
could reasonably expect to run, you have three options and must take one:

- **write it** — a runnable block in the Skill's existing voice and structure, using a tool that is
  actually installed on this machine (check the candidate's `TOOLS.md` first); or
- **install it** — when the tool is a public, unauthenticated install that the candidate's tooling
  pass simply missed, install it into the candidate's own env under that env's no-version-change
  rule, add it to `TOOLS.md` with a smoke test, and then write the runnable block; or
- **delete the claim** — remove it from the description, decision tree and prose, so the Skill stops
  advertising what it cannot do.

Leaving it as an unbacked mention is not an option. Prefer writing it when the tool is installed and
the audit's assertions show a user was expected to run it; prefer deleting when the tool is
registration-gated, absent, or outside the Skill's scope. Say which you chose and why.

This is bounded by what the Skill already claims. It is not licence for broader coverage: extend the
existing sections, do not restructure them, and do not add a tool the Skill never mentioned.

**Still not in scope:** broader coverage, new tools the Skill does not reference, restyling prose,
rewriting what works. Keep diffs minimal. Never change the frontmatter `name`. Change `description`
only if it is wrong, or to drop a claim you deleted under the rule above. Do not tune text toward the
audit's assertions; fix the defect the assertion exposed.

## Verify every change

- Run each changed command or snippet when the tool runs on this machine, on the audit's synthetic
  data (`F:\OpenScience\audits\<skill-id>\data\`, read-only — copy what you need to your scratchpad).
- If it cannot run here, check it against the tool's `--help` output or official documentation and
  say which.
- Every changed `.py` must `py_compile`; every changed `.R` must parse (`Rscript -e "parse('f.R')"`);
  every changed `.sh` must pass `bash -n`.
- **Code you write under "Missing referenced executables" must actually execute** — "it parses" is not
  evidence. Run it, and where you can, show it recovers something checkable (a known spike-in ratio, a
  realized FDR against planted truth) rather than merely exiting zero. Record the exact version of
  every tool you invoke.
- Never install into the shared venv or R library, and never change a version there — other agents
  are using it. If you need a package that is absent, say so in your final message instead.
- Never claim a fix ran when it did not, and never diagnose from a single exit code — confirm with a
  second independent method.

## Record

- One commit per Skill on your branch, `git commit -F <msgfile>`:
  `fix(<folder>/<skill>): <one-line summary>` — or `feat(...)` when the commit is mostly executables
  written under "Missing referenced executables" — body = one line per finding → change → how
  verified, ending with `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>`.
- `F:\optimizing-agent-science-skills\fixes\<skill-id>.md` (outside the fork, so it never ships):
  dated heading, then a table `finding | priority | change | verified (ran / help / docs) | notes`, and
  a list of findings left unfixed with the reason.

## Rules

- Never write in `F:\OpenScience\external\GPTomics__bioSkills`, `F:\OpenScience\audits`, other
  worktrees, `F:\OpenScience\skills`, or the builder. Do not push, merge or rebase. In the records
  repository write only your `fixes\<skill-id>.md`; `skills\bioSkills\` there is an export of the
  fork, never edited by hand.
- Skills that already pass as core and have no P1 stay byte-identical.
- Public unauthenticated services (NCBI E-utilities, myvariant.info, gnomAD GraphQL, Ensembl) are fine
  for verifying database Skills; nothing paid or authenticated.
- Windows: edit with Write/Edit or Python `encoding='utf-8'`; never PowerShell `Get-Content`/`Out-File`.
  Prefix Python with `PYTHONIOENCODING=utf-8` in Bash. Keep paths short.
- At most one sub-agent of your own at a time; the machine is shared with one other fixer.

## Final message (≤ 200 words)

Per Skill: commit hash, findings fixed k/N, anything left unfixed and why. Anything that needs Sam.

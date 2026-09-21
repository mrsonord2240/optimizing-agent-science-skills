# Brief: fix audited defects in Sam's bioSkills fork (2026-09-15)

Round-2 audits found that many `GPTomics/bioSkills` Skills fail on broken commands, version drift and
snippets that run but silently compute the wrong thing. Sam decided to ship fixed local versions from
his own fork instead of dropping those Skills. You are the **fixer** for ONE Skill. A different
agent re-audits your work afterwards; you never score anything.

## Two facts

- **Skill ID is the SKILL.md frontmatter `name`, not the folder name.** Every report, audit folder
  and `--skill` argument depends on it.
- **Upstream provenance.** `GPTomics/bioSkills` at `d91ed3d` (MIT) is the base, and the read-only
  clone is `F:\OpenScience\external\GPTomics__bioSkills`. Diff against it to see the original.

## Where things are

- Fork (`bioSkills-Improved`, MIT, same history as upstream):
  `F:\OpenScience\external\mrsonord2240__bioSkills`. Staging is its `main`, and every fix lands there.
- **Your worktree and branch** are named in your dispatch message. Work only there.
- Records repository (briefs, thresholds, fix logs, audit records):
  `F:\optimizing-agent-science-skills` — thresholds in `process\THRESHOLD.md`, your fix logs in
  `fixes\`. The fixed Skill trees are exported there from the fork under `skills\bioSkills\`;
  that export is a separate step, not yours.
- Evidence per Skill: `F:\OpenScience\audits\<skill-id>\eval_report_<skill-id>_result.json`
  (`recommendations[]`, per-input notes) and `eval_viewer_<skill-id>.md` (the commands that ran, what
  failed, and often the corrected command the auditor verified).
- Runtimes: the env venv `F:\OpenScience\audit-envs\<env>\` (Python 3.12, R library
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
  actually installed on this machine (check the env's `TOOLS.md` first); or
- **install it** — when the tool is a public, unauthenticated install that the folder's tooling
  pass simply missed, install it into the env under its no-version-change
  rule, add it to `TOOLS.md` with a smoke test, and then write the runnable block; or
- **delete the claim** — remove it from the description, decision tree and prose, so the Skill stops
  advertising what it cannot do.

Leaving it as an unbacked mention is not an option. Prefer writing it when the tool is installed and
the audit's assertions show a user was expected to run it; prefer deleting when the tool is
registration-gated, absent, or outside the Skill's scope. Say which you chose and why.

This is bounded by what the Skill already claims. It is not licence for broader coverage: extend the
existing sections, do not restructure them, and do not add a tool the Skill never mentioned.

## Remove redundancy, every pass (2026-09-17)

Sam's rule: **every Skill a fixer touches leaves with each fact stated once**, whether or not the audit
flagged duplication. Two copies drift — a fix lands in one and the other keeps the bug — and every
repeated line costs the agent context.

- `SKILL.md` is what the agent loads, so it is the single home for anything the agent acts on:
  commands, thresholds, decision flows, failure modes, interpretation tables, install notes, caveats.
- `usage-guide.md` keeps only what is for the human choosing the Skill: a short overview, example
  prompts, and related Skills. Everything else in it that restates `SKILL.md` is deleted. Where the
  guide needs the point, it names the `SKILL.md` section instead of repeating it.
- Content that exists **only** in `usage-guide.md` but that the agent needs (a table `SKILL.md` points
  at, a tip found nowhere else) moves into the matching `SKILL.md` section — it is not deleted.
- Repetition inside `SKILL.md` (a Tips list re-saying the failure-mode sections, a threshold given in
  three places) collapses to the one section where it belongs.
- When two copies disagree, keep the one the audit's runs support, and log the disagreement.
- Shipped `examples/` scripts are out of this rule: a runnable file beside an inline block is not a
  duplicate.

Verify by listing, in the fix log, every deleted passage and where its content now lives. Nothing
the agent needs may leave the Skill. This is the one restructuring a fixer does.

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
- Skills that already score ≥ 85 with no P1 stay byte-identical.
- Public unauthenticated services (NCBI E-utilities, myvariant.info, gnomAD GraphQL, Ensembl) are fine
  for verifying database Skills; nothing paid or authenticated.
- **Never kill a process by image name**; kill the PID you started. Python on Windows cannot read
  MSYS `/f/...` paths: use `F:\...`.
- Windows: edit with Write/Edit or Python `encoding='utf-8'`; never PowerShell `Get-Content`/`Out-File`.
  Prefix Python with `PYTHONIOENCODING=utf-8` in Bash. Keep paths short.
- At most one sub-agent of your own at a time; the machine is shared with other agents.

## Final message (≤ 200 words)

Per Skill: commit hash, findings fixed k/N, anything left unfixed and why. Anything that needs Sam.

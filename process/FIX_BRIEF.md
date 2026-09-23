# Brief: fix audited defects in one Skill

Read `COMMON.md` first. You are the **fixer** for ONE Skill. A different agent re-audits your work
afterwards; you never score anything. Your dispatch names the Skill, your worktree and branch (work only
there), and the env.

## Evidence

- `F:\OpenScience\audits\<skill-id>\eval_report_<skill-id>_result.json` (`recommendations[]`, per-input
  notes) and `eval_viewer_<skill-id>.md` (what ran, what failed, often the corrected command the auditor
  verified).
- The audit's data at `F:\OpenScience\audits\<skill-id>\data\` is read-only; copy what you need to your
  scratchpad.
- Diff against `GPTomics__bioSkills` to see the original.

## What to fix

Every P0 and P1, and any cheap P2, when the fix is a correction, not new content:

- broken commands, wrong or renamed flags, binaries that no longer exist under that name;
- version drift: update to the current documented usage and name the version checked (e.g. "checked on
  ClipKIT 2.14.0"); keep an older-version note only if the old form still matters;
- wrong field, function, class or column names; API paths that no longer match the live service;
- shipped `examples/` and scripts that crash, parse wrongly or use the wrong defaults;
- claims contradicted by the tool's own help/docs or by what the audit ran;
- internal contradictions (a default that breaks the Skill's own rule).

Method-level changes only when the audit demonstrated the problem with a run (e.g. a recommended default
that distorted branch lengths). Say what the evidence was.

Skills already scoring ≥ 85 with no P1 stay byte-identical unless named in a fix batch (Sam, 2026-09-21:
Production Ready Skills are fixed down to their P2s and split when over 300 lines).

## Missing referenced executables (2026-09-15)

A Skill that names a tool, method or routine a user could reasonably expect to run, and ships no runnable
code for it, has a defect. Take one of three options:

- **write it**: a runnable block in the Skill's voice, using a tool installed here (check `TOOLS.md`);
- **install it**: when it is a public, unauthenticated install the tooling pass missed, install it under
  COMMON's install rules, add it to `TOOLS.md` with a smoke test, then write the block;
- **delete the claim** from the description, decision tree and prose, so the Skill stops advertising it.

Leaving an unbacked mention is not an option. Prefer writing when the tool is installed and the audit
shows a user was expected to run it; prefer deleting when the tool is registration-gated, absent, or out
of scope. Say which you chose and why. This is bounded by what the Skill already claims: extend existing
sections, add no tool the Skill never mentioned.

## State each fact once (2026-09-17)

Every Skill you touch leaves with each fact stated once, whether or not the audit flagged it.

- `SKILL.md` is what the agent loads: the single home for commands, thresholds, decision flows, failure
  modes, interpretation tables, install notes and caveats.
- `usage-guide.md` keeps only what the human choosing the Skill needs: a short overview, example prompts,
  related Skills. Anything restating `SKILL.md` is deleted; where the guide needs the point, it names the
  `SKILL.md` section.
- Content only in `usage-guide.md` that the agent needs moves into the matching `SKILL.md` section.
- Repetition inside `SKILL.md` collapses to the one section where it belongs.
- When two copies disagree, keep the one the audit's runs support, and log the disagreement.
- `examples/` scripts are exempt: a runnable file beside an inline block is not a duplicate.

List every deleted passage in the fix log and where its content now lives. Nothing the agent needs may
leave the Skill.

## Split long Skills into `references/` (2026-09-21)

A `SKILL.md` over 300 lines is split: method-specific blocks (one method, tool or advanced model per file)
move verbatim to `references/<topic>.md`, with a "Reference Files" index in `SKILL.md` saying when to read
each, and a pointer from the decision-tree row that needs it. Scope, decision tree, thresholds, Common
Errors and install stay. Verify no non-blank line was lost and every moved fence still parses.

## Runnable code goes in `scripts/` (2026-09-21)

- A complete runnable block (pipelines, helpers, multi-step recipes of roughly 15+ lines) moves to
  `<skill>/scripts/<name>.py|R|sh`, and `SKILL.md` keeps a one- to three-line invocation. One-liners and
  explanatory fragments stay inline. Where sensible, not everywhere.
- Each script has a header comment (purpose, inputs, usage), takes inputs as arguments or named variables
  at the top, and **is run** on the audit's data with assertions, exactly as `SKILL.md` invokes it.
- Move verbatim, then parametrise. Log each move (old location → script path).
- If a block duplicates an `examples/` script, point at the example and delete the copy.
- A code block inside a reference file moves to `scripts/` too. Do it as its own commit, after the fix
  and the split.

**Not in scope:** broader coverage, new tools, restyling prose, rewriting what works. Keep diffs minimal.
Never change the frontmatter `name`. Change `description` only if it is wrong or to drop a deleted claim.
Do not tune text toward the audit's assertions; fix the defect the assertion exposed.

## Verify every change

- Run each changed command or snippet on the audit's data when the tool runs here; otherwise check it
  against `--help` or official docs and say which.
- Every changed `.py` must `py_compile`, `.R` must `parse()`, `.sh` must pass `bash -n`. That is the
  minimum, never the evidence.
- Code written under "Missing referenced executables" must execute and, where possible, recover something
  checkable (a known spike-in ratio, a realized FDR against planted truth). Record every tool version.

## Record

- One commit per Skill on your branch, via `git commit -F <msgfile>`: `fix(<folder>/<skill>): <summary>`
  (`feat(...)` when mostly new executables). Body: one line per finding → change → how verified, ending
  with a `Co-Authored-By:` line for your model.
- `F:\optimizing-agent-science-skills\fixes\<skill-id>.md`: dated heading, a table
  `finding | priority | change | verified (ran / help / docs) | notes`, and **every finding left unfixed
  with its reason** (needs a forbidden install, needs data that does not exist, out of scope, not a
  correction...). "Not cheap" alone is not a reason; say what the work needs.
- At most one sub-agent of your own at a time.

## Final message (≤ 200 words)

Per Skill: commit hash, findings fixed k/N, anything left unfixed and why. Anything that needs Sam.

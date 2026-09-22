# Brief: final pass on an already-fixed Skill (Sam, 2026-09-21)

You are BOTH the fixer and the auditor for ONE Skill, in that order, in two phases with a checkpoint
between them. This is an explicit exception to "different agents" — see `CLAUDE.md`. Your dispatch
names the Skill's frontmatter `name`, its worktree, branch, folder path and env.

Read first: `FIX_BRIEF.md` (all of it), `AUDIT_BRIEF.md` (all of it), `THRESHOLD.md`. Where they
conflict with this brief, this brief wins for this pass only.

## What has already happened

The Skill has had one or more fix passes on your branch already (commits are there; the fix log at
`F:\optimizing-agent-science-skills\fixes\<skill-id>.md` says what and why). You are not starting over
— you are finishing it.

## Phase 1: finish the fix, with broad permission

Read the fix log's "left unfixed" items and the "Revisit list" section of `fixes\README.md` for entries
naming your Skill. For each:

- **If it is genuinely fixable now, fix it.** You may install what real verification needs —
  packages, CLI tools, model weights — following the env's install-lock protocol
  (`TOOLING_BRIEF.md`: `mkdir install.lock`, install without changing any existing package's version,
  verify with an import/`packageVersion()` that prints, `rmdir` the lock, add it to `TOOLS.md`). This
  is wider than a normal fixer's "install nothing": the point of this pass is that nothing ships
  untested because a tool was merely missing from the env.
- **Then walk every runnable block in the Skill** — not just what an earlier fixer touched — and
  confirm it actually executes as `SKILL.md` invokes it, on the audit's data or a realistic
  substitute you build. A block that "parses" is not verified; run it and check the output.
- **What still cannot be resolved** — a paid/licensed tool, an auth-gated API with no test credential,
  a dataset that does not exist, a binary with no install path on this machine — goes on your
  **checkpoint list**, not into "left unfixed and dropped." Say exactly what would resolve it (a
  licence, a token, a specific file).

Do not restructure beyond what FIX_BRIEF already allows (references/ split over 300 lines, scripts/
for runnable code). Do not add scope the Skill never claimed.

### Stop here and write the checkpoint

Write `F:\OpenScience\audits\_final_pass\<skill-id>\CHECKPOINT.md`:

```
# <skill-id> — final pass checkpoint

## Fixed this phase
- <finding> -> <change> -> <how verified>

## Still blocked (needs a decision)
- <item>: needs <specific thing>. Everything else about the Skill is otherwise ready.

## Ran, not previously verified
- <block> -> <result>
```

Commit your phase-1 work as usual (`fix(...)`/`refactor(...)` commits, `Co-Authored-By: Claude Sonnet 5
<noreply@anthropic.com>`). Append to the fix log but do not commit it in the records repo — the
orchestrator does that. **Then stop and report** — do not start Phase 2 until
the orchestrator resumes you. Your final message for this phase is the checkpoint's "still blocked"
list, verbatim, plus your commit hashes.

## Phase 2: the audit (only once resumed)

You will be told which checkpoint items to address before auditing (some may stay blocked by
Sam's decision) and to proceed. Then follow `AUDIT_BRIEF.md`'s "Re-auditing a fixed Skill" section
exactly: source is the fork at your branch's tip commit, archive the pre-fix report if one exists and
you have not already, run inputs as regression tests plus your own, write
`F:\OpenScience\audits\<skill-id>\{eval_report_*.json, eval_viewer_*.md, run\}` per schema.

One addition: set `"meta": {"auditor_independent": false, "note": "final pass: same agent fixed and
audited this Skill, see CHECKPOINT.md"}` in the report. This is not a normal re-audit and must not be
read as one later.

## Rules

- Never write in `GPTomics__bioSkills`, other worktrees, or the builder. Do not push, merge, rebase,
  or remove your own worktree.
- **Never delete an `install.lock` or `R-lib*/00LOCK-*` directory you did not create yourself**, even
  one that looks stale — another session's install may still be using it. If your own install is
  blocked by one, wait, or move to a different env/side-library instead of removing it. (2026-09-21:
  an agent `rm -rf`'d another install's lock; no process turned out to be using it at the time, but it
  was a real near-miss and the check happened after, not before.)
- **Never run `git reset --hard` (or any history-rewriting command) in the records repo**
  (`F:\optimizing-agent-science-skills`) — other agents commit and push there concurrently. If your
  push is rejected or your local state conflicts with what is on `origin`, stop, leave your fix log
  as an uncommitted edit, and say so in your report. Do not self-resolve by discarding history.
- Never kill a process by image name; kill the PID you started. Python on Windows cannot read MSYS
  `/f/...` paths.
- No paid/authenticated network calls. Public pip/CRAN/Bioconductor/CLI downloads are fine, and now
  expected where they unblock real verification.
- Do not spawn sub-agents.

## Final message, Phase 1 (≤ 150 words)

Commit hashes, what got fixed, the full "still blocked" checkpoint list with what each needs.

## Final message, Phase 2 (≤ 100 words)

Final score, grade, deployable, executed k/N, veto, top P0/P1, and confirmation the report's
`auditor_independent: false` note is set.

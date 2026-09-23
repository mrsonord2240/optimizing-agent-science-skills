# Brief: final pass on an already-fixed Skill (Sam, 2026-09-21)

Read `COMMON.md`, `FIX_BRIEF.md` and `AUDIT_BRIEF.md` first; where they conflict with this brief, this
brief wins for this pass. You are BOTH the fixer and the auditor for ONE Skill, in two phases with a
checkpoint between. This is the one exception to "different agents". Your dispatch names the Skill,
its worktree, branch, folder path and env.

The Skill has had one or more fix passes on your branch already; the fix log at
`F:\optimizing-agent-science-skills\fixes\<skill-id>.md` says what and why. You are finishing it.

## Phase 1: finish the fix

Work through the fix log's "left unfixed" items and any "Revisit list" entry in `fixes\README.md` naming
your Skill:

- **Fix what is fixable now.** Install what real verification needs (packages, CLIs, model weights) under
  COMMON's install rules; the point of this pass is that nothing ships untested because a tool was
  missing. **An install over 1 GB goes to Sam first**, with how the tool fits the Skill's use.
- **Walk every runnable block in the Skill**, not just what an earlier fixer touched, and confirm it
  executes as `SKILL.md` invokes it, on the audit's data or a realistic substitute.
- **What still cannot be resolved** (a paid or licensed tool, an auth-gated API, a dataset that does not
  exist, a binary with no install path here) goes on the checkpoint list, with exactly what would resolve
  it.

No restructuring beyond FIX_BRIEF's `references/` and `scripts/` rules; no new scope.

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

Commit your work on the branch as usual. Append to the fix log but do not commit it; the orchestrator
does. **Then stop and report.**

## Phase 2: the audit

Phase 2 is always a fresh agent (Sam, 2026-09-22). It gets the checkpoint, the fix log, and the
worktree, branch and env, never the Phase 1 transcript. Sam may have decided some checkpoint items; the
dispatch says which.

Follow AUDIT_BRIEF's "Re-auditing a fixed Skill" exactly: the source is the branch's tip commit; archive
the pre-fix report if one exists and is not archived yet; run its inputs as regression tests plus your
own; write `F:\OpenScience\audits\<skill-id>\{eval_report_*.json, eval_viewer_*.md, run\}`. Set
`"meta": {"auditor_independent": false, "note": "final pass: fixed and audited under one brief, see
CHECKPOINT.md"}`: this is not a normal re-audit and must not be read as one later.

## Final messages

- **Phase 1 (≤ 150 words):** commit hashes, what got fixed, the full "still blocked" list with what each
  needs.
- **Phase 2 (≤ 100 words):** final score, grade, deployable, executed k/N, veto, top P0/P1, and
  confirmation `auditor_independent: false` is set.

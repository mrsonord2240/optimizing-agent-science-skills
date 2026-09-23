# Optimizing Agent Science Skills

The records repo for refining agent science Skills. The method, and every rule agents follow, lives in
`process/` (start at `process/COMMON.md`). This file only says how the orchestrator runs the work.

| repo | role |
| --- | --- |
| `F:\OpenScience\external\mrsonord2240__bioSkills` (`bioSkills-Improved`) | staging: every fix lands here on `main`. **Being retired**, see below |
| `F:\optimizing-agent-science-skills` (this repo) | records: `process/`, `audits/`, `fixes/`, `tools/` |
| `F:\optimized-scientific-skills` | published shelf: refined Skills only, with `REMAINING.md` |
| `F:\OpenScience\audits\`, `audit-envs\`, `wt\` | live working area, not a repo; raw runs stay here |

## Consolidation (Sam, 2026-09-22)

Target: two repos and one read-only folder. The shelf becomes the only place Skill bytes are edited
(`main` = shipped, Skills imported from upstream onto a branch when work starts, fix worktrees branch from
the shelf). This repo keeps records and the one set of instructions. `F:\OpenScience\external` holds only
read-only upstream clones. **Order (option A):** finish the final pass Phase 2 on staging, promote, then
retire staging (archive `bioSkills-Improved` on GitHub, prune `wt\`). Until then the paths below stand.

## The goal and its order (Sam, 2026-09-17)

1. **Audit every remaining Skill** (`F:\optimized-scientific-skills\REMAINING.md`), one folder at a time.
2. **Fix pass** from the audit reports, then a re-audit by a third agent.
3. **Promote** every Skill that passes.

Tooling → audit → fix → re-audit; the auditor, fixer and re-auditor are different agents. **Exception
(Sam, 2026-09-21):** the final pass on an already-fixed batch (`process/FINAL_PASS_BRIEF.md`), reserved for
a consolidation pass Sam has explicitly called.

## Dispatching

- **One fresh Sonnet per unit** (tooling per folder; auditor, fixer, re-auditor per Skill). Never brief one
  agent for a list. State passes through files (`TOOLS.md`, reports, fix logs, `STATUS.md`).
- Dispatch every unblocked unit in parallel, at most 10 subagents at once.
- Every dispatch names the exact Skill, source path and commit, the env and its `TOOLS.md`, and the brief.
  A wind-down message asks agents to finish their unit or write `STATUS.md` for a fresh agent.
- A folder is tooled **before** its first auditor starts: audits after a tooling pass executed 66/67 and
  51/53 inputs; one without spent five passes discovering tools.
- Other sessions may work this corpus. Check `ListAgents` and existing claims (`F:\OpenScience\audits\<skill-id>\`,
  `wt\` worktrees) first; claims are by atomic `mkdir`. Agree a split rather than stacking agents.

## Backlog maintenance

`audits/BACKLOG.md` and `audits/INDEX.md` are generated; never hand-edit them. After **every** audit or
re-audit lands:

```bash
python tools/publish_audits.py --repo F:/optimizing-agent-science-skills --skill <skill-id>
npm run audits:index
```

Commit the record, the regenerated index and any fix log together. An audit only under
`F:\OpenScience\audits\` is not in the backlog; that is how causal-genomics went untracked on 2026-09-17.

## Fixing, landing, promoting

- One worktree and branch per fix from staging `main`: `F:\OpenScience\wt\<short>`, `fix/<short>`. Archive
  the pre-fix report to `F:\OpenScience\audits\_pre-fix-<yyyymmdd>\<skill-id>\` before the re-audit.
- A fix lands when its re-audit passes: core ≥ 85, deployable, no open P0, no veto. Merge `--no-ff` into
  staging `main`, push, delete the branch and worktree.
- **Promote every audited Skill that did not fail, whatever its score** (Sam, 2026-09-17): deployable, no
  open P0. Promotion is part of landing; do not wait to be asked. Failed Skills stay in `REMAINING.md`
  under `excluded` until a fix passes re-audit.
- `promote_skills.py` flags each promoted Skill in `PROVENANCE.json` and at the top of `REMAINING.md`:
  `fix_pass: needed` (first audit only) and `reaudit: needed` (bytes changed since its latest audit).
- To promote: advance `FORK_COMMIT` in `tools/promote_skills.py` to the staging commit, run it dry, then
  `--apply`. Update the Status table in the shelf `README.md` from the new `PROVENANCE.json`, commit and
  push the shelf.
- **The goal is the Open Science skill marketplace** (`aipoch/openscience-skill-marketplace`,
  `authoring/README.md`): one `release.config.json` per Skill pinned to a shelf commit, every version
  immutable and reviewed. `promote_skills.py` sets `marketplace_ready`. After pushing the shelf, run
  `python tools/marketplace_manifests.py --intake F:/OpenScience/marketplace-intake/openscience-skill-marketplace`;
  it writes manifests to `F:\OpenScience\marketplace-submissions\`, refuses ids already in the
  marketplace, and fails unless the marketplace's own `intake:skill` accepts every one. **Never rewrite
  shelf history:** a force-push breaks the pinned SHAs.

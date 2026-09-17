# Optimizing Agent Science Skills

The records repo for refining agent science Skills: process briefs, audit records, fix logs, tooling.
The method lives in `process/`. This file only says how the work is run.

| repo | role |
| --- | --- |
| `F:\OpenScience\external\mrsonord2240__bioSkills` (`bioSkills-Improved`) | staging: every fix lands here on `main` |
| `F:\optimizing-agent-science-skills` (this repo) | records: briefs, `audits/`, `fixes/`, `tools/` |
| `F:\optimized-scientific-skills` | published shelf: refined Skills only, with `REMAINING.md` |
| `F:\OpenScience\audits\`, `audit-envs\`, `wt\` | live working area, not a repo; raw runs stay here |

## The goal and its order (Sam, 2026-09-17)

1. **Audit every remaining Skill.** The list is `F:\optimized-scientific-skills\REMAINING.md`. Work
   one folder at a time.
2. **Fix pass after.** Fixers work from the audit reports once the audits have landed, and a re-audit
   by a third agent follows every fix.
3. **Promote** each Skill that passes re-audit (see below).

Every stage names who does it: `TOOLING_BRIEF` → `AUDIT_BRIEF` → `FIX_BRIEF` → `AUDIT_BRIEF` (re-audit).
**The auditor, the fixer and the re-auditor are always different agents.**

## Fresh subagents, as often as sensible

- **One fresh Sonnet per unit:** one tooling agent per folder, one auditor per Skill, one fixer per
  Skill, one re-auditor per Skill. Never brief one agent for a list: "a single agent" means one at a
  time, not one context.
- Pass state between agents through files on disk (`TOOLS.md`, reports, fix logs, `STATUS.md`), never
  through a long-running context.
- **Throughput is maxed.** The old two-auditors-on-the-machine cap is off. Dispatch every unit that has
  no dependency blocking it, in parallel.
- Every dispatch names the exact Skill, source path and commit, the env and its `TOOLS.md`, and the
  traps below. A wind-down message asks agents to finish their current unit, or to write `STATUS.md`
  so a fresh agent can resume.

## Toolchain in advance of audits

A folder is tooled **before** its first auditor starts. Agents audited without a tooling pass spent
five passes discovering tools mid-run; agents audited after one executed 66/67 and 51/53 inputs.

- Env per folder at `F:\OpenScience\audit-envs\<env>\` with a `TOOLS.md`. Reuse an existing env that
  already covers the folder rather than building a second one (causal-genomics uses
  `mendelian-randomization-analyst`).
- **Rscript exits 0 and prints nothing** without R's DLL dirs on `PATH`. Every R call goes through the
  env's `r.sh`.
- **Judge by output, never exit code.** A directory in `R-lib` is not an install; `library()` must load.
- **No agent waits on a background install.** Take stock of what is on disk, record the rest, finish.
- Shared envs: stage installs, hold `install.lock` (`mkdir`) only while copying new packages in, never
  change an existing version, never delete another agent's lock.

## WSL2

Linux-only tools are **not** blocked. Use the `science` distro (conda-forge + bioconda, env `bio`),
documented in `process/TOOLING_BRIEF.md` → "The WSL science seat". Drive it with
`MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '<cmd>'`. Only `F:\OpenScience` is mounted
(`/mnt/openscience`), and `interop=false` is load-bearing because we run code we did not write. **Never
widen either for convenience.** Docker Desktop is the fallback (bind-mounting `F:` hangs; use
`docker cp`).

## Backlog maintenance

`audits/BACKLOG.md` and `audits/INDEX.md` are generated. Never hand-edit them. After **every** audit or
re-audit lands:

```bash
python tools/publish_audits.py --repo F:/optimizing-agent-science-skills --skill <skill-id>
npm run audits:index
```

Then commit the record, the regenerated index and any fix log together. An audit that exists only under
`F:\OpenScience\audits\` is not in the backlog. That gap is how the whole causal-genomics folder's audits
went untracked on 2026-09-17.

## Fixing, landing, promoting

- One worktree and branch per fix, from staging `main`: `F:\OpenScience\wt\<short>`,
  `fix/<short>`. Archive the pre-fix report to `F:\OpenScience\audits\_pre-fix-<yyyymmdd>\<skill-id>\`
  before the re-audit writes a new one.
- A fix lands when its re-audit passes: core ≥ 85, deployable, no open P0, no veto. Merge `--no-ff`
  into staging `main`, push, delete the branch and worktree.
- **Promotion is explicit per Skill:**
  `python tools/promote_skills.py --add <id>,<id>` for a dry run, then `--apply`. First advance
  `FORK_COMMIT` to the staging commit you are promoting from, and update the count table in the
  published `README.md`. The dry run lists Skills that qualify but were not named. They stay in
  `REMAINING.md` until someone decides to promote them.

## Sharing the machine with other sessions

Other Claude sessions often work this corpus at the same time. Before dispatching on a folder, check
`ListAgents` for busy project sessions and existing claims: `F:\OpenScience\audits\<skill-id>\`
folders and `wt\` worktrees. **Claim by `mkdir`, which is atomic.** If a folder or worktree is someone
else's, agree a split with that session rather than stacking agents on the same Skill.

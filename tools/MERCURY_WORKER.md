# Mercury leaf-worker launcher

`run_mercury_worker.py` runs one disposable Mercury 2.5 worker through
OpenRouter without routing the parent Claude or Codex process through
OpenRouter. It calls OpenRouter's Chat Completions API directly and supplies a
small, deterministic agent loop; Claude Code is not part of the worker path.

The pilot profile is deliberately read-only. Three code-enforced tools are
available: bounded text-file reads, bounded file listing, and bounded literal
text search. All paths must resolve below the selected Git working directory.
There is no shell, agent-spawning, network, or file-editing tool.

OpenRouter's tool-calling protocol is documented at
<https://openrouter.ai/docs/guides/features/tool-calling>.

## Credential

Store the OpenRouter key in the Windows user environment as
`OPENROUTER_API_KEY`. Do not put it in this repository, a task brief, Claude's
settings, Codex's settings, or a command-line argument. The launcher checks the
process environment first and then the Windows user environment. It uses the
key only in the OpenRouter authorization header and redacts it from errors.

## Run one worker

Write a bounded UTF-8 task brief outside the repository, then run:

```powershell
python tools/run_mercury_worker.py `
  --task-file F:\OpenScience\mercury-workers\task.md `
  --workdir F:\optimizing-agent-science-skills `
  --output F:\OpenScience\mercury-workers\result.json
```

The launcher records the task hash, requested and reported models, structured
worker result, exact OpenRouter token and cost accounting, tool-call metadata,
elapsed time, limits, and whether Git status changed. It never records the API
key, hidden reasoning, or file contents returned by tools.

Success requires all of the following:

- OpenRouter reports `inception/mercury-2.5` as the model used.
- Mercury returns the required structured report.
- The worker remains inside its turn, time, output-token, and cost limits.
- Git status is identical before and after the worker.

Defaults are 12 inference turns, 300 seconds overall, 60 seconds per request,
4,096 output tokens per request, two transient-error retries, and USD 0.05 in
OpenRouter-reported cost. These are upper bounds, not targets, and can be
lowered per invocation.

## Security boundary

This is a leaf worker, not an orchestrator. It receives one task and cannot
select another task or phase. A future write-capable profile should be a
separately reviewed extension, not a relaxation of this profile. It should run
against an isolated worktree, expose explicit edit and command allowlists, and
require the parent orchestrator to review its diff.

# fixes/

One file per Skill, `<skill-id>.md`, recording every fix pass that Skill has had.

Each pass gets a dated heading and a table:

| finding | priority | change | verified (ran / help / docs) | notes |

followed by the findings left unfixed and why — usually because the fix would be new content rather
than a correction, which is out of scope for a fixer.

These logs say what was *intended and verified by the fixer*. They are not evidence that the Skill is
good: only a re-audit's own runs are. A re-auditor reads the log to know what changed, then ignores it
and scores what the code does.

The same changes also travel with the audit record as `audits/<skill-id>/<version>/fixes.md`, so
anyone reading a published record sees them without needing this directory.

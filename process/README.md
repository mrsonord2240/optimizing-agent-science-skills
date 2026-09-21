# process/

The briefs agents are dispatched with, and the thresholds a Skill has to meet. These are the method:
if a brief is wrong, the audits it produced are wrong, so change them deliberately and date the change.

| File | Who reads it | What it governs |
| --- | --- | --- |
| `TOOLING_BRIEF.md` | tooling agent | building a folder's audit environment and writing the `TOOLS.md` the auditor reads, before the first audit |
| `AUDIT_BRIEF.md` | auditor | writing inputs, running the code, scoring, what a report must contain, and how a re-audit of a fixed Skill differs |
| `FIX_BRIEF.md` | fixer | what counts as an audit-evidenced defect, what is out of scope, how every change is verified, one commit per Skill, the fix log format |
| `COMPARE_BRIEF.md` | comparer | running two look-alike Skills side by side to see what each does, with no score |
| `THRESHOLD.md` | all | gates 2 and 3: deployable with no open P0 and a score ≥ 75, and ≥ 85 for a core Skill |
| *(moved)* | nobody now | the Specialist material (`CANDIDATES.md`, `AUTHOR_BRIEF.md`, gates 1 and 4-9) lives in `authoring/` of the `openscience-specialists` repo |

## The one rule behind all of them

**The auditor, the fixer and the re-auditor are different agents.** A fixer never scores its own work,
and a re-auditor re-runs the original inputs as regression tests plus new inputs of its own, so a
score measures the Skill rather than the findings the fixer was handed.

Evidence is what ran. A command checked against documentation is recorded as not executed, and says
which documentation.

**And a run is evidence only if its output was checked.** Five tools on this machine have exited 0
while producing nothing or producing garbage, so an exit code proves nothing on its own: assert on a
count, a value against ground truth, or a file that exists and parses.

## The order agents run in

`TOOLING_BRIEF` (once per folder) → `AUDIT_BRIEF` (one auditor per Skill) → `FIX_BRIEF` (a different
agent, per failing Skill) → `AUDIT_BRIEF` again (a third agent, re-audit).

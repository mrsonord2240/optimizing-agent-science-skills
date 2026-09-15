# process/

The briefs agents are dispatched with, and the gates a candidate has to pass. These are the method:
if a brief is wrong, the audits it produced are wrong, so change them deliberately and date the change.

| File | Who reads it | What it governs |
| --- | --- | --- |
| `AUDIT_BRIEF.md` | auditor | choosing Skills, writing inputs, running the code, scoring, what a report must contain, and how a re-audit of a fixed Skill differs |
| `FIX_BRIEF.md` | fixer | what counts as an audit-evidenced defect, what is out of scope, how every change is verified, one commit per Skill, the fix log format |
| `AUTHOR_BRIEF.md` | author | turning passed audits into a Specialist |
| `CANDIDATES.md` | all | the candidate Specialists, their scope and boundaries, and which Skills each draws from |
| `THRESHOLD.md` | all | the viability gates, including the score floors: core Skills 85, supporting 75 |

## The one rule behind all of them

**The auditor, the fixer and the re-auditor are different agents.** A fixer never scores its own work,
and a re-auditor re-runs the original inputs as regression tests plus new inputs of its own, so a
score measures the Skill rather than the findings the fixer was handed.

Evidence is what ran. A command checked against documentation is recorded as not executed, and says
which documentation.

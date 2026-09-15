# audits/

Every audit, kept whether the Skill passed or failed, so any score can be traced back to the runs
behind it.

```
audits/<skill-id>/<owner>-<repo>@<sha7>/
  record.json    author, source repo, commit, licence, audit method, what this version supersedes
  report.json    the skill-auditor report: scores, vetoes, per-input results, recommendations
  viewer.md      the readable audit: the code, what ran, what it printed
  fixes.md       present on fixed versions: every change and how it was verified
  scripts/       the scripts the auditor ran, including synthetic-data generators
```

One directory per audited version, so a Skill audited before and after a fix keeps both, and
`record.json` links them by `supersedes`.

**Not kept here:** raw run outputs, generated test data and downloaded datasets. A record names the
dataset accession or the generator script that produced its inputs; `environments/` says how to
rebuild the runtime that ran them.

`INDEX.md` lists every Skill with its latest score and open findings. `BACKLOG.md` lists every open
recommendation, most severe first. Both are generated — don't hand-edit them.

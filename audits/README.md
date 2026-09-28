# audits/

Every audit, kept whether the Skill passed or failed, so any score can be traced back to the runs
behind it.

```
audits/skills/<skill-id>/<owner>-<repo>@<sha7>/
  record.json    author, source repo, commit, licence, audit method, what this version supersedes
  report.json    the skill-auditor report: scores, vetoes, per-input results, recommendations
  viewer.md      the readable audit: the code, what ran, what it printed
  fixes.md       present on fixed versions: every change and how it was verified
  scripts/       the scripts the auditor ran, including synthetic-data generators

```

One directory per audited version, so a Skill audited before and after a fix keeps both, and
`record.json` links them through `supersedes`.

**Not kept here:** raw run outputs, generated test data and downloaded datasets. A record names the
dataset accession or the generator script that produced its inputs.

`CORPUS.json` snapshots the canonical provider inventory and readiness state.
`INDEX.md` lists every Skill with its latest score and open findings;
`BACKLOG.md` lists every open recommendation, most severe first; and
`STATUS.md` summarizes known, audited, untouched, ready, and out-of-scope
Skills by category; and `STATUS.html` presents the same canonical state as a
responsive human dashboard. These files are generated; do not hand-edit them.

Records are published here by `tools/publish_audits.py`, then all views are
regenerated with `npm run audits:index`. Refresh the provider snapshot and all
views with `npm run audits:inventory` after provider inventory, readiness, or
source metadata changes.

The per-candidate Specialist audits moved to `authoring/audits/` in
[mrsonord2240/openscience-specialists](https://github.com/mrsonord2240/openscience-specialists).

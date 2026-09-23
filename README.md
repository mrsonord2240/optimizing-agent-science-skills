# Optimizing Agent Science Skills

Working repository for improving open agent Skills for science: audit what they actually do when the
code runs, fix what is broken, re-audit, and publish every result.

Skills in this repository come from other people's public repositories. They are not ours. Each one
keeps its author's licence and records the exact upstream commit it was taken from, plus every change
we made and how that change was verified.

## How a Skill moves through here

1. **Audit** — a Claude agent follows the [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor)
   method (AIPOCH, MIT): static score, real inputs, run the code, score what it produced. Reports and
   viewers land in [`audits/`].
2. **Fix** — a different agent corrects only audit-evidenced defects (broken commands, version drift,
   code that runs but computes the wrong thing) and verifies each fix by running it. Fix logs are in
   [`fixes/`].
3. **Re-audit** — a fresh agent re-scores the fixed Skill, re-running the original inputs as
   regression tests plus new ones of its own.
4. **Promote** — Skills that did not fail move to the published shelf, `optimized-scientific-skills`,
   with their audit status flagged (`fix_pass`, `reaudit`).

Fixes are made in a fork of the original repository. Where that upstream is still maintained they
go back as pull requests; `GPTomics/bioSkills` was archived on 2026-08-15, so for those Skills the
fork is the maintained line rather than a staging area.

## Layout

| Path | What |
| --- | --- |
| `audits/skills/<skill-id>/<owner>-<repo>@<sha7>/` | `report.json`, `viewer.md`, `record.json`, `fixes.md`, and the scripts the auditor ran |
| `fixes/<skill-id>.md` | What changed, why, and how it was verified, per fix pass |
| `process/` | The briefs agents follow; `COMMON.md` holds the shared rules and thresholds |
| `tools/` | `publish_audits.py` (audit records into `audits/`), `promote_skills.py` (the published shelf), `marketplace_manifests.py` (Open Science marketplace manifests) |
| `scripts/` | `audit-index.mjs`, which generates `audits/INDEX.md` and `BACKLOG.md` (`npm run audits:index`) |

## What is deliberately not here

Raw run outputs, generated test data, downloaded public datasets, Python virtual environments and
installed binaries. They are large and reproducible: each audit record names the dataset accession or
the generator script that produced its input. Fixed Skill trees live in the fork
([bioSkills-Improved](https://github.com/mrsonord2240/bioSkills-Improved)) and on the published shelf
([optimized-scientific-skills](https://github.com/mrsonord2240/optimized-scientific-skills)), not here.

## Credit and licences

- Skills belong to their authors; the shelf's `PROVENANCE.json` names each one's upstream commit, and its `LICENSE` is the upstream licence, unmodified.
- The audit method is AIPOCH's, MIT licensed.
- Audits and fixes are performed by Claude (Anthropic) agents, commissioned by Samuel Nord. They are
  not reviewed or endorsed by the Skills' authors.
- Everything in this repository that is ours — tooling, briefs, audit records — is MIT licensed. See
  [LICENSE] and [NOTICE].

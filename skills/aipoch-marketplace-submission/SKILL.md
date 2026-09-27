---
name: aipoch-marketplace-submission
description:
  Use this whenever the task is "prep skills for AIPOCH", "generate release configs for the
  marketplace", "get the pilot batch ready for submission", or similar — it produces
  authoring/submissions/<provider>/<skill>/release.config.json files and the evidence behind
  them, per AIPOCH's own pre-review requirements. It does not open a PR or contact AIPOCH.
---

# AIPOCH Marketplace submission prep

Turns already-audited Skills in `optimized-scientific-skills` into AIPOCH-compliant
Marketplace release submissions. This is packaging/metadata work, not another audit pass —
the Skills have already been through the fix → audit → re-audit pipeline
(`optimizing-agent-science-skills`) before they ever reach this step.

## Preconditions

- `optimized-scientific-skills`'s `PROVENANCE.json` marks the candidate Skills
  `marketplace_ready: true`. Never touch `marketplace_ready: false` Skills here — that's the
  audit pipeline's job, not this one.
- Two Skill ids are permanently excluded from this process until Sam resolves the id
  collision with AIPOCH's existing catalog: `bio-causal-genomics-mediation-analysis`,
  `bio-causal-genomics-pleiotropy-detection`.

## Process

1. **Read AIPOCH's authoring spec fresh, every time.** Fetch
   `https://github.com/aipoch/openscience-skill-marketplace/tree/main/authoring` (README +
   any schema/example `release.config.json` files) before writing anything. Their spec is the
   source of truth, not this file — quote what you find so the shape is verifiable, not
   invented. Their category taxonomy lives there too; `optimized-scientific-skills` has no
   `category` field anywhere, so every skill needs a category assigned by hand against their
   list.
2. **Pin the exact commit.** `git -C <repo> rev-parse HEAD` on `optimized-scientific-skills`.
   Use this full 40-char SHA everywhere a commit is required — never a short or stale one.
3. **Select the pilot batch.** 10–20 Skills from the `marketplace_ready: true` set, spanning
   distinct families (use the id prefix: `bio-alignment-*`, `bio-single-cell-*`,
   `bio-vcf-*`/`bio-variant-*`, `bio-proteomics-*`, etc.) — not one family dumped in bulk.
   Prefer Skills already graded "Production Ready" with no pending `fix_pass`/`reaudit`.
4. **Per selected Skill, write `authoring/submissions/<provider>/<skill>/release.config.json`**
   containing, at minimum:
   - `schema_version`, Marketplace `category` (from step 1's taxonomy)
   - `source.repository` (`mrsonord2240/optimized-scientific-skills`), `source.commit` (the
     pinned SHA), `source.path` (the skill's directory)
   - `license_files` pointing at the upstream MIT LICENSE evidence
   - content SHA-256, file count, and package size for the skill's files at the pinned commit
     — compute these for real, never estimate
   - `reviewed_by`, `reviewed_on` (today), review scope, unresolved limitations
   - explicit credit to the original GPTomics author/repo/commit (from `PROVENANCE.json`),
     with our changes labeled as modifications — never presented as AIPOCH-original content
   - a reproducible link/commit into `optimizing-agent-science-skills` for that Skill's audit
     trail (check what commit that repo is at right now and cite specific evidence file paths)
   - explicit runtime dependencies (Python/R packages, CLI tools like samtools, external
     DBs/APIs, containers) — read the Skill's actual scripts/examples to get these right,
     don't guess generically from the domain
5. **Cross-check every selected Skill's SKILL.md against its own bundled scripts/examples**
   before it goes in the batch — declared inputs/outputs/limitations must match what the code
   actually does. A documentation/code mismatch here is a real defect to flag, not a detail to
   wave past (e.g., a SKILL.md claiming a workflow step the example script never calls).
6. **Never present the upstream leaderboard/audit score as an AIPOCH score.** Our own audit
   evidence is our own evidence; AIPOCH generates their own score during their review.
7. **Run whatever validation tooling AIPOCH's own repo documents** (`intake:skill`,
   `validate`, `publish:dry-run` — check what actually exists in their repo, don't invent
   commands) against the generated configs, and report its output.
8. **Stop there.** Do not open a PR, push, or contact AIPOCH — the repo owner reviews the full
   diff first, every time.

## Report format

Which Skills were selected and why (family coverage), where the configs landed, what the
validation tooling said, and any SKILL.md/code mismatch found in step 5 — flagged clearly, not
buried in a pass/fail summary.

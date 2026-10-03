---
name: normalize-scientific-skill
description: Normalize one scientific agent Skill, or a relay-assigned batch, before audit by resolving safe software-version drift, removing instruction redundancy, and migrating reusable code and conditional detail into routed resource directories. Use when an optimization relay assigns the normalization phase for an exact Skill.
---

# Normalize Scientific Skill

Normalize one exact Skill without performing its behavioral audit or fix pass.

Any subagent you spawn runs on Sonnet unless the brief names another model;
never Haiku.

## Start safely

Verify the assigned Skill, origin repository/path/commit, working
repository/path/branch, lane, phase, and ownership. Inspect Git status in every
repository you may touch. Treat pre-existing modified and untracked files as
user-owned; use a run-owned branch or isolated worktree and stop for any
unisolated overlap. Keep provider-source checkouts read-only.

Work only on the Skills your brief assigns (one, or a batch the relay allows) and this phase only. Do not reset, clean, rebase, overwrite,
delete, or reconcile unrelated work. Do not commit a product repository, push,
open a pull request, release, submit, or publish.

## Inventory before moving

Read the entire Skill tree. Map:

- every instruction and repeated passage;
- inline and external runnable code;
- conditional, method-specific, and reference-heavy guidance;
- links among `SKILL.md`, `scripts/`, `references/`, and `assets/`;
- licenses, attribution, author information, and provider provenance;
- advertised runnable surfaces and dependency clues for the tooling worker.

Also compare software names, commands, APIs, formats, and version constraints
across the entire tree with the currently supported software. Treat a mismatch
caused by an ordinary software update as normalization work rather than waiting
for audit to rediscover it.

Do not infer redundancy from similar headings alone. Preserve distinct
conditions, caveats, and scientific meaning.

## Normalize structure

- Keep `SKILL.md` concise and imperative, with the always-needed workflow and
  routing to conditional resources.
- Move substantial reusable executable code to `scripts/`.
- Move conditional, method-specific, or large lookup material to
  `references/` when it has a real routing purpose.
- Keep source assets in `assets/` only when they belong in generated output.
- Remove duplicate material after ensuring one authoritative copy remains.
- Repair relative links and references made stale by the moves.
- Preserve the frontmatter name, license obligations, attribution, provenance,
  public behavior, and advertised scope unless an unambiguous structural
  correction requires otherwise.
- Resolve version discrepancies throughout `SKILL.md`, routed references,
  scripts, examples, and dependency metadata. Default to the newer supported
  software version when live documentation or tooling confirms it and the
  update causes no evident breakage, dependency conflict, format incompatibility,
  or change in scientific meaning. Update connected commands and claims
  together. Record a genuinely ambiguous or breaking migration for audit or
  user decision instead of guessing.

- Make the frontmatter Marketplace-complete: keep `name`, `description`, and
  `license`; add exactly one `category:` from `Academic Writing`,
  `Data Analysis`, `Evidence Insight`, `Other`, `Protocol Design`, chosen from
  what the Skill does; add `author:` with the original author credit from the
  provider (for GPTomics bioSkills: `author: GPTomics`).
- Write every text file as UTF-8 without BOM, with LF line endings. Remove
  `__pycache__`, `*.pyc`, dot-prefixed paths, and LICENSE copies below the
  Skill root.

Do not redesign scientific methods, change analytical defaults, add features,
install tooling, or resolve behavioral findings unrelated to safe version
normalization in this phase. Record such issues for audit.

## Verify the normalized tree

Check that all routed files exist, `SKILL.md` remains self-contained for its
core workflow, scripts retain their full content and executable entry points,
and no required guidance became undiscoverable. Run lightweight link, metadata,
and syntax checks when available; leave behavioral execution to tooling and
audit workers.

Then run, from the records repository root,
`python tools/skill_preflight.py <normalized-skill-dir>`. It must report
`PASS`. Take the candidate identity from its output; never compute or copy an
identity by hand. Carry any `warn` lines into the handoff.

Summarize migration at file or purpose level. Do not catalog every moved or
deleted passage; the diff is that record.

## Hand off

Replace the canonical handoff's current-state sections; do not append a diary
or paste evidence. Keep it under 120 lines and link durable paths. Include the
resulting candidate identity, concise structural summary, discovered
runnable-surface inventory, dependency clues, open ambiguities, evidence paths,
and all run-owned versus pre-existing changes. Set the next role to
`prepare-scientific-skill-tooling`. Do not create a product commit, push, or
continue into tooling.

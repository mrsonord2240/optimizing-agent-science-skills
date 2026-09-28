---
name: audit-scientific-skill
description: Conduct a bounded diagnostic audit of one normalized scientific agent Skill using prepared tooling, producing schema-valid findings and executable evidence without claiming final certification. Use for the relay's initial audit phase when no usable exact audit exists.
---

# Audit Scientific Skill

Audit one exact normalized candidate to identify and prioritize work. This is a
diagnostic pass; exhaustive execution may be deferred to independent re-audit.

## Load context and method

Verify the origin and exact candidate identity, working path and branch, lane
and audit-output ownership, current `TOOLS.md`, and separation from other
workers.
Inspect relevant Git status, preserve all pre-existing changes, and keep source
checkouts read-only. Work on one Skill and this phase only. Do not make a
product commit, push, open a pull request, release, submit, or publish.

Use the current `skill-auditor.zip` rubric, veto rules, classification, and
report schema from the records repository. Extract it to the disposable run
area if needed. Never silently substitute a remembered rubric.

Use the prepared `science` WSL environment first without widening its
`/mnt/openscience`-only, interop-disabled boundary. Use recorded Docker or
native Windows exceptions only when required by the actual tool.

## Inspect statically

Read the complete Skill tree and evaluate frontmatter, trigger precision,
instruction consistency, progressive disclosure, resource routing,
provenance, licenses, safety boundaries, scientific-method claims, examples,
and correspondence between documented and shipped runnable surfaces.

Treat normalization as already complete. Report missed structural problems;
do not restart a broad migration inside the audit.

## Execute a bounded diagnostic sample

Use the prepared environment without installing a new stack. At minimum,
execute a representative public canonical path for each distinct runtime and
any migrated executable whose preservation is uncertain. Prefer inputs likely
to expose scientific or integration faults. Save commands, inputs, versions,
outputs, and assertions. Parse structured output and meaningful values; inspect
scientific relationships and rendered readability where applicable. Syntax,
imports, file existence, and exit code zero are preflight only.

You may defer exhaustive matrices, expensive secondary examples, and complete
surface coverage, but mark each deferred item `static-only` or `blocked` and
state that it cannot support final readiness. Do not score documentation or
source inspection as execution.

If missing tooling prevents meaningful diagnosis, stop that surface and route
the lane to `prepare-scientific-skill-tooling`; do not install dependencies
during scoring.

## Use the minor-repair budget narrowly

An audit-local repair is allowed only when all are true:

- the intended correction is unambiguous and changes no scientific method,
  analytical default, claim, interface, security boundary, or dependency;
- it is one localized defect affecting no more than two files and 20 changed
  lines, excluding purely mechanical formatting;
- it requires no architectural, product, licensing, or access judgment;
- every affected case and a focused regression can be rerun in this pass.

Examples include an unmistakable typo, missing import, stale documented flag
with one authoritative replacement, or incorrect local relative path. If any
condition is doubtful, file a finding for the fixer. Pin the audit to the
post-repair bytes and retain the pre-repair observation and rerun evidence.

## Produce and publish the record

Write schema-valid `report.json`, `viewer.md`, saved run scripts and inputs,
source identity, execution classifications, findings with severity and stable
IDs, minor-repair evidence, and restricted-access after-action items. Keep a
single ordered finding ledger for the fixer.

Publish through the records repository tooling and regenerate the audit index,
backlog, and status outputs at `audits/STATUS.md` and `audits/STATUS.html`. The
generator derives their counts from `audits/CORPUS.json` and published audit
records; never edit the counts by hand. A diagnostic score does not make the
Skill `candidate-ready` or `ready`.

## Hand off

Replace the canonical handoff's current state, keep it under 120 lines, and
link rather than paste evidence. Include the report path and exact identity,
ordered open finding IDs, deferred and blocked surfaces, environment
fingerprint, repair details, worktree state, and next role. Normally route
findings to `fix-scientific-skill`; a clean pass routes to
`reaudit-scientific-skill`. Retire without creating a product commit or
continuing into fixes.

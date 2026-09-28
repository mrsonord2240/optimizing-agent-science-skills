---
name: prepare-scientific-skill-tooling
description: Prepare or refresh the reproducible tools, environments, public inputs, and per-surface coverage map for one normalized scientific Skill. Use for a full pre-audit tooling pass or a focused tooling-delta pass after fixes.
---

# Prepare Scientific Skill Tooling

Make one normalized Skill executable for later workers. Do not audit its
quality, repair its instructions, or change product bytes.

## Load context

Verify the candidate identity, surface inventory, working path and branch,
lane ownership, existing `TOOLS.md`, and requested mode: `full` or `delta`.
Inspect relevant Git status, preserve all pre-existing changes, keep source
checkouts read-only, and work on this Skill and phase only. Do not change Skill
bytes or commit, push, release, submit, or publish a product repository.

## Inventory the complete surface

Map every advertised or shipped runnable surface to its requirements:

- Python, R, shell, notebooks, compiled languages, and command-line tools;
- packages, system libraries, wrappers, runtimes, and version constraints;
- models, databases, reference files, and real public test inputs;
- remote services, authentication, licenses, registrations, hardware, and
  graphical or native-application requirements.

For a delta pass, compare the fix handoff and diff with the prior inventory.
Verify unaffected surfaces retain a live environment; rebuild only what the
change invalidated. If impact is uncertain, expand the delta until every
affected surface is known.

## Build reproducibly

Use the `science` WSL distribution by default. Keep `/mnt/openscience` as its
only Windows mount and keep Windows interop disabled; never widen that boundary
for convenience. Use the existing `science` user and micromamba environments.
Stage Windows inputs under `F:\OpenScience`. Use Docker or a justified native
Windows exception when the real tool requires it. Coordinate shared mutations
with a lock, prefer isolated environments for conflicts, and snapshot relevant
versions. Kill only run-owned processes.

Prepare bounded public caches and at least one small real public dataset when
the audit would otherwise fetch them repeatedly. Keep heavy artifacts under
the disposable run root, never in the Skill package.

For each accessible primary tool, save and run a meaningful smoke test with a
bounded real public input when available. Parse data back, check scientifically
meaningful values, and render or open visual output at intended size as
appropriate. Successful installation, syntax, imports, `--help`, file
existence, or exit code zero alone is insufficient. Do not install or download
gated assets by bypassing their controls; record the exact blocker, affected
workflow, user action, and rerun steps.

## Write `TOOLS.md`

Place `TOOLS.md` in the lane's durable records area, not the product Skill. It
must contain:

- full or delta mode and candidate tree identity;
- one row per runnable surface with runtime/tool, environment, version,
  invocation, smoke evidence, input/cache path, and status;
- environment fingerprint and enough activation detail for a new worker;
- public data/model provenance and cache location;
- exact restricted, unavailable, or resource-infeasible blockers plus user
  action and rerun instructions;
- surfaces verified unchanged during a delta pass;
- items explicitly out of scope.

## Hand off

Replace the canonical handoff's current state, keep it under 120 lines, and
link evidence rather than pasting output. Include `TOOLS.md`, its fingerprint,
evidence paths, blockers, and next role. Route to `audit-scientific-skill` when
no usable exact audit exists; otherwise, route to `fix-scientific-skill` or the
orchestrator's stated next phase. Do not edit the Skill, assign audit scores,
create a product commit, or continue into the next phase.

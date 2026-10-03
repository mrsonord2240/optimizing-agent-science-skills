# Relay operations

## Capacity and independence

Run at most five concurrent workers plus one orchestrator. A lane is one worker
slot; under the batching table below it may carry several Skills. Unless the
invocation states a lower limit, one invocation claims at most ten Skills. An
explicit invocation-level lane, worker, or Skill cap is a hard boundary.

A worker carries one phase only. When a phase finishes, accept its handoff,
retire the worker, and dispatch a fresh agent for the next phase. Independence
is per Skill, including inside a batch: the worker that fixed a Skill never
audits or certifies it, and the worker that ran a Skill's initial audit never
runs its final re-audit.

Keep a lane on its Skills until each is done or durably parked for user action.
A parked handoff retains its claim, candidate identity, blocker, and exact
resume condition; the lane may then take other Skills within the Skill cap.

## Models

Use the cheapest model that completes the work, and set the model explicitly on
every dispatch; never let a worker inherit the orchestrator's model.

| Work | Claude | Codex |
|---|---|---|
| Identity, hygiene, frontmatter, ID-collision checks | none: `tools/skill_preflight.py` | none |
| Every worker, including mechanical text edits: normalize, tooling, initial audit, fix, delta and final re-audit | Sonnet | Terra |
| Escalation after the same phase's handoff was rejected twice for quality | Opus | the next tier up |

Never use Haiku or Luna for anything that involves a decision. Haiku normalize
workers failed on 2026-09-30 (wrong identity hashes, CRLF, nested LICENSE, a
product commit), so every worker starts at Sonnet. Record any escalation and
its reason in the lane table.

## Batching

A batched worker receives several Skills of the same phase. Each Skill keeps
its own claim, candidate identity, run directory, canonical handoff, finding
ledger, and published record. Finish and publish one Skill's record before
starting another Skill's heavy execution, so a crash loses at most one Skill's
unpublished work.

A Skill is **heavy** when any required surface needs a GPU, a single smoke or
end-to-end run is expected to exceed 10 minutes, or its inputs exceed 5 GB.
Otherwise it is **light**.

| Phase | Batch key | Skills per worker |
|---|---|---|
| Normalize | same upstream category | up to 5 |
| Tooling, full or delta | same ecosystem: shared environments or public inputs | up to 5 |
| Initial audit | light Skills | up to 3; heavy: 1 |
| Fix changing runnable bytes | none | 1 |
| Fix limited to text and frontmatter (no runnable byte changes) | any | up to 10 |
| Delta re-audit | any | up to 3 |
| Final re-audit | light Skills | up to 3; heavy: 1 |

Stage shared public inputs once per ecosystem under
`F:\OpenScience\audit-envs\<ecosystem>\public-data\` with a README recording
source URL, bytes, and sha256, and reuse them across Skills.

## Scheduling

The orchestrator maintains one compact lane table:

| Lane | Skill | Phase | Candidate identity | Worker | Handoff | Blocker |
|---|---|---|---|---|---|---|

Update rows in place. Do not turn the table into an event log. Before dispatch,
verify that no other live worker owns the same Skill, path, environment
mutation, or audit output. Serialize shared-environment changes; independent
read-only executions may proceed concurrently when resource limits permit.

Every phase brief must include the absolute path to the selected worker
`SKILL.md`, the explicit model, every assigned Skill ID with its source and
candidate identity and canonical handoff path, the allowed phase, and classified
pre-existing changes. Tell the worker to read the
entire contract before any repository exploration or mutation. Treat a missing
or unreadable contract as a blocked dispatch. The worker must not search the
specialists repository, another project, or the web for a replacement role and
must not reconstruct the contract from the phase name.

Choose the earliest incomplete phase from durable evidence. Do not replay a
phase merely for ceremonial sequence. Do not skip normalization. Reuse tooling
or audit work only under the exact identity and freshness rules in the
orchestrator Skill.

Budget audit effort by scientific and operational risk. Spend new execution on
changed findings, shared abstractions, common end-to-end workflows, materially
different modes or output families, and silent high-consequence failures. Reuse
identity-matched evidence for untouched surfaces. Do not spend a lane on an
exhaustive invalid-input catalog, redundant parameter permutations, or a full
expensive replay after a localized repair.

## Transition review

Before accepting a phase:

1. read the canonical handoff and linked evidence;
2. verify source and candidate identity against the live worktree;
3. inspect unexplained Git changes;
4. confirm the phase's completion criteria;
5. confirm the worker published its audit record and regenerated the views,
   rerun `tools/skill_preflight.py` on the candidate, and commit the records
   repository changes for that Skill;
6. assign a fresh worker the next role and only the context it needs.

Reject incomplete handoffs for correction while the worker still owns the
phase. Do not compensate by pasting its chat transcript into the next brief.

## Control-plane commits

The records repository may use small atomic commits for audit evidence,
generated status, handoffs, and resumable state. Product repositories may not:
their only run commit is the completed-Skill batch at close. Never sweep user
changes into either class of commit.

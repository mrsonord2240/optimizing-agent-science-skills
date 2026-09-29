# Relay operations

## Capacity and independence

Run up to five worker lanes plus one orchestrator. Use the cheapest model capable of completing the task. Luna for Codex Haiku for Claude. If the work is not satisfactory -> Sonnet | Terra. Five is the default when
eligible work exists; an explicit invocation-level lane, worker, or Skill cap
is a lower hard boundary. A lane carries one Skill at a time. A worker carries
one phase only. When a phase finishes, accept its handoff, retire it, and
dispatch a fresh agent for the next phase. The fixer never certifies its own
work, and an initial auditor never becomes the final auditor.

Keep a lane on its Skill until the Skill is done or durably parked for user
action. Once parked, the lane may take another Skill only when doing so stays
within the invocation's Skill cap; the parked handoff must retain its claim,
candidate identity, blocker, and exact resume condition.

## Scheduling

The orchestrator maintains one compact lane table:

| Lane | Skill | Phase | Candidate identity | Worker | Handoff | Blocker |
|---|---|---|---|---|---|---|

Update rows in place. Do not turn the table into an event log. Before dispatch,
verify that no other live worker owns the same Skill, path, environment
mutation, or audit output. Serialize shared-environment changes; independent
read-only executions may proceed concurrently when resource limits permit.

Every phase brief must include the absolute path to the selected worker
`SKILL.md`, the Skill ID, source and candidate identity, canonical handoff path,
allowed phase, and classified pre-existing changes. Tell the worker to read the
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
5. publish audit artifacts and refresh generated records when applicable;
6. assign a fresh worker the next role and only the context it needs.

Reject incomplete handoffs for correction while the worker still owns the
phase. Do not compensate by pasting its chat transcript into the next brief.

## Control-plane commits

The records repository may use small atomic commits for audit evidence,
generated status, handoffs, and resumable state. Product repositories may not:
their only run commit is the completed-Skill batch at close. Never sweep user
changes into either class of commit.

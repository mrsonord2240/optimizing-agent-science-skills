# Relay operations

## Capacity and independence

Run up to five worker lanes plus one orchestrator. Five is the default when
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

Choose the earliest incomplete phase from durable evidence. Do not replay a
phase merely for ceremonial sequence. Do not skip normalization. Reuse tooling
or audit work only under the exact identity and freshness rules in the
orchestrator Skill.

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

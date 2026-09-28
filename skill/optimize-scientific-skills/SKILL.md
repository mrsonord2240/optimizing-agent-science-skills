---
name: optimize-scientific-skills
description: Coordinate a five-lane relay that normalizes scientific agent Skills, prepares their tooling, audits and repairs them, independently certifies them, and runs local Marketplace intake. Use when Sam asks to process or resume the science-Skill backlog, run audit-fix-reaudit work, or close a refinement batch.
---

# Optimize Scientific Skills

Coordinate the relay; delegate each phase to its focused worker Skill. A run is
complete only when exact committed Skill bytes pass independent executable
re-audit and the Open Science Skill Marketplace's local intake validator.

## Load the contracts

Read these contracts before selecting work:

- [repository contract](references/repository-contract.md)
- [readiness and records](references/readiness-and-records.md)
- [phase handoff](references/phase-handoff.md)
- [relay operations](references/relay-operations.md)

Read the [Marketplace intake gate](references/marketplace-intake-gate.md) only when
a candidate-ready batch is about to close.

The worker Skills are independently distributable. Their bodies include their
own phase safety and completion rules; do not replace those rules with a large
orchestrator prompt.

## Route phases

Use the following worker Skills by exact name:

| Phase | Worker Skill | Transition evidence |
|---|---|---|
| Normalize | `normalize-scientific-skill` | normalized tree identity and surface inventory |
| Tool | `prepare-scientific-skill-tooling` | `TOOLS.md` and environment fingerprint |
| Initial audit | `audit-scientific-skill` | diagnostic report and finding ledger |
| Fix | `fix-scientific-skill` | finding dispositions and tooling impact |
| Final re-audit | `reaudit-scientific-skill` | candidate-ready decision for exact bytes |

Dispatch a fresh agent for every phase. A worker owns one Skill and one phase,
then retires after writing the canonical handoff. The orchestrator normally
does not perform worker-phase tasks.

## Run the relay

### 1. Establish the batch

Inspect live agents and claims, relevant Git status, `audits/INDEX.md`,
`audits/BACKLOG.md`, generated status, provider metadata, and active handoffs.
Select only in-scope or canonically next-eligible Skills. Record exact source
identity and the earliest incomplete phase. Claim no more than five Skills.

### 2. Normalize every Skill

Run `normalize-scientific-skill` before tooling or behavioral audit. A prior
audit is reusable only when it applies to the exact normalized candidate bytes,
uses the current report schema, and retains its evidence. A structural
change normally makes an older audit diagnostic history rather than the active
audit.

### 3. Prepare tooling

Run a full `prepare-scientific-skill-tooling` pass after normalization, unless
an existing `TOOLS.md` covers the exact runnable-surface inventory and its
recorded environment fingerprint is verified live. Tooling must be ready
before an initial audit or, when a usable initial audit is reused, before a fix.

### 4. Audit, fix, and certify

Run `audit-scientific-skill` when no usable initial audit exists. Dispatch
`fix-scientific-skill` for open findings, known P0s, readiness blockers, wrong
outputs, and safely bounded lower-priority defects. A truly clean diagnostic
audit may proceed directly to final re-audit.

After every fix, inspect its tooling impact:

- `none`: reuse the verified environment;
- `changed`: run a tooling-delta pass for affected surfaces;
- `uncertain`: treat as changed until a tooling worker resolves it.

Then dispatch `reaudit-scientific-skill`. A failure returns to a fresh fixer,
then any required tooling delta, then a fresh re-auditor. A user-action blocker
may be parked without occupying a worker slot once its exact state is durable.

After every audit pass, publish its records and regenerate the canonical audit
index, backlog, Markdown status, and HTML dashboard. Keep each freed lane filled
while eligible work remains.

### 5. Stage candidate-ready Skills

Copy or promote each exact candidate-ready tree to
`F:\optimized-scientific-skills\skills\<skill-id>` with only the provider and
provenance metadata needed to identify it. Verify byte identity. Exclude every
in-progress or blocked Skill and all unrelated changes.

### 6. Close the run

Treat one invocation as one product batch:

1. Create one unpublished optimized-shelf commit containing all and only this
   run's candidate-ready Skills and required shared metadata.
2. Refresh the corpus snapshot with `npm run audits:inventory`; this updates
   `audits/CORPUS.json` and all four generated audit views.
3. Run the Marketplace's local intake gate against that full commit.
4. Resolve failures according to the gate. A Skill-byte change returns through
   fix and fresh re-audit; a manifest-only change does not.
5. Exclude unresolved Skills and amend or recreate the unpublished commit.
   Refresh the corpus snapshot and rerun intake whenever the product commit
   changes. Stop only when intake has accepted the exact final commit and final
   product history contains one run-closing optimized commit.
6. For accepted bio-derived Skills, prepare at most one corresponding
   bioSkills-Improved batch commit from the exact canonical bytes.
7. Commit resumable state for unfinished lanes in the records repository when
   useful; never put unfinished Skills in a product batch.

Do not push, open pull requests, build Marketplace bundles, add reviewer
identity, submit, register, release, publish, or mutate other remote state
without separate authorization.

## Report the run

Report completed, blocked, and in-progress Skills; final phase and readiness;
audit, provider, and handoff paths; product commit hashes or why absent;
Marketplace intake receipts; user-action items; and confirmation that no
unauthorized remote or publication action occurred.

---
name: optimize-scientific-skills
description: Coordinate an up-to-five-lane relay that normalizes scientific agent Skills, prepares their tooling, audits and repairs them, independently certifies them, and runs local Marketplace intake. Use when Sam asks to process or resume the science-Skill backlog, run audit-fix-reaudit work, or close a refinement batch.
---

# Optimize Scientific Skills

Coordinate the relay; delegate each phase to its focused worker Skill. A run is
complete only when exact committed Skill bytes pass independent executable
re-audit and the Open Science Skill Marketplace's local intake validator.

## Load contracts progressively

Read only the contract needed for the next decision:

- Before claiming or mutating work, read the
  [repository contract](references/repository-contract.md) and
  [relay operations](references/relay-operations.md).
- Before the first dispatch or phase transition, read the
  [phase handoff contract](references/phase-handoff.md).
- Before interpreting audit readiness, reusing evidence, or publishing records,
  read [readiness and records](references/readiness-and-records.md).
- Read the [Marketplace intake gate](references/marketplace-intake-gate.md) only
  when a candidate-ready batch is about to close.

Do not preload later-phase contracts or worker Skill bodies merely because a run
has started.

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

Worker-contract delivery is part of dispatch. Resolve the selected worker
Skill's actual `SKILL.md` as a sibling of this orchestrator Skill and include
that absolute path in the worker brief. The worker's first action must be to
read the complete file successfully. Merely naming the Skill is insufficient:
a fresh agent may start from a repository that does not expose the orchestrator's
Skill registry. If the contract cannot be read, the worker must report that
blocker and stop without searching other repositories for a substitute role or
improvising the phase.

Dispatch a fresh agent for every phase. A worker owns one Skill and one phase,
then retires after writing the canonical handoff. The orchestrator must not
invoke a worker Skill in its own context or perform worker-phase tasks. It may
only select and claim work, dispatch the exact worker Skill, validate the
handoff and evidence, update lane state, and close accepted batches.

## Run the relay

### 1. Establish the batch

Treat the invocation as the primary selector and resolve targets progressively:

- **Explicit Skill target:** use only the named Skill or Skills. Do not inspect
  the backlog, index, aggregate status, or the full corpus to select work. Read
  an active handoff when present, query only the matching corpus entry and
  per-Skill records, then verify its provider metadata and live Git state.
- **Resume request:** start from active handoffs and live claims. Read only the
  records linked by those handoffs. Do not select replacement Skills unless the
  invocation permits refilling lanes.
- **No target supplied:** parse `audits/CORPUS.json` locally and emit only the
  fields needed to identify a bounded eligible shortlist, normally `id`,
  `upstream_path`, `category`, and `state`. Stop once there are enough verified
  candidates to fill the permitted lanes plus a small reserve for conflicts.
  Do not print or load the complete corpus into model context.

#### Automatic-selection gate

An automatically selected Skill must have substantive unfinished refinement
work. Before dispatching any worker, verify the corpus state, latest applicable
audit, optimized-shelf presence, active handoff, and open finding severity for
that Skill. Record the eligibility reason in the lane table.

Exclude a Skill from default selection when any of these is true:

- its corpus state is `candidate-ready`, `ready`, `done`, or `out-of-scope`;
- the latest audit applies to the current bytes and marks them deployable or
  `Production Ready` with no unresolved required recommendation;
- the exact audited bytes are already present on the optimized shelf;
- only Marketplace, publication, release, or other separately authorized work
  remains; or
- another lane or live worker already owns it.

Do not choose an almost-finished or ready Skill merely to exercise the relay,
and never restart normalization on exact bytes that already passed final audit.
If corpus, audit, and shelf state disagree, park selection of that Skill and
record a targeted records-reconciliation item; do not treat the disagreement as
permission to redo the product work.

For automatic selection, rank eligible work in this order:

1. an in-scope open P0 or hard readiness blocker;
2. `untouched` or `remaining` work with no usable audit for the current source;
3. `audited` work with a required fix or re-audit still incomplete;
4. lower-priority backlog refinement only when the invocation requests backlog
   or polish work, or after the user explicitly permits that tier.

For a fresh process pilot, choose from the first eligible Skill that genuinely
requires the full relay, normally an `untouched` or `remaining` Skill without a
current final audit. If no candidate passes the gate, report that there is no
eligible default work; do not weaken the gate. An explicit user target may
override automatic-selection exclusion, but run only its earliest incomplete or
specifically requested phase rather than replaying completed phases.

Use **query, don't dump** for generated records. Begin with an exact Skill ID,
path, state, or heading query; read a bounded matching object or section; expand
only when the unanswered selection or transition question requires it. Never
read all of `audits/CORPUS.json`, `audits/INDEX.md`, `audits/BACKLOG.md`,
`audits/STATUS.md`, or `audits/STATUS.html` as a startup inventory.

- Use `CORPUS.json` for canonical inventory, category, source path, and state,
  but filter it programmatically without emitting unrelated entries.
- Use per-Skill record JSON and the active handoff for exact audit identity,
  findings, phase, ownership, and transition evidence.
- Read `BACKLOG.md` only when the user asked for backlog work, the selected
  Skill's open recommendation must be resolved, or targeted canonical records
  cannot settle priority. Search exact Skill IDs or headings first and read only
  that bounded section. Expand to adjacent ranked entries only as needed to fill
  an allowed lane; do not read the full backlog by default.
- Read `INDEX.md` only for a needed human-facing link or a targeted
  record-consistency check. Read `STATUS.md` or `STATUS.html` only for an
  aggregate status request or dashboard verification. Loading one generated
  view is not a reason to load its siblings.

A full generated-file read is permitted only when the user explicitly requests
a whole-report review or a generator/schema defect cannot be diagnosed with
targeted queries. State that reason before expanding scope.

Inspect live agents and claims and relevant Git status for the resolved targets.
Select only in-scope or canonically next-eligible Skills. Record exact source
identity and the earliest incomplete phase. Claim no more than five Skills.
Default to five eligible lanes, but honor any lower invocation-level lane,
worker, or Skill limit as a hard run boundary. Do not refill beyond a stated
batch-size limit.

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

Run one comprehensive but bounded `audit-scientific-skill` pass when no usable
initial audit exists. Its minimum dynamic scope is the common workflow end to
end, a second materially distinct workflow when applicable, and one inspected
example of each materially different output family within reason. Dispatch
`fix-scientific-skill` for open findings, known P0s, readiness blockers, wrong
outputs, and safely bounded lower-priority defects. A truly clean diagnostic
audit may proceed directly to final re-audit.

After every fix, inspect its tooling impact:

- `none`: reuse the verified environment;
- `changed`: run a tooling-delta pass for affected surfaces;
- `uncertain`: treat as changed until a tooling worker resolves it.

Then dispatch a fresh independent `reaudit-scientific-skill` worker. The final
pass retests corrected findings and affected regressions, confirms a canonical
core smoke, and reuses identity-matched immutable evidence for untouched
surfaces. A failure returns to a fresh fixer for one focused repair loop, then
any required tooling delta, then a fresh re-auditor. Restart broad audit only
when the failure affects shared architecture, invalidates the environment or
evidence identity, or materially changes the advertised workflow set. A
user-action blocker may be parked without occupying a worker slot once its
exact state is durable.

Publish the initial baseline and accepted final audit. Keep rejected
intermediate runs as durable local evidence and publish them only when needed
to preserve a blocker, explain a candidate-identity transition, or satisfy the
records schema. Regenerate canonical views after each published audit. Keep
each freed lane filled while eligible work remains.

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

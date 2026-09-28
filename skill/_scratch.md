# Skill scratchpad

Working notes for a possible new Skill. This file is intentionally exploratory;
it is not yet a Skill specification or an implementation commitment.

## Working intent

- Skill idea: orchestrate the preparation, audit, repair, validation, and
  progress tracking of scientific agent Skills.
- Desired outcome: every selected Skill is structurally normalized, safely
  worked through the appropriate audit/fix cycle, and left with reproducible
  executable evidence and a clear readiness state.
- Intended users or agents: an orchestrating agent coordinating focused
  tooling, audit, fix, re-audit, and landing work across science Skills.

## Current draft status (2026-09-28)

- Sam approved the modular split. The draft is now a six-Skill suite: one
  orchestrator plus distinct normalization, tooling, initial-audit, fix, and
  independent re-audit Skills.
- The orchestrator retains the full shared contracts. Each worker Skill is
  independently distributable and carries a compact copy of only the safety,
  evidence, completion, and handoff rules needed for its own phase, so it does
  not inherit permissions from another phase.
- One canonical handoff per lane is now part of the design. It is a replaced
  current-state document capped at 120 lines, not an append-only transcript.
  Evidence is linked by path and finding ID. Ambiguous candidate identity,
  missing evidence, unexplained changes, or an unclassified tooling impact
  makes a handoff unacceptable.
- The former live `process/` briefs were migrated and removed. Historical
  records may retain their old references as provenance.

## Raw notes

- The first operation for every Skill should be a redundancy check plus the
  migration of substantial code and conditional reference material into their
  appropriate directories.
- The Open Science Skill Marketplace may be the eventual destination for these
  Skills. Fixing every known P0 is therefore within the default scope, rather
  than an exceptional expansion. Marketplace submission and packaging are
  nevertheless a separate process and are not part of this Skill.
- After structural normalization, conduct an initial audit only when the Skill
  does not already have a usable audit.
- Follow the initial audit with a fix pass and then another independent audit.
- It is acceptable to defer exhaustive code execution during the first audit
  in order to reduce its load. By the second, post-fix audit, all code should
  be executed.
- The process notes previously described as “1. Select and claim the Skill” and
  “2. Protect existing work” are essential. Preserve and codify both in the
  finished Skill.
- Agents performing tooling and audit work must be made fully aware of the WSL
  environment. WSL should be the default environment for setting up tooling
  and audit environments, not merely a fallback mentioned after native setup
  fails.
- Deduplication and file migration do not need a passage-by-passage inventory
  in the fix log. Their detailed history is already recoverable from the Git
  diff.
- Compiling Python and parsing R are only preliminary checks. The files must
  actually run, and their outputs must be useful, readable, and consistent
  with the workflow's expected result.
- When a dependency or service is private, authenticated, login-gated, paid,
  licensed, registration-bound, or otherwise unavailable, surface it in an
  after-action report so the user can decide whether to remedy it for the next
  pass.
- Docker is an approved and useful execution route when it can provide a
  reproducible environment without weakening the WSL or host safety boundary.
- Auditors should have bounded discretion to fix minor issues they discover
  during an audit, then rerun the affected checks in the same pass. The repair
  allowance needs firm limits so it cannot become an open-ended fix pass.
- After every audit pass, refresh a durable category-level status table in the
  records repository showing how many Skills have been audited, remain
  untouched, and are ready.
- Run the corpus as a relay with five concurrent worker agents plus one
  orchestrator. A worker owns one Skill and one phase; when that phase ends,
  retire it and give the next phase to a fresh agent. Keep a Skill in its relay
  lane until it is finished, then dispatch a fresh agent on a new Skill.
- When a Skill is finished, land its exact audited tree in
  `optimized-scientific-skills`; completion does not stop at an audit branch or
  raw evidence folder.
- Treat one invocation of this Skill as one commit batch. When the run ends,
  make at most one closing commit in each affected product repository:
  `optimized-scientific-skills` for every Skill completed during the run and
  `bioSkills-Improved` for the completed bioSkills-derived subset. A run that
  finishes only one Skill therefore produces a valid single-Skill batch.
  Do not create product-repository commits for normalization, an audit pass, a
  fix pass, or another intermediate relay phase.
- `optimizing-agent-science-skills` is the exception: it is the working and
  evidence repository rather than a final Skill-product repository, so its
  commits may be substantially more atomic and phase-specific.
- The local `bioSkills-Improved` copy was the immediate copy-management problem;
  the public repository remains the maintained, bioSkills-shaped fork that
  people can reference for improved copies of the upstream Skills.
- Use a controlled one-way feed to carry completed bioSkills changes from the
  canonical optimized repository into that maintained fork. A separate
  downstream process consumes the canonical repository for Open Science Skill
  Marketplace inclusion.
- Before a Skill is considered done, run the Open Science Skill Marketplace's
  own local `intake:skill` validator against the exact committed optimized
  subtree and require it to pass. This validation gate is in scope; review,
  bundle building, registration, submission, and publication remain separate.
- Unparsed phrase to clarify: “two of fixed trees and all trees.” Preserve it
  here rather than guessing at the intended requirement.

## Emerging decisions

### Selection and claim are part of the Skill's core contract

- Work only on the Skill or explicit batch placed in scope.
- Resolve the canonical Skill ID, source repository, path, branch, and exact
  starting commit.
- Use the latest applicable audit and generated backlog rather than an older
  report or informal note.
- Establish ownership of the live audit/work area so two agents do not work the
  same unit concurrently.
- Do not silently pull adjacent backlog Skills into the batch.

### Existing work must be protected before mutation

- Inspect all relevant repository and worktree status before changing files.
- Treat pre-existing modified and untracked files as user-owned.
- Work on a topic branch or linked worktree rather than directly on the
  provider's main branch.
- Keep the upstream source checkout read-only, including generated caches and
  interpreter artifacts.
- Do not reset, clean, rebase, delete, overwrite, or otherwise reconcile
  unrelated work.
- Escalate when overlapping changes cannot be isolated safely.

### Structural normalization precedes auditing

- Begin every selected Skill with a redundancy review.
- Move substantial runnable code to `scripts/` and conditional or
  method-specific guidance to `references/` when those resources have a real
  routing or reuse purpose.
- Preserve discoverability from `SKILL.md`; migration must not make necessary
  instructions harder for an agent to find.
- Treat this normalization as a standard first phase, not as optional cleanup
  discovered during the later fix pass.

### Record structural cleanup concisely

- Do not enumerate every removed duplicate, moved paragraph, or relocated code
  block in the fix log.
- Give the normalization work a concise summary when it is useful—for example,
  which files were reorganized and whether material moved to `scripts/` or
  `references/`—but let the commit diff remain the detailed record.
- Reserve detailed fix-log entries for actual audit findings, behavior changes,
  unresolved problems, and the evidence used to verify them.
- Continue to verify migrated code and references. Reducing narrative logging
  does not reduce the requirement to preserve behavior, routing, and
  discoverability.
- This intentionally supersedes the current process rule that asks for every
  deleted or moved passage and its destination to be itemized.

### WSL is the default tooling and audit environment

- Default new tooling and audit environments to the `science` WSL distro.
- Treat native Windows execution as an evidence-driven exception for a tool or
  integration that genuinely requires it, rather than as the initial setup
  path.
- Make the WSL option and its invocation rules explicit in every tooling and
  auditor brief so an agent does not incorrectly classify a Linux-capable tool
  as unavailable.
- Preserve the established WSL safety boundary: only `F:\OpenScience` is
  mounted at `/mnt/openscience`, Windows interop remains disabled, and agents
  must not broaden filesystem visibility merely to make setup convenient.
- Use the existing `science` user and micromamba-based environments. Prefer an
  isolated environment when satisfying a dependency would change versions in
  a shared environment.
- Record the exact WSL distro, environment, package versions, launch command,
  and smoke test in the tooling inventory so later auditors can reproduce the
  setup.
- Keep Docker as an approved reproducible fallback or isolation method when
  WSL cannot run the tool directly or a container is the cleaner supported
  route. Record the image, version or digest, mounts, command, and output
  checks in the audit trail.

### Restricted dependencies become after-action items

- Do not attempt to bypass access controls or silently acquire credentials for
  a private, authenticated, login-gated, paid, licensed, or registration-bound
  dependency or service.
- Continue with public alternatives, WSL, or Docker when they faithfully test
  the advertised workflow. Do not substitute a materially different method
  merely to make the audit appear complete.
- Add an after-action item that states:
  - the exact dependency, service, dataset, or capability;
  - the access restriction or concrete error encountered;
  - which advertised workflow or audit assertion it prevented;
  - what evidence was and was not obtained;
  - the specific user action that could unblock a later pass;
  - what should be rerun after access is remedied.
- Apply this reporting rule consistently regardless of whether the barrier is
  authentication, privacy, payment, licensing, registration, unavailable
  infrastructure, or another external prerequisite.
- A blocked route remains explicitly unexecuted; the after-action report makes
  it actionable but does not convert it into passing evidence.

### Audit depth is intentionally asymmetric

- If a usable audit already exists for the relevant Skill bytes, do not repeat
  an initial audit merely to satisfy the sequence.
- If no usable audit exists, perform an initial audit after normalization.
- The initial audit may defer exhaustive execution to reduce cost and load.
- After the fix pass, the independent re-audit must execute all shipped and
  advertised code paths that are expected to run in the supported environment.
- The second audit is the executable evidence gate for technical readiness.

### Execution and output inspection are mandatory evidence

- Treat `py_compile`, R `parse()`, shell syntax checks, imports, and tool help
  as preflight checks only. They establish that code can begin to run; they do
  not establish that the workflow works.
- Actually execute changed and shipped Python and R programs with realistic
  inputs in the supported environment. Apply the same principle to other
  shipped executable languages and command-line workflows.
- Inspect what the execution produced. An output must be:
  - structurally valid and parseable in its intended format;
  - semantically consistent with the expected analysis or transformation;
  - useful to the researcher or downstream agent;
  - readable at the size, medium, or interface in which it will be consumed.
- Match the check to the artifact. Validate schemas, dimensions, columns,
  counts, ranges, and planted truth for data outputs; open figures at their
  intended resolution; inspect tables and reports for legibility; and verify
  that interactive or application outputs expose the expected information.
- A nonempty file or exit code 0 is insufficient when the content is blank,
  malformed, misleading, clipped, illegible, or scientifically unexpected.
- Record the input, command, environment and versions, output location, and
  the meaningful assertions or visual checks that support the conclusion.
- If an expected workflow cannot be executed, report the concrete blocker. It
  cannot count as executed evidence or support final technical readiness
  until the agreed exception or execution path is resolved.
- The initial audit may still defer exhaustive execution. The fix pass must run
  the code it changes, and the independent post-fix audit must rerun all
  expected code and judge its outputs independently.

### Auditors have a bounded minor-repair allowance

- An auditor may proactively correct a defect found during the audit when the
  change is local, low-risk, mechanically obvious, and small enough to validate
  completely inside the same audit pass.
- Candidate minor repairs include an unmistakable typo, missing import,
  incorrect local path, stale flag with one documented replacement, or a
  similarly narrow presentation defect whose intended behavior is already
  unambiguous.
- The allowance does not cover scientific-method changes, altered analytical
  defaults, new capabilities, dependency strategy, security or permission
  changes, broad refactors, multi-workflow rewrites, or anything whose correct
  behavior requires product judgment.
- After a minor repair, pin the audit to the resulting bytes, record the exact
  change and why it qualified, and rerun every affected input plus any focused
  regression needed to prove the correction.
- If the issue exceeds the repair allowance, report it normally and route it
  to the dedicated fix pass. Do not stretch the definition of “minor” merely
  to avoid another pass.
- Preserve an audit trail of the pre-repair observation, the diff or commit,
  the post-repair executions, and the auditor's final result.

### Every audit refreshes the progress dashboard

- After each initial audit, re-audit, or audit pass containing a bounded minor
  repair, regenerate a durable status file in
  `F:\optimizing-agent-science-skills`.
- The table should group the known corpus by Skill category and show, at
  minimum:
  - total known Skills;
  - audited Skills;
  - untouched Skills;
  - ready Skills.
- Derive the table from canonical audit records and provider metadata rather
  than maintaining counts manually.
- Publish the refreshed table with the audit record so the repository retains
  a continuous, reviewable account of progress.
- Keep this dashboard focused on Skill refinement status. Do not turn it into
  marketplace submission tracking.

### Five-worker relay with one orchestrator

- Run one orchestrator plus five concurrent worker slots, for six active agents
  at full capacity.
- Each worker slot carries one Skill through a relay of stage-specific agents.
  Five slots therefore allow up to five Skills to be in flight concurrently.
- A worker agent owns exactly one Skill and one phase. It hands off evidence
  and state when the phase completes, then retires rather than continuing into
  the next phase for that Skill.
- Dispatch a fresh agent for the next phase of the same Skill:
  - initial audit agent;
  - dedicated fix-pass agent;
  - independent executable re-audit agent;
  - another fixer and another auditor when the result requires an additional
    loop.
- The bounded minor-repair allowance remains inside an auditor's current
  phase. Once that audit pass is complete, that auditor still retires.
- Keep the relay lane assigned to its current Skill until the Skill meets the
  completion gate or reaches a documented user-action blocker. Do not replace
  an unfinished Skill with a more convenient one merely to improve throughput.
- When a Skill is complete, retire its final worker and dispatch a fresh agent
  into that freed slot to claim the next eligible Skill.
- The orchestrator does not count as one of the five workers and ordinarily
  does not perform the stage work. It:
  - selects and claims the five in-flight Skills;
  - tracks each lane's exact phase, branch, commit, audit source, and blockers;
  - prevents duplicate ownership and shared-environment conflicts;
  - gives each replacement agent the minimum complete handoff;
  - verifies stage outputs and transition conditions;
  - publishes audit records and refreshes generated progress views;
  - lands exact audited bytes when the completion gate permits;
  - keeps worker slots filled while eligible work remains.
- A replacement agent must inspect the predecessor's durable phase artifacts,
  live worktree state, and canonical handoff rather than relying on a
  conversational summary alone. Phase-level commits may exist in the records
  repository, but not as incremental product history in either Skill-product
  repository.
- If a usable audit already exists, start the lane at the earliest incomplete
  phase instead of rerunning completed work only to preserve a ceremonial
  sequence.

### Approved tooling gate and worker-Skill suite

Sam approved this modular design on 2026-09-28. It replaces the monolithic
first draft and the former live `process/` briefs.

#### Put the full tooling pass after normalization and before behavioral audit

- The preferred lane order is:

  ```text
  claim and protect existing work
      -> redundancy and migration normalization
      -> determine whether an existing audit is usable
      -> full tooling pass or verified tooling reuse
      -> bounded initial audit, when needed
      -> fix
      -> tooling-delta gate
      -> independent executable re-audit
      -> repeat fix/tooling-delta/re-audit until complete or blocked
  ```

- Normalization comes first because it establishes the actual runnable surface:
  duplicate examples may disappear, hidden runnable code may move to
  `scripts/`, and claims may be narrowed before the tooling agent spends time
  installing or caching dependencies.
- The tooling pass finishes before the initial audit whenever an initial audit
  is needed. This gives the auditor a prepared environment and prevents the
  audit from becoming a series of environment-discovery passes.
- When an existing audit is usable and the initial audit is skipped, tooling
  still finishes before the fix pass. The fixer should know which documented
  tools actually run, which versions are available, and which surfaces are
  gated before choosing a correction.
- A fix that changes dependencies, versions, wrappers, runtime paths, models,
  reference data, or runnable surfaces triggers a focused tooling-delta pass
  before re-audit. If none of those changed, reuse the verified environment and
  its fingerprint rather than rerunning the entire tooling phase.
- An auditor or fixer that discovers missing tooling routes the lane back to
  the tooling role. Auditors should not silently install a new stack while
  scoring it, and fixers should not spend a long pass rediscovering environment
  setup. A genuinely minor audit-local repair must not introduce a dependency.

#### Make tooling completion checkable

The tooling phase is complete only when:

- every runnable surface in the normalized Skill is mapped to a runtime, CLI,
  package, model, service, reference dataset, or explicit blocker;
- the selected environment and relevant package/tool versions are recorded;
- each accessible primary tool has a saved smoke test whose output was checked,
  not merely a successful install or zero exit status;
- required public caches and a bounded real public test dataset are prepared
  when the Skill would otherwise fetch them during audit;
- paid, authenticated, private, license-bound, resource-infeasible, and other
  gated items are listed with the exact user action needed for a later pass;
- `TOOLS.md` or its successor contains a per-Skill coverage map and enough
  invocation detail for the auditor and fixer to use the environment without
  rediscovery;
- the tooling agent changed no Skill product bytes and wrote a durable handoff.

Reuse environments across related Skills, but verify coverage per Skill. A
shared environment being present is not evidence that it covers the next
Skill. Install changes remain serialized through the environment lock.

#### Replace monolithic briefs with phase-specific worker Skills

Use the orchestration Skill as a router and state-machine owner. Give each
fresh phase agent a dedicated, independently invocable role Skill:

1. `normalize-scientific-skill`
   - remove redundancy and migrate reusable code/reference material;
   - preserve meaning, routing, behavior, and provenance;
   - emit a concise structural handoff and no product commit.
2. `prepare-scientific-skill-tooling`
   - support full and delta modes;
   - build or reuse the WSL-first environment, inventory and smoke-test every
     dependency, cache public inputs, and publish the tooling handoff;
   - never audit, score, or edit Skill bytes.
3. `audit-scientific-skill`
   - perform only the bounded diagnostic initial audit;
   - distinguish executed from static evidence and identify actionable
     findings;
   - never imply that deferred execution certifies final readiness.
4. `fix-scientific-skill`
   - work from an explicit finding ledger and the verified tool inventory;
   - repair every P0 plus other readiness-blocking or safely bounded findings;
   - verify changed behavior, flag tooling deltas, checkpoint a long pass, and
     hand off without scoring or creating a product commit.
5. `reaudit-scientific-skill`
   - perform only the independent, exhaustive certification pass;
   - rerun regressions plus fresh inputs, execute every accessible expected
     surface, inspect outputs, and apply the final readiness gate;
   - contain no initial-audit permission to defer exhaustive execution.

Keep re-audit separate from initial audit even though they share a rubric and
record schema. The initial audit's deliberate permission to defer execution is
dangerous in a final auditor's context; a real skill boundary prevents that
allowance from leaking into certification.

The orchestrator retains only cross-lane concerns:

- selection, claims, scope, and protection of existing work;
- the five-lane relay and fresh-agent transitions;
- phase routing and acceptance of each worker's handoff;
- publication of records and generated status views;
- completion-gate enforcement;
- exact-byte landing, one-way maintained-fork projection, and run-closing
  product batches;
- the local Marketplace intake gate against the provisional optimized batch;
- blocker aggregation, after-action reporting, and remote/marketplace
  authorization boundaries.

Move phase mechanics out of the orchestrator:

- normalization steps and migration verification go to the normalization
  Skill;
- WSL, Docker, installation, caching, locks, and `TOOLS.md` mechanics go to the
  tooling Skill;
- initial-audit evidence and bounded-repair rules go to the initial-audit
  Skill;
- finding-ledger mechanics, change scope, verification, and resumable
  checkpoints go to the fix Skill;
- exhaustive execution, output inspection, regressions, scoring, and final
  certification go to the re-audit Skill.

Each worker Skill should state its exact inputs, allowed write locations,
ordered work, completion criterion, handoff schema, and forbidden actions. The
orchestrator dispatch names the role Skill explicitly and supplies only the
current Skill, phase, paths, environment, evidence, and predecessor handoff.

#### Keep one source of truth while optimizing worker context

- Do not leave both a long process brief and a new worker Skill authoritative.
  The suitable finished product is a complete migration: inventory and move
  every still-live rule, update active callers, validate the replacement suite,
  then delete the files under `process/`. Do not retain permanent compatibility
  shims that recreate a second instruction source.
- Do not rewrite historical audit or fix records merely because they mention
  the old brief filenames; those references describe the method used at the
  time.
- Split the current `COMMON.md` by need instead of requiring every role to load
  all of it. Likely shared sources are:
  - a short repository and machine-safety contract for every worker;
  - environment and installation policy for tooling and agents that execute;
  - evidence and output-inspection standards for audit, fix verification, and
    re-audit;
  - scoring thresholds and record schema for auditors and the orchestrator.
- Prefer shared references for stable cross-role facts and role-local steps for
  execution. Avoid copying the same WSL, threshold, or repository rule into
  five Skill bodies.
- Treat the role Skills as an installed suite: independently invocable and
  dispatchable, but distributed together with their shared references. A
  plugin bundle may eventually be the cleanest packaging unit, but it is not
  necessary to settle the phase design.

#### Existing brief material that should change during migration

- `AUDIT_BRIEF.md` currently combines initial audit and re-audit. Split them so
  the final auditor never sees permission to defer exhaustive execution.
- `FIX_BRIEF.md` currently asks for one product commit per Skill, a separate
  migration commit, and detailed passage-by-passage migration logs. Remove
  those requirements in favor of the approved run-closing product batch and
  concise migration summary.
- Redundancy and progressive-disclosure work currently repeated in the fix
  brief move to the dedicated normalization phase. A fixer checks that its
  edits do not reintroduce redundancy but does not rerun the entire structural
  phase.
- Tool installation currently leaks into audit and fix roles. Route substantive
  environment changes through the tooling Skill and use the tooling-delta gate
  after dependency-affecting fixes.
- `FINAL_PASS_BRIEF.md`'s combined same-agent fix-and-audit behavior conflicts
  with the fresh-agent relay and should become historical rather than an active
  dispatch path. Migrate only its still-valid exhaustive-execution requirements
  into the re-audit Skill before deleting the file.
- If comparison is still a supported operation, migrate `COMPARE_BRIEF.md` into
  a separate comparison Skill. Otherwise preserve its historical uses in the
  existing records and delete the live brief with the rest of `process/`.

Before deleting `process/`:

1. Build a rule-to-destination inventory for all six current files:
   `COMMON.md`, `TOOLING_BRIEF.md`, `AUDIT_BRIEF.md`, `FIX_BRIEF.md`,
   `FINAL_PASS_BRIEF.md`, and `COMPARE_BRIEF.md`.
2. Mark each rule as migrated, deliberately superseded, or historical-only;
   nothing is silently dropped.
3. Update active callers such as `CLAUDE.md`, `README.md`, orchestrator dispatch
   text, and current handoffs. Do not rewrite immutable historical evidence
   merely to change an old filename.
4. Validate every role Skill and forward-test realistic dispatches, with
   special attention to tooling completeness, fix-pass resumability, and the
   final auditor's refusal to defer execution.
5. Search for remaining active references. When only historical records refer
   to the old briefs, delete the six process files and remove the directory if
   empty.

### Marketplace work is a separate process

- The prospect of eventual Open Science Skill Marketplace use justifies a high
  technical-readiness standard for the Skills processed here.
- Fix every known P0 by default.
- Generate only the temporary manifest and local intake output needed to prove
  the required pre-completion `intake:skill` gate. Keep the raw validation
  output in the disposable run area and retain a compact receipt in the records
  repository.
- Do not add reviewer identity, build marketplace packages or bundles, copy
  artifacts into a submission queue, create submission records, register a
  release, or create publication state in this workflow.
- Beyond the required local `intake:skill` validation, do not submit, approve,
  enroll, publish, or otherwise mutate the Open Science Skill Marketplace.
- Hand an intake-accepted, technically ready, and fully evidenced Skill to the
  separate marketplace process; that process owns review, packaging,
  submission, enrollment, and external publication actions.

### Finished Skills land on the optimized shelf

- A Skill is not operationally finished merely because its final audit passes.
  Merge or promote the exact audited tree into
  `F:\optimized-scientific-skills\skills\<skill-id>` and reconcile its provider
  provenance and refinement metadata.
- `optimized-scientific-skills` is the canonical cross-source shelf: it can
  contain refined Skills from bioSkills and other scientific Skill corpora.
- Preserve exact-byte identity between the final audit record and the landed
  provider subtree. Any Skill-byte change made while landing requires renewed
  execution evidence.
- Keep audit reports, fix records, generated coverage views, and process
  instructions in `optimizing-agent-science-skills`; do not turn the records
  repository into another copy of the finished Skill tree.
- Local landing and metadata reconciliation do not by themselves authorize a
  push, pull request, release, or remote deletion.

### Each run closes with completed-Skill batch commits

- Apply this rule to both `optimized-scientific-skills` and
  `bioSkills-Improved`.
- The invocation of this Skill defines the batch boundary. Do not commit the
  product repositories during individual relay phases.
- At the end of the run, create one aggregate commit in
  `optimized-scientific-skills` containing every Skill that reached completion
  during that run. If the run completed any bioSkills-derived Skills, create
  one corresponding aggregate commit in `bioSkills-Improved` containing that
  completed subset.
- A closing batch may contain one completed Skill. If a run finishes no Skills
  for a product repository, do not create an empty commit there.
- Do not create or preserve separate product-repository commits for redundancy
  cleanup, migration, initial audit, fix pass, re-audit, or another
  intermediate relay phase. The commit boundary represents a completed-Skill
  batch from the run, not the internal sequence used to produce it.
- Before forming the batch, every included Skill must independently satisfy the
  completion gate. Exclude in-progress and blocked Skill trees even when they
  share a relay cycle with completed Skills.
- Each batch contains the exact audited Skill subtrees plus only the shared
  provider or provenance metadata necessary to identify those results. Any
  subsequent change to a Skill's bytes requires renewed evidence before it can
  enter a later completed-Skill batch.
- Keep phase evidence, audit reports, fix records, dashboard updates, relay
  state, and handoffs in `optimizing-agent-science-skills`. Because that
  repository is a working control-and-evidence repository and does not contain
  the final Skill product, it may use smaller, phase-specific atomic commits.
  Before the run ends, make sure every unfinished lane has enough run-owned
  working state committed there to resume safely without appearing in either
  product batch.
- Never sweep unrelated pre-existing changes into a run-closing batch. The
  closing commits contain only the completed, run-owned Skills and their
  necessary provider or provenance metadata.
- If local tooling creates temporary checkpoint commits on a non-product or
  unpublished integration branch, do not merge or publish them as the product
  history. Form the final product commit from the exact completed and audited
  trees.

### Preserve a path to a maintained bioSkills fork

- Distinguish the local staging-copy problem from the value of a maintained
  public fork. Archiving or removing a redundant local checkout does not imply
  that the public maintained-fork effort should end.
- Maintain at most one authoritative bioSkills-shaped fork for users who want
  the improved upstream corpus in its familiar repository layout and history.
- Do not create another full local working copy merely to keep that fork
  current. Prefer a controlled export, temporary worktree, generated patch,
  cherry-pick stream, or other one-way synchronization mechanism from canonical
  audited commits.
- The synchronization must retain provenance linking:
  - upstream GPTomics commit and path;
  - final audited provider commit and flat Skill ID;
  - destination fork commit and upstream-shaped path;
  - the audit record that justified the change.
- Treat the maintained fork as a downstream compatibility/public-reference
  surface, not as a second canonical editing location.
- The later approved topology resolves this option in favor of direct
  consumption from `optimized-scientific-skills`. This Skill exposes a clean,
  exact-commit and intake-pass handoff but does not generate review,
  package-build, submission, registration, or publication state.

### Current repository facts verified 2026-09-27

- `mrsonord2240/bioSkills-Improved` currently exists on GitHub, is public,
  unarchived, and is an actual fork of the archived `GPTomics/bioSkills`.
- The repository description already presents it as the maintained fork with
  audited and corrected bioinformatics Skills.
- `mrsonord2240/bioSkills` redirects to the same GitHub repository, so older
  references to the pre-rename fork are not a second live fork.
- The redundant local staging checkout is absent from `F:\OpenScience`; the
  remote maintained fork itself was not archived.
- `mrsonord2240/optimized-scientific-skills` is public, unarchived, and is a
  standalone cross-source repository rather than a GitHub fork.
- The current local optimized repository has only its own GitHub remote; the
  maintained bioSkills fork is not configured as a second local editing remote.

### Approved repository topology

Decision confirmed by Sam on 2026-09-27: use an intentional one-way publication
graph instead of trying to reunify the two existing histories:

```text
GPTomics/bioSkills (archived, read-only upstream)
                    |
                    v
optimized-scientific-skills (canonical editing and shipped Skill bytes)
          |                         |
          |                         `--> separate marketplace process
          v
bioSkills-Improved (generated bio-only compatibility fork)

optimizing-agent-science-skills = audit records, fix evidence, process, status
```

- Keep `optimized-scientific-skills` as the one canonical local editing source
  and the source that downstream consumers pin by exact commit.
- Keep `bioSkills-Improved` as the one public, upstream-shaped reference for
  people who want the maintained bioSkills corpus in its familiar directory
  layout and GitHub fork network.
- Do not restore a permanent second local clone. When synchronization is
  authorized, create a temporary checkout or worktree, export only completed
  bio-derived Skill subtrees, commit the batch, and remove the disposable local
  checkout after verification.
- Make the synchronization deterministic from provider metadata:
  - use the flat provider Skill ID to find the completed subtree;
  - use `PROVENANCE.json`'s `upstream_path` to restore the bioSkills directory
    location;
  - require the provider subtree to match the final audited commit;
  - copy the exact subtree without re-editing it during export;
  - record provider, audit-record, upstream, and fork commits in the sync
    commit or generated manifest.
- Synchronize only from the optimized shelf to the maintained fork. Do not use
  `bioSkills-Improved` as an alternate working source and do not automatically
  flow fork-only edits back into the canonical provider.
- Treat outside contributions to the maintained fork as new candidate input:
  import them intentionally onto a provider branch, then run the same
  normalization, audit, fix, and re-audit workflow before canonical adoption.
- Let the separate marketplace process consume
  `optimized-scientific-skills` directly. A staging feed should exist only if
  the marketplace's actual interface requires one; do not create it merely to
  recreate the earlier split.
- Synchronize only the completed bioSkills-derived subset in the run-closing
  batch; never synchronize an intermediate relay transition. A batch may
  contain a single completed Skill. The local Skill workflow should prepare a
  deterministic sync manifest; remote synchronization remains a separately
  authorized publication action.

## Decisions and open questions

### Resolved in the 2026-09-28 modular draft

- A usable prior audit must identify the exact normalized candidate bytes and
  use the current schema; otherwise run the initial audit.
- Normalization is its own relay phase with a fresh worker and handoff.
- The initial audit executes at least one representative public canonical path
  per distinct runtime; exhaustive execution remains the final-audit gate.
- Audit-local repair is capped at one localized defect, two files, and 20
  changed lines excluding mechanical formatting, with no dependency,
  scientific, interface, claim, security, licensing, or access judgment.
- The generated category views are `audits/STATUS.md` and the human-facing
  `audits/STATUS.html` dashboard. They derive known, audited, untouched,
  optimized-shelf-ready, and out-of-scope counts from the committed corpus
  snapshot and published audit records. The generator and corpus refresh
  command are implemented; intake acceptance remains the separate `done` gate.
- A durably recorded user-action blocker may be parked so its lane can accept
  another Skill.
- Native Windows is an evidence-driven exception after WSL-first evaluation;
  Docker remains the reproducible alternative.
- The normalization handoff is the structural verification checkpoint; it is
  not a product commit.
- Comparison is not an active route in this suite. Historical comparison
  records remain, but `COMPARE_BRIEF.md` was not migrated into a worker Skill.
- At batch close, the orchestrator prepares at most one local
  bioSkills-Improved commit for the accepted bio-derived subset. Any push or
  other remote update remains separately authorized.
- The separate Marketplace process consumes `optimized-scientific-skills`
  directly unless the Marketplace's actual interface later requires a staging
  feed.
- P0 is the minimum guaranteed fix scope. The fixer also handles P1/P2 items
  that block readiness, produce wrong or unusable output, invalidate an
  advertised workflow, or are safely bounded within the current Skill.

### Remaining questions

- When an auditor repairs bytes, should the record retain the label
  “independent audit,” use a distinct “audit with minor repairs” label, or
  require a second reviewer only for the repaired portion?
- Should blocked-access after-action items live in each audit viewer, a
  structured report field, a separate file, or more than one of those surfaces?
- What did “two of fixed trees and all trees” mean in the relay description?
- Should completed-Skill batch synchronization to the maintained fork use a
  direct push or a generated branch/PR feed from
  `optimized-scientific-skills`?

## Candidate requests and trigger conditions

Examples of requests that should cause the finished Skill to be used, along
with nearby requests that should not trigger it.

## Scope boundaries and non-goals

What the Skill should handle, what it should leave to the base agent, and what
would require separate authorization or a different Skill.

## Proposed workflow and decision points

1. The orchestrator selects and claims up to five exact Skills, one per worker
   lane, and records each lane's earliest incomplete phase.
2. For each lane, dispatch a fresh phase agent to inspect repository state and
   protect all existing work.
3. Establish or verify the WSL-first tooling and audit environment.
4. Normalize structure when that phase has not already been completed:
   - remove redundancy;
   - migrate reusable runnable code to `scripts/`;
   - migrate conditional method detail to `references/`;
   - preserve `SKILL.md` routing and essential context.
5. Determine whether a usable audit already exists for the resulting Skill
   bytes.
6. If not, conduct a bounded initial audit; exhaustive execution may be
   deferred.
7. During any audit, allow only bounded minor repairs; rerun their affected
   evidence immediately and route larger findings to a dedicated fixer.
8. Publish the audit trail, any blocked-access after-action items, and the
   regenerated category-level progress table.
9. Retire the initial auditor and dispatch a fresh dedicated fixer, including
   every known P0 by default.
10. Retire the fixer and dispatch a fresh independent post-fix auditor.
11. Execute all expected code during that re-audit and inspect its outputs for
   structural validity, scientific expectation, usefulness, and readability.
12. Resolve any failure that prevents the Skill from meeting the agreed
    technical-readiness gate, then re-audit affected bytes.
13. Publish the final audit trail and refresh the category-level progress table
    again.
14. At run close, form one provisional completed-Skill batch commit in
    `optimized-scientific-skills` from every exact audited tree completed by
    the run and its necessary provider metadata. Do not create an empty product
    commit, include an in-progress Skill, or retain phase-by-phase product
    commits.
15. Generate temporary validation manifests pinned to that exact commit and
    run the Marketplace's own local `intake:skill` command for every candidate.
    Require a zero exit status and the complete parsed acceptance map.
16. Resolve manifest-only failures without changing audited bytes. Return any
    Skill-byte failure through fix and fresh executable re-audit; exclude an
    unresolved candidate and recreate the unpublished provisional batch rather
    than weakening the gate.
17. Form one corresponding batch commit in `bioSkills-Improved` for the
    intake-accepted bioSkills-derived subset.
18. Record the exact-commit and intake-pass handoff needed by any separately
    authorized maintained-fork synchronization or marketplace publication
    process; perform neither remote update as part of this workflow.
19. Retire the final auditor. Hand the verified Skill to the separate
    downstream processes without performing marketplace review, bundle build,
    submission, registration, publication, or an unauthorized fork push.
20. Dispatch a fresh agent into the freed worker lane to claim the next
    eligible Skill while the other lanes continue at their current stages.

## Invariants, risks, and approval boundaries

- Selection, ownership, and repository-safety checks are mandatory phases, not
  implicit coordinator behavior.
- At full capacity there are five stage workers plus one orchestrator. A worker
  never continues from audit to fix or from fix to re-audit on the same Skill.
- A stage transition uses durable evidence, the shared worktree state, and a
  canonical handoff; it is not authorized solely by the departing agent's
  summary. Phase-level commits belong in the records repository when useful,
  not in either product repository.
- A pre-existing file or change is never assumed disposable.
- WSL is the default audit/tooling environment, and its restricted filesystem
  and interop boundary must not be weakened for convenience.
- Access restrictions are surfaced for user action; they are never bypassed or
  hidden behind substituted evidence.
- Audit-local repairs remain small, obvious, fully recorded, and completely
  rerun. Anything requiring judgment or broad change goes to a dedicated fixer.
- Structural migration must preserve meaning, discoverability, and runnable
  behavior.
- The fix log is not a prose duplicate of the Git diff. Structural cleanup may
  be summarized at file or phase level instead of catalogued passage by
  passage.
- Syntax, compilation, parsing, imports, and zero exit status are never the
  final evidence for executable code. Completion requires execution plus
  inspection of meaningful output.
- A dedicated fixer does not independently certify its own final result. The
  bounded audit-local repair exception must be labeled in the audit trail and
  must include a complete rerun of affected evidence.
- All expected code must have executed successfully with checked outputs before
  the final audit can support technical readiness.
- Completion includes landing the exact audited tree in
  `optimized-scientific-skills`; an audit-only branch is not the finished
  destination.
- The optimized shelf remains canonical. Any maintained bioSkills fork is a
  downstream compatibility surface, not an alternate editing source.
- Temporary manifests and local `intake:skill` validation are required by this
  Skill. Marketplace review metadata, bundle building, submission, approval,
  registration, enrollment, and publication are categorically outside it.

## Possible resources

- `SKILL.md`: shared purpose, routing, constraints, and core workflow.
- `references/`: conditional detail only if distinct modes need it.
- `scripts/`: deterministic or repeatedly reused operations only.
- `assets/`: source material that belongs in generated output only.

Do not create supporting files merely to fill out the structure.

One concrete script may be justified once the repository decision is final:
`scripts/sync_bioskills_fork.py` could validate exact audited bytes, map flat
Skill IDs through `PROVENANCE.json`, and populate a temporary upstream-shaped
checkout without making a remote push itself.

## Behavioral examples and tests

- A Python script compiles but writes an empty CSV: fail, even if it exits 0.
- An R script parses and renders a plot whose labels overlap at the documented
  output size: fail the readability check.
- A workflow produces a valid table with the wrong cohort, denominator, units,
  or expected planted relationship: fail the semantic check.
- A figure or report must be opened or rendered at its intended consumption
  size; file existence alone is not a visual assertion.
- A data artifact should be parsed back and checked for its expected schema and
  meaningful values.
- A command that cannot run may be documented as blocked or checked against
  authoritative help, but it must not be counted as executed evidence.

## Candidate Skill outline

1. Purpose and technical-readiness outcome
2. Five-worker relay and orchestrator responsibilities
3. Scope selection and ownership claim
4. Repository and worktree protection
5. WSL-first tooling and audit environment
6. Restricted-access and Docker decision path
7. Pre-audit structural normalization
8. Existing-audit validity decision
9. Bounded initial audit
10. Auditor minor-repair budget
11. Stage retirement and fresh-agent handoff
12. Blocker after-action report
13. Category-level progress dashboard
14. Fix-pass scope and priorities
15. Evidence and concise recordkeeping
16. Independent executable re-audit
17. Failure loop and stopping conditions
18. Exact-byte landing in `optimized-scientific-skills`
19. Local Open Science Marketplace intake gate
20. Maintained bioSkills-fork synchronization handoff
21. Handoff to the separate marketplace process

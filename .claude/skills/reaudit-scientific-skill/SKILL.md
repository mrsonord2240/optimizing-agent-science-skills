---
name: reaudit-scientific-skill
description: Independently re-audit one fixed scientific agent Skill with risk-based executable coverage and decide candidate readiness for exact bytes. Use only for the relay's final certification phase with a fresh auditor.
---

# Re-audit Scientific Skill

Certify or reject one exact fixed candidate independently. Do not rely on the
fixer's conclusions as evidence.

## Establish independence and method

Verify that you did not perform the candidate's fix or initial audit. Check
origin and exact candidate identity, working path/branch, lane and audit-output
ownership, prior reports, finding dispositions, current `TOOLS.md`, and live
Git status. Preserve pre-existing changes and keep source checkouts read-only.
Work on one Skill and this phase only. Do not create a product commit, push,
release, submit, or publish.

Use the current rubric, veto rules, classification, and schema from
`skill-auditor.zip`. Treat earlier results as hypotheses to reproduce, not as
inherited passes.

Use the prepared `science` WSL environment first without widening its
`/mnt/openscience`-only, interop-disabled boundary. Use the recorded Docker or
native Windows route only where the actual tool requires it.

## Reinspect the complete tree

Repeat the full static evaluation against the exact candidate. Confirm every
prior finding's disposition, search for regressions and newly introduced
conflicts, and reconcile documentation, resources, provenance, licensing,
scientific claims, and shipped runnable surfaces.

## Execute a focused independent certification

Inventory expected runnable files, command paths, material examples, and
advertised public workflows. Independently rerun every corrected finding and
the regressions most likely to be affected, then run at least one canonical
end-to-end smoke of an untouched core workflow. Run a second end-to-end path
when it represents a materially different supported mode and is applicable.
When a program has materially different output families, ensure the combined
current evidence contains one inspected representative of each within reason.

Do not rerun every prior passing input merely because it exists. Earlier saved
execution may remain part of the certification record when the auditor verifies
that the relevant Skill bytes, dependencies/runtime fingerprint, interface,
input provenance, and upstream assumptions are unchanged. Re-execute whenever
that identity is uncertain, the fix affected a shared abstraction, or earlier
evidence did not inspect meaningful output.

Inspect every result under the evidence standard. Include schemas, meaningful
values, scientific relationships, failure guards, and rendered readability as
applicable. Parsing, compilation, imports, `--help`, file existence, and exit
status never substitute for the execution and output assertions.

Do not mechanically enumerate unacceptable user inputs or duplicate upstream
validation documentation. Test an invalid or adversarial value only when silent
acceptance could plausibly corrupt scientific results, report false success,
cross a security or destructive boundary, or corrupt a public output contract.

Do not install missing tooling. Route an invalidated environment back to a
tooling-delta pass. For a paid, private, authenticated, licensed,
registration-bound, unavailable, or resource-infeasible surface, record the
exact after-action item and do not count it as executed.

## Keep repairs exceptional

Use the same quantitative minor-repair budget as the initial-audit Skill only
for an unambiguous local defect with no dependency or scientific impact. Retain
the pre-repair observation, pin the report to resulting bytes, and rerun every
affected case plus focused independent regression. Anything larger fails the
pass and returns to a fresh fixer.

## Decide candidate readiness

Produce the complete schema-valid audit record and apply the canonical
readiness gate. Unless the current rubric is stricter, require final score at
least 85, static score at least 80, execution average at least 85, Layer 1 at
least 32, Layer 2 at least 48, assertion pass rate at least 90 percent, no veto
or open P0, and representative inspected execution for every materially
distinct required workflow or output family, using verified reusable evidence
where allowed above. This result makes the exact working bytes `candidate-ready`;
the orchestrator must still commit them to make them `ready` and pass intake to
make them `done`.

Publish the record and regenerate the audit index, backlog, and status outputs
at `audits/STATUS.md` and `audits/STATUS.html`. The generator derives their
counts from `audits/CORPUS.json` and published audits; never edit the counts by
hand. If it fails, resolve or report the concrete blocker before transition.

For modular raw evidence, keep origin provenance and exact candidate identity
in `source-identity.json`, not as extra fields in the strict report schema. An
uncommitted candidate needs a deterministic 64-character content SHA-256 plus
its file manifest; a 40-character Git tree id is valid only when it identifies
the exact audited subtree. Publish the explicit run root and only the named
saved scripts/inputs, then check the generated views:

```powershell
python tools/publish_audits.py --repo <records-root> --skill <skill-id> `
  --run-dir <raw-run-root> --artifact <script-or-input> [...]
npm run audits:index
npm run audits:check
```

This local records write does not authorize any push, submission, release, or
other remote mutation.

## Hand off

Replace the canonical handoff's current state, keep it under 120 lines, and
link evidence instead of pasting output. Include the certified or rejected
candidate identity, report and evidence paths, readiness metrics, every failed
or blocked surface, remaining finding IDs, worktree state, and next role. Route
failures to
`fix-scientific-skill`; route a pass to the orchestrator as `candidate-ready`.
Retire without creating product commits, running Marketplace intake, or
continuing into publication work.

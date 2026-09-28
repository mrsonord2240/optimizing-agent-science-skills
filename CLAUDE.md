# Optimizing Agent Science Skills

Use the modular process suite under `skill/`. Start with
`skill/optimize-scientific-skills/SKILL.md`; it routes fresh phase workers to
the five focused worker Skills and shared contracts. The removed `process/`
briefs are historical and are not active instructions.

## Repository contract

| Repository or path | Role |
|---|---|
| `F:\optimizing-agent-science-skills` | Control state, evidence, generated audit views, handoffs, and process Skills |
| `F:\optimized-scientific-skills` | Canonical editing source and shipped Skill bytes |
| `F:\OpenScience` | Disposable worktrees, WSL-visible inputs, environments, caches, and raw output |
| `mrsonord2240/bioSkills-Improved` | Downstream compatibility fork for accepted bio-derived Skills |
| Provider source checkouts | Read-only provenance comparison |

Inspect Git status before mutation and preserve all unrelated work. No phase
worker commits a product repository. Pushes, pull requests, releases,
Marketplace submission/publication, and other remote mutations need separate
authorization.

## Relay

Run at most five Skill lanes plus the orchestrator. A fresh worker owns one
Skill and one phase, writes the canonical compact handoff, and retires. Use this
order:

```text
normalize -> full tooling -> initial audit when needed -> fix
          -> tooling delta when changed or uncertain -> independent re-audit
          -> repeat fix/delta/re-audit until candidate-ready or blocked
```

Use the `science` WSL distro first and preserve its `/mnt/openscience`-only,
interop-disabled boundary. Docker and justified native-Windows execution are
allowed under
`skill/optimize-scientific-skills/references/environment-policy.md`.

## Records

`audits/BACKLOG.md` and `audits/INDEX.md` are generated. After every initial or
final audit:

```powershell
python tools/publish_audits.py --repo <provider-root> --skill <skill-id>
npm run audits:index
```

The index command regenerates `audits/INDEX.md`, `audits/BACKLOG.md`, the
category-level `audits/STATUS.md`, and the human-facing
`audits/STATUS.html` dashboard. After provider inventory, readiness, or source
metadata changes, refresh the committed corpus snapshot and every view:

```powershell
npm run audits:inventory
```

Commit only explicit run-owned paths in the records repository. An audit that
exists only under `F:\OpenScience` is not published evidence. Never edit
generated counts by hand.

## Completion and commits

Final re-audit must execute every accessible advertised runnable surface and
inspect scientifically meaningful, useful, readable output. A passing final
audit makes the exact bytes `candidate-ready`, not done.

One invocation is one product batch. At run close, create at most one local
optimized-shelf commit containing all and only the run's candidate-ready
Skills. Committing exact audited bytes makes them `ready`. Run the
Marketplace's own local `intake:skill` validator against that exact commit;
only accepted Skills become `done`. Form at most one corresponding
bioSkills-Improved commit for the accepted bio-derived subset. Do not preserve
phase-by-phase commits in either product history.

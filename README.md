# Optimizing Agent Science Skills

Working repository for refining open scientific agent Skills: normalize their
structure, prepare reproducible tooling, audit real behavior, fix evidenced
defects, independently re-audit every accessible runnable surface, and retain
the evidence.

Skills come from public provider repositories and remain their authors' work.
Each finished Skill preserves its license and exact provenance. Final Skill
bytes live in
[optimized-scientific-skills](https://github.com/mrsonord2240/optimized-scientific-skills);
this repository holds the control plane and evidence.

## Active method

The modular Skill suite under [`skill/`](skill/) is the active process:

1. `normalize-scientific-skill` removes instruction redundancy and routes
   reusable code and conditional detail.
2. `prepare-scientific-skill-tooling` builds or refreshes the WSL-first
   environment and proves each accessible primary tool with checked output.
3. `audit-scientific-skill` performs a bounded diagnostic initial audit.
4. `fix-scientific-skill` resolves the durable finding ledger and reports
   tooling impact.
5. `reaudit-scientific-skill` independently executes and inspects every
   accessible advertised surface.
6. `optimize-scientific-skills` coordinates five lanes, lands one completed
   batch, and requires the Marketplace's local intake validator to pass before
   calling a Skill done.

Each phase uses a fresh worker and one compact canonical handoff. The final
auditor is never the fixer. Marketplace review, bundle building, submission,
registration, publication, pushes, and pull requests require separate
authorization.

## Repository topology

| Location | Role |
|---|---|
| `F:\optimizing-agent-science-skills` | Control state, audits, fix evidence, handoffs, generators, and the active Skill suite |
| `F:\optimized-scientific-skills` | Canonical editing source and final cross-source Skill product |
| `F:\OpenScience` | Disposable worktrees, environments, public caches, and heavy run output |
| `mrsonord2240/bioSkills-Improved` | Maintained bioSkills-shaped compatibility fork, fed one way from accepted optimized bytes |
| Original provider repositories | Read-only provenance sources |

The maintained bioSkills fork is not a staging editor and is not archived as a
consequence of removing a redundant local checkout.

## Layout

| Path | What |
|---|---|
| `skill/` | Modular orchestrator and independently distributable worker Skills |
| `audits/skills/<skill-id>/<owner>-<repo>@<sha7>/` | Reports, viewers, records, fix summaries, and saved audit scripts |
| `fixes/<skill-id>.md` | Durable finding dispositions and verification summaries |
| `tools/` | Audit publication, provider reconciliation, manifest support, and other deterministic control tooling |
| `scripts/` | Corpus-snapshot, audit-index, backlog, and status-dashboard generation |

The former monolithic files under `process/` were intentionally removed after
their live rules migrated into the modular suite. Historical audit records may
still mention those filenames; those mentions are provenance, not active
instructions.

## Generated records

`audits/CORPUS.json` is the committed snapshot of the canonical provider
inventory. Refresh it after provider inventory, readiness, or source metadata
changes:

```powershell
npm run audits:inventory
```

`audits/INDEX.md`, `audits/BACKLOG.md`, `audits/STATUS.md`, and the human-facing
`audits/STATUS.html` dashboard are generated from that snapshot and the
published audit records:

```powershell
npm run audits:index
```

The inventory command also regenerates all four views. Never edit their counts
by hand.

Raw run outputs, downloaded public datasets, environments, and installed tools
remain under `F:\OpenScience`. They are reproducible evidence inputs, not Git
product files.

## Credit and licenses

- Provider Skills retain their original authorship, license, and provenance.
- The audit method is derived from AIPOCH's MIT-licensed `skill-auditor`.
- Audit and fix work is commissioned by Samuel Nord and is not an endorsement
  by the original Skill authors.
- Repository-owned tooling, process Skills, and records are MIT licensed; see
  [LICENSE](LICENSE) and [NOTICE](NOTICE).

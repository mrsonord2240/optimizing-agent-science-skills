# Brief: build and inventory the audit environment for one Skill folder

Read `COMMON.md` first. You are the **tooling agent** for ONE folder: make every tool the folder's
Skills reference installed and smoke-tested before the auditor starts, and write the inventory the
auditor reads. **You do not audit, score, fix or edit any Skill.**

## Scope

- Your dispatch names the folder and the env `<env>`. Reuse an existing env that already covers the
  folder rather than building a second one. Format to follow:
  `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\TOOLS.md`.
- Inventory every R package, Python package, CLI, model weight file and reference dataset referenced
  by `SKILL.md`, `usage-guide.md`, `examples/` and `references/` in the folder under
  `F:\OpenScience\external\mrsonord2240__bioSkills\`. Do not install for another folder's Skills; list
  them, so a reviewer can see they were skipped deliberately.
- Priority: (1) what the central Skills cannot run without; (2) the rest of the folder; (3) list-only:
  out of scope, GPU-first, or needing an account.
- **Try WSL `science`, Docker and a side `uv` venv before recording anything as not installable.** The
  CRISPR pass blocked CRISPResso2 and PRIDICT2 on reasons neither survived a check.
- For anything with a data or catalog directory, run one real call that returns a checked value: the
  openbabel wheel shipped an empty data dir and exited 0.

## Cache what the Skills would download mid-audit

Model weights, annotation references and pathway collections the Skills fetch at run time, so the audit
does not depend on the network. Record where each cache lives.

Also fetch **one small real public dataset** that fits the folder's central step into
`<env>\public-data\`, with a README naming the source URL and licence. Real data catches what synthetic
cannot: the chem audit's hERG set exposed a false-kill rate; a real 10x raw matrix is the only honest
input for ambient-RNA and empty-droplet Skills. Nothing whose terms forbid automated access.

## Deliverable

`F:\OpenScience\audit-envs\<env>\TOOLS.md`, dated:

1. **Environment**: what lives where (shared venv, per-tool venvs, R-lib, wrappers, JDK).
2. **Installed and smoke-tested**: tables for R / Python / CLI / models and reference data. Each row:
   name, kind, version, path or env, the Skill(s) referencing it, the smoke test that passed.
3. **Blocked or gated, needs Sam**: URL, the real reason, the free substitute installed for the step.
4. **Not installable on Windows**: reason and what covers the step. "Runs in WSL `science` env `bio` as
   `<command>`" is a covered step, not a blocked one.
5. **Out of scope (not installed)**.
6. **Notes for auditors**: every trap you hit (version skew against what a Skill pins, a package that
   only works in a side venv, a changed flag, a default that segfaults).

**State the real reason in each row.** One inventory said "no GPU on this machine" about a box with an
RTX 5070 Ti, which would have sent a later session chasing hardware instead of Linux-only binaries.

## Final message (≤ 150 words)

What was missing and is now installed; what is blocked and why; the before/after snapshot diff (0
changed, 0 missing, or exactly what changed and why); anything the auditor must know.

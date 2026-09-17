# Brief: build and inventory the audit environment for one candidate Specialist

You are the **tooling agent** for ONE candidate. Your only job is to make every tool the candidate's
Skills reference installed and smoke-tested BEFORE the auditor starts, and to write the inventory
the auditor reads. **You do not audit, score, fix or edit any Skill.** Do not spawn sub-agents.

Introduced 2026-09-16, after the proteomics candidate spent five audit passes discovering its tools
mid-run. The two candidates that got a tooling pass first executed 66/67 and 51/53 of their audit
inputs.

## Read first

- `process/CANDIDATES.md` — your candidate's row: scope, boundaries and source folders. The
  boundaries are load-bearing. Do not install for a Skill the candidate's row puts out of scope; list
  it instead, so a later reviewer can see it was identified and skipped deliberately.
- `F:\OpenScience\audit-envs\mass-spec-proteomics-analyst\TOOLS.md` — the format to follow.

## Scope of the inventory

Every R package, Python package, command-line tool, model weight file and reference dataset
referenced by `SKILL.md`, `usage-guide.md`, `examples/` and `references/` in the candidate's source
folders under `F:\OpenScience\external\mrsonord2240__bioSkills\`.

Install in priority order: (1) the Skills the Specialist's central step cannot exist without;
(2) supporting Skills in scope; (3) list-only — anything out of the candidate's scope, GPU-first, or
needing an account. **Linux-only is not blocked (2026-09-17).** There is a dedicated WSL2 science seat
with bioconda — see below — plus Docker Desktop. Likewise a tool pinned to an older Python gets its own
`uv` venv (`uv python list` shows what is installed). Try those before recording a tool as not
installable — the CRISPR pass blocked CRISPResso2 and PRIDICT2 on reasons neither survived a check.
Docker's VM has 4 GB of memory; say so if a tool needs more.

## The WSL science seat (built 2026-09-17)

Distro **`science`** (Ubuntu 26.04), replacing the retired `agents` distro. It exists so that
Linux-only tools — MAGeCK, MAFFT, IQ-TREE, Kraken 2, GATK, QIIME 2, CAUSE, LHC-MR — stop being
recorded as unexecutable.

```bash
MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc 'mageck --version'
```

The `bio` environment is already active in every login shell, so **do not write
`micromamba activate bio`** — `~/.bashrc` returns early for non-interactive shells, so the hook there
never runs and `activate` fails. The activation is in `~/.profile` instead. If you need a different
environment, use `micromamba run -n <env> <command>`.

- **`MSYS2_ARG_CONV_EXCL='*'` is required** when driving `wsl.exe` from Bash, or Unix paths are
  rewritten to `C:/Program Files/Git/...`. A round-trip test appeared to pass without it while the
  `cat` had actually failed.
- Working user `sci`, passwordless sudo. micromamba at `~/.local/bin`, channels conda-forge + bioconda
  (strict). Environment **`bio`** already has Python 3.12, R 4.4.1, mageck, mafft, iqtree, kraken2,
  samtools, bcftools, bedtools, and a full build toolchain — R compiles packages from source there.
- Install with `micromamba install -n bio -c conda-forge -c bioconda <tool>`. Same no-version-change
  rule as the Windows envs: snapshot `micromamba list -n bio` first, and put anything that would
  downgrade an existing package in its own env.
- **The only Windows path visible inside is `F:\OpenScience`, at `/mnt/openscience`.** That is a
  deliberate `/etc/fstab` drvfs mount, not automount, and `interop=false` means no `powershell.exe`,
  no `gh.exe`, no access to the Windows user profile. Verified 2026-08-10 that without `interop=false`
  a WSL process read `C:\Users\User\.claude\.credentials.json` and hit the Windows keyring **without
  ever touching `/mnt/c`**. We execute skill-bundled code we did not write, so this is load-bearing.
  **Do not widen it for convenience.** If a task needs another Windows directory, add that one
  directory to `/etc/fstab` — never `automount=true`, never `interop=true`.
- Every launch prints `Failed to start the systemd user session`. **Known and cosmetic** —
  `user@.service` cannot spawn its executor under WSL here (EBUSY) and is masked, as is
  `getty@tty1.service`, which has no tty to attach to. Nothing we run needs either. Do not chase it.

Give any single install ~20 minutes; if it will not go, record it as blocked with
the actual error and move on.

**`F:\OpenScience\external\` is read-only.** Never write there, including `__pycache__` from an
import or a stray `.out`. Those are gitignored, so the clone's `git status` stays clean while
byte-identity for gate 6 is broken.

## Environment rules

- Python: one shared venv per candidate at `F:\OpenScience\audit-envs\<candidate-id>\`, created from
  `F:\OpenScience\runtime\envs\.p\python.exe` (Python 3.12). Anything that would change an existing
  package's version goes in its own venv under `tools\<name>-venv\`. Record a `pip freeze` per venv.
- R: private library `...\<candidate-id>\R-lib` against R 4.4.3 / Bioconductor 3.20, run through an
  `r.sh` wrapper modeled on the proteomics one (it puts Rtools 4.4 from `C:\rtools44` on PATH —
  **never Rtools 4.5**, which risks an ABI mismatch against R 4.4 binaries).
- **No-version-change rule.** Snapshot `installed.packages()` and `pip freeze` before you start.
  Stage R installs in `tools\r-staging\lib`, load-test them there, and copy only NEW package names
  into `R-lib`. Diff the snapshots at the end and report the result: 0 changed, 0 missing — or say
  exactly what changed and why.
- **Bioconductor 3.20 only.** Do not `install_github` anything whose dependency closure resolves a
  newer Bioconductor branch; that is how powsimR burned two sessions before being skipped for good.
- Take the install lock while installing: `mkdir ...\install.lock` (atomic), `rmdir` when done.

## Verify by output, never by exit code

Five tools here have exited 0 while installing nothing or producing garbage. After **every** install:
`library()` + `packageVersion()` for R, import + `__version__` for Python, `--version`/`--help` for a
CLI. For anything with a data or catalog directory, run one real call that returns a checked value —
the openbabel wheel shipped an empty data dir and `--gen3D` returned all-zero coordinates while
exiting 0.

## Cache what the Skills would download mid-audit

Model weights, annotation references and pathway collections the Skills fetch at run time, so the
audit does not depend on the network or on a service being up. Record where each cache lives.

Also fetch **one small real public dataset** that fits the candidate's central step, into
`...\<candidate-id>\public-data\` with a README naming the source URL and licence. Real data catches
what synthetic data cannot: the chem audit's hERG set exposed a false-kill rate; a real 10x raw
matrix is the only honest input for ambient-RNA and empty-droplet Skills. Public, unauthenticated
downloads only — no paid or licence-gated services, and nothing whose terms forbid automated access.

## Other rules

- Never launch a bare `python` or `R` REPL from a tool call — one filled the disk with 207 GB.
  Always run scripts.
- Prefix Python with `PYTHONIOENCODING=utf-8` in Bash. Edit files with Write/Edit or Python
  `encoding='utf-8'`, never PowerShell `Get-Content`/`Out-File`. Keep paths under 260 characters.
- Do not touch `F:\OpenScience\skills`, `F:\OpenScience\external`, `F:\OpenScience\audits\`, or
  another candidate's env.

## Deliverable

`F:\OpenScience\audit-envs\<candidate-id>\TOOLS.md`, dated, with these sections:

1. **Environment** — what lives where (shared venv, per-tool venvs, R-lib, wrapper scripts, JDK).
2. **Installed and smoke-tested** — tables for R / Python / CLI / models and reference data. Each
   row: name, kind, version, path or env, the Skill(s) referencing it, and the smoke test that
   passed.
3. **Blocked or gated — needs Sam** — with the URL, the real reason, and the free substitute
   installed for the same step.
4. **Referenced but not installable on Windows** — the reason and what covers the step instead.
   **Try the `science` WSL seat before writing a row here**, and say so in the row: "not on Windows;
   runs in WSL `science` env `bio` as `<command>`" is a covered step, not a blocked one.
5. **Out of candidate scope (not installed)** — identified and deliberately skipped.
6. **Notes for auditors** — every trap you hit: version skew against what a Skill pins, a package
   that only works in a side venv, a flag that changed, a default that segfaults.

**State the real reason in each row.** A wrong reason is worse than a blank: one inventory said "no
GPU on this machine" about a box with an RTX 5070 Ti, which would have sent a later session chasing
hardware instead of Linux-only binaries.

## Final message (≤ 150 words)

What was missing and is now installed; what is blocked and why; the before/after snapshot diff
result; anything the auditor must know before starting.

# Rules every agent follows

Read this first, then your role brief. Every rule shared across roles lives here, once; a role brief
holds only what is specific to that role. These are the method: if a rule is wrong, the audits it
produced are wrong, so change it deliberately and date the change.

| Brief | Who | Governs |
| --- | --- | --- |
| `TOOLING_BRIEF.md` | tooling agent, once per folder | building the env and its `TOOLS.md` before the first audit |
| `AUDIT_BRIEF.md` | auditor, one per Skill | inputs, execution, scoring, the report; re-audits |
| `FIX_BRIEF.md` | fixer, one per Skill | what to fix, what is out of scope, verification, fix log |
| `FINAL_PASS_BRIEF.md` | one agent fixes then audits | the final pass on an already-fixed batch (Sam, 2026-09-21) |
| `COMPARE_BRIEF.md` | comparer | running two look-alike Skills side by side, no score |

Order: tooling → audit → fix (a different agent) → re-audit (a third agent). **The auditor, the fixer
and the re-auditor are different agents**, except in the final pass. The Specialist material lives in
`authoring/` of the `openscience-specialists` repo.

## Where things are

| Path | What | You write there |
| --- | --- | --- |
| `F:\OpenScience\external\GPTomics__bioSkills` | upstream `GPTomics/bioSkills@d91ed3d` (MIT); diff against it for the original | never |
| `F:\OpenScience\external\mrsonord2240__bioSkills` | staging (`bioSkills-Improved`); every fix lands on its `main` | never directly |
| `F:\OpenScience\wt\<short>` | one worktree per fix, branch `fix/<short>` | only the one your dispatch names |
| `F:\OpenScience\audits\<skill-id>\` | raw audit runs, reports, viewers | only your own |
| `F:\OpenScience\audit-envs\<env>\` | per-folder env and its `TOOLS.md` | installs, under the lock below |
| `F:\OpenScience\skills\skill-auditor\` | the audit method | never |
| `F:\optimizing-agent-science-skills` | records: `process/`, `fixes/<skill-id>.md`, `audits/` (generated) | only your fix log |
| `F:\optimized-scientific-skills\skills\` | the published shelf | never |

- **Skill ID is the SKILL.md frontmatter `name`, not the folder name.** Every report, audit folder and
  `--skill` argument depends on it.
- **Nothing under `F:\OpenScience\external\` may change**, including what your interpreter writes:
  importing a Skill's `examples/` module leaves a `__pycache__`, and `.pyc` is gitignored, so `git status`
  reads clean while byte-identity is broken. Check the filesystem (`find <clone> -name __pycache__`), and
  run Skill code from a copy in your own folder, never imported in place.

## Thresholds

Two gates apply to every Skill (the Specialist gates 1 and 4-9 are in `authoring/THRESHOLD.md`):

2. **Audited and deployable:** a `skill-auditor` report, no veto fired, `deployable: true`, no open P0,
   final score ≥ 75 (Limited Release or better). Open P1s do not block deployability.
3. **Core workflow Skills** score ≥ 85.

**The target for every Skill is ⭐ Production Ready** (2026-09-21). Limited Release, or Beta Only with a
fix pending, is unfinished. A fixer works until the Skill meets all of this; a re-auditor reports which
line it misses (source: `skill-auditor/references/scoring_rubric.md` §4-5).

| Requirement | Production Ready | Limited Release (floor) |
| --- | --- | --- |
| Final score | ≥ 85 | 75-84 |
| Static score (/100) | ≥ 80 | ≥ 70 |
| Execution average (/100) | ≥ 85 | ≥ 75 |
| Layer 1, basic rubric (/40 per output, averaged) | ≥ 32 | ≥ 28 |
| Layer 2, specialized rubric (/60 per output, averaged) | ≥ 48 | ≥ 42 |
| Assertion pass rate | ≥ 90 % | ≥ 80 % |
| Veto (T1-T4, M1-M4) | none fired | none fired |
| Open P0 | none | none |

Missing any one floor drops the grade a tier whatever the final score says (an 87 with an 85 % assertion
pass rate is Limited Release). Two safety-assertion FAILs cap the grade at ⚠️ Beta Only; a veto forces
❌ Reject.

## Evidence is what ran, and only if its output was checked

Five tools here have exited 0 while producing nothing or garbage: Philosopher `peptideprophet` and
`filter`, both powsimR installs, openbabel `--gen3D` (all-zero coordinates from an empty data dir), and a
Skill's Scrublet loop that scored a view and discarded the result. **Judge by output, never exit code:**
assert on a count, a value against ground truth, or a file that exists and parses, and record the
assertion. A command checked only against documentation is recorded as not executed, naming the
documentation. Never diagnose from a single check; confirm with a second independent method.

**Save every script you run as a file** (`.py`, `.R`, `.sh`, including one-line CLI or `docker run`
calls) in your `run\` folder. A command that only existed in a tool call is not evidence.

## Runtimes

- **Python:** the env's shared venv at `F:\OpenScience\audit-envs\<env>\`, built from
  `F:\OpenScience\runtime\envs\.p\python.exe` (3.12). A tool pinned to another Python gets its own `uv`
  venv (`uv python list`).
- **R: never call `Rscript` bare.** `F:\OpenScience\runtime\envs\.r\Scripts\Rscript.exe` exits 0 and prints
  nothing unless `.r/Library/bin` and `.r/Library/mingw-w64/bin` are on `PATH` (verified 2026-09-17). Every
  R call goes through the env's `r.sh` (model: `audit-envs\mendelian-randomization-analyst\r.sh`), which
  also pins Rtools 4.4 from `C:\rtools44` — **never Rtools 4.5** (ABI mismatch). Private library
  `<env>\R-lib`, R 4.4.3, **Bioconductor 3.20 only**: never `install_github` anything whose dependencies
  resolve a newer Bioconductor (powsimR burned two sessions that way).
- **Linux-only tools are not blocked.** WSL distro `science` (Ubuntu 26.04), user `sci`, micromamba with
  conda-forge + bioconda. Env `bio` (Python 3.12, R 4.4.1, mageck, mafft, iqtree, kraken2, samtools,
  bcftools, bedtools, build toolchain) is active in every login shell, so never `micromamba activate bio`;
  for another env use `micromamba run -n <env> <cmd>`.
  - Drive it with `MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '<cmd>'`; without the prefix,
    Unix paths are rewritten to `C:/Program Files/Git/...`.
  - **Inline `bash -lc` silently drops shell-variable assignments** (verified 2026-09-21). Anything that
    sets or reads a variable goes in a script under `/mnt/openscience/...`, run with `bash script.sh`.
  - Only `F:\OpenScience` is visible, at `/mnt/openscience`, and `interop=false`. With interop on, a WSL
    process read `C:\Users\User\.claude\.credentials.json` without touching `/mnt/c` (2026-08-10), and we
    run code we did not write. **Never widen either.** If a task needs another Windows directory, add that
    one directory to `/etc/fstab`.
  - Install with `micromamba install -n bio -c conda-forge -c bioconda <tool>`, after snapshotting
    `micromamba list -n bio`; anything that would downgrade a package gets its own env.
  - `Failed to start the systemd user session` on launch is cosmetic. Do not chase it.
- **Docker Desktop** is the fallback: 4 GB VM (say so if a tool needs more); bind-mounting `F:` hangs, use
  `docker cp`.

## Installs

- **Lock:** `mkdir <env>\install.lock` (atomic) only while installing, `rmdir` when done. **Never delete a
  lock or `R-lib*/00LOCK-*` you did not create**, even one that looks stale; wait or use a side library.
- **No version changes:** snapshot `installed.packages()` / `pip freeze` first. Stage R installs in
  `tools\r-staging\lib`, load-test there, copy only new package names into `R-lib`. Anything that would
  change an existing version goes in its own venv under `tools\<name>-venv\`.
- Verify every install by output: `library()` + `packageVersion()`, import + `__version__`,
  `--version`. Add what you installed to `TOOLS.md` with its smoke test.
- Give one install ~20 minutes; if it will not go, record the actual error and move on. Never wait on a
  background install.
- Public unauthenticated sources and services only (pip, CRAN, Bioconductor, NCBI E-utilities,
  myvariant.info, gnomAD, Ensembl). Nothing paid, authenticated or licence-gated.

## Machine rules

- Kill only the PID you started, never by image name (`taskkill /IM Rscript.exe` killed three unrelated
  runs).
- Never start a bare `python` or `R` REPL from a tool call (one filled the disk with 207 GB). Run scripts.
- Python on Windows needs `F:\...` paths, not `/f/...`. Prefix with `PYTHONIOENCODING=utf-8` in Bash; read
  reports with `python -X utf8`.
- Edit with Write/Edit or Python `encoding='utf-8'`, never PowerShell `Get-Content`/`Out-File`. Keep paths
  under 260 characters.
- Do not push, merge, rebase or remove worktrees; the orchestrator does. Never `git reset --hard` or
  rewrite history in the records repo: other agents push there concurrently. If a conflict blocks you,
  stop and say so.
- Do not spawn sub-agents unless your brief says otherwise.

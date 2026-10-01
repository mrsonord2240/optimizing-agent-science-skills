# Handoff: bio-atac-seq-footprinting / final re-audit

- Updated: 2026-09-30 17:30 PDT
- Lane: 1
- Status: **candidate-ready**
- Owner leaving: reaudit-scientific-skill worker (fresh, independent; did not fix, tool or previously audit the candidate)
- Next role: orchestrator (commit the exact bytes to make them `ready`, then intake)

## Certified candidate

- Path: `F:\OpenScience\wt\atac-footprinting\skills\bio-atac-seq-footprinting` (branch `fix/atac-footprinting` @ 3186916, directory untracked)
- Identity: `sha256-manifest-v1 86dd7a021575d6f8ed7c8c5462a9ecdc1061640e8f6e6b122b32b140808c02e2`, 7 files, 52,673 bytes. Recomputed before, during and after execution: identical.
- Supersedes: `mrsonord2240-optimized-scientific-skills@ea3b976` (candidate `a71e5610...`, 86).

## Readiness metrics

| Gate | Value | Floor |
|---|---|---|
| Final | 88 | 85 |
| Static | 90 | 80 |
| Execution average | 87.0 | 85 |
| Layer 1 / Layer 2 | 35.5 / 51.5 | 32 / 48 |
| Assertions | 30/30 | 90 % |
| Vetoes, open P0, open P1 | none | none |

## Evidence

- Raw run: `F:\OpenScience\audits\bio-atac-seq-footprinting\reaudit-final-20260930\` (`report.json`, `viewer.md`, `source-identity.json`, `scripts/`, `logs/`, `out/`)
- Published record: `audits/skills/bio-atac-seq-footprinting/candidate@86dd7a021575-reaudit-final-20260930/` (23 scripts). `npm run audits:index` and `audits:check` pass.
- Heavy artifacts (disposable, 4.2 GB): `F:\OpenScience\audit-envs\bio-atac-seq-footprinting\reaudit-final\`

## What was checked

- CTCF bias check: rc 0 with real correction and rc 4 with correction absent, at full depth, 20% depth and NFR-only fragments.
- scPrinter in a fresh usage-guide env: bulk, `--groups` per-cluster, `--shift` (source and `detect_shift`), guards.
- seq2PRINT: usage-guide blocks run to rc 0 in 29 min (bounded; weak model, as documented).
- HINT-ATAC, Wellington `-A`, `site_concordance.sh`: re-run in the live envs.

## Remaining findings (P2)

- FOOT-016: the bias check catches absent correction, not always partial correction; the 0.2 default rests on two libraries.
- FOOT-017: the usage guide does not warn that bound-versus-unbound contrast cannot pick the scPrinter `--shift`.

## Not executed

- LoRA single-cell seq2PRINT and `seq_tfbs_seq2print`: resource-infeasible on the staged data; labelled not run in the Skill.
- Full-depth whole-genome runs: resource-infeasible.
- RGT data recipe rebuild, NFR count check, `alignmentSieve --ATACshift`: text and env fingerprints unchanged; prior re-audit evidence stands.

## Worktree state

- Skill bytes untouched; no commit, push or intake.
- `F:\optimizing-agent-science-skills`: new published version dir, regenerated `audits/INDEX.md` and `audits/BACKLOG.md`, this handoff. `fixes/bio-atac-seq-footprinting.md` was already modified by the fixer and is untouched.
- Fresh env `footprint-scprinter` removed; live env fingerprints unchanged; no run-owned processes remain.

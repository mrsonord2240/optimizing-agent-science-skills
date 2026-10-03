# Handoff: bio-ensembl-rest / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: candidate-ready
- Owner leaving: independent re-auditor (lane 2)
- Next role: orchestrator (commit to make `ready`, then intake)

## Certified candidate

- Identity (preflight --offline PASS before and after): sha256-manifest-v1 dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b, files=7, bytes=28785
- Path: F:\OpenScience\wt\dbaccess-ensembl-rest\skills\bio-ensembl-rest (branch fix/dbaccess-ensembl-rest at 2f38178; Skill dir untracked, uncommitted by design; no pycache)
- Published record: audits\skills\bio-ensembl-rest\candidate@dabba949803e-reaudit-run\ (supersedes the initial audit 3d116ba2e1c5)
- Run dir and evidence: F:\OpenScience\audits\bio-ensembl-rest\reaudit-run\ (scripts\evidence\)

## Readiness metrics

Score 87, Production Ready. Static 87, execution average 86.6, Layer 1 35.2, Layer 2 51.4, assertions 22/23 (96%). No veto, no open P0.

## Findings

ENS-001 to ENS-008: all verified-fixed (ledger: reaudit-run\finding-ledger.md). No new finding above P2.

P2 observations (not blocking): compara example not reproduced end to end on final bytes; VEP example prints one line per transcript.

## Surfaces not executed or failed

- examples\compara_homology.py: five attempts, Ensembl homology 500 / 503 / ReadTimeout (service-side), each a clean EnsemblError. Output taken from the fixer run on identical bytes (files unmodified since); live probes of BRCA1 paralogs ([]) and TP53 to mouse passed.
- Archive e116: 503 (service-side outage); failure guard verified (EnsemblError).
- Local VEP, BioMart bulk: out of scope.
- examples\vep_annotation.py passed on the fourth attempt (three service 500s).

## Worktree state

- Run-owned: audits\skills\bio-ensembl-rest\candidate@dabba949803e-reaudit-run\ (untracked), reaudit-run dir, this handoff, regenerated audits\ views
- Pre-existing/user-owned: test\validate.bats (untouched)
- No staging, commit or push in any repository.

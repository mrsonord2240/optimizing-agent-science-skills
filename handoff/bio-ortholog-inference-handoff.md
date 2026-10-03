# Handoff: bio-ortholog-inference / reaudit-scientific-skill

- Updated: 2026-10-03
- Lane: 2
- Status: not candidate-ready (score 84 < 85)
- Owner leaving: independent re-auditor (lane 2)
- Next role: fix-scientific-skill (two small P2 items), then a fresh re-audit

## Rejected candidate

- Identity (preflight --offline PASS before and after): sha256-manifest-v1 aa32b51586699da5ed4708ce63e6cbc9eb19751ed79f94b5ff5d73208e252495, files=7, bytes=34073
- Path: F:\OpenScience\wt\dbaccess-ortholog-inference\skills\bio-ortholog-inference (branch fix/dbaccess-ortholog-inference at 2f38178; Skill dir untracked, uncommitted; no pycache)
- Published record: audits\skills\bio-ortholog-inference\candidate@aa32b5158669-reaudit-run\ (supersedes the initial audit f6d4ccc5903d)
- Run dir and evidence: F:\OpenScience\audits\bio-ortholog-inference\reaudit-run\ (scripts\evidence\)

## Readiness metrics

Score 84, Limited Release. Static 82, execution average 85.4, Layer 1 34.6, Layer 2 50.8, assertions 23/25 (92%). No veto, no open P0. Fails only the final-score gate (85).

## Findings

- OI-01 to OI-08: verified-fixed (ledger: reaudit-run\finding-ledger.md). B1 OMA flakiness: not reproduced (OMA 200 on every call). B2 eggNOG: still blocked (403 / TLS), not executed.
- New, P2: OI-09 SKILL.md `/homology/id/<ensembl_gene_id>` returns 404; write `/homology/id/<species>/<ensembl_gene_id>`.
- New, P2: OI-10 examples\compara_orthologs.py hides batch symbols that failed (MDM2 read timeout, error column) or returned nothing (BRCA1); print them after the table.
- New, P2: eggNOG redirect note stale (eggnog6.embl.de now fails TLS; eggnogdb.org/api 403).

## Surfaces not executed or failed

- eggNOG API: refuses scripted access.
- PANTHER: liveness only (no client function, as documented).
- Ensembl homology was slow (45 s read timeouts on BRCA1/MDM2 to zebrafish); service-side. The final-bytes compara_orthologs.py run exited 0 on the first attempt.

## Worktree state

- Run-owned: audits\skills\bio-ortholog-inference\candidate@aa32b5158669-reaudit-run\ (untracked), reaudit-run dir, this handoff, regenerated audits\ views
- Pre-existing/user-owned: test\validate.bats (untouched)
- No staging, commit or push in any repository.

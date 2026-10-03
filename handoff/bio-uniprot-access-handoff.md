# Handoff: bio-uniprot-access / fix-scientific-skill (text-only batch)

- Updated: 2026-10-03
- Status: ready-for-phase
- Next role: reaudit-scientific-skill (delta mode, text-only change to certified bytes)
- Tooling impact: none

## Candidate identity

- New: sha256-manifest-v1 `7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b`, files=6, bytes=30468; `skill_preflight.py --offline` PASS, no pycache
- Previously certified (86, Production Ready): `ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1`, files=6, bytes=30291, record `audits\skills\bio-uniprot-access\candidate@ea100b041caf-reaudit-run\`
- Tree: `F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access` (untracked, uncommitted by design)

## Finding

- UNI-010 (P2): fixed (text-only). SKILL.md endpoint-table "Proteome FASTA" row now states reviewed and unreviewed TrEMBL entries are both returned (human UP000005640: 147,520 entries, 37.8 MB gzip) and that `AND reviewed:true` restricts to Swiss-Prot. The example's printed string literal now says ~38 MB compressed; ~87 MB unpacked; ~147.5K entries (reviewed + TrEMBL).
- Files changed: `SKILL.md`, `examples/isoforms_and_xrefs.py` (string literal inside a print only; ast.parse OK). Exact diff: `F:\OpenScience\audits\bio-uniprot-access\text-fix-run\diff.txt`
- Not executed this phase (text-only; delta re-audit executes).

## Worktree

Nothing staged, committed or pushed; `test\validate.bats` untouched.

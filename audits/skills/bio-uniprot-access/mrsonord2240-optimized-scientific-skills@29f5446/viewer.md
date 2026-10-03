> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@29f5446](https://github.com/mrsonord2240/optimized-scientific-skills/tree/29f5446e431db8eba803796e6f7dfc02f7886743/skills/bio-uniprot-access) match audited candidate `7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-uniprot-access`**
> - Audited working candidate `7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/uniprot-access), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-uniprot-access

**Date:** 2026-10-03
**Candidate:** `F:\OpenScience\wt\dbaccess-uniprot-access\skills\bio-uniprot-access` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 7a203a5063ea1cdad2c32516c1cc1740eb13c1e5008d53c5950e81b8cfdf7f5b` (6 files, 30,468 bytes), derived from certified `ea100b041cafcbf60a8d1202d6ca09387fff80515d37b45d5998162fb799bcb1` (86, Production Ready; record `candidate@ea100b041caf-reaudit-run`)
**Result:** Candidate-ready: **88/100, Production Ready** (static 87, execution average 88.7). UniProt release 2026_03. Delta mode: the text-only change qualified.

## Delta verification

| Check | Result | Evidence |
|---|---|---|
| Unchanged files (LICENSE, uniprot_query.py, uniprot_client.py, usage-guide.md) | byte-identical to certified | `evidence/text_claims.txt` |
| SKILL.md | only the Proteome FASTA table cell differs; reverting that cell reproduces the certified sha256 | `evidence/text_claims.txt` |
| examples/isoforms_and_xrefs.py | reverting the one string literal reproduces the certified sha256; ASTs differ only in that Constant | `evidence/text_claims.txt` |
| 147,520 entries, 37.8 MB gz, 20,416 reviewed | measured in the certified run; live counts re-queried (147,520 / 20,416, release 2026_03) | `reaudit-run/evidence/proteome_counts.txt` |
| ~87 MB unpacked | certified download measured 86,650,690 bytes (86.65 MB decimal, same convention as 37.8 MB gz) | `reaudit-run/evidence/proteome.txt` |
| `AND reviewed:true` on /uniprotkb/stream | returns 20,416 sp records and 0 tr records | `evidence/text_claims.txt` |
| Changed example executed | exit 0, new text printed | `evidence/example.txt` |

## Findings

- **UNI-010 (P2): verified-fixed.** SKILL.md and the example now state that the proteome route returns reviewed and TrEMBL entries, give the measured sizes, and show the `reviewed:true` restriction.
- No new findings. No open findings.

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | 88 (34.8 + 53.2) | 85 |
| Static | 87 | 80 |
| Execution average | 88.7 | 85 |
| Layer 1 average | 35.5 / 40 | 32 |
| Layer 2 average | 53.2 / 60 | 48 |
| Assertions | 30 / 30 | 90% |
| Veto / open P0 | none / none | none |

Carried forward from the certified record: all other scores and executed evidence (code bytes unchanged). Re-scored: functional suitability 11 to 12, human usability 7 to 8, input 5 (basic 31 to 35, specialized 46 to 52; assertion 4 now PASS).

Rerun: `Scripts\python.exe delta-reaudit-run\scripts\verify_text_only.py` and `reviewed_route_check.py`.

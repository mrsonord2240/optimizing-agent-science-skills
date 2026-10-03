> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@29f5446](https://github.com/mrsonord2240/optimized-scientific-skills/tree/29f5446e431db8eba803796e6f7dfc02f7886743/skills/bio-interaction-databases) match audited candidate `f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-interaction-databases`**
> - Audited working candidate `f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/interaction-databases), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Delta re-audit: bio-interaction-databases

**Date:** 2026-10-03
**Candidate:** `F:\OpenScience\wt\dbaccess-interaction-databases\skills\bio-interaction-databases` (untracked, uncommitted by design)
**Exact identity:** `sha256-manifest-v1 f4d95b083e70343c570554032b0592bc13d99f578274465d12367b91bf286c2d` (6 files, 42,364 bytes), derived from certified `16290147ab41129829074d65394467e2df7131b08099d0f2a4d42497af154024` (87, Production Ready; record `candidate@16290147ab41-reaudit-run-2`)
**Result:** Candidate-ready: **87/100, Production Ready** (static 87, execution average 87.0). Delta mode: the text-only change qualified.

## Delta verification

| Check | Result | Evidence |
|---|---|---|
| Unchanged files (LICENSE, both examples, usage-guide.md) | byte-identical to certified | `evidence/self_rows.txt` |
| SKILL.md | only the aggregate_networks parenthetical differs; reverting it reproduces the certified sha256 | `evidence/skill_md.txt` |
| scripts/interaction_clients.py | two docstring lines differ; reverting them reproduces the certified sha256; AST identical once the aggregate_networks docstring is removed | `evidence/self_rows.txt` |
| `gene_a == gene_b` rows remain in biogrid_lt_physical | true live with the real key: TP53 30 of 3,081 rows, MDM2 23 of 2,058 | `evidence/self_rows.txt` |
| Homodimer-only gene is not a node; aggregate has no self-loops | certified mocked probe (homodimer-only graph 0 nodes, 0 edges); live TP53+MDM2 aggregate 2 nodes, no self-loops | `reaudit-run-2/evidence/probe_idm10_11.txt`, `evidence/self_rows.txt` |

## Findings

- **IDM-012 (P2): verified-fixed.** The SKILL.md bullet and the docstring name homodimers, say such a gene is not a node, and point to `biogrid_lt_physical`. Dropping remains silent by design (no warning or count); it is now documented.
- **IDM-013 (P2): still open**, untouched by design (example edge attributes depend on SIGNOR record order).
- No new findings.

## Readiness gate

| Metric | Value | Requirement |
|---|---:|---:|
| Final score | 87 (34.8 + 52.2) | 85 |
| Static | 87 | 80 |
| Execution average | 87.0 | 85 |
| Layer 1 average | 34.7 / 40 | 32 |
| Layer 2 average | 52.3 / 60 | 48 |
| Assertions | 35 / 35 | 90% |
| Veto / open P0 | none / none | none |

Carried forward from the certified record: all scores and executed evidence except agent usability 14 to 15 (documentation gap closed). The BioGRID key was loaded at run time only; a scan of the run directory and Skill tree found no hit.

Rerun: `Scripts\python.exe delta-reaudit-run\scripts\self_rows_and_docstring.py` (needs BIOGRID_ACCESS_KEY file) and `verify_skill_md.py`.

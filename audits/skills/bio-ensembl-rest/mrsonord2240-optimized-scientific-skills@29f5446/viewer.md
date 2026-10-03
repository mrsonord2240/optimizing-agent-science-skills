> - Provider binding: exact committed bytes at [mrsonord2240/optimized-scientific-skills@29f5446](https://github.com/mrsonord2240/optimized-scientific-skills/tree/29f5446e431db8eba803796e6f7dfc02f7886743/skills/bio-ensembl-rest) match audited candidate `dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b` byte for byte. The scientific report was neither re-executed nor rewritten.

> **Audit record for `bio-ensembl-rest`**
> - Audited working candidate `dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ensembl-rest), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Independent re-auditor agent (not the fixer), commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Re-audit: bio-ensembl-rest

Identity sha256-manifest-v1 dabba949803e4c58bd3cc906389087520b3e5f5c32702fb6535c749131c0487b (7 files, 28,785 bytes), verified with `skill_preflight.py --offline` before and after. Independent of the fixer and the initial auditor.

**Score 87/100, Production Ready (candidate-ready).** Static 87, execution average 86.6, Layer 1 average 35.2, Layer 2 average 51.4, assertions 22/23 (96%). No veto, no open P0.

| # | Input | Total |
|---|---|---|
| 1 | lookup_and_overlap.py, protein by ENSP, e110 pinning | 89 |
| 2 | vep_annotation.py (region, dbSNP, HGVS c.803C>T) | 87 |
| 3 | compara_homology.py and Compara component calls | 80 |
| 4 | Pinning: e110, e111, GRCh37, e116, e90, timeout | 89 |
| 5 | Batch, LD, regulatory, homology/id, multiple_sequences, error claims | 88 |

Findings ENS-001 to ENS-008: all reproduced as fixed. No new findings; two P2 observations recorded.

Service state during the pass: Ensembl returned HTTP 500, 503 and read timeouts on `/homology` and intermittently on `/vep` and unknown-symbol lookups; the e116 archive host stayed at 503. Each failure surfaced as a clean `EnsemblError` naming the status and URL. `vep_annotation.py` passed on its fourth attempt. `compara_homology.py` failed on all five attempts (500, 503, ReadTimeout), so it was not reproduced end to end here. Its saved fixer output (170 one2one + 29 one2many, mouse ENSMUSG00000017146, `none returned` for paralogs) was inspected; the example and client files have not been modified since that run (mtimes 01:33 vs 01:50, manifest identical). Live probes of the same calls (BRCA1 paralogs `[]`, TP53 to mouse one2one ENSMUSG00000059552, confidence None) passed.

Not executed: `compara_homology.py` end to end (service), e116 archive resolution (503 service outage), local VEP and BioMart bulk routes (out of scope).

Evidence: scripts/evidence/ (run_reaudit.txt, example_*.txt, run_homology_probe.txt, run_batch.txt); scripts/.

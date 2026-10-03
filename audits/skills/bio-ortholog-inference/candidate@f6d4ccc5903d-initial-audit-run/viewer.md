> **Audit record for `bio-ortholog-inference`**
> - Audited working candidate `f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ortholog-inference), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

> **Audit record for `bio-ortholog-inference`**
> - Audited working candidate `f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac`; exact candidate provenance is in [source-identity.json](source-identity.json).
> - Derived from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/database-access/ortholog-inference), authored by [GPTomics](https://github.com/GPTomics) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-10-03 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test inputs and provenance are described in the published scripts/inputs and audit body; raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer - bio-ortholog-inference

Generated: 2026-10-03
Audit type: bounded diagnostic initial audit
Exact candidate content SHA-256: `f6d4ccc5903d157167ae1106f009ecf5d36a0e1d3c56c8a691e63625fcc2e9ac` (6 files, 27397 bytes)

## Summary

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---:|---:|---:|---:|---|
| 1 | Canonical | 30 | 44 | 74 | 3/5 | PARTIAL |
| 2 | Variant A | 20 | 22 | 42 | 2/5 | PARTIAL |
| 3 | Variant B | 36 | 50 | 86 | 4/4 | COMPLETED |

**Execution average:** 67.3 / 100
**Assertion pass rate:** 9 / 14
**Static score:** 72 / 100
**Final diagnostic score:** 69 / 100 - Beta Only (no veto; floors for Production Ready and Limited Release not met)

The strict audit JSON is [report.json](report.json). This is a diagnostic audit, not a certification.

## Veto review

- Skill veto: PASS. Stability was judged on the whole surface: Compara, KEGG and OMA calls succeed when upstream answers; failures were upstream flakiness exposed by missing client guards (OI-02) and one logic defect (OI-01).
- Research veto: PASS. No fabricated values; checked outputs match upstream records.

## Execution classification

| Surface | Class | Evidence |
|---|---|---|
| Compara resolve_symbol / compara_orthologs / compara_one2one | executed | TP53 human->mouse ENSMUSG00000059552 one2one; reverse Trp53; raw record compared |
| MARCH1 rename, batch_compara (zebrafish + bad symbol) | executed | tooling smoke output plus raw Ensembl probes |
| examples/compara_orthologs.py | failed (live) | hung >200 s twice, HTTP 500 once this session; passed in tooling phase |
| OrthoDB orthodb_groups | executed | 100 groups; first hits show full-text semantics (OI-04) |
| OrthoDB orthodb_orthologs | failed | None ids / TypeError (OI-01) |
| OMA oma_orthologs / oma_hog_for_protein / oma_hog_members | executed, intermittent | raw P04637 returns P53_MOUSE; client call 502 on other attempts; BRCA1 returns [] |
| examples/cross_resource.py | failed | exit 1 on OMA 502 (OI-05) |
| KEGG ko_for_gene / genes_for_ko / ko_info, examples/kegg_orthology.py | executed | K04451, 548 members, 446 species |
| PANTHER | executed (liveness only) | no client function; ortholog/matchortho P04637 -> Tp53 (OI-07) |
| eggNOG API | blocked (service) | TLS hostname mismatch and 403 to scripts; Skill labels it unverified |
| HomoloGene | not-applicable | efetch returns "not supported"; Skill states retired |

## Ordered finding ledger (for fix-scientific-skill)

| ID | Priority | Finding |
|---|---|---|
| OI-01 | P1 | orthodb_orthologs returns None ids or raises TypeError on live v12 schema |
| OI-02 | P1 | No request timeouts, no 5xx retry; Ensembl hang/500 and OMA 502 crash helpers and examples |
| OI-03 | P1 | Documented Compara confidence 0/1 is absent from live responses (always None) |
| OI-04 | P1 | OrthoDB /search is free text (TP53 -> TIGAR group first); example uses groups[0] |
| OI-05 | P1 | cross_resource.py has no per-resource error isolation; default BRCA1 OMA leg is empty |
| OI-06 | P2 | Documented OrthoDB /tab endpoint returns 404 |
| OI-07 | P2 | PANTHER evidence-code claim unsupported by live response; no client function |
| OI-08 | P2 | No Skill-root LICENSE; stale oma_orthologs docstring key |

## Upstream versus Skill defects

- Upstream and transient: Ensembl homology hangs and 500s, OMA 502s (unfiltered large result sets 502, `rel_type=1:1` answered), eggNOG refusing scripts, HomoloGene retirement. The Skill advises retry for OMA 502 yet implements none.
- Skill defects: OI-01, OI-03, OI-04, OI-06, OI-07 (claims or parsing that no longer hold) and OI-02, OI-05 (no timeout or error handling).

## Deferred and blocked

- OMA scientific values beyond TP53 (service flaky; rerun later).
- eggNOG API (service refuses scripts; eggNOG-mapper is local and not tooled).
- Tooling delta: none required; a later pass may re-run live probes in `scripts/` once Ensembl and OMA are stable.

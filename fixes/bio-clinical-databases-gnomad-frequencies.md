# bio-clinical-databases-gnomad-frequencies — fixes (2026-09-15)

Branch `fix/variant`. Verified live on 2026-09-15 against the gnomAD browser GraphQL API (Windows venv). SKILL.md blocks executed verbatim from the file (Hail block skipped); example `__main__` run as a subprocess; the myvariant helper run over plain HTTP (see myvariant record: HTTPS certificate mismatch).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| False "v4 constraint autosomes only" claim and note | P1 | Claim, table cells, failure mode, pushback row removed; note only when `gnomad_constraint` is null; description corrected; usage guide updated | ran: DMD (chrX) LOEUF 0.2354 with no note; SCN2A 0.1540; USP9Y (chrY) also returns constraint | |
| GraphQL errors swallowed; GRCh37 ids read as absent | P1 | `query_variant(..., build, dataset)` checks build against dataset; raises on errors other than "Variant not found"; example same; failure mode 3 now describes the build trap | ran: GRCh37 coords on gnomad_r4 -> ValueError; gnomad_r2_1 finds rs334 (FAF95 0.0442 afr); malformed id -> RuntimeError "Invalid variant ID" | a GRCh37 id passed as GRCh38 still reads as not found; the required `build` argument makes the caller state it |
| Absent handling inconsistent (0.0 vs None) | P1 | `grpmax_faf95` returns None with `source` = `absent` or `present_faf95_undefined` (SKILL.md and example) | ran: 17-43106487-A-G absent -> PM2_Supporting; AC=1 14-23412863-A-C -> PM2_Supporting; 14-23430853-C-A 2.34e-4 -> BS1 | tags documented as research annotation |
| Invalid demo variant; myvariant route claims FAF95 | P2 | Demo 17-43106487-A-C; myvariant helper returns gnomAD 2.1.1 AF only; bullets and decision tree say so | ran: example `__main__` (FAF95 1.387e-5 nfe); helper over HTTP (rs80359550 exome AF 0.000291, AN 250,700) | |
| No data-governance note | P2 | Consent/approvals note in SKILL.md and example | text | |
| Common Errors "FAF95 = 0" row wrong | cheap | Null-FAF95 and "Variant not found" rows | live responses above | |

Left unfixed: none.

## Backlog pass — 2026-09-15

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| No rate-limit handling for the gnomAD API | P2 | Added `_post_graphql()` with bounded exponential backoff on HTTP 429 in SKILL.md (`query_variant`, `query_gene_constraint`) and examples/gnomad_query.py (`query_variant_v4`, `query_gene_constraint_v4`); docstrings note batch pacing and point to the existing Hail Table path | ran: mocked requests.post (429, 429, 200) confirms 3 retries then success; live query_variant/query_variant_v4 on BRCA1 17-43106487-A-C unaffected (FAF95 1.387e-05 nfe) | commit 58bcb8d |
| GRCh37 ids declared as GRCh38 still read as absent (item 8) | P2 | Added a "Residual case" bullet to SKILL.md Failure Mode 3: the `build` check only catches a self-contradicting caller (build vs dataset), not GRCh37 coordinates paired with a correctly-stated `build='GRCh38'`; points to spot-checking a known common variant or confirming the reference allele via NCBI Variation Services before trusting a batch of "absent" results | ran: rs334 GRCh38 coords (11-5227002-T-A) on gnomad_r4 -> present, genome AF 0.01272; rs334 GRCh37 coords (11-5248232-T-A) on gnomad_r4 with build='GRCh38' -> "Variant not found" (identical to absent); NCBI Variation Services `/v0/spdi/.../canonical_representative` (0-based SPDI pos 5227001) -> clean match; deliberately wrong position -> "Disambiguation exception" warning; `/v0/refsnp/334` -> live rsID data | docs-only, no code changed; commit 15882e9 |
| SKILL.md long for single lookups (item 9) | P2 | Moved "SV Catalog and CNV", "mtDNA (Laricchia 2022)", and "Anticipated Reviewer Pushback" sections verbatim to usage-guide.md, appended before "## Related Skills"; one-line pointer left in SKILL.md per section. Mirrors clinvar-lookup commit f26acc9. | docs: git diff confirms moved blocks are line-for-line identical (cut-and-paste); both files read end-to-end for markdown integrity | docs-only, no code changed; SKILL.md 446 -> 427 lines, usage-guide.md 100 -> 125 lines; Reconciliation table and all code/decision-tree/threshold content kept in SKILL.md per finding's stated scope; commit 28bdd11 |

Left unfixed: none.

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

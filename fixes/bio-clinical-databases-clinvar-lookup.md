# bio-clinical-databases-clinvar-lookup — fixes (2026-09-15)

Branch `fix/variant`. Verified live on 2026-09-15: NCBI E-utilities, ClinGen Allele Registry (Windows venv, requests); ClinVar GRCh38 VCF slice (fileDate 2026-09-13) and cyvcf2 in the WSL `agents` distro. SKILL.md blocks were executed verbatim from the file.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `car_id()` PUT rejected (403) | P1 | Public `GET /allele?hgvs=`; HTTP 400 `IncorrectReferenceAllele` raised with the actual allele (SKILL.md; example `car_record`/`car_id`, batch uses the same response) | ran: `NC_000017.11:g.43106487A>C` -> CA001182, VariationID 17661; `43094464G>A` -> ValueError (actual T) | |
| Gene search truncates at 500 | P1 | Returns `(count, ids)`, pages with `retstart`; multi-gene `[gene]` note | ran: BRCA1 P/LP 4,721 of 4,721 unique; BRCA1 all 16,064 of 16,064 (paging past 10,000 works) | |
| Stale review-status string; ALLELEID labelled `vcv_id` | P1 | `criteria provided, conflicting classifications` -> 1 star (old wording kept); lookup returns `variation_id` (VCF ID) and `allele_id` | ran: VariationID 441519 -> 1 star; lookup on live VCF slice -> variation_id 441519, allele_id 435101 | |
| Clinical-action thresholds, no research boundary | P1 | Scope statement (research evidence; individual results need validated testing and clinical interpretation); "star >= 2 acceptable for clinical action" row removed; failure modes, reconciliation, thresholds, pushback reworded | text | description unchanged (not wrong) |
| chr-prefixed input annotates to `.` silently | P2 | `--rename-chrs` note in the annotate block; Common Errors rows | audit Input 2 run | |
| Invalid demo HGVS; `CLNSIGSOMATIC` | P2 | Demo `NC_000017.11:g.43106487A>C` (SKILL.md, example, usage guide); failure mode 7 cites `ONC`/`ONCREVSTAT`, `SCI`/`SCIREVSTAT` | ran: example `__main__`; live VCF header has ONC, ONCREVSTAT, SCI, SCIREVSTAT, no CLNSIGSOMATIC | |
| `parse_clnsig_conflict(None)` return type differs | cheap | Returns `{'calls': [], 'severity': None}` | ran | |

Left unfixed: none. Usage-guide myvariant prompt updated to `clinvar.rcv.review_status`.

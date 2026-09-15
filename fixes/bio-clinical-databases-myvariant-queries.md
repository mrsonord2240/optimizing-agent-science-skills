# bio-clinical-databases-myvariant-queries — fixes (2026-09-15)

Branch `fix/variant`. Verified live on 2026-09-15 against myvariant.info v1 with the myvariant 1.0.0 client (Windows venv). **myvariant.info HTTPS presented a certificate for another host on 2026-09-15 (curl and Python, Windows and WSL), so every call was verified over plain `http://myvariant.info/v1` for read-only public data.** Code in the Skill keeps `https://`. SKILL.md blocks executed verbatim from the file; example run as `__main__`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Field paths return nothing (`clinvar.clinical_significance`, `gnomad_exome.faf95`, `dbnsfp.cadd.phred`) | P1 | `clinvar.rcv.clinical_significance`, `clinvar.rcv.review_status`, `cadd.phred`; FAF95 dropped; rcv list parsed (SKILL.md, example, Lucene queries, failure mode 5, Common Errors row) | ran: BRAF V600E ClinVar, CADD 32, COSMIC populated; BRCA1 P/LP total 3,933 (hits 500 of total now returned); star >= 3: 2,156, >= 2: 2,405; hg19 CADD region 145; AlphaMissense BRAF 3,376; `/v1/metadata/fields` confirms the paths | also removed `dbnsfp.spliceai.*`: not a myvariant field (only `cadd.dst2splice`) |
| Source table misstates gnomAD version and ClinVar freshness | P1 | gnomAD 2.1.1 (GRCh37, no FAF95), ClinVar 2025-05, dbNSFP 4.8a; routes to gnomad-frequencies / clinvar-lookup; reconciliation and Common Errors rows | ran: `/v1/metadata` clinvar 2025-05, dbnsfp 4.8a, gnomad 2.1.1, dbsnp 156 | |
| Version tracking via `_meta` does not work | P1 | Versions read once from `/v1/metadata` (SKILL section rewritten, `source_versions()`, example `metadata_versions()`); description and usage guide corrected | ran: SKILL block and example `__main__` both record dbNSFP 4.8a; example no longer crashes | |
| Batch-cap claim wrong | P2 | POST over 1,000 ids returns HTTP 400; client chunks | audit Input 5 run | not re-run |
| `hg19.start` build unlabelled | P2 | Named GRCh37 in both region functions; `hg38.start` not offered | ran: `hg38.start` + `cadd.phred` 0 hits, `hg38.start` absent from `/v1/metadata/fields` | the audit's suggested hg38 alternative does not work, so it is not shown |

Left unfixed: none.

Needs attention outside the Skill: myvariant.info HTTPS certificate mismatch (2026-09-15). Until the service fixes it, the default client and every myvariant-based route (this Skill, gnomad-frequencies helper, dbsnp-queries batch) fail with CERTIFICATE_VERIFY_FAILED.

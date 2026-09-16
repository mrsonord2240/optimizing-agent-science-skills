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

## Backlog pass — 2026-09-15

Branch `fix/backlog-db`, worktree `bioSkills-wt-db`. HTTPS to myvariant.info works fine this session (2026-09-16) — no cert issue reproduced.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Item 10: state that myvariant `_id` HGVS-g is GRCh37 (chr17:g.43106487A>C returns notfound; record keyed chr17:g.41258504A>C hg19) | P2 | Added `_id` is hg19/GRCh37 bullet under "BioThings Architecture" with the confirmed 404-vs-200 example; guidance to convert to hg19 via rsID/SPDI (dbsnp-queries, clinvar-lookup, NCBI Variation Services) or query `clinvar.hg38.start`/`.end` or `dbnsfp.hg38.start`/`.end` directly; added matching Common Errors row | ran: `GET /v1/variant/chr17:g.43106487A>C` -> 404; `GET /v1/variant/chr17:g.41258504A>C` -> 200 full record; `/v1/metadata/fields` lists `clinvar.hg38.start/.end`, `dbnsfp.hg38.start/.end`, `evs.hg38.*`; `GET /v1/query?q=chrom:17 AND clinvar.hg38.start:43106487` -> 200, total 3, hits include `chr17:g.41258504A>C`; same for `dbnsfp.hg38.start` | commit `1f9f718`. **Corrects the earlier 2026-09-15 P2 row above** ("`hg38.start` not offered ... does not work"): that test used the unprefixed `hg38.start` combined with `cadd.phred` — CADD genuinely has no hg38 field, and the valid fields are namespaced (`clinvar.hg38.*`, `dbnsfp.hg38.*`, `evs.hg38.*`), not bare `hg38.start`. The namespaced fields do work. Left `find_high_cadd_in_region()` (queries `cadd.phred`) untouched — hg19-only is still correct there since CADD has no hg38 field |

| Item 11: Lucene escape advice (`chr7\:140453136`) returns 0 hits | P2 | Replaced the "Lucene escape" row (Quantitative Thresholds table) and the "0 hits" row (Common Errors table): drop the escaped-colon recommendation; recommend quoting a full HGVS id (`"chr7:g.140453136A>T"`) for an exact single-variant match, or the unescaped `chrom:pos` term for a broader positional search | ran: `GET /v1/query?q=chr7\:140453136` -> 200, total 0; `q=chr7:140453136` -> 200, total 5 (all variants at that position, includes chr7:g.140453136A>T); `q="chr7:g.140453136A>T"` -> 200, total 1 | commit `1dd9d05`. Confirms the finding's counts exactly (0/5/1). Checked `usage-guide.md` and `examples/query_myvariant.py` for the same escaped-colon pattern — neither uses it, no code change needed |

| Item 12: no consent note for participant-derived variants routed to OpenCRAVAT | P2 | Added a "Data governance:" note in the Standard Annotation Workflow section, beside the batch `getvariants` approach: batch-annotating participant-derived variants sends them to myvariant.info (a public API), needs consent and IRB/data-use approval, and PHI-sensitive work without those approvals should route to OpenCRAVAT instead | docs-only; re-read the section to confirm it reads naturally next to the existing "Offline / PHI-sensitive" decision-tree row without duplicating it | commit `d54291b`. Wording matches the "Data governance:" notes already in clinvar-lookup (905893a) and gnomad-frequencies. **myvariant-queries now complete (3/3 for this backlog pass: items 10, 11, 12)** |

Left unfixed: none (this pass, items 10-12).

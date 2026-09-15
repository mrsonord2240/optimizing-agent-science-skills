# bio-clinical-databases-dbsnp-queries — fixes (2026-09-15)

Branch `fix/variant`. Verified live on 2026-09-15 against NCBI Variation Services v0 (Windows venv); SKILL.md blocks executed verbatim from the file; example run as `__main__`; the example's myvariant path run over plain HTTP (myvariant.info HTTPS certificate mismatch, see myvariant record).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `resolve_merge_chain` KeyError on live merge schema | P1 | Follow `merged_snapshot_data.merged_into[0]`; ordered chain list (SKILL.md, example) | ran: rs630496 -> resolved 429358, chain [630496, 429358]; rs429358 1 hop | `is_withdrawn` branch not exercised (no withdrawn id tested) |
| `vcf_to_canonical_spdi` reads non-existent `data.spdi`; SKILL map chr1/chr17 only | P1 | Build SPDI from `data.seq_id/position/deleted_sequence/inserted_sequence`; full GRCh38 RefSeq map; REF-mismatch `warnings` raised | ran: 19:44908684 T>C -> NC_000019.10:44908683:T:C -> rs429358; chr17:43106487 A>C -> rs28897672; X:154536002 C>T -> rs1050828; 17:43094464 G>A -> ValueError | |
| ALFA frequencies not in RefSNP JSON | P1 | `GET /refsnp/{id}/frequency`, BioProject PRJNA507278, BioSample -> population map | ran: rs6025 Total 472,250 alleles (T 0.0237), European 364,284 | map structure checked by count arithmetic (Total = sum of 9 disjoint groups; African, Asian = their subgroups); individual labels from NCBI ALFA documentation, not fetched here (docs page is JS-rendered; freq.vcf.gz header lists ids only) |
| Example allele parser and batch table wrong | P2 | `placement_annot.seq_id_traits_by_assembly`; multi-allelic = more than one ALT; `clinvar.rcv` significance; one row per rsID, per-allele values joined with `.` placeholders | ran: rs6025, rs121913529 multi-allelic True; ClinVar significance populated; no duplicate rows | gnomAD values there are myvariant's gnomAD 2.1.1, labelled `gnomad_v2_*` |
| Merge history ignores `dbsnp1_merges` | P2 | `merged_from` from `dbsnp1_merges` (SKILL summarize, example resolve) | ran: rs429358 merged_from [630496, 61228756] | |

Left unfixed: none.

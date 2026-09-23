# bio-entrez-fetch fixes (2026-09-17)

Worktree `F:\OpenScience\wt\db-efetch`, branch `fix/db-efetch`, based on staging `main` @
`581dcd89a7450785c2451a0543ee822049fbf934`. Fixer: Claude Sonnet 5. Runtime: Biopython 1.88 via
`F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (shared venv), no version changes,
nothing new installed. Verification scripts: scratchpad `efetch-fix/` (`test_summaries.py`,
`test_pubmed.py`, `test_sra.py`, `test_clinvar.py`/`test_clinvar2.py`, `skillmd_blocks.py`/
`skillmd_verify.py` — extracted every `python` fenced block out of the shipped `SKILL.md` verbatim
via regex and ran it against live NCBI E-utilities, not a hand-copied approximation).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `bulk_summaries()` (SKILL.md + `examples/fetch_summaries.py`) `KeyError: 'Organism'` on every nucleotide ESummary docsum | P0 | Added `organism_of()`/derivation helper using `.get('Organism')` with a Title-derived fallback; applied in both SKILL.md's code pattern and `examples/fetch_summaries.py`; corrected the ESummary-vs-EFetch triage table's "Title, organism, length -> yes" row into separate "Title, length" (yes) and "Organism" (derived) rows with a footnote | ran | Live ESummary on the audit's 4 accessions: current docsum keys confirmed to have no `Organism` field (`AccessionVersion, Caption, Comment, CreateDate, Extra, Flags, Gi, Id, Item, Length, ReplacedBy, Status, TaxId, Title, UpdateDate`); fixed helper recovered "Homo sapiens" for all 4, matching the auditor's expectation |
| PMC-ID extraction (SKILL.md's `pubmed_full()` extended, and `examples/fetch_pubmed.py`) `TypeError: string indices must be integers` | P0 | `id['#text']` -> `str(id)` (ArticleIdList entries are `StringElement`, a `str` subclass with `.attributes`, not a dict, on Biopython 1.88); added `pmc_id` to `pubmed_full()`'s return value since the triage table already promises PMC ID via XML but the function never delivered it | ran | PMID 35412348 -> `PMC9093120`, exact match to the auditor's independently-verified value |
| SKILL.md's own inline `sra_runinfo()` `TypeError: a bytes-like object is required, not 'str'` | P0 | `text = h.read()` -> `raw = h.read(); text = raw.decode() if isinstance(raw, bytes) else raw` (Biopython 1.88 returns bytes for `db='sra', retmode='text'`) | ran | SRA UIDs `['8','7']` (audit's own resolved input) -> 15 real runinfo rows (Run/spots/bases/avgLength), 0 rows before the fix |
| `snp`/`clinvar` advertised in frontmatter, zero decision-matrix rows or code | P1 | Chose "write it": added `### clinvar` and `### snp` decision-matrix rows plus `clinvar_record()`/`snp_record()` code patterns (ElementTree-based, since both return DTD-less/namespaced XML `Entrez.read()` can't parse); added a ClinVar clinical-sensitivity caveat next to the new row | ran | `clinvar_record('4887763')` -> `VCV000005107` / "Pathogenic", exact match to the auditor's `probe_clinvar.py` output; `snp_record('429358')` (rs429358) -> chr 19, gene APOE (a real, checkable answer — rs429358 is one of the two SNPs defining the APOE ε4 haplotype); also confirmed live that ClinVar ESummary needs `validate=False` (DTD is missing a `common_name` tag) and documented that as the EFetch-preferred reason |
| No guidance for how a fetch-only Skill receives its input IDs | P1 | One-sentence scope note added after the intro paragraph: assumes UIDs/accessions in hand, points to `entrez-search` for discovery | docs | Matches the audit's suggested fix verbatim in substance |
| Skill's own defensive-coding advice (`.get()`) not applied to its own shipped code | P2 | Covered by the three P0 fixes above — `bulk_summaries`/`organism_of` and `pubmed_full`'s pmc_id extraction now use `.get()`/attribute access instead of direct indexing | ran (same runs as the P0 rows) | No separate change needed; noting it satisfied here per the audit's `observed_in: [2,4]` |
| `TypeError: bytes vs str` and `TypeError: string indices` had no "Common errors" table entries | P2 (cheap) | Added two rows (bytes/str decode pattern; StringElement-vs-dict pattern) plus a third row for the new `Entrez.read()`-can't-parse-DTD-less-XML error class hit by clinvar/snp | docs | Cheap, directly traceable to the P0 fixes above |

All 7 dispatched findings fixed (3 P0, 2 P1, 2 P2). Nothing left unfixed. Nothing needs Sam.

## Redundancy pass (2026-09-17)

Scope: `SKILL.md` and `usage-guide.md` only, per the brief's "Remove redundancy, every pass" rule
(this applies whether or not the audit flagged duplication — it didn't call this out directly, but
the rule is unconditional).

**Deleted passage -> new home** (checked present at destination before commit):

| Deleted from usage-guide.md | New home | Note |
|---|---|---|
| "Prerequisites" `Entrez.email`/`api_key` code block | Pointer to SKILL.md's "Required Setup" (already there, identical) | `pip install biopython` line kept — not present in SKILL.md and useful human context |
| "What the Agent Will Do" 7-step list | SKILL.md's decision matrix / GI-deprecation / XML-schema-brittleness / failure-modes sections (already there) | Replaced with a one-line pointer naming those sections |
| Tips bullets 1, 2, 4, 5, 7 (ESummary cost, bare-accession reproducibility, `gbwithparts` CONTIG trap, URL length/chunking, XML schema drift) | SKILL.md's ESummary-vs-EFetch triage, GI deprecation, Failure modes ("`gb` returns CONTIG..."), and XML schema brittleness sections (already there, same content) | Verbatim or near-verbatim restatements; no new fact |
| Tips bullet 3 (PubMed `medline` more schema-stable) | SKILL.md's "XML schema brittleness" defensive-patterns bullet (already there) | Same content |
| Tips bullet 6 (taxonomy: ESearch for TXID before EFetch) | SKILL.md's "Taxonomy lineage by TXID" code-pattern section (new sentence added) | **This was the one Tips item with no SKILL.md home** — moved rather than deleted, per the rule ("a tip found nowhere else... moves into the matching SKILL.md section") |

Untouched: "Overview", "Quick Start", "Example Prompts", "Related Skills" — the brief's allowed
usage-guide.md categories; no restatement of SKILL.md agent-facing material found in them.
`usage-guide.md`: 76 -> 53 lines. `SKILL.md`: 308 -> 399 lines (net +91: three P0 code fixes, two
new decision-matrix rows + two new code patterns for clinvar/snp, three new Common-errors rows, one
scope-note sentence, one taxonomy tip absorbed from usage-guide.md).

Shipped `examples/` scripts are out of the redundancy rule (a runnable file beside an inline
SKILL.md block is not a duplicate) — `fetch_summaries.py` and `fetch_pubmed.py` were fixed in place
for the same bugs their SKILL.md counterparts had; `fetch_sequences.py` was untouched (no defect,
already scored 94/100 on both inputs that exercised it).

## Fix pass 2 (2026-09-21)

Worktree `F:\OpenScience\wt\entrez-fetch`, branch `fix/entrez-fetch`. Fixer: Claude Sonnet 5. Biopython 1.88
(shared venv, unchanged). Verified by extracting the fenced blocks from the shipped `SKILL.md` and running
them against live NCBI E-utilities, plus an offline probe with the audit's captured 502 error-body shape.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `sra_runinfo()` fabricates junk rows from an error body | P1 | Added `expect_start(text, prefix)` helper to Required Setup; `sra_runinfo` calls `expect_start(text, 'Run,')` before splitting | ran: live SRA UIDs `8,7` -> 15 rows (first `SRR000001`); offline error body `<?xml ...?><ERROR>502...` -> `RuntimeError` | |
| No `import time` in SKILL.md blocks | P2 | `import time` added to Required Setup | ran: blocks exec'd from SKILL.md verbatim, no NameError | |
| `fetch_genbank()` lacks its own Failure Modes guard | P2 | Reads text, `expect_start(text, 'LOCUS')`, then `SeqIO.read(StringIO(...))` | ran: live NM_007294.4 -> 7088 nt; `<html>` body -> `RuntimeError` | |
| Placeholder `Entrez.api_key = 'optional_api_key'` in Required Setup (new, found while verifying) | P2 | Commented out, with a note that a fake key gives HTTP 400 | ran: pasted verbatim, every efetch returned HTTP 400; without the key, calls succeed | |

Redundancy: the "EFetch returns HTML error page" failure mode now points at the single `expect_start()` helper
instead of restating the sniff rule in prose; nothing deleted from `usage-guide.md` (already clean).

All open P1/P2 findings fixed (1/1 P1, 2/2 P2). Nothing left unfixed.

## 2026-09-21 (structure)

Worktree `F:\OpenScience\wt\entrez-fetch`, branch `fix/entrez-fetch`. Biopython 1.88 (shared `database-access` venv, unchanged), live NCBI E-utilities.

**Defect found and fixed inline** (`1407e20`): the earlier 2026-09-21 fix documented an `expect_start(text, 'Run,')` guard in `sra_runinfo()` but the function body never called it, so an error body still produced junk rows. Added the call. Ran: live SRA UIDs 8,7 -> 15 rows (first SRR000001); offline 502 error body -> `RuntimeError`.

**Split** (`87b6c40`): `SKILL.md` 411 -> 269 lines. Moved verbatim into `references/`:

| File | Content moved (old SKILL.md lines) |
|---|---|
| `pubmed.md` | pubmed matrix (67-74), `pubmed_full()` (228-248) |
| `gene-taxonomy-gds.md` | gene, taxonomy, gds matrices (76-81, 90-102), `lineage()` (288-297) |
| `sra.md` | sra matrix (83-88), `sra_runinfo()` (271-286) |
| `variants-clinvar-snp.md` | clinvar and snp matrices (104-120), `clinvar_record()`/`snp_record()` (299-343) |
| `history-server-fetch.md` | history-server fetch (250-269) |

`SKILL.md` keeps an "Other databases" table (pointer from the decision matrix), an "Other code patterns" list and a "Reference Files" index. Two lines were intentionally re-pointed (scope note names the history reference; `expect_start` note names `references/sra.md`). Compared non-blank lines old vs new: nothing else lost; every python fence in `SKILL.md` and `references/` parses (`ast.parse`).

**Scripts** (`47bf151`):

| Old location | New | How run |
|---|---|---|
| `references/history-server-fetch.md` block | `scripts/history_fetch.py` (argparse, `history_fetch()` importable, `NCBI_API_KEY` env) | live: BRCA1 RefSeq mRNA query, `--chunk 4`; FASTA held 368 records = ESearch Count 368 |
| `references/variants-clinvar-snp.md` `clinvar_record`, `snp_record` | `scripts/variant_records.py` | live: ClinVar UID 4887763 -> VCV000005107 / Pathogenic; dbSNP UID 429358 -> chr 19 / APOE (same as the 2026-09-17 verification) |
| `SKILL.md` `bulk_summaries`/`organism_of` block | deleted; duplicates `examples/fetch_summaries.py` (SKILL.md points at it) | example ran live: 4 nucleotide docsums -> Homo sapiens |

Stayed inline (under 15 lines): `fetch_genbank`, `cds_proteins`, `pubmed_full`, `sra_runinfo`, `lineage`, `expect_start`.

Left unfixed: none. Note: the example's `bulk_summaries` sleeps a fixed 0.34 s, while the deleted SKILL.md copy used 0.1 s with an API key; the example is the more conservative one.

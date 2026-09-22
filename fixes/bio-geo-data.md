# bio-geo-data — fix pass (2026-09-19)

Source audited: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:database-access/geo-data`.
Score 78/100, Beta Only, not deployable (no veto). Fixed on `fix/db-geo-data` in
`F:\OpenScience\wt\db-gd` against `mrsonord2240/bioSkills` staging `main` (4ed3e17). Commit `11ff205`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| `examples/geo_from_pubmed.py` hardcodes PMID `32228226`, labeled Blanco-Melo et al. 2020 *Cell*, but that PMID is a different paper (*Emerg Microbes Infect*) with 0 linked GDS records | P1 | Replaced with `32416070` | ran (live NCBI Entrez `esummary`/`elink`, Biopython 1.88): `32416070` = "Imbalanced Host Response to SARS-CoV-2..." *Cell*, links to `GSE147507` (110 samples); `32228226` confirmed to return 0 GDS links | matches `examples/geo_to_sra.py`'s existing `GSE147507` hardcode — the two examples are now internally consistent |
| `examples/search_geo.py`'s `detect_super_series()` raises `ValueError: Invalid mode: 'rt'` on every call (`gzip.GzipFile(..., mode='rt')` has no text mode) | P1 | Wrapped `GzipFile(mode='rb')` in `io.TextIOWrapper(..., encoding='utf-8')`, matching SKILL.md's own working `gzip.open(path, 'rt')` pattern | ran (live NCBI search + live FTP SOFT fetch for `GSE122288`/`GSE123456`): script now completes with no exception, correctly reports both as standalone Series | SKILL.md's own inline `check_super_or_sub_series()` was never broken — only the `examples/` copy |
| `examples/geo_to_sra.py`'s `gse_to_srr_entrez()` fallback raises `TypeError: a bytes-like object is required, not 'str'` on current Biopython (`efetch(..., retmode='text').read()` returns bytes) | P1 | Added `if isinstance(text, bytes): text = text.decode('utf-8')` before the string ops | ran (live NCBI + pysradb, `GSE147507`): both the pysradb path and the Entrez fallback path now complete, each returning 329 SRR runs, no crash | same bytes/str pattern as `bio-entrez-link`'s prior fix |
| SKILL.md's own worked example (`check_super_or_sub_series('GSE122288')` docstring) shows a populated `super_of` list, but `GSE122288` is a live standalone Series, not a SuperSeries | P1 | Swapped the worked example to `GSE346738`, live-confirmed a real SuperSeries of `GSE283260`/`GSE346737`; added a one-line note that SuperSeries status can drift | ran (live FTP SOFT fetch): `GSE346738` -> `{'super_of': ['GSE283260', 'GSE346737'], 'sub_of': None}`; also searched live via `Entrez.esearch(term='SuperSeries[All Fields] AND gse[Entry Type]')` to find a currently-real candidate rather than guessing | `GSE346737` (one of the two subseries) also appears in the audit's own Input 1 canonical run, independently confirmed `sub_of: 'GSE346738'` |
| Decision matrix asks "is this Affymetrix or RNA-seq" with no documented way to derive platform technology | P2 (cheap) | Added a short `gdsType`-based snippet under the decision matrix | ran (live NCBI `esummary`): `GSE147507` -> `gdsType` = "Expression profiling by high throughput sequencing" (RNA-seq); `GSE122288` -> "Methylation profiling by array" (array) | |
| `!Sample_data_processing` can be entirely absent, not just terse/inconsistent, and nothing said so | P2 (cheap) | Added a bullet to "Series matrix files" documenting the absent case and the `.get(key, [])` guard | ran (live, on cached `GSE470_series_matrix.txt.gz` per the audit env's own public-data): confirmed zero `!Sample_data_processing` lines | |
| `GDS` is overloaded between the Entrez `db='gds'` endpoint name and the `GDS` record-type prefix, undisambiguated | P2 (cheap) | Added a one-line disambiguation note under the GEO record taxonomy table | docs-only, placement verified adjacent to the taxonomy table | |

## Redundancy pass (FIX_BRIEF "remove redundancy every pass")

- `usage-guide.md`'s "Prerequisites" section duplicated SKILL.md's "Required Setup" `Entrez.email`/`api_key` snippet, except it additionally listed `pysradb` in the `pip install` line — SKILL.md's own `gse_to_srr` code pattern needs `pysradb` but "Required Setup" omitted it. Added `pysradb` to SKILL.md's "Required Setup", then replaced `usage-guide.md`'s "Prerequisites" with a pointer.
- `usage-guide.md`'s "What the Agent Will Do" (8-step workflow) was agent-facing decision-flow content that belongs in SKILL.md — moved verbatim to a new SKILL.md "## Workflow" section (after "Required Setup"); `usage-guide.md` now points to it.
- `usage-guide.md`'s "Tips" list (8 bullets) was entirely already stated in SKILL.md (SuperSeries trap, processed-vs-raw defaults, GEOparse suppl-file flakiness, GEOquery maturity, `[Entry Type]` case-sensitivity already in Common Errors, GEOmetadb deprecation, ArrayExpress->BioStudies migration, ARCHS4/recount3 already in the decision matrix) — deleted entirely, nothing moved (no non-duplicate content found).

## Left unfixed

None of the P0/P1/cheap-P2 findings were left unfixed.

Co-authored by Claude Sonnet 5.

---

## 2026-09-19 — second fix pass (re-audit found 1 remaining defect, score 84)

Re-audit source: `F:\OpenScience\audits\bio-geo-data\` (score 84, Limited Release — 1 point below
this project's core >= 85 landing bar). Fixed on `fix/db-geo-data` in `F:\OpenScience\wt\db-gd`
against commit `11ff205`. Commit `3327847`.

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| SKILL.md's own inline `check_super_or_sub_series('GSE346738')` worked example raises `UnicodeDecodeError` on default Windows Python 3.12 (cp1252 locale, no `PYTHONUTF8`): `gzip.open(path, 'rt')` has no `encoding=`, falls back to locale encoding; real GSE346738 SOFT file has genuine UTF-8 non-ASCII bytes | P1 | Added `encoding='utf-8', errors='replace'` to the `gzip.open(f'{gse}.soft.gz', 'rt', ...)` call (SKILL.md line 206) | ran (confirmed this machine's default locale is `cp1252`; ran SKILL.md's snippet copied out verbatim against live GSE346738): `{'super_of': ['GSE283260', 'GSE346737'], 'sub_of': None}`, no exception, matches documented expected output | the underlying SuperSeries claim was already true (re-auditor independently confirmed); only the code was unrunnable |
| Sibling instance of the same missing-encoding bug in `parse_series_matrix()`'s `gzip.open(path, 'rt')` (SKILL.md line 239) — not flagged by the re-audit because no cached fixture it used happened to contain non-ASCII bytes, but the same class of defect | P1 (found via brief's "grep for siblings" instruction) | Added `encoding='utf-8', errors='replace'` to this `gzip.open()` call too | ran (verbatim snippet against cached real `GSE470_series_matrix.txt.gz`): `expr.shape == (12625, 12)`, `metadata['!Series_geo_accession'] == ['GSE470']` — matches `TOOLS.md`'s recorded expected values, no regression | `pd.read_csv(f, ...)` continuing to read from the same now-encoding-safe text handle still works correctly |

Grepped all of `SKILL.md`, `usage-guide.md` and `examples/` for any other `gzip.open(..., 'rt')` /
`GzipFile(..., 'rt')` call: only the two above and the already-fixed `examples/search_geo.py`
(`GzipFile(mode='rb')` + `TextIOWrapper(encoding='utf-8', errors='replace')`, from the first pass)
exist. No other instances found.

### Left unfixed

None.

Co-authored by Claude Sonnet 5.

---

## 2026-09-21 — P2 pass and split (audit 2 P2s, Production Ready)

Worktree `F:\OpenScience\wt\database-access-geo-data`, branch `fix/database-access-geo-data`, from staging `431aa55`.
Commits: `7637eef` fix, `97008ed` redundancy, `aa0b1b3` split, `ae7abb8` scripts. Env: `database-access`
(Python 3.12.13, pandas 3.0, Biopython 1.88, pysradb 2.5.1, R 4.4.3 via `r.sh`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| No regression test guards the missing-encoding bug class | P2 | New `scripts/geo_series.py selftest`: offline, synthetic non-ASCII gz fixtures (U+0141; 0x81 is undefined in cp1252, so a cp1252 read raises) plus an `ast` check that every `gzip.open(..., 'rt')` passes `encoding=`. Fixture is asserted to fail under cp1252 first, so it is discriminating. Landed in the scripts commit (`ae7abb8`) | ran: `selftest OK`; with `encoding=` stripped from `parse_series_matrix` the selftest fails with the file/line | Synthetic fixture instead of the audit's suggested trimmed GSE283260 copy: same failure class, no network, no data to ship |
| Python/R default-encoding asymmetry on Windows undocumented | P2 | One paragraph in SKILL.md "Version Compatibility": Python default follows the locale (`cp1252` here), R was UTF-8; always pass `encoding='utf-8', errors='replace'` | ran: `locale.getpreferredencoding(False)` -> `cp1252`, `utf8_mode` 0 (Py 3.12.13); `Sys.getlocale('LC_CTYPE')` -> `English_United States.utf8` (R 4.4.3) | Stated as "checked 2026-09-21" for this machine |
| (found) `download_series_matrix()` fence raised `NameError: urllib` (never imported in that block) | P2 (correction) | Added `import urllib.request` | ran: reproduced the NameError; extracted the fence verbatim from SKILL.md, run on GSE470: `expr.shape == (12625, 12)`, `!Series_geo_accession == ['GSE470']` | Same fence later moved to `scripts/geo_series.py` |
| (found) `check_super_or_sub_series()` and `examples/search_geo.py::detect_super_series()` downloaded or read the whole SOFT family file (GSE122288: 486 MB, 76 s) although `!Series_relation` sits in the `^SERIES` header | P2 (correction) | Both now stream and stop at the first `^PLATFORM` / `^SAMPLE` | ran: `relation GSE122288` 76 s -> 5.5 s, same result; GSE346738 -> `super_of [GSE283260, GSE346737]`, GSE346737 -> `sub_of GSE346738`; `examples/search_geo.py` completes in 8 s with unchanged output | The old `break` on `^SAMPLE` alone did not help: platform tables of methylation arrays run to millions of lines |

### Redundancy pass

`usage-guide.md` was already deduplicated on 2026-09-19 (Prerequisites, Workflow, Tips); skipped. Inside SKILL.md:

| deleted passage | new home |
| --- | --- |
| Common errors row "Submitter 'normalized' matrix gives different result than paper" | Failure modes: "Series matrix is not what it appears to be" |
| Common errors row "404 on ArrayExpress URL" | Failure modes: "ArrayExpress URL rot" |
| Common errors row "GEOparse missing CEL files" | Failure modes: "GEOparse supplementary files flakey" |
| Common errors row "GEOmetadb-based pipeline missing recent series" | Failure modes: "GEOmetadb stale" |

### Split (SKILL.md 398 -> 267 lines, then 222 after scripts)

Verbatim moves, checked by multiset comparison of non-blank lines (only the six pointer-edited lines differ); all
python fences `ast.parse`, the R fence `parse()`s.

| section | new home |
| --- | --- |
| GEOparse vs GEOquery; GEOparse full Series download; R GEOquery | `references/geoparse-geoquery.md` |
| SOFT vs MINiML; GEOmetadb status; ArrayExpress -> BioStudies | `references/legacy-and-formats.md` |
| Search GEO; Link GEO Series to SRA; Find datasets by PubMed | `references/entrez-search-and-links.md` |

### scripts/

| old location | new location |
| --- | --- |
| SKILL.md "Detect SuperSeries before pulling data" fence | `scripts/geo_series.py relation <GSE>` |
| SKILL.md "Download series matrix with submitter caveat" fence | `scripts/geo_series.py matrix <GSE> [--outdir]` |
| `references/entrez-search-and-links.md` Search / SRA / PubMed fences | deleted, each duplicated an `examples/` script (`search_geo.py`, `geo_to_sra.py`, `geo_from_pubmed.py`); pointers left. All three ran live (GSE147507: 329 SRR by pysradb and by the Entrez chain; PMID 32416070 -> GSE147507) |
| GEOparse (12 lines) and GEOquery (13 lines) fences | left inline: short API illustrations, under the 15-line bar |

### Left unfixed

None. Nothing new for Sam: `examples/geo_to_sra.py` writes `<GSE>_sra_runs.txt` into the current directory when run (intended, not changed).

Co-authored by Claude Sonnet 5.

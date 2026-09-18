# bio-entrez-search — fixes (2026-09-17)

Branch `fix/db-esearch`, worktree `F:\OpenScience\wt\db-esearch`, staging base
`49aef6ad496292fcad78360ca4c4c6a7331d62ad`. Verified live 2026-09-17 against public NCBI E-utilities
with the shared venv's Biopython 1.88 (`F:\OpenScience\audit-envs\database-access\Scripts\python.exe`).
Every changed Python snippet (`examples/database_info.py`, `examples/global_query.py`) was run to
completion and its output checked against real values (real FieldList/LastUpdate for
nuccore/pubmed/sra/gds; real per-database CRISPR counts), not just exit code. No NCBI `<ERROR>` bodies
were observed on any call made during this fix (the earlier-reported outage did not recur while
verifying).

**Judgement call on EGQuery (P1):** confirmed the auditor's finding a second, independent way —
`Entrez.egquery()` raising `AttributeError` is a Biopython-side removal, and calling the underlying
`egquery.fcgi` endpoint directly with raw `urllib` is not a working substitute either: it 301-redirects
to `ext-http-eutils.linkerd.ncbi.nlm.nih.gov`, an NCBI-internal hostname that does not resolve outside
their network (checked live 2026-09-17). That rules out "write a raw-HTTP egquery()" as an option, so I
took the brief's other path: promoted the already-correct, already-verified-working
ESearch-loop-over-`CURATED_DBS` fallback (`examples/global_query.py`) to the primary documented route
in SKILL.md's decision table and usage-guide.md's worked example, and rewrote
`examples/global_query.py` so it demonstrates the `AttributeError` explicitly (matching what the
auditor's Input 6 actually ran) before falling back to the loop as the main path, rather than leaving
`egquery()` as the only top-level call.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `Entrez.egquery()` documented as core utility, doesn't exist on Biopython 1.88; breaks SKILL.md's decision table, `examples/global_query.py`, and usage-guide.md's "Cross-database discovery" prompt | P1 | SKILL.md: decision-table row now routes to the ESearch loop, with a new "Cross-database counts (EGQuery is broken)" section explaining both the Biopython and HTTP-level breakage. `examples/global_query.py` rewritten: `confirm_egquery_broken()` surfaces the `AttributeError` explicitly, `cross_db_counts()` (the old `loop_esearch_counts`) is now the primary path. usage-guide.md's worked example and Tips line updated to match. | ran: `examples/global_query.py` end-to-end, exit 0 — `Entrez.egquery() unavailable as documented: module 'Bio.Entrez' has no attribute 'egquery'`, then real per-db CRISPR counts (protein 201,718,454 ... clinvar 254) | also checked `egquery.fcgi` directly via raw `urllib`: HTTP 301 -> `ext-http-eutils.linkerd.ncbi.nlm.nih.gov` (unresolvable outside NCBI), ruling out a raw-HTTP rewrite as viable |
| EInfo `DbInfo` indexed as a dict in SKILL.md's `list_fields()` and `examples/database_info.py`'s `db_info()`; Biopython 1.88 returns a list-of-one | P1 | Both changed to index `r['DbInfo'][0]`, with a one-line comment noting the list-of-one wrapping | ran: `examples/database_info.py` end-to-end, exit 0 — real `FieldList`/`LastUpdate`/`Count` for nuccore (740,365,563 records), pubmed, sra, gds | |
| No progressive disclosure despite ~300-line SKILL.md; `examples/` never linked from SKILL.md/usage-guide.md | P2 | Declined the `references/` restructuring — out of this fix pass's scope per FIX_BRIEF.md ("restructuring beyond the redundancy rule is not in scope"). Did add the cheap, in-scope half of the finding: a "Code patterns" intro line and inline comments pointing to `examples/basic_search.py`, `examples/database_info.py`, `examples/global_query.py` | docs (cross-reference only, no runtime behavior to verify) | left unfixed by design; noted to re-auditor |
| API key documented as a hardcoded placeholder (`Entrez.api_key = 'YOUR_KEY'`) | P2 | SKILL.md's Required Setup now reads `Entrez.api_key = os.environ.get('NCBI_API_KEY')`, with a note never to hardcode a real key | ran: `import os` + the corrected setup block compiles and `os.environ.get` returns `None` when unset (Biopython treats `None` as "no key", same 3 req/sec fallback) | |
| MARCH1 worked example's "no hits" premise doesn't reproduce (live Count=702) | P2 | usage-guide.md's "Diagnosing a 'wrong count' bug" prompt softened from "returned no hits" to "returns a big pile of loosely-related hits" — the field-qualification technique (702 -> 1) is unchanged and still correct | ran: live `Entrez.esearch(db='gene', term='MARCH1 AND human')` -> Count 702, matches the new wording | |

**Checked, not a defect:** per the dispatch's warning about `entrez-fetch`'s sibling silently
fabricating rows from an `<ERROR>` body, tested whether `Bio.Entrez.read()` (used by every pattern
touched here) does the same — fed it a synthetic `<ERROR>Search Backend failed: Exception: 502 Proxy
Error</ERROR>` body and it raised `RuntimeError: Search Backend failed...` rather than returning
fabricated data. No fix needed; noted for the re-auditor as evidence, not left silent.

**Redundancy pass:** usage-guide.md's "Prerequisites" section restated SKILL.md's Required Setup code
block (`Entrez.email`/`Entrez.api_key` assignment) verbatim — trimmed to a pointer at SKILL.md's
"Required Setup" section, keeping only the human-facing content (`pip install`, why to get an API key,
the settings URL). usage-guide.md's Overview and "Cross-database discovery"/Tips lines that referenced
EGQuery as if it worked were updated to match SKILL.md rather than left to drift as a second, now-wrong
copy of the same fact.

Left unfixed: the `references/` progressive-disclosure split (P2, declined — see table above, out of
scope for this pass).

Needs Sam: nothing. All five findings addressed (four fixed, one explicitly declined with reason).

## 2026-09-17 — second fix pass (re-audit 86, Limited Release)

Branch `fix/db-esearch2`, worktree `F:\OpenScience\wt\db-esearch2`, staging base
`89269897`. Second re-audit's three P2s (`eval_report_bio-entrez-search_result.json`, 86/100). Verified
live 2026-09-17 with the shared venv's Biopython 1.88
(`F:\OpenScience\audit-envs\database-access\Scripts\python.exe`); no NCBI `<ERROR>` bodies observed
during this pass's calls.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| `CURATED_DBS` decision-table row implies exhaustive coverage; covers only 10 of NCBI's live databases, undisclosed | P2 | Decision-table question reworded to "Which of the 10 `CURATED_DBS` databases mention X?". Added a disclosure paragraph in "Cross-database counts": states 10/38 coverage and gives the one-line widen-to-all-databases snippet (`dbs=Entrez.read(Entrez.einfo())['DbList']`). usage-guide.md's Quick Start bullet and "Cross-database discovery" prompt reworded to match (no longer say "which NCBI databases", say "which of the curated/10 databases"). | ran: live `Entrez.einfo()` -> 38 databases, all 10 `CURATED_DBS` names confirmed valid live db names; ran the widen snippet against 2 of the 38 (pubmed 5,703,545; protein 18,388,431) to confirm it executes and returns real counts | figure independently reconfirmed, not taken from the audit/brief |
| No progressive disclosure; SKILL.md grew longer in the first fix pass | P2 | **Declined the `references/` split again** (out of `FIX_BRIEF.md`'s restructuring limit; not reversing the first fixer's judgement call). Did the required redundancy pass instead: collapsed 4 Failure Modes entries (Silent retmax cap, WebEnv expiration, Index lag, Organism over-expansion) that fully restated Trigger/Mechanism already given in earlier SKILL.md sections, to a one-line pointer + Fix only; moved a PMC-subset fact that existed only in usage-guide.md's Tips into SKILL.md's field-qualified-pattern table (agent-needed, was nowhere in SKILL.md); deleted usage-guide.md's entire Tips section (all 6 bullets were either now-duplicate of SKILL.md or moved into it, none were unique human-facing content) | docs (structural collapse, no runtime behavior) | **SKILL.md net +5 lines (334 -> 339)**, not shorter: the two other findings' fixes (CURATED_DBS disclosure, term-validation paragraph) add more than the collapse removes. usage-guide.md net -9 lines (74 -> 65). Declining the restructuring finding again, same reasoning as the first pass, now with the redundancy pass done and documented rather than only the cheap cross-link half |
| No input-validation guidance for term strings | P2 | Added a short paragraph after "Required Setup": term strings are URL query parameters (Biopython URL-encodes, no shell/eval risk); sanity-check length/count before large batch loops (long OR-joined term is a common HTTPError 400 cause); points to EPost chunking instead | docs (prose guidance, ties into existing "Common errors" HTTPError 400 row and EPost's 200-IDs/call limit already documented in "retmax silent caps") | |

**Found while collapsing, fixed inline:** the old "Index lag for fresh deposits" Failure Modes entry
said the indexer is "batch (Tue/Fri primary)", contradicting the "Index lag" section two screens above
it, which says the indexer "runs nightly". Could not verify NCBI's exact schedule live; dropped the
unhedged, contradicting "Tue/Fri primary" claim rather than keep two disagreeing statements, per
document doctrine (resolve on recency/support, not invention).

**Deleted passages and where the content now lives:**
- usage-guide.md Tips bullet 1 (gene-symbol/HGNC lookup) -> already stated in SKILL.md's "Query
  translation mismatch" Failure Mode; not duplicated elsewhere, deleted outright.
- usage-guide.md Tips bullet 2 ([Organism] taxonomy walk) -> already stated in SKILL.md's "Organism
  field gotcha" section; deleted outright.
- usage-guide.md Tips bullet 3 (fresh deposits/EFetch) -> already stated in SKILL.md's "Index lag"
  section; deleted outright.
- usage-guide.md Tips bullet 4 (history server for large sets) -> already stated in SKILL.md's
  "History server" section; deleted outright.
- usage-guide.md Tips bullet 5 (PMC subset `pubmed pmc[sb]`) -> did not previously exist in SKILL.md;
  moved into SKILL.md's field-qualified-pattern table, pubmed row.
- usage-guide.md Tips bullet 6 (`Entrez.egquery()` doesn't exist) -> already stated in SKILL.md's
  "Cross-database counts" section; deleted outright.
- SKILL.md Failure Modes' Trigger/Mechanism text for Silent retmax cap, WebEnv expiration, Index lag,
  Organism over-expansion -> each already stated in an earlier SKILL.md section (named inline);
  collapsed to a one-line pointer, Fix line kept.

Left unfixed: the `references/` progressive-disclosure split (P2, declined a second time — see table
above). Needs Sam: nothing.

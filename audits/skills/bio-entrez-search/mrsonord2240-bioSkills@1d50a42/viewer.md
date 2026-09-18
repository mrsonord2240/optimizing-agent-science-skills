> **Audit record for `bio-entrez-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1d50a42](https://github.com/mrsonord2240/bioSkills/tree/1d50a42db19bbfba3cfca8530ab9853cb38c409c/database-access/entrez-search) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-entrez-search (RE-AUDIT, post-fix)
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@1d50a42:database-access/entrez-search` (branch `fix/db-esearch`, worktree `F:\OpenScience\wt\db-esearch`, based on staging `main` `49aef6ad496292fcad78360ca4c4c6a7331d62ad`)
Category: Evidence Insight | Execution Mode: A (Direct) | Complexity: Complex (N=7)

This is a **re-audit** of a fixed Skill. The pre-fix report (83/100, Limited Release, no veto, no P0) is
archived at `F:\OpenScience\audits\_pre-fix-20260917d\bio-entrez-search\`. Per the dispatch, **the fix
log (`F:\optimizing-agent-science-skills\fixes\bio-entrez-search.md`) is not evidence** — every claim in
it was independently re-verified below, not trusted. All 7 pre-fix inputs are regression-tested; inputs
2, 6, and 7 use databases/terms/checks the fixer's own verification never touched, to avoid measuring
only the defects the fixer was told about.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 46 | 84 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 47 | 85 | 4/4 PASS | ✅ |
| 3 | Variant B | 39 | 49 | 88 | 3/3 PASS | ✅ |
| 4 | Edge | 39 | 50 | 89 | 4/4 PASS | ✅ |
| 5 | Stress | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 36 | 46 | 82 | 4/5 PASS | ✅ |
| 7 | Adversarial | 37 | 42 | 79 | 4/4 PASS | ✅ |

**Execution Average: 85.0 / 100**
**Assertion Pass Rate: 27/28 (96.4%)**

All scripts executed with the shared venv `F:\OpenScience\audit-envs\database-access\Scripts\python.exe`
(Biopython 1.88), against live NCBI E-utilities, `Entrez.email='audit-tooling@optimizing-agent-science-skills.local'`,
0.34s delay between calls (no API key). Scripts run from this folder's own `run\`, copied from the fix
worktree, never imported in place. `find F:/OpenScience/external/mrsonord2240__bioSkills -name __pycache__`
returned nothing (no writes into the byte-identical clone). NCBI was reachable and healthy throughout this
audit (quick status check before starting; no `<ERROR>` bodies encountered on any real call).

**Method note:** Per the dispatch's hard rule, fenced `python` code blocks were extracted
programmatically straight from the shipped `SKILL.md` (`run/extract_skill_blocks.py` → 11
`skill_block_NN.py` files) and executed via those files, not hand-copied. Inputs 1, 2, 3 (partially) use
these blocks directly.

> **Note for reviewer:** Input 6 carries the one assertion FAIL in this re-audit — not a regression of
> either original P1, but a new, narrower honesty finding surfaced by this audit's own independent
> checking (see below). Read it before the rest.

## Detailed Outputs

### Input 1 — Canonical (regression)
**Prompt:** "Search PubMed for 2024 papers on tumor-mutational-burden in non-small-cell lung cancer. Print the QueryTranslation, then return the count and first 20 PMIDs."
**Script:** `run/input1_canonical.py` (uses `run/skill_block_06.py`, extracted verbatim from SKILL.md's "Single search with explicit retmax" pattern)
**Output:**
```
WARNING: 65 matched, returning first 20; use history server for full set
Count: 65
Translation: "tumor mutational burden"[Title/Abstract] AND "non small cell lung cancer"[Title/Abstract] AND 2024/01/01:2024/12/31[Date - Publication]
Returned 20 PMIDs (capped at 20): ['39830744', '39715755', '39694414', '39673162', '39670022'] ...
ASSERT OK
```
Identical to the pre-fix run (Count=65, same translation) — confirms no regression.
**Scores:** Basic: 38/40 | Specialized: 46/60 | Total: 84/100
**Assertions:**
- [PASS] Output prints QueryTranslation for the constructed query — printed verbatim, matches pre-fix run exactly.
- [PASS] retmax cap warning issued when Count > retmax — WARNING printed (65 > 20).
- [PASS] Output does not fabricate PMIDs — 20 real, live 8-digit PMIDs returned.
- [PASS] Output stays within ESearch's stated capability (UIDs only, not full records) — no record content claimed.

### Input 2 — Variant A (new: DbInfo[0] fix generalization check)
**Prompt:** "List the searchable fields for the taxonomy and assembly databases, and tell me when each was last updated."
**Script:** `run/input2_variantA_newdb.py` (uses `run/skill_block_10.py`, extracted verbatim from SKILL.md's `list_fields()` pattern)
**Why this input:** The fixer's own verification tested nuccore/pubmed/sra/gds; the pre-fix auditor tested clinvar. This input deliberately uses **four different databases** (taxonomy, assembly, structure, biosample) to check whether the `DbInfo[0]` fix generalizes, rather than being tuned to the fixer's own four test cases.
**Output (trimmed):**
```
=== taxonomy ===
Field count: 21
=== assembly ===
Field count: 51
structure: DbInfo type = list, len = 1
  DbName=structure  Count=259356  LastUpdate=2026/09/10 04:34
biosample: DbInfo type = list, len = 1
  DbName=biosample  Count=59383983  LastUpdate=2026/09/17 07:09
ASSERT OK: DbInfo[0] fix generalizes across 4 additional databases the fixer did not test
```
**Scores:** Basic: 38/40 | Specialized: 47/60 | Total: 85/100
**Assertions:**
- [PASS] `list_fields()` as shipped in SKILL.md runs without error against taxonomy and assembly — both returned non-empty FieldList (21, 51 fields), no TypeError.
- [PASS] The `DbInfo[0]` fix generalizes to databases the fixer did not test — structure and biosample both confirmed list-of-one shape.
- [PASS] Field lists, Count, and LastUpdate are real, non-fabricated live values — structure Count=259,356; biosample Count=59,383,983.
- [PASS] No TypeError or other exception raised across any of the 4 new databases — clean execution throughout.

### Input 3 — Variant B (regression, new term)
**Prompt:** "Find every RefSeq protein for Homo sapiens. Use the history server so downstream EFetch can pull in chunks without re-sending IDs."
**Script:** `run/input3_variantB_history.py`
**Output:**
```
197929 proteins queued on history server; WebEnv len=29, QueryKey=1
ASSERT OK
```
**Scores:** Basic: 39/40 | Specialized: 49/60 | Total: 88/100
**Assertions:**
- [PASS] Count exceeds retmax non-history cap (9,999) — 197,929 > 9,999.
- [PASS] WebEnv and QueryKey both returned and non-empty.
- [PASS] No UIDs fetched directly (history-server path defers retrieval to EFetch).

### Input 4 — Edge (regression: MARCH1 wording check)
**Prompt (usage-guide.md's current worked example):** "My esearch for 'MARCH1 AND human' returns a big pile of loosely-related hits ... re-run with MARCHF1[Gene Name]."
**Script:** `run/input4_edge_march1.py`
**Why this input:** The pre-fix audit flagged the *old* usage-guide wording ("returned no hits") as factually false (live Count=702). This checks whether the *new*, softened wording matches reality.
**Output:**
```
=== Original query: MARCH1 AND human ===
Count: 702
QueryTranslation: MARCH1[All Fields] AND ("Homo sapiens"[Organism] OR human[All Fields])
=== Field-qualified retry ===
Count: 1
old usage-guide claim was "no hits" (Count==0): False
new usage-guide claim is "a big pile of loosely-related hits" (Count large, >>1): True
ASSERT OK: new wording matches live reality; old "no hits" wording would NOT have
```
**Scores:** Basic: 39/40 | Specialized: 50/60 | Total: 89/100
**Assertions:**
- [PASS] QueryTranslation printed for the original query.
- [PASS] Corrected query uses a field-qualified HGNC-permanent symbol — `MARCHF1[Gene Name]`.
- [PASS] Corrected query returns fewer, more precise hits — 1 vs 702.
- [PASS] usage-guide.md's current wording matches the live count observed — 702 is indeed "a big pile", not zero; the old wording would have failed this same assertion.

### Input 5 — Stress (regression, new terms)
**Prompt:** "Find PubMed records about 'TP53 AND colorectal cancer', then on the same WebEnv search 'review[PT] AND 2023[PDAT]'. Intersect. Also check 'colen carsinoma' for a possible misspelling."
**Script:** `run/input5_stress_chain.py`
**Output:**
```
=== Part A: history-server chained intersection ===
TP53 AND colorectal cancer: 3033
review[PT] AND 2023[PDAT]: 216862
Intersection: 15
=== Part B: spell-check ===
Original: colen carsinoma
Corrected: colon carcinoma
ASSERT OK
```
**Scores:** Basic: 37/40 | Specialized: 51/60 | Total: 88/100
**Assertions:**
- [PASS] Intersection count does not exceed either parent set — 15 ≤ 3,033 and ≤ 216,862.
- [PASS] WebEnv reused (not re-fetched) across all three ESearch calls.
- [PASS] Spell-check correction resolves the misspelling — "colen carsinoma" → "colon carcinoma".
- [PASS] All three counts and the correction are real API values.

### Input 6 — Scope Boundary (new term + independent verification of the fixer's two central claims)
**Prompt:** "I have the gene symbol PTEN. Show which NCBI databases contain records mentioning it, then drill into the gene database with a field-qualified search to get the canonical Gene UID."
**Script:** `run/input6_scope_egquery.py` (runs a copy of the shipped `examples/global_query.py`, not the pre-fix auditor's `CRISPR` or the fixer's own verification term)
**Output (trimmed):**
```
=== Step 1: confirm Entrez.egquery() unavailable, term='PTEN' ===
Entrez.egquery() unavailable as documented: module 'Bio.Entrez' has no attribute 'egquery'
=== Step 2: cross-database counts for 'PTEN' via ESearch loop ===
  nucleotide  192,099 | pmc 190,407 | protein 76,480 | pubmed 28,634 | sra 15,955
  gds 12,969 | gene 9,712 | biosample 9,359 | clinvar 4,848 | bioproject 1,221
=== Step 3: drill into gene db for canonical Gene UID ===
Gene UIDs: ['5728']
QueryTranslation: PTEN[Gene Name] AND "Homo sapiens"[Organism]

=== Independent check: does egquery.fcgi really redirect to an unresolvable host? ===
  Redirect: HTTP 301 -> https://ext-http-eutils.linkerd.ncbi.nlm.nih.gov/gquery?term=PTEN&retmode=xml
  Confirmed: ext-http-eutils.linkerd.ncbi.nlm.nih.gov does NOT resolve here ([Errno 11001] getaddrinfo failed)

=== CURATED_DBS coverage check ===
Total live Entrez databases (EInfo): 38
CURATED_DBS covers: 10 of 38
Databases NOT covered by CURATED_DBS (28): ['annotinfo', 'assembly', 'biocollections', ..., 'taxonomy']
```
**Two things verified independently here, not taken from the fix log:**
1. **The `egquery.fcgi`-is-unusable claim holds.** Not trusting the fixer's report, this re-audit made
   its own raw HTTP request (with redirects intercepted, not followed) and its own DNS resolution
   attempt: confirmed 301 → `ext-http-eutils.linkerd.ncbi.nlm.nih.gov`, and confirmed that hostname
   does not resolve from here. The "write it" vs. "repair it" judgement call was sound.
2. **New finding: `CURATED_DBS` covers only 10 of 38 live databases (26%).** SKILL.md's decision table
   still asks "Which NCBI databases mention X at all?" — the same question the old, broken `EGQuery`
   row answered exhaustively (EGQuery queried *all* databases in one call). The replacement is
   materially narrower and this is not disclosed anywhere in SKILL.md.
**Scores:** Basic: 36/40 | Specialized: 46/60 | Total: 82/100
**Assertions:**
- [PASS] `Entrez.egquery()` is attempted/demonstrated and the AttributeError is caught, not silently swallowed.
- [PASS] Fallback CURATED_DBS loop returns nonzero counts for a real gene symbol — 10/10 databases nonzero for PTEN.
- [PASS] Gene UID resolved matches the real NCBI Gene ID — UID `5728`, the real Gene ID for human PTEN.
- [PASS] The egquery.fcgi-unusable justification holds up under independent verification — 301 + non-resolution both reproduced from scratch.
- [FAIL] The decision-table question ("which NCBI databases mention X at all") matches what CURATED_DBS actually checks — it covers 10/38 (26%) with no disclosure of the narrower scope.

### Input 7 — Adversarial (new: independent verification of the `<ERROR>`-body claim)
**Prompt:** "My pipeline hit a WebEnv-expired error during today's NCBI outage. Before I trust this Skill's error handling, show me that `Bio.Entrez.read()` actually fails loudly — not silently — when NCBI returns an `<ERROR>` body, so I know I won't get fabricated results downstream."
**Script:** `run/input7_error_body.py`
**Why this input:** The dispatch specifically warned that the sibling Skill `bio-entrez-fetch` was caught
today silently fabricating four rows from exactly such an `<ERROR>` body, and that the difference was
which parser was used. The fix log claims `Bio.Entrez.read()` (used by every pattern in this Skill)
already raises `RuntimeError` and needed no fix. This input tests that claim directly rather than
trusting it.
**Output:**
```
=== Body 1: ...WebEnv not found</ERROR></eSearchResult> ===
  RuntimeError raised (expected, per fix log): WebEnv not found

=== Body 2: ...Search Backend failed: Exception: 502 Proxy Error</ERROR></eSearchResult> ===
  RuntimeError raised (expected, per fix log): Search Backend failed: Exception: 502 Proxy Error

Control: real successful ESearch parses fine, Count=23326, type=DictionaryElement
```
Both a documented WebEnv-expiration body and a body shaped exactly like today's real NCBI 502 outage
were fed through `Bio.Entrez.read()`. Both raised `RuntimeError`; neither returned parsed data, let
alone fabricated it. The control case (a real successful parse) confirms the parser isn't just
throwing on everything. **The fix log's claim is confirmed independently — this Skill does not carry
the sibling Skill's fabrication defect.**
**Scores:** Basic: 37/40 | Specialized: 42/60 | Total: 79/100
**Assertions:**
- [PASS] Feeding a documented WebEnv-expired `<ERROR>` body raises rather than returning parsed/fabricated data.
- [PASS] Feeding an outage-shaped 502 `<ERROR>` body also raises rather than silently returning empty/fabricated data.
- [PASS] The raised exception is `RuntimeError` specifically, matching the fix log's claim.
- [PASS] A real successful parse is unaffected by the same code path (control case).

## Static Evaluation Notes (Step 2, 25 criteria, re-scored from scratch against the current SKILL.md)

- **Functional Suitability (11/12):** Both pre-fix P1s confirmed fixed and generalizing beyond the fixer's own test cases. One point held back for the CURATED_DBS coverage-honesty gap (Input 6).
- **Reliability (11/12):** Failure Modes / Common Errors tables re-verified accurate against live behavior, including the `<ERROR>`-body RuntimeError path (Input 7).
- **Performance/Context (6/8):** SKILL.md grew ~300 → ~335 lines in this fix pass rather than shrinking; still no `references/` split, though `examples/*.py` are now cross-linked (previously not linked at all).
- **Agent Usability (15/16):** Decision table remains clear; CURATED_DBS gap is a minor error-prevention miss.
- **Human Usability (8/8):** MARCH1 wording now matches reality — the pre-fix P2 is closed.
- **Security (9/12):** API key now sourced from an env var with verified `None`-when-unset behavior, closing the pre-fix P2. No input-validation guidance for `term` strings (minor, unaddressed by either fix round).
- **Maintainability (9/12):** Cross-links improve testability discovery; no `references/` split.
- **Agent-Specific (19/20):** Trigger description now accurately documents the EGQuery removal; cross-links partially address progressive disclosure.

**Static Subtotal: 88/100**

## Floors Check (per `scoring_rubric.md` §5)

| Component | Value | Production floor | Limited Release floor | Met? |
|---|---|---|---|---|
| Static Score | 88 | ≥ 80 | ≥ 70 | Production ✓ |
| Execution Average | 85.0 | ≥ 85 | ≥ 75 | Production ✓ |
| Layer 1 avg (Basic) | 37.7 | ≥ 32 | ≥ 28 | Production ✓ |
| Layer 2 avg (Specialized) | 47.3 | ≥ 48 | ≥ 42 | **Production ✗ — Limited Release ✓** |
| Assertion pass rate | 96.4% | ≥ 90% | ≥ 80% | Production ✓ |

Raw Final Score (88 × 0.4 + 85.0 × 0.6 = 86.2 → **86**) falls in the Production Ready band (85–100), but
the Layer 2 (Specialized) floor of ≥48 is missed by 0.7 points (47.3). Per the rubric, **any missed floor
downgrades the grade by exactly one tier** — Production Ready → **Limited Release**. All Limited Release
floors are independently met.

## Veto Gates

**Skill Veto (Step 1):** PASS on all four dimensions (T1 Stability, T2 Contract, T3 Determinism, T4
Security) — all 7 inputs executed cleanly with real values; frontmatter complete; no eval/exec of raw
input; deterministic given live NCBI data.

**Research Veto (Step 6, Category 1 applicable):** PASS on all four dimensions — see `veto_gates` in the
JSON for details. No fabrication, no practice-boundary violations, no methodological fallacy, all
executed code ran (M4 PASS).

## Gate Re-checks (per dispatch)

- **Gate 8 (shipped-means-present):** All three files SKILL.md/usage-guide.md point at
  (`examples/basic_search.py`, `examples/database_info.py`, `examples/global_query.py`) exist in the fix
  worktree and were run from copies in this audit's `run/`. No missing primary file.
- **Gate 7 (research scope):** No diagnostic, prescriptive, or individual-patient content anywhere in
  SKILL.md, usage-guide.md, or examples/ — pure database-search tooling.

## Final Score

```
Static Score   : 88/100  × 40% = 35.2
Dynamic Score  : 85.0/100 × 60% = 51.0
FINAL SCORE    : 86 / 100
GRADE          : ✅ Limited Release (downgraded one tier from Production Ready band on the Layer 2 floor)
Deployable     : true
Veto           : PASS (no override)
```

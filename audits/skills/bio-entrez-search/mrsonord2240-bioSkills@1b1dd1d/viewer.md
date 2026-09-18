> **Audit record for `bio-entrez-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@1b1dd1d](https://github.com/mrsonord2240/bioSkills/tree/1b1dd1d7c11113e788ae408f2a8c62405b7ead71/database-access/entrez-search) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-entrez-search (second-fix-pass re-audit)

Generated: 2026-09-17
Source: `mrsonord2240/bioSkills@1b1dd1d:database-access/entrez-search` (worktree `F:\OpenScience\wt\db-esearch2`)
Prior re-audit (regression baseline): `F:\OpenScience\audits\_pre-fix-20260917e\bio-entrez-search\` — 86/100, Limited Release, deployable, no veto, no P0. Held below Production Ready by Layer-2 specialized average 47.3 against a 48 floor, tripped by undisclosed `CURATED_DBS` coverage.

This re-audit is independent: every assertion below was verified by scripts run in this session against the shipped Skill in the fix worktree, not taken from the fix log (`F:\optimizing-agent-science-skills\fixes\bio-entrez-search.md`), which is cited only for context on what changed.

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 46 | 84 | 4/4 PASS | ✅ |
| 2 | Variant A | 38 | 47 | 85 | 4/4 PASS | ✅ |
| 3 | Variant B | 39 | 49 | 88 | 3/3 PASS | ✅ |
| 4 | Edge | 39 | 50 | 89 | 4/4 PASS | ✅ |
| 5 | Stress | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 39 | 50 | 89 | 5/5 PASS | ✅ |
| 7 | Adversarial | 37 | 42 | 79 | 4/4 PASS | ✅ |
| 8 (NEW) | Scope Boundary | 38 | 48 | 86 | 5/5 PASS | ✅ |
| 9 (NEW) | Adversarial | 37 | 37 | 74 | 4/4 PASS | ⚠️ |

**Execution Average: 84.7 / 100**
**Assertion Pass Rate: 37/37 (100%)**
**Layer 1 (Basic) average: 38.0/40** — floor for Production Ready ≥32 ✓, Limited Release ≥28 ✓
**Layer 2 (Specialized) average: 46.7/60** — floor for Production Ready ≥48 ✗ (misses by 1.3), Limited Release ≥42 ✓
**Static Score: 92/100** — floor for Production Ready ≥80 ✓, Limited Release ≥70 ✓
**Execution Average floor: 84.7 < 85 (Production Ready floor) ✗**, ≥75 (Limited Release floor) ✓

Two floors miss the Production Ready bar by a small margin (Execution Avg 84.7 vs 85; Layer 2 avg 46.7 vs 48) even though the raw weighted score (88) falls in the 85–100 band — per `scoring_rubric.md` §5, a missed floor forces a one-tier downgrade regardless of raw score. **Grade: Limited Release**, same tier as the prior re-audit, now at 88 instead of 86.

The Layer-2 miss is *not* driven by a regression: inputs 1–5 and 7 are unchanged regressions with identical scores to the prior re-audit. Input 6 (the fixed CURATED_DBS wording) improved from 46→50. The two new inputs this audit added average 48 and 37 specialized — input 9 in particular is a security/injection-safety check that the Evidence-Insight rubric (built for literature search strategy) scores poorly regardless of how well the Skill performs, the same pattern the prior re-audit's own input 7 showed (42/60, its lowest).

## Note for reviewer

Check the ⚠️ row (Input 9) first — its low specialized score is a rubric-fit artifact (an injection-safety check scored against a literature-search rubric), not a Skill defect: all 4 of its assertions passed and the Skill's security claim was directly verified true.

---

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Search PubMed for 2024 papers on tumor-mutational-burden in non-small-cell lung cancer. Print the QueryTranslation, then return the count and first 20 PMIDs."
**Script:** `run/input1_canonical.py` (uses `run/skill_block_06.py`, extracted programmatically from SKILL.md)
**Output (trimmed):**
```
WARNING: 65 matched, returning first 20; use history server for full set
Count: 65
Translation: "tumor mutational burden"[Title/Abstract] AND "non small cell lung cancer"[Title/Abstract] AND 2024/01/01:2024/12/31[Date - Publication]
Returned 20 PMIDs (capped at 20): ['39830744', '39715755', '39694414', '39673162', '39670022'] ...
ASSERT OK
```
**Scores:** Basic: 38/40 | Specialized: 46/60 | Total: 84/100
**Assertions:**
- [PASS] Output prints QueryTranslation for the constructed query — printed verbatim.
- [PASS] retmax cap warning issued when Count > retmax — 65 > 20.
- [PASS] Output does not fabricate PMIDs — 20 real, live 8-digit PMIDs.
- [PASS] Output stays within ESearch's stated capability (UIDs only) — no record content claimed.

### Input 2 — Variant A
**Prompt:** "List the searchable fields for the taxonomy and assembly databases, and tell me when each was last updated."
**Script:** `run/input2_variantA_newdb.py` (uses `run/skill_block_10.py`)
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
ASSERT OK: DbInfo[0] fix generalizes across 4 additional databases
```
**Scores:** Basic: 38/40 | Specialized: 47/60 | Total: 85/100
**Assertions:** all 4 PASS — see JSON for text.

### Input 3 — Variant B
**Prompt:** "Find every RefSeq protein for Homo sapiens. Use the history server so downstream EFetch can pull in chunks."
**Script:** `run/input3_variantB_history.py`
**Output:**
```
197929 proteins queued on history server; WebEnv len=29, QueryKey=1
ASSERT OK
```
**Scores:** Basic: 39/40 | Specialized: 49/60 | Total: 88/100
**Assertions:** all 3 PASS.

### Input 4 — Edge
**Prompt:** usage-guide.md's own "wrong count" worked example (MARCH1 vs MARCHF1).
**Script:** `run/input4_edge_march1.py`
**Output:**
```
=== Original query: MARCH1 AND human ===
Count: 702
QueryTranslation: MARCH1[All Fields] AND ("Homo sapiens"[Organism] OR human[All Fields])
=== Field-qualified retry ===
Count: 1
ASSERT OK: new wording matches live reality
```
**Scores:** Basic: 39/40 | Specialized: 50/60 | Total: 89/100
**Assertions:** all 4 PASS.

### Input 5 — Stress
**Prompt:** Chained history-server intersection (TP53 AND colorectal cancer / review 2023) + spell-check.
**Script:** `run/input5_stress_chain.py`
**Output:**
```
TP53 AND colorectal cancer: 3033
review[PT] AND 2023[PDAT]: 216862
Intersection: 15
Corrected: colon carcinoma
ASSERT OK
```
**Scores:** Basic: 37/40 | Specialized: 51/60 | Total: 88/100
**Assertions:** all 4 PASS.

### Input 6 — Scope Boundary
**Prompt:** "I have the gene symbol PTEN. Show which of the curated databases contain records mentioning it, then get the canonical Gene UID." Also independently re-checks the fixer's egquery.fcgi claim and, this round, the decision-table wording fix.
**Script:** `run/input6_scope_egquery.py` (runs `global_query_copy.py`'s functions directly)
**Output (trimmed):**
```
Entrez.egquery() unavailable as documented: module 'Bio.Entrez' has no attribute 'egquery'
  nucleotide         192,099
  pmc                190,407
  ... (10/10 curated dbs nonzero)
Gene UIDs: ['5728']
  Redirect: HTTP 301 -> https://ext-http-eutils.linkerd.ncbi.nlm.nih.gov/gquery?term=PTEN&retmode=xml
  Confirmed: ext-http-eutils.linkerd.ncbi.nlm.nih.gov does NOT resolve here
```
**Scores:** Basic: 39/40 | Specialized: 50/60 | Total: 89/100
**Assertions:** 5/5 PASS. **The 5th assertion (decision-table wording matches actual CURATED_DBS scope) FAILED in the prior re-audit; it PASSES now** — SKILL.md's decision table was reworded from "Which NCBI databases mention X at all?" to "Which of the 10 CURATED_DBS databases mention X?".

### Input 7 — Adversarial
**Prompt (implicit):** verify `Bio.Entrez.read()` raises rather than silently fabricates on an `<ERROR>` body (the defect that hit sibling Skill `entrez-fetch`).
**Script:** `run/input7_error_body.py`
**Output:**
```
RuntimeError raised (expected): WebEnv not found
RuntimeError raised (expected): Search Backend failed: Exception: 502 Proxy Error
Control: real successful ESearch parses fine, Count=23326, type=DictionaryElement
```
**Scores:** Basic: 37/40 | Specialized: 42/60 | Total: 79/100
**Assertions:** all 4 PASS.

### Input 8 — Scope Boundary (NEW)
**Prompt:** "Confirm CURATED_DBS really only covers 10 of NCBI's 38 databases today, that all 10 are real live databases, and that the widen-to-all-databases snippet actually works across every database EInfo lists — not just a couple."
**Script:** `run/input8_curated_dbs_widen.py`
**Output (trimmed):**
```
Live EInfo database count: 38
CURATED_DBS entries NOT found in live EInfo list: []
All 10 CURATED_DBS names confirmed valid live databases.
CURATED_DBS covers 10/38 = 26.3% of live databases
Widen snippet ran against 38 databases in 25.3s
Succeeded on 38/38 databases; 0 raised an exception
Nonzero-count databases (32): protein 251,685 / geoprofiles 228,738 / pmc 103,670 / clinvar 85,265 / ...
ASSERT OK: widen-to-all-databases snippet ran clean across the FULL 38-database list, zero errors
```
**This is the load-bearing check for this audit.** The fixer's own verification ran the widen snippet against only 2 of the 38 databases (pubmed, protein). This audit ran it against all 38, with rate-limiting honored (25.3s for 38 calls at 0.34s spacing), and it succeeded cleanly on every one — the escape hatch the disclosure paragraph offers genuinely works, not just for the two cases spot-checked before.
**Scores:** Basic: 38/40 | Specialized: 48/60 | Total: 86/100
**Assertions:** 5/5 PASS — see JSON for text.

### Input 9 — Adversarial (NEW)
**Prompt:** "A caller passes a search term containing shell metacharacters and quotes. Confirm the Skill's new claim that this is safe (URL-encoded, no shell/eval risk) rather than trusting the prose."
**Script:** `run/input9_term_validation.py`
**Output (trimmed):**
```
Dangerous calls found: NONE
Bio/Entrez/__init__.py references urllib.parse/urlencode: True
term = "human; rm -rf / && echo pwned' OR 1=1 -- $(whoami) `id`"
percent-encoded form: human%3B+rm+-rf+%2F+%26%26+echo+pwned%27+OR+1%3D1+--+%24%28whoami%29+%60id%60
Live ESearch with malicious-looking term succeeded (no crash, no shell execution). Count=0
ASSERT OK: term is passed as a URL query parameter (percent-encoded via urllib), never shelled out or eval-ed
```
**Scores:** Basic: 37/40 | Specialized: 37/60 | Total: 74/100 (⚠️ — Evidence Insight rubric doesn't fit a security-check input well; all assertions passed)
**Assertions:** 4/4 PASS — see JSON for text.

---

## Regression checks not re-derived from the fix log

- **`Tue/Fri` indexer contradiction:** grepped both `SKILL.md` and `usage-guide.md` in the fix worktree for `tue/fri` (case-insensitive) — zero matches. The surviving "Index lag" section says "runs nightly" and the Failure Modes entry now points to it rather than restating a second, disagreeing claim.
- **PMC-subset fact migration:** `pubmed pmc[sb]` now appears in SKILL.md's field-qualified-pattern table (pubmed row) and in the "Filter properties" code example; `usage-guide.md`'s Tips section (which used to carry it) is gone entirely.
- **Line counts:** `SKILL.md` 339 lines, `usage-guide.md` 65 lines — matches the fix log's claimed net deltas (+5 / -9).
- **Filesystem check:** `find F:/OpenScience/external/mrsonord2240__bioSkills -name __pycache__` returned nothing — the external clone was not touched by this audit.

## Gate checks

- **Gate 8 (shipped-means-present):** `examples/basic_search.py`, `examples/database_info.py`, `examples/global_query.py` all exist and were run in this audit (directly, or via the copy in `run/global_query_copy.py`). PASS.
- **Gate 7 (research scope):** no output diagnoses, prescribes, or triages an individual — pure database-search tooling. PASS.

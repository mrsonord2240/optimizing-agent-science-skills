> **Audit record for `bio-entrez-search`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@581dcd8](https://github.com/mrsonord2240/bioSkills/tree/581dcd89a7450785c2451a0543ee822049fbf934/database-access/entrez-search) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-entrez-search
Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@581dcd89a7450785c2451a0543ee822049fbf934:database-access/entrez-search`
Category: Evidence Insight | Execution Mode: A (Direct — agent writes Bio.Entrez code following SKILL.md patterns; `examples/` are reference implementations, not an invokable `scripts/` CLI) | Complexity: Complex (N=7)

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical | 38 | 46 | 84 | 4/4 PASS | ✅ |
| 2 | Variant A | 30 | 43 | 73 | 3/4 PASS | ⚠️ |
| 3 | Variant B | 39 | 49 | 88 | 3/3 PASS | ✅ |
| 4 | Edge | 35 | 49 | 84 | 3/4 PASS | ✅ |
| 5 | Stress | 37 | 51 | 88 | 4/4 PASS | ✅ |
| 6 | Scope Boundary | 31 | 47 | 78 | 4/5 PASS | ✅ |
| 7 | Adversarial | 38 | 47 | 85 | 3/3 PASS | ✅ |

**Execution Average: 82.9 / 100**
**Assertion Pass Rate: 24/27 (88.9%)**

All scripts executed with the shared venv `F:\OpenScience\audit-envs\database-access\Scripts\python.exe` (Biopython 1.88), against live NCBI E-utilities, `Entrez.email='audit-tooling@optimizing-agent-science-skills.local'`, 0.34s delay between calls (no API key, per dispatch instructions). Copies run from this folder's own `run\`; the upstream clone under `F:\OpenScience\external\...\entrez-search\` was never imported or executed in place (`find ... -name __pycache__` returns nothing).

> **Note for reviewer:** Inputs 2 and 6 hit real, confirmed API-surface defects already documented in `TOOLS.md` (EInfo `DbInfo` list-indexing; `Entrez.egquery` missing on Biopython 1.88). Both were reproduced first exactly as SKILL.md/examples document them, then recovered via the Skill's own documented fallback/introspection guidance — see Detailed Outputs.

## Detailed Outputs

### Input 1 — Canonical
**Prompt:** "Search PubMed for 2024 papers on tumor-mutational-burden in non-small-cell lung cancer. Print the QueryTranslation so I can lock the exact field-qualified rewrite into my code, then return the count and first 100 PMIDs." (capped to 20 for the test)
**Script:** `run/input1_canonical.py`
**Output (trimmed):**
```
WARNING: 65 matched, returning first 20; use history server for full set
Query: tumor mutational burden[TIAB] AND non-small-cell lung cancer[TIAB] AND 2024[PDAT]
Count: 65
QueryTranslation: "tumor mutational burden"[Title/Abstract] AND "non small cell lung cancer"[Title/Abstract] AND 2024/01/01:2024/12/31[Date - Publication]
First 20 PMIDs: ['39830744', '39715755', ... '39045557']
ASSERT OK: count>0, len(ids)<=20, translation present
```
**Scores:** Basic: 38/40 | Specialized: 46/60 | Total: 84/100
**Assertions:**
- [PASS] Output prints QueryTranslation for the constructed query — printed verbatim.
- [PASS] retmax cap warning issued when Count > retmax — WARNING printed (65 > 20).
- [PASS] Output does not fabricate PMIDs — 20 real, live 8-digit PMIDs returned.
- [PASS] Output stays within ESearch's stated capability (UIDs only, not full records) — no record content claimed.

### Input 2 — Variant A
**Prompt:** "List the searchable fields for the ClinVar database, and tell me when it was last updated and how many records it has."
**Script:** `run/input2_variantA.py`
**Output (trimmed):**
```
=== Step 1: EInfo call exactly as SKILL.md documents it ===
type(r["DbInfo"]) = <class 'list'>
FAILED as documented in TOOLS.md note #2: TypeError: list indices must be integers or slices, not str

=== Step 2: corrected access -- DbInfo is a list-of-one on Biopython 1.88 ===
DbName: clinvar
Description: ClinVar Database
Count: 4563915
LastUpdate: 2026/09/14 15:01
Field count: 47
  ALL  ... UID ... FILT ... TITL ... WORD ... ORGN ... MDAT ... CHR ... GENE ... MIM
ASSERT OK (after correcting the indexing bug): DbName matches, Count>0, FieldList non-empty
```
**Scores:** Basic: 30/40 | Specialized: 43/60 | Total: 73/100
**Assertions:**
- [PASS] EInfo call for clinvar returns DbName matching 'clinvar' — after correction, matched.
- [PASS] Output does not silently swallow the DbInfo-indexing TypeError — caught and printed explicitly.
- [PASS] Field list and LastUpdate are real, non-fabricated values — Count 4,563,915; LastUpdate 2026/09/14 (live).
- [FAIL] Code as literally documented in SKILL.md/`examples/database_info.py` runs without error — confirmed TypeError on `r['DbInfo']['FieldList']` / `info["DbName"]`; both index DbInfo as a dict, but Biopython 1.88 returns a one-element list.

### Input 3 — Variant B
**Prompt:** "Find every RefSeq mRNA for Homo sapiens. The total is large — use the history server (usehistory='y') so downstream EFetch can pull in chunks without re-sending IDs."
**Script:** `run/input3_variantB.py`
**Output:**
```
197890 mRNAs queued on history server; WebEnv len=29, QueryKey=1
ASSERT OK: count exceeds 9999 (the scenario history-server is meant to solve), WebEnv/QueryKey present
```
**Scores:** Basic: 39/40 | Specialized: 49/60 | Total: 88/100
**Assertions:**
- [PASS] Count exceeds retmax non-history cap (9,999), justifying history-server use — 197,890 > 9,999.
- [PASS] WebEnv and QueryKey both returned and non-empty — confirmed.
- [PASS] No UIDs fetched directly (history-server path defers retrieval to EFetch) — retmax=0, no IdList requested.

### Input 4 — Edge
**Prompt:** "My esearch for 'MARCH1 AND human' returned no hits. Print the QueryTranslation, then re-run with the proper field-qualified form using the HGNC-permanent symbol MARCHF1." (usage-guide.md's own worked example)
**Script:** `run/input4_edge.py`
**Output:**
```
=== Original query: MARCH1 AND human ===
Count: 702
QueryTranslation: MARCH1[All Fields] AND ("Homo sapiens"[Organism] OR human[All Fields])

=== Field-qualified retry: MARCHF1[Gene Name] AND Homo sapiens[Organism] ===
Count: 1
QueryTranslation: MARCHF1[Gene Name] AND "Homo sapiens"[Organism]
IdList: ['55016']
```
**Scores:** Basic: 35/40 | Specialized: 49/60 | Total: 84/100
**Assertions:**
- [PASS] QueryTranslation printed for the original query — printed.
- [PASS] Corrected query uses a field-qualified HGNC-permanent symbol — `MARCHF1[Gene Name]`.
- [PASS] Corrected query returns fewer, more precise hits than the original — 1 vs 702.
- [FAIL] Diagnosis matches the actual live count observed — the usage-guide's premise ("no hits") does not reproduce today (live Count=702, not 0); the script doesn't flag this mismatch to the user before proceeding with the retry.

### Input 5 — Stress
**Prompt:** "Find PubMed records about 'BRCA1 AND breast cancer', then on the same WebEnv search 'review[PT] AND 2024[PDAT]'. Intersect QueryKey #1 AND #2. Also check 'breast canser' for a possible misspelling while you're at it."
**Script:** `run/input5_stress.py`
**Output:**
```
=== Part A: history-server chained intersection ===
BRCA1 AND breast cancer: 16601
review[PT] AND 2024[PDAT]: 226611
Intersection (2024 reviews about BRCA1/breast cancer): 117

=== Part B: spell-check ===
Original: breast canser
Corrected: breast cancer
ASSERT OK: intersection <= both parents; spell correction contains "cancer"
```
**Scores:** Basic: 37/40 | Specialized: 51/60 | Total: 88/100
**Assertions:**
- [PASS] Intersection count does not exceed either parent set — 117 ≤ 16,601 and ≤ 226,611.
- [PASS] WebEnv reused (not re-fetched) across all three ESearch calls — same WebEnv string passed through.
- [PASS] Spell-check correction resolves 'canser' to 'cancer' — confirmed.
- [PASS] All three counts and the correction are real API values, not fabricated — live NCBI call.

### Input 6 — Scope Boundary
**Prompt:** "I have the gene symbol DDX3X. Use EGQuery to show which NCBI databases contain records mentioning it, then drill into the gene database with a field-qualified search to get the canonical Gene UID." (usage-guide.md's own worked example)
**Script:** `run/input6_scope_boundary.py`
**Output (trimmed):**
```
=== Step 1: attempt EGQuery as SKILL.md/usage-guide.md documents ===
EGQuery FAILED as documented in TOOLS.md: AttributeError: module 'Bio.Entrez' has no attribute 'egquery'

=== Step 2: documented fallback -- loop ESearch over CURATED_DBS ===
  nucleotide 6,394 | pmc 5,638 | protein 4,655 | gene 2,818 | sra 1,496 | clinvar 1,304 | biosample 951 | pubmed 824 | gds 494 | bioproject 94

=== Step 3: drill into gene db for canonical Gene UID ===
Gene UIDs: ['1654']
QueryTranslation: DDX3X[Gene Name] AND "Homo sapiens"[Organism]
ASSERT OK: EGQuery confirmed broken as documented; fallback and drill-down both succeed.
```
**Scores:** Basic: 31/40 | Specialized: 47/60 | Total: 78/100
**Assertions:**
- [PASS] `Entrez.egquery()` call is attempted as SKILL.md documents — attempted.
- [PASS] AttributeError is caught and surfaced, not silently ignored — printed explicitly.
- [PASS] Fallback CURATED_DBS loop returns nonzero counts for a real gene — 10/10 databases nonzero.
- [PASS] Gene UID resolved for DDX3X via field-qualified query — UID `1654` (matches the real NCBI Gene ID for DDX3X).
- [FAIL] SKILL.md's own decision-table entry ("Which NCBI databases mention X at all? -> EGQuery") is runnable as documented — confirmed broken; only the fallback path (also documented, in `examples/global_query.py`) works.

### Input 7 — Adversarial
**Prompt:** "Great, that ESearch found the PMIDs and accessions I need. Now just fetch me the actual full-text abstracts and GenBank sequences for the top 5 results directly through this skill."
**Executed:** false — this tests instruction-following on an out-of-scope retrieval request, not a Bio.Entrez code path. See `run/input7_adversarial_note.md` for the full reasoning and simulated response.
**Simulated response (Mode A, following SKILL.md verbatim):** declines to fabricate record content, cites the Skill's own "ESearch returns UIDs... not records" framing, and hands the already-obtained UIDs to the documented sibling Skill `entrez-fetch` (listed under Related Skills in both SKILL.md and usage-guide.md).
**Scores:** Basic: 38/40 | Specialized: 47/60 | Total: 85/100
**Assertions:**
- [PASS] Response does not fabricate abstract text or GenBank sequence content.
- [PASS] Response identifies `entrez-fetch` (or an EFetch/ESummary call) as the correct next step.
- [PASS] Response reuses the UIDs already obtained rather than re-running ESearch.

## Static Evaluation Notes (Step 2, informing category scores)

- **Functional Suitability (9/12):** broad, accurate coverage of ESearch/EInfo/EGQuery/ESpell/history-server/retmax patterns, but two of the Skill's own copy-pasteable code patterns (EGQuery call; EInfo `DbInfo` indexing) crash as written on the currently-installed Biopython 1.88 — confirmed by direct execution, not inferred.
- **Reliability (11/12):** excellent Failure Modes and Common Errors tables, both verified accurate against live behavior (retmax cap, WebEnv expiration semantics, rate-limit table).
- **Performance/Context (6/8):** single flat SKILL.md (~300 lines) with no `references/` split; `examples/` exist but are never linked from SKILL.md or usage-guide.md.
- **Agent Usability (15/16):** decision table + Goal/Approach/Reference code-pattern structure is unusually clear and consistent.
- **Human Usability (7/8):** natural trigger language in the description; usage-guide's own worked examples cover ambiguity/typos well (though one, MARCH1, has drifted — see Input 4).
- **Security (8/12):** no credential exposure risk in practice, but the "Required Setup" snippet hardcodes `Entrez.api_key = 'YOUR_KEY'` rather than showing an env-var pattern, and no input-validation guidance is given for `term` strings.
- **Maintainability (9/12):** small reusable functions, but no `references/` modularity split despite non-trivial length.
- **Agent-Specific (17/20):** precise, well-calibrated trigger description and explicit Related Skills composability; the missing progressive-disclosure split (8.2) is the main gap.

**Static Subtotal: 82/100**

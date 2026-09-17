> **Audit record for `bio-pathway-wikipathways`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@41650aa](https://github.com/mrsonord2240/bioSkills/tree/41650aaada13fe9b267c617e40353f480740940b/pathway-analysis/wikipathways) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-17 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-pathway-wikipathways (RE-AUDIT, fixed Skill)

Generated: 2026-09-17

Source: `mrsonord2240/bioSkills@41650aa:pathway-analysis/wikipathways` (fork worktree `F:\OpenScience\wt\pw-wiki`, branch `fix/pw-wiki`)
Category: Data Analysis | Execution Mode: A (Direct — SKILL.md instructions + `examples/` reference scripts) | Complexity: Complex (N=9)
Environment: `crispr-screen-analyst` audit env — R 4.4.3 via `r.sh` (clusterProfiler 4.14.6, rWikiPathways 1.26.0, org.Hs.eg.db 3.20.0, tidyr 1.3.2). All WikiPathways calls hit the live, public, unauthenticated API/archive.

Re-auditor: independent of the auditor who wrote the pre-fix report and the fixer who made the changes.

## What changed since the pre-fix audit (92, Production Ready)

Per `F:\optimizing-agent-science-skills\fixes\bio-pathway-wikipathways.md`:
1. **P1 fix**: `downloadPathwayArchive(date='20240310', ...)`, which 404s (live archive retains ~12 months), replaced with `archive_date <- format(Sys.Date() - 60, '%Y%m10')`, plus retention-window + Zenodo-fallback documentation.
2. **Undiscovered defect exposed while verifying the P1 fix**: `examples/wikipathways_explore.R` referenced `entrez_ids`/`all_entrez`, undefined in that file. Fixed by making the script self-contained (reuses genes already fetched via `getXrefList()` earlier in the same file).
3. **P2 fix**: Common Errors table gained a row for the silent-NULL wrong-organism-string symptom.
4. **Redundancy pass** (separate commit `41650aa`): moved unique content from `usage-guide.md` into `SKILL.md`, deleted true duplicates. SKILL.md 209→250 lines, usage-guide.md 100→37 lines.

## Regression strategy for this re-audit

A `git diff d9971f6 41650aa -- pathway-analysis/wikipathways/` shows the fix touched only: the Version Compatibility install block, the "Single Most Important Modern Insight" point 1, the new "WikiPathways vs KEGG/Reactome" table, the new "Agent Workflow" section, the "Reproducible Analysis with a Dated GMT" section and its code block, the new "Understanding Results" table, one new Common Errors row, and `examples/wikipathways_explore.R`. `examples/wikipathways_ora.R` and the ORA/GSEA/universe/compareCluster/zebrafish/adversarial-symbols code blocks in SKILL.md are **byte-identical** to the pre-fix commit.

On that basis, Inputs 1, 2, 3, 5, 7 were **not re-executed** — their pre-fix run evidence is carried forward as regression evidence, justified by the diff rather than a fresh run, per the machine-sharing rule to keep runs short. Input 6 was not re-run either, but its one FAILed assertion (the doc gap) is re-checked by inspection since the fix there is documentation-only. Inputs 4, 8, 9 were **re-executed live** this pass: Input 4 is the direct regression test for the P1 fix, Input 8 is new (runs the shipped `wikipathways_explore.R` byte-for-byte, testing both fixes at once), and Input 9 is new (a targeted content-loss check on the redundancy pass).

## Summary Table

| Input | Type | Executed | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|---|
| 1 | Canonical (ORA) | carried fwd | 38 | 57 | 95 | 5/5 PASS | ✅ |
| 2 | Variant A (GSEA) | carried fwd | 37 | 59 | 96 | 5/5 PASS | ✅ |
| 3 | Edge (universe) | carried fwd | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 4 | Variant B (dated GMT, RE-RUN) | **live** | 38 | 53 | 91 | 4/5 PASS | ✅ |
| 5 | Stress (compareCluster) | carried fwd | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (zebrafish) | carried fwd + doc check | 38 | 58 | 96 | 5/5 PASS | ✅ |
| 7 | Adversarial (raw symbols) | carried fwd | 38 | 57 | 95 | 4/4 PASS | ✅ |
| 8 | **NEW**: shipped `wikipathways_explore.R` verbatim | **live** | 39 | 55 | 94 | 4/4 PASS | ✅ |
| 9 | **NEW**: redundancy-pass content-loss check | **live** | 38 | 52 | 90 | 3/4 PASS | ✅ |

**Execution Average: 94.1 / 100**
**Assertion Pass Rate: 38/40 (95.0%)**
**Static Score: 95/100** | **Final Score: 94/100 → ⭐ Production Ready, deployable**

> Reviewer note: the two open findings are both new P2s from THIS pass (Input 4's residual "computed date can still miss" gap, Input 9's one dropped Tips claim) — both pre-fix findings (P1 stale date, P2 undocumented organism error) are resolved.

---

## Live-executed inputs (full detail)

### Input 4 — Variant B: reproducible dated-GMT analysis, RE-RUN with the fixed computed-date pattern
**Prompt:** Same as pre-fix Input 4 ("Run WikiPathways enrichment but make it reproducible...").

**Code:** `run/in4_dated_gmt_computed.R` — the Skill's own current `archive_date <- format(Sys.Date() - 60, '%Y%m10')` worked example, run verbatim against the same synthetic DE data as the pre-fix report.

**Output (trimmed):**
```
computed archive_date: 20260710
trying URL 'https://data.wikipathways.org/20260710/gmt/wikipathways-20260710-gmt-Homo_sapiens.gmt'
downloaded 333 KB
downloadPathwayArchive took 0.97 s
WP554 present in computed-date archive: TRUE
WP430 present in computed-date archive: TRUE

n significant terms (computed-date archive): 14
  WP430 ... p.adjust 8.900982e-22   Count 31
  WP554 ... p.adjust 6.435188e-11   Count 17
WP554 present: TRUE
WP430 present: TRUE

--- Simulated retention-window miss (archive_date - 400 days) ---
stale simulated date: 20250810
Warning: cannot open URL '...20250810...': HTTP status was '404 Not Found'
downloadPathwayArchive ERROR (expected, simulating an unlucky computed date): cannot open URL ...
```
The fix works exactly as the fix log claims (p.adjust values match to 4 significant figures). The added probe (a date 400 days back, simulating a computed date that unluckily lands outside the window) shows the failure mode is unchanged from pre-fix — a bare 404 with no code-level recovery — it's just far less likely to occur now that the date is computed rather than frozen at a single hardcoded value from 2024.

**Scores:** Basic 38/40 | Specialized 53/60 | Total 91/100 | Assertions 4/5 PASS.

---

### Input 8 — NEW: shipped `examples/wikipathways_explore.R`, byte-for-byte, unmodified
**Why:** The pre-fix audit's strongest evidence for the P1 defect was that the shipped file itself — not just a prose example — halted with an unhandled R error. This is the direct regression test for that, and incidentally exercises the second (entrez_ids) bug fix too, since that bug is in the same file, later in the same run.

**Code:** `run/in8_explore_verbatim.sh` → `skill_copy/examples/wikipathways_explore.R`, copied unmodified from the fixed Skill folder.

**Output (trimmed):** listOrganisms/get_wp_organisms/listPathways/findPathwaysByText/getPathwayInfo/getXrefList all ran and printed live data, then:
```
trying URL 'https://data.wikipathways.org/20260710/gmt/wikipathways-20260710-gmt-Homo_sapiens.gmt'
downloaded 333 KB
          ID                Description  GeneRatio  BgRatio     p.adjust  Count
WP554  WP554     ACE inhibitor pathway     17/17   17/9028  2.731556e-51    17
WP4969 WP4969  Renin Angiotensin System... 10/17   29/9028  2.591558e-20    10
...
```
Exit code 0, no R error anywhere in the run — a clean pass where the pre-fix run of this identical file halted at the `downloadPathwayArchive` call. WP554 is the clear top hit, `p.adjust 2.7316e-51`, matching the fix log's reported `2.7e-51` exactly.

**Scores:** Basic 39/40 | Specialized 55/60 | Total 94/100 | Assertions 4/4 PASS.

---

### Input 9 — NEW: does the redundancy pass lose anything an agent needs?
**Why:** Per the dispatch, one new input must specifically test the redundancy pass (SKILL.md absorbed content from usage-guide.md; usage-guide.md dropped from 100 to 37 lines).

**Code:** `run/in9_redundancy_check.py` — 18 automated substring checks (one per row in the fix log's own deletion table) plus manual comparison of the deleted "Quick Start" one-liners against surviving Example Prompts / Decision Tree entries.

**Output (trimmed):**
```
[PASS] Prerequisites install block moved to Version Compatibility
[PASS] Internet-required conceptual bullet preserved
[PASS] CC0 / no peer review conceptual bullet preserved
[PASS] Entrez-keyed / wrong-ID-type conceptual bullet preserved
[PASS] universe=NULL inflates significance conceptual bullet preserved
[PASS] 'What the Agent Will Do' -> 'Agent Workflow' section present in SKILL.md
[PASS] 'Understanding Results' column table present in SKILL.md
[PASS] 'WikiPathways vs Other Databases' -> 'WikiPathways vs KEGG/Reactome' table present
[PASS] Tip: exact organism string via listOrganisms()/get_wp_organisms()
[PASS] Tip: pin dated GMT / report date
[PASS] Tip: format='gmt' required (default gpml)
[PASS] Tip: split term field on %
[PASS] Tip: getPathwayInfo last-edit check before trusting a hit
[PASS] Tip: PFOCR as noise-tolerant complement
[PASS] Tip: setReadable() converts Entrez to symbols
[FAIL] Tip: WikiPathways has FEWER TOTAL PATHWAYS than KEGG (quantitative claim, not just species count)
[PASS] New P2 fix: wrong-organism-string Common Errors row present
[PASS] New P1 fix: Zenodo fallback named
[PASS] New P1 fix: retention window (~12 months) stated

18/19 checks passed
```
Manual read confirms: everything an agent needs operationally (install command, ID-conversion/universe/reproducibility rules, the numbered workflow, the results-column reference, every failure-mode tip checked) is present at its claimed new home. The one genuine loss — "WikiPathways has fewer total pathways than KEGG" — was an unsourced, non-operational comparative aside; the fix log's deletion table filed it under "no unique content," but it does not actually restate anywhere. Low materiality, noted as a new P2.

The three deleted "Quick Start" one-liners were checked against surviving prompts: basic-enrichment and reproducible-analysis both survive near-verbatim in usage-guide.md's Example Prompts; the "disease pathways missing from KEGG/Reactome" one-liner is covered by SKILL.md's Decision Tree row rather than a matching prompt — coverage survives, but it moved files and changed form, which is a fair characterization of "duplicated," not a clean loss.

**Scores:** Basic 38/40 | Specialized 52/60 | Total 90/100 | Assertions 3/4 PASS.

---

## Carried-forward inputs (regression, not re-executed — see pre-fix report for full detail)

Inputs 1, 2, 3, 5, 7: code paths confirmed byte-identical to the pre-fix commit by `git diff`; pre-fix results and assertions stand unchanged. Full detail in `F:\OpenScience\audits\_pre-fix-20260917\bio-pathway-wikipathways\eval_viewer_bio-pathway-wikipathways.md`.

Input 6 (zebrafish): code path unchanged; only its assertion 4 ("SKILL.md documents what happens on an incorrect organism string") flips from the pre-fix FAIL to PASS, verified by inspection of the new Common Errors row rather than a re-run, since the change is documentation-only and does not alter the R call's live behavior.

## Zenodo fallback claim — verified live this pass
```
curl -sL -o /dev/null -w "FINAL_STATUS:%{http_code} FINAL_URL:%{url_effective}" https://zenodo.org/communities/wikipathways
FINAL_STATUS:200 FINAL_URL:https://zenodo.org/communities/wikipathways/records
```
The URL SKILL.md cites (308 redirect → 200, a real, populated Zenodo community page) is correct and live, not a dead or placeholder link.

## Recommendations
See JSON `recommendations` for full text. Both new, both P2:
- **P2** — No documented recovery path if the *computed* `archive_date` itself unexpectedly 404s (distinct from the already-documented "date deliberately older than 12 months → use Zenodo" case). Confirmed live this pass that a near-window date still fails with a bare error and no pointer to Zenodo or a wider retry window.
- **P2** — The redundancy pass dropped one unsourced, non-operational Tips claim ("WikiPathways has fewer total pathways than KEGG") with no surviving equivalent. Low materiality.

Both pre-fix findings are resolved:
- **Pre-fix P1** (stale hardcoded date, 404s) — **RESOLVED**, confirmed by live re-execution of both the SKILL.md worked example and the shipped `examples/wikipathways_explore.R`.
- **Pre-fix P2** (undocumented wrong-organism-string symptom) — **RESOLVED**, confirmed by inspection of the new Common Errors row.

## Floors check (THRESHOLD.md / scoring_rubric.md)
| Floor | Value | Core (≥85) | Supporting (≥75) |
|---|---|---|---|
| Static Score | 95 | ✓ (≥80) | ✓ (≥70) |
| Execution Average | 94.1 | ✓ (≥85) | ✓ (≥75) |
| Layer 1 avg (Basic) | ~38.1/40 | ✓ (≥32) | ✓ (≥28) |
| Layer 2 avg (Specialized) | ~56.1/60 | ✓ (≥48) | ✓ (≥42) |
| Assertion pass rate | 95.0% | ✓ (≥90%) | ✓ (≥80%) |
| **Final Score** | **94** | **✓ Production Ready (≥85)** | ✓ (≥75) |

No veto fired (Skill Veto: PASS all four; Research Veto: PASS all four). **Deployable against both the core (85) and supporting (75) floor.**

> **Audit record for `bio-microbiome-taxonomy-assignment`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a/microbiome/taxonomy-assignment) (MIT).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-taxonomy-assignment
Generated: 2026-09-19

Skill: `microbiome/taxonomy-assignment` (frontmatter name `bio-microbiome-taxonomy-assignment`)
Source: `GPTomics/bioSkills@d91ed3d563019e649dc854c56ccd62551359488a:microbiome/taxonomy-assignment`
Category: Data Analysis | Execution Mode: A | Complexity: Complex (7 inputs)

**VERDICT: Skill Veto FAIL (T3 — Result Determinism). Grade forced to ❌ Reject regardless of
numeric score. Not deployable. Needs a fix pass before re-audit.**

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (QIIME2 classify-sklearn, region-matched) | 36 | 55 | 91 | 4/4 PASS | ✅ |
| 2 | Variant A (DADA2 assignTaxonomy+addSpecies, region-matched) | 35 | 48 | 83 | 4/5 PASS | ✅ |
| 3 | Edge (full-length vs region-matched Trap-1 quantification) | 38 | 56 | 94 | 4/4 PASS | ✅ |
| 4 | Variant B (DECIPHER IdTaxa) | 24 | 40 | 64 | 2/5 PASS | ⚠️ |
| 5 | Stress (vsearch-consensus vs sklearn + organelle filter) | 36 | 55 | 91 | 5/5 PASS | ✅ |
| 6 | Scope Boundary (shotgun reads) | 38 | 55 | 93 | 3/3 PASS | ✅ |
| 7 | Adversarial (over-claiming species) | 38 | 56 | 94 | 4/4 PASS | ✅ |

**Execution Average: 87.1 / 100**
**Assertion Pass Rate: 26/30 (86.7%)**
**Static Score: 84/100** | **Final Score (diagnostic, veto overrides): 86 → forced grade ❌ Reject**

## Skill Veto (Step 1)

```
SKILL VETO — REJECTED
══════════════════════════════════
Skill: bio-microbiome-taxonomy-assignment
Reason: Failed structural redline check
T1. Stability    : PASS — 0 crashes across 7 real-tool executions once the environment was tooled
T2. Contract     : PASS — frontmatter complete (name, description, tool_type, primary_tool)
T3. Determinism  : FAIL — assignTaxonomy() (DADA2) is non-deterministic without set.seed(),
                   which SKILL.md never mentions despite explicitly naming the bootstrap method.
                   Empirically confirmed: 2 identical back-to-back runs on the same 770 real ASVs
                   differ at 15/770 (1.9%) genus calls. Confirmed fixed by set.seed(100).
T4. Security     : PASS — no eval/exec of raw strings, no credentials, no injection vectors

This skill must not be deployed. Fix T3 before resubmitting.
══════════════════════════════════
```

Per `scoring_rubric.md` §3, this hard gate forces `grade = Reject` and `deployable = false`
regardless of the numeric Final Score (86, which would otherwise be Production-Ready range). The
Static and Dynamic scores below are still reported in full because they are real, useful
diagnostic evidence for the fix pass and re-audit — not because they change the verdict.

## Environment

- Real ASVs: 770 sequences from denoising the public `moving-pictures` dataset (Caporaso et al.,
  QIIME2's own tutorial data) via `qiime dada2 denoise-single --p-trunc-len 120` in the
  `qiime2-amplicon-2024.10` WSL env — not a synthetic fixture.
- Real reference: the cached SILVA 138 QIIME2 artifacts (`silva-138-99-seqs.qza`,
  `silva-138-99-tax.qza`, 436,680 sequences). `extract-reads` (515F/806R) was re-run against the
  full reference in this audit (~28 min, 432,916 region-matched sequences), confirming the
  tooling pass's result independently.
- Practical scale compromise: `fit-classifier-naive-bayes` (QIIME2) and `LearnTaxa()` (DECIPHER)
  both **crashed the WSL VM via OOM** when run against the full 400K+/433K-sequence reference on
  this 31GB machine. Both were re-run successfully against a 60,000-sequence random subsample
  (seed 42) of the same real, region-matched extraction — still real SILVA data, not synthetic,
  just smaller than full production scale. This scale limitation is itself recorded as a P1.
- R via `rr.sh` (dada2 1.34.0, DECIPHER 3.2.0). QIIME2 2024.10.1 via
  `MSYS2_ARG_CONV_EXCL='*' wsl.exe -d science -- bash -lc '...'` in the `qiime2-amplicon-2024.10`
  env. All scripts in `run/`.

## Detailed Outputs

### Input 1 — Canonical: QIIME2 classify-sklearn, region-matched
**Prompt:** "I have 16S V4 ASVs from DADA2. Assign taxonomy with SILVA, but make sure the
classifier is matched to the V4 region rather than full-length."

**What ran:** `run/qiime2_sklearn_regionmatched.sh` (adapted to the 60k-subsample reference) —
`extract-reads` → `fit-classifier-naive-bayes` → `classify-sklearn --p-confidence 0.7` against the
real 770-ASV `rep-seqs.qza`.

**Output (real):** 653/770 (84.8%) genus-assigned, 403/770 species-labeled. Confidence range
0.7000755–0.999999999954 (min value confirms the 0.7 truncation mechanism works exactly as
documented). Example calls: `Bacteroides vulgatus` (0.716), `Streptococcus` (0.99999999989),
`Neisseria` (0.993), `Fusobacterium periodonticum` (0.859) — all real, plausible human
gut/oral/skin taxa consistent with the moving-pictures dataset's known composition.

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:** 4/4 PASS (see JSON for full text/justification)

### Input 2 — Variant A: DADA2 assignTaxonomy + addSpecies, region-matched
**Prompt:** "Run assignTaxonomy and tell me what minBoot you used, what it trades, and which ASVs
you left unassigned at genus rather than force-filling."

**What ran:** `run/assign_regionmatched.R` against `regionmatched_dada2_train.fasta` /
`regionmatched_dada2_species.fasta` (60k real region-matched SILVA subsample).

**Output (real):** minBoot=50, tryRC=TRUE: 653/770 (84.8%) genus, 117/770 left honestly NA.
`addSpecies` (exact match only): 131/770 (17.0%) species — low recall, exactly as SKILL.md
describes. Examples: `Bacteroides dorei`, `Haemophilus parainfluenzae`, `Bacteroides uniformis`.

**⚠️ This is also where the Skill Veto T3 defect was found and confirmed** (see
`run/determinism_check.R` and `run/determinism_check_seeded.R`): running the identical,
unmodified call twice back-to-back with no seed set (exactly as SKILL.md's shipped
`examples/assign_silva.R` does it) produced different genus calls for 15/770 ASVs
(`identical()==FALSE`). Re-running with `set.seed(100)` before each call made the two runs
bit-for-bit identical across all 6 ranks (`identical()==TRUE`).

**Scores:** Basic 35/40 | Specialized 48/60 | Total 83/100
**Assertions:** 4/5 PASS — 1 FAIL (determinism, see JSON)

### Input 3 — Edge: quantifying the "Trap 1" claim with real data
**Prompt:** "Classify these V4 ASVs with a full-length-trained classifier and tell me exactly how
the results differ from a region-matched one."

**What ran:** `run/assign_fulllength.R` (60k full-length SILVA subsample) vs
`run/assign_regionmatched.R` (60k region-matched subsample), same 770 real ASVs, direct
row-matched comparison.

**Output (real):** Of 770 ASVs: 580 agree, 71 both NA, **50 cases where region-matching
RECOVERED a call the full-length classifier missed**, **46 cases where the full-length classifier
OVER-CALLED relative to region-matched refusal** (i.e. fabricated a specific genus the
region-matched classifier correctly declined to assert), and **23 outright disagreements**
(different genus from each classifier). Example disagreements: full-length says `Frederiksenia`,
region-matched says `uncultured`; full-length says `Selenomonas`, region-matched says
`Erysipelotrichaceae_UCG-007`.

This is a clean, quantitative, real-data confirmation of SKILL.md's central claim: "A
full-length-trained classifier applied to a V4 read mismatches k-mer composition and both
fabricates and erases calls."

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS

### Input 4 — Variant B: DECIPHER IdTaxa
**Prompt:** "Use IDTAXA for a conservative, novelty-aware classification of these ASVs."

**What ran:** `run/decipher_idtaxa.R` — real `LearnTaxa()` (26 min on the 60k real region-matched
SILVA subsample) + real `IdTaxa()` (51 sec) against the same 770 real ASVs.

**⚠️ SKILL.md's own shipped flattening code is broken.** SKILL.md's DECIPHER section (and
`usage-guide.md`) instruct:
```r
ranks <- c('domain', 'phylum', 'class', 'order', 'family', 'genus', 'species')
taxa_idtaxa <- t(sapply(ids, function(x) {
    out <- x$taxon[match(ranks, x$rank)]
    ...
```
Run verbatim against a real `IdTaxa()` result from a `LearnTaxa()`-trained trainingSet (the only
way to build one, since SKILL.md never shows loading OR building a rank-aware pre-trained
artifact), `x$rank` is `NULL` — confirmed directly (`str(ids_result[[1]])` shows only `$taxon` and
`$confidence`, no `$rank` field). `match(ranks, NULL)` returns all-`NA`, so **every single cell of
the output table is silently NA, with no error, warning, or any indication anything went wrong.**
See `run/inspect_idtaxa.R` for the direct confirmation.

**Recovering the real result** (`run/reflatten_idtaxa.R`, positional extraction instead of
`match()` — an audit workaround, not a SKILL.md fix): 482/770 (62.6%) genus-assigned, vs DADA2
NB's 84.8% — genuinely more conservative, as SKILL.md claims. Of the 482 IdTaxa genus calls, 458
(95.0%) agree with the independent DADA2 NB call on the same ASV. 125/770 (16.2%) were refused
before genus (a real, honest "novelty-aware refusal," not a bug) — but the SKILL.md code path as
shipped would show 770/770 (100%) refused, indistinguishable from total failure, with nothing to
tell a user which is which.

**Scores:** Basic 24/40 | Specialized 40/60 | Total 64/100
**Assertions:** 2/5 PASS — 3 FAIL (see JSON: broken flattening code; no from-scratch training
guidance; failure mode absent from Common Errors table)

### Input 5 — Stress: method-disagreement analysis + organelle filtering (multi-part)
**Prompt:** "Classify my ASVs two ways — naive Bayes and vsearch alignment-consensus — and tell me
where they disagree. Then filter mitochondria/chloroplast before diversity/DA and tell me what
fraction of reads that removed."

**What ran:** `classify-consensus-vsearch` directly against the full 97MB `silva-138-99-seqs.qza`
(SKILL's own documented command, no training step) on the same 770 ASVs, compared against Input
1's region-matched `classify-sklearn` result; then `qiime taxa filter-table --p-exclude
mitochondria,chloroplast` against `table.qza`.

**Output (real):** vsearch-consensus: 699/770 (90.8%) genus-assigned. vs sklearn: 599 agree, 42
both NA, 29 sklearn-only, 75 vsearch-only, **25 outright disagreements** (e.g. `Lachnoclostridium`
vs `uncultured`, `Agathobacter` vs `Roseburia`). Organelle filter: 29/770 features removed
(770→741), 2,307/153,807 reads removed (**1.5%**) — cross-validated two ways (the QIIME2 filter's
own before/after `biom summarize-table` counts, and an independent `grep -c` of
Mitochondria/Chloroplast rows in the exported taxonomy, both giving 29). Consistent with
SKILL.md's own caveat that organelle contamination is heaviest in plant/biopsy samples, not
general human gut/skin/tongue samples (this dataset).

**Scores:** Basic 36/40 | Specialized 55/60 | Total 91/100
**Assertions:** 5/5 PASS

### Input 6 — Scope Boundary: raw shotgun reads
**Prompt:** "I have raw shotgun metagenomic reads (WGS, not amplicon) from a soil sample. Can you
use this taxonomy-assignment pipeline to classify them?"

**Output:** correctly declines, cites SKILL.md's Scope line and decision-tree row verbatim,
redirects to `metagenomics/kraken-classification` / `metagenomics/metaphlan-profiling`. Full text
at `run/input6_scope_boundary_response.md`.

**Scores:** Basic 38/40 | Specialized 55/60 | Total 93/100
**Assertions:** 3/3 PASS

### Input 7 — Adversarial: over-claiming a species ID
**Prompt:** "My classify-sklearn run returned *Enterobacter cloacae* at 99% confidence for one V4
ASV. I want to state in my manuscript that this confirms *Enterobacter cloacae* was present. Is
that justified?"

**Output:** correctly refuses, explains the confidence-within-database vs proof-of-presence
distinction and V4-region cross-species ambiguity, names SKILL.md's own "Over-reading species from
16S" failure mode, and gives a concrete path to a defensible claim (report genus; addSpecies exact
match; an alternate marker; culturing). Full text at `run/input7_adversarial_response.md`.

**Scores:** Basic 38/40 | Specialized 56/60 | Total 94/100
**Assertions:** 4/4 PASS

## Top Findings (see JSON `recommendations` for full detail)

- **[P0]** `assignTaxonomy()` is non-deterministic without `set.seed()` — fires Skill Veto T3.
  Confirmed fixable with `set.seed(100)`.
- **[P0]** DECIPHER's shipped flattening code (`match(ranks, x$rank)`) silently returns 100% NA
  against a `LearnTaxa()`-trained set, and SKILL.md never shows how to train one with rank
  metadata in the first place.
- **[P1]** No memory-budget warning for training against a full-scale SILVA/GTDB reference
  (OOM-crashed the audit VM twice).

> **Note for reviewer:** Check Input 4 (⚠️) first — it is the pattern most likely to also affect
> other Skills in this folder or corpus that use DECIPHER's `IdTaxa`/`LearnTaxa` pair.

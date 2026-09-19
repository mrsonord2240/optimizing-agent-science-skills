> **Audit record for `bio-microbiome-amplicon-processing`**
> - Skill authored by [GPTomics](https://github.com/GPTomics); audited version [mrsonord2240/bioSkills@d99180a](https://github.com/mrsonord2240/bioSkills/tree/d99180a5685df2b0c7e076077e2aa326020fc9c7/microbiome/amplicon-processing) (MIT).
> - Modified by Samuel Nord from [GPTomics/bioSkills@d91ed3d](https://github.com/GPTomics/bioSkills/tree/d91ed3d563019e649dc854c56ccd62551359488a); every change is listed in [fixes.md](fixes.md).
> - Audit method: [skill-auditor](https://github.com/aipoch/medical-research-skills/tree/f5ef65b9bea79b6dd9553f52f95b0d08f7d64d26/skill-auditor) by AIPOCH (MIT), skill-auditor@1.0.
> - Performed on 2026-09-19 by Claude (Anthropic) auditor agents, commissioned by Samuel Nord. Not reviewed or endorsed by the Skill's authors.
> - Test data are synthetic. Scripts the auditor ran are in [scripts/](scripts/); raw run outputs are not published. Local paths below refer to the auditor's workstation.

# Eval Viewer — bio-microbiome-amplicon-processing (RE-AUDIT)
Generated: 2026-09-19
Source: `mrsonord2240/bioSkills@d99180a:microbiome/amplicon-processing` (worktree `F:\OpenScience\wt\mb-ap`, branch `fix/mb-amplicon-proc`)
Prior report (pre-fix, archived): `F:\OpenScience\audits\_pre-fix-20260919\bio-microbiome-amplicon-processing\` — 87/100, Limited Release, deployable, no open P0.
Fix log (claim, not evidence): `F:\optimizing-agent-science-skills\fixes\bio-microbiome-amplicon-processing.md`
Auditor: independent re-auditor (different agent from both the original auditor and the fixer).

## Summary Table

| Input | Type | Basic /40 | Specialized /60 | Total /100 | Assertions | Status |
|---|---|---|---|---|---|---|
| 1 | Canonical (regression) | 39 | 58 | 97 | 4/4 PASS | ✅ |
| 2 | Variant A (regression) | 39 | 59 | 98 | 4/4 PASS | ✅ |
| 3 | Edge (regression) | 36 | 48 | 84 | 3/3 PASS | ⚠️ |
| 4 | Variant B (regression) | 34 | 45 | 79 | 2/3 PASS | ❌ |
| 5 | Stress (regression) | 39 | 56 | 95 | 4/4 PASS | ✅ |
| 6 | Scope Boundary (regression) | 36 | 46 | 82 | 3/3 PASS | ⚠️ |
| 7 | Adversarial (regression) | 33 | 43 | 76 | 2/3 PASS | ❌ |
| 8 | Stress (NEW, auditor) | 38 | 57 | 95 | 3/3 PASS | ✅ |
| 9 | Edge (NEW, auditor) | 39 | 58 | 97 | 3/3 PASS | ✅ |

**Execution Average: 89.2 / 100**
**Assertion Pass Rate: 28/30**

**Static score: 95/100** (up from 90/100 pre-fix)
**Final score: 92/100 — ⭐ Production Ready** (up from 87/100 — ✅ Limited Release)

> Note for reviewer: the score moved from Limited Release to Production Ready primarily because
> Input 1's core assertion — "the Skill's own documented default truncLen runs successfully... without
> modification" — flips from FAIL to PASS, and that flip is independently reproduced from scratch in
> this audit, not read off the fix log.

---

## What changed vs the pre-fix audit

`git diff 4ed3e17 d99180a -- microbiome/amplicon-processing` touches exactly 3 files (SKILL.md,
examples/dada2_workflow.R, usage-guide.md), 14 insertions / 7 deletions:

1. `truncLen=c(240,160)` (SKILL.md inline) and `truncLen=c(240,200)` (dada2_workflow.R) → both
   `c(220,200)`. A new "silent ceiling" paragraph, a Quantitative Thresholds row, and a sharpened
   Common Errors row were added explaining that `truncLen` must respect the *post-primer-trim* read
   length (~231bp/~230bp for this fixture), not the raw 250bp cycle count.
2. `library(ggplot2)` added to dada2_workflow.R (and to usage-guide.md's install line) — found during
   the fixer's own verification, not in the original audit: `ggsave()` needs it, `library(dada2)`
   alone does not re-export it.
3. Two P2s (ITS fixture, DADA2 seed/reproducibility note) deliberately left unfixed, with reasons
   given in the fix log.

---

## Detailed Outputs

### Input 1 — Canonical (regression, examples/dada2_workflow.R run VERBATIM)
**Prompt:** "Process my 16S V4 paired-end amplicon data (2 sequencing runs, 10 samples) into a
chimera-free ASV table."
**What I did:** Copied `examples/dada2_workflow.R` from the worktree byte-for-byte (`diff` confirmed
no edits), independently regenerated primer-trimmed input from `raw_reads/` using the Skill's own
`remove_primers.sh` unmodified (515F/806R, cutadapt 5.2 → confirmed 231bp F / 230bp R, 1989/1989
pairs kept for S01), split into `run1`/`run2` per `sample_metadata.csv`, then ran the script end-to-end
via `rr.sh`.
**Output:** Exit 0. No crash. `error_fit_F.png` written for both runs (ggsave worked). Console:
"reads retained after chimera removal: 99.5 %", `table(nchar(...))` → `253: 11`. Cross-checked against
`truth.tsv` by exact sequence match: **8/8 real community ASVs retained**, `Mitochondria` and
`Ralstonia` (kit_contaminant) decoys correctly present (left for decontam/taxonomy steps), `CHIMERA_1`
removed, `CHIMERA_2` survived (1/2 seeded chimeras removed — a documented consensus-bimera recall
limit, unchanged P2, not part of this fix).
**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100
**Assertions:**
- [PASS] Pipeline produces a chimera-free ASV table with a read-tracking summary
- [PASS] All real community ASVs from the input data are retained (8/8)
- [PASS] **REGRESSION FIXED** — the Skill's own documented default truncLen runs successfully without
  modification, and the shipped example does not crash (previously FAIL on both counts pre-fix)
- [PASS] Chimera removal applied exactly once, after combining per-run tables

### Input 2 — Variant A (regression, decontam)
**Prompt:** "I have negative-control (blank) samples with known DNA concentrations — which ASVs are
likely reagent contamination?"
**What I did:** Ran `decontam::isContaminant(method='combined')` on my own freshly-produced
chimera-free table (not the archived pre-fix output) using the fixture's real `is_control`/`dna_conc`
metadata (S09/S10 true blanks).
**Output:** 1/11 ASVs flagged = `ASV_true_10` (Ralstonia), exactly the fixture's designated kit
contaminant. Zero false positives.
**Scores:** Basic: 39/40 | Specialized: 59/60 | Total: 98/100
**Assertions:** 4/4 PASS (unchanged from pre-fix; this code path was untouched by the fix and behaves
identically).

### Input 3 — Edge (regression, V3-V4 merge budget)
**Prompt:** "My V3-V4 (341F/805R) run has almost no reads merging — why?"
**What I did:** No V3-V4 fixture exists in this env (unchanged); independently re-derived the Skill's
stated arithmetic.
**Output:** 500bp raw pair − (460bp amplicon + 12bp minOverlap) = 28bp slack, matching the Skill's
text exactly. This section's prose is untouched by the fix.
**Scores:** Basic: 36/40 | Specialized: 48/60 | Total: 84/100 — 3/3 PASS.

### Input 4 — Variant B (regression, ITS)
**Prompt:** "How do I process ITS2 fungal amplicons — do I still use a fixed truncLen?"
**What I did:** No ITS fixture exists (unchanged; the fixer explicitly declined to fabricate one).
Independently ran `itsxpress --help` myself (WSL science distro, `itsxpress` env, ITSxpress 2.2.0) —
did not simply trust the fix log's re-confirmation.
**Output:** `--fastq`, `--fastq2`, `--region {ITS2,ITS1,ALL}`, `--taxa` (Fungi valid), `--outfile`,
`--threads` all present and correctly spelled in real `--help` output.
**Scores:** Basic: 34/40 | Specialized: 45/60 | Total: 79/100 — 2/3 PASS (full end-to-end run still
not possible; correctly left as an open, documented P2, not silently claimed fixed).

### Input 5 — Stress (regression, primers-left-on false-chimera experiment)
**Prompt:** "My chimera rate is 30%+ — is that normal for 16S data?"
**What I did:** Independently re-ran, from scratch, the controlled comparison: same 5 samples, same
truncLen(220,200)/maxEE/truncQ, varying only whether cutadapt ran first.
**Output:** Primers removed: 0.5% chimeric (1/12 bimeras, 12017 reads). Primers left on: 31.7%
chimeric (170/403 bimeras, 11732 reads). Exact match to both the original audit and the fix log.
**Scores:** Basic: 39/40 | Specialized: 56/60 | Total: 95/100 — 4/4 PASS.

### Input 6 — Scope Boundary (regression)
**Prompt:** "Can this Skill give me a definitive species ID, and should I just switch to 97% OTUs to
be safe?"
**What I did:** Text-only inspection; this section untouched by the fix.
**Scores:** Basic: 36/40 | Specialized: 46/60 | Total: 82/100 — 3/3 PASS.

### Input 7 — Adversarial (regression)
**Prompt:** "Decontam seems complicated — can I just drop any ASV under 1% relative abundance instead?"
**What I did:** Text-only inspection plus independent sanity check against the fixture's own read
counts; decontam section untouched by this fix.
**Scores:** Basic: 33/40 | Specialized: 43/60 | Total: 76/100 — 2/3 PASS (SKILL.md still doesn't name
this shortcut explicitly — unchanged P2, out of scope for this fix).

### Input 8 — NEW (auditor-added): Determinism check
**Prompt (self-directed regression probe):** re-run the unmodified fixed pipeline twice from scratch
and diff the output.
**What I did:** Ran `examples/dada2_workflow.R` unmodified in two independent working directories from
the same primer-trimmed input, then compared `seqtab_nochim.rds` directly: `identical(dim)`,
`identical(sort(colnames))`, `identical(values)` — all TRUE. Also independently checked
`formals(learnErrors)$randomize` in the installed DADA2 1.34.0 → `FALSE` (the default), confirming —
not just trusting — the fix log's stated reason for not adding a `set.seed()` note.
**Scores:** Basic: 38/40 | Specialized: 57/60 | Total: 95/100 — 3/3 PASS.

### Input 9 — NEW (auditor-added): truncLen silent-ceiling boundary test
**Prompt (self-directed regression probe):** quantitatively test the fixed guidance's new claim at
an exact base-pair boundary, not just the specific chosen values.
**What I did:** Ran `filterAndTrim` at `truncLen=c(231,230)` (exactly the real post-cutadapt length),
`c(232,230)` (1bp over on the forward read only), and the shipped `c(220,200)` default, on the same
5-sample run.
**Output:**
```
truncLen=c(231,230) [at_ceiling]:    11974/12017 passed (99.6%)
truncLen=c(232,230) [one_over_F]:        0/12017 passed (0%) — "No reads passed the filter."
truncLen=c(220,200) [fixed_default]: 12017/12017 passed (100%)
```
This is stronger evidence than the fix log's own verification (which tested only 240 vs 220): it
proves the new "silent ceiling" ceiling is exact to the bp, and that the shipped default has real
margin rather than barely working.
**Scores:** Basic: 39/40 | Specialized: 58/60 | Total: 97/100 — 3/3 PASS.

---

## Research Veto — PASS (all four dimensions), unchanged in substance from the pre-fix audit; code
usability (M4) specifically re-affirmed with new, independent execution evidence (Inputs 1, 8, 9).

## Final Verdict

**Score: 92/100 — ⭐ Production Ready. Deployable. No open P0. No veto.**

Passes the landing bar (core ≥ 85, deployable, no open P0, no veto) with margin. Merged to staging
`main`; see fix log and this report's `meta.re_audit` block for provenance.

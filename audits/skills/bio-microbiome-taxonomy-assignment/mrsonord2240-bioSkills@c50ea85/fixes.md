# Fix: bio-microbiome-taxonomy-assignment (2026-09-19)

Audit: `F:\OpenScience\audits\bio-microbiome-taxonomy-assignment\` — 86/100 diagnostic, graded
❌ Reject on a Skill Veto (T3, determinism). Fork worktree `F:\OpenScience\wt\mb-tax`, branch
`fix/mb-taxonomy-assignment`, commit `c50ea85`.

| finding | priority | change | verified (ran/help/docs) | notes |
|---|---|---|---|---|
| `assignTaxonomy()` non-deterministic without `set.seed()` — fires Skill Veto T3 | P0 | Added `set.seed(100)` before every `assignTaxonomy()` call in SKILL.md's DADA2 section and `examples/assign_silva.R`, with a note explaining the 100-bootstrap stochasticity | ran — independently reproduced on 770 real ASVs (moving-pictures) against 2 real SILVA-138 subsamples (8k and 30k sequences, extracted directly from the cached `silva-138-99-seqs.qza`/`-tax.qza`, not WSL/qiime2): unseeded pairs differed at 26/770 and 13/770 (3.4%, 1.7%) genus calls; seeded pairs matched at genus in both runs (0/770 differing) | A small residual (1–3 cells among ~4,600 checked, at non-genus ranks) persisted even seeded in my environment (24-core multithreaded reduction), where the audit's own reference gave a fully bit-identical result. Genus — the level the veto and SKILL.md's own claims turn on — was fully reproducible in both of my independent runs. Noted in the SKILL.md comment as "reproducible at the genus rank" rather than overclaiming universal bit-identity; a user needing bitwise identity at every rank can additionally set `multithread=FALSE`. |
| DECIPHER `IdTaxa` flattening code (`x$taxon[match(ranks, x$rank)]`) silently returns 100%-NA against a `LearnTaxa()`-trained set | P0 | Replaced flattening with positional extraction (`x$taxon[-1]`, padded/truncated to the rank vector) — robust regardless of whether `LearnTaxa`'s optional `rank=` data.frame was supplied. Added a commented `LearnTaxa()` training-from-scratch example (the DECIPHER section previously only showed loading a pre-trained `.RData`, never training one). Added a Common Errors row for the all-NA symptom. | ran — against the audit's own cached real `IdTaxa()` result (`idtaxa_result.rds`, 770 real ASVs): old code reproduced exactly as the audit found (0/770 assigned at every rank, no error); new code recovers 482/770 (62.6%) genus-assigned, matching the audit's independently-verified `reflatten_idtaxa.R` result exactly | Chose fix option (b) (positional flattening) over (a) (populate `rank=`) because `LearnTaxa`'s `rank=` argument requires a 5-column Index/Name/Parent/Level/Rank data.frame that DECIPHER's own docs say is "often provided in a separate taxid file" from a database release — rarely available outside DECIPHER's own pre-built sets — confirmed via `?LearnTaxa`/`?IdTaxa`. Positional extraction is correct because `x$taxon[1]` is always `"Root"` and the rest follow taxonomy depth regardless of `rank=`. |
| No memory-budget warning for training against the full SILVA/GTDB reference (OOM-crashed the audit VM twice) | P1 | Added a MEMORY note under QIIME2 `fit-classifier-naive-bayes` (SKILL.md + `examples/assign_qiime2_region.sh`) and DECIPHER `LearnTaxa`, naming the RAM requirement and the subsampling fallback | docs — matches the audit's own account (400K+/433K-sequence full-scale attempt OOM-killed the WSL VM on a 31GB machine) | Not independently re-crashed (no reason to); took the audit's own confirmed finding as ground truth per the brief. |

## Redundancy pass (mandatory every fix, not audit-flagged)

`usage-guide.md`'s Prerequisites conceptual bullets, "What the Agent Will Do" (8-step workflow),
Tips (8 bullets), Classification Methods table, and Reference Databases table all restated facts
already stated once in SKILL.md (Single Most Important Modern Insight, Tool Taxonomy, Decision
Tree, Per-Method Failure Modes, Common Errors, Version Compatibility). Deleted from usage-guide.md;
it now keeps only Overview, Prerequisites (install commands only — these are genuinely unique to
usage-guide.md), Quick Start, Example Prompts, and Related Skills.

- The one fact from the deleted Reference Databases table not already present elsewhere (RDP as
  a legacy/historical-reproducibility database choice) was moved into SKILL.md's Decision Tree
  by Scenario table before deletion — nothing the agent needs left the Skill.
- The Classification Methods table's "IDTAXA... needs a pre-trained DECIPHER trainingSet" claim
  would have become stale after this fix (SKILL.md now shows training one from scratch); deleting
  it avoided landing a new internal contradiction.

## Left unfixed

Nothing from the audit's P0/P1 list. Did not chase the tiny residual non-determinism noted above
(1–3 non-genus cells in my own larger-scale verification runs, absent in the audit's own
verification) — it is far smaller than the veto-triggering effect, does not affect genus (the
rank SKILL.md and the veto turn on), and chasing it further would mean debugging DADA2's own
multithreaded C internals, which is out of scope for a Skill-doc fix pass.

## 2026-09-19 — second pass: sibling `IdTaxa()` non-determinism (re-audit 87, Reject — Skill Veto T3 still fired)

Re-audit (`F:\OpenScience\audits\bio-microbiome-taxonomy-assignment\eval_viewer_...md`, third
independent agent) confirmed the first pass's `assignTaxonomy()` fix and DECIPHER flattening fix
both fully held on regression, but found a bug the first pass never tested: `DECIPHER::IdTaxa()`
is itself non-deterministic without a seed, and SKILL.md's DECIPHER section never called
`set.seed()` anywhere — the same bug class as `assignTaxonomy()`, larger in magnitude (re-auditor:
33/770 and 23/770, 3.0–4.3%, genus differences across unseeded runs on the same 770 real ASVs, vs.
1.9–3.4% for the original `assignTaxonomy()` bug). Worktree `F:\OpenScience\wt\mb-tax`, branch
`fix/mb-taxonomy-assignment`, starting commit `c50ea85`, fix commit `7552317`.

| finding | priority | change | verified (ran/help/docs) | notes |
|---|---|---|---|---|
| `IdTaxa()` non-deterministic without `set.seed()` — fires Skill Veto T3 (re-audit finding) | P0 | Added `set.seed(100)` immediately before the `IdTaxa()` call in SKILL.md's DECIPHER section (one call site serves both the pre-trained-`.RData` path and the from-scratch `LearnTaxa()` path); added a matching Common Errors row | ran — reused the re-audit's cached `trainingSet.rds` (real 60K-seq region-matched SILVA-138) and the same 770 real moving-pictures ASVs; ran 3 independent seeded `IdTaxa()` runs (stricter than the re-audit's own 2-run test) in both default multithreaded (`processors=NULL`) and single-threaded (`processors=1`) configs — all 3 pairwise comparisons `identical()==TRUE` at all 7 ranks (domain..species), 0 differences anywhere, both threading modes | Same seed value/convention (`set.seed(100)`) as the first pass's `assignTaxonomy()` fix |
| `LearnTaxa()` itself is also internally stochastic (not raised by the re-audit; found while verifying the above) — its own docs: tree-descent tuning "is repeated with 100 random subsamples" | P0 | Added `set.seed(100)` before the commented `LearnTaxa()` training example, with a comment explaining why | ran — independent test on a different real data slice than the re-audit used (fresh random 5000-sequence subsample of the same SILVA-138 region-matched reference, not the re-audit's full 60K set): two unseeded `LearnTaxa()` calls on identical input produced non-identical `trainingSet` objects (`identical()==FALSE`); `set.seed()` before each call made them `identical()==TRUE`. Downstream seeded `IdTaxa()` genus calls against the two unseeded-trainingSets still matched by chance (0/770 differing) for this particular slice, but the underlying object is confirmed non-deterministic, so the seed was added defensively rather than relying on that outcome | A third sibling instance the brief warned about — caught by testing the training step in isolation rather than only re-running the re-auditor's own test |

## Redundancy pass

No new duplication introduced — the change is additive within SKILL.md's existing DECIPHER code
block and Common Errors table; `usage-guide.md` was checked and contains no DECIPHER/IdTaxa code
or claims to go stale.

## Left unfixed

Nothing. Grepped SKILL.md, usage-guide.md, and `examples/` for every other call to a stochastic
method (`assignTaxonomy` already seeded from pass 1; `classify-sklearn`, `classify-consensus-vsearch`,
`fit-classifier-naive-bayes`, `addSpecies` are all deterministic algorithms/models) — found no
further unseeded sibling instance.

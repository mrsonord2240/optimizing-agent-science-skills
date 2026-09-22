# Fix log: bio-causal-genomics-effector-gene-prioritization

2026-09-18

Source: `GPTomics/bioSkills@d91ed3d:causal-genomics/effector-gene-prioritization`.
Fixed on `fix/cg-egp` (worktree `F:\OpenScience\wt\cg-egp`), off staging `main` in
`F:\OpenScience\external\mrsonord2240__bioSkills`. Commit `f4755df` (local to that fork/branch,
not pushed/merged by this fixer per the brief).

Prior audit: `F:\optimizing-agent-science-skills\audits\skills\bio-causal-genomics-effector-gene-prioritization\GPTomics-bioSkills@d91ed3d\` (score 84, Limited Release, deployable, no veto).

| finding | priority | change | verified | notes |
| --- | --- | --- | --- | --- |
| No explicit research-only / clinical-boundary language | P1 | Added `## Scope` section to `SKILL.md`: effector-gene calls are population-level/hypothesis-generating, not individual clinical decisions; instructs redirecting patient-specific treatment questions to a clinician | Docs-only change; reviewed against the audit's Input 6 (PCSK9 inhibitor vs. statin) transcript to confirm the added language matches the correct behavior already observed | The audit's Input 6 output was already correct (base-model safety behavior); this closes the gap that `SKILL.md` itself gave the agent no instruction supporting that refusal |
| MAGMA gene-set enrichment (`--set-annot`) has an undocumented minimum-gene-count requirement | P1 | Added a note to the MAGMA pipeline section of `SKILL.md` and to `examples/magma_genebased.sh` (counts genes in `.genes.raw`, skips Step 3 automatically under 200 genes, prints why); added a `Common Errors` row | Ran / reproduced myself: real MAGMA v1.10 run on a fresh 3-gene synthetic locus (chr1 PCSK9 window, real 1000G EUR SNPs) failed Step 3 with `no input variables to analyse` (gene-set variance check fails first at this scale); this matches, and is caused by the same root issue as, the audit's own real 5-gene run which failed with `insufficient degrees of freedom to run analyses` (`audits/.../run/magma_geneset.log`, already on disk) | Both failure messages are cited in `SKILL.md` since the exact one MAGMA raises depends on gene count |
| Undocumented Windows filename mismatch between MAGMA output (`<prefix>.genes.out.txt`) and PoPS input (`<prefix>.genes.out`) | P1 | Added a note to the PoPS section of `SKILL.md` (cites `mendelian-randomization-analyst/TOOLS.md` as prior independent confirmation) and a `Common Errors` row; new `examples/pops_run.py` auto-renames before invoking `pops.py` | Ran real MAGMA -> PoPS end-to-end twice on a fresh 3-gene fixture: without the fix, `pops.py` raised `FileNotFoundError: ... 'toy_gene.genes.out'`; with the copy/rename, exit 0 and real `.preds`/`.coefs`/`.marginals` written (PCSK9 ranked correctly, though scores are non-discriminating at this toy scale, as already documented) | Also found and fixed the same bug independently inside `examples/magma_genebased.sh` itself: its own Bonferroni/top-50 steps read `.genes.out` directly and crashed on Windows before ever reaching PoPS -- not one of the 6 flagged findings, fixed inline under "fix, don't report" |
| `SKILL.md` dense/un-layered relative to its size (Algorithmic Taxonomy, Quantitative Thresholds, Per-Method Failure Modes all inline) | P1 | Split those three tables into `references/algorithmic-taxonomy.md`, `references/quantitative-thresholds.md`, `references/failure-modes.md`; `SKILL.md` now carries a short summary + pointer for each, matching the `references/` progressive-disclosure convention already used by `bio-alignment-multiple` and `bio-alignment-trimming` in the published shelf | Diffed old vs. new content by hand; every row/subsection preserved verbatim in its new file; `SKILL.md` still states the load-bearing summary inline (L2G+PoPS baseline, coloc PP.H4 >= 0.7, >= 3-of-6 concordance) so routine use doesn't require opening a reference file | Citations in the `## References` section were left in `SKILL.md` (unlike the alignment-multiple precedent) because nearly every citation is also used by sections that stayed in `SKILL.md` (Common Errors, Tool Install Notes, Reconciliation, Anticipated Reviewer Pushback) |
| Thin file-level modularity: 10+ tools described, only 2 runnable examples (MAGMA CLI, R concordance scoring); PoPS, Open Targets GraphQL, cS2G, ABC/ENCODE-rE2G prose-only | P1 | Added `examples/pops_run.py` (Windows-safe PoPS CLI wrapper, handles the filename-rename fix automatically) and `examples/opentargets_l2g_query.py` (dependency-free, stdlib-only live L2G GraphQL query) | Both actually executed. `pops_run.py`: real end-to-end run against real MAGMA output (see above). `opentargets_l2g_query.py`: three real live calls against `api.platform.opentargets.org` -- auto-discovery of a real GWAS-type `studyLocusId`, an explicit GWAS-type lookup (NFE2L3 score 0.7509), and an explicit QTL-type lookup correctly reporting no L2G predictions | cS2G and ABC/ENCODE-rE2G were left prose-only per FIX_BRIEF's "delete the claim" option is not applicable here (both are legitimately referenced with correct usage instructions, not fabricated), but writing runnable examples for them was out of scope for this dispatch (not flagged) and cS2G is a static Zenodo lookup / ABC-ENCODE-rE2G is explicitly cross-referenced to `atac-seq/enhancer-gene-linking`'s own examples, so it is not an unbacked claim |
| No bundled toy/test fixture data | P1 | Added `examples/toy_gwas_sumstats.tsv`, `examples/toy_gene_loc.txt`, `examples/toy_snp_loc.txt` (~1,800 real 1000G-EUR SNPs across 3 gene bins spanning the real PCSK9 locus, chr1:55.4-55.6Mb hg19; only the GWAS p-values are synthetic) plus `examples/make_toy_fixture.py` to regenerate/rescale | Ran the real Steps 1-2 MAGMA pipeline against the fixture (via the updated `examples/magma_genebased.sh`, fully executed end-to-end): 100% of SNPs annotated; PCSK9 correctly recovered as the top gene (Z=9.84, p=3.86e-23) against both null decoy bins | Fixture is intentionally requires a real 1000G EUR PLINK reference (as MAGMA always does; documented already) rather than shipping a synthetic LD reference, since a genuine smoke test of this pipeline needs real LD structure |

Redundancy pass (FIX_BRIEF's standing rule, not one of the 6 flagged items): `usage-guide.md`
trimmed to Overview / Prerequisites-pointer / Quick Start / Example Prompts / Related Skills.
Deleted passages and where their content now lives:
- `Prerequisites` list (inputs) -> moved verbatim into `SKILL.md`'s new `## Prerequisites` section.
- `eQTL / pQTL Panel Selection` table -> moved verbatim into `SKILL.md`'s `## Prerequisites` (agent-needed content that existed only in the guide).
- `Install` code block's MAGMA-download gotcha (redirect trap) -> merged into `SKILL.md`'s existing `## Tool Install Notes` MAGMA bullet (the rest of that block duplicated what `## Tool Install Notes` already said).
- `What the Agent Will Do` (9 steps) -> deleted; fully covered by `SKILL.md`'s Decision Tree, MAGMA/L2G/PoPS sections, Multi-Evidence Integration Framework, and Reconciliation table already.
- `Tips` (10 bullets) -> deleted; each restated a fact already in `SKILL.md` (nearest-gene 30-50%, >=3-of-6 concordance, L2G/PoPS orthogonality, tissue-first sequencing, MAGMA window choice, HLA exclusion, multi-effector loci, cS2G aggregator semantics, CRISPRi-FlowFISH as gold standard).

## Left unfixed

Nothing from the 6 flagged findings was left unfixed. Not attempted (explicitly out of this
dispatch's scope, not a flagged finding): runnable examples for cS2G lookup and ABC/ENCODE-rE2G
(cross-referenced to their own Skill, `atac-seq/enhancer-gene-linking`, which is where their
executables belong); LDSC-SEG / S-MultiXcan tissue-prioritization code path (not installed in
this shared env, and out of scope -- the audit itself scored Input 4 lower for the same reason
without treating it as a defect).

## Needs Sam

Nothing. The `references/` restructuring follows the sanctioned progressive-disclosure exception
in `FIX_BRIEF.md`, matched against the existing `bio-alignment-multiple` / `bio-alignment-trimming`
convention in `optimized-scientific-skills`.

---

## 2026-09-21

Worktree `F:\OpenScience\wt\causal-genomics-effector-gene-prioritization`, branch `fix/causal-genomics-effector-gene-prioritization`
(from staging `main` 431aa55). Commits: `5737796` fix, `bb021b8` split, `eb1b953` scripts. Audit: 3 P2s
(report under `F:\OpenScience\audits\bio-causal-genomics-effector-gene-prioritization\`). Env:
`mendelian-randomization-analyst` (R 4.4.3 via `r.sh`; `venv-pops` Python 3.12.13; MAGMA 1.10 from `tools/magma`).
None of the three findings was fixed by the 2026-09-18 pass (checked against current `examples/magma_genebased.sh`).

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| `magma_genebased.sh` Bonferroni line needs `bc`, absent from Git-for-Windows bash (printed blank) | P2 | `bc -l` -> `awk -v n=... 'BEGIN{printf "%.6g", 0.05/n}'` | Ran: whole script end-to-end on the toy fixture with real MAGMA 1.10 (bash here has no `bc`); prints `0.0166667` for 3 genes | |
| printed gene count off by one (counts `.genes.out` header) | P2 | `wc -l` -> `tail -n +2 ... \| wc -l` | Ran: same run prints "across 3 genes" (fixture has 3); `.genes.out` has 4 lines | |
| 6 of 10 V2G tools prose-only | P2 | Took "write it" for cS2G: new `examples/cs2g_lookup.py` (stdlib; reads `cS2G_1000GEUR.zip` or an extracted dir) and a `cS2G Lookup` section (now `references/cs2g-lookup.md`) | Ran on the real Zenodo 7754032 zip (95 MB, downloaded to scratchpad), zip and directory modes; rs11206509 -> PCSK9 1 (ABC), rs10788994 -> PCSK9 1, rs114983708 -> FAM87B 0.882 + PLEKHN1 0.118; cross-checked against `zcat \| awk` on the raw file; unknown rsID reported | 1 of the 6 remaining tools now runnable |
| (found while running) closing echo told users to pass `.genes.raw` as PoPS `--magma_prefix` | not flagged | wording now says pass the prefix `magma_run_gene` | Read against `pops_run.py`/`pops.py` usage in SKILL.md | fixed inline |
| (found while running) `examples/` headers cited SKILL.md sections that moved | not flagged | repointed to `references/pops.md`, `references/opentargets-l2g.md`, `references/failure-modes.md` | grep | |
| (found while running) `concordance` R block: an unavailable stream (NA) made the whole row NA, so `filter(concordance >= 3)` silently dropped the gene and the tier fell to `associational_only` | not flagged | NA counts as not passed (`coalesce`); new `n_streams_available` column | Ran the script on a 6-row synthetic table incl. an all-NA row: tiers as expected (6/6 near_certain, 4 with 1 stream missing, all-NA row kept) | matches SKILL.md's own "report per-stream availability" instruction |

### Left unfixed

- FUMA: web platform, account-gated (registration) and server-side; there is nothing to execute locally, and the Skill already says so.
- DEPICT: Java tool plus a large data bundle (`perslab/depict`), not on this machine; FIX_BRIEF allows an install only for public tools the tooling pass missed, and the data bundle makes this a multi-GB install, so no smoke test could run. Claim kept (legacy method, install line present).
- INQUISIT: a method from Fachal 2020's supplementary material, not a released tool; no code exists to run. Claim kept as a pointer to the paper.
- FLAMES: the Skill itself gives no install path ("check the publication's GitHub"), and it needs trained models and their inputs; not installed here.
- ABC / ENCODE-rE2G: cross-referenced to `atac-seq/enhancer-gene-linking`, which owns their runnable examples (the auditor also called this reasonable).

### Redundancy pass

`usage-guide.md` was already reduced to overview, quick start, example prompts and related Skills on 2026-09-18; nothing left to remove. Skipped.

### Split (SKILL.md 413 -> 295 -> 274 lines)

The 2026-09-18 pass had already moved taxonomy, thresholds and failure modes to `references/`. After the cS2G addition SKILL.md was 413 lines, so the four method blocks moved verbatim. No non-blank line lost (multiset comparison: only the four lines that received a `references/` pointer differ); the python fence ast-parses, the bash fences pass `bash -n`.

| old location (SKILL.md) | new home |
| --- | --- |
| `## MAGMA Gene-Based and Gene-Set Pipeline` | `references/magma-gene-based.md` |
| `## Open Targets L2G via GraphQL` (incl. Platform vs Genetics subsection) | `references/opentargets-l2g.md` |
| `## PoPS Polygenic Priority Score` | `references/pops.md` |
| `## cS2G Lookup` | `references/cs2g-lookup.md` |

SKILL.md keeps a "Reference Files" index, decision-tree pointers on the L2G / MAGMA / PoPS rows, and repointed Common Errors rows.

### Scripts (runnable code out of SKILL.md)

| old location | script path | run |
| --- | --- | --- |
| SKILL.md concordance-scoring R block (29 lines) | `scripts/concordance_scoring.R` (input TSV and output prefix as arguments; NA handling and `n_streams_available` added, see table) | Ran via `r.sh`, dplyr, assertions on tiers/row count |
| `references/magma-gene-based.md` three-step MAGMA bash block | not moved: duplicated `examples/magma_genebased.sh`; copy deleted and replaced by a pointer | example ran end to end with MAGMA 1.10 |

Kept inline (short or API-shape illustrations): the two GraphQL queries, the 8-line Python request/`json_normalize` fragment, the 11-line PoPS invocation (wrapped by `examples/pops_run.py`).

### Needs Sam

Nothing.

---

## 2026-09-21 -- final pass, Phase 1

Worktree `F:\OpenScience\wt\causal-genomics-effector-gene-prioritization`, branch
`fix/causal-genomics-effector-gene-prioritization`. Same agent fixes and will audit (see
`process/FINAL_PASS_BRIEF.md`); this entry is Phase 1 (fix) only.

Read the "Left unfixed" list above (2026-09-21 entry) and re-checked each against this session's
broader install permission:

| finding | priority | change | verified (ran / help / docs) | notes |
| --- | --- | --- | --- | --- |
| FLAMES had no runnable example ("check the publication's GitHub for the current install path") | P1 (missing referenced executable) | Installed `Marijn-Schipper/FLAMES` (HEAD `159e83a`, v1.1.3) + a new `flames-py38` micromamba env + the 1.7 GB Zenodo annotation bundle (record 12635505); added `references/flames.md`, updated the `Tool Install Notes` bullet, `Reference Files` index, and the FLAMES row in `references/algorithmic-taxonomy.md` | Ran: `FLAMES.py annotate` + `FLAMES.py FLAMES` end to end on FLAMES' own bundled 4-locus dizygotic-twinning example data; correctly recovers `GNRH1`/`FSHB`/`SMAD3`/`ZFPM1` (the reproductive-hormone/TGF-beta genes, precision 0.88/0.87/0.95/0.98) over other locus candidates | Env details in `mendelian-randomization-analyst/TOOLS.md`, "Added 2026-09-21 ... FLAMES" |
| `examples/multi_evidence_integration.R` (upstream-original, orphaned after the 2026-09-21 `scripts/` split) duplicated `scripts/concordance_scoring.R` and still carried the pre-fix NA-handling bug the split already fixed | P2 (dedup) | Deleted `examples/multi_evidence_integration.R` | Confirmed nothing in `SKILL.md`/`usage-guide.md`/`references/` referenced it (grep); its two extra outputs (per-locus winner, L2G-vs-PoPS flag on a `pops_score` column) are not part of `concordance_scoring.R`'s documented/tested input schema | |

Re-ran (not previously flagged as needing it, but "walk every runnable block" per `FINAL_PASS_BRIEF.md`):
`magma_genebased.sh`, `pops_run.py` (this time against PoPS' own bundled real genome-wide
`PASS_Schizophrenia` example -- 18,384 genes, real non-degenerate score distribution, stronger evidence
than the toy locus-scale run previously on record), `cs2g_lookup.py` (fresh Zenodo download),
`concordance_scoring.R` (fresh synthetic NA-inclusive table), `opentargets_l2g_query.py` (live API).
All still produce the results already on record; no version drift found.

### Left unfixed (checkpoint, needs Sam's call)

- FUMA: web platform, registration-gated; needs a FUMA account/token to test live. Full detail:
  `F:\OpenScience\audits\_final_pass\bio-causal-genomics-effector-gene-prioritization\CHECKPOINT.md`.
- DEPICT: legacy (2015) Java+Python tool needing a 2.3-4.3 GB data bundle; not attempted this session
  (judged lower value than FLAMES for the time budget; Skill's own taxonomy already flags it as
  superseded). Needs a decision: invest a future pass, or downgrade to a citation-only pointer.
- INQUISIT: no released software exists (paper-supplementary-methods only) -- not blocked, just
  nothing to install; `SKILL.md` already frames it correctly as a pointer to the paper.

### Needs Sam

Whether DEPICT's legacy install (2.3-4.3 GB) is worth a future pass, or the claim should be downgraded
to a citation-only pointer the way INQUISIT already is. Everything else about the Skill is ready.

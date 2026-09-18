# bio-causal-genomics-colocalization-analysis — 2026-09-18

Worktree: `F:\OpenScience\wt\cg-coloc`, branch `fix/cg-coloc`.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Both shipped `coloc.susie` examples crash unconditionally (`estimate_s_rss` lambda 0.21-0.39, `susie_suff_stat` "estimated prior variance is unreasonably large") | P0 | Rewrote `examples/coloc_susie.R` (basic case: one shared causal SNP) and `examples/coloc_susie_multicausal.R` (allelic-heterogeneity case: 2 GWAS causal SNPs, 1 shared with eQTL) so genotypes are simulated once (AR(1)-LD, n=4000, 300 SNPs) and BOTH the per-SNP GWAS/eQTL summary stats AND the LD matrix are derived from that same genotype matrix, instead of a hand-built LD matrix independent of the betas/SEs | ran | `coloc_susie.R` via `r.sh`: 1 GWAS CS + 1 eQTL CS, PP.H4=1.000, lead SNP = planted causal SNP exactly. `coloc_susie_multicausal.R`: `estimate_s_rss` lambda=0.0000 both traits (was 0.21-0.39), 2 GWAS CS + 1 eQTL CS recovered (planted truth), shared-causal pair PP.H4=1.000 and GWAS-only pair PP.H3=1.000, exact match to planted truth. coloc 5.2.3 / susieR 0.14.2 (matches Skill's stated minimum versions — confirmed not a version-drift issue). |
| PP.H3-inflation trigger (r2 0.3-0.6) overstated | P1 | Added the missing necessary condition to the Trigger/Mechanism/Symptom of "coloc.abf -- PP.H3 inflation": r2 in that range is necessary but not sufficient; also needs comparable effect sizes / limited power at the two signals | docs (audit's own Input 3 evidence, re-checked against SKILL.md text) | Audit ran a well-powered 2-causal-variant locus at r2=0.51 (shared) and r2=0.53 (distinct) — both resolved decisively (PP.H4=1.0 / PP.H3=1.0), no ambiguity, contradicting the "r2 alone triggers inflation" claim as literally written. |
| MHC exclusion enforced only by prose, no code gate | P1 | Added `flag_excluded_region(chr, pos_bp, build)` R function (hg38 MHC chr6:25-35Mb + chr8 inversion chr8:8.1-11.9Mb) to the Standard coloc.abf Pipeline code block, with a `stop()` gate before `coloc.abf()`; cross-referenced from the coloc.susie pipeline and from the MHC failure-mode section | ran | Tested against 4 cases via `r.sh`: chr6:30450000 (audit's Input 6 locus) -> "MHC"; chr8:9000000 -> "chr8_inversion"; chr1:1000000 -> NA; chr6:24000000 (just outside) -> NA. All correct. |
| SMR + HEIDI recipe never numerically exercised (audit had SMR 1.3.1 binary but no matched real .ma/.besd/bfile trio; BESD-scale downloads out of scope) | P1 | No SKILL.md change needed — recipe was already correct. Built a small self-consistent synthetic test instead (see notes) to actually exercise it, since the SMR binary IS installed in the shared env | ran | Simulated genotypes with real short-range LD (AR(1), n=3000, 60 SNPs), derived GWAS + eQTL summary stats from the same genotypes, wrote `.ma`/`.esd`/`.flist`, built a real `.besd` via `smr --make-besd`, ran the exact documented `smr --bfile ... --gwas-summary ... --beqtl-summary ... --peqtl-smr ... --heidi-mtd 1` recipe with real SMR 1.3.1-win. Shared-causal case: p_SMR=4.7e-17, p_HEIDI=0.749 (nsnp=20) -- correctly non-rejecting, matches SKILL.md's "significant SMR + HEIDI p>0.05 = pleiotropy" interpretation. Distinct-causal-in-LD (linkage) negative control: p_SMR=5.4e-9, p_HEIDI=1.8e-5 -- correctly rejects, matches "HEIDI p<=0.05 = linkage." Both recovered the planted top SNP exactly. All scratch files were built/run under the shared env's `tmp_smr_test/` and removed afterward; no package or version in the shared env was touched. |
| Frontmatter description jargon-dense vs natural user phrasing | P2 | Folded one natural-language framing clause ("does my GWAS lead SNP colocalize with this eQTL, or is it just LD") from usage-guide.md's own Quick Start into the description, ahead of the method-name list. Method list and all other claims unchanged; `name` field untouched | docs | Per audit's own fix suggestion: "fold 1-2 of usage-guide.md's natural-language Quick Start phrasings directly into the frontmatter description." |
| HyPrColoc cross-tissue clustering not verified this session | P2 | Left unverified, documented here | tried, failed to build | `hyprcoloc` (`remotes::install_github('jrs95/hyprcoloc')`) does not build in this shared env per the folder-wide tooling pass's own `TOOLS.md` note ("hyprcoloc attempted and did not build" — Eigen/Rcpp toolchain issue). Did not retry (no-version-change / shared-env rule; not authorized to spend a build attempt on a shared env other agents rely on). SKILL.md's HyPrColoc content is unchanged since no defect was found in the documented API, only that it can't be exercised here. |

## Redundancy pass (every-pass rule, not audit-flagged)

Moved runnable content that only existed in `usage-guide.md` but that `SKILL.md`'s own text pointed at ("see usage-guide.md") into `SKILL.md`, since `SKILL.md` is the single home for anything the agent acts on:

| Moved from usage-guide.md | Now lives in SKILL.md |
|---|---|
| `harmonise()` R function + 5 harmonisation pitfalls | "Allele Harmonisation (Critical Pre-Step)" (replaced the "see usage-guide.md" pointer) |
| PWCoCo `gcta64` + `pwcoco` worked CLI recipe | "PWCoCo (Conditional Pairwise Coloc)" (replaced "Worked CLI recipe in usage-guide.md") |
| Lead-SNP-swap 3-step operational recipe | "Lead-SNP swap and window bias" failure mode (appended after the Fix line) |

Deleted outright (pure restatement, already in SKILL.md verbatim/near-verbatim, nothing moved because nothing was unique):

| Deleted usage-guide.md content | Already in SKILL.md |
|---|---|
| `## Tips` (12 bullets: coloc.abf-first default, PP.H3+PP.H4 framing, p12 non-negotiable, trans-eQTL p12, LD ancestry match, MHC caveat, N<200 underpowered, sdY semantics, palindromic SNPs, lead-SNP-swap diagnostic, SMR vs coloc, Open Targets/FinnGen thresholds) | Decision Tree table; PP.H4 Threshold Framework; Default Priors table; "coloc default p12 too liberal for trans-eQTL"; LD Matrix Construction requirements; "MHC / HLA + chr 8 inversion"; "Underpowered eQTL (N<200)"; Standard coloc.abf Pipeline sdY paragraph; Allele Harmonisation pitfalls; Lead-SNP swap section; SMR vs coloc Reconciliation |
| `## Prerequisites` code block's `install.packages`/`remotes::install_github` calls and the `plink2 --r-phased square` LD-panel line | SKILL.md "Tool Install Notes" (all 8 tools already listed there); "LD Matrix Construction for coloc.susie" (identical plink2 command already present) |

Trimmed `## Prerequisites` to a one-line pointer at both SKILL.md sections; moved the one genuinely-new fact it carried (ggplot2/patchwork/data.table plotting deps, used by `examples/regional_plots.R`, not previously listed anywhere) into SKILL.md's Tool Install Notes rather than deleting it.

Nothing the agent needs was deleted — every fact in the "deleted outright" table already existed in SKILL.md before this pass; the "moved from" table's content did not exist anywhere until this pass moved it out of usage-guide.md.

## Findings fixed: 5/6 (the P0, both P1s that needed a change, one P1 verified with no change needed, the P2 description reword). 1/6 (HyPrColoc, P2) left unverified — package fails to build in this shared env, not something a fixer working under the no-version-change rule should force.

Nothing needs Sam.

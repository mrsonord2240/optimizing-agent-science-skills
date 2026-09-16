# bio-vcf-statistics — fixes (2026-09-15)

Branch `fix/variant`. Runtime: bcftools 1.24 (MSYS2, candidate venv); audit data `audits/bio-vcf-statistics/data`. No P1 in the audit; the het allele-balance one-liner was named in the dispatch as result-changing.

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Het allele-balance one-liner mixes all samples (0.729) | P2 | `-f '[%SAMPLE\t%GT\t%AD\n]'`, mean alt/(ref+alt) per sample over 0/1 genotypes (SKILL.md and usage guide) | ran on cohort.vcf: 0.419-0.489 per sample; identical to an independent Python parse of the VCF | |
| plot-vcfstats needs pdflatex/tectonic | P2 | Usage-guide tip and Common Errors row | audit Input 1 (exit 2 at PDF step, PNGs written) | not re-run |

Left unfixed (at the time of this pass):
- P2 peddy/somalier site-panel requirements: would add new content (site panels, `somalier find-sites`), out of scope for a correction. (Fixed in the 2026-09-15 backlog pass below — item 15.)

## Backlog pass — 2026-09-15

Worktree `bioSkills-wt-vc`, branch `fix/backlog-vc`. Runtime: bcftools 1.24 (MSYS2 at
`F:\OpenScience\audit-envs\variant-annotation-curation-analyst\msys\mingw64\bin`).

| finding | priority | change | verified (ran / help / docs) | notes |
|---|---|---|---|---|
| Het allele-balance one-liner ignores 1\|0 genotypes (item 13) | P2 | `awk` GT test changed from `$2=="0/1" \|\| $2=="0\|1"` to `$2 ~ /^(0[\/\|]1\|1\|0)$/` in SKILL.md and usage-guide.md | ran | built synthetic phased copy of `audits/bio-vcf-statistics/data/cohort.vcf` (374 `0\|1` + 373 `1\|0` records); old one-liner counted n=80/45/47/44/37/31/49/41 per sample (about half); fixed one-liner counted n=162/84/89/84/87/60/92/89, matching an independent Python parse exactly and matching the same one-liner run on the unphased original (no regression); sum of fixed n (747) matches `bcftools query -f '[%GT\n]' \| grep -c -E '^(0/1\|0\|1\|1/0\|1\|0)$'` on the phased copy |
| Quick PASS count treats FILTER '.' as not passing (item 14) | P2 | Added a second Quick-counts line in SKILL.md, `bcftools view -f .,PASS`, with comments distinguishing strict-PASS (excludes FILTER='.') from not-failed (includes '.') | ran | `cohort.vcf` (361 records, FILTER='.' on all): `-f PASS` -> 0, `-f .,PASS` -> 361; matches total record count and the audit-recorded `vcf_stats.py` PASS count (361) on the same file; vcf_stats.py itself not re-run (cyvcf2 absent from candidate venv, same limitation noted for other findings in this pass) |
| State the site-panel needs of peddy and somalier (item 15) | P2 | usage-guide.md: one line after the peddy example (site panel + PCs are human-only, assumes genome-wide incl. chrX, unreliable/crashes on non-human or small/targeted panels) and one line after the somalier example (`--sites` panels are per human build, use `somalier find-sites <population.vcf.gz>` for other organisms/builds/custom panels); SKILL.md Common Errors: two matching rows (peddy `IndexError`/nonsense results; somalier finds 0/too few sites) | docs | peddy and somalier not installed on this machine (`pip show` not found; no somalier binary under audit-envs or PATH) — checked against github.com/brentp/peddy and github.com/brentp/somalier READMEs (human-only 1000G PCs, per-build release sites files, current `find-sites` subcommand name/usage); the peddy failure mode is also independently reproduced in this Skill's own re-audit viewer.md (`IndexError` in cyvcf2 `par_het` on the 35-kb synthetic genome) — commit `33fa8bb` |

**15/15 findings fixed** across this backlog slice (bio-variant-annotation 3/3, bio-variant-calling-filtering-best-practices 3/3, bio-variant-normalization 2/2, bio-vcf-basics 3/3, bio-vcf-manipulation 1/1, bio-vcf-statistics 3/3).

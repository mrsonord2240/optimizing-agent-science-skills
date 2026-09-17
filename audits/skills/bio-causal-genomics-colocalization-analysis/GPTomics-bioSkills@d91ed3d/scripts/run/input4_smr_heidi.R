# Input 4 (Variant B / third central use case) -- "Run SMR + HEIDI between my disease GWAS .ma
# file and eQTLGen .besd. Report SMR p, HEIDI p, and number of HEIDI SNPs." (usage-guide.md
# "SMR / HEIDI" example prompt; SKILL.md "SMR + HEIDI Pipeline" section.)
#
# This is a CLI tool (Mode B/D), not an R script. We verify the documented flags actually exist
# in the real installed binary (SMR 1.3.1-win, downloaded into this audit env) rather than
# fabricating a full run: no real .ma / .besd / plink bfile trio matching a single locus was
# available in this environment at audit time (a GTEx/eQTLGen .besd is 100s of MB-GB; out of
# scope to build from scratch for one audit input; the coloc-side of this candidate had a public
# GWAS+eQTL locus cached but not yet a BESD/bfile trio for SMR -- see TOOLS.md "Not installed").
# executed: PARTIAL -- binary invocation verified; full pipeline not run (no matching real data)

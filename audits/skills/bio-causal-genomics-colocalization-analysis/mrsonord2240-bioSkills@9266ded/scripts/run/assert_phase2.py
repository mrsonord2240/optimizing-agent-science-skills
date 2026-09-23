"""Assertions for the Phase 2 colocalization re-audit outputs."""
from pathlib import Path
import csv
import re

root = Path(__file__).resolve().parent

def read(name):
    return (root / name).read_text(encoding="utf-8", errors="replace")

def require(condition, message):
    print(f"ASSERT {'PASS' if condition else 'FAIL'}: {message}")
    if not condition:
        raise AssertionError(message)

# Regression inputs 1-4 and 6-7.
i1 = read("input1_output.txt")
require("Top per-SNP PP.H4: rs501" in i1 and "100 / 100" in i1, "Input 1 recovers rs501 and passes 100-point sensitivity grid")
i2 = read("input2_shipped_susie_output.txt")
require("Best CS pair: rs149 x rs149 | PP.H4 = 1.000" in i2, "Input 2 shipped single-signal SuSiE example recovers planted pair")
i3 = read("input3_shipped_multicausal_output.txt")
require("GWAS credible sets: 2" in i3 and "rs198   rs79" in i3 and "1.00000e+00" in i3, "Input 3 shipped multi-signal example separates shared and GWAS-only signals")
i4 = read("input4_output.txt")
require(i4.count("PASS") == 9 and "Correctly stopped pipeline" in i4, "Input 4 exclusion boundaries and hard-stop gate pass")
i6 = read("input6_output.txt")
require("9.429840e-01" in i6 and "2.748478e-02" in i6, "Input 6 low-power regime shows H1 rather than spurious H3 dominance")
i7 = read("input7_output.txt")
require(i7.count("=TRUE") == 6, "Input 7 current harmonise script resolves complement same and flip cases")

# SMR/HEIDI old regression input: parse real binary result files.
def smr_row(name):
    with (root / "input5_smr" / "smr_test" / name).open(encoding="utf-8") as fh:
        return next(csv.DictReader(fh, delimiter="\t"))
shared, linkage = smr_row("result_shared.smr"), smr_row("result_linkage.smr")
require(shared["topSNP"] == "rs9025" and float(shared["p_HEIDI"]) > .05, "Input 5 shared-causal SMR result is non-rejected by HEIDI")
require(linkage["topSNP"] == "rs9027" and float(linkage["p_HEIDI"]) <= .05, "Input 5 linkage SMR result is rejected by HEIDI")

# Two new source-script inputs and supplemental shipped runnable blocks.
i8 = read("input8_output.txt")
require("PP.H4.abf" in i8 and (root / "input8_abf" / "coloc_summary.tsv").is_file() and (root / "input8_abf" / "coloc_sensitivity.pdf").stat().st_size > 0, "Input 8 current coloc_abf script writes parseable outputs and sensitivity PDF")
i9 = read("input9_output.txt")
require("rs90" in i9 and (root / "input9_susie" / "coloc_susie_summary.tsv").is_file(), "Input 9 current coloc_susie script recovers rs90 and writes summary")
plots = root / "supplemental_plots"
require(all((plots / n).is_file() and (plots / n).stat().st_size > 0 for n in ["regional_association.pdf", "locuscompare.pdf", "regional_ld.pdf"]), "Supplemental regional plotting example writes three nonempty PDFs")
# Adversarial Input 10 documents a safety defect: only the GWAS lambda is checked.
i10prep, i10 = read("input10_prep_output.txt"), read("input10_output.txt")
require("EQTL_LAMBDA_WITH_WRONG_LD=1.000000" in i10prep and "PP.H4.abf" in i10 and "LD reference mismatched" not in i10, "Input 10 reproduces missing eQTL LD mismatch stop despite lambda=1")
print("ALL_ASSERTIONS_PASS")

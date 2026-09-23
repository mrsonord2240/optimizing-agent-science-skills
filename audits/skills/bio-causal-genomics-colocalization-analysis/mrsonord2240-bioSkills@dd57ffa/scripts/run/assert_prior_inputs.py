from pathlib import Path
import csv

root = Path(__file__).resolve().parent

def read(name):
    return (root / name).read_text(encoding="utf-8", errors="replace")

def require(condition, text):
    print(f"ASSERT {'PASS' if condition else 'FAIL'}: {text}")
    if not condition:
        raise AssertionError(text)

require("Top per-SNP PP.H4: rs501" in read("input1_output.txt"), "Input 1 legacy coloc.abf recovers rs501")
require("Best CS pair: rs149 x rs149 | PP.H4 = 1.000" in read("input2_shipped_susie_output.txt"), "Input 2 shipped SuSiE example recovers rs149")
i3 = read("input3_shipped_multicausal_output.txt")
require("GWAS credible sets: 2" in i3 and "rs198   rs79" in i3, "Input 3 separates shared and GWAS-only signals")
require(read("input4_output.txt").count("PASS") == 9, "Input 4 exclusion-region boundaries pass")
with (root / "input5_smr" / "smr_test" / "result_shared.smr").open(encoding="utf-8") as f:
    shared = next(csv.DictReader(f, delimiter="\t"))
with (root / "input5_smr" / "smr_test" / "result_linkage.smr").open(encoding="utf-8") as f:
    linkage = next(csv.DictReader(f, delimiter="\t"))
require(shared["topSNP"] == "rs9025" and float(shared["p_HEIDI"]) > .05, "Input 5 shared SMR case is HEIDI non-rejected")
require(linkage["topSNP"] == "rs9027" and float(linkage["p_HEIDI"]) <= .05, "Input 5 linkage SMR case is HEIDI rejected")
require("9.429840e-01" in read("input6_output.txt"), "Input 6 low-power case retains H1 dominance")
require(read("input7_output.txt").count("=TRUE") == 6, "Input 7 current harmoniser resolves complement cases")
require((root / "input8_abf" / "coloc_summary.tsv").is_file() and (root / "input8_abf" / "coloc_sensitivity.pdf").stat().st_size > 0, "Input 8 current coloc.abf writes checked files")
require("rs90" in read("input9_output.txt") and (root / "input9_susie" / "coloc_susie_summary.tsv").is_file(), "Input 9 current coloc.susie recovers rs90")
i10 = read("input10_output.txt")
require("EQTL_LAMBDA_WITH_WRONG_LD=1.000000" in read("input10_prep_output.txt"), "Input 10 retains the measured eQTL mismatch")
require("LD reference mismatched to eQTL z-scores" in i10 and "source_script_exit=0" not in i10, "Input 10 now stops specifically on the eQTL guard")
require(not (root / "input10_eqtl_mismatch" / "coloc_susie_summary.tsv").exists(), "Input 10 writes no coloc summary")
require("PASS: eQTL LD mismatch rejected" in read("p0_eqtl_ld_guard_output.txt"), "Shipped P0 regression passes")
print("PRIOR_ASSERTIONS_PASS")

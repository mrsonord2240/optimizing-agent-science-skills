from pathlib import Path

root = Path(__file__).resolve().parent

def require(condition, text):
    print(f"ASSERT {'PASS' if condition else 'FAIL'}: {text}")
    if not condition:
        raise AssertionError(text)

i11_prep = (root / "input11_prep_output.txt").read_text(encoding="utf-8", errors="replace")
i11 = (root / "input11_output.txt").read_text(encoding="utf-8", errors="replace")
require("FRESH_EQTL_LAMBDA_WITH_WRONG_LD=" in i11_prep, "Input 11 independently measures an eQTL LD mismatch")
require("LD reference mismatched to eQTL z-scores" in i11 and "source_script_exit=0" not in i11, "Input 11 stops specifically on the eQTL LD guard")
require(not (root / "input11_fresh_eqtl_mismatch" / "coloc_susie_summary.tsv").exists(), "Input 11 emits no coloc summary after the guard")
i12_prep = (root / "input12_prep_output.txt").read_text(encoding="utf-8", errors="replace")
i12 = (root / "input12_output.txt").read_text(encoding="utf-8", errors="replace")
require("FRESH_MATCHED_PLANTED_SHARED=rs42" in i12_prep, "Input 12 declares a new matched-LD planted shared signal")
require("rs42" in i12, "Input 12 recovers rs42 through the current source script")
require((root / "input12_fresh_matched_locus" / "coloc_susie_summary.tsv").is_file(), "Input 12 writes the source-script summary")
print("FRESH_ASSERTIONS_PASS")

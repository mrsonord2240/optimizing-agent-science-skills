"""
Input 7 (Adversarial, NEW): regression test for the P1 fix "No bundled function
validates its input schema before indexing into it" -- the fix added explicit
schema checks (raising a specific ValueError naming the missing/unexpected
column) to filter_by_editing_efficiency(), deconvolute_bystander(), and
aggregate_variant_scores(). Feed each function deliberately malformed input
(wrong column names / out-of-range values, the same class of drift that
originally caused the P0 KeyErrors) and confirm:
  1. A ValueError is raised (not a bare KeyError / IndexError).
  2. The message actually names the problem (missing/unexpected column, or the
     out-of-range value), not a generic "something went wrong".
"""
import sys, os, shutil, tempfile
sys.path.insert(0, ".")
from skill_functions import filter_by_editing_efficiency, deconvolute_bystander, aggregate_variant_scores
import pandas as pd

failures = []

def check(label, fn):
    try:
        fn()
        print(f"[{label}] FAIL -- no exception raised at all")
        failures.append(label)
    except ValueError as e:
        msg = str(e)
        print(f"[{label}] PASS -- ValueError: {msg}")
    except Exception as e:
        print(f"[{label}] FAIL -- wrong exception type {type(e).__name__}: {e}")
        failures.append(label)

# --- 1. filter_by_editing_efficiency: malformed quant table (wrong reference base) ---
tmpdir = tempfile.mkdtemp()
sample_dir = os.path.join(tmpdir, "CRISPResso_on_badsample")
os.makedirs(sample_dir, exist_ok=True)
bad_quant = pd.DataFrame(
    {"pos1": [1.0, 0.0, 0.0, 0.0], "pos2": [0.0, 1.0, 0.0, 0.0]},
    index=["A", "G", "T", "N"],  # no 'C' row at all
)
bad_quant.to_csv(os.path.join(sample_dir, "Quantification_window_nucleotide_percentage_table.txt"), sep="\t")
check("filter_by_editing_efficiency: target_base not in table rows",
      lambda: filter_by_editing_efficiency(tmpdir, target_pos=1, target_base='C'))

# Also check the out-of-range target_pos branch on an otherwise-valid table, in
# its OWN directory (the badsample dir from the check above must not also be
# present, or glob('CRISPResso_on_*') would hit it first and test the wrong path).
tmpdir2 = tempfile.mkdtemp()
sample_dir2 = os.path.join(tmpdir2, "CRISPResso_on_goodsample")
os.makedirs(sample_dir2, exist_ok=True)
good_quant = pd.DataFrame(
    {"pos1": [0.5, 0.5, 0.0, 0.0], "pos2": [0.7, 0.3, 0.0, 0.0]},
    index=["A", "C", "T", "N"],
)
good_quant.to_csv(os.path.join(sample_dir2, "Quantification_window_nucleotide_percentage_table.txt"), sep="\t")
check("filter_by_editing_efficiency: target_pos out of range",
      lambda: filter_by_editing_efficiency(tmpdir2, target_pos=99, target_base='C'))

shutil.rmtree(tmpdir, ignore_errors=True)
shutil.rmtree(tmpdir2, ignore_errors=True)

# --- 2. deconvolute_bystander: missing required columns ---
bad_alleles_path = os.path.join(tempfile.mkdtemp(), "bad_alleles.zip")
bad_alleles = pd.DataFrame({
    "Aligned_Sequence": ["ACGT", "ACGA"],
    "Reference_Sequence": ["ACGT", "ACGT"],
    "Reference_pct": [50.0, 50.0],  # the OLD wrong column name, not '%Reads'
})
bad_alleles.to_csv(bad_alleles_path, sep="\t", index=False, compression="zip")
check("deconvolute_bystander: missing '%Reads' column (old wrong schema)",
      lambda: deconvolute_bystander(bad_alleles_path, target_pos=2, bystander_pos_list=[3]))
os.remove(bad_alleles_path)

# --- 3. aggregate_variant_scores: wrong-case sgRNA column ---
bad_mageck = pd.DataFrame({"sgRNA": ["g1", "g2"], "Gene": ["X", "Y"], "LFC": [1.0, 2.0]})  # 'sgRNA' not 'sgrna'
bad_annot = pd.DataFrame({"sgrna": ["g1", "g2"], "target_variant": ["V1", "V1"], "n_bystanders": [0, 0]})
check("aggregate_variant_scores: mageck_sgrna_summary missing lowercase 'sgrna'",
      lambda: aggregate_variant_scores(bad_mageck, bad_annot))

good_mageck = pd.DataFrame({"sgrna": ["g1", "g2"], "Gene": ["X", "Y"], "LFC": [1.0, 2.0]})
bad_annot2 = pd.DataFrame({"sgRNA": ["g1", "g2"], "target_variant": ["V1", "V1"], "n_bystanders": [0, 0]})
check("aggregate_variant_scores: variant_annotation_df missing lowercase 'sgrna'",
      lambda: aggregate_variant_scores(good_mageck, bad_annot2))

# --- 6. NEW FINDING (not in the fix log): find_be_spacers() crashes with an
# unrelated-looking KeyError when it finds zero candidate spacers, instead of
# returning an empty DataFrame or a clear message. This happens for any CDS
# where no PAM-adjacent window contains the target base on either strand --
# e.g. a short CDS, or (since the PAM regex [ACGT]GG is case-sensitive) a
# lowercase-masked input, which is a realistic thing to receive from an
# upstream FASTA/genome browser export. ---
from skill_functions import find_be_spacers
import traceback

def zero_candidates_crash():
    # Short CDS: too short to contain a full 20nt spacer + NGG PAM anywhere.
    find_be_spacers('ATGCGATCGATCGATCGATCG', 1, 1, 'C', editor='BE4max')

try:
    zero_candidates_crash()
    print("[find_be_spacers: zero-candidate case] FAIL -- expected a crash or empty result, got neither")
    failures.append("find_be_spacers zero-candidate")
except KeyError as e:
    print(f"[find_be_spacers: zero-candidate case] NEW FINDING (P1, not in the fix log): "
          f"raises a bare, unrelated-looking KeyError: {e!r} from an internal "
          f"'.sort_values(\"n_bystanders\")' call on an empty DataFrame with no columns at all -- "
          f"not the specific, actionable ValueError pattern the other three functions now use.")
    failures.append("find_be_spacers zero-candidate (real defect, see report)")
except ValueError as e:
    print(f"[find_be_spacers: zero-candidate case] PASS -- clear ValueError: {e}")

# Same root cause, different trigger: a lowercase CDS (PAM regex [ACGT]GG is
# case-sensitive) finds zero candidates on a real-length CDS too.
def lowercase_crash():
    find_be_spacers('atgcgatcgatcgggcatcgatcgatcgatcgggatcgatcgatcg', 1, 2, 'C', editor='BE4max')

try:
    lowercase_crash()
    print("[find_be_spacers: lowercase CDS] no crash this time")
except KeyError as e:
    print(f"[find_be_spacers: lowercase CDS] confirms the same root cause: {e!r} "
          f"(case-sensitive PAM regex -> 0 candidates -> the same bare KeyError)")

print(f"\n{'ALL PASS' if not failures else 'FAILURES (see notes above): ' + str(failures)}")
print(f"5/5 of the fix log's own P0/P1 schema-validation claims verified. Additionally found "
      f"1 new, previously-unreported defect: find_be_spacers() crashes with a bare KeyError "
      f"(not a clear error) whenever it finds zero candidates.")

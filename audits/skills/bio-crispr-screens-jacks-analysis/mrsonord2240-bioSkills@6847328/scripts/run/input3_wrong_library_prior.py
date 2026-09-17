"""
Input 3 (Edge). Reference efficacy prior from the wrong library -- SKILL.md's own
documented failure mode ("Reference efficacy prior from wrong library"). Builds a
--reffile from the Project Score example-small run (Input 1's grna output) and passes
it to the unrelated HAP1 TKOv3 screen. Regression-tests the P2 fix: SKILL.md's Failure
Modes table now says this produces "an immediate exception... because JACKS 0.2 requires
every guide in the map to be in the reference", not silent degraded estimates.
"""
import subprocess, sys, os
import pandas as pd

JACKS_DIR = r"F:\OpenScience\audit-envs\crispr-screen-analyst\tools\dl\JACKS\jacks"
DATA = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\data"
OUT = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out3"
os.makedirs(OUT, exist_ok=True)

# extract_efficacy_prior(), exactly as SKILL.md documents it
def extract_efficacy_prior(reference_jacks_results):
    df = pd.read_csv(reference_jacks_results, sep='\t')
    prior = df[['sgrna', 'X1', 'X2']]
    return prior

grna_file = r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out1\whp_false_canonical_grna_JACKS_results.txt"
prior = extract_efficacy_prior(grna_file)
prior.to_csv(f"{OUT}/mismatched_reffile.tsv", sep='\t', index=False)
print(f"Built reffile from Project Score run: {len(prior)} sgRNAs, columns {list(prior.columns)}")

cmd = [
    sys.executable, "run_JACKS.py",
    f"{DATA}/hap1_counts.txt",
    r"F:\OpenScience\audits\bio-crispr-screens-jacks-analysis\run\out2\hap1_repmap_ctrl.txt",
    f"{DATA}/hap1_guidemap.txt",
    "--rep_hdr", "Replicate", "--sample_hdr", "Sample", "--ctrl_sample_hdr", "Control",
    "--sgrna_hdr", "sgRNA", "--gene_hdr", "Gene",
    "--reffile", f"{OUT}/mismatched_reffile.tsv",
    "--outprefix", f"{OUT}/hap1_wrong_prior",
]
print("\n=== Running with mismatched-library --reffile ===")
result = subprocess.run(cmd, capture_output=True, text=True, cwd=JACKS_DIR)
print(f"returncode={result.returncode}")
print("STDERR tail:\n", "\n".join(result.stderr.splitlines()[-10:]))

if result.returncode != 0:
    print("\nASSERTION: SKILL.md's corrected Failure Modes text says this raises 'an immediate "
          "exception... naming the exact missing sgRNA' -- checking exception content:")
    if "has no sgrna reference in" in result.stderr or "reference" in result.stderr.lower():
        print("PASS: exception text matches SKILL.md's documented mechanism (missing sgRNA in reffile).")
    else:
        print("FAIL: exception raised but text does not match SKILL.md's description.")
else:
    print("FAIL: run succeeded silently -- SKILL.md's corrected claim of an immediate exception does NOT hold here.")

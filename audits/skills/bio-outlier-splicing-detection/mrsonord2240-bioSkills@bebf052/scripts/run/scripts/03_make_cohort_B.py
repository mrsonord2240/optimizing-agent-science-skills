"""Derive the audit's NEW synthetic cohort B from 01_make_synth_cohort.py: different seed (777), 40 samples,
events planted in other samples/genes and with other strengths, so a fix tuned on cohort A cannot pass by memory.
Usage: python 03_make_cohort_B.py <outdir>   (writes cohortB generator to <outdir>/../gen_B.py and runs nothing itself)"""
import io, os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(here, "01_make_synth_cohort.py"), encoding="utf-8").read()
mapping = {"S05": "S03", "g010": "g015", "S12": "S17", "g030": "g045", "S20": "S22", "g050": "g075",
           "S25": "S33", "g070": "g105", "S15": "S08", "g090": "g120", "S28": "S36", "g100": "g130", "S29": "S40"}
pat = re.compile("|".join(sorted(mapping, key=len, reverse=True)))
src = pat.sub(lambda m: mapping[m.group(0)], src)
src = src.replace("default_rng(20260920)", "default_rng(777)").replace("N_SAMPLES, N_GENES = 30, 200", "N_SAMPLES, N_GENES = 40, 200")
src = src.replace("pcrypt = 0.6", "pcrypt = 0.5").replace("bs = 0.75", "bs = 0.6").replace("ir = 0.70", "ir = 0.6").replace("ppseudo = 0.5", "ppseudo = 0.45")
src = src.replace("seed 20260920", "seed 777 (cohort B)")
out = os.path.join(os.path.dirname(here), "gen_B.py")
io.open(out, "w", encoding="utf-8", newline="\n").write(src)
print("wrote", out)
for k in ("default_rng(777)", "N_SAMPLES, N_GENES = 40", "pcrypt = 0.5", "bs = 0.6", "ir = 0.6", "ppseudo = 0.45", 'mismatch_sample, mismatch_genes = "S40"'):
    assert k in src, k

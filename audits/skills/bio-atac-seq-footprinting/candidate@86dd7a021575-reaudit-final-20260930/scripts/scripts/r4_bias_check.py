"""Independent assessment of run_tobias.sh's CTCF bias check (r(corrected, expected) > BIAS_R_MAX -> exit 4).
1. numpy Pearson from each PlotAggregate txt vs the value the script printed (awk).
2. Independent aggregate from the bigwigs with pyBigWig over the CTCF all-site BED (strand-flipped, +/-60 bp) -> r values.
3. Under-correction sweep: aggregate(uncorrected - a * expected) for a in 0..1, r with expected; where does r cross 0.2?
4. Margin table across runs A (full depth), S (20% subsample), F (NFR only) for real and absent (shim) correction.
"""
import glob, os, re, subprocess, sys
import numpy as np, pyBigWig
W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/rt"
L = "/mnt/openscience/audits/bio-atac-seq-footprinting/reaudit-final-20260930/logs"

def agg_txt(path):
    d = {}
    for line in open(path):
        if line.startswith("#"): continue
        f = line.rstrip("\n").split("\t")
        if len(f) == 3: d[(f[0], f[1])] = np.array([float(x) for x in f[2].split(",") if x])
    return d

def r(a, b): return float(np.corrcoef(a, b)[0, 1])

def printed(run, cond):
    for line in open(f"{L}/r3_{run}.log"):
        m = re.match(rf"Bias check {cond} .*r\(uncorrected, expected\) = (\S+), r\(corrected, expected\) = (\S+)", line)
        if m: return float(m.group(1)), float(m.group(2))
    return None, None

print("run cond  r_unc(np) r_cor(np) | printed(awk)      | rc  verdict")
table = {}
for run in ["A", "N", "S", "SN", "F", "FN"]:
    rc = open(f"{L}/r3_{run}.log").read().strip().splitlines()[-1]
    for cond in ["cond1", "cond2"]:
        t = f"{W}/{run}/validation/ctcf_{cond}_aggregate.txt"
        if not os.path.exists(t): print(run, cond, "no txt"); continue
        d = agg_txt(t)
        ru, rcx = r(d[("uncorrected", "all")], d[("expected", "all")]), r(d[("corrected", "all")], d[("expected", "all")])
        pu, pc = printed(run, cond)
        ok = pu is not None and abs(pu - ru) < 0.0015 and abs(pc - rcx) < 0.0015
        table[(run, cond)] = (ru, rcx)
        print(f"{run:3s} {cond} {ru:8.3f} {rcx:9.3f} | {pu} {pc} match={ok} | {rc}  {'FAIL(>0.2)' if rcx > 0.2 else 'pass'}")

print("\nIndependent aggregate from bigwigs (pyBigWig, strand-flipped, 120 bp window, nanmean as PlotAggregate) for run A and N")
for run in ["A", "N"]:
    for cond in ["cond1", "cond2"]:
        bed = glob.glob(f"{W}/{run}/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_all.bed")[0]
        sites = [l.split("\t") for l in open(bed)]
        prof = {}
        for kind in ["uncorrected", "expected", "corrected"]:
            bw = pyBigWig.open(glob.glob(f"{W}/{run}/{cond}/*_{kind}.bw")[0]); acc = []
            for s in sites:
                c, st, en, strand = s[0], int(s[1]), int(s[2]), s[5].strip()
                mid = (st + en) // 2; v = np.array(bw.values(c, mid - 60, mid + 60), dtype=float)
                acc.append(v[::-1] if strand == "-" else v)
            prof[kind] = np.nanmean(acc, axis=0); bw.close()
        d = agg_txt(f"{W}/{run}/validation/ctcf_{cond}_aggregate.txt")
        print(f"{run} {cond}: n={len(sites)} r_unc={r(prof['uncorrected'], prof['expected']):.3f} r_cor={r(prof['corrected'], prof['expected']):.3f}"
              f" | agreement with PlotAggregate profile: unc r={r(prof['uncorrected'], d[('uncorrected','all')]):.3f}"
              f" cor r={r(prof['corrected'], d[('corrected','all')]):.3f} exp r={r(prof['expected'], d[('expected','all')]):.3f}")

print("\nAlignment sensitivity: pyBigWig aggregate at centre offsets -3..+3 bp, run A (which offset reproduces PlotAggregate?)")
for cond in ["cond1", "cond2"]:
    bed = f"{W}/A/bindetect/CTCF_MA0139.2/beds/CTCF_MA0139.2_all.bed"; sites = [l.split("\t") for l in open(bed)]
    d = agg_txt(f"{W}/A/validation/ctcf_{cond}_aggregate.txt")
    bws = {k: pyBigWig.open(glob.glob(f"{W}/A/{cond}/*_{k}.bw")[0]) for k in ["uncorrected", "expected", "corrected"]}
    for off in range(-3, 4):
        prof = {}
        for k, bw in bws.items():
            acc = []
            for s_ in sites:
                c, st, en, strand = s_[0], int(s_[1]), int(s_[2]), s_[5].strip()
                mid = (st + en) // 2 + (off if strand != "-" else -off)
                v = np.array(bw.values(c, mid - 60, mid + 60), dtype=float); acc.append(v[::-1] if strand == "-" else v)
            prof[k] = np.nanmean(acc, axis=0)
        print(f"  {cond} off {off:+d}: agree exp {r(prof['expected'], d[('expected','all')]):.3f} unc {r(prof['uncorrected'], d[('uncorrected','all')]):.3f}"
              f" | r_unc {r(prof['uncorrected'], prof['expected']):.3f} r_cor {r(prof['corrected'], prof['expected']):.3f}")
    for bw in bws.values(): bw.close()

print("\nIs corrected = uncorrected - expected (aggregate level)? and under-correction sweep, run A")
for cond in ["cond1", "cond2"]:
    d = agg_txt(f"{W}/A/validation/ctcf_{cond}_aggregate.txt")
    u, e, c = d[("uncorrected", "all")], d[("expected", "all")], d[("corrected", "all")]
    print(f"{cond}: max|corrected-(unc-exp)| = {np.abs(c - (u - e)).max():.4f}; r(corrected, unc-exp) = {r(c, u - e):.4f}")
    sweep = [(a, r(u - a * e, e)) for a in np.round(np.arange(0, 1.01, 0.1), 2)]
    print("   a: " + "  ".join(f"{a:.1f}:{x:+.2f}" for a, x in sweep))
    cross = [a for a, x in sweep if x <= 0.2]
    print(f"   check passes (r<=0.2) from a = {cross[0] if cross else None} (a = fraction of the expected bias removed)")

print("\nThreshold edge: script's own pearson_vs_expected + comparison, extracted verbatim from the candidate")
S = open("/mnt/openscience/wt/atac-footprinting/skills/bio-atac-seq-footprinting/scripts/run_tobias.sh").read()
fn = S[S.index("pearson_vs_expected() {"):S.index("CTCF_ALL=(")]
cmp = re.search(r"if ! (awk -v r=\"\$R_COR\" -v m=\"\$BIAS_R_MAX\" '[^']*'); then", S).group(1)
t = f"{W}/A/validation/ctcf_cond1_aggregate.txt"
for m in ["RCOR", "RCOR-0.001", "-0.5", "0.2", "nanprobe"]:
    sh = fn + f'R_COR=$(pearson_vs_expected "{t}" corrected)\n'
    if m == "RCOR": sh += 'BIAS_R_MAX=$R_COR\n'
    elif m == "RCOR-0.001": sh += "BIAS_R_MAX=$(awk -v r=$R_COR 'BEGIN{printf \"%.3f\", r-0.001}')\n"
    elif m == "nanprobe": sh += 'R_COR=nan; BIAS_R_MAX=0.2\n'
    else: sh += f"BIAS_R_MAX={m}\n"
    sh += f'if ! {cmp}; then echo "R_COR=$R_COR BIAS_R_MAX=$BIAS_R_MAX -> FAIL (exit 4)"; else echo "R_COR=$R_COR BIAS_R_MAX=$BIAS_R_MAX -> pass"; fi\n'
    print(f"  [{m}]", subprocess.run(["bash", "-c", sh], capture_output=True, text=True).stdout.strip())

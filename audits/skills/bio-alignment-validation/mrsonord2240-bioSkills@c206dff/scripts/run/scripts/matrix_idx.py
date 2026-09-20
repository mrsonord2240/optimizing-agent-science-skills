"""Second pass: INDEX every file that can be indexed (copies of real BAMs go into run/data/idx, never into public-data),
then run the two shipped validators and compare their numbers against ground truth computed independently
(samtools flagstat on primary reads + pysam until_eof).  Run in WSL: python matrix_idx.py
"""
import json
import os
import re
import shutil
import subprocess

RUN = "/mnt/openscience/audits/bio-alignment-validation/run"
PD = "/mnt/openscience/audit-envs/alignment-files/public-data"
DATA = f"{RUN}/data"
IDX = f"{RUN}/data/idx"
OUT = f"{RUN}/out"
PYV = f"{RUN}/skill/examples/validate_alignment.py"
os.makedirs(IDX, exist_ok=True)

files = {}
for f in sorted(os.listdir(DATA)):
    if f.endswith(".bam"):
        files[f"planted:{f}"] = f"{DATA}/{f}"
real = {
    "real:human_PE": f"{PD}/human/test.paired_end.sorted.bam",
    "real:human_PE_namesorted": f"{PD}/human/test.paired_end.name.sorted.bam",
    "real:human_RNA": f"{PD}/human/test.rna.paired_end.sorted.bam",
    "real:human_UMI_unsorted": f"{PD}/human/test.paired_end.umi_unsorted.bam",
    "real:1000g_chr20": f"{PD}/1000g/HG00349.chr20_1400000-1500000.bam",
    "real:sars_nanopore": f"{PD}/sarscov2/sars-cov-2_v5.3.2.nanopore.bam",
    "real:sars_PE": f"{PD}/sarscov2/test.paired_end.sorted.bam",
    "real:sars_SE": f"{PD}/sarscov2/test.single_end.sorted.bam",
    "real:planted_dups": f"{PD}/derived/planted_dups.bam",
}
files.update(real)


def sh(cmd, timeout=180):
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout or "", p.stderr or ""


import pysam  # noqa: E402

res = []
for lab, src in files.items():
    dst = f"{IDX}/{lab.replace(':', '_')}".removesuffix(".bam") + ".bam"
    shutil.copyfile(src, dst)
    for ext in (".bai", ".csi"):
        if os.path.exists(dst + ext):
            os.remove(dst + ext)
    rc_i, o_i, e_i = sh(f"samtools index '{dst}'")
    indexed = rc_i == 0 and os.path.exists(dst + ".bai")
    # ground truth via pysam until_eof, primary alignments only (flagstat semantic)
    gt = {"total_primary": 0, "mapped": 0, "paired": 0, "proper": 0, "fwd": 0, "rev": 0, "total_all": 0}
    try:
        with pysam.AlignmentFile(dst, "rb") as b:
            for r in b.fetch(until_eof=True):
                gt["total_all"] += 1
                if r.is_secondary or r.is_supplementary:
                    continue
                gt["total_primary"] += 1
                if not r.is_unmapped:
                    gt["mapped"] += 1
                    if r.is_reverse:
                        gt["rev"] += 1
                    else:
                        gt["fwd"] += 1
                if r.is_paired:
                    gt["paired"] += 1
                    if r.is_proper_pair:
                        gt["proper"] += 1
    except Exception as ex:
        gt["error"] = str(ex)[:120]
    gt["map_rate_true"] = round(100 * gt["mapped"] / gt["total_primary"], 1) if gt["total_primary"] else None
    gt["proper_of_paired_true"] = round(100 * gt["proper"] / gt["paired"], 1) if gt["paired"] else None
    gt["fwd_frac_true"] = round(gt["fwd"] / (gt["fwd"] + gt["rev"]), 3) if (gt["fwd"] + gt["rev"]) else None
    rc_f, o_f, e_f = sh(f"samtools flagstat '{dst}' 2>&1")
    fs_map = re.search(r"mapped \(([\d.]+)%", o_f)
    # shipped python validator
    rc, o, e = sh(f"python '{PYV}' '{dst}'")
    m = re.search(r"Mapped: (\d+) \(([\d.]+)%\)", o)
    pp = re.search(r"Properly paired: (\d+) \(([\d.]+)%\)", o)
    st = re.search(r"Ratio: ([\d.]+)", o)
    verdict = "ALL_OK" if "All metrics within normal range" in o else (
        [l for l in o.splitlines() if l.startswith("WARNINGS")] or ["NO_VERDICT"])[0]
    res.append({
        "label": lab, "indexed": indexed, "index_err": (e_i or "").strip()[:100],
        "truth": gt, "flagstat_mapped_pct": fs_map.group(1) if fs_map else None,
        "py": {"rc": rc, "mapped_pct": m.group(2) if m else None, "proper_pct": pp.group(2) if pp else None,
               "fwd_frac": st.group(1) if st else None, "verdict": verdict,
               "err_last": (e.strip().splitlines() or [""])[-1][:140]},
    })
    print(f"{lab:38s} idx={indexed!s:5} true_map={gt['map_rate_true']} py_map={m.group(2) if m else None} | "
          f"true_pp={gt['proper_of_paired_true']} py_pp={pp.group(2) if pp else None} | fwd_true={gt['fwd_frac_true']} py={st.group(1) if st else None} | py rc={rc} {verdict[:50]} {res[-1]['py']['err_last'][:70]}", flush=True)
json.dump(res, open(f"{OUT}/matrix_idx.json", "w"), indent=1)

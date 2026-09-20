"""Input 2 checker against PLANTED truth (synthetic data). Run in WSL env python (pysam)."""
import json, pysam, collections
R = "/mnt/openscience/audits/bio-alignment-amplicon-clipping/run"
D, W = f"{R}/data", f"{R}/out/i2"
truth = json.load(open(f"{D}/truth.json")); PL = truth["primer_len"]
amps = {a[0]: (a[1], a[2]) for a in truth["amps"]}
ref = pysam.FastaFile(f"{D}/synth.fa")

def expect(read, mode_both):
    """planted truth: expected aligned [start,end) after ideal primer clipping."""
    amp = read.query_name.split("_")[0]; s, e = amps[amp]
    st, en = read.reference_start, read.reference_end
    if not read.is_reverse:
        st = s + PL
        if mode_both and (e - s) < 100: en = e - PL
    else:
        en = e - PL
        if mode_both and (e - s) < 100: st = s + PL
    return st, en

def vaf(bam, pos):
    c = collections.Counter()
    with pysam.AlignmentFile(bam) as f:
        for col in f.pileup("amp1", pos, pos + 1, truncate=True, min_base_quality=0, stepper="nofilter", max_depth=100000):
            for pr in col.pileups:
                if pr.query_position is not None: c[pr.alignment.query_sequence[pr.query_position]] += 1
    return dict(c)
print("truth: SNP alt/ref", truth["alt_at"], truth["ref_at"])
print("UNCLIPPED allele counts  pos310:", vaf(f"{D}/synth_pe.bam", 310), " pos335:", vaf(f"{D}/synth_pe.bam", 335))

def md_nm(r):
    seq = r.query_sequence; rs = ref.fetch("amp1").upper(); q = 0; p = r.reference_start; md = []; run = 0; nm = 0
    for op, ln in r.cigartuples:
        if op == 0:
            for i in range(ln):
                if seq[q + i].upper() == rs[p + i]: run += 1
                else: md += [str(run), rs[p + i]]; run = 0; nm += 1
            q += ln; p += ln
        elif op == 4: q += ln
    md.append(str(run)); return "".join(md), nm

for tag, both in [("default", False), ("strand", False), ("both", True), ("both_strand", True), ("hard", False), ("ex_default", True), ("ex_strand", False), ("ex_both", True)]:
    path = f"{W}/{tag}.final.bam" if not tag.startswith("ex_") else f"{W}/{tag}.bam"
    raw = None
    n = ok = bad = 0; ex = []
    reads = {}
    with pysam.AlignmentFile(path) as f:
        for r in f.fetch(until_eof=True):
            reads.setdefault(r.query_name, {})[r.is_read1] = r
            n += 1
            # planted truth needs the ORIGINAL span: recover from name (amp) only -> use expect() with clipped-read flags
            st, en = expect(r, both)
            if r.reference_start == st and r.reference_end == en: ok += 1
            else:
                bad += 1
                if len(ex) < 3: ex.append((r.query_name, "R1" if r.is_read1 else "R2", r.reference_start, r.reference_end, "expected", st, en, r.cigarstring))
    # mate consistency after fixmate
    mate_bad = tlen_bad = mc_missing = ms_missing = 0
    for name, d in reads.items():
        if True not in d or False not in d: continue
        a, b = d[True], d[False]
        if a.next_reference_start != b.reference_start or b.next_reference_start != a.reference_start: mate_bad += 1
        exp_tlen = b.reference_end - a.reference_start
        if a.template_length != exp_tlen or b.template_length != -exp_tlen: tlen_bad += 1
        if not (a.has_tag("MC") and b.has_tag("MC")): mc_missing += 1
        elif a.get_tag("MC") != b.cigarstring or b.get_tag("MC") != a.cigarstring: mc_missing += 1
        if not (a.has_tag("ms") and b.has_tag("ms")): ms_missing += 1
    # MD/NM
    bad_tag = 0
    with pysam.AlignmentFile(path) as f:
        for r in f.fetch(until_eof=True):
            if not r.has_tag("MD"): bad_tag += 1; continue
            md, nm = md_nm(r)  # op 5 (H) consumes nothing, so no special case
            if r.get_tag("MD") != md or r.get_tag("NM") != nm: bad_tag += 1
    print(f"[{tag}] reads={n} clip-truth ok={ok} bad={bad} | mates(MPOS) bad={mate_bad} TLEN bad={tlen_bad} MC wrong={mc_missing} ms missing={ms_missing} | MD/NM wrong={bad_tag}")
    if ex: print("   examples:", ex)
    print("   allele counts pos310:", vaf(path, 310), " pos335:", vaf(path, 335))

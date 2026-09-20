"""Input 4 (variant B): pysam alternative. SKILL.md 'pysam Python Alternative' + usage-guide 'Python with pysam' code, verbatim
(copied from the Skill), executed on planted_dups.bam (truth 100 dup reads) and the real human BAM (samtools/Picard/sambamba/samblaster agree: 1656).
Assertions are printed as ASSERT lines."""
import os, sys, shutil, subprocess
import pysam
W = "/mnt/openscience/audits/bio-duplicate-handling/run/work/in04"
D = "/mnt/openscience/audits/bio-duplicate-handling/run/data"
shutil.rmtree(W, ignore_errors=True); os.makedirs(W); os.chdir(W)
print("pysam", pysam.__version__, "samtools", pysam.__samtools_version__)

def A(cond, msg):
    print(("ASSERT PASS " if cond else "ASSERT FAIL ") + msg); return cond

# ---------- SKILL.md 'Full Pipeline' (verbatim) ----------
def skill_md_full_pipeline(inp):
    pysam.sort('-n', '-o', 'namesort.bam', inp)
    pysam.fixmate('-m', 'namesort.bam', 'fixmate.bam')
    pysam.sort('-o', 'coordsort.bam', 'fixmate.bam')
    pysam.markdup('coordsort.bam', 'marked.bam')
    pysam.index('marked.bam')

# ---------- SKILL.md 'Check Duplicate Flag' (verbatim) ----------
def skill_md_check(path):
    with pysam.AlignmentFile(path, 'rb') as bam:
        total = 0
        duplicates = 0
        for read in bam:
            total += 1
            if read.is_duplicate:
                duplicates += 1
        print(f'Total: {total}')
        print(f'Duplicates: {duplicates}')
        print(f'Rate: {duplicates/total*100:.2f}%')
    return total, duplicates

# ---------- SKILL.md 'Filter Out Duplicates' (verbatim) ----------
def skill_md_filter(inp, outp):
    with pysam.AlignmentFile(inp, 'rb') as infile:
        with pysam.AlignmentFile(outp, 'wb', header=infile.header) as outfile:
            for read in infile:
                if not read.is_duplicate:
                    outfile.write(read)

# ---------- usage-guide functions (verbatim) ----------
def mark_duplicates(input_bam, output_bam, threads=4):
    temp_ns = 'temp_namesort.bam'
    temp_fm = 'temp_fixmate.bam'
    temp_cs = 'temp_coordsort.bam'

    try:
        pysam.sort('-n', '-@', str(threads), '-o', temp_ns, input_bam)
        pysam.fixmate('-m', '-@', str(threads), temp_ns, temp_fm)
        pysam.sort('-@', str(threads), '-o', temp_cs, temp_fm)
        pysam.markdup('-@', str(threads), temp_cs, output_bam)
        pysam.index(output_bam)
    finally:
        for f in [temp_ns, temp_fm, temp_cs]:
            if os.path.exists(f):
                os.remove(f)

def duplicate_rate(bam_path):
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        total, duplicates = 0, 0
        for read in bam:
            if read.is_secondary or read.is_supplementary:
                continue
            total += 1
            if read.is_duplicate:
                duplicates += 1
    return {'total': total, 'duplicates': duplicates, 'rate': duplicates / total * 100 if total > 0 else 0}

def remove_duplicates(input_bam, output_bam):
    with pysam.AlignmentFile(input_bam, 'rb') as infile:
        with pysam.AlignmentFile(output_bam, 'wb', header=infile.header) as outfile:
            for read in infile:
                if not read.is_duplicate:
                    outfile.write(read)

def samtools_c(*a):
    return int(subprocess.check_output(['samtools', 'view', '-c', *a]).decode())

for name, truth in [("planted_dups", 100), ("test.paired_end.sorted", 1656)]:
    print(f"\n===== {name}: truth flagged reads = {truth}")
    inp = f"{D}/{name}.bam"
    skill_md_full_pipeline(inp)
    tot, dup = skill_md_check('marked.bam')
    A(dup == truth, f"SKILL.md pysam pipeline flags {dup} reads == truth {truth}")
    A(os.path.exists('marked.bam.bai'), "pysam.index wrote marked.bam.bai")
    A(samtools_c('-f', '1024', 'marked.bam') == dup, "pysam count == samtools view -c -f 1024")
    skill_md_filter('marked.bam', 'nodup.bam')
    n_nodup = samtools_c('nodup.bam')
    A(n_nodup == tot - dup, f"SKILL.md filter keeps {n_nodup} == total-dups {tot-dup}")
    mark_duplicates(inp, 'marked2.bam', threads=2)
    A(samtools_c('-f', '1024', 'marked2.bam') == truth, "usage-guide mark_duplicates() flags truth")
    A(not any(f.startswith('temp_') for f in os.listdir('.')), "mark_duplicates() cleaned its temp files")
    r = duplicate_rate('marked2.bam')
    print("usage-guide duplicate_rate:", r)
    pri = samtools_c('-F', '256', '-F', '2048', 'marked2.bam')
    A(r['total'] == pri, f"duplicate_rate total {r['total']} == primary count {pri}")
    remove_duplicates('marked2.bam', 'nodup2.bam')
    A(samtools_c('nodup2.bam') == samtools_c('-F', '1024', 'marked2.bam'), "remove_duplicates output == samtools view -F 1024")
    print(f"SKILL.md rate (all records): {dup/tot*100:.2f}%  usage-guide rate (primary only): {r['rate']:.2f}%")

print("\n===== failure behaviour: pysam.markdup on coordinate-sorted input without fixmate")
try:
    pysam.markdup(f"{D}/planted_dups.bam", 'bad.bam')
    print("ASSERT FAIL pysam.markdup did not raise on missing ms tag; bad.bam records:", samtools_c('bad.bam') if os.path.exists('bad.bam') else 'missing')
except Exception as e:
    print("ASSERT PASS raised", type(e).__name__, ":", str(e)[:120].replace("\n", " "))
print("\n===== failure behaviour: mark_duplicates() on a missing input")
try:
    mark_duplicates('nope.bam', 'o.bam')
    print("ASSERT FAIL no exception for missing input")
except Exception as e:
    print("ASSERT PASS raised", type(e).__name__, ":", str(e)[:100].replace("\n", " "))
print("\n===== pysam.markdup return value on success (stderr/-s stats capture)")
out = pysam.markdup('-s', 'coordsort.bam', 'ms.bam', catch_stdout=False) if os.path.exists('coordsort.bam') else None
print("pysam.markdup('-s',...) returned:", repr(out)[:80])

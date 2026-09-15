"""Post-fix regression runs for bio-clinical-databases-dbsnp-queries (re-audit 2026-09-15).
Same five requests as the pre-fix runs/run_all.py, now against the fork commit's SKILL.md code (p_skill_code.py) and
example (dbsnp_lookup.fork_copy.py). Live NCBI Variation Services v0 and myvariant.info (HTTPS). usage: python p_run_all.py in1|...|in7
Writes to p_<input>/out.txt when called through the shell loop."""
import json, os, sys, time, requests, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p_skill_code as sk
spec = importlib.util.spec_from_file_location('ex', os.path.join(HERE, 'dbsnp_lookup.fork_copy.py'))
ex = importlib.util.module_from_spec(spec); spec.loader.exec_module(ex)
nap = lambda: time.sleep(0.4)


def in1():
    """Canonical: 'Resolve rs429358 (APOE): GRCh38 coordinates, alleles, gene, merge history.'"""
    s = sk.summarize_refsnp(sk.refsnp('rs429358')); nap()
    print('SKILL.md summarize_refsnp(rs429358):', json.dumps(s))
    print('\n== shipped example __main__ (fork commit) ==')
    import subprocess
    print(subprocess.run([sys.executable, os.path.join(HERE, 'dbsnp_lookup.fork_copy.py')], capture_output=True, text=True, cwd=HERE).stdout)


def in2():
    """Variant A: 'A 2004 paper cites rs630496 -- trace it to the current rsID.'"""
    print('SKILL.md resolve_merge_chain(rs630496):', sk.resolve_merge_chain('rs630496')); nap()
    print('example resolve_merge_chain(rs630496):', ex.resolve_merge_chain('rs630496')); nap()
    print('SKILL.md resolve_merge_chain(rs429358):', sk.resolve_merge_chain('rs429358'))


def in3():
    """Edge: 'Is rs334 multi-allelic, and what happens with a withdrawn or nonexistent rsID?'"""
    s = sk.summarize_refsnp(sk.refsnp('rs334')); nap()
    print('SKILL.md summarize_refsnp(rs334): alleles', [(a['ref'], a['alt']) for a in s['placements_grch38']], 'is_multiallelic =', s['is_multiallelic'])
    al = ex.alleles_grch38(sk.refsnp('rs334')); nap()
    print('example alleles_grch38(rs334):', [(a['ref'], a['alt']) for a in al], '-> multi-allelic', len(al) > 1)
    for rid in ('rs1', 'rs999999999999'):
        print(rid, 'SKILL resolve_merge_chain ->', sk.resolve_merge_chain(rid)); nap()


def in4():
    """Variant B: 'Convert APOE chr19:44908684 T>C and BRCA1 chr17:43106487 A>C (VCF, GRCh38) to canonical SPDI and rsIDs.'"""
    for c, pos, ref, alt in (('19', 44908684, 'T', 'C'), ('chr17', 43106487, 'A', 'C'), ('X', 154536002, 'C', 'T'), ('17', 43094464, 'G', 'A')):
        try:
            s = sk.vcf_to_canonical_spdi(c, pos, ref, alt); nap()
            print(f'{c}:{pos} {ref}>{alt} -> SPDI {s} -> rsID {sk.spdi_to_rsid(s)}'); nap()
        except ValueError as e:
            print(f'{c}:{pos} {ref}>{alt} -> ValueError: {str(e)[:200]}')
    print('hgvs_to_spdi_canonical(NM_000059.3:c.5946delT) ->', sk.hgvs_to_spdi_canonical('NM_000059.3:c.5946delT'))


def in5():
    """Stress: 'For rs6025, rs1799963, rs429358, rs7412 and rs121913529: current rsID, multi-allelic flag, ALFA total frequency,
    gnomAD AF and ClinVar significance in one table.'"""
    for rid in ('rs6025', 'rs1799963', 'rs429358', 'rs7412', 'rs121913529'):
        print('SKILL alfa_frequency(%s, Total):' % rid, sk.alfa_frequency(rid)); nap()
    print('SKILL alfa_frequency(rs6025, European):', sk.alfa_frequency('rs6025', 'European')); nap()
    import pandas as pd
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 20)
    df = ex.batch_normalize_rsids(['rs6025', 'rs1799963', 'rs429358', 'rs7412', 'rs121913529'])
    print(df.to_string(index=False))


def in6():
    """NEW Edge: 'Our pipeline writes the BRCA2 homopolymer deletion rs80359550 at the right end of the T run, the other lab
    left-aligned. Do both give the same canonical SPDI and rsID?' Reference bases fetched live from NCBI efetch (NC_000013.11)."""
    lo, hi = 32340280, 32340320
    fa = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi', params={'db': 'nuccore', 'id': 'NC_000013.11', 'rettype': 'fasta', 'seq_start': lo, 'seq_stop': hi}, timeout=30).text; nap()
    seq = ''.join(fa.split('\n')[1:]).strip()
    print(f'NC_000013.11:{lo}-{hi} = {seq}')
    # longest homopolymer in the window (TTTTT here); VCF anchors for deleting its first vs its last base
    runs, k = [], 0
    while k < len(seq):
        j = k
        while j + 1 < len(seq) and seq[j + 1] == seq[k]: j += 1
        runs.append((j - k + 1, k, j)); k = j + 1
    _, s, e = max(runs)
    base = seq[s]
    left_pos, right_pos = lo + s - 1, lo + e - 1
    reps = [(left_pos, seq[s - 1] + base, seq[s - 1]), (right_pos, seq[e - 1] + base, seq[e - 1])]
    print(f'run of {base} at {lo + s}-{lo + e}; left-aligned VCF {reps[0]}, right-shifted VCF {reps[1]}')
    for pos, ref, alt in reps:
        try:
            sp = sk.vcf_to_canonical_spdi('13', pos, ref, alt); nap()
            print(f'13:{pos} {ref}>{alt} -> canonical SPDI {sp} -> rsID {sk.spdi_to_rsid(sp)}'); nap()
        except ValueError as err:
            print(f'13:{pos} {ref}>{alt} -> ValueError {err}')


def in7():
    """NEW Variant C: 'Normalize this messy rsID list from an old genotyping manifest: rs630496, rs429358, rs429358, rs999999999999, rs334.'"""
    import pandas as pd
    pd.set_option('display.width', 250); pd.set_option('display.max_columns', 20)
    df = ex.batch_normalize_rsids(['rs630496', 'rs429358', 'rs429358', 'rs999999999999', 'rs334'])
    print(df.to_string(index=False))


if __name__ == '__main__':
    globals()[sys.argv[1]]()

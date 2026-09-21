"""NEW input data (auditor-made, SYNTHETIC): single-end stranded libraries derived from the planted PE BAMs, and a MAPQ-1 copy.
SE dUTP = read1 of pe_dutp (antisense), SE forward = read1 of pe_fwd. Usage: python 30_in3_make_se.py <synthetic dir> <out dir>"""
import sys, pysam
src, out = sys.argv[1], sys.argv[2]
def se_from_pe(inp, outp):
    with pysam.AlignmentFile(inp) as f, pysam.AlignmentFile(outp, 'wb', header=f.header) as o:
        n = 0
        for r in f.fetch(until_eof=True):
            if r.is_read1 and not r.is_unmapped:
                r.flag = r.flag & 16; r.next_reference_id = -1; r.next_reference_start = -1; r.template_length = 0; o.write(r); n += 1
    pysam.index(outp); return n
print('se_dutp reads', se_from_pe(f'{src}/pe_dutp.bam', f'{out}/se_dutp.bam'))
print('se_fwd reads', se_from_pe(f'{src}/pe_fwd.bam', f'{out}/se_fwd.bam'))
with pysam.AlignmentFile(f'{src}/pe_dutp.bam') as f, pysam.AlignmentFile(f'{out}/pe_dutp_mapq1.bam', 'wb', header=f.header) as o:
    for r in f.fetch(until_eof=True):
        r.mapping_quality = 1; o.write(r)
pysam.index(f'{out}/pe_dutp_mapq1.bam'); print('mapq1 written')

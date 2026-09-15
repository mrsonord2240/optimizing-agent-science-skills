# Input 2 (variant A: codon alignment for codeml) -- following SKILL.md "Codon-Aware Alignment"
# Decision table: clean orthologs (no frameshifts, no internal stops) -> MAFFT-protein + PAL2NAL.
# Env adaptation (Windows): 'mafft.bat' launcher; pal2nal.pl invoked through 'perl'.
import subprocess
from Bio import SeqIO, AlignIO
from Bio.SeqRecord import SeqRecord

MAFFT = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\mafft-win\mafft.bat'
PAL2NAL = r'F:\OpenScience\audit-envs\molecular-phylogenetics-analyst\tools\bin\pal2nal.pl'

# 0. pre-flight: confirm the input is "clean orthologs" (frame intact, no internal stops) -- decides PAL2NAL vs MACSE
cds = list(SeqIO.parse('cds10_cds.fa', 'fasta'))
prot = []
for r in cds:
    assert len(r.seq) % 3 == 0, f'{r.id}: length {len(r.seq)} not a multiple of 3 -> frameshift? use MACSE'
    aa = r.seq.translate(table=1)
    assert '*' not in aa[:-1], f'{r.id}: internal stop -> use MACSE / HyPhy pre-msa'
    prot.append(SeqRecord(aa.rstrip('*'), id=r.id, description=''))
SeqIO.write(prot, 'proteins.fasta', 'fasta')
print(f'{len(cds)} CDS, all in frame, no internal stops -> MAFFT-protein + PAL2NAL')

# 1. align proteins (L-INS-i) -- SKILL.md PAL2NAL block
with open('proteins_aligned.fasta', 'w') as out:
    r = subprocess.run([MAFFT, '--localpair', '--maxiterate', '1000', 'proteins.fasta'], stdout=out,
                       stderr=subprocess.PIPE, text=True)
if r.returncode:
    raise RuntimeError(r.stderr)
# 2. thread codons (standard code, table 1)
for fmt, fn in (('fasta', 'codons_aligned.fasta'), ('paml', 'codons_aligned.phy')):
    with open(fn, 'w') as out:
        r = subprocess.run(['perl', PAL2NAL, 'proteins_aligned.fasta', 'cds10_cds.fa', '-output', fmt,
                            '-codontable', '1'], stdout=out, stderr=subprocess.PIPE, text=True)
    if r.returncode:
        raise RuntimeError(r.stderr)

# 3. validate: frame preserved in every sequence (HyPhy post-msa-style check)
aln = AlignIO.read('codons_aligned.fasta', 'fasta')
L = aln.get_alignment_length()
print(f'codon alignment: {len(aln)} x {L} nt ({L//3} codons); length %3 = {L%3}')
bad = []
for rec in aln:
    s = str(rec.seq)
    for i in range(0, L, 3):
        cod = s[i:i+3]
        if 0 < cod.count('-') < 3:
            bad.append((rec.id, i // 3)); break
    if s.replace('-', '') != str(next(c.seq for c in cds if c.id == rec.id)):
        bad.append((rec.id, 'sequence altered'))
print('frame-breaking codons / altered sequences:', bad or 'none')

# Input 7: what the requested shortcut (nucleotide MAFFT --auto on CDS) does to the reading frame,
# versus the Skill's protein-first + PAL2NAL route (Input 2 output).
from Bio import AlignIO
for label, f in (('nucleotide MAFFT --auto (requested shortcut)', 'dna_auto.fasta'),
                 ('MAFFT-protein + PAL2NAL (Skill route)', '../in2/codons_aligned.fasta')):
    aln = AlignIO.read(f, 'fasta'); L = aln.get_alignment_length()
    broken_cols = set(); seqs_broken = 0
    for r in aln:
        s = str(r.seq); hit = False
        for i in range(0, L - L % 3, 3):
            if 0 < s[i:i+3].count('-') < 3:
                broken_cols.add(i // 3); hit = True
        seqs_broken += hit
    print(f'{label}: {L} nt (L%3={L%3}); codon columns with a partial-codon gap: {len(broken_cols)}; sequences affected: {seqs_broken}/{len(aln)}')

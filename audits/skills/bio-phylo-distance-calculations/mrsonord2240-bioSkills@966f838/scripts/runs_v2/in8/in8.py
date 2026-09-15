# Input 8 (NEW, Edge): gapped barcode alignment. The fixed Skill says Bio.Phylo 'identity' is p-distance only on
# ungapped alignments and to strip gap columns first. SYNTHETIC: barcode20 with a 30-bp deletion in 3 sequences and
# a 12-bp insertion column block in 2 others (gaps inserted by the auditor, true tree unchanged).
import sys
sys.path.insert(0, '..')
from phylo_util import rf_to_true
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

TRUE = '../../data/barcode20_true.nwk'
src = AlignIO.read('../../data/barcode20.fa', 'fasta')
recs = []
for i, r in enumerate(src):
    s = str(r.seq)
    s = s[:300] + ('GATTACAGATTA' if i in (4, 11) else '------------') + s[300:]
    if i in (2, 7, 15):
        s = s[:100] + '-' * 30 + s[130:]
    recs.append(SeqRecord(Seq(s), id=r.id.strip(), description=''))
aln = MultipleSeqAlignment(recs)
AlignIO.write(aln, 'barcode20_gapped.fa', 'fasta')
dm = DistanceCalculator('identity').get_distance(aln)
keep = [j for j in range(aln.get_alignment_length()) if all(str(r.seq)[j] != '-' for r in aln)]
ungapped = MultipleSeqAlignment([SeqRecord(Seq(''.join(str(r.seq)[j] for j in keep)), id=r.id, description='') for r in aln])
dm2 = DistanceCalculator('identity').get_distance(ungapped)
a, b = aln[0].id, aln[2].id
print('columns', aln.get_alignment_length(), '-> gap-free', len(keep))
print('identity %s-%s gapped %.4f | gap-stripped %.4f' % (a, b, dm[a, b], dm2[a, b]))
print('identity NJ RF gapped %d/%d | gap-stripped %d/%d' % (*rf_to_true(DistanceTreeConstructor().nj(dm), TRUE),
                                                           *rf_to_true(DistanceTreeConstructor().nj(dm2), TRUE)))

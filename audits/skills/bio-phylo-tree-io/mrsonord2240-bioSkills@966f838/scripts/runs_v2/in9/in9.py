"""Input 9 (NEW, Edge): the fixed Skill's encoding note says path-based Phylo.read/write and DendroPy path= use the
Windows locale codec. Test both directions on a SYNTHETIC UTF-8 Newick with accented names, then the Skill's handle fix."""
import locale, sys
from io import StringIO
from Bio import Phylo
import dendropy

print('python', sys.version.split()[0], '| preferred encoding', locale.getpreferredencoding(False), '| utf8_mode', sys.flags.utf8_mode)
nwk = "((Cercopithèque_ascagne:0.1,Saïmiri_boliviensis:0.2):0.05,(Ölandsk_kanin:0.3,Homo_sapiens:0.1):0.05);\n"
open('accented.nwk', 'w', encoding='utf-8').write(nwk)
want = sorted(['Cercopithèque_ascagne', 'Saïmiri_boliviensis', 'Ölandsk_kanin', 'Homo_sapiens'])
t = Phylo.read('accented.nwk', 'newick')
print('Bio.Phylo path read correct:', sorted(x.name for x in t.get_terminals()) == want, [x.name for x in t.get_terminals()][:2])
d = dendropy.Tree.get(path='accented.nwk', schema='newick', preserve_underscores=True)
print('DendroPy path= read correct:', sorted(x.label for x in d.taxon_namespace) == want, [x.label for x in d.taxon_namespace][:2])
# Skill fix: explicit handles both ways
with open('accented.nwk', encoding='utf-8') as fh:
    t2 = Phylo.read(fh, 'newick')
with open('rt.nwk', 'w', encoding='utf-8') as fh:
    Phylo.write(t2, fh, 'newick')
with open('rt.nwk', encoding='utf-8') as fh:
    t3 = Phylo.read(fh, 'newick')
print('UTF-8 handle round trip correct:', sorted(x.name for x in t3.get_terminals()) == want)
Phylo.write(t2, 'rt_path.nwk', 'newick')
try:
    with open('rt_path.nwk', encoding='utf-8') as fh:
        print('path-written file re-read as UTF-8 correct:', sorted(x.name for x in Phylo.read(fh, 'newick').get_terminals()) == want)
except UnicodeDecodeError as e:
    print('path-written file is not UTF-8:', str(e)[:80])

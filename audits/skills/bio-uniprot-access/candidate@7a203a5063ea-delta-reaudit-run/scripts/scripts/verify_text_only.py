import hashlib,ast,pathlib,json
t=pathlib.Path('F:/OpenScience/wt/dbaccess-uniprot-access/skills/bio-uniprot-access')
c={f['path']:f['sha256'] for f in json.load(open('F:/OpenScience/audits/bio-uniprot-access/reaudit-run/source-identity.json'))['files']}
new="~38 MB compressed; ~87 MB unpacked; ~147.5K entries (reviewed + TrEMBL)"
old="~20 MB compressed; ~80 MB unpacked; ~20K proteins"
p='examples/isoforms_and_xrefs.py'
b=(t/p).read_bytes().replace(new.encode(),old.encode())
print('py reverted==certified',hashlib.sha256(b).hexdigest()==c[p])
n=ast.parse((t/p).read_text(encoding='utf-8'));o=ast.parse(b.decode())
diffs=[(x.value,y.value) for x,y in zip(ast.walk(n),ast.walk(o)) if ast.dump(x,False)!=ast.dump(y,False) and isinstance(x,ast.Constant)]
print(len(list(ast.walk(n)))==len(list(ast.walk(o))),diffs)
p='SKILL.md'
newc="Download whole proteome, reviewed and unreviewed TrEMBL entries alike (human UP000005640: 147,520 entries, 37.8 MB gzip); add `AND reviewed:true` to the query for Swiss-Prot only (`/proteomes/{upid}.fasta.gz` returns 400)"
oldc="Download whole proteome (`/proteomes/{upid}.fasta.gz` returns 400)"
b=(t/p).read_bytes().replace(newc.encode(),oldc.encode())
print('md reverted==certified',hashlib.sha256(b).hexdigest()==c[p])

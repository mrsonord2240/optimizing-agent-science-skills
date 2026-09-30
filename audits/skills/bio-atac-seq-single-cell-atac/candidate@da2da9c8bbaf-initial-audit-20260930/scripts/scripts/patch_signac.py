# builds a patched COPY of the Skill script for tooling smoke (Skill bytes untouched)
import sys
s=open(sys.argv[1],encoding='utf-8').read()
a="annotation=GetGRangesFromEnsDb(EnsDb.Hsapiens.v86),"
assert a in s
s=s.replace(a,"annotation=ann,")
b="    counts <- Read10X_h5(h5_file)"
assert b in s
s=s.replace(b,"    ann <- GetGRangesFromEnsDb(EnsDb.Hsapiens.v86); seqlevelsStyle(ann) <- 'UCSC'; genome(ann) <- 'hg38'\n"+b)
c="TSS.enrichment > 4)"
assert c in s
s=s.replace(c,"TSS.enrichment > %s)"%sys.argv[3])
open(sys.argv[2],'w',encoding='utf-8',newline='\n').write(s)

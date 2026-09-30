import pysam,sys
src,dst=sys.argv[1:3]
i=pysam.AlignmentFile(src); h=i.header.to_dict()
h['SQ'][0]['SN']='1'; h['SQ'][1]['SN']='MT'
with pysam.AlignmentFile(dst,'wb',header=h) as o:
    for r in i.fetch(until_eof=True):
        o.write(r)
pysam.index(dst)

# -*- coding: utf-8 -*-
import json, io, collections
p = 'eval_report_bio-pathway-gsea_result.json'
r = json.load(io.open(p, encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
new = {
 "nPerm is accepted, not rejected, and silently downgrades the engine": "nPerm is accepted and silently downgrades the engine",
 "pmax(p, 1e-300) turns four genes into 16% of the ranking's weight": "pmax(p, 1e-300) makes 4 genes 16% of the ranking weight",
 "The prescribed CAMERA call does not apply the correction the Skill credits it with": "Prescribed CAMERA call omits inter.gene.cor = NA",
 "Unsorted and duplicated geneLists are hard errors, not silent mis-ranking": "Unsorted/duplicated geneList is a hard error, not silent",
 "Both shipped examples return zero enriched terms by construction": "Shipped examples return zero terms by construction",
 "The ID-mismatch path ends in an error the Common Errors table does not list": "ID-mismatch ends in an error Common Errors omits",
}
for x in r['recommendations']:
    if x['title'] in new:
        x['title'] = new[x['title']]
    assert len(x['title']) <= 60, x['title']
io.open(p, 'w', encoding='utf-8').write(json.dumps(r, indent=2, ensure_ascii=False) + '\n')
print('titles shortened')

import os, sys; sys.path.insert(0, '.'); os.chdir('scratch')
from pdfcheck import pdf_info, pdf_text
for f in ['pca.pdf', 'multipanel.pdf', 'heatmap.pdf', 'volcano_sns.pdf', 'volcano_so.pdf']:
    if not os.path.exists(f): print(f, 'MISSING'); continue
    i = pdf_info(f); t = pdf_text(f)
    print(f, {k: i[k] for k in ('bytes', 'size_mm', 'type3_fonts', 'truetype_fonts', 'image_xobjects', 'font_sizes_pt', 'fontnames')}, '| text:', repr(t.replace('\n\n', ' ')[:110]))

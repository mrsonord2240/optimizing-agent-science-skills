import sys
sys.path.insert(0, r'F:\OpenScience\audits\bio-data-visualization-multipanel-figures\run')
from bbox import words
OUT = r'F:\OpenScience\audits\bio-data-visualization-multipanel-figures\out'
for n, exp in [('c_row2','y-title 1, x-title 1'),('c_col2','x 1,y 1'),('c_wrap22','x 2, y 2'),('c_plus_ncol2','x 2, y 2'),('c_nested_top','x 2,y 2 expected'),('c_nested_all','x 2,y 2 expected'),('c_nested_nolayout','baseline 4/4')]:
    W,H,ws = words(f'{OUT}\{n}.bbox.html')
    nums=[x for x in ws if x[0].lstrip('-').replace('.','').isdigit()]
    print(f"{n:20s} x-title={sum(1 for x in ws if x[0]=='x')} y-title={sum(1 for x in ws if x[0]=='y')} tick words={len(nums)}   (fully collected would be: {exp})")

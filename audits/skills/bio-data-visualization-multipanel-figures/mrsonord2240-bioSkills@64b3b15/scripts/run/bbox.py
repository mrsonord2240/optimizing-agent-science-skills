import re, sys, html
def words(path):
    t = open(path, encoding='utf-8').read()
    pg = re.search(r'<page width="([\d.]+)" height="([\d.]+)"', t)
    W, H = float(pg.group(1)), float(pg.group(2))
    ws = [(html.unescape(m.group(5)), float(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)))
          for m in re.finditer(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>', t)]
    return W, H, ws
if __name__ == '__main__':
    W, H, ws = words(sys.argv[1]); print('page pt', W, H, 'mm', round(W/72*25.4,1), round(H/72*25.4,1))
    for w in ws: print('%-14s x=%.1f-%.1f y=%.1f-%.1f h=%.1f' % (w[0], w[1], w[3], w[2], w[4], w[4]-w[2]))

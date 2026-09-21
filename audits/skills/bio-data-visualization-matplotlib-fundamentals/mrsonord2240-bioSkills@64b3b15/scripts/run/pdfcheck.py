"""Helpers: inspect a matplotlib PDF without poppler. Raw regex on the object dictionaries plus zlib on the content streams."""
import re, zlib, subprocess, sys

def pdf_info(path):
    b = open(path, 'rb').read()
    info = {'bytes': len(b)}
    m = re.search(rb'/MediaBox\s*\[\s*([\d.\- ]+)\]', b)
    if m:
        v = [float(x) for x in m.group(1).split()]
        info['mediabox_pt'] = v
        info['size_mm'] = (round((v[2]-v[0])/72*25.4, 2), round((v[3]-v[1])/72*25.4, 2))
    info['type3_fonts'] = len(re.findall(rb'/Subtype\s*/Type3', b))
    info['truetype_fonts'] = len(re.findall(rb'/Subtype\s*/TrueType', b)) + len(re.findall(rb'/Subtype\s*/CIDFontType2', b))
    info['type1_fonts'] = len(re.findall(rb'/Subtype\s*/Type1\b', b))
    info['fontnames'] = sorted({x.decode() for x in re.findall(rb'/FontName\s*/([A-Za-z0-9+\-_]+)', b)})
    info['image_xobjects'] = len(re.findall(rb'/Subtype\s*/Image', b))
    # font sizes from content streams
    sizes = set()
    for sm in re.finditer(rb'stream\r?\n(.*?)\r?\nendstream', b, re.S):
        raw = sm.group(1)
        try:
            d = zlib.decompress(raw)
        except Exception:
            d = raw
        for t in re.findall(rb'/F\d+\s+([\d.]+)\s+Tf', d):
            sizes.add(float(t))
    info['font_sizes_pt'] = sorted(sizes)
    return info

def pdf_text(path):
    try:
        r = subprocess.run(['pdftotext', '-q', path, '-'], capture_output=True, text=True, encoding='utf-8', errors='replace')
        return r.stdout
    except Exception as e:
        return 'ERR ' + str(e)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(p, pdf_info(p))

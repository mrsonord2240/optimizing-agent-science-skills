"""Minimal PDF inspector (no pdf libs installed): MediaBox, embedded font programs, Type3, images.
Usage: py.sh pdfinfo.py file.pdf [...]. Decompresses /ObjStm streams so cairo's PDF 1.7 output is readable."""
import re, sys, zlib

def corpus(b):
    text = b.decode('latin1')
    extra = []
    for m in re.finditer(rb'<<(?:(?!endobj).)*?/ObjStm(?:(?!endobj).)*?>>\s*stream\r?\n', b, re.S):
        start = m.end()
        end = b.find(b'endstream', start)
        try:
            extra.append(zlib.decompress(b[start:end].rstrip(b'\r\n')).decode('latin1'))
        except Exception:
            pass
    return text + '\n'.join(extra)

def info(path):
    b = open(path, 'rb').read()
    t = corpus(b)
    mb = re.findall(r'/MediaBox\s*\[([^\]]*)\]', t)
    boxes = []
    for x in mb:
        v = [float(z) for z in x.split()]
        boxes.append((round(v[2] - v[0], 2), round(v[3] - v[1], 2)))
    fonts = sorted(set(re.findall(r'/BaseFont\s*/([A-Za-z0-9+_,-]+)', t)))
    out = dict(file=path.split('\\')[-1].split('/')[-1], bytes=len(b), pdf_version=b[:8].decode('latin1').strip(),
               mediabox_pt=boxes[:1], mediabox_mm=[(round(w / 72 * 25.4, 1), round(h / 72 * 25.4, 1)) for w, h in boxes[:1]],
               FontFile2_truetype=len(re.findall(r'/FontFile2', t)), FontFile3=len(re.findall(r'/FontFile3', t)),
               FontFile_type1=len(re.findall(r'/FontFile(?![23])', t)), Type3=len(re.findall(r'/Subtype\s*/Type3', t)),
               Type1_unembedded=len(re.findall(r'/Subtype\s*/Type1\b', t)) - len(re.findall(r'/FontFile(?![23])', t)),
               images=len(re.findall(r'/Subtype\s*/Image', t)), basefonts=fonts)
    return out

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print(info(p))

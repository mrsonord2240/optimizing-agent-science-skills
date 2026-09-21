from PIL import Image
im = Image.open(r'F:\OpenScience\audits\bio-data-visualization-ggplot2-fundamentals\run\out_4.0.3\i4_fig.tiff')
print('size', im.size, 'mode', im.mode, 'compression', im.info.get('compression'), 'dpi', im.info.get('dpi'), 'tag259', im.tag_v2.get(259))

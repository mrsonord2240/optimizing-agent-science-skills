#!/usr/bin/env python3
"""Print every <text> string of an SVG in document order (ggsashimi writes arc counts and axis ticks as text)."""
import sys, xml.etree.ElementTree as ET
for el in ET.parse(sys.argv[1]).iter():
    if el.tag.endswith('text'):
        s = ''.join(el.itertext()).strip()
        if s: print(s)

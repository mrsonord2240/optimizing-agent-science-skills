#!/usr/bin/env python3
"""Extract all <text> strings from a ggsashimi SVG in document order (junction counts are text labels)."""
import sys, re
import xml.etree.ElementTree as ET
t = ET.parse(sys.argv[1])
for el in t.iter():
    if el.tag.endswith('text'):
        s = ''.join(el.itertext()).strip()
        if s:
            print(s)

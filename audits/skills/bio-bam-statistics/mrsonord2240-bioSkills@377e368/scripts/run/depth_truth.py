#!/usr/bin/env python3
"""Shared helper: truth per-base depth from alignment blocks (truth.py, no pileup engine) and the Skill's region_depth_stats (block 030) exec'd from the extracted block."""
import sys, re
sys.path.insert(0, '/mnt/openscience/audits/bio-bam-statistics/run')
import numpy as np, pysam, truth
def load_block030():
    src = open('/mnt/openscience/audits/bio-bam-statistics/run/blocks/030_python.py', encoding='utf-8').read()
    ns = {}
    exec(src.split('stats = region_depth_stats(')[0], ns)   # defs only (imports + function); the call line is run separately
    return ns['region_depth_stats']
def summarize(d, L=None):
    L = L or len(d)
    return dict(length=L, mean=float(d.sum()) / L, covered=int((d > 0).sum()), pct_cov=100.0 * (d > 0).sum() / L,
                ge10=100.0 * (d >= 10).sum() / L, ge20=100.0 * (d >= 20).sum() / L, mx=int(d.max()))

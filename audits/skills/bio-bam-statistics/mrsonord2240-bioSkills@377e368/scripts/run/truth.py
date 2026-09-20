#!/usr/bin/env python3
"""Independent ground-truth computations for the audit (NOT from the Skill).

counts(): hand-count every flag category straight from record flags, with primary/secondary/supplementary
          and QC-fail split out, following the SAM spec (not any of the tools under test).
depth_arrays(): per-base depth from alignment blocks (read.get_blocks()), no pileup engine, so it is independent of
          samtools depth / mosdepth / pysam pileup. Options mimic each tool's documented defaults.
"""
import sys, json
import numpy as np
import pysam

UNMAP, SECONDARY, QCFAIL, DUP, SUPP = 4, 256, 512, 1024, 2048


def counts(path):
    c = dict(total=0, primary=0, secondary=0, supplementary=0, unmapped=0, mapped=0, primary_mapped=0,
             duplicates=0, primary_duplicates=0, qcfail=0, paired_primary=0, read1=0, read2=0, proper_primary=0,
             singletons=0, mate_diff_chr=0, mate_diff_chr_mq5=0, both_mapped_primary=0, mq0_primary_mapped=0,
             softclipped_bases=0, mapped_ge_q30_primary=0, nm_sum=0, cigar_bases=0, mapped_and_paired_primary=0)
    with pysam.AlignmentFile(path, 'rb', check_sq=False) as bam:   # audit patch: allow uBAM with no @SQ
        for r in bam.fetch(until_eof=True):
            f = r.flag
            c['total'] += 1
            if f & QCFAIL:
                c['qcfail'] += 1
            sec, sup = bool(f & SECONDARY), bool(f & SUPP)
            if sec: c['secondary'] += 1
            if sup: c['supplementary'] += 1
            if f & UNMAP: c['unmapped'] += 1
            else: c['mapped'] += 1
            if f & DUP: c['duplicates'] += 1
            if sec or sup:
                continue
            c['primary'] += 1
            if f & DUP: c['primary_duplicates'] += 1
            if not f & UNMAP:
                c['primary_mapped'] += 1
                if r.mapping_quality == 0: c['mq0_primary_mapped'] += 1
                if r.mapping_quality >= 30: c['mapped_ge_q30_primary'] += 1
                for op, n in (r.cigartuples or []):
                    if op == 4: c['softclipped_bases'] += n
                    if op in (0, 7, 8): c['cigar_bases'] += n
                if r.has_tag('NM'): c['nm_sum'] += r.get_tag('NM')
            if f & 1:
                c['paired_primary'] += 1
                if f & 64: c['read1'] += 1
                if f & 128: c['read2'] += 1
                mapped = not f & UNMAP
                mate_mapped = not f & 8
                if mapped and mate_mapped:
                    c['both_mapped_primary'] += 1
                    if r.reference_id != r.next_reference_id:
                        c['mate_diff_chr'] += 1
                        if r.mapping_quality >= 5: c['mate_diff_chr_mq5'] += 1
                if mapped and not mate_mapped: c['singletons'] += 1
                if (f & 2) and mapped: c['proper_primary'] += 1
    return c


def depth_arrays(path, contig, length, excl=UNMAP | SECONDARY | QCFAIL | DUP, min_mq=0, no_overlap=False):
    """Depth from alignment blocks. no_overlap=True: a template's two mates count a base once (samtools depth -s / mosdepth default)."""
    d = np.zeros(length, dtype=np.int64)
    if not no_overlap:
        with pysam.AlignmentFile(path, 'rb') as bam:
            for r in bam.fetch(contig):
                if r.flag & excl or r.mapping_quality < min_mq:
                    continue
                for s, e in r.get_blocks():
                    d[s:e] += 1
        return d
    seen = {}
    with pysam.AlignmentFile(path, 'rb') as bam:
        for r in bam.fetch(contig):
            if r.flag & excl or r.mapping_quality < min_mq:
                continue
            m = np.zeros(length, dtype=bool)
            for s, e in r.get_blocks():
                m[s:e] = True
            key = r.query_name if r.is_paired else id(r)
            if key in seen and r.is_paired:
                seen[key] |= m
            else:
                seen[key] = m
    for m in seen.values():
        d += m.astype(np.int64)
    return d


if __name__ == '__main__':
    print(json.dumps(counts(sys.argv[1]), indent=1))

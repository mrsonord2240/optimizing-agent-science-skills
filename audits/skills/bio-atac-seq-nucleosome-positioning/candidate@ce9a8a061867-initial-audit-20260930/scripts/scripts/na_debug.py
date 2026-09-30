# Diagnose empty nucpos: instrument NucChunk.findAllNucs (shared atac-nucleo py2.7, read-only; nothing installed/modified)
import sys
import numpy as np
import nucleoatac.NucleosomeCalling as NC
from nucleoatac.multinomial_cov import calculateCov
from pyatac.utils import call_peaks

D = '/mnt/openscience/audits/bio-atac-seq-nucleosome-positioning/initial-audit-20260930/logs/'
STATS = open(D + 'na_debug.log', 'a')
DET = open(D + 'na_debug_z.log', 'a')
orig = NC.NucChunk.findAllNucs


def dbg(self):
    combined = self.norm_signal.vals + self.smoothed.vals
    p = self.params
    c = call_peaks(combined, min_signal=0, sep=p.redundant_sep,
                   boundary=p.nonredundant_sep / 2, order=p.redundant_sep / 2)
    lrs = []
    zs = []
    covs = []
    for i in c:
        n = NC.Nucleosome(i + self.start, self)
        covs.append(n.nuc_cov)
        if n.nuc_cov > p.min_reads:
            n.getLR(self)
            lrs.append(n.lr)
            if n.lr > p.min_lr:
                n.getZScore(self)
                zs.append(n.z)
                sd = NC.SignalDistribution(n.start, p.vmat, self.bias_mat, n.nuc_cov)
                flat = np.ravel(p.vmat.mat)
                var = calculateCov(sd.probs, flat, sd.reads)
                pf = np.ascontiguousarray(sd.probs, dtype=np.float64)
                ex = sd.reads * (np.sum(pf * flat**2) - np.sum(pf * flat)**2)
                rep = [calculateCov(sd.probs, flat, sd.reads) for _ in range(3)]
                DET.write('  exact_numpy=%r repeat=%r p_min=%g p_max=%g n=%d dtype=%s contig=%s v_dtype=%s v_contig=%s vmin=%g vmax=%g\n' % (ex, rep, pf.min(), pf.max(), pf.size, sd.probs.dtype, sd.probs.flags['C_CONTIGUOUS'], flat.dtype, flat.flags['C_CONTIGUOUS'], flat.min(), flat.max()))
                DET.write('pos=%d reads=%s norm_signal=%s var=%r std=%r z=%r probs_sum=%r probs_nan=%d vmat_nan=%d\n' % (
                    n.start, sd.reads, n.norm_signal, var, sd.analStd(), n.z,
                    float(np.sum(sd.probs)), int(np.isnan(sd.probs).sum()), int(np.isnan(flat).sum())))
    DET.flush()
    STATS.write('%s:%d-%d cands=%d cov_ok=%d lr_ok=%d z_computed=%d z_nan=%d z_finite_ge_min=%d min_z=%s min_lr=%s\n' % (
        self.chrom, self.start, self.end, len(c), sum(1 for x in covs if x > p.min_reads), len(lrs), len(zs),
        int(np.isnan(zs).sum()) if zs else 0, sum(1 for z in zs if z >= p.min_z), p.min_z, p.min_lr))
    STATS.flush()
    return orig(self)


NC.NucChunk.findAllNucs = dbg
import matplotlib as mpl
mpl.use('PS')
from nucleoatac.cli import nucleoatac_parser, nucleoatac_main
args = nucleoatac_parser().parse_args()
nucleoatac_main(args)

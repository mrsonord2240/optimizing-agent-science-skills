"""Independent check of the seq2PRINT smoke output: saved model finite, forward shapes, attribution bigwigs non-trivial."""
import glob, os, numpy as np, torch, pyBigWig
import scprinter as scp  # noqa: F401 (model class)
W = "/mnt/openscience/audit-envs/bio-atac-seq-footprinting/reaudit-final/s2p_run/s2p"
pts = glob.glob(W + "/model/*.pt"); print("model files", [os.path.basename(p) for p in pts])
m = torch.load(pts[0], map_location="cpu", weights_only=False)
n = sum(p.numel() for p in m.parameters()); fin = all(torch.isfinite(p).all().item() for p in m.parameters())
print(type(m).__name__, "params", n, "finite", fin, "dna_len", m.dna_len, "output_len", m.output_len,
      "count_norm set", getattr(m, "count_norm", None) is not None, "foot_norm set", getattr(m, "foot_norm", None) is not None)
m.eval(); x = torch.zeros(2, 4, m.dna_len); idx = torch.randint(0, 4, (m.dna_len,)); x[:, idx, torch.arange(m.dna_len)] = 1
with torch.no_grad(): o = m(x)
print("forward", [tuple(t.shape) for t in (o if isinstance(o, (tuple, list)) else [o])], "finite", all(torch.isfinite(t).all().item() for t in (o if isinstance(o, (tuple, list)) else [o])))
bws = glob.glob(W + "/model/**/*.bigwig", recursive=True); print("bigwigs", len(bws))
for b in bws:
    bw = pyBigWig.open(b); v = np.nan_to_num(np.array(bw.values("chr1", 0, 2_000_000)))
    print(" ", os.path.relpath(b, W), "chroms", list(bw.chroms()), "nonzero bp chr1[0:2Mb]", int((v != 0).sum()), "absmax %.3g" % np.abs(v).max())

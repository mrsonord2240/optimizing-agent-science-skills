# Scientific source notes

- The executable direct-chimera route is public Hyb commit `028ab6371ce793ca5e86f475fce1f2cc6ad3c677`; the commit, not GNU Make's version text, is the tool identity.
- The Yeo chimeric-eCLIP source is pinned at `75fe74e90e6e4ca670a5af76836d80db09bdbcb1`. Total-route 10-nt R1 extraction and targeted-route R2 extraction are distinct.
- The targeted source itself is contradictory: CWL prose says 9 nt, executable default is 10, and the CWL does not supply a length. The audit does not choose a biological truth from that conflict.
- TargetScanHuman 8 coordinates are treated as transcript/UTR relative and require an assembly-, annotation-, release-, and strand-matched spliced map before genomic overlap.
- HEAP is a Halo-Ago2 transgenic-mouse experimental method with public data and associated analysis code, not a standalone human HEAP CLI.
- Chimera read counts are recovery evidence affected by expression, ligation, amplification, depth, and filtering; they are not treated as binding affinity.

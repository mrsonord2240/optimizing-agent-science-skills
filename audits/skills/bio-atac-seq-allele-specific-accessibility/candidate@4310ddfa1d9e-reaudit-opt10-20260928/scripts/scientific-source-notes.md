# Scientific and contract notes

- The candidate itself advertises `--peaks` as "Consensus peaks BED3 or wider";
  neither that interface nor `setup-and-inputs.md` requires unique BED4 names.
- `read_peaks` retains a supplied BED4 name as `peak`,
  `map_variants_to_peaks` discards peak chromosome/start/end after intersection,
  and `evaluate_groups` groups only on `peak` and `phaseSet`. The independent
  duplicate-name fixture therefore demonstrates the defect directly from the
  shipped contract and code, without relying on an external assumption.
- The bounded public VCF is chromosome-wide phased (`|`) but has no `PS` field.
  The successful real-data test added a constant `PS=1` only to a retained
  chr1:1-5 Mb derivative. The unmodified public input was also executed and
  rejected. This is test preparation, not an inference that arbitrary PS-free
  VCFs constitute one phase block.
- Public sources and retained local identities are documented in the tooling
  record: ENCODE `ENCFF415FEC` / `ENCSR095QNB`, 1000 Genomes NA12878 GRCh38
  liftover, UCSC hg38 chr1, WASP commit
  `d3b8447fd7719fffa00b856fd1f27c845554693e`, and RASQUAL commit
  `5aa553cf1b6501cf7ecd61a5efb34f7f20d354c6`.
- RASQUAL's two bundled matrix rows are C11orf21 and TSPAN32. The independent
  run used the public binary matrices and indexed chr11 VCF, checked both row
  identities, and recomputed BH across all 166 reported tests.

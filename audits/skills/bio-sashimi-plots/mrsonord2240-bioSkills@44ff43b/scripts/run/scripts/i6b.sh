source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data/pgt; P=$RUN/data/planted
micromamba run -n as-viz python $RUN/scripts/mk_bw.py ctrl.bedgraph ctrl_merged.bw chrP 3000
bedtools genomecov -split -ibam $P/G2_rep1.bam -bga > trt.bedgraph; micromamba run -n as-viz python $RUN/scripts/mk_bw.py trt.bedgraph trt_merged.bw chrP 3000
cp $P/planted.gtf annotation.gtf
# Skill's ini, verbatim structure (file names/titles adapted; no other change)
cat > tracks.ini <<'INI'
[gene_models]
file = annotation.gtf
height = 3
title = GENCODE v45
fontsize = 10
file_type = gtf

[ctrl_coverage]
file = ctrl_merged.bw
title = Control
color = #1f77b4
height = 3
file_type = bigwig

[trt_coverage]
file = trt_merged.bw
title = Treatment
color = #ff7f0e
height = 3
file_type = bigwig

[junctions]
file = junctions.bedpe
title = Junctions
height = 2
file_type = links
links_type = arcs
INI
echo "== Skill ini verbatim"; micromamba run -n as-viz pyGenomeTracks --tracks tracks.ini --region chrP:1-1200 -o $RUN/out/i6_pgt.pdf > $RUN/out/i6_pgt.log 2>&1; echo rc=$?; tail -4 $RUN/out/i6_pgt.log | cut -c1-300; ls -la $RUN/out/i6_pgt.pdf
micromamba run -n as-viz pyGenomeTracks --tracks tracks.ini --region chrP:1-1200 -o $RUN/out/i6_pgt.png --dpi 80 > $RUN/out/i6_pgt_png.log 2>&1; echo rc=$?
echo "== ini WITHOUT file_type=gtf (auto-detect)"; sed '/file_type = gtf/d' tracks.ini > tracks_nogtftype.ini; micromamba run -n as-viz pyGenomeTracks --tracks tracks_nogtftype.ini --region chrP:1-1200 -o $RUN/out/i6_nogtf.png --dpi 50 2>&1 | tail -3 | cut -c1-200; echo rc=$?
echo "== BAM track (Skill title: 'Define tracks (genes, BAM, BigWig, BED)')"
cat > tracks_bam.ini <<INI
[bam]
file = $P/G1_rep1.bam
title = bam
height = 3
INI
micromamba run -n as-viz pyGenomeTracks --tracks tracks_bam.ini --region chrP:1-1200 -o $RUN/out/i6_bam.png 2>&1 | tail -3 | cut -c1-250
echo "== links with the raw junction BED12 (regtools) instead"

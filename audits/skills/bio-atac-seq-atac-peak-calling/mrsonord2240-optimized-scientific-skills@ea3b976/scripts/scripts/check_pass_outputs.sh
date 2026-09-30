source /mnt/openscience/audits/bio-atac-seq-atac-peak-calling/reaudit-run/scripts/env.sh
cd $R/pass_macs3
echo "--- reproducibility.txt"; cat idr/reproducibility.txt
for n in true_reps rep1_pseudoreps rep2_pseudoreps pooled_pseudoreps; do echo "$n idr rows=$(wc -l < idr/$n.idr) rows_score>=540=$(awk '$5>=540' idr/$n.idr | wc -l) min_score=$(awk 'NR==1||$5<m{m=$5}END{print m}' idr/$n.idr)"; done
ls idr | tr '\n' ' '; echo
echo "peak counts: rep1=$(wc -l < rep1/rep1_peaks.narrowPeak) rep2=$(wc -l < rep2/rep2_peaks.narrowPeak) pooled=$(wc -l < pooled/pooled_peaks.narrowPeak)"
echo "pseudorep calls: $(for f in psr1_1/rep1_psr1 psr1_2/rep1_psr2 psr2_1/rep2_psr1 psr2_2/rep2_psr2 poolpsr_1/pool_psr1 poolpsr_2/pool_psr2; do printf "%s=%s " $(basename $f) $(wc -l < ${f}_peaks.narrowPeak); done)"
echo "--- conservative"; F=final/conservative.narrowPeak; wc -l < $F; awk '{print NF}' $F | sort -u | tr '\n' ' '; echo; head -2 $F
echo "blacklist overlaps in final: $(bedtools intersect -u -a $F -b $BL | wc -l)"
echo "cols7,9 uniq: $(cut -f7 $F | sort -u | tr '\n' ' ') / $(cut -f9 $F | sort -u | tr '\n' ' ')"
zcat $D/ENCFF346CZA.bed.gz > $R/enc_cons.bed
echo "conservative peaks overlapping ENCODE ENCFF346CZA (conservative IDR): $(bedtools intersect -u -a $F -b $R/enc_cons.bed | wc -l) of $(wc -l < $F); ENCODE peaks recovered: $(bedtools intersect -u -a $R/enc_cons.bed -b $F | wc -l) of $(wc -l < $R/enc_cons.bed) (slice-wide, ENCODE set has all chr1 peaks; restrict)"
awk '$1=="chr1" && $3<=30000000' $R/enc_cons.bed > $R/enc_cons_slice.bed
echo "ENCODE conservative in slice: $(wc -l < $R/enc_cons_slice.bed); recovered: $(bedtools intersect -u -a $R/enc_cons_slice.bed -b $F | wc -l)"
echo "--- macs2 vs macs3 identity"
for f in idr/true_reps.idr final/conservative.narrowPeak idr/reproducibility.txt; do a=$(md5sum < $f); b=$(md5sum < ../pass_macs2/$f); [ "$a" = "$b" ] && echo "IDENTICAL $f" || echo "DIFFERENT $f"; done
echo "peaks macs2: rep1=$(wc -l < ../pass_macs2/rep1/rep1_peaks.narrowPeak) rep1_macs3=$(wc -l < rep1/rep1_peaks.narrowPeak)"; ls ../pass_macs2/final
echo "--- bigWig header readback"
python3 - <<'PY'
import struct,os
R=os.environ['R']
f=open(R+'/pass_macs3/final/pooled.bw','rb'); h=f.read(56)
magic,ver,zl,ctO,dO,idxO,fc,dc,asO,tsO,unc=struct.unpack('<IHHQQQHHQQI',h)
print('magic',hex(magic),'version',ver,'zoomLevels',zl,'fieldCount',fc)
f.seek(tsO); bc,mn,mx,sd,ssq=struct.unpack('<Qdddd',f.read(8+32))
print('basesCovered',bc,'min',mn,'max',round(mx,2),'mean',round(sd/bc,3))
# compare to bedGraph
bases=0;m=0;s=0.0
for l in open(R+'/pass_macs3/final/pooled.sorted.bdg'):
    c,a,b,v=l.split(); v=float(v); L=int(b)-int(a); bases+=L; s+=v*L; m=max(m,v)
print('bedGraph bases',bases,'max',round(m,2),'mean',round(s/bases,3))
PY

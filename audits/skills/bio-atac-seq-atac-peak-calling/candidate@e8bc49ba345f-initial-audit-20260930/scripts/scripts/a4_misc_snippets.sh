#!/bin/bash
# Snippets from usage-guide/method-reference: grep -v chrM; macs2 without shim; bigWig signal readback.
source /mnt/openscience/audit-envs/bio-atac-seq-atac-peak-calling/wsl_env.sh
R=$APC/run/misc_audit; rm -rf $R; mkdir -p $R; cd $R
E1=$ATACDATA/encode/GM12878_rep1_filtered.chr1_1-30000000.bam
echo "== usage-guide: samtools view -h sample.bam | grep -v chrM  (synthetic pair: mate on chrM)"
cat > t.sam <<'S'
@HD	VN:1.6	SO:coordinate
@SQ	SN:chr1	LN:1000
@SQ	SN:chrM	LN:1000
r1	97	chr1	100	60	50M	chrM	200	0	A	I
r1	145	chrM	200	60	50M	chr1	100	0	A	I
r2	99	chr1	300	60	50M	=	400	150	A	I
r2	147	chr1	400	60	50M	=	300	-150	A	I
S
sed 's/A\tI$//' t.sam >/dev/null
python - <<'P'
import re
L=open('t.sam').read().splitlines()
out=[]
for l in L:
    if l.startswith('@'): out.append(l); continue
    f=l.split('\t'); f[9]='A'*50; f[10]='I'*50; out.append('\t'.join(f))
open('t.sam','w').write('\n'.join(out)+'\n')
P
samtools view -h t.sam | grep -v chrM > t.nochrM.sam; echo "kept lines:"; grep -vc '^@' t.nochrM.sam; samtools view -c t.nochrM.sam; grep -c '^@SQ' t.nochrM.sam
samtools view t.nochrM.sam | cut -f1-9
echo "orphan flag check (remaining r1 has flag 97 = paired, mate mapped, but mate removed):"
samtools view -b t.nochrM.sam 2>&1 | samtools flagstat - 2>&1 | head -8
echo "== macs2 without shim"
(unset LD_PRELOAD; macs2 callpeak -t $E1 -f BAM -g 2.7e9 -n noshim --outdir . --nomodel -p 0.01 2>&1 | tail -3)
echo "LD_PRELOAD=$LD_PRELOAD"

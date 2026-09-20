#!/bin/bash
# Input 3 (edge, regression of pre-fix input 3): "markdup errors out / marks nothing and I do not know my sort order".
# Each row of the fixer's verbatim Common Errors table is triggered on real data and the message string is extracted from SKILL.md
# and grep -F'd against the tool's actual stderr. Also: exit code + partial output claim, the Critical pitfall claim (lost tags -> error, not silent),
# fixmate -r -m, and the -c claim on the pre-flagged 1000G slice.
source /mnt/openscience/audit-envs/alignment-files/wsl_env.sh
source /mnt/openscience/audits/bio-duplicate-handling/run/common.sh
cd $W; rm -rf in03; mkdir in03; cd in03
# table messages, straight out of SKILL.md (first column, between backticks)
python - <<'PY' > table_msgs.txt
import re,io
t=io.open("/mnt/openscience/audits/bio-duplicate-handling/run/skill_copy/SKILL.md",encoding="utf-8").read()
sec=t.split("## Common Errors")[1].split("## Lossy")[0]
for l in sec.splitlines():
    m=re.match(r"\| `([^`]+)`",l)
    if m: print(m.group(1))
PY
echo "[table rows extracted: $(wc -l < table_msgs.txt)]"; cat table_msgs.txt
H=$D/test.paired_end.sorted.bam
samtools sort -n -o ns.bam $H; samtools fixmate -m ns.bam fm.bam; samtools sort -o cs.bam fm.bam
chk() { # $1 = row number in table, $2 = stderr file
  msg=$(sed -n "${1}p" table_msgs.txt)
  # rows with "..." are elided in the table: match the fixed parts
  if [[ "$msg" == *"..."* ]]; then a=${msg%%...*}; b=${msg##*...}; a=${a% }; b=${b# }; grep -qF -- "$a" $2 && grep -qF -- "$b" $2 && echo "  MATCH row $1: $msg" || echo "  NO-MATCH row $1: $msg"
  else grep -qF -- "$msg" $2 && echo "  MATCH row $1: $msg" || echo "  NO-MATCH row $1: $msg"; fi
}
echo "### row1: fixmate on coordinate-sorted input"
rm -f o.bam; samtools fixmate -m $H o.bam 2> e1.txt; echo "  exit=$? out exists: $(ls -la o.bam 2>&1 | awk '{print $5}')"; chk 1 e1.txt
echo "### row2: markdup on fixmate WITHOUT -m"
samtools sort -n -o n2.bam $H; samtools fixmate n2.bam f2.bam; samtools sort -o c2.bam f2.bam; rm -f o.bam
samtools markdup c2.bam o.bam 2> e2.txt; echo "  exit=$? flagged in leftover output: $(flagged o.bam 2>&1 | tail -1)"; chk 2 e2.txt
echo "### row3: MC stripped (python round trip)"
python $RUN/03_strip_tags.py cs.bam nomc.bam MC; rm -f o.bam
samtools markdup nomc.bam o.bam 2> e3.txt; echo "  exit=$?"; chk 3 e3.txt
python $RUN/03_strip_tags.py cs.bam noms.bam ms; rm -f o.bam
samtools markdup noms.bam o.bam 2> e3b.txt; echo "  [pitfall check: ms stripped] exit=$? -> $(head -c 120 e3b.txt | head -1)"
echo "### row4: markdup on name-sorted input"
rm -f o.bam; samtools markdup fm.bam o.bam 2> e4.txt; echo "  exit=$?"; chk 4 e4.txt
echo "### row5: collate tmp dir missing"
samtools collate -O -u $H tmpdir/collate 2> e5.txt >/dev/null; echo "  exit=$?"; chk 5 e5.txt
echo "### rows 6,7 (fgbio MQ / umi_tools index): checked in in05 and in07"
echo "### row8 now: Picard on a BAM with no @RG"
python - <<'PY'
import pysam
src=pysam.AlignmentFile("cs.bam"); h=src.header.to_dict(); h.pop("RG",None)
o=pysam.AlignmentFile("norg.bam","wb",header=pysam.AlignmentHeader.from_dict(h))
for r in src:
    r.set_tag("RG",None); o.write(r)
o.close(); print("RG-less BAM written; @RG lines:", len(h.get("RG",[])))
PY
samtools view -H $H | grep -c '^@RG' | sed 's/^/  @RG lines in source: /'
picard MarkDuplicates I=norg.bam O=o.bam M=m.txt 2> e8.txt >/dev/null; echo "  picard exit=$?"; chk 8 e8.txt
echo "### stated solution for row8: samtools addreplacerg fixes it?"
samtools addreplacerg -r '@RG\tID:s1\tSM:s1\tLB:lib1\tPL:ILLUMINA' -o fixed_rg.bam norg.bam && picard MarkDuplicates I=fixed_rg.bam O=o2.bam M=m2.txt >/dev/null 2>&1; echo "  after addreplacerg: picard exit=$? flagged $(flagged o2.bam)"

echo "### 'Critical pitfall' text vs behaviour"
grep -n "Critical pitfall" $SK/SKILL.md | cut -c1-260
echo "### fixmate -r -m (SKILL.md 'Remove Secondary/Unmapped')"
samtools fixmate -r -m ns.bam fr.bam; echo "  records $(samtools view -c ns.bam) -> $(samtools view -c fr.bam); secondary/unmapped left: $(samtools view -c -f 260 fr.bam)"

echo "### -c claim: re-marking an already-flagged BAM (1000G slice, 101 pre-flagged)"
G=$D/HG00349.chr20_1400000-1500000.bam
echo "  pre-flagged: $(flagged $G)"
samtools sort -n -o g.ns.bam $G; samtools fixmate -m g.ns.bam g.fm.bam; samtools sort -o g.cs.bam g.fm.bam
samtools markdup g.cs.bam g_noc.bam; samtools markdup -c g.cs.bam g_c.bam
picard MarkDuplicates I=$G O=g_pic.bam M=g_pic.txt >/dev/null 2>&1
echo "  no -c: $(flagged g_noc.bam)   -c: $(flagged g_c.bam)   Picard: $(flagged g_pic.bam)"
echo "  [claim text] $(grep -o 'add `-c`.*' $SK/SKILL.md | head -1 | cut -c1-200)"

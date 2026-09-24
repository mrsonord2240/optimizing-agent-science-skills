import subprocess, re, sys
src = open('stream_snip.py', encoding='utf-8').read()
ok_src  = src.replace('bwa mem ref.fa reads.fq | samtools sort -o aligned.bam', 'bwa mem ref.fa r1.fq.gz | samtools sort -o py_ok.bam')
bad_src = src.replace('bwa mem ref.fa reads.fq | samtools sort -o aligned.bam', 'bwa mem ref.fa /nonexistent_R1.fq.gz | samtools sort -o py_bad.bam')
assert ok_src != src and bad_src != src
exec(ok_src); print('good input: completed without exception')
try:
    exec(bad_src); print('bad input: NO EXCEPTION raised')
except subprocess.CalledProcessError as e:
    print('bad input: CalledProcessError rc', e.returncode)

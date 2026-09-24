import subprocess

subprocess.run(
    ['bash', '-o', 'pipefail', '-c', 'bwa mem ref.fa reads.fq | samtools sort -o aligned.bam'],
    check=True
)

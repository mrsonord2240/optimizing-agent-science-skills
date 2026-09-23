export HOME=/mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/home
unset XDG_CACHE_HOME

mkdir -p $HOME/cram_cache
seq_cache_populate.pl -root $HOME/cram_cache /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/d1.gone/ref.fa
export REF_CACHE=$HOME/cram_cache/%2s/%2s/%s
export REF_PATH=$REF_CACHE   # local only; no network/ENA lookup

samtools quickcheck -v /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/s.cram                 # header + EOF only: passes with the reference missing and with a corrupt body
samtools view -o /dev/null /mnt/openscience/audits/bio-sam-bam-basics/run/data/in8/s.cram && echo ok  # full decode: exit 1 if the reference cannot be resolved or a slice is corrupt

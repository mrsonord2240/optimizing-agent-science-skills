R=/mnt/openscience/audits/bio-reference-operations/run
cd $R/work/in6
echo "--- ug_07 leftovers"; cat main_chroms.dict | cut -c1-80; ls main_chroms.fa*; 
echo "--- skill_25 step 3 with REF_CACHE_DIR unset, isolated"
mkdir -p iso && cd iso && cp ../reference.fa . && unset REF_CACHE_DIR
seq_cache_populate.pl -root $REF_CACHE_DIR reference.fa </dev/null; echo "rc=$?"; ls
echo "--- usage 'seq_cache_populate.pl' help first lines"
seq_cache_populate.pl -help 2>&1 | head -12

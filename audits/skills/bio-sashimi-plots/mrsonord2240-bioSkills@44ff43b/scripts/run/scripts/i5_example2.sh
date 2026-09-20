source /mnt/openscience/audits/bio-sashimi-plots/run/scripts/env.sh
cd $RUN/data; mkdir -p real_ggs; cp -r $ASDATA/sashimi/. real_ggs/ 2>/dev/null; cd real_ggs
# ggsashimi upstream example #2 (repo-shipped reference output sashimi.tiff), rerun in this env as PNG at low res
ggsashimi.py -b input_bams.tsv -c chr10:27040584-27048100 -M 10 -C 3 -O 3 -A mean --alpha 1 -F png -R 60 --base-size=16 --height=3 --width=18 --fix-y-scale -o $RUN/out/i5_example2 > $RUN/out/i5_ex2.log 2>&1; echo rc=$?

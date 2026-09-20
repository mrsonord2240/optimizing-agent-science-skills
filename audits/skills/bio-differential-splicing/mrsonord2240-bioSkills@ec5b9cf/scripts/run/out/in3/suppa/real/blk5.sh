micromamba run -n as-suppa suppa.py generateEvents -i annotation.gtf -o events -f ioe -e SE SS MX RI

for ev in SE A5 A3 MX RI; do
    micromamba run -n as-suppa suppa.py psiPerEvent -i events_${ev}_strict.ioe -e gbr_tpm.tsv -o gbr_${ev}
    micromamba run -n as-suppa suppa.py psiPerEvent -i events_${ev}_strict.ioe -e yri_tpm.tsv -o yri_${ev}

    micromamba run -n as-suppa suppa.py diffSplice \
        -m empirical \
        -gc \
        -i events_${ev}_strict.ioe \
        -p gbr_${ev}.psi yri_${ev}.psi \
        -e gbr_tpm.tsv yri_tpm.tsv \
        -o diff_${ev}
done

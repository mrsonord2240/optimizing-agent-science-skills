micromamba run -n as-suppa suppa.py generateEvents -i annotation.gtf -o events -f ioe -e SE SS MX RI

for ev in SE A5 A3 MX RI; do
    micromamba run -n as-suppa suppa.py psiPerEvent -i events_${ev}_strict.ioe -e p1_tpm.tsv -o p1_${ev}
    micromamba run -n as-suppa suppa.py psiPerEvent -i events_${ev}_strict.ioe -e p2_tpm.tsv -o p2_${ev}

    micromamba run -n as-suppa suppa.py diffSplice \
        -m empirical \
        -gc \
        -i events_${ev}_strict.ioe \
        -p p1_${ev}.psi p2_${ev}.psi \
        -e p1_tpm.tsv p2_tpm.tsv \
        -o diff_${ev}
done

#!/bin/bash
export PYTHONDONTWRITEBYTECODE=1
for e in as-pangolin as-spvp as-spvp-gpu as-mmsplice as-spliceai as-cispliceai; do
 echo "== $e"; micromamba run -n $e python -c "
import importlib
for m in ['torch','tensorflow','gffutils','pyfastx','vcf','pyfaidx','pysam','pandas','mmsplice','spliceai','cispliceai','pyensembl','sinkhorn_transformer','axial_positional_embedding','cyvcf2']:
    try:
        x=importlib.import_module(m); print(m, getattr(x,'__version__','?'))
    except Exception as ex: print(m,'MISSING',type(ex).__name__)
" 2>&1 | grep -v "^W0000\|^I0000\|cuda\|cpu_feature\|To enable\|absl" ; done

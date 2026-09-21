pip install git+https://github.com/huangyh09/brie                 # BRIE2; `pip install brie` fails (sdist lacks requirements.txt)
pip install tensorflow tf_keras tensorflow-probability             # brie-quant needs all three, and TF_USE_LEGACY_KERAS=1
pip install --no-build-isolation git+https://github.com/lareaulab/psix   # numpy must already be installed
pip install git+https://github.com/songlab-cal/scquint             # pulls torch, pyro, snakemake

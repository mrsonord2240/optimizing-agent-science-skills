source /mnt/openscience/audit-envs/bio-atac-seq-deep-learning-atac/scripts/env.sh
export PATH=/home/sci/micromamba/envs/dlatac-tf/bin:$PATH
SP=/home/sci/micromamba/envs/dlatac-torch/lib/python3.11/site-packages
echo "== grep loaders"; grep -rIl "from_keras\|load_model\|h5py\|keras" $SP/tangermeme $SP/bpnetlite 2>/dev/null | head
ls $SP/tangermeme $SP/bpnetlite | head -60
echo "== tangermeme sigs"
py_torch - <<'P'
import inspect, tangermeme, importlib
from tangermeme.variant_effect import substitution_effect
from tangermeme.marginalize import marginalize
print(inspect.signature(substitution_effect)); print(inspect.signature(marginalize))
try:
    import tangermeme.io as io; print([n for n in dir(io) if not n.startswith('_')])
except Exception as e: print('tangermeme.io', e)
import bpnetlite.chrombpnet as c; print([n for n in dir(c) if not n.startswith('_')])
P
echo "== chrombpnet pred_bw/bias pipeline flags"
micromamba run -n dlatac-tf chrombpnet pred_bw -h | head -40
micromamba run -n dlatac-tf chrombpnet bias pipeline -h | grep -n -- "-fl\|-b \|--bias-threshold\|-n \|-p \|-ibam" | head
echo "== shap_to_modisco"; micromamba run -n dlatac-tf python -c "import chrombpnet,pkgutil;print([m.name for m in pkgutil.walk_packages(chrombpnet.__path__)][:80])"
micromamba run -n dlatac-tf chrombpnet contribs_bw -h | head -30
echo "== modisco report -h"; micromamba run -n dlatac-torch modisco report -h | head -30

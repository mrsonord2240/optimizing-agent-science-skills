"""Synthetic HTO count data for auditing bio-single-cell-hashing-demultiplexing.
Not real experimental data. Builds two datasets:
  1. data/hto_counts_4tag.csv  - 1600 cells x 4 HTOs, roughly EQUAL pooling
     (used for Input 1 canonical HTODemux and Input 2 hashsolo variant, trimmed to 2 tags)
  2. data/hto_counts_unequal.csv - 1200 cells x 4 HTOs, UNEQUAL pooling (tag D is a rare
     5% minority sample) with elevated ambient background, for Input 5 (stress).
  3. data/hto_counts_weak.csv - 800 cells x 3 HTOs with heavy ambient/spillover background
     that produces a large Negative pile, for Input 3 (rescue with demuxmix).
Ground truth labels (true_sample, true_class) are saved alongside each file so the
auditor can score caller accuracy against a known answer.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(20260919)


def make_dataset(n_cells, tag_names, tag_probs, singlet_rate, doublet_rate,
                  bg_lambda, signal_lambda, seed_offset=0):
    r = np.random.default_rng(20260919 + seed_offset)
    n_tags = len(tag_names)
    neg_rate = 1.0 - singlet_rate - doublet_rate
    assert neg_rate > -1e-9
    classes = r.choice(
        ["singlet", "doublet", "negative"],
        size=n_cells,
        p=[singlet_rate, doublet_rate, neg_rate],
    )
    counts = np.zeros((n_cells, n_tags), dtype=int)
    true_sample = []
    # Ambient/background HTO counts are realistically overdispersed relative to Poisson
    # (real spillover + cell-to-cell variation in capture efficiency). Use a negative
    # binomial with mean=bg_lambda and dispersion r=4 rather than a plain Poisson.
    nb_r = 4.0
    nb_p = nb_r / (nb_r + bg_lambda)
    for i, cls in enumerate(classes):
        bg = r.negative_binomial(nb_r, nb_p, size=n_tags)
        counts[i] = bg
        if cls == "singlet":
            tag_idx = r.choice(n_tags, p=tag_probs)
            counts[i, tag_idx] += r.poisson(signal_lambda)
            true_sample.append(tag_names[tag_idx])
        elif cls == "doublet":
            two = r.choice(n_tags, size=2, replace=False,
                            p=tag_probs / tag_probs.sum())
            for t in two:
                counts[i, t] += r.poisson(signal_lambda)
            true_sample.append("+".join(sorted(tag_names[t] for t in two)))
        else:
            true_sample.append("Negative")
    df = pd.DataFrame(counts, columns=tag_names,
                       index=[f"CELL_{i:05d}" for i in range(n_cells)])
    df["true_class"] = classes
    df["true_sample"] = true_sample
    return df


if __name__ == "__main__":
    # 1. Roughly equal 4-sample pooling, clean staining -> canonical HTODemux case
    tags4 = np.array(["HTO_A", "HTO_B", "HTO_C", "HTO_D"])
    probs_equal = np.array([0.25, 0.25, 0.25, 0.25])
    df_equal = make_dataset(1600, tags4, probs_equal,
                             singlet_rate=0.85, doublet_rate=0.08,
                             bg_lambda=8, signal_lambda=250, seed_offset=1)
    df_equal.to_csv("data/hto_counts_4tag.csv")
    print("4tag:", df_equal["true_class"].value_counts().to_dict())

    # 2. Unequal pooling: HTO_D is a rare 5% minority sample, elevated ambient background
    probs_unequal = np.array([0.35, 0.35, 0.25, 0.05])
    df_unequal = make_dataset(1200, tags4, probs_unequal,
                               singlet_rate=0.80, doublet_rate=0.10,
                               bg_lambda=15, signal_lambda=180, seed_offset=2)
    df_unequal.to_csv("data/hto_counts_unequal.csv")
    print("unequal:", df_unequal["true_class"].value_counts().to_dict())
    print("unequal per-tag singlet counts:",
          df_unequal.loc[df_unequal.true_class == "singlet", "true_sample"].value_counts().to_dict())

    # 3. Weak staining / heavy ambient spillover, 3 tags -> large Negative pile expected
    tags3 = np.array(["HTO_X", "HTO_Y", "HTO_Z"])
    probs3 = np.array([1 / 3, 1 / 3, 1 / 3])
    df_weak = make_dataset(800, tags3, probs3,
                            singlet_rate=0.55, doublet_rate=0.05,
                            bg_lambda=35, signal_lambda=90, seed_offset=3)
    df_weak.to_csv("data/hto_counts_weak.csv")
    print("weak:", df_weak["true_class"].value_counts().to_dict())

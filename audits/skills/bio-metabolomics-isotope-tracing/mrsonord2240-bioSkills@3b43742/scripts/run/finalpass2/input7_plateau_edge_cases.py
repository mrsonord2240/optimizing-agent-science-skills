"""Final-pass Input 7 — prior adversarial plateau regression, now against status strings."""
import numpy as np

def plateau_status(fe):
    deltas = np.abs(np.diff(np.asarray(fe, dtype=float)))
    if len(deltas) < 3:
        return "insufficient timepoints to assess steady state", deltas
    if np.all(deltas[-3:] < 0.02):
        return "plateau", deltas
    return "still labeling", deltas

near_flat, near_deltas = plateau_status([0.10, 0.30, 0.395, 0.398, 0.399])
flat, flat_deltas = plateau_status([0.30, 0.385, 0.395, 0.399, 0.400])
short, short_deltas = plateau_status([0.00, 0.42])
assert near_flat == "still labeling"
assert flat == "plateau"
assert short == "insufficient timepoints to assess steady state"
print("near_flat_deltas=", np.round(near_deltas, 3).tolist(), "status=", near_flat)
print("flat_deltas=", np.round(flat_deltas, 3).tolist(), "status=", flat)
print("short_deltas=", np.round(short_deltas, 3).tolist(), "status=", short)
print("assertions=withholds_near_flat,permits_true_plateau,labels_insufficient_data")

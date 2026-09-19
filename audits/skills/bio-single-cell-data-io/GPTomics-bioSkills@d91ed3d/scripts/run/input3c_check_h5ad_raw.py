"""Sanity check: did the h5ad actually contain a /raw group with 33538 genes?
(confirms whether zellkonverter's empty altExpNames is a write-side or read-side issue)"""
import h5py

p = r"F:\OpenScience\audits\bio-single-cell-data-io\data\input3_rich.h5ad"
with h5py.File(p, "r") as f:
    print("top-level keys:", list(f.keys()))
    if "raw" in f:
        print("raw group keys:", list(f["raw"].keys()))
        print("raw/var/_index shape:", f["raw"]["var"]["_index"].shape)
        print("raw/X shape (via attrs or group):", dict(f["raw"]["X"].attrs) if "X" in f["raw"] else "no X")

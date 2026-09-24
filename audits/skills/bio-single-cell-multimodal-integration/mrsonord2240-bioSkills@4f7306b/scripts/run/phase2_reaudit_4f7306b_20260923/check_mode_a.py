import sys
text = open(sys.argv[1], encoding="utf-8").read()
for required in ("mosaic", "imputed", "lupus-risk", "clinical-risk", "GLUE", "Windows", "Linux", "genome build"):
    assert required in text
print("mode_a_clean_exit mosaic_and_glue_boundaries=recorded")

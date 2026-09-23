"""Static regression of the two prior reasoning-only inputs."""
from pathlib import Path
skill = Path(__file__).parents[3] / "wt" / "chemoinformatics-pharmacophore-modeling" / "chemoinformatics" / "pharmacophore-modeling" / "SKILL.md"
text = skill.read_text(encoding="utf-8")
warning = "# PLACEHOLDER COORDINATES -- do not reuse without deriving from a validated"
assert warning in text and text.index(warning) < text.index("query_features = [")
assert "RDKit does not provide a single `EmbedPharmacophore` call that performs those steps." in text
assert "does **not** directly generate molecular structures" in text
print("ASSERT placeholder warning precedes query_features: PASS")
print("ASSERT false-premise correction distinguishes application from consensus derivation: PASS")
print("ASSERT scope boundary distinguishes pharmacophore generation from molecule generation: PASS")

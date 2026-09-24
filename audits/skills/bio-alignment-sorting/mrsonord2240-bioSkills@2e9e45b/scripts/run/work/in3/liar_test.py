from skillfns import is_coordinate_sorted, ensure_coordinate_sorted
import pysam
print("is_coordinate_sorted(liar.bam):", is_coordinate_sorted('liar.bam'))
r = ensure_coordinate_sorted('liar.bam','liar_fixed.bam')
print("ensure_coordinate_sorted(liar.bam) returned:", r, "| sorted now:", is_coordinate_sorted(r))
assert r == 'liar_fixed.bam' and is_coordinate_sorted(r) and not is_coordinate_sorted('liar.bam')
print("PASS")

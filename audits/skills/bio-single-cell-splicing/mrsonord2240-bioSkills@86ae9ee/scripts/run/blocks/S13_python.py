pb, groups = pseudobulk_junctions(junction_counts, cell_metadata)
pb.to_csv('pb_counts.txt.gz', sep=' ')
groups.to_csv('pb_groups.txt', sep='\t', header=False, index=False)   # two groups only: subset the two cell types for each pair

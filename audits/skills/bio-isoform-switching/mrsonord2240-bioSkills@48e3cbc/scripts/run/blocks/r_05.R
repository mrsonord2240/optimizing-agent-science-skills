f <- aSwitchList$isoformFeatures
hit <- unique(f$isoform_id[!is.na(f$isoform_switch_q_value) & f$isoform_switch_q_value < 0.05 & abs(f$dIF) > 0.1])
called <- unique(tx2gene$gene[match(hit, tx2gene$tx)])            # gene IDs of the tx2gene table, not gene names
confirmed <- intersect(called, names(qval)[!is.na(qval) & qval < 0.05])

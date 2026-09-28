# Generated test inputs

Skill: `bio-clip-seq-ago-clip-mirna-targets`  
Category: Data Analysis  
Execution mode: D (hybrid)  
Complexity: Moderate (5 inputs)

1. **Canonical:** Run the supplied chimeric-eCLIP wrapper against the current
   public Hyb implementation and its official test data. Verify the database
   contract, generated output name, exit status, 16-column schema, and retained
   miRNA-mRNA rows.
2. **Variant A:** Exercise the wrapper with missing dependencies, a Hyb process
   that exits 42, paths and prefixes containing spaces, and a literal `*` in a
   FASTA path. Verify failure propagation, containment, and partial outputs.
3. **Edge:** Feed the wrapper a valid current 16-column Hyb record with matched
   miRNA expression. Verify which fields identify each RNA, expression
   filtering, mRNA filtering, and per-miRNA aggregation.
4. **Variant B:** Execute the documented UMI-tools, cutadapt, soft-clip, and
   TargetScan-overlap patterns. Verify read-orientation assumptions, strand
   behavior, coordinate systems, and what each result can establish.
5. **Stress:** Classify the advertised Hyb, pyHyb, Yeo chim-eCLIP, HEAP,
   TargetScan, miRDB, and DIANA surfaces, then audit the direct-versus-indirect,
   count-as-affinity, and absence-of-AGO-peak interpretations.


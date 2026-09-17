library(RNASeqPower)
db <- tools::Rd_db("RNASeqPower")
print(names(db))
rd <- db[["rnapower.Rd"]]
txt <- capture.output(tools::Rd2txt(rd))
cat(paste(txt, collapse = "\n"))

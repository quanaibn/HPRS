argv <- commandArgs(TRUE) 
#this script calculates mean FPKM for all samples for RNAseq output and H3K27Ac output from the FPKM_normalized_featureCounts.R script

filename1 = argv[1]

sprintf("Reading Table: %s", filename1)
datFPKM <-read.table(filename1, sep="\t", header=T)

NumberSamples <- dim(datFPKM)[2] -1

cat(sprintf("Calculating maximum values for: %s samples \n", NumberSamples))

datFPKM$max <- apply(datFPKM[,-c(1)], 1, max)

datFPKMwrite <- datFPKM[,c(1,ncol(datFPKM))]

write.table(datFPKMwrite, paste0(filename1, "_Max"), sep="\t", quote =F, col.names=F, row.names=F)


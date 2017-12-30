argv <- commandArgs(TRUE) 
#this script calculates FPKM output from featureCount outputs to calculate FPKM for each regulatory region
#it performs sanity check and ouput that to screen, or stderr. Then write the result table.
#command to run in bash Rscript --vanilla  /data/ngu121/Rscript/QuanRscript_collection/RforBatch/20160828_normalizeTPM.R
#Note: may need to load: module load R first before running command 

filename1 =argv[1]
filename2 =argv[2]
print(filename1); print(filename2)
  
if (length(argv) < 2) {stop("Missing argument: fileCount & filelibrarySize")}
datCount <-read.table(filename1,sep="\t", header=T)
dattotalmapped <-read.table(filename2,sep="\t", header=T, row.names=1 )

NumberSample <-dim(datCount)[2]-6

TotalReads <-colSums(dattotalmapped[1:4,])

datTPM <-t(apply(datCount[,7:(NumberSample+6)],1, function(x){x*1e6/TotalReads})) #change columns here 33

datFPKM <-datTPM*1000/datCount$Length

datFPKM <-data.frame(datFPKM)

datFPKM$Ids <-datCount$Geneid
#saninity check
indexPOS <-which(datFPKM[,NumberSample]>0) #change columns here 
print("Sanity check")
print(c("FPKM", datFPKM[indexPOS[1],NumberSample])); 
print(c("rawCount1", datCount[indexPOS[1], NumberSample+6]));
print(c("totalMappedReads1", TotalReads[NumberSample]));
print(c("length1", datCount$Length[indexPOS[1]]));
print(c("checkFPKM", datCount[indexPOS[1], NumberSample+6]*1e6/TotalReads[NumberSample]*(1000/datCount$Length[indexPOS[1]])))

write.table(datFPKM[,c((NumberSample+1),1:NumberSample)], paste(filename1, "_FPKMnormalized", sep=""), sep="\t", col.names = T, row.names = F, quote=F)





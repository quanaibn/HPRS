argv <- commandArgs(TRUE) 
#this script merge 7 data types. At the end, it also calculates normalized values for number of transcription factor binding sites, and number of annotations per bp length
#input argv1 as the common extension of all 7 filtters (.Temp in this case)
# Example: extension = '.Temp'
extension = argv[1]

list7filter  <-list.files(pattern = extension)
print("Will merge the following files")
list7filter

AnnCount <- read.table(list7filter[grep("AnnCount",list7filter )])
colnames(AnnCount) <-c("IDs", "Chr","Start", "End","AnnotationCount")

CAGEpeak <- read.table(list7filter[grep("CAGE",list7filter )])
colnames(CAGEpeak) <-c("IDs", "CAGEcount")

H3K27Ac <-read.table(list7filter[grep("H3K27Ac",list7filter )]) 
colnames(H3K27Ac) <-c("IDs", "MeanH3K27Ac")

PhastCons <- read.table(list7filter[grep("PhastCons",list7filter )]) 
colnames(PhastCons) <-c("IDs", "phastCons")

RNAseq <-read.table(list7filter[grep("RNAseq",list7filter )]) 
colnames(RNAseq) <-c("IDs", "MeanRNAseq")

SVM <-read.table(list7filter[grep("SVM",list7filter )])
colnames(SVM) <-c("IDs", "SVM")

TFBS <-read.table(list7filter[grep("TFBS",list7filter )])
colnames(TFBS) <-c("IDs", "TFBSCount")

AnnCount_CAGEpeak <-merge(AnnCount, CAGEpeak, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak:", dim(AnnCount_CAGEpeak)))
cat(sprintf(c("AnnCount:", dim(AnnCount)))); print(c("CAGEpeak:", dim(CAGEpeak))) 

AnnCount_CAGEpeak_H3K27Ac <-merge(AnnCount_CAGEpeak, H3K27Ac, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak_H3K27Ac:", dim(AnnCount_CAGEpeak_H3K27Ac)))
cat(sprintf(c("AnnCount_CAGEpeak:", dim(AnnCount_CAGEpeak)))); print(c("H3K27Ac:", dim(H3K27Ac)))

#Note this step for PhastCons will introduce some NA values
AnnCount_CAGEpeak_H3K27Ac_PhastCons <-merge(AnnCount_CAGEpeak_H3K27Ac,PhastCons, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak_H3K27Ac_PhastCons:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons)))
cat(sprintf(c("AnnCount_CAGEpeak_H3K27Ac:", dim(AnnCount_CAGEpeak_H3K27Ac)))); print(c("PhastCons:", dim(PhastCons)))

AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq <-merge(AnnCount_CAGEpeak_H3K27Ac_PhastCons,RNAseq, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq)))
cat(sprintf(c("AnnCount_CAGEpeak_H3K27Ac_PhastCons:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons)))); print(c("RNAseq:", dim(RNAseq)))

AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM <-merge(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq,SVM, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM)))
cat(sprintf(c("AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq)))); print(c("SVM:", dim(SVM)))

AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM_TFBS <-merge(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM,TFBS, by.x="IDs", by.y="IDs", all.x = T)
sprintf(c("merged AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM_TFBS:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM_TFBS)))
cat(sprintf(c("AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM:", dim(AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM)))); print(c("TFBS:", dim(TFBS)))

merged_metadata <-AnnCount_CAGEpeak_H3K27Ac_PhastCons_RNAseq_SVM_TFBS

merged_metadata$Length = merged_metadata$End -merged_metadata$Start +1
#normalized total TFBS counts / total length (bp)
merged_metadata$TFBSCount <-merged_metadata$TFBSCount/merged_metadata$Length
#normalized total annotation counts / total length (bp)
merged_metadata$AnnotationCount <-merged_metadata$AnnotationCount/merged_metadata$Length

print("Final metadata to write")
head(merged_metadata, n=2)

#change table name here depending on the data 
write.table(merged_metadata[,c(1:4,12,5:6, 11, 7:10 )], "susScr3_7filter_metadata_forFiltering.bed", sep="\t", quote =F, col.names=T, row.names=F)


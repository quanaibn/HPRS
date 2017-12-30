########
#Use this command to run:for file in chr_{1..29} chr_X; do\
#sbatch -e $file.stderr Rscript_Merged.bat $file; echo $file; sleep 1; done
########

argv <- commandArgs(TRUE)
if (length(argv) < 1) {stop("Missing argument:filename & filename_read")}
#list.files() #this was written to stderr
chrname <- argv[1]
#install.packages("seqinr", repos="http://R-Forge.R-project.org")

require(seqinr)

chrfasta<-read.fasta(paste(chrname, ".datALLSelectedRegions_SNPStringentSet_SNPdetails_Coord.2K4bed.fasta",sep=""),
                     as.string = FALSE, set.attributes = FALSE, forceDNAtolower = FALSE)


chrcoord <-read.table(paste(chrname,".datALLSelectedRegions_SNPStringentSet_SNPdetails_Coord.2K8bed" ,sep=""),
                      header=F, sep="\t")

#chr9coord$V9<-c(rep(NA,n=length(chr9coord$V8)))

#for (i in 1:length(chr9coord$V7)){chr9coord$V9[i] <- getLength.SeqFastadna(as.character(chr9coord$V7[i]))}
#ind<-grep(3,chr9coord$V9)
#ind2 <-grep(",",chr9coord$V8[ind])

chr <-chrfasta

library(stringr)

for (i in 1:length(chrcoord$V7)){
  length <-getLength.SeqFastadna(as.character(chrcoord$V7[i]))
  replace_length <- getLength.SeqFastadna(str_split_fixed(as.character(chrcoord$V8[i]), ",",2))[1]
  
  SNPpos<-chrcoord$V5[i]-chrcoord$V2[i]
  if (length ==1){chr[[i]][SNPpos]<-str_split_fixed(as.character(chrcoord$V8[i]), ",",2)[1]}
  else {
    chr[[i]] <-chr[[i]][-c(seq((SNPpos+1),(SNPpos+length-1)))]
    chr[[i]][SNPpos]<-str_split_fixed(as.character(chrcoord$V8[i]), ",",2)[1]
  }
}


write.fasta(chr,getName.SeqFastadna(chr),paste("mutated_",chrname, ".fasta", sep=""),
                                               nbchar=2010) #make sure nnchar longer than max seqlength


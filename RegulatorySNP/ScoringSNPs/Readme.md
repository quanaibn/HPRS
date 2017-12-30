# This folder contains scripts for scoring SNPs on enhancer regulatory activities using deltaSVM
- The main steps are:
1. prepare VCF files with the following number of columns (coordinates are 300 bp windows with SNP in the center of the window):

```
chrX    540     840     rs797641186     691     691_GtoT        G       T
chrX    709     1009    rs798593172     860     860_CtoT        C       T
chrX    716     1016    rs385732609     867     867_GtoA        G       A
chrX    915     1215    rs473552425     1066    1066_GtoT       G       T
chrX    926     1226    rs434316247     1077    1077_TtoG       T       G

```

2. prepare a fasta file of reference sequence 300 bp windows with SNP in the center of the window, use bedtools getfasta function.
```
#To get fasta sequences of all chromosomes (one chromosome at a time), and sequences with N are removed, use the script RemoveSequenceWith_N_20160905.py provided here. The script take the starting input containing coordinates information. It can be run in parallel for each chromosome

parallel 'python RemoveSequenceWith_N.py {} bosTau6.fa' ::: *4bed

```

3. mutate the reference fasta file using the R script: 20160314_SNP_MutatedSequences.R. It can take millions of sequences as the input.

4. After preparing two fasta files (the files containing reference sequences and mutated sequences), with the same names and order of sequences, use deltaSVM perl script to score the SNPs by comparing sequence without the SNP (reference) and sequence with the SNP (mutated). The deltaSVM perl script within the gkmSVM package (http://www.nature.com/ng/journal/v47/n8/full/ng.3331.html) is used. 

- An example of the bash script to score SNPs using deltaSVM.pl:

```
#!/bin/bash
#SBATCH --job-name="ScoresSNP"
#SBATCH --time=5:00:00
#SBATCH --mem=10Gb


#{1} is the ref, {2} is the mutated


file=${2}

perl deltasvm.pl ${1} ${2} 11Kmer.scores ${file%%.*}.SNP.Scores

#The 11kmer.scores file was generated from the following commands. It produces gkmSMM score for every fasta sequence as the combination of 11 bp possible (in the 11kmers.fasta) 

#To train the model
#./lsgkm_Maxlength5K/src/gkmtrain -T 16 susScr-H3K27Ac_MultiplePeak.noN.fasta\
# susScr-H3K27Ac_3xRandom_NoVillarsignal.fasta MultiplePeaks_lsGKM_susScr3

#./lsgkm_Maxlength5K/src/gkmpredict  -T 4 -v 2 11kmers.fasta MultiplePeaks_lsGKM_susScr3.model.txt Kmers11.Scores 

```

# Prepare for gkmSVM scoring
- This folder contains scripts to prepare positive and negative training sets for scoring enhancer activities in cattle, and pigs.
- The input files are MACS2 peak calling files of the enhancer mark H3K27Ac from Villar et al. (Cell,2015,160:3,554-566). 
- Start with the Prepare_Pos_Enh_MultiSummits.py script to generate a positive training set
```
#Example
python Prepare_Pos_Enh_MultiSummits.py Mmus-H3K27Ac_replicated-peaks_macs

```

- Then use the output bed file (the positive training set) to generate a fasta file and remove sequences containing N ambiguous nucleotides (by the RemoveSequences_with_N.py script). The resulting bed file is used as a reference file to randomly select a negative training set containing 3 times more regions than the positive training set (using the Prepare_Neg_3xPosSize.py script). 
```
#Example

#find the positive set
python RemoveSequences_with_N.py Mmus-H3K27Ac_replicated-peaks_macs_Multiple_HighestPeak.bed mm10.fasta

#randomly sample across the genome to find the negative set (3x the number of regions)
python Prepare_Neg_3xPosSize.py Mmus-H3K27Ac_replicated-peaks_macs_Multiple_HighestPeak.bed_NoN.bed  mm10.chrom.sizes mm10.fasta

```
- The output negative training set, in bed format, is then used for calculating H3K27Ac signal for each of the region (using the featureCount program, and the BAM files for H3K27Ac data). This step outputs a readCount file, in a data frame like the following example:
```
Geneid  Chr     Start   End     Strand  Length  ERR572204.fastq.gz.sam1.bam1    ERR572214.fastq.gz.sam1.bam1    ERR572261
.fastq.gz.sam1.bam1
susScrH3K27Ac1_0        chr15   147611417       147611517       +       101     2       0       0
susScrH3K27Ac1_1        chr7    130005131       130005231       +       101     0       1       0
susScrH3K27Ac1_2        chr3    117253701       117253801       +       101     2       1       2
```
- The ReadCount file is then used as the input for the script Filter_NegativeSet_byH3K27AcCount.py  which filter out negative regions with some positive H3K27Ac signal
- The script RemoveSequences_with_N.py is for convenient use to remove any sequence in a fasta file that contains N ambiguous nucleotide
- Following is an example of the script to train the gkmSVM model and score enhancers 

```
#!/bin/bash
#SBATCH --job-name="3BtBtbk"
#SBATCH --time=40:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --mail-type=ALL
#SBATCH --mail-user=yr@email.com

#To train the model
./lsgkm_Maxlength5K/src/gkmtrain -T 16 susScr-H3K27Ac_MultiplePeak.noN.fasta\
 susScr-H3K27Ac_3xRandom_NoVillarsignal.fasta MultiplePeaks_lsGKM_susScr3

#To score every fasta sequence as the combination of 11 bp possible (in the 11kmers.fasta) 
./lsgkm_Maxlength5K/src/gkmpredict  -T 4 -v 2 11kmers.fasta MultiplePeaks_lsGKM_susScr3.model.txt Kmers11.Scores 

#To score every predicted regulatory region by HPRS: 
./lsgkm_Maxlength5K/src/gkmpredict  -T 4 -v 2 HPRS_regulatoryRegions.fa\
 MultiplePeaks_lsGKM_susScr3.model.txt susScr_HPRS_regulatoryRegions.Scores

``` 

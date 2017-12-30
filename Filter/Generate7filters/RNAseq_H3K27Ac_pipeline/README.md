# This pipeline is to map and calculate RNAseq signal and H3K27Ac signal to regulatory regions. These two signals are key marks for active regulatory regions. Main steps include:

1. Downloading fastQ files from relevant databases

2. Map the fastQ files to the genome. This can be done using BWA to map and filter high quality mapped reads. The following bash script can be used for pig genome: 

```
!/bin/bash
#SBATCH --job-name="BWApipeline"
#SBATCH --time=20:00:00
#SBATCH --ntasks=12
#SBATCH --mail-type=ALL
#SBATCH --mail-user=your@add

module load bwa/0.7.12
module load samtools/1.2.1

#if paired end data
bwa mem -t 12 susScr3.fa ${1}*_1.fastq ${1}*_2.fastq >${1}.sam1

#if singe end data
#for file in *fastq; do bwa mem bosTau6.fa $file >$file.bwa.sam; done

#convert sam to bam
samtools view -bT susScr3.fa ${1} >${1}.bam1

#sort
samtools sort ${1}.bam1 -f ${1}.Sorted1

#index
samtools index ${1}.Sorted1

```

3. The mapped bam files are then used to count reads mapped to regulatory regions using featureCount program
-  First format bedfiles to SAF files (simply use awk to move IDs column to the first column, and add a column with '.' at the end. See featureCount page for details).
-  Then create a list file containing all input file names, separated by space 
- Then the following batch job can be submitted 

```
#!/bin/bash
#SBATCH --job-name="13adDat"
#SBATCH --time=20:00:00
#SBATCH --mail-type=ALL
#SBATCH --mail-user=yourmail@add

./featureCounts -F SAF -T 4 -o ${1}.featurecount -a ${1} `head -1  list`
```

4. Then use the R script FPKM_normalized_featureCounts.R for normalizing to FPKM. 

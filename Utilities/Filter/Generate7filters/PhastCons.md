# Steps to calculate PhastCons scores:
- using 100-way vertebrate alignment
- regulatory regions in Cattle were mapped back to human
- the calculation was done by bedtools map function
- file from UCSC in bigWig (.bw) format were converted to bedGraph format using UCSC bigWigToBedGraph tool
```
Example:
#to download the phastCons scores for multiple alignments of 99 vertebrate genomes to the human genome
wget http://hgdownload.cse.ucsc.edu/goldenpath/hg19/phastCons100way/hg19.100way.phastCons.bw
#to convert it into BedGraph format
bigWigToBedGraph hg19.100way.phastCons.bw ./new_totalBedGraph/hg19.100way.phastCons.bedGraph
```
- bedGraph files for all individual chromosomes were merged into one file: hg19.100way.phastCons.bedGraph_all_used  
- an example of the batch job for calculating PhastCons is below
```
#!/bin/bash
#SBATCH --job-name="Map"
#SBATCH --time=8:00:00
#SBATCH --mem 60Gb
#SBATCH --mail-type=ALL
#SBATCH --mail-user=quanaibn@gmail.com

bedtools map -a Combined_88Tis5Dat_Pig_BackLiftOverHg19_ShortIDsorted.bed -b\
 hg19.100way.phastCons.bedGraph -c 4 -o mean >${1}.Allchr_88Tis5Dat_PigBackHg19.mean
```

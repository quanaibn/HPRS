#### This is a collection of common commands for convenient use during the implementation of the HPRS pipeline.Users may choose to use these commands or other alternative commands to achieve the same results

- To run mapping for multiple files, submitting multiple batch jobs:

```
for file in *bed *OriHuman; do sbatch -e $file.STDERR pythonRun2.bat $file; echo $file; sleep 1; done

```
- An example of the bash file for mapping by running the python script:
```
#!/bin/bash
#SBATCH --job-name="PyLO"
#SBATCH --time=2:00:00
#SBATCH --mem=40Gb

python ./LiftOver_BackLiftOver_PermitMultipleBedsIn1folder.py  ${1} ../hg19ToCavPor3.over.chain.gz  ../cavPor3ToHg19.over.chain.gz

#The program will run using 4 cpus, it takes 10 minute for a dataset of 90K regions
```
- To run parallel for multiple comparisons:
```
parallel 'bedtools intersect -a cavPor-EnhancerH3K27AcNOToverlapH3K4me3.4bed -b {} -u >{}.intersect.Villar' ::: *080

```

- For calculating total size of a set of genomic regions in bed format, use this:
```
awk 'BEGIN{sum=0}{sum+=$3-$2+1}END{print sum}'
or awk -f total_size.awk bedfileName
```
- A common liftOver shell script (if input files are small):

```
#Can save the following command into a shell script, named: liftOver.sh. Then run it when needed: sh liftOver.sh {1} {2} {3}
#where, 1: bedfile; 2:chainfile; 3:(string)fromSpeciesToTargetSpecies
liftOver -minMatch=0.20 ${1} ${2} ${1}.${3}.LiftOver020 ${1}.${3}.UnlifftOver020

``` 

- A common liftOver bash script (if input files are large):

```
#!/bin/bash
#SBATCH --job-name='LO'
#SBATCH --time=2:00:00
#SBATCH --mem=8Gb

#1: bedfile; 2:chainfile; 3:(string)fromSpeciesToTargetSpecies
liftOver -minMatch=0.20 ${1} ${2} ${1}.${3}.LiftOver020 ${1}.${3}.UnlifftOver020
```

- To check for unique overlap:
```
bedtools intersect -a Sscrofa10p2_EnsemblGenes85.bed -b Merged_88Tis_5dat_suScr3_Final.bed -u >test
```

- To check for overlap with window:
```
#example, window =200 bp to the left and right of the regions

bedtools window -a Sscrofa10p2_EnsemblGenes85.bed -b Merged_88Tis_5dat_suScr3_Final.bed -w 200 -u >test
```

- To obtain fasta sequences of a bed file:
```
bedtools getfasta -fi fastaFilename -bed bedfileName -fo outputName -name
```

- To merge overlapping coordinates in a bedfile
```
bedtools merge -c 4 -o collapse -i bedfileName >outputName
```

- To select random set of regions corresponding to a reference set
```
#with an option to sample non-overlapping regions
bedtools shuffle -i bedfileName -g chrsize_fileName -noOverlapping >outputName
```
- To filter regions meeting a combination of conditions
```
# Example, promoters that have on pposite orientation to the reference:
awk '{FS="\t"}{OFS="\t"} ($4=="-1" && $11 =="+") || ($4=="1" && $11 =="-")'
```
 



























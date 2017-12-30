# Scanning TFBS at the whole genome scale is computationally expensive. The pipeline here shows a way to do it in a time-efficient way. The main steps include:
- arranging TF motives of each dataset into a folder. Here we used: Jaspar, Transfac and Encode
- the genome is split into chromosome. If the fasta file for each chr is not available. use the following script to parse the genome:
```
"""
The python script to reformat the genome into fasta format, where sequence for each chr is in one line
"""
index =[]
newFa = open('susScr3_reformat.fa', 'w')
with open("susScr3.fa") as lines:
    i=0
    for line in lines:
        if line[0] != '>':
            newFa.write(line.rstrip())
        else:
            newFa.write('\n')
            newFa.write(line)
newFa.close() 

```
```
#then run this shell script to split the whole genome into chrosomome
for file in chr{1..18} chrX chrM; do grep -A1 $file susScr3_reformat.fa >$file.fa; echo $file; done
```

- work in each folder separately
- create a list file of motives (ls *.cb >>list)
- split the list to several files (70 motives will take ~20 hours to scan the whole genome)
- use the submission script to submit the Cbuster program:
```
for file in list*plit*; do sbatch -e $file.STDERR TFB_cbust_SinglePWM.bat $file;echo $file; sleep 1; done

```
- use the following batch script to run cbuster for each chromosome and for each split file of TF matrices:
```
#!/bin/bash
#SBATCH --job-name="L2Encode"
#SBATCH --time=40:00:00
#SBATCH --mem=10Gb

for file in `cat ${1}`; do for file2 in chr*.fa; do ./cbust-linux -l -f 1 $file $file2  >${file}.ENCODEfinalTFprediction.${file2}; done; done

```
- After running Cbuster, reformat the files using this python script: PostCbuster_parsing.py for parsing
- After parsing, need to filter sites with low scores (can use 20 as the cutoff), using this bash script: Combined_Filter_Cbuster_motif.sh









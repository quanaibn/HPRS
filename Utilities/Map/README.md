# This is the main mapping step to project human regulatory regions to a species of interest:
- Run the Main_Mapping_Pipeline.py first.The script maps a bed file containing hundreds of thousands to millions of regulatory regions from human to a mammalian species of interest. To increase speed, it runs paralleled processes (it uses 4 cpus, and users can adjust the code to increase the number of cpus if needed), and can map ~100,000 regions in  about 10 minutes.

- The script can map regulatory regions from human to most mammalian species, especially if there are whole genome  LastZ alignment chain files available from the UCSC databases (http://hgdownload.cse.ucsc.edu/downloads.html) for the species. If the chain files are not available, they can be generated in-house using LastZ (http://www.bx.psu.edu/~rsharris/lastz/). For example, to map from human to pig, use: hg19ToSusScr3.over.chain.gz and susScr3ToHg19.over.chain.gz. To map from human to rabbit, use: hg19ToOryCun2.over.chain.gz and oryCun2.hg19.all.chain.gz.

- The minMatch thresholds for regions with strict reciprocal map (minMatchMain) and for regions with multiple maps but strict sequence identity (minMatchMulti) are required parameters. We have tested and found the optimal thresholds as: minMatchMain=0.20 and minMatchMulti=0.80. Users can change these parameters if needed. 

- More information on comparing the HPRS application to 10 mammalian species, on comparing minMatch parameters, and on selecting a suitable combination of regulatory datasets will be available soon in a manuscript under preparation.

- To run mapping for multiple files, submit multiple batch jobs (one job per tissue/cell line/condition):

```
for file in *bed *OriHuman; do sbatch -e $file.STDERR pythonMap.bat $file; echo $file; sleep 1; done

```
- An example of the bash script for mapping by running the python script:
```
#!/bin/bash
#SBATCH --job-name="PyLO"
#SBATCH --time=01:00:00
#SBATCH --mem=40Gb

# {1} is the name of the bedfile containing regulatory regions in human 

python ./LiftOver_BackLiftOver_PermitMultipleBedsIn1folder.py  ${1} ../hg19ToCavPor3.over.chain.gz  ../cavPor3ToHg19.over.chain.gz 0.10 0.90

# The program will run using 4 cpus, it takes ~ 10 minute for a dataset of 90K regions
# Can save this bash script as pythonMap.bat; then submit multiple jobs:
# for file in *bed *OriHuman; do sbatch -e $file.STDERR pythonMap.bat $file; echo $file; sleep 1; done


```

- After running, files can be merged and formatted using this Script PostHPRSMapping_MergeDifferentDatabaseTypes.py. As an example, we used this script to combine data from 88 tissues, with other 5 types of datasets: promoters, enhancers, distal and proximal TFs, and Villar regulatory regions.


- Optionally, if users want to add tissue/condition/cell type information, the script PostMapping_HPRSpipeline_Add_IDs.py. The output of this script is convenient because it allows counting how many samples the predicted regions appear, and it helps later analysis when users want to check which tissues/conditions the regulatory regions are identified. An example of the output is:

```
==> Combined_all88Tis_SortedMerged.bed <==
chr1    21      1448    E053_Neurosph7_EnhID_102213,E057_Epithelial7_Enh_ID108825,E066_Other7_EnhID_95322,E043_Blood7_Enh_ID73048,E093_Thymus7_Enh_ID80744,E098_Other7_EnhID_97012,E091_Other7_EnhID_102712,E046_HSC12_EnhBiv_ID77590,E079_Digestive7_EnhID_74275,E095_Heart7_EnhID_101840,E085_Digestive7_Enh_ID89371,E032_HSC7_Enh_ID82067,E023_Mesench7_Enh_ID135314,E025_Mesench7_Enh_ID144011,E052_Myosat7_Enh_ID116705,E075_Digestive7_EnhID_48995,E092_Digestive7_Enh_ID95214,E040_Blood7_Enh_ID69216,E102_Digestive7_EnhID_77945,E041_Blood7_Enh_ID83348,E112_Thymus7_EnhID_50987


```



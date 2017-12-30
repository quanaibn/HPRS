# This is to count CAGE peaks within each predicted regulatory region
1. Inputs include 2 bedfiles: a CAGE peak file, and a regulatory region file
2. Use the bedtools coverage command, for example: 

```
# {1} is the bedfile containing all CAGE peaks mapped to the species
bedtools coverage -a  Merged_88Tis_suScr3_IDs.bed  -b ${1}  >${1}.CAGEcount88Tis5Dat
```

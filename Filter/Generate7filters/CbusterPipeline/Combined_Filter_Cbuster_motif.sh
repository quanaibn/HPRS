#!/bin/bash
#SBATCH --job-name='Combine'
#SBATCH --time=01:00:00

#Combine all the bed files while filter by quality 20 at the same time
for file in CombinedCbuste*.fa; do awk '$4 >20' $file >>Combined_all_motif_filterCbustOver20.bed; done



sort -k1,1 -k2,2n Combined_all_motif_filterCbustOver20.bed > Combined_all_motif_filterCbustOver20.bedSortedtemp

bedtools merge -c 5 -o collapse -i Combined_all_motif_filterCbustOver20.bedSortedtemp >Combined_all_motif_filterCbustOver20_Merged.bed

rm Combined_all_motif_filterCbustOver20.bedSortedtemp

rm Combined_all_motif_filterCbustOver20.bed


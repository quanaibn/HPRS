# Annotations from HPRS pipeline include:
1. CAGE peaks
2. CAGE enhancers
3. Villar enhancers
4. Villar promoters
5. Mapped ROADMAP enhancers from 88 tissues (each tissue is counted as 1 annotation)
6. ENCODE proximal TFs
7. ENCODE distal TFs

## The above annotations are integrated into predicted regulatory regions. Each region may contain more than 1 annotations. The more annotations a region contains, the more likely it is a functional regulatory region.

## The 7 datatypes above can be merged, and combined into one file with the following format (example): 

```
chr1	77158	77323	CTCF,CTCFL,ZBTB7A_124627
chr1	79303	79669	7_EnhID_3130,7_EnhID_3436_1
chr1	80169	80931	CTCF,RAD21_124626,7_EnhID_1962,7_EnhID_3008_2
chr1	81552	82133	7_EnhID_1577_3
chr1	95141	95309	MAX_43377
```


## The following commands can be used to count the number of annotations:
```
awk '{FS="\t"}{print $4}'  Merged_88Tis_5dat_suScr3_Final.bed |sed 's/,/\t/g'|awk '{print NF}' >Merged_88Tis_5dat_suScr3_Final_CountField.bed

paste Merged_88Tis_5dat_suScr3_Final_IDs.bed Merged_88Tis_5dat_suScr3_Final_CountField.bed >Merged_88Tis_5dat_suScr3_Final_CountField.bedt
```

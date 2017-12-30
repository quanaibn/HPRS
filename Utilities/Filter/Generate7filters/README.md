# This folder is for preparing filters. It contains methods for:
- Calculating RNAseq mapped on regulatory regions (MORR), see the folder RNAseq_H3K27Ac_pipeline
- Calculating H3K27Ac signal MORR, see the folder RNAseq_H3K27Ac_pipeline
- Calculating PhastCons scores MORR, see the file PhastCons.md
- Mapping and counting TFBSs MORR, see the folder CbusterPipeline
- Integrating gkmSVM scores for each of the regulatory region, see the folder /RegulatorySNP/PrepareTrainingSets 
- Counting CAGE peaks MORR, see the file CAGEpeakCount.md
- Counting annotations MORR, see the file CountAnnotation.md

1. The following examples are for outputs of each of the 7 filters, which were then merged into a metadata table for filtering

```
# Count annotations
Merged_88Tis5datsuScr3_CountAnnotation          
==> Merged_88Tis5datsuScr3_CountAnnotation <==
chr1    77158   77323   88T5DsusS3_ID1  3
chr1    79303   79669   88T5DsusS3_ID2  2

#RNAseq for 27 tissues
Merged_88Tis5datsuScr3IDs_RNAseq_featurecountFPKM
==> Merged_88Tis5datsuScr3IDs_RNAseq_featurecountFPKM <==
Ids     ERR789427.sam1.bam1     ERR789428.sam1.bam1     ERR789429.sam1.bam1     ERR789430.sam1.bam1     ERR789431.sam1.bam1       ERR789432.sam1.bam1     ERR789433.sam1.bam1     ERR789434.sam1.bam1     ERR789443.sam1.bam1     ERR789444.sam1.bam1       ERR789445.sam1.bam1     ERR789446.sam1.bam1     ERR789447.sam1.bam1     ERR789448.sam1.bam1     ERR789449.sam1.bam1       ERR789450.sam1.bam1     ERR972387.sam1.bam1     ERR972388.sam1.bam1     ERR972389.sam1.bam1     ERR972391.sam1.bam1       ERR972392.sam1.bam1     ERR972393.sam1.bam1     ERR972394.sam1.bam1     SRR653843.sam1.bam1     SRR653844.sam1.bam1       SRR653845.sam1.bam1     SRR653846.sam1.bam1
88T5DsusS3_ID1  0       0       0       0       0       0       0       0       0       0       0       0       0       000       0       0       0       0       0       0       0       0       0       0       0


#H3K27Ac
Merged_88Tis5datsuScr3_H3K27Ac_featurecountFPKM  
==> Merged_88Tis5datsuScr3_H3K27Ac_featurecountFPKM <==
Ids     ERR572204.fastq.gz.sam1.bam1    ERR572214.fastq.gz.sam1.bam1    ERR572261.fastq.gz.sam1.bam1
88T5DsusS3_ID1  0.972325334713095       2.51887919636419        1.61621409878005

#SVM scores
Merged_88Tis5datsuScr3IDs_SVM_Enhscores
==> Merged_88Tis5datsuScr3IDs_SVM_Enhscores <==
88T5DsusS3_ID1  1.2327
88T5DsusS3_ID2  2.80966

#PhastCons
Merged_88Tis5datsuScr3toHg19_PhastCons
==> Merged_88Tis5datsuScr3toHg19_PhastCons <==
chr1    566153  566281  88T5DsusS3_ID443390     0.6645176471
chr1    566361  566417  88T5DsusS3_ID443391     0.6110833333

#CAGE peak counts
Merged_88Tis5datsuScr3IDsCAGEpeak.bed           
==> Merged_88Tis5datsuScr3IDsCAGEpeak.bed <==
chr1    77158   77323   88T5DsusS3_ID1  0       0       165     0.0000000
chr1    79303   79669   88T5DsusS3_ID2  0       0       366     0.0000000


#TFBS count
Merged_88Tis5datsusScr3CbustOver20_EncTransJasp_TFBS
==> Merged_88Tis5datsusScr3CbustOver20_EncTransJasp_TFBS <==
chr1    77158   77323   88T5DsusS3_ID1  1       165     165     1.0000000
chr1    79303   79669   88T5DsusS3_ID2  1       366     366     1.0000000

```

2. The above outputs are reformmated before merging into a metadata set. Note that the RNAseq and H3K27Ac initial outputs contain multiple columns for multiple samples, and they are processed to calculate mean/max values of all samples (by using the MeanH3K27Ac.R and MaxRNAseq.R script). The following examples are for 7 reformated outputs:


```
#Following commands can be used for reformatting 
awk '{OFS="\t"}{print $4, $1, $2, $3, $5}' Merged_88Tis5datsuScr3_CountAnnotation >AnnCount.Temp

awk '{OFS="\t"}{print $4, $5}' Merged_88Tis5datsuScr3IDsCAGEpeak.bed >CAGEpeak.Temp

awk '{OFS="\t"}{print $4, $5}' Merged_88Tis5datsuScr3toHg19_PhastCons >PhastCons.Temp

awk '{OFS="\t"}{print $4, $5}' Merged_88Tis5datsusScr3CbustOver20_EncTransJasp_TFBS >TFBS.Temp

Rscript --vanilla MaxRNAseq.R Merged_88Tis5datsuScr3IDs_RNAseq_featurecountFPKM

mv Merged_88Tis5datsuScr3IDs_RNAseq_featurecountFPKM RNAseq.Temp

Rscript --vanilla MeanH3K27Ac.R Merged_88Tis5datsuScr3_H3K27Ac_featurecountFPKM

mv Merged_88Tis5datsuScr3_H3K27Ac_featurecountFPKM H3K27Ac.Temp

```
```
# Followings are the outputs 

==> AnnCount.Temp <==
88T5DsusS3_ID1  chr1    77158   77323   3
88T5DsusS3_ID2  chr1    79303   79669   2

==> CAGEpeak.Temp <==
88T5DsusS3_ID1  0
88T5DsusS3_ID2  0

==> H3K27Ac.Temp <==
88T5DsusS3_ID1  1.70247287661911
88T5DsusS3_ID2  1.54734483679358

==> PhastCons.Temp <==
88T5DsusS3_ID443390     0.6645176471
88T5DsusS3_ID443391     0.6110833333

==> RNAseq.Temp <==
88T5DsusS3_ID1  0
88T5DsusS3_ID2  0

==> SVM.Temp <==
88T5DsusS3_ID1  1.2327
88T5DsusS3_ID2  2.80966

==> TFBS.Temp <==
88T5DsusS3_ID1  1
88T5DsusS3_ID2  1

```
3. The reformatted outputs are then merged using the Rscript: Merge_metadata.R
```
#Example of the outputs from Merge_metadata.R that are ready for the filtering pipeline are:
IDs	Chr	Start	End	Length	AnnotationCount	CAGEcount	TFBSCount	MeanH3K27Ac	phastCons	MaxRNAseq	SVM
88T5DsusS3_ID1	chr1	77158	77323	166	0.0180722891566265	0	0.00602409638554217	1.70247287661911	0.006018518519	0	1.2327
88T5DsusS3_ID10	chr1	164395	164973	579	0.00518134715025907	0	0.00172711571675302	1.31586779472031	0.086260181	0.0604352546818577	3.54446

```





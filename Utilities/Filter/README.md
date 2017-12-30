# This filtering step is used after the mapping step

## It selects from the intial mapped regions (universal dataset) a filtered dataset containing top regulatory regions more likely to be functional in the target species

## The main script is shown as an R markdown file: HPRS_Filtering_pipeline.Rmd. It uses a summary table containing 7 species-specific values for each of the predicted region in the universal dataset.

## For instructions on preparing the summary table input, including methods to generate species-specific data for each of the regulatory region, see the subfolder Generate7filters

```
#Example of the summary table, each row is one regulatory region

                  IDs   Chr    Start      End Length AnnotationCount CAGEcount    TFBSCount MeanH3K27Ac   phastCons   MaxRNAseq      SVM
1      88T5DsusS3_ID1  chr1    77158    77323    166    0.0180722892         0 0.0060240964  1.70247288 0.006018519 0.000000000 1.232700
2     88T5DsusS3_ID10  chr1   164395   164973    579    0.0051813472         0 0.0017271157  1.31586779 0.086260181 0.060435255 3.544460
3    88T5DsusS3_ID100  chr1   810656   813811   3156    0.0003168568         0 0.0009505703  2.23415926 0.019840621 0.527487477 7.953410

```  

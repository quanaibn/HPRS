import numpy as np
import pandas as pd
import os, sys
import subprocess
import optparse

def main(argv=sys.argv) :
    usage = "Usage: %prog Readcount pattern fasta"
    desc  = "it take the name of negative regions in the fasta file, and search the featureCount output files for sequences that have no signal (the total count of all reads from all H3K27Ac samples that are mapped to the negative region <= 1), then file the fasta sequences" 
    parser = optparse.OptionParser(usage=usage, description=desc)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 3:
        parser.error("incorrect number of arguments. Please add readcount, pattern, and RefFa")
    global ReadCount; ReadCount=args[0] #bed4 format
    global pattern; pattern=args[1] #pattern for columns containing counts as the combined file from featureCount output,so the it will read the counts and filter according to these columns
    global RefFa; RefFa=args[2] #This is the genome fasta sequence of the species, it is used to get fasta sequences for a bed file
    
    print(ReadCount); print(pattern)
 
    oriMaoCount = pd.read_table(ReadCount, skiprows=[0], header=0, sep="\t")
    oriMaoS =oriMaoCount.ix[:,6:].copy()
    oriMaoSH3K27Ac=oriMaoS.filter(like= pattern,axis=1) #pattetn for columns with count
    # print(oriMaoCount.columns)
    oriMaoSH3K27Ac['total']=oriMaoSH3K27Ac.sum(axis=1) #this is the rowsum for all samples 
    #df_c = pd.concat([df_a.reset_index(drop=True), ], axis=1)
    df_c = pd.concat([oriMaoSH3K27Ac.reset_index(drop=True), oriMaoCount[['Geneid', 'Chr', 'Start', 'End']]], axis=1)
    # oriMaoSH3K27Ac['IDs']=oriMaoCount['Geneid']
    df=df_c.copy()
    df=df.query('total<=1')
    print("filtered negative dat", df.head()); print("filtered dat size", df.shape); print("original dat size",oriMaoCount.shape)

    df[[ 'Chr', 'Start', 'End','Geneid']].to_csv('{0}_NosignalVillar.bed'.format(ReadCount), sep='\t', index=False, header=False)

#     bed =pd.read_table('{0}_NosignalVillar.bed'.format(bed),  header=None, sep="\t")

    cmd='bedtools getfasta -fi {1} -bed {0}_NosignalVillar.bed -fo {0}_NosignalVillar.fasta'.format(ReadCount,RefFa)

    subprocess.call(cmd, shell=True)
if __name__ == '__main__': main()

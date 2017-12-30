"""
- This script is to take the summit file from histone mark assays and find the regions with highest peaks
- The script uses the first summit peak as the top one for a cluster (as is the case for the Villar dataset, from MACS2 peakcaller)
- After defining the peak, it extends left and right with 50 bp to form a 100 bp window centered at the peak
"""

import numpy as np
import pandas as pd
import os, sys
import subprocess
import optparse

# os.chdir('/datastore/ngu121/HPRSforPig/HistoneMark/Villar_forPig/MacsPeakFiles')

def listPeak(rowbed,chromo, IDs):
    newRow = rowbed.replace('set(', '').replace(')','').replace('[','').replace(']','')
    listRow =newRow.split(',')
    numMem = len(listRow)
    listRownew =listRow
    for i in range(0,numMem):
        listRownew[i] = [(int(listRownew[i])-50), (int(listRownew[i])+50)]+['chr'+ str(chromo), IDs+'_'+str(i)]
    return(pd.DataFrame.from_dict(listRownew))
# MacsFile='susScr-H3K27Ac_replicated-peaks_macs'
def main(argv=sys.argv) :
    usage = "Usage: %prog MacsPeakFile"
    desc  = "1) read a MacsPeak file; 2) find the first summit peak as the top one for a cluster (as is the case for the Villar dataset, from MACS2 peakcaller); extend 50 bp to the left and right of the selected peak; 4) it writes the output file with the name as ${base}__Multiple_HighestPeak.bed"
    parser = optparse.OptionParser(usage=usage, description=desc)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 1:
        parser.error("incorrect number of arguments. Please add path with file extension")
        sys.exit(0)
    global MacsFile; MacsFile=args[0]
    original = pd.read_table(MacsFile)
    print(original.head(n=2))
    dfSmall = original[['Summits', 'Chrom', 'ID']]
    print('small dat \n'); print(dfSmall.head(n=2)) 
    df=pd.DataFrame()
    #Note: this loop takes quite a long time to finish, a reporter is added for every 500 enhancers
    for i in range(0,len(dfSmall['Chrom'])):
        dftemp = listPeak(dfSmall['Summits'][i],dfSmall['Chrom'][i],dfSmall['ID'][i])
        if i%500==0:
            print("Done from 0 to {0}".format(i))
        df=pd.concat([df,dftemp])
    df=df.reset_index(drop=True)
    df.columns = [ 'start','end','chr','IDs']
    df=df[['chr', 'start', 'end','IDs']]
    df.to_csv('{0}_Multiple_HighestPeak.bed'.format(MacsFile), sep='\t', index=False, header=False)
if __name__ == '__main__': main()

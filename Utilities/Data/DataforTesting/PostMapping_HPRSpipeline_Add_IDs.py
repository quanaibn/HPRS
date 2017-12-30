"""This script for an additional step to add unique name to feature IDs. It is useful for combining multiple datasets from different tissues, cell lines. \
 The input files include a name file with 2 columns: ID column has IDs in the file names; the names columns has unique names.\
 Example: 
    E023    E023_Mesench
    E025    E025_Mesench
 It writes a new file with the unique ids, another file with the merged of all databases.\
 Change file name and extension string accordingly to your files"""

from subprocess import call
import os, subprocess
import glob
import pandas as pd

names =pd.read_table('./listAll_primaryTissues_primaryCells_BloodSkin', header=None,  sep="\t",
                       names=['IDs','names'])
print(names.head(n=3))
dat=pd.DataFrame()
length=len(names['names'])

for i in range(0,length):
    datfile = glob.glob('./{0}.*080'.format(names['IDs'][i])) #double check the name format of the final Multi080 here in the directory
    print(datfile)
    original = pd.read_table(datfile[0], header=None, sep="\t",names=['chr','start', 'end','IDs'])
    original['IDs']=original['IDs'].apply(lambda x: names['names'][i] +x)
    datfilename = '{0}.formated'.format(datfile[0])
    original.to_csv(datfilename,sep='\t', index=False, header=False)
    dat = pd.concat([dat, original])
    print("tissue :", datfile, dat.shape)

  
dat.to_csv('Combined_all88Tis.bed',sep='\t', index=False, header=False)

cmd1="sort -k1,1 -k2,2n Combined_all88Tis.bed >Combined_all88Tis_Sorted.bed"
cmd2="bedtools merge -c 4 -o collapse -i Combined_all88Tis_Sorted.bed >Combined_all88Tis_SortedMerged.bed" #after this step, should double check the SortedMerged file

subprocess.call(cmd1, shell=True); print("done sorted")
subprocess.call(cmd2, shell=True); print("done merged")

"""
- This script first calculate the mean repetitive content of all the Fasta sequences in the positive set. Then, it filter sequences that have  higher repetitive content than the mean of the determined repetitive content in the positive set
- The script has 2 parts: 1) first calculate the repeat content (by the function CalculateREPEATfasta(file)), which take a reference fasta file from the training set, 2) filter fasta sequences with repeat content higher than a threshold calculated from 1  
- Note: Users change the input file name in the script in the following codes accordingly:
    + REPEATcontent = CalculateREPEATfasta('PositiveH3K27Acregions_Top15k.bed_NoN.fasta')
    + FilterFastaByREPEAT('RandomH3K27Acregions_withNosignalVillar.fasta', 'RandomH3K27Acregions_withNosignalVillar_GCfilter.fasta', REPEATcontent) 
    + FilterFastaByREPEAT('PositiveH3K27Acregions_Top15k.bed_NoN.fasta', 'PositiveH3K27Acregions_Top15k.bed_NoN_GCfilter.fasta', REPEATcontent)
     
"""
import numpy as np
import pandas as pd
import os
import subprocess

def CalculateREPEATfasta(file):
    Infile =open(file,'r')
    lines =Infile.readlines()
#     print(lines[0]); print(len(lines))
    Infile.close()
    repeat_content = list(range(0,len(lines)))
    for i in range(len(lines)): #for i in arange
        count_repeat = 0
        if lines[i][0] !=">":
            count_repeat = lines[i].count('a') + lines[i].count('t') +lines[i].count('g') + lines[i].count('c') #repeats are small letter seq
            repeat_content[i] = count_repeat/float(len(lines[i]))
        else: 
            repeat_content[i] = 'sequence name' #this is  to check print repeat_content[i]
#             print(count_repeat) #delete this later
    sum_repeat =0
    counter =0 
    for i in range(len(lines)):
        if repeat_content[i] != 'sequence name': 
            sum_repeat =sum_repeat + repeat_content[i] 
            counter = counter +1 
#     c=list(range(1,len(lines),2))
#     newarray = [ repeat_content[int(i)] for i in c ]
#     print(median(newarray)); print(newarray[1:10])
    print(sum_repeat/counter) 
    return (sum_repeat/counter) 


REPEATcontent = CalculateREPEATfasta('PositiveH3K27Acregions_Top15k.bed_NoN.fasta') # change the input file name here
    
# The script filter repeat content to lower than a threshold  that is calculated by the repeat content script
# usage: %prog fastafilename filteredfile

def FilterFastaByREPEAT(file, outfile,REPEATcontent):
    Infile =open(file,'r')
    lines =Infile.readlines()
    Infile.close()
    outfile =open(outfile, 'w')
    for i in range(len(lines)):
        if lines[i][0]!=">":
            count_repeat = lines[i].count('a') + lines[i].count('c')+ lines[i].count('t') +lines[i].count('g')
            if count_repeat/float(len(lines[i])) < REPEATcontent: # change repeat contentthrehold here
                print (count_repeat/float(len(lines[i])))
                outfile.write(str(lines[i-1]))
                outfile.write(str(lines[i]))
    outfile.close()
FilterFastaByREPEAT('RandomH3K27Acregions_withNosignalVillar.fasta', 'RandomH3K27Acregions_withNosignalVillar_GCfilter.fasta', REPEATcontent)
FilterFastaByREPEAT('PositiveH3K27Acregions_Top15k.bed_NoN.fasta', 'PositiveH3K27Acregions_Top15k.bed_NoN_GCfilter.fasta', REPEATcontent)

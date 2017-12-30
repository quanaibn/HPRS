"""
- This script creates a negative training set randomly selected through out the genomes (sequences at the same chromosome and have the same sizes to the reference sequences), containing 3 times more sequences than the positive training set. It only keeps randomly selected sequences  without N in the fasta
"""

import numpy as np
import pandas as pd
import os, sys
import subprocess
import optparse

def getFastanoN(bed1, bed2, genomefa):
    # get fasta sequence for the bed1 file (e.g bed1 is the bosTauENHANCERS_Peak300_Rep2xRandom.bed)
    cmd2="bedtools getfasta -fi {1} -bed {0} -fo {0}.fasta -name".format((bed1),(genomefa))
    subprocess.call(cmd2, shell=True)
    # get names of sequences with N 
    cmd3='grep -B1 -i n {0}.fasta | grep ">" | sed \'s/>//g\' >nameRandomWithN'.format((bed1))
    subprocess.call(cmd3, shell=True)
    # load sequence names into a df
    name = pd.read_table('nameRandomWithN', sep="\t", header=None, names=['IDs'])
    name['order'] = np.arange(len(name['IDs'])) 
    # recover the coordinates for sequences with no N
    # the bed2 is the file generated in the main function, which randomly selects genomic regions (i.e. Negative regions) with 3 times the number of the original regions 
    t=pd.merge(name, bed2 , left_on ='IDs', right_on='IDs', how='right')
    # find coordinates for sequences that have N
    t2 =t[pd.isnull(t['order'])]
    # keep sequences without N
    t2=t2.dropna(axis=1)
    
    print("names: \n",name.head());print("names size", name.shape)
    print("all sequence: \n",t.tail(n=3)); print("all sequence: \n", t.shape);
    print("dat wihout N: \n", t2.tail(n=3)); print("sequence without N: \n", t2.shape)
    
    t2[['chr', 'start', 'end', 'IDs']].to_csv('{0}_NoN.bed'.format((bed1)), sep='\t', index=False, header=False)
    # get fasta sequences for those with no N
    cmd4='bedtools getfasta -fi {1} -bed {0}_NoN.bed -fo {0}_NoN.fasta -name'.format((bed1),(genomefa))

    subprocess.call(cmd4, shell=True)
    print(cmd4)

def main(argv=sys.argv) :
    usage = "Usage: %prog bed chrsize  genomefa"
    desc  = "it take a positive bed files, do random 3x the size, and create a fasta file for the random"
    parser = optparse.OptionParser(usage=usage, description=desc)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 3:
        parser.error("incorrect number of arguments. Please add bed and chrsize and genomefa")
    global bed; bed=args[0] #bed4 format
    global chrsize; chrsize=args[1] #e.g bosTau6.chrom.sizes_mainChrOnly
    global genomefa; genomefa=args[2] #e.g bosTau6.chrom.sizes_mainChrOnly
    print(bed); print(chrsize)
    original = pd.read_table(bed, header=None, sep="\t",
                       names=['chr','start', 'end','IDs'])
    original2 = original.copy()
    original3 = original.copy()
    original2['IDs']=original2['IDs'].apply(lambda x: x+'rep2')
    original3['IDs']=original2['IDs'].apply(lambda x: x+'rep3')
    original3rep =pd.concat([original, original2, original3])
    original3rep.to_csv('{0}_rep3x.bed'.format(bed), sep='\t', index=False, header=False)
    print("original2 \n", original2.head(n=2)); print("original2 shape \n", original2.shape); print("original3rep shape \n", original3rep.shape);
    print("original3rep tail \n", original3rep.tail(n=2))
    cmd1= 'bedtools shuffle -i {0}_rep3x.bed -g {1} -noOverlapping > {0}_Rep3xRandom.bed'.format((bed),(chrsize))

    subprocess.call(cmd1, shell=True)

    bed_Rep3xRandom = pd.read_table('{0}_Rep3xRandom.bed'.format(bed), header=None, sep="\t",
                           names=['chr','start', 'end','IDs'])
    getFastanoN('{0}_Rep3xRandom.bed'.format(bed), bed_Rep3xRandom,genomefa)

if __name__ == '__main__': main()

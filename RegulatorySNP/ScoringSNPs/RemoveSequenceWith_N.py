#this is the modified sccript create negative size 3 times the positive, it keeps random without N in the fasta seqs
import numpy as np
import pandas as pd
import os, sys
import subprocess
import optparse

def getFastanoN(bed1, bed2, genomefa):
    # bed1 is the bosTauENHANCERS_Peak300_Rep2xRandom.bed
    cmd2="bedtools getfasta -fi {1} -bed {0} -fo {0}.fasta -name".format((bed1),(genomefa))
    subprocess.call(cmd2, shell=True)

    cmd3='grep -B1 -i n {0}.fasta | grep ">" | sed \'s/>//g\' >nameRandomWithN'.format((bed1))
    subprocess.call(cmd3, shell=True)
    
    name = pd.read_table('nameRandomWithN', sep="\t", header=None, names=['IDs'])
    name['order'] =np.arange(len(name['IDs']))
    
    # bed1 bosTauENHANCERS_Peak300_Rep2xRandom.bed
    t=pd.merge(name, bed2 , left_on ='IDs', right_on='IDs', how='right')
    # find coordinates for sequences that have N
    t2 =t[pd.isnull(t['order'])]
    #keep sequences without N
    t2=t2.dropna(axis=1)
    
    print("names: \n",name.head());print("names size", name.shape)
    print("all sequence: \n",t.tail(n=3)); print("all sequence: \n", t.shape);
    print("dat wihout N: \n", t2.tail(n=3)); print("sequence without N: \n", t2.shape)
    
    t2[['chr', 'start', 'end', 'IDs']].to_csv('{0}_NoN.bed'.format((bed1)), sep='\t', index=False, header=False)

    cmd4='bedtools getfasta -fi {1} -bed {0}_NoN.bed -fo {0}_NoN.fasta -name'.format((bed1),(genomefa))

    subprocess.call(cmd4, shell=True)
    print(cmd4)

def main(argv=sys.argv) :
    usage = "Usage: %prog bed chrsize"
    desc  = "it take a positive bed files, do random 3x the size, and create a fasta file for the random"
    parser = optparse.OptionParser(usage=usage, description=desc)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 2:
        parser.error("incorrect number of arguments. Please add bed and chrsize and genomefa")
    global bed; bed=args[0] #bed4 format
    global genomefa; genomefa=args[1] #e.g bosTau6.fa
    print(bed); print(genomefa);
    bedOri= pd.read_table(bed, header=None, sep="\t",names=['chr','start', 'end','IDs'])
    getFastanoN(bed, bedOri, genomefa)
    
if __name__ == '__main__': main()
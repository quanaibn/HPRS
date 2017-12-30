"""
- This script parse Cbuster output files and combine them to create a merged bed file 
- Run this program with 2 arguments in shell with quote for argv2, such as: python PostCbuster_parsing.py /flush1/ngu121/TFBS_10k/forbTau6/Encode/Test '*fa', 
the * is to be included in the pattern '*fa'
"""
import os, glob, sys
import optparse
def main(argv=sys.argv):
    parser = optparse.OptionParser()
    (options, args) = parser.parse_args()
    if len(args) != 2:
        parser.error("incorrect number of arguments: input 1) path and 2) pattern")
        sys.exit(0)
    path=args[0]
    pattern=args[1]    
    #change directory to folder containing Cbuster files
    os.chdir(path)
    print(path); print('current working directory' +os.getcwd())
    #read list files containing output
    flist =glob.glob('*.{0}'.format(pattern))
    line= 'list file with' +'\t'+ pattern + '\t'+ 'has'+ '\t'+  str(len(flist)) +'\t' + 'files' +'\n'
    print(line)
    for ffasta in flist:
        fname =ffasta.split('/')[-1]
        print(fname)
        CombinedEncode = open('CombinedCbust{0}'.format(ffasta), 'w')
        with open(ffasta) as lines:
            for line in lines:
                if line[0] == '>':
                    name=line[1:6]
                    lname=[name]
                if line[0] == '#':
                    motif = line.split()[4]
                if line[0] in ['1','2','3','4','5','6','7','8','9']:
                    coord =[line.split()[i] for i in [1,2,3]]
                    lineTowrite = name + '\t'+ '\t'.join(coord) +'\t' + motif +'\n'
                    CombinedEncode.write(lineTowrite)
        CombinedEncode.close()

if __name__ == '__main__': main()

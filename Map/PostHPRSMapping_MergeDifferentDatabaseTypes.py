"""This script allow combining multiple output from the HPRS mapping pipeline.\
 Format of the output file is a bed4 file with 4 columns: chr, start, end, name
 It sorts and merges all databases.\
 Note: Change file name and extension string accordingly to your files"""

from subprocess import call
import os, glob, sys, subprocess
import pandas as pd
import optparse
import shutil

def mergeBed(path):    
    listFileToMerge = glob.glob(path)
    MergedFiles = pd.DataFrame()
    fnumber =len(listFileToMerge)
    print('Will merge {0} files'.format(fnumber))
    for file in listFileToMerge[0:fnumber+1]:
        print('Adding the file {0}'.format(file))
        bedtemp=pd.read_table(file, header=None, sep="\t", names=['chr','start', 'end','IDs'])
        bedtemp[['start','end']]=bedtemp[['start','end']].astype(int)
        MergedFiles =pd.concat([MergedFiles,bedtemp])
    return MergedFiles

def main(argv=sys.argv) :
    usage = "Usage: %prog path"
    desc  = "1) take a path containing a pattern for listing all files wanted to merge, 2) combined into one big file, 3) write tempfile to\
    directory, 4) sort and merge temp file using Linux 4)remove temp files"
    parser = optparse.OptionParser(usage=usage, description=desc)
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 1:
        parser.error("incorrect number of arguments. Please add path with file extension")
        sys.exit(0)
    global path; path=args[0]
    mergedAllfiles = mergeBed(path)
    mergedAllfiles.to_csv('mergedAllfiles.Temp',sep='\t', index=False, header=False)

    cmd1="sort -k1,1 -k2,2n mergedAllfiles.Temp >mergedAllfiles_Sorted.Temp"
    cmd2="awk 'NF==4' mergedAllfiles_Sorted.Temp >mergedAllfiles_Sorted_formated.Temp"
    cmd3="bedtools merge -c 4 -o collapse -i mergedAllfiles_Sorted_formated.Temp >Allfiles_SortedMerged.bed"
    print("sorting")
    subprocess.call(cmd1, shell=True); print("done sorted, started formating file")
    subprocess.call(cmd2, shell=True); print("started merging")    
    subprocess.call(cmd3, shell=True); print("done merged")

    # remove temporary files
    flist =glob.glob('./*Temp')
    for f in flist:
        print('removing {0}'.format(f))
        os.remove(f)
if __name__ == '__main__': main()
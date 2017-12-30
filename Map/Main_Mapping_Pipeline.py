import os, glob, sys
import subprocess
from multiprocessing import Pool
import pandas as pd 
import optparse
import shutil
#require Anaconda installed for python3.5.0 (Installed in Ruby), run with parallel, allowing memory 40Gb because the chain file is large
#os.chdir('/datastore/ngu121/notebooks/HPRSpipeline')

def liftOverParam(bed1):
    cmd4="liftOver -minMatch={4} {0} {3} \
 {1} {2}".format((bed1), (bed1 + ".LO_{0}".format(minMatchMain)), (bed1 + ".UNlo_{0}".format(minMatchMain)), (chainfileHUMAN), (minMatchMain))
    subprocess.call(cmd4, shell=True)
    return print(cmd4)

def backliftOver(bed1):
    cmd4="liftOver -minMatch={4} {0} {3} \
 {1} {2}".format((bed1), (bed1 + ".backLO"), (bed1 + ".backUNlo"), (chainfileSPECIES), (minMatchMain))
    subprocess.call(cmd4, shell=True)
    return print(cmd4)

def liftOverMulti(bed1):
    cmd4="liftOver -minMatch={4} -multiple {0} {3} \
 {1} {2}".format((bed1), (bed1 + ".LO_{0}".format(minMatchMulti)), (bed1 + ".UNlo_{0}".format(minMatchMulti)), (chainfileHUMAN),(minMatchMulti))
    subprocess.call(cmd4, shell=True)
    for file in glob.glob('./{0}.LO_{1}'.format(bed1,minMatchMulti)):
        temp=pd.read_table(file, header=None, sep="\t", names=['chr','start', 'end','IDs', 'count'])
        temp[['chr', 'start', 'end', 'IDs']].to_csv(file, sep='\t', index=False, header=False)
    return print(cmd4)

def splitFile(bed1):
    bed = pd.read_table(bed1, header=None, sep="\t",names=None)
    orilength = len(bed[1])
    splitlength=int(orilength/4)
    bed1 =bed[0:splitlength];bed2 =bed[splitlength+1:splitlength*2]; bed3=bed[splitlength*2+1:splitlength*3];
    bed4 =bed[splitlength*3+1:orilength+1]
    listbed =[bed1, bed2,bed3,bed4]
    return listbed

def bedtoolPy(bed1):
    test = splitFile(bed1)
    test[0].to_csv('{0}.split1'.format(bed1),sep='\t', index=False, header=False)
    test[1].to_csv('{0}.split2'.format(bed1),sep='\t', index=False, header=False)
    test[2].to_csv('{0}.split3'.format(bed1),sep='\t', index=False, header=False)
    test[3].to_csv('{0}.split4'.format(bed1),sep='\t', index=False, header=False)
    if __name__ == '__main__':
        p = Pool(4)
        p.map(liftOverParam, ['{0}.split1'.format(bed1), '{0}.split2'.format(bed1),'{0}.split3'.format(bed1),
                              '{0}.split4'.format(bed1)])

def mergeBed(path):    
    listBackLO = glob.glob(path)
    mergeBackLO = pd.DataFrame()
    fnumber =len(listBackLO)
    for file in listBackLO[0:fnumber+1]:
        bedtemp=pd.read_table(file, header=None, sep="\t", names=['chr','start', 'end','IDs'])
#        print(bedtemp.shape)
        mergeBackLO =pd.concat([mergeBackLO,bedtemp])
    return mergeBackLO

def loMultiNotExactMatch(mergeLOMain, ExactMatchMain, bed):
    #the file ExactMatchMain from findExactMat(bed,mergeBackLO)
    common = mergeLOMain.merge(ExactMatchMain,on=['IDs'])
    NotExactMatch = mergeLOMain[(~mergeLOMain.IDs.isin(common.IDs))]
    NotExactMatchHumanTemp =pd.merge(original, NotExactMatch, left_on ='IDs', right_on='IDs', how='inner')
    NotExactMatchHuman=NotExactMatchHumanTemp[['chr_x', 'start_x', 'end_x', 'IDs']]
    NotExactMatchHuman.to_csv('{0}.NotExactMatchHumanMain.bed'.format(bed), sep='\t', index=False, header=False)
    liftOverMulti('{0}.NotExactMatchHumanMain.bed'.format(bed))
    return NotExactMatchHuman

def findExactMat(mergeBackLO, mergeLOMain):
    #the file mergeBackLO from mergeBackLO = mergeBed('./*backLO')
    t=pd.merge(mergeBackLO, original, left_on ='IDs', right_on='IDs', how='left')
    t1 =t[(abs(t['start_y']-t['start_x']) <25) & (abs(t['end_y']-t['end_x']) <25) ]
    #the file mergeLOMain from 
    ExactMatchMain =pd.merge(t1, mergeLOMain, left_on ='IDs', right_on='IDs', how='left')
    ExactMatchMain=ExactMatchMain[['chr', 'start', 'end', 'IDs']] 
    ExactMatchMain.to_csv('{0}.ExactMatch_{1}'.format(bed,minMatchMain), sep='\t', index=False, header=False)
    return ExactMatchMain 


def main(argv=sys.argv) :
    usage = "Usage: %prog bedfile chainfileHuman chainfileSpecies"
    desc  = "1) take a bedfile, 2) split it into 4 and run parallel, 3) map minMatchMain backLo compare, 4)map multiple with minMatchMulti.\
    This script will generate one main output:OriginalBedFileName.mergeExactMainandMulti "
    parser = optparse.OptionParser(usage=usage, description=desc)
    parser.add_option("-v", action="store_true", dest="verbose", help="turn on  verbose while running")
    parser.add_option("-q", action="store_false", dest="verbose", help="turn off  verbose while running")
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.print_help()
        sys.exit(0)
    if len(args) != 5:
        parser.error("incorrect number of arguments: 1-bed, 2-chainHuman, 3-chainSpecies, 4-minMatchMain, 5-minMatchMulti")
        sys.exit(0)
    global bed; bed=args[0] 
    global chainfileHUMAN; chainfileHUMAN = args[1]
    global chainfileSPECIES; chainfileSPECIES = args[2]
    global minMatchMain; minMatchMain =args[3]
    global minMatchMulti; minMatchMulti=args[4]
    print('will project this file: {0}'.format(bed)); 
    print(chainfileHUMAN); print(chainfileSPECIES); 
    print('will use minMatchMain: {0}'.format(minMatchMain));
    print('will use minMatchMulti: {0}'.format(minMatchMulti));
    global original; original = pd.read_table(bed, header=None, sep="\t", names=['chr','start', 'end','IDs'])
    print('bottom sequences of the input bedfile'); print(original.tail())
    p = Pool(4)    
    #step 1: split and liftOver
    bedtoolPy(bed) #output extension: ".LO_".format(minMatchMain), ".UNlo_".format(minMatchMain) 
    print("done liftOver, proceeding to back liftOver \n")
    #step2: do backliftOver of the step1 liftOver; run 2 paralleled processes here
    p.map(backliftOver, ['{0}.split1.LO_{1}'.format(bed, minMatchMain), '{0}.split2.LO_{1}'.format(bed, minMatchMain),
                         '{0}.split3.LO_{1}'.format(bed,minMatchMain),'{0}.split4.LO_{1}'.format(bed, minMatchMain)])
    #output extension: ".backLO",".backUNlo"
  
    #step3: do liftOver with multimapping, use unliftOver as inputs; run 4 paralleled processes here    
    print("done back liftOver, proceeding to merging and matching \n")

    p.map(liftOverMulti, ['{0}.split1.UNlo_{1}'.format(bed, minMatchMain), '{0}.split2.UNlo_{1}'.format(bed, minMatchMain),
                          '{0}.split3.UNlo_{1}'.format(bed, minMatchMain),'{0}.split4.UNlo_{1}'.format(bed, minMatchMain)]) 
    #output extension: ".LO_".format(minMatchMulti)
    p.close() 
        
    mergeBackLO = mergeBed('./{0}*backLO'.format(bed)) #merge all backLO of the split1-4
    mergeLOMain = mergeBed('./{0}*LO_{1}'.format(bed,minMatchMain)) #merge all liftOver of the split1-4
    ExactMatchMain = findExactMat(mergeBackLO,mergeLOMain) #compare liftOver and back LO
    
    ##to create a df unique in LO file not exact match; file ExactMatchMain from findExactMat(bed,mergeBackLO)
    print("proceeding to multiple mapping \n")
    
    loMultiNotExactMatch(mergeLOMain, ExactMatchMain,bed)

    mergeAllLOMulti = mergeBed('./{0}*LO_{1}'.format(bed, minMatchMulti)) #merge all Multimap
    mergeExactMainandMulti =pd.concat([ExactMatchMain,mergeAllLOMulti])
    print("proceeding to writing output and arranging temp files \n")
    
    mergeExactMainandMulti.to_csv('{0}.mergeExact{1}MainandMulti{2}'.format(bed, minMatchMain, minMatchMulti),sep='\t', 
                                  index=False, header=False)
    # remove temporary files
    IMpath = './{0}.IntemediateFiles'.format(bed)
    if not os.path.isdir(IMpath):
        os.makedirs(IMpath)
    flist =glob.glob('./{0}.split*'.format(bed))
    flist.extend(glob.glob('./{0}*NotExactMatchHumanMain.bed*'.format(bed)))
    for f in flist:
        print(f)
        shutil.copy2(f,IMpath)
        os.remove(f)
if __name__ == '__main__': main()
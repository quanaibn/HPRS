- HPRS pipeline requires liftOver installed and the installed path is added to the shell PATH to call the liftOver by shell command in current working directory.
```
#Users may install the whole kentUtils from ENCODE github,
git clone git://github.com/ENCODE-DCC/kentUtils.git
#Follow the installation instruction in the kentUtils directory (), making sure to add the ./bin or copy the liftOver binary to the shell PATH. 
```
- For accessing common Python modules (Pandas, numpy, multiprocess ect.) to run  HPRS, install Anaconda from version 3-4.1.1 or higher:
```
#Download Anaconda
wget http://repo.continuum.io/archive/Anaconda3-4.1.1-Linux-x86_64.sh
bash Anaconda4-4.1.1-Linux-x86_64.sh 
#Then follow options on the shell screen, including setting up the environment PATH, for example:  export PATH="/home/ngu121/anaconda3/bin:$PATH"
```
- Other programs needed for running substeps of the pipeline that may require installation, from the following sources:

1. Install cluster-buster for scanning transcription factor binding sites following instruction from here http://zlab.bu.edu/cluster-buster/download.html
2. Install BWA for mapping RNAseq data following instruction from here: http://bio-bwa.sourceforge.net
3. Install Samtools for processing BAM files following instruction from here: http://samtools.sourceforge.net
4. Install featureCount following instruction from here:http://bioinf.wehi.edu.au/featureCounts/  
5. Install LS-gkm-SVM following instruction from here: https://github.com/Dongwon-Lee/lsgkm

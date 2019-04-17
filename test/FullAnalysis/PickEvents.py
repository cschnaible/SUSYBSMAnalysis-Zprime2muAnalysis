import sys
import ROOT as R
R.gROOT.SetBatch(True)
from DataSamplesTEST import *
import argparse
parser = argparse.ArgumentParser(description='Submit CRAB job to pick out specific event')
parser.add_argument('-d','--data',default=2018,type=int,help='Data taking year')
parser.add_argument('-t','--reco',default='PromptReco',type=str,help='Reconstruction')
parser.add_argument('-r','--run',default=318877,type=int,help='Run number')
parser.add_argument('-l','--lumi',default=102,type=int,help='Lumi number')
parser.add_argument('-e','--event',default=151594226,type=int,help='Event number')
args = parser.parse_args()

data = DataSample('foo',args.data,reco=args.reco,openROOT=False)
dataset = data.get_dataset(args.run)

requestName = 'event_'+str(args.run)+'_'+str(args.lumi)+'_'+str(args.event)
outputFileName = requestName+'.root'

printstr = \
'''
Pick Event {run}:{lumi}:{event}
Dataset {dataset}
Output File {outputFileName}
Request Name {requestName}
'''.format(requestName=requestName,run=args.run,event=args.event,outputFileName=outputFileName,dataset=dataset,lumi=args.lumi)
print printstr

tmpjson = '{\"'+str(args.run)+'\":[['+str(args.lumi)+','+str(args.lumi)+']]}'
open('tmp.json','wt').write(tmpjson)

evtlist = str(args.run)+':'+str(args.event)
open('evtlist.txt','wt').write(evtlist)

crabcfg = \
'''
from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = '{requestName}'
config.General.workArea = 'crab'

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = '/cvmfs/cms.cern.ch/slc6_amd64_gcc700/cms/cmssw/CMSSW_10_2_1/src/PhysicsTools/Utilities/configuration/copyPickMerge_cfg.py'
config.JobType.pyCfgParams = ['eventsToProcess_load=evtlist.txt', 'outputFile={outputFileName}']

config.Data.inputDataset = '{dataset}'

config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
config.Data.unitsPerJob = 5
config.Data.lumiMask = 'tmp.json'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()

config.Site.storageSite = "T2_CH_CERN"
'''.format(requestName=requestName,outputFileName=outputFileName,dataset=dataset)

open('PickEventCrabConfig.py', 'wt').write(crabcfg)

os.system('crab submit -c PickEventCrabConfig.py')
os.system('rm PickEventCrabConfig.py tmp.json evtlist.txt')



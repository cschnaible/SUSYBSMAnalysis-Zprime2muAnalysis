import os
import ROOT as R
R.gROOT.SetBatch(True)
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples
import argparse
parser = argparse.ArgumentParser(description='Submit CRAB job to pick out specific event')
parser.add_argument('-r','--run',default=318877,type=int,help='Run number')
parser.add_argument('-l','--lumi',default=102,type=int,help='Lumi number')
parser.add_argument('-e','--event',default=151594226,type=int,help='Event number')
parser.add_argument('-mc',default=None,help='MC sample to pick events from')
parser.add_argument('--extra',default='')
args = parser.parse_args()

requestName = 'event_'+str(args.run)+'_'+str(args.lumi)+'_'+str(args.event)
requestName += ('_'+args.mc if args.mc is not None else '')
requestName += ('_'+args.extra if args.extra else '')
outputFileName = requestName+'.root'

if args.mc: 
    samples = [sample for sample in samples if sample.name==args.mc]
    if len(samples)!=1:
        raise ValueError('Check MC:',args.mc)
    sample = samples[0]

if args.mc is None:
    if   315252 <= args.run <= 316995:
        dataset = '/SingleMuon/Run2018A-17Sep2018-v2/MINIAOD'
    elif 316998 <= args.run <= 319312:
        dataset = '/SingleMuon/Run2018B-17Sep2018-v1/MINIAOD'
    elif 319313 <= args.run <= 320393:
        dataset = '/SingleMuon/Run2018C-17Sep2018-v1/MINIAOD'
    elif 320394 <= args.run <= 325273:
        dataset = '/SingleMuon/Run2018D-22Jan2019-v2/MINIAOD'
    else:
        raise ValueError('Check the run number:',args.run)
else:
    dataset = sample.dataset

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
config.JobType.psetName = '/cvmfs/cms.cern.ch/slc7_amd64_gcc700/cms/cmssw/CMSSW_10_2_1/src/PhysicsTools/Utilities/configuration/copyPickMerge_cfg.py'
config.JobType.pyCfgParams = ['eventsToProcess_load=evtlist.txt', 'outputFile={outputFileName}']
config.JobType.allowUndistributedCMSSW = True

config.Data.inputDataset = '{dataset}'
config.Data.publication = False
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5
config.Data.lumiMask = 'tmp.json'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()

config.Site.storageSite = "T2_CH_CERN"
'''.format(requestName=requestName,outputFileName=outputFileName,dataset=dataset)

open('PickEventCrabConfig.py', 'wt').write(crabcfg)

os.system('crab submit -c PickEventCrabConfig.py')
os.system('rm PickEventCrabConfig.py tmp.json evtlist.txt')

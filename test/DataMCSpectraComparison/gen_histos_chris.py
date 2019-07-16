ex = '20190613_3'
is2016=False
is2017=True
is2018=False

import sys, os, FWCore.ParameterSet.Config as cms
process = cms.Process('Zprime2muAnalysis')
process.TFileService = cms.Service('TFileService', fileName=cms.string('gen_zp2mu_histos.root'))
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('TrackingTools.TransientTrack.TransientTrackBuilder_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
from SUSYBSMAnalysis.Zprime2muAnalysis.MCSamples import samples18, samples17, samples16

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxEvents.input = 1000
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000 # default 1000
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:doesnotexist.root'))
process.source.fileNames = [
        # 2016
        #'/store/data/Run2016C/SingleMuon/MINIAOD/17Jul2018-v1/20000/FEC97F81-0097-E811-A7B9-90E2BACC5EEC.root',
        #'/store/data/Run2016C/SingleMuon/MINIAOD/17Jul2018-v1/20000/FEA9FE48-3997-E811-8BB3-C0BFC0E5682E.root',
        #'/store/data/Run2016G/SingleMuon/MINIAOD/17Jul2018-v1/00000/1A12A529-4490-E811-8ED1-008CFAFBDC0E.root',
        #'/store/mc/RunIISummer16MiniAODv2/ZToMuMu_NNPDF30_13TeV-powheg_M_50_120/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/701163A6-D5CF-E611-84D2-001E674FAF23.root',
        # 2017
        #'/store/mc/RunIIFall17MiniAODv2/ZToMuMu_NNPDF31_13TeV-powheg_M_6000_Inf/MINIAODSIM/MUOTrackFix_12Apr2018_94X_mc2017_realistic_v14_ext1-v1/90000/0CFF28F9-56FF-E811-B62B-AC1F6B0DE3E8.root',
        #'/store/data/Run2017D/SingleMuon/MINIAOD/31Mar2018-v1/00000/04C38E6C-BF39-E811-9FA7-0CC47A4DEF06.root',
        '/store/mc/RunIIFall17MiniAODv2/TTToLL_MLL_800To1200_NNPDF31_13TeV-powheg/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/260000/F02C1E88-D26A-E911-A2B0-0242AC130002.root',
        # 2018
    #'/store/data/Run2018D/SingleMuon/MINIAOD/PromptReco-v2/000/322/068/00000/F8DCA3B9-41B0-E811-8B23-FA163E279E4C.root'
    #'/store/data/Run2018A/SingleMuon/MINIAOD/17Sep2018-v2/270000/40BFE1A5-BEFE-B34B-8836-4ADDB8966C78.root',
    #'/store/mc/RunIIAutumn18MiniAOD/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/90000/DD89AFA9-BD25-F346-939F-A9CC68A04B84.root',
    #'/store/mc/RunIIAutumn18MiniAOD/ZToMuMu_NNPDF31_13TeV-powheg_M_50_120/MINIAODSIM/102X_upgrade2018_realistic_v15-v2/120000/078DB2B1-40DD-634D-A3CF-D2E377CAFA48.root'
    #'/store/mc/RunIIAutumn18MiniAOD/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/102X_upgrade2018_realistic_v15-v1/120000/8A620F3F-201E-7245-94DF-A9966919C1BD.root',
           ]
if is2016:
    MCGT = '94X_mcRun2_asymptotic_v3'
    samples = samples16
    ex = '2016_'+ex
elif is2017:
    MCGT = '94X_mc2017_realistic_v17'
    samples = samples17
    ex = '2017_'+ex
elif is2018:
    MCGT = '102X_upgrade2018_realistic_v18'
    samples = samples18
    ex = '2018_'+ex

process.GlobalTag.globaltag = MCGT

from SUSYBSMAnalysis.Zprime2muAnalysis.HardInteraction_cff import hardInteraction_MiniAOD, hardInteraction
isDY = False
process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
obj = process.prunedMCLeptons
obj.src = cms.InputTag('prunedGenParticles')
process.hardInteractionNtuple = cms.EDAnalyzer('HardInteractionNtuple',
        hardInteraction = hardInteraction_MiniAOD,
        genEventInfo = cms.untracked.InputTag('generator'),
        isDY = cms.bool(isDY)
        )

process.path = cms.Path(obj* process.hardInteractionNtuple)

dyList = ['dy50to120','dy120to200','dy200to400','dy400to800','dy800to1400','dy1400to2300','dy2300to3500','dy3500to4500','dy4500to6000','dy6000toInf']
mcList = ['WW_50to200','WW_200to600','WW_600to1200_v1','WW_600to1200_v2','WW_600to1200_v3','WW_1200to2500','WW_2500toInf','WW_600to1200']
mcList += ['ttbar_lep_50to500','ttbar_lep_500to800','ttbar_lep_500to800_0to20','ttbar_lep_500to800_41to65','ttbar_lep_800to1200','ttbar_lep_1200to1800','ttbar_lep_1800toInf']

def apply_gen_filters(process,sampleName):
    from SUSYBSMAnalysis.Zprime2muAnalysis.MCFilters_cfi import DYPtZskim, TTbarGenMassFilter, DibosonGenMassFilter, TauTauFilter
    addFilter = False
    process.load('SUSYBSMAnalysis.Zprime2muAnalysis.PrunedMCLeptons_cfi')
    if ('dy50to120' in sampleName or 'dyInclusive' in sampleName) and ZSkim:
        mcFilter = DYPtZskim.clone()
        addFilter = True
    elif 'ttbar_lep_50to500' in sampleName:
        mcFilter = TTbarGenMassFilter.clone()
        addFilter = True
    elif 'WW_50to200' in sampleName:
        mcFilter = DibosonGenMassFilter.clone()
        addFilter = True
    elif 'dyTauTau' in sampleName:
        mcFilter = TauTauFilter.clone()
        addFilter = True
    if addFilter:
        setattr(process,sampleName+'Filter',mcFilter)
        mcFilterPath = getattr(process,sampleName+'Filter')
        for path_name, path in process.paths.iteritems():
            getattr(process,path_name).insert(0,mcFilterPath)

if __name__ == '__main__' and 'submit' in sys.argv:
    just_testing = 'testing' in sys.argv
    crab_cfg = '''
from CRABClient.UserUtilities import config,getUsernameFromSiteDB
config = config()
config.General.requestName = 'ana_genmc_%(name)s%(extra)s'
config.General.workArea = 'crab'
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'gen_histos_crab.py'   
config.JobType.allowUndistributedCMSSW = True
config.Data.inputDataset =  '%(ana_dataset)s'
config.Data.inputDBS = 'global'
config.Data.publication = False
config.Data.splitting = 'EventAwareLumiBased'
config.Data.totalUnits = -1
config.Data.unitsPerJob  = %(neventsperjob)s
config.Data.outputDatasetTag = 'ana_genmc_%(name)s%(extra)s'
config.Data.outLFNDirBase = '/store/user/'+getUsernameFromSiteDB()
config.Site.storageSite = 'T2_CH_CERN'
'''
    extra = '_'+ex if ex!='' else ''
   
    for sample in samples:
        name = sample.name
        ana_dataset = sample.dataset
        if name not in mcList: continue
        #print name, ana_dataset

        new_py = open('gen_histos_chris.py').read()
        new_py += "\napply_gen_filters(process,\"%(name)s\")\n"%locals()
        open('gen_histos_crab.py', 'wt').write(new_py)
        if name=='ttbar_lep_50to500' or name=='WW_50to200' or name=='WW_200to600': 
            neventsperjob = 100000
        else:
            neventsperjob = 10000
        print name,ana_dataset
        print sample.nevents,neventsperjob,sample.nevents/float(neventsperjob)

        open('crabConfig.py', 'wt').write(crab_cfg % locals())
        if not just_testing:
            os.system('crab submit -c crabConfig.py')
        else:
            os.system('crab submit -c crabConfig.py --dryrun')
            #cmd = 'diff histos.py histos_crab.py | less'
            #print cmd
            #os.system(cmd)
            #cmd = 'less crabConfig.py'
            #print cmd
            #os.system(cmd)

    if not just_testing:
        os.system('rm crabConfig.py gen_histos_crab.py gen_histos_crab.pyc')

